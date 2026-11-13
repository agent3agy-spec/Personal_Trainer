# 06 · The interview audit · from its author's training to anyone's

Research cluster for the shareable Personal trainer agent. Compiled 13 Nov 2026, after the owner's walkthrough (`../Personal trainer · walkthrough notes.md`, section 2). Scope: audit every onboarding question in `doctrine/02_INTERVIEW.md` and `.claude/skills/train/SKILL.md` against fourteen kinds of people, look at how serious coaches and the best consumer apps take an intake, find which inputs actually change program choice and dosing, then propose a branching interview, the engine fields it needs, and the ten changes worth making first.

This file holds no rules. If it is adopted, the rules move to `doctrine/02_INTERVIEW.md`, `03_MATRIX.md` and the engine, and this note stays as found (see `README.md`).

## How to read the marks

Same marks as files 01 to 04. Page fetches were not used this session; everything below was confirmed in search engine extracts of the named source.

| mark | meaning |
|:-|:-|
| **[checked]** | confirmed this session in a search extract quoting the named source (abstract, official help page, official manual). Not a full read. |
| **[seen]** | confirmed only in a secondary source (a review, a design teardown, an app store listing, a forum post by staff). Good enough for "what an app asks", never for a training rule. |
| **[believe]** | from memory or a single weak source. A lead, not a rule. |
| **[inferred]** | reasoned from checked parts. |

Where a claim drives a design change, two independent sources are named. Where only one was found, it says so.

* * *

## Part 1 · What the evidence says to ask

### 1.1 How serious coaching intake is done

