"""match.py · which program fits this person, by a fixed rule (doctrine/03_MATRIX.md).

Step 1 hard filters · Step 2 the score · Step 3 tie-breaks · Step 4 the top three · Step 5 never empty.
The coach explains the result; it never computes it.
"""
import core

# What each family asks you to do, in the activity words of the interview (core.ENJOY). An adherence input only:
# the person never picks a family, they say what they enjoy or can't stand (doctrine/03_MATRIX.md Step 2).
ENJOY_OF = {"strength": ["heavy"], "powerbuild": ["heavy", "pump"], "muscle": ["pump"], "weightlifting": ["heavy"],
            "functional": ["circuits"], "hyrox": ["circuits", "running"], "hybrid": ["heavy", "running", "long_cardio"],
            "run": ["running", "long_cardio"], "health": []}
ENJOY_WORDS = {"heavy": "heavy lifting", "pump": "muscle work", "circuits": "fast circuits", "long_cardio": "long cardio",
               "running": "running"}
LEGACY_LIKES = {"barbell": "heavy", "machines": "pump", "dumbbells": "pump", "circuits": "circuits", "classes": "circuits",
                "running": "running"}
# The families an outcome's follow-up points at (core.OUTCOMES). Goal fit already ranks most of them; this settles the
# outcomes a goal key cannot say alone, like strength and running in one week.
OUTCOME_FAMILY = {"size": ["muscle", "powerbuild"], "lean": ["muscle", "powerbuild"], "general": ["strength", "powerbuild"],
                  "powerlifting": ["strength"], "olympic": ["weightlifting"], "crossfit": ["functional"], "hybrid": ["hybrid"],
                  "run_5k_10k": ["run"], "run_half": ["run"], "run_marathon": ["run"], "hyrox": ["hyrox"], "meet": ["strength"],
                  "lifting": ["muscle", "powerbuild", "strength"], "fitness": ["functional", "hybrid"], "mix": ["health", "muscle"]}
# The shape of each program's week, to keep the shape of a routine someone already runs (mode improve).
SPLIT_OF = {"muscle-ppl-6": "ppl", "muscle-upperlower-4": "upper_lower", "muscle-fullbody-3": "full_body",
            "muscle-bodypart-5": "body_part", "powerbuild-phul-4": "upper_lower", "powerbuild-phat-5": "body_part",
            "strength-rpe-4": "upper_lower", "strength-531-bbb-4": "upper_lower", "strength-gzclp-4": "full_body",
            "strength-lp-3": "full_body", "strength-texas-3": "full_body", "strength-531-beginners-3": "full_body",
            "weightlifting-novice-3": "full_body", "health-baseline-2to3": "full_body", "functional-gpp-3to5": "classes",
            "hyrox-prep-4": "strength_cardio", "hybrid-strength-endurance-4to6": "strength_cardio",
            "run-base-3to5": "run_plan", "run-c25k-3": "run_plan"}
# A preferred style (asked of experienced people only) and the family it names.
STYLE_FAMILY = {"strength": ["strength"], "bodybuilding": ["muscle"], "powerbuilding": ["powerbuild"],
                "crossfit": ["functional"], "hyrox": ["hyrox"], "running": ["run"], "hybrid": ["hybrid"]}
STYLE_WORDS = {"strength": "strength training", "bodybuilding": "bodybuilding", "powerbuilding": "power-building",
               "crossfit": "CrossFit-style training", "hyrox": "HYROX-style training", "running": "running",
               "hybrid": "hybrid training"}


def style_pref(prof):
    """The style they asked for, or None: beginners are never asked, and 'trainer' means the trainer decides."""
    st = prof.get("style_pref")
    experienced = prof.get("mode") == "improve" or prof.get("experience") in ("intermediate", "advanced") or \
        any(v in ("intermediate", "advanced") for v in (prof.get("experience_by") or {}).values())
    return st if st in STYLE_FAMILY and experienced else None


# Which activity's experience counts for a family (Step 1). Conditioning families take the higher of lifting and
# conditioning, capped one step above the lower.
DOMAIN = {"run": "running", "hyrox": "mixed", "hybrid": "mixed", "functional": "mixed"}
PLAIN = {"strength": "Strength first: heavy main lifts, then muscle work",
         "powerbuild": "Strength and size: heavy days and muscle days",
         "muscle": "Muscle building: plenty of sets that end near your limit",
         "weightlifting": "The Olympic lifts: technique first, then strength",
         "functional": "Mixed fitness: a strength part, then a short fast workout",
         "hyrox": "Race training: running plus the HYROX stations",
         "hybrid": "Strength and running in the same week",
         "run": "Running, mostly easy, building up week by week",
         "health": "Full body strength with easy cardio"}
