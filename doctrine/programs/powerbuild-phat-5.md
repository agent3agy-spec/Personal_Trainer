# PHAT · powerbuild-phat-5

**What it is.** Power Hypertrophy Adaptive Training: two power days early in the week, three hypertrophy days after. Each hypertrophy day opens with light, fast speed work on the matching power lift, then goes for size with sets of 8 to 20.

**Who it is for.** Intermediate to advanced lifters who want strength and size and have 5 days, 60 to 90 minutes each. A barbell, a rack, a bench, plates and dumbbells; cable and machine moves have fallbacks.

**The week.** Upper power, lower power, rest, back and shoulders, lower hypertrophy, chest and arms. On 4 days the trainer picks a 4 day plan instead: five sessions are never squeezed into four days.

| session | main block | then |
|:-|:-|:-|
| Upper power | bench press 3 x 3 to 5 · barbell row 3 x 3 to 5 | pull-ups 2 x 6 to 10 · shoulder press 3 x 6 to 10 · curls and triceps 3 x 6 to 10 |
| Lower power | squat 3 x 3 to 5 | hack squat 2 x 6 to 10 · Romanian deadlift 3 x 5 to 8 · leg curl 2 x 6 to 10 · calves |
| Back and shoulders | speed rows 6 x 3 · chest supported row 3 x 8 to 12 | pulldown 3 x 8 to 12 · shoulder press, lateral raise, rear delts |
| Lower hypertrophy | speed squats 6 x 3 · leg press 3 x 8 to 12 | Romanian deadlift 3 x 8 to 12 · leg extension, leg curl, calves |
| Chest and arms | speed bench 6 x 3 · incline dumbbell press 3 x 8 to 12 | fly, curls, triceps 8 to 15 |

**How it climbs.** Power lifts: double progression in the 3 to 5 range, top of the range on every set, then the smallest jump. Hypertrophy work: double progression in its range. Speed work does not climb on its own: it is 6 sets of 3 at about 65 to 70% of what you lifted on the power day, every rep as fast as you can [believe: research/01, the speed work percentages are not verified]. The 5 day split of 2 power plus 3 hypertrophy days is [checked, secondary]; the power day 3 to 5 reps is [believe].

**Deload.** After 6 weeks, one week at half the sets, 90% of the load, 4 reps left [believe: research/01, a deload after 4 to 6 accumulation weeks].

**Graduates to.** `strength-rpe-4` if strength becomes the goal, or a coach.

**Evidence: B.** High weekly volume at twice a week per muscle fits Schoenfeld 2017 and Pelland [checked, research/01]. Sources conflict on the day count (one app lists it as 6 days); this file follows Norton's 5 day layout. No trial of PHAT itself.

**Credit.** PHAT is Layne Norton's (biolayne.com). This file uses the public outline only. Read his original write up and support the author.

## The data (the engine reads this block)

