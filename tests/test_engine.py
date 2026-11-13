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

    def test_first_timer_health_in_a_gym(self):
        t = top(prof(goal="health", minutes=45, places={"main": {"type": "gym", "equipment": ["basic_gym"]}}))
        self.assertEqual(t[0], "health-baseline-2to3")

    def test_home_gym_all_round(self):
        t = top(prof(goal="functional", experience="novice", minutes=45,
                     places={"main": {"type": "home_gym", "equipment": ["dumbbell", "bench", "rower"]}}, dumbbells=[4, 8, 12]))
        self.assertEqual(t[0], "functional-gpp-3to5")

    def test_outdoors_running(self):
        t = top(prof(goal="run", minutes=30, places={"main": {"type": "outdoors", "equipment": ["outdoors"]}}))
        self.assertEqual(t[0], "run-c25k-3")

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
            (cwd / "me" / "a.json").write_text(json.dumps({"items": [], "language": "en"}))      # no age: it is never asked
            self.assertEqual(run("screen", "me/a.json")["result"], "clear")
            (cwd / "me" / "a.json").write_text(json.dumps({"goal": "strength", "experience": "none", "days": 3, "minutes": 60,
                                                         "places": {"main": {"equipment": ["full_gym"]}}}))
            self.assertTrue(run("profile", "me/a.json")["ok"])
            self.assertIn('"age_band": "18_39"', (cwd / "me" / "PROFILE.md").read_text())
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
        p = prof()
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


class WebBuildRegressions(unittest.TestCase):
    """Found while building the web version, 13 nov 2026."""

    def home_strength(self, **kw):
        return prof(goal="strength", minutes=45, places={"main": {"type": "home", "equipment": ["home_dumbbells"]}},
                    dumbbells=[4, 8, 12], **kw)

    def test_goal_fit_beats_the_health_default_on_a_tie(self):
        p = self.home_strength(experience="novice")
        p["places"] = {"main": {"type": "home_gym", "equipment": ["home_dumbbells", "rower"]}}     # a home gym with a cardio machine
        r = match.match(p, BANK, build.select)
        self.assertEqual(r["top"][0]["id"], "functional-gpp-3to5")          # strength fit 2 ties Health baseline on points
        self.assertGreaterEqual(r["top"][0]["goal_fit"], 2)

    def test_no_strength_fit_says_why(self):
        r = match.match(self.home_strength(), BANK, build.select)
        self.assertLess(r["top"][0]["goal_fit"], 2)                          # honestly nothing built for strength fits
        self.assertIn("fallback", r)
        self.assertIn("barbell", r["goal_gap"])
        self.assertEqual(r["fallback"]["always_available"], ["health-baseline-2to3"])
        self.assertTrue(all("Only partly" in t["why"] or "Not built" in t["why"] for t in r["top"]))
        self.assertFalse(any(h["only_blocker"].startswith("age") for h in r["fallback"]["one_change_away"]))

    def test_every_offer_has_a_reason(self):
        for p in (prof(likes=["barbell"]), self.home_strength(), prof(goal="health", minutes=45)):
            for t in match.match(p, BANK, build.select)["top"]:
                self.assertTrue(t["why"] and "evidence" in t["why"], t)
        self.assertIn("heavy lifting you enjoy", top_why(prof(likes=["barbell"])))

    def test_pound_score_line(self):
        import logbook
        sess = {"blocks": [{"kind": "main", "items": [{"name": "Goblet squat", "_slot": {"key": "squat", "score": True}}]}]}
        done = [{"key": "squat", "rule": "double_progression", "result": {"load": logbook.to_kg(25, "lb"), "reps": [8, 8]}}]
        self.assertEqual(logbook.score_text(sess, done, "lb"), "25 lb x 8/8")
        self.assertEqual(core.fmt_load(logbook.to_kg(12, "lb"), "lb"), "12 lb")
        self.assertEqual(core.fmt_load(logbook.to_kg(27.5, "lb"), "lb"), "27.5 lb")
        self.assertEqual(core.fmt_load(60, "kg"), "60 kg")

    def test_pound_grid_and_owned_weights(self):
        import plan
        p = plan.normalise({"units": "lb", "dumbbells": [10, 15, 25]}, prof())
        self.assertEqual(p["dumbbells_lb"], [10, 15, 25])
        self.assertAlmostEqual(p["dumbbells"][-1], 11.34, places=2)
        db = build.load_ctx(BANK["goblet_squat"], p)
        self.assertEqual(db["fmt"](db["round"](12)), "25 lb")                # the 25 lb pair they own, not 25 kg
        bb = build.load_ctx(BANK["back_squat"], dict(p, dumbbells=None))
        self.assertEqual(bb["fmt"](bb["round"](10)), "45 lb")                 # never under the 45 lb bar
        self.assertEqual(bb["fmt"](bb["round"](bb["next_load"](bb["round"](40)))), "90 lb")

    def test_rebuild_does_not_convert_pounds_twice(self):
        import logbook
        p = dict(prof(units="lb"), dumbbells=None)
        it = {"name": "Goblet squat", "_slot": {"key": "squat", "ex": "goblet_squat", "rule": "double_progression", "state_key": "squat",
              "slot": {"sets": 2, "reps": "8-15"}, "prescribed": {"sets": 2, "reps": "8-15", "load": None}, "kind": "main",
              "load_type": "dumbbell", "muscles": [], "muscles2": []}}
        sess = {"blocks": [{"kind": "main", "items": [it]}]}
        st1, st2 = {}, {}
        logbook.apply(sess, {"as_written": True, "results": {"squat": {"load": 25, "reps": [8, 8]}}}, p, st1, BANK)
        logbook.apply(sess, {"as_written": False, "loads_in_kg": True, "results": {"squat": {"load": st1["slots"]["squat"]["load"], "reps": [8, 8]}}},
                      p, st2, BANK)
        self.assertEqual(st1["slots"]["squat"]["load"], st2["slots"]["squat"]["load"])


