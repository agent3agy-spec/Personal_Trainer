# Full body for muscle, three days · muscle-fullbody-3

**What it is.** Three different full-body sessions, A, B and C, done in order. Every major muscle gets hit about twice a week, with a big lift first and the small stuff after. You add reps, then weight, and every four weeks you take a light week.

**Who it is for.** Novice to intermediate, the goal is size first and strength alongside. 2 or 3 days a week, 45 to 75 minutes. A basic gym is enough: every barbell or machine choice has a dumbbell fallback, so dumbbells and a bench are the minimum.

**The week.** A, B, C, then start again. On 2 days a week you still rotate all three, so a muscle gets about 1.5 hits a week instead of 2: fine for muscle, slower for strength.

| session | main block | second lift | accessories |
|:-|:-|:-|:-|
| A | squat 3 x 6 to 10 · bench press 3 x 6 to 10 | lat pulldown or pull-up 3 x 6 to 10 | seated leg curl 3 x 10 to 15 · lateral raise 3 x 10 to 15 · overhead triceps extension 2 x 10 to 15 |
| B | Romanian deadlift 3 x 6 to 10 · incline press 3 x 6 to 10 | chest-supported row 3 x 6 to 10 | Bulgarian split squat 2 x 10 to 15 · incline dumbbell curl 2 x 10 to 15 · calf raise 3 x 10 to 15 |
| C | leg press 3 x 6 to 10 · overhead press 3 x 6 to 10 | chin-up or pulldown 3 x 6 to 10 | seated leg curl 3 x 10 to 15 · cable fly 2 x 10 to 15 · rear delt fly 2 x 10 to 15 · hammer curl 2 x 10 to 15 |

At 3 days that is about 10 to 16 hard sets a week per major muscle once you count a compound's indirect work at half (rows count half for biceps, presses half for triceps), which is the Pelland fractional count [checked]. 10 or more weekly sets grew more than under 10 (about 9.8% against 6.6% for 5 to 9) [checked, Schoenfeld, Ogborn, Krieger 2017]. Twice a week per muscle is the Schoenfeld floor [checked 2016 data, believe the packaged rule].

Rests: big lifts 120 to 150 s, isolation 60 to 90 s.

**How it climbs.** Double progression on everything. Work inside the range: when every set hits the top (10 on compounds, 15 on accessories) at the written effort, add the smallest weight step and start again at the bottom. Compounds stay at 1 to 3 reps in reserve, isolation goes to 0 to 2 with the last set close to failure [checked: Refalo 2023, Robinson 2024, research/01 rule 4].

Inside each 4 week block the accessories get harder on a schedule: reps in reserve 3, 2, 2, 1, and one extra set on each accessory in weeks 3 and 4. The ramp from about 3 RIR to about 1 is the RP mesocycle shape [believe, coach consensus, evidence B].

**Long muscle lengths on purpose.** Romanian deadlift, incline curl, overhead triceps extension and seated leg curl are picked because the stretched position grew more: overhead extension about 20% against 14% for pushdowns [checked, Maeo 2022/23], seated over lying leg curl for the hamstrings [checked, Maeo 2021].

**Deload.** Week 5: half the sets, about 10% off the weight, 3 to 4 reps in reserve [believe, RP model, research/01 rule 7]. Take it early if your lifts drop two sessions running.

**Graduates to.** `muscle-upperlower-4` when you can give 4 days, or `muscle-ppl-6` with 5 or 6, once a session no longer leaves enough room for the sets you need.

**Evidence: B.** The principles under it are A level (volume dose, effort, twice a week, long length). The program itself, like every named program, has no trial [research/01].

**Credit.** The structure follows the public description of Jeff Nippard's Fundamentals Full Body (jeffnippard.com/products/fundamentals-hypertrophy-program), buy it for his exact sessions and coaching. The principles are Brad Schoenfeld's meta-analyses. The spirit of three full-body days on alternate days comes from Arnold's Golden Six (liftvault.com/programs/bodybuilding/arnold-schwarzenegger-workout-routine-golden-six). Nothing here copies paid programming.

## The data (the engine reads this block)

