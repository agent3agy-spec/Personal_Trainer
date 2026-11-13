# 02 · The interview

_This file owns: the questions asked at onboarding and on `/train goals`, and the field each answer writes in `me/PROFILE.md`. The exact wording the coach uses is in `.claude/skills/train/SKILL.md`; the web screens are in `site/app.js` (`interview`). This file is the contract behind both. Code: `engine/plan.py profile` (`normalise`, `interview_fields`), validated by `engine/checks.py` (`check_interview`). Rewritten 13 nov 2026 from `research/06_interview_audit.md`, adapted to the scope in `00_MISSION.md`._

## The rule under every question

**The person says who they are; the trainer decides the training.** They say what they want, what they have done, what they enjoy, their week and their body. They never pick a method, a school or a program: those are the trainer's library (`03_MATRIX.md`, `schools/INDEX.md`). A coach does not ask "do you want to train like X"; he says "this is what you'll do", and why.

**One exception, gated by experience.** Someone experienced (any activity at 6 months to 2 years or more) may name a training style they prefer, on one optional screen whose first and default tile is "Let the trainer decide". A beginner, or someone coming back whose level steps down to beginner, never sees it: they get the frictionless path. The improve path does not ask it: they already have their style, and the trainer keeps it.

**The second exception: the improve path.** Someone who already trains keeps their own routine. They say their split, their days, their exercises and their sets and reps; the trainer runs its rules on that routine and changes nothing in it without a yes (`06_BUILD.md`, Their own routine).

**Shape.** The screen, the fork, the outcome, where you are now, your week, you. One question a screen on the page; at most four questions a turn in chat. Every question has a "you decide" default where it makes sense, and the coach says which default it took. Units and paper are guessed and confirmed at the first weight entered. Age is never asked (`00_MISSION.md`).

**Taps to the plan, measured on the page:** 14 from Start for a beginner on the new path, about 17 to their routine on the improve path with every sets and reps row left on "Not sure" (`window.__planTaps`; the sets and reps screen replaced the style screen, phase F).

## Round 0 · the screen

See `01_SAFETY.md`, unchanged. The twelve health items only. Writes `screen` and `language`; `age_band` is fixed by the engine at `18_39`.

## Round 1 · the fork

| question | answers | field |
|:-|:-|:-|
| Do you already train? | **Build me a new plan** · Improve what I already do | `mode`: `new` · `improve` |

The improve path captures the routine they run (Round 2b), then `plan.py adopt` turns it into `me/PROGRAM.md`: their split, their days in their order, their exercises, their sets and reps. There is no match and no library plan on this path. The page shows "Your routine" (their sessions in plain words, as they gave them) and the coach's proposals as cards, each with **Yes, do it** and **Keep mine** (`06_BUILD.md`, Their own routine). **One exception:** a week of classes only gives the trainer nothing it can write or score, so `adopt` answers `fallback` and the path goes on to the match, which prefers programs whose week has the same shape (`03_MATRIX.md` Step 2) and says: "Your classes stay yours as they are: the trainer cannot write a class. This is the plan closest to the rest of your week."

## Round 1 · the outcome, then one follow-up

**Up to three outcomes; the first tap is the main one.** Then one follow-up for the main outcome only (the others take their default). The follow-up maps onto the existing goal keys, so `goal` and `goal2` keep working.

| outcome (`outcome`) | follow-up (`outcome_detail`) | `goal` · `goal2` | served by |
|:-|:-|:-|:-|
| look better · `look` | **more muscle, more size** `size` | muscle | muscle and powerbuilding programs |
| | leaner and defined `lean` | fat_loss · muscle (after an eating disorder answer: muscle · health) | muscle programs, fat-loss principle line (`01_SAFETY.md`) |
| get strong · `strong` | **stronger at everything** `general` | strength | strength programs |
| | squat, bench and deadlift, a lift to compete in `powerlifting` | powerlifting | strength programs, the RPE one first for the experienced |
| | the Olympic lifts `olympic` | weightlifting | `weightlifting-novice-3` (needs coaching on the lifts) |
| be athletic · `athletic` | **fit for anything** `crossfit` | functional | `functional-gpp-3to5` |
| | strong and able to run far `hybrid` | functional · run | `hybrid-strength-endurance-4to6` (outcome bonus, `03_MATRIX.md` Step 2) |
| an event · `event` | **a 5K or 10K** `run_5k_10k` · a half marathon `run_half` | run | `run-c25k-3`, `run-base-3to5` |
| | a marathon `run_marathon` | run | `run-base-3to5` composed with a protected long run up to about 3 hours and a strength day (`06_BUILD.md`, The composer); `core.OUTCOME_PLAN` says how |
| | HYROX `hyrox` | hyrox | `hyrox-prep-4` |
| | a lifting meet `meet` | powerlifting | strength programs |
| keep it going · `keep_going` | lifting `lifting` · fitness and cardio `fitness` · **a bit of everything** `mix` | muscle · strength, functional · health, health · muscle | the steady plan for the follow-up, composed with conditioning where it asks for it, and a new challenge every block printed on every sheet (`compose.CHALLENGES`, `core.OUTCOME_PLAN`) |

