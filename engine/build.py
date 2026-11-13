"""build.py · today's session, built by rule from the program file, the bank, the state and today's readiness.

The coach never writes a session by hand. It runs `plan.py build`, then only translates and
personalises the words (title, why, cues) before the sheet is rendered. Every number here
comes from a program file, a rule in progress.py, or the person's own log.
"""
import copy, datetime, math, re
import core, progress, coach
from sheet import session_seconds, block_seconds, TOLERANCE

LOWER = {"squat", "hinge", "lunge", "calves", "hamstrings_iso", "quads_iso", "glutes_iso"}
NOT_LOADABLE = {"bodyweight", "band", "time", "distance", "calories"}
GYM_DB = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 50]
GYM_KB = [8, 12, 16, 20, 24, 28, 32, 40, 48]
GYM_DB_LB = [5, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 90, 100]   # a US dumbbell rack
GYM_KB_LB = [10, 15, 20, 25, 30, 35, 40, 45, 50, 53, 62, 70, 80, 88, 97, 106]
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


LEVEL_TEXT = {"planned": "a normal day", "standard": "a steady day, nothing all out",
              "light": "a light day: fewer sets, a little lighter", "rest": "rest day"}


# · choosing an exercise

# What most often sets each region off, used when the person gave a status but no trigger (the coach asks to confirm).
DEFAULT_TRIGGERS = {"shoulder": ["overhead"], "neck": ["overhead"], "knee": ["kneeling", "impact"], "hip": ["kneeling"],
                    "low_back": ["bending"], "elbow": ["gripping"], "wrist": ["gripping"], "ankle": ["impact"]}


def lim_triggers(lim):
    """The stored triggers, or the region's usual ones for a limit given with a status (02_INTERVIEW.md Round 4).
    A limit without a status (an older profile, or pain logged after a session) has none: its region stays out."""
    if lim.get("triggers"):
        return list(lim["triggers"])
    if lim.get("status") in ("now", "mild", "unchecked"):
        return list(DEFAULT_TRIGGERS.get(lim.get("region"), []))
    return []


def _narrowed(lim):
    """A limit with triggers (what sets it off) swaps only those moves, unless it flared up since."""
    return bool(lim_triggers(lim)) and not lim.get("flare") and lim.get("status") != "cleared"


def avoid_regions(prof, today):
    """Regions left out completely: a limit marked exclude with no trigger stored (or one that flared up in a
    session), or pain today over 3, sharp or lasting. A limit with triggers never bans its region: it swaps the
    moves that set it off (trigger_limits, doctrine/01_SAFETY.md)."""
    out = set()
    for lim in prof.get("limits", []):
        if lim.get("exclude", True) and lim.get("region") and not _narrowed(lim):
            out.add(lim["region"])
    for p in (today or {}).get("pain") or []:
        if p.get("region") and (p.get("score", 0) > 3 or p.get("sharp") or p.get("days", 0) >= 10):
            out.add(p["region"])
    return out


def care_regions(prof, today):
    """Regions trained with care: an old injury that is cleared, mild pain today (3 or less), or a limit narrowed
    by its triggers. Care means: no impact on that region, and nothing above level 3 that loads it."""
    out = {l["region"] for l in prof.get("limits", []) if l.get("region") and (not l.get("exclude", True) or _narrowed(l))}
    out |= {p["region"] for p in (today or {}).get("pain") or [] if p.get("region") and p.get("score", 0) <= 3
            and not p.get("sharp") and p.get("days", 0) < 10}
    return out


def trigger_limits(prof):
    """[(region, {triggers})] for every limit narrowed by what sets it off (02_INTERVIEW.md Round 4)."""
    return [(l["region"], set(lim_triggers(l))) for l in prof.get("limits", []) if l.get("region") and _narrowed(l)]


# What a move asks of the body, in the interview's trigger words (core.TRIGGERS).
OVERHEAD = {"thruster", "db_thruster", "kb_clean_and_press", "devil_press", "wall_ball", "overhead_carry", "turkish_get_up",
            "overhead_squat", "band_shoulder_dislocate", "overhead_db_triceps_extension", "cable_overhead_extension",
            "seated_overhead_triceps_extension"}
BENDING = {"barbell_row", "pendlay_row", "t_bar_row", "burpee", "burpee_broad_jump", "kb_swing", "single_leg_rdl", "good_morning"}
TWISTING = {"thoracic_rotation", "seated_thoracic_rotation", "seated_band_rotation", "med_ball_slam", "worlds_greatest_stretch"}


def row_triggers(row):
    p, i, t = row["pattern"], row["id"], set()
    if p in ("v_push", "v_pull", "olympic") or i in OVERHEAD:
        t.add("overhead")
    if p in ("hinge", "olympic", "flexion") or i in BENDING:
        t.add("bending")
    if row["impact"] or p == "jump":
        t.add("impact")
    if p in ("squat", "lunge") or "kneel" in i:
        t.add("kneeling")
    if p in ("carry", "h_pull", "v_pull", "biceps", "olympic") or (p == "hinge" and row["load_type"] in ("barbell", "dumbbell", "kettlebell")):
        t.add("gripping")
    if i in TWISTING or "rotation" in i or "twist" in i or "chop" in i:
        t.add("twisting")
    return t


def allowed(row, prof, tags, avoid, cap):
    flags = set((prof.get("screen") or {}).get("flags", []))
    if not core.has_equipment(row, tags):
        return False
    if row["needs_coaching"] and "olympic_coached" not in prof.get("skills", []):
        return False
    if set(row["regions"]) & avoid:
        return False
    for reg, trig in prof.get("_trig") or []:
        if (reg in row["regions"] and row_triggers(row) & trig) or ("impact" in trig and row["impact"]):
            return False                                   # the move that sets it off is swapped, the region stays
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
    if row["id"] in (prof.get("_skip") or ()):          # swapped out for today, at their ask (today.json swap)
        return False
    return True


# When a limit empties a pattern, the nearest pattern that trains the same job (a coach swaps the move, not the day).
SIBLING = {"v_push": "h_push", "v_pull": "h_pull", "h_push": "v_push", "h_pull": "v_pull", "hinge": "glutes_iso", "lunge": "squat",
           "squat": "lunge", "olympic": "hinge", "jump": "squat", "throw": "h_push", "flexion": "anti_ext", "anti_rot": "anti_ext"}


