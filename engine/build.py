"""build.py · today's session, built by rule from the program file, the bank, the state and today's readiness.

The coach never writes a session by hand. It runs `plan.py build`, then only translates and
personalises the words (title, why, cues) before the sheet is rendered. Every number here
comes from a program file, a rule in progress.py, or the person's own log.
"""
import copy, datetime, math, re
import core, progress
from sheet import session_seconds, TOLERANCE

LOWER = {"squat", "hinge", "lunge", "calves", "hamstrings_iso", "quads_iso", "glutes_iso"}
NOT_LOADABLE = {"bodyweight", "band", "time", "distance", "calories"}
GYM_DB = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 50]
GYM_KB = [8, 12, 16, 20, 24, 28, 32, 40, 48]
PRIORITY = {"glutes": ["glutes"], "arms": ["biceps", "triceps"], "biceps": ["biceps"], "triceps": ["triceps"],
            "back": ["lats", "upper_back"], "chest": ["chest"], "shoulders": ["side_delts", "rear_delts", "front_delts"],
            "legs": ["quads", "hamstrings", "glutes"], "quads": ["quads"], "hamstrings": ["hamstrings"], "core": ["core", "obliques"],
            "calves": ["calves"], "abs": ["core"]}
DISLIKE_TYPES = {"machines": {"machine", "cable"}, "barbell": {"barbell"}, "kettlebells": {"kettlebell"}, "dumbbells": {"dumbbell"},
                 "bodyweight": {"bodyweight"}}


# · readiness (doctrine/04_INTENSITY.md)

def readiness(today):
    """today: {"energy": 1-10, "pain": [{"region": "knee", "score": 0-10, "days": n}], "minutes": n,
               "ill": bool, "hard_cardio_24h": bool, "place": "main", "notes": ""}"""
    e = int(today.get("energy", 7))
    pain = today.get("pain") or []
    refer = [p["region"] for p in pain if p.get("score", 0) > 3 or p.get("days", 0) >= 10 or p.get("sharp")]
    if today.get("ill"):
        return "rest", "ill", refer
    if e <= 3:
        return "rest", "energy", refer
    if e <= 5:
        return "light", "", refer
    if e <= 7:
        return "standard", "", refer
    return "planned", "", refer


LEVEL_TEXT = {"planned": "full dose", "standard": "normal dose, no max efforts",
              "light": "light dose: fewer sets, a little lighter", "rest": "rest day"}


# · choosing an exercise

def avoid_regions(prof, today):
    """Regions left out completely: a limit marked exclude, or pain today over 3, sharp or lasting."""
    out = set()
    for lim in prof.get("limits", []):
        if lim.get("exclude", True) and lim.get("region"):
            out.add(lim["region"])
    for p in (today or {}).get("pain") or []:
        if p.get("region") and (p.get("score", 0) > 3 or p.get("sharp") or p.get("days", 0) >= 10):
            out.add(p["region"])
    return out


def care_regions(prof, today):
    """Regions trained with care: an old injury that is cleared, or mild pain today (3 or less).
    Care means: no impact on that region, and nothing above level 3 that loads it."""
    out = {l["region"] for l in prof.get("limits", []) if l.get("region") and not l.get("exclude", True)}
    out |= {p["region"] for p in (today or {}).get("pain") or [] if p.get("region") and p.get("score", 0) <= 3
            and not p.get("sharp") and p.get("days", 0) < 10}
    return out


def allowed(row, prof, tags, avoid, cap):
    flags = set((prof.get("screen") or {}).get("flags", []))
    if not core.has_equipment(row, tags):
        return False
    if row["needs_coaching"] and "olympic_coached" not in prof.get("skills", []):
        return False
    if set(row["regions"]) & avoid:
        return False
    if row["impact"] and ({"pregnant", "low_bone_density"} & flags or prof.get("no_impact")
                          or ("postpartum" in flags and not prof.get("impact_ok"))):
        return False
    care = prof.get("_care") or set()
    if care & set(row["regions"]) and (row["impact"] or row["level"] > 3):
        return False
    if "pregnant" in flags and row["id"] in ("bench_press", "db_bench_press", "close_grip_bench", "dead_bug", "glute_bridge",
                                            "single_leg_glute_bridge", "hip_thrust", "skull_crusher", "db_floor_press", "reverse_crunch"):
        return False                                   # no lying on the back after the first trimester (ACOG) [believe list]
    if prof.get("position") == "seated" and not (row.get("position") == "seated" or "wheelchair_ok" in row["tags"]):
        return False
    if row["pattern"] == "v_pull" and row["load_type"] == "bodyweight" and row["level"] >= 3 \
            and "pullup" not in prof.get("skills", []) and prof.get("experience") in ("none", "novice"):
        return False                                   # no strict pull-up yet: negatives, hangs and rows first
    if row["level"] > cap:
        return False
    return True


