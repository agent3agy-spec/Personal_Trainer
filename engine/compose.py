"""compose.py · the week, composed from what the person wants (doctrine/06_BUILD.md, "The composer").

A profile is a blend of outcomes with shares (doctrine/02_INTERVIEW.md). The trainer turns the blend into
components (lifting days, running days, HYROX days, mixed conditioning days, easy cardio days) and gives
each one days in proportion to its share. A component too small for a whole day becomes a goal finisher
that the clock protects. Programs and modules are the library the components draw on: the lead program
is the one `match` picks for the biggest share, the others come from programs and modules that fit.
The person never picks a method, and no method name reaches them.

Standard library only, no network: the web page runs this file in Pyodide.
"""
import copy, math
import core

# What each outcome follow-up asks of a week, as shares of components (sum 1).
RECIPE = {
    "size": {"lift": 1.0}, "lean": {"lift": 0.7, "conditioning": 0.3},
    "general": {"lift": 1.0}, "powerlifting": {"lift": 1.0}, "olympic": {"lift": 1.0}, "meet": {"lift": 1.0},
    "crossfit": {"mixed": 1.0}, "hybrid": {"hybrid": 1.0},
    "run_5k_10k": {"run": 1.0}, "run_half": {"run": 1.0}, "run_marathon": {"run": 1.0}, "hyrox": {"hyrox": 1.0},
    "lifting": {"lift": 1.0}, "fitness": {"mixed": 0.6, "conditioning": 0.4}, "mix": {"lift": 0.6, "conditioning": 0.4},
}
# An older profile without outcomes: its goal keys, read the same way.
GOAL_COMPONENT = {"muscle": "lift", "strength": "lift", "powerlifting": "lift", "weightlifting": "lift", "health": "lift",
                  "independent": "lift", "skills": "lift", "run": "run", "hyrox": "hyrox", "functional": "mixed",
                  "fat_loss": "conditioning"}
# Which components a program family already serves inside its own week.
COVERS = {"strength": {"lift"}, "muscle": {"lift"}, "powerbuild": {"lift"}, "weightlifting": {"lift"}, "health": {"lift"},
          "functional": {"mixed", "conditioning"}, "hyrox": {"hyrox", "run", "mixed", "conditioning"},
          "hybrid": {"hybrid", "lift", "run"}, "run": {"run"}}
LIFT_FAMILIES = ("strength", "muscle", "powerbuild", "weightlifting", "health")
LEAD_COMPONENT = {"run": "run", "hyrox": "hyrox", "functional": "mixed", "hybrid": "hybrid"}
# A component that is not given a whole day comes as this finisher on the lifting sessions.
FINISHER = {"conditioning": "conditioning", "mixed": "conditioning", "hyrox": "hyrox-stations", "run": "easy-running",
            "lift": "core", "hybrid": "conditioning"}
DAY_WORDS = {"lift": ("lifting day", "lifting days"), "run": ("running day", "running days"), "hyrox": ("HYROX day", "HYROX days"),
             "mixed": ("mixed conditioning day", "mixed conditioning days"), "conditioning": ("easy cardio day", "easy cardio days"),
             "hybrid": ("strength and running day", "strength and running days")}
FINISH_WORDS = {"conditioning": "a short cardio burst to finish", "mixed": "a short cardio burst to finish", "hyrox": "a short practice of the HYROX stations",
                "run": "a short easy run", "lift": "a few core moves to finish", "hybrid": "a short cardio burst to finish"}
SHORT = {"strength": "Strength", "powerbuild": "Strength and size", "muscle": "Muscle", "weightlifting": "Olympic lifting",
         "functional": "Mixed fitness", "hyrox": "HYROX", "hybrid": "Strength and running", "run": "Running",
         "health": "Full body strength"}
COMP_SHORT = {"lift": "Strength", "run": "Running", "hyrox": "HYROX", "mixed": "Mixed fitness", "conditioning": "Easy cardio",
              "hybrid": "Strength and running"}
