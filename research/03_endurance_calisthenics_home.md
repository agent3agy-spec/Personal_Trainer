# 03 · Endurance, calisthenics, home and bodyweight training

Research cluster for the shareable Personal trainer agent. Researched 13 Nov 2026.

## How to read the marks

WebFetch was blocked for every host tried this session (reddit, nhs.uk, strongfirst.com, pubmed, pmc, vdoto2.com all failed DNS in the sandbox). So no source page was opened in full. The marks are therefore:

| mark | meaning |
|:-|:-|
| [seen] | confirmed this session in the search tool's extract of the named page (abstract or page text quoted by the search engine). Stronger than memory, weaker than reading the paper. |
| [believe] | from memory, not confirmed this session. Verify before encoding as a hard rule. |
| [checked] | opened and read in full. None reached this level because of the fetch block. |

Hosts that must be allowed to upgrade [seen] to [checked]: `pubmed.ncbi.nlm.nih.gov`, `pmc.ncbi.nlm.nih.gov`, `www.nhs.uk`, `www.reddit.com`, `www.strongfirst.com`, `vdoto2.com`.

Evidence levels used below: **MA** meta-analysis or systematic review · **RCT** randomised trial · **Cohort** observational · **Coach** practitioner consensus or a book method · **Anecdote**.

· · ·

## Part A · Endurance and running basics

### A1 · Intensity zones (the vocabulary everything else uses)

| model | zones | anchors | field proxy without a lab |
|:-|:-|:-|:-|
| Seiler 3 zone | Z1 below VT1, Z2 between VT1 and VT2 (respiratory compensation), Z3 above VT2 | ventilatory or lactate thresholds | talk test [seen] |
| 5 zone HR | Z1 to Z5 as % HRmax or % HR reserve | max HR, usually estimated | HR strap, but formula HRmax is off by about 10 bpm for many people [believe] |
| RPE (Borg CR10) | 1 to 10 | perception | Z1 about RPE 2 to 4, threshold about 6 to 7, intervals 8 to 9 [believe] |

