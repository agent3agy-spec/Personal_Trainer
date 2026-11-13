"""coach.py · the coach's habits around the plan (doctrine/07_CYCLE.md, phase E, research/07).

The tests at the start of every block, the first milestone, the weekly check-in, the missed week and the
forgiving streak, the block review, and the taper before an event. Personal bests live in logbook.py,
soreness in build.py. Everything the coach keeps sits in the plan's data block under "coach" (me/PLAN.md);
nothing here changes a number by itself without the doctrine saying so.
"""
import datetime, math
import core, progress

LEVELS = ["rest", "light", "standard", "planned"]          # build.readiness, lowest first


def _d(iso):
    return datetime.date.fromisoformat(iso)


def cap_level(level, top):
    """The day's dose, never above `top` (a rest day stays a rest day)."""
    return level if LEVELS.index(level) <= LEVELS.index(top) else top


# · the tests (week 1 of every block)

TESTS = {
    "push_ups": {"name": "Push-ups", "unit": "reps", "better": "higher",
                 "how": "As many push-ups as you can with a straight body. Stop when the form breaks. Knees down or hands "
                        "on a bench is fine: do it the same way every time.",
                 "when": "at the end of any session"},
    "plank": {"name": "Plank hold", "unit": "seconds", "better": "higher",
              "how": "On forearms and toes, a straight line from head to heels. Stop when the hips sag.",
              "when": "at the end of any session"},
    "run_2k": {"name": "2 km run", "unit": "time", "better": "lower",
               "how": "2 km at the fastest pace you can hold evenly from start to finish. Not a sprint start.",
               "when": "after the warm-up of a run day, or on a fresh day"},
    "walk_run_12": {"name": "12 minutes, walk and run", "unit": "metres", "better": "higher",
                    "how": "12 minutes, running when you can and walking when you need to. How far did you get?",
                    "when": "after the warm-up of a run day, or on a fresh day"},
    "row_1k": {"name": "1000 m row", "unit": "time", "better": "lower",
               "how": "1000 m on the rower at the fastest pace you can hold evenly, after the warm-up.",
               "when": "after the warm-up of any session"},
}
LIFT_WORDS = "your main lifts, from the weights you log this week (nothing extra to do)"


def _parts(plan, prog=None):
    whats = {c.get("what") for c in (plan or {}).get("components") or []}
    fam = (prog or {}).get("family")
    if fam and fam != "own":                            # their own routine: its components say what it holds
        whats.add({"strength": "lift", "powerbuild": "lift", "muscle": "lift", "weightlifting": "lift", "health": "lift",
                   "functional": "mixed", "hyrox": "hyrox", "hybrid": "lift", "run": "run"}.get(fam, "lift"))
        if fam == "hybrid":
            whats.add("run")
    return whats


def battery(prof, plan, prog=None):
    """Two short, safe tests for this person, plus the main lifts read from their own log. No max test, ever."""
    import build
    whats = _parts(plan, prog)
    tags = set(core.place_tags(prof))
    avoid = build.avoid_regions(prof, {})
    tests = []
    can_run = not prof.get("no_impact") and not ({"knee", "ankle", "hip"} & avoid) and ({"outdoors", "treadmill"} & tags)
    runner = "run_30min" in (prof.get("skills") or []) or prof.get("run_30min") or \
        (prof.get("experience_by") or {}).get("running") in ("novice", "intermediate", "advanced")
    if ({"run", "hyrox"} & whats) and can_run:
        tests.append("run_2k" if runner else "walk_run_12")
    elif "rower" in tags and ({"mixed", "hyrox", "conditioning"} & whats or prof.get("goal") in ("fat_loss", "health", "functional")):
        tests.append("row_1k")
    elif can_run and ({"conditioning"} & whats or prof.get("goal") in ("fat_loss", "functional")):
        tests.append("walk_run_12")
    if not ({"shoulder", "wrist", "elbow"} & avoid):
        tests.append("push_ups")
    elif "low_back" not in avoid:
        tests.append("plank")
    lifts = bool({"lift", "mixed"} & whats)
    return {"tests": [dict(TESTS[t], id=t) for t in tests[:2]], "lifts": lifts, "lift_words": LIFT_WORDS if lifts else None}


