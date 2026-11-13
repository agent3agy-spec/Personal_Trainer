# 03 · The matrix · how a program is chosen

_This file owns: the rule that picks a program. Code: `engine/match.py`. The coach explains the result; it never computes it._

## Step 1 · Hard filters

A program is out if any of these fails, and the person is told which:

1. **Experience** outside the program's `experience` list.
2. **Days:** fewer than the program's minimum. More days are fine: the program runs at its own maximum and the extra days take a running add-on or rest.
3. **Minutes:** fewer than its `express_minutes` (its shortest legal version).
4. **Equipment:** a tag in `equipment_all` missing at their main place, or none of an `equipment_any` group present.
5. **Skills:** a `skills_required` they have not reported (coached Olympic lifts, running 30 minutes, a pull-up).
6. **Population:** pregnancy (only `health-baseline-2to3` and `home-fullbody-2to4`) · low bone density on a program excluded for it · seated on a program whose main lifts need standing · `under_60` or `over_60` programs.
7. **Fillable:** every main-block slot of every session can be filled from the bank for their equipment, limits and position. If not, the program is out with the slot named.

## Step 2 · The score

`3 x goal fit (main goal) + 1.5 x goal fit (second goal) + evidence (A 2, G 2, B 1, C 0) + 2 if a style they like + minus 3 if a style they dislike + 1 if their days are in the program's sweet spot + 1 if the program is built for their age group (60 and over) minus 2 if it would leave two or more of their days empty`

Goal fit is the 0 to 3 each program declares for all 11 goals. Styles per family: strength and Olympic lifting barbell · powerbuilding barbell, machines · muscle machines, dumbbells · functional circuits, classes · HYROX running, circuits · hybrid running, barbell · running running · calisthenics bodyweight · kettlebell kettlebells · home dumbbells, bodyweight · health and older dumbbells, machines.

## Step 3 · Tie-breaks

In order: the simpler program for `none` and `novice` (`simplicity` 1 linear, 2 double progression, 3 waves, 4 RPE) · the higher evidence · the fewer minutes · the id.

## Step 4 · The offer

The top three, recommendation first, each with one line: what it is, its days, the schools it draws from, its evidence letter. The person may choose any program that passed Step 1, never one that failed it.

## Step 5 · Never an empty answer

When nothing fits the goal well, `match` returns `fallback`: programs that are one change away (the single filter that blocked them), a note if the goal itself is not served, and the two programs that fit almost anyone (`health-baseline-2to3`, `home-fullbody-2to4`).

## Second goals

Never a second program. `plan.py choose` adds a module (`modules/README.md`): running goals get `run-race` on extra days, all-round fitness and health get `conditioning`, HYROX gets `hyrox-stations`, skills get `skill-blocks`, staying independent gets `balance`. Everyone 60 and over gets `balance`.

## Worked examples (checked by `tests/test_engine.py`)

| person | likely top pick |
|:-|:-|
| never trained, 3 x 60 min, full gym, wants strength, likes barbells | `strength-lp-3` |
| 2 years in, 4 x 75 min, full gym, wants muscle | `muscle-upperlower-4` or `powerbuild-phul-4` |
| 69, 3 x 45 min, basic gym, wants to stay independent | `older-strong-3` |
| home, bands and a pair of 8 kg dumbbells, 3 x 30 min, wants fat loss | `home-fullbody-2to4` |
| park bars only, wants skills | `calisthenics-rr-3` |
| CrossFit 3 years, 5 days, HYROX race, runs 30 min | `hyrox-prep-4` |
