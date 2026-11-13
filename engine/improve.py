"""improve.py · coaching inside a routine someone already runs (doctrine/06_BUILD.md, "Their own routine"; research/09).

    adopt(prof, bank)                      their routine (profile current_routine) becomes a program dict, id "mine"
    write_program(prog, bank)              me/PROGRAM.md: their week in plain words, then the json block
    routine_words(prog, bank)              their sessions as they gave them, for the page and the coach
    proposals(prog, prof, plan, st, log, bank)   what the coach would change, each with a reason; nothing applied
    accept(prog, plan, st, pid, ...)       one proposal applied, with their yes, and kept in the ledger
    decline(prog, pid, ...)                one proposal refused, remembered, not asked again while its facts stay

The routine stays theirs: their split, their days in their order, their exercises, their sets and reps. The
engine's own rules (loads, progression, logging, the readiness dose, the coach's habits) run on it unchanged.
Every change the engine would otherwise make by itself is a proposal here: what, why in one plain line, and
yes or no. Standard library only, no network: the web page runs this file in Pyodide.
"""
import copy, difflib, json, math, re, unicodedata
import core

ID = "mine"
NAME = "Your routine, coached"
COMPOUND = {"squat", "hinge", "lunge", "h_push", "v_push", "h_pull", "v_pull", "carry", "olympic"}
PUSH, PULL = {"h_push", "v_push"}, {"h_pull", "v_pull"}
GROUPS = {"chest": ["chest"], "back": ["lats", "upper_back"], "quads": ["quads"], "hamstrings and glutes": ["hamstrings", "glutes"],
          "shoulders": ["side_delts", "front_delts", "rear_delts"]}
GROUP_PATTERN = {"chest": "h_push", "back": "h_pull", "quads": "quads_iso", "hamstrings and glutes": "hamstrings_iso", "shoulders": "delts"}
ADD_PREFER = {"h_pull": ["chest_supported_row", "seated_cable_row", "db_row", "band_row"], "v_pull": ["lat_pulldown", "chin_up", "band_lat_pulldown"],
              "h_push": ["incline_db_press", "db_bench_press", "push_up"], "delts": ["lateral_raise", "cable_lateral_raise", "band_lateral_raise"],
              "rear_delts": ["face_pull", "rear_delt_fly", "band_pull_apart"], "biceps": ["incline_db_curl", "db_curl", "cable_curl", "band_curl"],
              "triceps": ["overhead_db_triceps_extension", "cable_overhead_extension", "rope_pushdown", "band_pushdown"],
              "quads_iso": ["leg_extension", "goblet_squat"], "hamstrings_iso": ["seated_leg_curl", "lying_leg_curl", "db_romanian_deadlift"],
              "hinge": ["hip_thrust", "glute_bridge", "db_romanian_deadlift"], "calves": ["calf_raise", "seated_calf_raise"],
              "anti_ext": ["dead_bug", "plank"]}
# The parent program lends the block rhythm and the easier week; it is never run (research/09 2.3).
PARENT = {"ppl": "muscle-ppl-6", "body_part": "muscle-bodypart-5", "strength_cardio": "hybrid-strength-endurance-4to6",
          "run_plan": "run-base-3to5", "classes": "functional-gpp-3to5"}
RUN_SESSION = {"easy": "E", "intervals": "Q", "long": "L", "cardio": "E"}
LIFT_KINDS = {"push", "pull", "legs", "upper", "lower", "fa", "fb", "fc", "chest", "back", "shoulders", "arms", "strength",
              "d1", "d2", "d3", "d4", "d5", "d6"}
SPLIT_KINDS = {"ppl": ["push", "pull", "legs"], "upper_lower": ["upper", "lower"], "full_body": ["fa", "fb", "fc"],
               "body_part": ["chest", "back", "legs", "shoulders", "arms"], "strength_cardio": ["strength", "cardio"],
               "run_plan": ["easy", "intervals", "long"], "classes": ["class"], "custom": ["d1", "d2", "d3", "d4", "d5", "d6"]}
# What a typed name says about the movement, when no bank row is close enough (their own exercise, kept by name).
WORD_PATTERN = [("pulldown", "v_pull"), ("pull down", "v_pull"), ("pull up", "v_pull"), ("pullup", "v_pull"), ("chin", "v_pull"),
                ("row", "h_pull"), ("face pull", "rear_delts"), ("rear delt", "rear_delts"), ("reverse fly", "rear_delts"),
                ("lateral", "delts"), ("side raise", "delts"), ("overhead", "v_push"), ("shoulder press", "v_push"), ("military", "v_push"),
                ("curl", "biceps"), ("pushdown", "triceps"), ("extension tri", "triceps"), ("tricep", "triceps"), ("skull", "triceps"),
                ("dip", "triceps"), ("leg extension", "quads_iso"), ("leg curl", "hamstrings_iso"), ("hamstring", "hamstrings_iso"),
                ("calf", "calves"), ("lunge", "lunge"), ("split squat", "lunge"), ("step up", "lunge"), ("squat", "squat"),
                ("leg press", "squat"), ("hack", "squat"), ("deadlift", "hinge"), ("rdl", "hinge"), ("thrust", "hinge"),
                ("glute", "hinge"), ("good morning", "hinge"), ("bench", "h_push"), ("press", "h_push"), ("fly", "h_push"),
                ("pec", "h_push"), ("push up", "h_push"), ("crunch", "flexion"), ("plank", "anti_ext"), ("ab", "anti_ext"),
                ("run", "cyclic"), ("bike", "cyclic"), ("rower", "cyclic"), ("erg", "cyclic"), ("carry", "carry")]
KIND_PATTERN = {"push": "h_push", "chest": "h_push", "pull": "h_pull", "back": "h_pull", "legs": "squat", "lower": "squat",
                "shoulders": "delts", "arms": "biceps"}
