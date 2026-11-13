#!/usr/bin/env python3
"""smoke_programs.py · every program, run for ten sessions in a throwaway copy, through the real commands.

    python3 tests/smoke_programs.py            all programs
    python3 tests/smoke_programs.py <id> ...   only these (a program id, or improve:<persona>)
For each program: a profile that fits it, the screen, choose, then ten build + log rounds (one with low
energy, one with a missed set, one with knee pain), and two sheets rendered. It fails on any crash,
any refused sheet, any session over the minutes, and any state that does not pass its check.
"""
import json, pathlib, shutil, subprocess, sys, tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "engine"))
import core  # noqa: E402

EVERYTHING = ["full_gym", "rings", "skierg", "sled", "sandbag", "jump_rope", "mini_band", "suspension", "crossfit_box"]


def run(cwd, *args):
    r = subprocess.run([sys.executable, "engine/plan.py"] + list(args), cwd=cwd, capture_output=True, text=True)
    try:
        return json.loads(r.stdout[r.stdout.index("{"):]) if "{" in r.stdout else {"raw": r.stdout, "err": r.stderr}
    except Exception:
        return {"raw": r.stdout[-400:], "err": r.stderr[-800:]}


def profile_for(p):
    exp = p["experience"][-1] if "advanced" not in p["experience"] else "intermediate"
    if exp not in p["experience"]:
        exp = p["experience"][0]
    goal = max(p["goals"], key=lambda g: p["goals"][g])
    return {"goal": goal, "experience": exp, "days": (p.get("sweet_days") or p["days"])[0],
            "minutes": max(p["minutes"][0], min(60, p["minutes"][1])),
            "places": {"main": {"type": "gym", "equipment": EVERYTHING}}, "units": "kg",
            "skills": ["olympic_coached", "run_30min", "pullup"]}


def _ex(*items):
    return [{"name": n, "sets": s, "reps": r} for n, s, r in items]


# The improve path (engine/improve.py): routines people bring, adopted, one proposal accepted, then ten sessions.
GYM = {"main": {"type": "gym", "equipment": ["full_gym"]}}
IMPROVE = {
    "bro_split_5": {"outcome": "look", "outcome_detail": "size", "minutes": 75, "places": GYM, "priority": ["arms"],
                    "current_routine": {"split": "body_part", "days": 5, "age": "over_1y", "stalls": ["not_growing"], "keep": ["split"],
                                        "day_labels": ["Chest", "Back", "Legs", "Shoulders", "Arms"],
                                        "day_kinds": ["chest", "back", "legs", "shoulders", "arms"],
                                        "exercises": {"Chest": _ex(("bench press", 4, "6-8"), ("incline db press", 3, "8-12"), ("pec deck", 3, "12-15")),
                                                      "Back": _ex(("deadlift", 3, "5"), ("lat pulldown", 4, "8-12"), ("cable row", 3, "10-12")),
                                                      "Legs": _ex(("squat", 4, "6-8"), ("leg press", 3, "10-12"), ("leg curl", 3, "10-15")),
                                                      "Shoulders": _ex(("ohp", 4, "6-8"), ("lateral raises", 4, "12-15"), ("face pulls", 3, "15")),
                                                      "Arms": _ex(("barbell curl", 3, "8-12"), ("skullcrushers", 3, "8-12"), ("hammer curls", 3, "10-12"))}}},
    "upper_lower_home_4": {"outcome": "strong", "outcome_detail": "general", "minutes": 45,
                           "places": {"main": {"type": "home_gym", "equipment": ["dumbbell", "bench", "pullup_bar"]}}, "dumbbells": [6, 10, 14, 18],
                           "limits": [{"region": "shoulder", "status": "mild", "triggers": ["overhead"]}],
                           "current_routine": {"split": "upper_lower", "days": 4, "age": "3_12m", "stalls": ["tired"],
                                               "day_labels": ["Upper", "Lower", "Upper", "Lower"], "day_kinds": ["upper", "lower", "upper", "lower"],
                                               "exercises": {"Upper": _ex(("DB bench", 4, "8-10"), ("pull ups", 4, "6-8"), ("seated db press", 3, "8-10"), ("db curl", 3, "10-12")),
                                                             "Lower": _ex(("goblet squat", 4, "8-12"), ("db rdl", 3, "8-12"), ("bulgarian split squat", 3, "8-10"), ("my calf thing", 3, "15"))}}},
    "runner_4": {"outcome": "event", "outcome_detail": "run_5k_10k", "minutes": 50, "skills": ["run_30min"],
                 "places": {"main": {"type": "outdoors", "equipment": ["outdoors"]}},
                 "current_routine": {"split": "run_plan", "days": 4, "age": "over_1y", "stalls": ["fine"],
                                     "day_labels": ["Easy run", "Intervals", "Easy run", "Long run"], "day_kinds": ["easy", "intervals", "easy", "long"],
                                     "exercises": {}}},
    "classes_plus_lifting": {"outcome": "athletic", "outcome_detail": "crossfit", "minutes": 60,
                             "places": {"main": {"type": "gym", "equipment": ["crossfit_box"]}},
                             "current_routine": {"split": "custom", "days": 4, "age": "1_3m", "stalls": ["lift_stuck"], "stuck": ["back_squat"],
                                                 "day_labels": ["Strength A", "Class", "Strength B", "Class"], "day_kinds": ["d1", "class", "d2", "class"],
                                                 "exercises": {"Strength A": _ex(("back squat", 5, "5"), ("bench press", 5, "5"), ("pendlay row", 3, "8")),
                                                               "Strength B": _ex(("deadlift", 3, "5"), ("overhead press", 5, "5"), ("pull up", 3, "8"))}}},
    "ppl_6_long_days": {"outcome": "look", "outcome_detail": "size", "minutes": 60, "places": GYM,
                        "current_routine": {"split": "ppl", "days": 6, "age": "over_1y", "keep": ["exercises"],
                                            "day_labels": ["Push", "Pull", "Legs", "Push", "Pull", "Legs"],
                                            "day_kinds": ["push", "pull", "legs", "push", "pull", "legs"],
                                            "exercises": {"Push": _ex(("bench press", 5, "5"), ("incline bench", 4, "8"), ("dips", 4, "10"), ("lateral raises", 5, "15"), ("pushdowns", 4, "12")),
                                                          "Pull": _ex(("barbell rows", 5, "5"), ("pull ups", 4, "8"), ("face pulls", 4, "15"), ("curls", 4, "12")),
                                                          "Legs": _ex(("squat", 5, "5"), ("rdl", 4, "8"), ("leg press", 4, "12"), ("calf raises", 5, "15"))}}},
}


