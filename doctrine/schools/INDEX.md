# schools · the map of what the trainer knows

_This file owns: which schools the trainer knows, what each prescribes, for whom, the evidence level, and how v1 serves it. A program the trainer can run lives in `../programs/`; a school can sit here without a program, and the row says why. The rules a program follows live in its own file and in `engine/`, never here._

**Almost no named program has been tested head to head against another.** The trials and meta-analyses test principles: weekly volume, load range, how close to failure, frequency, progressive overload, autoregulation, and the concurrent training rules. A named program is a package of those principles that fits a goal, a schedule and a taste. So the principles below are the A layer: they apply inside every program, and they win when a school's tradition disagrees with them.

"Objective" means a fixed, written rule picks the program from the person's facts, run by code and shown with its score, never a freehand choice. See `../03_MATRIX.md`.

**Evidence levels:** **A** the core principle is backed by meta-analyses or RCTs · **B** a coach system built on A principles, the program itself untested · **C** tradition or anecdote · **G** a public health guideline built on systematic reviews.

**Marks on a claim:** [checked] confirmed this session in an abstract, a PubMed record or an official excerpt, never a full text (page fetches were blocked, see `../../research/README.md`) · [snippet] or [seen] confirmed in a search engine's extract of the named source · [believe] from memory or a secondary site, listed under "To verify" below · [inferred] reasoned from checked parts.

## The principles

| rule | evidence | source |
|:-|:-|:-|
| **Weekly volume for muscle.** 10+ hard sets per muscle per week beat fewer [checked: Schoenfeld 2017, data reach about 10]; more keeps helping with diminishing returns and no clear plateau [checked direction: Pelland]. Start at 8 to 12 and a ceiling near 20 are coach consensus [believe]. Indirect sets count 0.5 [checked direction: Pelland] | A and B | Schoenfeld, Ogborn, Krieger 2017 · Pelland et al. 2025, Sports Med, doi 10.1007/s40279-025-02344-w |
| **Frequency.** For muscle, frequency adds little once weekly volume is equal [checked]. 2x a week is the default because it keeps one session's sets for a muscle under about 10 [believe]. For strength, train the target lift more often [checked]. A 1x bodypart split is legal for muscle, never for strength | A and B | Pelland et al. 2025 · Schoenfeld 2016 |
| **Load range.** Strength needs regular heavy work (about 1 to 6 reps, 80% of 1RM and up) on the target lifts. Muscle grows across about 6 to 30 reps when sets end close to failure [checked] | A | Schoenfeld et al. 2017 JSCR, PMID 28834797 |
| **Proximity to failure.** Muscle sets end at 0 to 3 reps in reserve; strength work can sit at 2 to 4 RIR with no loss; true failure adds little and costs fatigue [checked] | A | Refalo 2023 · Robinson 2024 |
| **Long muscle length.** Prefer overhead triceps work, seated leg curls, deep squats and RDLs, incline curls [checked, small trials] | A | Maeo 2021, 2022 · Pedrosa 2022 |
| **Effort reading.** RIR is asked at the end of a set. People underestimate reps left by about one and guess better near failure and in low rep sets [checked]; so novices aim at 3 to 4 RIR [inferred] | A | Halperin 2022 · Zourdos 2016 |
| **Autoregulation.** RPE or RIR loading is at least as good as fixed percentages for strength, sometimes better [checked] | A | Helms 2018 · Hickmott 2022 · Zhang 2021 |
| **Novice progression.** Full body, 2 to 3 days, 8 to 12 rep loads, add 2 to 10% when the target is beaten by 1 to 2 reps [checked] | G | ACSM 2009 position stand (the 2026 update is read at milestone 2) |
| **Concurrent training.** Cardio does not cost muscle or max strength for most people; explosive strength, and max strength in trained lifters, suffer when both are crammed into one session. Separate hard legs and hard running by 3 h or more, better by a day; prefer bike or rower for extra conditioning when leg muscle is the goal [snippet: Schumann 2022, Petré 2021; seen: Wilson 2012] | A | Schumann 2022 · Petré 2021 · Wilson 2012 |
| **Running load.** The 10% rule did not protect novices in a trial [seen: Buist 2008]. Hold a new weekly volume about 3 weeks [seen, secondary: Daniels]; stay under about 30% over two weeks, a soft band from a cohort that missed significance, p = .07 [seen: Nielsen 2014] | A and B | Buist 2008 · Nielsen 2014 · Daniels |
| **Easy aerobic work.** Prescribed by the talk test (full sentences) or RPE 3 to 4, never by a formula heart rate [seen] | A | talk test validity · Seiler (research/03) |
| **Women.** Same principles as men, no "toning" special case. No planning by menstrual cycle phase; adjust day to day by readiness [checked] | A | Roberts 2020 · McNulty 2020 · Colenso-Semple 2023 |
| **Older adults.** Strength plus balance plus some fast intent, multicomponent work 3+ days a week; exercise cuts the rate of falls by 23% [checked] | A and G | WHO 2020 · Sherrington 2019 Cochrane |
| **Fat loss.** The deficit is mostly diet. Exercise alone gives about 2 kg, matters most for keeping weight off, and lifting keeps muscle while dieting [checked] | A | Swift 2014 · Donnelly 2009 · Sardeli 2018 |
| **Health floor.** 150 to 300 min a week of moderate aerobic activity (or 75 to 150 vigorous) plus strength 2+ days a week [checked] | G | WHO 2020 · UK CMO 2019 |