**The event branch** asks one more screen: the date (a date picker, or "No date yet") → `event`: `{"name", "date"}`.

**The blend, when two or three outcomes are picked:** one screen, "How much of your week for each?", a three-step choice per outcome (a little · some · most), "you decide" giving the main one most. Stored as `outcomes`: `[{"id": "look", "detail": "size", "share": 0.6}, {"id": "event", "detail": "run_5k_10k", "share": 0.4}]`, one to three different outcomes, shares above 0 adding up to 1. The engine sorts by share (the first tap wins a tie): the largest becomes `outcome` and `goal`, the next one's goal becomes `goal2`. The composer builds the week from these shares (`06_BUILD.md`, The composer): each outcome becomes components (lifting, running, HYROX, mixed conditioning, conditioning), each gets days in proportion to its share, the lead program is matched for the days it gets, and a share too small for a whole day becomes a goal finisher the clock protects. The why line says it: "your blend: building muscle 60%, running 40%, so your week is 2 lifting days and 2 running days".

## Round 2a · where you are now (new path)

| question | answers | field |
|:-|:-|:-|
| What have you done regularly, at any point? | I lift weights · I run · I cycle, row or swim · I do classes or circuits · I do CrossFit or HYROX · **Nothing yet** | `done_before`: `lifting` · `running` · `cardio` · `classes` · `crossfit` (activities, never methods) |
| How long have you done it? (one row per activity ticked) | under 6 months · up to 2 years · 2 years or more | `experience_by`: `{"lifting": "novice"}` with `novice` · `intermediate` · `advanced`; an activity not ticked is `none` |
| I'm coming back after a break (a toggle) | | `returning: true`: every level steps down one (`advanced` to `intermediate`, `intermediate` to `novice`), the old ones kept in `experience_was`; the first sessions' logs correct it |

**Derived, never asked:** `experience` (the single field the session builder reads) is the lifting experience: `experience_by.lifting`, or CrossFit and HYROX one step lower when that is higher. `match` uses the experience of each program's own domain (`03_MATRIX.md` Step 1), so a runner of five years who never lifted runs as a runner and lifts as a beginner.

| question | answers | field |
|:-|:-|:-|
| **Experienced only:** do you have a training style you prefer? (optional) | **Let the trainer decide** · Strength · Bodybuilding · Power-building · CrossFit-style · HYROX-style · Running · Hybrid | `style_pref`: `trainer` · `strength` · `bodybuilding` · `powerbuilding` · `crossfit` · `hyrox` · `running` · `hybrid`. The engine ignores it for a beginner even if it is sent |
| What do you enjoy? (optional) | heavy lifting · muscle work and the pump · fast circuits · long cardio · running | `enjoys` (activity words, an adherence input only, `core.ENJOY`) |
| What can't you stand? (optional) | the same words | `avoids` |
| Free weights or machines? | free weights · machines · **either** | `kit_pref`; `free_weights` also writes `machines` into `dislikes`, which the session builder already reads to avoid machines when it can |

## Round 2b · your routine (improve path)

Low effort: templates and ticks, typing only if they want.

| question | answers | field |
|:-|:-|:-|
| What does your week look like? | Push, pull, legs · Upper and lower · Full body · One body part a day · Strength days plus cardio days · A running plan · Classes · A mix I made up | `current_routine.split`: `ppl` · `upper_lower` · `full_body` · `body_part` · `strength_cardio` · `run_plan` · `classes` · `custom` |
| How many days a week? | 2 to 6 | `current_routine.days` and `days`; `day_labels` follow the split (Push, Pull, Legs, Push...), in their order; `day_kinds` carries the page's key for each (`push`, `easy`, `class`...) so a run day or a class day is known in any language |
| Your main exercises, per lifting day | the usual ones for that day pre-ticked from the bank, untick or tick more, or type your own | `current_routine.exercises`: `{"Upper": [{"id": "bench_press", "sets": 4, "reps": "6-8"}, {"name": "cable thing"}]}`; a typed name is matched to the bank (`improve.match_name`: an exact id or name, gym words and a few French ones, then a close name at 0.85 or better); an unmatched one is kept by name as theirs, never dropped |
| Sets and reps, per exercise (one screen) | 3 x 5 · 4 x 6-8 · 3 x 8-12 · 3 x 12-15 · **Not sure** | `sets`, `reps` on each exercise; "Not sure" takes a usual number (compounds 3 x 6-10, other moves 3 x 10-15, the first lift of a strength goal 4 x 4-6), shown as "my guess" |
| How long have you run it? | under a month · 1 to 3 months · 3 to 12 months · over a year | `current_routine.age`; it sets `experience_by` for the routine's activity when not given (`none`, `novice`, `novice`, `intermediate`) |
| What's stuck? · Which lift won't go up? · What must stay? (optional, one screen) | a lift won't go up, not growing, always tired or sore, bored, I skip sessions, something hurts, it's fine · up to two of their exercises · the split, the exercises, the days, the pump, short sessions, everything | `current_routine.stalls`, `current_routine.stuck` (bank ids; picking one adds `lift_stuck`), `current_routine.keep` (`locks` in their routine: a proposal that touches one says so) |

