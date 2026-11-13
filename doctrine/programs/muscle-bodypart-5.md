# Body part split, five days · muscle-bodypart-5

**What it is.** The classic gym week: chest day, back day, leg day, shoulder day, arm day. Each muscle once a week, with a lot of sets on its day.

**Who it is for.** Intermediate or advanced, the goal is muscle, and you simply like training this way. **It is served only when you ask for it.** It is never offered for strength or powerlifting. 5 days, 50 to 75 minutes, dumbbells and a bench minimum.

**Why it is legal for muscle, and only for muscle.** Once weekly volume is equal, how often you hit a muscle barely changes how much it grows (Pelland meta-regression, and a volume-equated 2019 analysis) [checked Pelland direction, believe 2019]. Strength is the opposite: it clearly rises with frequency [checked, Pelland]. So once a week is a fair choice for size if you like it, and a bad one for a stronger lift. The cost is per session: past about 10 sets on one muscle in one session the extra sets return less [believe], which is why the days here stop around 10.

**The week.** Chest, Back, Legs, Shoulders, Arms. One lap a week on 5 days. On 4 days the trainer picks a 4 day plan instead: five sessions are never squeezed into four days.

| session | main block | then |
|:-|:-|:-|
| Chest | bench press 4 x 6 to 10 | incline press 3 x 6 to 10 · cable fly 3 x 10 to 15 · dip 2 x 8 to 12 |
| Back | pulldown or pull-up 4 x 6 to 10 | chest-supported row 3 x 6 to 10 · one-arm row 3 x 8 to 12 · straight-arm pulldown 2 x 10 to 15 |
| Legs | squat 4 x 6 to 10 | Romanian deadlift 3 x 6 to 10 · leg extension 3 · seated leg curl 3 · calf raise 3, 10 to 15 |
| Shoulders | overhead press 4 x 6 to 10 | lateral raise 4 · rear delt 3 · face pull 2 · seated calf raise 3, 10 to 15 |
| Arms | close-grip bench 3 x 6 to 10 | incline curl 3 · overhead triceps extension 3 · hammer curl 3 · pushdown 2, 10 to 15 |

Weekly direct sets land at about 10 to 16 per major muscle, more for arms because chest and back days add indirect work [checked dose, Schoenfeld 2017; checked fractional count, Pelland]. Rests: compounds 120 to 150 s, isolation 60 to 90 s.

**How it climbs.** Double progression, compounds at 1 to 3 in reserve, isolation 0 to 2 [checked, Refalo 2023, Robinson 2024]. Accessories ramp reps in reserve 3, 2, 2, 1 with an extra set in weeks 3 and 4 [believe, RP shape].

**Deload.** Week 5: half the sets, about 10% lighter, 3 to 4 in reserve [believe].

**Graduates to.** `muscle-ppl-6` if strength starts to matter to you, because it hits each muscle twice.

**Evidence: C.** As a program it is tradition [research/01, Arnold and bro split entry]. The one principle that makes it acceptable for muscle (frequency matters little once volume is matched) is solid; nothing makes it good for strength.

**Credit.** The body part split is decades of gym tradition. Jeff Nippard's Fundamentals has a 5 day bodypart version (jeffnippard.com/products/fundamentals-hypertrophy-program), buy it for his sessions. The frequency finding is Pelland et al., Sports Med, doi 10.1007/s40279-025-02344-w.

## The data (the engine reads this block)

