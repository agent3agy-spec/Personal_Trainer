# 09 · Improve mode · coaching inside a routine they already run

_Design note, 13 nov 2026. Not built. It turns the owner's walkthrough note (section "3 to 5") and Part 3b of `06_interview_audit.md` into an exact engine plan: what the person types, the file it becomes, what the coach changes and never changes, the code changes file by file, the tests, and the risks. Read against the engine as it stands at VERSION in this repo: `engine/plan.py`, `core.py`, `build.py`, `progress.py`, `logbook.py`, `match.py`, `sheet.py`, `checks.py`._

## How to read the marks

- **[read]** seen in this repo's code or doctrine this session, with the file named.
- **[checked]** a research claim already marked checked in files 01 to 06, cited from there. No new web research was done for this note.
- **[believe]** a coaching claim from memory or a secondary source. Allowed in a proposal's wording, never as a hard rule until checked.
- **[inferred]** a design choice reasoned from the parts above.

* * *

## Part 0 · The problem in one paragraph

Today the engine has one road: `match` scores 24 program files and `choose` installs one, which replaces whatever the person did before [read, `match.py`, `plan.py cmd_choose`]. The owner's words: people "already have splits and style of trainings ... we would like just to improve their trainings not change their type of training". The strongest adherence signal in our research is that people keep doing what they enjoy, and someone already training three to five days a week has the habit we would otherwise spend six weeks building [checked, file 06 Part 3b, Rhodes & Kates 2015, Kaushal & Rhodes 2015]. Replacing that routine risks the one thing that already works. What a self-coached lifter usually lacks is the part our engine already owns: a load rule, a progression rule, deloads, readiness, the clock, and a coach's eye on balance.

**The design in one line [inferred]:** do not build a second engine. Turn their routine into a program file of their own, in the exact json shape of `doctrine/programs/*.md`, saved in `me/`, and let `build.py`, `progress.py`, `logbook.py` and `sheet.py` run it. Every improvement the coach sees is computed by the engine as a numbered proposal with a reason, and the person says yes or no to each one.

* * *

## Part 1 · How the person describes their routine, with little effort

### 1.1 Where it sits in the funnel

The fork from file 06 Stage F, right after the screen [read, `06_interview_audit.md`]:

| tile | what follows | `mode` |
|:-|:-|:-|
| Build me a new plan | today's interview, `match`, `choose` | `new` |
| Improve what I already do | outcome (Q1, Q2), the routine (R1 to R7 below), minutes, place, body, then `adopt` | `improve` |
| I train, but I'm open to change | the new-plan path, with the routine captured and offered as option one beside the top three | `open` |

Someone who taps "improve" and then has no routine (R1 "nothing regular") is moved to `new` with one line. The profile is refined first and training comes after, as the owner asked.

### 1.2 The seven screens

Tap budget: about 2 minutes for a 4 day split. Nothing is typed unless they want to.

| # | question | answers | writes (`me/routine.json`) |
|:-|:-|:-|:-|
| R1 | What does your week look like? | a split template (1.3) | `split` |
| R2 | How many days, in what order? | days 1 to 7, then the day labels in their usual order, pre-filled from the template, editable | `days`, `order[]` |
| R3 | What are the main exercises on each day? | the template's pre-filled list per day to keep or untick; "+ add" opens a search of the bank (1.4); "type it" for anything else; "same as Upper A" copies a day | `sessions[label].exercises[]` |
| R4 | Sets and reps you usually do | one chip row per exercise: 3 x 5 · 4 x 6 to 8 · 3 x 8 to 12 · 3 x 12 to 15 · "not sure". "Not sure" takes the default (2.4) | `exercises[].sets`, `.reps` |
| R5 | Recent numbers | for the first one or two lifts of each day: the weight and reps of the last working set, and when ("this week", "this month", "longer"). Runners: a recent easy run in minutes, or a race time | `exercises[].last` `{load, reps, when}` |
| R6 | What's stuck, and what must stay? | stuck (multi): a lift won't go up (tap which) · not growing · always tired or sore · something hurts · bored · I skip sessions · fine. Must stay (multi): the split · the exercises · the days · training to failure · the short sessions · all of it | `stalls[]`, `keep[]` |
| R7 | How hard do your sets go? | to failure most sets · 1 or 2 reps left · 3 or more left · not sure | `effort` |

Then the existing Q8 (minutes, typed or slid), the place and kit (one tap: gym, home with dumbbells, bodyweight, park, box), and the body question (limits). Experience is derived, not asked: routine age "over a year" and a known number on a main lift gives `intermediate`, otherwise `novice`; the person can correct it [inferred].

**Two safety asks the adopt step may add, one line each, only when triggered [inferred from `build.allowed`]:**

- a lift with `needs_coaching: yes` in their list (power clean, snatch...): "were you coached on it?" Yes adds `olympic_coached` to `skills`; no keeps the day and swaps that one lift for the nearest uncoached row of the same pattern, said once.
- pull-ups or chin-ups in their list add `pullup` to `skills`, so the novice pull-up gate in `build.allowed` never swaps a lift they already do.