```json
{
  "id": "powerbuild-phat-5",
  "name": "PHAT",
  "family": "powerbuild",
  "draws_from": [
    "PHAT"
  ],
  "goals": {
    "muscle": 3,
    "strength": 3,
    "powerlifting": 2,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 2,
    "health": 1,
    "independent": 1
  },
  "experience": [
    "intermediate",
    "advanced"
  ],
  "days": [
    5,
    5
  ],
  "sweet_days": [
    5
  ],
  "minutes": [
    60,
    90
  ],
  "express_minutes": 40,
  "equipment_all": [
    "barbell",
    "rack",
    "bench",
    "plates",
    "dumbbell"
  ],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [
    "pregnancy",
    "seated"
  ],
  "evidence": "B",
  "simplicity": 2,
  "graduates_to": [
    "strength-rpe-4"
  ],
  "block_weeks": 6,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 0.9,
    "rir": "4"
  },
  "meso": null,
  "layouts": {
    "5": [
      "UpperPower",
      "LowerPower",
      "BackShoulders",
      "LowerHyp",
      "ChestArms"
    ]
  },
  "modules": [],
  "sessions": {
    "UpperPower": {
      "title": "Upper body, heavy · Bench · Row",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "bench",
              "pattern": "h_push",
              "prefer": [
                "bench_press",
                "db_bench_press"
              ],
              "sets": 3,
              "reps": "3-5",
              "rest": 180,
              "effort": "heavy, 1 or 2 reps spare, every rep clean",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "pendlay_row",
                "barbell_row",
                "db_row"
              ],
              "sets": 3,
              "reps": "3-5",
              "rest": 180,
              "effort": "heavy, 1 or 2 reps spare, every rep clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Second exercise",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "pullup",
              "pattern": "v_pull",
              "prefer": [
                "pull_up",
                "chin_up",
                "lat_pulldown"
              ],
              "sets": 2,
              "reps": "6-10",
              "rest": 120,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "shoulder_press",
              "pattern": "v_push",
              "prefer": [
                "seated_db_press",
                "db_shoulder_press",
                "overhead_press"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "curl_power",
              "pattern": "biceps",
              "prefer": [
                "ez_bar_curl",
                "db_curl"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "triceps_power",
              "pattern": "triceps",
              "prefer": [
                "skull_crusher",
                "overhead_db_triceps_extension"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LowerPower": {
      "title": "Legs, heavy · Squat",
      "tags": [
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 3,
              "reps": "3-5",
              "rest": 210,
              "effort": "heavy, 1 or 2 reps spare, every rep clean",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Second exercise",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "hack",
              "pattern": "squat",
              "prefer": [
                "hack_squat",
                "leg_press",
                "front_squat"
              ],
              "sets": 2,
              "reps": "6-10",
              "rest": 150,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "rdl",
              "pattern": "hinge",
              "prefer": [
                "romanian_deadlift",
                "db_romanian_deadlift"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 150,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "leg_curl",
              "pattern": "hamstrings_iso",
              "prefer": [
                "lying_leg_curl",
                "seated_leg_curl",
                "slider_leg_curl"
              ],
              "sets": 2,
              "reps": "6-10",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "calves",
              "pattern": "calves",
              "prefer": [
                "calf_raise",
                "single_leg_calf_raise"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "BackShoulders": {
      "title": "Back and shoulders, for muscle",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "row_speed",
              "pattern": "h_pull",
              "prefer": [
                "barbell_row",
                "pendlay_row"
              ],
              "sets": 6,
              "reps": "3",
              "rest": 90,
              "effort": "light and fast: about two thirds of your heavy day row, every rep as fast as you can",
              "rule": "fixed"
            },
            {
              "key": "row_h",
              "pattern": "h_pull",
              "prefer": [
                "chest_supported_row",
                "seated_cable_row",
                "db_row"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 120,
              "effort": "2 reps spare",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Second exercise",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "pulldown",
              "pattern": "v_pull",
              "prefer": [
                "lat_pulldown",
                "band_lat_pulldown",
                "chin_up"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 90,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "press_h",
              "pattern": "v_push",
              "prefer": [
                "db_shoulder_press",
                "arnold_press"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "delts",
              "pattern": "delts",
              "prefer": [
                "lateral_raise",
                "cable_lateral_raise"
              ],
              "sets": 3,
              "reps": "12-20",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "rear_delts",
              "pattern": "rear_delts",
              "prefer": [
                "rear_delt_fly",
                "reverse_pec_deck",
                "band_pull_apart"
              ],
              "sets": 3,
              "reps": "12-20",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LowerHyp": {
      "title": "Legs, for muscle",
      "tags": [
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat_speed",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 6,
              "reps": "3",
              "rest": 90,
              "effort": "light and fast: about two thirds of your heavy day squat, every rep as fast as you can",
              "rule": "fixed"
            },
            {
              "key": "leg_press",
              "pattern": "squat",
              "prefer": [
                "leg_press",
                "hack_squat",
                "goblet_squat"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 120,
              "effort": "2 reps spare",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Second exercise",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "rdl_h",
              "pattern": "hinge",
              "prefer": [
                "romanian_deadlift",
                "db_romanian_deadlift"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 120,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "leg_ext",
              "pattern": "quads_iso",
              "prefer": [
                "leg_extension",
                "spanish_squat"
              ],
              "sets": 3,
              "reps": "15-20",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "leg_curl_h",
              "pattern": "hamstrings_iso",
              "prefer": [
                "seated_leg_curl",
                "lying_leg_curl",
                "slider_leg_curl"
              ],
              "sets": 3,
              "reps": "12-15",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "calves_h",
              "pattern": "calves",
              "prefer": [
                "seated_calf_raise",
                "calf_raise"
              ],
              "sets": 3,
              "reps": "12-15",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "ChestArms": {
      "title": "Chest and arms, for muscle",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "bench_speed",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 6,
              "reps": "3",
              "rest": 90,
              "effort": "light and fast: about two thirds of your heavy day bench, every rep as fast as you can",
              "rule": "fixed"
            },
            {
              "key": "incline",
              "pattern": "h_push",
              "prefer": [
                "incline_db_press",
                "incline_bench_press"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 120,
              "effort": "2 reps spare",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "fly",
              "pattern": "h_push",
              "prefer": [
                "cable_fly",
                "push_up",
                "db_floor_press"
              ],
              "sets": 2,
              "reps": "12-15",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "curl",
              "pattern": "biceps",
              "prefer": [
                "ez_bar_curl",
                "db_curl"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "curl_incline",
              "pattern": "biceps",
              "prefer": [
                "incline_db_curl",
                "hammer_curl"
              ],
              "sets": 2,
              "reps": "12-15",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "triceps",
              "pattern": "triceps",
              "prefer": [
                "overhead_db_triceps_extension",
                "cable_overhead_extension"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "pushdown",
              "pattern": "triceps",
              "prefer": [
                "rope_pushdown",
                "band_pushdown"
              ],
              "sets": 2,
              "reps": "12-15",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Short version · Squat · Bench",
    "tags": [
      "heavy_legs"
    ],
    "blocks": [
      {
        "name": "The main lifts",
        "kind": "main",
        "format": "straight",
        "slots": [
          {
            "key": "squat",
            "pattern": "squat",
            "prefer": [
              "back_squat"
            ],
            "sets": 3,
            "reps": "3-5",
            "rest": 180,
            "effort": "heavy, 1 or 2 reps spare, every rep clean",
            "rule": "double_progression",
            "score": true
          },
          {
            "key": "bench",
            "pattern": "h_push",
            "prefer": [
              "bench_press",
              "db_bench_press"
            ],
            "sets": 3,
            "reps": "3-5",
            "rest": 180,
            "effort": "heavy, 1 or 2 reps spare, every rep clean",
            "rule": "double_progression"
          }
        ]
      }
    ]
  }
}
```