SHORT = {"db": "dumbbell", "bb": "barbell", "kb": "kettlebell", "ohp": "overhead press", "rdl": "romanian deadlift",
         "rdls": "romanian deadlift", "sldl": "romanian deadlift", "bss": "bulgarian split squat", "pullup": "pull up",
         "pullups": "pull up", "chinup": "chin up", "chinups": "chin up", "skullcrushers": "skull crusher",
         "skullcrusher": "skull crusher", "pushups": "push up", "pushup": "push up"}
KIT_WORDS = {"press", "dumbbell", "barbell", "cable", "machine", "kettlebell", "bar", "ez"}
# Whole names people type that are not a bank name: gym words and a few French ones. [believe: to grow from real routines]
ALIASES = {"bench": "bench_press", "flat bench": "bench_press", "squat": "back_squat", "squats": "back_squat",
           "deadlifts": "deadlift", "dips": "dip", "lunges": "walking_lunge", "pulldown": "lat_pulldown",
           "lat pull down": "lat_pulldown", "lat pulldowns": "lat_pulldown", "bicep curl": "db_curl", "biceps curl": "db_curl",
           "bicep curls": "db_curl", "biceps curls": "db_curl", "curls": "db_curl", "tricep pushdown": "rope_pushdown",
           "triceps pushdown": "rope_pushdown", "tricep pushdowns": "rope_pushdown", "pushdowns": "rope_pushdown",
           "cable row": "seated_cable_row", "seated row": "seated_cable_row", "military press": "overhead_press",
           "shoulder press": "overhead_press", "leg curl": "seated_leg_curl", "leg curls": "seated_leg_curl",
           "calf raises": "calf_raise", "calves": "calf_raise", "flyes": "cable_fly", "flys": "cable_fly", "pec fly": "cable_fly",
           "incline bench": "incline_bench_press", "hip thrusts": "hip_thrust", "face pulls": "face_pull",
           "developpe couche": "bench_press", "developpe militaire": "overhead_press", "souleve de terre": "deadlift",
           "tractions": "pull_up", "traction": "pull_up", "rowing barre": "barbell_row", "presse a cuisses": "leg_press",
           "presse": "leg_press", "fentes": "walking_lunge", "curl biceps": "db_curl", "elevations laterales": "lateral_raise",
           "developpe incline": "incline_bench_press", "tirage vertical": "lat_pulldown", "tirage horizontal": "seated_cable_row",
           "squat barre": "back_squat", "extension triceps": "rope_pushdown", "mollets": "calf_raise",
           "pec deck": "cable_fly", "pec deck fly": "cable_fly", "barbell curl": "ez_bar_curl", "bb curl": "ez_bar_curl",
           "barbell curls": "ez_bar_curl", "ez curl": "ez_bar_curl"}
# The order a proposal comes in (research/09 3.4): the clock first, then recovery and the goal, then balance.
RANK = ["limit", "kit", "time_fit", "recovery", "conditioning", "priority", "pull_volume", "group_low", "stall", "harder", "deload"]
SAFETY = {"limit", "kit"}          # never held back by the two-a-block cap: it is about their body or their kit
PER_BLOCK = 2
MUSCLE_WORDS = {"side_delts": "side shoulders", "rear_delts": "rear shoulders", "front_delts": "front shoulders", "upper_back": "upper back",
                "lats": "lats", "core": "abs"}
LOCK_OF = {"add_slot": "exercises", "swap_ex": "exercises", "set_reps_rule": "exercises", "add_module": "short"}


# · names to the bank

def _fold(t):
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def _norm(t, typed=False):
    words = [SHORT.get(w, w) if typed else w for w in _fold(t).split()]
    return re.sub(r"(?<=[a-z]{2}[a-rt-z])s\b", "", " ".join(words))   # plurals: "raises" and "rows" match "raise" and "row"


def match_name(text, bank):
    """A typed exercise to a bank id: an exact id or name first, then a close name (0.85 or better). None: their own."""
    if text in bank:
        return text
    if _fold(text) in ALIASES and ALIASES[_fold(text)] in bank:
        return ALIASES[_fold(text)]
    n = _norm(text, typed=True)
    if not n:
        return None
    best, score = None, 0.0
    for i, r in sorted(bank.items()):
        for cand in (_norm(i.replace("_", " ")), _norm(r["name"])):
            if n == cand:
                return i
            s = difflib.SequenceMatcher(None, n, cand).ratio()
            nt, ct = n.split(), cand.split()
            if len(nt) >= 2 and set(nt) <= set(ct) and len(ct) - len(nt) == 1 and (set(ct) - set(nt)) <= KIT_WORDS:
                s = max(s, 0.9)                         # "DB bench" is a dumbbell bench press: one word left out
            if s > score:
                best, score = i, s
    return best if score >= 0.85 else None


def guess_pattern(text, kind=None):
    n = " " + _fold(text) + " "
    for word, pat in WORD_PATTERN:
        if " " + word in n:
            return pat
    return KIND_PATTERN.get(kind, "h_push")


def closest_row(text, pattern, bank, tags=None):
    """The bank row an exercise of their own is tracked like: same movement, their kit, not a band if anything else fits."""
    pool = [r for r in bank.values() if r["pattern"] == pattern]
    for keep in (lambda r: tags is None or core.has_equipment(r, tags), lambda r: r["load_type"] != "band"):
        if [r for r in pool if keep(r)]:
            pool = [r for r in pool if keep(r)]
    if not pool:
        return None
    n = _norm(text, typed=True)
    pool.sort(key=lambda r: (-difflib.SequenceMatcher(None, n, _norm(r["name"])).ratio(), r["level"], r["id"]))
    return pool[0]["id"]


