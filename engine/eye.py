"""eye.py · the coach's eye: the checks a coach runs by reflex on every plan and every session (research/07 Part 3).

    review(prof, plan, st, bank)       a whole week, built for real on a copy of the state, at `plan.py choose`
    session_checks(session, plan, prof) one built session, at every `plan.py build`

A check returns {"check", "ok", "say"}. A failed check either fixes the plan (a weekly set target is added
and the week is built again) or is reported in plain words: never silent. Standard library only.
"""
import copy, datetime
import core
from sheet import session_seconds

PUSH, PULL = {"h_push", "v_push"}, {"h_pull", "v_pull"}
GROUPS = {"chest": ["chest"], "back": ["lats", "upper_back"], "quads": ["quads"], "hamstrings and glutes": ["hamstrings", "glutes"],
          "shoulders": ["side_delts", "front_delts", "rear_delts"]}
STATIONS = ("Sled", "Wall ball", "Farmer", "Sandbag", "Burpee", "Ski", "Rowing", "carry")
HEAVY = ("tm_wave", "rpe_top_set", "linear_session", "tier_stages")


def _items(s):
    for b in s.get("blocks", []):
        for it in b["items"]:
            yield b, it


def _sets(it):
    try:
        return int(it.get("sets") or 1)
    except (TypeError, ValueError):
        return 1


def minutes_check(s, asked):
    if s.get("rest_day") or s.get("mode") == "travel":
        return None
    built = session_seconds(s) / 60.0
    if s.get("long_run_day"):
        return {"check": "minutes", "ok": True, "say": "Long run day: %d minutes, more than your usual %d, said on the sheet." % (round(built), asked)}
    ok = (0.9 * asked <= built or s.get("lighter") or s.get("own")) and built <= asked + 3   # their own routine is as long as they wrote it     # a taper, a sore day or an easier week is short on purpose
    return {"check": "minutes", "ok": ok, "built": round(built), "asked": asked,
            "say": "" if ok else ("%s is %d of your %d minutes: nothing more in this plan fits that session well." % (s.get("title"), round(built), asked)
                                  if built < asked else "%s runs %d minutes, over your %d." % (s.get("title"), round(built), asked))}


def session_checks(session, plan, prof):
    """One session: the minutes are real, and the goal finisher and the priority survived the clock."""
    out = []
    asked = int((session.get("long_run_day") or {}).get("asked") or session.get("minutes") or prof.get("minutes", 45))
    m = minutes_check(session, asked)
    if m:
        out.append(m)
    lifting = any(b["kind"] in ("main", "secondary", "accessory") and it.get("_slot", {}).get("rule") not in ("run_volume", "c25k_week", "benchmark")
                  and it.get("ex") != "piece" for b, it in _items(session))
    if lifting and plan.get("goal_modules"):
        have = {b.get("_module") for b in session.get("blocks", [])}
        miss = [g for g in plan["goal_modules"] if g not in have]
        if miss:
            out.append({"check": "goal_finisher", "ok": False,
                        "say": "Your %s work did not fit today; the notes say how many minutes it needs." % ", ".join(core.load_module(g)["name"].lower() for g in miss)})
    return [c for c in out if not c["ok"]]


def simulate(prof, plan, st, bank, days=None):
    """The next week, built for real on a copy of the state: energy 7, the usual minutes, every session done."""
    import build
    st = copy.deepcopy(st)
    out = []
    d0 = datetime.date(2030, 1, 7)
    for i in range(days or plan["days"]):
        if not st.get("queue"):
            build.refill(st, core.load_program(plan["program"]), plan)
        s = build.build({"energy": 7, "minutes": prof.get("minutes", 45)}, prof, plan, st, bank, (d0 + datetime.timedelta(days=i)).isoformat())
        out.append(s)
        q = st.get("queue") or []
        qi = s.get("_queue_index", 0)
        if s.get("mode") not in ("rest", "travel") and qi < len(q):
            q.pop(qi)
        st["week_sessions"] = st.get("week_sessions", 0) + 1
    return out


