# 08 · Session review, a coach reads what the engine serves

_13 nov 2026. Twelve people run through the real chain (screen, profile, match, choose the recommended program, then a full first week of builds, each logged as done so progression moves). Every line quoted below is from a session file the engine wrote. The engine was not edited. Driver and raw output: `/private/tmp/claude-502/-Users-AC-Desktop-matier/1acef9e8-21cd-4c11-9436-677c4987bda7/scratchpad/coachreview/drive.py`, one `.txt` and one `.json` per person beside it._

**How it was run.** Readiness every time: energy 7, no pain, the profile minutes. First outings logged at a plausible found weight (barbell 40, dumbbell 10, kettlebell 12, cable 20). Sessions built = max(3, days), so a 4 or 5 day program shows its whole first week. Sets per muscle count a primary muscle as 1 set and a secondary as half.

**The short verdict.** The core lifting templates are sound: exercise order, rep ranges, rest and the found-weight first session are what a good coach writes, and the 60+ and postpartum safety filters hold. What breaks is everything around the template: the add-on that serves the second goal is the first thing the clock cuts, a single limit can push someone off strength training entirely, the minutes are only ever cut and never filled, and the stated priority barely moves the week.


## Part 1 · persona by persona

### 1 · 25, aesthetics, 4 days x 60, full gym, priority arms (intermediate)

| | |
|:-|:-|
| got | `muscle-upperlower-4` + core finisher. UA bench, chest supported row, OHP, pulldown, laterals, cable overhead extension, incline curl. LA squat, RDL, leg ext, leg curl, calves. UB incline, chin-up, cable row, fly, rear delt, lateral, skull crusher, hammer curl. LB leg press, hip thrust, Bulgarian split squat, leg curl, seated calf. |
| verdict | **Good program, small leaks.** Order, 6 to 10 on compounds at 120 to 150 s, 10 to 15 on isolations at 60 s, first-outing wording: all correct. Priority arms did work: tri and curl slots went 2 to 3 sets, 12 direct arm sets in the week. |
| problems | (a) Chest 8 sets in the week (bench 3, incline 3, fly 2), the low end for a muscle goal, while core gets 24 sets from the finisher on all four days. (b) Lower days run short: LA 49 min, LB 50 min of 60, while UA is 61. (c) S2 `Calf raise 3x 10-15 @ bodyweight` and S4 `Bulgarian split squat 3x 10-15 @ bodyweight` for an intermediate in a full gym: unloaded, so they stop working within weeks. (d) Warm-up `Band shoulder dislocate` and `Ankle rocks` before every session, leg day or not. |

### 2 · the owner: advanced, strength first, HYROX second, 3 x 45, priority arms

| | |
|:-|:-|
| got | `strength-531-bbb-4` on 3 days, modules core + hyrox-stations. S1 squat 5/3/1 (92.5 / 107.5 / 122.5 kg) + 5x10 squat + chin-up 5 sets. S2 bench 67.5 / 77.5 / 87.5 + 5x10 bench + DB row 4. S3 deadlift 120 / 140 / 157.5 + 5x10 deadlift + chin-up 5. |
| verdict | **Fails both stated asks.** The strength part is a correct 5/3/1 BBB with a sensible training max (squat TM 145 from 140x5), and the 4-day rotation on 3 days does not drop a lift (Press is next in the queue). But the second goal and the priority are absent. |
| problems | (a) **HYROX second goal: 0 minutes in 3 sessions.** Notes on all three: `finisher dropped to fit your minutes`. The dropped finisher is hyrox-stations; the core finisher survives. No run, no station, no erg in the week. (b) **Priority arms: 0 direct arm sets in week 1.** The program has no arm slot and the priority rule only adds sets to an existing one. (c) `5x 10 @ (blank) · 50 to 60% of your training max, same lift. Load it yourself` while the engine knows the TM is 145: it could print 72.5 to 87.5 kg. (d) `3x 5/5/5 (stop with 1 left)` printed beside `last set as many clean reps as you have`: energy 7, the most common answer, caps the PR set, which is the set 5/3/1 progresses on. (e) "Boring But Big", "training max", "5/5/5" all on the sheet. |

