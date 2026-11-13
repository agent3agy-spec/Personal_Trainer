# 10 · Plain words: what the person sees vs what the trainer thinks

Research note, 13 nov 2026. Read only audit, nothing edited. Owner's rule (walkthrough notes, section "3 to 5"): method names (5/3/1, Boring But Big, PHUL, PHAT, GZCL, RPE, RIR, AMRAP, training max, block, deload) are the trainer's thinking. The person sees a plain plan ("3 days a week, strength first, squat focus") and the method only behind a "how it works" tap.

**Sources read:** `site/app.js` (STR en and fr, lines 16 to 488, plus the engine fields the page draws: program card 1171 to 1186, week line 1206, ready line 1217, sheet screen 1351, log screen 1520 to 1550), `engine/sheet.py` (LABELS 28 to 59, FORM_LABELS 146 to 171, header meta 248 to 250), `engine/minipdf.py` (labels 142 to 144), `engine/theme/sheet.css` (no `content:` text, nothing to change), `engine/build.py`, `engine/progress.py`, `engine/plan.py`, `engine/match.py`, `engine/logbook.py` (every string the page or sheet prints), the 24 files in `doctrine/programs/`, the 10 add-ons in `doctrine/modules/`, `doctrine/exercises/bank.csv`, and `.claude/skills/train/SKILL.md`.

**How the counts were made:** a regex pass over the client-facing fields only (program and module json `name`, `title`, `effort`, `cue`, `reps`, `rest_note`, `standard`, the "What it is" first sentence the card shows, string literals in the engine and page, bank `name` and `cue`). Code keys and doctrine prose are not counted. Line numbers are file lines; "+N" means more lines in the same file. Counts are occurrences, not lines.

## 1 · Where the jargon reaches the person

| surface | what prints | file and line |
|:-|:-|:-|
| program card (pick screen) | `p.name` as the card title, the first sentence of "What it is" (EN only), "Based on" + the first two `draws_from` credits | `site/app.js:1178`, `1175`, `1184`; `engine/match.py:113` |
| week screen after choosing | "4 sessions a week of 5/3/1 Boring But Big" | `site/app.js:146`, `380`, `1206` |
| ready screen | next session title, or the program name | `site/app.js:1217` |
| sheet header | h1 = session title; meta = program name · Block n · week n · level text | `engine/sheet.py:248` to `250`, `266` |
| sheet "Why this session" | "Session 2 of 4 this week, next in your rotation. Block 1, week 2 (deload week: easy on purpose). Main job: Back squat. Energy 7: full dose." | `engine/build.py:527` to `529` |
| sheet section headings | block names: Main block, Accessory, T1, Boring But Big, Metcon... | `engine/sheet.py:240` from program json |
| sheet rows | exercise name, cue, effort ("2 left", "0 to 2 left in the tank, last set close to failure") | `engine/build.py:390`, program json |
| logged screen | score line, then "Next time" lines: "Back squat: training max 100 kg, wave 2" | `engine/plan.py:381` to `385`, `site/app.js:1523` to `1526` |
| coach in Claude Code | the SKILL script's own examples | `.claude/skills/train/SKILL.md:70`, `106`, `180` |

**French gap, same audit:** on the web page the card description is shown in English only and hidden in French (`site/app.js:1175`), and every engine word on the sheet (title, why, effort, cue, exercise name, low energy line, log lines, score, next time) stays English for a French user. Only the sheet labels (`engine/sheet.py:34`), `nextLoad` (`site/app.js:1523`) and three `sayAlso` lines are French. The Claude Code path translates through the coach (`SKILL.md:128`), and that same line tells it to translate `program_name`, which carries the method name through.

## 2 · The jargon table

Priority: **A** prints on the card, the sheet header or the "why" line; **B** prints on the sheet body; **C** coach script or rare.

