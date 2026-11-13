#!/usr/bin/env python3
"""test_engine.py · the rules that are code, proven. Run: python3 tests/test_engine.py

Covers the screen, the matrix worked examples of doctrine/03_MATRIX.md, every progression rule,
the readiness dose, the clock and its refusal, the first-outing protocol, pregnancy and seated
filters, and the rebuild of state from the log.
"""
import json, pathlib, shutil, subprocess, sys, tempfile, unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "engine"))
import core, screen, match, build, progress, sheet  # noqa: E402

BANK = core.load_bank()


def prof(**kw):
    p = {"language": "en", "units": "kg", "age_band": "18_39", "goal": "strength", "experience": "none", "days": 3,
         "minutes": 60, "places": {"main": {"type": "gym", "equipment": ["full_gym"]}}, "default_place": "main",
         "screen": {"result": "clear", "flags": []}, "likes": [], "dislikes": [], "limits": [], "skills": []}
    p.update(kw)
    return p


def top(p):
    return [t["id"] for t in match.match(p, BANK, build.select)["top"]]


class Screen(unittest.TestCase):
    def test_clear(self):
        self.assertEqual(screen.run({"items": [], "age_band": "18_39"})["result"], "clear")

    def test_parq_stops_until_cleared(self):
        self.assertEqual(screen.run({"items": [2], "age_band": "40_59"})["result"], "stop")
        self.assertEqual(screen.run({"items": [2], "age_band": "40_59", "cleared": True})["result"], "clear")

    def test_under_18(self):
        self.assertEqual(screen.run({"items": [], "age_band": "under_18", "cleared": True})["result"], "stop")

    def test_pregnancy_needs_provider(self):
        r = screen.run({"items": [8], "age_band": "18_39"})
        self.assertEqual(r["result"], "needs_ok")
        self.assertIn("pregnant", screen.run({"items": [8], "age_band": "18_39", "provider_ok": True})["flags"])


class Matrix(unittest.TestCase):
    def test_novice_strength(self):
        self.assertEqual(top(prof(likes=["barbell"]))[0], "strength-lp-3")

    def test_muscle_intermediate(self):
        t = top(prof(goal="muscle", experience="intermediate", days=4, minutes=75))
        self.assertTrue(set(t[:2]) & {"muscle-upperlower-4", "powerbuild-phul-4"}, t)

    def test_older(self):
        t = top(prof(goal="independent", age_band="60_74", minutes=45, places={"main": {"equipment": ["basic_gym"]}}))
        self.assertEqual(t[0], "older-strong-3")

    def test_home_fat_loss(self):
        t = top(prof(goal="fat_loss", minutes=30, places={"main": {"equipment": ["home_dumbbells"]}}, dumbbells=[8]))
        self.assertEqual(t[0], "home-fullbody-2to4")

    def test_park_skills(self):
        t = top(prof(goal="skills", experience="novice", places={"main": {"equipment": ["park"]}}))
        self.assertEqual(t[0], "calisthenics-rr-3")

    def test_hyrox(self):
        t = top(prof(goal="hyrox", experience="intermediate", days=5, skills=["run_30min"],
                     places={"main": {"equipment": ["crossfit_box", "sled", "skierg"]}}))
        self.assertEqual(t[0], "hyrox-prep-4")

    def test_pregnancy_only_gentle(self):
        p = prof(goal="health", screen={"result": "clear", "flags": ["pregnant"]})
        self.assertTrue(set(match.match(p, BANK, build.select)["passed"]) <= match.PREGNANCY_OK)

    def test_never_empty(self):
        r = match.match(prof(goal="powerlifting", days=2, minutes=15), BANK, build.select)
        self.assertTrue(r["top"] or r.get("fallback"))

    def test_seated_gets_something(self):
        r = match.match(prof(goal="strength", position="seated"), BANK, build.select)
        self.assertTrue(r["top"], r["failed"])


