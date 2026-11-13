# modules · the add-ons

_This folder owns: the pieces a program borrows. A secondary goal is served by a module, never by stacking a second full program (research/02, the hybrid rule)._

| module | when | what it adds |
|:-|:-|:-|
| `core` | finisher | 2 core moves, 2 to 3 rounds |
| `conditioning` | finisher | 6 to 10 min of intervals on whatever cardio machine is there, or bodyweight |
| `balance` | finisher, **mandatory from 60** | 3 balance moves, about 6 min (WHO 2020, Sherrington 2019) |
| `mobility` | finisher | 5 to 8 min for the day's joints |
| `locomotion` | finisher, or the first 2 to 4 weeks for a deconditioned person | GMB-style crawls |
| `hyrox-stations` | finisher in a HYROX block | one station piece, scored |
| `skill-blocks` | finisher in calisthenics | handstand, pull and pistol skill work |
| `easy-running` | extra days | an easy run by the talk test, volume rule `run_volume` |
| `run-race` | extra days, for a 5 km to half marathon goal next to strength | easy run, long run, one quality run, Daniels caps |
| `travel` | replaces the day | a bodyweight session when the main block cannot be filled; nothing progresses |

## The json block of a module

```
{"id": "core", "name": "Core finisher", "when": "finisher",     finisher · extra_day · replace
 "minutes": 6,                                                   its usual cost on the clock
 "session": SESSION}                                             finisher and replace modules
```

An `extra_day` module carries `"sessions": {"easy": SESSION, "long": SESSION, "quality": SESSION}` and `"order": ["easy", "long", "quality"]`, and the engine runs them in that order on the days a person trains beyond what their program uses. SESSION, BLOCK and SLOT are exactly as in `../programs/README.md`.
