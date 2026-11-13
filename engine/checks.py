#!/usr/bin/env python3
"""checks.py · the gate before every commit, and the template's CI.

    python3 engine/checks.py            the person's memory files (me/, sessions/)
    python3 engine/checks.py template   the whole template: programs, modules, bank, house style, no personal data
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import core, progress

REQUIRED_PROFILE = ["language", "units", "age_band", "goal", "experience", "days", "minutes", "places", "screen"]


def check_profile(p):
    errs = []
    for k in REQUIRED_PROFILE:
        if k not in p:
            errs.append("profile: missing '%s'" % k)
    if p.get("goal") not in core.GOALS:
        errs.append("profile: goal must be one of " + ", ".join(core.GOALS))
    if p.get("goal2") not in (None, "") and p.get("goal2") not in core.GOALS:
        errs.append("profile: goal2 must be one of the goals or empty")
    if p.get("experience") not in core.EXPERIENCE:
        errs.append("profile: experience must be one of " + ", ".join(core.EXPERIENCE))
    if p.get("age_band") not in core.AGE_BANDS:
        errs.append("profile: age_band must be one of " + ", ".join(core.AGE_BANDS))
    if not isinstance(p.get("days"), int) or not 1 <= p.get("days", 0) <= 7:
        errs.append("profile: days must be a whole number from 1 to 7")
    if not isinstance(p.get("minutes"), int) or not 10 <= p.get("minutes", 0) <= 180:
        errs.append("profile: minutes must be a whole number from 10 to 180")
    if p.get("units") not in ("kg", "lb"):
        errs.append("profile: units must be kg or lb")
    for name, pl in (p.get("places") or {}).items():
        for t in pl.get("equipment", []):
            if t not in core.PRESETS and t not in core.ALL_TAGS:
                errs.append("profile: unknown equipment '%s' at %s" % (t, name))
    if "no_fat_loss_goal" in (p.get("screen") or {}).get("flags", []) and "fat_loss" in (p.get("goal"), p.get("goal2")):
        errs.append("profile: fat loss is not offered after an eating disorder answer, pick health or strength")
    return errs


def check_data():
    errs = []
    prof = core.read_json_block(core.PROFILE) if core.PROFILE.exists() else None
    if prof:
        if prof.get("goal"):
            errs += check_profile(prof)
    pl = core.read_json_block(core.PLAN) if core.PLAN.exists() else None
    if pl:
        if not (core.PROGRAMS / (pl.get("program", "") + ".md")).exists():
            errs.append("plan: program '%s' has no file" % pl.get("program"))
    st = core.load_json(core.STATE)
    if st is not None:
        for k in ("program", "block", "week", "queue", "slots"):
            if k not in st:
                errs.append("state: missing '%s' (run: python3 engine/plan.py rebuild)" % k)
    for i, line in enumerate(core.LOG.read_text(encoding="utf-8").splitlines() if core.LOG.exists() else []):
        if line.strip():
            try:
                json.loads(line)
            except Exception:
                errs.append("log: line %d is not valid json" % (i + 1))
    return errs


def check_template():
    errs = []
    bank = core.load_bank()
    progs = core.all_programs()
    if len(progs) < 10:
        errs.append("programs: only %d found" % len(progs))

    def walk_session(owner, sid, s):
        for b in s.get("blocks", []):
            if b.get("kind") not in ("main", "secondary", "accessory", "finisher"):
                errs.append("%s %s: block kind '%s'" % (owner, sid, b.get("kind")))
            for sl in b.get("slots", []):
                if sl.get("kind") == "piece":
                    for pc in sl.get("pieces") or [sl.get("moves", [])]:
                        for mv in pc:
                            for i in mv.get("prefer", []):
                                if i not in bank:
                                    errs.append("%s %s: move id '%s' not in the bank" % (owner, sid, i))
                    continue
                if sl.get("rule") not in progress.RULES:
                    errs.append("%s %s: rule '%s' unknown" % (owner, sid, sl.get("rule")))
                for i in sl.get("prefer", []):
                    if i not in bank:
                        errs.append("%s %s: id '%s' not in the bank" % (owner, sid, i))
                    elif bank[i]["pattern"] != sl.get("pattern"):
                        errs.append("%s %s: '%s' is %s, slot says %s" % (owner, sid, i, bank[i]["pattern"], sl.get("pattern")))
                for k in ("key", "pattern", "sets", "reps", "rule"):
                    if k not in sl:
                        errs.append("%s %s: slot missing '%s'" % (owner, sid, k))

    for p in progs:
        pid = p.get("id")
        for k in ("id", "name", "family", "goals", "experience", "days", "minutes", "layouts", "sessions"):
            if k not in p:
                errs.append("%s: missing '%s'" % (pid, k))
        if set(p.get("goals", {})) != set(core.GOALS):
            errs.append("%s: goals must have exactly the 11 keys" % pid)
        for d in range(p["days"][0], p["days"][1] + 1):
            lay = p["layouts"].get(str(d))
            if lay is None:
                errs.append("%s: no layout for %d days" % (pid, d))
            for sid in lay or []:
                if sid not in p["sessions"]:
                    errs.append("%s: layout names a missing session '%s'" % (pid, sid))
        for sid, s in p["sessions"].items():
            walk_session(pid, sid, s)
        if p.get("express"):
            walk_session(pid, "express", p["express"])
        else:
            errs.append("%s: no express session" % pid)
    for f in sorted(core.MODULES.glob("*.md")):
        if f.name == "README.md":
            continue
        m = core.read_json_block(f)
        if not m:
            errs.append("module %s: no json block" % f.name)
            continue
        if m.get("session"):
            walk_session("module " + m["id"], "session", m["session"])
        for sid, s in (m.get("sessions") or {}).items():
            walk_session("module " + m["id"], sid, s)
    for r in bank.values():
        for k in ("easier", "harder"):
            if r[k] and (r[k] not in bank or bank[r[k]]["pattern"] != r["pattern"]):
                errs.append("bank %s: %s '%s' missing or another pattern" % (r["id"], k, r[k]))
    for f in core.ROOT.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".py", ".csv", ".json", ".css", ".html", ".yml") and ".git" not in f.parts:
            t = f.read_text(encoding="utf-8", errors="ignore")
            if "\u2014" in t or "\u2013" in t:
                errs.append("style: em or en dash in %s" % f.relative_to(core.ROOT))
            for ln, line in enumerate(t.splitlines(), 1):
                if re.search(r"(?<!-)-{2}(?!-)", line) and not re.match(r"^\|?[:\- |]+\|?$", line.strip()):
                    errs.append("style: double dash in %s line %d" % (f.relative_to(core.ROOT), ln))
    for f in ("PROFILE.md", "PLAN.md"):
        if core.read_json_block(core.ME / f):
            errs.append("template: me/%s holds data, the template must ship it empty" % f)
    if core.LOG.exists() and core.LOG.read_text().strip():
        errs.append("template: me/log.jsonl is not empty")
    if core.STATE.exists():
        errs.append("template: me/state.json must not ship")
    if [p for p in core.SESSIONS.glob("*") if p.name != "README.md"]:
        errs.append("template: sessions/ must ship empty")
    return errs


if __name__ == "__main__":
    errs = check_template() if sys.argv[1:] == ["template"] else check_data()
    for e in errs:
        print("FAIL", e)
    print("OK" if not errs else "%d problem(s)" % len(errs))
    sys.exit(1 if errs else 0)
