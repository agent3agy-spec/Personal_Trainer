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
        # Phase D: a limit that empties one main slot costs score, one that empties more than half a session's rules it out.
        free = {t["id"]: t["score"] for t in match.match(prof(), BANK, build.select)["top"]}
        p = prof(limits=[{"region": "knee", "exclude": True}, {"region": "low_back", "exclude": True}])
        r = match.match(p, BANK, build.select)
        lp = next(t for t in r["top"] if t["id"] == "strength-lp-3")
        self.assertLess(lp["score"], free["strength-lp-3"])
        p = prof(limits=[{"region": r_, "exclude": True} for r_ in ("knee", "low_back", "shoulder")])
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
            served = det == "run_marathon" or oc == "keep_going"
            self.assertNotIn("outcome_note", r, (oc, det))                 # phase D: every outcome has a real plan now
            self.assertEqual("plan_note" in r, served, (oc, det))           # the two new ones say how they are served
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

    def test_answers_changed_later_from_the_settings(self):
        # coming back after a break steps down once: a later change (days, a 'not for me') never steps it down again
        p, _, _ = self.run_ans({"outcome": "strong", "experience_by": {"lifting": "advanced"}, "returning": True})
        q, errs, _ = self.run_ans({"days": 4}, p)
        self.assertEqual((errs, q["experience_by"]["lifting"], q["experience_was"]["lifting"]), ([], "intermediate", "advanced"))
        q, _, _ = self.run_ans({"experience_by": {"lifting": "advanced"}, "returning": None}, q)
        self.assertEqual((q["experience_by"]["lifting"], "returning" in q, "experience_was" in q), ("advanced", False, False))
        # an answer taken back (null) leaves the profile, and the goal follows a blend that went
        p, _, _ = self.run_ans({"outcomes": [{"id": "look", "detail": "size", "share": 0.6}, {"id": "event", "detail": "run_5k_10k", "share": 0.4}]})
        q, errs, _ = self.run_ans({"outcome": "look", "outcome_detail": "size", "outcomes": None, "event": None}, p)
        self.assertEqual((errs, "outcomes" in q, q["goal"], q.get("goal2")), ([], False, "muscle", None))
        # free weights writes machines into dislikes; changing the answer takes it out again
        p, _, _ = self.run_ans({"kit_pref": "free_weights"})
        self.assertIn("machines", p["dislikes"])
        q, _, _ = self.run_ans({"kit_pref": "either"}, p)
        self.assertNotIn("machines", q["dislikes"])
        # no_impact follows the limits when they are given again
        p, _, _ = self.run_ans({"limits": [{"region": "knee", "status": "mild", "triggers": ["impact"]}]})
        self.assertTrue(p.get("no_impact"))
        q, _, _ = self.run_ans({"limits": []}, p)
        self.assertFalse(q.get("no_impact"))

    def test_a_move_swapped_for_today(self):
        p = prof()
        self.assertTrue(build.allowed(BANK["back_squat"], p, core.place_tags(p), set(), 5))
        self.assertFalse(build.allowed(BANK["back_squat"], dict(p, _skip={"back_squat"}), core.place_tags(p), set(), 5))

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
        self.assertIn("your blend: building muscle 60%, running 40%, so your week is 2 lifting days and 2 running days", r["plan"]["why"])
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