SHAPE = {"ppl": "push, pull and legs days", "upper_lower": "upper body and lower body days", "full_body": "full body every session",
         "body_part": "one or two muscle groups a day", "strength_cardio": "strength days and running days",
         "run_plan": "runs of different kinds", "classes": "a new mix every session"}
EVIDENCE = {"A": 2, "B": 1, "C": 0, "G": 2}
PREGNANCY_OK = {"health-baseline-2to3"}
ALWAYS = ("health-baseline-2to3",)                   # the gentle start-here plan that fits almost anyone in a gym
GOAL_WORDS = {"muscle": "building muscle", "strength": "getting stronger", "powerlifting": "powerlifting",
              "weightlifting": "the Olympic lifts", "functional": "all-round fitness", "hyrox": "HYROX",
              "run": "running", "skills": "bodyweight skills", "fat_loss": "losing fat", "health": "feeling healthier",
              "independent": "staying strong as you age"}
FIT_WORDS = {3: "Built for %s", 2: "Good for %s", 1: "Only partly serves %s", 0: "Not built for %s"}
SERVES = 2                                           # a goal fit of 2 or 3 means the program serves the goal
FIXED = ("age:", "pregnancy:", "bone density:", "seated:", "experience:", "not for me:")   # blockers a person cannot change today


def _age_num(band):
    return {"under_18": 17, "18_39": 30, "40_59": 50, "60_74": 67, "75_plus": 80}.get(band, 30)


def filters(prog, prof, bank, select, cost=None):
    """The list of reasons this program is out. Empty list: it passes. The days that count are the days the
    composer gives this program's family (compose.lead_days): a 60/40 blend on 4 days leaves the lead 2 or 3.
    A main slot that only a limit empties costs score (`cost`), it does not rule the program out, unless it
    empties more than half the main slots of a session: a limit removes moves, never the goal (03_MATRIX.md)."""
    import compose
    out = []
    flags = set((prof.get("screen") or {}).get("flags", []))
    exp = domain_experience(prof, prog["family"])
    days = compose.lead_days(prof, prog["family"])
    if any(r.get("program") == prog["id"] and r.get("reason") != "days" for r in prof.get("rejected", [])):
        out.append("not for me: you turned it down")
    if exp not in prog["experience"]:
        out.append("experience: it is built for %s" % " or ".join(prog["experience"]))
    if days < prog["days"][0]:
        out.append("days: it needs at least %d a week" % prog["days"][0])
    else:
        n = min(days, prog["days"][1])
        lay = prog["layouts"].get(str(n))
        if lay is None:
            out.append("days: it has no %d day week" % n)
        elif len(lay) > n and not prog.get("rotates"):
            out.append("days: its %d sessions need %d days, never squeezed into %d" % (len(lay), len(lay), n))
    if prof.get("minutes", 45) < prog.get("express_minutes", prog["minutes"][0]):
        out.append("minutes: its shortest version takes %d" % prog.get("express_minutes", prog["minutes"][0]))
    tags = set(core.place_tags(prof))
    miss = [t for t in prog.get("equipment_all", []) if t not in tags]
    miss += ["one of " + "/".join(any_) for any_ in prog.get("equipment_any", []) if not (set(any_) & tags)]
    if miss:
        out.append("equipment: needs " + ", ".join(miss))
    skills = set(prof.get("skills", []))
    for sk in prog.get("skills_required", []):
        if sk not in skills:
            out.append("skill: needs " + sk.replace("_", " "))
    ex = set(prog.get("excluded_for", []))
    age = _age_num(prof.get("age_band"))
    if "pregnant" in flags and prog["id"] not in PREGNANCY_OK:
        out.append("pregnancy: only gentle full body programs during pregnancy")
    if "low_bone_density" in flags and "low_bone_density" in ex:
        out.append("bone density: heavy or impact loading only with a physio")
    if prof.get("position") == "seated" and "seated" in ex:
        out.append("seated: its main lifts need standing")
    if "under_60" in ex and age < 60:
        out.append("age: built for 60 and over")
    if "over_60" in ex and age >= 60:
        out.append("age: not built for 60 and over")
    if not out:                                      # can its main blocks actually be filled for this person, limits included?
        import build as _b
        avoid = _b.avoid_regions(prof, {})
        lim = dict(prof, _care=_b.care_regions(prof, {}) - avoid, _trig=_b.trigger_limits(prof))
        free = dict(prof, limits=[], _care=set(), _trig=[])
        soft = 0
        for sid, sess in prog["sessions"].items():
            mains = [sl for b in sess["blocks"] if b["kind"] == "main" for sl in b["slots"] if sl.get("kind") != "piece"]
            gone = []
            for slot in mains:
                if select(slot, lim, list(tags), avoid, bank) is None:
                    if select(slot, free, list(tags), set(), bank) is None:
                        out.append("can't fill '%s' in session %s with your equipment" % (slot["key"], sid))
                        break
                    gone.append(slot)
            if out:
                break
            if gone and 2 * len(gone) > len(mains):
                out.append("can't fill '%s' in session %s with your limits" % (gone[0]["key"], sid))
                break
            soft += len(gone)
        if cost is not None and not out:
            cost[prog["id"]] = soft
    return out