| # | term | where it appears (file:line) | count | plain EN | plain FR | pri |
|:-|:-|:-|-:|:-|:-|:-|
| 1 | 5/3/1 | programs/strength-531-bbb-4.md:3,33,35,130,132,200,202,272 +14; programs/strength-531-beginners-3.md:3,32,34,120,122,136,138,247 +10; SKILL.md:16,180 | 44 | name: "Strength plus size" / "Steady strength"; effort "the 5/3/1 waves of your training max": "3 sets, each heavier; on the last, as many clean reps as you can" | "Force et volume" / "Force régulière"; "3 séries de plus en plus lourdes ; à la dernière, autant de reps propres que possible" | A |
| 2 | Boring But Big, BBB | programs/strength-531-bbb-4.md:33,113,142,185,212,254,284,328 +5 | 13 | block: "Extra sets, lighter"; title "Squat · BBB": "Squat · extra squat sets" | "Séries en plus, plus léger"; "Squat · séries de squat en plus" | A |
| 3 | PHUL | programs/powerbuild-phul-4.md:31,33; programs/muscle-upperlower-4.md:37 | 3 | "Strength and size, 4 days" | "Force et muscle, 4 jours" | A |
| 4 | PHAT | programs/powerbuild-phat-5.md:32,34 | 2 | "Strength and size, 5 days" | "Force et muscle, 5 jours" | A |
| 5 | GZCLP, GZCL | programs/strength-gzclp-4.md:37,39 | 3 | "Heavy, then lighter" | "Lourd, puis plus léger" | A |
| 6 | T1, T2, T3 (tiers) | programs/strength-gzclp-4.md:3,110,116,129,138,151,159,175 +26 | 42 | T1 "Heavy lift", T2 "Second lift, lighter", T3 "Extra work"; title "T1 squat · T2 bench": "Heavy squat · lighter bench" | "Exercice lourd", "Deuxième exercice, plus léger", "Travail en plus"; "Squat lourd · développé couché plus léger" | A |
| 7 | RPE | programs/strength-rpe-4.md:3,31; SKILL.md:16 | 3 | name "RPE upper lower": "Strength by feel, 4 days"; "RPE 8": "2 reps left in the tank" | "Force au ressenti, 4 jours"; "encore 2 reps en réserve" | A |
| 8 | RIR | SKILL.md:9,16 (ban list only) | 2 | already banned; keep "reps left in the tank" | "reps en réserve" | C |
| 9 | AMRAP | engine/build.py:412; programs/functional-gpp-3to5.md:130,520,853 | 4 | "AMRAP 12 min": "As many rounds as you can in 12 min" | "Max de tours en 12 min" | A |
| 10 | EMOM, every minute on the minute | engine/build.py:413; programs/functional-gpp-3to5.md:412,454; modules/conditioning.md:78 | 4 | "A set at the start of every minute, 12 min" | "Une série au début de chaque minute, 12 min" | A |
| 11 | For time, cap | engine/build.py:412; programs/functional-gpp-3to5.md:253, plus "cap" in 2 efforts | 5 | "For time, cap 15 min": "As fast as you can, stop at 15 min" | "Le plus vite possible, arrêt à 15 min" | A |
| 12 | training max, TM | site/app.js:1525; engine/progress.py:144,171; engine/plan.py:383; programs/strength-531-bbb-4.md:3,132,155,202,225,274,298,345 +9; programs/strength-531-beginners-3.md:3,122,138,249,265,376,392,503 +1; SKILL.md:16,180 | 38 | "your working weight" (one number the plan works from, a bit under your best); "65, 70, 75% of the TM": "the weight of today's first set" | "ta charge de travail"; "la charge de ta première série du jour" | A |
| 13 | wave | engine/plan.py:383; site/app.js:1525 | 2 | "training max 100 kg, wave 2": "next time: week 2 of 4, top set 85 kg" | "semaine 2 sur 4" | A |
| 14 | block (a stretch of weeks) | site/app.js:211,445; engine/sheet.py:33,38,43,48,53,58,249; engine/minipdf.py:144; engine/build.py:527; modules/skill-blocks.md:10,14; SKILL.md:131,152 | 16 | "Block 1 · week 2": "week 2 of 6"; "That closes a block": "That closes these 6 weeks. The next stretch starts from your new numbers." | "semaine 2 sur 6"; "Ces 6 semaines sont bouclées. La suite part de tes nouveaux chiffres." | A |
| 15 | Main block, main job, main piece | 69 block names in programs (e.g. strength-lp-3.md:107,171,257); engine/build.py:470,527,537 | 72 | "The main lifts"; "Main job: Back squat": "Today's main lift: back squat" | "Les exercices principaux"; "L'exercice principal du jour : squat" | B |
| 16 | deload | engine/build.py:528; SKILL.md:152 | 2 | "(deload week: easy on purpose)": "Easy week: lighter on purpose so you come back stronger" | "Semaine légère : plus facile exprès, pour revenir plus fort" | A |
| 17 | top set, back off | engine/build.py:366,367,564; engine/progress.py:230,236,237; engine/logbook.py:132; programs/strength-rpe-4.md:3,109,126,194,213,280,297,364 +4 | 19 | "your heaviest set, then 3 lighter sets" | "ta série la plus lourde, puis 3 séries plus légères" | A |
| 18 | 5RM | programs/strength-texas-3.md:114,219,239,253,305,324 | 6 | "a new best for 5 reps" | "un nouveau record sur 5 reps" | A |
| 19 | metcon | programs/functional-gpp-3to5.md:3,159,282,442,549,707,882; SKILL.md:147 | 8 | "Timed workout" | "Circuit chronométré" | B |
| 20 | hypertrophy | programs/powerbuild-phat-5.md:3,315,424,533; programs/powerbuild-phul-4.md:3,330,433 | 10 | "Lower hypertrophy": "Legs, for muscle" | "Jambes, pour le muscle" | A |
| 21 | power day, speed work | programs/powerbuild-phat-5.md:3,110,219,333,443,550; programs/powerbuild-phul-4.md:3,126,233; 3 efforts "speed work: about 65 to 70% of your power day squat" | 12 | "Upper power": "Upper body, heavy"; "speed work": "light and fast, about two thirds of your heavy day weight" | "Haut du corps, lourd"; "léger et rapide, environ deux tiers de ta charge du jour lourd" | A |
| 22 | linear progression, novice | programs/strength-lp-3.md:29; programs/strength-gzclp-4.md:3; programs/strength-texas-3.md:3; programs/weightlifting-novice-3.md:33 | 4 | "Beginner strength: a little heavier every session" | "Force débutant : un peu plus lourd à chaque séance" | A |
| 23 | dose (level text) | engine/build.py:44,45 (prints in sheet meta and why); programs/health-baseline-2to3.md:3; programs/hybrid-strength-endurance-4to6.md:3 | 6 | "full dose": "normal day"; "normal dose, no max efforts": "steady day, nothing all out"; "light dose": "light day: fewer sets, a little lighter" | "journée normale"; "journée tranquille, rien à fond"; "journée légère : moins de séries, un peu plus léger" | A |
| 24 | rotation | engine/build.py:527; SKILL.md:160,177 | 3 | "next in your rotation": "next in your plan" | "la suivante de ton plan" | A |
| 25 | "2 left", "in the tank" (bare shorthand) | 293 effort lines across all 24 programs and modules core, travel (e.g. muscle-ppl-6.md:148,170,190); engine/build.py:349,353,371,379,381; engine/progress.py:50,55,57,143,230,237 | 304 | "2 left": "stop 2 reps before you'd have to stop" (first time, then "2 reps spare") | "arrête-toi 2 reps avant la limite", puis "2 reps en réserve" | B |
| 26 | failure, near failure | 81 effort lines (e.g. muscle-bodypart-5.md:149, powerbuild-phul-4.md:143) | 81 | "last set close to failure": "last set: stop when one more clean rep is all you have" | "dernière série : arrête quand il ne reste qu'une rep propre" | B |
| 27 | Accessory, Assistance | 41 + 9 block names (e.g. muscle-ppl-6.md:176, strength-531-bbb-4.md:161); engine/build.py:537 | 51 | "Extra work" | "Travail en plus" | B |
| 28 | Second lift(s) | 41 block names (e.g. muscle-upperlower-4.md:169) | 41 | "Second exercise" (mild, low priority) | "Deuxième exercice" | B |
| 29 | finisher | engine/build.py:537,648,653; modules/balance.md, conditioning.md, core.md, mobility.md:10,14; programs/run-c25k-3.md:3 | 12 | "Core finisher": "Core, to finish"; "skip the finisher": "skip the last part" | "Gainage pour finir"; "saute la dernière partie" | B |
| 30 | couplet, triplet, chipper | programs/functional-gpp-3to5.md:130,253,520,678; programs/calisthenics-rr-3.md:3,235 | 6 | "Couplet AMRAP": "2 moves, as many rounds as you can"; "Chipper": "one long list, top to bottom"; "Core triplet": "3 core moves" | "2 exercices, max de tours"; "une longue liste, de haut en bas"; "3 exercices de gainage" | A |
| 31 | single modality | programs/functional-gpp-3to5.md:412 | 1 | "one move, a set every minute" | "un seul exercice, une série par minute" | A |
| 32 | compromised running | programs/hyrox-prep-4.md:3,379,547 | 3 | "Running straight off a station" | "Course juste après un atelier" | A |
| 33 | quality run, threshold, tempo, strides | programs/run-base-3to5.md:3,157,163,184,194,204; programs/hybrid-strength-endurance-4to6.md:369,375,396,416,426; modules/run-race.md:75,81,102,112,132 | 17 | "Quality run": "Faster run"; "threshold": "a hard pace you could hold for about an hour"; "tempo": "steady and comfortably hard"; "strides": "short fast bursts" | "Sortie rapide"; "allure dure tenable environ une heure"; "allure soutenue mais contrôlée"; "accélérations courtes" | B |
| 34 | ladders, rungs | programs/kettlebell-rop-3.md:3,95,99,113,130,138,144,158 +9; programs/calisthenics-rr-3.md:3; engine/progress.py:407; 5 "rung" efforts | 29 | "climbing sets: 1 rep, rest, 2, rest, 3, then start again" | "séries en escalier : 1 rep, repos, 2, repos, 3, puis on recommence" | A |
| 35 | Volume day, Intensity day, Recovery day | programs/strength-texas-3.md:95,158,219 | 3 | "Hard day", "Easy day", "Test day: a new best for 5" | "Jour dur", "Jour facile", "Jour test : nouveau record sur 5" | A |
| 36 | Express | 24 titles, one per program (e.g. strength-gzclp-4.md:403, functional-gpp-3to5.md:853) | 24 | "Short version" | "Version courte" | A |
| 37 | Classic lift | programs/weightlifting-novice-3.md:117,189,273,360,450 | 5 | "Today's Olympic lift" | "Le mouvement olympique du jour" | B |
| 38 | First set last | programs/strength-531-beginners-3.md:147,274,401 | 3 | "5 more sets at your first set's weight" | "5 séries de plus à la charge de la première" | B |
| 39 | station piece, station practice, module, division | programs/hyrox-prep-4.md:3,134,183,383,551; modules/hyrox-stations.md:29,33,39; 3 efforts "see the hyrox-stations module for your division" | 11 | "Race stations practice"; "station weights are on your sheet (Open or Pro)" | "Entraînement aux ateliers de course"; "les charges des ateliers sont sur ta fiche" | B |
| 40 | Scale load first, then reps, then the movement; Novices | programs/functional-gpp-3to5.md (6 efforts, 3 with "Novices") | 9 | "Too hard? Go lighter first, then fewer reps, then an easier move. New to this? Skip the tricky moves once you are tired." | "Trop dur ? D'abord plus léger, puis moins de reps, puis un exercice plus simple. Débutant ? Pas d'exercice technique une fois fatigué." | B |
| 41 | hard sets | site/app.js:235,469; SKILL.md:160 | 3 | "sets that ended close to your limit" | "séries finies près de ta limite" | B |
| 42 | evidence letter | engine/match.py:172 ("evidence B"); SKILL.md:106 | 2 | "well tested" (the page already maps A, B, C, G to words at site/app.js:140) | "bien éprouvé" | A |
| 43 | school credits on the card ("Based on") | site/app.js:141,375,1184 drawing `draws_from` from all 24 programs (e.g. strength-lp-3.md:31, powerbuild-phul-4.md:33 "RP mesocycle model") | 24 | move behind "How it works" | "Comment ça marche" | A |
| 44 | reset and stage notes | engine/progress.py:93 ("reset 10 percent after 3 misses"), 171 ("training max down 10 percent after a missed minimum"), 214 ("back to the first stage at 85 percent") | 3 | "Missed 3 times: this lift drops 10% and climbs back" | "Raté 3 fois : cet exercice baisse de 10 % et remonte" | A |
| 45 | Recommended Routine | programs/calisthenics-rr-3.md:3,44,46 | 3 | "Bodyweight strength" | "Force au poids du corps" | A |
| 46 | Simple and Sinister | programs/kettlebell-ss-5.md:39,41,107 | 3 | "One kettlebell, two moves" | "Un kettlebell, deux exercices" | A |
| 47 | Rite of Passage | programs/kettlebell-rop-3.md:3,34,36 | 3 | "Kettlebell strength" | "Force au kettlebell" | A |
| 48 | Texas Method | programs/strength-texas-3.md:30,32 | 2 | "Strength, week by week" | "Force, semaine par semaine" | A |
| 49 | 80/20 | programs/run-base-3to5.md:40,42 | 2 | "Running base: mostly easy" | "Base de course : surtout facile" | A |
| 50 | Couch to 5K | programs/run-c25k-3.md:42,114,189 | 3 | "Walk to running 30 minutes" (NHS name behind the tap) | "De la marche à 30 minutes de course" | A |
| 51 | pistols | site/app.js:91,325; SKILL.md:70 | 3 | "one-leg squats" | "squats sur une jambe" | B |
| 52 | RDL | programs/powerbuild-phul-4.md:433; programs/strength-rpe-4.md:194 | 2 | "Romanian deadlift" spelled out | "soulevé de terre roumain" | B |
| 53 | CrossFit style | site/app.js:91,325; SKILL.md:70; programs/functional-gpp-3to5.md:3 | 4 | keep as a hint under the tile, not as the label: "Mixed workouts: weights, bodyweight, cardio" | "Séances mixtes : charges, poids du corps, cardio" | C |
| 54 | Program, proven program | site/app.js:26,28,260,262 | 4 | phase "Program": "Your plan"; "a proven program": "a plan that works" | "Ton plan"; "un plan qui marche" | C |
| 55 | gym and body words in cues | bank.csv: lats 9 (lines 16,25,32,76,98,99,100,109,190), glutes 5, rack 3, midfoot 2, lockout 2, brace 2, sternum 79, thoracic 222, slack 19, hike 29, cadence 189, dead stop 76, pivot 150, transition 224, pelvis 118, hamstrings 21 | 34 | "lats": "the big back muscles under your arms"; "midfoot": "the middle of your foot"; "lockout": "arms (or hips) fully straight"; "rack": "the bell resting on your forearm at your chest" | "grands dorsaux"; "milieu du pied"; "bras (ou hanches) tendus"; "kettlebell posé sur l'avant-bras contre la poitrine" | B |

