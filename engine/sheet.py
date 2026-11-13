#!/usr/bin/env python3
"""sheet.py · a session JSON becomes one A4 (or Letter) page: HTML, then PDF.

Usage (from the repo root):
    python3 engine/sheet.py <session.json>          writes .html and .pdf beside the json
    python3 engine/sheet.py clock <session.json>    prints the minutes of every block

The clock counts every rest (carried from Adam's trainer, 11 nov 2026):
  straight sets  : sum of sets x (work + rest), minus the very last rest
  superset       : per round, the work of each move + 15 s between moves + the rest after the round
  timed formats  : the minutes of the format (emom, amrap, fortime, intervals, run, warmup)
  every block after the warm-up adds a 60 s changeover
It REFUSES (exit code 2) a sheet more than 3 minutes over the minutes asked for.

PDF, in order: Playwright if it is already installed (Python, then Node) · a Chromium-family browser
already installed (Chrome, Edge, Chromium, Brave) in headless print mode · engine/minipdf.py (standard library).
Nothing is ever installed.
"""
import html, json, os, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
CHANGEOVER = 60
SUPERSET_GAP = 15
TOLERANCE = 180
DD = "-" * 2          # the command line flag prefix, spelled this way on purpose (house style)

LABELS = {
    "en": {"score": "Score to beat", "why": "Why this session", "sets": "Sets x reps", "load": "Load",
           "effort": "Effort", "rest": "Rest", "total": "Total", "min": "min", "log": "After the session, write down",
           "low": "If your energy drops", "first": "First time: find your weight", "done": "Done",
           "footer": "General guidance, not medical advice. Stop if anything feels wrong: sharp pain, chest pain, dizziness.",
           "rest_none": "none", "block": "Block", "week": "week", "week_of": "week %s of %s", "demo": "how to"},
    "fr": {"score": "Le score à battre", "why": "Pourquoi cette séance", "sets": "Séries x reps", "load": "Charge",
           "effort": "Effort", "rest": "Repos", "total": "Total", "min": "min", "log": "Après la séance, note",
           "low": "Si l'énergie baisse", "first": "Première fois : trouve ta charge", "done": "Fait",
           "footer": "Conseils généraux, pas un avis médical. Arrête si quelque chose ne va pas : douleur vive, douleur thoracique, vertige.",
           "rest_none": "aucun", "block": "Bloc", "week": "semaine", "week_of": "semaine %s sur %s", "demo": "démo"},
    "es": {"score": "La marca a batir", "why": "Por qué esta sesión", "sets": "Series x reps", "load": "Carga",
           "effort": "Esfuerzo", "rest": "Descanso", "total": "Total", "min": "min", "log": "Después de la sesión, anota",
           "low": "Si te falta energía", "first": "Primera vez: encuentra tu peso", "done": "Hecho",
           "footer": "Orientación general, no consejo médico. Para si algo va mal: dolor agudo, dolor en el pecho, mareo.",
           "rest_none": "ninguno", "block": "Bloque", "week": "semana", "demo": "cómo"},
    "de": {"score": "Das Ziel", "why": "Warum diese Einheit", "sets": "Sätze x Wdh", "load": "Last",
           "effort": "Anstrengung", "rest": "Pause", "total": "Gesamt", "min": "Min", "log": "Nach dem Training notieren",
           "low": "Wenn die Energie fehlt", "first": "Erstes Mal: finde dein Gewicht", "done": "Erledigt",
           "footer": "Allgemeine Hinweise, keine medizinische Beratung. Hör auf, wenn sich etwas falsch anfühlt.",
           "rest_none": "keine", "block": "Block", "week": "Woche", "demo": "so geht's"},
    "it": {"score": "Il risultato da battere", "why": "Perché questa seduta", "sets": "Serie x rip", "load": "Carico",
           "effort": "Sforzo", "rest": "Recupero", "total": "Totale", "min": "min", "log": "Dopo la seduta, annota",
           "low": "Se l'energia cala", "first": "Prima volta: trova il tuo peso", "done": "Fatto",
           "footer": "Indicazioni generali, non un parere medico. Fermati se qualcosa non va.",
           "rest_none": "nessuno", "block": "Blocco", "week": "settimana", "demo": "come"},
    "pt": {"score": "A marca a bater", "why": "Porquê esta sessão", "sets": "Séries x reps", "load": "Carga",
           "effort": "Esforço", "rest": "Descanso", "total": "Total", "min": "min", "log": "Depois da sessão, anota",
           "low": "Se a energia baixar", "first": "Primeira vez: encontra o teu peso", "done": "Feito",
           "footer": "Orientação geral, não é conselho médico. Para se algo parecer errado.",
           "rest_none": "nenhum", "block": "Bloco", "week": "semana", "demo": "como"},
}


