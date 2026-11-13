# 07 · Cycle · the week, the block, the deload, the spacing

_This file owns: how sessions follow each other, when a week and a block close, deloads, how running and lifting share a week, and the coach's habits around them (the starting numbers, the first milestone, the weekly check-in, the missed week and the streak, personal bests, the block review, the taper). Code: `engine/build.py` (`refill`, `pick_session`, `week_info`, `taper_session`), `engine/logbook.py` (`advance`, `deload_triggers`, `records`, `new_records`), `engine/coach.py`._

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

## The coach's habits (phase E, 13 nov 2026, research/07 Part 4)

A plan is half of coaching; the other half is the loop around it: a baseline, a goal with a date, feedback against it, a weekly plan, and a review [Michie 2009, McEwan 2016: checked in research/07]. None of these blocks a session: they are turns the coach offers beside it (`plan.py status` → `coach.next_turn`, in this order: block review, after an event, weekly check-in, starting numbers). Everything is kept in the plan's data block under `coach` (`me/PLAN.md`), and follows the person across a change of plan.

### The starting numbers (`coach.battery`, `plan.py tests`)

Week 1 and 2 of every block until done or skipped, and again after 4 weeks or more off. Never in a taper. **Never a max test.** Two short tests at most, picked for the person:

| test | when it is picked | kept as |
|:-|:-|:-|
| 2 km run, even pace | running, HYROX or hybrid, and they can run 30 minutes | time, lower is better |
| 12 minutes, walk and run | the same, not yet running 30 minutes; or fat loss and fitness outdoors | metres |
| 1000 m row, even pace | a rower, and mixed fitness, HYROX, fat loss or health | time |
| push-ups to form failure | everyone, unless the shoulder, elbow or wrist is left out (then a plank hold, unless the low back is) | reps |

The lifts are never tested: their weights logged in week 1 of a block are the baseline, read from the log (`coach.lift_changes`, the estimated max of each main and second lift). No impact test when impact is off, nothing on a region that is left out [the field tests: research/07 Part 1, believe for the exact choice].

### The first milestone (`coach.milestone`, at `choose` and at every block review)

Set at the end of the first block, clamped to 4 to 6 weeks. Two parts, both very likely: **sessions**, three quarters of their days over those weeks, and **one number**: the first main lift about 10 percent above week 1 (none or novice), 5 (intermediate) or 2.5 (advanced), or, without a lift, the engine test about 5 percent better (3 for intermediates). Checked after every log and at the review: hit, on track, behind (one session this week puts you back on pace), or missed, said without blame ("the next one starts from where you are") [the numbers: believe, research/07].

### The weekly check-in (`coach.checkin`, `plan.py checkin`)

Due when a week closes. Three questions: what got in the way (`core.BARRIERS` or nothing), energy (low, ok, good), which days next week. It feeds the next week (`state.next_week`, 9 days at most): low energy, stress or pain → an easier week (no all-out sets, one set fewer on the extra moves) · time → sessions 15 minutes shorter by default · the days are said on the home page. Two weeks short on time in a row → fewer days is offered, never imposed [implementation intentions with barrier planning: Bélanger-Gravel 2013, checked in research/07].

### The missed week and the streak (`coach.back_tier`, `coach.streak`)

| days since the last session | the next session |
|:-|:-|
| 7 to 13 | a light dose (`04_INTENSITY.md`), the next in the rotation, "welcome back" once |
| 14 to 27 | loads about 15 percent lighter, then one more easy session |
| 28 or more | the same, and the starting numbers again that week |

**The streak** counts weeks with at least one session. One empty week is a rest week: it pauses the streak and never resets it; two empty weeks in a row end it. One missed session changes nothing. The copy never mentions a miss twice [Lally 2010, Marlatt: seen in research/07].

### Personal bests (`logbook.new_records`, `logbook.records`)

Read from the log after every session, never stored twice: a heavier best on a main or second lift (the estimated max from weight and reps), or more reps at a weight done before. A first time on a lift is the starting point, never a record. The read-back leads with it.

### The block review (`coach.block_review`, `plan.py blockreview`)

When a block closes, or 1 to 21 days after their event: the block in plain numbers (sessions of planned, each lift's change since week 1, the tests against the first time, the milestone, what got in the way), wins first, then one turn: what went well, and the next block. The answer adjusts the next block:

| answer | what changes |
|:-|:-|
| keep going | nothing; a new milestone |
| a bit easier · a bit harder | one set fewer or more on the extra moves for the whole block (`state.block_adjust`) |
| shorter · longer | the minutes, 15 less or more |
| fewer · more days | the days, then the plan is matched again |
| a new focus | the priority, then the same plan is chosen again (progress kept) |
| move on | the program's `graduates_to`, chosen |

### The taper (`coach.taper`, `build.taper_session`)

The last weeks before `event.date` cut volume and keep intensity [Bosquet 2007 meta-analysis on tapering, Mujika: believe, not re-checked this session]. Sized to the event:

| event | taper | volume, from the final week back |
|:-|:-|:-|
| 5K or 10K, HYROX | 1 week | 60 percent |
| half marathon, a lifting meet | 2 weeks | 50, 70 percent |
| marathon | 3 weeks | 50, 65, 80 percent |

Sets and run minutes take that share (a run never under 15 minutes); weights, effort and the main lifts stay; hard finishers go; nothing is added to fill the time; no progression is logged until after the event; no tests. The event day is a rest day. After it, the block review asks how it went and what is next.