def select(slot, prof, tags, avoid, bank, offset=0):
    bad = set().union(*[DISLIKE_TYPES.get(d, set()) for d in prof.get("dislikes", [])]) if prof.get("dislikes") else set()
    if bad:
        pick = _select(slot, prof, tags, avoid, bank, offset, bad)
        if pick:
            return pick
    return _select(slot, prof, tags, avoid, bank, offset, set())


def _select(slot, prof, tags, avoid, bank, offset, bad):
    exp = prof.get("experience", "none")
    cap = core.LEVEL_CAP[exp]
    target = core.LEVEL_TARGET[exp]
    for i in slot.get("prefer", []):
        if i in bank and bank[i]["load_type"] not in bad and allowed(bank[i], prof, tags, avoid, cap + 1):
            return i
    pool = [r for r in bank.values() if r["pattern"] == slot["pattern"]
            and (not slot.get("muscles") or set(slot["muscles"]) & set(r["muscles_primary"]))
            and r["load_type"] not in bad and allowed(r, prof, tags, avoid, cap)]
    if not pool:
        return None
    pool.sort(key=lambda r: (abs(r["level"] - target), 0 if "lengthened" in r["tags"] else 1, r["id"]))
    return pool[min(offset, len(pool) - 1)]["id"]


# · loads

def load_ctx(row, prof):
    lt = row["load_type"]
    units = prof.get("units", "kg")
    if lt == "dumbbell":
        steps = sorted(prof.get("dumbbells") or GYM_DB)
    elif lt == "kettlebell":
        steps = sorted(prof.get("kettlebells") or GYM_KB)
    else:
        steps = None
    step = prof.get("plate_step", 2.5) if lt == "barbell" else 2.5

    def rnd(kg):
        if kg is None:
            return None
        if steps:
            below = [s for s in steps if s <= kg + 1e-9]
            return below[-1] if below else steps[0]
        v = core.kg_round_down(kg, step)
        return max(v, 20.0) if lt == "barbell" else v

    def nxt(kg):
        if kg is None:
            return None
        if steps:
            up = [s for s in steps if s > kg + 1e-9]
            return up[0] if up else None
        return kg + step

    return {"lower": row["pattern"] in LOWER, "round": rnd, "next_load": nxt,
            "fmt": lambda kg: core.fmt_load(kg, units), "units": units, "loadable": lt not in NOT_LOADABLE}


def seed_from_numbers(slot, st, ex, prof, ctx, carried_max=None):
    """Known numbers enter once (doctrine/05_LOADS.md rule 9): the only discount is applied here."""
    num = (prof.get("numbers") or {}).get(ex)
    if not num and carried_max:
        num = {"kg": carried_max, "reps": 1}
    if not num or st.get("seeded"):
        return
    e = progress.epley(num.get("kg"), num.get("reps", 1))
    if not e:
        return
    rule = slot["rule"]
    if rule == "tm_wave":
        st["tm"] = ctx["round"](e * slot.get("tm_pct", 0.9))
        st["wave"] = 1
    elif rule == "rpe_top_set":
        st["e1rm"] = round(e * 0.9, 1)          # the one discount (doctrine/05_LOADS.md)
    elif rule in ("linear_session", "double_progression", "fixed_load", "tier_stages", "timed_standard"):
        lo, hi = progress.rep_range(slot["reps"])
        st["load"] = ctx["round"](progress.from_e1rm(e, max(lo, 1)) * 0.9)
        st["target"] = lo
    st["seeded"] = True


# · bodyweight and band slots: reps, then a harder step

def bw_prescribe(slot, st, ctx):
    lo, hi = progress.rep_range(slot["reps"])
    t = st.get("target", lo)
    return {"sets": slot["sets"], "reps": slot["reps"], "load": None,
            "beat": ("%d+ a set" % t) if t and hi else None}