def _slug(t):
    return re.sub(r"_+", "_", _fold(t).replace(" ", "_")).strip("_") or "day"


def plain_reps(reps):
    return str(reps).replace("-", " to ")


# · the routine to a program

def _kinds(rt):
    labels = rt.get("day_labels") or []
    kinds = rt.get("day_kinds") or []
    base = SPLIT_KINDS.get(rt.get("split"), SPLIT_KINDS["custom"])
    days = int(rt.get("days") or len(labels) or len(base))
    if not labels:
        labels = [base[i % len(base)].capitalize() for i in range(days)]
    if len(kinds) != len(labels):
        kinds = [base[i % len(base)] for i in range(len(labels))]
    return list(zip(labels, kinds))


def _entry(e, bank, kind):
    """One exercise as they gave it: {"id"} · {"own"} · {"name"} · a string, with optional sets and reps."""
    if isinstance(e, str):
        e = {"name": e}
    e = dict(e)
    if not e.get("id") and not e.get("own"):
        i = match_name(e.get("name", ""), bank)
        if i:
            e["id"] = i
        else:
            e["own"] = e.get("name", "")
    if e.get("id") and e["id"] not in bank:
        e = {"own": e["id"], "sets": e.get("sets"), "reps": e.get("reps")}
    return e


def _sets_reps(e, row, first, goal):
    sets, reps = e.get("sets"), e.get("reps")
    if isinstance(sets, str) and sets.isdigit():
        sets = int(sets)
    if isinstance(sets, int) and 1 <= sets <= 10 and reps and re.search(r"\d", str(reps)):
        return sets, str(reps).replace(" ", ""), False
    if first and goal in ("strength", "powerlifting") and row["pattern"] in COMPOUND:
        return 4, "4-6", True
    return (3, "6-10", True) if row["pattern"] in COMPOUND else (3, "10-15", True)


def _rest(reps, row):
    lo, hi = [int(x) for x in re.findall(r"\d+", reps)][0], [int(x) for x in re.findall(r"\d+", reps)][-1]
    if hi <= 6:
        return 180
    return 120 if row["pattern"] in COMPOUND else 75


def _slot(sid, e, row, bank, first, goal, used):
    sets, reps, assumed = _sets_reps(e, row, first, goal)
    base = "%s_%s" % (sid, row["id"] if e.get("id") else "own_" + _slug(e["own"]))
    key, n = base, 2
    while key in used:
        key, n = "%s_%d" % (base, n), n + 1
    used.add(key)
    lo, hi = [int(x) for x in re.findall(r"\d+", reps)][0], [int(x) for x in re.findall(r"\d+", reps)][-1]
    sl = {"key": key, "pattern": row["pattern"], "prefer": [row["id"]], "sets": sets, "reps": reps, "rest": _rest(reps, row),
          "effort": "1 to 2 reps spare", "rule": "linear_session" if lo == hi else "double_progression", "theirs": True}
    if lo == hi and row["pattern"] in COMPOUND:
        sl["inc"] = 5 if row["pattern"] in ("squat", "hinge") else 2.5
    if e.get("own"):
        sl["own_name"] = e["own"]
    if assumed:
        sl["assumed"] = True
    return sl


def _lift_session(label, sid, exs, bank, goal, used, kind, tags=None):
    main, sec, acc = [], [], []
    for e in exs:
        e = _entry(e, bank, kind)
        if e.get("id"):
            row = bank[e["id"]]
        else:
            pid = closest_row(e["own"], guess_pattern(e["own"], kind), bank, tags)
            if not pid:
                continue
            row = bank[pid]
        sl = _slot(sid, e, row, bank, not main, goal, used)
        if not main:
            sl["score"] = True
            main.append(sl)
        elif not sec and row["pattern"] in COMPOUND:
            sec.append(sl)
        else:
            acc.append(sl)
    if not main:
        return None
    blocks = [{"name": "Main lift", "kind": "main", "format": "straight", "slots": main}]
    if sec:
        blocks.append({"name": "Second lift", "kind": "secondary", "format": "straight", "slots": sec})
    if acc:
        blocks.append({"name": "The rest of your session", "kind": "accessory", "format": "straight", "slots": acc})
    tags = []
    if any(bank[s["prefer"][0]]["pattern"] in ("squat", "hinge") for b in blocks[:2] for s in b["slots"]):
        tags.append("heavy_legs")
    if any(bank[s["prefer"][0]]["pattern"] in ("olympic", "jump") for b in blocks for s in b["slots"]):
        tags.append("power")
    return {"title": label, "tags": tags, "blocks": blocks, "kind": kind}


def _run_session(label, sid, kind):
    tpl = copy.deepcopy(core.load_program("run-base-3to5")["sessions"][RUN_SESSION[kind]])
    for b in tpl["blocks"]:
        for sl in b["slots"]:
            sl["key"] = "%s_%s" % (sid, sl["key"])
            if kind == "cardio" and sl.get("prefer"):
                sl["prefer"] = ["easy_run", "bike_erg", "row_erg", "run"]
    tpl["title"] = label
    tpl["kind"] = kind
    return tpl


def parent_of(rt, prof):
    split, goal = rt.get("split"), prof.get("goal")
    if split in PARENT:
        return PARENT[split]
    if split == "upper_lower":
        return "powerbuild-phul-4" if goal in ("strength", "powerlifting") else "muscle-upperlower-4"
    if split == "full_body":
        return "strength-lp-3" if goal in ("strength", "powerlifting") else "muscle-fullbody-3"
    return {"muscle": "muscle-upperlower-4", "strength": "strength-lp-3", "powerlifting": "strength-lp-3"}.get(goal, "health-baseline-2to3")