# · the clock

def secs(v):
    """Seconds from 90, "90", "90s", "1:30", "2min"."""
    if v in (None, ""):
        return 0
    if isinstance(v, (int, float)):
        return int(v)
    t = str(v).strip().lower()
    if ":" in t:
        m, s_ = t.split(":", 1)
        return int(re.sub(r"\D", "", m) or 0) * 60 + int(re.sub(r"\D", "", s_) or 0)
    n = float(re.sub(r"[^\d.]", "", t) or 0)
    return int(n * 60) if "min" in t else int(n)


def work_s(it):
    if it.get("work"):
        return secs(it["work"])
    r = str(it.get("reps", "")).lower()
    m = re.search(r"(\d+)\s*min", r)
    if m:
        return int(m.group(1)) * 60
    m = re.search(r"(\d+)\s*s\b", r)
    if m:
        return int(m.group(1))
    if re.search(r"\d\s*(m|cal|km)\b", r):
        return 45
    nums = [int(n) for n in re.findall(r"\d+", r)]
    reps = max(nums) if nums else 8
    if "side" in r or "each" in r or "/ side" in r:
        reps *= 2
    return max(15, reps * 4)


def block_seconds(b):
    fmt = b.get("format", "straight")
    items = [i for i in b.get("items", []) if not i.get("paired")]
    if b.get("minutes"):
        return int(b["minutes"] * 60)
    if fmt in ("superset", "circuit"):
        rounds = max([int(i.get("sets") or 1) for i in items] or [1])
        total = 0
        for r in range(rounds):
            live = [i for i in items if int(i.get("sets") or 1) > r]
            total += sum(work_s(i) for i in live) + SUPERSET_GAP * max(0, len(live) - 1)
            if r < rounds - 1:
                total += secs(b.get("rest_after_round", 90))
        return total
    total = 0
    for idx, it in enumerate(items):
        n = int(it.get("sets") or 1)
        total += n * (work_s(it) + secs(it.get("rest")))
    if items:
        total -= secs(items[-1].get("rest"))
    return max(total, 0)


def session_seconds(s):
    total = 0
    for i, b in enumerate(s.get("blocks", [])):
        lead = secs(b["lead_rest"]) if b.get("lead_rest") else (CHANGEOVER if i > 0 else 0)
        total += block_seconds(b) + lead
    return total


