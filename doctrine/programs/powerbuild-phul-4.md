# PHUL · powerbuild-phul-4

**What it is.** Power Hypertrophy Upper Lower: two heavy days and two size days a week. The power days build strength on the big lifts in sets of 3 to 5, the hypertrophy days build muscle in sets of 8 to 15. Every muscle is trained twice a week.

**Who it is for.** A late novice to intermediate who wants size and strength in the same block. 3 or 4 days a week, 60 to 75 minutes, a barbell, a rack, a bench, plates and dumbbells. Cable and machine moves have dumbbell or bodyweight fallbacks.

**The week.** Upper power, lower power, rest, upper hypertrophy, lower hypertrophy. On 3 days the four sessions keep rotating.

| session | main block | then |
|:-|:-|:-|
| Upper power | bench press 4 x 3 to 5 · barbell row 4 x 3 to 5 | overhead press 3 x 6 to 10 · chin-ups 3 x 6 to 10 · curls and triceps 2 x 6 to 10 |
| Lower power | squat 4 x 3 to 5 · deadlift 3 x 3 to 5 | leg press 3 x 10 to 15 · leg curl 3 x 6 to 10 · calves 4 x 6 to 10 |
| Upper hypertrophy | incline dumbbell press 3 x 8 to 12 · cable row 3 x 8 to 12 | fly, lateral raise, curl, triceps 3 x 10 to 15 |
| Lower hypertrophy | front squat 3 x 8 to 12 · Romanian deadlift 3 x 8 to 12 | lunge, leg extension, leg curl, calves 3 x 10 to 15 |

**How it climbs.** Double progression everywhere: hit the top of the range on every set, then add the smallest jump [believe: research/01, PHUL says "add load when the top of the range is hit"]. The rep ranges themselves are [believe]; the 4 day, 2 power plus 2 hypertrophy structure is [checked, secondary]. Accessories follow a 4 week mesocycle: 3 reps left in week 1, 2 in week 2, 1 to 2 in week 3, 1 in week 4, plus one set from week 2 on. That ramp is the RP style mesocycle on top of Robinson 2024, where growth improves as sets end closer to failure [checked for the direction; the ramp itself is coach consensus, B].

**Deload.** After each 4 week block, one week at half the sets, 90% of the load, 4 reps left [believe: research/01, 1 week at about half volume after 4 to 6 weeks].

**Graduates to.** `powerbuild-phat-5` with a fifth day, or `strength-rpe-4` if strength takes over.

**Evidence: B.** Twice a week per muscle with 10 or more hard sets fits the volume and frequency research (Schoenfeld 2017, Pelland) [checked, research/01]. PHUL itself has no trial.

**Credit.** PHUL is Brandon Campbell's program [checked, secondary]. This file uses its public outline only; read the original write up and support the author.

## The data (the engine reads this block)

