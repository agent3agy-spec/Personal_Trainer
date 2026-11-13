"""progress.py · every progression rule, as code. The model never invents a progression.

Each rule has two functions:
  prescribe(slot, st, ctx) -> dict   what today's sets, reps, load and effort are
  update(slot, st, result, ctx)      changes the slot state after the person logs it

slot   : the slot from the program file (sets, reps, rest, rule, params)
st     : the slot's state in me/state.json (created empty on first use)
result : what was done: {"load": kg, "reps": [5, 5, 4], "rir": 2, "time": "12:30",
          "rounds": 7, "completed": true}
ctx    : {"lower": bool, "step": kg, "week_in_block": n, "deload": bool, "level": str,
          "units": "kg", "prof": profile}
Marks on each rule say how sure the doctrine is: see doctrine/schools/INDEX.md.
"""
import re


def epley(load, reps):
    """1RM estimate from a set of 10 or fewer reps. [believe, verified at M2]"""
    if not load or not reps:
        return None
    reps = min(int(reps), 10)
    return load * (1 + reps / 30.0)


def from_e1rm(e1rm, reps):
    return e1rm / (1 + min(int(reps), 10) / 30.0)


def rep_range(reps):
    """'8-12' -> (8, 12); '5' -> (5, 5); '5+' -> (5, 5); 'AMRAP' -> (0, 0)."""
    nums = [int(n) for n in re.findall(r"\d+", str(reps))]
    if not nums:
        return (0, 0)
    return (nums[0], nums[-1])


def default_inc(slot, ctx):
    if "inc" in slot:
        return slot["inc"]
    return 5.0 if ctx.get("lower") else 2.5


def first_outing_text(load_type, reps):
    lo, hi = rep_range(reps)
    target = hi or 10
    if load_type == "barbell":
        n = lo or 5
        return ("empty bar first, sets of %d adding a little each set. "
                "Stop at the first set of %d that feels like 3 left in the tank. Write that weight down" % (n, n))
    if target <= 3:
        return "learn the move with no weight first (a shoe balanced on your fist works), then a light weight. Smooth beats heavy"
    if load_type in ("dumbbell", "kettlebell", "machine", "cable"):
        return ("start with a weight you could lift 15 times. Do %d. Go a little heavier "
                "each set until %d reps leave 3 or 4 in the tank. Write that weight down" % (target, target))
    if load_type == "band":
        return "the band that makes %d reps hard but clean, 3 left in the tank. Write its colour" % target
    return ""


# · linear (StrongLifts / Starting Strength)

def linear_prescribe(slot, st, ctx):
    load = st.get("load")
    return {"sets": slot["sets"], "reps": slot["reps"], "load": load,
            "first_outing": load is None,
            "beat": ("all %s x %s at %s" % (slot["sets"], slot["reps"], ctx["fmt"](load))) if load else None}


def linear_update(slot, st, res, ctx):
    lo, _ = rep_range(slot["reps"])
    load = res.get("load", st.get("load"))
    if load is None:
        return
    reps = res.get("reps") or []
    all_done = res.get("completed") or (len(reps) >= slot["sets"] and all(r >= lo for r in reps[:slot["sets"]]))
    if st.get("load") is None:                      # first outing: the found load is the start
        st["load"] = load
        st["fails"] = 0
        return
    if all_done:
        inc = default_inc(slot, ctx)
        if slot.get("inc_after_100") and load >= 100:
            inc = slot["inc_after_100"]
        st["load"] = load + inc
        st["fails"] = 0
    else:
        st["fails"] = st.get("fails", 0) + 1
        st["load"] = load
        if st["fails"] >= slot.get("fails_to_reset", 3):     # StrongLifts: 3 misses, minus 10% [checked]
            st["load"] = ctx["round"](load * 0.9)
            st["fails"] = 0
            st["note"] = "reset 10 percent after 3 misses"


# · double progression (accessories everywhere)

def double_prescribe(slot, st, ctx):
    lo, hi = rep_range(slot["reps"])
    load = st.get("load")
    target = st.get("target", lo)
    return {"sets": slot["sets"], "reps": slot["reps"], "load": load, "first_outing": load is None,
            "beat": ("%d+ reps a set at %s" % (target, ctx["fmt"](load))) if load else None}


