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
    lo, hi = core.MINUTES_RANGE
    if not isinstance(p.get("minutes"), int) or not lo <= p.get("minutes", 0) <= hi:
        errs.append("profile: minutes must be a whole number from %d to %d" % (lo, hi))
    if p.get("units") not in ("kg", "lb"):
        errs.append("profile: units must be kg or lb")
    for name, pl in (p.get("places") or {}).items():
        for t in pl.get("equipment", []):
            if t not in core.PRESETS and t not in core.ALL_TAGS:
                errs.append("profile: unknown equipment '%s' at %s" % (t, name))
        if not core.place_in_scope(pl.get("equipment", [])):
            errs.append("profile: %s is out of scope: a gym, a home gym with real kit (a barbell, dumbbells or a cardio "
                        "machine), or outdoors for running and cardio" % name)
    errs += check_interview(p)
    if "no_fat_loss_goal" in (p.get("screen") or {}).get("flags", []) and "fat_loss" in (p.get("goal"), p.get("goal2")):
        errs.append("profile: fat loss is not offered after an eating disorder answer, pick health or strength")
    return errs


def _one_of(errs, p, key, allowed):
    if p.get(key) not in (None, "") and p.get(key) not in allowed:
        errs.append("profile: %s must be one of %s" % (key, ", ".join(allowed)))


def _all_in(errs, p, key, allowed):
    v = p.get(key)
    if v is None:
        return
    if not isinstance(v, list) or [x for x in v if x not in allowed]:
        errs.append("profile: %s must be a list from %s" % (key, ", ".join(allowed)))


def check_interview(p):
    """The fields of the 13 nov interview (doctrine/02_INTERVIEW.md). All optional, all checked when present."""
    errs = []
    _one_of(errs, p, "mode", core.MODES)
    _one_of(errs, p, "outcome", list(core.OUTCOMES))
    if p.get("outcome") in core.OUTCOMES and p.get("outcome_detail") not in (None, ""):
        _one_of(errs, p, "outcome_detail", list(core.OUTCOMES[p["outcome"]]))
    bl = p.get("outcomes")
    if bl is not None:
        if not isinstance(bl, list) or not 1 <= len(bl) <= 3 or len({o.get("id") for o in bl if isinstance(o, dict)}) != len(bl) \
                or any(not isinstance(o, dict) or o.get("id") not in core.OUTCOMES or not isinstance(o.get("share"), (int, float))
                       or not 0 < o["share"] <= 1 for o in bl):
            errs.append("profile: outcomes is one to three different outcomes, each with a share above 0")
        elif abs(sum(o["share"] for o in bl) - 1) > 0.02:
            errs.append("profile: the shares of outcomes add up to 1")
    _all_in(errs, p, "done_before", core.ACTIVITIES)
    for k, v in (p.get("experience_by") or {}).items():
        if k not in core.ACTIVITIES or v not in core.EXPERIENCE:
            errs.append("profile: experience_by maps an activity (%s) to a level (%s)" % (", ".join(core.ACTIVITIES), ", ".join(core.EXPERIENCE)))
            break
    _all_in(errs, p, "enjoys", core.ENJOY)
    _all_in(errs, p, "avoids", core.ENJOY)
    _one_of(errs, p, "kit_pref", core.KIT_PREF)
    _one_of(errs, p, "style_pref", core.STYLES)
    _all_in(errs, p, "strengths", core.STRENGTHS)
    _all_in(errs, p, "barriers", core.BARRIERS)
    _one_of(errs, p, "sleep", core.SLEEP)
    _one_of(errs, p, "stress", core.STRESS)
    if p.get("units_confirmed") is not None and not isinstance(p["units_confirmed"], bool):
        errs.append("profile: units_confirmed is true or false")
    for lim in p.get("limits", []):
        if lim.get("region") not in core.REGIONS:
            errs.append("profile: a limit's region must be one of " + ", ".join(core.REGIONS))
        if lim.get("status") not in (None, "") and lim["status"] not in core.LIMIT_STATUS:
            errs.append("profile: a limit's status must be one of " + ", ".join(core.LIMIT_STATUS))
        if [t for t in lim.get("triggers") or [] if t not in core.TRIGGERS]:
            errs.append("profile: a limit's triggers come from " + ", ".join(core.TRIGGERS))
    for r in p.get("rejected", []):
        if not isinstance(r, dict) or r.get("reason") not in core.REJECT_REASONS:
            errs.append("profile: a 'not for me' needs a reason from " + ", ".join(core.REJECT_REASONS))
    rt = p.get("current_routine")
    if p.get("mode") == "improve":
        if not isinstance(rt, dict):
            errs.append("profile: improve mode needs current_routine")
        else:
            _one_of(errs, rt, "split", core.SPLITS)
            if not isinstance(rt.get("days"), int) or not 1 <= rt["days"] <= 7:
                errs.append("profile: current_routine.days must be a whole number from 1 to 7")
            _one_of(errs, rt, "age", core.ROUTINE_AGE)
            _all_in(errs, rt, "stalls", core.ROUTINE_STALLS)
            _all_in(errs, rt, "keep", core.ROUTINE_KEEP)
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
        bad = [g for g in r["regions"] if g not in core.REGIONS]
        if bad:
            errs.append("bank %s: unknown region %s" % (r["id"], ", ".join(bad)))
        if not r["regions"] and "region_free" not in r["tags"]:
            errs.append("bank %s: no regions; tag the joints it loads, or tag it region_free on purpose" % r["id"])
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