### 1.3 The split templates (new file `doctrine/routines/templates.md`, one json block)

A template is a starting point, never a rule: every label and exercise is editable.

| template id | labels, in order | pre-filled main exercises per label (bank ids) | parent program (2.3) |
|:-|:-|:-|:-|
| `ppl` | Push, Pull, Legs | Push: `bench_press`, `overhead_press`, `incline_db_press`, `lateral_raise`, `rope_pushdown` · Pull: `pull_up` or `lat_pulldown`, `barbell_row`, `face_pull`, `db_curl` · Legs: `back_squat`, `romanian_deadlift`, `leg_press`, `seated_leg_curl`, `calf_raise` | `muscle-ppl-6` |
| `upper_lower` | Upper A, Lower A, Upper B, Lower B | Upper: `bench_press`, `barbell_row`, `overhead_press`, `lat_pulldown`, `db_curl`, `rope_pushdown` · Lower: `back_squat`, `romanian_deadlift`, `bulgarian_split_squat`, `seated_leg_curl`, `calf_raise` | `muscle-upperlower-4` (goal muscle) or `powerbuild-phul-4` (goal strength) |
| `full_body` | A, B, C | A: `back_squat`, `bench_press`, `barbell_row` · B: `deadlift`, `overhead_press`, `lat_pulldown` · C: `goblet_squat`, `db_bench_press`, `chest_supported_row` | `muscle-fullbody-3` or `strength-lp-3` |
| `body_part` (bro split) | Chest, Back, Legs, Shoulders, Arms | Chest: `bench_press`, `incline_db_press`, `cable_fly` · Back: `deadlift`, `lat_pulldown`, `seated_cable_row` · Legs: `back_squat`, `leg_press`, `seated_leg_curl`, `leg_extension` · Shoulders: `overhead_press`, `lateral_raise`, `rear_delt_fly` · Arms: `ez_bar_curl`, `skull_crusher`, `hammer_curl`, `rope_pushdown` | `muscle-bodypart-5` |
| `run_plan` | Easy, Long, Intervals | Easy: `easy_run` · Long: `easy_run` · Intervals: `interval_run` | `run-base-3to5` |
| `lift_plus_run` | Strength A, Run easy, Strength B, Long run | strength days as `full_body` A and B, runs as `run_plan` | `hybrid-strength-endurance-4to6` |
| `classes_plus_lifting` | lifting days from any template above, plus classes | classes are not sessions: `classes[]` `{name, per_week, hard}` (2.6) | the lifting template's parent |
| `custom` | they name each day | empty lists, the search opens | chosen by the goal: muscle → `muscle-upperlower-4`, strength → `strength-lp-3`, else `health-baseline-2to3` |

Every pre-filled id above exists in `bank.csv` today [read]. The pre-filled list for a home or park place is swapped to that place's rows before it is shown (`build.select` on the template's patterns), so a home user never sees a barbell list [inferred].

### 1.4 Typed names, matched to the bank (fuzzy, stdlib)

`An exercise that is not in the bank is never prescribed` [read, `doctrine/exercises/README.md`]. The matcher keeps that law while accepting how people actually write.

1. **Normalise:** lower case, accents folded (`unicodedata`), plurals and punctuation stripped, shorthands expanded from a table (`db` dumbbell, `bb` barbell, `kb` kettlebell, `ohp` overhead press, `rdl` romanian deadlift, `sldl` romanian deadlift, `bss` bulgarian split squat, `pulldown` lat pulldown...).
2. **Aliases:** a new `doctrine/exercises/aliases.csv` (`alias,id`): gym slang and the five sheet languages for the 40 most common lifts ("développé couché" `bench_press`, "sentadilla" `back_squat`, "skullcrushers" `skull_crusher`...). An alias hit scores 1.0. An alias may point to a near row on purpose, marked `close` (the bank has no pec deck fly, so "pec deck" points to `cable_fly` as close, never to `reverse_pec_deck`, which is the rear-delt move), and a close alias is always shown as a question.
3. **Score** every bank `name` and `id` with `difflib.SequenceMatcher` ratio and a token overlap (Jaccard), take the higher. The coach may pass an English rendering beside the typed text when the person wrote in another language; the engine scores both and keeps the best. The coach never picks the id.
4. **Bands:** 0.85 or more is a match, shown in the summary screen. 0.60 to 0.85 returns the top three as a question ("Incline dumbbell press, Incline bench press or Dumbbell bench press?"). Under 0.60, or no answer: the engine asks for the movement in one tap (push, pull, squat, hinge, lunge, arms, shoulders, core, cardio) and offers the three closest rows of that pattern.
5. **Their own exercise (no row fits):** kept as `own_name` on a slot bound to the closest row of the chosen pattern, `"match": "own"`. That row supplies the safety data (regions, impact, level, position) and the load rounding; the sheet prints their name, no borrowed cue ("your usual form"), and no demo link. It is shown once on the summary screen: "Hammer Strength incline, tracked like an incline press for weights and safety". This is the only door for a name outside the bank, and it is narrow on purpose [inferred].