def one(pid):
    improve_answers = IMPROVE.get(pid.split(":", 1)[1]) if pid.startswith("improve:") else None
    prog = core.load_program(pid) if improve_answers is None else None
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="pt_"))
    try:
        shutil.copytree(REPO, tmp / "r", ignore=shutil.ignore_patterns(".git", "sessions", "me"))
        cwd = tmp / "r"
        (cwd / "me").mkdir()
        (cwd / "sessions").mkdir()
        prof = dict(improve_answers, mode="improve", units="kg") if improve_answers else profile_for(prog)
        (cwd / "me" / "a.json").write_text(json.dumps({"items": [], "language": "en"}))
        assert run(cwd, "screen", "me/a.json")["result"] == "clear"
        (cwd / "me" / "a.json").write_text(json.dumps(prof))
        r = run(cwd, "profile", "me/a.json")
        assert r.get("ok"), r
        problems = []
        if improve_answers:
            r = run(cwd, "adopt")
            assert r.get("ok"), ("adopt", r)
            if r["proposals"]:
                a = run(cwd, "improve", "accept", r["proposals"][0]["id"])
                if not a.get("ok"):
                    problems.append(("accept", a))
            if r["proposals"][1:]:
                d = run(cwd, "improve", "decline", r["proposals"][1]["id"])
                if not d.get("ok") or r["proposals"][1]["id"] in [x["id"] for x in d["proposals"]]:
                    problems.append(("decline", d))
        else:
            r = run(cwd, "choose", pid)
            assert r.get("ok"), ("choose", r)
        for i in range(10):
            date = "2026-12-%02d" % (i * 2 + 1)
            today = {"energy": 4 if i == 3 else 8, "minutes": prof["minutes"], "date": date}
            if i == 6:
                today["pain"] = [{"region": "knee", "score": 2}]
            (cwd / "me" / "t.json").write_text(json.dumps(today))
            b = run(cwd, "build", "me/t.json")
            if not b.get("ok"):
                problems.append(("build", i, b))
                break
            if b["minutes"] > b["asked"] + 3:
                problems.append(("over minutes", i, b["minutes"], b["asked"]))
            if i in (0, 9):
                rr = run(cwd, "render", b["session"])
                if not rr.get("ok") or rr.get("pages", 1) > 1:
                    problems.append(("render", i, rr))
            report = {"as_written": True, "date": date, "results": {}}
            s = json.loads((cwd / b["session"]).read_text())
            for blk in s["blocks"]:
                for it in blk["items"]:
                    sl = it.get("_slot")
                    if not sl:
                        continue
                    if sl["rule"] == "benchmark":
                        report["results"][sl["key"]] = {"score": "%d rounds" % (5 + i)}
                    elif it.get("first_outing") and sl["load_type"] not in ("bodyweight", "band", "time", "distance", "calories"):
                        report["results"][sl["key"]] = {"load": 20}
                    elif i == 5 and blk["kind"] == "main" and sl["rule"] in ("linear_session", "double_progression"):
                        report["results"][sl["key"]] = {"reps": [1] * int(it.get("sets") or 1)}
            (cwd / "me" / "r.json").write_text(json.dumps(report))
            lg = run(cwd, "log", "me/r.json")
            if not lg.get("ok"):
                problems.append(("log", i, lg))
                break
        chk = subprocess.run([sys.executable, "engine/checks.py"], cwd=cwd, capture_output=True, text=True)
        if chk.returncode:
            problems.append(("checks", chk.stdout[-500:]))
        st = json.loads((cwd / "me" / "state.json").read_text())
        return problems, {"block": st["block"], "week": st["week"], "sessions": st.get("sessions_done")}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    ids = sys.argv[1:] or [p["id"] for p in core.all_programs()] + ["improve:" + k for k in IMPROVE]
    bad = 0
    for pid in ids:
        try:
            probs, info = one(pid)
        except AssertionError as e:
            probs, info = [("setup", str(e)[:600])], {}
        except Exception as e:
            probs, info = [("crash", repr(e)[:600])], {}
        print(("OK  " if not probs else "FAIL"), pid, info)
        for p in probs:
            bad += 1
            print("     ", str(p)[:700])
    sys.exit(1 if bad else 0)