def fmt_rest(s, none="none"):
    if s is None or s == "":
        return ""
    s = secs(s)
    if s == 0:
        return none
    return "%d:%02d" % (s // 60, s % 60)


# · the page

CSS_FILE = HERE / "theme" / "sheet.css"


def esc(x):
    return html.escape(str(x if x is not None else ""))


FORM_LABELS = {
    "en": {"warmup": "Warm-up", "cooldown": "Cool-down", "hard": "How hard", "hard_scale": "1 easy · 5 max",
           "reps": "reps", "set": "set", "time": "time or rounds", "minutes_done": "minutes done", "notes": "Notes",
           "notes_hint": "How did it feel? Any pain (where, 0 to 10)?", "tell": "Tell the trainer",
           "cool_walk": "Easy walk or slow cycling, then breathe slowly", "cool_walk_reps": "2 to 3 min", "date": "Date"},
    "fr": {"warmup": "Échauffement", "cooldown": "Retour au calme", "hard": "Difficulté", "hard_scale": "1 facile · 5 max",
           "reps": "reps", "set": "série", "time": "temps ou tours", "minutes_done": "minutes faites", "notes": "Notes",
           "notes_hint": "Comment c'était ? Une douleur (où, de 0 à 10) ?", "tell": "À dire au coach",
           "cool_walk": "Marche ou vélo tranquille, puis respire lentement", "cool_walk_reps": "2 à 3 min", "date": "Date"},
    "es": {"warmup": "Calentamiento", "cooldown": "Vuelta a la calma", "hard": "Dureza", "hard_scale": "1 fácil · 5 máx",
           "reps": "reps", "set": "serie", "time": "tiempo o rondas", "minutes_done": "minutos hechos", "notes": "Notas",
           "notes_hint": "¿Cómo fue? ¿Algún dolor (dónde, de 0 a 10)?", "tell": "Cuéntale al entrenador",
           "cool_walk": "Camina o pedalea suave, luego respira despacio", "cool_walk_reps": "2 a 3 min", "date": "Fecha"},
    "de": {"warmup": "Aufwärmen", "cooldown": "Cool-down", "hard": "Wie hart", "hard_scale": "1 leicht · 5 max",
           "reps": "Wdh", "set": "Satz", "time": "Zeit oder Runden", "minutes_done": "Minuten", "notes": "Notizen",
           "notes_hint": "Wie war es? Schmerzen (wo, 0 bis 10)?", "tell": "Für den Trainer",
           "cool_walk": "Locker gehen oder radeln, dann ruhig atmen", "cool_walk_reps": "2 bis 3 Min", "date": "Datum"},
    "it": {"warmup": "Riscaldamento", "cooldown": "Defaticamento", "hard": "Fatica", "hard_scale": "1 facile · 5 max",
           "reps": "rip", "set": "serie", "time": "tempo o giri", "minutes_done": "minuti fatti", "notes": "Note",
           "notes_hint": "Com'è andata? Dolore (dove, da 0 a 10)?", "tell": "Da dire al coach",
           "cool_walk": "Cammina o pedala piano, poi respira lentamente", "cool_walk_reps": "2 o 3 min", "date": "Data"},
    "pt": {"warmup": "Aquecimento", "cooldown": "Retorno à calma", "hard": "Esforço", "hard_scale": "1 fácil · 5 máx",
           "reps": "reps", "set": "série", "time": "tempo ou voltas", "minutes_done": "minutos feitos", "notes": "Notas",
           "notes_hint": "Como correu? Alguma dor (onde, de 0 a 10)?", "tell": "Diz ao treinador",
           "cool_walk": "Caminha ou pedala devagar, depois respira com calma", "cool_walk_reps": "2 a 3 min", "date": "Data"},
}
for _k, _v in FORM_LABELS.items():
    LABELS.setdefault(_k, {}).update(_v)

NOT_LOADABLE = {"bodyweight", "band", "time", "distance", "calories"}
TIMED_FORMATS = {"fortime", "amrap", "emom", "intervals", "run"}


def labels_for(s):
    lang = s.get("language", "en")
    L = dict(LABELS["en"])
    L.update(LABELS.get(lang, {}))
    L.update(s.get("labels") or {})
    return L


def _role(b):
    name = str(b.get("name", "")).lower()
    if b.get("kind") == "warmup":
        return "warmup"
    if b.get("_module") == "mobility" or "mobility" in name or "cool" in name or "stretch" in name:
        return "cooldown"
    return "work"


def form(s):
    """The workout form, one model for the HTML sheet and the stdlib PDF, so both are the same design.

    Sections in order: the warm-up, the work, the cool-down. A row is a checklist line (warm-up and
    cool-down), a set row (one cell per set: the weight used when the move is loaded, the reps done, a
    tick) or a score row (one cell: time or rounds for a timed piece, minutes for a run).
    The sheet never invents work: when the engine built no cool-down, the cool-down is one easy line
    (walk it off), outside the clock."""
    L = labels_for(s)
    unit = s.get("units", "kg")
    firsts, total, secs_by = [], 0, []
    for i, b in enumerate(s.get("blocks", [])):
        sec = block_seconds(b) + (secs(b["lead_rest"]) if b.get("lead_rest") else (CHANGEOVER if i > 0 else 0))
        total += sec
        secs_by.append(sec)
    warm, work, cool = [], [], []
    for i, b in enumerate(s.get("blocks", [])):
        role = _role(b)
        timed = b.get("format") in ("superset", "circuit")
        rows = []
        for it in b.get("items", []):
            sl = it.get("_slot") or {}
            fo = it.get("first_outing")
            if fo and fo not in firsts:
                firsts.append(fo)
            sets = it.get("sets")
            reps = it.get("reps")
            many = sets and reps and role == "work" and int(sets or 1) > 1
            target = ("%s × %s" % (sets, reps)) if many else str(reps or (sets or ""))
            row = {"name": it.get("name") or it.get("ex"), "cue": it.get("cue", ""), "target": target,
                   "load": it.get("load", ""), "effort": it.get("effort", ""), "demo": it.get("demo"),
                   "rest": fmt_rest(it.get("rest")) if not timed and many and secs(it.get("rest")) else "",
                   "star": (firsts.index(fo) + 1) if fo else 0}
            lt = sl.get("load_type")
            if role != "work":
                row["kind"] = "check"
            elif sl.get("rule") in ("run_volume", "c25k_week"):
                row.update(kind="score", cell=L["minutes_done"])
            elif it.get("work") or sl.get("rule") == "benchmark" or b.get("format") in TIMED_FORMATS:
                row.update(kind="score", cell=L["time"])
            else:
                loaded = (lt not in NOT_LOADABLE) if lt else bool(re.search(r"\d\s*(kg|lb)", str(it.get("load", ""))))
                row.update(kind="sets", n=max(1, min(int(sets or 1), 10)), weight=unit if loaded else None)
            rows.append(row)
        sec = {"title": b.get("name", ""), "minutes": round(secs_by[i] / 60), "note": b.get("rest_note", ""),
               "role": role, "main": b.get("kind") == "main", "rows": rows}
        {"warmup": warm, "work": work, "cooldown": cool}[role].append(sec)
    if not cool:
        cool = [{"title": L["cooldown"], "minutes": None, "note": "", "role": "cooldown", "main": False, "added": True,
                 "rows": [{"name": L["cool_walk"], "cue": "", "target": L["cool_walk_reps"], "kind": "check", "star": 0}]}]
    for sec_ in warm:
        sec_["title"] = L["warmup"] if str(sec_["title"]).lower() in ("warm-up", "warm up") else sec_["title"]
    week = ""
    if s.get("week") and s.get("weeks"):              # "week 2 of 6": never a block number, never a method name
        week = L.get("week_of", L["week"] + " %s / %s") % (min(int(s["week"]), int(s["weeks"])), s["weeks"])
    elif s.get("week"):
        week = "%s %s" % (L["week"], s["week"])
    meta = " · ".join(x for x in [s.get("program_name"), week, s.get("level_text")] if x)
    return {"L": L, "title": s.get("title", ""), "date": s.get("date", ""), "meta": meta, "minutes": round(total / 60),
            "beat": s.get("score_to_beat", ""), "why": s.get("why", ""), "firsts": firsts, "unit": unit,
            "sections": warm + work + cool, "low": s.get("low_energy", ""), "log": s.get("log") or [],
            "footer": L["footer"] + ((" · " + s["notes"]) if s.get("notes") else "")}


def render_html(s):
    f = form(s)
    L = f["L"]
    css = CSS_FILE.read_text(encoding="utf-8") if CSS_FILE.exists() else ""
    paper = "letter" if s.get("paper", "A4").lower().startswith("letter") else "A4"
    lang = s.get("language", "en")
    out = ['<!doctype html><html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<title>%s</title>' % (esc(lang), esc(f["title"])),
           '<style>@page{size:%s;margin:11mm}%s</style></head><body><main class="sheet">' % (paper, css)]
    out.append('<header><div class="hl"><div class="brand"><span class="mark"></span>Personal trainer</div><h1>%s</h1>'
               '<p class="meta">%s</p></div><div class="hr"><div class="when">%s</div><div class="mins"><b>%d</b> %s</div></div></header>'
               % (esc(f["title"]), esc(f["meta"]), esc(f["date"]), f["minutes"], esc(L["min"])))
    top = []
    if f["beat"]:
        top.append('<div class="beat"><b>%s</b><span>%s</span></div>' % (esc(L["score"]), esc(f["beat"])))
    if f["why"]:
        top.append('<div class="why"><b>%s</b><span>%s</span></div>' % (esc(L["why"]), esc(f["why"])))
    out.append('<section class="top">%s</section>' % "".join(top))
    if f["firsts"]:
        legend = "".join('<div><span class="star">%s</span> %s</div>' % ("&#9733;" * (i + 1), esc(x)) for i, x in enumerate(f["firsts"]))
        out.append('<section class="firsts"><b>%s</b>%s</section>' % (esc(L["first"]), legend))
    for sec in f["sections"]:
        mins = ('%d %s' % (sec["minutes"], esc(L["min"]))) if sec.get("minutes") is not None else ""
        head = '<div class="sh"><h2>%s</h2><span class="sm">%s%s</span></div>' % (
            esc(sec["title"]), (esc(sec["note"]) + " · ") if sec.get("note") and mins else esc(sec.get("note") or ""), mins)
        rows = []
        for r in sec["rows"]:
            name = esc(r["name"])
            if r.get("demo"):
                name = '<a href="%s">%s</a>' % (esc(r["demo"]), name)
            star = (' <span class="star">%s</span>' % ("&#9733;" * r["star"])) if r.get("star") else ""
            if r["kind"] == "check":
                rows.append('<div class="chk"><i class="tick"></i><span class="n">%s%s</span><span class="num">%s</span>'
                            '<span class="cue">%s</span></div>' % (name, star, esc(r["target"]), esc(r.get("cue"))))
                continue
            tgt = " · ".join(x for x in [esc(r["target"]), esc(r.get("load")), (esc(L["rest"]).lower() + " " + esc(r["rest"])) if r.get("rest") else ""] if x)
            left = ('<div class="ex"><div class="n">%s%s</div><div class="num tgt">%s</div><div class="ef">%s</div><div class="cue">%s</div></div>'
                    % (name, star, tgt, esc(r.get("effort")), esc(r.get("cue"))))
            if r["kind"] == "score":
                cells = '<div class="cell wide"><span class="lab">%s</span><i class="tick"></i></div>' % esc(r["cell"])
            else:
                cells = "".join('<div class="cell%s"><span class="lab"><em>%d</em>%s%s</span><i class="tick"></i></div>' % (
                    " two" if r.get("weight") else "", k + 1, ('<span>%s</span>' % esc(r["weight"])) if r.get("weight") else "",
                    '<span>%s</span>' % esc(L["reps"]))
                    for k in range(r["n"]))
            hard = '<div class="hard"><span class="lab">%s</span><div class="dots">%s</div></div>' % (
                esc(L["hard"]), "".join('<i>%d</i>' % k for k in range(1, 6)))
            rows.append('<div class="row">%s<div class="cells">%s</div>%s</div>' % (left, cells, hard))
        out.append('<section class="sec %s%s">%s%s</section>' % (sec["role"], " main" if sec.get("main") else "", head, "".join(rows)))
    tell = " · ".join(esc(x) for x in f["log"])
    out.append('<section class="notes"><div class="nh"><h2>%s</h2><span>%s</span></div><div class="lines"><em></em><em></em><em></em></div>'
               '<p class="tell"><b>%s</b> %s</p>%s</section>' % (
                   esc(L["notes"]), esc(L["notes_hint"]), esc(L["tell"]), tell,
                   ('<p class="low"><b>%s</b> %s</p>' % (esc(L["low"]), esc(f["low"]))) if f["low"] else ""))
    out.append('<footer>%s</footer></main></body></html>' % esc(f["footer"]))
    return "\n".join(out)


# · the pdf

BROWSERS = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "brave-browser",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]