def bw_update(slot, st, res, ctx):
    lo, hi = progress.rep_range(slot["reps"])
    reps = res.get("reps") or ([hi] * slot["sets"] if res.get("completed") else [])
    if hi and reps and len(reps) >= slot["sets"] and min(reps[:slot["sets"]]) >= hi:
        st["harder"] = True
        st["target"] = lo
    elif reps:
        st["target"] = max(lo, min(hi or lo, min(reps) + 1))
    if res.get("band"):
        st["band"] = res["band"]


def effective_rule(slot, row):
    if row and row["load_type"] in NOT_LOADABLE and slot["rule"] in ("linear_session", "double_progression", "fixed_load", "tier_stages",
                                                                     "tm_wave", "rpe_top_set", "timed_standard"):
        return "bw"
    return slot["rule"]


def rule_fns(name):
    if name == "bw":
        return bw_prescribe, bw_update
    return progress.RULES[name]


# · the queue (sessions in order, never by weekday)

def refill(st, prog, plan):
    days = plan["days"]
    lay = prog["layouts"].get(str(min(days, prog["days"][1]))) or prog["layouts"].get(str(prog["days"][1]))
    q = list(lay)
    extra = days - prog["days"][1]
    mods = [m for m in plan.get("extra_modules", [])]
    if extra > 0 and mods:
        m = core.load_module(mods[0])
        order = m.get("order", list(m.get("sessions", {}).keys()))
        k = st.setdefault("extra_index", 0)
        for i in range(extra):
            q.append("mod:%s:%s" % (m["id"], order[(k + i) % len(order)]))
        st["extra_index"] = k + extra
    st["queue"] = q


def session_template(prog, sid, minutes, force_express=False):
    """The normal session, always, so every lift of the rotation comes round. The express version only when
    the normal one cannot be cut to fit the minutes (build() retries with force_express)."""
    if sid.startswith("mod:"):
        _, mid, s = sid.split(":", 2)
        m = core.load_module(mid)
        return copy.deepcopy(m["sessions"][s]), "module"
    if force_express and prog.get("express"):
        return copy.deepcopy(prog["express"]), "express"
    return copy.deepcopy(prog["sessions"][sid]), "normal"


def pick_session(st, prog, plan, today):
    if not st.get("queue"):
        refill(st, prog, plan)
    q = st["queue"]
    bad = set()
    if today.get("hard_cardio_24h"):
        bad |= {"heavy_legs", "power", "hard_cardio"}
    for i, sid in enumerate(q):
        tags = set()
        if not sid.startswith("mod:"):
            tags = set(prog["sessions"][sid].get("tags", []))
        if not (tags & bad):
            return sid, i
    return q[0], 0


# · the warm-up (written by the engine)

def warmup(blocks, bank, tags, minutes, prof=None, avoid=frozenset()):
    prof = prof or {}
    ok = lambda r: allowed(r, prof, tags, set(avoid), 5)
    order = ("arm_ergometer", "seated_shadow_boxing") if prof.get("position") == "seated" else ("bike_erg", "row_erg", "incline_walk", "ski_erg", "jump_rope")
    fallback = "Arm circles and seated punches" if prof.get("position") == "seated" else "Brisk walk or marching on the spot"
    raise_ = next((bank[i]["name"] for i in order if i in bank and ok(bank[i])), fallback)
    mob = [r for r in bank.values() if r["pattern"] == "mobility" and ok(r)]
    regions = set()
    for b in blocks:
        for it in b["items"]:
            regions |= set(it.get("_regions", []))
    mob.sort(key=lambda r: (-len(set(r["regions"]) & regions), r["id"]))
    items = [{"ex": "raise", "name": raise_, "reps": "3 min", "cue": "easy, then a little faster in the last 30 s"}]
    for r in mob[:2]:
        items.append({"ex": r["id"], "name": r["name"], "reps": "5 slow reps", "cue": r["cue"]})
    first = next((it for b in blocks for it in b["items"] if b["kind"] == "main" and it.get("_loadable")), None)
    if first:
        items.append({"ex": "ramp", "name": "Ramp: " + first["name"], "reps": "2 to 3 lighter sets",
                      "cue": "half, then three quarters of today's weight, few reps, then start"})
    return {"name": "Warm-up", "kind": "warmup", "format": "straight", "minutes": 6 if minutes < 35 else 8, "items": items}