### 3 · first marathon, 4 days x 60, park, can run 40 min (novice)

| | |
|:-|:-|
| got | `run-base-3to5` + mobility. E 40 min easy, Q `25 min easy plus 6 x 20 s strides`, E 40 min, L `Express · 20 min easy run`. |
| verdict | **Unsafe to call this a marathon plan, and the long run is broken.** Doctrine (`00_MISSION.md`) says marathon is not served; the engine accepted the event and wrote `18 weeks to first marathon` on every sheet. |
| problems | (a) **The long run is the shortest run of the week: 20 min.** The L slot asked 60 min (1.5 x 40); 60 + 8 min warm-up + mobility overflowed 60, so `build()` switched to the program's express session. Total week 125 min with no long run. (b) Q session titled `For time, cap 45 min` for an easy run with strides, effort text `Threshold about 10% of your week, intervals at most 8%`: wrong format and jargon. `Main job: For time, cap 45 min` in the why line. (c) Mobility `Cat cow · wide grip, slow, arms straight`: the band dislocate's effort line printed on a substitute. (d) No strength work at all for a runner. |

### 4 · HYROX competitor, 5 days x 60, full gym + sled + ski + rower, event in 15 weeks (intermediate)

| | |
|:-|:-|
| got | `hyrox-prep-4` + mobility + hyrox-stations. S lower strength (back squat 4x5-8, sandbag lunge) + station practice + a station piece. E easy run 30 + a for-time station piece. I 6 x 1 km at race pace. R easy run 25 + a for-time station piece. C 4 x (1 km run + 500 m ski) for time. |
| verdict | **Right ingredients, wrong dose distribution.** Run volume, compromised running and stations are what HYROX needs. But easy days are not easy and strength is thin. |
| problems | (a) **Both easy runs end with a for-time piece:** E `20 m Burpee broad jump · 250 m Rowing machine` for time, R `100 m Farmer carry · 25 m Sandbag lunge · 25 Wall ball` for time. Five sessions, five hard efforts in week 1. (b) S1 carries two station blocks back to back (`Station practice` with sled push and wall ball, then `HYROX station piece` with sled push, sled pull, ski): sled push twice. (c) One strength session a week, squat and lunge only: no hinge, no upper-body pull or push for a race with sled pull, rowing, ski and carries. (d) `Sandbag lunge 3x 8-12 @ bodyweight`: the sandbag is the load. (e) `see the hyrox-stations module for your division` and `race weight from the table in this module`: the client never sees a module. (f) Mobility finisher dropped on I and C. |

### 5 · busy parent, 3 x 20 min, home, bodyweight only (never trained)

| | |
|:-|:-|
| got | `home-fullbody-2to4`, all three sessions `Express · Squat · Push · Row circuit`: split squat, push-up, door frame row, 2 rounds. |
| verdict | **Safe, too little, and the same session three times.** Progression is clean (`8+ a set` then 9+ then 10+). |
| problems | (a) Built 15 min of the 20 asked, every session. (b) A, B and C are identical: the express session replaces the rotation. (c) No hinge or bridge in the week: posterior chain 0 sets. (d) 6 working sets a session. Three rounds fit in 20 minutes. (e) "Express" in the title the client reads. |

### 6 · 55, beginner, home, dumbbells 4 to 12 kg (health)

| | |
|:-|:-|
| got | `health-baseline-2to3`: A incline push-up + DB row superset, goblet squat, DB RDL, Pallof press, 15 min brisk walk. B DB shoulder press + band pulldown, reverse lunge, glute bridge, dead bug, walk. |
| verdict | **The best-built week of the twelve.** Balanced push, pull, squat, hinge; 2 sets at 2 to 3 in reserve for week 1; walk included; loads from the found weight in S3. |
| problems | (a) Mobility add-on dropped every session. (b) `Pallof press · find your weight` with a band at home, then printed `@ 20 kg` in S3: a band has no kilos (`pallof_press` is load type `cable`). |