def double_update(slot, st, res, ctx):
    lo, hi = rep_range(slot["reps"])
    load = res.get("load", st.get("load"))
    reps = res.get("reps") or []
    if st.get("load") is None:
        st["load"] = load
        st["target"] = lo
        return
    if res.get("completed") and not reps:
        reps = [hi] * slot["sets"]
    if reps and len(reps) >= slot["sets"] and min(reps[:slot["sets"]]) >= hi:
        nxt = ctx["next_load"](load)
        if nxt is None:                               # fixed weights: climb the harder variant instead
            st["harder"] = True
            st["target"] = lo
            st["load"] = load
        else:
            st["load"] = nxt
            st["target"] = lo
    else:
        st["load"] = load
        st["target"] = max(lo, min(hi, (min(reps) if reps else lo) + 1))


# · 5/3/1 training max waves (Wendler)

WAVES = {1: [(0.65, 5), (0.75, 5), (0.85, "5+")],
         2: [(0.70, 3), (0.80, 3), (0.90, "3+")],
         3: [(0.75, 5), (0.85, 3), (0.95, "1+")],
         4: [(0.40, 5), (0.50, 5), (0.60, 5)]}


def tm_prescribe(slot, st, ctx):
    tm = st.get("tm")
    wave = st.get("wave", 1)
    if tm is None:
        return {"sets": 1, "reps": "5", "load": None, "first_outing": True,
                "text": "find your 5: empty bar first, sets of 5 climbing until one feels like 2 left. "
                        "That set sets your training max", "beat": None}
    rows = WAVES[wave if slot.get("deload_wave", True) else min(wave, 3)]
    sets = [{"load": ctx["round"](tm * p), "reps": r} for p, r in rows]
    if ctx.get("cap_amrap"):
        sets[-1]["reps"] = str(sets[-1]["reps"]).replace("+", "") + " (stop with 1 left)"
    return {"sets": len(sets), "reps": "/".join(str(s["reps"]) for s in sets), "load": sets[-1]["load"],
            "set_list": sets, "wave": wave,
            "beat": ("last set: more than %s at %s" % (str(rows[-1][1]).replace("+", ""), ctx["fmt"](sets[-1]["load"])))}


def tm_update(slot, st, res, ctx):
    if st.get("tm") is None:
        load, reps = res.get("load"), (res.get("reps") or [5])[-1]
        e = epley(load, reps)
        st["tm"] = ctx["round"](e * slot.get("tm_pct", 0.9)) if e else None
        st["wave"] = 1
        st["misses"] = 0
        return
    wave = st.get("wave", 1)
    reps = res.get("reps") or []
    minimum = {1: 5, 2: 3, 3: 1, 4: 0}[wave]
    if wave in (1, 2, 3) and reps and reps[-1] < minimum:
        st["misses"] = st.get("misses", 0) + 1
    last_wave = 4 if slot.get("deload_wave", True) else 3
    if wave >= last_wave:
        if st.get("misses", 0):
            st["tm"] = ctx["round"](st["tm"] * 0.9)          # a missed minimum: TM minus 10% [checked]
            st["note"] = "training max down 10 percent after a missed minimum"
        else:
            st["tm"] = st["tm"] + default_inc(slot, ctx)      # +2.5 upper, +5 lower per cycle [checked]
        st["wave"] = 1
        st["misses"] = 0
        st["cycles"] = st.get("cycles", 0) + 1
    else:
        st["wave"] = wave + 1


# · GZCLP tier stages [believe, verified at M2]

STAGES = {"T1": [(5, 3), (6, 2), (10, 1)], "T2": [(3, 10), (3, 8), (3, 6)]}


def tier_prescribe(slot, st, ctx):
    tier = slot.get("tier", "T1")
    stage = st.get("stage", 0)
    sets, reps = STAGES[tier][stage]
    load = st.get("load")
    r = "%d" % reps + ("+" if tier == "T1" else "")
    return {"sets": sets, "reps": r, "load": load, "first_outing": load is None,
            "beat": ("all %d x %d at %s" % (sets, reps, ctx["fmt"](load))) if load else None}


def tier_update(slot, st, res, ctx):
    tier = slot.get("tier", "T1")
    load = res.get("load", st.get("load"))
    if st.get("load") is None:
        st["load"], st["stage"] = load, 0
        return
    stage = st.get("stage", 0)
    sets, reps = STAGES[tier][stage]
    done = res.get("reps") or []
    ok = res.get("completed") or (len(done) >= sets and min(done[:sets]) >= reps)
    if ok:
        st["load"] = load + default_inc(slot, ctx)
    elif stage < 2:
        st["stage"] = stage + 1
        st["load"] = load
    else:
        st["stage"] = 0
        st["load"] = ctx["round"](load * 0.85)
        st["note"] = "back to the first stage at 85 percent"