def adopt(prof, bank):
    """Their routine as a program file, in the schema of doctrine/programs/README.md plus the ledger. None when no
    day of it is one the engine can run (classes only): the coach cannot write or score a class."""
    rt = prof.get("current_routine") or {}
    goal = prof.get("goal")
    exmap = rt.get("exercises") or {}
    sessions, order, classes, used, seen = {}, [], [], set(), {}
    for label, kind in _kinds(rt):
        if kind == "class":
            classes.append(label)
            continue
        if label in seen:
            order.append(seen[label])
            continue
        sid = _slug(label)
        while sid in sessions:
            sid += "_2"
        if kind in RUN_SESSION and not exmap.get(label):
            s = _run_session(label, sid, kind)
        else:
            s = _lift_session(label, sid, exmap.get(label) or [], bank, goal, used, kind, core.place_tags(prof))
        if not s:
            continue
        sessions[sid] = s
        seen[label] = sid
        order.append(sid)
    if not order:
        return None
    parent = core.load_program(parent_of(rt, prof))
    n = len(order)
    mins = int(prof.get("minutes", 60))
    prog = {"id": ID, "name": NAME, "family": "own", "parent": parent["id"], "draws_from": ["your own routine"],
            "goals": {g: 0 for g in core.GOALS}, "experience": [prof.get("experience", "none")], "days": [n, n],
            "sweet_days": [n], "minutes": [mins, mins], "express_minutes": mins, "equipment_all": [], "equipment_any": [],
            "skills_required": [], "excluded_for": [], "evidence": "G", "simplicity": 2, "graduates_to": [],
            "block_weeks": parent.get("block_weeks", 4), "deload": None, "meso": None,
            "layouts": {str(n): order}, "modules": [], "sessions": sessions, "classes": classes,
            "source": {k: rt.get(k) for k in ("split", "days", "day_labels", "day_kinds", "exercises", "age", "stalls", "keep", "stuck") if k in rt},
            "locks": [k for k in rt.get("keep") or [] if k in core.ROUTINE_KEEP],
            "version": 1, "changes": [], "declined": []}
    return prog


# · words for people

def _name(sl, bank):
    return sl.get("own_name") or bank.get(sl["prefer"][0], {}).get("name") or sl["prefer"][0]


def routine_words(prog, bank):
    out = []
    order = list(dict.fromkeys(prog["layouts"][str(prog["days"][0])]))
    for sid in order:
        s = prog["sessions"][sid]
        exs = []
        for b in s["blocks"]:
            for sl in b["slots"]:
                if sl.get("kind") == "piece":
                    exs.append({"key": sl["key"], "name": "Intervals", "run": True})
                    continue
                e = {"key": sl["key"], "name": _name(sl, bank), "sets": sl.get("sets"), "reps": sl.get("reps"),
                     "id": sl["prefer"][0] if sl.get("prefer") else None}
                if sl.get("own_name"):
                    e["own"] = True
                    e["tracked_as"] = bank.get(sl["prefer"][0], {}).get("name")
                if sl.get("assumed"):
                    e["assumed"] = True
                if sl.get("rule") == "run_volume":
                    e["run"] = True
                if sl.get("added"):
                    e["added"] = True
                exs.append(e)
        out.append({"session": sid, "label": s.get("title", sid), "kind": s.get("kind"), "times": prog["layouts"][str(prog["days"][0])].count(sid),
                    "exercises": exs})
    return out


def _line(e):
    if e.get("run"):
        return e["name"]
    return "%s %s x %s%s" % (e["name"], e["sets"], plain_reps(e["reps"]), " (my guess)" if e.get("assumed") else "")


def write_program(prog, bank):
    lay = prog["layouts"][str(prog["days"][0])]
    words = routine_words(prog, bank)
    names = {w["session"]: w["label"] for w in words}
    prose = ["# Your routine", "",
             "_Your own week, coached. The trainer keeps your split, your days in your order, your exercises and your sets "
             "and reps. It runs the weights, the progress and the easier days on it. Anything it would change is asked "
             "first, and only what you said yes to is in here._", "",
             "**Your week:** %d sessions, done in order: %s." % (len(lay), ", ".join(names[s] for s in lay))]
    if prog.get("classes"):
        prose.append("Plus your classes (%s): the trainer cannot write them, so they stay yours as they are." % ", ".join(prog["classes"]))
    prose.append("")
    for w in words:
        prose.append("**%s:** %s." % (w["label"], "; ".join(_line(e) for e in w["exercises"])))
    own = [e for w in words for e in w["exercises"] if e.get("own")]
    if own:
        prose += ["", "**Your own exercises,** kept by name and tracked like the nearest one in the bank for weights and safety: " +
                  "; ".join("%s like %s" % (e["name"], e["tracked_as"]) for e in own) + "."]
    if prog.get("changes"):
        prose += ["", "## What the coach changed, with your yes", ""] + ["- %s · %s. %s" % (c["date"], c["what"], c["why"]) for c in prog["changes"]]
    if prog.get("declined"):
        prose += ["", "## What you kept as it was", ""] + ["- %s · %s" % (d["date"], d["what"]) for d in prog["declined"]]
    prose += ["", "## How it works", "",
              "Rules borrowed from `doctrine/programs/%s.md`: a block of %d weeks, then a short review. A fixed number of "
              "reps adds weight when every set is done; a range adds reps, then weight." % (prog["parent"], prog["block_weeks"])]
    core.write_json_block(core.MINE, prog, "\n".join(prose))


# · reading their week: planned sets and the clock

def _rows(prog, bank):
    """(sid, block, slot, row) for every lifting slot."""
    for sid, s in prog["sessions"].items():
        for b in s["blocks"]:
            for sl in b["slots"]:
                if sl.get("kind") == "piece" or sl.get("rule") in ("run_volume", "benchmark", "c25k_week"):
                    continue
                row = bank.get((sl.get("prefer") or [None])[0])
                if row:
                    yield sid, b, sl, row