### 7 · 70, independence goal, basic gym (never trained)

| | |
|:-|:-|
| got | `older-strong-3` + balance. Each session: a Balance block, a Strength block (sit to stand or goblet squat or step-up, incline push-up, cable row or DB press, pulldown), a carry, then a Balance finisher. Falls line said at choose. |
| verdict | **Right content, balance served twice.** Power cue (`lift fast, lower slow`), carries, floor get-up: what the guidelines ask for. |
| problems | (a) **The same balance moves twice in one session:** S1 main `Single leg stand · Heel to toe walk · Clock reach`, finisher `Single leg stand · Heel to toe walk · Clock reach`. About 12 of 45 minutes on balance, strength gets 2 sets a move. (b) `Main job: Single leg stand, Heel to toe walk, Clock reach, Sit to stand, Incline push-up, Seated cable row` in the why line. (c) `Farmer carry 2x 20-40 m @ (blank)`: no weight and no first-outing line. |

### 8 · postpartum, cleared by her midwife, home dumbbells 6 and 10 kg, 3 x 30, health then fat loss

| | |
|:-|:-|
| got | `home-fullbody-2to4` + core + conditioning. A goblet squat, floor press, DB row, DB RDL, lateral raise. B reverse lunge, DB shoulder press, kettlebell row, glute bridge. C heel-elevated goblet squat, floor press, DB row, slider leg curl. Pelvic health line said. No impact anywhere. |
| verdict | **Safe, but the two things she most needs are cut.** |
| problems | (a) **Core add-on: 0 of 3 sessions. Conditioning (her fat-loss goal): 0 of 3.** Notes: `finisher dropped to fit your minutes finisher dropped to fit your minutes`. After a birth the trunk and pelvic floor work is the one block that should never go. (b) `Kettlebell row` for someone who owns no kettlebell; it then sits on a kettlebell grid (12 kg) she cannot load. (c) Floor press drops from the 10 kg she used in A to `6 kg` in C: the second slot of the same lift is re-seeded with a discount. (d) Accessories also cut: `Overhead dumbbell triceps extension dropped`, `Single leg calf raise dropped`. |

### 9 · desk worker, 40s, shoulder pain now (excluded), full gym, health

| | |
|:-|:-|
| got | Screen item 6 stopped, then cleared. Match returned **one** program: `run-c25k-3`. Three sessions `8 x (1 min run, 1:30 walk)`, 17 min each of 45 asked. |
| verdict | **The worst result of the twelve.** A person with a sore shoulder, in a full gym, asking to feel healthier, gets no strength training at all and is sent jogging. |
| problems | (a) **Every strength and health program failed the match** because one pressing slot cannot be filled: `can't fill 'hpush' in session A`, `can't fill 'push' in session A`, `can't fill 'bench' in session A`. Legs, hinge, rows, carries were all available. (b) **Safety: `Band shoulder dislocate` served twice a session (warm-up and mobility finisher) to an excluded shoulder.** The bank row has an empty `regions` field, so the exclusion cannot see it. (c) 17 of 45 minutes. |

### 10 · climber, strength first, bodyweight skills second, 3 x 60, priority back (intermediate, has a pull-up)

| | |
|:-|:-|
| got | `strength-531-beginners-3` + skill-blocks. A squat + bench 5/3/1 + FSL 5x5 each, dip, chin-up 4, Bulgarian. B deadlift + press + FSL, dip, inverted row 4, ab wheel. C bench + squat + FSL, dip. |
| verdict | **Wrong shape for a climber who asked for back.** |
| problems | (a) **Push to pull about 2.5 to 1 with priority back:** in 3 sessions triceps 29, chest 23 sets vs lats 9.5. Dips every session. (b) **The priority item was cut:** S3 notes `Chin-up dropped to fit your minutes` while `Dip 3x` stays. (c) Skill-blocks (his second goal): dropped every session. (d) S1 and S2 main lifts `1x 5 @ (blank)` then `5x 5 · Load it yourself`; by S3 bench and squat sit at 25 / 30 / 32.5 kg after he found 40 kg, which reads as a regression to the client. (e) "First set last" as a block name. |