# · RPE top set (RTS / SBS)

RPE_PCT = {(1, 10): 1.0, (1, 9): .955, (1, 8): .922, (3, 8): .863, (3, 9): .892, (5, 8): .811,
           (5, 9): .837, (5, 7): .786, (3, 7): .837, (8, 8): .739, (8, 9): .762}   # RTS chart rows [checked chart]


def rpe_prescribe(slot, st, ctx):
    reps, rpe = slot.get("top_reps", 3), slot.get("rpe", 8)
    e = st.get("e1rm")
    backoff = slot.get("backoff_sets", 3)
    if e is None:
        return {"sets": 1 + backoff, "reps": "1 x %d, then %d x %d" % (reps, backoff, reps),
                "load": None, "first_outing": True,
                "text": "work up in small jumps to a set of %d that feels like %d left. That is your top set. "
                        "Then %d more sets of %d at about 90 percent of it" % (reps, 10 - rpe, backoff, reps),
                "beat": None}
    pct = RPE_PCT.get((reps, rpe), from_e1rm(1, reps))
    top = ctx["round"](e * pct)
    return {"sets": 1 + backoff, "reps": "1 x %d, then %d x %d" % (reps, backoff, reps),
            "load": top, "backoff_load": ctx["round"](top * (1 - slot.get("fatigue_drop", 0.1))),
            "beat": "top set %s for %d with %d left or more" % (ctx["fmt"](top), reps, 10 - rpe)}


def rpe_update(slot, st, res, ctx):
    load, reps = res.get("load"), (res.get("reps") or [slot.get("top_reps", 3)])[0]
    rpe = res.get("rpe") or (10 - res["rir"] if res.get("rir") is not None else slot.get("rpe", 8))
    if not load:
        return
    pct = RPE_PCT.get((int(reps), int(rpe)))
    new = round(load / pct, 1) if pct else round(epley(load, reps + (10 - rpe)), 1)
    if res.get("completed") and st.get("e1rm"):
        new = max(new, st["e1rm"])             # done as written at the target: the estimate never drops
    st["e1rm"] = new


# · calisthenics ladder step (BWF Recommended Routine)

def ladder_prescribe(slot, st, ctx):
    return {"sets": slot.get("sets", 3), "reps": slot.get("reps", "5-8"), "load": None,
            "step": st.get("ex"), "first_outing": st.get("found") is None,
            "text": None if st.get("found") else
            "find your step: the hardest version you can do 3 sets of 5 with clean form",
            "beat": "3 x %d on this step" % (st.get("target", 5) + 1) if st.get("found") else None}


def ladder_update(slot, st, res, ctx):
    lo, hi = rep_range(slot.get("reps", "5-8"))
    st["found"] = True
    reps = res.get("reps") or ([hi] * 3 if res.get("completed") else [])
    if reps and len(reps) >= 3 and min(reps[:3]) >= hi:
        st["harder"] = True                      # 3 x 8: next step at 3 x 5 [snippet]
        st["target"] = lo
    else:
        st["target"] = max(lo, min(hi, (min(reps) if reps else lo)))


# · timed standard (Simple and Sinister)

def timed_prescribe(slot, st, ctx):
    ramp = st.get("ramp", 0.5)
    sets = max(1, round(slot["sets"] * ramp))
    return {"sets": sets, "reps": slot["reps"], "load": st.get("load"),
            "first_outing": st.get("load") is None,
            "beat": "inside %s at %s" % (slot.get("standard", "the standard"), ctx["fmt"](st.get("load")))
            if st.get("load") else None}


def timed_update(slot, st, res, ctx):
    load = res.get("load", st.get("load"))
    if st.get("load") is None:
        st["load"] = load
        return
    st["load"] = load
    if res.get("completed") is False:
        st["ramp"] = max(0.3, st.get("ramp", 0.5) - 0.2)      # a hard day: step back
    else:
        st["ramp"] = min(1.0, st.get("ramp", 0.5) + 0.25)     # build to the full dose over a few sessions
    st["streak"] = st.get("streak", 0) + 1 if res.get("inside_standard") else 0
    if st["streak"] >= slot.get("sessions_to_move", 3):
        nxt = ctx["next_load"](load)
        if nxt:
            st["load"], st["streak"] = nxt, 0


# · benchmark (metcons, HYROX pieces)

def bench_prescribe(slot, st, ctx):
    best = st.get("best")
    return {"sets": 1, "reps": slot.get("reps", ""), "load": None,
            "beat": ("your best on this piece: %s" % best) if best else "first time: it sets your score"}