class Composer(unittest.TestCase):
    """Phase D, 13 nov 2026: the engine trains like a coach (research/07 and research/08, doctrine/06_BUILD.md)."""

    BASE = {"language": "en", "units": "kg", "age_band": "18_39", "days": 3, "minutes": 60, "mode": "new",
            "places": {"main": {"type": "gym", "equipment": ["full_gym"]}}, "screen": {"result": "clear", "flags": []}}

    def profile(self, **ans):
        import plan, checks
        p = plan.normalise(ans, dict(self.BASE))
        self.assertEqual(checks.check_profile(p), [])
        return p

    def plan_for(self, p, pid=None):
        """What plan.py choose writes, without the files: the match, the composed week, the eye's fixes."""
        import compose, eye
        pid = pid or match.match(p, BANK, build.select)["plan"]["id"]
        prog = core.load_program(pid)
        c = compose.compose(p, prog, BANK, build.select)
        pl = dict(program=pid, plain_name=c["plain_name"], days=c["days"], modules=c["modules"], goal_modules=c["goal_modules"],
                  streams=c["streams"], order=c["order"], components=c["components"], blend=c["blend"], targets=c["targets"],
                  lift_days=c["lift_days"], long_run=c["long_run"], challenge=c["challenge"], goal_on_all=c["goal_on_all"])
        st = {"block": 1, "week": 1, "week_sessions": 0, "queue": [], "slots": {}}
        build.refill(st, prog, pl)
        found, week = eye.review(p, pl, st, BANK)
        return pl, c, found, week

    def test_shares_are_respected(self):
        for days, want in ((5, (3, 2)), (4, (2, 2)), (3, (2, 1))):
            p = self.profile(outcomes=[{"id": "look", "detail": "size", "share": 0.6}, {"id": "event", "detail": "run_5k_10k", "share": 0.4}],
                             experience_by={"lifting": "intermediate", "running": "novice"}, skills=["run_30min"], days=days)
            pl, c, _, week = self.plan_for(p)
            per = [s["per_week"] for s in c["streams"]]
            self.assertEqual((per[0], sum(per[1:])), want, days)
            self.assertEqual([s["what"] for s in c["streams"]][:2], ["lift", "run"])
            self.assertEqual(len(week), days)
            runs = [s for s in week if s["session_id"].startswith("mod:run-race")]
            self.assertEqual(len(runs), want[1], days)                     # the running days really come round in the week
        p = self.profile(outcomes=[{"id": "strong", "detail": "general", "share": 0.8}, {"id": "event", "detail": "hyrox", "share": 0.2}],
                         experience_by={"lifting": "intermediate"}, skills=["run_30min"], days=4)
        _, c, _, week = self.plan_for(p)
        self.assertIn("hyrox", [x["what"] for x in c["components"]])      # a small share becomes a protected finisher or a day
        seen = json.dumps([[s.get(k) for k in ("title", "program_name", "why", "notes", "score_to_beat")] +
                           [[b["name"]] + [(i.get("name"), i.get("reps"), i.get("effort")) for i in b["items"]] for b in s["blocks"]] for s in week])
        self.assertFalse([n for n in ("5/3/1", "BBB", "GZCL", "Boring But Big", "T1 ", "training max", "Express") if n in seen])

    def test_marathon_has_a_plan_with_a_protected_long_run(self):
        p = self.profile(outcome="event", outcome_detail="run_marathon", experience_by={"running": "novice"}, days=4, minutes=60,
                         places={"main": {"type": "outdoors", "equipment": ["outdoors"]}}, skills=["run_30min"],
                         numbers={"easy_run_minutes": 40})
        r = match.match(p, BANK, build.select)
        self.assertEqual(r["plan"]["family"], "run")
        self.assertIn("plan_note", r)
        pl, c, found, week = self.plan_for(p)
        self.assertEqual(c["long_run"]["max_minutes"], 180)
        self.assertEqual(c["days"], 4)                                    # no gym outdoors: the strength day goes back to running
        longs = [s for s in week if any("long" in it.get("key", "") for b in s["blocks"] for it in b["items"])]
        self.assertTrue(longs)
        ls = longs[0]
        self.assertNotEqual(ls["mode"], "express")
        run_min = lambda s, k: max(int(str(it["reps"]).split()[0]) for b in s["blocks"] for it in b["items"] if k in it.get("key", ""))
        easy = max(run_min(s, "easy") for s in week if any("easy" in it.get("key", "") for b in s["blocks"] for it in b["items"]))
        self.assertGreaterEqual(run_min(ls, "long"), easy)                # never shorter than the easy run
        self.assertTrue(ls.get("long_run_day"))                           # 60 min long run plus warm-up: more than 60, said
        self.assertGreater(ls["minutes"], 60)
        self.assertIn("Long run day", ls["notes"])
        self.assertTrue(all(f["ok"] for f in found if f["check"] == "key_quality"), found)

    def test_keep_it_going_has_a_plan_with_challenges(self):
        for det in ("lifting", "fitness", "mix"):
            p = self.profile(outcome="keep_going", outcome_detail=det, experience_by={"lifting": "novice", "classes": "novice"}, days=3, minutes=45)
            r = match.match(p, BANK, build.select)
            self.assertIn("plan_note", r)
            pl, c, found, week = self.plan_for(p)
            self.assertTrue(c["challenge"], det)
            self.assertTrue(all("This month's challenge" in s["why"] for s in week), det)

    def test_priority_reaches_its_weekly_sets(self):
        p = self.profile(outcome="look", outcome_detail="size", experience_by={"lifting": "intermediate"}, days=4, minutes=60, priority=["arms"])
        pl, c, found, week = self.plan_for(p)
        pri = [f for f in found if f["check"] == "priority"]
        self.assertTrue(pri and pri[0]["ok"], found)
        self.assertGreaterEqual(pri[0]["added"], 4)
        hit = [s for s in week if any(it.get("_priority") == "arms" for b in s["blocks"] for it in b["items"])]
        self.assertGreaterEqual(len(hit), 2)
        self.assertTrue(any(it.get("_priority") == "arms" for b in week[0]["blocks"] for it in b["items"]))   # in session 1
        # a strength program with no arm slot still gets direct arm work (08 persona 2)
        p = self.profile(outcome="strong", outcome_detail="general", experience_by={"lifting": "advanced"}, days=4, minutes=60, priority=["arms"])
        pl, c, found, week = self.plan_for(p)
        self.assertTrue(any(BANK.get(it.get("ex"), {}).get("pattern") in ("biceps", "triceps") for s in week for b in s["blocks"] for it in b["items"]))

    def test_priority_is_cut_last(self):
        it = lambda n, s, pri=None: {"name": n, "ex": "db_curl", "sets": s, "reps": "10", "rest": 60, "_priority": pri,
                                    "_slot": {"prescribed": {"sets": s}, "slot": {"sets": 2 if pri else s}}}   # the curl: 2 sets + 1 added
        s = {"minutes": 20, "blocks": [
            {"name": "Main", "kind": "main", "format": "straight", "items": [it("Squat", 3)]},
            {"name": "Accessory", "kind": "accessory", "format": "straight", "items": [it("Fly", 3), it("Curl", 3, "arms")]},
            {"name": "Conditioning", "kind": "finisher", "format": "intervals", "minutes": 8, "_goal": True, "items": []},
            {"name": "Mobility", "kind": "finisher", "format": "circuit", "minutes": 6, "items": []}]}
        notes = []
        build.fit(s, 12, notes)
        names = [i["name"] for b in s["blocks"] for i in b["items"]] + [b["name"] for b in s["blocks"]]
        self.assertNotIn("Mobility", names)                                # the nice-to-have goes first
        self.assertNotIn("Fly", names)                                     # then accessories that serve no target
        self.assertIn("Curl", names)                                       # the priority stays, a set lighter
        self.assertIn("Conditioning", names)                               # the goal finisher stays, at its minimum dose
        self.assertEqual(next(b for b in s["blocks"] if b["name"] == "Conditioning")["minutes"], 6)
        self.assertEqual(next(i for b in s["blocks"] for i in b["items"] if i["name"] == "Curl")["sets"], 2)

    def test_never_squeeze_silently(self):
        for prog in core.all_programs():
            for k, lay in prog["layouts"].items():
                self.assertTrue(len(lay) <= int(k) or prog.get("rotates"), (prog["id"], k))
        p = self.profile(outcome="look", outcome_detail="size", experience_by={"lifting": "intermediate"}, days=3)
        r = match.match(p, BANK, build.select)
        self.assertNotIn("muscle-upperlower-4", r["passed"])               # 4 sessions never run on 3 days
        fake = dict(core.load_program("muscle-upperlower-4"), days=[3, 4], layouts={"3": ["UA", "LA", "UB", "LB"], "4": ["UA", "LA", "UB", "LB"]})
        self.assertTrue(any("never squeezed" in w for w in match.filters(fake, p, BANK, build.select)))
        p = self.profile(outcome="event", outcome_detail="hyrox", experience_by={"lifting": "intermediate", "crossfit": "intermediate"},
                         skills=["run_30min"], days=3, places={"main": {"type": "gym", "equipment": ["full_gym", "sled", "skierg"]}})
        pl, c, _, week = self.plan_for(p, "hyrox-prep-4")
        self.assertEqual(c["streams"][0]["rotation"], ["S", "I", "C"])
        self.assertTrue(any("easy run is the session left out" in n for n in c["notes"]))   # what is lost is said
        p = self.profile(outcome="look", outcome_detail="size", experience_by={"lifting": "novice"}, days=2)
        pl, c, _, _ = self.plan_for(p, "muscle-fullbody-3")
        self.assertTrue(any("take turns" in n for n in c["notes"]))       # a rotation is said, and only whole body ones rotate

    def test_minutes_are_filled_within_10_percent(self):
        p = self.profile(outcome="event", outcome_detail="meet", experience_by={"lifting": "intermediate"}, days=4, minutes=75,
                         numbers={"back_squat": {"kg": 160, "reps": 3}, "bench_press": {"kg": 110, "reps": 3}, "deadlift": {"kg": 200, "reps": 3}})
        pl, c, found, week = self.plan_for(p)
        for s in week:
            m = sheet.session_seconds(s) / 60
            self.assertTrue(67.5 <= m <= 78, (s["title"], m))
        for mins in (45, 60):
            p = self.profile(outcome="look", outcome_detail="size", experience_by={"lifting": "intermediate"}, days=4, minutes=mins)
            _, _, _, week = self.plan_for(p)
            for s in week:
                self.assertGreaterEqual(sheet.session_seconds(s) / 60, 0.9 * mins, (mins, s["title"]))
        p = self.profile(outcome="look", outcome_detail="lean", days=3, minutes=45, places={"main": {"type": "outdoors", "equipment": ["outdoors"]}})
        _, c, found, week = self.plan_for(p)
        for s in week:                                                    # a fat-loss beginner on the couch to 5K: easy cardio fills it
            self.assertGreaterEqual(sheet.session_seconds(s) / 60, 40.5, s["title"])

    def test_fat_loss_gets_conditioning(self):
        p = self.profile(outcome="look", outcome_detail="lean", experience_by={"lifting": "novice"}, days=3, minutes=60)
        pl, c, found, week = self.plan_for(p)
        self.assertIn("conditioning", c["goal_modules"])
        self.assertTrue(any(b.get("_module") == "conditioning" for s in week for b in s["blocks"]))

    def test_pain_swaps_a_move_and_never_bans_the_region(self):
        lim = [{"region": "shoulder", "status": "now", "triggers": ["overhead"]}]
        p = self.profile(outcome="keep_going", outcome_detail="mix", days=3, minutes=45, limits=lim)
        q = dict(p, _care=build.care_regions(p, {}), _trig=build.trigger_limits(p))
        tags = core.place_tags(p)
        avoid = build.avoid_regions(p, {})
        self.assertEqual(avoid, set())                                     # the region is not banned
        self.assertFalse(build.allowed(BANK["overhead_press"], q, tags, avoid, 5))
        self.assertFalse(build.allowed(BANK["lat_pulldown"], q, tags, avoid, 5))
        self.assertTrue(build.allowed(BANK["db_bench_press"], q, tags, avoid, 5))
        self.assertTrue(build.allowed(BANK["seated_cable_row"], q, tags, avoid, 5))
        r = match.match(p, BANK, build.select)
        self.assertNotEqual(r["plan"]["family"], "run")                    # never knocked off strength training (08 persona 9)
        pl, c, found, week = self.plan_for(p)
        served = [it["ex"] for s in week for b in s["blocks"] for it in b["items"] if it.get("ex") in BANK]
        self.assertFalse([i for i in served if "shoulder" in BANK[i]["regions"] and "overhead" in build.row_triggers(BANK[i])])
        self.assertTrue([i for i in served if BANK[i]["pattern"] == "h_push"])   # the press is swapped, not dropped
        self.assertTrue(any("swapped" in s["notes"] for s in week))
        # a status without a trigger takes the region's usual one and asks; no status (an older limit, a flare) still bans it
        p2 = self.profile(outcome="keep_going", outcome_detail="mix", limits=[{"region": "shoulder", "status": "now"}])
        self.assertEqual(build.trigger_limits(p2), [("shoulder", {"overhead"})])
        self.assertEqual(build.avoid_regions(prof(limits=[{"region": "shoulder", "exclude": True}]), {}), {"shoulder"})
        self.assertEqual(build.avoid_regions(prof(limits=[dict(lim[0], exclude=True, flare="2026-12-01")]), {}), {"shoulder"})

    def test_the_coach_eye_fixes_or_reports(self):
        import eye
        p = self.profile(outcome="event", outcome_detail="meet", experience_by={"lifting": "intermediate"}, days=4, minutes=75)
        pl, c, found, week = self.plan_for(p)
        self.assertTrue(all(f.get("say") or f["ok"] for f in found))        # a failed check always has a plain line
        names = {f["check"] for f in found}
        self.assertTrue({"days", "push_pull", "key_quality"} <= names, names)
        s = dict(week[0], blocks=week[0]["blocks"][:2])                    # a session cut short is reported, not passed
        bad = eye.session_checks(s, pl, p)
        self.assertTrue(bad and bad[0]["check"] == "minutes" and bad[0]["say"])