### 11 · powerlifter, 4 x 75, full gym, meet in 12 weeks (intermediate, knows his numbers)

| | |
|:-|:-|
| got | `strength-rpe-4`. Upper A bench top triple + back-offs, OHP, row, skull crusher. Lower A squat top triple + back-offs, RDL, Bulgarian, ab wheel. Upper B bench top 5, close grip, chin-up, lateral. Lower B deadlift top triple, front squat, leg curl, calf. |
| verdict | **Correct loads, half a workout.** Top sets from his numbers are right (squat 135 for 3 at 2 left from 160x3). |
| problems | (a) **40 to 41 min built of 75 asked, all four sessions.** (b) Squat 4 work sets and deadlift 4 work sets in the week; an intermediate lifter 12 weeks out wants roughly double. (c) No meet logic: the event date prints (`12 weeks to regional meet`) and changes nothing. (d) `Bulgarian split squat @ bodyweight` and `Calf raise @ bodyweight` for this lifter. |

### 12 · fat loss, 40s, dislikes gyms, outdoors in a park, likes running (never trained)

| | |
|:-|:-|
| got | `home-fullbody-2to4` + core. Split squat, push-up, inverted row, single-leg RDL; reverse lunge, pike push-up, incline inverted row, glute bridge; split squat, decline push-up, inverted row, slider leg curl. |
| verdict | **A decent strength circuit, but not a fat-loss week and not what she likes.** |
| problems | (a) **0 minutes of running or conditioning** for a fat-loss goal from someone who said she likes running. (b) `Inverted row · each arm on one-arm rows`, `Side plank 3x 8-12 · each side, no twist`: effort lines written for other exercises, and side plank in reps. (c) Notes `'lateral' left out today: nothing in the bank fits your equipment and limits`, `'curl' left out`, `'tri' left out`, `'rear' left out`: internal slot keys and "the bank" on the client sheet. (d) Core finisher dropped in S3. |


## Part 2 · root causes, ranked by how much they hurt results

### 1 · The add-on that serves the second goal is the first thing the clock cuts
**Where:** `engine/build.py` `fit()` cuts `fin[-1]` (any non-balance finisher) before any accessory set; `engine/plan.py` `cmd_choose` appends the goal2 module last, so it is `fin[-1]`. `doctrine/06_BUILD.md` "The minutes are a ceiling" lists optional finishers first.
**Hit:** owner HYROX 0 of 3, climber skills 0 of 3, postpartum core 0 of 3 and conditioning 0 of 3, 55 year old mobility 0 of 3, HYROX mobility 2 of 5.
**Fix:** split add-ons into *goal* modules (goal2 module, core after a birth, balance from 60) and *nice-to-have* (mobility, a generic core finisher). Goal modules are cut last, after accessory sets and whole accessory blocks, and shrink to a minimum dose (like balance to 4 min) rather than vanish. At `choose`, if the program's normal session plus the goal module cannot fit the minutes, say so once ("45 minutes holds your strength work; your HYROX work needs 15 more minutes or a fourth day") and offer the module as an extra day.

### 2 · One limit can throw a person off strength training entirely
**Where:** `engine/match.py` `filters()`, the "can its main blocks actually be filled" pass: one unfillable main slot fails the whole program.
**Hit:** desk worker with a shoulder: every strength and health program failed on a pressing slot, C25K was the only option, 17 min of 45.
**Fix:** at match, a main slot that fails only because of a limit region should cost score, not fail the program, since `build()` already drops such a slot with a note. Fail only when more than half the main slots in a session go. Add a doctrine line in `03_MATRIX.md`: a limit removes moves, never the goal.