def bench_update(slot, st, res, ctx):
    score = res.get("score") or res.get("time") or res.get("rounds")
    if score is None:
        return
    if res.get("completed") is False or res.get("capped"):
        st.setdefault("scores", []).append(score)   # a piece cut short is logged, never a new best
        return
    hist = st.setdefault("scores", [])
    hist.append(score)
    st["best"] = score if st.get("best") is None else _better(st["best"], score, slot.get("format"))


def score_value(x):
    """Rounds + reps as rounds x 1000 + reps; a time h:mm:ss or mm:ss in seconds; else the first number."""
    if isinstance(x, (int, float)):
        return x
    t = str(x).lower()
    m = re.match(r"\s*(\d+)\s*(?:rounds?|r)?\s*\+\s*(\d+)", t)
    if m:
        return int(m.group(1)) * 1000 + int(m.group(2))
    m = re.search(r"(\d+):(\d+)(?::(\d+))?", t)
    if m:
        a, b, c = int(m.group(1)), int(m.group(2)), m.group(3)
        return a * 3600 + b * 60 + int(c) if c else a * 60 + b
    m = re.search(r"(\d+(?:\.\d+)?)", t)
    v = float(m.group(1)) if m else 0
    return v * 1000 if "round" in t else v


def _better(a, b, fmt):
    secs = score_value
    if fmt == "fortime":
        return a if secs(a) <= secs(b) else b
    return a if secs(a) >= secs(b) else b


# · running volume (Daniels hold, novice caution)

def run_prescribe(slot, st, ctx):
    mins = st.get("minutes", slot.get("start_minutes", 20))
    return {"sets": 1, "reps": "%d min" % mins, "load": None, "minutes": mins,
            "beat": "%d min at a pace where you can talk in full sentences" % mins}


def run_update(slot, st, res, ctx):
    mins = st.get("minutes", slot.get("start_minutes", 20))
    if res.get("minutes"):                              # they ran longer and it was easy: follow them, up to +30%
        mins = max(mins, min(int(res["minutes"]), int(mins * 1.3)))
    st["minutes"] = mins
    if res.get("completed") or res.get("time"):
        st["weeks_held"] = st.get("weeks_held", 0) + (1.0 / max(1, slot.get("per_week", 1)))
    if st.get("weeks_held", 0) >= 3:                    # hold about 3 weeks, then about +10% [B]
        st["minutes"] = min(slot.get("max_minutes", 150), int(round(mins * 1.1)))
        st["weeks_held"] = 0


# · Couch to 5K weeks [believe the table]

def c25k_prescribe(slot, st, ctx):
    week = st.get("week", 1)
    table = slot["table"]
    run_n = st.get("run_in_week", 0)
    w = table[min(week, len(table)) - 1]
    text = w[run_n % len(w)] if isinstance(w, list) else w
    return {"sets": 1, "reps": text, "load": None, "week": week,
            "beat": "week %d, run %d of 3: finish it, walking where it says walk" % (week, run_n + 1)}


def c25k_update(slot, st, res, ctx):
    st.setdefault("week", 1)
    st.setdefault("run_in_week", 0)
    st.setdefault("done_in_week", 0)
    st["run_in_week"] += 1
    if res.get("completed", True):
        st["done_in_week"] += 1
    if st["run_in_week"] >= 3:
        if st["done_in_week"] >= 3 and st["week"] < len(slot["table"]):
            st["week"] += 1                      # all three runs done: next week, else repeat it
        st["run_in_week"], st["done_in_week"] = 0, 0


# · fixed work (warm-ups, mobility, balance holds)

def fixed_prescribe(slot, st, ctx):
    return {"sets": slot.get("sets", 1), "reps": slot.get("reps", ""), "load": None, "beat": None}


def fixed_update(slot, st, res, ctx):
    pass


RULES = {
    "linear_session": (linear_prescribe, linear_update),
    "double_progression": (double_prescribe, double_update),
    "fixed_load": (double_prescribe, double_update),     # double progression that climbs a harder variant at a fixed weight
    "tm_wave": (tm_prescribe, tm_update),
    "tier_stages": (tier_prescribe, tier_update),
    "rpe_top_set": (rpe_prescribe, rpe_update),
    "ladder_step": (ladder_prescribe, ladder_update),
    "timed_standard": (timed_prescribe, timed_update),
    "benchmark": (bench_prescribe, bench_update),
    "run_volume": (run_prescribe, run_update),
    "c25k_week": (c25k_prescribe, c25k_update),
    "fixed": (fixed_prescribe, fixed_update),
}