```json
{
  "id": "muscle-fullbody-3",
  "name": "Full body for muscle, three days",
  "family": "muscle",
  "draws_from": [
    "Nippard Fundamentals Full Body",
    "Schoenfeld volume and frequency",
    "Arnold Golden Six"
  ],
  "goals": {
    "muscle": 3,
    "strength": 2,
    "powerlifting": 1,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 2,
    "health": 2,
    "independent": 1
  },
  "experience": [
    "novice",
    "intermediate"
  ],
  "days": [
    2,
    3
  ],
  "sweet_days": [
    3
  ],
  "minutes": [
    45,
    75
  ],
  "express_minutes": 30,
  "equipment_all": [
    "dumbbell",
    "bench"
  ],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [
    "seated"
  ],
  "evidence": "B",
  "simplicity": 2,
  "graduates_to": [
    "muscle-upperlower-4",
    "muscle-ppl-6"
  ],
  "block_weeks": 4,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 0.9,
    "rir": "3 to 4"
  },
  "meso": {
    "rir_by_week": [
      "3",
      "2",
      "2",
      "1"
    ],
    "extra_sets_by_week": [
      0,
      0,
      1,
      1
    ],
    "applies_to": [
      "accessory"
    ]
  },
  "layouts": {
    "2": [
      "A",
      "B",
      "C"
    ],
    "3": [
      "A",
      "B",
      "C"
    ]
  },
  "modules": [
    "core"
  ],
  "sessions": {
    "A": {
      "title": "Squat · Bench · Pulldown",
      "tags": [
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat",
              "pattern": "squat",
              "prefer": [
                "back_squat",
                "hack_squat",
                "leg_press",
                "goblet_squat"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 150,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "bench",
              "pattern": "h_push",
              "prefer": [
                "bench_press",
                "chest_press_machine",
                "db_bench_press"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "vpull",
              "pattern": "v_pull",
              "prefer": [
                "lat_pulldown",
                "pull_up",
                "assisted_pull_up",
                "band_lat_pulldown"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Accessory",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "legcurl",
              "pattern": "hamstrings_iso",
              "prefer": [
                "seated_leg_curl",
                "lying_leg_curl",
                "slider_leg_curl"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            },
            {
              "key": "lateral",
              "pattern": "delts",
              "prefer": [
                "cable_lateral_raise",
                "lateral_raise",
                "band_lateral_raise"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            },
            {
              "key": "tri",
              "pattern": "triceps",
              "prefer": [
                "cable_overhead_extension",
                "overhead_db_triceps_extension",
                "seated_overhead_triceps_extension"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "B": {
      "title": "Romanian deadlift · Incline · Row",
      "tags": [
        "hinge_heavy"
      ],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "rdl",
              "pattern": "hinge",
              "prefer": [
                "romanian_deadlift",
                "db_romanian_deadlift"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 150,
              "effort": "1 to 3 left in the tank, every rep clean, flat back, deep stretch",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "incline",
              "pattern": "h_push",
              "prefer": [
                "incline_bench_press",
                "incline_db_press"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "chest_supported_row",
                "barbell_row",
                "machine_row",
                "db_row"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Accessory",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "lunge",
              "pattern": "lunge",
              "prefer": [
                "bulgarian_split_squat",
                "db_reverse_lunge",
                "reverse_lunge"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 90,
              "effort": "0 to 2 left in the tank, last set close to failure, each leg",
              "rule": "double_progression"
            },
            {
              "key": "curl",
              "pattern": "biceps",
              "prefer": [
                "incline_db_curl",
                "cable_curl",
                "db_curl"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            },
            {
              "key": "calves",
              "pattern": "calves",
              "prefer": [
                "calf_raise",
                "single_leg_calf_raise",
                "seated_calf_raise"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure, pause in the stretch",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "C": {
      "title": "Leg press · Press · Chin-up",
      "tags": [
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "legpress",
              "pattern": "squat",
              "prefer": [
                "leg_press",
                "hack_squat",
                "heel_elevated_goblet_squat",
                "goblet_squat"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "ohp",
              "pattern": "v_push",
              "prefer": [
                "overhead_press",
                "db_shoulder_press",
                "seated_db_press"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "chin",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "single_arm_cable_pulldown",
                "lat_pulldown",
                "band_lat_pulldown"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Accessory",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "legcurl",
              "pattern": "hamstrings_iso",
              "prefer": [
                "seated_leg_curl",
                "lying_leg_curl",
                "slider_leg_curl"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            },
            {
              "key": "fly",
              "pattern": "h_push",
              "prefer": [
                "cable_fly",
                "db_bench_press"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure, deep stretch at the bottom",
              "rule": "double_progression"
            },
            {
              "key": "rear",
              "pattern": "rear_delts",
              "prefer": [
                "reverse_pec_deck",
                "rear_delt_fly",
                "band_pull_apart"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            },
            {
              "key": "hammer",
              "pattern": "biceps",
              "prefer": [
                "hammer_curl",
                "db_curl"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · Squat · Bench · Row",
    "tags": [
      "heavy_legs"
    ],
    "blocks": [
      {
        "name": "Main block",
        "kind": "main",
        "format": "straight",
        "slots": [
          {
            "key": "squat",
            "pattern": "squat",
            "prefer": [
              "back_squat",
              "hack_squat",
              "leg_press",
              "goblet_squat"
            ],
            "sets": 2,
            "reps": "6-10",
            "rest": 120,
            "effort": "1 to 3 left in the tank, every rep clean",
            "rule": "double_progression",
            "score": true
          },
          {
            "key": "bench",
            "pattern": "h_push",
            "prefer": [
              "bench_press",
              "chest_press_machine",
              "db_bench_press"
            ],
            "sets": 2,
            "reps": "6-10",
            "rest": 120,
            "effort": "1 to 3 left in the tank, every rep clean",
            "rule": "double_progression"
          }
        ]
      },
      {
        "name": "Second lift",
        "kind": "secondary",
        "format": "straight",
        "slots": [
          {
            "key": "row",
            "pattern": "h_pull",
            "prefer": [
              "chest_supported_row",
              "barbell_row",
              "machine_row",
              "db_row"
            ],
            "sets": 2,
            "reps": "6-10",
            "rest": 90,
            "effort": "1 to 3 left in the tank, every rep clean",
            "rule": "double_progression"
          }
        ]
      }
    ]
  }
}
```
