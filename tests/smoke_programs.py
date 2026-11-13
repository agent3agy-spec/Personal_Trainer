#!/usr/bin/env python3
"""smoke_programs.py · every program, run for ten sessions in a throwaway copy, through the real commands.

    python3 tests/smoke_programs.py            all programs
    python3 tests/smoke_programs.py <id> ...   only these
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


def one(pid):
    prog = core.load_program(pid)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="pt_"))
    try:
        shutil.copytree(REPO, tmp / "r", ignore=shutil.ignore_patterns(".git", "sessions", "me"))
        cwd = tmp / "r"
        (cwd / "me").mkdir()
        (cwd / "sessions").mkdir()
        prof = profile_for(prog)
        (cwd / "me" / "a.json").write_text(json.dumps({"items": [], "language": "en"}))
        assert run(cwd, "screen", "me/a.json")["result"] == "clear"
        (cwd / "me" / "a.json").write_text(json.dumps(prof))
        r = run(cwd, "profile", "me/a.json")
        assert r.get("ok"), r
        r = run(cwd, "choose", pid)
        assert r.get("ok"), ("choose", r)
        problems = []
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
    ids = sys.argv[1:] or [p["id"] for p in core.all_programs()]
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
