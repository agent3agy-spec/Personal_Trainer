# modules · the add-ons

_This folder owns: the pieces a week borrows. The composer (`../06_BUILD.md`) uses a module in two ways: as **days** of a component (`run-race`, `easy-running`), or as a **finisher**. A finisher is either a **goal finisher** (`goal_modules` in the plan: a component too small for a whole day, or core after a birth), which the clock cuts last and shrinks to a minimum dose first, or a **nice-to-have** (`modules`: the program's own core or mobility), which the clock cuts first. A second goal is never served by stacking a second full program in the same session (research/02, the hybrid rule)._

| module | when | what it adds |
|:-|:-|:-|
| `core` | finisher; the goal finisher for a lifting share too small for a day, and after a birth (never cut before the others) | 2 core moves, 2 to 3 rounds |
| `conditioning` | the goal finisher for fat loss, leaner, fitness and "a bit of everything" on lifting days; never after a run or a metcon | 6 to 10 min of intervals on whatever cardio machine is there, or bodyweight; 6 min minimum dose |
| `balance` | finisher, mandatory from 60 (the age band is fixed at 18 to 39, so this never fires; kept for the record) | 3 balance moves, about 6 min (WHO 2020, Sherrington 2019) |
| `mobility` | finisher | 5 to 8 min for the day's joints |
| `locomotion` | finisher, or the first 2 to 4 weeks for a deconditioned person | GMB-style crawls |
| `hyrox-stations` | the goal finisher for a HYROX share too small for a day, or when no HYROX day fits the kit; never stacked on `hyrox-prep-4`, whose sessions already hold the stations | one station piece, scored |
| `skill-blocks` | finisher for the `skills` goal (no longer offered: bodyweight skill training is out of scope; kept for old profiles) | handstand, pull and pistol skill work |
| `easy-running` | easy cardio days (a conditioning share on 4 days or more, spare days for someone who enjoys running), or a short easy run as a goal finisher | an easy run by the talk test (a bike when running is out), volume rule `run_volume` |
| `run-race` | the running days of a blend next to a lifting lead: 1 day the long run, 2 easy and long, 3 easy, quality and long | easy run, long run, one quality run, Daniels caps; the long run is protected for an event |
| `travel` | replaces the day | a bodyweight session when the main block cannot be filled; nothing progresses |

## The json block of a module

```
{"id": "core", "name": "Core finisher", "when": "finisher",     finisher · extra_day · replace
 "minutes": 6,                                                   its usual cost on the clock
 "session": SESSION}                                             finisher and replace modules
```

An `extra_day` module carries `"sessions": {"easy": SESSION, "long": SESSION, "quality": SESSION}` and `"order": ["easy", "long", "quality"]`, and the engine runs them in that order on the days a person trains beyond what their program uses. SESSION, BLOCK and SLOT are exactly as in `../programs/README.md`.