def find_browser():
    for b in BROWSERS:
        p = shutil.which(b) if not os.path.isabs(b) else (b if os.path.exists(b) else None)
        if p:
            return p
    return None


def pdf_browser(h, p):
    exe = find_browser()
    if not exe:
        return False
    with tempfile.TemporaryDirectory() as prof:
        cmd = [exe, DD + "headless", DD + "disable-gpu", DD + "no-sandbox", DD + "no-pdf-header-footer", DD + "no-first-run",
               DD + "disable-background-networking", DD + "disable-component-update",
               DD + "user-data-dir=" + prof, DD + "print-to-pdf=" + str(p), pathlib.Path(h).resolve().as_uri()]
        try:
            subprocess.run(cmd, capture_output=True, timeout=45)
        except Exception:
            return False
    return p.exists() and p.stat().st_size > 1000


def pdf_playwright(h, p):
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return False
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            pg = br.new_page()
            pg.goto(pathlib.Path(h).resolve().as_uri())
            pg.pdf(path=str(p), prefer_css_page_size=True, print_background=True)
            br.close()
        return p.exists()
    except Exception:
        return False


NODE_JS = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
           "await p.goto(process.argv[1]);await p.pdf({path:process.argv[2],preferCSSPageSize:true,printBackground:true});"
           "await b.close();})().catch(e=>{console.error(e);process.exit(1)})")