def select(slot, prof, tags, avoid, bank, offset=0):
    bad = set().union(*[DISLIKE_TYPES.get(d, set()) for d in prof.get("dislikes", [])]) if prof.get("dislikes") else set()
    if bad:
        pick = _select(slot, prof, tags, avoid, bank, offset, bad)
        if pick:
            return pick
    pick = _select(slot, prof, tags, avoid, bank, offset, set())
    if pick is None and (avoid or prof.get("_trig") or prof.get("_skip")) and slot.get("pattern") in SIBLING:
        sib = dict(slot, pattern=SIBLING[slot["pattern"]], prefer=[], muscles=None)
        pick = _select(sib, prof, tags, avoid, bank, offset, bad) or _select(sib, prof, tags, avoid, bank, offset, set())
    return pick


def theirs_prof(prof):
    """Their own exercise, in a routine they brought (mode improve): never refused for its level, a pull-up they
    already do, a standing limit, or a liked kit type. Those become proposals (engine/improve.py). Today's pain,
    the screen's flags, coaching gates and the kit still decide the day, and the sheet says so."""
    return dict(prof, _trig=[], _care=prof.get("_care_today") or set(), skills=list(prof.get("skills") or []) + ["pullup"])


def ex_ok(slot, row, prof, tags, avoid):
    if slot.get("theirs") and row["id"] in slot.get("prefer", []):
        return allowed(row, theirs_prof(prof), tags, avoid, 5)
    return allowed(row, prof, tags, avoid, core.LEVEL_CAP[prof.get("experience", "none")] + 1)


def _select(slot, prof, tags, avoid, bank, offset, bad):
    if slot.get("theirs"):
        for i in slot.get("prefer", []):
            if i in bank and ex_ok(slot, bank[i], prof, tags, avoid):
                return i
        slot = dict(slot, prefer=[])
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
    lb = units == "lb"                             # pound users train on a pound grid: 5 lb plates, a 45 lb bar, a pound rack
    rack_db = [core.lb_to_kg(x) for x in GYM_DB_LB] if lb else GYM_DB
    rack_kb = [core.lb_to_kg(x) for x in GYM_KB_LB] if lb else GYM_KB
    if lt == "dumbbell":
        steps = sorted(prof.get("dumbbells") or rack_db)
    elif lt == "kettlebell":
        steps = sorted(prof.get("kettlebells") or rack_kb)
    else:
        steps = None
    step = prof.get("plate_step", 5 if lb else 2.5) if lt == "barbell" else (5 if lb else 2.5)
    step = core.lb_to_kg(step) if lb else step       # plate_step is said in the person's unit
    bar = core.lb_to_kg(45) if lb else 20.0

    def rnd(kg):
        if kg is None:
            return None
        if steps:
            below = [s for s in steps if s <= kg + 1e-9]
            return below[-1] if below else steps[0]
        v = core.kg_round_down(kg, step)
        return max(v, bar) if lt == "barbell" else v

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
    """One week into the queue. A composed plan (engine/compose.py) has streams and an order: each stream takes
    its next sessions in its own rotation, so every session of every component comes round in turn."""
    if plan.get("streams"):
        rot = st.setdefault("rotation", {})
        q = []
        for idx in plan["order"]:
            s = plan["streams"][idx]
            k = rot.get(str(idx), 0)
            sid = s["rotation"][k % len(s["rotation"])]
            rot[str(idx)] = k + 1
            q.append(sid if s["kind"] == "lead" else "%s:%s:%s" % ("mod" if s["kind"] == "module" else "prog", s["id"], sid))
        st["queue"] = q
        return
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


def _prefix(plan, pid):
    return next((s.get("prefix", "") for s in (plan or {}).get("streams", []) if s["kind"] == "program" and s["id"] == pid), "")


def session_template(prog, sid, minutes, force_express=False, plan=None):
    """The normal session, always, so every lift of the rotation comes round. The express version only when
    the normal one cannot be cut to fit the minutes (build() retries with force_express). A day of another
    component is a module session ("mod:id:session") or another program's session ("prog:id:session"), whose
    slot keys carry the stream's prefix so their progress never mixes with the lead program's."""
    if sid.startswith("mod:"):
        _, mid, s = sid.split(":", 2)
        m = core.load_module(mid)
        return copy.deepcopy(m["sessions"][s]), "module"
    if sid.startswith("prog:"):
        _, pid, s = sid.split(":", 2)
        tpl = copy.deepcopy(core.load_program(pid)["sessions"][s])
        pre = _prefix(plan, pid)
        for b in tpl["blocks"]:
            for sl in b["slots"]:
                sl["key"] = pre + sl["key"]
        return tpl, "component"
    if force_express and prog.get("express"):
        return copy.deepcopy(prog["express"]), "express"
    return copy.deepcopy(prog["sessions"][sid]), "normal"


def session_tags(prog, sid):
    if sid.startswith("mod:"):
        _, mid, s = sid.split(":", 2)
        return set(core.load_module(mid)["sessions"][s].get("tags", []))
    if sid.startswith("prog:"):
        _, pid, s = sid.split(":", 2)
        return set(core.load_program(pid)["sessions"][s].get("tags", []))
    return set(prog["sessions"][sid].get("tags", []))