def domain_experience(prof, family):
    """The experience that counts for this family. Without experience_by (an older profile), the one experience."""
    by = prof.get("experience_by")
    exp = prof.get("experience", "none")
    if not by:
        return exp
    lv = core.EXPERIENCE
    dom = DOMAIN.get(family, "lifting")
    if dom == "running":
        return by.get("running", "none")
    if dom == "mixed":
        cond = max((by.get(a, "none") for a in ("running", "cardio", "classes", "crossfit")), key=lv.index)
        hi, lo = max(exp, cond, key=lv.index), min(exp, cond, key=lv.index)
        return lv[min(lv.index(hi), lv.index(lo) + 1)]
    return exp


def enjoys(prof):
    if prof.get("enjoys"):
        return set(prof["enjoys"])
    return {LEGACY_LIKES[x] for x in prof.get("likes", []) if x in LEGACY_LIKES}


def avoids(prof):
    out = set(prof.get("avoids", [])) | {LEGACY_LIKES[x] for x in prof.get("dislikes", []) if x in LEGACY_LIKES and x != "machines"}
    if any(r.get("reason") == "too_much_running" for r in prof.get("rejected", [])):
        out.add("running")
    return out


def score(prog, prof, programs_by_id=None):
    g1, g2 = prof.get("goal"), prof.get("goal2")
    s = 3 * prog["goals"].get(g1, 0) + (1.5 * prog["goals"].get(g2, 0) if g2 else 0)
    s += EVIDENCE.get(prog.get("evidence", "C"), 0)
    acts = set(ENJOY_OF.get(prog["family"], []))
    if acts & enjoys(prof):
        s += 2
    if acts & avoids(prof):
        s -= 3
    if prog["family"] in OUTCOME_FAMILY.get(prof.get("outcome_detail"), []):
        s += 2
    rt = prof.get("current_routine") or {}
    if prof.get("mode") == "improve" and rt:
        if SPLIT_OF.get(prog["id"]) == rt.get("split"):
            s += 2                                   # keep the shape of the week they already run
        if isinstance(rt.get("days"), int) and prog["days"][0] <= rt["days"] <= prog["days"][1]:
            s += 1
    for r in prof.get("rejected", []):
        other = (programs_by_id or {}).get(r.get("program"))
        if not other:
            continue
        if r.get("reason") == "too_long" and prog["minutes"][0] >= other["minutes"][0]:
            s -= 2
        if r.get("reason") == "not_enjoy" and prog["family"] == other["family"]:
            s -= 3
    import compose
    days = compose.lead_days(prof, prog["family"])
    if days in prog.get("sweet_days", []):
        s += 1
    if days - prog["days"][1] >= 2:
        s -= 2                                       # it would leave two or more of their days empty
    return s