def pdf_node(h, p):
    if not shutil.which("node"):
        return False
    try:
        r = subprocess.run(["node", "-e", NODE_JS, pathlib.Path(h).resolve().as_uri(), str(p)], capture_output=True, timeout=90)
    except Exception:
        return False
    return r.returncode == 0 and p.exists()


def render_pdf(h, p):
    return pdf_playwright(h, p) or pdf_node(h, p) or pdf_browser(h, p)


def pdf_pages(p):
    try:
        return len(re.findall(rb"/Type\s*/Page[^s]", p.read_bytes()))
    except Exception:
        return 0


def make_pdf(s, h, p):
    if render_pdf(h, p):
        base = render_html(s).replace('<main class="sheet">', '<main class="sheet tight">')
        for zoom in (None, 0.92, 0.85, 0.78, 0.72, 0.66, 0.6, 0.55):      # shrink the type in steps, never cut content
            if pdf_pages(p) <= 1:
                break
            html_ = base if zoom is None else base.replace("</style>", ".sheet{zoom:%s}</style>" % zoom, 1)
            h.write_text(html_, encoding="utf-8")
            render_pdf(h, p)
        return "browser"
    import minipdf
    minipdf.write(s, p, labels_for(s))
    return "minipdf"


def outputs(jpath):
    jpath = pathlib.Path(jpath)
    return jpath.with_suffix(".html"), jpath.with_suffix(".pdf")


