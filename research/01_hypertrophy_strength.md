# 01 · Hypertrophy and Strength / Powerlifting schools

Research cluster for the shareable "Personal trainer" agent. Compiled 2026-11-13.

## How to read the tags

- **[checked]**: the claim was confirmed this session in text from the cited source as returned by web search (journal abstract, official program page, author site or official support doc). **Limit to know:** WebFetch was blocked by the session network for every host I tried (pubmed.ncbi.nlm.nih.gov, sportrxiv.org, rpstrength.com, jimwendler.com), so no full page was opened. "Checked" means confirmed in a search excerpt of that source, not a full read of the paper.
- **[believe]**: from memory, or only from a secondary site (app listings, blogs, Lift Vault, Boostcamp, Liftosaur, fitnessvolt). Treat as plausible, verify before hard coding.
- **Evidence level** per school: **A** = core principle supported by RCTs or meta-analyses · **B** = coach consensus built on A-level principles but the specific program is not itself trialled · **C** = anecdote / tradition.

Key fact for the agent: almost no named program has been tested head to head in an RCT. The evidence supports *principles* (volume dose, load range, proximity to failure, frequency, progressive overload, autoregulation). Programs are packaging of those principles. The agent should pick on principle fit plus adherence fit (days, time, equipment, preference).

* * *

## Part 1 · The evidence base (principles)