def times(prog):
    lay = prog["layouts"][str(prog["days"][0])]
    return {sid: lay.count(sid) for sid in prog["sessions"]}


def weekly_sets(prog, bank, direct=False):
    """Planned hard sets a week by muscle (primary a full set, secondary half; direct: primary only), and pressing and pulling sets."""
    t = times(prog)
    sets, push, pull = {}, 0, 0
    for sid, b, sl, row in _rows(prog, bank):
        n = int(sl.get("sets") or 1) * t[sid]
        for m in row["muscles_primary"]:
            sets[m] = sets.get(m, 0) + n
        if direct:
            continue
        for m in row["muscles_secondary"]:
            sets[m] = sets.get(m, 0) + 0.5 * n
        push += n if row["pattern"] in PUSH else 0
        pull += n if row["pattern"] in PULL else 0
    return sets, push, pull


def session_minutes(s):
    """The clock of one of their sessions as written: the warm-up, every set, every rest (doctrine/06_BUILD.md)."""
    from sheet import session_seconds
    blocks = [{"kind": "warmup", "minutes": 8, "items": []}]
    for b in s["blocks"]:
        nb = {k: b[k] for k in ("format", "rest_after_round", "minutes") if k in b}
        nb["items"] = [{"sets": sl.get("sets", 1), "reps": sl.get("reps", ""), "rest": sl.get("rest", 90)} for sl in b["slots"]
                       if sl.get("kind") != "piece"]
        blocks.append(nb)
    return session_seconds({"blocks": blocks}) / 60.0


# · the proposals

def _where(prog, key):
    for sid, s in prog["sessions"].items():
        for b in s["blocks"]:
            for sl in b["slots"]:
                if sl["key"] == key:
                    return sid, b, sl
    return None, None, None


def _label(prog, sid):
    return prog["sessions"][sid].get("title", sid)


def _new_slot(prog, sid, pattern, pid, bank, sets=3):
    base = "%s_%s" % (sid, pid)
    keys = {sl["key"] for s in prog["sessions"].values() for b in s["blocks"] for sl in b["slots"]}
    key, n = base, 2
    while key in keys:
        key, n = "%s_%d" % (base, n), n + 1
    return {"key": key, "pattern": pattern, "prefer": [pid], "sets": sets, "reps": "10-15", "rest": 75,
            "effort": "1 to 2 reps spare", "rule": "double_progression", "theirs": True, "added": True}


def _pick(pattern, prof, tags, avoid, bank, prefer=None):
    import build
    return build.select({"key": "x", "pattern": pattern, "prefer": list(prefer or ADD_PREFER.get(pattern, []))}, prof, tags, avoid, bank)


def _lightest_day(prog, words=None):
    lifting = [sid for sid, s in prog["sessions"].items() if any(b["kind"] == "main" and any(sl.get("theirs") for sl in b["slots"]) for b in s["blocks"])]
    if not lifting:
        return None
    if words:
        named = [sid for sid in lifting if any(w in (prog["sessions"][sid].get("kind") or "") for w in words)]
        if named:
            lifting = named
    return min(lifting, key=lambda sid: (session_minutes(prog["sessions"][sid]), list(prog["sessions"]).index(sid)))


def _ctx(prof):
    import build
    tags = core.place_tags(prof)
    avoid = build.avoid_regions(prof, {})
    p = dict(prof, _care=build.care_regions(prof, {}) - avoid, _trig=build.trigger_limits(prof))
    return p, tags, avoid


def _limit_words(row, prof):
    regs = [l["region"].replace("_", " ") for l in prof.get("limits", []) if l.get("region") in row["regions"]]
    return "your " + (" and ".join(regs) if regs else "body")


def _stalled(key, log):
    seen = [d for l in log if not l.get("unreported") for d in l.get("done") or []
            if d.get("key") == key and (d.get("result") or {}).get("load") and (d.get("result") or {}).get("reps")]
    if len(seen) < 3:
        return False
    last = seen[-3:]
    loads = {d["result"]["load"] for d in last}
    reps = [sum(d["result"]["reps"]) for d in last]
    return len(loads) == 1 and reps[-1] <= reps[0]