class CoachHabits(unittest.TestCase):
    """Phase E, 13 nov 2026: the coach's habits around the plan (research/07, doctrine/07_CYCLE.md)."""

    BASE = Composer.BASE

    def profile(self, **ans):
        import plan, checks
        p = plan.normalise(ans, dict(self.BASE))
        self.assertEqual(checks.check_profile(p), [])
        return p

    def setup_plan(self, p):
        import compose, eye
        pid = match.match(p, BANK, build.select)["plan"]["id"]
        prog = core.load_program(pid)
        c = compose.compose(p, prog, BANK, build.select)
        pl = dict(program=pid, plain_name=c["plain_name"], days=c["days"], modules=c["modules"], goal_modules=c["goal_modules"],
                  streams=c["streams"], order=c["order"], components=c["components"], blend=c["blend"], targets=c["targets"],
                  lift_days=c["lift_days"], long_run=c["long_run"], challenge=c["challenge"], goal_on_all=c["goal_on_all"])
        st = {"block": 1, "week": 1, "week_sessions": 0, "queue": [], "slots": {}, "flags": {}}
        build.refill(st, prog, pl)
        found, week = eye.review(p, pl, st, BANK)
        return pl, st, prog, week

    def test_1_baseline_tests_are_safe_and_due_each_block(self):
        import coach
        lifter = self.profile(outcome="strong", outcome_detail="general", experience_by={"lifting": "none"})
        pl, st, prog, _ = self.setup_plan(lifter)
        b = coach.battery(lifter, pl, prog)
        ids = [t["id"] for t in b["tests"]]
        self.assertTrue(b["lifts"] and "push_ups" in ids)                      # the lifts come from the log: no max test
        self.assertFalse([t for t in ids if "max" in t])
        runner = self.profile(outcome="event", outcome_detail="run_5k_10k", run_30min=True,
                              experience_by={"running": "novice"})
        rpl, _, rprog, _ = self.setup_plan(runner)
        self.assertIn("run_2k", [t["id"] for t in coach.battery(runner, rpl, rprog)["tests"]])
        sore_shoulder = self.profile(outcome="strong", outcome_detail="general", limits=[{"region": "shoulder", "status": "now"}])
        self.assertNotIn("push_ups", [t["id"] for t in coach.battery(dict(sore_shoulder, limits=[{"region": "shoulder", "exclude": True}]), pl, prog)["tests"]])
        self.assertTrue(coach.tests_due(pl, st, lifter, "2026-12-01"))
        cmp1 = coach.record_tests(pl, st, {"results": {"push_ups": 12}}, "2026-12-01")
        self.assertIsNone(cmp1[0]["since_start"])                             # the first time is the starting point
        self.assertFalse(coach.tests_due(pl, st, lifter, "2026-12-01"))
        st.update(block=2, week=1)
        self.assertTrue(coach.tests_due(pl, st, lifter, "2027-01-01"))          # again at the start of the next block
        cmp2 = coach.record_tests(pl, st, {"results": {"push_ups": 15}}, "2027-01-01")
        self.assertEqual(cmp2[0]["since_start"], 25.0)
        self.assertEqual(coach.parse_value("run_2k", "10:30"), 630)
        self.assertEqual(coach.better("run_2k", 600, 630), 4.8)                 # faster is better for a time

    def test_2_first_milestone_is_set_and_checked(self):
        import coach
        p = self.profile(outcome="strong", outcome_detail="general", experience_by={"lifting": "novice"})
        pl, st, prog, week = self.setup_plan(p)
        m = coach.milestone(p, pl, prog, week, start="2026-12-01")
        self.assertTrue(4 * 7 <= (coach._d(m["by"]) - coach._d("2026-12-01")).days <= 6 * 7)
        self.assertTrue(m.get("lift") and m["sessions"] < pl["days"] * m["weeks"])   # very likely: under the full count
        pl["coach"] = {"milestone": m}
        ex = m["lift"]["ex"]
        log = [{"date": "2026-12-%02d" % (1 + 2 * i), "block": 1, "week": 1 + i // 3,
                "done": [{"ex": ex, "kind": "main", "result": {"load": 40 + 5 * i, "reps": [5, 5, 5]}}]} for i in range(m["sessions"])]
        self.assertEqual(coach.check_milestone(pl, log[:2], "2026-12-04")["status"], "on_track")
        self.assertEqual(coach.check_milestone(pl, log, "2026-12-30")["status"], "hit")
        missed = coach.check_milestone(pl, log[:3], "2027-03-01")             # the date has passed with 3 sessions
        self.assertEqual(missed["status"], "missed")
        self.assertNotIn("fail", missed["say"].lower())                        # said without blame

    def test_3_weekly_checkin_feeds_the_next_week(self):
        import coach
        p = self.profile(outcome="look", outcome_detail="size", experience_by={"lifting": "intermediate"}, days=4, minutes=60)
        pl, st, prog, _ = self.setup_plan(p)
        log = [{"date": "2026-12-01", "block": 1, "week": 1}, {"date": "2026-12-03", "block": 1, "week": 1}]
        st["flags"]["checkin_due"] = True
        r = coach.checkin(pl, st, p, {"barriers": ["time", "energy"], "energy": "low", "next_days": ["mon", "thu"]}, log, "2026-12-08")
        self.assertEqual(r["checkin"]["done"], 2)
        self.assertEqual(r["next_week"]["dose"], "easier")
        self.assertEqual(r["next_week"]["minutes"], 45)
        self.assertNotIn("checkin_due", st["flags"])
        a = build.build({"energy": 9, "date": "2026-12-09"}, p, pl, dict(st), BANK, "2026-12-09")
        self.assertEqual(a["minutes"], 45)                                     # the shorter week is the default
        self.assertNotEqual(a["level"], "planned")                             # and no all-out sets
        self.assertEqual(coach.week_plan(st, "2026-12-30"), {})                # it lasts one week, never longer

    def test_4_missed_week_and_forgiving_streak(self):
        import coach
        p = self.profile(outcome="strong", outcome_detail="general", experience_by={"lifting": "novice"})
        pl, st, prog, _ = self.setup_plan(p)
        st["last_session"] = "2026-12-01"
        a = build.build({"energy": 9}, p, pl, dict(st, queue=list(st["queue"])), BANK, "2026-12-10")
        self.assertEqual(a["level"], "light")                                  # 7 to 13 days: a lighter re-entry
        s2 = dict(st, queue=list(st["queue"]), flags={})
        b = build.build({"energy": 9}, p, pl, s2, BANK, "2027-01-15")
        self.assertEqual(s2["reentry"], 2)                                     # 4 weeks off: 15 percent lighter, an easy one after
        self.assertTrue(s2["flags"].get("retest"))                             # and the tests again
        self.assertIn("Welcome back", b["notes"])
        week = lambda d: {"date": d}
        log = [week("2026-11-02"), week("2026-11-10"), week("2026-11-18"), week("2026-11-30"), week("2026-12-08")]   # 23 nov empty
        s = coach.streak(log, "2026-12-09")
        self.assertEqual((s["weeks"], s["rest_weeks"]), (5, 1))                # one empty week pauses, never resets
        gap2 = [week("2026-11-02"), week("2026-11-10"), week("2026-12-08")]     # 16 and 23 nov, then 30 nov: empty
        self.assertEqual(coach.streak(gap2, "2026-12-09")["weeks"], 1)         # two empty weeks end it
        one_miss = [week("2026-11-30"), week("2026-12-02"), week("2026-12-08")]
        self.assertEqual(coach.streak(one_miss, "2026-12-09")["weeks"], 2)     # a missed session changes nothing

    def test_5_personal_bests_from_the_log(self):
        import logbook
        d = lambda load, reps, kind="main": {"ex": "back_squat", "kind": kind, "result": {"load": load, "reps": reps}}
        log = [{"date": "2026-12-01", "done": [d(60, [5, 5, 5])]}, {"date": "2026-12-03", "done": [d(62.5, [5, 5, 5])]}]
        self.assertEqual(logbook.new_records(log[:0], log[0], BANK), [])        # a first time is a start, not a record
        rec = logbook.new_records(log[:1], log[1], BANK)
        self.assertEqual((rec[0]["kind"], rec[0]["load"]), ("best", 62.5))
        more = logbook.new_records(log, {"done": [d(60, [8, 6, 6])]}, BANK)
        self.assertTrue(more and more[0]["load"] == 60 and more[0]["reps"] == 8)
        self.assertEqual(logbook.new_records(log, {"done": [d(80, [12], "accessory")]}, BANK), [])
        self.assertEqual(logbook.records(log, BANK, "lb")[0]["text"], "138 lb x 5")

    def test_6_soreness_is_not_pain(self):
        p = self.profile(outcome="look", outcome_detail="size", experience_by={"lifting": "intermediate"}, days=4, minutes=60)
        pl, st, prog, _ = self.setup_plan(p)
        today = {"energy": 9, "sore": "very", "sore_areas": ["upper"]}
        self.assertEqual(build.avoid_regions(p, today), set())                 # no region is removed
        self.assertEqual(build.readiness(today)[2], [])                        # and nothing is referred
        normal = build.build({"energy": 9}, p, pl, dict(st, queue=list(st["queue"])), BANK, "2026-12-01")
        sore = build.build(today, p, pl, dict(st, queue=list(st["queue"])), BANK, "2026-12-01")
        self.assertEqual([it["ex"] for b in normal["blocks"] if b["kind"] == "main" for it in b["items"]],
                         [it["ex"] for b in sore["blocks"] if b["kind"] == "main" for it in b["items"]])
        self.assertEqual(sore["level"], "standard")
        self.assertIn("Soreness is not an injury", sore["notes"])
        legs = build.SORE_AREAS["upper"]
        leg_sets = lambda s: sum(int(it["sets"]) for b in s["blocks"] if b["kind"] == "accessory" for it in b["items"]
                                 if legs & set(it["_slot"]["muscles"]))
        self.assertGreater(leg_sets(normal), 0)
        self.assertLess(leg_sets(sore), leg_sets(normal))                      # one set fewer on the sore muscles' extra moves

    def test_7_block_review_adjusts_the_next_block(self):
        import coach
        p = self.profile(outcome="strong", outcome_detail="general", experience_by={"lifting": "novice"})
        pl, st, prog, week = self.setup_plan(p)
        pl["coach"] = {"milestone": coach.milestone(p, pl, prog, week, start="2026-12-01")}
        st.update(block=2, week=1, flags={"review_due": True})
        log = [{"date": "2026-12-%02d" % (1 + 2 * i), "block": 1, "week": 1 + i // 3,
                "done": [{"ex": "back_squat", "kind": "main", "result": {"load": 40 + 5 * i, "reps": [5, 5, 5]}}]} for i in range(9)]
        r = coach.block_review(p, pl, st, log, prog, BANK, "2027-01-05")
        self.assertEqual((r["block"], r["sessions"]), (1, 9))
        self.assertTrue(r["lifts"] and r["lifts"][0]["pct"] > 0 and r["wins"])
        self.assertIn("keep", r["options"])
        out = coach.apply_review(p, pl, st, {"went_well": "got_stronger", "change": "harder"}, prog, "2027-01-05")
        self.assertEqual(st["block_adjust"], "harder")
        self.assertNotIn("review_due", st["flags"])
        self.assertEqual(pl["coach"]["milestone"]["from"], "2027-01-05")         # a new milestone for the new block
        self.assertIsNone(out["next_command"])
        self.assertEqual(coach.apply_review(p, pl, st, {"change": "fewer_days"}, prog, "2027-01-05")["profile"]["days"], 2)
        self.assertEqual(coach.apply_review(p, pl, st, {"change": "new_focus", "priority": ["arms"]}, prog, "2027-01-05")["next_command"],
                         ["choose", pl["program"]])

    def test_8_taper_before_an_event(self):
        import coach
        p = self.profile(outcome="event", outcome_detail="run_half", event={"name": "Lyon half", "date": "2027-03-21"},
                         experience_by={"running": "intermediate"}, run_30min=True, days=4, minutes=60)
        pl, st, prog, _ = self.setup_plan(p)
        self.assertIsNone(coach.taper(p, "2027-02-28"))                         # 3 weeks out: normal training
        t = coach.taper(p, "2027-03-10")
        self.assertEqual((t["weeks"], t["volume"]), (2, 0.7))                  # a half: two weeks, sized to the event
        self.assertEqual(coach.taper(p, "2027-03-18")["volume"], 0.5)
        self.assertEqual(coach.TAPER_WEEKS["run_marathon"], 3)
        self.assertEqual(coach.TAPER_WEEKS["run_5k_10k"], 1)
        normal = build.build({"energy": 8}, p, pl, dict(st, queue=list(st["queue"])), BANK, "2027-02-20")
        taper = build.build({"energy": 8}, p, pl, dict(st, queue=list(st["queue"])), BANK, "2027-03-18")
        self.assertTrue(taper.get("taper"))
        self.assertLess(sheet.session_seconds(taper), sheet.session_seconds(normal))   # less volume
        self.assertEqual(taper["level"], normal["level"])                     # same intensity
        self.assertIn("Easing off", taper["why"])
        self.assertTrue(build.build({"energy": 8}, p, pl, dict(st, queue=list(st["queue"])), BANK, "2027-03-21")["rest_day"])
        pl["coach"] = {}
        self.assertTrue(coach.event_after(p, pl, "2027-03-23"))                 # after it: how did it go, what is next
        self.assertFalse(coach.tests_due(pl, st, p, "2027-03-18"))              # no tests in a taper