# The run module's sessions for a running component of n days: the long run first, then easy, then one quality run.
RUN_DAYS = {1: ["long"], 2: ["easy", "long"], 3: ["easy", "quality", "long"]}
HYROX_DAYS = {1: ["C"], 2: ["I", "C"], 3: ["E", "I", "C"]}
# The long run, by event: its ceiling, and how many weeks it holds before it grows about 10 percent.
LONG_RUN = {"run_marathon": {"max_minutes": 180, "hold_weeks": 2}, "run_half": {"max_minutes": 120, "hold_weeks": 3},
            "run_5k_10k": {"max_minutes": 80, "hold_weeks": 3}}
# Weekly sets added for a priority area, spread over the lifting sessions (07 change 6; Schoenfeld 2017 dose response).
PRIORITY_WEEKLY = 6
PRIORITY_PARTS = {"arms": [["biceps", "biceps"], ["triceps", "triceps"]], "biceps": [["biceps", "biceps"]],
                  "triceps": [["triceps", "triceps"]], "back": [["lats", "v_pull"], ["upper_back", "h_pull"]],
                  "chest": [["chest", "h_push"]], "shoulders": [["side_delts", "delts"], ["rear_delts", "rear_delts"]],
                  "glutes": [["glutes", "hinge"]], "legs": [["quads", "quads_iso"], ["hamstrings", "hamstrings_iso"]],
                  "quads": [["quads", "quads_iso"]], "hamstrings": [["hamstrings", "hamstrings_iso"]],
                  "core": [["core", "anti_ext"]], "abs": [["core", "anti_ext"]], "calves": [["calves", "calves"]]}
CHALLENGES = {"lift": "one more clean rep on your first main lift than in week 1, at the same weight",
              "mixed": "beat your first score on one of the timed pieces",
              "conditioning": "beat your first score on the cardio burst",
              "run": "one easy run 5 minutes longer than in week 1, still able to talk",
              "hyrox": "beat your first time on the run straight off a station", "hybrid": "a new best on any main lift or run"}


def _detail(oid, det):
    return det if det in core.OUTCOMES.get(oid, {}) else core.OUTCOME_DEFAULT.get(oid)


def _legacy(prof):
    g1, g2 = prof.get("goal"), prof.get("goal2")
    c1 = GOAL_COMPONENT.get(g1, "lift")
    rec = {"lift": 0.7, "conditioning": 0.3} if c1 == "conditioning" else {c1: 1.0}
    c2 = GOAL_COMPONENT.get(g2) if g2 else None
    if c2 and c2 not in rec:
        rec = {k: v * 0.7 for k, v in rec.items()}
        rec[c2] = rec.get(c2, 0) + 0.3
    return rec


def outcome_parts(prof):
    """[(outcome id, detail, share)] in order, from the blend, the single outcome, or nothing."""
    outs = [o for o in (prof.get("outcomes") or []) if isinstance(o, dict) and o.get("id") in core.OUTCOMES]
    if outs:
        return [(o["id"], _detail(o["id"], o.get("detail")), float(o.get("share") or 0)) for o in outs]
    if prof.get("outcome") in core.OUTCOMES:
        return [(prof["outcome"], _detail(prof["outcome"], prof.get("outcome_detail")), 1.0)]
    return []


def blend(prof):
    """The components of this person's week and their shares, biggest first: [("lift", 0.6), ("run", 0.4)]."""
    parts = outcome_parts(prof)
    recs = [(RECIPE.get(det, {"lift": 1.0}), sh) for _, det, sh in parts] or [(_legacy(prof), 1.0)]
    out = {}
    for rec, sh in recs:
        for c, w in rec.items():
            out[c] = out.get(c, 0) + sh * w
    tot = sum(out.values()) or 1.0
    items = [(c, round(v / tot, 3)) for c, v in out.items()]
    items.sort(key=lambda kv: -kv[1])                    # stable: on a tie the first outcome leads
    return items


def main_component(prof):
    return next((c for c, _ in blend(prof) if c != "conditioning"), "lift")