| topic | finding | tag | source |
|:-|:-|:-|:-|
| Weekly volume, hypertrophy | Graded dose response: under 5 weekly sets per muscle ~5.4% growth, 5 to 9 sets ~6.6%, 10+ sets ~9.8%. Continuous volume significant (P = 0.002). Data only allowed conclusions up to ~10 sets; only two included studies used trained subjects. | [checked] | Schoenfeld, Ogborn, Krieger 2017, J Sports Sci. [PDF](https://researchgate.net/profile/Brad-Schoenfeld/publication/305455324), [Krieger commentary](https://biolayne.com/reps/issue-31/the-king-of-volume-metas/) |
| Volume and frequency meta-regression | Pelland et al., "The resistance-training dose response: meta-regressions exploring the effects of weekly volume and frequency on muscle hypertrophy and strength gains", Sports Med, doi 10.1007/s40279-025-02344-w (~67 studies, ~2058 participants). Volume positively associated with growth with diminishing returns and no clear plateau in the primary model; low minimum effective dose (~4 fractional weekly sets). Frequency: negligible effect on hypertrophy once volume is accounted for, clear positive effect on strength. "Fractional" set counting (indirect sets count 0.5) fit hypertrophy best, "direct" counting fit strength best. | [checked] for title/doi and direction of effects (search excerpts); [believe] for exact study counts | [SportRxiv preprint](https://sportrxiv.org/index.php/server/preprint/view/460), [FAU press release](https://fau.edu/newsdesk/articles/build-muscle-gain-strength-study.php), [EurekAlert](https://www.eurekalert.org/news-releases/1086804) |
| Frequency (older) | Training a muscle 2x/week gave larger effect size than 1x (0.49 vs 0.30), but higher frequency groups often did more volume. Volume-equated 2019 follow up: no meaningful difference. | [checked] 2016; [believe] 2019 | Schoenfeld, Ogborn, Krieger 2016, Sports Med. [PDF](https://springerlink.bibliotecabuap.elogim.com/content/pdf/10.1007/s40279-016-0543-8.pdf) |
| Load range | 21 studies: 1RM strength gains greater with heavy loads; hypertrophy similar across a wide load spectrum (roughly 30% to 80%+ 1RM when sets go hard). | [checked] | Schoenfeld et al. 2017, JSCR, PMID 28834797. [pubmed.gov](https://www.pubmed.gov/28834797/) |
| Practical rep range | Hypertrophy works from about 6 to 30+ reps when close to failure; very high reps are more uncomfortable and fatiguing per set. | [believe] (derived from the load meta-analysis plus Schoenfeld's practical writing) | as above |
| Proximity to failure, hypertrophy | Failure vs non-failure: small effect favouring failure (ES 0.19, 95% CI 0.00 to 0.37, p = 0.045) for any failure definition; no advantage when restricted to momentary muscular failure. Suggests a non-linear relationship. A 2024 letter (Fonseca et al.) flagged possible sample size errors. | [checked] | Refalo, Helms, Trexler, Hamilton, Fyfe 2023, Sports Med 53(3):649 to 665. [bibbase](https://bibbase.org/network/publication/refalo-helms-trexler-hamilton-fyfe-influenceofresistancetrainingproximitytofailureonskeletalmusclehypertrophyasystematicreviewwithmetaanalysis-2023), [AUT repository](https://openrepository.aut.ac.nz/items/78679612-6ff4-4d00-95d1-7920d072a760/full) |
| Proximity to failure, dose response | Meta-regressions on estimated RIR (~55 studies): hypertrophy improves as sets end closer to failure; strength gains similar across a wide RIR range. Authors call it exploratory. | [checked] | Robinson et al. 2024, Sports Med, doi 10.1007/s40279-024-02069-2. [Abertay record](https://rke.abertay.ac.uk/en/publications/exploring-the-dose-response-relationship-between-estimated-resist/), [FAU release](https://www.fau.edu/newsdesk/articles/muscle-growth-strength-study) |
| Long muscle length | Knee extension, untrained women: partials in the lengthened position beat shortened partials and were at least equal to full ROM. | [checked] direction; [believe] magnitude | Pedrosa et al. 2022 (online 2021), Eur J Sport Sci, doi 10.1080/17461391.2021.1927199. [summary](https://train.fitness/personal-trainer-blogs/do-half-reps-build-as-much-muscle) |
| Long muscle length | Overhead triceps extension grew the triceps ~20% vs ~14% for neutral pushdowns over 12 weeks. | [checked] | Maeo et al. 2022/2023, Eur J Sport Sci. [summary](https://getfitcraft.com/science/lengthened-partials-research) |
| Long muscle length | Seated leg curl (hip flexed, hamstrings longer) gave more hamstring growth than prone leg curl over 12 weeks. | [checked] | Maeo et al. 2021, Med Sci Sports Exerc 53(4):825 to 837 |
| RIR-based RPE scale | RPE 10 = 0 RIR, RPE 9 = 1 RIR, etc. Experienced lifters rated 1RM higher than novices; scale described as a practical way to regulate daily load. Implication: novices estimate RIR less accurately. | [checked] | Zourdos et al. 2016, JSCR 30(1):267 to 275, doi 10.1519/JSC.0000000000001049. [AUT](https://openrepository.aut.ac.nz/items/efef3b25-6701-4fb5-bb82-55fcd2a26027/full) |
| RIR scale application | Practitioner guide to using the RIR-based RPE scale. | [checked] (existence) | Helms et al. 2016, Strength Cond J. [AUT](https://openrepository.aut.ac.nz/items/92cefeac-7c32-44f1-bfbc-f48f4a5dd8cf/full) |
| RPE vs %1RM | Trained men, 8 weeks DUP, squat and bench 3x/week, sets and reps matched: both groups gained strength and muscle thickness, no significant difference; RPE showed a small 1RM edge in most individuals. n = 21. | [checked] | Helms et al. 2018, Front Physiol, doi 10.3389/fphys.2018.00247. [Frontiers](https://www.frontiersin.org/articles/10.3389/fphys.2018.00247/text) |

* * *

## Part 2 · Hypertrophy schools

### Renaissance Periodization (Mike Israetel)

| field | content |
|:-|:-|
| Prescribes | Volume landmarks per muscle per week: **MV** (maintenance), **MEV** (minimum effective), **MAV** (maximum adaptive, best gain per fatigue), **MRV** (maximum recoverable). [believe, secondary sources only, RP site unreachable] |
| Split / days | Any split; typically each muscle 2x/week or more, 4 to 6 days. [believe] |
| Volume | Start mesocycle near MEV, add sets weekly (often ~1 to 2 sets per muscle per week, driven by soreness/pump/performance feedback), approach MRV by the last accumulation week. Third party tables put MEV ~8 to 10, MAV ~12 to 18, MRV ~18 to 22+ sets per muscle per week, with big differences by muscle and person. [believe] |
| Intensity | Load range ~5 to 30 reps; RIR progresses from ~3 to 4 RIR in week 1 down to ~0 to 1 RIR in the final week. [believe] |
| Progression | Add reps or load at the target RIR week to week, and add sets as recovery allows. [believe] |
| Deload | After 4 to 6 accumulation weeks, or when MRV is hit early: 1 week at roughly half volume and lower effort. [believe] |
| For | Intermediate to advanced, hypertrophy goal, 4 to 6 days, 60 to 90 min. |
| Equipment | Full gym preferred (machines, cables). |
| Evidence | **B**. Volume dose and proximity to failure principles are A-level (Schoenfeld 2017, Pelland, Robinson 2024). The landmark numbers themselves are coach estimates, not measured constants. |
| Sources | [arvo.guru summary](https://arvo.guru/resources/methods/rp-training), [Lift Vault RP template](https://liftvault.com/programs/bodybuilding/mike-israetel-5-week-hypertrophy-workout-routine-spreadsheet/), [RP progressing article](https://rpstrength.com/blogs/articles/progressing-for-hypertrophy) (not opened) |

### Brad Schoenfeld (evidence school, not a branded program)

- **Prescribes:** ~10+ hard sets per muscle per week as a sensible floor, each muscle trained at least 2x/week, loads anywhere from ~6 to 30 reps taken close to failure, mix of heavy compound and moderate/light isolation work. [checked for the underlying data, believe for the packaged rule]
- **For:** everyone; the baseline the agent can fall back on.
- **Evidence:** **A** (he authored most of the meta-analyses in Part 1).

### Jeff Nippard · Fundamentals and PowerBuilding family

| field | content |
|:-|:-|
| Fundamentals | Beginner to intermediate, build muscle while gaining strength. Three versions: Full Body 3 days/week, Upper/Lower 4 days/week (Mon, Tue, Thu, Fri), Bodypart split 5 days/week. [checked, jeffnippard.com product page] |
| Other programs | Upper Lower Size & Strength (intermediate to advanced; Nippard advises Fundamentals first if in year 1 to 2) [checked] · Pure Bodybuilding (intermediate to advanced, PPL 5 to 6 days or Full Body / Upper Lower 4 to 5 days, 10 weeks) [checked] · High Frequency Full Body (full body ~4x/week) [checked] · PowerBuilding (strength on the big three plus hypertrophy accessories) [believe, not found this session] |
| Intensity / progression | RPE/RIR targets per set, final sets of isolations often to failure, double progression (add reps in a range, then load). [believe] |
| Deload | Scheduled deload weeks inside blocks. [believe] |
| Equipment | Full gym. |
| Evidence | **B**. Explicitly built on the Part 1 literature; program not trialled. |
| Sources | [Fundamentals](https://jeffnippard.com/products/fundamentals-hypertrophy-program), [Upper Lower Size & Strength](https://jeffnippard.com/products/upper-lower-size-and-strength-program), [Pure Bodybuilding](https://jeffnippard.com/products/the-pure-bodybuilding-program-preorder), [Ultimate PPL](https://jeffnippard.com/products/the-ultimate-push-pull-legs-system) |

### PHUL (Power Hypertrophy Upper Lower)

- **Prescribes:** 4 days: Upper Power, Lower Power, rest, Upper Hypertrophy, Lower Hypertrophy. Power days ~3 to 5 reps on compounds, hypertrophy days ~8 to 15 reps. Each muscle ~2x/week. [checked structure via secondary; rep ranges believe]
- **Creator:** Brandon Campbell. [checked, secondary]
- **Progression:** add load when the top of the rep range is hit. [believe]
- **For:** late novice to intermediate, size and strength, 4 days, ~60 to 75 min. Full gym.
- **Evidence:** **B**.
- **Sources:** [Hevy PHUL](https://www.hevyapp.com/phul-power-hypertrophy-upper-lower/), [Lift Vault](https://liftvault.com/programs/bodybuilding/phul-spreadsheet/)

### PHAT (Layne Norton)

- **Prescribes:** 5 days: Upper Power, Lower Power, rest, then Back/Shoulders hypertrophy, Lower hypertrophy, Chest/Arms hypertrophy. Power days ~3 to 5 reps; hypertrophy days include "speed work" at ~65 to 70% of the power day loads for 6 to 8 x 3, then 8 to 20 rep work. [checked 5 day / 2 power + 3 hypertrophy via secondary; speed work detail believe]
- **For:** intermediate to advanced, powerbuilding, 5 days, 75 to 90 min. Full gym.
- **Evidence:** **B** (conflict: one app lists it as 6 days).
- **Sources:** [Hevy PHAT](https://www.hevyapp.com/phat-workout/), [powerliftingtechnique](https://powerliftingtechnique.com/phat-workout-program/)

### Push / Pull / Legs

- **Prescribes:** PPL once (3 days) or twice (6 days) per week. 6 day version gives each muscle 2x/week. Typical 3 to 5 exercises per day, 3 to 4 sets, 6 to 15 reps. [believe]
- **For:** 3 days = novice/time poor (frequency 1x, weaker for strength per Pelland); 6 days = intermediate to advanced with time.
- **Evidence:** **B** for the 6 day version (meets frequency and volume principles), weaker for 3 day PPL on strength.

### Arnold "Golden Six" and Arnold split / bro splits

- **Golden Six:** 3 full body days on alternate days, same six lifts each time: back squat 4x10, wide grip bench 3x10, chin up 3xAMRAP, behind the neck press 4x10, barbell curl 3x10, sit up 3 to 4xAMRAP; ~20 sets, ~1 hour; no direct triceps work. [checked via secondary sources, Lift Vault and Fitnessvolt agree]
- **Arnold split:** 6 days, chest+back / shoulders+arms / legs, done twice per week, very high volume (often 20+ sets per body part per session). [believe]
- **Classic bro split:** 5 days, one body part per day, each muscle 1x/week, 15 to 25 sets per session. [believe]
- **For:** Golden Six: novice, 3 days, barbell + chin bar. Arnold split: advanced only, high recovery capacity, 6 days, 90 to 120 min. Bro split: intermediate who prefers it.
- **Evidence:** **C** as programs. Bro split's 1x/week frequency is not worse for hypertrophy when volume is matched (Pelland, Schoenfeld 2019), but per-session volume beyond ~10 sets per muscle shows diminishing returns (this is the frequency rationale) [believe for the per-session ceiling].
- **Sources:** [Lift Vault Golden Six](https://liftvault.com/programs/bodybuilding/arnold-schwarzenegger-workout-routine-golden-six/), [Fitnessvolt](https://fitnessvolt.com/arnold-golden-six-routine/)

* * *

## Part 3 · Strength / powerlifting schools

### Wendler 5/3/1 (core)

| field | content |
|:-|:-|
| Training max | TM = 90% of true 1RM (later Forever books lean to 85%, and Wendler pushes "start too light"). Run periodic TM test weeks and lower TM if too high. [checked 90% and TM test; 85% believe] |
| Waves | Week 1: 65/75/85% TM x5, 5, 5+ · Week 2: 70/80/90% x3, 3, 3+ · Week 3: 75/85/95% x5, 3, 1+ · Week 4 deload: 40/50/60% x5. [believe, standard and consistent across sources] |
| Split | 4 days, one main lift per day (squat, bench, deadlift, press); 3 day and 2 day variants. |
| Progression | After each cycle: +5 lb (2.5 kg) TM upper, +10 lb (5 kg) TM lower. [checked in 5/3/1 Beginners sources] |
| Stall | Reset TM down ~10% or by 3 cycle increments. [checked for Beginners stall rule, Liftosaur] |
| Boring But Big | After main work, 5x10 of the same (or paired) lift at 50 to 60% TM; Wendler: from cycle three you can use 60% for all cycles; deload: 5x10 or cut to 3x10. Assistance light: chin ups, dips, rows. [checked, jimwendler.com excerpt] |
| Leaders / anchors (Forever) | Leaders (usually 2 cycles) build volume at lower main-lift intensity; anchor (1 cycle) realises it with higher intensity and PR sets; a 7th week deload or TM test between. [checked leader/anchor logic; 7th week believe] |
| For | Late novice to advanced; general strength, powerlifting, athletes; 2 to 4 days, 45 to 75 min. |
| Equipment | Barbell, rack, bench, plates, chin bar. |
| Evidence | **B**. Submaximal TM, AMRAP autoregulation and slow progression match principles; no RCT of 5/3/1 itself. |
| Sources | [BBB, jimwendler.com](https://www.jimwendler.com/blogs/jimwendler-com/101077382-boring-but-big), [5/3/1 Primer](https://thefitness.wiki/5-3-1-primer/), [Lift Vault leaders/anchors](https://liftvault.com/resources/leader-anchor-cycles/), [On starting too light](https://physicalculture.substack.com/p/on-starting-too-light) |

### 5/3/1 for Beginners

- **Prescribes:** 3 full body days, two main lifts per session (e.g. Mon squat + bench, Wed deadlift + press, Fri bench + squat), 5/3/1 waves then **FSL 5x5** (first set weight: 65/70/75% TM). Assistance 50 to 100 reps each of push, pull, single leg/core every session. Conditioning on off days. TM 90%. [checked via secondary sources]
- **Progression:** +5 lb upper, +10 lb lower per 3 week cycle; no built-in deload week (Wendler suggests a deload/TM test every few cycles). [checked]
- **For:** novice to early intermediate, 3 days, ~60 min. Barbell gym.
- **Evidence:** **B**.
- **Sources:** [thefitness.wiki](https://thefitness.wiki/routines/5-3-1-for-beginners/), [Lift Vault](https://liftvault.com/programs/strength/531-for-beginners/), [Liftosaur](https://liftosaur.com/programs/the5314b)

### Starting Strength (Rippetoe) · novice linear progression

- **Prescribes:** 3 non-consecutive days, alternating A/B: squat 3x5 every session; bench and press alternate 3x5; deadlift 1x5 (power clean added later). [checked, secondary]
- **Progression:** add weight every session (classic ~5 to 10 lb squat/deadlift, ~2.5 to 5 lb presses, smaller as it slows). [believe]
- **Stall/deload:** repeat weight; after repeated failures reset ~10% and work back. Do not leave LP too early. [checked "don't jump ship", believe exact reset]
- **Next step:** Texas Method (Rippetoe's suggested continuation) though startingstrength.com also argues Texas Method and 5/3/1 are not best for most people finishing LP. [checked, sources conflict]
- **For:** true novice, strength goal, 3 days, 60 to 90 min (long rests). Barbell, rack, bench, plates.
- **Evidence:** **B to C**. Novice rapid progression is real; the minimal volume (3x5, little upper back/arm work) is weak for hypertrophy relative to the volume literature.
- **Sources:** [Liftosaur SS](https://www.liftosaur.com/programs/ss3), [Don't jump ship](https://mail.startingstrength.com/article/dont-jump-ship-earning-the-transition-from-novice-to-intermediate-training), [intermediate assessment PDF](https://startingstrength.com/contentfiles/intermediate_program_assessment.pdf)

### Texas Method

- **Prescribes:** 3 days/week: **Volume day** (Mon) squat 5x5 at ~90% of the Friday 5RM, the main weekly stressor; **Recovery day** (Wed) light squats ~80% of Monday, light press; **Intensity day** (Fri) a new 5RM single top set. [checked structure; percentages believe]
- **Progression:** weekly, a PR on Friday each week. [checked]
- **For:** post-novice (LP exhausted), strength, 3 days. Barbell.
- **Evidence:** **B to C**.
- **Sources:** [Understanding the Texas Method intensity day](https://mail.startingstrength.com/article/understanding-the-texas-method-intensity-day), [The Texas Method](https://mail.startingstrength.com/article/the_texas_method)

### StrongLifts 5x5 (Mehdi)

- **Prescribes:** 3 non-consecutive days alternating A (squat, bench, barbell row) and B (squat, overhead press, deadlift); 5x5 except deadlift 1x5. [checked, official support doc + secondary]
- **Progression:** +2.5 kg / 5 lb per workout on squat, bench, press, row; deadlift +5 kg / 10 lb until ~100 kg then +2.5 kg. Missed reps: repeat weight. [checked, support.stronglifts.com]
- **Deload:** 3 consecutive failed workouts on a lift: cut 10% (app may suggest 1 kg microloading). [checked]
- **For:** true novice, 3 days, 45 to 60 min. Barbell, rack, bench.
- **Evidence:** **B to C** (same as SS: novice LP principle).
- **Sources:** [StrongLifts increments](https://support.stronglifts.com/article/71-increments), [All Things Gym summary](https://www.allthingsgym.com/summary-of-stronglifts-5x5/)

### GZCL / GZCLP (Cody Lefever)

- **Tiers:** **T1** main compound, heavy, low reps (GZCLP: 5x3+ at ~85% of 5RM, last set AMRAP); **T2** secondary compound, 3x10 lighter; **T3** accessory, 3x15+ with last set AMRAP. Volume ratio 1:2:3 reps T1:T2:T3. [checked, secondary]
- **Split:** GZCLP 4 days (3 day variants), each day 1 T1 + 1 T2 + T3s.
- **Progression (GZCLP):** add load each session when all reps met. On failure T1 moves 5x3 then 6x2 then 10x1, then retest 5RM and restart at 85%. T2 moves 3x10 then 3x8 then 3x6, then reset. T3 adds load when the AMRAP reaches 25 reps. [believe for the stage sequence; not confirmed this session]
- **For:** late novice to early intermediate, strength + size, 3 to 4 days, 60 to 75 min. Barbell gym plus some machines/dumbbells.
- **Evidence:** **B**.
- **Sources:** [Boostcamp GZCLP](https://www.boostcamp.app/coaches/cody-lefever/gzcl-program-gzclp), [Lift Vault GZCLP](https://liftvault.com/programs/powerlifting/gzclp-program-spreadsheets), [GZCL substack](https://gzcl.substack.com/p/p-zero)

### Sheiko (Boris Sheiko)

- **Prescribes:** high frequency on the competition lifts: bench ~3x/week, squat ~2x, deadlift ~1x (numbered programs #29 to #32 run 3 days/week; 4 day versions exist). Average intensity ~70% 1RM (±2%), most work 70 to 80%, some 80 to 90%, rarely above 90%. Many sets of 1 to 5 reps, never near failure. [checked, secondary]
- **Volume:** counted in lifts (NL) per month: roughly 700 for beginners, 600 to 750 prep for intermediates, up to 900 to 1900 for elite; NL drops ~20 to 40% in competition cycles. Mix ~20% competition lifts, ~60% variations/special exercises, ~20% GPP. [checked, secondary, coach write-ups]
- **Progression:** fixed 4 week blocks from %1RM; retest after a block. **Deload:** built into block waves. [believe]
- **For:** intermediate to advanced powerlifters, 3 to 4 days, 90 to 150 min. Barbell, bench, rack.
- **Evidence:** **B** (submaximal, high frequency practice fits frequency-for-strength data from Pelland; program not trialled).
- **Sources:** [powerliftingtowin Sheiko](https://powerliftingtowin.com/sheiko), [simplifaster](https://simplifaster.com/articles/sheiko-system-powerlifting/), [Kevin Cann](https://robbwolf.com/2016/09/22/what-i-have-learned-about-programming-from-sheiko/)

### Westside / Conjugate (Louie Simmons)

- **Prescribes:** 4 days: Max Effort lower, Max Effort upper, Dynamic Effort lower, Dynamic Effort upper. **ME:** work to a 1 to 3RM on a variation that rotates weekly (box squat, good morning, deadlift variants, floor press, board press). **DE:** speed work in 3 week pendulum waves, e.g. box squat 12x2 at 70%, 10x2 at 75%, 8x2 at 80% with ~25% accommodating resistance; bench speed ~9x3. **Repetition method / accessories:** ME lower accessories hit hamstrings/glutes (2), low/mid back (1), quads (1). Short rests on DE (~60 s). [checked, westside-barbell.com excerpts]
- **Progression:** variation rotation and new PRs on variations; waves restart with new bands/variations. **Deload:** no classic deload, rotation manages fatigue. [believe]
- **For:** advanced, often equipped lifters; raw adaptations exist. 4 days, 60 to 90 min. Specialty bars, boxes, bands/chains, reverse hyper ideal.
- **Evidence:** **C to B** (velocity/accommodating resistance has some trial support; the system is tradition).
- **Sources:** [Westside conjugate](https://westside-barbell.com/pages/conjugate-method), [DE lower structure](https://www.westside-barbell.com/a/blog/wsbb-blog-structuring-your-de-lower-training), [ME lower walkthrough](https://www.westside-barbell.com/a/blog/starting-conjugate-me-lower-walkthrough)

### Reactive Training Systems (Mike Tuchscherer)

- **Prescribes:** sets prescribed by reps @ RPE (e.g. 1 @ 8, then volume). Chart maps reps x RPE to %1RM (e.g. 5 reps @ RPE 8 = 81.1%). **e1RM** = load / chart % (e.g. 300 lb x3 @ 8 ≈ 87.5%, e1RM ≈ 343). Tuchscherer warns the chart is a guide, accuracy drifts as a cycle goes on. [checked]
- **Fatigue percents:** after a top set, either "load drop" (reduce load by X%, e.g. 5%, and do sets until RPE returns to the top set RPE) or "repeat" sets at the same load until the RPE rises to a cap; X% is the fatigue target (often 3 to 9%). [believe, not found this session]
- **For:** intermediate to advanced powerlifters with good RPE accuracy; 3 to 5 days. Barbell gym.
- **Evidence:** **A to B** for RIR/RPE autoregulation as a method (Zourdos 2016, Helms 2018); fatigue percent method is coach practice.
- **Sources:** [EliteFTS, Tuchscherer ch. 2](https://elitefts.com/blogs/training/rate-of-perceived-exertion-rpe), [Fitnessvolt RPE chart](https://fitnessvolt.com/rpe-training/guides/tuchscherer-chart-explained)

### Stronger by Science (Greg Nuckols)

- **Programs:** SBS Linear Progression, SBS Novice Hypertrophy, SBS Hypertrophy Template, SBS Strength Program in Last Set RIR and Last Set Reps To Failure (RtF) versions, each in normal and LF variants. [checked lineup via a fan compiled doc, believe exact names]
- **Mechanism (RtF):** each main lift's last set is AMRAP against a target; beating the target raises the next week's TM, missing lowers it. 20 week, 2 to 5 day templates with deloads at weeks 7 and 14, reps per set trend down over the block with undulation. Up to 3 user-chosen accessories per day. [checked deload weeks via a review; believe AMRAP TM rule]
- **Stance:** most sets 1 to 3 RIR, some final isolation sets to failure. [checked, secondary]
- **For:** novice (LP) to intermediate; 2 to 6 days. Barbell gym.
- **Evidence:** **B to A** (autoregulated AMRAP progression matches RPE/RIR evidence).
- **Sources:** [Reddit RtF review](https://redlib.reallyaweso.me/r/weightroom/comments/1ccu48o/program_review_stronger_by_science_reps_to/l18cxn0/?context=3), [SBS MASS best of](https://www.strongerbyscience.com/wp-content/uploads/2022/04/Best-Of-MASS-2021-2022.pdf)

* * *

## Part 4 · Quick selection grid

| profile | days | strength goal | hypertrophy goal | both |
|:-|:-|:-|:-|:-|
| novice, barbell gym | 3 | StrongLifts 5x5 or Starting Strength, then 5/3/1 Beginners | Nippard Fundamentals Full Body, SBS Novice Hypertrophy | 5/3/1 for Beginners, GZCLP 3 day |
| novice / late novice | 4 | GZCLP | Fundamentals Upper/Lower | PHUL, GZCLP |
| intermediate | 3 | Texas Method, 5/3/1 (3 day), SBS RtF 3 day | Full body 3x, RP style meso | 5/3/1 BBB |
| intermediate | 4 | 5/3/1 Forever leaders/anchors, SBS RtF 4 day, Sheiko 4 day | Upper/Lower, RP meso | PHUL, Nippard ULSS |
| intermediate to advanced | 5 to 6 | Sheiko, RTS, conjugate (if equipment) | PPL x2, Pure Bodybuilding, RP | PHAT, Nippard PowerBuilding |
| home, minimal kit | 2 to 4 | (barbell needed for this cluster) | dumbbells/bands, high rep to near failure works per load meta-analysis | see other clusters |

* * *

## For the agent

1. **Default hypertrophy dose: 10 to 20 hard sets per muscle per week, start new users at the low end (~8 to 12) and add sets only while recovery and performance hold.** Gains rise with volume with diminishing returns; 10+ beats under 10. Source: Schoenfeld, Ogborn, Krieger 2017; Pelland et al. Sports Med (doi 10.1007/s40279-025-02344-w). Count indirect sets (e.g. rows for biceps) as 0.5 when tallying hypertrophy volume, per Pelland's fractional counting.
2. **Train each muscle at least 2x/week, and train a lift more often when the goal is strength.** Frequency barely matters for hypertrophy once volume is equal, but strength rises with frequency, and splitting volume keeps per-session sets manageable. Source: Pelland et al.; Schoenfeld 2016.
3. **Pick the rep range from the goal, not dogma: strength users need regular heavy work (roughly 1 to 6 reps, ≥ 80% 1RM) on the target lifts; for hypertrophy any range from ~6 to 30 reps works if sets end close to failure.** Source: Schoenfeld et al. 2017 JSCR (PMID 28834797).
4. **Effort rule: hypertrophy sets at 0 to 3 RIR (compounds 1 to 3, isolation last set 0 to 1); strength work can sit at 2 to 4 RIR with no loss.** True failure gives at most a small extra growth effect and costs fatigue. Source: Refalo et al. 2023; Robinson et al. 2024.
5. **Novices: do not rely on RPE/RIR alone, use fixed linear progression.** Novices misjudge effort near 1RM (Zourdos 2016). Rule: 3 day/week novice wanting strength gets StrongLifts 5x5 or Starting Strength style LP (+2.5 kg upper / +5 kg lower per session, repeat on a miss, cut 10% after 3 consecutive misses), then graduates to 5/3/1 for Beginners or GZCLP when session-to-session progress stalls twice. Source: StrongLifts support docs; Zourdos 2016.
6. **Intermediates: autoregulate.** Use a submaximal training max (90% of 1RM, or 85% if unsure) with an AMRAP last set (5/3/1, SBS RtF) or RPE targets (RTS). Raise TM +2.5 kg upper / +5 kg lower per cycle; if the AMRAP misses its minimum, drop TM ~10%. RPE loading is at least as good as %1RM. Source: Helms et al. 2018; jimwendler.com BBB page; 5/3/1 Beginners rules.
7. **Hypertrophy progression: double progression inside a mesocycle.** Hit the top of the rep range at the target RIR on all sets, then add the smallest load; ramp effort from ~3 RIR to ~0 to 1 RIR over 4 to 6 weeks, then deload one week (halve sets, stay 3+ RIR). Deload early if performance drops two sessions running. Source: RP mesocycle model (coach consensus, evidence level B) on top of Robinson 2024.
8. **Bias exercise choice toward long muscle length positions** (overhead triceps extension, seated leg curl, deep squats and RDLs, incline curls, lengthened partials at the end of a set). Source: Maeo 2021 (MSSE), Maeo 2022/23 (EJSS), Pedrosa 2022 (EJSS).
9. **Match program to schedule first, then to school.** Adherence beats design: 3 days = full body (Golden Six style, Fundamentals Full Body, 5/3/1 Beginners); 4 days = upper/lower (PHUL, GZCLP, Fundamentals U/L); 5 to 6 days = PPL x2 / PHAT / Sheiko. Never give a 1x/week bro split to someone whose goal is strength, and never give Westside/conjugate or Sheiko to a novice. Source: program pages above; frequency evidence from Pelland.
10. **Tell the user the evidence level.** Every named program is evidence level B or C; the agent should present programs as "evidence-based packaging" and cite the principle (volume, load, effort, frequency) that justifies the choice. Source: absence of program-vs-program RCTs in this cluster's literature (believe).

* * *

## Not verified this session

- Full texts of any paper (all hosts blocked for WebFetch); effect sizes for Pelland and Robinson beyond direction.
- RP's own MEV/MAV/MRV numbers per muscle (rpstrength.com blocked); all per-muscle figures above are third party.
- GZCLP failure stage sequence (5x3, 6x2, 10x1; 3x10, 3x8, 3x6) and T3 25 rep rule.
- RTS fatigue percent method numbers.
- 5/3/1 Forever 85% TM default and the 7th week protocol.
- Exact Starting Strength increments and reset percentage.
- Nippard PowerBuilding specifics; PHAT speed work percentages.
- Arnold 6 day split structure.
- Schoenfeld 2019 volume-equated frequency meta-analysis (seen only in secondary sources).