def _find(prof, plan, st, log, prog, bank):
    """Every proposal the facts support, ranked, before the cap and the ledger."""
    out = []
    p, tags, avoid = _ctx(prof)
    import build
    mins = int(prof.get("minutes", 60))
    t = times(prog)
    goals = {prof.get("goal"), prof.get("goal2")} - {None}
    rt = prog.get("source") or {}

    def add(kind, ident, title, why, change, ops, args=None, cost=0):
        out.append({"id": ident, "kind": kind, "title": title, "why": why, "change": change, "ops": ops, "args": args or {},
                    "minutes": round(cost)})

    # their exercise against their body and their kit: a safer or a possible version, said, never silent
    def other(sid, sl):
        here = {x["prefer"][0] for bb in prog["sessions"][sid]["blocks"] for x in bb["slots"] if x.get("prefer")}
        for off in range(8):
            i = build.select(dict(sl, prefer=[], theirs=False), p, tags, avoid, bank, off)
            if i is None:
                return None
            if i not in here:
                return i
        return None

    for sid, b, sl, row in list(_rows(prog, bank)):
        name = _name(sl, bank)
        if not core.has_equipment(row, tags):
            alt = other(sid, sl)
            if alt:
                add("kit", "kit:" + sl["key"], "%s: a version for your kit" % name,
                    "%s needs kit your place does not have; %s trains the same thing." % (name, bank[alt]["name"]),
                    "%s: %s instead of %s" % (_label(prog, sid), bank[alt]["name"], name),
                    [{"op": "swap_ex", "sid": sid, "key": sl["key"], "id": alt}], {"day": _label(prog, sid), "from": name, "to": bank[alt]["name"]})
        elif not build.allowed(row, dict(p, skills=list(p.get("skills", [])) + ["pullup"]), tags, avoid, 5):
            alt = other(sid, sl)
            if alt and alt != row["id"]:
                add("limit", "limit:" + sl["key"], "%s: easier on %s" % (name, _limit_words(row, prof)),
                    "%s can set off %s; %s trains the same thing and leaves it alone." % (name, _limit_words(row, prof), bank[alt]["name"]),
                    "%s: %s instead of %s" % (_label(prog, sid), bank[alt]["name"], name),
                    [{"op": "swap_ex", "sid": sid, "key": sl["key"], "id": alt}],
                    {"day": _label(prog, sid), "from": name, "to": bank[alt]["name"], "region": _limit_words(row, prof),
                     "regions": sorted({l["region"] for l in prof.get("limits", []) if l.get("region") in row["regions"]})})

    # the clock: a day that runs over the minutes they gave
    for sid, s in prog["sessions"].items():
        took = session_minutes(s)
        if took <= mins + 3 or not any(b["kind"] == "main" and any(sl.get("theirs") for sl in b["slots"]) for b in s["blocks"]):
            continue
        trial = copy.deepcopy(s)
        ops, cuts = [], []
        order = [sl for b in reversed(trial["blocks"]) if b["kind"] == "accessory" for sl in reversed(b["slots"])] + \
                [sl for b in trial["blocks"] if b["kind"] == "secondary" for sl in b["slots"]]
        for sl in order:
            while int(sl.get("sets") or 1) > 2 and session_minutes(trial) > mins + 3:
                sl["sets"] = int(sl["sets"]) - 1
            orig = next(x for b in s["blocks"] for x in b["slots"] if x["key"] == sl["key"])
            if sl["sets"] != orig["sets"]:
                ops.append({"op": "set_sets", "sid": sid, "key": sl["key"], "sets": sl["sets"]})
                cuts.append("%s %d sets instead of %d" % (_name(sl, bank), sl["sets"], orig["sets"]))
            if session_minutes(trial) <= mins + 3:
                break
        if ops:
            add("time_fit", "time_fit:" + sid, "%s: fit your %d minutes" % (_label(prog, sid), mins),
                "%s takes about %d minutes with your rests; you said %d." % (_label(prog, sid), round(took), mins),
                "%s: %s" % (_label(prog, sid), ", ".join(cuts)), ops,
                {"day": _label(prog, sid), "took": round(took), "minutes": mins, "cuts": cuts}, -(took - session_minutes(trial)))

    # recovery: always tired or sore
    if "tired" in (rt.get("stalls") or []):
        ops = [{"op": "set_sets", "sid": sid, "key": sl["key"], "sets": int(sl["sets"]) - 1}
               for sid, b, sl, row in _rows(prog, bank) if b["kind"] == "accessory" and int(sl.get("sets") or 1) > 2]
        if ops:
            add("recovery", "recovery", "One set less on the extra moves",
                "You said you're always tired or sore: one set less on the extra moves lets you recover and keeps your main lifts moving.",
                "One set less on %d extra moves; the main lifts stay as they are" % len(ops), ops, {"n": len(ops)})

    # the goal: an engine or a race with nothing in the week that trains it
    cyclic = any(sl.get("rule") in ("run_volume", "benchmark") for s in prog["sessions"].values() for b in s["blocks"] for sl in b["slots"])
    mod = "hyrox-stations" if "hyrox" in goals else "easy-running" if "run" in goals else "conditioning" if goals & {"functional", "fat_loss"} else None
    if mod and not cyclic and not prog.get("classes") and mod not in (plan.get("goal_modules") or []):
        mname = {"hyrox-stations": "HYROX stations practice", "easy-running": "An easy run",
                 "conditioning": "A cardio burst"}.get(mod, core.load_module(mod)["name"])
        add("conditioning", "conditioning", "%s to finish" % mname,
            "Your goal needs an engine, and nothing in your week trains it yet.",
            "%s at the end of your lifting days, about 8 to 12 minutes" % mname, [{"op": "add_module", "module": mod}],
            {"module": mod, "name": mname}, 10)

    # a part they want to bring up, with no direct work on it
    import compose
    sets, push, pull = weekly_sets(prog, bank)
    for area in prof.get("priority") or []:
        parts = compose.PRIORITY_PARTS.get(area) or []
        dsets = weekly_sets(prog, bank, direct=True)[0]
        low = [(m, pat) for m, pat in parts if dsets.get(m, 0) < 6]
        if not low:
            continue
        direct = min(dsets.get(m, 0) for m, _ in low)
        who = " and ".join(MUSCLE_WORDS.get(m, m) for m, _ in low)
        ops, words = [], []
        for muscle, pattern in low:
            have = [(sid, sl) for sid, b, sl, row in _rows(prog, bank) if row["pattern"] == pattern and muscle in row["muscles_primary"]]
            if have:
                sid, sl = have[0]
                ops.append({"op": "add_sets", "sid": sid, "key": sl["key"], "by": 1})
                words.append("%s: +1 set of %s" % (_label(prog, sid), _name(sl, bank)))
            else:
                pid = _pick(pattern, p, tags, avoid, bank)
                sid = _lightest_day(prog, {"arms": ["arms", "pull", "upper", "push"], "biceps": ["arms", "pull", "upper"],
                                           "triceps": ["arms", "push", "upper"], "glutes": ["legs", "lower"], "legs": ["legs", "lower"],
                                           "calves": ["legs", "lower"], "shoulders": ["shoulders", "push", "upper", "pull"],
                                           "back": ["back", "pull", "upper"], "chest": ["chest", "push", "upper"],
                                           "quads": ["legs", "lower"], "hamstrings": ["legs", "lower"]}.get(area))
                if pid and sid:
                    ops.append({"op": "add_slot", "sid": sid, "slot": _new_slot(prog, sid, pattern, pid, bank, 3)})
                    words.append("%s: 3 sets of %s" % (_label(prog, sid), bank[pid]["name"]))
        if ops:
            add("priority", "priority:" + area, "More direct work for your %s" % area,
                "You want to bring up your %s, and your %s get about %d direct sets a week; 6 or more make a clear difference."
                % (area, who, round(direct)), "; ".join(words), ops, {"area": area, "sets": round(direct), "muscles": [m for m, _ in low]}, 4 * len(ops))

    # balance: pulling against pressing (the coach's eye, doctrine/06_BUILD.md)
    if push >= 6 and pull < push * 2.0 / 3:
        need = int(math.ceil(push * 2.0 / 3 - pull))
        ops, words = [], []
        pulls = [(sid, sl) for sid, b, sl, row in _rows(prog, bank) if row["pattern"] in PULL and int(sl.get("sets") or 1) < 5]
        for sid, sl in pulls:
            if need <= 0:
                break
            ops.append({"op": "add_sets", "sid": sid, "key": sl["key"], "by": 1})
            words.append("%s: +1 set of %s" % (_label(prog, sid), _name(sl, bank)))
            need -= t[sid]
        if need > 0:
            pid = _pick("h_pull", p, tags, avoid, bank) or _pick("rear_delts", p, tags, avoid, bank)
            sid = _lightest_day(prog, ["pull", "back", "upper"])
            if pid and sid:
                ops.append({"op": "add_slot", "sid": sid, "slot": _new_slot(prog, sid, bank[pid]["pattern"], pid, bank, 3)})
                words.append("%s: 3 sets of %s" % (_label(prog, sid), bank[pid]["name"]))
        if ops:
            add("pull_volume", "pull_volume", "More pulling to match your pressing",
                "%d pressing sets a week and %d pulling: shoulders do better when the two are nearer even." % (push, pull),
                "; ".join(words), ops, {"push": push, "pull": pull}, 3 * len(ops))

    # a muscle goal: a major group under 8 hard sets a week
    if prof.get("goal") in ("muscle", "fat_loss") or "muscle" in goals:
        for g, ms in GROUPS.items():
            have = max(sets.get(m, 0) for m in ms)
            if have >= 8:
                continue
            slots = [(sid, sl) for sid, b, sl, row in _rows(prog, bank) if set(ms) & set(row["muscles_primary"]) and int(sl.get("sets") or 1) < 5]
            ops, words = [], []
            for sid, sl in slots[:2]:
                ops.append({"op": "add_sets", "sid": sid, "key": sl["key"], "by": 1})
                words.append("%s: +1 set of %s" % (_label(prog, sid), _name(sl, bank)))
            if not ops:
                pat = GROUP_PATTERN[g]
                pid = _pick(pat, p, tags, avoid, bank)
                sid = _lightest_day(prog)
                if pid and sid:
                    ops.append({"op": "add_slot", "sid": sid, "slot": _new_slot(prog, sid, pat, pid, bank, 3)})
                    words.append("%s: 3 sets of %s" % (_label(prog, sid), bank[pid]["name"]))
            if ops:
                if any(o.get("key") in {q.get("key") for x in out for q in x["ops"]} for o in ops if o.get("key")):
                    continue                            # already in a proposal above (pulling covers the back)
                add("group_low", "group_low:" + g.replace(" ", "_"), "More sets for your %s" % g,
                    "About %d hard sets a week reach your %s; 8 to 10 or more grow clearly better." % (round(have), g),
                    "; ".join(words), ops, {"group": g, "sets": round(have)}, 3 * len(ops))

    # a lift that does not move: what they named, or what the log shows
    stuck = set(rt.get("stuck") or [])
    first_main = next((sl for sid, b, sl, row in _rows(prog, bank) if b["kind"] == "main"), None)
    for sid, b, sl, row in _rows(prog, bank):
        named = sl["prefer"][0] in stuck or (sl is first_main and "lift_stuck" in (rt.get("stalls") or []) and not stuck)
        if not (named or _stalled(sl["key"], log)) or b["kind"] not in ("main", "secondary"):
            continue
        lo, hi = progress_range(sl["reps"])
        if lo == hi:
            new = {"op": "set_reps_rule", "sid": sid, "key": sl["key"], "reps": "%d-%d" % (max(lo + 1, 6), max(lo + 3, 8)), "rule": "double_progression"}
            words = "%s: %d x %s, adding reps before weight" % (_name(sl, bank), sl["sets"], plain_reps(new["reps"]))
        elif int(sl.get("sets") or 1) > 2:
            new = {"op": "set_sets", "sid": sid, "key": sl["key"], "sets": int(sl["sets"]) - 1}
            words = "%s: %d sets instead of %d for a few weeks, same weight" % (_name(sl, bank), new["sets"], sl["sets"])
        else:
            continue
        add("stall", "stall:" + sl["key"], "%s: restart the progress" % _name(sl, bank),
            "%s has not moved; a new rep range or a little less volume usually gets it going again." % _name(sl, bank),
            words, [new], {"name": _name(sl, bank)})

    # a bodyweight or fixed weight move done at the top of its range: the next step, on their yes
    for sid, b, sl, row in _rows(prog, bank):
        ss = (st.get("slots") or {}).get(sl["key"]) or {}
        h = row.get("harder")
        if ss.get("ready_harder") and h and h in bank and build.allowed(bank[h], p, tags, avoid, 5):
            add("harder", "harder:" + sl["key"], "%s: the next step" % _name(sl, bank),
                "You hit the top of your range on %s: %s is the next step." % (_name(sl, bank), bank[h]["name"]),
                "%s: %s instead of %s" % (_label(prog, sid), bank[h]["name"], _name(sl, bank)),
                [{"op": "swap_ex", "sid": sid, "key": sl["key"], "id": h}], {"from": _name(sl, bank), "to": bank[h]["name"]})

    # an easier week every block, as the parent program runs it
    par = core.load_program(prog["parent"])
    if not prog.get("deload") and par.get("deload"):
        add("deload", "deload", "An easier week after every %d weeks" % prog["block_weeks"],
            "A lighter week after each block lets the work sink in and keeps your joints happy.",
            "Every week %d: half the sets, a little lighter" % (prog["block_weeks"] + 1),
            [{"op": "set_deload", "deload": par["deload"]}], {"weeks": prog["block_weeks"]})
    out.sort(key=lambda x: (RANK.index(x["kind"]), x["id"]))
    for x in out:
        lock = next((LOCK_OF[o["op"]] for o in x["ops"] if o["op"] in LOCK_OF and LOCK_OF[o["op"]] in prog.get("locks", [])), None)
        if "everything" in prog.get("locks", []):
            lock = "everything"
        x["touches_lock"] = lock
        x["safety"] = x["kind"] in SAFETY
        x["facts"] = json.dumps(x["ops"], sort_keys=True)
    return out