* Seiler's group defines zone 1 as below the first ventilatory threshold, zone 2 between VT1 and the respiratory compensation threshold, zone 3 above it [seen] ([Seiler, Impact of TID on performance](https://researchgate.net/profile/Stephen_Seiler/publication/6153247_Impact_of_Training_Intensity_Distribution_on_Performance_in_Endurance_Athletes/links/09e4150ab8efd3de6e000000.pdf)).
* The talk test is a valid and reliable field stand in for VT1 and VT2. The passage read matters: a short passage can be rushed in one breath and overestimates the threshold [seen] ([ACE, talk test validity](https://www.acefitness.org/continuing-education/certified/research-special-issue/6945/validity-of-the-talk-test-in-identifying-the-respiratory-compensation-threshold)). Practical rule: if you can speak full sentences comfortably you are below VT1; if speech is broken into a few words you are near or above VT2 [believe].
* 80/20 is Seiler's description of how elite athletes already train, not a designed prescription, and it is often counted in sessions, not minutes, so applying it to minutes misleads [seen] ([Roadman Cycling](https://roadmancycling.com/blog/stephen-seiler-research-polarised-training-lessons), [UltraRunning, zones](https://ultrarunning.com/featured/training-zones-behind-the-numbers/)).

Evidence level: zone definitions are physiology consensus; talk test validity is supported by lab studies (Cohort / validation).

### A2 · 80/20 (Matt Fitzgerald)

* **Prescribes:** about 80% of training time at low intensity, 20% at moderate plus high. Plans are graded by level and come in pace, power or HR versions [seen] ([TrainingPeaks 80/20 plans](https://www.trainingpeaks.com/training-plans/running/tp-285100/80-20-running-2024-edition-starting-out-starting-over-level-0-pace-based)).
* **Zones:** the 80/20 Endurance system uses a seven zone scale with in between "X" zones not numbered [seen] ([8020endurance.com](https://www.8020endurance.com/understanding-your-norwegian-training-run-plan/), [Runzy summary](https://runzy.com/blog/?p=1263)). Fitzgerald recommends HR for easy runs, HR plus pace for moderate, RPE plus pace for short hard intervals [seen].
* **Entry levels:** Level 0 is a six week plan for easing (back) into running; the Level 2 "starting out" plan expects you can walk comfortably 40 minutes [seen].
* **Frequency / volume / progression:** level plans run roughly 2.5 to 3.5 h per week at Level 0 maintenance [seen] ([Final Surge](https://www.finalsurge.com/club/team8020/plan/66259)); progression is by moving up a level [believe].
* **Who:** recreational runners from beginner to competitive. Caveat: the original research Fitzgerald leaned on used runners under 40 min for 10K, and beginners with lots of room to improve do not need every run slowed to a crawl [seen] ([Lifehacker/Skwarecki via pipedot](https://pipedot.org/6NS8W)).
* **Evidence:** Coach, built on observational elite data plus the RCTs in A3.

### A3 · Polarized vs pyramidal vs threshold: the evidence

| study | design | finding | mark |
|:-|:-|:-|:-|
| Stöggl and Sperlich 2014, Front Physiol | RCT, 48 well trained runners, cyclists, triathletes, XC skiers, 9 weeks, 4 groups (POL, threshold, HIIT, high volume), HR controlled | POL largest gains: VO2peak +11.7%, time to exhaustion +17.4%, peak velocity/power +5.1%. Threshold and high volume added nothing further | [seen] ([Frontiers](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2014.00033/full)) |
| Rosenblat et al. 2019, JSCR | MA | POL beat threshold for time trial performance, ES = -0.66 (95% CI -1.17 to -0.15), but from only 3 studies | [seen] ([PubMed 29863593](https://pubmed.ncbi.nlm.nih.gov/29863593/)) |
| Oliveira et al. 2024, Sports Med | MA | POL superior for VO2peak; no POL superiority for other endurance performance surrogates | [seen] ([Springer PDF](https://link.springer.com/content/pdf/10.1007/s40279-024-02034-z.pdf)) |
| Rosenblat et al. 2025, Sports Med | network MA of individual participant data | no significant difference POL vs PYR for VO2max or time trial. Signal: competitive athletes may benefit from POL, recreational athletes from PYR | [seen] ([PMC11329428](https://pmc.ncbi.nlm.nih.gov/articles/PMC11329428)) |
| Burnley, Bearden, Jones 2022 vs Foster et al. 2022, MSSE | opposing commentaries | the "is polarized optimal" debate | [seen] (titles only) |

Note: a "Rosenblat 2022" pyramidal vs polarized meta-analysis could not be found. The relevant Rosenblat papers are 2019 and 2025.

**Takeaway for a non elite user:** what all models share is a large low intensity base. Whether the remaining 10 to 20% is mostly threshold (pyramidal) or mostly hard intervals (polarized) matters little for recreational runners, and pyramidal may suit them slightly better [seen, Rosenblat 2025].

### A4 · Daniels' Running Formula (Jack Daniels)

* **VDOT:** a race time maps to a VDOT number, which maps to five training paces [believe, widely known].
* **Paces and purpose** [believe for % values, roughly from the book]:

| pace | intensity | purpose | per session cap (as reported in Daniels summaries) |
|:-|:-|:-|:-|
| E (easy) | about 59 to 74% VO2max, 65 to 79% HRmax | base, recovery | long run the lesser of 25 to 30% of weekly mileage or 150 min (30% if under 40 mi/week) [seen] |
| M (marathon) | about 75 to 84% VO2max | race specific | lesser of 20% weekly mileage or 18 mi [seen] |
| T (threshold) | about 83 to 88% VO2max, "comfortably hard" | raise lactate threshold | about 10% weekly mileage, or a steady 20 min tempo; up to about 30 to 40 min if broken into bouts [seen] |
| I (interval) | about 95 to 100% VO2max | VO2max | lesser of 8% weekly mileage or 10 km [seen] |
| R (repetition) | faster than I | speed, economy | lesser of 5% weekly mileage or 8 km (5 mi) [seen] |

Sources for the caps: [Reading Daniels, ch.4](https://cdbaca.github.io/ssg/reading-daniels-running-formula-chapter-4.html), [Daniels notes](https://obsidian-1k7.pages.dev/books/daniels-running-formula), [r/AdvancedRunning dissection](https://reddit.birdcat.cafe/r/AdvancedRunning/comments/6pb807/dissecting_daniels_understanding_daniels_running). These are secondary summaries; the book is 4th ed., Human Kinetics 2021.

* **Mileage rule:** hold a mileage level for at least 3 weeks before increasing it [seen, secondary]. Daniels' step: add about 1 mile per session per week, up to the number of sessions you run, every 3 to 4 weeks [believe].
* **Structure:** phased plans (foundation, early quality, transition quality, final quality), usually two quality sessions per week once past the base [believe].
* **Who:** runners with a recent race result; beginners use his "white" novice plan [believe].
* **Evidence:** Coach, grounded in Daniels' lab work on VO2max and economy. The per session caps are expert heuristics, not trial derived.

### A5 · Couch to 5K (NHS)

* **Structure:** 9 weeks, 3 runs per week with a rest day between. Week 1: brisk 5 min walk warm up, then run 1 min / walk 90 s repeated, about 20 min of intervals, 5 min cool down; NHS lists the week 1 total as 28 min 30 s excluding stretches. Any week may be repeated until ready [seen] ([NHS plan](https://www.nhs.uk/better-health/get-active/get-running-with-couch-to-5k/couch-to-5k-running-plan), [EANI week by week](https://healthwell.eani.org.uk/healthtopic/get-fit/couch-5k-week-week?type_1=1)).
* **Progression:** run segments lengthen each week, ending at about 30 min continuous running in week 9 [believe].
* **Who:** total beginners, no equipment. **Evidence:** public health programme; no RCT on its injury rate found [believe].

### A6 · The 10% rule and novice injury risk

| study | design | finding | mark |
|:-|:-|:-|:-|
| Buist et al. 2008 (GRONORUN), Am J Sports Med | RCT, 532 novice runners. 13 week graded programme built on the 10% rule vs standard 8 week programme | injury incidence 20.8% graded vs 20.3% standard: **no protective effect** of the 10% rule | [seen] ([Running Physio summary](https://www.running-physio.com/skimpyresearch/), [BMC protocol](https://link.springer.com/content/pdf/10.1186/1471-2474-8-24.pdf)) |
| Nielsen et al. 2014, JOSPT 44(10):739 | Cohort, 874 novice runners with GPS, 1 year, 202 injured | progression above 30% over 2 weeks: HR 1.59 (95% CI 0.96 to 2.66, p = .07) vs under 10%; stronger for some injury types. Authors' cautious advice: under 30% per week over 2 weeks | [seen] ([AAU record](https://vbn.aau.dk/da/publications/excessive-progression-in-weekly-running-distance-and-risk-of-runn), [core.ac.uk](https://core.ac.uk/display/60599525), [JOSPT patient page PDF](https://www.orthobethesda.com/wp-content/uploads/2020/06/jospt-running-increased-mileage.pdf)) |
| Videbæk et al. 2015, Sports Med | MA, 13 studies | **17.8 injuries per 1000 h in novice runners** (95% CI 16.7 to 19.1) vs 7.7 in recreational runners | [seen] ([PMC4473093](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4473093/)) |
| Nielsen group, Run Clever 2018 | RCT | progressing volume vs progressing intensity: no clear difference in injury | [seen, summary only] |

**Takeaway:** novices get hurt about 2.3 times as often per hour as recreational runners. The 10% rule itself is not protective in trials, but jumps above about 30% over two weeks are a plausible red flag. Use "under 10 to 30%" as a soft band, not a law, and watch symptoms.

### A7 · How an agent prescribes runs without a coach (synthesis)

1. Easy days by the talk test (full sentences) or RPE 3 to 4, never by a formula HR alone.
2. Beginners (no current running): run/walk intervals, C25K style, 3 days/week, no quality session until 20 to 30 min continuous is comfortable.
3. Base runners: at most one quality session a week (strides, short T or I work, capped by Daniels' % rules); the rest easy.
4. Long run at most 25 to 30% of weekly volume and at most 150 min.
5. Weekly volume increases kept under about 10 to 30%, hold each new level 3 weeks, cut back about 20 to 30% every 3 to 4 weeks [believe for the cut back figure].

· · ·

## Part B · Calisthenics

### B1 · r/bodyweightfitness Recommended Routine (RR)

* **Structure** [seen] ([Liftosaur RR](https://www.liftosaur.com/programs/recommended-routine), [gist copy](https://gist.github.com/sgup/f10f1d57e54b7876495f4bafb6d697eb), [RR PDF](https://www.scribd.com/document/435002158/rr-pdf), [wiki mirror](https://reddit.rtrace.io/r/bodyweightfitness/wiki/kb/recommended_routine)):
  * Warm up (about 10 to 15 min): joint and dynamic mobility, plus easier squat and hinge variations as ramp up [seen]. In the wiki the warm up includes yuri's shoulder band routine, squat sky reaches, GMB wrist prep, deadbugs, and arch/hollow/support holds [believe].
  * Strength (40 to 60 min) done as three supersets: **pull-up + squat**, **dip + hinge**, **row + push-up** [seen].
  * Core triplet: anti extension (e.g. ab wheel / plank progression), anti rotation (e.g. banded Pallof press), extension (e.g. reverse hyperextension) [seen, 3x8 to 12].
  * **Sets x reps:** 3 sets of 5 to 8 per strength exercise; core 3 x 8 to 12 [seen].
  * **Rest:** about 90 s between paired exercises [seen].
  * **Frequency:** 3 times per week on non consecutive days [believe, wiki standard].
  * **Progression:** start at the hardest step you can do for 3x5 with good form, add reps until 3x8, then move to the next step [seen].
  * **Beginners overwhelmed:** cut sets first, add back over time [seen]. With a barbell and rack, the wiki suggests barbell squat and deadlift in place of the squat and hinge ladders [seen].
* **Ladders** [believe, from the wiki as remembered]:

| slot | progression |
|:-|:-|
| pull-up | scapular pulls, arch hangs, pull-up negatives, pull-up, weighted pull-up / L pull-up |
| squat | assisted squat, squat, split squat, Bulgarian split squat, beginner shrimp squat, intermediate shrimp, advanced shrimp (or pistol path) |
| dip | parallel bar support hold, negative dips, parallel bar dips, weighted dips (or ring path) |
| hinge | Romanian deadlift (single leg, bodyweight), banded / weighted single leg RDL, banded Nordic curl negatives, Nordic curls |
| row | vertical rows, incline rows, horizontal rows, wide rows, archer rows, front lever rows |
| push-up | wall push-up, incline push-up, full push-up, diamond push-up, pseudo planche push-up |

* **Equipment:** pull-up bar, dip bars or rings (rings strongly suggested), something to row from. **Who:** beginners. **Evidence:** Coach (community consensus, distilled from Overcoming Gravity principles).

### B2 · Overcoming Gravity (Steven Low, 2nd ed. 2016)

* **What it is:** a textbook for building your own gymnastics strength routine, not a fixed programme. Skills sit on progression charts graded by level; beginners live in **levels 1 to 5** (push-ups, dips, pull-ups, rows, squats); chapters cover untrained beginners, trained beginners, intermediates, advanced [seen] ([Coconote lecture notes](https://coconote.app/notes/c38251da-226b-45a8-91d0-8ae025f20e78), [book notes](https://dpetkovski.pages.dev/overcoming-gravity-by-steven-low-book-notes)).
* **Packaged version:** a 10 week, 3 days per week beginner programme, about 45 min sessions [seen] ([Boostcamp](https://www.boostcamp.app/coaches/steve-low/overcoming-gravity)).
* **Session order:** skill work first while fresh, then strength, then accessory/flexibility [seen, unofficial copy].
* **Volume / intensity rules** [believe]: strength work in roughly the 5 to 8 rep range (or 3 to 6 for heavier); total volume per exercise about 25 to 50 reps for beginners; isometric holds counted in seconds (e.g. 3 to 6 sets of 10 to 30 s); a progression is "earned" when its top of range is clean on all sets; full body 3x/week for beginners and early intermediates. A Reddit post quotes a book rule of thumb of at least 15 full reps per exercise [seen, unverified wording].
* **Connective tissue:** straight arm skills (planche, front lever, iron cross) load tendons that adapt slower than muscle, so progress slowly and deload every 4 to 8 weeks [believe].
* **Who:** self coached intermediates who want gymnastics skills. **Evidence:** Coach (Low is a physical therapist and ex gymnast) [seen].

### B3 · GMB Fitness

* **Elements:** foundation programme on four locomotion patterns: Bear (shoulder integration, overhead strength), Monkey (lateral control), Frogger (upper to lower body link), Crab (hips and core, supine). Each has a tutorial, a timer and scaling; sample schedule uses about 15 min locomotion blocks with variations (bent arm bear, monkey 180, sumo frogger) [seen] ([GMB Bear](https://gmb.io/bear/), [Frogger](https://gmb.io/frogger/), [Praxis](https://gmb.io/praxis/)).
* **Pathway:** Elements first, then Integral Strength and/or Mobility, then Sequences [seen].
* **Integral Strength:** progressive strength going bodyweight, then bar, then rings, adding leverage and instability [seen]. Typically 3 sessions/week, about 45 to 60 min [believe].
* **Mobility (GMB):** active, strength through range approach [believe].
* **Who:** deconditioned or older beginners, people returning from injury, anyone wanting movement quality before load. **Equipment:** floor for Elements; bar or rings later. **Evidence:** Coach; no trials on the programmes.

### B4 · Convict Conditioning (Paul Wade, 2009)

* **Structure:** "Big Six": push-up, squat, pull-up, leg raise, bridge, handstand push-up; ten steps each, each step with beginner, intermediate and progression standards (often 20+ reps, e.g. 2 x 20 to 3 x 50 depending on step) [seen for six moves and ten steps; believe for exact rep numbers] ([Breaking Muscle review](https://breakingmuscle.com/book-review-convict-conditioning-by-paul-wade/), [Dragon Door FAQ](https://www.dragondoor.com/pdf/Convict_Conditioning_SUPER_FAQ.pdf)).
* Wade himself calls the ten steps an artificial construct with many hidden steps in between [seen]. Author is pseudonymous and the prison backstory is disputed [seen].
* **Evidence:** Anecdote / Coach. High rep standards are slow and conservative; low frequency (often one or two sessions per move per week). Useful as an equipment light ladder, not as an evidence anchor.

### B5 · Skill progressions with entry tests

[believe, synthesis of RR, OG and GMB conventions]

| skill | entry test | ladder | "move on" rule |
|:-|:-|:-|:-|
| push-up | max strict push-ups | wall, incline (bench), knee, full, diamond / decline, archer, pseudo planche | 3 x 8 at current step |
| pull-up | dead hang 30 s, 1 negative of 5 s | dead hang, scap pulls, negatives (3 to 5 s), band assisted, full, weighted | 3 x 8 (or 3 x 5 to 8 for RR) |
| dip | 30 s support hold | support hold, negatives, bench dips (shoulder caution), bar dips, ring dips | 3 x 8 |
| row | incline row reps | high incline, horizontal, feet elevated, archer | 3 x 8 |
| handstand | 30 s wall plank / pike hold | wall plank, chest to wall hold to 60 s, kick up practice, freestanding | skill: daily or near daily, short sets, time based |
| pistol | bodyweight squat x 20, split squat x 10 each | assisted / box pistol, Bulgarian split squat, shrimp squat, pistol | 3 x 8 each leg |
| front lever | 5 strict pull-ups, 30 s hollow hold | tuck, advanced tuck, one leg, straddle, full | 3 to 6 sets of 10 to 15 s holds |

### B6 · Does bodyweight / low load training to near failure build muscle?

| study | design | finding | mark |
|:-|:-|:-|:-|
| Schoenfeld et al. 2016, JSCR (likely the "2015" well trained study, published online 2015) | RCT, 18 trained men, 25 to 35 reps vs 8 to 12 reps per set, 3x/week, 8 weeks, to failure | similar muscle thickness gain; squat 1RM larger with heavy (19.6% vs 8.8%); low load better for muscular endurance | [seen, snippet] ([search extract](https://www.bisp-surf.de/Record/PU201603001398)) |
| Schoenfeld, Grgic, Ogborn, Krieger 2017, JSCR | MA, 21 studies, ≤60% vs >60% 1RM, all to failure | **hypertrophy similar**; 1RM strength greater with heavy | [seen] ([PubMed 28834797](https://pubmed.ncbi.nlm.nih.gov/28834797/)) |
| Kikuchi and Nakazato 2017, J Exerc Sci Fit | RCT, 18 men, bench at 40% 1RM vs push-ups at matched load, 2x/week, 8 weeks | push-ups comparably effective for pec hypertrophy and 1RM gain | [seen] ([DOAJ](https://doaj.org/article/f70cce826f3348b5b4f3ace8cf8ac33e)) |
| Kotarsky et al. 2018, JSCR | RCT, 23 men, progressive push-up vs bench, 4 weeks | both raised bench 1RM; no difference in muscle thickness | [seen] ([NDSU repository](https://library.ndsu.edu/ir/handle/10365/28060)) |
| Calatayud et al. 2015, JSCR 29(1):246 | RCT, 30 trained students, 6RM bench vs 6RM elastic band push-up vs control, 5 weeks | similar 1RM and 6RM gains when EMG activity is matched | [seen] ([PubMed 24983847](https://pubmed.ncbi.nlm.nih.gov/24983847/)) |
| Refalo et al. 2023, Sports Med | MA, 15 studies | trivial advantage for failure vs non failure; no evidence failure is required; possibly non linear link with proximity to failure | [seen] ([AUT repository](https://openrepository.aut.ac.nz/items/78679612-6ff4-4d00-95d1-7920d072a760)) |

**Takeaway:** for hypertrophy, load matters little across a wide range (about 30% 1RM up) if sets go close to failure (roughly 0 to 3 reps in reserve). For max strength in a specific heavy lift, heavier loads win. So bodyweight is a full hypertrophy tool as long as each set is hard; it becomes a strength limitation only when the user cannot make a variation harder and reps climb above about 30.

· · ·

## Part C · Home training: kettlebells, dumbbells, bands

### C1 · StrongFirst Simple and Sinister (Pavel Tsatsouline)

* **Session:** 100 one arm swings (10 x 10, alternating hands) and 10 Turkish get-ups (alternating), plus a warm up (prying goblet squat, halos, hip bridges) [seen for swings/get-ups; believe for warm up] ([LiftVault](https://liftvault.com/programs/strength/simple-sinister-kettlebell-program-spreadsheet-pavel/), [StrongFirst Sinister](https://www.strongfirst.com/sinister/)).
* **Frequency:** daily or near daily, at an effort that leaves you fresher [believe].
* **Timed standard:** 10 swings every 30 s, 100 inside 5 min; 1 min rest; 1 get-up per minute, 10 inside 10 min [seen].
* **Standards:** Simple, men 32 kg both; women 24 kg swing / 16 kg get-up. Sinister, men 48 kg both; women 32 kg swing / 24 kg get-up [seen].
* **Progression:** stay at a bell until the full session is comfortable inside the time targets, then step up a size; StrongFirst's later "5 to 1" style mixes heavier and lighter bells in a session [seen for the first; believe for the mix].
* **Who:** general strength and conditioning with one or two bells; minimal space. **Evidence:** Coach. No RCT on S&S specifically [believe]; swing training has small trials for strength/power [believe].

### C2 · Enter the Kettlebell, Rite of Passage (Pavel, 2006)

* **Heavy, medium, light days** for clean and press ladders (1, 1-2, 1-2-3 rungs etc.), alternated with pull-ups, 3 days/week; light about 50 to 60% of heavy day reps [seen].
* **Progression:** add a ladder each week until 5 ladders, then add rungs up to 5 [seen]. On non heavy days roll dice for minutes of swings or snatches [seen]. Variety days allowed [seen].
* **Goals:** press a bell half bodyweight; men snatch 24 kg 200 times in 10 min [seen] ([Blackstone Valley Kettlebells](https://blackstonevalleykettlebells.blogspot.com/2016/10/enter-kettlebell-rite-of-passage.html)).
* **Evidence:** Coach. Note: the text's rung counts differ slightly between sources [seen].

### C3 · Dan John (Easy Strength, goblet squat, minimalism)

* **Easy Strength (with Pavel):** five lifts (press, hinge, squat, loaded carry, ab work), 40 workouts, **never miss a rep, never more than about 10 reps per movement**, if it feels light go heavier [seen] ([Even Easier Strength, Dan John](https://medium.com/@danjohn84123/even-easier-strength-d7fc672eb9d), [Liftosaur](https://www.liftosaur.com/programs/easy-strength)).
* **Warm up he uses:** 10 to 25 goblet squats, about 75 swings in sets of 10 to 25, 1 to 5 get-ups [seen].
* **Movement menu:** push, pull, hinge, squat, loaded carry (plus a sixth, the get-up / ground work) [believe]. Goblet squat as the teaching squat [believe].
* **Who:** anyone with one or two kettlebells or dumbbells. **Evidence:** Coach.

### C4 · Elastic bands

* **Lopes et al. 2019, SAGE Open Med:** MA, 8 RCTs comparing elastic resistance to machines or free weights, strength outcome. **No difference**: lower limbs SMD 0.09 (95% CI -0.18 to 0.35), upper limbs SMD -0.11 (corrected value, 95% CI -0.40 to 0.19) [seen] ([DOAJ](https://doaj.org/article/f76933a02f3a4ff08fd3d81de9169831), [PMC6383082](https://pmc.ncbi.nlm.nih.gov/articles/PMC6383082)).
* A 2020 MA by overlapping authors found band training similar for body composition except fat mass, where conventional did better [seen].
* **Caveat:** band load is a colour and a stretch factor, not a number, so progression must be logged as band + stretch + reps [seen, secondary].
* **Evidence:** MA of RCTs. Strong for "bands are a legitimate strength tool".

### C5 · How to progress with fixed light weights

[believe unless marked; the principle rests on B6: hard sets near failure grow muscle across loads]

Order the agent should try, cheapest first:

1. **Reps** within a range (e.g. 8 to 15, then 15 to 30), double progression: hit the top on all sets, then make it harder.
2. **Tempo:** 3 to 4 s eccentric, a 1 to 2 s pause at the hardest point (bottom of squat, chest an inch off floor).
3. **Unilateral:** goblet squat to split squat to Bulgarian split squat to single leg; two arm row to one arm; push-up to archer. Halves the external support and roughly doubles relative load.
4. **Range and leverage:** deficit push-ups, elevated feet, longer lever arms, 1.5 reps.
5. **Mechanical drop sets:** hardest variation to failure, then switch to an easier one without rest (e.g. decline, flat, incline push-up).
6. **Density:** same work in less time (EMOM, rest pause, myo reps).
7. **Sets:** add a set (weekly hard sets per muscle about 10 to 20 for hypertrophy [believe, Schoenfeld volume MA 2017]).
8. **Buy the next bell or a heavier band** when reps exceed about 30 at the hardest variation; past that point sets become cardio limited.

Proximity to failure is the knob that makes all of these work: no failure needed, but within about 0 to 3 RIR [seen, Refalo 2023].

### C6 · Concurrent training (adding running to a strength plan)

* Wilson et al. 2012 (MA, as described by a later Sports Med review): concurrent training attenuated power, did not compromise hypertrophy or max strength; a later MA found running vs cycling had no significant effect, and explosive strength suffered more when both were done in the same session [seen] ([Springer s40279-021-01587-7](https://link.springer.com/article/10.1007/s40279-021-01587-7)).
* Wilson 2012 itself reported running caused more interference than cycling, dose related to frequency and duration [believe].

· · ·

## Comparison summary

| programme | structure | freq/week | progression | equipment | who | evidence |
|:-|:-|:-|:-|:-|:-|:-|
| 80/20 | about 80% easy time | 3 to 7 runs | levels | none, HR optional | all runners | Coach on RCT/MA base |
| Polarized / pyramidal | TID models | any | n/a | none | trained / recreational | RCT + MA |
| Daniels | VDOT paces, % caps | 4 to 7 | 3 week holds | watch | runners with a race time | Coach |
| Couch to 5K | run/walk | 3 | weekly, repeatable | none | total beginners | public health |
| BWF RR | 3 supersets + core, 3x5 to 8 | 3 | reps to 8, next step | bar, rings | beginners | Coach |
| Overcoming Gravity | level charts | 3 full body | levels | bar, rings | self coached intermediates | Coach |
| GMB | locomotion then strength | 3 | scaling, bar to rings | floor, bar, rings | deconditioned, return to sport | Coach |
| Convict Conditioning | 6 moves x 10 steps | 2 to 3 | high rep standards | bar | hobbyists | Anecdote |
| Simple and Sinister | 100 swings + 10 TGU | 5 to 7 | timed standard, bigger bell | 1 to 2 KB | general | Coach |
| Rite of Passage | C&P ladders, pull-ups, swings | 3 + variety | ladders, rungs | 1 KB, bar | general strength | Coach |
| Easy Strength | 5 lifts, max 10 reps | 5 | never miss, add load | any | athletes, busy adults | Coach |
| Bands | any template | any | band + stretch + reps | bands | home, older adults | MA of RCTs |

· · ·

## For the agent

Rules the coach can encode. Each names its source and its mark.

1. **Pick a calisthenics step by test, not by ego.** For each slot (push, pull, squat, hinge, dip, row) run the user down the ladder until they can do 3 sets of 5 clean reps; that is the working step. When all 3 sets hit 8, move up one step and restart at 5. Source: BWF Recommended Routine [seen]. If they cannot do 5 of the easiest step, use isometric holds or negatives (5 s lowering) for 3 to 5 sets [believe, OG and RR convention].

2. **A bodyweight set counts only if it is hard.** Prescribe sets ending at 0 to 3 reps in reserve. Low load to near failure gives hypertrophy equal to heavy load. Source: Schoenfeld 2017 MA, Refalo 2023 MA, Kikuchi 2017, Calatayud 2015 [seen].

3. **Progress a fixed weight user in this order:** reps to top of range, then tempo and pauses, then unilateral, then leverage/range, then mechanical drop sets, then density, then sets. When the hardest variation exceeds about 30 reps, recommend the next bell or band. Source: synthesis on B6 evidence [believe for the ordering; seen for the underlying load evidence].

4. **Easy runs are prescribed by speech.** "You can say full sentences" or RPE 3 to 4. Do not hand a formula HR zone to someone who has not tested max HR. Source: talk test validity (ACE) [seen]; Seiler zones [seen].

5. **Beginners start run/walk.** No continuous running ability: Couch to 5K, 3 days per week with rest days between, any week repeatable. No quality session until 20 to 30 min of continuous easy running is comfortable. Source: NHS C25K [seen]; novice injury rate 17.8 per 1000 h, Videbæk 2015 [seen].

6. **Volume grows slowly and has a red line.** Hold a weekly volume for about 3 weeks before raising it; never raise it more than about 30% over two weeks; 10% is a comfortable default, not a safety guarantee. Source: Nielsen 2014 cohort (>30% flag, p = .07) [seen]; Buist 2008 RCT (10% rule not protective) [seen]; Daniels 3 week hold [seen, secondary].

7. **One quality run per week for non competitive users, capped.** Threshold block about 10% of weekly volume or 20 min; intervals at most 8% of weekly volume; long run at most 25 to 30% of weekly volume and 150 min. Recreational users default to pyramidal (some tempo, little all out work); competitive users can go polarized. Source: Daniels caps [seen, secondary]; Rosenblat 2025 IPD network MA [seen].

8. **Adding running to a strength plan:** keep runs mostly easy, put hard runs and leg strength on the same day with strength first, or separate them by at least 6 h, and keep legs' hardest day away from the interval day. Hypertrophy and max strength survive concurrent training; power suffers most. Source: Wilson 2012 as summarised in later MA [seen]; same session interference for explosive strength [seen]; 6 h spacing [believe].

9. **Kettlebell only users get a standard to chase.** Default to Simple and Sinister (100 swings, 10 get-ups, test against 5 min and 10 min) and move up a bell when the session is comfortable inside the times. Users who want pressing strength get Rite of Passage ladders 3 days per week. Source: StrongFirst / LiftVault [seen]; ETK summaries [seen].

10. **Bands are a real load, log them as data.** Record band colour, anchor distance (stretch) and reps every session so progression is visible. Strength gains match free weights. Source: Lopes 2019 MA [seen].

11. **Deconditioned, older or returning from injury users start with GMB style locomotion** (bear, monkey, frogger, crab, 15 min blocks) for 2 to 4 weeks before ladders. Source: GMB Elements [seen for content; believe for the 2 to 4 week bridge].

· · ·

## Could not verify this session

* No page opened in full: WebFetch failed DNS on reddit.com, old.reddit.com, a reddit mirror, nhs.uk, strongfirst.com, pubmed, pmc, vdoto2.com. Everything [seen] is from search engine extracts.
* No "Rosenblat 2022" polarized vs pyramidal MA exists that I could find; 2019 (POL vs threshold) and 2025 (IPD network MA) do.
* BWF RR exact ladders and warm up contents: from memory.
* Overcoming Gravity numeric volume rules (reps per exercise, deload cadence): not confirmed.
* Convict Conditioning per step rep standards: not confirmed.
* Daniels % VO2max ranges per pace, and the easy run share: secondary sources conflict.
* Schoenfeld "2015" low vs high load paper: confirmed only via snippet, and it was formally published in JSCR 2016 (online 2015) [believe].
