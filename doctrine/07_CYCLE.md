# 07 · Cycle · the week, the block, the deload, the spacing

_This file owns: how sessions follow each other, when a week and a block close, deloads, and how running and lifting share a week. Code: `engine/build.py` (`refill`, `pick_session`, `week_info`), `engine/logbook.py` (`advance`, `deload_triggers`)._

## Sessions in order, never by weekday

The program's layout for their number of days is a queue (A, B, A...). The next session is the first one in the queue. Missed days break nothing: the next session is simply the one due. Extra days beyond what the program uses take the running add-on in `PLAN.md`, or rest.

## The week and the block

- **A week closes** after as many logged sessions as their days, or 9 days after it started, whichever first.
- **A block** is the program's `block_weeks`, then a deload week if the program has one. Then block + 1: main lifts stay, accessories may rotate.
- **Hypertrophy programs** step effort through the block ("3 left" to "1 left" or "0 to 1") and add a set to accessories in later weeks (the program's `meso`) [RP model, believe numbers].
- **5/3/1** runs its own waves per lift (5s, 3s, 5/3/1, deload) and moves the training max each cycle [checked].
- **Linear programs** have no deload week: three misses on a lift drop it 10% [checked].

## Early deload, any program

Any two of: energy 5 or less in 3 of the last 4 sessions · the same session's score down twice in a row · sore, flat or in pain three sessions in a row. The next week is a deload: half the sets, about 10% lighter, "4 left" [believe, adapted from Adam's trainer].

## Spacing, and running with lifting

- Hard cardio or a hard run in the last 24 h: no heavy-legs or power session that day if another session in the queue fits [Schumann 2022, Petré 2021: checked].
- Same day: lift first, run after, at least 3 hours apart; better a day apart [checked].
- When leg muscle is the goal, extra conditioning prefers the bike or the rower to running [Wilson 2012, believe direction].
- Running volume: hold a weekly volume about 3 weeks, then about +10%; never more than about 30% over two weeks [Buist 2008, Nielsen 2014: snippet, band B].
- Easy runs by the talk test (full sentences), never by a formula heart rate.