### 3 · Safety: rows with empty `regions` pass every exclusion
**Where:** `doctrine/exercises/bank.csv` (`band_shoulder_dislocate` regions empty, and the other mobility rows); `engine/build.py` `allowed()` trusts `regions`.
**Hit:** an excluded, painful shoulder got band dislocates twice a session.
**Fix:** tag `band_shoulder_dislocate` with `shoulder`, then audit every row whose muscles include delts, upper back, lower back or calves for an empty `regions`. Add a rule to `engine/checks.py`: no row may have empty `regions` unless it is tagged `region_free` on purpose.

### 4 · The minutes are only ever cut, never filled
**Where:** `doctrine/06_BUILD.md` "The minutes are a ceiling"; `engine/build.py` `fit()` has no fill pass.
**Hit:** powerlifter 40 of 75 four times, desk worker 17 of 45, parent 15 of 20, aesthetics lower days 49 and 50 of 60.
**Fix:** add a fill step after `fit()`: while more than 10 minutes are spare, add back cut add-ons, then one set to priority and main-muscle accessories up to the program's set ceiling (or the meso's `extra_sets_by_week` early). The doctrine line becomes "a ceiling and a target". At the least the sheet says "35 spare minutes: this program is short on purpose" so nobody thinks it is a bug.

### 5 · The long run collapses to a 20 minute express run
**Where:** `engine/build.py` `build()` retries with `_express` whenever the normal session is over the minutes; `doctrine/programs/run-base-3to5.md` express is a 20 min easy run.
**Hit:** the marathon runner's long run was 20 min, shorter than both easy runs. It hits any runner whose long run plus warm-up passes the minutes, half-marathon runners included.
**Fix:** for `run_volume` slots, cap the run at the minutes minus the warm-up instead of switching to express, and never prescribe the long run below the week's easy run. Add a sheet line: "your long run wants about 60 minutes: put it on the day you have time".

### 6 · Priority is weak and unprotected
**Where:** `engine/build.py` lines after the block loop (`pri`, `added < 2`): +1 set to at most two accessory items that already hit the muscle. No rule in any doctrine file; `02_INTERVIEW.md` only names the field.
**Hit:** owner arms 0 direct sets; climber back priority lost its chin-up to `fit()` while dips stayed; aesthetics got +4 arm sets a week, which is the best case.
**Fix:** write the rule in `06_BUILD.md`: a priority gets 4 to 6 extra direct sets a week. If no accessory slot hits it, add one from the bank (arms: a curl and a triceps move; back: a row or pulldown). Mark priority items protected in `fit()` so they are the last accessory cut.

### 7 · Fat loss and "likes running" get no conditioning
**Where:** `engine/plan.py` `MODULE_FOR_GOAL2` applies only to `goal2`; `easy-running` is added only as an extra day when days exceed the program's days.
**Hit:** fat-loss runner in the park: 0 minutes of running or conditioning in the week.
**Fix:** goal `fat_loss` (as goal 1 or 2) adds `conditioning` or `easy-running` as a goal module (protected, see 1). `likes: running` adds a short easy run as a finisher when no extra day exists.

### 8 · Modules stack on programs that already contain them
**Where:** `engine/plan.py` `cmd_choose` inserts `balance` for 60+ without looking at the program; `doctrine/programs/hyrox-prep-4.md` lists `hyrox-stations` although its S session already has a station block; the station piece has no rule against easy days.
**Hit:** 70 year old does the same three balance moves twice a session; HYROX athlete gets two sled blocks in S1 and a for-time piece after both easy runs.
**Fix:** skip a module when the program has a block of the same kind (balance, stations). Tag sessions `easy` in program files and forbid hard finishers on them; the hyrox-stations piece then lands on S and C only.

### 9 · The load type belongs to the bank row, not to the kit in hand
**Where:** `bank.csv` `load_type` (`kb_row` kettlebell, `pallof_press` cable, `sandbag_lunge` bodyweight); `engine/build.py` `load_ctx()`.
**Hit:** kettlebell row and a 12 kg grid for a dumbbell-only mother; Pallof press with a band printed at 20 kg; sandbag lunge printed "bodyweight"; unloaded Bulgarian and calf raises for intermediates and the powerlifter in full gyms.
**Fix:** when a row allows several kits, take the load type and grid from the kit the person has (dumbbell grid at home); prefer `band_pallof_press` when the kit is a band; give `sandbag_lunge` a load. For intermediate and up with loads available, `_select` should prefer the loadable variant of a pattern.