# · one slot to one sheet line

def slot_item(slot, block, prof, st_all, bank, tags, avoid, level, prog, week_info, notes, today):
    st_slots = st_all.setdefault("slots", {})
    key = slot["key"]
    st = st_slots.setdefault(key, {})
    if slot.get("kind") == "piece":
        return piece_item(slot, st, prof, bank, tags, avoid, notes)
    offset = (st_all.get("block", 1) - 1) % 2 if block["kind"] == "accessory" else 0
    ex = st.get("ex")
    if ex and st.get("harder") and bank.get(ex, {}).get("harder"):
        h, seen = bank[ex]["harder"], set()
        while h and h in bank and h not in seen and not allowed(bank[h], prof, tags, avoid, core.LEVEL_CAP[prof.get("experience", "none")] + 1):
            seen.add(h)
            h = bank[h].get("harder")
        if h and h in bank and h not in seen:
            notes.append("%s moves up a step: %s" % (bank[ex]["name"], bank[h]["name"]))
            st.update({"ex": h, "load": None, "target": None, "found": None})
            ex = h
        else:
            notes.append("%s: top step for your kit. Make it harder with a 3 second lowering and a pause." % bank[ex]["name"])
        st["harder"] = False
    today_ex = ex if ex and ex in bank and allowed(bank[ex], prof, tags, avoid, core.LEVEL_CAP[prof.get("experience", "none")] + 1) else None
    if today_ex is None:
        today_ex = select(slot, prof, tags, avoid, bank, offset)
        if today_ex is None:
            return None
        if not ex:
            st["ex"] = today_ex
        elif ex != today_ex:
            notes.append("%s swapped for %s today" % (bank.get(ex, {}).get("name", ex), bank[today_ex]["name"]))
    row = bank[today_ex]
    ctx = load_ctx(row, prof)
    ctx["cap_amrap"] = level in ("standard", "light")
    rule = effective_rule(slot, row)
    use = st if today_ex == st.get("ex") else st_slots.setdefault(key + "@" + today_ex, {})
    if use.get("load") is None and use.get("tm") is None and ctx["loadable"]:
        carried = st_all.get("loads_by_ex", {}).get(today_ex)
        if carried and rule in ("linear_session", "double_progression", "fixed_load", "tier_stages", "timed_standard"):
            use["load"] = carried
        seed_from_numbers(slot, use, today_ex, prof, ctx, st_all.get("maxes_by_ex", {}).get(today_ex))
    if rule == "run_volume" and "minutes" not in use and (prof.get("numbers") or {}).get("easy_run_minutes"):
        base = int(prof["numbers"]["easy_run_minutes"])
        use["minutes"] = min(slot.get("max_minutes", 150), max(slot.get("start_minutes", 20),
                             int(base * 1.5) if "long" in slot["key"] else base))
    if ctx["loadable"] and use.get("load") is None and row["load_type"] in ("dumbbell", "kettlebell"):
        owned = prof.get("dumbbells" if row["load_type"] == "dumbbell" else "kettlebells") or []
        if len(owned) == 1 and rule in ("double_progression", "fixed_load", "linear_session", "timed_standard"):
            use["load"] = owned[0]                     # they own one weight: that is the load, nothing to find
    pre_fn, _ = rule_fns(rule)
    pr = pre_fn(slot, use, ctx)
    sets = pr.get("sets", slot.get("sets", 1))
    reps = pr.get("reps", slot.get("reps"))
    load = pr.get("load")
    effort = slot.get("effort", "")
    deload, meso_w = week_info
    if deload and rule != "tm_wave":
        d = prog.get("deload") or {}
        sets = max(1, math.ceil(sets * d.get("sets_factor", 0.5)))
        load = ctx["round"](load * d.get("load_factor", 0.9)) if load else load
        effort = "easy and crisp, %s left" % d.get("rir", "4")
    elif meso_w is not None and block["kind"] in (prog.get("meso") or {}).get("applies_to", []):
        m = prog["meso"]
        w = min(meso_w, len(m["rir_by_week"]) - 1)
        effort = "%s left in the tank" % m["rir_by_week"][w]
        sets += m.get("extra_sets_by_week", [0])[min(w, len(m.get("extra_sets_by_week", [0])) - 1)]
    if level == "light":
        sets = max(1, math.ceil(sets * 2 / 3))
        load = ctx["round"](load * 0.9) if load else load
    if today.get("_restart") and load:
        load = ctx["round"](load * 0.85)
    load_text = ""
    if pr.get("set_list"):
        ls = [s_["load"] * (0.9 if level == "light" else 1) for s_ in pr["set_list"]]
        load_text = " / ".join(ctx["fmt"](ctx["round"](x)) for x in ls)
    elif load:
        load_text = ctx["fmt"](load)
        if pr.get("backoff_load"):
            load_text += ", then " + ctx["fmt"](pr["backoff_load"])
    elif row["load_type"] == "bodyweight":
        load_text = "bodyweight"
    elif row["load_type"] == "band":
        load_text = ("band: " + use["band"]) if use.get("band") else "a band that leaves 2 to 3 in the tank"
    first = None
    if (pr.get("first_outing") or (ctx["loadable"] and load is None and rule not in ("benchmark", "run_volume", "c25k_week", "fixed"))):
        first = pr.get("text") or progress.first_outing_text(row["load_type"], reps)
        if rule in ("tm_wave", "rpe_top_set"):
            sets = 1 if rule == "tm_wave" else sets
        elif prof.get("experience") in ("none", "novice"):
            sets = min(sets, 2)          # session one is short on purpose (doctrine/05_LOADS.md rule 7)
            effort = "about 3 left: today you find your weight"
        else:
            effort = "about 2 left: find your weight on the first set, then the rest at it"
    if rule in ("run_volume", "c25k_week"):
        load_text = ""
    item = {"ex": today_ex, "name": row["name"], "key": key, "sets": sets, "reps": reps, "load": load_text,
            "effort": effort, "rest": slot.get("rest", 90), "cue": row["cue"],
            "demo": "https://www.youtube.com/results?search_query=" + re.sub(r"\s+", "+", row["name"]) + "+exercise+form",
            "_regions": row["regions"], "_loadable": ctx["loadable"] and bool(load)}
    if first:
        item["first_outing"] = first
    if pr.get("minutes"):
        item["work"] = pr["minutes"] * 60
    item["_slot"] = {"key": key, "ex": today_ex, "rule": rule, "slot": slot, "state_key": key if use is st else key + "@" + today_ex,
                     "prescribed": {"sets": sets, "reps": reps, "load": load}, "beat": pr.get("beat"),
                     "score": bool(slot.get("score")), "load_type": row["load_type"], "kind": block["kind"],
                     "muscles": row["muscles_primary"], "muscles2": row["muscles_secondary"]}
    return item