Marks corrected against the research: concurrent training is [snippet] (research/02 opened no page), running load and easy aerobic work are [seen] (research/03's mark for a search extract).

## Hypertrophy

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| Schoenfeld, the evidence school (Schoenfeld volume and frequency · Schoenfeld 2017 load meta-analysis) | 10+ hard sets per muscle a week, 2x a week, 6 to 30 reps near failure, compounds plus isolation | everyone, the fallback | A | the principles layer above · `muscle-fullbody-3`, `muscle-upperlower-4`, `muscle-ppl-6`, `home-fullbody-2to4` |
| Pelland 2025 frequency finding (study) | equal weekly volume, frequency barely changes growth; fractional set counting | the case for a 1x split for muscle only | A | `muscle-bodypart-5` |
| Robinson 2024 (study) | growth improves as sets end closer to failure | every hypertrophy program | A | `powerbuild-phul-4` |
| Renaissance Periodization (Israetel), the RP mesocycle model | volume landmarks MEV, MAV, MRV; a 4 to 6 week mesocycle from near MEV, adding sets; RIR from about 3 to 4 down to 0 to 1; a deload at about half the sets [believe, RP site unreachable] | intermediate+, 4 to 6 days | B | the accessory ramp of `muscle-fullbody-3`, `muscle-upperlower-4`, `muscle-ppl-6`, `muscle-bodypart-5`, `powerbuild-phul-4` |
| Jeff Nippard: Nippard Fundamentals Full Body · Nippard Fundamentals Upper/Lower · Nippard Fundamentals Bodypart split · Nippard Pure Bodybuilding | full body 3 days, upper/lower 4 days, bodypart 5 days; RPE targets, double progression [checked lineup, believe details]. Paid: public shape only | beginner to intermediate | B | credited source of `muscle-fullbody-3`, `muscle-upperlower-4`, `muscle-bodypart-5`, `muscle-ppl-6` |
| PHUL (Brandon Campbell) | 4 days: upper power, lower power, upper hypertrophy, lower hypertrophy; power 3 to 5 reps, hypertrophy 8 to 15 [checked structure, believe ranges] | late novice to intermediate | B | `powerbuild-phul-4`, and the shape of `muscle-upperlower-4` |
| PHAT (Layne Norton) | 5 days: 2 power days, then back and shoulders, legs, chest and arms hypertrophy, with speed work [checked structure, believe percentages] | intermediate to advanced | B | `powerbuild-phat-5` |
| Push / Pull / Legs (Push Pull Legs x2) | 3 days (each muscle 1x) or 6 days (2x); 3 to 5 exercises, 6 to 15 reps [believe] | 6 days: intermediate+ | B at 6 days, weaker at 3 | `muscle-ppl-6`; the 3 day version only on request |
| Arnold Golden Six | 3 full body days, the same six lifts, about 20 sets [checked secondary] | novice with a barbell and a chin bar | C | a credited variant inside `muscle-fullbody-3` |
| Arnold split, Classic bro split | 6 days very high volume, or 5 days one body part each [believe] | advanced, or by preference | C | `muscle-bodypart-5`, only when asked for, never for a strength goal |

## Strength and powerlifting

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| Starting Strength (Rippetoe) | 3 days, A/B: squat 3x5 every session, bench and press alternate, deadlift 1x5; add weight every session; reset about 10% after repeated misses [checked structure, believe increments] | true novice, strength | B to C | credited source of `strength-lp-3` |
| StrongLifts 5x5 | 3 days, A (squat, bench, row) and B (squat, press, deadlift), 5x5, deadlift 1x5; +2.5 kg a session, deadlift +5 kg; 3 failed sessions on a lift: minus 10% [checked, official support docs] | true novice | B to C | the exact rules of `strength-lp-3` |
| Texas Method (Practical Programming for Strength Training) | 3 days: volume day 5x5 at about 90% of Friday, light day, intensity day a new 5RM; progresses weekly [checked structure, believe percentages] | post novice, linear progression exhausted | B to C | `strength-texas-3` |
| Wendler 5/3/1 (5/3/1 for Beginners · 5/3/1 Boring But Big · 5/3/1 Forever) | training max 90% of 1RM (85% when unsure); 3 weeks of 5s, 3s, 5/3/1 with an AMRAP last set, then a deload; +2.5 kg upper, +5 kg lower per cycle; a stall: TM down about 10%. BBB 5x10 at 50 to 60% TM. Leaders and anchors [checked core, believe Forever details] | late novice to advanced, 2 to 4 days | B | `strength-531-beginners-3`, `strength-531-bbb-4` |
| GZCL method, GZCLP (Cody Lefever) | tiers: T1 heavy (5x3+), T2 moderate (3x10), T3 light (3x15+, AMRAP last); stages on failure [checked tiers, believe stages] | late novice to early intermediate, 3 to 4 days | B | `strength-gzclp-4` (stages verified at milestone 2, or replaced by the 5/3/1 stall rule) |
| Reactive Training Systems (Tuchscherer) | reps @ RPE, e1RM from the RPE chart, fatigue percents for back off work [checked chart, believe fatigue percents] | intermediate+ with good RPE accuracy | A to B (method) | `strength-rpe-4` |
| Stronger by Science (Nuckols) | templates where the last set AMRAP beats or misses a target and moves the TM; deloads at weeks 7 and 14 [checked partly] | novice to intermediate, 2 to 6 days | B to A | credited source of the AMRAP and TM rule in `strength-rpe-4` |
| Helms 2018 · Zourdos 2016 (studies) | RPE loading matches or beats %1RM loading; RIR based RPE scale | anyone loading by effort | A | `strength-rpe-4` |
| Sheiko | bench 3x a week, squat 2x, deadlift 1x; average about 70% of 1RM, many sets of 1 to 5, never near failure; volume counted in lifts per month [checked secondary] | intermediate to advanced powerlifters, 90 to 150 min | B | **index only**: fixed percentage blocks need real 1RMs and long sessions. v2 candidate |
| Westside, conjugate (Simmons) | max effort and dynamic effort, upper and lower, 4 days; rotating variations; bands, chains, boxes [checked, westside-barbell.com] | advanced, specialty kit | C to B | **index only**: kit and experience few users have. A "conjugate lite" is a v2 candidate |

## Olympic weightlifting

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| Catalyst Athletics (Everett) | Level 1 at 4 days for people who have just learned the lifts; "Simplest program" at 3 days for 4 weeks; lift variant, then pull, then squat [snippet]. Paid: public shape only | novice who can already do the lifts | B | credited source of `weightlifting-novice-3` |
| Soviet school, Prilepin's chart (Medvedyev, Prilepin) | most volume at 70 to 85%; 70 to 80%: sets of 3 to 6, about 18 reps; 80 to 90%: sets of 2 to 4, about 15; 90%+: sets of 1 to 2 [snippet, copies disagree on the top row] | developing lifter with a coach | B (observational) | the volume cap in `weightlifting-novice-3` |
| USAW top down teaching | PVC, then high hang, then hang or blocks, then the floor; video at least, a coach at best [snippet] | everyone new to the lifts | B | **the gate** in `weightlifting-novice-3` and `functional-gpp-3to5`: no classic lift from the floor without reported coached instruction |
| Bulgarian (Abadjiev) | tiny exercise pool, a daily max, many sessions a week [snippet, disputed] | full time elites | C | **index only, never served**: built for full time athletes, unsafe as self coaching |
| Chinese approach | the lifts plus heavy squats, pulls and bodybuilding work for weaknesses [snippet, details disputed] | intermediate+ | C | **index only**: its accessory hypertrophy idea informs the accessories of `weightlifting-novice-3` |

## CrossFit and functional

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| CrossFit methodology (Glassman): CrossFit, What Is Fitness 2002 · CrossFit theoretical template 2003 | ten skills, three energy pathways; the 3 on 1 off template rotates single, two and three modality days (M, G, W), and admits it does not fit a 5 on 2 off week. Class: warm-up, skill or strength, metcon, cool-down. Scale load, then reps, then movement [snippet] | general population, broad fitness | C (method) on A principles | `functional-gpp-3to5`, built on 5 on 2 off |
| CrossFit injury data | about 2 to 4 per 1000 h, called comparable to other training [snippet, Klimek 2018]; shoulder and low back first [believe] | | observational | the safety rule in `functional-gpp-3to5`: no high skill move under fatigue for a novice |
| CompTrain, Mayhem, PRVN, HWPO, Invictus | paid daily programming, 5 to 6 days, tracks by level; only the public shape is known [snippet] | people who want a coach's daily feed | marketing | **index only, never copied**: paid work, named as an option to buy (see "Paid programs") |

## HYROX and hybrid

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| HYROX race format | 8 x (1 km run + a station): SkiErg 1000 m, sled push 50 m, sled pull 50 m, burpee broad jumps 80 m, row 1000 m, farmers carry 200 m, sandbag lunges 100 m, wall balls 100; weights by division [snippet; hyrox.com unreachable] | anyone with a race | facts | `hyrox-prep-4` through `../modules/hyrox-stations.md`; the person confirms against the current rulebook |
| Beginner HYROX plans: Men's Fitness AU 8 week HYROX plan · Centr HYROX beginner plan · Genesis Fitness | 3 to 4 days: two runs, one strength, one HYROX session; compromised running weekly from about week 5; practise on real sleds and targets [snippet, third party plans] | can already run 30 min | C | `hyrox-prep-4` |
| Alex Viada, The Hybrid Athlete | minimum effective dose for each quality, never a full strength plan on a full endurance plan, easy stays easy, separate hard legs from hard runs [snippet, secondary write-ups] | trained adults | B on A principles | `hybrid-strength-endurance-4to6` |
| Nick Bare BPN 16 week plan (Hybrid Athlete) | 6 days, lifts plus runs, doubles; a free 16 week plan [snippet] | trained, 6 days, doubles | B | credited source of the 6 day layout of `hybrid-strength-endurance-4to6` |
| Schumann 2022 · Petré 2021 (studies) | concurrent training: little interference for most, separate hard legs and hard runs | anyone lifting and running | A | `hybrid-strength-endurance-4to6`, `hyrox-prep-4` |
| Fergus Crawley | nothing reliable found in the research | | | **not encoded**: no source to build on |

## Endurance and running

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| NHS Couch to 5K | 9 weeks, 3 runs a week, run/walk from 1 min run, 90 s walk; any week can be repeated [snippet, week 1 seen] | cannot run 20 min | G | `run-c25k-3` |
| Videbæk 2015 · Nielsen 2014 (studies) | novice runners get hurt more (17.8 against 7.7 injuries per 1000 h); a fast rise in weekly volume looks risky [seen] | new runners | A | `run-c25k-3`, and the `run_volume` rule behind `run-base-3to5` |
| Matt Fitzgerald, 80/20 Running · Stephen Seiler (polarized) · Rosenblat 2025 | about 80% easy; polarized beat threshold training in some trials, but a 2025 pooled analysis found no difference against pyramidal, pyramidal maybe better for recreational runners [seen] | all runners | A | `run-base-3to5`: pyramidal by default, and the intensity split of every running module |
| Daniels' Running Formula | VDOT paces E, M, T, I, R; caps: T about 10% of weekly volume, I at most 8% or 10 km, R 5%, long run 25 to 30% or 150 min; hold each level 3 weeks [seen, secondary] | runners with a race time | B | `run-base-3to5`, `hybrid-strength-endurance-4to6`, `hyrox-prep-4`, `../modules/run-race.md`; paces only once a recent race or time trial exists |

## Calisthenics

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| r/bodyweightfitness Recommended Routine | 3 days; supersets pull-up + squat, dip + hinge, row + push-up; a core triplet; 3 x 5 to 8, move up a step at 3 x 8 [seen, ladders believe] | beginners with a bar | B | `calisthenics-rr-3` |
| Overcoming Gravity (Steven Low) | levels 1 to 5 for beginners, full body 3 days, progressions by level; tendons adapt slower, deload every 4 to 8 weeks [seen, numbers believe] | self coached intermediates | B | credited source of the levels in `calisthenics-rr-3` and `../modules/skill-blocks.md` |
| GMB Fitness | Elements locomotion (bear, monkey, frogger, crab), then Integral Strength [seen] | deconditioned, returning | B | `../modules/locomotion.md`, the on-ramp of `calisthenics-rr-3` |
| Convict Conditioning (Paul Wade) | six moves, ten steps each [seen] | hobbyists | C | **index only**: per step standards not confirmed, and the Recommended Routine covers the same ladders with better sources |
| Does bodyweight build muscle | yes, near failure: push-ups match bench at 40% 1RM, band push-ups match a 6RM bench [seen] | | A | why `calisthenics-rr-3` and `home-fullbody-2to4` are real programs |

## Home and minimal equipment

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| StrongFirst Simple and Sinister (Pavel Tsatsouline) | 100 one arm swings and 10 get-ups; timed standards 5 min and 10 min; bell standards by sex [seen] | one or two kettlebells | C | `kettlebell-ss-5` (days 3 to 6, near daily as published) |
| Enter the Kettlebell, Rite of Passage (Pavel Tsatsouline, 2006) | clean and press ladders, pull-ups, swings, 3 days [seen] | pressing strength with one bell | C | `kettlebell-rop-3` |
| Dan John minimalism, Easy Strength | five lifts, never miss a rep, about 10 reps a lift, 5 days [seen] | busy adults, athletes | B | `home-fullbody-2to4`; its rules inform every express session |
| Kikuchi 2017 push-ups (study) | push-ups to failure match bench press at 40% 1RM for growth [seen] | home trainees | A | `home-fullbody-2to4` |
| Lopes 2019 bands (study) | elastic bands match free weights for strength; log colour, anchor distance and reps [seen] | home, older adults | A | `home-fullbody-2to4`, and a load type in the bank |
| Fixed light weights | progress by reps, then tempo and pauses, then single limb, then range and leverage, then mechanical drop sets, then density, then sets; past about 30 reps, a heavier bell [believe ordering, A evidence below it] | dumbbell or band users | B | the `fixed_load` rule in `home-fullbody-2to4` |

## General health, fat loss and populations

| school | what it prescribes | for whom | evidence | served by |
|:-|:-|:-|:-|:-|
| WHO 2020 · UK CMO 2019 | 150 to 300 min moderate or 75 to 150 vigorous aerobic a week, strength 2+ days, less sitting; 65+ add balance and strength 3+ days [checked] | everyone | G | `health-baseline-2to3`, `older-strong-3`, and the floor every program is checked against |
| ACSM 2009 resistance training stand | novice 8 to 12 RM, 2 to 3 days full body, +2 to 10% when the target is beaten by 1 to 2 reps, 2 to 3 min rest on heavy lifts [checked] | novices | G | `health-baseline-2to3`, `older-strong-3`, `strength-lp-3`, `functional-gpp-3to5`; the 2026 update replaces it at milestone 2 |
| NSCA Essentials | %1RM to reps table, rest and load ranges per goal [checked via study guides] | | G | the first outing loads in `engine/`, no program of its own |
| Older adults: Sherrington 2019 Cochrane · ICFSR 2021 | multicomponent, balance challenging work, power at light to moderate load moved fast; heavy loading for low bone density only supervised (LIFTMOR) [checked] | 65+ | A and G | `older-strong-3`, plus `../modules/balance.md`, mandatory from 60 |
| Pregnancy and postpartum, ACOG 804 | activity is safe without complications; 150 min plus strength; continue rather than start vigorous work; stop signs [checked in part] | pregnant, postpartum | G | `health-baseline-2to3` with the pregnancy overrides, only after the person confirms their provider has no objection |
| Fat loss | the deficit is diet; strength training keeps muscle; more than 250 min a week of activity for real exercise driven loss [checked] | | A | **not a program**: the goal picks a muscle or health program, adds activity minutes and states the principle. No calorie targets, no meal plans |

## To verify (milestone 2)

Every number below is [believe] and is used by a file. Each one is checked against the primary source at milestone 2, then either marked [checked] or replaced.

- PAR-Q+ items 2 to 7, exact wording and the follow-up questions · `engine/screen.py`
- ACOG list of moves to avoid lying on the back after the first trimester · `engine/build.py`
- Epley 1RM estimate from a set of 10 or fewer reps (and Brzycki as the alternative) · `engine/progress.py`
- GZCLP stage sequence on failure (T1 5x3, 6x2, 10x1; T2 3x10, 3x8, 3x6; reset at 85%) and the T3 25 rep rule · `strength-gzclp-4.md`, `engine/progress.py`
- Texas Method volume day at about 90% of the Friday 5RM, recovery day at about 80% of the volume day · `strength-texas-3.md`
- 5/3/1 Forever details: the 85% TM default when unsure, the 7th week protocol; the 40, 50, 60% deload wave · `strength-531-bbb-4.md`, `strength-531-beginners-3.md`
- Starting Strength exact increments and reset percentage · `strength-lp-3.md` (credited source; the program uses the checked StrongLifts rules)
- RPE back off drop of 10% (RTS fatigue percents of 3 to 9% not found) · `strength-rpe-4.md`
- RP volume landmarks MEV, MAV, MRV per muscle, and the accessory mesocycle ramp (RIR 3, 2, 2, 1, an extra set in weeks 3 and 4) · `muscle-fullbody-3.md`, `muscle-upperlower-4.md`, `muscle-ppl-6.md`, `muscle-bodypart-5.md`, `powerbuild-phul-4.md`
- The deload week shape (half the sets, about 10% lighter, 3 to 4 RIR, or 90% load and 4 RIR) · `muscle-fullbody-3.md`, `muscle-upperlower-4.md`, `muscle-ppl-6.md`, `muscle-bodypart-5.md`, `powerbuild-phul-4.md`, `powerbuild-phat-5.md`, `functional-gpp-3to5.md`, `weightlifting-novice-3.md` (Catalyst 4 week blocks), `hyrox-prep-4.md` (60% of the sets)
- The weekly set ceiling near 20 and the start at 8 to 12 · `muscle-ppl-6.md`, `home-fullbody-2to4.md`
- Schoenfeld 2019 volume equated frequency analysis (seen only in secondary sources) · `muscle-bodypart-5.md`
- PHAT speed work at 65 to 70% for 6 x 3, and the power day 3 to 5 reps · `powerbuild-phat-5.md`
- PHUL rep ranges and the "add load at the top of the range" rule · `powerbuild-phul-4.md`
- Couch to 5K weeks 2 to 9 · `run-c25k-3.md`, `engine/progress.py`
- Daniels pace caps (T about 10%, I 8% or 10 km, R 5%, long run 25 to 30% or 150 min) and % VO2max per pace, seen only in secondary sources that conflict · `run-base-3to5.md`, `../modules/run-race.md`
- HYROX station weights per division, the Women Pro wall ball (6 kg at 2.70 m), the doubles and relay weights · `../modules/hyrox-stations.md`, `hyrox-prep-4.md`
- HYROX beginner plan length of 4 to 20 weeks, and the absence of any trial · `hyrox-prep-4.md`
- Recommended Routine ladders and warm-up · `calisthenics-rr-3.md`, `../modules/skill-blocks.md`
- Overcoming Gravity deload every 4 to 8 weeks · `calisthenics-rr-3.md`
- The fixed weight ladder ordering, and buying the next bell past about 30 reps · `home-fullbody-2to4.md`
- Simple and Sinister frequency and effort, and the mixed bell advice · `kettlebell-ss-5.md`
- CrossFit benchmark retest every 8 to 12 weeks; benchmark WOD loads (from memory, research/02) · `functional-gpp-3to5.md`, `../modules/conditioning.md`
- UK CMO "any bout counts" toward the 150 minutes · `health-baseline-2to3.md`
- The content of the 2026 ACSM resistance training update · `health-baseline-2to3.md`, `older-strong-3.md`, the novice progression principle

## Paid programs

- **Credit by name, link to buy.** A program file built on a published or paid system names the author, the book or site, and links to it, so the person can buy the real thing.
- **Never copy.** Public structures (5/3/1's waves, StrongLifts' A and B days, the Recommended Routine's ladders) are described as structures. Paid daily programming (CompTrain, Mayhem, PRVN, HWPO, Invictus, Catalyst, Nippard, RP) is never copied or imitated as "their" workout; the trainer may name its public shape and recommend it to someone who wants it.
- **Never quote a price.** Prices change. Link the live page and let the person read it there.