def progress_range(reps):
    nums = [int(n) for n in re.findall(r"\d+", str(reps))]
    return (nums[0], nums[-1]) if nums else (0, 0)


def basis(prof):
    """What a proposal rests on, from their answers: a no is asked again early only when one of these changed."""
    return json.dumps({k: prof.get(k) for k in ("goal", "goal2", "minutes", "priority", "event", "limits", "places")}, sort_keys=True)


def proposals(prog, prof, plan, st, log, bank):
    """The open proposals: safety ones always, the rest at most two a block, never one they answered while its facts
    stand (a declined one comes back only two blocks later, or when what it rests on changed)."""
    block = (st or {}).get("block", 1)
    found = _find(prof, plan or {}, st or {}, log or [], prog, bank)
    answered = [c for c in prog.get("changes", []) + prog.get("declined", []) if c.get("block") == block and c.get("kind") not in SAFETY]
    keep = []
    for x in found:
        if any(c["id"] == x["id"] and (c.get("facts") == x["facts"] or c.get("block") == block) for c in prog.get("changes", [])):
            continue                                    # said yes to this block: the next step waits for the next block
        if any(d["id"] == x["id"] and d.get("basis") == basis(prof) and block - d.get("block", block) < 2 for d in prog.get("declined", [])):
            continue                                    # their no stands two blocks, unless what it rests on changed
        keep.append(x)
    safety = [x for x in keep if x["safety"]]
    rest = [x for x in keep if not x["safety"]]
    room = max(0, PER_BLOCK - len(answered))
    return {"open": safety + rest[:room], "later": len(rest[room:]), "all": keep}


