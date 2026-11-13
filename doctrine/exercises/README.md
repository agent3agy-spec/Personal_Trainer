# exercises · the bank

_This folder owns: every exercise the trainer can prescribe (`bank.csv`), and how it is chosen. **An exercise that is not in the bank is never prescribed.**_

## The columns of `bank.csv`

| column | what it holds | example |
|:-|:-|:-|
| `id` | lower case, underscores, unique, never renamed once shipped | `goblet_squat` |
| `name` | the common English gym name | Goblet squat |
| `pattern` | ONE pattern from the list below | squat |
| `muscles_primary` | muscles, `;` between | quads;glutes |
| `muscles_secondary` | count half a set | core;adductors |
| `equipment` | alternatives with `\|`, tags needed together with `+` | `dumbbell\|kettlebell` · `barbell+rack` |
| `load_type` | barbell · dumbbell · kettlebell · machine · cable · band · bodyweight · time · distance · calories | dumbbell |
| `level` | 1 easiest to 5 hardest | 1 |
| `needs_coaching` | yes for the classic Olympic lifts from the floor and high-skill gymnastics | no |
| `regions` | joints it loads hard, `;` between: knee · hip · low_back · shoulder · elbow · wrist · ankle · neck | knee;hip |
| `impact` | yes for jumps, running, landings | no |
| `position` | standing · seated · floor · hanging | standing |
| `easier` | the id one step easier in the same pattern, or empty | bodyweight_squat |
| `harder` | the id one step harder, or empty | front_squat |
| `tags` | any of: lengthened · unilateral · power · heavy_legs · hinge_heavy · skill · cardio · balance · metcon_ok · mobility · wheelchair_ok | lengthened |
| `cue` | one short line in English, second person, the one thing to get right | Elbows inside the knees, sit between your heels |

## Patterns

squat · hinge · lunge · h_push · v_push · h_pull · v_pull · carry · anti_ext · anti_rot · flexion · biceps · triceps · delts · rear_delts · calves · hamstrings_iso · quads_iso · glutes_iso · olympic · jump · throw · cyclic · balance · locomotion · mobility

## Muscles

quads · glutes · hamstrings · adductors · calves · chest · front_delts · side_delts · rear_delts · triceps · lats · upper_back · lower_back · biceps · forearms · core · obliques · heart (cardio work)

For counting hard sets the engine groups them: **chest** · **back** (lats, upper_back) · **shoulders** (front, side, rear delts) · **biceps** · **triceps** · **quads** · **glutes** · **hamstrings** · **calves** · **core** (core, obliques, lower_back).

## Equipment tags

bodyweight · pullup_bar · dip_bars · rings · bench · box · band · mini_band · suspension · dumbbell · kettlebell · barbell · rack · plates · ez_bar · trap_bar · med_ball · sandbag · jump_rope · cable · lat_pulldown · leg_press · leg_curl · leg_extension · chest_press_machine · row_machine · pec_deck · smith · rower · bike · skierg · treadmill · sled · outdoors

The presets a person ticks (full gym, basic gym, home with dumbbells, bodyweight only, park, CrossFit box) are expanded to these tags in `engine/core.py`.

## How an exercise is chosen for a slot (`engine/build.py`)

1. The slot's `prefer` list, in order, then every row of the slot's pattern.
2. Removed if: the equipment is not there today · `needs_coaching` and the person has not said they were coached · it loads a region that hurts or is excluded · `impact` and the person is pregnant or has low bone density · the person trains seated and `position` is not seated (or the row is not `wheelchair_ok`) · its level is above the person's cap (none 2, novice 3, intermediate 4, advanced 5; one more for a `prefer` id).
3. Of what is left: the first `prefer` id; otherwise the level closest to the person's (none 1, novice 2, intermediate 3, advanced 4), then `lengthened`, then the id in alphabetical order. The same input always gives the same exercise.
4. The choice is kept for the whole block, so loads can climb. A new block keeps the main lifts and may rotate accessories.

**Substitution:** same pattern, same or fewer regions, equipment available, level within one step. If nothing passes, an accessory slot is dropped and the sheet says why; a main slot that cannot be filled turns the day into the travel module. Never improvised.

**Demo links:** the sheet prints a search link for "<name> exercise form" so the person sees a demonstration without the bank holding links that rot.