class RegionLimits(unittest.TestCase):
    """Safety, 13 nov 2026: an excluded region never reaches a sheet, in any program, warm-up and finishers included.
    The bug behind it: band_shoulder_dislocate had no regions, so a person who excluded the shoulder got it twice a session."""

    PROGRAMS = ["strength-lp-3", "strength-531-bbb-4", "strength-rpe-4", "muscle-upperlower-4", "muscle-ppl-6",
                "powerbuild-phul-4", "weightlifting-novice-3", "functional-gpp-3to5", "hyrox-prep-4",
                "hybrid-strength-endurance-4to6", "run-base-3to5", "health-baseline-2to3"]
    KIT = ["full_gym", "crossfit_box", "sled", "skierg", "sandbag", "rings"]
    NAMES = {r["name"]: i for i, r in BANK.items()}
    # The region audit of 13 nov 2026, written here as well as in bank.csv, so a row that loses its tag fails this test
    # instead of passing it (a test that only read the bank could never see a missing region).
    AUDIT = {"band_shoulder_dislocate": "shoulder", "thoracic_rotation": "shoulder", "couch_stretch": "knee;hip",
             "worlds_greatest_stretch": "knee;hip", "hip_90_90": "knee;hip", "ankle_rocks": "knee;ankle",
             "cat_cow": "low_back;wrist", "seated_thoracic_rotation": "low_back", "hip_hinge_drill": "hip;low_back",
             "hollow_hold": "low_back", "bird_dog": "low_back;wrist", "seated_band_rotation": "low_back",
             "cable_crunch": "low_back", "reverse_crunch": "low_back", "sit_up": "hip;low_back", "seated_band_crunch": "low_back",
             "bike_erg": "knee", "row_erg": "knee;low_back;shoulder", "jump_rope": "knee;ankle", "tandem_stance": "ankle",
             "heel_to_toe_walk": "ankle", "step_over": "hip", "back_squat": "shoulder", "front_squat": "shoulder",
             "good_morning": "shoulder", "back_extension": "hip", "band_good_morning": "low_back", "cable_pull_through": "low_back",
             "single_leg_rdl": "low_back", "step_up": "hip", "farmer_carry": "low_back", "long_lever_plank": "low_back",
             "body_saw": "low_back", "sled_pull": "low_back", "burpee": "ankle", "burpee_broad_jump": "ankle;hip",
             "thruster": "hip;wrist", "db_thruster": "hip", "kb_clean_and_press": "hip;low_back", "devil_press": "hip"}

    def loads(self, i):
        return set(BANK[i]["regions"]) | set(self.AUDIT.get(i, "").split(";")) - {""}

    def served(self, region, pid, pain_today=False):
        """Every bank id a few sessions of this program would put on a sheet, for someone with that region left out."""
        prog = core.load_program(pid)
        exp = "intermediate" if "intermediate" in prog["experience"] else prog["experience"][0]
        limits = [] if pain_today else [{"region": region, "note": "hurts now", "exclude": True}]
        p = prof(goal=max(prog["goals"], key=prog["goals"].get), experience=exp, days=prog["days"][0],
                 minutes=max(60, prog["minutes"][0]), places={"main": {"type": "gym", "equipment": self.KIT}},
                 skills=["olympic_coached", "run_30min", "pullup"], limits=limits)
        days = str(prog["days"][0])
        queue = prog["layouts"][days]
        plan = {"program": pid, "days": prog["days"][0], "modules": prog.get("modules", []) + ["mobility", "core", "conditioning"]}
        seen, picked = set(), []
        real = build.select

        def spy(*a, **k):
            i = real(*a, **k)
            if i:
                picked.append(i)
            return i
        build.select = spy
        try:
            for n, sid in enumerate(queue):
                st = {"block": 1, "week": 1, "week_sessions": 0, "queue": queue[n:] + queue[:n], "slots": {}}
                today = {"energy": 8, "minutes": p["minutes"]}
                if pain_today:
                    today["pain"] = [{"region": region, "score": 6}]
                s = build.build(today, p, plan, st, BANK, "2026-12-%02d" % (n + 1))
                for b in s["blocks"]:
                    for it in b["items"]:
                        if it.get("ex") in BANK:
                            seen.add(it["ex"])
                        elif it.get("name") in self.NAMES:
                            seen.add(self.NAMES[it["name"]])       # the warm-up raise is written by name
        finally:
            build.select = real
        return seen | set(picked)

    def test_no_excluded_region_is_served(self):
        for region in core.REGIONS:
            for pid in self.PROGRAMS:
                bad = sorted(i for i in self.served(region, pid) if region in self.loads(i))
                self.assertEqual(bad, [], "%s excluded, %s served %s" % (region, pid, bad))

    def test_sharp_pain_today_is_left_out_too(self):
        for region in ("shoulder", "knee", "low_back"):
            for pid in ("strength-lp-3", "functional-gpp-3to5", "hyrox-prep-4", "health-baseline-2to3"):
                bad = sorted(i for i in self.served(region, pid, pain_today=True) if region in self.loads(i))
                self.assertEqual(bad, [], "%s sharp today, %s served %s" % (region, pid, bad))

    def test_the_audit_is_in_the_bank(self):
        for i, regs in self.AUDIT.items():
            self.assertTrue(set(regs.split(";")) <= set(BANK[i]["regions"]), i)

    def test_no_row_is_silently_region_free(self):
        for r in BANK.values():
            self.assertTrue(r["regions"] or "region_free" in r["tags"], r["id"])
            self.assertTrue(set(r["regions"]) <= set(core.REGIONS), r["id"])