**Totals:** 55 terms, 1,018 occurrences in client-facing text. The heavy ones by volume are the effort shorthand ("2 left", "failure": 385 together) and the block names (Main block, Accessory, Second lift, T1 to T3, Boring But Big: about 210). The heavy ones by harm are rows 1 to 7, 12 to 14, 16, 23 and 43: they sit on the card, the sheet header and the "why" line, the first things a person reads.

**Two lines in the coach script break the owner's rule directly:** `SKILL.md:106` gives the coach an example card line "built from StrongLifts and Starting Strength, ... evidence B" (school names and a grade up front), and `SKILL.md:128` lists `program_name` among the words to translate, so the method name survives into French. Proposed: line 106 example becomes "3 days a week, the same big lifts, a little heavier each time (how it works: StrongLifts and Starting Strength)"; line 128 swaps `program_name` for the plain name below. `SKILL.md:16` ("Your training max only for 5/3/1 programs, and explained once") can stay as the "how it works" rule.

## 3 · The 24 programs in plain words

Pattern: plain name, then one line "days · what comes first · the focus". The method and its credits move behind "How it works".

| id | today's name | plain name EN | one line EN | plain name FR | one line FR | how it works (behind the tap) |
|:-|:-|:-|:-|:-|:-|:-|
| strength-lp-3 | Novice linear progression | Beginner strength | 3 days a week, the same few big lifts, a little heavier every session. | Force débutant | 3 jours par semaine, les mêmes gros exercices, un peu plus lourd à chaque séance. | StrongLifts 5x5, Starting Strength |
| strength-531-beginners-3 | 5/3/1 for Beginners | Steady strength, full body | 3 days a week, two big lifts each time, the weights climb month by month. | Force régulière, tout le corps | 3 jours par semaine, deux gros exercices par séance, les charges montent de mois en mois. | 5/3/1 for Beginners, Jim Wendler |
| strength-531-bbb-4 | 5/3/1 Boring But Big | Strength plus size | 2 to 4 days a week, one big lift a day done heavy, then many lighter sets of it for muscle. | Force et volume | 2 à 4 jours par semaine, un gros exercice par jour en lourd, puis beaucoup de séries plus légères pour le muscle. | 5/3/1 Boring But Big, Jim Wendler |
| strength-gzclp-4 | GZCLP | Heavy, then lighter | 3 to 4 days a week, one heavy lift, one lighter lift, then extra work, heavier while it keeps moving. | Lourd, puis plus léger | 3 à 4 jours par semaine, un exercice lourd, un plus léger, puis du travail en plus, plus lourd tant que ça avance. | GZCLP, Cody Lefever |
| strength-rpe-4 | RPE upper lower | Strength by feel | 3 to 4 days a week, upper and lower body, work up to a heavy set with 2 reps spare, then lighter sets. | Force au ressenti | 3 à 4 jours par semaine, haut et bas du corps, monte jusqu'à une série lourde avec 2 reps en réserve, puis des séries plus légères. | RPE top set and back off sets, Reactive Training Systems, Stronger by Science |
| strength-texas-3 | Texas Method | Strength, week by week | 3 days a week: a hard day, an easy day, and a test day for a new best on 5 reps. For when your weights stopped rising every session. | Force, semaine par semaine | 3 jours par semaine : un jour dur, un jour facile, un jour test pour un record sur 5 reps. Pour quand tes charges ne montent plus à chaque séance. | Texas Method, Practical Programming |
| powerbuild-phul-4 | PHUL | Strength and size, 4 days | 4 days a week: two heavy days for strength, two days of more reps for muscle, upper and lower body. | Force et muscle, 4 jours | 4 jours par semaine : deux jours lourds pour la force, deux jours avec plus de reps pour le muscle, haut et bas du corps. | PHUL, Brandon Campbell |
| powerbuild-phat-5 | PHAT | Strength and size, 5 days | 4 to 5 days a week: two heavy days early in the week, three muscle days after. | Force et muscle, 5 jours | 4 à 5 jours par semaine : deux jours lourds en début de semaine, trois jours muscle ensuite. | PHAT, Layne Norton |
| muscle-fullbody-3 | Full body for muscle, three days | Full body for muscle | 2 to 3 days a week, the whole body each time, a big lift first, an easier week every 4. | Tout le corps pour le muscle | 2 à 3 jours par semaine, tout le corps à chaque fois, un gros exercice d'abord, une semaine plus légère toutes les 4. | Nippard Fundamentals, Schoenfeld |
| muscle-upperlower-4 | Upper lower for muscle, four days | Upper and lower body for muscle | 3 to 4 days a week, upper body and lower body days in turn, each muscle twice a week. | Haut et bas du corps pour le muscle | 3 à 4 jours par semaine, haut du corps et bas du corps en alternance, chaque muscle deux fois par semaine. | Nippard Fundamentals, PHUL |
| muscle-ppl-6 | Push pull legs twice, six days | Push, pull, legs | 5 to 6 days a week: a pushing day, a pulling day, a leg day, twice, each one short. | Pousser, tirer, jambes | 5 à 6 jours par semaine : un jour poussée, un jour tirage, un jour jambes, deux fois, des séances courtes. | Push Pull Legs, Nippard |
| muscle-bodypart-5 | Body part split, five days | One muscle group a day | 4 to 5 days a week: chest, back, legs, shoulders, arms, one each day. | Un groupe musculaire par jour | 4 à 5 jours par semaine : pecs, dos, jambes, épaules, bras, un par jour. | The classic bodybuilding split |
| functional-gpp-3to5 | Functional fitness, general preparedness | All-round fitness | 3 to 5 days a week: one lift or skill first, then a short timed workout mixing weights, bodyweight and cardio. | Forme complète | 3 à 5 jours par semaine : un exercice ou une technique d'abord, puis un court circuit chronométré qui mélange charges, poids du corps et cardio. | CrossFit general fitness template |
| hyrox-prep-4 | HYROX preparation, beginner week | HYROX race prep | 3 to 5 days a week: an easy run, a legs and race stations day, a fast run, and running straight off a station like on race day. | Préparation HYROX | 3 à 5 jours par semaine : une course facile, un jour jambes et ateliers, une course rapide, et de la course juste après un atelier comme le jour J. | Beginner HYROX plans, Daniels |
| hybrid-strength-endurance-4to6 | Hybrid strength and endurance | Lift and run | 4 to 6 days a week: 2 to 3 strength days and 2 to 3 runs, mostly easy, so neither spoils the other. | Muscu et course | 4 à 6 jours par semaine : 2 à 3 jours de force et 2 à 3 courses, surtout faciles, pour que l'un n'abîme pas l'autre. | Alex Viada, The Hybrid Athlete |
| run-base-3to5 | Running base, 80/20 | Running base | 3 to 5 runs a week: mostly easy, one faster run, one long run. | Base de course | 3 à 5 courses par semaine : surtout faciles, une course rapide, une sortie longue. | 80/20 Running, Fitzgerald and Seiler |
| run-c25k-3 | Couch to 5K | Walk to running 30 minutes | 2 to 3 days a week, running and walking mixed, the running grows until you run 30 minutes in 9 weeks. | De la marche à 30 minutes de course | 2 à 3 jours par semaine, course et marche mélangées, la course grandit jusqu'à 30 minutes en 9 semaines. | NHS Couch to 5K |
| calisthenics-rr-3 | Bodyweight Recommended Routine | Bodyweight strength | 2 to 3 days a week, the same bodyweight session: three pairs of moves and core, each move gets harder as you do. Needs a pull-up bar. | Force au poids du corps | 2 à 3 jours par semaine, la même séance au poids du corps : trois paires d'exercices et du gainage, chacun devient plus dur quand tu progresses. Il faut une barre de traction. | r/bodyweightfitness Recommended Routine |
| kettlebell-ss-5 | Kettlebell Simple and Sinister | One kettlebell, two moves | 3 to 6 days a week, 20 to 40 minutes: 100 swings and 10 get-ups, a heavier bell once it feels easy. | Un kettlebell, deux exercices | 3 à 6 jours par semaine, 20 à 40 minutes : 100 swings et 10 relevés turcs, un kettlebell plus lourd quand ça devient facile. | Simple and Sinister, Pavel Tsatsouline |
| kettlebell-rop-3 | Kettlebell Rite of Passage | Kettlebell strength | 3 days a week, heavy, light and medium: presses and pull-ups in climbing sets, swings on the lighter days. | Force au kettlebell | 3 jours par semaine, lourd, léger, moyen : développés et tractions en escalier, swings les jours légers. | Rite of Passage, Enter the Kettlebell |
| health-baseline-2to3 | Health baseline | Healthy basics | 2 to 3 days a week of simple full body strength, plus brisk walks building to 150 minutes a week. | Les bases santé | 2 à 3 jours par semaine de renfo simple pour tout le corps, plus de la marche rapide jusqu'à 150 minutes par semaine. | WHO 2020, ACSM guidelines |
| home-fullbody-2to4 | Home full body, any kit | Full body at home | 2 to 4 days a week at home with dumbbells, bands or just your body. Works seated too. | Tout le corps à la maison | 2 à 4 jours par semaine à la maison avec haltères, élastiques ou juste ton corps. Possible assis aussi. | Home training research, Dan John |
| older-strong-3 | Older and strong | Strong and steady after 60 | 2 to 3 days a week: balance first, then strength for getting up, carrying and catching a trip. | Fort et stable après 60 ans | 2 à 3 jours par semaine : l'équilibre d'abord, puis la force pour se relever, porter et se rattraper. | WHO 2020, Sherrington 2019 |
| weightlifting-novice-3 | Novice weightlifting | Learning the Olympic lifts | 3 to 4 days a week: snatch or clean and jerk practice first, then pulls and squats. Needs a coach to teach the lifts first. | Apprendre l'haltérophilie | 3 à 4 jours par semaine : arraché ou épaulé-jeté d'abord, puis tirages et squats. Un coach doit d'abord t'apprendre les mouvements. | Catalyst Athletics |

