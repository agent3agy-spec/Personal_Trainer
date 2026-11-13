# 06 · Build · the session, the clock, the sheet

_This file owns: the shape of a session, the time math, the cut order, and what the sheet shows. Code: `engine/build.py`, `engine/sheet.py`._

## The shape

| # | block | rule |
|:-|:-|:-|
| 1 | warm-up, 6 to 8 min | written by the engine: 3 min raise on whatever cardio is there, 2 mobility moves for the day's joints, ramp sets of the first main lift |
| 2 | main block | the program's main work, with the score to beat. **Never cut** |
| 3 | second lift | the program's secondary work, if any |
| 4 | accessories | the program's slots, filled from the bank, supersets where the program says |
| 5 | finisher | add-ons from `PLAN.md` (core, conditioning, balance, mobility...). (Balance from 60 never fires: the age band is fixed at 18 to 39) |

## The clock (every rest counted)

- Straight sets: the sum of sets x (work + rest), minus the very last rest.
- Supersets: per round, the work of each move + 15 s between moves + the rest after the round.
- Timed formats (warm-up, AMRAP, EMOM, for time, intervals, runs): their minutes.
- Every block after the warm-up: +1 min changeover.
- Work time: about 4 s a rep, 15 s minimum, a set "per side" counts double, a time written on the line is that time.

## The minutes are a ceiling

`engine/build.py fit` cuts in this order until the clock is within 3 minutes of the minutes asked: optional finishers · the last accessory · accessory sets to 2 · whole accessory blocks · second-lift sets by one · the balance block to 4 min · the warm-up to 5 min. If the minutes are under the program's normal range, its **express** session is used. `engine/sheet.py` refuses any sheet more than 3 minutes over.

## The sheet (one page, A4 or Letter)

1. The title, date, program, block, week and the dose of the day.
2. **The score to beat**, in a box, and **why this session today**, in two lines.
3. "First time" instructions once, at the top, with a star on each line it applies to.
4. Every line: the exercise (a tap opens a demonstration search), its one cue, sets x reps, load, effort, rest, a tick box per set.
5. Every block: its computed minutes and how the rest works.
6. What to do if energy drops, the lines to fill in afterwards, the total time.
7. The footer: "General guidance, not medical advice. Stop if anything feels wrong."

**Rendering** (no install, ever): Playwright if already there, then any Chrome, Edge, Chromium or Brave on the machine, then a plain built-in PDF writer. If the page would spill, the type is tightened in steps; content is never cut.