class ImproveMode(unittest.TestCase):
    """Phase F, 13 nov 2026: "improve what I already do" (research/09, engine/improve.py). Their routine becomes
    me/PROGRAM.md and the engine runs on it; nothing of it changes without a proposal they accept."""

    BASE = {"language": "en", "units": "kg", "age_band": "18_39", "minutes": 60, "places": {"main": {"type": "gym", "equipment": ["full_gym"]}},
            "screen": {"result": "clear", "flags": []}}
    ROUTINE = {"split": "ppl", "days": 4, "day_labels": ["Push", "Pull", "Legs", "Push"], "day_kinds": ["push", "pull", "legs", "push"],
               "age": "over_1y", "stalls": ["lift_stuck"], "stuck": ["bench_press"], "keep": ["split"],
               "exercises": {"Push": [{"id": "bench_press", "sets": 4, "reps": "6-8"}, {"name": "OHP", "sets": 3, "reps": "8-10"},
                                      {"name": "lateral raises", "sets": 3, "reps": "12-15"},
                                      {"name": "Hammer Strength incline thing", "sets": 3, "reps": "10-12"},
                                      {"name": "push ups", "sets": 3, "reps": "10-15"}],
                             "Pull": [{"id": "lat_pulldown", "sets": 3, "reps": "8-12"}, {"name": "bicep curls", "sets": 3, "reps": "10-12"}],
                             "Legs": [{"name": "squat", "sets": 4, "reps": "5"}, {"id": "leg_press", "sets": 3, "reps": "10-12"}]}}

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self._mine = core.MINE
        core.MINE = self.tmp / "PROGRAM.md"                 # never the repo's me/

    def tearDown(self):
        core.MINE = self._mine
        shutil.rmtree(self.tmp, ignore_errors=True)

    def adopt(self, **kw):
        import plan, checks, improve
        ans = {"mode": "improve", "outcome": "look", "outcome_detail": "size", "priority": ["arms"],
               "current_routine": json.loads(json.dumps(self.ROUTINE))}
        ans.update(kw)
        p = plan.normalise(ans, dict(self.BASE))
        self.assertEqual(checks.check_profile(p), [])
        prog = improve.adopt(p, BANK)
        improve.write_program(prog, BANK)
        pl = plan.own_plan(p, prog, {})
        st = {"version": 1, "program": "mine", "block": 1, "week": 1, "week_sessions": 0, "queue": [], "slots": {}, "flags": {}}
        build.refill(st, prog, pl)
        return p, prog, pl, st

    def slot_of(self, prog, key):
        return next(sl for s in prog["sessions"].values() for b in s["blocks"] for sl in b["slots"] if sl["key"] == key)

    def test_1_their_routine_round_trips_into_program_md(self):
        import improve
        p, prog, pl, st = self.adopt()
        back = core.read_json_block(core.MINE)
        self.assertEqual(back, prog)                                       # the file holds exactly what runs
        self.assertEqual(core.load_program("mine"), prog)
        self.assertEqual([back["sessions"][s]["title"] for s in back["layouts"]["4"]], ["Push", "Pull", "Legs", "Push"])
        self.assertEqual(pl["days"], 4)
        words = {d["label"]: [(e.get("id"), e["sets"], e["reps"]) for e in d["exercises"]] for d in improve.routine_words(back, BANK)}
        self.assertEqual(words["Push"][:3], [("bench_press", 4, "6-8"), ("overhead_press", 3, "8-10"), ("lateral_raise", 3, "12-15")])
        self.assertEqual(words["Pull"], [("lat_pulldown", 3, "8-12"), ("db_curl", 3, "10-12")])
        self.assertEqual(words["Legs"], [("back_squat", 4, "5"), ("leg_press", 3, "10-12")])
        self.assertIn("Bench press 4 x 6 to 8", core.MINE.read_text(encoding="utf-8"))
        self.assertTrue(all(sl.get("theirs") for s in prog["sessions"].values() for b in s["blocks"] for sl in b["slots"]))
        again = improve.adopt(p, BANK)
        self.assertEqual(again, prog)                                      # the same answers, the same file

    def test_2_an_unknown_exercise_is_kept_by_name(self):
        import improve
        p, prog, pl, st = self.adopt()
        own = [sl for s in prog["sessions"].values() for b in s["blocks"] for sl in b["slots"] if sl.get("own_name")]
        self.assertEqual([sl["own_name"] for sl in own], ["Hammer Strength incline thing"])
        self.assertEqual(BANK[own[0]["prefer"][0]]["pattern"], own[0]["pattern"])   # tracked like a bank row, for weights and safety
        w = [e for d in improve.routine_words(prog, BANK) for e in d["exercises"] if e.get("own")]
        self.assertEqual(w[0]["name"], "Hammer Strength incline thing")
        s = build.build({"energy": 8}, p, pl, st, BANK, "2026-12-01")
        item = next(it for b in s["blocks"] for it in b["items"] if it.get("key") == own[0]["key"])
        self.assertEqual((item["name"], item["cue"]), ("Hammer Strength incline thing", "your usual form"))

    def test_3_the_routine_is_unchanged_until_a_proposal_is_accepted(self):
        import copy, improve, eye
        p, prog, pl, st = self.adopt(minutes=30)                           # their Push day runs long; arms are a priority
        before = copy.deepcopy(prog)
        props = improve.proposals(prog, p, pl, st, [], BANK)
        self.assertTrue(props["open"])
        self.assertEqual(prog, before)                                     # proposing touches nothing
        for i, sid in enumerate(["push", "pull", "legs"]):
            s = build.build({"energy": 8, "minutes": 30}, p, pl, dict(st, queue=[sid]), BANK, "2026-12-0%d" % (i + 1))
            got = [(it["_slot"]["slot"]["key"], it["sets"], it["reps"]) for b in s["blocks"] if b["kind"] != "warmup" for it in b["items"]]
            want = [(sl["key"], sl["sets"], sl["reps"]) for b in prog["sessions"][sid]["blocks"] for sl in b["slots"]]
            self.assertEqual(got, want, sid)                               # no priority sets, no fill, no cut, no finisher
            self.assertLessEqual(sheet.session_seconds(s), s["minutes"] * 60 + sheet.TOLERANCE)   # the sheet is never refused
            self.assertFalse(eye.session_checks(s, pl, p))
        self.assertEqual(core.read_json_block(core.MINE), before)
        short = build.build({"energy": 8, "minutes": 20}, p, pl, dict(st, queue=["push"]), BANK, "2026-12-05")
        self.assertIn("your routine stays as it is", short["notes"])       # a shorter day they ask for: cut today, said
        self.assertEqual(core.read_json_block(core.MINE), before)
        # a bodyweight move at the top of its range: the next step is a proposal, never a switch
        key = next(sl["key"] for sl in prog["sessions"]["push"]["blocks"][-1]["slots"] if sl["prefer"] == ["push_up"])
        st2 = dict(st, queue=["push"], slots={key: {"ex": "push_up", "harder": True}})
        s = build.build({"energy": 8, "minutes": 60}, p, pl, st2, BANK, "2026-12-06")
        self.assertIn("push_up", [it["ex"] for b in s["blocks"] for it in b["items"]])
        self.assertTrue(st2["slots"][key]["ready_harder"])
        self.assertIn("harder:" + key, [x["id"] for x in improve.proposals(prog, p, pl, st2, [], BANK)["all"]])

    def test_4_an_accepted_proposal_applies(self):
        import improve
        p, prog, pl, st = self.adopt()
        ids = [x["id"] for x in improve.proposals(prog, p, pl, st, [], BANK)["open"]]
        self.assertIn("pull_volume", ids)                                  # 4 presses a Push day, twice a week, and little pulling
        pulldown = self.slot_of(prog, "pull_lat_pulldown")["sets"]
        x = improve.accept(prog, pl, st, "pull_volume", p, [], BANK, "2026-12-01")
        self.assertTrue(x)
        self.assertEqual(self.slot_of(prog, "pull_lat_pulldown")["sets"], pulldown + 1)
        self.assertEqual((prog["version"], prog["changes"][0]["id"]), (2, "pull_volume"))
        improve.write_program(prog, BANK)
        self.assertIn("What the coach changed, with your yes", core.MINE.read_text(encoding="utf-8"))
        s = build.build({"energy": 8}, p, pl, dict(st, queue=["pull"]), BANK, "2026-12-02")
        self.assertEqual(next(it["sets"] for b in s["blocks"] for it in b["items"] if it.get("key") == "pull_lat_pulldown"), pulldown + 1)
        self.assertNotIn("pull_volume", [y["id"] for y in improve.proposals(prog, p, pl, st, [], BANK)["open"]])
        self.assertIsNone(improve.accept(prog, pl, st, "no_such_idea", p, [], BANK))

    def test_5_a_refused_proposal_is_not_proposed_again(self):
        import improve
        p, prog, pl, st = self.adopt()
        first = improve.proposals(prog, p, pl, st, [], BANK)["open"][0]
        before = json.dumps(prog["sessions"], sort_keys=True)
        self.assertTrue(improve.decline(prog, st, first["id"], p, pl, [], BANK, "2026-12-01"))
        self.assertEqual(json.dumps(prog["sessions"], sort_keys=True), before)    # "keep mine" keeps it
        for blk in (1, 2):
            again = improve.proposals(prog, p, pl, dict(st, block=blk), [], BANK)
            self.assertNotIn(first["id"], [x["id"] for x in again["all"]])         # not asked every session
        self.assertIn(first["id"], [x["id"] for x in improve.proposals(prog, p, pl, dict(st, block=3), [], BANK)["all"]])
        self.assertIn(first["id"], [x["id"] for x in improve.proposals(prog, dict(p, minutes=45), pl, st, [], BANK)["all"]])   # a fact changed
        self.assertLessEqual(len([x for x in improve.proposals(prog, p, pl, st, [], BANK)["open"] if not x["safety"]]), 1)   # two a block

    def test_6_progression_runs_on_their_lifts(self):
        import logbook
        p, prog, pl, st = self.adopt()
        loads = []
        for i in range(3):
            st["queue"] = ["legs"]
            s = build.build({"energy": 8}, p, pl, st, BANK, "2026-12-%02d" % (i * 2 + 1))
            res = {"legs_back_squat": {"load": 60}} if i == 0 else {}
            if i == 0:
                res["legs_leg_press"] = {"load": 100}
            logbook.apply(s, {"as_written": True, "results": res}, p, st, BANK)
            loads.append(st["slots"]["legs_back_squat"]["load"])
        self.assertEqual(loads, [60, 65, 70])                              # their 4 x 5: found, then +5 each clean session
        self.assertEqual(st["slots"]["legs_leg_press"]["target"], 12)      # their 3 x 10-12: reps first (10, 11, 12), then weight
        self.assertEqual(self.slot_of(prog, "legs_back_squat")["sets"], 4)

    def test_7_a_standing_limit_is_a_proposal_and_a_line(self):
        import improve
        p, prog, pl, st = self.adopt(limits=[{"region": "shoulder", "status": "mild", "triggers": ["overhead"]}])
        props = improve.proposals(prog, p, pl, st, [], BANK)["open"]
        lim = [x for x in props if x["id"] == "limit:push_overhead_press"]
        self.assertTrue(lim and lim[0]["safety"])
        s = build.build({"energy": 8}, p, pl, dict(st, queue=["push"]), BANK, "2026-12-01")
        self.assertIn("overhead_press", [it["ex"] for b in s["blocks"] for it in b["items"]])     # kept until they say yes
        self.assertIn("you kept Overhead press", s["notes"])
        self.assertTrue(improve.accept(prog, pl, st, "limit:push_overhead_press", p, [], BANK))
        improve.write_program(prog, BANK)
        s = build.build({"energy": 8}, p, pl, dict(st, queue=["push"]), BANK, "2026-12-03")
        self.assertNotIn("overhead_press", [it["ex"] for b in s["blocks"] for it in b["items"]])

    def test_8_names_match_the_bank(self):
        import improve
        for typed, want in (("bench", "bench_press"), ("DB bench", "db_bench_press"), ("RDLs", "romanian_deadlift"),
                            ("lat pull down", "lat_pulldown"), ("skullcrushers", "skull_crusher"), ("d\u00e9velopp\u00e9 couch\u00e9", "bench_press"),
                            ("pec deck", "cable_fly"), ("OHP", "overhead_press"), ("my cable thing", None)):
            self.assertEqual(improve.match_name(typed, BANK), want, typed)