Note: the card today shows only the first sentence of "What it is" (`site/app.js:696`); for 5/3/1 BBB that sentence is "The best known 5/3/1 template.", for GZCLP "Cody Lefever's linear progression built on tiers.", for RPE "Strength training run by effort instead of by a fixed percentage." The plain line above replaces that sentence on the card, and needs a FR twin so French users see one at all.

## 4 · The 10 add-ons in plain words

| id | today's name | plain name EN | one line EN | plain name FR | one line FR |
|:-|:-|:-|:-|:-|:-|
| core | Core finisher | Core, to finish | 2 core moves, 2 to 3 rounds, about 6 minutes at the end. | Gainage pour finir | 2 exercices de gainage, 2 à 3 tours, environ 6 minutes à la fin. |
| conditioning | Conditioning finisher | Cardio burst, to finish | 6 to 10 minutes of hard and easy bursts on a bike, rower or bodyweight. | Cardio pour finir | 6 à 10 minutes d'efforts durs et faciles en alternance, sur vélo, rameur ou au poids du corps. |
| balance | Balance finisher | Balance, to finish | 3 balance moves next to something solid, about 6 minutes. In every session from 60. | Équilibre pour finir | 3 exercices d'équilibre près d'un appui, environ 6 minutes. À chaque séance dès 60 ans. |
| mobility | Mobility finisher | Loosen up, to finish | 5 to 8 slow minutes for the joints you just used. Never into pain. | Assouplissement pour finir | 5 à 8 minutes lentes pour les articulations travaillées. Jamais jusqu'à la douleur. |
| locomotion | Locomotion | Crawls | About 10 minutes of crawling on hands and feet, a gentle way back into training. | Déplacements au sol | Environ 10 minutes de déplacements à quatre pattes, une reprise en douceur. |
| hyrox-stations | HYROX station piece | Race stations practice | One timed round of the HYROX stations at the end of a session. | Ateliers HYROX | Un passage chronométré des ateliers HYROX en fin de séance. |
| skill-blocks | Skill blocks | Bodyweight skills | About 10 minutes of handstand, pull-up and one-leg squat practice, stopped while still clean. | Figures au poids du corps | Environ 10 minutes d'équilibre sur les mains, tractions et squat sur une jambe, arrêté tant que c'est propre. |
| easy-running | Easy running | Easy run on your extra days | A talk-pace run on the days beyond your plan, 20 minutes growing slowly. | Course facile les jours en plus | Une course où tu peux parler, les jours en plus de ton plan, 20 minutes qui grandissent doucement. |
| run-race | Run race | Running for a race, on your extra days | An easy run, a long run and one faster run, for a 5 km to a half marathon. | Course pour un objectif, les jours en plus | Une course facile, une longue et une rapide, du 5 km au semi. |
| travel | Travel day | Travel day | 30 minutes of bodyweight, anywhere, when your kit is missing. Your weights wait for you. | Jour de voyage | 30 minutes au poids du corps, n'importe où, quand ton matériel manque. Tes charges t'attendent. |

