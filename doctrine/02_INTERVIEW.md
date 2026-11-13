# 02 · The interview

_This file owns: the questions asked at onboarding and on `/train goals`, and the field each answer writes in `me/PROFILE.md`. The exact wording the coach uses is in `.claude/skills/train/SKILL.md`; this file is the contract behind it. Code: `engine/plan.py profile`, validated by `engine/checks.py`._

**The shape:** the screen, then three rounds, each one turn. Units and paper are inferred, not asked. Every question accepts "you decide": the coach picks the default in bold and says which.

## Round 0 · the screen

See `01_SAFETY.md`. Writes `screen` (`result`, `reasons`, `flags`, `date`, `items`), `age_band` (`under_18` · `18_39` · `40_59` · `60_74` · `75_plus`) and `language` (a two-letter code).

## Round 1 · the goal

| question | answers | field |
|:-|:-|:-|
| main goal | build muscle · get stronger · compete in powerlifting · learn the Olympic lifts · all-round fitness · a HYROX race · running (5 km to half marathon) · bodyweight skills · lose fat · feel healthier · **stay strong and independent** | `goal`: `muscle` · `strength` · `powerlifting` · `weightlifting` · `functional` · `hyrox` · `run` · `skills` · `fat_loss` · `health` · `independent` (default **health**) |
| a second goal | the same list, optional | `goal2` |
| an event and its date | free text, optional | `event`: `{"name", "date"}` |
| experience | never, or not for 2+ years · under 6 months, adding weight most sessions · 6 months to 2 years, progress week to week · 2+ years, progress month to month, or competing | `experience`: `none` · `novice` · `intermediate` · `advanced` (default **none**) |

**Experience is asked as a description, never as a label,** because people over-rate themselves.

## Round 2 · the week

| question | answers | field |
|:-|:-|:-|
| days a week | 2 · **3** · 4 · 5 · 6 | `days` |
| minutes a session | 30 · **45** · 60 · 75+ (any number 15 to 120) | `minutes` |
| where | gym · home · outdoors or a park · a mix | `places` (`main`, and `home` for a mix) and `default_place` |
| what's there | full gym · basic gym · dumbbells or bands at home · just my bodyweight · plus any of: kettlebell, pull-up bar, rings, rower, bike, ski erg, treadmill, sled, a running route | `places.<name>.equipment`: presets `full_gym` · `basic_gym` · `home_dumbbells` · `home_bodyweight` · `park` · `crossfit_box`, plus single tags (list in `exercises/README.md`) |
| at home: which weights | e.g. "a pair of 8 kg", "adjustable up to 24", "one 16 kg kettlebell" | `dumbbells`: `[8]` or a list of steps · `kettlebells`: `[16]` |

## Round 3 · you (all optional)

| question | field |
|:-|:-|
| styles you love or hate (barbell, machines, dumbbells, kettlebells, bodyweight, circuits, running, classes) | `likes`, `dislikes` |
| any injury, pain or limit, and where; or "I train seated" | `limits`: `[{"region", "note", "exclude": true}]` (regions: knee, hip, low_back, shoulder, elbow, wrist, ankle, neck) · `position: "seated"` |
| an area to bring up (glutes, arms, back...) | `priority` |
| numbers you know (a weight and the reps, recent) | `numbers`: `{"<bank id>": {"kg", "reps"}}` |
| only when it matters: can you run 30 minutes non-stop · coached on the snatch and clean · one strict pull-up | `skills`: `run_30min` · `olympic_coached` · `pullup` |

## Inferred, never asked

- **Units and paper:** English from the United States: pounds and Letter. Everyone else: kilograms and A4. Said once, changeable.
- **Audits:** `full` for the first three sessions (see `08_WORKFLOW.md`).
- **Push to GitHub:** yes, said once ("your sheets will also be on GitHub so you can open them on your phone").

## On `/train goals`

Small changes update one field. A new goal, new days, or a new place re-run rounds 1 to 3 with the current answers as defaults, then the match. Loads that carry over (the same exercise) are kept.
