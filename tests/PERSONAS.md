# The persona runs · 13 nov 2026

_Ten fictional people run end to end through the real skill and engine, each in a throwaway copy, by five independent subagents playing both the trainer and the person. Every finding below was fixed, and the ones that are code have a test in `test_engine.py` (class `PersonaRegressions`). Run them again before every release: brief each person to a fresh agent with the skill and this table._

| person | what it covered | what it found (all fixed) |
|:-|:-|:-|
| Léa, 34, French, never trained, home with bands and 8 kg dumbbells, fat loss, hates running | French sheets, home filter, fixed weights, fat-loss scope | "few changes" logs skipped unmentioned lifts · the home preset had a bench · rounding ignored her own weights · one owned weight still said "find your weight" |
| Jay, 19, first week, wants a max test and 7 days of 2 hours | holding the rules without a lecture | a result for a lift not in the session vanished · a missed session closed the week |
| Marcus, 27, powerlifting meet in 16 weeks, knows his numbers | known numbers, RPE program, goal change | RPE line overprinted the load · "as written" lowered his estimates · first sessions cut to 2 sets for an experienced lifter · a bodyweight swap in an RPE slot · estimates lost on a program change |
| Ben, 45, chest pain when active | the screen stop and the push back | re-answering "none" undid a stop · the chest-pain flag never reached the sheet |
| Aiko, 41, CrossFit, HYROX doubles, shoulder pain in week 2 | hybrid, stations, pain mid-block | **shoulder exercises passed a shoulder limit** (bank under-tagged) · HYROX filtered out for an experienced athlete · benchmark scores compared wrongly · hard cardio served the day after intervals |
| Sam, 38, runs 25 km a week, sub-50 10 km plus strength | running with lifting | running not seeded from his usual run · logged longer runs ignored · the second goal under-weighted |
| Giorgio, 69, Italian, replaced knee (cleared), fear of falling | 60 and over, a cleared old injury | a cleared knee wiped out all leg work · pain over 3 lost when a limit existed · the falls-programme line never said |
| Priya, 30, 7 months postpartum, one 12 kg kettlebell, 20 minutes | the postpartum path, express sessions | **impact moves reached a postpartum user** · Simple and Sinister jumped to the full dose on session 2 · no pelvic-health line · no way to rebuild after an audit |
| Tom, 22, Spanish, park bars, first muscle-up | calisthenics ladders | no muscle-up line in the bank · ladders stalled when the next step needed kit · `/train goals` wiped ladder progress |
| Noor, 29, wheelchair user, bands and 5 kg dumbbells, travels | the seated filter, travel days | the warm-up ignored seated and pain · a travel day ate the next session · no honest line about what seated covers |