## 5 · The sheet header pattern

**Today** (`engine/sheet.py:248` to `250`, `engine/build.py:527` to `529`):

> **Squat · BBB**
> 5/3/1 Boring But Big · Block 1 · week 2 · full dose
> *Why this session:* Session 2 of 4 this week, next in your rotation. Block 1, week 2 (deload week: easy on purpose). Main job: Back squat. Energy 7: full dose.

**Proposed:**

| line | pattern EN | example EN | pattern FR | example FR |
|:-|:-|:-|:-|:-|
| h1 | `{main lift} day` or the plain session title | Squat day | `Jour {exercice principal}` | Jour squat |
| meta | `{plain plan name} · week {w} of {weeks} · {plain day}` | Strength plus size · week 2 of 6 · normal day | `{plan} · semaine {w} sur {semaines} · {journée}` | Force et volume · semaine 2 sur 6 · journée normale |
| why | `Session {n} of {d} this week. Today's main lift: {lift}. Energy {e}: {plain day}.` + easy week line when it is one | Session 2 of 4 this week. Today's main lift: back squat. Energy 7: a normal day. | `Séance {n} sur {d} cette semaine. Exercice principal : {exo}. Énergie {e} : {journée}.` | Séance 2 sur 4 cette semaine. Exercice principal : squat. Énergie 7 : journée normale. |
| easy week | `Easy week: lighter on purpose, so you come back stronger.` | | `Semaine légère : plus facile exprès, pour revenir plus fort.` | |
| footer link, the one place the method prints | `How it works: {method}, {author}` | How it works: 5/3/1 Boring But Big, Jim Wendler | `Comment ça marche : {méthode}, {auteur}` | Comment ça marche : 5/3/1 Boring But Big, Jim Wendler |

