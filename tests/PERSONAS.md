# The persona runs

_Ten fictional people run end to end through the real skill and engine, each in a throwaway copy, by independent subagents playing both the trainer and the person. Every finding that is code has a test in `test_engine.py` (class `PersonaRegressions`). Run them again before every release: brief each person to a fresh agent with the skill and this table._

**Scope (13 nov 2026, `doctrine/00_MISSION.md`):** adults 18 to 40, in a gym, a home gym with real kit, or outdoors for running and cardio. Age is never asked, so a persona's age is only for the agent playing them.

## The ten to run

| person | what it covers | last run |
|:-|:-|:-|
| Léa, 34, French, never trained, home gym with bands and 8 kg dumbbells, fat loss, hates running | French sheets, a home gym, fixed weights, fat-loss scope | 13 nov 2026, findings below |
| Jay, 19, first week, wants a max test and 7 days of 2 hours | holding the rules without a lecture | 13 nov 2026 |
| Marcus, 27, powerlifting meet in 16 weeks, knows his numbers | known numbers, RPE program, goal change | 13 nov 2026 |
| Ben, 36, chest pain when active | the screen stop and the push back | 13 nov 2026 (then 45; the age is not asked, nothing else changes) |
| Aiko, 34, CrossFit, HYROX doubles, shoulder pain in week 2 | hybrid, stations, pain mid-block, the shoulder exclusion through warm-up and finishers | 13 nov 2026 (then 41) |
| Sam, 38, runs 25 km a week, sub-50 10 km plus strength | running with lifting | 13 nov 2026 |
| Noor, 29, wheelchair user, home gym with bands and 5 kg dumbbells, travels | the seated filter, travel days | 13 nov 2026 |
| Elif, 31, ACL reconstruction cleared by her physio, full gym, muscle | a cleared old injury trained with care, no impact on it | not yet run (replaces Giorgio) |
| Priya, 30, 7 months postpartum, home gym with dumbbells and a bike, 20 minutes | the postpartum path, express sessions | not yet run in this form (replaces the kettlebell-only version) |
| Tom, 24, Spanish, CrossFit box, all-round fitness, cannot do a pull-up yet | the CrossFit-style plan in a gym, scaling inside a timed workout, Spanish sheets | not yet run (replaces the park calisthenics version) |

## What the 13 nov 2026 run found (all fixed)

| person | what it found |
|:-|:-|
| Léa | "few changes" logs skipped unmentioned lifts · the home preset had a bench · rounding ignored her own weights · one owned weight still said "find your weight" |
| Jay | a result for a lift not in the session vanished · a missed session closed the week |
| Marcus | RPE line overprinted the load · "as written" lowered his estimates · first sessions cut to 2 sets for an experienced lifter · a bodyweight swap in an RPE slot · estimates lost on a program change |
| Ben | re-answering "none" undid a stop · the chest-pain flag never reached the sheet |
| Aiko | **shoulder exercises passed a shoulder limit** (bank under-tagged; the full region audit followed, class `RegionLimits` in `test_engine.py`) · HYROX filtered out for an experienced athlete · benchmark scores compared wrongly · hard cardio served the day after intervals |
| Sam | running not seeded from his usual run · logged longer runs ignored · the second goal under-weighted |
| Noor | the warm-up ignored seated and pain · a travel day ate the next session · no honest line about what seated covers |

## Retired, out of scope since 13 nov 2026

Their findings stay fixed and their tests stay where the code still runs: the cleared-injury care rule (`test_care_region_keeps_legs`) and the postpartum impact gate (`test_postpartum_no_impact_until_ok`) cover every program.

| person | why retired | what it found (all fixed) |
|:-|:-|:-|
| Giorgio, 69, Italian, replaced knee, fear of falling | over 60 | a cleared knee wiped out all leg work · pain over 3 lost when a limit existed · the falls-programme line never said |
| Priya with one 12 kg kettlebell | a kettlebell-only plan | **impact moves reached a postpartum user** · Simple and Sinister jumped to the full dose on session 2 · no pelvic-health line · no way to rebuild after an audit |
| Tom on park bars, first muscle-up | bodyweight-only skill training | no muscle-up line in the bank · ladders stalled when the next step needed kit · `/train goals` wiped ladder progress |