def top_why(p):
    return match.match(p, BANK, build.select)["top"][0]["why"]


# · phase G: plain words, and a French sheet in French (research/10_plain_words.md)

import re as _re
import words, compose as _compose  # noqa: E402

# The trainer's words that never reach the person (research/10 section 2), in English and in French.
JARGON = [r"\bRPE\b", r"\bRIR\b", r"AMRAP", r"EMOM", r"\bdeload", r"training max", r"\bTM\b", r"hypertroph", r"\baccessor",
          r"\bsuperset", r"\bfinisher\b", r"\bmetcon", r"5/3/1", r"\bBBB\b", r"Boring But Big", r"\bGZCL", r"\bT[123]\b", r"\bPHUL\b",
          r"\bPHAT\b", r"\b5RM\b", r"in the tank", r"\bfailure\b", r"\btop set", r"\bwave\b", r"your rotation", r"\bdose\b",
          r"\bExpress\b", r"[Mm]ain block", r"\bblock\b", r"\bthreshold", r"\bstrides\b", r"\btempo\b", r"[Cc]ompromised", r"[Cc]hipper",
          r"[Cc]ouplet", r"[Tt]riplet", r"\bRDL\b", r"\blats?\b", r"\bmidfoot\b", r"\blockout\b", r"\bcap\b", r"[Nn]ovices?\b",
          r"\bdivision\b", r"\b\d+ left\b", r"max d.entra[iî]nement", r"\bvague\b", r"[ée]chec", r"d[ée]charge", r"\bbloc\b",
          r"hypertrophie", r"accessoire"]
