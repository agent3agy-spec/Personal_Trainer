#!/usr/bin/env python3
"""plan.py · the one command the trainer runs. Every step of /train is a subcommand.

    python3 engine/plan.py status                 where this person is, and the next step (always first)
    python3 engine/plan.py screen  me/answers.json   the safety screen
    python3 engine/plan.py profile me/answers.json   the interview answers become me/PROFILE.md
    python3 engine/plan.py match                  the top three programs, by rule
    python3 engine/plan.py choose  <program-id>   writes me/PLAN.md and me/state.json, commits
    python3 engine/plan.py build   me/today.json  today's session JSON in sessions/
    python3 engine/plan.py render  <session.json> the PDF (engine/sheet.py), then commits
    python3 engine/plan.py log     me/report.json what was done becomes memory, commits
    python3 engine/plan.py log     unreported     the last session was never reported
    python3 engine/plan.py week                   this week: done, left, hard sets per muscle
    python3 engine/plan.py rebuild                state.json rebuilt from the log alone
    python3 engine/plan.py review  "<two lines>"  keeps the end-of-block verdict in me/PLAN.md
    python3 engine/plan.py discard                throw away a session built but not trained (after an audit), to build again
    python3 engine/plan.py commit  "<message>"    checks, then commit and push me/ and sessions/
    python3 engine/plan.py visibility             is this copy public or private on GitHub
    python3 engine/plan.py update                 what changed upstream (add "yes" to apply)
    python3 engine/plan.py forget                 how to erase everything (add "yes" to wipe me/ and sessions/ here)

Every command prints JSON first (for the coach) and nothing else. The coach turns it into words.
"""
import datetime, json, pathlib, re, shutil, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core, screen as screen_mod, match as match_mod, build as build_mod, logbook, gitops, checks

UPSTREAM = "https://github.com/agent3agy-spec/Personal_Trainer"