class Scope(unittest.TestCase):
    """The product scope of 13 nov 2026 (doctrine/00_MISSION.md): gym, home gym with real kit, outdoors for cardio; 18 to 40."""

    OUT = ["calisthenics-rr-3", "home-fullbody-2to4", "kettlebell-rop-3", "kettlebell-ss-5", "older-strong-3"]

    def test_out_of_scope_programs_are_never_loaded(self):
        ids = {p["id"] for p in core.all_programs()}
        for pid in self.OUT:
            self.assertNotIn(pid, ids)
            self.assertTrue((core.PROGRAMS / "_out_of_scope" / (pid + ".md")).exists(), pid)
            with self.assertRaises(SystemExit):
                core.load_program(pid)
        for p in core.all_programs():
            self.assertFalse(set(p.get("graduates_to", [])) & set(self.OUT), p["id"])

    def test_places_in_and_out_of_scope(self):
        import checks
        ok = lambda eq: not [e for e in checks.check_profile(prof(places={"main": {"equipment": eq}})) if "out of scope" in e]
        for eq in (["full_gym"], ["basic_gym"], ["crossfit_box"], ["home_dumbbells"], ["barbell", "rack", "plates", "bench"],
                   ["dumbbell"], ["rower"], ["outdoors"]):
            self.assertTrue(ok(eq), eq)
        for eq in (["park"], ["home_bodyweight"], ["kettlebell"], ["kettlebell", "band"], ["pullup_bar", "rings"], []):
            self.assertFalse(ok(eq), eq)

    def test_age_is_fixed_whatever_is_sent(self):
        import plan
        self.assertEqual(plan.normalise({"age_band": "60_74"}, {})["age_band"], "18_39")
        self.assertEqual(plan.normalise({}, {"age_band": "75_plus"})["age_band"], "18_39")

    def test_functional_is_a_gym_plan(self):
        p = core.load_program("functional-gpp-3to5")
        for eq in (["kettlebell"], ["home_bodyweight"], ["park"], ["home_dumbbells"]):
            why = match.filters(p, prof(goal="functional", experience="novice", places={"main": {"equipment": eq}}), BANK, build.select)
            self.assertTrue(why, eq)
        self.assertFalse(match.filters(p, prof(goal="functional", experience="novice"), BANK, build.select))


