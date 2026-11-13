"""logbook.py · what was done becomes memory: the log line, the progression, the week and the block.

The report file (written by the coach from what the person said, in any words):
  {"as_written": true,                         everything not listed below was done as written
   "results": {"squat": {"load": 60, "reps": [5, 5, 5, 5, 4], "rir": 1},
               "metcon": {"score": "7 rounds + 3"},
               "row": {"load": 40}},             a first outing: the weight they found
   "skipped": ["vpull"],
   "felt": "hard", "pain": [{"region": "knee", "score": 2}], "notes": "free text",
   "date": "2026-11-20"}                       optional, defaults to the session date
Loads are in the person's units; the engine stores kilograms.
"""
import datetime
import core, progress
from build import load_ctx, rule_fns

GROUPS = {"chest": "chest", "lats": "back", "upper_back": "back", "front_delts": "shoulders", "side_delts": "shoulders",
          "rear_delts": "shoulders", "biceps": "biceps", "triceps": "triceps", "quads": "quads", "glutes": "glutes",
          "hamstrings": "hamstrings", "calves": "calves", "core": "core", "obliques": "core", "lower_back": "core",
          "adductors": "quads", "forearms": "biceps"}


def to_kg(v, units):
    if v is None or v == "":
        return None
    v = float(v)
    return round(v / 2.20462, 2) if units == "lb" else v


def needs(session, report):
    """First outings with no weight reported: the coach must ask for them before logging."""
    out = []
    res = report.get("results", {})
    for b in session["blocks"]:
        for it in b["items"]:
            sl = it.get("_slot")
            if not sl or sl.get("travel") or sl["key"] in report.get("skipped", []):
                continue
            if it.get("first_outing") and sl["kind"] in ("main", "secondary") and sl["load_type"] not in ("bodyweight", "band", "time", "distance", "calories") \
                    and not (res.get(sl["key"]) or {}).get("load"):
                out.append({"key": sl["key"], "name": it["name"], "ask": "what weight did you end on for %s?" % it["name"]})
    return out


def optional_asks(session, report):
    """Accessories on a first outing: worth one line ("and roughly what you used on X?"), never blocking."""
    res = report.get("results", {})
    return [it["name"] for b in session["blocks"] for it in b["items"]
            if it.get("_slot") and it.get("first_outing") and it["_slot"]["kind"] in ("accessory", "finisher")
            and it["_slot"]["load_type"] not in ("bodyweight", "band", "time", "distance", "calories")
            and not (res.get(it["_slot"]["key"]) or {}).get("load")]


def apply(session, report, prof, st, bank):
    units = prof.get("units", "kg")
    res_all = report.get("results", {})
    skipped = set(report.get("skipped", []))
    as_written = report.get("as_written", True)
    done, hard = [], {}
    for b in session["blocks"]:
        for it in b["items"]:
            sl = it.get("_slot")
            if not sl:
                continue
            key = sl["key"]
            if key in skipped or sl.get("travel"):
                done.append({"key": key, "ex": sl["ex"], "skipped": key in skipped, "travel": bool(sl.get("travel"))})
                continue
            r = dict(res_all.get(key) or {})
            if not r and not as_written:
                done.append({"key": key, "ex": sl["ex"], "skipped": True})
                continue
            pres = sl["prescribed"]
            if "load" in r:
                r["load"] = to_kg(r["load"], units)
            elif pres.get("load") is not None:
                r["load"] = pres["load"]
            if not r.get("reps") and as_written and not r.get("score"):
                r["completed"] = True
                lo, hi = progress.rep_range(pres.get("reps") or sl["slot"].get("reps", ""))
                if hi and sl["rule"] not in ("tm_wave", "rpe_top_set", "benchmark", "run_volume", "c25k_week"):
                    cur = (st.get("slots", {}).get(sl["state_key"]) or {}).get("target") or lo
                    r["reps"] = [max(lo, min(hi, cur))] * int(pres.get("sets") or 1)
                elif sl["rule"] == "tm_wave":
                    r["reps"] = [progress.rep_range(str(pres.get("reps")).split("/")[-1])[0] or 1]
            st_slots = st.setdefault("slots", {})
            target = st_slots.setdefault(sl["state_key"], {})
            if r.get("ex") in bank and bank[r["ex"]]["pattern"] == bank.get(sl["ex"], {}).get("pattern"):
                target["ex"] = r["ex"]                      # they did another step of the ladder: that is the step now
            row = bank.get(sl["ex"])
            ctx = load_ctx(row, prof) if row else {"round": lambda x: x, "next_load": lambda x: None, "fmt": str, "lower": False}
            ctx["lower"] = row["pattern"] in ("squat", "hinge", "lunge") if row else False
            _, upd = rule_fns(sl["rule"])
            upd(sl["slot"], target, r, ctx)
            if sl["rule"] == "benchmark":
                target["outings"] = target.get("outings", 0) + 1
            if target.get("load") and row and row["load_type"] not in ("bodyweight", "band"):
                st.setdefault("loads_by_ex", {})[sl["ex"]] = target["load"]
            est = target.get("e1rm") or (round(target["tm"] / 0.9, 1) if target.get("tm") else None)
            if not est and target.get("load") and row and row["load_type"] not in ("bodyweight", "band"):
                lo = progress.rep_range(sl["slot"].get("reps", "")) [0] or 5
                est = round(progress.epley(target["load"], lo), 1)
            if est:
                st.setdefault("maxes_by_ex", {})[sl["ex"]] = est
            n = len(r.get("reps") or []) or int(pres.get("sets") or 1)
            if sl["kind"] in ("main", "secondary", "accessory") and sl["rule"] != "benchmark":
                for m in sl.get("muscles", []):
                    g = GROUPS.get(m)
                    if g:
                        hard[g] = hard.get(g, 0) + n
                for m in sl.get("muscles2", []):
                    g = GROUPS.get(m)
                    if g:
                        hard[g] = hard.get(g, 0) + 0.5 * n
            done.append({"key": key, "ex": sl["ex"], "rule": sl["rule"], "result": r, "prescribed": pres,
                         "after": {k: v for k, v in target.items() if k in ("load", "tm", "wave", "stage", "e1rm", "target", "best", "minutes", "week", "note")}})
    return done, hard