def piece_item(slot, st, prof, bank, tags, avoid, notes):
    pieces = slot.get("pieces") or [slot.get("moves", [])]
    n = st.get("outings", 0)
    moves = []
    for mv in pieces[n % len(pieces)]:
        ms = dict(mv)
        ms.setdefault("key", "move")
        i = select(ms, prof, tags, avoid, bank)
        if i:
            moves.append("%s %s" % (mv.get("reps", ""), bank[i]["name"]))
    if not moves:
        return None
    fmt = slot.get("format", "amrap")
    head = {"amrap": "AMRAP %d min" % slot.get("minutes", 12), "fortime": "For time, cap %d min" % slot.get("minutes", 15),
            "emom": "EMOM %d min" % slot.get("minutes", 12), "intervals": "Intervals, %d min" % slot.get("minutes", 10)}.get(fmt, fmt)
    pr = progress.bench_prescribe(slot, st, {})
    item = {"ex": "piece", "name": head, "key": slot["key"], "sets": 1, "reps": " · ".join(moves), "load": "",
            "effort": slot.get("effort", "steady, then hard in the last third"), "rest": 0,
            "cue": slot.get("cue", "scale the load first, then the reps, then the move, to keep the pace"),
            "work": slot.get("minutes", 12) * 60, "_regions": [], "_loadable": False}
    item["_slot"] = {"key": slot["key"], "ex": "piece", "rule": "benchmark", "slot": slot, "state_key": slot["key"],
                     "prescribed": {"piece": n % len(pieces), "moves": moves}, "beat": pr.get("beat"),
                     "score": bool(slot.get("score")), "load_type": "time", "kind": "main", "muscles": [], "muscles2": []}
    return item


# · the whole session

