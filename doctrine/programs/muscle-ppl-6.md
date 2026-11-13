# Push pull legs twice, six days · muscle-ppl-6

**What it is.** Push, pull, legs, then again with different lifts: six sessions done in order. Each muscle twice a week, and each session short enough to stay sharp because it only has to train a third of the body.

**Who it is for.** Intermediate or advanced, size is the goal, and you can show up 5 or 6 days a week for 50 to 75 minutes. Dumbbells and a bench are the minimum; barbell, cables and machines are used first when they are there.

**The week.** PushA, PullA, LegsA, PushB, PullB, LegsB. On 6 days that is one lap a week. On 5 days it keeps rotating, so the lap takes a little over a week.

| session | main block | second lift | accessories |
|:-|:-|:-|:-|
| Push A | bench press 3 x 6 to 10 | overhead press 3 x 6 to 10 | cable fly 2 · lateral raise 3 · overhead triceps extension 3, all 10 to 15 |
| Pull A | pull-up or pulldown 3 x 6 to 10 | chest-supported row 3 x 6 to 10 | rear delt 2 · incline curl 3 · face pull 2, all 10 to 15 |
| Legs A | squat 3 x 6 to 10 | Romanian deadlift 3 x 6 to 10 | leg extension 2 · seated leg curl 3 · calf raise 3, all 10 to 15 |
| Push B | incline press 3 x 6 to 10 | seated dumbbell press 3 · dip 2, 6 to 10 | lateral raise 3 · skull crusher 2, 10 to 15 |
| Pull B | cable row 3 x 6 to 10 | chin-up 3 x 6 to 10 | straight-arm pulldown 2 · rear delt 2 · hammer curl 3, 10 to 15 |
| Legs B | leg press 3 x 6 to 10 | hip thrust 3 x 6 to 10 | Bulgarian split squat 3 · lying leg curl 3 · seated calf raise 3, 10 to 15 |

Over a 6 day lap each major muscle gets about 10 to 16 weekly hard sets counted the fractional way [checked, Pelland], and twice a week, which is what makes the 6 day version good where the 3 day PPL is weak [believe, research/01 PPL entry]. Per-session volume stays under about 10 sets a muscle, past which returns shrink [believe]. Rests: compounds 120 to 150 s, isolation 60 to 90 s.

**How it climbs.** Double progression: top of the range on every set at the written effort, then the smallest step up and back to the bottom of the range. Compounds 1 to 3 in reserve, isolation 0 to 2 [checked, Refalo 2023, Robinson 2024]. Accessories ramp over each 4 week block: reps in reserve 3, 2, 2, 1, plus a set each in weeks 3 and 4 [believe, RP mesocycle shape]. Long-length picks throughout: Romanian deadlift, seated leg curl, overhead triceps extension, incline curl [checked, Maeo 2021, 2022/23].

**Deload.** Week 5: half the sets, about 10% lighter, 3 to 4 in reserve [believe, research/01 rule 7]. Six days a week is a lot of recovery to ask for, so take it early the moment two sessions go backwards.

**Graduates to.** Nothing above it in this folder. The next step is more sets inside the same split, added only while recovery holds (10 to 20 a week is the working range) [checked direction, Pelland; believe the ceiling].

**Evidence: B.** Meets the volume and frequency principles; the split itself is tradition, not a trial [research/01].

**Credit.** Push pull legs is public domain coaching. The twice-a-week shape matches Jeff Nippard's Pure Bodybuilding and Ultimate PPL (jeffnippard.com/products/the-ultimate-push-pull-legs-system): buy those for his exact sessions. Volume and effort numbers come from Brad Schoenfeld's work and the Pelland meta-regression.

## The data (the engine reads this block)

```json
{
  "id": "muscle-ppl-6",
  "name": "Push pull legs twice, six days",
  "family": "muscle",
  "draws_from": [
    "Push Pull Legs x2",
    "Nippard Pure Bodybuilding",
    "Schoenfeld volume and frequency"
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
    "health": 1,
    "independent": 1
  },
  "experience": [
    "intermediate",
    "advanced"
  ],
  "days": [
    5,
    6
  ],
  "sweet_days": [
    6
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
  "evidence": "B",
  "simplicity": 2,
  "graduates_to": [],
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
      "PushA",
      "PullA",
      "LegsA",
      "PushB",
      "PullB",
      "LegsB"
    ],
    "6": [
      "PushA",
      "PullA",
      "LegsA",
      "PushB",
      "PullB",
      "LegsB"
    ]
  },
  "modules": [
    "core"
  ],
  "sessions": {
    "PushA": {
      "title": "Push A · Bench · Press",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
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
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
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
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "PullA": {
      "title": "Pull A · Pull-up · Row",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
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
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression",
              "score": true
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
              "effort": "0 to 2 left in the tank, last set close to failure",
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
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LegsA": {
      "title": "Legs A · Squat · Romanian deadlift",
      "tags": [
        "heavy_legs",
        "hinge_heavy"
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
            }
          ]
        },
        {
          "name": "Second lift",
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
              "effort": "1 to 3 left in the tank, every rep clean, flat back, deep stretch",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Accessory",
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
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
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
    "PushB": {
      "title": "Push B · Incline · Dip",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
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
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "ohp2",
              "pattern": "v_push",
              "prefer": [
                "seated_db_press",
                "arnold_press",
                "db_shoulder_press"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
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
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean, lean forward",
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
              "key": "lateral2",
              "pattern": "delts",
              "prefer": [
                "lateral_raise",
                "cable_lateral_raise",
                "band_lateral_raise"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            },
            {
              "key": "tri2",
              "pattern": "triceps",
              "prefer": [
                "skull_crusher",
                "rope_pushdown",
                "band_pushdown"
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
    "PullB": {
      "title": "Pull B · Row · Chin-up",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "row2",
              "pattern": "h_pull",
              "prefer": [
                "seated_cable_row",
                "t_bar_row",
                "db_row"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 left in the tank, every rep clean",
              "rule": "double_progression",
              "score": true
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
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            },
            {
              "key": "rear2",
              "pattern": "rear_delts",
              "prefer": [
                "rear_delt_fly",
                "reverse_pec_deck",
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
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LegsB": {
      "title": "Legs B · Leg press · Hip thrust",
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
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "hipthrust_heavy",
              "pattern": "hinge",
              "prefer": [
                "hip_thrust",
                "glute_bridge",
                "single_leg_glute_bridge"
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
              "sets": 3,
              "reps": "10-15",
              "rest": 90,
              "effort": "0 to 2 left in the tank, last set close to failure, each leg",
              "rule": "double_progression"
            },
            {
              "key": "legcurl2",
              "pattern": "hamstrings_iso",
              "prefer": [
                "lying_leg_curl",
                "seated_leg_curl",
                "nordic_curl",
                "slider_leg_curl"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "0 to 2 left in the tank, last set close to failure",
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
              "effort": "0 to 2 left in the tank, last set close to failure",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · the day's two big lifts",
    "tags": [],
    "blocks": [
      {
        "name": "Main block",
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
            "sets": 2,
            "reps": "6-10",
            "rest": 120,
            "effort": "1 to 3 left in the tank, every rep clean",
            "rule": "double_progression"
          },
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
          }
        ]
      }
    ]
  }
}
```