def run_event(prof):
    """The running event detail this person trains for, or None (a long run is protected only for an event)."""
    for oid, det, _ in outcome_parts(prof):
        if oid == "event" and det in LONG_RUN:
            return det
    if not outcome_parts(prof) and (prof.get("goal") == "run" or prof.get("goal2") == "run"):
        return "run_5k_10k"
    return None


def _largest_remainder(want, n):
    tot = sum(s for _, s in want) or 1.0
    raw = [(c, n * s / tot) for c, s in want]
    out = {c: int(math.floor(v)) for c, v in raw}
    left = n - sum(out.values())
    for c, v in sorted(raw, key=lambda cv: -(cv[1] - math.floor(cv[1]))):
        if left <= 0:
            break
        out[c] += 1
        left -= 1
    return out


def allocate(prof, family):
    """Days for the lead program of this family, days for every other component, and the finishers.
    The lead keeps at least 2 days (all of them on a 2 day week); easy cardio earns a day only from 4 days."""
    D = int(prof.get("days") or 3)
    comps = blend(prof)
    cov = COVERS.get(family, {"lift"})
    if any(c == "hybrid" for c, _ in comps) and "hybrid" not in cov:
        merged = {}
        for c, s in comps:
            for cc, w in ({"lift": 0.5, "run": 0.5} if c == "hybrid" else {c: 1.0}).items():
                merged[cc] = merged.get(cc, 0) + s * w
        comps = sorted(merged.items(), key=lambda kv: -kv[1])
    main = next((c for c, _ in comps if c != "conditioning"), "lift")
    cov = cov | {main}                                   # the lead program is picked for the biggest share: it serves it
    lead = sum(s for c, s in comps if c in cov)
    others = [(c, s) for c, s in comps if c not in cov and c != "conditioning"]
    cond = 0 if "conditioning" in cov else dict(comps).get("conditioning", 0)
    want = [("lead", lead)] + others + ([("conditioning", cond)] if cond and D >= 4 else [])
    days = _largest_remainder(want, D)
    floor = D if D <= 2 else 2
    while days["lead"] < floor:
        donors = [c for c in days if c != "lead" and days[c] > 0]
        if not donors:
            break
        c = max(donors, key=lambda c: days[c])
        days[c] -= 1
        days["lead"] += 1
    support = None
    if family == "run" and D >= 4 and "lift" not in days and days["lead"] >= 4:
        days["lead"] -= 1                                # a runner on 4 days or more keeps one strength day
        days["lift"] = 1
        support = "lift"
    comp_days = {c: n for c, n in days.items() if c != "lead" and n > 0}
    finishers = [c for c, _ in others if not comp_days.get(c)]
    if cond:
        finishers.append("conditioning")                 # fat loss and leaner goals: conditioning on the lifting days
    return {"days": D, "lead": days["lead"], "components": comp_days, "finishers": finishers, "blend": comps,
            "support": support, "lead_component": LEAD_COMPONENT.get(family, "lift")}


def lead_days(prof, family):
    return allocate(prof, family)["lead"]


def _interleave(counts):
    total = sum(counts) or 1
    pos = []
    for i, n in enumerate(counts):
        for k in range(n):
            pos.append(((k + 0.5) * total / n, i))
    return [i for _, i in sorted(pos)]


def _fillable(sess, prof, tags, avoid, bank, select):
    for b in sess.get("blocks", []):
        for sl in b.get("slots", []):
            if sl.get("kind") == "piece":
                moves = [mv for pc in (sl.get("pieces") or [sl.get("moves", [])]) for mv in pc]
                if not any(select(dict(mv, key="move"), prof, tags, avoid, bank) for mv in moves):
                    return False
            elif b.get("kind") == "main" and select(sl, prof, tags, avoid, bank) is None:
                return False
    return True


def _ctx(prof):
    import build
    avoid = build.avoid_regions(prof, {})
    p = dict(prof, _care=build.care_regions(prof, {}) - avoid, _trig=build.trigger_limits(prof))
    return p, list(core.place_tags(p)), avoid