class Interview(unittest.TestCase):
    """The interview of 13 nov 2026 (doctrine/02_INTERVIEW.md): the fork, outcome first, experience by activity,
    an optional style for experienced people only, one plan with 'not for me', typed minutes, units confirmed."""

    BASE = {"language": "en", "units": "kg", "age_band": "18_39", "days": 3, "minutes": 60,
            "places": {"main": {"type": "gym", "equipment": ["full_gym"]}}, "screen": {"result": "clear", "flags": []}}

    def run_ans(self, ans, old=None):
        import plan, checks
        p = plan.normalise(ans, dict(old or self.BASE))
        errs = checks.check_profile(p)                                     # plan.py profile stops on errors, before any match
        return p, errs, (None if errs else match.match(p, BANK, build.select))

    def test_fork_new_path(self):
        p, errs, r = self.run_ans({"mode": "new", "outcome": "strong", "outcome_detail": "general",
                                   "done_before": ["lifting"], "experience_by": {"lifting": "novice"}})
        self.assertEqual(errs, [])
        self.assertEqual((p["goal"], p["experience"]), ("strength", "novice"))
        self.assertEqual(r["plan"]["id"], r["top"][0]["id"])
        self.assertNotIn("improve_note", r)

    def test_fork_improve_path_keeps_the_split_and_days(self):
        for split, days, want in (("ppl", 6, "muscle-ppl-6"), ("upper_lower", 4, "muscle-upperlower-4"), ("full_body", 3, "muscle-fullbody-3")):
            p, errs, r = self.run_ans({"mode": "improve", "outcome": "look", "outcome_detail": "size",
                                       "current_routine": {"split": split, "days": days, "age": "over_1y", "stalls": ["not_growing"],
                                                           "keep": ["split"], "exercises": {"Day 1": ["bench_press", "Incline dumbbell press", "my cable thing"]}}})
            self.assertEqual(errs, [], split)
            self.assertEqual(p["days"], days)
            self.assertEqual(p["experience"], "intermediate")              # a year on their routine
            self.assertEqual(r["plan"]["id"], want, split)
            self.assertIn("improve_note", r)
            self.assertIn("same shape as your week", r["plan"]["why"])
            ex = p["current_routine"]["exercises"]["Day 1"]
            self.assertEqual(ex, [{"id": "bench_press"}, {"id": "incline_db_press"}, {"own": "my cable thing"}])
        p, errs, r = self.run_ans({"mode": "improve", "outcome": "look"})
        self.assertTrue(any("current_routine" in e for e in errs))

    def test_every_outcome_maps_to_a_goal_and_a_plan(self):
        want = {("look", "size"): ("muscle", "muscle"), ("look", "lean"): ("fat_loss", "muscle"),
                ("strong", "general"): ("strength", "strength"), ("strong", "powerlifting"): ("powerlifting", "strength"),
                ("strong", "olympic"): ("weightlifting", "weightlifting"), ("athletic", "crossfit"): ("functional", "functional"),
                ("athletic", "hybrid"): ("functional", "hybrid"), ("event", "run_5k_10k"): ("run", "run"),
                ("event", "run_half"): ("run", "run"), ("event", "run_marathon"): ("run", "run"),
                ("event", "hyrox"): ("hyrox", "hyrox"), ("event", "meet"): ("powerlifting", "strength"),
                ("keep_going", "lifting"): ("muscle", None), ("keep_going", "fitness"): ("functional", None),
                ("keep_going", "mix"): ("health", None)}
        self.assertEqual(set(want), {(o, d) for o, ds in core.OUTCOMES.items() for d in ds})
        for (oc, det), (goal, fam) in want.items():
            p, errs, r = self.run_ans({"outcome": oc, "outcome_detail": det, "days": 4, "skills": ["run_30min", "olympic_coached"],
                                       "experience_by": {"lifting": "intermediate", "running": "intermediate", "crossfit": "intermediate"}})
            self.assertEqual(errs, [], (oc, det))
            self.assertEqual(p["goal"], goal, (oc, det))
            if fam:
                self.assertEqual(r["plan"]["family"], fam, (oc, det))
            gap = det == "run_marathon" or oc == "keep_going"
            self.assertEqual("outcome_note" in r, gap, (oc, det))           # unserved outcomes say so, honestly
        p, _, _ = self.run_ans({"outcome": "look"})
        self.assertEqual((p["outcome_detail"], p["goal"]), ("size", "muscle"))   # a skipped follow-up takes the default
        ed = dict(self.BASE, screen={"result": "clear", "flags": ["no_fat_loss_goal"]})
        p, errs, _ = self.run_ans({"outcome": "look", "outcome_detail": "lean"}, ed)
        self.assertEqual((p["goal"], errs), ("muscle", []))

    def test_experience_by_activity_and_coming_back(self):
        p, _, r = self.run_ans({"outcome": "event", "outcome_detail": "run_5k_10k", "skills": ["run_30min"],
                                "experience_by": {"running": "advanced"}, "places": {"main": {"type": "outdoors", "equipment": ["outdoors"]}}})
        self.assertEqual(p["experience"], "none")                         # a runner who never lifted lifts as a beginner
        self.assertEqual(r["plan"]["id"], "run-base-3to5")                # but runs as the runner she is
        p, _, _ = self.run_ans({"outcome": "strong", "experience_by": {"lifting": "intermediate"}, "returning": True})
        self.assertEqual((p["experience"], p["experience_was"]["lifting"]), ("novice", "intermediate"))

    def test_enjoy_and_avoid_move_the_plan(self):
        ans = {"outcome": "look", "outcome_detail": "size", "experience_by": {"lifting": "intermediate"}, "days": 4}
        _, _, r = self.run_ans(dict(ans, enjoys=["heavy"]))
        self.assertEqual(r["plan"]["family"], "powerbuild")
        _, _, r = self.run_ans(dict(ans, enjoys=["pump"], avoids=["heavy"]))
        self.assertEqual(r["plan"]["family"], "muscle")

    def test_style_only_for_the_experienced(self):
        ans = {"outcome": "look", "outcome_detail": "size", "days": 4, "style_pref": "powerbuilding"}
        _, errs, r = self.run_ans(dict(ans, experience_by={"lifting": "intermediate"}))
        self.assertEqual((errs, r["plan"]["family"]), ([], "powerbuild"))
        _, _, r = self.run_ans(dict(ans, experience_by={"lifting": "novice"}))
        self.assertEqual(r["plan"]["family"], "muscle")                   # a beginner's style is never read
        _, _, r = self.run_ans(dict(ans, experience_by={"lifting": "intermediate"}, style_pref="trainer"))
        self.assertEqual(r["plan"]["family"], "muscle")                   # let the trainer decide
        _, _, r = self.run_ans(dict(ans, experience_by={"lifting": "intermediate"}, style_pref="running"))
        self.assertIn("style_note", r)                                    # a style that does not serve the outcome: said why

    def test_one_plan_in_plain_words_and_not_for_me(self):
        ans = {"outcome": "look", "outcome_detail": "size", "experience_by": {"lifting": "intermediate"}, "days": 4}
        p, _, r = self.run_ans(ans)
        first = r["plan"]
        for name in ("5/3/1", "PHUL", "PHAT", "GZCLP", "RPE", "Texas"):
            self.assertNotIn(name, first["plain"]["headline"] + first["plain"]["week"])
        self.assertIn("4 days a week", first["plain"]["week"])
        q, errs, r2 = self.run_ans({"rejected": [{"program": first["id"], "reason": "not_enjoy"}]}, p)
        self.assertEqual(errs, [])
        self.assertNotEqual(r2["plan"]["id"], first["id"])
        self.assertNotEqual(r2["plan"]["family"], first["family"])
        self.assertTrue(r2["failed"][first["id"]][0].startswith("not for me"))
        _, _, r3 = self.run_ans({"rejected": [{"program": first["id"], "reason": "too_long"}]}, p)
        self.assertLess(core.load_program(r3["plan"]["id"])["minutes"][0], core.load_program(first["id"])["minutes"][0])
        _, errs, _ = self.run_ans({"rejected": [{"program": first["id"], "reason": "meh"}]}, p)
        self.assertTrue(errs)

    def test_a_blend_is_stored_and_reaches_the_why_line(self):
        p, errs, r = self.run_ans({"outcomes": [{"id": "look", "detail": "size", "share": 0.6},
                                                {"id": "event", "detail": "run_5k_10k", "share": 0.4}],
                                   "experience_by": {"lifting": "intermediate", "running": "novice"}, "days": 4})
        self.assertEqual(errs, [])
        self.assertEqual([(o["id"], o["share"]) for o in p["outcomes"]], [("look", 0.6), ("event", 0.4)])
        self.assertEqual((p["goal"], p["goal2"]), ("muscle", "run"))       # current code keeps working on goal and goal2
        self.assertIn("your blend: building muscle 60% leads the plan, running 40% comes as an add-on", r["plan"]["why"])
        p, errs, r = self.run_ans({"outcomes": [{"id": "look", "share": 1}, {"id": "event", "share": 2}],
                                   "experience_by": {"lifting": "intermediate", "running": "intermediate"}, "skills": ["run_30min"]})
        self.assertEqual((p["outcome"], p["goal"], p["goal2"], errs), ("event", "run", "muscle", []))   # more running than gym
        self.assertEqual(r["plan"]["family"], "run")
        _, errs, _ = self.run_ans({"outcomes": [{"id": "look", "share": 0.5}] * 2})
        self.assertTrue(errs)
        _, errs, _ = self.run_ans({"outcomes": [{"id": o, "share": 0.25} for o in ("look", "strong", "athletic", "event")]})
        self.assertTrue(errs)

    def test_typed_minutes_15_to_120(self):
        for m in (15, "15", 37, 120, "120"):
            p, errs, _ = self.run_ans({"outcome": "strong", "minutes": m})
            self.assertEqual(errs, [], m)
            self.assertEqual(p["minutes"], int(m))
        for m in (14, 121, 0, 180, "ten"):
            _, errs, _ = self.run_ans({"outcome": "strong", "minutes": m})
            self.assertTrue([e for e in errs if "minutes" in e], m)

    def test_units_confirmed_at_the_first_weight(self):
        p, errs, _ = self.run_ans({"outcome": "strong", "units": "lb", "paper": "Letter", "units_confirmed": True,
                                   "numbers": {"back_squat": {"lb": 225, "reps": 5}}})
        self.assertEqual(errs, [])
        self.assertTrue(p["units_confirmed"])
        self.assertAlmostEqual(p["numbers"]["back_squat"]["kg"], 102.1, places=1)
        p, errs, _ = self.run_ans({"outcome": "strong", "units": "kg", "units_confirmed": True,
                                   "numbers": {"back_squat": {"kg": 100, "reps": 5}}})
        self.assertEqual((p["units"], p["numbers"]["back_squat"]["kg"], errs), ("kg", 100, []))
        _, errs, _ = self.run_ans({"outcome": "strong", "units_confirmed": "yes"})
        self.assertTrue(errs)

    def test_pain_by_status_and_trigger_sleep_and_stress(self):
        p, errs, r = self.run_ans({"outcome": "strong", "sleep": "under_6", "stress": "high", "limits": [
            {"region": "shoulder", "status": "mild", "triggers": ["overhead"]},
            {"region": "knee", "status": "now", "triggers": ["impact"]},
            {"region": "low_back", "status": "cleared"}]})
        self.assertEqual(errs, [])
        self.assertEqual([l["exclude"] for l in p["limits"]], [False, True, False])   # mild is care, not a ban
        self.assertTrue(p["no_impact"])
        self.assertEqual(p["start_volume"], "low")
        self.assertIn("dose_note", r)


def top_why(p):
    return match.match(p, BANK, build.select)["top"][0]["why"]


if __name__ == "__main__":
    unittest.main(verbosity=1)
