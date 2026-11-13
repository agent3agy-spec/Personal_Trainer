# programs · one file per runnable program

_This folder owns: every program the trainer can run. **A program with no file here cannot be served.** The schools behind them, and the ones studied but not runnable, are in `../schools/INDEX.md`._

Each file has two parts:

1. **For people (prose):** what it is, who it is for, the week, how it progresses, when it deloads, what it graduates to, the evidence and its marks ([checked] / [believe]), and the credit: the book or site of the school, with a link to buy the real thing.
2. **For the engine (the first ```json block):** the exact data below. The engine (`engine/build.py`, `engine/progress.py`) reads only this block. If the prose and the block disagree, the block is what runs and the prose is the bug.

## The json block

```
{
  "id": "strength-lp-3",                 same as the file name
  "name": "Novice linear progression",
  "family": "strength",                  strength · muscle · powerbuild · weightlifting · functional ·
                                         hyrox · hybrid · run · calisthenics · kettlebell · home · health · older
  "draws_from": ["StrongLifts 5x5", "Starting Strength", "ACSM 2009"],
  "goals": {"muscle": 2, "strength": 3, "powerlifting": 2, "weightlifting": 0, "functional": 1,
            "hyrox": 0, "run": 0, "skills": 0, "fat_loss": 1, "health": 2, "independent": 1},
                                         ALL 11 keys, 0 to 3: how well it serves that goal
  "experience": ["none", "novice"],      any of none · novice · intermediate · advanced
  "days": [2, 3],                        min and max sessions a week
  "sweet_days": [3],
  "minutes": [45, 75],                   the normal session length range
  "express_minutes": 30,                 the shortest legal version (the "express" session below)
  "equipment_all": ["barbell", "rack", "bench", "plates"],     every tag needed (see engine/core.py PRESETS)
  "equipment_any": [],                   list of lists: at least one tag of each inner list
  "skills_required": [],                 e.g. ["olympic_coached"], ["run_30min"], ["pullup"]
  "excluded_for": [],                    pregnancy · low_bone_density · seated · under_60 · over_60
  "evidence": "B",                       A · B · C · G
  "simplicity": 1,                       1 linear · 2 double progression · 3 waves · 4 RPE
  "graduates_to": ["strength-531-beginners-3"],
  "block_weeks": 6,                      weeks in a block before the deload (or the block review)
  "deload": {"sets_factor": 0.5, "load_factor": 0.9, "rir": "4"},   or null when the rule resets itself
  "meso": null,                          or {"rir_by_week": ["3","2","1 to 2","0 to 1"],
                                             "extra_sets_by_week": [0,1,1,2], "applies_to": ["accessory"]}
  "layouts": {"2": ["A","B"], "3": ["A","B"]},   the rotation of sessions for a given days a week;
                                         sessions are done IN ORDER, never tied to a weekday
  "modules": ["core"],                   default finisher modules (see ../modules/)
  "sessions": {"A": SESSION, "B": SESSION},
  "express": SESSION                     the short version, used when the minutes are under "minutes"[0]
}
```

**SESSION:**

```
{"title": "Squat · Bench · Row",
 "tags": ["heavy_legs"],                 heavy_legs · power · hard_cardio · hinge_heavy (used by spacing rules)
 "blocks": [BLOCK, ...]}                 no warm-up: the engine writes it from the main patterns
```

**BLOCK:** `{"name": "Main block", "kind": "main", "format": "straight", "slots": [SLOT, ...]}`

- `kind`: `main` (never cut, carries the score) · `secondary` · `accessory` · `finisher`
- `format`: `straight` · `superset` (add `"rest_after_round": 90`) · `circuit` · `emom` · `amrap` · `fortime` · `intervals` · `run`. The timed formats also take `"minutes": 12`.

**SLOT, a lift:**

```
{"key": "squat",                         unique in the program: loads and the chosen exercise are stored under it
 "pattern": "squat",                     the bank pattern (see ../exercises/README.md)
 "prefer": ["back_squat", "goblet_squat"],   bank ids tried first, in order
 "muscles": [],                          optional filter on muscles_primary
 "sets": 5, "reps": "5", "rest": 180,    reps as "5", "8-12", "5+", "30 s", "400 m", "12 cal"
 "effort": "1 or 2 left in the tank",                 what the sheet prints
 "rule": "linear_session",               a rule kind from engine/progress.py RULES
 "inc": 5,                               optional, kg per success (default 5 lower body, 2.5 upper)
 "score": true}                          this slot's result is the score to beat
```

Rule parameters: `tm_wave` takes `"tm_pct": 0.9`, `"deload_wave": true`. `tier_stages` takes `"tier": "T1"`. `rpe_top_set` takes `"top_reps": 3, "rpe": 8, "backoff_sets": 3, "fatigue_drop": 0.1`. `timed_standard` takes `"standard": "100 swings in 5 min"`, `"sessions_to_move": 3`. `run_volume` takes `"start_minutes": 20, "per_week": 2, "max_minutes": 90`. `c25k_week` takes `"table": [[run 1, run 2, run 3] per week]`.

**SLOT, a timed piece** (metcons, HYROX work): `{"key": "metcon", "kind": "piece", "format": "amrap", "minutes": 12, "rule": "benchmark", "score": true, "pieces": [[MOVE, MOVE, MOVE], [MOVE, MOVE]]}` where MOVE is `{"pattern": "cyclic", "prefer": ["row_erg", "bike_erg", "run"], "reps": "12 cal"}`. The engine rotates through `pieces` one per outing and fills each move from the bank for today's equipment.

## The rules of this folder

- Only bank ids from `../exercises/bank.csv` in `prefer`. A slot whose pattern has no exercise for the person's equipment is dropped (accessory) or turns the day into the travel module (main).
- Every number in a block has its source in the prose with a mark. A [believe] number is allowed, and listed in `../schools/INDEX.md` under "to verify".
- Paid programs are credited and linked, never copied.
- English, no em dash, no double dash.