def pick_session(st, prog, plan, today):
    if not st.get("queue"):
        refill(st, prog, plan)
    q = st["queue"]
    bad = set()
    if today.get("hard_cardio_24h"):
        bad |= {"heavy_legs", "power", "hard_cardio"}
    for i, sid in enumerate(q):
        if not (session_tags(prog, sid) & bad):
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
    theirs = bool(slot.get("theirs")) and bool(slot.get("prefer"))
    if theirs and st.get("ex") not in slot["prefer"]:
        st["ex"] = slot["prefer"][0]                    # their exercise is the slot's, whatever today allows
    ex = st.get("ex")
    if theirs and st.get("harder"):                     # their routine: the next step is a proposal, never a switch
        if bank.get(ex, {}).get("harder"):
            st["ready_harder"] = True
            notes.append("%s: top of your range. The next step is waiting in your routine's proposals." % _own(slot, bank[ex]))
        st["harder"] = False
    if ex and st.get("harder") and bank.get(ex, {}).get("harder"):
        h, seen = bank[ex]["harder"], set()
        while h and h in bank and h not in seen and not allowed(bank[h], prof, tags, avoid, core.LEVEL_CAP[prof.get("experience", "none")] + 1):
            seen.add(h)
            h = bank[h].get("harder")
        if h and h in bank and h not in seen:
            notes.append("%s moves up a step: %s." % (bank[ex]["name"], bank[h]["name"]))
            st.update({"ex": h, "load": None, "target": None, "found": None})
            ex = h
        else:
            notes.append("%s: top step for your kit. Make it harder with a 3 second lowering and a pause." % bank[ex]["name"])
        st["harder"] = False
    today_ex = ex if ex and ex in bank and ex_ok(slot, bank[ex], prof, tags, avoid) else None
    if today_ex is None:
        today_ex = select(slot, prof, tags, avoid, bank, offset)
        if today_ex is None:
            return None
        if not ex:
            st["ex"] = today_ex
        elif ex != today_ex and theirs:
            notes.append("%s is not possible today (your kit or what hurts today): %s instead, today only. Your routine keeps %s."
                         % (_own(slot, bank.get(ex, {"name": ex})), bank[today_ex]["name"], _own(slot, bank.get(ex, {"name": ex}))))
        elif ex != today_ex:
            notes.append("%s swapped for %s today." % (bank.get(ex, {}).get("name", ex), bank[today_ex]["name"]))
    elif theirs and not allowed(bank[today_ex], prof, tags, avoid, 5):
        regs = sorted({l["region"].replace("_", " ") for l in prof.get("limits", []) if l.get("region") in bank[today_ex]["regions"]})
        notes.append("Your %s: you kept %s in your routine. Go by feel, and stop the set if it hurts." % (" and ".join(regs) or "limit", _own(slot, bank[today_ex])))
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
    if rule == "run_volume" and "long" in key:          # the long run is never shorter than the week's easy run
        easy = [v.get("minutes") for k, v in st_slots.items() if "easy" in k and isinstance(v, dict) and v.get("minutes")]
        if easy and use.get("minutes", slot.get("start_minutes", 20)) < max(easy):
            use["minutes"] = max(easy)
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
        effort = "easy and crisp, %s reps spare" % d.get("rir", "4")
    elif meso_w is not None and block["kind"] in (prog.get("meso") or {}).get("applies_to", []):
        m = prog["meso"]
        w = min(meso_w, len(m["rir_by_week"]) - 1)
        effort = "%s reps spare" % m["rir_by_week"][w]
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
        load_text = ("band: " + use["band"]) if use.get("band") else "a band that leaves 2 to 3 reps spare"
    first = None
    if (pr.get("first_outing") or (ctx["loadable"] and load is None and rule not in ("benchmark", "run_volume", "c25k_week", "fixed"))):
        first = pr.get("text") or progress.first_outing_text(row["load_type"], reps)
        if rule in ("tm_wave", "rpe_top_set"):
            sets = 1 if rule == "tm_wave" else sets
        elif prof.get("experience") in ("none", "novice"):
            sets = min(sets, 2)          # session one is short on purpose (doctrine/05_LOADS.md rule 7)
            effort = "about 3 reps spare: today you find your weight"
        else:
            effort = "about 2 reps spare: find your weight on the first set, then the rest at it"
    if rule in ("run_volume", "c25k_week"):
        load_text = ""
    shown = slot["own_name"] if slot.get("own_name") and today_ex == slot["prefer"][0] else row["name"]
    item = {"ex": today_ex, "name": shown, "key": key, "sets": sets, "reps": reps, "load": load_text,
            "effort": effort, "rest": slot.get("rest", 90), "cue": "your usual form" if shown != row["name"] else row["cue"],
            "demo": "https://www.youtube.com/results?search_query=" + re.sub(r"\s+", "+", shown) + "+exercise+form",
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


def _own(slot, row):
    return slot.get("own_name") if slot.get("own_name") and row.get("id") in slot.get("prefer", []) else row.get("name", "")


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
    head = {"amrap": "As many rounds as you can in %d min" % slot.get("minutes", 12),
            "fortime": "As fast as you can, stop at %d min" % slot.get("minutes", 15),
            "emom": "A set at the start of every minute, %d min" % slot.get("minutes", 12), "intervals": "Intervals, %d min" % slot.get("minutes", 10)}.get(fmt, fmt)
    if all("run" in m.lower() and "station" not in m.lower() for m in moves) and len(moves) == 1:
        head = "Run, about %d min" % slot.get("minutes", 40)   # a run is never "for time" on the sheet (08 root cause 11)
    pr = progress.bench_prescribe(slot, st, {})
    item = {"ex": "piece", "name": head, "key": slot["key"], "sets": 1, "reps": " · ".join(moves), "load": "",
            "effort": slot.get("effort", "steady, then hard in the last third"), "rest": 0,
            "cue": slot.get("cue", "too hard? lighter first, then fewer reps, then an easier move, to keep the pace"),
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


PATTERN_WORDS = {"h_push": "the press", "v_push": "the overhead press", "h_pull": "the row", "v_pull": "the pull-up or pull-down",
                 "squat": "the squat", "hinge": "the hinge", "lunge": "the lunge", "biceps": "curls", "triceps": "triceps work",
                 "delts": "lateral raises", "rear_delts": "rear shoulder work", "calves": "calf raises", "hamstrings_iso": "leg curls",
                 "quads_iso": "leg extensions", "glutes_iso": "glute work", "anti_ext": "core work", "anti_rot": "core work",
                 "flexion": "core work", "carry": "the carry", "cyclic": "the cardio", "olympic": "the Olympic lift",
                 "balance": "balance work", "mobility": "mobility", "jump": "jumps", "throw": "throws", "locomotion": "crawls"}
FILL_PREFER = {"biceps": ["incline_db_curl", "db_curl", "cable_curl", "band_curl"], "triceps": ["cable_overhead_extension", "overhead_db_triceps_extension", "rope_pushdown", "band_pushdown"],
               "v_pull": ["lat_pulldown", "chin_up", "assisted_pull_up", "band_lat_pulldown"], "h_pull": ["chest_supported_row", "seated_cable_row", "db_row", "band_row"],
               "h_push": ["incline_db_press", "db_bench_press", "push_up", "band_chest_press"], "delts": ["lateral_raise", "cable_lateral_raise", "band_lateral_raise"],
               "rear_delts": [], "hinge": ["hip_thrust", "glute_bridge", "db_romanian_deadlift"], "quads_iso": [], "hamstrings_iso": [],
               "anti_ext": ["dead_bug", "plank"], "calves": []}


def _words(slot):
    return PATTERN_WORDS.get(slot.get("pattern"), "one move")


def _is_lifting(blocks):
    return any(b["kind"] in ("main", "secondary", "accessory") and any(it.get("_slot", {}).get("rule") not in
               ("run_volume", "c25k_week", "benchmark") and it.get("ex") != "piece" for it in b["items"]) for b in blocks)


def _module_blocks(mid, prof, st, bank, tags, avoid, level, prog, deload, today, goal=False):
    m = core.load_module(mid)
    sess = m.get("session") or (m.get("sessions") or {}).get((m.get("order") or ["easy"])[0])
    out = []
    for b in (sess or {}).get("blocks", []):
        items = [it for it in (slot_item(sl, dict(b, kind="finisher"), prof, st, bank, tags, avoid, level, prog, (deload, None), [], today)
                               for sl in b["slots"]) if it]
        if items:
            nb = {"name": m["name"], "kind": "finisher", "format": b.get("format", "straight"), "items": items,
                  "_module": mid, "_mandatory": mid == "balance", "_goal": goal}
            for k in ("rest_after_round", "minutes"):
                if b.get(k):
                    nb[k] = b[k]
            out.append(nb)
    return out


def apply_targets(blocks, plan, prof, st, bank, tags, avoid, level, prog, deload, today, notes):
    """Weekly set targets (the priority area, or a balance fix from the coach's eye), spread over the lifting
    sessions of the week: sets added to an accessory that already trains the muscle, else a new accessory from
    the bank. Every added set is marked, so the clock cuts it last (doctrine/06_BUILD.md)."""
    lift_days = max(1, int(plan.get("lift_days") or plan.get("days") or 3))
    new = []
    for t in plan.get("targets") or []:
        parts = t.get("parts") or []
        if not parts:
            continue
        per = max(1, math.ceil(float(t.get("weekly", 6)) / len(parts) / lift_days))
        for muscle, pattern in parts:
            cands = [it for b in blocks if b["kind"] in ("accessory", "secondary") for it in b["items"]
                     if muscle in (it.get("_slot", {}).get("muscles") or []) and it.get("ex") in bank and bank[it["ex"]]["pattern"] == pattern]
            add = per
            for it in cands:
                room = 5 - int(it.get("sets") or 1)
                if room <= 0:
                    continue
                k = min(room, add)
                it["sets"] = int(it["sets"]) + k
                it["_priority"] = t["area"]
                it["_slot"]["pri_added"] = it["_slot"].get("pri_added", 0) + k
                add -= k
                if not add:
                    break
            if add:
                slot = {"key": "pri_%s" % muscle, "pattern": pattern, "muscles": [muscle], "prefer": FILL_PREFER.get(pattern, []),
                        "sets": max(2, add), "reps": "10-15", "rest": 60, "effort": "2 reps spare", "rule": "double_progression"}
                it = slot_item(slot, {"kind": "accessory"}, prof, st, bank, tags, avoid, level, prog, (deload, None), notes, today)
                if it is None:
                    notes.append("No move for your %s fits your kit or limits today." % muscle.replace("_", " "))
                    continue
                if any(x["ex"] == it["ex"] for b in blocks for x in b["items"]):
                    continue
                it["_priority"] = t["area"]
                it["_slot"]["pri_added"] = int(it["sets"])
                new.append(it)
    if new:
        areas = list(dict.fromkeys(it["_priority"] for it in new))
        name = "Priority: " + " and ".join("pulling" if a == "pull" else a for a in areas)
        blocks.append({"name": name, "kind": "accessory", "format": "straight", "items": new, "_priority": True})


def build(today, prof, plan, st, bank, date=None):
    date = date or core.today()
    prog = core.load_program(plan["program"])
    level, why_level, refer = readiness(today)
    week_plan = coach.week_plan(st, date or core.today())  # what the weekly check-in set for this week
    minutes = int(today.get("minutes") or week_plan.get("minutes") or prof.get("minutes", 45))
    tags = core.place_tags(prof, today.get("place"))
    if today.get("equipment"):
        tags = core.expand_equipment(today["equipment"])
    avoid = avoid_regions(prof, today)
    care_today = {p["region"] for p in (today or {}).get("pain") or [] if p.get("region") and p.get("score", 0) <= 3
                  and not p.get("sharp") and p.get("days", 0) < 10} - avoid
    prof = dict(prof, _care=care_regions(prof, today) - avoid, _trig=trigger_limits(prof), _care_today=care_today,
                _skip={x for x in (today or {}).get("swap") or [] if isinstance(x, str)})
    own = prog.get("family") == "own"                   # their own routine (engine/improve.py): nothing of it changes unasked
    short_day = own and int(today.get("minutes") or 0) and int(today["minutes"]) < int(prof.get("minutes", 45))
    notes = []
    if "symptoms_reported" in (prof.get("screen") or {}).get("flags", []):
        notes.append("If chest pain, dizziness or fainting happens: stop and get medical help.")
    if refer:
        notes.append("Sharp, worsening or lasting pain (%s): that area is left out. Please see a physiotherapist or doctor before loading it again."
                     % ", ".join(refer))
    for reg, trig in ([] if own else prof["_trig"]):    # their own routine: each kept move says it on its own line
        guessed = not any(l.get("triggers") for l in prof.get("limits", []) if l.get("region") == reg)
        notes.append("Your %s: the moves that %sset it off (%s) are swapped for ones that leave it alone; the rest is trained with care.%s"
                     % (reg.replace("_", " "), "usually " if guessed else "", ", ".join(sorted(TRIGGER_WORDS.get(t, t) for t in trig)),
                        " Tell the trainer what sets yours off and only those moves are swapped." if guessed else ""))
    gap, back = coach.back_tier(st, date)               # the missed week (doctrine/07_CYCLE.md)
    if back in ("two_weeks", "long"):
        today = dict(today, _restart=True)
        st["reentry"] = 2                               # today 15 percent lighter, then one easy session
        if back == "long":
            st.setdefault("flags", {})["retest"] = True
        notes.append(coach.BACK_LINES[back])
    elif back == "week":
        level = coach.cap_level(level, "light")
        st["reentry"] = 1
        notes.append(coach.BACK_LINES["week"])
    elif st.get("reentry"):
        level = coach.cap_level(level, "light")
        notes.append("One more easy session after your break; full sessions from the next one.")
    if week_plan.get("dose") == "easier" or st.get("block_adjust") == "easier":
        level = coach.cap_level(level, "standard")
    sore = today.get("sore") if today.get("sore") in ("some", "very") else None
    if sore == "very":                                  # soreness is never pain: it lowers the dose, it never removes a region
        level = coach.cap_level(level, "standard")
    tp = coach.taper(prof, date)
    if tp and tp["race_day"]:
        return recovery(today, prof, bank, tags, date, "event", notes)
    if level == "rest":
        return recovery(today, prof, bank, tags, date, why_level, notes)
    st_before = copy.deepcopy(st)
    sid, qi = pick_session(st, prog, plan, today)
    tpl, mode = session_template(prog, sid, minutes, today.get("_express"), plan)
    if plan.get("long_run"):
        for b in tpl["blocks"]:
            for sl in b["slots"]:
                if sl.get("rule") == "run_volume" and "long" in sl.get("key", ""):
                    sl.update({k: v for k, v in plan["long_run"].items() if k in ("max_minutes", "hold_weeks")})
    deload, meso_w = week_info(st, prog)
    blocks = []
    for b in tpl["blocks"]:
        items = []
        for slot in b["slots"]:
            it = slot_item(slot, b, prof, st, bank, tags, avoid, level, prog, (deload, meso_w), notes, today)
            if it is None:
                if b["kind"] == "main" and len(b["slots"]) == 1 and not any(bb["kind"] == "main" and bb is not b for bb in tpl["blocks"]):
                    notes.append("The main lift can't be done with today's equipment or limits: today is the travel session.")
                    return travel(today, prof, plan, st, bank, tags, avoid, date, notes)
                if b["kind"] == "main":
                    notes.append("%s left out today (your equipment or limits); the rest of the main lifts stand." % _words(slot).capitalize())
                    continue
                notes.append("%s left out today: no move for it fits your equipment and limits." % _words(slot).capitalize())
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
    lifting = _is_lifting(blocks)
    if own:
        pass                                            # their sets stay theirs: a priority is a proposal (engine/improve.py)
    elif lifting and plan.get("targets") is not None:
        apply_targets(blocks, plan, prof, st, bank, tags, avoid, level, prog, deload, today, notes)
    elif lifting:                                       # an older plan without weekly targets: the old +1 set rule
        pri = {g for w in prof.get("priority", []) for g in PRIORITY.get(str(w).lower().strip(), [])}
        added = 0
        for b in blocks:
            if b["kind"] != "accessory":
                continue
            for it in b["items"]:
                if added < 2 and pri & set(it["_slot"]["muscles"]):
                    it["sets"] = int(it["sets"]) + 1
                    added += 1
    if st.get("block_adjust") == "harder" and not tp:
        for b in blocks:
            if b["kind"] == "accessory" and not b.get("_priority"):
                for it in b["items"]:
                    it["sets"] = min(5, int(it.get("sets") or 1) + 1)
    sess_tags = set(tpl.get("tags", []))
    run_day = any(it.get("_slot", {}).get("rule") in ("run_volume", "c25k_week") for b in blocks if b["kind"] == "main" for it in b["items"])
    long_day = (plan.get("long_run") or {}).get("protect") and any("long" in it.get("key", "") for b in blocks for it in b["items"])
    has_piece = any(it.get("ex") == "piece" for b in blocks for it in b["items"])
    if has_piece:
        sess_tags.add("hard_cardio")                    # a session that already holds a timed piece takes no second one
    goal_mods = list(plan.get("goal_modules", [])) if (lifting or plan.get("goal_on_all")) and not long_day else []
    nice = [] if mode == "express" else [m for m in plan.get("modules", []) if lifting or m == "mobility"]
    for mid in goal_mods + [m for m in nice if m not in goal_mods]:
        m = core.load_module(mid)
        if m.get("when") != "finisher" and mid not in goal_mods:
            continue
        if "hard_cardio" in (m.get("session") or {}).get("tags", []) and ("hard_cardio" in sess_tags or run_day):
            continue                                    # one hard piece a session, and none after a run
        blocks += _module_blocks(mid, prof, st, bank, tags, avoid, level, prog, deload, today, goal=mid in goal_mods)
    blocks.insert(0, warmup(blocks, bank, tags, minutes, prof, avoid))
    title = tpl.get("title", sid).replace("Express \u00b7 ", "").replace("Short version \u00b7 ", "")
    mains = [it for b in blocks if b["kind"] == "main" for it in b["items"]]
    if prof.get("position") == "seated" or any(n.endswith("swapped for %s today." % it["name"]) for it in mains for n in notes):
        title = " · ".join(it["name"] for it in mains[:3]) or title
    session = {"date": date, "title": title, "program": prog["id"], "program_name": plan.get("plain_name") or PLAIN_FAMILY.get(prog["family"], "Your plan"),
               "session_id": sid, "mode": mode, "block": st.get("block", 1), "week": st.get("week", 1),
               "deload": deload, "level": level, "level_text": LEVEL_TEXT[level], "energy": today.get("energy"),
               "weeks": prog.get("block_weeks", 4) + (1 if prog.get("deload") else 0),
               "minutes": minutes, "language": prof.get("language", "en"), "units": prof.get("units", "kg"),
               "paper": prof.get("paper", "A4"), "blocks": blocks}
    if own:
        session["own"] = True
        if short_day:
            before = session_seconds(session)
            fit(session, minutes, notes)                # a shorter day they asked for: cut today only, said on the sheet
            if session_seconds(session) < before:
                notes.append("Shorter today because you asked for %d minutes; your routine stays as it is." % minutes)
        need = int(math.ceil(session_seconds(session) / 60.0))
        if need > minutes + TOLERANCE // 60:
            if not short_day:
                notes.append("Your %s takes about %d minutes as you wrote it, more than your usual %d. The trainer can trim it if you want: "
                             "see your routine's proposals." % (title, need, minutes))
            session["minutes"] = need
        over = False
    else:
        fit(session, minutes, notes)
        over = session_seconds(session) > minutes * 60 + TOLERANCE
    if over:
        over = protect_run(session, minutes, plan, notes)
    if over and mode == "normal" and prog.get("express"):
        st.clear()
        st.update(st_before)                       # undo what the first attempt touched, then build the express version
        return build(dict(today, _express=True), {k: v for k, v in prof.items() if k not in ("_care", "_trig")}, plan, st, bank, date)
    if not over and not session.get("long_run_day") and not tp and not own:
        fill(session, minutes, notes, fill_extras(session, plan, prof, st, bank, tags, avoid, level, prog, deload, today, sess_tags),
             {x["area"] for x in plan.get("targets") or [] if x.get("why") == "priority"})
    lighter = []
    if week_plan.get("dose") == "easier" or st.get("block_adjust") == "easier":
        ease(session, None)
        lighter.append("This week runs a little easier, as agreed at your check-in: one set fewer on the extra moves.")
    if sore:
        areas = [a for a in today.get("sore_areas") or ["all"] if a in SORE_AREAS] or ["all"]
        if sore == "very":
            ease(session, set().union(*(SORE_AREAS[a] for a in areas)))
            lighter.append("Very sore: the main work stays, one set fewer on the extra moves for the sore muscles, and no all-out sets. "
                           "Soreness is not an injury; it eases as you warm up and fades as you keep training.")
        else:
            lighter.append("A bit sore is normal after training: the warm-up eases it. Train as written.")
    if tp:
        taper_session(session, tp, notes)
        session["minutes"] = minutes
    notes += lighter
    if lighter or tp:
        session["lighter"] = True
    for b in session["blocks"]:
        for it in b["items"]:
            if it.get("_slot"):
                it["_slot"]["prescribed"]["sets"] = it["sets"]
    score = next((it["_slot"]["beat"] for b in session["blocks"] for it in b["items"]
                  if it.get("_slot", {}).get("score") and it["_slot"].get("beat")), None)
    session["score_to_beat"] = score or "first time on this session: today sets the numbers you will beat"
    main_names = [it["name"] for b in session["blocks"] if b["kind"] == "main" for it in b["items"]]
    pos = "Session %d of %d this week" % (st.get("week_sessions", 0) + 1, plan["days"])
    total = prog.get("block_weeks", 4) + (1 if prog.get("deload") else 0)
    session["why"] = "%s. Week %d of %d%s. Today's main work: %s. Energy %s: %s." % (
        pos, min(st.get("week", 1), total), total, " (an easy week: lighter on purpose, so you come back stronger)" if deload else "",
        ", ".join(main_names[:2]) or "the timed piece", today.get("energy", "?"), LEVEL_TEXT[level])
    ev = prof.get("event") or {}
    try:
        wk = (datetime.date.fromisoformat(ev.get("date", "")) - datetime.date.fromisoformat(date)).days // 7
        if wk >= 0:
            session["why"] += " %d weeks to %s." % (wk, ev.get("name") or "your event")
    except ValueError:
        pass
    if tp:
        session["why"] += " Easing off before your event: less work, the same weights, so you arrive fresh."
    elif coach.tests_due(plan, st, prof, date):
        notes.append("This week: your starting numbers, a few minutes of simple tests the trainer gives you. They show how far you come.")
    if plan.get("challenge"):
        ch = plan["challenge"][(st.get("block", 1) - 1) % len(plan["challenge"])]
        session["why"] += " This month's challenge: %s." % ch
    session["low_energy"] = "Finish the main lifts, do one extra move, skip the last part, and log what you did."
    session["log"] = log_lines(session)
    session["notes"] = " ".join(dict.fromkeys(notes))
    session["_queue_index"] = qi
    import eye
    session["coach_eye"] = eye.session_checks(session, plan, prof)
    return session


SORE_AREAS = {"legs": {"quads", "hamstrings", "glutes", "calves", "adductors"},
              "upper": {"chest", "lats", "upper_back", "front_delts", "side_delts", "rear_delts", "biceps", "triceps", "forearms"},
              "core": {"core", "obliques", "lower_back"}}
SORE_AREAS["all"] = set().union(*SORE_AREAS.values())


def ease(session, muscles):
    """One set fewer on the accessories (all of them, or those hitting these muscles). The main work is never touched."""
    for b in session["blocks"]:
        if b["kind"] != "accessory":
            continue
        for it in b["items"]:
            sl = it.get("_slot") or {}
            if muscles is None or muscles & set(sl.get("muscles", [])):
                it["sets"] = max(1, int(it.get("sets") or 1) - 1)


def taper_session(session, tp, notes):
    """The last weeks before an event: less volume, the same weights and effort (doctrine/07_CYCLE.md, the taper).
    Sets and run minutes take the taper's share; hard finishers go; nothing is added to fill the time."""
    f = tp["volume"]
    keep = []
    for b in session["blocks"]:
        if b["kind"] == "finisher" and b.get("_module") not in ("mobility", "core"):
            continue
        for it in b["items"]:
            sl = it.get("_slot") or {}
            if sl.get("rule") == "run_volume" and it.get("work"):
                m = max(15, int(round(it["work"] / 60.0 * f)))
                it["reps"], it["work"] = "%d min" % m, m * 60
            elif b["kind"] in ("main", "secondary", "accessory") and it.get("sets") and sl.get("rule") != "benchmark":
                it["sets"] = max(1, int(math.ceil(int(it["sets"]) * f)))
        keep.append(b)
    session["blocks"] = keep
    session.pop("long_run_day", None)
    notes[:] = [n for n in notes if not n.startswith("Long run day")]
    session["taper"] = tp
    notes.append("Easing off: %d days to %s. About %d percent of your usual work, at the same weights and effort, so you arrive fresh. "
                 "Do not add anything: the fitness is already in the bank." % (tp["days"], tp["event"], round(100 * f)))


PLAIN_FAMILY = {"strength": "Strength", "powerbuild": "Strength and size", "muscle": "Muscle", "weightlifting": "Olympic lifting",
                "functional": "Mixed fitness", "hyrox": "HYROX", "hybrid": "Strength and running", "run": "Running",
                "health": "Full body strength"}
TRIGGER_WORDS = {"bending": "bending forward", "overhead": "reaching overhead", "impact": "jumping or running",
                 "kneeling": "kneeling or deep squats", "gripping": "gripping", "twisting": "twisting"}


def protect_run(session, minutes, plan, notes):
    """A run session over the minutes is never swapped for a shorter session. The long run of a running event
    is protected: the sheet takes the minutes it needs and says so. Any other run is trimmed to fit, never under
    15 minutes. Returns True if the session is still over."""
    runs = [it for b in session["blocks"] if b["kind"] == "main" for it in b["items"] if it.get("_slot", {}).get("rule") == "run_volume"]
    if not runs:
        return True
    it = runs[0]
    if "long" in it["key"] and (plan.get("long_run") or {}).get("protect"):
        need = int(math.ceil(session_seconds(session) / 60.0))
        session["long_run_day"] = {"asked": minutes, "needs": need}
        session["minutes"] = need
        notes.append("Long run day: about %d minutes in all today. Put it on the day you have the time; it is the run your event is built on." % need)
        return False
    spare = minutes * 60 + TOLERANCE - (session_seconds(session) - int(it.get("work") or 0))
    new = max(15, int(spare // 60) - 1)
    it["reps"], it["work"] = "%d min" % new, new * 60
    notes.append("%s cut to %d minutes to fit your time today." % (it["name"], new))
    return session_seconds(session) > minutes * 60 + TOLERANCE


def fill_extras(session, plan, prof, st, bank, tags, avoid, level, prog, deload, today, sess_tags):
    """What may be added when the session is short of the minutes: a second variation of the main lift for a
    lifting goal, then core, then conditioning for fitness and fat-loss goals, then mobility."""
    have = {b.get("_module") for b in session["blocks"]}
    lifting = _is_lifting(session["blocks"])
    out = []
    goals = {prof.get("goal"), prof.get("goal2")}
    if lifting and goals & {"muscle", "strength", "powerlifting", "health", "fat_loss", None} - {None}:
        first = next((it for b in session["blocks"] if b["kind"] in ("main", "secondary") for it in b["items"]
                      if it.get("_slot", {}).get("rule") not in ("run_volume", "c25k_week", "benchmark") and it.get("ex") in bank), None)
        if first:
            pat = bank[first["ex"]]["pattern"]
            used = {it.get("ex") for b in session["blocks"] for it in b["items"]}
            slot = {"key": "fill_%s" % pat, "pattern": pat, "sets": 3, "reps": "8-12", "rest": 90, "rule": "double_progression",
                    "effort": "2 reps spare"}
            for off in range(6):
                i = select(slot, prof, tags, avoid, bank, off)
                if i and i not in used:
                    slot["prefer"], slot["key"] = [i], "fill_" + i        # its own progress, one key per move
                    it = slot_item(slot, {"kind": "accessory"}, prof, st, bank, tags, avoid, level, prog, (deload, None), [], today)
                    if it:
                        out.append({"name": "More %s" % PATTERN_WORDS.get(pat, "volume").replace("the ", ""), "kind": "accessory",
                                    "format": "straight", "items": [it], "_fill": True})
                    break
    run_day = any(it.get("_slot", {}).get("rule") in ("run_volume", "c25k_week") for b in session["blocks"] for it in b["items"])
    if (run_day and not lifting) or goals & {"fat_loss", "health"} or dict(plan.get("blend") or []).get("conditioning"):
        cw = next((i for i in ("walk", "incline_walk", "bike_erg", "row_erg") if i in bank and allowed(bank[i], prof, tags, avoid, 5)), None)
        if cw:
            out.append({"name": "Easy cardio to finish", "kind": "finisher", "format": "run", "_fill": True, "_stretch": True,
                        "items": [{"ex": cw, "name": bank[cw]["name"], "sets": 1, "reps": "10 min", "work": 600, "load": "", "rest": 0,
                                   "effort": "easy: you can talk in full sentences", "cue": bank[cw]["cue"], "_regions": bank[cw]["regions"]}]})
    for mid in ("core", "conditioning", "mobility"):
        if mid in have:
            continue
        if mid == "core" and not lifting and sess_tags & {"hard_cardio"}:
            continue
        if mid == "conditioning" and (not lifting or "hard_cardio" in sess_tags or not (goals & {"fat_loss", "health", "functional", "hyrox"}
                                                                                       or dict(plan.get("blend") or []).get("conditioning"))):
            continue
        for b in _module_blocks(mid, prof, st, bank, tags, avoid, level, prog, deload, today):
            b["_fill"] = True
            out.append(b)
    return out


def fill(session, minutes, notes, extras, areas=()):
    """The minutes are a target as well as a ceiling: a session more than 10 percent short gets sets back on the
    priority and the accessories, then whole blocks from `fill_extras`, as long as it stays inside the minutes."""
    low, cap = 0.9 * minutes * 60, minutes * 60 + TOLERANCE

    def short():
        return session_seconds(session) < low

    def try_sets(items, ceiling):
        changed = False
        for it in items:
            if not short():
                break
            if int(it.get("sets") or 1) >= ceiling(it):
                continue
            it["sets"] = int(it["sets"]) + 1
            if session_seconds(session) > cap:
                it["sets"] = int(it["sets"]) - 1
            else:
                changed = True
        return changed

    base = lambda it: int(((it.get("_slot") or {}).get("slot") or {}).get("sets") or it.get("sets") or 1)
    for _ in range(3):
        if not short():
            return
        pri = [it for b in session["blocks"] for it in b["items"] if it.get("_priority") and it["_priority"] in areas]
        acc = [it for b in session["blocks"] if b["kind"] == "accessory" for it in b["items"] if it.get("_slot") and not it.get("_priority")]
        sec = [it for b in session["blocks"] if b["kind"] == "secondary" for it in b["items"]
               if it.get("_slot") and it["_slot"].get("rule") not in ("run_volume", "c25k_week", "benchmark", "tm_wave", "rpe_top_set", "fixed")]
        moved = try_sets(pri, lambda it: 4) | try_sets(acc, lambda it: min(4, base(it) + 1)) | try_sets(sec, lambda it: min(5, base(it) + 1))
        if not moved:
            break
    for b in extras:
        if not short():
            return
        session["blocks"].append(b)
        if b.get("_stretch"):                           # an easy cardio block takes the minutes that are left, 10 to 20
            it = b["items"][0]
            left = int((minutes * 60 - session_seconds(session) + it["work"]) // 60)
            it["work"] = max(10, min(20, left)) * 60
            it["reps"] = "%d min" % (it["work"] // 60)
        if session_seconds(session) > cap:
            session["blocks"].remove(b)
        else:
            notes.append("%s added to use your minutes." % b["name"])


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
                    out.append("%s: heaviest set weight x reps, and how many reps were spare" % it["name"])
                else:
                    out.append("%s: reps on the last set, and how many reps were spare" % it["name"])
    out.append("Anything that hurt (where, 0 to 10)")
    return out[:6]


def fit(session, minutes, notes):
    """The minutes are a ceiling. Cut order (doctrine/06_BUILD.md): nice-to-have finishers, then accessories that
    serve no target, then secondary sets; only then the goal finisher shrinks to its minimum dose, then the
    priority sets go down, then the goal finisher goes (said, with the minutes it needs). The main block is never cut."""
    limit = minutes * 60 + TOLERANCE
    guard = 0
    while session_seconds(session) > limit and guard < 60:
        guard += 1
        bl = session["blocks"]
        fin = [b for b in bl if b["kind"] == "finisher" and not b.get("_mandatory") and not b.get("_goal")]
        if fin:
            bl.remove(fin[-1])
            notes.append("%s left out to fit your minutes." % fin[-1]["name"])
            continue
        acc = [b for b in bl if b["kind"] == "accessory" and not b.get("_priority")]
        free = lambda b: [it for it in b["items"] if not it.get("_priority")]
        cand = [b for b in acc if len(b["items"]) > 1 and free(b)]
        if cand:
            gone = free(cand[-1])[-1]
            cand[-1]["items"].remove(gone)
            notes.append("%s left out to fit your minutes." % gone["name"])
            continue
        big = [it for b in acc for it in free(b) if int(it.get("sets") or 1) > 2]
        if big:
            big[-1]["sets"] = 2
            continue
        whole = [b for b in acc if not any(it.get("_priority") for it in b["items"])]
        if whole:
            bl.remove(whole[-1])
            continue
        half = lambda it: max(1, math.ceil(int(((it.get("_slot") or {}).get("slot") or {}).get("sets") or it.get("sets") or 1) / 2.0))
        sec = [it for b in bl if b["kind"] == "secondary" for it in b["items"] if int(it.get("sets") or 1) > half(it) and not it.get("_priority")]
        if sec:
            sec[-1]["sets"] = int(sec[-1]["sets"]) - 1   # the program's second lift keeps at least half its sets until the targets give way
            continue
        goal = [b for b in bl if b.get("_goal")]
        shrink = [b for b in goal if b.get("minutes", 0) > 6]
        if shrink:
            shrink[-1]["minutes"] = 6                  # the minimum dose of a goal finisher
            for it in shrink[-1]["items"]:
                if it.get("work"):
                    it["work"] = 6 * 60
            continue
        walk = [it for b in bl if b["kind"] == "secondary" for it in b["items"]
                if it.get("_slot", {}).get("rule") == "run_volume" and int(it.get("work") or 0) > 600]
        if walk:
            walk[-1]["work"] = int(walk[-1]["work"]) - 300  # an easy walk gives 5 minutes before a goal block does
            walk[-1]["reps"] = "%d min" % (walk[-1]["work"] // 60)
            continue
        gsets = [it for b in goal for it in b["items"] if int(it.get("sets") or 1) > 2]
        if gsets:
            gsets[-1]["sets"] = 2
            continue
        own = lambda it, b: 2 if b.get("_priority") else max(2, int(((it.get("_slot") or {}).get("slot") or {}).get("sets") or 2))
        pri = [it for b in bl for it in b["items"] if it.get("_priority") and int(it.get("sets") or 1) > own(it, b)]
        if pri:
            pri[-1]["sets"] = int(pri[-1]["sets"]) - 1   # the added sets go, the program's own sets stay
            continue
        pblocks = [b for b in bl if b.get("_priority")]
        if pblocks:
            gone = pblocks[-1]["items"].pop()
            if not pblocks[-1]["items"]:
                bl.remove(pblocks[-1])
            notes.append("%s left out today: the clock ran out. It comes back next session." % gone["name"])
            continue
        sec = [it for b in bl if b["kind"] == "secondary" for it in b["items"] if int(it.get("sets") or 1) > 1]
        if sec:
            sec[-1]["sets"] = int(sec[-1]["sets"]) - 1
            continue
        if goal:
            g = goal[-1]
            bl.remove(g)
            notes.append("%s left out today: it needs about %d more minutes than you have. It is part of your goal, so it is the "
                         "first thing back next time." % (g["name"], max(1, round((session_seconds(session) + block_seconds(g) - limit) / 60))))
            continue
        big = [it for b in bl if b["kind"] == "accessory" for it in b["items"] if int(it.get("sets") or 1) > 2]
        if big:
            big[-1]["sets"] = 2
            continue
        acc_left = [b for b in bl if b["kind"] == "accessory"]
        if acc_left and not any(it.get("_priority") for b in acc_left for it in b["items"]):
            bl.remove(acc_left[-1])
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
        "Event day: no session. Warm up the way you practised, start easy, and enjoy it. Tell the trainer how it went." if why == "event" else \
        "Energy 3 or lower: today is a rest day. If you want to move, this easy session helps and counts for nothing in your plan."
    return {"date": date, "title": "Rest day", "program": None, "session_id": "rest", "mode": "rest", "level": "rest",
            "level_text": LEVEL_TEXT["rest"], "minutes": 30, "language": prof.get("language", "en"),
            "units": prof.get("units", "kg"), "paper": prof.get("paper", "A4"),
            "blocks": [] if why in ("ill", "event") else [{"name": "Optional easy movement", "kind": "warmup", "format": "straight",
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