Then the minutes, the place and you. No style screen and no enjoy screen on this path: their routine is their style, and what they enjoy is read from it (`enjoys` defaults from the split).

## Round 3 · the week

| question | answers | field |
|:-|:-|:-|
| days a week (new path; the improve path already has them) | 2 · **3** · 4 · 5 · 6 | `days` |
| minutes a session | a number field with + and −, typed or stepped, chips 20 · 30 · **45** · 60 · 90 underneath. **15 to 120**; anything outside is refused with a line on the page and by `checks.py` | `minutes` |
| where | **a gym** · a home gym · outdoors (shown only when running is part of the outcome: a running event, main or blended, or the hybrid outcome) | `places.main.type` and `default_place` |
| at a gym | **full gym** · basic gym · CrossFit box | `places.main.equipment` preset |
| at a home gym | a tick list: rack, barbell and plates · bench · dumbbells · kettlebells · pull-up bar · bands · rower · bike · ski erg · treadmill. At least one of a rack and barbell, dumbbells, or a cardio machine | single tags |
| at a home gym with dumbbells: which | four sets, shown in the unit confirmed on that screen | `dumbbells` |

**Never offered as a place:** a park, or home with just your bodyweight (`core.place_in_scope`).

## Round 4 · you (skippable, but asked)

One screen, every part optional, Continue always works.

| question | answers | field |
|:-|:-|:-|
| What you're good at | strong for my size · good engine · flexible · good technique · I show up | `strengths` |
| What holds you back (up to two) | time · motivation · energy or sleep · stress · pain or stiffness · not knowing what to do · getting bored | `barriers` |
| A part to bring up (up to two) | glutes · arms · back · chest · legs · shoulders · core | `priority` |
| Anything that hurts, or hurt before? | a region, then its status: **hurts now** · only on some moves · old, cleared · old, never checked; then what sets it off: bending forward · reaching overhead · jumping or running · kneeling or deep squats · gripping · twisting | `limits`: `[{"region", "status", "triggers", "note"}]`. `exclude` is derived: `now` and `unchecked` true (left out), `mild` and `cleared` false (trained with care: no impact, nothing advanced on it, `01_SAFETY.md`). A `jumping or running` trigger writes `no_impact: true`. The session builder uses the triggers: a limit swaps the moves that set it off for the nearest move that leaves it alone, and never bans the region (`01_SAFETY.md`); a status given without a trigger takes the region's usual one (`build.DEFAULT_TRIGGERS`) and the sheet asks them to say what sets theirs off |
| Sleep most nights | under 6 h · 6 to 7 h · 7 h or more | `sleep` |
| Stress lately | low · medium · high | `stress` |
| Numbers you know | squat, bench press, deadlift, overhead press: a weight and the reps | `numbers`: `{"back_squat": {"kg": 60, "reps": 5}}` |

**Sleep and stress set the starting volume** (`research/06` Part 4, Stults-Kolehmainen 2014, Knowles 2018): under 6 hours or high stress writes `start_volume: "low"`, and `match` returns a `dose_note`: the first weeks start at the low end of the program's sets and one rep further from failure. For now this is a note the coach says; it does not change the program choice.

**Units, confirmed at the first weight.** The guess (pounds and Letter for English from the United States, kilograms and A4 for everyone else) is preselected, and a "Kilos or pounds?" choice appears right where the first weight is entered: the dumbbells screen or the numbers. Using it writes `units`, `paper` and `units_confirmed: true`, and every weight given is read in that unit; the engine stores kilograms. Nobody who never types a weight is asked.

**Only when it matters:** a running goal (main or blended), HYROX, or the hybrid outcome asks "Can you run 30 minutes without stopping?" (`skills: run_30min`); the Olympic lifts ask "Has a coach taught you the snatch and the clean?" (`olympic_coached`).

## The plan, then "not for me"

The interview ends on **one plan**, never a menu (`03_MATRIX.md` Step 4): in plain words, why it fits, what a week looks like, and the method and schools only behind "How it works". Two buttons: **Start this plan** · **Not for me**. "Not for me" asks why, in one tap, and re-runs the match:

| reason | field | what the match does |
|:-|:-|:-|
| sessions are too long | `rejected`: `[{"program", "reason": "too_long"}]` | that program is out; programs whose shortest session is as long or longer lose 2 |
| too much running | `too_much_running` | that program is out; running counts as something they can't stand |
| I wouldn't enjoy it | `not_enjoy` | that program is out; its family loses 3 |
| I can't do these days | `days` | asks the days again and writes `days`; the program is not ruled out |

A fresh interview clears `rejected`. After "Start this plan" the coach sets expectations in one line (`research/07` stage 1): the first 2 to 4 weeks are for learning the moves and finding the weights, strength shows before the mirror does, a missed week is normal.

## On `/train goals`

Small changes update one field. A new outcome, new days, or a new place re-run the interview with the current answers as defaults, then the match. Loads that carry over (the same exercise) are kept.