def render_file(jpath):
    """Render one session file. Returns a dict; "refused" is set when the clock is over."""
    jpath = pathlib.Path(jpath)
    s = json.loads(jpath.read_text(encoding="utf-8"))
    total = session_seconds(s)
    asked = int(s.get("minutes") or 60) * 60
    if total > asked + TOLERANCE:
        return {"refused": True, "minutes": round(total / 60), "asked": asked // 60,
                "message": "REFUSED: the session takes %d min with every rest counted, you asked for %d. Cut in the order of "
                           "doctrine/06_BUILD.md and run again." % (round(total / 60), asked // 60)}
    h, p = outputs(jpath)
    h.write_text(render_html(s), encoding="utf-8")
    how = make_pdf(s, h, p)
    return {"html": str(h), "pdf": str(p), "minutes": round(total / 60), "renderer": how, "pages": pdf_pages(p)}


def main(argv):
    if len(argv) >= 2 and argv[0] == "clock":
        s = json.loads(pathlib.Path(argv[1]).read_text(encoding="utf-8"))
        for i, b in enumerate(s["blocks"]):
            print("%-28s %5.1f min" % (b.get("name"), block_seconds(b) / 60))
        print("total %.1f min (asked %s)" % (session_seconds(s) / 60, s.get("minutes")))
        return 0
    if not argv:
        print(__doc__)
        return 1
    r = render_file(argv[0])
    print(json.dumps(r, ensure_ascii=False))
    return 2 if r.get("refused") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