def out(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    return 0


def read_arg_json(path):
    p = pathlib.Path(path)
    if not p.is_absolute():
        p = core.ROOT / p
    return json.loads(p.read_text(encoding="utf-8"))


def write_profile(prof):
    goal = prof.get("goal")
    if not goal:
        core.write_json_block(core.PROFILE, prof, "# Your profile\n\n_The safety check is done. The rest fills in after the interview._")
        return
    lines = ["# Your profile", "",
             "_The trainer wrote this from your answers. You can change it any time: say `/train goals`, or edit the values in the block below on GitHub._",
             "", "| | |", "|:-|:-|",
             "| goal | %s%s |" % (goal, (" · then " + prof["goal2"]) if prof.get("goal2") else ""),
             "| what you want | %s |" % (" · ".join(x.replace("_", " ") for x in (prof.get("outcome"), prof.get("outcome_detail")) if x) or goal),
             "| how you start | %s |" % ("improving what you already do" if prof.get("mode") == "improve" else "a new plan"),
             "| experience | %s |" % prof.get("experience"),
             "| week | %s sessions of %s min |" % (prof.get("days"), prof.get("minutes")),
             "| where | %s |" % ", ".join("%s: %s" % (k, ", ".join(v.get("equipment", []))) for k, v in (prof.get("places") or {}).items()),
             "| limits | %s |" % (", ".join(l.get("region", "") + (" (" + l["note"] + ")" if l.get("note") else "") for l in prof.get("limits", [])) or "none"),
             "| language · units | %s · %s |" % (prof.get("language"), prof.get("units")),
             "| safety screen | %s on %s |" % ((prof.get("screen") or {}).get("result"), (prof.get("screen") or {}).get("date")),
             "| what I keep in mind | %s |" % (", ".join(f.replace("_", " ") for f in (prof.get("screen") or {}).get("flags", [])) or "nothing special")]
    core.write_json_block(core.PROFILE, prof, "\n".join(lines))


# · status

def cmd_status(args):
    prof = core.profile() or {}
    pl = core.plan()
    st = core.state()
    log = core.read_log()
    res = {"language": prof.get("language"), "today": core.today()}
    scr = prof.get("screen") or {}
    if not prof or not scr:
        res.update(stage="new", next="Say hello in the person's language, explain in two lines, then the safety screen (doctrine/02_INTERVIEW.md round 0).")
    elif scr.get("result") == "stop":
        res.update(stage="screen_stopped", reasons=scr.get("reasons"),
                   next="Ask whether they have since been cleared. If yes: re-run screen with cleared true. If not: the stop message, kindly.")
    elif scr.get("result") == "needs_ok":
        res.update(stage="screen_needs_ok", reasons=scr.get("reasons"),
                   next="Ask whether their provider or doctor has agreed. If yes: re-run screen with provider_ok or doctor_ok true.")
    elif not prof.get("goal"):
        res.update(stage="interview", next="Rounds 1 to 3 of the interview (doctrine/02_INTERVIEW.md), then plan.py profile.")
    elif not pl:
        res.update(stage="needs_program", next="Run plan.py match and offer the top three.")
    elif st and st.get("pending"):
        res.update(stage="pending_log", pending=st["pending"],
                   next="Ask how the last session went (or 'skip it'). Then plan.py log. Then offer today's session.")
    else:
        prog = core.load_program(pl["program"])
        q = (st or {}).get("queue") or []
        res.update(stage="ready", program=pl["program"], program_name=prog["name"],
                   block=(st or {}).get("block"), week=(st or {}).get("week"),
                   next_session=(prog["sessions"].get(q[0], {}).get("title") if q and not q[0].startswith("mod:") else (q[0] if q else "the first session")),
                   next="Ask the four readiness questions in one turn, write me/today.json, run plan.py build.")
    res["sessions_logged"] = len(log)
    if prof.get("screen", {}).get("date"):
        try:
            if (datetime.date.today() - datetime.date.fromisoformat(prof["screen"]["date"])).days > 365:
                res["screen_due"] = True
        except ValueError:
            pass
    return out(res)


# · screen and profile

def cmd_screen(args):
    ans = read_arg_json(args[0])
    prof = core.profile() or {}
    old = prof.get("screen") or {}
    r = screen_mod.run(ans)
    if old.get("result") == "needs_ok" and r["result"] == "clear" and not (ans.get("provider_ok") or ans.get("doctor_ok") or ans.get("correction")):
        return out({"result": "needs_ok", "reasons": old.get("reasons"), "message": " ".join(screen_mod.MESSAGES[n] for n in old.get("reasons", []) if n in screen_mod.MESSAGES),
                    "say": "A hold is lifted only by the go-ahead (provider_ok or doctor_ok) or a confirmed mistake (correction)."})
    if old.get("result") == "stop" and r["result"] != "stop" and not ans.get("cleared") and not ans.get("correction"):
        return out({"result": "stop", "reasons": old.get("reasons"), "message": screen_mod.MESSAGES["parq"],
                    "say": "A stop is lifted only when they say a professional cleared them (cleared: true), or when they say they "
                           "ticked a box by mistake and confirm it when you read the item back (correction: true)."})
    prof.setdefault("language", ans.get("language", "en"))
    prof["age_band"] = core.AGE_BAND                    # never asked: the audience is 18 to 40 (00_MISSION.md)
    prof["screen"] = {"result": r["result"], "reasons": r["reasons"], "flags": r["flags"], "date": core.today(),
                      "items": ans.get("items", [])}
    write_profile(prof)
    c = gitops.commit("screen: " + r["result"])
    return out(dict(r, saved=c["status"]))


LEVELS = core.EXPERIENCE
LEGACY_LIKES = {"barbell": "heavy", "machines": "pump", "dumbbells": "pump", "circuits": "circuits", "classes": "circuits",
                "running": "running"}                 # old profiles said equipment words; they become activity words
ROUTINE_ACTIVITY = {"run_plan": ["running"], "classes": ["classes"], "strength_cardio": ["lifting", "running"]}
ROUTINE_ENJOY = {"ppl": ["pump"], "body_part": ["pump"], "run_plan": ["running"], "classes": ["circuits"],
                 "strength_cardio": ["heavy", "running"]}
ROUTINE_LEVEL = {"under_1m": "none", "1_3m": "novice", "3_12m": "novice", "over_1y": "intermediate"}


def _step_down(level):
    return LEVELS[max(0, LEVELS.index(level) - 1)]


def lifting_experience(p):
    """The single experience the session builder reads: lifting, the domain of nearly every bank row."""
    by = p.get("experience_by") or {}
    lift = by.get("lifting", "none")
    cf = by.get("crossfit", "none")
    if LEVELS.index(cf) > LEVELS.index(lift):        # CrossFit or HYROX lifts too, one step behind a lifter
        lift = max(lift, _step_down(cf), key=LEVELS.index)
    return lift


def bank_match(name, bank):
    """A typed exercise name to a bank id, by id or by name. None when it is their own exercise."""
    n = re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()
    for i, r in bank.items():
        if n in (i.replace("_", " "), re.sub(r"[^a-z0-9]+", " ", r["name"].lower()).strip()):
            return i
    return None


def interview_fields(p, ans):
    """The outcome, the routine, experience by activity, enjoy, pain status and recovery, turned into the fields
    the engine already reads (goal, goal2, experience, days, dislikes, limits[].exclude, no_impact). 02_INTERVIEW.md."""
    blend = ans.get("outcomes")
    if isinstance(blend, list) and blend and all(isinstance(o, dict) and o.get("id") in core.OUTCOMES for o in blend):
        tot = sum(float(o.get("share") or 0) for o in blend) or float(len(blend))
        for o in blend:
            o["share"] = round(float(o.get("share") or (tot / len(blend))) / tot, 2)
            if o.get("detail") not in core.OUTCOMES[o["id"]]:
                o["detail"] = core.OUTCOME_DEFAULT[o["id"]]
        blend.sort(key=lambda o: -o["share"])          # stable: on a tie the first tap stays the main outcome
        p["outcomes"] = blend
        p["outcome"], p["outcome_detail"] = blend[0]["id"], blend[0]["detail"]
        ans = dict(ans, outcome=p["outcome"], outcome_detail=p["outcome_detail"])
    oc = p.get("outcome")
    if oc in core.OUTCOMES and "goal" not in ans and ("outcome" in ans or "outcome_detail" in ans):
        det = p.get("outcome_detail") if p.get("outcome_detail") in core.OUTCOMES[oc] else core.OUTCOME_DEFAULT[oc]
        p["outcome_detail"] = det
        g1, g2 = core.OUTCOMES[oc][det]
        if "no_fat_loss_goal" in ((p.get("screen") or {}).get("flags") or []):
            g1, g2 = ("muscle", "health") if g1 == "fat_loss" else (g1, None if g2 == "fat_loss" else g2)
        for o in (p.get("outcomes") or [])[1:]:        # the blend: the next outcome's goal is the second goal (an add-on)
            og = core.OUTCOMES[o["id"]][o["detail"]][0]
            if og != g1:
                g2 = og
                break
        p["goal"] = g1
        if g2:
            p["goal2"] = g2
        else:
            p.pop("goal2", None)
    rt = p.get("current_routine")
    if p.get("mode") == "improve" and isinstance(rt, dict):
        if isinstance(rt.get("days"), int) and "days" not in ans:
            p["days"] = rt["days"]
        bank = core.load_bank()
        for label, exs in (rt.get("exercises") or {}).items():
            out = []
            for e in exs:
                if isinstance(e, dict):
                    out.append(e)
                    continue
                bid = e if e in bank else bank_match(e, bank)
                out.append({"id": bid} if bid else {"own": str(e)})
            rt["exercises"][label] = out
        by = dict(p.get("experience_by") or {})
        lvl = ROUTINE_LEVEL.get(rt.get("age"))
        for act in ROUTINE_ACTIVITY.get(rt.get("split"), ["lifting"]):
            if lvl and act not in by:
                by[act] = lvl
        if by:
            p["experience_by"] = by
        if not p.get("enjoys"):
            p["enjoys"] = list(ROUTINE_ENJOY.get(rt.get("split"), []))
    if p.get("experience_by"):
        by = {k: v for k, v in p["experience_by"].items() if v in LEVELS}
        if p.get("returning"):                          # coming back after a break: one step below, the logs correct it
            p["experience_was"] = dict(by)
            by = {k: _step_down(v) for k, v in by.items()}
        p["experience_by"] = by
        p["experience"] = lifting_experience(p)
    p.setdefault("experience", "none")
    if not p.get("enjoys") and p.get("likes"):
        p["enjoys"] = sorted({LEGACY_LIKES[x] for x in p["likes"] if x in LEGACY_LIKES})
    if p.get("kit_pref") == "free_weights" and "machines" not in p.get("dislikes", []):
        p["dislikes"] = list(p.get("dislikes", [])) + ["machines"]   # the session builder avoids machines when it can
    for lim in p.get("limits", []):
        st = lim.get("status")
        if st in core.LIMIT_STATUS:
            lim["exclude"] = st in ("now", "unchecked")  # mild and cleared: trained with care (01_SAFETY.md)
        if "impact" in (lim.get("triggers") or []):
            p["no_impact"] = True
    low = (p.get("sleep") == "under_6") + (p.get("stress") == "high")
    p["start_volume"] = "low" if low else "normal"
    return p


def normalise(ans, old):
    p = dict(old or {})
    for k, v in ans.items():
        p[k] = v
    p["age_band"] = core.AGE_BAND                       # fixed, whatever an old profile or an answer says
    p.setdefault("units", "kg")
    p.setdefault("paper", "A4")
    p.setdefault("audits", "full")
    p.setdefault("push", True)
    p.setdefault("limits", [])
    p.setdefault("skills", [])
    p.setdefault("likes", [])
    p.setdefault("dislikes", [])
    p.setdefault("numbers", {})
    p.setdefault("priority", [])
    if isinstance(p.get("days"), str) and p["days"].isdigit():
        p["days"] = int(p["days"])
    if isinstance(p.get("minutes"), str) and p["minutes"].isdigit():
        p["minutes"] = int(p["minutes"])
    if p.get("units") == "lb":
        for k, n in p.get("numbers", {}).items():
            if isinstance(n, dict) and n.get("lb") and not n.get("kg"):
                n["kg"] = round(n["lb"] / core.LB_PER_KG, 1)
        for k in ("dumbbells", "kettlebells"):          # the weights they own, said in pounds: kept as said, stored in kg
            if k in ans and isinstance(ans[k], list):
                p[k + "_lb"] = list(ans[k])
                p[k] = [core.lb_to_kg(x) for x in ans[k]]
    if not p.get("places"):
        p["places"] = {"main": {"type": "gym", "equipment": ["full_gym"]}}
    p.setdefault("default_place", list(p["places"])[0])
    p.setdefault("mode", "new")
    return interview_fields(p, ans)


def cmd_profile(args):
    ans = read_arg_json(args[0])
    old = core.profile() or {}
    if not old.get("screen"):
        return out({"ok": False, "error": "run the screen first (plan.py screen)"})
    if old["screen"].get("result") != "clear":
        return out({"ok": False, "error": "the screen is not clear: " + ", ".join(old["screen"].get("reasons", []))})
    prof = normalise(ans, old)
    errs = checks.check_profile(prof)
    if errs:
        return out({"ok": False, "errors": errs, "say": "Ask again only for the answers listed in errors."})
    write_profile(prof)
    c = gitops.commit("profile: %s · %sx%s min" % (prof["goal"], prof["days"], prof["minutes"]))
    return out({"ok": True, "saved": c["status"], "next": "plan.py match"})


# · match and choose

def cmd_match(args):
    prof = core.profile()
    if not prof or (prof.get("screen") or {}).get("result") != "clear" or not prof.get("goal"):
        return out({"ok": False, "error": "no clear screen and profile yet: run the screen and the interview first"})
    bank = core.load_bank()
    r = match_mod.match(prof, bank, build_mod.select)
    r["say"] = ("Tell them their plan: ONE plan, 'plan', in plain words from plan.plain (the headline, the week) and why it "
                "fits their answers. Never a method or school name, never a list of three: the runner-up stays with you. "
                "Say outcome_note, style_note, improve_note and dose_note if present. Then offer: start it, or 'not for me' "
                "with a reason (too long, too much running, I don't enjoy it, I can't do these days). "
                "If 'fallback' is present, say what single change would open a better fit.")
    return out(r)


MODULE_FOR_GOAL2 = {"run": "run-race", "functional": "conditioning", "hyrox": "hyrox-stations", "skills": "skill-blocks",
                    "health": "conditioning", "fat_loss": "conditioning", "independent": "balance"}


def age_num(b):
    return {"under_18": 17, "18_39": 30, "40_59": 50, "60_74": 67, "75_plus": 80}.get(b, 30)


def cmd_choose(args):
    pid = args[0]
    prof = core.profile()
    bank = core.load_bank()
    m = match_mod.match(prof, bank, build_mod.select)
    if pid in m["failed"]:
        return out({"ok": False, "error": "that program does not fit: " + "; ".join(m["failed"][pid])})
    prog = core.load_program(pid)
    mods = list(prog.get("modules", []))
    g2 = prof.get("goal2")
    extra_mods = []
    if g2 == "run" or (prof.get("goal") == "run" and prog["family"] not in ("run", "hybrid", "hyrox")):
        extra_mods.append("run-race")
    elif "running" in prof.get("likes", []) or g2 in ("health", "fat_loss"):
        extra_mods.append("easy-running")
    g1 = prof.get("goal")
    if g1 == "hyrox" and prog["family"] != "hyrox" and "hyrox-stations" not in mods:
        mods.append("hyrox-stations")
    if g1 == "skills" and "skill-blocks" not in mods:
        mods.append("skill-blocks")
    flags = set((prof.get("screen") or {}).get("flags", []))
    extra_lines = []
    if age_num(prof.get("age_band")) >= 60:
        extra_lines.append("Balance work is in every session. If you have fallen or are afraid of falling, a falls programme run by a "
                           "physiotherapist is the best thing you can add.")
    if "postpartum" in flags:
        extra_lines.append("No jumping or running until you tell me it feels fine. Leaking, heaviness or pelvic pain: see a pelvic health physio.")
    if prof.get("mode") == "improve":
        extra_lines.append("Once coaching inside your own routine lands, this plan keeps your split and your exercises.")
    seated_note = ("Everything stays seated. Some goals need standing moves; for those, an adaptive fitness professional is the right person."
                   if prof.get("position") == "seated" else None)
    if g2 and MODULE_FOR_GOAL2.get(g2) and MODULE_FOR_GOAL2[g2] not in ("run-race",) and MODULE_FOR_GOAL2[g2] not in mods:
        mods.append(MODULE_FOR_GOAL2[g2])
    if age_num(prof.get("age_band")) >= 60 and "balance" not in mods:
        mods.insert(0, "balance")
    mods = [x for x in mods if (core.MODULES / (x + ".md")).exists()]
    extra_mods = [x for x in extra_mods if (core.MODULES / (x + ".md")).exists()]
    days = prof["days"]
    used = min(days, prog["days"][1])
    extra = days - used if extra_mods else 0
    old_plan = core.plan() or {}
    old_state = core.state() or {}
    top = [t["id"] for t in m["top"] if t["id"] != pid]
    plan = {"program": pid, "program_name": prog["name"], "days": used + extra, "program_days": used,
            "modules": mods, "extra_modules": extra_mods if extra else [], "start": core.today(),
            "review": (datetime.date.today() + datetime.timedelta(weeks=prog.get("block_weeks", 4) + 1)).isoformat(),
            "runner_up": top[0] if top else None, "overrides": old_plan.get("overrides", []),
            "history": old_plan.get("history", []) + [{"date": core.today(), "program": pid}]}
    prose = ["# Your plan", "",
             "**Program:** %s (`doctrine/programs/%s.md`). It draws from %s. Evidence level %s." % (
                 prog["name"], pid, ", ".join(prog.get("draws_from", [])), prog.get("evidence")),
             "", "**Your week:** %d sessions, done in order, on whatever days suit you. %s" % (
                 used, ("Plus %d extra day(s): %s." % (extra, ", ".join(extra_mods))) if extra else
                 ("You said %d days; this program uses %d, so the other days are rest or an easy walk." % (days, used) if days > used else "")),
             "", "**Add-ons:** %s." % (", ".join(mods) or "none"),
             "", "**Review:** %s, at the end of the first block, or any time you say `/train goals`." % plan["review"]]
    if plan["runner_up"]:
        prose += ["", "**Runner-up:** `%s`." % plan["runner_up"]]
    core.write_json_block(core.PLAN, plan, "\n".join(prose))
    if old_state.get("program") == pid:
        st = dict(old_state)
        st["queue"] = []
        build_mod.refill(st, prog, plan)
        core.save_json(core.STATE, st)
        c = gitops.commit("goals: %s · same program, progress kept" % prof["goal"])
        return out({"ok": True, "program": pid, "days": plan["days"], "modules": mods, "extra_modules": plan["extra_modules"],
                    "kept_progress": True, "saved": c["status"], "next": "Say what changed in two lines, then offer the next session."})
    st = {"version": 1, "program": pid, "block": 1, "week": 1, "week_sessions": 0, "week_start": None, "queue": [],
          "slots": {}, "loads_by_ex": old_state.get("loads_by_ex", {}),
          "maxes_by_ex": old_state.get("maxes_by_ex", {}), "flags": {}, "pending": None,
          "last_session": old_state.get("last_session"), "sessions_done": old_state.get("sessions_done", 0)}
    build_mod.refill(st, prog, plan)
    core.save_json(core.STATE, st)
    c = gitops.commit("onboard: %s · %s · %dx%d min" % (prof["goal"], pid, plan["days"], prof["minutes"]))
    return out({"ok": True, "program": pid, "days": plan["days"], "modules": mods, "extra_modules": plan["extra_modules"],
                "saved": c["status"], "say_also": " ".join(x for x in [seated_note] + extra_lines if x) or None, "next": "Offer the first session now: the readiness turn, then plan.py build."})


# · build and render

def cmd_build(args):
    try:
        today = read_arg_json(args[0]) if args else {}
    except FileNotFoundError:
        return out({"ok": False, "error": "no readiness file: ask the four readiness questions and write me/today.json first"})
    prof, pl, st = core.profile(), core.plan(), core.state()
    if not (prof and pl and st):
        return out({"ok": False, "error": "no plan yet: run the interview first"})
    if st.get("pending"):
        return out({"ok": False, "error": "the last session (%s) is not logged yet: log it, or run plan.py log unreported" % st["pending"]})
    bank = core.load_bank()
    date = today.get("date") or core.today()
    s = build_mod.build(today, prof, pl, st, bank, date)
    core.SESSIONS.mkdir(exist_ok=True)
    title = re.sub(r"[/\\:*?\"<>|]", "", s["title"])
    path = core.SESSIONS / ("%s · %s.json" % (date, title))
    n = 2
    while path.exists():
        path = core.SESSIONS / ("%s · %s (%d).json" % (date, title, n))
        n += 1
    s["readiness"] = today
    core.save_json(path, s)
    if not s.get("rest_day"):
        st["pending"] = str(path.relative_to(core.ROOT))
    core.save_json(core.STATE, st)
    from sheet import session_seconds
    summary = [{"block": b["name"], "items": ["%s %s x %s %s" % (i["name"], i.get("sets", ""), i.get("reps", ""), i.get("load", "")) for i in b["items"]]}
               for b in s["blocks"]]
    return out({"ok": True, "session": str(path.relative_to(core.ROOT)), "title": s["title"], "minutes": round(session_seconds(s) / 60),
                "asked": s["minutes"], "rest_day": bool(s.get("rest_day")), "summary": summary, "notes": s.get("notes"),
                "language": s["language"],
                "next": "Translate only the words (title, why, cues, names, effort, notes, log lines, labels) into the person's language if it is not English, "
                        "keeping every number, then run the audits, then plan.py render."})


def cmd_render(args):
    import sheet
    p = pathlib.Path(args[0])
    if not p.is_absolute():
        p = core.ROOT / p
    r = sheet.render_file(p)
    if r.get("refused"):
        return out({"ok": False, "error": r["message"]})
    s = json.loads(p.read_text(encoding="utf-8"))
    c = gitops.commit("session: %s · %s" % (s.get("date"), s.get("title")))
    rel = p.with_suffix(".pdf").relative_to(core.ROOT)
    return out({"ok": True, "pdf": str(rel), "github_url": gitops.file_url(rel, None if c.get("pushed_main") or not c.get("pushed") else gitops.branch()) if c.get("pushed") or c.get("pushed_main") else None,
                "pages": r.get("pages"),
                "renderer": r.get("renderer"), "saved": c["status"], "warning": c.get("warning"),
                "next": "Send the PDF path and one line on what to beat. On a pushed copy, it is also on GitHub in sessions/."})


# · log

def cmd_log(args):
    prof, pl, st = core.profile(), core.plan(), core.state()
    if not st or not st.get("pending"):
        return out({"ok": False, "error": "no session waiting to be logged"})
    sp = core.ROOT / st["pending"]
    session = json.loads(sp.read_text(encoding="utf-8"))
    bank = core.load_bank()
    prog = core.load_program(pl["program"])
    if args and args[0] == "unreported":
        report = {"as_written": False, "unreported": True}
    else:
        report = read_arg_json(args[0])
        need = logbook.needs(session, report)
        if need:
            return out({"ok": False, "needs": need, "optional": logbook.optional_asks(session, report),
                        "say": "Ask these in one short turn (and, in the same line, roughly what they used on the 'optional' ones, "
                               "if they remember), add them to results, run log again."})
    done, hard = ([], {}) if report.get("unreported") else logbook.apply(session, report, prof, st, bank)
    keys = {it["_slot"]["key"] for b in session["blocks"] for it in b["items"] if it.get("_slot")}
    unknown = [k for k in (report.get("results") or {}) if k not in keys]
    date = report.get("date") or session.get("date") or core.today()
    sc = logbook.score_text(session, done, prof.get("units", "kg"))
    line = {"date": date, "session": st["pending"], "title": session.get("title"), "session_id": session.get("session_id"),
            "program": session.get("program"), "mode": session.get("mode"), "level": session.get("level"),
            "energy": (session.get("readiness") or {}).get("energy"), "felt": report.get("felt"),
            "pain": report.get("pain"), "notes": report.get("notes"), "score": sc or ("unreported" if report.get("unreported") else ""),
            "unreported": bool(report.get("unreported")), "done": done, "hard_sets": hard}
    if report.get("pain"):
        prof_l = prof.setdefault("limits", [])
        for pn in report["pain"]:
            if pn.get("score", 0) > 3 or pn.get("sharp"):
                ex = [l for l in prof_l if l.get("region") == pn["region"]]
                if ex:
                    ex[0].update({"exclude": True, "note": (ex[0].get("note", "") + " · pain %s on %s, until cleared" % (pn.get("score"), date)).strip(" ·")})
                else:
                    prof_l.append({"region": pn["region"], "note": "reported %s, until cleared" % date, "exclude": True})
        write_profile(prof)
    if unknown:
        line["notes"] = ((line.get("notes") or "") + " Also did, not in the plan: " + ", ".join(unknown)).strip()
    with open(core.LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    st["pending"] = None
    events = logbook.advance(st, pl, prog, session, date, counted=not report.get("unreported"))
    log = core.read_log()
    if logbook.deload_triggers(log, st):
        events.append("early_deload")
    core.save_json(core.STATE, st)
    core.LOGMD.write_text(logbook.render_logmd(log, prof), encoding="utf-8")
    nexts = []
    for d in done:
        a = d.get("after") or {}
        if a.get("load"):
            nexts.append("%s: next time %s" % (bank.get(d["ex"], {}).get("name", d["ex"]), core.fmt_load(a["load"], prof.get("units", "kg"))))
        elif a.get("tm"):
            nexts.append("%s: training max %s, wave %s" % (bank.get(d["ex"], {}).get("name", d["ex"]), core.fmt_load(a["tm"], prof.get("units", "kg")), a.get("wave")))
        if a.get("note"):
            nexts.append(a["note"])
    c = gitops.commit("log: %s · %s · %s" % (date, session.get("title"), sc or "done"))
    return out({"ok": True, "score": sc, "events": events, "next_loads": nexts, "not_in_session": unknown, "saved": c["status"], "warning": c.get("warning"),
                "say": "Read back the log in one line, then the one or two loads that moved. If events has week_closed, block_closed "
                       "or early_deload, say it in one line and run the cycle audit."})


# · week, rebuild, commit, visibility, update, forget

TARGETS = {"chest": (10, 20), "back": (10, 20), "shoulders": (6, 16), "quads": (10, 20), "glutes": (8, 20),
           "hamstrings": (6, 16), "biceps": (4, 14), "triceps": (4, 14), "calves": (0, 12), "core": (4, 12)}


def cmd_week(args):
    pl, st = core.plan(), core.state()
    log = core.read_log()
    since = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    last7 = [l for l in log if l["date"] > since]
    sets = {}
    for l in last7:
        for g, n in (l.get("hard_sets") or {}).items():
            sets[g] = sets.get(g, 0) + n
    return out({"block": st.get("block") if st else None, "week": st.get("week") if st else None,
                "done_this_week": st.get("week_sessions") if st else 0, "planned": pl.get("days") if pl else None,
                "queue": (st or {}).get("queue"), "last_7_days": [{"date": l["date"], "title": l.get("title"), "score": l.get("score")} for l in last7],
                "hard_sets_7d": {g: {"done": round(v, 1), "usual_range": TARGETS.get(g)} for g, v in sorted(sets.items())},
                "note": "usual_range is the 10 to 20 sets research band (Schoenfeld 2017, Pelland) for the main muscles; it is a guide, not a target for every program"})


def cmd_rebuild(args):
    prof, pl = core.profile(), core.plan()
    prog = core.load_program(pl["program"])
    bank = core.load_bank()
    st = {"version": 1, "program": pl["program"], "block": 1, "week": 1, "week_sessions": 0, "week_start": None, "queue": [],
          "slots": {}, "loads_by_ex": {}, "flags": {}, "pending": None, "last_session": None, "sessions_done": 0}
    old = core.state() or {}
    st["loads_by_ex"] = dict(old.get("loads_by_ex") or {})
    st["maxes_by_ex"] = dict(old.get("maxes_by_ex") or {})
    build_mod.refill(st, prog, pl)
    for l in core.read_log():
        if l.get("program") != pl["program"]:
            continue
        sp = core.ROOT / l["session"]
        if not sp.exists():
            continue
        session = json.loads(sp.read_text(encoding="utf-8"))
        if not st.get("queue"):
            build_mod.refill(st, prog, pl)
        if not l.get("unreported"):
            results = {d["key"]: d["result"] for d in l.get("done", []) if d.get("result")}
            skipped = [d["key"] for d in l.get("done", []) if d.get("skipped")]
            logbook.apply(session, {"as_written": False, "results": results, "skipped": skipped, "loads_in_kg": True}, prof, st, bank)
        if session.get("session_id") in st["queue"]:
            session["_queue_index"] = st["queue"].index(session["session_id"])
        logbook.advance(st, pl, prog, session, l["date"])
    core.save_json(core.STATE, st)
    c = gitops.commit("rebuild: state from the log")
    return out({"ok": True, "block": st["block"], "week": st["week"], "saved": c["status"]})


def cmd_review(args):
    """The cycle auditor's verdict, in two lines, kept in me/PLAN.md."""
    pl, st = core.plan(), core.state()
    pl.setdefault("reviews", []).append({"date": core.today(), "block": (st or {}).get("block"), "week": (st or {}).get("week"),
                                        "note": " ".join(args)})
    txt = core.PLAN.read_text(encoding="utf-8").split("## The data")[0].rstrip()
    if "## Reviews" not in txt:
        txt += "\n\n## Reviews"
    txt += "\n- %s · block %s: %s" % (core.today(), (st or {}).get("block"), " ".join(args))
    core.write_json_block(core.PLAN, pl, txt)
    return out({"ok": True, "saved": gitops.commit("review: block %s" % (st or {}).get("block"))["status"]})


def cmd_discard(args):
    st = core.state()
    if not st or not st.get("pending"):
        return out({"ok": False, "error": "no session waiting"})
    p = core.ROOT / st["pending"]
    for ext in (".json", ".html", ".pdf"):
        q = p.with_suffix(ext)
        if q.exists():
            q.unlink()
    st["pending"] = None
    core.save_json(core.STATE, st)
    c = gitops.commit("session: discarded before training, rebuilt")
    return out({"ok": True, "saved": c["status"], "next": "Fix me/today.json if needed and run plan.py build again."})


def cmd_commit(args):
    return out(gitops.commit(args[0] if args else "trainer: save"))


def cmd_visibility(args):
    v = gitops.visibility()
    return out({"visibility": v, "say": "If public: tell them anyone can read their health answers and to set the repo to Private in Settings, General, Danger zone."
                if v == "public" else ""})


SHIPPED = [l.strip() for l in (HERE / "SHIPPED").read_text().splitlines() if l.strip() and not l.startswith("#")] \
    if (HERE / "SHIPPED").exists() else []


def cmd_update(args):
    g = gitops.git
    if "upstream" not in g("remote").stdout.split():
        g("remote", "add", "upstream", UPSTREAM)
    f = g("fetch", "upstream", "main")
    if f.returncode:
        return out({"ok": False, "error": "could not reach the template on GitHub: " + f.stderr.strip()[:200]})
    mine = (core.ROOT / "VERSION").read_text().strip() if (core.ROOT / "VERSION").exists() else "?"
    theirs = g("show", "upstream/main:VERSION").stdout.strip()
    changes = g("show", "upstream/main:CHANGELOG.md").stdout
    if not args or args[0] != "yes":
        return out({"current": mine, "available": theirs, "changelog_head": changes[:1500],
                    "say": "Explain the changes in plain words. If they say yes: plan.py update yes. Their me/ and sessions/ are never touched."})
    up = set(g("ls-tree", "-r", "-" * 2 + "name-only", "upstream/main").stdout.split("\n"))
    here = set(g("ls-files").stdout.split("\n"))
    shipped = lambda p: any(p == s or p.startswith(s.rstrip("/") + "/") for s in SHIPPED)
    for p in sorted(up):
        if p and shipped(p):
            g("checkout", "upstream/main", p)
    removed = [p for p in here if p and shipped(p) and p not in up]
    for p in removed:
        g("rm", "-q", p)
    g("add", "-A", *SHIPPED)
    r = g("commit", "-m", "update: personal trainer " + theirs)
    if gitops.has_remote():
        g("push", "origin", "HEAD")
    return out({"ok": r.returncode == 0, "version": theirs, "removed": removed})


def cmd_forget(args):
    if not args or args[0] != "yes":
        return out({"say": "Git keeps history, so deleting files does not erase them. The only full erase: delete this repository on GitHub "
                           "(Settings, General, Danger zone, Delete) and delete this folder on your computer. I can wipe me/ and sessions/ "
                           "here now (say 'forget yes'), but the history stays until the repo is deleted. A fresh copy: "
                           + UPSTREAM + "/generate"})
    for p in core.ME.glob("*"):
        if p.name in ("README.md",):
            continue
        p.unlink()
    for p in core.SESSIONS.glob("*"):
        if p.name != "README.md":
            p.unlink()
    (core.ME / "PROFILE.md").write_text("# Your profile\n\n_Empty. Type /train to start._\n", encoding="utf-8")
    (core.ME / "PLAN.md").write_text("# Your plan\n\n_Empty until the interview._\n", encoding="utf-8")
    c = gitops.commit("forget: me/ and sessions/ wiped", push=True)
    return out({"ok": True, "saved": c["status"], "say": "Wiped here. To erase the history too, delete the repository on GitHub."})


CMDS = {"status": cmd_status, "screen": cmd_screen, "profile": cmd_profile, "match": cmd_match, "choose": cmd_choose,
        "build": cmd_build, "render": cmd_render, "log": cmd_log, "week": cmd_week, "rebuild": cmd_rebuild,
        "commit": cmd_commit, "discard": cmd_discard, "review": cmd_review, "visibility": cmd_visibility, "update": cmd_update, "forget": cmd_forget}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__)
        sys.exit(1)
    sys.exit(CMDS[sys.argv[1]](sys.argv[2:]) or 0)
