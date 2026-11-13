# 03 · The matrix · how a program is chosen

_This file owns: the rule that picks a program. Code: `engine/match.py`. The coach explains the result; it never computes it._

The candidates are the files directly in `programs/`. The ones in `programs/_out_of_scope/` are never read (`00_MISSION.md` says why).

## Step 1 · Hard filters

A program is out if any of these fails, and the person is told which:

1. **Experience** outside the program's `experience` list. The experience that counts is the program's own domain (`match.domain_experience`): running programs read `experience_by.running`; HYROX, hybrid and CrossFit-style programs take the higher of lifting and conditioning (running, cycling or rowing, classes, CrossFit or HYROX), capped one step above the lower; every other family reads the lifting experience (`experience`). A profile without `experience_by` uses its one `experience` everywhere.
2. **Days:** the days that count are the ones the composer gives this program's family (`compose.lead_days`: a 60/40 blend on 4 days leaves the lead 2 or 3). Fewer than the program's minimum is out; so is a day count the program has no honest week for, and a layout that would squeeze more sessions than days (only whole body programs marked `rotates` may take turns). More days are fine: the program runs at its own maximum and the composer gives the extra days to the other components, a running or cardio day, or rest, said.
3. **Minutes:** fewer than its `express_minutes` (its shortest legal version).
4. **Equipment:** a tag in `equipment_all` missing at their main place, or none of an `equipment_any` group present.
5. **Skills:** a `skills_required` they have not reported (coached Olympic lifts, running 30 minutes, a pull-up).
6. **Population:** pregnancy (only `health-baseline-2to3`) · low bone density on a program excluded for it · seated on a program whose main lifts need standing · `under_60` or `over_60` programs (the schema keeps them; the age band is fixed at 18 to 39, so no program in scope uses them).
7. **Fillable:** every main-block slot of every session can be filled from the bank for their equipment and position. A slot that only a limit empties costs 1 point of score (Step 2) instead, unless the limit empties more than half the main slots of a session: a limit removes moves, never the goal. If not fillable, the program is out with the slot named.
8. **Not for me:** a program they turned down with a reason other than "I can't do these days" (`rejected`) is out, and says so.

## Step 2 · The score

`3 x goal fit (main goal) + 1.5 x goal fit (second goal) + evidence (A 2, G 2, B 1, C 0) + 2 if it asks for something they enjoy, minus 3 if it asks for something they can't stand + 2 if its family is the one their outcome points at + 1 if their days are in the program's sweet spot, minus 2 if it would leave two or more of their days empty`, then the improve and "not for me" terms below.

Goal fit is the 0 to 3 each program declares for all 11 goals. The goal comes from the outcome and its follow-up (`02_INTERVIEW.md`, `core.OUTCOMES`).

**Enjoy and can't stand are activity words, an adherence input, never a menu** (`match.ENJOY_OF`): strength and Olympic lifting ask for heavy lifting · powerbuilding heavy lifting and muscle work · muscle building muscle work · CrossFit-style fast circuits · HYROX fast circuits and running · hybrid heavy lifting, running and long cardio · running running and long cardio · health nothing in particular. Older profiles that said equipment words (barbell, machines, circuits) are read through `match.LEGACY_LIKES`; equipment words never score a family.

**The outcome family** (`match.OUTCOME_FAMILY`): the follow-up names the families that serve it (more size: muscle, powerbuilding · strong and able to run far: hybrid · fit for anything: CrossFit-style · a running event: running ...). It settles what a goal key alone cannot say, like strength and running in one week.

**The improve path** (`mode: improve`): plus 2 when the program's week has the same shape as their routine (`match.SPLIT_OF`: push pull legs, upper and lower, full body, body part, strength plus cardio days, a running plan, classes), plus 1 when their routine's day count is inside the program's days. The why line says "the same shape as your week". Since phase F the improve path does not reach the match: `plan.py adopt` keeps their own routine (`06_BUILD.md`, Their own routine). The match runs on that path only for a week of classes only, which the trainer cannot write.

**Not for me** (`rejected`, `02_INTERVIEW.md`): too long, minus 2 for every program whose shortest session is as long or longer than the one turned down · too much running, running counts as something they can't stand · I wouldn't enjoy it, minus 3 for the family turned down · I can't do these days, the days are asked again and written.

**A preferred style, experienced people only** (`style_pref`, `match.style_pref`): read only when the profile is on the improve path or holds an intermediate or advanced experience; a beginner's is ignored even if sent, and `trainer` means the trainer decides. When a passing program of that style serves the goal (goal fit 2 or more) or the outcome's family, the passing programs of that style go first: a filter where the style fits the outcome. When none does, the ranking is untouched and `match` returns `style_note`, one honest line: "You prefer running, but running is not built for building muscle, so the trainer picked what serves your goal better."