def parse_value(test_id, v):
    """A test result as one number: seconds for a time ("10:45" or 645), metres, reps or seconds held."""
    if v is None or v == "":
        return None
    if TESTS[test_id]["unit"] == "time" and isinstance(v, str) and ":" in v:
        m, s = v.split(":", 1)
        return int(m) * 60 + float(s)
    return float(v)


def fmt_value(test_id, v):
    if v is None:
        return ""
    u = TESTS[test_id]["unit"]
    if u == "time":
        return "%d:%02d" % (int(v) // 60, int(round(v)) % 60)
    if u == "metres":
        return "%d m" % round(v)
    if u == "seconds":
        return "%d s" % round(v)
    return "%d" % round(v)


def better(test_id, new, old):
    """Percent better (positive) or worse (negative), the right way round for times."""
    if not new or not old:
        return None
    pct = (old - new) / old if TESTS[test_id]["better"] == "lower" else (new - old) / old
    return round(100 * pct, 1)


def coach_data(plan):
    return (plan or {}).setdefault("coach", {})


def tests_due(plan, st, prof=None, date=None):
    """Due in weeks 1 and 2 of every block until done or skipped, and again after 4 weeks or more off. Never in a taper."""
    if not plan or not st:
        return False
    if prof and taper(prof, date or core.today()):
        return False
    if (st.get("flags") or {}).get("retest"):
        return True
    done = {t.get("block") for t in coach_data(plan).get("tests", [])}
    return st.get("block", 1) not in done and st.get("week", 1) <= 2


def record_tests(plan, st, data, date):
    """Keep the results (or the skip) for this block. Returns the comparison with the first and the last time."""
    cd = coach_data(plan)
    hist = cd.setdefault("tests", [])
    res = {}
    for k, v in (data.get("results") or {}).items():
        if k in TESTS:
            try:
                val = parse_value(k, v)
            except (TypeError, ValueError):
                continue
            if val:
                res[k] = val
    prev = [t for t in hist if t.get("results")]
    hist[:] = [t for t in hist if t.get("block") != st.get("block", 1)]
    hist.append({"block": st.get("block", 1), "date": date, "results": res, "skipped": bool(data.get("skip")) and not res})
    (st.setdefault("flags", {})).pop("retest", None)
    cmp_ = []
    for k, v in res.items():
        first = next((t["results"][k] for t in prev if k in t["results"]), None)
        last = next((t["results"][k] for t in reversed(prev) if k in t["results"]), None)
        cmp_.append({"id": k, "name": TESTS[k]["name"], "now": fmt_value(k, v), "first": fmt_value(k, first) if first else None,
                     "since_start": better(k, v, first), "since_last": better(k, v, last),
                     "best": bool(last and better(k, v, max((t["results"][k] for t in prev if k in t["results"]),
                                                             key=lambda x: -x if TESTS[k]["better"] == "lower" else x)) > 0)})
    return cmp_


# · the lifts, read from the log (no extra test)

def _e1rm(d):
    r = d.get("result") or {}
    reps = [int(x) for x in (r.get("reps") or []) if x]
    if d.get("skipped") or not r.get("load") or not reps:
        return None
    return progress.epley(float(r["load"]), max(reps))


def lift_bests(log, block=None, week=None, kinds=("main", "secondary", None)):
    """The best estimated max per main lift, for a block (and a week of it) or the whole log."""
    out = {}
    for l in log:
        if l.get("unreported") or (block is not None and l.get("block") != block) or (week is not None and l.get("week") != week):
            continue
        for d in l.get("done") or []:
            e = _e1rm(d)
            if e and d.get("kind") in kinds:
                out[d["ex"]] = max(out.get(d["ex"], 0), e)
    return out


def lift_changes(log, bank, block):
    """Each main lift: its week 1 estimate in this block, its best by the end of it, in percent."""
    first, last = {}, {}
    for l in log:
        if l.get("unreported") or l.get("block") != block:
            continue
        for d in l.get("done") or []:
            e = _e1rm(d)
            if e and d.get("kind") in ("main", "secondary", None):
                first.setdefault(d["ex"], e)
                last[d["ex"]] = max(last.get(d["ex"], 0), e)
    return [{"ex": ex, "name": bank.get(ex, {}).get("name", ex), "pct": round(100 * (last[ex] - v) / v, 1)}
            for ex, v in first.items() if v and last.get(ex)]


# · the first milestone (4 to 6 weeks out)

LIFT_PCT = {"none": 10, "novice": 10, "intermediate": 5, "advanced": 2.5}
TEST_PCT = {"none": 5, "novice": 5, "intermediate": 3, "advanced": 2}


def milestone(prof, plan, prog, week=None, start=None, block=1):
    """A first milestone they are very likely to hit: sessions done (three quarters of the plan) and one number
    (the first main lift a little up on week 1, or the engine test a little better), at the end of the first block."""
    start = start or core.today()
    weeks = max(4, min(6, int(prog.get("block_weeks", 4))))
    by = (_d(start) + datetime.timedelta(weeks=weeks)).isoformat()
    sessions = max(2, int(round(plan.get("days", prof.get("days", 3)) * weeks * 0.75)))
    exp = prof.get("experience", "none")
    m = {"from": start, "by": by, "weeks": weeks, "sessions": sessions, "block": block}
    lift = None
    for s in week or []:
        for b in s.get("blocks", []):
            if b.get("kind") != "main":
                continue
            for it in b["items"]:
                sl = it.get("_slot") or {}
                if sl.get("load_type") in ("barbell", "dumbbell", "kettlebell", "machine", "cable") and \
                        sl.get("rule") not in ("benchmark", "run_volume", "c25k_week"):
                    lift = lift or {"ex": it["ex"], "name": it["name"]}
    tests = [t["id"] for t in battery(prof, plan, prog)["tests"] if t["id"] not in ("push_ups", "plank")]
    if lift and "lift" in _parts(plan, prog):
        m["lift"] = dict(lift, pct=LIFT_PCT.get(exp, 5))
    elif tests:
        m["test"] = {"id": tests[0], "name": TESTS[tests[0]]["name"], "pct": TEST_PCT.get(exp, 3)}
    m["text"] = milestone_text(m)
    return m


def nice_date(iso):
    d = _d(iso)
    return "%d %s" % (d.day, d.strftime("%B"))


def milestone_text(m):
    t = "By %s: %d sessions done" % (nice_date(m["by"]), m["sessions"])
    if m.get("lift"):
        t += ", and %s about %g percent above your first week" % (m["lift"]["name"].lower(), m["lift"]["pct"])
    elif m.get("test"):
        t += ", and your %s test about %g percent better than the first one" % (m["test"]["name"].lower(), m["test"]["pct"])
    return t + "."


def check_milestone(plan, log, today=None):
    """Where the milestone stands: hit, on track, behind, or missed (once its date has passed)."""
    m = coach_data(plan).get("milestone")
    if not m:
        return None
    today = today or core.today()
    lines = [l for l in log if not l.get("unreported") and l.get("mode") != "rest" and m["from"] <= l.get("date", "") <= m["by"]]
    done = len(lines)
    res = {"text": m["text"], "by": m["by"], "sessions": done, "sessions_target": m["sessions"], "parts": {"sessions": done >= m["sessions"]},
           "lift": m.get("lift"), "test": m.get("test"), "block": m.get("block", 1)}
    if m.get("lift"):
        ex = m["lift"]["ex"]
        vals = [e for l in lines for d in l.get("done") or [] if d.get("ex") == ex for e in [_e1rm(d)] if e]
        if len(vals) >= 2:
            gain = round(100 * (max(vals[1:]) - vals[0]) / vals[0], 1)
            res["lift_gain"] = gain
            res["parts"]["lift"] = gain >= m["lift"]["pct"]
        else:
            res["parts"]["lift"] = None
    if m.get("test"):
        k = m["test"]["id"]
        vals = [t["results"][k] for t in coach_data(plan).get("tests", []) if k in (t.get("results") or {})]
        if len(vals) >= 2:
            res["test_gain"] = better(k, vals[-1], vals[0])
            res["parts"]["test"] = res["test_gain"] >= m["test"]["pct"]
        else:
            res["parts"]["test"] = None
    known = [v for v in res["parts"].values() if v is not None]
    hit = all(known) and res["parts"]["sessions"]
    elapsed = max(0, (_d(today) - _d(m["from"])).days)
    pace = m["sessions"] * min(1.0, elapsed / max(1, (_d(m["by"]) - _d(m["from"])).days))
    if hit:
        res["status"] = "hit"
    elif today > m["by"]:
        res["status"] = "missed"
    else:
        res["status"] = "on_track" if done + 1 >= math.floor(pace) else "behind"
    res["say"] = {"hit": "Milestone reached: %s" % m["text"],
                  "on_track": "On track for your milestone: %d of %d sessions so far." % (done, m["sessions"]),
                  "behind": "%d of %d sessions so far for your milestone. One session this week puts you back on pace." % (done, m["sessions"]),
                  "missed": "Not this one, and that is fine: the next milestone starts from where you are now."}[res["status"]]
    return res


# · the weekly check-in

BARRIERS = core.BARRIERS + ["nothing"]
ENERGY = ["low", "ok", "good"]
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def week_done(log, block, week):
    return len([l for l in log if not l.get("unreported") and l.get("block") == block and l.get("week") == week])


def checkin(plan, st, prof, data, log, date):
    """Which days happened, what got in the way, energy. It sets next week: an easier dose, shorter sessions, the days."""
    cd = coach_data(plan)
    last = next((l for l in reversed(log) if l.get("block")), None)      # the week that just closed is the last one logged
    blk, wk = (last["block"], last.get("week")) if last else (st.get("block", 1), max(1, st.get("week", 1) - 1))
    done = data.get("days_done")
    if done is None:
        if last:
            done = week_done(log, blk, wk)
        else:
            since = (_d(date) - datetime.timedelta(days=7)).isoformat()
            done = len([l for l in log if not l.get("unreported") and l.get("date", "") > since])
    barriers = [b for b in data.get("barriers") or [] if b in BARRIERS]
    energy = data.get("energy") if data.get("energy") in ENERGY else "ok"
    nxt = [d for d in data.get("next_days") or [] if d in DAYS]
    item = {"date": date, "block": blk, "week": wk, "done": done, "planned": plan.get("days"), "barriers": barriers,
            "energy": energy, "next_days": nxt, "skipped": bool(data.get("skip"))}
    hist = cd.setdefault("checkins", [])
    hist.append(item)
    del hist[:-12]
    st.setdefault("flags", {}).pop("checkin_due", None)
    week_plan = {}
    say = []
    if done is not None and plan.get("days"):
        say.append("%d of %d sessions last week." % (done, plan["days"]) if done < plan["days"] else
                   "All %d sessions last week. That is the habit that builds everything else." % plan["days"])
    if energy == "low" or {"energy", "stress", "pain"} & set(barriers):
        week_plan["dose"] = "easier"
        say.append("This week runs a little easier: no all-out sets, one set fewer on the extra moves.")
    if "time" in barriers:
        week_plan["minutes"] = max(core.MINUTES_RANGE[0], int(prof.get("minutes", 45)) - 15)
        say.append("Time got in the way, so the sessions this week aim at %d minutes. Short and done beats long and skipped." % week_plan["minutes"])
    if nxt:
        week_plan["days"] = nxt
        say.append("Your days this week: %s. If one goes, the session waits for the next free day." % ", ".join(d.capitalize() for d in nxt))
    if "bored" in barriers:
        say.append("Bored is worth fixing: at the end of this block you can change the extra moves or the focus.")
    if "know_how" in barriers:
        say.append("Not sure how a move goes: every line on your sheet links to a demonstration.")
    short = [c for c in hist[-2:] if c.get("done") is not None and c.get("planned") and c["done"] < c["planned"]]
    suggest = None
    if len(hist) >= 2 and len(short) == 2 and all("time" in c["barriers"] for c in hist[-2:]) and plan.get("days", 0) > 2:
        suggest = "fewer_days"
        say.append("Two weeks running short on time: %d days a week might fit your life better. Say the word and the plan changes." % (plan["days"] - 1))
    if week_plan:
        week_plan["set"] = date
    st["next_week"] = week_plan
    return {"checkin": item, "next_week": week_plan, "suggest": suggest, "say": " ".join(say)}


def week_plan(st, date):
    """What the last check-in set, for at most 9 days (a week closes after 9 days whatever happens)."""
    wp = (st or {}).get("next_week") or {}
    try:
        if wp.get("set") and (_d(date) - _d(wp["set"])).days > 9:
            return {}
    except ValueError:
        return {}
    return wp


# · the missed week and the streak

def back_tier(st, date):
    """Days since the last session, and how the trainer welcomes them back."""
    last = (st or {}).get("last_session")
    if not last:
        return 0, None
    gap = (_d(date) - _d(last)).days
    if gap >= 28:
        return gap, "long"            # 15 percent lighter, two easy sessions, and the tests again
    if gap >= 14:
        return gap, "two_weeks"       # 15 percent lighter, then one more easy session
    if gap >= 7:
        return gap, "week"            # one lighter session
    return gap, None


BACK_LINES = {"week": "Welcome back. A lighter session to get going again; the plan carries on where you left it.",
              "two_weeks": "Welcome back: after two weeks or more off, loads start about 15 percent lighter today, and the next session is easy too.",
              "long": "Welcome back. Loads start about 15 percent lighter, the next session is easy too, and this week we redo your starting numbers so the plan fits the you of today."}


def streak(log, today=None, weeks=8):
    """Weeks in a row with at least one session. One empty week is a rest week: it pauses the streak and never
    resets it. Two empty weeks in a row end it. The current week counts once it has a session."""
    today = _d(today or core.today())
    monday = today - datetime.timedelta(days=today.weekday())
    counts = {}
    for l in log:
        if l.get("unreported") or l.get("mode") == "rest" or not l.get("date"):
            continue
        d = _d(l["date"])
        k = (monday - (d - datetime.timedelta(days=d.weekday()))).days // 7
        if k >= 0:
            counts[k] = counts.get(k, 0) + 1
    n, rest, k, empty = 0, 0, 0 if counts.get(0) else 1, 0
    while True:
        if counts.get(k):
            n += 1
            empty = 0
        else:
            empty += 1
            if empty >= 2 or not any(v for kk, v in counts.items() if kk > k):
                break
            rest += 1
        k += 1
    rest = rest if n else 0
    return {"weeks": n, "rest_weeks": rest, "this_week": counts.get(0, 0),
            "paused": bool(n) and not counts.get(0) and not counts.get(1),
            "by_week": [counts.get(i, 0) for i in range(weeks - 1, -1, -1)]}


# · the taper

EVENT_NAMES = {"run_5k_10k": "your race", "run_half": "your half marathon", "run_marathon": "your marathon",
               "hyrox": "your HYROX race", "meet": "your meet"}
TAPER_WEEKS = {"run_5k_10k": 1, "run_half": 2, "run_marathon": 3, "hyrox": 1, "meet": 2}
# The volume left in each of the last weeks, the final week first. Weights and effort stay (Bosquet 2007, Mujika).
TAPER_VOLUME = {1: [0.6], 2: [0.5, 0.7], 3: [0.5, 0.65, 0.8]}


def event_kind(prof):
    import compose
    for oid, det, _ in compose.outcome_parts(prof):
        if oid == "event" and det in TAPER_WEEKS:
            return det
    return None


def taper(prof, date):
    """None, or the taper of this day: the event, the days to go, the share of the usual volume."""
    ev = prof.get("event") or {}
    kind = event_kind(prof)
    if not kind or not ev.get("date"):
        return None
    try:
        days = (_d(ev["date"]) - _d(date)).days
    except ValueError:
        return None
    weeks = TAPER_WEEKS[kind]
    if not 0 <= days < weeks * 7:
        return None
    return {"kind": kind, "event": ev.get("name") or EVENT_NAMES[kind], "days": days, "weeks": weeks,
            "volume": TAPER_VOLUME[weeks][min(days // 7, weeks - 1)], "race_day": days == 0}


def event_after(prof, plan, date):
    """The event is 1 to 21 days behind them and nothing has been reviewed since: ask how it went and what is next."""
    ev = prof.get("event") or {}
    if not event_kind(prof) or not ev.get("date"):
        return False
    try:
        gone = (_d(date) - _d(ev["date"])).days
    except ValueError:
        return False
    reviewed = [r for r in coach_data(plan).get("reviews", []) if r.get("date", "") >= ev["date"]]
    return 1 <= gone <= 21 and not reviewed


# · the block review

CHANGES = ["keep", "easier", "harder", "shorter", "longer", "fewer_days", "more_days", "new_focus", "move_on"]
WELL = ["showed_up", "got_stronger", "fitter", "enjoyed", "felt_good", "nothing"]


def reviewed_block(st):
    """The block that just closed, or the one running when the review comes early (after an event)."""
    return max(1, st.get("block", 1) - 1) if (st.get("flags") or {}).get("review_due") else st.get("block", 1)


def block_review(prof, plan, st, log, prog, bank, today=None):
    """The block that just closed, in plain numbers, and the choices for the next one."""
    blk = reviewed_block(st)
    lines = [l for l in log if not l.get("unreported") and l.get("block") == blk]
    weeks = prog.get("block_weeks", 4) + (1 if prog.get("deload") else 0)
    planned = plan.get("days", 3) * weeks
    tests = coach_data(plan).get("tests", [])
    this = next((t for t in tests if t.get("block") == blk and t.get("results")), None)
    first = next((t for t in tests if t.get("results")), None)
    tcmp = []
    if this and first and this is not first:
        for k, v in this["results"].items():
            if k in first["results"]:
                tcmp.append({"id": k, "name": TESTS[k]["name"], "first": fmt_value(k, first["results"][k]), "now": fmt_value(k, v),
                             "pct": better(k, v, first["results"][k])})
    grads = [g for g in prog.get("graduates_to") or [] if (core.PROGRAMS / (g + ".md")).exists()]
    barriers = {}
    for c in coach_data(plan).get("checkins", []):
        if c.get("block") == blk:
            for b in c.get("barriers", []):
                if b != "nothing":
                    barriers[b] = barriers.get(b, 0) + 1
    lifts = lift_changes(log, bank, blk)
    ms = check_milestone(plan, log, today)
    options = [c for c in CHANGES if c != "move_on" or grads]
    up = [x for x in lifts if x["pct"] > 0]
    wins = []
    if lines:
        wins.append("%d of %d sessions done this block." % (len(lines), planned))
    if up:
        top = max(up, key=lambda x: x["pct"])
        wins.append("%s up %g percent since week 1." % (top["name"], top["pct"]))
    for t in tcmp:
        if t["pct"] and t["pct"] > 0:
            wins.append("%s: %s now, %s at the start." % (t["name"], t["now"], t["first"]))
    return {"block": blk, "sessions": len(lines), "planned": planned, "lifts": lifts, "tests": tcmp, "milestone": ms,
            "barriers": sorted(barriers, key=lambda b: -barriers[b]), "options": options, "went_well": WELL,
            "next_program": grads[0] if grads else None, "wins": wins,
            "event_after": event_after(prof, plan, today or core.today())}


def apply_review(prof, plan, st, data, prog, today):
    """The answer to the block review. Returns what changed and the next command, if any, for the coach to run."""
    ch = data.get("change") if data.get("change") in CHANGES else "keep"
    cd = coach_data(plan)
    cd.setdefault("reviews", []).append({"date": today, "block": reviewed_block(st), "went_well": data.get("went_well"),
                                         "change": ch, "note": str(data.get("note") or "")[:300]})
    st.setdefault("flags", {}).pop("review_due", None)
    out = {"change": ch, "profile": {}, "next_command": None}
    if ch in ("easier", "harder"):
        st["block_adjust"] = ch
    else:
        st.pop("block_adjust", None)
    lo, hi = core.MINUTES_RANGE
    if ch == "shorter":
        out["profile"]["minutes"] = max(lo, int(prof.get("minutes", 45)) - 15)
    elif ch == "longer":
        out["profile"]["minutes"] = min(hi, int(prof.get("minutes", 45)) + 15)
    elif ch == "fewer_days":
        out["profile"]["days"] = max(1, int(prof.get("days", 3)) - 1)
        out["next_command"] = ["match"]
    elif ch == "more_days":
        out["profile"]["days"] = min(7, int(prof.get("days", 3)) + 1)
        out["next_command"] = ["match"]
    elif ch == "new_focus":
        out["profile"]["priority"] = [p for p in data.get("priority") or [] if isinstance(p, str)][:2]
        out["next_command"] = ["choose", plan["program"]]
    elif ch == "move_on":
        g = next((x for x in prog.get("graduates_to") or [] if (core.PROGRAMS / (x + ".md")).exists()), None)
        out["next_command"] = ["choose", g] if g else None
    if out["next_command"] is None:
        cd["milestone"] = dict(milestone(dict(prof, **out["profile"]), plan, prog, start=today, block=st.get("block", 1)),
                               lift=(cd.get("milestone") or {}).get("lift"))
        if not cd["milestone"].get("lift"):
            cd["milestone"].pop("lift", None)
        cd["milestone"]["text"] = milestone_text(cd["milestone"])
    return out
