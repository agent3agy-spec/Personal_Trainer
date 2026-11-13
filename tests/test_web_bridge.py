#!/usr/bin/env python3
"""test_web_bridge.py · the web trainer's engine, proven end to end. Run: python3 tests/test_web_bridge.py

The page runs engine/ and doctrine/ unchanged, except engine/gitops.py, which is swapped for
site/py/gitops_web.py. This test does the same swap in a temporary copy, then walks the whole
chain the page walks, through plan.py subprocesses: status, screen, profile, match, choose,
build, render, log, week. It also renders once with the browser printers switched off, which is
the path the page takes (Pyodide has no browser to print with), so the standard library PDF is proven.
"""
import json, pathlib, shutil, subprocess, sys, tempfile, unittest

REPO = pathlib.Path(__file__).resolve().parent.parent


class WebBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="trainer-web-")
        root = pathlib.Path(cls.tmp)
        shutil.copytree(REPO / "engine", root / "engine", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(REPO / "doctrine", root / "doctrine")
        shutil.copy(REPO / "site" / "py" / "gitops_web.py", root / "engine" / "gitops.py")
        if (REPO / "VERSION").exists():
            shutil.copy(REPO / "VERSION", root / "VERSION")
        (root / "me").mkdir()
        (root / "sessions").mkdir()
        cls.root = root

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def plan(self, *args):
        r = subprocess.run([sys.executable, "engine/plan.py", *args], cwd=self.root, capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, "plan.py %s failed: %s" % (" ".join(args), r.stderr[-800:]))
        return json.loads(r.stdout)

    def write(self, name, data):
        (self.root / "me" / name).write_text(json.dumps(data), encoding="utf-8")
        return "me/" + name

    def test_chain(self):
        s = self.plan("status")
        self.assertEqual(s["stage"], "new")

        r = self.plan("screen", self.write("answers.json", {"items": [], "language": "en"}))
        self.assertEqual(r["result"], "clear")
        self.assertEqual(r["saved"], "saved on this device")
        self.assertEqual(self.plan("status")["stage"], "interview")

        r = self.plan("profile", self.write("answers.json", {
            "goal": "health", "experience": "none", "days": 3, "minutes": 45,
            "places": {"main": {"type": "gym", "equipment": ["full_gym"]}}, "default_place": "main",
            "units": "kg", "paper": "A4", "likes": [], "dislikes": [], "limits": [], "numbers": {}, "skills": []}))
        self.assertTrue(r["ok"], r)
        self.assertEqual(self.plan("status")["stage"], "needs_program")

        m = self.plan("match")
        self.assertEqual(len(m["top"]), 3)
        pid = m["top"][0]["id"]
        self.assertNotIn(pid, m["failed"])

        r = self.plan("choose", pid)
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["program"], pid)
        self.assertEqual(self.plan("status")["stage"], "ready")

        b = self.plan("build", self.write("today.json", {"energy": 7, "pain": [], "minutes": 45}))
        self.assertTrue(b["ok"], b)
        self.assertFalse(b["rest_day"])
        session = b["session"]
        self.assertTrue((self.root / session).exists())

        r = self.plan("render", session)
        self.assertTrue(r["ok"], r)
        pdf = self.root / r["pdf"]
        self.assertTrue(pdf.exists() and pdf.stat().st_size > 500, "no PDF after render")
        self.assertTrue(pdf.read_bytes().startswith(b"%PDF"))
        self.assertTrue((self.root / session).with_suffix(".html").exists(), "no html beside the session")
        self.assertEqual(self.plan("status")["stage"], "pending_log")

        # the page's how-did-it-go: done as written, but a first outing must carry its weight
        sess = json.loads((self.root / session).read_text(encoding="utf-8"))
        r = self.plan("log", self.write("report.json", {"as_written": True}))
        self.assertFalse(r["ok"])
        need = [n["key"] for n in r.get("needs", [])]
        results = {}
        for blk in sess["blocks"]:
            for it in blk["items"]:
                sl = it.get("_slot")
                if sl and sl["key"] in need:
                    results[sl["key"]] = {"load": 10}
        r = self.plan("log", self.write("report.json", {"as_written": True, "results": results,
                                                         "felt": "good", "pain": []}))
        self.assertTrue(r["ok"], r)
        self.assertEqual(self.plan("status")["stage"], "ready")
        self.assertEqual(self.plan("status")["sessions_logged"], 1)

        w = self.plan("week")
        self.assertEqual(w["done_this_week"], 1)
        self.assertTrue(w["last_7_days"])

    def test_french_chain(self):
        """A French person, the page's way: the status, the sheet, the log and the records come back in French."""
        other = pathlib.Path(tempfile.mkdtemp(prefix="trainer-web-fr-"))
        try:
            for d in ("engine", "doctrine"):
                shutil.copytree(self.root / d, other / d, ignore=shutil.ignore_patterns("__pycache__"))
            (other / "me").mkdir()
            (other / "sessions").mkdir()

            def plan(*args):
                r = subprocess.run([sys.executable, "engine/plan.py", *args], cwd=other, capture_output=True, text=True, timeout=120)
                self.assertEqual(r.returncode, 0, r.stderr[-800:])
                return json.loads(r.stdout)

            def write(name, data):
                (other / "me" / name).write_text(json.dumps(data), encoding="utf-8")
                return "me/" + name
            plan("screen", write("answers.json", {"items": [], "language": "fr"}))
            r = plan("profile", write("answers.json", {
                "goal": "strength", "experience": "novice", "days": 3, "minutes": 60, "language": "fr",
                "places": {"main": {"type": "gym", "equipment": ["full_gym"]}}, "default_place": "main",
                "units": "kg", "paper": "A4", "likes": [], "dislikes": [], "limits": [], "numbers": {}, "skills": []}))
            self.assertTrue(r["ok"], r)
            pid = plan("match")["top"][0]["id"]
            self.assertTrue(plan("choose", pid)["ok"])
            st = plan("status")
            self.assertEqual(st["stage"], "ready")
            b = plan("build", write("today.json", {"energy": 7, "pain": [], "minutes": 60}))
            s = json.loads((other / b["session"]).read_text(encoding="utf-8"))
            self.assertTrue(s["why"].startswith("Séance 1 sur"), s["why"])
            self.assertIn("Échauffement", [blk["name"] for blk in s["blocks"]])
            names = [it["name"] for blk in s["blocks"] for it in blk["items"]]
            self.assertTrue({"Soulevé de terre", "Développé couché", "Développé militaire", "Rowing barre"} & set(names), names)
            r = plan("render", b["session"])
            self.assertTrue(r["ok"], r)
            html = (other / b["session"]).with_suffix(".html").read_text(encoding="utf-8")
            self.assertIn("Pourquoi cette séance", html)
            self.assertNotIn("Why this session", html)
            results = {}
            for blk in s["blocks"]:
                for it in blk["items"]:
                    if it.get("_slot") and it.get("first_outing"):
                        results[it["_slot"]["key"]] = {"load": 40, "reps": [5, 5, 5]}
            r = plan("log", write("report.json", {"as_written": True, "results": results, "felt": "good", "pain": []}))
            self.assertTrue(r["ok"], r)
            for line in r["next_loads"]:
                self.assertIn("la prochaine fois", line)
            self.assertNotIn("first session", json.dumps(plan("status"), ensure_ascii=False))
        finally:
            shutil.rmtree(other, ignore_errors=True)

    def test_web_pdf_path(self):
        """No browser to print with, as in the page: the standard library PDF must still come out, one page."""
        code = r"""
import json, sys, pathlib
sys.path.insert(0, 'engine')
import sheet
sheet.render_pdf = lambda h, p: False
p = pathlib.Path(sys.argv[1])
r = sheet.render_file(p)
print(json.dumps(r))
"""
        root = self.root
        sub = [sys.executable, "engine/plan.py"]
        # a fresh person in a second copy, so the chain test above is untouched
        other = pathlib.Path(tempfile.mkdtemp(prefix="trainer-web-pdf-"))
        try:
            for d in ("engine", "doctrine"):
                shutil.copytree(root / d, other / d, ignore=shutil.ignore_patterns("__pycache__"))
            (other / "me").mkdir()
            (other / "sessions").mkdir()

            def run(*a):
                return json.loads(subprocess.run(sub + list(a), cwd=other, capture_output=True, text=True, timeout=120).stdout)
            (other / "me" / "a.json").write_text(json.dumps({"items": [], "language": "fr"}))
            self.assertEqual(run("screen", "me/a.json")["result"], "clear")
            (other / "me" / "a.json").write_text(json.dumps({"goal": "strength", "experience": "none", "days": 3, "minutes": 60,
                                                             "places": {"main": {"type": "home_gym", "equipment": ["home_dumbbells"]}},
                                                             "dumbbells": [4, 8, 12]}))
            self.assertTrue(run("profile", "me/a.json")["ok"])
            pid = run("match")["top"][0]["id"]
            self.assertTrue(run("choose", pid)["ok"])
            (other / "me" / "t.json").write_text(json.dumps({"energy": 5, "pain": [], "minutes": 30}))
            b = run("build", "me/t.json")
            self.assertTrue(b["ok"], b)
            r = subprocess.run([sys.executable, "-c", code, b["session"]], cwd=other, capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stderr[-800:])
            out = json.loads(r.stdout)
            self.assertEqual(out["renderer"], "minipdf")
            self.assertEqual(out["pages"], 1)
            self.assertTrue((other / out["pdf"]).read_bytes().startswith(b"%PDF"))
        finally:
            shutil.rmtree(other, ignore_errors=True)

    def fresh(self, prefix):
        other = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
        for d in ("engine", "doctrine"):
            shutil.copytree(self.root / d, other / d, ignore=shutil.ignore_patterns("__pycache__"))
        (other / "me").mkdir()
        (other / "sessions").mkdir()

        def run(name, data, *args):
            if data is not None:
                (other / "me" / name).write_text(json.dumps(data))
            r = subprocess.run([sys.executable, "engine/plan.py", *args], cwd=other, capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stderr[-800:])
            return json.loads(r.stdout)
        return other, run

    def test_both_fork_paths_as_the_page_sends_them(self):
        """The two paths of the page: one plan, 'not for me' re-runs the match, improve keeps the shape of the week."""
        for path in ("new", "improve"):
            other, run = self.fresh("trainer-web-%s-" % path)
            try:
                self.assertEqual(run("a.json", {"items": [], "language": "en"}, "screen", "me/a.json")["result"], "clear")
                ans = {"mode": path, "outcome": "look", "outcome_detail": "size", "days": 4, "minutes": 60,
                       "places": {"main": {"type": "gym", "equipment": ["full_gym"]}}, "default_place": "main",
                       "units": "kg", "paper": "A4", "units_confirmed": False, "enjoys": [], "avoids": [], "limits": [],
                       "sleep": "7_plus", "stress": "low"}
                if path == "new":
                    ans.update(done_before=["lifting"], experience_by={"lifting": "intermediate"}, style_pref="trainer")
                else:
                    ans.update(current_routine={"split": "upper_lower", "days": 4, "age": "over_1y", "stalls": ["lift_stuck"],
                                                "keep": ["split"], "exercises": {"Upper": ["bench_press", "barbell_row"]}})
                r = run("a.json", ans, "profile", "me/a.json")
                self.assertTrue(r["ok"], r)
                m = run(None, None, "match")
                self.assertIn("plan", m)
                self.assertEqual("improve_note" in m, path == "improve")
                first = m["plan"]["id"]
                r = run("a.json", {"rejected": [{"program": first, "reason": "not_enjoy"}]}, "profile", "me/a.json")
                self.assertTrue(r["ok"], r)
                m2 = run(None, None, "match")
                self.assertNotEqual(m2["plan"]["id"], first)
                c = run(None, None, "choose", m2["plan"]["id"])
                self.assertTrue(c["ok"], c)
                self.assertEqual("Your classes stay yours" in (c.get("say_also") or ""), path == "improve")   # match is the classes-only fallback
                self.assertTrue(c.get("components"), c)                # the composer wrote the week
            finally:
                shutil.rmtree(other, ignore_errors=True)

    def test_improve_path_as_the_page_sends_it(self):
        """Phase F: their routine becomes me/PROGRAM.md (adopt), the proposals come back as cards (improve), a yes
        applies, a no is remembered, and the sheet and the log run on their own program, rebuild included."""
        other, run = self.fresh("trainer-web-improve-")
        try:
            run("a.json", {"items": [], "language": "en"}, "screen", "me/a.json")
            ex = lambda *xs: [{"name": n, "sets": s, "reps": r} for n, s, r in xs]
            r = run("a.json", {"mode": "improve", "outcome": "look", "outcome_detail": "size", "days": 4, "minutes": 60,
                               "places": {"main": {"type": "gym", "equipment": ["full_gym"]}}, "default_place": "main", "units": "kg",
                               "priority": ["arms"], "limits": [],
                               "current_routine": {"split": "upper_lower", "days": 4, "age": "over_1y", "stalls": ["lift_stuck"], "stuck": ["bench_press"],
                                                   "keep": ["split"], "day_labels": ["Upper", "Lower", "Upper", "Lower"],
                                                   "day_kinds": ["upper", "lower", "upper", "lower"],
                                                   "exercises": {"Upper": ex(("Bench press", 4, "6-8"), ("Overhead press", 3, "8-10"), ("my machine press", 3, "10-12")),
                                                                 "Lower": ex(("Back squat", 4, "5"), ("Leg press", 3, "10-12"))}}}, "profile", "me/a.json")
            self.assertTrue(r["ok"], r)
            st = run(None, None, "status")
            self.assertEqual((st["stage"], st["mode"]), ("needs_program", "improve"))
            a = run(None, None, "adopt")
            self.assertTrue(a["ok"], a)
            self.assertTrue((other / "me" / "PROGRAM.md").exists())
            self.assertEqual([d["label"] for d in a["routine"]], ["Upper", "Lower"])
            self.assertEqual([(e["name"], e["sets"], e["reps"]) for e in a["routine"][0]["exercises"]],
                             [("Bench press", 4, "6-8"), ("Overhead press", 3, "8-10"), ("my machine press", 3, "10-12")])
            self.assertTrue(a["proposals"])
            for x in a["proposals"]:
                self.assertTrue(x["why"] and x["change"] and x["kind"] and "ops" not in x)
            first = a["proposals"][0]["id"]
            y = run(None, None, "improve", "accept", first)
            self.assertTrue(y["ok"] and y["answer"] == "accept" and y["changes"], y)
            self.assertNotIn(first, [x["id"] for x in y["proposals"]])
            if y["proposals"]:
                second = y["proposals"][0]["id"]
                n = run(None, None, "improve", "decline", second)
                self.assertTrue(n["ok"] and n["declined"], n)
                self.assertNotIn(second, [x["id"] for x in run(None, None, "improve")["proposals"]])
            self.assertFalse(run(None, None, "improve", "accept", "nothing_here")["ok"])
            self.assertIn("What the coach changed, with your yes", (other / "me" / "PROGRAM.md").read_text(encoding="utf-8"))
            st = run(None, None, "status")
            self.assertEqual((st["stage"], st["program"]), ("ready", "mine"))
            self.assertIn("proposals", st["coach"])
            for d in ("2026-12-01", "2026-12-03", "2026-12-05", "2026-12-07"):           # Upper, Lower, Upper, Lower
                b = run("today.json", {"energy": 8, "minutes": 60, "date": d}, "build", "me/today.json")
                self.assertTrue(b["ok"], b)
                if d == "2026-12-01":
                    self.assertTrue(run(None, None, "render", b["session"])["ok"])
                sess = json.loads((other / b["session"]).read_text(encoding="utf-8"))
                self.assertEqual(sess["program"], "mine")
                res = {it["_slot"]["key"]: {"load": 40} for blk in sess["blocks"] for it in blk["items"]
                       if it.get("_slot") and it.get("first_outing") and it["_slot"]["load_type"] not in ("bodyweight", "band", "time", "distance", "calories")}
                lg = run("report.json", {"as_written": True, "date": d, "results": res}, "log", "me/report.json")
                self.assertTrue(lg["ok"], lg)
            state = json.loads((other / "me" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["slots"]["upper_bench_press"]["load"], 40)
            self.assertEqual(state["slots"]["lower_back_squat"]["load"], 45)          # their 4 x 5 moved up with a clean session
            (other / "me" / "state.json").write_text("{}")
            self.assertTrue(run(None, None, "rebuild")["ok"])
            again = json.loads((other / "me" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(again["slots"]["lower_back_squat"]["load"], 45)
            self.assertEqual(again["queue"], state["queue"])
            k = run(None, None, "adopt")                                               # the same routine again: their yes kept
            self.assertTrue(k["ok"] and k["kept"] and k["changes"], k)
        finally:
            shutil.rmtree(other, ignore_errors=True)

    def test_classes_only_falls_back_to_the_closest_plan(self):
        other, run = self.fresh("trainer-web-classes-")
        try:
            run("a.json", {"items": [], "language": "en"}, "screen", "me/a.json")
            r = run("a.json", {"mode": "improve", "outcome": "athletic", "days": 3, "minutes": 60,
                               "places": {"main": {"type": "gym", "equipment": ["crossfit_box"]}}, "units": "kg",
                               "current_routine": {"split": "classes", "days": 3, "age": "3_12m", "day_labels": ["Class", "Class", "Class"],
                                                   "day_kinds": ["class", "class", "class"], "exercises": {}}}, "profile", "me/a.json")
            self.assertTrue(r["ok"], r)
            a = run(None, None, "adopt")
            self.assertEqual((a["ok"], a["fallback"]), (False, "match"))
            self.assertFalse((other / "me" / "PROGRAM.md").exists())
            self.assertIn("improve_note", run(None, None, "match"))
        finally:
            shutil.rmtree(other, ignore_errors=True)

    def test_coach_turns_as_the_page_sends_them(self):
        """Phase E: the tests, the check-in, the records and the block review, through the page's own calls."""
        other, run = self.fresh("trainer-web-coach-")
        try:
            run("a.json", {"items": [], "language": "en"}, "screen", "me/a.json")
            r = run("a.json", {"mode": "new", "outcome": "strong", "outcome_detail": "general", "days": 3, "minutes": 45,
                               "places": {"main": {"type": "gym", "equipment": ["full_gym"]}}, "default_place": "main",
                               "experience_by": {"lifting": "novice"}, "units": "kg"}, "profile", "me/a.json")
            self.assertTrue(r["ok"], r)
            c = run(None, None, "choose", run(None, None, "match")["plan"]["id"])
            self.assertTrue(c["milestone"]["text"].startswith("By "))
            self.assertTrue(c["tests"]["tests"])
            st = run(None, None, "status")
            self.assertTrue(st["coach"]["tests_due"])
            self.assertEqual(st["coach"]["next_turn"], "tests_due")
            t = run("tests.json", {"results": {c["tests"]["tests"][0]["id"]: 20}}, "tests", "me/tests.json")
            self.assertTrue(t["ok"] and t["compare"], t)
            self.assertFalse(run(None, None, "status")["coach"]["tests_due"])
            lg = None
            for i, d in enumerate(("2026-12-01", "2026-12-03", "2026-12-05")):
                b = run("today.json", {"energy": 8, "minutes": 45, "date": d, "sore": "some"}, "build", "me/today.json")
                self.assertTrue(b["ok"], b)
                sess = json.loads((other / b["session"]).read_text(encoding="utf-8"))
                res = {it["_slot"]["key"]: {"load": 40} for blk in sess["blocks"] for it in blk["items"]
                       if it.get("_slot") and it.get("first_outing") and it["_slot"]["load_type"] not in ("bodyweight", "band", "time", "distance", "calories")}
                lg = run("report.json", {"as_written": True, "date": d, "results": res}, "log", "me/report.json")
                self.assertTrue(lg["ok"], lg)
                self.assertIn("records_new", lg)
            self.assertTrue(lg["checkin_due"])
            self.assertTrue(lg["records_new"])                                  # the squat went up: a best, from the log
            self.assertEqual(run(None, None, "status")["coach"]["next_turn"], "checkin_due")
            ci = run("checkin.json", {"barriers": ["time"], "energy": "ok", "next_days": ["mon", "wed", "fri"]}, "checkin", "me/checkin.json")
            self.assertTrue(ci["ok"] and ci["next_week"]["minutes"] == 30, ci)
            w = run(None, None, "week")
            self.assertIn("streak", w)
            self.assertTrue(w["records"])
            br = run(None, None, "blockreview")
            self.assertTrue(br["ok"] and "keep" in br["options"], br)
            ap = run("review.json", {"went_well": "showed_up", "change": "keep"}, "blockreview", "me/review.json")
            self.assertTrue(ap["ok"] and ap["milestone"], ap)
            self.assertIn('"coach"', (other / "me" / "PLAN.md").read_text(encoding="utf-8"))   # kept where the page's backup reads it
        finally:
            shutil.rmtree(other, ignore_errors=True)

    def test_screen_stop_builds_nothing(self):
        other = pathlib.Path(tempfile.mkdtemp(prefix="trainer-web-stop-"))
        try:
            for d in ("engine", "doctrine"):
                shutil.copytree(self.root / d, other / d, ignore=shutil.ignore_patterns("__pycache__"))
            (other / "me").mkdir()
            (other / "sessions").mkdir()
            (other / "me" / "a.json").write_text(json.dumps({"items": [2], "language": "en"}))
            r = json.loads(subprocess.run([sys.executable, "engine/plan.py", "screen", "me/a.json"], cwd=other,
                                          capture_output=True, text=True).stdout)
            self.assertEqual(r["result"], "stop")
            self.assertTrue(r["message"])
            st = json.loads(subprocess.run([sys.executable, "engine/plan.py", "status"], cwd=other, capture_output=True, text=True).stdout)
            self.assertEqual(st["stage"], "screen_stopped")
            r = json.loads(subprocess.run([sys.executable, "engine/plan.py", "profile", "me/a.json"], cwd=other,
                                          capture_output=True, text=True).stdout)
            self.assertFalse(r["ok"])
        finally:
            shutil.rmtree(other, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
