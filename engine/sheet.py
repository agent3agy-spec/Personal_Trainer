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
           "rest_none": "none", "block": "Block", "week": "week", "demo": "how to"},
    "fr": {"score": "Le score à battre", "why": "Pourquoi cette séance", "sets": "Séries x reps", "load": "Charge",
           "effort": "Effort", "rest": "Repos", "total": "Total", "min": "min", "log": "Après la séance, note",
           "low": "Si l'énergie baisse", "first": "Première fois : trouve ta charge", "done": "Fait",
           "footer": "Conseils généraux, pas un avis médical. Arrête si quelque chose ne va pas : douleur vive, douleur thoracique, vertige.",
           "rest_none": "aucun", "block": "Bloc", "week": "semaine", "demo": "démo"},
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


def render_html(s):
    lang = s.get("language", "en")
    L = dict(LABELS["en"])
    L.update(LABELS.get(lang, {}))
    L.update(s.get("labels") or {})
    css = CSS_FILE.read_text(encoding="utf-8") if CSS_FILE.exists() else ""
    paper = "letter" if s.get("paper", "A4").lower().startswith("letter") else "A4"
    out = ['<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s</title>' % (esc(lang), esc(s.get("title"))),
           '<style>@page{size:%s;margin:11mm}%s</style></head><body><main class="sheet">' % (paper, css)]
    meta = " · ".join(x for x in [s.get("date"), s.get("program_name"),
                                  ("%s %s · %s %s" % (L["block"], s.get("block"), L["week"], s.get("week"))) if s.get("block") else "",
                                  s.get("level_text")] if x)
    out.append('<header><div class="brand"><span class="mark"></span>Personal trainer</div>'
               '<h1>%s</h1><p class="meta">%s</p></header>' % (esc(s.get("title")), esc(meta)))
    top = []
    if s.get("score_to_beat"):
        top.append('<div class="beat"><b>%s</b><span>%s</span></div>' % (esc(L["score"]), esc(s["score_to_beat"])))
    if s.get("why"):
        top.append('<div class="why"><b>%s</b><span>%s</span></div>' % (esc(L["why"]), esc(s["why"])))
    out.append('<section class="top">%s</section>' % "".join(top))
    legend_at = len(out)
    total = 0
    firsts = []
    for i, b in enumerate(s.get("blocks", [])):
        sec = block_seconds(b) + (secs(b["lead_rest"]) if b.get("lead_rest") else (CHANGEOVER if i > 0 else 0))
        total += sec
        head = '<div class="bh"><h2>%s</h2><span class="bm">%d %s%s</span></div>' % (
            esc(b.get("name")), round(sec / 60), esc(L["min"]), (" · " + esc(b["rest_note"])) if b.get("rest_note") else "")
        rows = []
        for it in b.get("items", []):
            n = int(it.get("sets") or 1)
            boxes = "".join('<i></i>' for _ in range(min(n, 10)))
            demo = it.get("demo")
            name = esc(it.get("name") or it.get("ex"))
            if demo:
                name = '<a href="%s">%s</a>' % (esc(demo), name)
            star = ""
            if it.get("first_outing"):
                fo = it["first_outing"]
                if fo not in firsts:
                    firsts.append(fo)
                star = ' <span class="star">%s</span>' % ("&#9733;" * (firsts.index(fo) + 1))
            sets = it.get("sets")
            sr = ("%s x %s" % (sets, it.get("reps"))) if sets and it.get("reps") else (it.get("reps") or (str(sets) if sets else ""))
            rest = esc(fmt_rest(it.get("rest"), L["rest_none"])) if b.get("format") not in ("superset", "circuit") and it.get("sets") else ""
            rows.append('<tr><td class="ex"><div class="n">%s%s</div><div class="cue">%s</div></td>'
                        '<td class="sr">%s</td><td class="ld">%s</td><td class="ef">%s</td><td class="rs">%s</td><td class="bx">%s</td></tr>'
                        % (name, star, esc(it.get("cue")), esc(sr), esc(it.get("load", "")), esc(it.get("effort", "")), rest, boxes))
        cols = '<colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"><col class="c5"><col class="c6"></colgroup>'
        thead = '<tr><th></th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' % (
            esc(L["sets"]), esc(L["load"]), esc(L["effort"]), esc(L["rest"]), esc(L["done"]))
        out.append('<section class="block %s">%s<table>%s%s%s</table></section>' % (esc(b.get("kind", "")), head, cols, thead, "".join(rows)))
    if firsts:
        legend = "".join('<div><span class="star">%s</span> %s</div>' % ("&#9733;" * (i + 1), esc(f)) for i, f in enumerate(firsts))
        out.insert(legend_at, '<section class="firsts"><b>%s</b>%s</section>' % (esc(L["first"]), legend))
    foot = []
    if s.get("low_energy"):
        foot.append('<div class="low"><b>%s</b> %s</div>' % (esc(L["low"]), esc(s["low_energy"])))
    if s.get("log"):
        lines = "".join('<div class="ll"><span>%s</span><em></em></div>' % esc(x) for x in s["log"])
        foot.append('<div class="log"><b>%s</b>%s</div>' % (esc(L["log"]), lines))
    out.append('<section class="foot">%s<div class="total">%s <b>%d %s</b></div></section>' % (
        "".join(foot), esc(L["total"]), round(total / 60), esc(L["min"])))
    note = esc(L["footer"]) + ((" · " + esc(s["notes"])) if s.get("notes") else "")
    out.append('<footer>%s</footer></main></body></html>' % note)
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
        for zoom in (None, 0.92, 0.85, 0.78, 0.72):      # shrink the type in steps, never cut content
            if pdf_pages(p) <= 1:
                break
            html_ = base if zoom is None else base.replace("</style>", ".sheet{zoom:%s}</style>" % zoom, 1)
            h.write_text(html_, encoding="utf-8")
            render_pdf(h, p)
        return "browser"
    import minipdf
    minipdf.write(s, p, LABELS.get(s.get("language", "en"), LABELS["en"]))
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