SPREAD = ["strength-lp-3", "strength-531-bbb-4", "strength-531-beginners-3", "strength-gzclp-4", "strength-rpe-4", "strength-texas-3",
          "powerbuild-phul-4", "powerbuild-phat-5", "muscle-ppl-6", "functional-gpp-3to5", "hyrox-prep-4", "run-base-3to5", "run-c25k-3",
          "hybrid-strength-endurance-4to6", "weightlifting-novice-3", "health-baseline-2to3"]


def person_text(s):
    """Every word of a built session the person reads on the sheet."""
    out = [s.get(k) for k in ("title", "program_name", "level_text", "why", "notes", "low_energy", "score_to_beat")] + list(s.get("log") or [])
    for b in s["blocks"]:
        out += [b.get("name"), b.get("rest_note")]
        for it in b["items"]:
            out += [it.get(k) for k in ("name", "cue", "effort", "reps", "load", "first_outing")]
    return [str(x) for x in out if x not in (None, "")]


def week_of(pid, lang, variant="plain"):
    import smoke_programs
    prog = core.load_program(pid)
    p = prof(language=lang, **{k: v for k, v in smoke_programs.profile_for(prog).items() if k != "units"})
    if variant == "numbers":
        p["numbers"] = {"back_squat": {"kg": 100, "reps": 5}, "bench_press": {"kg": 70, "reps": 5}, "deadlift": {"kg": 120, "reps": 5},
                        "overhead_press": {"kg": 45, "reps": 5}}
    c = _compose.compose(p, prog, BANK, build.select)
    pl = dict(program=pid, plain_name=c["plain_name"], days=c["days"], modules=c["modules"], goal_modules=c["goal_modules"],
              streams=c["streams"], order=c["order"], components=c["components"], blend=c["blend"], targets=c["targets"],
              lift_days=c["lift_days"], long_run=c["long_run"], challenge=c["challenge"], goal_on_all=c["goal_on_all"])
    st = {"block": 1, "week": prog.get("block_weeks", 4) + 1 if variant == "deload" else 1, "week_sessions": 0, "queue": [], "slots": {}}
    build.refill(st, prog, pl)
    out = []
    for i in range(pl["days"]):
        s = build.build({"energy": 4 if variant == "light" else 7, "minutes": p["minutes"]}, p, pl, st, BANK, "2030-01-%02d" % (7 + i))
        out.append(words.localize_session(s, BANK))
        q = st.get("queue") or []
        if s.get("_queue_index", 0) < len(q):
            q.pop(s["_queue_index"])
        st["week_sessions"] += 1
    return out


