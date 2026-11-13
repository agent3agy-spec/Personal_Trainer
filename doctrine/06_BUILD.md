# 06 · Build · the session, the clock, the sheet

_This file owns: the composer (how a week is made from the person's outcomes), their own routine (the improve path), the shape of a session, the time math, the cut order and the fill, the coach's eye, and what the sheet shows. Code: `engine/compose.py`, `engine/improve.py`, `engine/build.py`, `engine/eye.py`, `engine/sheet.py`._

## The composer (phase D, 13 nov 2026)

**The person says what they want; the trainer builds the week.** A profile is a blend of up to three outcomes with shares (`02_INTERVIEW.md`). `engine/compose.py` turns it into components and gives each one days in proportion to its share. The person never picks a method, and no method name reaches the sheet, the plan name or a note.

| component | what serves it | from |
|:-|:-|:-|
| lifting | the lead program when the main outcome is a lifting one, else a whole body plan (`health-baseline-2to3`, `muscle-fullbody-3`, `strength-lp-3`, `strength-531-beginners-3`), the best fit for their goal and kit | `programs/` |
| running | the lead program for a running event, else `run-race` days (1 day: the long run · 2: easy and long · 3: easy, quality, long), or the couch to 5K session for someone who cannot run 30 minutes yet | `programs/`, `modules/run-race.md` |
| HYROX | the lead program, else `hyrox-prep-4` sessions (1 day: the compromised run · 2: intervals and compromised · 3: easy, intervals, compromised) | `programs/hyrox-prep-4.md` |
| mixed conditioning | the lead program, else `functional-gpp-3to5` sessions in turn | `programs/functional-gpp-3to5.md` |
| conditioning (fat loss, leaner, a bit of everything) | always the protected `conditioning` finisher on the lifting days; one easy cardio day (`easy-running`) when its share earns a whole day on 4 days or more | `modules/` |

**How the days are shared** (`compose.allocate`): each outcome follow-up has a recipe (`compose.RECIPE`: leaner is lifting 70 and conditioning 30, "a bit of everything" lifting 60 and conditioning 40, fitness and cardio mixed 60 and conditioning 40, every other follow-up one component). The lead program's family covers the components it already serves in its own week (`compose.COVERS`: HYROX covers running, hybrid covers lifting and running). The days left go to the other components by largest remainder of their shares. The lead keeps at least 2 days (all of them on a 2 day week). A runner on 4 days or more keeps one short full body strength day. A component left without a whole day becomes a goal finisher. Example: muscle 60, running 40 on 5 days is 3 lifting days and 2 running days; on 3 days, 2 and 1.

**A component that nothing fits** (no kit, no skill, a limit) gives its days back to the lead program, in the lead's own layout, and comes as its finisher instead; the plan says so in one line.

**The order of the week** spreads the other components between the lead's sessions (`compose._interleave`): lifting, running, lifting, running, lifting. Every stream keeps its own rotation, so every session of every component comes round in turn (`build.refill`).

**The lead program is chosen for the days the composer gives it** (`match.filters` reads `compose.lead_days`), so a 60/40 week on 4 days looks for a 2 or 3 day lifting plan, never a 4 day one squeezed.

**Never squeezed.** A program's layout for N days has at most N sessions. Only whole body programs may rotate more sessions than days (`"rotates": true`, with the `rotation_note` the plan says: every session trains the whole body, so nothing is lost). A program with fewer sessions on fewer days states what is lost in `layout_notes` (HYROX on 3 days: the easy run is the session left out). `match` refuses a squeezed layout and `checks.py template` refuses one in a file.

**Weekly targets.** A priority area (`priority`, up to two) gets about 6 extra direct sets a week (`compose.PRIORITY_WEEKLY`, research/01 dose response), spread over the lifting sessions: sets added to an accessory of the same pattern that already trains it, up to 5, else a new accessory from the bank in a "Priority" block, present from session 1. The coach's eye can add a target too (pulling to balance pressing, a muscle group under 8 sets for a muscle goal). Every added set is marked and the clock cuts it late (below).

**Keep it going** gets a real plan: the lead program for its follow-up, plus a challenge that changes every block of about a month (`compose.CHALLENGES`), printed in the why line of every sheet. **A marathon** gets one too: mostly easy running, one quality run, a strength day from 4 days a week when there is a gym, and the protected long run (below), growing about 10 percent every 2 weeks up to about 3 hours (half marathon: every 3 weeks up to 2 hours).

## Their own routine (phase F, 13 nov 2026)

**Someone who already trains keeps their routine.** On the improve path (`02_INTERVIEW.md` Round 2b) `plan.py adopt` turns what they said into `me/PROGRAM.md`, a program file of their own in the schema of `programs/README.md` (id `mine`, family `own`): one session per day label, in their order (`layouts`), the first exercise of a day as the main lift, the next compound as the second lift, the rest as one block in their order, each exercise with their sets and reps. Every slot is marked `theirs`. An exercise not in the bank is kept by its own name (`own_name`) and tracked like the nearest bank row of the same movement for weights and safety; the sheet prints their name and "your usual form". Run days and cardio days take the easy, quality and long runs of `run-base-3to5`; class days stay theirs and are said, never written. A **parent program** of the same split and goal (`improve.parent_of`) lends the block length; it is never run. The same answers give the same file, byte for byte.

**What runs on it, unchanged:** the load rules and the first outing (`05_LOADS.md`), progression (a fixed number of reps adds weight, a range adds reps then weight), logging, records, the readiness dose (a light day, a rest day), the coach's habits (tests, milestone, check-in, block review, the missed week, the taper) and the warm-up.

**What never changes without a yes.** Every path where the engine would change their routine by itself is a proposal instead:

| the engine would | in their routine |
|:-|:-|
| add priority sets or a priority move | the `priority` proposal |
| fill a short session with sets, a variation, core, conditioning or mobility | nothing: no fill |
| cut accessories or sets to fit the minutes | the `time_fit` proposal (trim named sets until the day fits); until then the sheet takes the time their day needs and says so |
| add pulling or a low muscle group from the coach's eye | the `pull_volume` and `group_low` proposals |
| swap a move for a standing limit | the `limit` proposal (a version that leaves it alone); until then their move stays, with a line on the sheet: go by feel, stop the set if it hurts |
| switch a move their place cannot do | the `kit` proposal; on the day, the nearest move is used and the sheet says "today only" |
| climb to the harder step of a bodyweight or fixed weight move | the `harder` proposal; the sheet says the next step is waiting |
| add an easier week, or a goal finisher | the `deload` and `conditioning` proposals |
| change a stalled lift | the `stall` proposal (a rep range on a fixed number of reps, else one set fewer for a block) |
| ask for less on a tired routine | the `recovery` proposal (one set less on the extra moves) |

**The day still decides the day, and says it.** Pain today, the screen's flags (pregnancy, after a birth), a lift that needs coaching, and a place without the kit change that one session only, with a line on the sheet; their routine file is untouched. A shorter day they ask for ("30 minutes today") is cut by the normal order, said, and the next session is their full day again.

**A proposal** (`improve.proposals`, `plan.py improve`) is what (in plain words, with their numbers), why (one line) and the exact change. The order: limit and kit first (about their body or their kit, always shown), then the clock, recovery, the goal, a priority, pulling, a low group, a stall, the next step, the easier week. **At most two others a block**, counted with the ones answered this block; the rest wait for the next block. **Yes** (`plan.py improve accept <id>`) applies it from five operations (sets, a new move, a swap, a rep range, a finisher or an easier week), adds it to "What the coach changed, with your yes" in `me/PROGRAM.md` and `me/PLAN.md`, and keeps loads under the same slot keys. **Keep mine** (`decline <id>`) is remembered: it is not asked again for two blocks, unless what it rests on changed (the goal, the minutes, a priority, an event, a limit, the place). A lock from "what must stay" is said on the card: "you said your exercises stay: only if you want".

**Marks.** The 2 to 3 pulling sets for every pressing one and the 6 direct sets for a priority are [believe] ratios for a proposal's wording; the 8 to 10 weekly sets per group is [checked] (Schoenfeld 2017, Pelland, `research/01`). Not built yet from `research/09`: the effort question (R7), their working weight entering without the 10 percent discount, undo of an accepted change, the effort ramp across a block.

## The shape

| # | block | rule |
|:-|:-|:-|
| 1 | warm-up, 6 to 8 min | written by the engine: 3 min raise on whatever cardio is there, 2 mobility moves for the day's joints, ramp sets of the first main lift |
| 2 | main block | the program's main work, with the score to beat. **Never cut** |
| 3 | second lift | the program's secondary work, if any |
| 4 | accessories | the program's slots, filled from the bank, supersets where the program says |
| 5 | finisher | the goal finishers of the composer first (`goal_modules`: conditioning for fat loss, a HYROX station piece, a short easy run, core after a birth), then the program's nice-to-have add-ons (`modules`: core, mobility). Finishers go on lifting sessions; a run day gets mobility only, and one hard piece a session at most. (Balance from 60 never fires: the age band is fixed at 18 to 39) |

## The clock (every rest counted)

- Straight sets: the sum of sets x (work + rest), minus the very last rest.
- Supersets: per round, the work of each move + 15 s between moves + the rest after the round.
- Timed formats (warm-up, AMRAP, EMOM, for time, intervals, runs): their minutes.
- Every block after the warm-up: +1 min changeover.
- Work time: about 4 s a rep, 15 s minimum, a set "per side" counts double, a time written on the line is that time.

## The minutes are a ceiling and a target

**The cut** (`build.fit`), until the clock is within 3 minutes of the minutes asked: the nice-to-have finishers · accessories that serve no target, then their sets to 2, then whole blocks · secondary sets down to half the program's · **only then** the goal finisher shrinks to its minimum dose (6 minutes, or 2 sets) · the easy walk of a health session by 5 minutes · priority sets down to 2, then priority moves · secondary sets to 1 · the goal finisher itself, said with the minutes it needs · balance to 4 min · the warm-up to 5 min. The main block is never cut. If the minutes are under the program's normal range, its **express** session is used.

**The long run is protected.** A run session is never swapped for the express one. For a running event the long run takes the minutes it needs: the sheet says "Long run day: about N minutes" and asks them to put it on the day they have the time, and `session.minutes` carries the real figure. Any other run over the minutes is trimmed to fit, never under 15 minutes, and the long run is never shorter than the week's easy run.

**The fill** (`build.fill`): a session more than 10 percent short of the minutes gets, in order and only while it stays inside them, a set more on the priority work, the accessories and the secondary lifts · a second variation of the session's first lift (lifting goals) · core · conditioning (fitness and fat-loss goals, never after a run or a metcon) · easy cardio to finish, 10 to 20 minutes, on run days and for fitness or fat loss · mobility · then accessories up to 5 sets. What still cannot be filled is reported by the coach's eye, never hidden. **No fill** on a taper day, and a very sore day or an easier week is short on purpose: the eye does not report those minutes (`07_CYCLE.md`, `04_INTENSITY.md`).

`engine/sheet.py` refuses any sheet more than 3 minutes over.

## The coach's eye (`engine/eye.py`)

Run at `plan.py choose` on a whole week built for real (energy 7, the usual minutes), and on every `plan.py build`. Each check returns `ok` and a plain line; a failed check fixes the plan or is reported in `say_also`, `coach_eye` and `PLAN.md`. Never silent. **In their own routine the eye fixes nothing by itself:** its pulling and volume checks are proposals (above), and a session shorter than their minutes is not reported: it is as long as they wrote it.

| check | rule | on fail |
|:-|:-|:-|
| days | the lead's sessions fit its days, or it is a whole body rotation | refused at match |
| minutes | every session within 90 percent of the minutes and at most 3 over (a protected long run day is said instead) | reported |
| priority | at least 4 added sets a week on the area, in at least 2 sessions | reported |
| push and pull | pulling sets at least equal to pressing sets (1 set of slack) | a pulling target (4 to 6 sets a week) is added and the week rebuilt |
| volume | a muscle goal: chest, back, quads, hamstrings and glutes, shoulders at 8 or more hard sets a week | a target of 4 sets for up to two groups |
| key quality | strength: 2 heavy sessions · running event: a long run · HYROX: running and a station piece · mixed: a conditioning piece per mixed day | reported |
| second goal | every component of the blend reaches the week (its days come round, its finisher survives the clock) | reported |
| a session | the minutes, and the goal finisher still there | reported with the session |

## The sheet (one page, A4 or Letter)

1. The title, date, the plan's plain name (`plain_name`, e.g. "Strength 2 days · HYROX 1 day", never a method name), the week and the dose of the day.
2. **The score to beat**, in a box, and **why this session today**, in two lines (in a taper, it says so).
3. "First time" instructions once, at the top, with a star on each line it applies to.
4. Every line: the exercise (a tap opens a demonstration search), its one cue, sets x reps, load, effort, rest, a tick box per set.
5. Every block: its computed minutes and how the rest works.
6. What to do if energy drops, the lines to fill in afterwards, the total time.
7. The footer: "General guidance, not medical advice. Stop if anything feels wrong."

**Rendering** (no install, ever): Playwright if already there, then any Chrome, Edge, Chromium or Brave on the machine, then a plain built-in PDF writer. If the page would spill, the type is tightened in steps; content is never cut.