The same rule on the page: the card title is the plain name, the card line is the plain line, the facts row stays (days, fit, evidence words), and "Based on" becomes a "How it works" tap that opens the method, its credits and the 5/3/1 style explanation of the working weight. The week line (`site/app.js:146`) reads "4 sessions a week of Strength plus size". The "Next time" line reads "Back squat: next time 85 kg on the last set" instead of "training max 100 kg, wave 2".

## 6 · French translation count (the lost number)

| what | total | needs French | stays as is |
|:-|-:|-:|-:|
| exercise names, `doctrine/exercises/bank.csv` | 225 | **194** | 31 gym loanwords used unchanged in French gyms: Back squat, Front squat, Goblet squat, Box squat, Hack squat, Pistol squat, Deadlift, Hip thrust, Kettlebell swing, Good morning, Pendlay row, Face pull, Dip, Burpee, Thruster, Devil press, Wall ball, Muscle-up, SkiErg, Dead bug, Bird dog, Hollow hold, Pallof press, Push press, Push jerk, Power clean, Hang power clean, Leg extension, Turkish get up, World's greatest stretch, Sit-up (SKILL.md:128 says keep the English in brackets when gyms use it) |
| exercise cues, same file | 225 (224 unique, about 2,509 words) | **225** | 0 |
| **names and cues together** | 450 | **419** | 31 |

Beyond the bank, for the same French sheet: in programs and modules, 24 program names, 37 block names, 109 session titles, 137 effort lines, 39 `reps` strings with words, 10 add-on names and 10 add-on block names, 2 standards; plus the engine's sentence templates (why, low energy, log lines, score, next time, first outing text, level text) in `engine/build.py`, `engine/progress.py`, `engine/logbook.py`, `engine/plan.py`. If the plain names in sections 3 and 4 are adopted, translate those instead of today's names, so the work is done once.