def match(prof, bank, select, programs=None):
    programs = programs or core.all_programs()
    passed, failed, cost = [], {}, {}
    for p in programs:
        why = filters(p, prof, bank, select, cost)
        if why:
            failed[p["id"]] = why
        else:
            passed.append(p)
    novice = prof.get("experience") in ("none", "novice")
    by_id = {p["id"]: p for p in programs}

    total = lambda p: score(p, prof, by_id) - cost.get(p["id"], 0)

    def key(p):
        return (-total(p), -p["goals"].get(prof.get("goal"), 0), p.get("simplicity", 2) if novice else 0,
                -EVIDENCE.get(p.get("evidence", "C"), 0), p.get("express_minutes", 30), p["id"])
    ranked = sorted(passed, key=key)
    style_note = None
    st = style_pref(prof)
    if st:                                           # a filter where the style serves the outcome, else an honest line
        fam = STYLE_FAMILY[st]
        mine = [p for p in ranked if p["family"] in fam]
        fits = [p for p in mine if p["goals"].get(prof.get("goal"), 0) >= SERVES
                or p["family"] in OUTCOME_FAMILY.get(prof.get("outcome_detail"), [])]
        if fits:
            ranked = fits + [p for p in ranked if p not in fits]
        elif ranked:
            why = ("nothing in %s fits your week, kit or experience" % STYLE_WORDS[st]) if not mine else \
                  ("%s is not built for %s" % (STYLE_WORDS[st], GOAL_WORDS.get(prof.get("goal"), prof.get("goal"))))
            style_note = "You prefer %s, but %s, so the trainer picked what serves your goal better." % (STYLE_WORDS[st], why)
    gap = goal_gap(prof, failed, programs)
    top = [{"id": p["id"], "name": p["name"], "score": total(p), "family": p["family"],
            "split": SPLIT_OF.get(p["id"]), "evidence": p.get("evidence"), "draws_from": p.get("draws_from", []),
            "goal_fit": p["goals"].get(prof.get("goal"), 0), "why": reason(p, prof, gap), "plain": plain(p, prof)}
           for p in ranked[:3]]
    res = {"top": top, "passed": [p["id"] for p in ranked], "failed": failed}
    if top:
        res["plan"] = top[0]                         # one plan; the runner-up stays internal (Step 4)
        res["runner_up"] = top[1]["id"] if len(top) > 1 else None
    if style_note:
        res["style_note"] = style_note
    note = core.OUTCOME_GAP.get(prof.get("outcome_detail")) or core.OUTCOME_GAP.get(prof.get("outcome"))
    if note:
        res["outcome_note"] = note
    pn = core.OUTCOME_PLAN.get(prof.get("outcome_detail")) or core.OUTCOME_PLAN.get(prof.get("outcome"))
    if pn:
        res["plan_note"] = pn
    if prof.get("mode") == "improve":
        res["improve_note"] = ("Your classes stay yours as they are: the trainer cannot write a class. This is the plan closest "
                               "to the rest of your week.")
    if prof.get("start_volume") == "low":
        res["dose_note"] = ("Short sleep or high stress: the first weeks start at the low end of the sets, and the effort "
                            "stays a rep further from failure.")
    if not top or top[0]["goal_fit"] < SERVES:
        res["fallback"] = fallback(prof, failed, programs, bank, select)
        if gap:
            res["goal_gap"] = gap
    return res


def _blocker(why):
    """The plain-words blocker of a failed program, or None when it is one the person cannot change today."""
    for w in why:
        if w.startswith(FIXED):
            return None
    eq = [w.split("needs ", 1)[1] for w in why if w.startswith("equipment:")]
    if eq:
        kit = [k.strip().replace("pullup_bar", "pull-up bar").replace("_", " ") for k in eq[0].split(",")]
        if kit[0].startswith("one of "):                 # an any-group: "a rower, bike, ski erg or treadmill"
            alts = [k.replace("skierg", "ski erg") for k in kit[0][7:].split("/")]
            return "needs a " + (alts[0] if len(alts) == 1 else ", ".join(alts[:-1]) + " or " + alts[-1])
        return "needs a " + (kit[0] if len(kit) == 1 else ", ".join(kit[:-1]) + " and " + kit[-1])
    return why[0].split(": ", 1)[-1] if why else None