sys.path.insert(0, str(REPO / "tests"))


class PlainWords(unittest.TestCase):
    def jargon_in(self, sessions):
        hits = []
        for s in sessions:
            for line in person_text(s):
                for j in JARGON:
                    if _re.search(j, line):
                        hits.append((s["program"], j, line))
        return hits

    def test_no_jargon_on_an_english_sheet(self):
        for pid in SPREAD:
            for v in ("plain", "numbers", "deload", "light"):
                hits = self.jargon_in(week_of(pid, "en", v))
                self.assertFalse(hits, hits[:3])

    def test_no_jargon_on_a_french_sheet(self):
        for pid in SPREAD:
            for v in ("plain", "numbers", "deload"):
                hits = self.jargon_in(week_of(pid, "fr", v))
                self.assertFalse(hits, hits[:3])

    def test_a_french_sheet_is_in_french(self):
        words.clear()
        fr = words.bank_fr()
        for pid in SPREAD:
            for v in ("plain", "numbers", "deload", "light"):
                for s in week_of(pid, "fr", v):
                    for b in s["blocks"]:
                        for it in b["items"]:
                            if it.get("ex") in fr and not (it.get("_slot") or {}).get("slot", {}).get("own_name"):
                                self.assertEqual(it["name"], fr[it["ex"]]["name"])
        self.assertEqual(words.MISSES, [], words.MISSES[:5])     # every line found its French: no English on the sheet
        s = week_of("strength-531-bbb-4", "fr")[0]
        names = [it["name"] for b in s["blocks"] for it in b["items"]]
        self.assertIn("Back squat", names)
        self.assertIn("Tractions supination", names)
        bs = next(it for b in s["blocks"] for it in b["items"] if it["ex"] == "back_squat")
        self.assertEqual(bs["cue"], fr["back_squat"]["cue"])
        self.assertTrue(s["why"].startswith("Séance 1 sur"), s["why"])
        self.assertIn("Version courte", dict(_csv_rows())["Short version · Heavy squat · lighter bench"])
        html = sheet.render_html(s)
        self.assertIn('lang="fr"', html)
        self.assertIn("semaine 1 sur", html)
        for en in ("Why this session", "Score to beat", "Warm-up", "Main lifts", "reps spare", "next in your"):
            self.assertNotIn(en, html)

    def test_french_coverage_is_complete(self):
        cov = words.coverage()
        self.assertEqual(cov, {"bank_missing": [], "bank_unknown": [], "lines_missing": []})
        self.assertEqual(len(words.bank_fr()), len(BANK))

    def test_engine_lines_in_french(self):
        self.assertEqual(words.tr("Back squat: next time 85 kg on the last set", "fr"), "Back squat : la prochaine fois 85 kg sur la dernière série")
        self.assertEqual(words.tr("Bench press: 70 kg x 6, your best yet", "fr"), "Développé couché : 70 kg x 6, ton record")
        self.assertEqual(words.tr("the first session", "fr"), "la première séance")
        self.assertEqual(words.tr("Strength, 3 days", "fr"), "Force, 3 jours")
        self.assertEqual(words.swap_names("Push A: Lat pulldown instead of Pull-up", "fr"), "Push A: Tirage vertical instead of Tractions")
        self.assertEqual(words.tr("anything", "en"), "anything")

    def test_next_load_is_a_weight_not_a_method(self):
        s = week_of("strength-531-bbb-4", "en", "numbers")[0]
        self.assertNotIn("training max", json.dumps(s))
        self.assertIn("week 1 of", sheet.form(s)["meta"])


def _csv_rows():
    import csv
    with open(REPO / "doctrine" / "words" / "fr.csv", encoding="utf-8") as f:
        return [(r["en"], r["fr"]) for r in csv.DictReader(f)]


if __name__ == "__main__":
    unittest.main(verbosity=1)