def _source(comp, n, prof, lead, bank, select):
    """The stream that serves n days of a component, or None when nothing in the library fits this person."""
    p, tags, avoid = _ctx(prof)
    if comp == "run":
        if "run_30min" in (prof.get("skills") or []) or (prof.get("experience_by") or {}).get("running") in ("novice", "intermediate", "advanced"):
            m = core.load_module("run-race")
            rot = RUN_DAYS.get(n, RUN_DAYS[3] + ["easy"] * (n - 3))
            if all(_fillable(m["sessions"][s], p, tags, avoid, bank, select) for s in set(rot)):
                return {"kind": "module", "id": "run-race", "rotation": rot, "per_week": n, "what": "run"}
        c25 = core.load_program("run-c25k-3")
        if _fillable(c25["sessions"]["A"], p, tags, avoid, bank, select):
            return {"kind": "program", "id": "run-c25k-3", "rotation": ["A"], "per_week": n, "what": "run", "prefix": "r_"}
        return _source("conditioning", n, prof, lead, bank, select)
    if comp == "conditioning":
        m = core.load_module("easy-running")
        if _fillable(m["sessions"]["easy"], p, tags, avoid, bank, select):
            return {"kind": "module", "id": "easy-running", "rotation": ["easy"], "per_week": n, "what": "conditioning"}
        return None
    if comp == "hyrox":
        hp = core.load_program("hyrox-prep-4")
        rot = HYROX_DAYS.get(n, HYROX_DAYS[3])
        if _kit_ok(hp, p) and "run_30min" in (prof.get("skills") or []) and \
                all(_fillable(hp["sessions"][s], p, tags, avoid, bank, select) for s in rot):
            return {"kind": "program", "id": "hyrox-prep-4", "rotation": rot, "per_week": n, "what": "hyrox", "prefix": "h_"}
        return None
    if comp == "mixed":
        fp = core.load_program("functional-gpp-3to5")
        rot = fp["layouts"][str(fp["days"][0])]
        if _kit_ok(fp, p) and all(_fillable(fp["sessions"][s], p, tags, avoid, bank, select) for s in rot):
            return {"kind": "program", "id": "functional-gpp-3to5", "rotation": list(rot), "per_week": n, "what": "mixed", "prefix": "f_"}
        return None
    if comp == "lift":
        return _lift_source(n, prof, p, bank, select)
    return None


def _kit_ok(prog, prof):
    tags = set(core.place_tags(prof))
    return all(t in tags for t in prog.get("equipment_all", [])) and all(set(a) & tags for a in prog.get("equipment_any", []))


def lift_goal(prof):
    for oid, det, _ in outcome_parts(prof):
        if "lift" in RECIPE.get(det, {}):
            return core.OUTCOMES[oid][det][0] if core.OUTCOMES[oid][det][0] != "fat_loss" else "muscle"
    for g in (prof.get("goal"), prof.get("goal2")):
        if GOAL_COMPONENT.get(g) == "lift":
            return g
    return "health"


def _lift_source(n, prof, p, bank, select):
    """A full body plan for the lifting days next to another lead: every session trains the whole body,
    so 1 or 2 days a week lose nothing to a split (07 Part 3 check 1)."""
    import match
    goal = lift_goal(prof)
    q = dict(prof, goal=goal, goal2=None, outcomes=None, outcome=None, outcome_detail=None, days=max(2, n))
    best = None
    for prog in core.all_programs():
        if prog["family"] not in LIFT_FAMILIES:
            continue
        lay = prog["layouts"].get(str(prog["days"][0]))
        if not lay or not (prog.get("rotates") or len(lay) <= max(n, prog["days"][0])) or prog["days"][0] > 3:
            continue
        why = [w for w in match.filters(prog, dict(q, days=prog["days"][0]), bank, select) if not w.startswith("days:")]
        if why:
            continue
        s = match.score(prog, q) + (2 if prog["family"] == "health" and n == 1 else 0)
        if best is None or s > best[0]:
            best = (s, prog, lay)
    if not best:
        return None
    return {"kind": "program", "id": best[1]["id"], "rotation": list(best[2]), "per_week": n, "what": "lift", "prefix": "l_"}