def week_checks(prof, plan, sessions, bank):
    out = []
    lead = core.load_program(plan["program"])
    lead_stream = (plan.get("streams") or [{}])[0]
    rot = lead_stream.get("rotation") or []
    if rot and len(rot) > lead_stream.get("per_week", len(rot)) and not lead.get("rotates"):
        out.append({"check": "days", "ok": False, "say": "This plan's %d sessions would rotate over %d days and lose volume."
                    % (len(rot), lead_stream["per_week"])})
    else:
        out.append({"check": "days", "ok": True, "say": ""})
    asked = int(prof.get("minutes", 45))
    for s in sessions:
        m = minutes_check(s, asked)
        if m and not m["ok"]:
            out.append(m)
    sets, push, pull, pri_sets, pri_sessions = {}, 0, 0, {}, {}
    heavy_sessions, lifting_sessions, long_run, easy_run, stations, running, pieces, cond = 0, 0, False, False, 0, False, 0, False
    for s in sessions:
        heavy = lifting = False
        for b, it in _items(s):
            sl = it.get("_slot") or {}
            row = bank.get(it.get("ex"))
            if sl.get("rule") == "run_volume":
                running = True
                long_run |= "long" in sl.get("key", "")
                easy_run |= "easy" in sl.get("key", "")
            if sl.get("rule") == "c25k_week":
                running = True
            if sl.get("rule") in ("run_volume", "c25k_week") or b.get("format") == "run":
                cond = True                              # easy cardio minutes serve a fitness or fat-loss goal too
            if it.get("ex") == "piece":
                pieces += 1
                moves = " ".join(sl.get("prescribed", {}).get("moves", []))
                stations += any(w.lower() in moves.lower() for w in STATIONS)
                running |= " run" in (" " + moves.lower())
                cond |= b.get("_module") == "conditioning" or b["kind"] == "finisher"
                continue
            if b["kind"] == "warmup" or not row or b["kind"] == "finisher" and row["pattern"] in ("mobility", "balance"):
                continue
            if sl.get("rule") in ("run_volume", "c25k_week"):
                continue
            n = _sets(it)
            lifting = True
            if row["pattern"] in PUSH:
                push += n
            if row["pattern"] in PULL:
                pull += n
            for m in row["muscles_primary"]:
                sets[m] = sets.get(m, 0) + n
            for m in row["muscles_secondary"]:
                sets[m] = sets.get(m, 0) + 0.5 * n
            if b["kind"] == "main" and (sl.get("rule") in HEAVY or str(it.get("reps", "")).split("-")[0].strip() in ("1", "2", "3", "4", "5", "6")):
                heavy = True
            if it.get("_priority"):
                a = it["_priority"]
                pri_sets[a] = pri_sets.get(a, 0) + int(sl.get("pri_added") or 0)
                pri_sessions.setdefault(a, set()).add(s.get("date"))
        heavy_sessions += heavy
        lifting_sessions += lifting
    for t in plan.get("targets") or []:
        if t.get("why") != "priority":
            continue
        a = t["area"]
        need = min(2, lifting_sessions)
        ok = pri_sets.get(a, 0) >= 4 and len(pri_sessions.get(a, ())) >= need
        out.append({"check": "priority", "ok": ok, "area": a, "added": pri_sets.get(a, 0),
                    "say": "" if ok else "Your %s get %d extra sets this week, short of the 4 to 6 a priority needs: the minutes run out first."
                    % (a, pri_sets.get(a, 0))})
    if push or pull:
        ok = pull >= push or push - pull <= 1
        out.append({"check": "push_pull", "ok": ok, "push": push, "pull": pull,
                    "say": "" if ok else "Pulling still trails pushing a little: %d sets against %d this week." % (pull, push),
                    "fix": None if ok else push - pull})
    comps = [c.get("what") for c in plan.get("components") or []]
    main = comps[0] if comps else "lift"
    goal = prof.get("goal")
    if main == "lift" and goal in ("strength", "powerlifting", "weightlifting") and lifting_sessions >= 2:
        ok = heavy_sessions >= 2
        out.append({"check": "key_quality", "ok": ok, "say": "" if ok else "Only %d heavy session this week for a strength goal." % heavy_sessions})
    if main == "lift" and goal in ("muscle", "fat_loss") and lifting_sessions >= 3:
        low = [g for g, ms in GROUPS.items() if max(sets.get(m, 0) for m in ms) < 8]
        out.append({"check": "volume", "ok": not low, "low": low,
                    "say": "" if not low else "Under 8 hard sets this week for: %s." % ", ".join(low)})
    if "run" in comps or main == "run":
        need_long = bool(plan.get("long_run"))
        ok = running and (long_run or not need_long)
        out.append({"check": "key_quality", "ok": ok, "say": "" if ok else "No long run in the week for a running event."})
    if "hyrox" in comps:
        ok = running and stations >= 1
        out.append({"check": "key_quality", "ok": ok, "say": "" if ok else "HYROX needs running and at least one station piece each week."})
    if "mixed" in comps:
        ok = pieces >= sum(c.get("days") or 1 for c in plan.get("components") or [] if c.get("what") == "mixed")
        out.append({"check": "key_quality", "ok": ok, "say": "" if ok else "Mixed fitness needs at least two conditioning pieces a week."})
    if "conditioning" in comps:
        ok = cond or any(c.get("what") == "conditioning" and c.get("role") == "day" for c in plan.get("components") or [])
        out.append({"check": "second_goal", "ok": ok, "say": "" if ok else "No conditioning reached the week: the minutes ran out before it."})
    for c in plan.get("components") or []:
        if c.get("role") == "day":
            seen = any(s.get("session_id", "").startswith(("prog:%s" % c["from"], "mod:%s" % c["from"])) for s in sessions)
            out.append({"check": "second_goal", "ok": seen, "say": "" if seen else "The %s days did not come round this week." % c["what"]})
    return out


def review(prof, plan, st, bank):
    """At choose: build the week, check it, fix what a weekly target can fix (pulling, a low muscle group),
    build it again, and return what is still wrong in plain words."""
    sessions = simulate(prof, plan, st, bank)
    found = week_checks(prof, plan, sessions, bank)
    fixes = []
    for f in found:
        if f["check"] == "push_pull" and not f["ok"]:
            fixes.append({"area": "pull", "parts": [["upper_back", "h_pull"], ["lats", "v_pull"]], "weekly": min(6, max(4, f["fix"])), "why": "balance"})
        if f["check"] == "volume" and not f["ok"]:
            for g in f["low"][:2]:
                fixes.append({"area": g, "parts": [[GROUPS[g][0], {"chest": "h_push", "back": "h_pull", "quads": "quads_iso",
                                                                    "hamstrings and glutes": "hamstrings_iso", "shoulders": "delts"}[g]]],
                              "weekly": 4, "why": "volume"})
    if fixes and plan.get("targets") is not None:
        plan["targets"] = list(plan["targets"]) + fixes
        sessions = simulate(prof, plan, st, bank)
        found = week_checks(prof, plan, sessions, bank)
        for fx in fixes:
            found.append({"check": "fixed", "ok": True, "say": "The trainer added %d weekly sets of %s to balance the week."
                          % (fx["weekly"], "pulling" if fx["area"] == "pull" else fx["area"])})
    return found, sessions
