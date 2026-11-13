# 04 · Intensity · effort, readiness, rest

_This file owns: how hard, how the day's readiness changes the dose, and the rest periods. Code: `engine/build.py` (`readiness`, `slot_item`, `fit`)._

## Effort, in plain words

| on the sheet | means | the old name |
|:-|:-|:-|
| "4 left in the tank" | easy, crisp, technique | RPE 6 |
| "3 left" | moving well, could do 3 more clean reps | RPE 7 |
| "2 left" | hard, 2 more clean reps at most | RPE 8 |
| "1 left" | very hard | RPE 9 |
| "to the limit" | no more clean reps | RPE 10 |

**Ask at the END of the set:** "how many more clean reps?". People underestimate what is left by about one, and guess better close to the limit and on low-rep sets [Halperin 2022, checked]. So newcomers aim at 3 to 4 left while they find a weight (`05_LOADS.md`); after that, the program's own effort line rules.

Muscle work ends 0 to 3 from the limit; strength work can sit 2 to 4 from it with no loss [Refalo 2023, Robinson 2024, checked].

## Readiness: the dose, not the session

| energy | the day | what changes |
|:-|:-|:-|
| 8 to 10 | full dose | as planned |
| 6 to 7 | normal dose | as planned, but any "as many as you can" set stops with 1 left |
| 4 to 5 | light dose | sets cut by about a third, loads about 10% lighter, no tests |
| 1 to 3, or ill | rest | no session (ill), or an optional easy walk and mobility |

**Soreness is asked apart from pain, and never takes the pain path.** Muscle soreness after training (both sides, in the muscle) is normal and is not an injury: "a bit" changes nothing but a line that the warm-up eases it; "very sore" keeps the main work, takes one set off the extra moves for the sore muscles (legs, upper body, middle or all over), and caps the day at the normal dose (no all-out sets). It never removes a region, never refers. Pain in a joint, or in one spot, is pain: the rules of `01_SAFETY.md` and below. Code: `build.SORE_AREAS`, `build.ease` [research/07 change 10; the dose: believe].

**Readiness lowers the dose, it never chooses the session** (kept from Adam's trainer: otherwise people always land on the session they like). Only four things change which session runs: pain (removes a region), illness or energy 3 or less (a rest day), today's equipment (swaps, or the travel session), and the spacing rules of `07_CYCLE.md`.

**Back after a break:** 7 to 13 days, a light dose; 14 days or more, loads about 15% lighter that day and one easy session after; the tiers are in `07_CYCLE.md` (the missed week) [believe]. **An easier week** agreed at the weekly check-in, or an easier block at the block review, caps the dose at normal and takes one set off the extra moves.

## Rest (the program file gives each line its rest; these are the ranges it must sit in)

| kind of set | rest |
|:-|:-|
| heavy compound, 1 to 6 reps | 2:00 to 4:00 |
| compound, 6 to 12 reps | 1:30 to 2:30 |
| isolation, 10 to 20 reps | 1:00 to 1:30 |
| supersets of two non-competing moves | 0:15 between, 1:00 to 1:30 after the pair |
| timed pieces (AMRAP, EMOM, for time, intervals) | only what the format says |
| runs | none: the time is the work |

Rest is intensity: the same load with half the rest is a different session. That is why the clock counts every rest (`06_BUILD.md`).