Same input, same output, always: the matcher sorts ties by id, like `build._select` [read].

### 1.5 Example input (`me/routine.json`, written by the coach or the page)

```json
{"split": "ppl", "days": 4, "order": ["Push", "Pull", "Legs"],
 "sessions": {
   "Push": {"exercises": [{"name": "bench press", "sets": 4, "reps": "6-8", "last": {"load": 80, "reps": 6, "when": "week"}},
                          {"name": "OHP", "sets": 3, "reps": "8-10"},
                          {"name": "incline db press", "sets": 3, "reps": "8-12"},
                          {"name": "lateral raises", "sets": 3, "reps": "12-15"},
                          {"name": "tricep pushdown", "sets": 3, "reps": "10-12"}]},
   "Pull": {"exercises": [{"name": "lat pulldown", "sets": 3, "reps": "8-12"}, {"name": "bicep curls", "sets": 3, "reps": "10-12"}]},
   "Legs": {"exercises": [{"name": "squat", "sets": 4, "reps": "5", "last": {"load": 100, "reps": 5, "when": "week"}},
                          {"name": "leg press", "sets": 3, "reps": "10-12"}, {"name": "leg extension", "sets": 3, "reps": "12-15"}]}},
 "age": "over_year", "stalls": ["bench press"], "keep": ["split", "days"], "effort": "failure", "classes": []}
```

* * *

## Part 2 · How it is stored

### 2.1 The file: `me/PROGRAM.md`

