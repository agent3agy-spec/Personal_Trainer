# Upper lower for muscle, four days · muscle-upperlower-4

**What it is.** Four sessions, two upper and two lower, done in order: Upper A, Lower A, Upper B, Lower B. Every muscle twice a week, with more room per session than full body, so more sets fit without a two hour day.

**Who it is for.** Intermediate, or a late novice who has run out of room in a full-body week (the Fundamentals Upper/Lower slot in the research grid). 4 days, 50 to 75 minutes. Dumbbells and a bench are the minimum, barbell and machines are used when they are there.

**The week.** UA, LA, UB, LB. One lap a week on 4 days. On 3 days the trainer uses a full body plan instead: four sessions are never squeezed into three days, because each muscle would drop to about 1.5 hits a week.

| session | main block | second lift | accessories |
|:-|:-|:-|:-|
| Upper A | bench press 3 x 6 to 10 · chest-supported row 3 x 6 to 10 | overhead press 2 x 6 to 10 · pulldown 3 x 6 to 10 | lateral raise 3 x 10 to 15 · overhead triceps extension 2 x 10 to 15 · incline curl 2 x 10 to 15 |
| Lower A | squat 3 x 6 to 10 | Romanian deadlift 3 x 6 to 10 | leg extension 2 x 10 to 15 · seated leg curl 3 x 10 to 15 · calf raise 3 x 10 to 15 |
| Upper B | incline press 3 x 6 to 10 · chin-up 3 x 6 to 10 | cable row 3 x 6 to 10 | cable fly 2 · rear delt fly 2 · lateral raise 2 · skull crusher 2 · hammer curl 2, all 10 to 15 |
| Lower B | leg press 3 x 6 to 10 | hip thrust 3 x 6 to 10 | Bulgarian split squat 3 x 10 to 15 · lying leg curl 3 x 10 to 15 · seated calf raise 3 x 10 to 15 |

At 4 days each major muscle lands at about 10 to 16 weekly hard sets counted the fractional way [checked, Pelland], above the 10 set line that grew more [checked, Schoenfeld 2017]. Rests: compounds 120 to 150 s, isolation 60 to 90 s.

**How it climbs.** Double progression everywhere: top of the range on every set at the written effort, then the smallest weight step and back to the bottom. Compounds at 1 to 3 reps in reserve, isolation at 0 to 2 [checked, Refalo 2023 and Robinson 2024]. Accessories ramp over each 4 week block: reps in reserve 3, 2, 2, 1, plus one set each in weeks 3 and 4 [believe, RP mesocycle shape].

Lengthened choices again: Romanian deadlift, seated leg curl, overhead triceps extension, incline curl [checked, Maeo 2021 and 2022/23].

**Deload.** Week 5: half the sets, about 10% lighter, 3 to 4 in reserve [believe, research/01 rule 7]. Earlier if two sessions in a row go backwards.

**Graduates to.** `muscle-ppl-6` when you have 5 or 6 days and the four sessions cannot hold the volume you recover from.

**Evidence: B.** Twice a week per muscle with enough sets is the A level principle; the upper lower split itself is coach packaging [research/01].

**Credit.** The split follows the public outline of Jeff Nippard's Fundamentals Upper/Lower (jeffnippard.com/products/fundamentals-hypertrophy-program) and PHUL by Brandon Campbell (hevyapp.com/phul-power-hypertrophy-upper-lower). Buy Nippard's program for his exact sessions. The volume and effort numbers are Brad Schoenfeld's and the Pelland meta-regression.

## The data (the engine reads this block)

```json
{
  "id": "muscle-upperlower-4",
  "name": "Upper lower for muscle, four days",
  "family": "muscle",
  "draws_from": [
    "Nippard Fundamentals Upper/Lower",
    "PHUL (Brandon Campbell)",
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
    "health": 2,
    "independent": 1
  },
  "experience": [
    "novice",
    "intermediate",
    "advanced"
  ],
  "days": [
    4,
    4
  ],
  "sweet_days": [
    4
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
    "4": [
      "UA",
      "LA",
      "UB",
      "LB"
    ]
  },
  "modules": [
    "core"
  ],
  "sessions": {
    "UA": {
      "title": "Upper A · Bench · Row",
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
              "rule": "double_progression",
              "score": true
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
              "key": "ohp",
              "pattern": "v_push",
              "prefer": [
                "overhead_press",
                "db_shoulder_press",
                "seated_db_press"
              ],
              "sets": 2,
              "reps": "6-10",
              "rest": 120,
              "effort": "1 to 3 reps spare, every rep clean",
              "rule": "double_progression"
            },
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
              "effort": "1 to 3 reps spare, every rep clean",
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
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
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
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LA": {
      "title": "Lower A · Squat · Romanian deadlift",
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
              "sets": 3,
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
              "sets": 2,
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
    "UB": {
      "title": "Upper B · Incline · Chin-up",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
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
              "effort": "1 to 3 reps spare, every rep clean",
              "rule": "double_progression"
            },
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
              "effort": "1 to 3 reps spare, every rep clean",
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
              "key": "fly",
              "pattern": "h_push",
              "prefer": [
                "cable_fly",
                "db_bench_press"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have, deep stretch at the bottom",
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
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
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
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have",
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
    "LB": {
      "title": "Lower B · Leg press · Hip thrust",
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
              "effort": "1 to 3 reps spare, every rep clean",
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
              "effort": "0 to 2 reps spare, last set: stop when one more clean rep is all you have, each leg",
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
    }
  },
  "express": {
    "title": "Short version · Squat · Bench · Row",
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
              "back_squat",
              "hack_squat",
              "leg_press",
              "goblet_squat"
            ],
            "sets": 2,
            "reps": "6-10",
            "rest": 120,
            "effort": "1 to 3 reps spare, every rep clean",
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
            "sets": 2,
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
