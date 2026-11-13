"""match.py · which program fits this person, by a fixed rule (doctrine/03_MATRIX.md).

Step 1 hard filters · Step 2 the score · Step 3 tie-breaks · Step 4 the top three · Step 5 never empty.
The coach explains the result; it never computes it.
"""
import core

STYLE_OF = {"strength": ["barbell"], "powerbuild": ["barbell", "machines"], "muscle": ["machines", "dumbbells"],
            "weightlifting": ["barbell"], "functional": ["circuits", "classes"], "hyrox": ["running", "circuits"],
            "hybrid": ["running", "barbell"], "run": ["running"], "calisthenics": ["bodyweight"],
            "kettlebell": ["kettlebells"], "home": ["dumbbells", "bodyweight"], "health": ["dumbbells", "machines"],
            "older": ["dumbbells", "machines"]}
EVIDENCE = {"A": 2, "B": 1, "C": 0, "G": 2}
PREGNANCY_OK = {"health-baseline-2to3", "home-fullbody-2to4"}


def _age_num(band):
    return {"under_18": 17, "18_39": 30, "40_59": 50, "60_74": 67, "75_plus": 80}.get(band, 30)


def filters(prog, prof, bank, select):
    """The list of reasons this program is out. Empty list: it passes."""
    out = []
    flags = set((prof.get("screen") or {}).get("flags", []))
    exp = prof.get("experience", "none")
    if exp not in prog["experience"]:
        out.append("experience: it is built for %s" % " or ".join(prog["experience"]))
    if prof.get("days", 3) < prog["days"][0]:
        out.append("days: it needs at least %d a week" % prog["days"][0])
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
        prof = dict(prof, _care=_b.care_regions(prof, {}) - avoid)
        for sid, sess in prog["sessions"].items():
            for b in sess["blocks"]:
                if b["kind"] != "main":
                    continue
                for slot in b["slots"]:
                    if slot.get("kind") == "piece":
                        continue
                    if select(slot, prof, list(tags), avoid, bank) is None:
                        out.append("can't fill '%s' in session %s with your equipment or limits" % (slot["key"], sid))
                        break
    return out


def score(prog, prof):
    g1, g2 = prof.get("goal"), prof.get("goal2")
    s = 3 * prog["goals"].get(g1, 0) + (1.5 * prog["goals"].get(g2, 0) if g2 else 0)
    s += EVIDENCE.get(prog.get("evidence", "C"), 0)
    styles = set(STYLE_OF.get(prog["family"], []))
    if styles & set(prof.get("likes", [])):
        s += 2
    if styles & set(prof.get("dislikes", [])):
        s -= 3
    if prof.get("days") in prog.get("sweet_days", []):
        s += 1
    if prof.get("days", 3) - prog["days"][1] >= 2:
        s -= 2                                       # it would leave two or more of their days empty
    if "under_60" in prog.get("excluded_for", []) and _age_num(prof.get("age_band")) >= 60:
        s += 1                                       # a program built for their age group
    return s


def match(prof, bank, select, programs=None):
    programs = programs or core.all_programs()
    passed, failed = [], {}
    for p in programs:
        why = filters(p, prof, bank, select)
        if why:
            failed[p["id"]] = why
        else:
            passed.append(p)
    novice = prof.get("experience") in ("none", "novice")

    def key(p):
        return (-score(p, prof), p.get("simplicity", 2) if novice else 0,
                -EVIDENCE.get(p.get("evidence", "C"), 0), p.get("express_minutes", 30), p["id"])
    ranked = sorted(passed, key=key)
    top = [{"id": p["id"], "name": p["name"], "score": score(p, prof), "family": p["family"],
            "evidence": p.get("evidence"), "draws_from": p.get("draws_from", []),
            "goal_fit": p["goals"].get(prof.get("goal"), 0)} for p in ranked[:3]]
    res = {"top": top, "passed": [p["id"] for p in ranked], "failed": failed}
    if not top or top[0]["goal_fit"] == 0:
        res["fallback"] = fallback(prof, failed, programs, bank, select)
    return res


def fallback(prof, failed, programs, bank, select):
    """Step 5: never an empty answer. What would make a program fit, and the nearest supported goal."""
    hints = []
    goal = prof.get("goal")
    for p in programs:
        if p["goals"].get(goal, 0) < 2 or p["id"] not in failed:
            continue
        why = failed[p["id"]]
        if len(why) == 1:
            hints.append({"id": p["id"], "name": p["name"], "only_blocker": why[0]})
    near = None
    if not any(p["goals"].get(goal, 0) >= 2 for p in programs):
        near = "this goal is not served yet: the nearest is " + ("health" if goal != "health" else "muscle")
    always = [i for i in ("health-baseline-2to3", "home-fullbody-2to4") if i not in failed]
    out = {"one_change_away": hints[:3], "goal_note": near, "always_available": always}
    if not always and not hints:
        out["nothing_fits"] = ("Nothing in this trainer fits safely yet. Say so plainly, and suggest a qualified coach or, for seated "
                               "training, an adaptive fitness professional.")
    return out