def week_info(st, prog):
    w = st.get("week", 1)
    deload = bool(prog.get("deload")) and (w > prog.get("block_weeks", 4) or st.get("flags", {}).get("early_deload"))
    meso_w = (w - 1) if prog.get("meso") and not deload else None
    return deload, meso_w


def build(today, prof, plan, st, bank, date=None):
    date = date or core.today()
    prog = core.load_program(plan["program"])
    level, why_level, refer = readiness(today)
    minutes = int(today.get("minutes") or prof.get("minutes", 45))
    tags = core.place_tags(prof, today.get("place"))
    if today.get("equipment"):
        tags = core.expand_equipment(today["equipment"])
    avoid = avoid_regions(prof, today)
    prof = dict(prof, _care=care_regions(prof, today) - avoid)
    notes = []
    if "symptoms_reported" in (prof.get("screen") or {}).get("flags", []):
        notes.append("If chest pain, dizziness or fainting happens: stop and get medical help.")
    if refer:
        notes.append("Sharp, worsening or lasting pain (%s): that area is left out. Please see a physiotherapist or doctor before loading it again."
                     % ", ".join(refer))
    last = st.get("last_session")
    if last and (datetime.date.fromisoformat(date) - datetime.date.fromisoformat(last)).days >= 14:
        today = dict(today, _restart=True)
        notes.append("Welcome back: after two weeks or more off, loads start about 15 percent lighter today.")
    if level == "rest":
        return recovery(today, prof, bank, tags, date, why_level, notes)
    st_before = copy.deepcopy(st)
    sid, qi = pick_session(st, prog, plan, today)
    tpl, mode = session_template(prog, sid, minutes, today.get("_express"))
    deload, meso_w = week_info(st, prog)
    blocks = []
    for b in tpl["blocks"]:
        items = []
        for slot in b["slots"]:
            it = slot_item(slot, b, prof, st, bank, tags, avoid, level, prog, (deload, meso_w), notes, today)
            if it is None:
                if b["kind"] == "main" and len(b["slots"]) == 1 and not any(bb["kind"] == "main" and bb is not b for bb in tpl["blocks"]):
                    notes.append("The main lift '%s' can't be done with today's equipment or limits: today is the travel session." % slot["key"])
                    return travel(today, prof, plan, st, bank, tags, avoid, date, notes)
                if b["kind"] == "main":
                    notes.append("'%s' left out today (your equipment or limits); the rest of the main block stands." % slot["key"])
                    continue
                notes.append("'%s' left out today: nothing in the bank fits your equipment and limits." % slot["key"])
                continue
            items.append(it)
        if items:
            nb = {"name": b["name"], "kind": b["kind"], "format": b.get("format", "straight"), "items": items}
            for k in ("rest_after_round", "minutes", "lead_rest"):
                if b.get(k):
                    nb[k] = b[k]
            if nb["format"] in ("superset", "circuit"):
                nb["rest_note"] = "%s after each round" % _mmss(b.get("rest_after_round", 90))
            blocks.append(nb)
    pri = {g for w in prof.get("priority", []) for g in PRIORITY.get(str(w).lower().strip(), [])}
    added = 0
    for b in blocks:
        if b["kind"] != "accessory":
            continue
        for it in b["items"]:
            if added < 2 and pri & set(it["_slot"]["muscles"]):
                it["sets"] = int(it["sets"]) + 1
                added += 1
    mods = [] if mode == "express" else list(plan.get("modules", []))
    for mid in mods:
        m = core.load_module(mid)
        if m.get("when") != "finisher":
            continue
        for b in m["session"]["blocks"]:
            items = [it for it in (slot_item(sl, dict(b, kind="finisher"), prof, st, bank, tags, avoid, level, prog, (deload, None), [], today)
                                   for sl in b["slots"]) if it]
            if items:
                nb = {"name": m["name"], "kind": "finisher", "format": b.get("format", "straight"), "items": items,
                      "_module": mid, "_mandatory": mid == "balance"}
                for k in ("rest_after_round", "minutes"):
                    if b.get(k):
                        nb[k] = b[k]
                blocks.append(nb)
    blocks.insert(0, warmup(blocks, bank, tags, minutes, prof, avoid))
    title = tpl.get("title", sid)
    mains = [it for b in blocks if b["kind"] == "main" for it in b["items"]]
    if prof.get("position") == "seated" or any(n.endswith("swapped for %s today" % it["name"]) for it in mains for n in notes):
        title = " · ".join(it["name"] for it in mains[:3]) or title
    session = {"date": date, "title": title, "program": prog["id"], "program_name": prog["name"],
               "session_id": sid, "mode": mode, "block": st.get("block", 1), "week": st.get("week", 1),
               "deload": deload, "level": level, "level_text": LEVEL_TEXT[level], "energy": today.get("energy"),
               "minutes": minutes, "language": prof.get("language", "en"), "units": prof.get("units", "kg"),
               "paper": prof.get("paper", "A4"), "blocks": blocks}
    fit(session, minutes, notes)
    if session_seconds(session) > minutes * 60 + TOLERANCE and mode == "normal" and prog.get("express"):
        st.clear()
        st.update(st_before)                       # undo what the first attempt touched, then build the express version
        return build(dict(today, _express=True), prof, plan, st, bank, date)
    score = next((it["_slot"]["beat"] for b in session["blocks"] for it in b["items"]
                  if it.get("_slot", {}).get("score") and it["_slot"].get("beat")), None)
    session["score_to_beat"] = score or "first time on this session: today sets the numbers you will beat"
    main_names = [it["name"] for b in session["blocks"] if b["kind"] == "main" for it in b["items"]]
    pos = "Session %d of %d this week" % (st.get("week_sessions", 0) + 1, plan["days"])
    session["why"] = "%s, next in your rotation. Block %d, week %d%s. Main job: %s. Energy %s: %s." % (
        pos, st.get("block", 1), st.get("week", 1), " (deload week: easy on purpose)" if deload else "",
        ", ".join(main_names) or "the main piece", today.get("energy", "?"), LEVEL_TEXT[level])
    ev = prof.get("event") or {}
    try:
        wk = (datetime.date.fromisoformat(ev.get("date", "")) - datetime.date.fromisoformat(date)).days // 7
        if wk >= 0:
            session["why"] += " %d weeks to %s." % (wk, ev.get("name") or "your event")
    except ValueError:
        pass
    session["low_energy"] = "Finish the main block, do one accessory, skip the finisher, and log what you did."
    session["log"] = log_lines(session)
    session["notes"] = " ".join(notes)
    session["_queue_index"] = qi
    return session