def _lifting(sess):
    return any(b.get("kind") in ("main", "secondary", "accessory") and any(sl.get("kind") != "piece" and sl.get("rule") not in
               ("run_volume", "c25k_week", "benchmark") for sl in b.get("slots", [])) for b in sess.get("blocks", []))


def session_of(stream, sid):
    if stream["kind"] == "module":
        return core.load_module(stream["id"])["sessions"][sid]
    return core.load_program(stream["id"])["sessions"][sid]


def _plural(n, c):
    one, many = DAY_WORDS[c]
    return "%d %s" % (n, one if n == 1 else many)


def compose(prof, prog, bank, select):
    """The composed week for this lead program. Returns the plan fields `plan.py choose` writes."""
    al = allocate(prof, prog["family"])
    D = al["days"]
    notes = []
    used = min(al["lead"], prog["days"][1])
    lay = prog["layouts"].get(str(used)) or prog["layouts"].get(str(prog["days"][1]))
    lead_comp = al["lead_component"]
    streams = [{"kind": "lead", "id": prog["id"], "rotation": list(lay), "per_week": used, "what": lead_comp}]
    if len(lay) > used:
        notes.append(prog.get("rotation_note") or "Its %d sessions take turns over your %d days." % (len(lay), used))
    if (prog.get("layout_notes") or {}).get(str(used)):
        notes.append(prog["layout_notes"][str(used)])
    comps = dict(al["components"])
    spare = al["lead"] - used
    if spare > 0:
        if comps:
            big = max(comps, key=comps.get)
            comps[big] += spare
        elif "running" in (prof.get("enjoys") or []) or "running" in (prof.get("likes") or []) or \
                dict(al["blend"]).get("conditioning") or prof.get("goal") in ("health", "fat_loss") or prof.get("goal2") in ("health", "fat_loss", "run"):
            comps["run" if (prof.get("goal2") == "run" or "running" in (prof.get("enjoys") or []) + (prof.get("likes") or [])) else "conditioning"] = spare
        else:
            notes.append("This plan uses %d of your %d days: the other %s rest or an easy walk." % (used, D, "is" if spare == 1 else "are"))
    finishers = list(al["finishers"])
    for c, n in comps.items():
        src = _source(c, n, prof, prog, bank, select)
        if src:
            streams.append(src)
            continue
        if c not in finishers:
            finishers.append(c)
        back = min(n, prog["days"][1] - streams[0]["per_week"])
        if back > 0:                                     # the days go back to the lead program, in its own layout
            nl = prog["layouts"].get(str(streams[0]["per_week"] + back))
            if nl and (len(nl) <= streams[0]["per_week"] + back or prog.get("rotates")):
                streams[0]["per_week"] += back
                streams[0]["rotation"] = list(nl)
                used = streams[0]["per_week"]
        if c == "lift" and al["support"]:
            al["support"] = None
        notes.append("Nothing here fits %s with your kit or limits, so it comes as %s instead."
                     % (_plural(n, c), FINISH_WORDS.get(c, "a short piece to finish")))
    order = _interleave([s["per_week"] for s in streams])
    goal_modules = []
    for c in finishers:
        m = FINISHER.get(c)
        if m and m not in goal_modules and (core.MODULES / (m + ".md")).exists():
            goal_modules.append(m)
    flags = set((prof.get("screen") or {}).get("flags", []))
    if "postpartum" in flags:
        goal_modules = ["core"] + [g for g in goal_modules if g != "core"]   # after a birth the trunk work is cut last of all (08 persona 8)
    nice = [m for m in prog.get("modules", []) if m not in goal_modules]
    week = []
    for idx in order:
        s = streams[idx]
        week.append((s, s["rotation"][len([w for w in week if w[0] is s]) % len(s["rotation"])]))
    lift_days = sum(1 for s, sid in week if _lifting(session_of(s, sid) if s["kind"] != "lead" else prog["sessions"][sid]))
    targets = []
    for area in (prof.get("priority") or [])[:2]:
        parts = PRIORITY_PARTS.get(str(area).lower().strip())
        if parts and lift_days:
            targets.append({"area": str(area).lower().strip(), "parts": parts, "weekly": PRIORITY_WEEKLY, "why": "priority"})
    ev = run_event(prof)
    long_run = dict(LONG_RUN[ev], protect=True) if ev and any(s["what"] == "run" for s in streams) else None
    challenge = None
    if any(oid == "keep_going" for oid, _, _ in outcome_parts(prof)[:1]):
        challenge = [CHALLENGES[s["what"]] for s in streams if s["what"] in CHALLENGES]
        challenge += [CHALLENGES["conditioning"]] if "conditioning" in finishers else []
        challenge = list(dict.fromkeys(challenge))
    week_words = [_plural(used, lead_comp)] + [_plural(s["per_week"], s["what"]) for s in streams[1:]]
    if al["support"]:
        notes.append("One of your days is a short full body strength session: it keeps a runner's legs and trunk strong.")
    if not lift_days and "conditioning" in goal_modules:
        goal_modules.remove("conditioning")              # no hard intervals after a run: easy cardio fills the minutes instead
        finishers = [c for c in finishers if c != "conditioning"]
        notes.append("For your fitness goal, easy cardio after each run uses the rest of your minutes.")
    finish_words = [FINISH_WORDS[c] for c in finishers if c in FINISH_WORDS]
    if finish_words:
        notes.append("Your %s end with %s, and the clock cuts it last." % ("lifting sessions" if lift_days else "sessions",
                                                                         " and ".join(dict.fromkeys(finish_words))))
    if long_run:
        notes.append("Your long run is protected: when it needs more than your usual minutes, the sheet says so and you put it "
                     "on the day you have the time. It grows about 10 percent every %d weeks, up to about %d minutes."
                     % (long_run["hold_weeks"], long_run["max_minutes"]))
    if len(streams) == 1:
        plain_name = "%s, %d days" % (SHORT.get(prog["family"], "Your plan"), used)
    else:
        plain_name = " · ".join("%s %d %s" % (SHORT.get(prog["family"], "Training") if i == 0 else COMP_SHORT.get(s["what"], "Training"),
                                              s["per_week"], "day" if s["per_week"] == 1 else "days") for i, s in enumerate(streams))
    return {"days": sum(s["per_week"] for s in streams), "asked_days": D, "goal_on_all": lift_days == 0, "program_days": used, "streams": streams, "order": order,
            "components": [{"what": s["what"], "days": s["per_week"], "from": s["id"], "role": "lead" if i == 0 else "day"}
                           for i, s in enumerate(streams)] + [{"what": c, "days": 0, "from": FINISHER.get(c), "role": "finisher"} for c in finishers],
            "blend": al["blend"], "goal_modules": goal_modules, "modules": nice, "targets": targets, "lift_days": lift_days,
            "long_run": long_run, "challenge": challenge, "notes": notes, "plain_name": plain_name,
            "week_words": week_words}


def describe(prof, prog):
    """The week in plain words for the offer card, without building anything: '2 lifting days and 1 HYROX day'."""
    al = allocate(prof, prog["family"])
    used = min(al["lead"], prog["days"][1])
    parts = [_plural(used, al["lead_component"])] + [_plural(n, c) for c, n in al["components"].items()]
    line = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    fin = [FINISH_WORDS[c] for c in al["finishers"] if c in FINISH_WORDS]
    if al["lead_component"] == "run" and "lift" not in al["components"] and "conditioning" in al["finishers"]:
        fin = [f for f in fin if f != FINISH_WORDS["conditioning"]] + ["easy cardio after the runs"]
    if fin:
        line += ", with %s" % " and ".join(dict.fromkeys(fin))
    return line, al