```json
{
  "id": "powerbuild-phul-4",
  "name": "PHUL",
  "family": "powerbuild",
  "draws_from": [
    "PHUL",
    "RP mesocycle model",
    "Robinson 2024"
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
    "health": 2,
    "independent": 2
  },
  "experience": [
    "novice",
    "intermediate"
  ],
  "days": [
    3,
    4
  ],
  "sweet_days": [
    4
  ],
  "minutes": [
    60,
    75
  ],
  "express_minutes": 35,
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
    "powerbuild-phat-5",
    "strength-rpe-4"
  ],
  "block_weeks": 4,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 0.9,
    "rir": "4"
  },
  "meso": {
    "rir_by_week": [
      "3",
      "2",
      "1 to 2",
      "1"
    ],
    "extra_sets_by_week": [
      0,
      1,
      1,
      1
    ],
    "applies_to": [
      "accessory"
    ]
  },
  "layouts": {
    "3": [
      "UpperPower",
      "LowerPower",
      "UpperHyp",
      "LowerHyp"
    ],
    "4": [
      "UpperPower",
      "LowerPower",
      "UpperHyp",
      "LowerHyp"
    ]
  },
  "modules": [],
  "sessions": {
    "UpperPower": {
      "title": "Upper power · Bench · Row",
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
                "bench_press"
              ],
              "sets": 4,
              "reps": "3-5",
              "rest": 180,
              "effort": "heavy, 1 or 2 left, every rep clean",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "barbell_row",
                "pendlay_row",
                "db_row"
              ],
              "sets": 4,
              "reps": "3-5",
              "rest": 180,
              "effort": "heavy, 1 or 2 left, every rep clean",
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
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "overhead_press",
                "db_shoulder_press"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "chin",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "pull_up",
                "lat_pulldown"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 120,
              "effort": "2 left",
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
              "key": "curl_power",
              "pattern": "biceps",
              "prefer": [
                "ez_bar_curl",
                "db_curl"
              ],
              "sets": 2,
              "reps": "6-10",
              "rest": 75,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "triceps_power",
              "pattern": "triceps",
              "prefer": [
                "skull_crusher",
                "overhead_db_triceps_extension"
              ],
              "sets": 2,
              "reps": "6-10",
              "rest": 75,
              "effort": "2 left",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LowerPower": {
      "title": "Lower power · Squat · Deadlift",
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
                "back_squat"
              ],
              "sets": 4,
              "reps": "3-5",
              "rest": 210,
              "effort": "heavy, 1 or 2 left, every rep clean",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "deadlift",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift"
              ],
              "sets": 3,
              "reps": "3-5",
              "rest": 210,
              "effort": "heavy, 1 or 2 left, every rep clean",
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
              "key": "leg_press",
              "pattern": "squat",
              "prefer": [
                "leg_press",
                "hack_squat",
                "goblet_squat"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 120,
              "effort": "2 left",
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
              "key": "leg_curl",
              "pattern": "hamstrings_iso",
              "prefer": [
                "seated_leg_curl",
                "lying_leg_curl",
                "slider_leg_curl"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 75,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "calves",
              "pattern": "calves",
              "prefer": [
                "calf_raise",
                "single_leg_calf_raise"
              ],
              "sets": 4,
              "reps": "6-10",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "UpperHyp": {
      "title": "Upper hypertrophy · Incline · Row",
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
                "incline_db_press",
                "incline_bench_press"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 120,
              "effort": "2 left",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "cable_row",
              "pattern": "h_pull",
              "prefer": [
                "seated_cable_row",
                "chest_supported_row",
                "db_row"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 120,
              "effort": "2 left",
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
                "push_up",
                "db_floor_press"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
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
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "curl",
              "pattern": "biceps",
              "prefer": [
                "incline_db_curl",
                "db_curl",
                "cable_curl"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "triceps",
              "pattern": "triceps",
              "prefer": [
                "rope_pushdown",
                "overhead_db_triceps_extension",
                "band_pushdown"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LowerHyp": {
      "title": "Lower hypertrophy · Front squat · RDL",
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
              "key": "front_squat",
              "pattern": "squat",
              "prefer": [
                "front_squat",
                "hack_squat",
                "goblet_squat"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 150,
              "effort": "2 left",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "rdl",
              "pattern": "hinge",
              "prefer": [
                "romanian_deadlift",
                "db_romanian_deadlift"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 150,
              "effort": "2 left",
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
                "walking_lunge",
                "db_reverse_lunge",
                "bulgarian_split_squat"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left, each leg",
              "rule": "double_progression"
            },
            {
              "key": "leg_ext",
              "pattern": "quads_iso",
              "prefer": [
                "leg_extension",
                "spanish_squat"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
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
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
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
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · Squat · Bench",
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
              "back_squat"
            ],
            "sets": 3,
            "reps": "3-5",
            "rest": 180,
            "effort": "heavy, 1 or 2 left, every rep clean",
            "rule": "double_progression",
            "score": true
          },
          {
            "key": "bench",
            "pattern": "h_push",
            "prefer": [
              "bench_press"
            ],
            "sets": 3,
            "reps": "3-5",
            "rest": 180,
            "effort": "heavy, 1 or 2 left, every rep clean",
            "rule": "double_progression"
          }
        ]
      }
    ]
  }
}
```