def _mmss(s):
    s = int(s)
    return "%d:%02d" % (s // 60, s % 60)


def log_lines(session):
    out = ["Done as written? If not, what changed"]
    for b in session["blocks"]:
        for it in b["items"]:
            sl = it.get("_slot")
            if not sl:
                continue
            if sl.get("score") or (b["kind"] == "main"):
                if sl["rule"] == "benchmark":
                    out.append("%s: score (rounds + reps, or time)" % it["name"])
                elif it.get("first_outing"):
                    out.append("%s: the weight you found" % it["name"])
                elif sl["rule"] in ("run_volume", "c25k_week"):
                    out.append("%s: minutes, and could you talk in full sentences?" % it["name"])
                elif sl["rule"] == "rpe_top_set":
                    out.append("%s: top set weight x reps, and how many were left" % it["name"])
                else:
                    out.append("%s: reps on the last set, and how many were left" % it["name"])
    out.append("Anything that hurt (where, 0 to 10)")
    return out[:6]


def fit(session, minutes, notes):
    """The minutes are a ceiling. Cut order (doctrine/06_BUILD.md): optional finishers, the last accessory,
    accessory sets to 2, secondary sets by one. The main block is never cut."""
    limit = minutes * 60 + TOLERANCE
    guard = 0
    while session_seconds(session) > limit and guard < 40:
        guard += 1
        bl = session["blocks"]
        fin = [b for b in bl if b["kind"] == "finisher" and not b.get("_mandatory")]
        if fin:
            bl.remove(fin[-1])
            notes.append("finisher dropped to fit your minutes")
            continue
        acc = [b for b in bl if b["kind"] == "accessory"]
        if acc and len(acc[-1]["items"]) > 1:
            gone = acc[-1]["items"].pop()
            notes.append("%s dropped to fit your minutes" % gone["name"])
            continue
        big = [it for b in acc for it in b["items"] if int(it.get("sets") or 1) > 2]
        if big:
            big[-1]["sets"] = 2
            continue
        if acc:
            bl.remove(acc[-1])
            continue
        sec = [it for b in bl if b["kind"] == "secondary" for it in b["items"] if int(it.get("sets") or 1) > 1]
        if sec:
            sec[-1]["sets"] = int(sec[-1]["sets"]) - 1
            continue
        mand = [b for b in bl if b.get("_mandatory")]
        if mand and mand[-1].get("minutes", 0) > 4:
            mand[-1]["minutes"] = 4
            continue
        wu = bl[0]
        if wu["kind"] == "warmup" and wu.get("minutes", 8) > 5:
            wu["minutes"] = 5
            continue
        break
    for b in session["blocks"]:
        for it in b["items"]:
            if it.get("_slot"):
                it["_slot"]["prescribed"]["sets"] = it["sets"]


def recovery(today, prof, bank, tags, date, why, notes):
    walk = "Easy walk outside, or easy bike" if "outdoors" in tags else "Easy bike, row or marching on the spot"
    mob = [r for r in bank.values() if r["pattern"] == "mobility" and allowed(r, prof, tags, set(), 5)][:4]
    items = [{"ex": "walk", "name": walk, "reps": "15 to 20 min", "cue": "you can talk in full sentences the whole time"}]
    items += [{"ex": r["id"], "name": r["name"], "reps": "5 slow reps", "cue": r["cue"]} for r in mob]
    msg = "You said you're ill: no training today. Rest, drink, sleep. Come back when you're better." if why == "ill" else \
        "Energy 3 or lower: today is a rest day. If you want to move, this easy session helps and counts for nothing in your plan."
    return {"date": date, "title": "Rest day", "program": None, "session_id": "rest", "mode": "rest", "level": "rest",
            "level_text": LEVEL_TEXT["rest"], "minutes": 30, "language": prof.get("language", "en"),
            "units": prof.get("units", "kg"), "paper": prof.get("paper", "A4"),
            "blocks": [] if why == "ill" else [{"name": "Optional easy movement", "kind": "warmup", "format": "straight",
                                                "minutes": 25, "items": items}],
            "why": msg, "score_to_beat": "", "log": [], "notes": " ".join(notes), "rest_day": True}


def travel(today, prof, plan, st, bank, tags, avoid, date, notes):
    m = core.load_module("travel")
    tpl = copy.deepcopy(m["session"])
    blocks = []
    tmp_state = {"slots": {}}
    for b in tpl["blocks"]:
        items = [it for it in (slot_item(sl, b, prof, tmp_state, bank, tags, avoid, "standard", {"deload": None}, (False, None), notes, today)
                               for sl in b["slots"]) if it]
        for it in items:
            it["_slot"]["travel"] = True
        if items:
            nb = {"name": b["name"], "kind": b["kind"], "format": b.get("format", "straight"), "items": items}
            if b.get("rest_after_round"):
                nb["rest_after_round"] = b["rest_after_round"]
            blocks.append(nb)
    if {"60_74": 1, "75_plus": 1}.get(prof.get("age_band")):
        m2 = core.load_module("balance")
        for b in m2["session"]["blocks"]:
            items = [it for it in (slot_item(sl, dict(b, kind="finisher"), prof, tmp_state, bank, tags, avoid, "standard",
                                             {"deload": None}, (False, None), notes, today) for sl in b["slots"]) if it]
            for it in items:
                it["_slot"]["travel"] = True
            if items:
                blocks.append({"name": m2["name"], "kind": "finisher", "format": b.get("format", "straight"), "items": items, "_mandatory": True})
    blocks.insert(0, warmup(blocks, bank, tags, 30, prof, avoid))
    s = {"date": date, "title": tpl.get("title", "Travel session"), "program": plan["program"], "program_name": m["name"],
         "session_id": "travel", "mode": "travel", "block": st.get("block", 1), "week": st.get("week", 1), "level": "standard",
         "level_text": "travel day: nothing progresses", "minutes": int(today.get("minutes") or 30),
         "language": prof.get("language", "en"), "units": prof.get("units", "kg"), "paper": prof.get("paper", "A4"),
         "blocks": blocks, "score_to_beat": "keep moving: this day keeps the habit, your loads wait for you",
         "why": "Your main lifts need equipment you don't have today, so this is the travel session.",
         "low_energy": "Do the first round only.", "log": ["Done as written? If not, what changed"], "notes": " ".join(notes)}
    fit(s, s["minutes"], notes)
    return s