### 10 · The slot's effort line survives an exercise swap
**Where:** `engine/build.py` `slot_item()`: `effort = slot.get("effort")` whatever exercise `select()` picked.
**Hit:** Cat cow told "wide grip, arms straight", inverted row "each arm on one-arm rows", side plank prescribed in reps.
**Fix:** keep the slot's effort only when the picked exercise is the slot's first `prefer`; otherwise use a generic effort plus the row's own cue, and print time-based rows in seconds.

### 11 · Jargon and internal references reach the client
**Where:** program and module files (`run-base-3to5.md`, `hyrox-prep-4.md`, `hyrox-stations.md`, the 5/3/1 files), `piece_item()` headings, `build()` notes and `why`.
**Hit:** "For time, cap 45 min" on easy runs and intervals, "Boring But Big", "First set last", "5/5/5", "Express ·", "see the hyrox-stations module", "nothing in the bank fits", slot keys `'lateral'`, `'curl'`, "Threshold about 10% of your week". The skill tells the coach to rewrite slot keys, but an English-speaking user gets the raw note when the coach does not.
**Fix:** one plain-words pass on those files; `piece_item()` uses "Intervals" or "Run" for run formats; notes name the exercise ("lateral raises left out: no kit for them today"); the why line lists at most the first two main lifts.

### 12 · 5/3/1 details that break the method
**Where:** `engine/progress.py` `tm_prescribe` (`cap_amrap` at energy 6 to 7); the BBB and FSL slots in the 5/3/1 program files.
**Hit:** the default readiness answer turns the PR set into "stop with 1 left", next to text saying "as many as you have"; supplemental sets say "Load it yourself" while the TM is known.
**Fix:** cap the PR set only at energy 5 or less; compute the supplemental weight from the TM and print it.

### 13 · A second slot of the same lift is re-seeded with a discount
**Where:** `engine/build.py` `slot_item()`: a carried load is set, then `seed_from_numbers()` with `maxes_by_ex` overwrites it.
**Hit:** postpartum floor press 10 kg in session A, 6 kg in session C.
**Fix:** when a carried load exists, convert it to the new rep range without the 10 percent discount and skip the seed.

### 14 · Scope is said by the coach, never held by the engine
**Where:** `engine/checks.py` `check_profile`; `doctrine/00_MISSION.md` "marathon and longer" not served.
**Hit:** the engine accepted "first marathon" and printed the countdown on every sheet; the powerlifter's meet date prints and changes nothing.
**Fix:** `profile` returns a `scope` warning when the event names a marathon or longer, which the coach must say. For a meet date, either a simple peak rule in the RPE program or a line saying the date is not used for planning.

### 15 · Weekly balance is never checked
**Where:** nothing in `engine/` sums sets per muscle or per pattern across the rotation.
**Hit:** climber push to pull 2.5 to 1; HYROX athlete no hinge and no upper body; parent no hinge; aesthetics chest 8 a week.
**Fix:** a check in `checks.py` (or a test) that sums a program's rotation by pattern and flags pull below push, no hinge, or a goal's key muscle under 10 sets for `muscle`. Fix the program files it flags.

### 16 · The warm-up does not read the session
**Where:** `engine/build.py` `warmup()`: mobility rows with empty `regions` tie, then sort by id.
**Hit:** `Ankle rocks` and `Band shoulder dislocate` before every session, bench day or long run.
**Fix:** fixed by 3 (regions on every row) plus a sort that prefers the main lift's pattern.


## What held up

The safety screen and its holds, the no-impact filter after a birth, the 60+ falls line, the found-weight first session with two sets for beginners, double progression targets climbing one rep a session, training maxes and RPE top sets from known numbers, and a 4-day rotation run on 3 days that keeps every lift in turn.