class Rules(unittest.TestCase):
    ctx = {"lower": True, "round": lambda x: round(x / 2.5) * 2.5, "next_load": lambda x: x + 2.5,
           "fmt": lambda x: "%s kg" % x}

    def test_linear(self):
        slot = {"sets": 5, "reps": "5", "inc": 5}
        st = {"load": 60}
        progress.linear_update(slot, st, {"load": 60, "reps": [5] * 5}, self.ctx)
        self.assertEqual(st["load"], 65)
        for _ in range(3):
            progress.linear_update(slot, st, {"load": 65, "reps": [5, 5, 3, 2, 2]}, self.ctx)
        self.assertEqual(st["load"], 57.5)          # 65 x 0.9 rounded to 2.5

    def test_double(self):
        slot = {"sets": 3, "reps": "8-12"}
        st = {"load": 20, "target": 8}
        progress.double_update(slot, st, {"load": 20, "reps": [12, 12, 12]}, self.ctx)
        self.assertEqual((st["load"], st["target"]), (22.5, 8))

    def test_tm_wave(self):
        slot = {"sets": 3, "reps": "5", "deload_wave": True, "inc": 5}
        st = {"tm": 100, "wave": 1}
        for w, last in ((1, 8), (2, 5), (3, 3), (4, 5)):
            progress.tm_update(slot, st, {"reps": [5, 5, last]}, self.ctx)
        self.assertEqual((st["tm"], st["wave"]), (105, 1))

    def test_tm_miss(self):
        slot = {"sets": 3, "reps": "5", "deload_wave": True, "inc": 5}
        st = {"tm": 100, "wave": 1}
        for last in (2, 3, 1, 5):
            progress.tm_update(slot, st, {"reps": [5, 5, last]}, self.ctx)
        self.assertEqual(st["tm"], 90)

    def test_c25k_repeat_and_advance(self):
        slot = {"table": [["a"] * 3, ["b"] * 3]}
        st = {}
        for ok in (True, False, True):
            progress.c25k_update(slot, st, {"completed": ok}, self.ctx)
        self.assertEqual(st["week"], 1)
        for _ in range(3):
            progress.c25k_update(slot, st, {"completed": True}, self.ctx)
        self.assertEqual(st["week"], 2)

    def test_epley(self):
        self.assertAlmostEqual(progress.epley(100, 5), 116.67, places=1)