# · their yes, their no

def _apply(prog, plan, st, op, bank):
    sid = op.get("sid")
    if op["op"] in ("set_sets", "add_sets", "swap_ex", "set_reps_rule"):
        _, b, sl = _where(prog, op["key"])
        if sl is None:
            return
        if op["op"] == "set_sets":
            sl["sets"] = int(op["sets"])
        elif op["op"] == "add_sets":
            sl["sets"] = int(sl["sets"]) + int(op.get("by", 1))
        elif op["op"] == "swap_ex":
            sl["prefer"] = [op["id"]]
            sl["pattern"] = bank[op["id"]]["pattern"]
            sl.pop("own_name", None)
            (st.setdefault("slots", {}))[sl["key"]] = {}           # a new exercise finds its own weight
        else:
            sl["reps"], sl["rule"] = op["reps"], op["rule"]
            sl.pop("inc", None)
            ss = (st.setdefault("slots", {})).setdefault(sl["key"], {})
            ss["target"] = progress_range(op["reps"])[0]
        sl.pop("assumed", None)
    elif op["op"] == "add_slot":
        s = prog["sessions"][sid]
        acc = next((b for b in s["blocks"] if b["kind"] == "accessory"), None)
        if acc is None:
            acc = {"name": "The rest of your session", "kind": "accessory", "format": "straight", "slots": []}
            s["blocks"].append(acc)
        acc["slots"].append(op["slot"])
    elif op["op"] == "add_module":
        prog["goal_modules"] = list(dict.fromkeys(list(prog.get("goal_modules") or []) + [op["module"]]))
        plan["goal_modules"] = list(prog["goal_modules"])
    elif op["op"] == "set_deload":
        prog["deload"] = op["deload"]


def accept(prog, plan, st, pid, prof, log, bank, date=None):
    found = {x["id"]: x for x in _find(prof, plan, st, log, prog, bank)}
    x = found.get(pid)
    if not x:
        return None
    for op in x["ops"]:
        _apply(prog, plan, st, op, bank)
    prog["version"] = prog.get("version", 1) + 1
    prog.setdefault("changes", []).append({"id": pid, "kind": x["kind"], "date": date or core.today(), "block": st.get("block", 1),
                                           "what": x["change"], "why": x["why"], "facts": x["facts"]})
    return x


def decline(prog, st, pid, prof, plan, log, bank, date=None):
    found = {x["id"]: x for x in _find(prof, plan, st, log, prog, bank)}
    x = found.get(pid)
    if not x:
        return None
    prog.setdefault("declined", []).append({"id": pid, "kind": x["kind"], "date": date or core.today(), "block": st.get("block", 1),
                                            "what": x["change"], "facts": x["facts"], "basis": basis(prof)})
    return x


def public(x):
    return {k: v for k, v in x.items() if k not in ("ops", "facts")}