**Sleep and stress** never change the choice for now: `start_volume: low` (under 6 hours or high stress) returns a `dose_note` the coach says.

## Step 3 · Tie-breaks

In order: the higher goal fit for the main goal (a program built for what they asked beats a generic default that ties it on points, 13 nov 2026) · the simpler program for `none` and `novice` (`simplicity` 1 linear, 2 double progression, 3 waves, 4 RPE) · the higher evidence · the fewer minutes · the id.

## Step 4 · The offer · one plan

**The trainer decides one plan and says it.** `match` returns `plan` (the first of the ranking) and keeps `runner_up` and `top` for the coach only: the person is never shown three programs to choose from. The plan is told in plain words, built by `match` in `plain` (`headline`: what comes first, e.g. "Strength first: heavy main lifts, then muscle work"; `week`: days, minutes and the shape of the week) and `why` (goal fit in words, the days, what they enjoy, the same shape as their week, how a blend was honoured, the evidence letter). The page and the coach translate those words and never assemble or recompute them.

**Method and school names stay behind "How it works"** (5/3/1, PHUL, GZCLP, the Texas method and the rest): the card's title is the plain family name, and the method is one tap away for anyone who wants it, an experienced person especially.

Then two answers: **start this plan** (`plan.py choose <plan.id>`), or **not for me** with a reason, which writes `rejected` and re-runs the match (Step 2). A blend of outcomes is honoured by the composer (`06_BUILD.md`): the lead program plus days or a protected finisher for every other outcome, by share, said in `why` and `plain.week`.

Notes that travel with the plan, said in one line each when present: `outcome_note` (an outcome no program is built for, `core.OUTCOME_GAP`, empty since the composer), `plan_note` (how the marathon or "keep it going" is served, `core.OUTCOME_PLAN`), `style_note`, `improve_note`, `dose_note`.

## Step 5 · Never an empty answer

When nothing fits the goal well (the first pick's goal fit is under 2), `match` returns `fallback`: programs that are one change away (the single filter that blocked them, only one the person can change: kit, days, minutes, a skill, never age, experience, pregnancy, bone density or position), a note if the goal itself is not served, and the start-here program that fits almost anyone in a gym (`health-baseline-2to3`). It also returns `goal_gap`, one line naming why nothing built for the goal passed ("nothing built for getting stronger fits your kit: PHUL needs a barbell, rack, bench and plates; Functional fitness, general preparedness needs a rower, bike, ski erg or treadmill"), and each offered program's `why` says it only partly serves the goal. Example: strength in a home gym with dumbbells up to 12 kg and bands, a few months in. Every strength program needs a barbell and rack, and the CrossFit-style plan needs a cardio machine, so Health baseline (strength fit 1) is honestly the best on offer, and the coach says so with the one purchase that opens a real strength program.

## Second goals

Never a second program stacked in one session. The composer (`06_BUILD.md`) gives a second goal its own days by share (running days, HYROX days, mixed conditioning days, a whole body lifting plan), or a goal finisher the clock cuts last when its share is too small for a day (`conditioning`, `hyrox-stations`, a short easy run, `core`). (The `skills` and `independent` goals, and the balance add-on from 60, stay in the code for old profiles but are never offered.)

## Worked examples (checked by `tests/test_engine.py`, the `Interview` class covers every outcome, both fork paths, the style gate, the blend and "not for me")

| person | likely top pick |
|:-|:-|
| never trained, 3 x 60 min, full gym, wants strength, likes barbells | `strength-lp-3` |
| 2 years in, 4 x 75 min, full gym, wants muscle | `muscle-upperlower-4` or `powerbuild-phul-4` |
| first time in a gym, 3 x 45 min, basic gym, wants to feel healthier | `health-baseline-2to3` |
| home gym with dumbbells and a rower, 3 x 45 min, novice, wants all-round fitness | `functional-gpp-3to5` |
| outdoors only, 3 x 30 min, never ran, wants running | `run-c25k-3` |
| CrossFit 3 years, 5 days, HYROX race, runs 30 min | `hyrox-prep-4` |
| a year on an upper and lower routine, 4 days, wants more size, improve path | `muscle-upperlower-4` |
| strong and able to run far, intermediate at both, 4 days, full gym | `hybrid-strength-endurance-4to6` |
| never lifted, runs 5 years, a 10K, outdoors | `run-base-3to5`, lifting experience none |