| finding | mark | sources |
|:-|:-|:-|
| The NSCA personal trainer job analysis puts three things before any program: a personal and family medical history or health appraisal, **a lifestyle questionnaire that includes exercise and injury history**, and then goals set by discussing the interview, the history and a fitness evaluation together. Goals are an output of the intake, not its first question. | [checked] | NSCA-CPT certification handbook 2025, [PDF](https://dxpprod.nsca.com/globalassets/certification/certification-pdfs/certification-handbook-2025-nsca-cpt-dco.pdf) · NSCA-CPT detailed content outline 2019, [PDF](https://dxpprod.nsca.com/globalassets/certification/certification-pdfs/cpt-dco-public-view-effective-01-2019-.pdf) |
| The NSCA strength coach "needs analysis" has two stages: **an evaluation of the sport** (movement analysis, physiological analysis: strength, power, size or endurance priority; injury analysis: the common injury sites of that sport) and **an assessment of the athlete** (training status: type of prior program, how long they have trained regularly, how hard, and their technique experience; then tests chosen from the sport analysis). | [seen] (textbook chapter reproduced in study notes, not the book) | NSCA Essentials ch. 17 summaries: [Medium CSCS notes](https://medium.com/@troytheschumer/nsca-cscs-chapter-17-program-design-for-resistance-training-34aa667e1e1d), [Faster Function needs analysis](https://fasterfunction.learnworlds.com/blog/level4-strength-conditioning-coach-needs-analysis) · NSCA's own [Needs analysis for a tactical athlete](https://www.nsca.com/education/articles/kinetic-select/needs-analysis-for-a-tactical-athlete/) uses the same two stages |
| NASM puts intake (PAR-Q, history, lifestyle) first and movement tests after it; OPEX makes the movement assessment a separate third step after the consultation. Both treat **movement quality and pain history** as their own block, not one line. | [seen] | [NASM movement assessments](https://blog.nasm.org/a-guide-to-movement-assessments) · [OPEX assessment guide](https://pages.opexfit.com/hubfs/Fitness%20Assessments%20for%20New%20Clients%20PDF%20Guide.pdf?hsLang=en) |
| Intake forms used by online coaches group questions into: personal info, health history, **goals, exercise experience, lifestyle (sleep, stress, job), preferences**. | [seen] | [FitBudd onboarding questionnaire guide](https://fitbudd.com/post/the-ultimate-guide-to-writing-the-perfect-onboarding-questionnaire-for-personal-trainers) · [Coachway athlete needs analysis](https://coachway.io/articles/jared-feather-athlete-needs-analysis-for-coaches/) ("goal, history, recovery, weak points and logistics") |
| PAR-Q+ already gates the screen (`01_SAFETY.md`). Nothing here changes Round 0. | [checked in file 04] | file 04 §6 |

**What this means for us [inferred]:** the current interview covers medical screen, goal, logistics and a thin "you" round. It is missing three blocks every professional intake has: **training history by type** (not one experience label), **lifestyle recovery** (sleep, stress, job), and **injury history as history**, not just "pain now".

### 1.2 How the best consumer apps onboard

None of these apps publishes its full question list. What follows is pieced from help pages, design teardowns and reviews, so the exact order is [seen] at best.

| app | what it asks | order and taps | what it infers or learns instead of asking | mark · source |
|:-|:-|:-|:-|:-|
| **Future** (human coach) | a short quiz on goals, experience, equipment, lifestyle; then matches four coaches; then a video kickoff call where the coach takes the real history | quiz before account, then the call | the coach fills every gap in conversation | [seen] [Medical News Today](https://www.medicalnewstoday.com/articles/future-review) · [App Store](https://apps.apple.com/us/app/-/id1288178982) · [Future FAQ](https://faq.future.co/en/articles/12073321-what-should-i-expect-from-my-future-coach) |
| **Caliber** | strength-training experience in years (with "2 to 5 years" as a tile), training frequency, where you train, workout duration, what you like to do, lifestyle, eating habits, equipment | "extensive" quiz, one question a screen | a **Strength Score** generated after the first week of logged lifts, so level is measured, not self-rated | [seen] [screensdesign teardown](https://screensdesign.com/showcase/caliber-strength-training) · [Tom's Guide](https://www.tomsguide.com/news/forget-chatgpt-this-workout-app-lets-you-text-your-personal-trainer-247) |
| **Fitbod** | goal (get stronger, build muscle, get lean, lose weight), experience (beginner, intermediate, advanced), a detailed equipment list; session length later in My Plan, 15 min to 1 h 30 **or a custom value** | three core screens, skippable and fixable later | loads from its strength model after the first logs | [checked] [Fitbod help: getting started](https://help.fitbod.me/hc/en-us/articles/30721771750039-Getting-Started-with-Fitbod-A-New-User-s-Guide) · [How Fitbod creates your workout](https://help.fitbod.me/hc/en-us/articles/360004429814-How-Fitbod-Creates-Your-Workout) · [seen] [Garage Gym Reviews](https://www.garagegymreviews.com/fitbod-review) |
| **Ladder** | a ~2 minute quiz that matches you to a **team by training style** (strength, bodybuilding, HIIT, kettlebell, Pilates-strength, hybrid) and level | about 2 minutes | the style is the product: people pick how they like to train | [seen] [joinladder llms.txt](https://www.joinladder.com/llms.txt) · [Garage Gym Reviews](https://www.garagegymreviews.com/ladder-app-review) |
| **TrainHeroic** | coach-led: the coach invites, the athlete joins a team; coaches can build their own **readiness survey** | setup is the coach's | the program is chosen by the coach, not the athlete | [checked] [TrainHeroic onboarding update](https://www.trainheroic.com/blog/product-update-mobile-athlete-onboarding/) · [support FAQ](https://support.trainheroic.com/hc/en-us/sections/17996086785933-FAQs-on-TrainHeroic-Functionality) |
| **Runna** (now Strava) | ability level, distance goal (5 km to marathon), days a week (1 to 7), current 5 km time, which days are free and which for the long run, a recent race time; then a Training Preferences screen to adjust weekly volume and longest run | about 8 screens | starting volume estimated from **how recently you last ran, how often you exercise and what kind of exercise you do** | [checked] [Runna support: how Runna builds your plan](https://support.runna.com/en/articles/15231838-how-does-runna-build-your-training-plan-around-your-current-fitness) · [seen] [Motion ad library quiz](https://library.motionapp.com/runna) · [Tom's Guide](https://www.tomsguide.com/wellness/fitness/i-signed-up-for-my-first-trail-race-and-let-an-app-train-me-heres-what-happened) |
| **Garmin Coach** (adaptive plans) | "answer a few questions": race distance and date, current fitness, schedule preferences, number of runs a week | a handful | adapts to your fitness level and training data from the watch | [checked] [Garmin manual: adaptive training plans](https://www8.garmin.com/manuals/webhelp/forerunner245/EN-US/GUID-71798B16-A9A9-4D0F-BF64-50DD65AFC0D5.html) · [seen] [Garmin forum](https://forums.garmin.com/sports-fitness/running-multisport/f/forerunner-265-series/417659/garmin-run-coach-newbie-questions) |
| **Freeletics** | gender, age, height, weight, goal (top three), fitness level, **preferred training style (bodyweight, running, weights)**, training days | long; one reviewer flags the drop-off risk | **the first week is an assessment week**: completion times tell the coach your strengths and weaknesses | [checked] [Freeletics: getting started](https://www.freeletics.com/en/blog/posts/getting-started-with-freeletics/) · [Freeletics forum, staff](https://forum.freeletics.com/t/onboarding-how-to-go-through-initial-assessment/2789) · [seen] [hotelgyms review](https://www.hotelgyms.com/blog/the-freeletics-fitness-app-review) |
| **Nike Training Club** | how often you work out, where, your level; per program "how often a week" | two to four questions | filters by equipment and duration later | [seen] [NTC teardown 2020](https://trailsofcuriosity.notion.site/Product-Teardown-Nike-Training-Club-Mobile-App-iOS-5e0cc8f9162c4089a5dde85f0d658f4f) · [Zoe Report review](https://www.thezoereport.com/wellness/nike-training-club-app-review) |
| **Apple Fitness+** custom plan | the days, total time a day, **up to five activity types** (HIIT, yoga, strength, Pilates, meditation...), plan length, trainers and music | five taps | nothing: it is a scheduler of liked activities | [checked] [Apple support: Custom Plans](https://support.apple.com/guide/fitness-plus/create-a-custom-plan-apdf222051d8/ios) |
| **WHOOP Coach** | lets you choose what to focus on; reads sleep, strain and recovery from the strap | conversational | recovery and sleep are measured daily, never asked | [checked] [WHOOP press](https://www.whoop.com/us/en/press-center/whoop-unveils-the-new-whoop-coach-powered-by-openai/) · [seen] [9to5Google](https://9to5google.com/2023/09/26/whoop-ai-coach-game-changer-hands-on/) |

**Patterns [inferred from the table]:**

1. **Style is asked as style.** Ladder, Freeletics and Apple Fitness+ all ask how people like to train (HIIT, yoga, strength, bodyweight, running), never "barbell or machines". Equipment is a separate, later question in every app that asks it.
2. **Level is learned, not trusted.** Caliber (Strength Score after week 1), Freeletics (assessment week), Fitbod (strength model) and Runna (last ran, how often, what kind) all start from a light self-report and correct it from the first logs. Our engine already does this for loads (`05_LOADS.md`, the first outing); the interview can lean on it and ask less.
3. **Running apps ask the time and the date, then the free days and the long-run day.** Runna asks a current 5 km time and the race date; it does not ask "how many years have you trained".
4. **Session length is open.** Fitbod allows a custom duration; Apple offers a duration per day. Four fixed cards is the outlier.
5. **Short quizzes win the top of the funnel.** Ladder's is about two minutes; reviewers flag Freeletics' long one as a drop-off risk. Survey research agrees the cost of each extra question is real: a shortened survey cut drop-off from 65.7% to 20.2% in one JMIR study [checked, [JMIR 2023](https://jmir.org/2023/1/e48236)], with the caveat that other studies did not find the effect; vendor data puts the steepest per-question loss in the first ~15 questions [seen, [Koji citing SurveyMonkey](https://www.koji.so/docs/ideal-survey-length-guide)].

### 1.3 Which inputs actually change the best plan

| input | what it changes | evidence | mark · two sources where found |
|:-|:-|:-|:-|
| **Training status, by type** | starting intensity, frequency and progression model. Untrained people progressed best near 60% 1RM and 3 days a week per muscle, trained people near 80% and 2 days. Later models found training status adds little prediction once volume and intensity are known, so it matters most at the start and for the progression model, not as a fixed label. | Rhea 2003 MA (140 studies) · 2024 Sports Med MA | [checked] [Rhea 2003 PDF](https://paulogentil.com/pdf/A%20meta-analysis%20to%20determine%20the%20dose%20response%20for%20strength%20development.pdf) · [Sports Med 2024](https://link.springer.com/article/10.1007/s40279-024-02006-3) |
| **Training status is domain specific** | NSCA defines training status as the type of prior program, its length, its intensity and the technique learned. A runner with five years of running and no lifting is a lifting novice. Runna sizes the start from **what kind** of exercise you do. | NSCA needs analysis · Runna support | [seen] / [checked], sources in 1.1 and 1.2 |
| **Previous injury** | the single strongest predictor of the next one. In runners, injury in the last 12 months was the main risk factor in 5 of 8 studies; a later review rated a previous running injury the strongest risk factor for long-distance runners (moderate quality). | Saragiotto 2014 SR · van Poppel 2021 SR | [checked] [PubMed 24809248](https://pubmed.ncbi.nlm.nih.gov/24809248/) · [van Poppel, J Sport Health Sci](https://pure.eur.nl/en/publications/risk-factors-for-overuse-injuries-in-short-and-long-distance-runn/) |
| **Chronic stress** | slower recovery of muscle function, energy and soreness over 96 h after a hard session, after adjusting for fitness, workload and training experience. One observational study of 31 lifters. | Stults-Kolehmainen 2014 | [checked] [PSU record](https://pure.psu.edu/en/publications/chronic-psychological-stress-impairs-recovery-of-muscular-functio/) · single study, so dosing changes from it stay modest |
| **Sleep** | repeated nights of short sleep cut force in multi-joint lifts, not single-joint ones; one night of no sleep had little effect on strength. Acute sleep loss lowers performance across outcomes, with a small effect on strength. | Knowles 2018 SR · Craven 2022 MA | [checked] [PubMed 29422383](https://pubmed.ncbi.nlm.nih.gov/29422383/) · Craven via [Stronger by Science summary](https://www.strongerbyscience.com/research-spotlight-sleep-loss/) [seen] |
| **Enjoyment and affect** | the feeling during moderate exercise predicts later activity; post-exercise feeling does not. Affective judgments correlate with physical activity at a medium size. HIIT gives more enjoyment but less pleasant affect than moderate continuous work, so "likes HIIT" and "hates hard breathing" are both real inputs. | Rhodes & Kates 2015 SR · Rhodes, Fiala & Conner 2009 MA · Oliveira/Tavares 2021 MA | [checked] [Rhodes & Kates, Ann Behav Med](https://link.springer.com/10.1007/s12160-015-9704-5) · [Tavares 2021, Northumbria](https://nrl.northumbria.ac.uk/id/eprint/46483) · Rhodes 2009 via [PMC editorial](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5504143/) |
| **Choice and autonomy** | self-selected intensity added about 26 min a week of walking in one trial; for resistance training the adherence trials (APART, open-rep RPE) are registered but their adherence results were not found. One yoked study found autonomy did not change affect after lifting. **Choice helps aerobic adherence; for lifting it is plausible, not proven.** | Williams 2015 RCT (secondhand) · yoked RT study | [seen] [sportrxiv preprint citing Williams](https://sportrxiv.org/index.php/server/preprint/download/319/version/414/643/586) · [ClinicalTrials APART](https://clinicaltrials.gov/study/NCT05371587) |
| **Frequency for habit** | new gym members needed at least four sessions a week for about six weeks to form a habit (observational, 111 people). The authors' advice: keep it fun and simple and focus on consistency. This is the evidence under a "consistency with challenges" outcome. | Kaushal & Rhodes 2015 · Kaushal 2017 RCT | [checked] [PubMed 25851609](https://pubmed.ncbi.nlm.nih.gov/25851609/) · [Ann Behav Med 2017](https://link.springer.com/10.1007/s12160-017-9881-5) |
| **Second goal that is endurance** | running added to lifting cut strength and size more than cycling in a 2012 MA, with a dose effect; a 2021 MA (43 studies) found no interference on strength or size, a small one on explosive strength when done in the same session. **The mode and the dose of endurance work matter more than the fact of it.** | Wilson 2012 MA · Schumann 2022 MA | [checked] [Wilson 2012, BVS](https://pesquisa.bvsalud.org/sms/resource/pt/mdl-22002517) · [Sports Med 2021](https://link.springer.com/article/10.1007/s40279-021-01587-7) |
| **Weight loss without a gym** | step counts: mortality fell up to 6 000 to 8 000 steps a day from 60, 8 000 to 10 000 under 60 (observational). The fat-loss scope in `01_SAFETY.md` already says exercise alone moves about 2 kg; walking is the honest lever for someone who hates gyms. | Paluch 2022 MA · Swift 2014 (file 04) | [checked] [Lancet Public Health record](https://doaj.org/article/c3639c468b4348958202e52793ab979d) · file 04 §2 |
| **Postpartum return to impact** | about 3 months postnatal and passing a set of load and impact tests before running; pelvic health physio assessment advised before high impact for all, whatever the delivery. A reasoning aid, not a protocol. | Goom, Donnelly & Brockwell 2019 · BJSM blog 2021 | [checked] [Moving Medicine record](https://movingmedicine.ac.uk/evidence/goom-t-donnelly-g-brockwell-e-returning-to-running-postnatal-guidelines-for-medical-health-and-fitness-professionals-managing-this-population-march-2019/) · [BJSM blog](https://blogs.bmj.com/bjsm/2021/08/22/return-to-running-following-childbirth-when-the-principles-of-sports-medicine-and-pelvic-health-collide/) |
| **Seated or wheelchair** | SCI guidelines: at least 20 min moderate to vigorous aerobic work twice a week plus 3 sets per major muscle group twice a week for fitness; 30 min three times a week for cardiometabolic health; start smaller if inactive; cervical and high thoracic injuries need to know autonomic dysreflexia signs. | Martin Ginis 2018 · 2011 precursor | [checked] [Spinal Cord 2018, VU record](https://research.vu.nl/en/publications/evidence-based-scientific-exercise-guidelines-for-adults-with-spi-2/) · [SCIRE community](https://community.scireproject.com/topic/exercise-guidelines/) |
| **Schedule variability** | no trial found. Coaches and apps (Runna's free-days screen, our session rotation that is never tied to a weekday) handle it by design. | none | [inferred] |
| **Sport demands** | the whole NSCA needs analysis exists because the sport decides the movement, the energy system and the injury sites. An in-season athlete needs a lower dose than an off-season one. | NSCA ch. 17 notes | [seen], sources in 1.1; in-season dosing [believe] |

* * *

## Part 2 · The audit of every current question

Fourteen personas, numbered for the tables below.

| # | persona |
|:-|:-|
| P1 | 18, team-sport player (football), in season, gym at school |
| P2 | 25, aesthetics lifter, 4 years in, full gym |
| P3 | 30, runs 3 times a week, first marathon in 20 weeks, never lifted |
| P4 | 33, HYROX competitor, CrossFit box, 5 days |
| P5 | 38, busy parent, 20 minutes, home, unpredictable week |
| P6 | 45, back after 8 years off, recurring low-back pain, gym |
| P7 | 55, total beginner, home, a pair of dumbbells |
| P8 | 70, wants to stay independent, fears falling, can't get off the floor easily |
| P9 | 31, 6 months postpartum, cleared, bands and a kettlebell |
| P10 | 36, desk worker, shoulder pain on overhead work |
| P11 | 28, climber (or Muay Thai), wants sport-specific strength, 2 gym days next to sport |
| P12 | 29, experienced powerlifter, meet in 14 weeks, knows his numbers |
| P13 | 42, wants to lose weight, hates gyms, walks the dog |
| P14 | 40, wheelchair user, trains seated, bands and dumbbells |

### 2.1 Question by question

| current question | what it gets right | who it fails, and why |
|:-|:-|:-|
| **Round 0 · the 12-item screen and age band** | PAR-Q+ structure, pregnancy, postpartum, low bone density, eating disorder; one reply | Nobody is failed by it. Two small gaps: the age band arrives before anyone has said what they want, which is fine; and **the screen never asks about wheelchair use**, so P14 only surfaces in Round 3 as a "limit", after the equipment and place questions assumed standing training. |
| **R1 · main goal, 11 options** | every option maps to a program goal key | The list is shaped by one person's training: three of eleven are barbell sports (strength, powerlifting, Olympic lifts), one is HYROX, one is bodyweight skills. **P1 and P11 have no option** (no sport or athlete line; `SKILL.md` says sport preparation is "not served yet"). **P3 has no option**: running stops at the half marathon. **P5 and P13** want consistency or weight loss without a gym and must squeeze into "lose fat" or "feel healthier". **P2** wants a look, not a lift; "build muscle" is close but misses lean or recomposition. Eleven text options in one message breaks the "never more than four questions" law of `SKILL.md` in spirit. People choose an outcome; the list asks them to pick a method. |
| **R1 · a second goal** | the module rule (`03_MATRIX.md`, second goals) is sound | Same list, so same failures. Nobody is told what a second goal costs (concurrent interference is small for strength and size, larger for explosive strength in the same session; Part 1.3). |
| **R1 · an event and its date** | free text, optional | Asked of everyone, in the same message as the goal, so most skip it. **P3, P4, P12 and P1 (a season, not a date)** need it to drive the block; it should be a branch of the event outcome, with a date tap and a target ("finish" or a time). |
| **R1 · experience, four descriptions** | describes progress rate instead of a label, which beats self-rating | The descriptions are about **adding weight to a bar**: "adding weight most sessions", "progress month to month". **P3** (5 years of running, never lifted) cannot answer it truthfully; **P13, P8, P14** have no lift progress to describe. **P6** is "not for 2+ years" and lands in `none`, the same as someone who never trained, though he has technique and will regain fast. One number cannot hold a person who is advanced at one thing and new at another. |
| **R2 · days a week, 2 to 6** | the rotation never ties sessions to weekdays, which already suits unpredictable weeks | **P5** cannot say "it depends"; **P13** might do 1 planned session plus daily walks; **P1 and P11** have sport practice on other days that the trainer never hears about, so it can stack hard days. Nothing asks whether the week is predictable. |
| **R2 · minutes, four cards** | the engine already takes any number 15 to 120 | The owner's complaint: four cards hide that. **P5 (20)** is the fourth card only in `SKILL.md`, not on the page; **P12 (90+)** and **P4 (two-a-days)** have no card. Free input with suggestion chips is a page-only fix. |
| **R2 · where** | gym, home, outdoors, a mix | Fine. Missing "I travel a lot" (the `travel` module exists but nobody is asked). |
| **R2 · what's there** | presets plus single tags is the right model | Presets assume a gym vocabulary. **P13** (no kit, walks) and **P9** (one kettlebell, bands) work, **P4** (a CrossFit box) has a preset but no tile for it in `SKILL.md`. Fine otherwise. |
| **R3 · styles you love or hate: barbell, machines, dumbbells, kettlebells, bodyweight, circuits, running, classes** | asks about preference at all, which the adherence evidence supports | **Five of eight words are equipment, not styles** (owner's complaint 2). Real styles missing: bodybuilding, strength training, HIIT, endurance other than running (cycling, rowing, swimming), mobility, yoga or Pilates, sport, walking, dance, CrossFit-style. **P13** cannot say "I hate gyms" in this vocabulary; **P6** cannot say "I like Pilates"; **P10** cannot say "I hate overhead work" (that is a movement, so it belongs with pain). `match.py STYLE_OF` scores on these equipment words, so a dislike of "machines" is a vote against whole program families. |
| **R3 · injury, pain or limit, and where; or "I train seated"** | the region list and `exclude` true or false logic are right; pain is never diagnosed | One free-text question carries **pain now, old injuries, surgery, and seated training**. **P6** must decide whether a recurring back is "a limit"; **P10** gets a whole shoulder region excluded when only overhead pressing hurts (`exclude` is all or nothing per region); **P8** has no way to say "I can't get down to the floor"; **P14** is a footnote. Injury **history** (the strongest predictor of the next injury, Part 1.3) is not asked unless it hurts today. |
| **R3 · an area to bring up** | maps to `priority` in `build.py` | Phrased for aesthetics ("glutes, arms, back"). **P1, P11** have weak points that are qualities (speed, grip, hip mobility, aerobic base), not body parts. **P8**'s is balance. |
| **R3 · numbers you know** | known numbers become estimates, discounted once | Lift-only examples. **P3** has a 10 km time; **P4** a HYROX time; **P8** could report "I can stand up from a chair without hands". |
| **R3 · skill checks (run 30 min, Olympic coached, pull-up)** | asked only when they matter, which is the right pattern | The pattern is good; there are too few branches. Missing: chair rise without hands (P8), floor transfer (P8, P9, P13), impact tolerance for everyone, not only postpartum (P6, P13 at higher body weight), sport season and practice load (P1, P11). |
| **Inferred · units, paper, audits** | right to infer | Nothing else is inferred. Age 60+ could pre-select "stay strong and independent"; a running event could skip the lifting history; "home with bodyweight" could skip the equipment detail. |

### 2.2 The persona table · current interview

| # | can they say what they want? | where it breaks | likely result today |
|:-|:-|:-|:-|
| P1 team sport | no option; picks "all-round fitness" | sport practice days unseen; season unseen; `functional-gpp-3to5` excludes `none` experience if he has never lifted | a CrossFit-style plan stacked on top of football practice |
| P2 aesthetics | partly ("build muscle") | no lean or recomposition; liked styles are equipment words | fine (`muscle-upperlower-4`), by luck of matching the author's world |
| P3 first marathon | no; running stops at half | lifting experience question does not fit a runner; marathon not served | `run-base-3to5` with a "not served" line; the race date never drives the block |
| P4 HYROX | yes | fine | `hyrox-prep-4` |
| P5 busy parent | partly | 20 min is not a card on the page; unpredictable week unseen | `home-fullbody-2to4`, acceptable |
| P6 returner, bad back | partly ("feel healthier"? "get stronger"?) | experience lands on `none`; back is excluded entirely or not at all; history unseen | a beginner plan with no lower-back training, or one that ignores the back |
| P7 55 beginner at home | yes ("feel healthier") | fine | `home-fullbody-2to4` or `health-baseline-2to3` |
| P8 70 independent | yes | floor transfers and chair rise unseen; floor exercises can be served | `older-strong-3`, with possible floor work he cannot do |
| P9 postpartum | yes | handled by the screen; impact gate good | `home-fullbody-2to4` |
| P10 shoulder | partly | `shoulder` region excludes all shoulder work instead of overhead only | a plan with no pressing at all |
| P11 climber | no | no sport; weak points are qualities | a muscle or strength plan unaware of climbing load |
| P12 powerlifter | yes | fine | `strength-rpe-4` |
| P13 weight loss, hates gyms | partly ("lose fat") | cannot say "hates gyms"; walking not a style | `home-fullbody-2to4`, plus a fat-loss principle line; walking never planned |
| P14 seated | only as a limit in round 3 | place and kit asked as if standing | health or home program with the seated filter; works, but late and by accident |

**Verdict:** the interview serves 5 of 14 well (P2, P4, P7, P9, P12), serves 4 acceptably by fallback (P5, P8, P13, P14), and misreads 5 (P1, P3, P6, P10, P11). The five it misreads are exactly the people unlike its author: athletes outside the barbell, a runner, a returner, and people in pain.

* * *

## Part 3 · The proposed interview · a branching tree

**Shape.** The screen, then four short stages: what you want, where you are, your week, you. Every screen is one question with tap tiles (pictures on the page, numbered options in chat) unless the answer is unbounded. Every question takes "you decide" or "skip", and the engine has a default for each. In chat (`SKILL.md`) the stages compress into four turns of at most four questions; on the page they are one question a screen.

**Tap budget.** Core path, everyone: **11 screens, about 14 taps and one typed number, under 3 minutes.** Longest branch (an athlete with an event, numbers and an injury): 17 screens. Shortest (60+, "you decide" on extras): 9 screens. Ladder's quiz is about 2 minutes; Freeletics' long flow is the cautionary tale (Part 1.2).

**Learned, not asked.** The first outing (`05_LOADS.md`) finds loads; the first two weeks of logs correct the level (Caliber and Freeletics do the same). So the interview asks for the least that changes the **program choice** and the **starting dose**, and leaves the rest to the logs.

### Stage 0 · the screen (unchanged, one turn)

The twelve PAR-Q+ based items and the age band, as in `01_SAFETY.md`. **One addition:** item 13, "I use a wheelchair or train seated" (writes `position: "seated"` before place and kit are asked, so every later tile list is already filtered).

### Stage F · the fork (everyone, one tap, right after the screen)

Owner input, 13 nov (walkthrough notes, section 3 to 5): many people already train with their own split and style, and the trainer must keep it and improve it, never swap it.

> Do you want a new plan, or to get more out of what you already do?

| tile | branch | writes |
|:-|:-|:-|
| Build me a new plan | Stages 1 to 5 below | `mode: new` (NEW) |
| Improve what I already do | Stage 1 (Q1 and Q2 only, to know what "better" means), then **the improve branch** (Part 3b), then Stage 3 Q8 and Stage 4 | `mode: improve` (NEW) |
| Not sure: I train, but I'm open to change | the new-plan path, with their current routine captured (Part 3b, I1 to I3) and offered as option one in the pick | `mode: open` (NEW) |

**Inferred:** "Nothing yet" on Q4 later never shows the improve branch; someone who taps "improve" and then reports no routine is moved to `new` with one line.

**The order of the funnel follows the owner's words, "refine the interests in the beginning... and then from there we would start giving the trainings":** screen, fork, outcome, the routine or the history, the week, you, and only then a plan.

### Stage 1 · what you want

**Q1 · the outcome** (everyone, one tap)

> What do you want training to do for you?

| tile | writes `outcome` |
|:-|:-|
| Look better | `look` |
| Get strong | `strong` |
| Be more athletic, or better at my sport | `athletic` |
| Get ready for an event (a race, HYROX, a test) | `event` |
| Build a habit that sticks, with challenges to chase | `habit` |
| Feel healthier, move better, have more energy | `health` |
| Stay strong and independent as I get older | `independent` (shown first when the age band is 60+) |

If screen item 11 (eating disorder) was ticked, the lean and weight answers below are hidden, as today.

**Q2 · the follow-up** (one tap, the tiles depend on Q1)

| Q1 | question | tiles → `goal` (existing key) and new fields |
|:-|:-|:-|
| look | What change do you want most? | More muscle, more size → `muscle` · Leaner, lose fat → `fat_loss` · Both: leaner and more muscle → `muscle` + `goal2: fat_loss` · A body part I want to bring up → `muscle` + Q2b (body map tap, writes `priority`) · Stepping on a physique stage → `muscle`, flag `goal_gap: physique_show` |
| strong | Strong for what? | Stronger at everything → `strength` · A powerlifting meet → `powerlifting` (+ event branch) · The Olympic lifts → `weightlifting` · Bodyweight strength: pull-ups, handstands, muscle-ups → `skills` · Strong for daily life or work (carrying, lifting, a physical job) → `strength`, `strength_for: daily` (NEW) |
| athletic | What kind of athletic? | A team sport · A combat sport · Climbing · A racket sport · Another sport (type it) → `sport` (NEW) and Q2c · All-round: fast, fit, jumps, no weak spot → `functional` |
| event | Which event? | 5 or 10 km → `run` · Half marathon → `run` · Marathon or longer → `run`, flag `goal_gap: marathon` (NEW program needed) · HYROX → `hyrox` · Triathlon, cycling or swimming → flag `goal_gap: multisport` · An obstacle race → `functional` · A fitness test (army, police, firefighter, school) → `functional`, `event.test` (NEW) · Then Q2d: the date (date picker, "no date yet") and the target ("finish it", "a time": typed) → `event` `{name, date, target}` |
| habit | What keeps you coming back? | Beating my own numbers · Monthly challenges and streaks · Variety, never the same session twice · Short sessions I can't talk myself out of → `goal: consistency` (NEW key) and `motivator` (NEW) |
| health | What matters most? | More energy and fitness → `health` · Less pain or stiffness → `health`, `health_focus: mobility` (NEW) · My heart, blood pressure or blood sugar → `health`, `health_focus: cardio` · Lose weight for my health → `fat_loss` · Sleep and stress → `health`, `health_focus: stress` |
| independent | What matters most? | Balance and not falling · Getting up, stairs, carrying shopping · Keeping up with grandchildren or travel · All of it → `independent` and `health_focus` |

**Q2c · sport only** (athletic → a sport; two taps)

> Where are you in your season, and how many days a week do you already play or practise?

`sport_season`: off season · pre season · in season · no season (recreational) (NEW) · `sport_days`: 0 to 6 (NEW). This is the NSCA "evaluation of the sport" in two taps; the trainer already knows the sport's movement and injury profile from a small table (see Part 4, new program).

**Q3 · anything else?** (skippable, one tap) The Q1 tiles again, minus the one chosen. Writes `goal2` through the same follow-up mapping, without asking the follow-up (the default for that outcome: look → `muscle`, strong → `strength`, athletic → `functional`, event → `run`, habit → `consistency`, health → `health`, independent → `independent`). One line tells them a second goal becomes an add-on, not a second program.

### Stage 2 · where you are now

**Q4 · what have you done most of?** (everyone, multi-tap, "nothing yet" is a tile)

> What kind of training have you done regularly, at any point?

Tiles: Lifting weights · Running · Cycling, rowing or swimming · A sport · Classes, HIIT or circuits · Yoga, Pilates or mobility · Bodyweight or calisthenics · CrossFit or HYROX · Martial arts or climbing · Nothing yet → `history_styles` (NEW).

**Q5 · how long, and how recently** (one tap per style picked, max two shown: the two closest to the goal; the rest default to "a while")

> Lifting weights: how long, and are you doing it now?

| tile | writes `experience_by` (NEW) for that domain |
|:-|:-|
| Never, or just tried it | `none` |
| Under 6 months, or on and off | `novice` |
| 6 months to 2 years, regularly | `intermediate` |
| 2 years or more, regularly, or I compete | `advanced` |

Then one tap: **Doing it now** · **Stopped under a year ago** · **Stopped over a year ago** → `returning` (NEW: `{domain, years_off}`).

For lifters who say intermediate or advanced, the current progress-rate description stays as a check ("do your main lifts still go up most sessions, most weeks, or most months?") because it beats self-rating. For runners, the equivalent is Q11 (a recent time). The engine derives today's single `experience` from `experience_by` for the domain of each program family (Part 4).

### Stage 3 · your week

**Q6 · days** (one tap) 1 · 2 · **3** · 4 · 5 · 6+ → `days`. For athletes the question reads "days a week for this training, on top of your sport".

**Q7 · is your week predictable?** (one tap) Same days most weeks · It changes week to week · Shifts or travel → `schedule` (NEW: `fixed` · `variable` · `shifts`).

**Q8 · minutes** (typed or slid, 10 to 120, chips 20 · 30 · 45 · 60 underneath) → `minutes`. Follow-up line, no question: "Some days shorter? Tell me on the day." (the readiness turn already asks).

**Q9 · where** (one tap) A gym · Home · Outdoors or a park · A mix · I travel a lot → `places`, and `travel: true` (NEW, switches the `travel` module on).

**Q10 · what's there** (one tap on a preset, then optional add chips) Full gym · Basic gym · CrossFit box · Dumbbells, bands or a kettlebell at home · Nothing: my body and the outdoors → `places.<name>.equipment`. Home weights: typed, as today. **Inferred:** a park skips this; "nothing" skips the add chips.

### Stage 4 · you · the strengths and weaknesses block

One question a screen, all skippable. This is the block the owner asked for: what they are good at, what holds them back, what hurts or hurt, what they hated before.

**Q11 · what do you enjoy, or think you would?** (multi-tap, up to three)

Tiles, all training styles, none equipment: Lifting heavy · Bodybuilding: pump and shape · HIIT and circuits · Running · Cycling, rowing or swimming · Walking and outdoors · Yoga, Pilates, mobility · Bodyweight and calisthenics · Kettlebells · CrossFit or HYROX style · Sport and games · Classes and training with others → `likes` (style ids, Part 4).

**Q12 · anything you've hated or won't do?** (multi-tap)

The same style tiles, plus four that are not styles but kill adherence: The gym itself · Jumping · Getting down on the floor · Long sessions → `dislikes`, and `floor_ok: false` (NEW) if the floor tile is picked, and a `dislikes: ["gym"]` that steers to home and outdoor programs.

**Q13 · what are you already good at?** (multi-tap, "not sure yet" is fine)

Strong for my size · Good engine, I don't get out of breath · Flexible · Good balance and coordination · I know the lifts, good technique · I show up, I'm consistent → `strengths` (NEW).

**Q14 · what holds you back most?** (one or two taps)

Time · Staying motivated · Energy or sleep · Stress · Pain or stiffness · Not knowing what to do · Getting bored · Feeling awkward in a gym · Money or kit → `barriers` (NEW).

**Q15 · a weak spot you want to fix?** (one or two taps, or the body map)

Upper body strength · Legs and glutes · Core · Cardio, breathing · Mobility, stiffness · Balance · Grip · Posture, back · A body part (map) → `weak_points` (NEW) and `priority` (existing, for body parts).

**Q16 · your body: pain and history** (body map, tap a region or "nothing")

For each tapped region, one tap: **Hurts now** · **Old injury, a professional cleared it** · **Old injury, never checked** · **Surgery or a replaced joint** → `limits[]` with `status` (NEW: `now` · `cleared` · `unchecked` · `surgery`), mapping to today's `exclude` (now and unchecked → `true`; cleared and surgery → `false`).
Then one multi-tap: **What sets it off?** Bending forward · Reaching overhead · Impact, jumping, running · Kneeling or deep squats · Gripping · Twisting · Long sitting · Not sure → `limits[].aggravators` (NEW, maps to bank `pattern` and `impact` columns).
Two toggles at the foot of the screen, for everyone: **I can get down to the floor and back up easily** (`floor_ok`, default yes; default no from 75+) and **Jumping and running feel fine** (`impact_ok`, default yes; already used after a birth).

**Q17 · recovery** (one screen, three rows of taps)

Sleep most nights: under 6 h · 6 to 7 h · 7 h or more → `sleep` (NEW)
Stress lately: low · medium · high → `stress` (NEW)
Your day: mostly sitting · on my feet · heavy physical work → `job` (NEW)

### Stage 5 · only when it matters (each a branch, all skippable)

| who sees it | question | writes |
|:-|:-|:-|
| lifting history intermediate+ | Numbers you know, recent: a weight and the reps | `numbers` (existing) |
| goal run, hyrox, or running history | A recent time (5 km, 10 km, half, HYROX), or how long your usual easy run is | `numbers.easy_run_minutes`, `numbers.run_time` (NEW key) and `skills: run_30min` inferred if the easy run is 30+ min |
| goal weightlifting | Have you been coached on the snatch and the clean? | `skills: olympic_coached` |
| goal skills, or bodyweight history | Can you do one strict pull-up? | `skills: pullup` |
| outcome independent, or age 60+ | Can you stand up from a chair without using your hands? | `skills: chair_rise` (NEW) |
| postpartum (screen item 9) | Any leaking, heaviness or pelvic pain? (yes adds the pelvic-health line, as today) | `screen.flags` |
| sport | Your position or role, if it changes the demand (goalkeeper, prop, sprinter...) | `sport_role` (NEW, optional) |

### Inferred, never asked

Units and paper (as today) · `experience` per program family from `experience_by` · `skills.run_30min` from a usual easy run of 30+ minutes · equipment from a park or "nothing" · `floor_ok: false` default from 75+ · `outcome: independent` preselected from 60+ · `travel` module from "I travel a lot" · the second goal's follow-up from its default · the readiness of the day from the daily turn, never from the interview.

### The persona walk · proposed interview

| # | path (screens) | taps | what changes for them |
|:-|:-|:-|:-|
| P1 team sport | Q1 athletic · Q2 team sport · Q2c in season, 3 practice days · Q4 sport, some lifting · Q5 novice lifting · Q6 2 days · Q7 fixed · Q8 45 · Q9 gym · Q10 basic · Q11 lifting heavy, sport · Q14 time · Q16 old ankle, cleared · Q17 7h, low, sitting | 17 | a 2-day in-season strength and power plan that counts practice as load (needs the new sport program) |
| P2 aesthetics | look · both · lifting, advanced, now · numbers · 4 · fixed · 75 · gym · full · bodybuilding · weak: arms | 13 | `muscle` + `fat_loss` second, priority arms; same programs, better reasons |
| P3 marathon | event · marathon, date, target · running advanced, lifting none · run time · 4 · fixed · 60 · outdoors · nothing · running · weak: legs · old knee (impact) | 14 | running experience drives the plan; lifting starts at `none`; marathon flagged until a program exists |
| P4 HYROX | event · HYROX, date · CrossFit advanced · HYROX time · 5 · fixed · 75 · CrossFit box · CrossFit style | 12 | as today, with the event date driving the block |
| P5 busy parent | habit · short sessions · on and off · 3 · variable · 20 · home · dumbbells · HIIT · time | 11 | `consistency`, variable week favours full-body rotations, short-session programs |
| P6 returner | strong · daily life · lifting intermediate, stopped 8 years · 3 · fixed · 45 · gym · full · lifting heavy, Pilates · back: old, unchecked, bending forward · sleep 6 to 7, stress high, sitting | 14 | `returning` lets him start as `novice` with a faster ramp; only forward-bending under load is held back, not the whole back; high stress starts volume low |
| P7 55 beginner | health · energy · nothing yet · 3 · fixed · 30 · home · dumbbells · walking | 10 | as today |
| P8 70 | independent · balance · nothing · chair rise: no · 3 · fixed · 30 · home · nothing · floor: no | 10 | no floor exercises, chair-rise ladder, balance mandatory (already) |
| P9 postpartum | health · energy · lifting novice, stopped under a year · 3 · variable · 20 · home · kettlebell · impact off | 11 | as today plus the variable week |
| P10 shoulder | look · more muscle · lifting intermediate · 4 · fixed · 60 · gym · full · shoulder: hurts now, overhead | 11 | overhead pressing held back, horizontal pressing and rows kept |
| P11 climber | athletic · climbing · no season, 3 days climbing · climbing advanced, lifting novice · 2 · 60 · gym · weak: grip, shoulders | 13 | sport program with antagonist and lower-body strength, grip volume counted against climbing days |
| P12 powerlifter | strong · meet, date · lifting advanced · numbers · 4 · 90 · gym · full · lifting heavy | 11 | as today, with the meet date driving the peak |
| P13 weight loss, no gym | look or health · lose weight · nothing · 3 · variable · 30 · home or outdoors · nothing · walking · hates: the gym, jumping | 12 | no gym programs offered, low impact, walking as a module with a step target |
| P14 seated | screen item 13 · health · energy · lifting novice · 3 · 30 · home · dumbbells | 9 | seated known before place and kit, every tile already filtered |

* * *

## Part 3b · The improve branch · coaching inside a routine they already run

**Why it matters [inferred from Part 1.3]:** the strongest adherence signal we have is that people keep doing what they enjoy (Rhodes & Kates 2015, Rhodes 2009), and a person who already trains three to five days a week has, by Kaushal & Rhodes 2015, already built the habit we would otherwise spend six weeks building. Replacing their routine risks the one thing that works. TrainHeroic and Future both treat the existing program as the coach's starting point, not a blank page (Part 1.2). What the trainer adds is the part self-coached lifters usually lack: a load and progression rule, volume balance, weak points and recovery.

**Tap budget:** 6 to 9 screens on top of the screen and the outcome. Exercises are tapped from a short list per day, never typed one by one unless they want to.

| # | question | answers | writes |
|:-|:-|:-|:-|
| I1 | What does your week look like? | tiles: Push, pull, legs · Upper and lower · Full body · One body part a day (bro split) · Strength days plus cardio days · A running plan · Classes (CrossFit, HYROX, HIIT, Pilates...) · A mix I made up | `routine.split` (NEW): `ppl` · `upper_lower` · `full_body` · `body_part` · `hybrid` · `run_plan` · `classes` · `custom` |
| I2 | How many days, and which days are which? | days 1 to 7, then one tap per day naming it from the split's labels (Push, Pull, Legs; Upper, Lower; A, B, C; Chest, Back...; Run easy, Long run, Intervals; Class) | `routine.days[]` `{label}` and `days` (EXISTING) |
| I3 | What are the main exercises on each day? | per day, a pre-filled list from the split (Push: bench press, overhead press, incline dumbbell press, dips, lateral raise, triceps pushdown) to tick, swap from a search of the bank, or "type it"; "the same as last time" copies a day. A typed name is matched to the bank by name and pattern; unmatched lines are kept as "your own" and shown once to confirm | `routine.days[].exercises[]` `{bank_id or own_name, sets, reps}` (sets and reps optional: "3 x 8 to 12" chips) |
| I4 | Numbers you know, recent | for the first 1 to 3 exercises of each day: a weight and the reps, or "skip"; runners: a recent time or easy pace | `numbers` (EXISTING), `numbers.run_time` (NEW) |
| I5 | How long have you run this routine? | Under a month · 1 to 3 months · 3 to 12 months · Over a year | `routine.age` (NEW); also sets `experience_by` for its domain when Q5 was skipped |
| I6 | What's stuck or not working? | multi-tap: A lift won't go up (which: tap) · Not growing · Always sore or tired · Something hurts (goes to Q16) · Bored · I skip sessions · Not sure, it's fine | `routine.stalls` (NEW) |
| I7 | What do you like about it, and what must stay? | multi-tap: The split · The exercises · The days · Training to failure · The pump · The short sessions · Everything | `routine.keep` (NEW): the trainer may not change what is ticked here without asking |
| I8 | How hard do your sets usually go? | To failure most sets · 1 or 2 reps left · 3 or more left · Not sure | `routine.effort` (NEW), sets the starting reps-in-reserve |

Then Q8 (minutes), Q14 (barriers), Q16 (body), Q17 (recovery) from Stage 4. The rest of Stage 4 is skipped: their likes are already the routine.

### What the engine needs: an `adopt` mode

**The idea [inferred from the program schema in `programs/README.md`]:** do not build a second engine. Turn their routine into a **program file of their own** in the exact json shape every program already uses, then let `build.py`, `progress.py`, `logbook.py` and `sheet.py` run unchanged.

1. **`plan.py adopt me/routine.json`** (NEW command) writes `me/programs/mine.md`: `family: "own"`, `layouts` from `routine.days` (sessions in their order, never tied to weekdays, as now), each exercise a SLOT with its bank id. Unmatched own exercises get the closest bank row by `pattern` for cues and loading, and keep their own name on the sheet.
2. **Sets and reps:** theirs where given. Where not, the default by pattern and goal from `04_INTENSITY.md` (compounds 3 x 6 to 10, isolation 2 to 3 x 10 to 15 for muscle; 3 to 5 x 3 to 6 for strength).
3. **Progression:** the existing rules, picked by experience and effort, never named to them: double progression for accessories and for `none` to `intermediate`; for advanced lifters with known numbers, the RPE rule already used by `strength-rpe-4`. A program-level `meso` and `deload` from the closest family (muscle, strength, powerbuild).
4. **The coaching layer, applied as suggestions, never as swaps:** (a) **volume balance**: count weekly hard sets per muscle with the fractional rule already in `muscle-fullbody-3` (Pelland, file 01) and flag a muscle under 10 sets or a push to pull ratio far from 1; (b) **weak points**: one accessory slot added to the day that has room, or one set moved; (c) **recovery**: the Q17 rules; (d) **stalls**: a stalled lift gets the existing stall rule (reset or rep-range change) from its closest program; (e) **pain**: the `allowed` filter swaps the offending exercise for its `easier` or same-pattern alternative, and says so.
5. **The `keep` list is a lock.** Anything ticked in I7 is never changed without a yes. Every other suggestion is offered as "one change this block", at most two, so the routine stays theirs.
6. **Running plans and classes:** a class they attend is a fixed, unscored day the trainer plans around (spacing hard days, as with `sport_days`); a running plan is adopted as `run-race` sessions with their days and long-run day. Both are smaller than the lifting case.
7. **Checks:** `checks.py` validates the adopted file like any program; `match` is skipped (no offer of three), and the sheet header says "your plan, coached".

**Cost:** engine (one new command, a matcher from names to bank ids, a volume counter), no new program. The heaviest single item on the list, and the one with the biggest reach: every person who already trains.

## Part 3c · How the plan is presented · plain words first

Owner input: program names are "the thinking of the personal trainer and not of the person doing the training".

**Rule proposed for `03_MATRIX.md` Step 4 and the page cards:** an offer is described in four plain parts, built by `match` from data it already has; the method name and the schools appear only behind a **"How it works"** tap.

| part | built from | example |
|:-|:-|:-|
| the week | `days`, `minutes` | 3 days a week, about 60 minutes |
| what comes first | `family` and the first main block | strength first, then muscle work |
| the focus | the goal fit, `priority`, `weak_points` | squat focus, arms brought up |
| what is added | modules from the second goal and `health_focus` | adds HYROX stations after two sessions a week |
| why it fits them | the existing `why` line, reworded without letters | built for getting stronger; uses the barbell you like; evidence strong |

**Card:** "3 days a week, about 60 minutes · strength first, squat focus · adds HYROX work twice a week". **How it works (tap):** "Built on 5/3/1 Boring But Big by Jim Wendler: four-week waves, a heavy top set, then five sets of ten. Evidence B. Buy the book: link." The evidence letter becomes words on the card (strong, good, coach-tested) and the letter stays in the tap. The sheet header follows the same rule: "Week 2 · Day B · heavy day" instead of "5/3/1 BBB · W2 · 5s week". `SKILL.md`'s current instruction to say "built from StrongLifts and Starting Strength" in the offer moves behind the tap.

**Cost:** page + doctrine (`03_MATRIX` Step 4, `06_BUILD` sheet header) + engine (small: `match` returns the four parts as fields; `sheet.py` header string).

## Part 3d · Units

Today: guessed from the browser or the language (US English → pounds and Letter, everyone else kg and A4; `02_INTERVIEW.md` "Inferred"). The owner saw pounds and Letter on screen when he expected kilos.

**Proposed:** keep the guess as the **preselected** answer and confirm it in one tap, placed where the first weight is asked (I4 or Stage 5 numbers, or Q10 home weights), not at the start: "Kilos or pounds?" with the guess first. Nobody who never types a weight sees it before session one; the sheet says the unit at the top with a one-tap switch. Paper follows the unit unless changed. Fitbod, Runna and Garmin ask units once in settings or setup [believe, not checked this session]; a confirm costs one tap and removes a wrong first sheet.

**Cost:** page only (the engine already stores kg and converts, `05_LOADS.md` Rounding).

* * *

## Part 4 · The mapping · each new answer to the engine

**Field status:** EXISTING (no engine change), DERIVED (the page or `plan.py profile` computes an existing field from it), NEW (the engine must learn to use it).

| answer | field | status | what the engine must do | rule it lands in |
|:-|:-|:-|:-|:-|
| Q1 outcome | `outcome` | DERIVED | store; the follow-up maps it to `goal` | `02_INTERVIEW` Round 1 |
| Q2 follow-up | `goal`, `goal2`, `priority` | EXISTING | nothing for the nine of eleven keys it reuses | `03_MATRIX` Step 2 |
| Q2 habit | `goal: consistency` | NEW key | every program declares a 0 to 3 fit for it (24 files); a `challenge` module (monthly test, streak line on the sheet) | `03_MATRIX` Step 2, `modules/`, `06_BUILD` sheet |
| Q2 athletic → sport | `sport`, `sport_season`, `sport_days`, `sport_role` | NEW | count `sport_days` as training days in the hard-day spacing; in season cap at 2 sessions and drop volume; pick a sport profile (movement, energy system, injury sites) | `03_MATRIX` Step 1 (days), `04_INTENSITY`, `07_CYCLE`, **new program** |
| Q2 event | `event` `{name, date, target}` | EXISTING plus `target` NEW | `build.py` already prints weeks to the event; it should also set the block so the peak or taper lands on the date | `07_CYCLE` |
| Q2 marathon, multisport, physique | `goal_gap` | NEW flag | `match` says plainly it is not served and offers the nearest (already the `SKILL.md` line; make it data) | `03_MATRIX` Step 5 |
| Q2 strong for daily life | `strength_for: daily` | NEW | score bonus to programs with carries and hinges (`older-strong-3`, `kettlebell-rop-3`, `functional-gpp`) | `03_MATRIX` Step 2 |
| Q2 health focus | `health_focus` | NEW | adds a module: `mobility` for mobility, `conditioning` for cardio, `mobility` plus easy cardio for stress | `03_MATRIX` second goals, `modules/` |
| Q4 history | `history_styles` | NEW | feeds `experience_by` defaults and `likes` (people tend to like what they kept doing) | `02_INTERVIEW` |
| Q5 experience by domain | `experience_by` `{lifting, running, ...}` | NEW, with `experience` DERIVED | Step 1 filter and the tie-break use the experience of the program's domain: strength, muscle, powerbuild, weightlifting, kettlebell, home, health, older → lifting; run → running; hyrox, hybrid, functional → the higher of lifting and conditioning, capped one step above the lower | `03_MATRIX` Step 1 and 3 |
| Q5 returning | `returning` `{domain, years_off}` | NEW | filter as one level below their old level (never `none` for a former intermediate); first outing as today; double the early load jumps for the first block | `03_MATRIX` Step 1, `05_LOADS`, `progress.py` |
| Q6 days | `days` | EXISTING | add 1 as a legal answer: only `health-baseline-2to3`, `home-fullbody-2to4` and walking reach it; say so | `03_MATRIX` Step 1 |
| Q7 schedule | `schedule` | NEW | score +1 full-body programs and programs whose `days` range is wide; −1 programs whose week breaks if a day is missed (PPL 6, body part 5) | `03_MATRIX` Step 2 |
| Q8 minutes | `minutes` | EXISTING | page only: a number field with chips; the engine already takes 15 to 120 (allow 10 for express-only programs) | page, `06_BUILD` |
| Q9 travel | `travel` | NEW flag | switches on the existing `travel` module | `modules/travel` |
| Q10 kit | `places` | EXISTING | add a `crossfit_box` tile (the preset exists) | page |
| Q11 likes | `likes` (style ids) | EXISTING field, NEW vocabulary | rewrite `match.py STYLE_OF` to style ids: `heavy` (strength, powerbuild, weightlifting), `bodybuilding` (muscle, powerbuild), `hiit` (functional, hyrox, kettlebell-ss), `running` (run, hyrox, hybrid), `endurance` (hybrid, run), `walking` (health, older), `mobility` (health, older, calisthenics), `bodyweight` (calisthenics, home), `kettlebells` (kettlebell), `crossfit` (functional, hyrox), `sport` (functional), `group` (functional, hyrox). Equipment words leave scoring | `03_MATRIX` Step 2 |
| Q12 dislikes | `dislikes`, `floor_ok` | EXISTING field, NEW vocabulary; `floor_ok` NEW | style dislike −3 as today; `gym` dislike: hard filter to home and outdoor places; `jumping` → `impact_ok: false`; `floor_ok: false` drops bank rows with `position: floor` (45 of 225) and swaps to their `easier` or a standing alternative | `03_MATRIX` Step 1 and 2, `build.py allowed` |
| Q13 strengths | `strengths` | NEW | tie-break toward programs that use them (good engine → hybrid, hyrox; technique → barbell programs over machines); never a filter | `03_MATRIX` Step 3 |
| Q14 barriers | `barriers` | NEW | time → prefer programs with low `express_minutes`; motivation or boredom → `challenge` module and higher-variety programs; not knowing what to do or gym awkwardness → `simplicity` 1 to 2 and home options first; energy or sleep → same as low `sleep` | `03_MATRIX` Step 2 and 3, `06_BUILD` |
| Q15 weak points | `weak_points` | NEW (body parts stay `priority`) | cardio → `conditioning` module; mobility → `mobility`; balance → `balance`; grip → carries in accessory slots; core → `core` | `modules/`, `06_BUILD` accessory slots |
| Q16 limits by status | `limits[].status` | NEW, `exclude` DERIVED | `now`, `unchecked` → `exclude: true`; `cleared`, `surgery` → `false` (today's rule, `01_SAFETY` pain table) | `01_SAFETY`, `build.py allowed` |
| Q16 aggravators | `limits[].aggravators` | NEW | exclude only bank rows whose `pattern` matches the aggravator in that region (overhead → `v_push`; bending → `hinge` and `flexion`; impact → `impact: yes`; kneeling and deep squat → `squat` and `lunge` at level 3+; gripping → `carry`, heavy `v_pull`; twisting → `anti_rot` loaded) instead of the whole region | `01_SAFETY`, `build.py allowed`, bank tags |
| Q16 impact | `impact_ok` | EXISTING (postpartum only) | ask everyone; apply the same bank filter | `build.py allowed` |
| Q17 sleep, stress, job | `sleep`, `stress`, `job` | NEW | under 6 h or high stress: start accessories at the low end of the program's sets and the meso one RIR easier; both: tie-break toward lower-volume programs and an earlier deload trigger; heavy physical work: −1 lower-body accessory set | `04_INTENSITY`, `07_CYCLE`, `03_MATRIX` Step 3 |
| Stage 5 run time | `numbers.run_time` | NEW key | seed running paces (Daniels) from a real time instead of easy-run minutes | `modules/run-race`, `run-base` |
| Stage 5 chair rise | `skills.chair_rise` | NEW | `older-strong-3` starts its squat ladder at the supported sit-to-stand if no | `older-strong-3`, bank ladders |
| Screen item 13 | `position: seated` | EXISTING, asked earlier | page and screen only | `01_SAFETY` |
| Fork | `mode` (`new` · `improve` · `open`) | NEW | `improve`: skip `match`, run `adopt`; `open`: run `match` and add their own routine as option one | `03_MATRIX` Step 4, `08_WORKFLOW` |
| I1 to I3 routine | `routine.split`, `routine.days[].exercises[]` | NEW | `plan.py adopt` writes `me/programs/mine.md` in the program schema; name matcher to bank ids; unmatched rows keep their name and borrow a same-pattern row | `programs/README` schema, new `adopt` |
| I5 routine age | `routine.age` | NEW | default `experience_by` for that domain | `03_MATRIX` Step 1 |
| I6 stalls | `routine.stalls` | NEW | apply the stall rule of the closest program to the named lift; tired or sore → recovery rules | `05_LOADS`, `07_CYCLE` |
| I7 keep | `routine.keep` | NEW | a lock: suggestions may not touch it without a yes | `06_BUILD`, `08_WORKFLOW` |
| I8 effort | `routine.effort` | NEW | starting RIR for the adopted program | `04_INTENSITY` |
| Offer wording | `offer.parts` | NEW output of `match` | the four plain parts; method only in "how it works" | `03_MATRIX` Step 4, `06_BUILD` sheet |
| Units confirm | `units`, `paper` | EXISTING, now confirmed | none | `02_INTERVIEW` Inferred |

### Outcomes no current program serves

| outcome | today | nearest offered | what would serve it | cost |
|:-|:-|:-|:-|:-|
| **Sport-specific** (P1, P11) | `SKILL.md`: "not served yet" | `functional-gpp-3to5` (excludes `none`) | one season-aware program, `sport-strength-2to3`: 2 days in season, 3 off season, full body strength and power with a sport profile table (team, combat, climbing, racket, field) picking the injury-prevention accessories | new program + small engine |
| **Consistency with challenges** (P5) | no goal key | `home-fullbody-2to4`, `kettlebell-ss-5` | a `consistency` goal key scored on all 24 programs, and a `challenge` module: a monthly benchmark, a streak on the sheet, a new target each block | doctrine + new module |
| **Marathon or longer** (P3) | stops at the half | `run-base-3to5` | `run-marathon-4to5` from Daniels or Pfitzinger, with the long run and taper; [believe] both are well documented | new program |
| **Triathlon, cycling, swimming** | none | `hybrid` | out of scope for v1; say so | flag only |
| **Physique competition** | not served | `muscle-*` | out of scope; say so | flag only |
| **Mobility, yoga or Pilates as the main style** (P6, P10 partly) | `mobility` module only | `health-baseline-2to3` | a `mobility-strength-2to3` program (mobility flow plus light strength), or accept the module as enough | new program, optional |
| **Weight loss without a gym** (P13) | `home-fullbody-2to4` + the fat-loss principle | same | a `walking` extra-day module with a step target (Paluch 2022) | new module |
| **Fitness test (army, police)** | none | `functional-gpp` | a test table per service, the test as the benchmark | new program, later |

* * *

## Part 5 · The ten changes ranked by effect on the best outcome

Ranked by how many personas move from a wrong or merely acceptable plan to the right one, weighted by how wrong the old plan was. Cost: **page** (the web page and `SKILL.md` wording only) · **doctrine** (a `doctrine/*.md` rule and program json edits) · **engine** (Python in `engine/`) · **new program** (a new file in `programs/` or `modules/`).

Re-ranked after the owner's second input (the fork, plain-word plans, units). Two former entries merged to make room: the event date now sits with the sport branch as "events and seasons", and free minutes sits with the plain-word page change.

| rank | change | personas it fixes | cost |
|:-|:-|:-|:-|
| 1 | **The fork and the improve mode** (Stage F, Part 3b): "new plan" or "improve what I do"; `plan.py adopt` turns their routine into their own program file, the existing loading, progression and pain rules run on it, the coach only suggests (balance, weak points, stalls, recovery) and never touches what they lock | every person who already trains: P2, P4, P10, P12 at least, and P1, P11 for their gym days | engine (new command, name matcher, volume counter); no new program |
| 2 | **Experience by domain, plus "returning"** (Q4, Q5): lifting, running and sport experience asked separately; each program filtered on its own domain | P3, P6, P1, P11, P9 | doctrine + engine |
| 3 | **Outcome first, one follow-up** (Q1, Q2): seven outcomes, then a tap onto the existing goal keys | P1, P2, P3, P5, P6, P11, P13 and everyone's first screen | page + doctrine (no engine for the 9 reused keys) |
| 4 | **Pain as status and trigger, not region** (Q16): now, cleared, unchecked, surgery; then what sets it off; filter by bank pattern, not the whole region | P6, P10, P3, P1; the strongest injury predictor finally gets asked | page + engine (bank already has `pattern` and `impact`) |
| 5 | **Styles, not equipment, in likes and dislikes** (Q11, Q12), "the gym itself" and "jumping" as dislikes; rewrite `STYLE_OF` | P13, P6, P5, P2 and every adherence case | page + engine (small) |
| 6 | **Plain-word plans, method behind a tap, free minutes, units confirmed** (Part 3c, 3d, Q8): "3 days, strength first, squat focus, adds HYROX work"; a number field for minutes; "kilos or pounds?" preselected at the first weight | everyone; the owner's walkthrough complaints 2, 4 and the units bug | page + doctrine + engine (small: `match` returns the plain parts, `sheet.py` header) |
| 7 | **Accessibility for everyone**: seated in the screen, `floor_ok`, `impact_ok` | P8, P14, P13, P9 | page + engine (bank already tags `floor` and `impact`) |
| 8 | **Recovery block** (Q17): sleep, stress, job set the starting volume and the deload trigger | P6, P5, P9, any stressed beginner, every improve user who is "always tired" | doctrine + engine |
| 9 | **Sport, events and seasons**: Q2c with `sport_days` counted as load, a season-aware sport program, the event date and target driving the block, a marathon program | P1, P11, P3, P4, P12 | new programs (sport, marathon) + engine (`07_CYCLE`) |
| 10 | **Barriers and the consistency outcome** (Q14, `goal: consistency`, `challenge` module), plus schedule variability (Q7) | P5, P13, P7, P9 | doctrine + new module + engine (small) |

**Cheapest first:** 3, the page half of 6 (minutes field, unit confirm, plain card wording) and the wording of 5 are page only and can ship before any engine change. 2, 4 and 7 are the biggest correctness gains per line of code. 1 is the largest engine job and the biggest reach. 9 and 10 need new programs or modules and a research pass of their own.

## Not verified this session

- The exact current onboarding screens of Future, Caliber, TrainHeroic, Nike Training Club and WHOOP (no official question list is published; screens drift between versions).
- Full text of Stults-Kolehmainen 2014, Knowles 2018, Rhodes & Kates 2015 and Wilson 2012; effect sizes are quoted from abstracts or summaries.
- Adherence results of the APART and open-repetition RPE trials (registered, results not found).
- The 2018 SCI guideline's strength frequency (the 2011 version says twice a week).
- In-season dosing for team sports and climbing-specific strength rules: [believe], need their own research pass before the sport program is written.
- The Goom 2019 test battery (not opened).