One flat file, beside `PROFILE.md` and `PLAN.md`, same convention: prose for people, then the first ```json block for the engine [read, `core.read_json_block`]. **Flat, not `me/programs/mine.md`:** `plan.py forget` unlinks every entry of `me/` with `Path.unlink`, which fails on a folder [read, `cmd_forget`]; a flat file needs no change there. The web page already persists everything under `me/` recursively [read, `site/app.js fsWalk`], so it works there too.

The id is always `mine`. `plan.json` then says `"program": "mine", "mode": "improve"`.

### 2.2 The json block, in the program schema plus four fields

Every key of `doctrine/programs/README.md` is present, so `build.py` runs it unchanged [read]. New keys are ignored by every existing reader.

| key | value for an adopted routine |
|:-|:-|
| `id`, `name`, `family` | `mine` · "Your plan, coached" · `own` |
| `goals`, `experience`, `evidence`, `simplicity`, `equipment_all` | filled for schema completeness; never used for scoring (`match` never sees this file, 2.7) |
| `days`, `sweet_days` | `[n, n]`, `[n]` from R2 |
| `minutes`, `express_minutes` | from the profile; `express_minutes` is the shortest per-session express (2.5) |
| `layouts` | `{"4": ["Push", "Pull", "Legs"]}`: their order, a queue, never a weekday [read, `07_CYCLE`] |
| `block_weeks`, `deload`, `meso` | copied from the parent program (2.3), `meso.extra_sets_by_week` forced to zeros (3.2) |
| `modules` | `[]` at adopt; filled only by accepted proposals |
| `sessions` | one SESSION per label, blocks and slots built as in 2.4 |
| **`parent`** (new) | the doctrine program it borrows rules from, e.g. `muscle-ppl-6` |
| **`source`** (new) | the normalised `routine.json` it was built from, so a re-adopt is reproducible |
| **`version`, `changes`, `declined`** (new) | the proposal ledger (3.4) |
| **`locks`** (new) | from R6 `keep`: `split`, `days`, `exercises`, `failure`, `short` |

### 2.3 The parent program

The parent is the doctrine program of the same split and goal (table 1.3). It is never run. It lends: `block_weeks`, `deload`, the `meso` effort ramp, and, for any exercise with "not sure" sets and reps, the sets, reps, rest and effort of the parent slot of the same pattern and block kind [inferred]. The prose of `me/PROGRAM.md` names it plainly ("rules borrowed from the push pull legs program"), and the method name stays behind the "how it works" tap, as file 06 Part 3c asks.

### 2.4 From an exercise to a SLOT

| SLOT key | rule |
|:-|:-|
| `key` | `<label>_<bank id>`, lower case, unique in the file (a duplicate gets `_2`). The same lift on two days has two keys; the second one seeds from `loads_by_ex`, which already carries a load across slots [read, `build.slot_item`] |
| `pattern`, `prefer` | the bank row's pattern; `prefer` is **their id only**, `[id]` |
| `theirs` (new) | `true`. Changes three engine behaviours (4.3) |
| `own_name`, `match` (new, optional) | only for an "own" exercise (1.4) |
| `sets`, `reps` | theirs; "not sure" from the parent slot, else compounds 3 x 6-10, isolation 3 x 10-15, strength-goal first lift 4 x 4-6 [read, file 06 Part 3b rule 2] |
| `rest` | the `04_INTENSITY` table by reps and compound or isolation: up to 6 reps 180 s, 6 to 12 compound 120 s, isolation 75 s [read] |
| `effort` | from R7: "failure" keeps "0 to 1 left" on isolation and "1 left" on compounds; "1 or 2" keeps "1 to 2 left"; "3 or more" keeps "2 to 3 left"; "not sure" the parent's line |
| `rule` | fixed reps ("5", "3") and experience none or novice: `linear_session`. Fixed reps and intermediate or advanced: `linear_session` with `inc` 2.5 on every lift. A range ("6-8", "8-12"): `double_progression`. Bodyweight rows fall to `bw` by themselves [read, `build.effective_rule`]. Running days: `run_volume` with `start_minutes` from R5. Never `tm_wave`, `tier_stages` or `rpe_top_set`: those rewrite the set structure, which is theirs |
| `score` | `true` on the first slot of each day |

**Blocks:** the first exercise of a day is the `main` block; the next compound (squat, hinge, lunge, h_push, v_push, h_pull, v_pull, carry, olympic) is `secondary`; the rest is one `accessory` block in their order. Two exercises they mark "together" become a `superset` block with `rest_after_round` 90 [read, schema]. **Session tags:** `heavy_legs` if any row carries it, `power` for olympic or jump rows, `hard_cardio` for an interval run, so the existing spacing rule in `build.pick_session` works [read].

**If their routine is already one of ours** ("I run 5/3/1 Boring But Big"), adopt is the wrong tool: the coach says so in one line and installs the doctrine program with their exercises put first in each `prefer`. The doctrine version runs the method as written [inferred].

### 2.5 The express version, per session

`build.session_template` uses one program-level `express` [read]. One express cannot stand for Push, Pull and Legs. Adopt writes `sessions[label].express`: the main block and the secondary block of that day, sets capped at 3, no accessories. Build uses it only when `fit` cannot bring the normal day under the minutes, exactly as today (4.3).

### 2.6 Classes and running

- **Classes** (`classes[]`) are not sessions and never enter the queue: the engine cannot write or score a class it does not run. They count in three places: the readiness turn already asks about hard cardio in the last 24 hours, so `hard_cardio_24h` moves a heavy-legs day back in the queue [read, `build.pick_session`]; the gap rules treat a class with `hard: true` as conditioning (no conditioning proposal); the week text says "plus your 2 CrossFit classes".
- **A running plan** becomes sessions whose single slot is `cyclic`, `prefer` `easy_run` or `interval_run`, rule `run_volume` for easy and long days (hold about 3 weeks, then about +10%, the existing rule [read, `progress.run_update`, `07_CYCLE`]), and a `benchmark` piece for an interval day with their own description as the piece text.

### 2.7 What else is written

- `me/PLAN.md`: `program: mine`, `mode: improve`, `days`, `modules: []`, `start`, `review`, `history` (+ `{"date", "program": "mine", "version": 1}`), and a prose section "What the coach changed, with your yes" generated from the ledger.
- `me/PROFILE.md`: `mode`, `numbers` from R5 (4.5), `skills` additions (1.2), `experience` derived.
- `me/state.json`: as `choose` writes it today, `program: "mine"`.
- `match` never reads `me/` (`core.all_programs` globs `doctrine/programs/` only [read]), so the person's file is never offered to anyone else and never scored. In `open` mode, `plan.py match` adds `"own": {...}` in front of `top`, unscored.

* * *

## Part 3 · What the coach changes, and what it never changes

### 3.1 The three lists

| never changes without a yes | applied always, said once (existing rules) | proposed, one by one, with a reason |
|:-|:-|:-|
| the days a week and their order | the load each session (first outing, or their working weight, 4.5) | adding a set, a slot or a module |
| the split and the day labels | the progression of every slot (double, linear) | changing a rep range or a rule on a stalled lift |
| their exercises and which day each one is on | the readiness dose (light day, rest day) [read, `build.readiness`] | trimming sets to fit the minutes |
| their sets x reps | the deload week of the parent block, and the early deload triggers [read, `logbook.deload_triggers`] | an effort change (leaving a rep in the tank) |
| training to failure, if they locked it | the clock and the minutes ceiling on the day [read, `build.fit`] | swapping one of their exercises for a better one |
| | **safety, never a proposal:** pain, limits, pregnancy, seated, the coached-lift gate swap an exercise for that day and say why [read, `build.allowed`] | |

### 3.2 Existing rules that would change their routine silently, and what improve mode does with each

This is the heart of "keep their routine": the engine already makes five quiet edits that are fine inside our own programs and wrong inside theirs [read, `build.py`].

| existing behaviour | where | in improve mode |
|:-|:-|:-|
| accessory sets +1 on up to two slots for a `priority` muscle | `build.build`, the `pri` loop | off for `family: own`; the same need becomes the `priority_direct` or `group_low` proposal |
| a bodyweight or fixed-weight lift at the top of its range jumps to the bank's `harder` row | `build.slot_item`, the `harder` branch | for a `theirs` slot: no switch; the note "ready for Archer push-up" becomes a `harder_step` proposal |
| accessory sets +1 in weeks 3 and 4 (`meso.extra_sets_by_week`) | `build.slot_item`, the meso branch | forced to zeros at adopt; offered once as the `ramp` proposal |
| the effort ramp "3 left" to "1 left" (`meso.rir_by_week`) | same | kept, except when `failure` is locked: then off |
| a level gate one above their cap on a `prefer` id | `build._select`, `slot_item` | a `theirs` slot uses cap 5 (their own lift is never refused for being "too advanced"); every other gate stays |
| `fit` drops their last accessory when the day runs long | `build.fit` | kept on the day (the minutes are their own ceiling), and the `time_fit` proposal is offered first at adopt so it rarely fires |

### 3.3 The coach's eye: gap rules, computed by the engine

New module `engine/improve.py`, function `gaps(program, prof, plan, log)`. Every rule reads the program file (planned weekly sets) and, after two weeks, the log (done sets, `hard_sets` per line [read, `logbook.apply`]). Planned volume uses the same fractional count as the log: primary muscles a full set, secondary half, grouped by `logbook.GROUPS` [read]. A rule fires or not; the coach never adds one.

| id | fires when | the change it proposes | why, in one line | mark |
|:-|:-|:-|:-|:-|
| `time_fit` | a day's dry-built clock is more than 3 min over their minutes | option A: raise their minutes to the number the clock found; option B: trim the named sets (last accessory sets to 2, then one secondary set) | "Push takes 74 minutes with your rests; you said 60" | [read] `06_BUILD` clock |
| `pull_volume` | weekly back sets under two thirds of chest plus front-delt sets | +1 set on their existing row or pulldown; if none, a `chest_supported_row` or `face_pull` slot on the pull or upper day with most spare minutes | "12 pressing sets, 4 pulling: shoulders like it nearer even" | [believe] ratio; [checked] volume, file 01 |
| `group_low:<group>` | goal muscle or physique priority and a major group (chest, back, shoulders, quads, glutes, hamstrings) under 10 weekly sets; any goal and under 4 | +1 set on their existing work for that group first; a slot only if they have none | "hamstrings get 3 sets a week; 10 or more grow clearly better" | [checked] Schoenfeld 2017, Pelland, file 01 |
| `group_high:<group>` | over 20 weekly sets on one group, or over 10 in one session | −1 set on the last slot for that group | "22 chest sets a week: past 20 the extra rarely pays" | [checked direction] file 01; [believe] the 10 per session line |
| `priority_direct` | `priority` names arms, biceps, triceps, delts or calves, and the week has no slot of that pattern | a 2 to 3 set slot of the lengthened pick (`incline_db_curl`, `overhead_db_triceps_extension`, `cable_lateral_raise`, `seated_calf_raise` if the kit allows) on the day with most spare minutes | "you want bigger arms and no set trains them directly" | [checked] Maeo 2022/23 lengthened picks, file 01 |
| `conditioning_event` | `event` set, or goal `hyrox`, `run` or `functional`, and the week has no cyclic slot, no running day and no `hard` class | the module of that goal: `hyrox-stations`, `conditioning`, or `run-race` on an extra day if their days allow, else a `conditioning` finisher | "HYROX in 9 weeks and nothing in the week trains the engine" | [read] `MODULE_FOR_GOAL2`; research/02 |
| `stall:<key>` | a lift in R6 `stalls`, or the log shows the same slot without a load or rep gain in 3 outings | for `linear_session`: the existing 10% reset already runs, so the proposal is the rep range (5 x 5 to 3 x 6-8, double progression) at the same load; for `double_progression`: one fewer set at the same load for a block | "bench has not moved in 3 weeks; a new rep range usually restarts it" | [believe] coaching consensus, file 01 stall rules |
| `recovery` | R6 says always tired or sore, or two `felt: flat` in the last four logs, together with any `group_high` or effort to failure on compounds | one set less on every accessory for one block, or compounds at "1 to 2 left" | "you're tired and every compound goes to failure: strength gains hold at 2 left" | [checked] Refalo 2023, Robinson 2024, file 01 |
| `harder_step:<key>` | a `theirs` bodyweight or fixed-weight slot hit the top of its range (3.2) | switch to the bank's `harder` row | "3 x 15 push-ups done twice: decline push-ups next?" | [read] `05_LOADS` fixed weights |
| `ramp` | once, after the first full block, on muscle goal | turn on `extra_sets_by_week` from the parent | "add a set to accessories in the last two weeks of each block" | [believe] RP shape, `07_CYCLE` |

**Never proposed, on purpose:** changing the split or the frequency. Once volume is equal, how often a muscle is trained barely moves growth [checked, Pelland, file 01], so a bro split is coached as a bro split. Weekday tying is out of scope: the engine runs sessions in order, never by weekday [read, `07_CYCLE`].

**Where an added slot goes, deterministically:** the session of the matching role (pull work to a Pull or Upper day, arms to Arms or the upper day), then the one with the most spare minutes by the dry-built clock, then the first in their order.

### 3.4 How a change is proposed, accepted or declined

1. **The engine ranks.** Order: `time_fit`, then `recovery`, then goal gaps (`conditioning_event`, `priority_direct`), then balance (`pull_volume`, `group_low`, `group_high`), then `stall`, `harder_step`, `ramp`. Ties by id.
2. **The lock filter.** Each rule carries its alternatives in order; the engine takes the first that touches no lock (with `exercises` locked, `group_low` adds a set to an existing lift before it would add a new one). If every alternative touches a lock, the proposal still goes out with `"touches_lock": "exercises"`, and the coach says "you said your exercises stay: only if you want".
3. **At most two per block.** The output holds the top two open proposals plus the count of the rest. Adopt day counts as block 1. This keeps the routine theirs and the coach not a nag [read, file 06 Part 3b rule 5].
4. **The coach explains, never decides.** `plan.py improve` prints per proposal: `id`, `title`, `why` (the line above, filled with their numbers), `evidence` (file and mark), `change` (the exact patch in plain words: "Pull day: +1 set of Lat pulldown, 3 to 4"), `minutes_cost`, `touches_lock`. Claude translates the words, one line each, and asks yes or no in one turn.
5. **Yes:** `plan.py improve accept <id>` applies the patch from a whitelist of five operations (`add_sets`, `add_slot`, `set_reps_rule`, `set_effort`, `add_module`; `swap_ex` only for `harder_step`), bumps `version`, appends to `changes` `{id, date, block, what, why}`, rewrites the prose section of `me/PROGRAM.md` and `me/PLAN.md`, refills the queue if a session changed, and commits ("improve: +1 pull set, with your yes"). Slot keys of existing lifts never change, so their loads and progress carry [inferred].
6. **No:** `plan.py improve decline <id>` appends `{id, date, block, facts}` to `declined`. A declined proposal is not offered again until two blocks have passed or the facts behind it changed (a new priority, a new event, the minutes) [inferred].
7. **Undo:** `plan.py improve undo <id>` reverses one accepted patch (each op stores its inverse). Their routine is never more than one sentence away from how they brought it.

**Timing:** proposals are computed at adopt, at every `block_closed` event (the cycle audit already runs then [read, `08_WORKFLOW`]), and when the person says `/train improve`. Never mid-session.

* * *

## Part 4 · The engine changes, file by file

Standard library only (`difflib`, `unicodedata`, `json`, `re`, `copy`), as today. Line counts are estimates of code, not comments.

| file | change | size |
|:-|:-|:-|
| **`engine/improve.py`** (new) | `match_name(text, bank, english=None)` → `{id, score, band, choices}` (1.4) · `adopt(routine, prof, bank)` → program dict (2.2 to 2.6) · `planned_sets(program)` fractional per group · `dry_clock(program, prof, bank)` per session, by running `build.build` on a deep copy of a fresh state at energy 8 and their minutes plus 60 with `fit` skipped, then `sheet.session_seconds` · `gaps(...)` the ten rules of 3.3 with alternatives · `apply_patch` / `invert_patch` for the six ops · `write_program(path, program)` prose plus json via `core.write_json_block` | ~480 |
| `engine/core.py` | `MINE = ME / "PROGRAM.md"`; `load_program("mine")` reads `MINE`; `TARGETS` (from `plan.py`) and `GROUPS` (from `logbook.py`) move here so `improve.py` shares them; `load_aliases()` | ~25 |
| `engine/plan.py` | `cmd_adopt(routine.json)`: checks the screen and profile, runs the matcher, returns `needs` (mid-band names, unknown patterns, the coached-lift ask) like `log` does, else writes `PROGRAM.md`, `PLAN.md`, state, commits, and returns the first two proposals · `cmd_improve [accept|decline|undo <id>]` · `status`: a `mode: improve` person with no `PLAN.md` gets `stage: needs_routine` · `choose mine` routes to adopt's plan writer · `rebuild` unchanged (it already calls `load_program`) · the CMDS table and the docstring | ~110 |
| `engine/build.py` | `_select` and `slot_item`: a `theirs` slot uses level cap 5 for its own id (one helper, `slot_cap`) · the `harder` branch: for `theirs`, append a note and set `st["ready_harder"]`, no switch · the priority bump skipped when `prog["family"] == "own"` · `session_template`: prefer `prog["sessions"][sid]["express"]` over `prog["express"]` · `slot_item`: print `own_name` and "your usual form" when present · `seed_from_numbers`: a number with `working: true` enters at its own load, no discount (4.5) | ~35 |
| `engine/checks.py` | `walk_session` lifted out of `check_template` into `check_program(p, bank)`; `check_data` runs it on `me/PROGRAM.md` when the plan says `mine` and fixes the "program has no file" check to look there; `check_template` adds `me/PROGRAM.md` to the "must ship empty" list; the bank check also validates `aliases.csv` ids | ~30 |
| `engine/match.py` | `open` mode: `match` gains `own=None`; when given, `res["own"]` is put in front, unscored, with a plain `why` ("your own split, coached") | ~10 |
| `engine/sheet.py` | the header meta prints "Your plan, coached" for `family: own` instead of a method name; no layout change | ~3 |
| `engine/logbook.py` | none. `apply` reads the slot from the session file, `advance` reads `plan["days"]` and the program's `block_weeks` [read] | 0 |
| `engine/progress.py` | none. Only existing rules are used | 0 |
| `doctrine/routines/templates.md` (new) | the eight templates of 1.3: labels, rotations per day count, pre-filled ids, parent per goal | ~120 incl. json |
| `doctrine/exercises/aliases.csv` (new) | about 150 alias rows for the common lifts, five languages | ~150 rows |
| `doctrine/09_IMPROVE.md` (new) | owns 3.1 to 3.4: the three lists, the ten gap rules with their marks, the two-per-block cap, the locks | ~70 |
| `doctrine/02_INTERVIEW.md`, `03_MATRIX.md`, `05_LOADS.md`, `06_BUILD.md`, `08_WORKFLOW.md` | the fork and R1 to R7 · `open` mode in Step 4 · working numbers (4.5) · per-session express and the priority bump off for own · the improve steps and their audit | ~40 |
| `.claude/skills/train/SKILL.md` | the improve branch wording, "explain each proposal in one line, never add one", the yes or no turn | ~35 |
| `.claude/agents/school-auditor.md` | at adopt: the routine on the sheet is the routine they described (every exercise, set and rep traceable to `routine.json` or to an accepted change) | ~10 |
| `site/app.js` | the fork tile, R1 to R7 screens, the summary screen with match bands, the proposal cards with yes and no; `build_bundle.py` unchanged (it packs `doctrine/` whole [read]) | ~250 JS |
| `tests/test_improve.py` (new), `tests/smoke_programs.py` | Part 5 | ~230 |

**Totals:** about 700 lines of Python in the engine (480 new in one file, about 215 changed across six), about 400 lines of doctrine and data, about 230 lines of tests, about 250 lines of page script. Roughly two working days for the engine and tests, one for the page [inferred].

### 4.5 One doctrine change worth naming: their working weight

`05_LOADS` says a known number enters once with a 10% discount [read, `build.seed_from_numbers`]. That rule is right for a number from memory. For someone who benched 80 kg x 6 this week on the same 4 x 6-8, the discount prescribes about 70 kg, and the first thing the coach does is lower their bench. **Proposed:** a number marked `working: true` (same exercise, same rep range, done in the last 14 days) seeds the slot's `load` at that weight and its `target` at those reps, rounded down to their plates, no discount. Anything older or from another rep range keeps today's rule. The first sheet says "your usual weight: if it's not about 2 left, tell me" and the log corrects it after one session [inferred]. Mark: [believe], to verify with the session-auditor on the first ten real users.

* * *

## Part 5 · The tests that prove it

`tests/test_improve.py`, unittest, same style as `test_engine.py` [read]. Each test names the rule it proves.

| # | test | proves |
|:-|:-|:-|
| 1 | `match_name`: "bench" → `bench_press`, "DB bench" → `db_bench_press`, "RDLs" → `romanian_deadlift`, "lat pull down" → `lat_pulldown`, "skullcrushers" → `skull_crusher`, "développé couché" → `bench_press`; "incline press" returns three choices; "Hammer Strength incline" returns band low | the matcher and its bands, 1.4 |
| 2 | the same `routine.json` adopted twice gives byte-identical `PROGRAM.md` | determinism |
| 3 | adopt output passes `checks.check_program` with zero errors, for all eight templates | the schema holds, 2.2 |
| 4 | every slot's `prefer` is `[their id]`, sets and reps equal the input, `layouts` equals their order | nothing of theirs is rewritten, 3.1 |
| 5 | `build.build` on the adopted program: the main and accessory items are their exercises in their order, and no set count differs from the file (priority set to arms) | the priority bump is off, 3.2 |
| 6 | an intermediate's level 5 row in their list is prescribed; the same row with `pain: shoulder 6` is swapped and the note says why | cap 5 for theirs, safety still wins |
| 7 | a `working: true` 80 kg x 6 seeds 80 kg; the same number without `working` seeds the discounted load | 4.5 |
| 8 | a bodyweight `theirs` slot at the top of its range for two sessions: the exercise does not change, and `gaps` returns `harder_step` | no silent ladder climb, 3.2 |
| 9 | gap fixtures: PPL with 12 push and 4 pull sets → `pull_volume` first; arms priority with no arm slot → `priority_direct`; HYROX event with no cyclic work → `conditioning_event` with `hyrox-stations`; a 74 min day at 60 min → `time_fit` ranked first; the same HYROX fixture with a `hard` class → no conditioning gap | each rule fires, 3.3 |
| 10 | a balanced upper/lower 4 x 75 routine, goal muscle → `gaps` returns nothing | no false positives |
| 11 | `exercises` locked: `group_low` picks `add_sets` over `add_slot`; with no lift of that group, the proposal carries `touches_lock` | the lock filter, 3.4 |
| 12 | `accept` then `undo` restores the file byte for byte; `decline` hides the id until block + 2 or a changed fact; never more than two open proposals | the ledger, 3.4 |
| 13 | full loop through `plan.py` in a temp copy (as `Memory.test_full_loop_and_rebuild`): screen, profile, adopt, three build and log rounds, an accepted proposal, then `rebuild` gives the same slots and queue | memory and rebuild hold across a changed program |
| 14 | `forget yes` removes `me/PROGRAM.md`; `checks.py template` fails if it ships with data | the privacy rules hold |
| 15 | per-session express: a 25 minute day on the adopted PPL builds the Push express, under the minutes, and the sheet is not refused | 2.5 |
| 16 | `smoke_programs.py` gains five improve personas run for ten sessions each (bro split 5 days, upper/lower 4, full body at home with 2 dumbbell pairs, runner 4 days, CrossFit 2 classes plus lifting 2): no crash, no refused sheet, no session over the minutes, state passes its check | the whole road |
| 17 | `test_web_bridge.py`: `adopt` and `improve` run in the bundle and `me/PROGRAM.md` survives `persist` and `restore` | the web page |

The existing suite must stay green unchanged: no doctrine program is touched, `match` results for `mode: new` are identical (a regression test pins the six worked examples of `03_MATRIX`) [read].

* * *

## Part 6 · Risks

| # | risk | why it matters | the guard |
|:-|:-|:-|:-|
| 1 | **Silent rewrites by rules built for our own programs** | five existing behaviours change sets, exercises or effort without a word (3.2). Missing one breaks the promise "we keep your routine" on day one, which is exactly the owner's complaint | each one is switched by `family: own` or `theirs`, and test 5 and 8 pin them. The school-auditor checks the first sheet against `routine.json` line by line |
| 2 | **A wrong name match** | a wrong row brings the wrong regions and impact into the safety filter, and a wrong cue | only 0.85 and up maps without a question; the summary screen shows every mapping once; "own" exercises print no borrowed cue |
| 3 | **Their working weight is overstated** | no discount (4.5) means a bad number lands on the first sheet | 14 day and same-rep-range conditions, "2 left" check on the sheet, the log corrects after one session, light dose rules still apply |
| 4 | **We now coach a routine with known holes** | a declined `pull_volume` stays a hole, and the sheet carries our name | declined proposals stay listed in `PLAN.md`; safety is never a proposal; the cycle audit re-offers after two blocks |
| 5 | **Proposal nagging** | ten gaps at once reads as "your routine is bad", and they leave | two per block, ranked, alternatives that respect locks first |
| 6 | **The clock refuses their real day** | a 90 minute bro split at 60 minutes gets accessories cut each session | `time_fit` is first at adopt and offers raising the minutes, the honest fix; per-session express covers short days |
| 7 | **Classes and runs are thinner than lifting** | the engine cannot see inside a class, so conditioning credit is taken on their word | `hard: true` is asked, not assumed; run days use only existing run rules; the lifting case ships first if time is short |
| 8 | **[believe] numbers in gap rules** | the push to pull ratio and the 10 sets per session line are not checked | marked in `09_IMPROVE.md` and listed under "to verify" in `doctrine/schools/INDEX.md`, as every other [believe] number |
| 9 | **The program file changes under the state** | an accepted patch changes a session after loads were logged | slot keys never change, `rebuild` replays from session files that carry their own slots (test 13) |
| 10 | **Their routine is one of ours** | adopting 5/3/1 as a custom file loses its waves | detected at R1 by name; the doctrine program is installed with their lifts first in `prefer` |

**Main risk:** number 1. The engine was written to run its own programs, so several helpful rules quietly edit sets and exercises. Improve mode is only honest if every one of those is turned into a proposal, and the tests have to pin each one.

## Not verified this session

- No web research: every [checked] mark is inherited from files 01, 04 and 06, which carry their own limits (abstracts and excerpts only).
- The size estimates are from reading the engine, not from a prototype.
- The 0.85 and 0.60 match bands are a guess until the matcher is run on real typed routines; tune them on the first fifty.
- The alias list does not exist yet; the five language rows need a native check per language.