def score_text(session, done):
    for d in done:
        for b in session["blocks"]:
            for it in b["items"]:
                sl = it.get("_slot")
                if sl and sl["key"] == d["key"] and sl.get("score") and d.get("result"):
                    r = d["result"]
                    if r.get("score"):
                        return str(r["score"])
                    if r.get("load") and r.get("reps"):
                        if d.get("rule") == "rpe_top_set":
                            return "top set %s x %s" % (core.fmt_load(r["load"]), r["reps"][0])
                        return "%s x %s" % (core.fmt_load(r["load"]), "/".join(str(x) for x in r["reps"]))
                    if r.get("reps"):
                        return "/".join(str(x) for x in r["reps"]) + " reps"
                    if r.get("completed"):
                        return "done as written"
    return ""


def advance(st, plan, prog, session, date, counted=True):
    """The queue, the week and the block. A missed session (counted False) stays first in line."""
    if not counted:
        st["week_sessions"] = st.get("week_sessions", 0)
        return []
    if session.get("mode") not in ("rest",):
        q = st.get("queue") or []
        qi = session.get("_queue_index", 0)
        if session.get("mode") != "travel" and q and qi < len(q):
            q.pop(qi)
        # a travel day keeps the planned session first in line
        st["queue"] = q
        st["week_sessions"] = st.get("week_sessions", 0) + 1
        st["sessions_done"] = st.get("sessions_done", 0) + 1
        st["last_session"] = date
    events = []
    ws = st.get("week_start") or date
    if st["week_sessions"] >= plan["days"] or (datetime.date.fromisoformat(date) - datetime.date.fromisoformat(ws)).days >= 9:
        events.append("week_closed")
        st["week"] = st.get("week", 1) + 1
        st["week_sessions"] = 0
        st["week_start"] = date
        if st.get("flags", {}).get("early_deload_done"):
            st["flags"]["early_deload"] = False
            st["flags"]["early_deload_done"] = False
        if st.get("flags", {}).get("early_deload"):
            st["flags"]["early_deload_done"] = True
        total = prog.get("block_weeks", 4) + (1 if prog.get("deload") else 0)
        if st["week"] > total:
            events.append("block_closed")
            st["block"] = st.get("block", 1) + 1
            st["week"] = 1
    return events


def deload_triggers(log, st):
    """Any two: energy 5 or less in 3 of the last 4 · the same score down twice · pain or flat 3 in a row."""
    last = log[-4:]
    hits = 0
    if sum(1 for l in last if (l.get("energy") or 10) <= 5) >= 3:
        hits += 1
    if len(log) >= 3 and all((l.get("felt") in ("flat", "bad", "awful")) or l.get("pain") for l in log[-3:]):
        hits += 1
    drops = 0
    by = {}
    for l in log:
        if l.get("score_value") is not None:
            by.setdefault(l.get("session_id"), []).append(l["score_value"])
    for v in by.values():
        if len(v) >= 3 and v[-1] < v[-2] < v[-3]:
            drops += 1
    if drops:
        hits += 1
    if hits >= 2:
        st.setdefault("flags", {})["early_deload"] = True
        return True
    return False


def render_logmd(log, prof):
    units = prof.get("units", "kg") if prof else "kg"
    rows = ["# Your log", "", "_Written by the trainer after every session. The truth is `log.jsonl`; this page is the same thing, easier to read._", "",
            "| date | session | dose | score | how it felt | pain | notes |", "|:-|:-|:-|:-|:-|:-|:-|"]
    for l in log:
        pain = ", ".join("%s %s/10" % (p.get("region"), p.get("score")) for p in (l.get("pain") or []))
        rows.append("| %s | %s | %s | %s | %s | %s | %s |" % (l.get("date"), l.get("title", ""), l.get("level", ""),
                                                             l.get("score") or "", l.get("felt") or "", pain,
                                                             (l.get("notes") or "").replace("|", "/")))
    return "\n".join(rows) + "\n"