class Readiness(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(build.readiness({"energy": 9})[0], "planned")
        self.assertEqual(build.readiness({"energy": 5})[0], "light")
        self.assertEqual(build.readiness({"energy": 3})[0], "rest")
        self.assertEqual(build.readiness({"energy": 9, "ill": True})[0], "rest")

    def test_pain_refers(self):
        self.assertEqual(build.readiness({"energy": 8, "pain": [{"region": "knee", "score": 6}]})[2], ["knee"])


class Filters(unittest.TestCase):
    def test_pregnancy_no_supine(self):
        p = prof(screen={"flags": ["pregnant"]})
        self.assertFalse(build.allowed(BANK["bench_press"], p, core.place_tags(p), set(), 5))

    def test_seated(self):
        p = prof(position="seated")
        self.assertFalse(build.allowed(BANK["back_squat"], p, core.place_tags(p), set(), 5))

    def test_coaching_gate(self):
        p = prof(experience="advanced")
        self.assertFalse(build.allowed(BANK["snatch"], p, core.place_tags(p), set(), 5))

    def test_pain_region(self):
        p = prof()
        self.assertFalse(build.allowed(BANK["back_squat"], p, core.place_tags(p), {"knee"}, 5))


class Clock(unittest.TestCase):
    def test_straight(self):
        b = {"format": "straight", "items": [{"sets": 3, "reps": "10", "rest": 60}]}
        self.assertEqual(sheet.block_seconds(b), 3 * (40 + 60) - 60)

    def test_refuses_over(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        s = {"minutes": 10, "blocks": [{"format": "straight", "items": [{"sets": 10, "reps": "10", "rest": 180}]}]}
        f = tmp / "s.json"
        f.write_text(json.dumps(s))
        self.assertTrue(sheet.render_file(f).get("refused"))
        shutil.rmtree(tmp)


class Memory(unittest.TestCase):
    def test_full_loop_and_rebuild(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            shutil.copytree(REPO, tmp / "r", ignore=shutil.ignore_patterns(".git", "sessions", "me"))
            cwd = tmp / "r"
            (cwd / "me").mkdir()
            (cwd / "sessions").mkdir()

            def run(*a):
                r = subprocess.run([sys.executable, "engine/plan.py"] + list(a), cwd=cwd, capture_output=True, text=True)
                return json.loads(r.stdout)
            (cwd / "me" / "a.json").write_text(json.dumps({"items": [], "age_band": "18_39"}))
            run("screen", "me/a.json")
            (cwd / "me" / "a.json").write_text(json.dumps({"goal": "strength", "experience": "none", "days": 3, "minutes": 60,
                                                         "places": {"main": {"equipment": ["full_gym"]}}}))
            self.assertTrue(run("profile", "me/a.json")["ok"])
            self.assertTrue(run("choose", "strength-lp-3")["ok"])
            loads = []
            for i, rep in enumerate(({"squat": {"load": 40}, "bench": {"load": 30}, "row": {"load": 30}},
                                     {"press": {"load": 20}, "deadlift": {"load": 50}}, {})):
                (cwd / "me" / "t.json").write_text(json.dumps({"energy": 8, "minutes": 60, "date": "2026-12-0%d" % (i * 2 + 1)}))
                b = run("build", "me/t.json")
                self.assertTrue(b["ok"], b)
                (cwd / "me" / "r.json").write_text(json.dumps({"as_written": True, "results": rep}))
                lg = run("log", "me/r.json")
                self.assertTrue(lg["ok"], lg)
                loads.append(json.loads((cwd / "me" / "state.json").read_text())["slots"]["squat"]["load"])
            self.assertEqual(loads, [40, 45, 50])      # found, then +5 each clean session
            before = json.loads((cwd / "me" / "state.json").read_text())
            (cwd / "me" / "state.json").write_text("{}")
            self.assertTrue(run("rebuild")["ok"])
            after = json.loads((cwd / "me" / "state.json").read_text())
            self.assertEqual(after["slots"]["squat"]["load"], before["slots"]["squat"]["load"])
            self.assertEqual(after["queue"], before["queue"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class PersonaRegressions(unittest.TestCase):
    """Found by the persona runs of 13 nov 2026. Each one stays fixed."""

    def test_shoulder_limit_blocks_presses_rows_and_rower(self):
        p = prof()
        for i in ("db_floor_press", "barbell_row", "row_erg", "overhead_press"):
            self.assertFalse(build.allowed(BANK[i], p, core.place_tags(p), {"shoulder"}, 5), i)

    def test_postpartum_no_impact_until_ok(self):
        p = prof(screen={"flags": ["postpartum"]})
        self.assertFalse(build.allowed(BANK["box_jump"], p, core.place_tags(p), set(), 5))
        p["impact_ok"] = True
        self.assertTrue(build.allowed(BANK["box_jump"], p, core.place_tags(p), set(), 5))

    def test_care_region_keeps_legs(self):
        p = prof(_care={"knee"})
        self.assertTrue(build.allowed(BANK["goblet_squat"], p, core.place_tags(p), set(), 5))
        self.assertFalse(build.allowed(BANK["box_jump"], p, core.place_tags(p), set(), 5))

    def test_benchmark_scores(self):
        self.assertEqual(progress._better("5 rounds + 12", "6 rounds + 1", "amrap"), "6 rounds + 1")
        self.assertEqual(progress._better("1:02:10", "24:30", "fortime"), "24:30")

    def test_rpe_as_written_never_drops(self):
        st = {"e1rm": 115.9}
        progress.rpe_update({"top_reps": 3, "rpe": 8}, st, {"load": 92.5, "reps": [3], "completed": True}, {})
        self.assertGreaterEqual(st["e1rm"], 115.9)

    def test_beginner_without_pullup_gets_no_strict_pullup(self):
        p = prof(places={"main": {"equipment": ["park"]}})
        self.assertFalse(build.allowed(BANK["pull_up"], p, core.place_tags(p), set(), 5))
        p["skills"] = ["pullup"]
        self.assertTrue(build.allowed(BANK["pull_up"], p, core.place_tags(p), set(), 5))

    def test_home_dumbbells_has_no_bench(self):
        self.assertNotIn("bench", core.PRESETS["home_dumbbells"])

    def test_screen_stop_needs_clearance(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            shutil.copytree(REPO, tmp / "r", ignore=shutil.ignore_patterns(".git", "sessions", "me"))
            cwd = tmp / "r"
            (cwd / "me").mkdir()

            def run(*a):
                r = subprocess.run([sys.executable, "engine/plan.py"] + list(a), cwd=cwd, capture_output=True, text=True)
                return json.loads(r.stdout)
            (cwd / "me" / "a.json").write_text(json.dumps({"items": [2], "age_band": "40_59"}))
            self.assertEqual(run("screen", "me/a.json")["result"], "stop")
            (cwd / "me" / "a.json").write_text(json.dumps({"items": [], "age_band": "40_59"}))
            self.assertEqual(run("screen", "me/a.json")["result"], "stop")
            (cwd / "me" / "a.json").write_text(json.dumps({"items": [2], "age_band": "40_59", "cleared": True}))
            self.assertEqual(run("screen", "me/a.json")["result"], "clear")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class FinalAuditRegressions(unittest.TestCase):
    """Found by the final independent audit of 13 nov 2026."""

    def test_short_minutes_still_rotate_every_session(self):
        p = prof(minutes=40)
        pl = {"program": "strength-lp-3", "days": 3, "modules": []}
        st = {"block": 1, "week": 1, "week_sessions": 0, "queue": ["A", "B"], "slots": {}}
        a = build.build({"energy": 8, "minutes": 40}, p, pl, st, BANK, "2026-12-01")
        st["queue"] = ["B"]
        b = build.build({"energy": 8, "minutes": 40}, p, pl, st, BANK, "2026-12-03")
        names = lambda s: {it["ex"] for bl in s["blocks"] if bl["kind"] == "main" for it in bl["items"]}
        self.assertNotEqual(names(a), names(b))
        self.assertIn("overhead_press", names(b))

    def test_limits_count_in_the_fit_filter(self):
        p = prof(limits=[{"region": "knee", "exclude": True}, {"region": "low_back", "exclude": True}])
        self.assertNotIn("strength-lp-3", match.match(p, BANK, build.select)["passed"])

    def test_disliked_machines_avoided_when_possible(self):
        p = prof(dislikes=["machines"])
        pick = build.select({"pattern": "v_pull", "prefer": ["lat_pulldown", "chin_up"], "key": "v"}, p, core.place_tags(p), set(), BANK)
        self.assertNotIn(BANK[pick]["load_type"], ("machine", "cable"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