def goal_gap(prof, failed, programs):
    """When nothing that serves the main goal passed: one line saying why, so the offer never looks random."""
    goal = prof.get("goal")
    serving = [p for p in programs if p["goals"].get(goal, 0) >= SERVES]
    if any(p["id"] not in failed for p in serving):
        return None
    if not serving:
        return "no program here is built for %s yet" % GOAL_WORDS.get(goal, goal)
    seen, parts = set(), []
    for p in sorted(serving, key=lambda p: (len(failed[p["id"]]), -p["goals"][goal], p["id"])):
        b = _blocker(failed[p["id"]])
        if b and b not in seen:
            seen.add(b)
            parts.append("%s %s" % (p["name"], b))
        if len(parts) == 2:
            break
    if not parts:
        return "nothing built for %s fits your experience, age or position yet" % GOAL_WORDS.get(goal, goal)
    return "nothing built for %s fits your kit: %s" % (GOAL_WORDS.get(goal, goal), "; ".join(parts))


def reason(prog, prof, gap=None):
    """One short human line: why this program is on the list. The coach translates it, never recomputes it."""
    import compose
    g1, g2 = prof.get("goal"), prof.get("goal2")
    fit = prog["goals"].get(g1, 0)
    bits = [FIT_WORDS[fit] % GOAL_WORDS.get(g1, g1)]
    if g2 and prog["goals"].get(g2, 0) >= SERVES:
        bits[0] += ", and " + GOAL_WORDS.get(g2, g2)
    week, al = compose.describe(prof, prog)
    days = al["lead"]
    if days in prog.get("sweet_days", []) and not al["components"]:
        bits.append("%d days a week is its sweet spot" % days)
    elif days > prog["days"][1] and not al["components"]:
        bits.append("uses %d of your %d days" % (prog["days"][1], days))
    liked = set(ENJOY_OF.get(prog["family"], [])) & enjoys(prof)
    if liked:
        bits.append("the %s you enjoy" % " and ".join(ENJOY_WORDS[x] for x in sorted(liked)))
    rt = prof.get("current_routine") or {}
    if prof.get("mode") == "improve" and SPLIT_OF.get(prog["id"]) == rt.get("split"):
        bits.append("the same shape as your week")
    blend = prof.get("outcomes") or []
    if len(blend) > 1:
        words = ["%s %d%%" % (GOAL_WORDS.get(core.OUTCOMES[o["id"]][o["detail"]][0], o["id"]), round(100 * o["share"])) for o in blend]
        bits.append("your blend: %s, so your week is %s" % (", ".join(words), week))
    elif al["components"] or al["finishers"]:
        bits.append("your week: %s" % week)
    bits.append("evidence %s" % prog.get("evidence", "C"))
    if fit < SERVES and gap:
        bits[0] += " (nothing built for it fits you yet)"
    return " · ".join(bits)


def plain(prog, prof):
    """The plan in plain words, for the person: never a method name (Step 4). The page and the coach translate it."""
    import compose
    week, al = compose.describe(prof, prog)
    days = min(al["lead"], prog["days"][1]) + sum(al["components"].values())
    mins = max(prog.get("express_minutes", 30), min(prof.get("minutes", 45), prog["minutes"][1]))
    shape = SHAPE.get(SPLIT_OF.get(prog["id"]))
    if al["components"] or al["finishers"]:
        return {"headline": PLAIN.get(prog["family"], prog["name"]),
                "week": "%d days a week, about %d minutes: %s" % (days, mins, week)}
    return {"headline": PLAIN.get(prog["family"], prog["name"]),
            "week": "%d days a week, about %d minutes%s" % (days, mins, (", " + shape) if shape else "")}


def fallback(prof, failed, programs, bank, select):
    """Step 5: never an empty answer. What would make a program fit, and the nearest supported goal."""
    hints = []
    goal = prof.get("goal")
    for p in programs:
        if p["goals"].get(goal, 0) < SERVES or p["id"] not in failed:
            continue
        why = failed[p["id"]]
        if len(why) == 1 and not why[0].startswith(FIXED):
            hints.append({"id": p["id"], "name": p["name"], "only_blocker": why[0]})
    near = None
    if not any(p["goals"].get(goal, 0) >= SERVES for p in programs):
        near = "this goal is not served yet: the nearest is " + ("health" if goal != "health" else "muscle")
    always = [i for i in ALWAYS if i not in failed]
    out = {"one_change_away": hints[:3], "goal_note": near, "always_available": always}
    if not always and not hints:
        out["nothing_fits"] = ("Nothing in this trainer fits safely yet. Say so plainly, and suggest a qualified coach or, for seated "
                               "training, an adaptive fitness professional.")
    return out