```json
{
  "id": "muscle-bodypart-5",
  "name": "Body part split, five days",
  "family": "muscle",
  "draws_from": [
    "Classic bro split",
    "Nippard Fundamentals Bodypart split",
    "Pelland 2025 frequency finding"
  ],
  "goals": {
    "muscle": 2,
    "strength": 1,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 0,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 1,
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
    50,
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
  "evidence": "C",
  "simplicity": 2,
  "graduates_to": [
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
    "5": [
      "Chest",
      "Back",
      "Legs",
      "Shoulders",
      "Arms"
    ]
  },
  "modules": [
    "core"
  ],
  "sessions": {
    "Chest": {
      "title": "Chest",
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
                "chest_press_machine",
                "db_bench_press"
              ],
              "sets": 4,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 reps spare, every rep clean",
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
              "key": "incline",
              "pattern": "h_push",
              "prefer": [
                "incline_bench_press",
                "incline_db_press"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 reps spare, every rep clean",
              "rule": "double_progression",
              "score": false
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
                "db_bench_press"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have, deep stretch at the bottom",
              "rule": "double_progression"
            },
            {
              "key": "dip",
              "pattern": "h_push",
              "prefer": [
                "dip",
                "chest_press_machine",
                "db_bench_press"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have, lean forward",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Back": {
      "title": "Back",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
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
              "sets": 4,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 reps spare, every rep clean",
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
              "effort": "1 to 3 reps spare, every rep clean",
              "rule": "double_progression"
            },
            {
              "key": "onearmrow",
              "pattern": "h_pull",
              "prefer": [
                "db_row",
                "machine_row",
                "seated_cable_row"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 90,
              "effort": "1 to 3 reps spare, every rep clean, each arm",
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
              "key": "straightarm",
              "pattern": "v_pull",
              "prefer": [
                "straight_arm_pulldown",
                "single_arm_cable_pulldown",
                "band_lat_pulldown"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Legs": {
      "title": "Legs",
      "tags": [
        "heavy_legs",
        "hinge_heavy"
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
                "back_squat",
                "hack_squat",
                "leg_press",
                "goblet_squat"
              ],
              "sets": 4,
              "reps": "6-10",
              "rest": 150,
              "effort": "1 to 3 reps spare, every rep clean",
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
              "key": "rdl",
              "pattern": "hinge",
              "prefer": [
                "romanian_deadlift",
                "db_romanian_deadlift"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 150,
              "effort": "1 to 3 reps spare, every rep clean, flat back, deep stretch",
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
              "key": "legext",
              "pattern": "quads_iso",
              "prefer": [
                "leg_extension",
                "spanish_squat"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            },
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
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
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
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have, pause in the stretch",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Shoulders": {
      "title": "Shoulders",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "ohp",
              "pattern": "v_push",
              "prefer": [
                "overhead_press",
                "db_shoulder_press",
                "seated_db_press"
              ],
              "sets": 4,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 reps spare, every rep clean",
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
              "key": "lateral",
              "pattern": "delts",
              "prefer": [
                "cable_lateral_raise",
                "lateral_raise",
                "band_lateral_raise"
              ],
              "sets": 4,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
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
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            },
            {
              "key": "face",
              "pattern": "h_pull",
              "prefer": [
                "face_pull",
                "band_row",
                "db_row"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            },
            {
              "key": "calves2",
              "pattern": "calves",
              "prefer": [
                "seated_calf_raise",
                "calf_raise"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Arms": {
      "title": "Arms",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "closegrip",
              "pattern": "h_push",
              "prefer": [
                "close_grip_bench",
                "db_bench_press"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 reps spare, every rep clean",
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
              "key": "curl",
              "pattern": "biceps",
              "prefer": [
                "incline_db_curl",
                "cable_curl",
                "db_curl"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
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
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            },
            {
              "key": "hammer",
              "pattern": "biceps",
              "prefer": [
                "hammer_curl",
                "db_curl"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            },
            {
              "key": "tri2",
              "pattern": "triceps",
              "prefer": [
                "rope_pushdown",
                "band_pushdown",
                "skull_crusher"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Short version · the day's first two lifts",
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
              "chest_press_machine",
              "db_bench_press"
            ],
            "sets": 3,
            "reps": "6-10",
            "rest": 120,
            "effort": "1 to 3 reps spare, every rep clean",
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
            "rest": 90,
            "effort": "1 to 3 reps spare, every rep clean",
            "rule": "double_progression"
          }
        ]
      }
    ]
  }
}
```
