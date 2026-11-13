# Home full body, any kit · home-fullbody-2to4

**What it is.** Full-body sessions for home that work with whatever you have: dumbbells, bands, or nothing but the floor. Every slot tries dumbbells first, then a band, then a bodyweight version, so the same plan runs in a flat with a pair of dumbbells or in a hotel room. It also runs seated: every session has a seated option on at least one slot (seated band chest press, seated dumbbell press, seated band row, seated curl, seated calf raise).

**Who it is for.** Anyone, from never trained to advanced, who trains at home. Best for health, fat loss and staying independent; good for muscle; limited for maximal strength. 2 to 4 days a week, 20 to 60 minutes, and a 15 minute express circuit for the bad days.

**The week.** Sessions in order, never tied to a weekday.

| days | rotation |
|:-|:-|
| 2 | A, B |
| 3 | A, B, C |
| 4 | A, B, C, D |

| session | main block | second lifts | accessories |
|:-|:-|:-|:-|
| A | goblet squat 3 x 8 to 15 · floor press or push-up 3 x 8 to 15 | one-arm row 3 x 8 to 15 · Romanian deadlift 3 x 10 to 20 | lateral raise 2 x 10 to 20 |
| B | reverse lunge 3 x 8 to 15 · shoulder press 3 x 8 to 15 | row 3 x 10 to 20 · hip thrust or glute bridge 3 x 10 to 20 | curl 2 · overhead triceps 2, 10 to 20 |
| C | heel-raised goblet squat 3 x 10 to 20 · bench press or push-up 3 x 10 to 20 | one-arm row 3 x 8 to 15 · slider leg curl 2 x 8 to 15 | rear delt fly 2 · calf raise 2, 10 to 20 |
| D | step-up 3 x 10 to 20 · Arnold press 3 x 10 to 20 | row 3 x 10 to 20 · Romanian deadlift 3 x 10 to 20 | lateral raise 2 · curl 2, 10 to 20 |

Rests: 90 s on the big moves, 60 s on the small ones. Express: squat, push and row as a circuit, 2 rounds, 60 s between rounds.

**Why light weights work.** For muscle, the load hardly matters across a wide range, from about 30% of your max upward, as long as the set ends close to failure [checked, Schoenfeld 2017 load meta-analysis; seen in research/03 B6]. Push-ups built the chest as well as a bench press at matched load [seen, Kikuchi 2017], and bands gave the same strength as free weights [seen, Lopes 2019]. So every set here ends 1 to 3 reps short of failure [seen, Refalo 2023]. Only maximal strength in a heavy lift really needs heavy weight [seen, Schoenfeld 2016 snippet].

**How it climbs: the fixed-weight ladder.** Double progression first: hit the top of the range on every set, then make it harder. If there is a heavier dumbbell, take it. If there is not, the engine moves you to the next harder version of the move instead of asking for weight you do not own. The order to make a move harder, cheapest first [believe the ordering, seen the load evidence under it, research/03 C5]:

1. more reps inside the range (8 to 15, then 10 to 20)
2. slower lowering, 3 to 4 s, and a 1 to 2 s pause at the hardest point
3. one side at a time: goblet squat to split squat to Bulgarian, two-arm row to one-arm
4. more range or leverage: deficit or feet-raised push-ups, 1.5 reps
5. a mechanical drop set: hardest version to failure, then an easier one straight away
6. the same work in less time
7. one more set (about 10 to 20 hard sets a week per muscle is the target) [believe here, checked in research/01]
8. once the hardest version goes past about 30 reps, buy the next bell or band [believe]

Bands are logged by colour and how far you stand from the anchor, so the progression stays visible [seen, research/03 C4].

**Deload.** After 6 weeks, one week at half the sets and 3 to 4 in reserve. No load change: there is no load to cut.

**Graduates to.** `muscle-fullbody-3` when a gym becomes possible, or `calisthenics-rr-3` once you have a pull-up bar.

**Evidence: B.** The principle (hard sets near failure grow muscle at any load) is meta-analysis level; the packaging is coach practice.

**Credit.** Built on the published research named above, and on Dan John's minimalist movement menu (push, pull, hinge, squat, carry: danjohn.net). Nothing here copies a paid program.

## The data (the engine reads this block)

```json
{
  "id": "home-fullbody-2to4",
  "name": "Home full body, any kit",
  "family": "home",
  "draws_from": [
    "Schoenfeld 2017 load meta-analysis",
    "Kikuchi 2017 push-ups",
    "Lopes 2019 bands",
    "Dan John minimalism"
  ],
  "goals": {
    "muscle": 2,
    "strength": 1,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 3,
    "health": 3,
    "independent": 2
  },
  "experience": [
    "none",
    "novice",
    "intermediate",
    "advanced"
  ],
  "days": [
    2,
    4
  ],
  "sweet_days": [
    3
  ],
  "minutes": [
    20,
    60
  ],
  "express_minutes": 15,
  "equipment_all": [],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [],
  "evidence": "B",
  "simplicity": 2,
  "graduates_to": [
    "muscle-fullbody-3",
    "calisthenics-rr-3"
  ],
  "block_weeks": 6,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 1.0,
    "rir": "3 to 4"
  },
  "meso": null,
  "layouts": {
    "2": [
      "A",
      "B"
    ],
    "3": [
      "A",
      "B",
      "C"
    ],
    "4": [
      "A",
      "B",
      "C",
      "D"
    ]
  },
  "modules": [
    "core"
  ],
  "sessions": {
    "A": {
      "title": "Squat · Push · Row",
      "tags": [],
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
                "goblet_squat",
                "band_squat",
                "split_squat",
                "bodyweight_squat",
                "sit_to_stand",
                "assisted_squat"
              ],
              "sets": 3,
              "reps": "8-15",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load",
              "score": true
            },
            {
              "key": "push",
              "pattern": "h_push",
              "prefer": [
                "db_floor_press",
                "db_bench_press",
                "band_chest_press",
                "seated_band_chest_press",
                "push_up",
                "incline_push_up",
                "knee_push_up"
              ],
              "sets": 3,
              "reps": "8-15",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
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
                "db_row",
                "band_row",
                "seated_band_row",
                "inverted_row",
                "incline_inverted_row"
              ],
              "sets": 3,
              "reps": "8-15",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure, each arm on one-arm rows",
              "rule": "fixed_load"
            },
            {
              "key": "hinge",
              "pattern": "hinge",
              "prefer": [
                "db_romanian_deadlift",
                "band_good_morning",
                "single_leg_rdl",
                "glute_bridge"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        },
        {
          "name": "Accessory",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "lateral",
              "pattern": "delts",
              "prefer": [
                "lateral_raise",
                "seated_lateral_raise",
                "band_lateral_raise"
              ],
              "sets": 2,
              "reps": "10-20",
              "rest": 60,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        }
      ]
    },
    "B": {
      "title": "Lunge · Press · Row",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "lunge",
              "pattern": "lunge",
              "prefer": [
                "db_reverse_lunge",
                "bulgarian_split_squat",
                "reverse_lunge",
                "step_up"
              ],
              "sets": 3,
              "reps": "8-15",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure, each leg",
              "rule": "fixed_load",
              "score": true
            },
            {
              "key": "vpush",
              "pattern": "v_push",
              "prefer": [
                "db_shoulder_press",
                "seated_db_press",
                "band_overhead_press",
                "pike_push_up"
              ],
              "sets": 3,
              "reps": "8-15",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "row2",
              "pattern": "h_pull",
              "prefer": [
                "kb_row",
                "db_row",
                "seated_band_row",
                "band_row",
                "incline_inverted_row",
                "inverted_row"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            },
            {
              "key": "bridge",
              "pattern": "hinge",
              "prefer": [
                "hip_thrust",
                "glute_bridge",
                "single_leg_glute_bridge"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 75,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        },
        {
          "name": "Accessory",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "curl",
              "pattern": "biceps",
              "prefer": [
                "db_curl",
                "seated_db_curl",
                "band_curl"
              ],
              "sets": 2,
              "reps": "10-20",
              "rest": 60,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            },
            {
              "key": "tri",
              "pattern": "triceps",
              "prefer": [
                "overhead_db_triceps_extension",
                "seated_overhead_triceps_extension",
                "band_pushdown"
              ],
              "sets": 2,
              "reps": "10-20",
              "rest": 60,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        }
      ]
    },
    "C": {
      "title": "Squat · Push · Hamstrings",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat2",
              "pattern": "squat",
              "prefer": [
                "heel_elevated_goblet_squat",
                "band_squat",
                "shrimp_squat",
                "split_squat",
                "bodyweight_squat",
                "sit_to_stand"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load",
              "score": true
            },
            {
              "key": "push2",
              "pattern": "h_push",
              "prefer": [
                "db_bench_press",
                "db_floor_press",
                "band_chest_press",
                "seated_band_chest_press",
                "decline_push_up",
                "push_up",
                "incline_push_up",
                "wall_push_up"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
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
                "db_row",
                "band_row",
                "seated_band_row",
                "inverted_row",
                "incline_inverted_row"
              ],
              "sets": 3,
              "reps": "8-15",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure, each arm on one-arm rows",
              "rule": "fixed_load"
            },
            {
              "key": "hamcurl",
              "pattern": "hamstrings_iso",
              "prefer": [
                "slider_leg_curl",
                "nordic_curl"
              ],
              "sets": 2,
              "reps": "8-15",
              "rest": 75,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
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
                "rear_delt_fly",
                "band_pull_apart"
              ],
              "sets": 2,
              "reps": "10-20",
              "rest": 60,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            },
            {
              "key": "calves",
              "pattern": "calves",
              "prefer": [
                "single_leg_calf_raise",
                "calf_raise",
                "seated_calf_raise"
              ],
              "sets": 2,
              "reps": "10-20",
              "rest": 60,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        }
      ]
    },
    "D": {
      "title": "Lunge · Press · Hinge",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "lunge2",
              "pattern": "lunge",
              "prefer": [
                "step_up",
                "bulgarian_split_squat",
                "reverse_lunge",
                "lateral_lunge"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure, each leg",
              "rule": "fixed_load",
              "score": true
            },
            {
              "key": "vpush2",
              "pattern": "v_push",
              "prefer": [
                "arnold_press",
                "seated_db_press",
                "band_overhead_press",
                "pike_push_up"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "row2",
              "pattern": "h_pull",
              "prefer": [
                "kb_row",
                "db_row",
                "seated_band_row",
                "band_row",
                "incline_inverted_row",
                "inverted_row"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            },
            {
              "key": "hinge",
              "pattern": "hinge",
              "prefer": [
                "db_romanian_deadlift",
                "band_good_morning",
                "single_leg_rdl",
                "glute_bridge"
              ],
              "sets": 3,
              "reps": "10-20",
              "rest": 90,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        },
        {
          "name": "Accessory",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "lateral",
              "pattern": "delts",
              "prefer": [
                "lateral_raise",
                "seated_lateral_raise",
                "band_lateral_raise"
              ],
              "sets": 2,
              "reps": "10-20",
              "rest": 60,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            },
            {
              "key": "curl",
              "pattern": "biceps",
              "prefer": [
                "db_curl",
                "seated_db_curl",
                "band_curl"
              ],
              "sets": 2,
              "reps": "10-20",
              "rest": 60,
              "effort": "1 to 3 left in the tank, the last set near failure",
              "rule": "fixed_load"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · Squat · Push · Row circuit",
    "tags": [],
    "blocks": [
      {
        "name": "Circuit",
        "kind": "main",
        "format": "superset",
        "rest_after_round": 60,
        "slots": [
          {
            "key": "squat",
            "pattern": "squat",
            "prefer": [
              "goblet_squat",
              "band_squat",
              "split_squat",
              "bodyweight_squat",
              "sit_to_stand",
              "assisted_squat"
            ],
            "sets": 2,
            "reps": "8-15",
            "rest": 0,
            "effort": "1 to 3 left in the tank, the last set near failure",
            "rule": "fixed_load",
            "score": true
          },
          {
            "key": "push",
            "pattern": "h_push",
            "prefer": [
              "db_floor_press",
              "db_bench_press",
              "band_chest_press",
              "seated_band_chest_press",
              "push_up",
              "incline_push_up",
              "knee_push_up"
            ],
            "sets": 2,
            "reps": "8-15",
            "rest": 0,
            "effort": "1 to 3 left in the tank, the last set near failure",
            "rule": "fixed_load"
          },
          {
            "key": "row",
            "pattern": "h_pull",
            "prefer": [
              "db_row",
              "band_row",
              "seated_band_row",
              "inverted_row",
              "incline_inverted_row"
            ],
            "sets": 2,
            "reps": "8-15",
            "rest": 0,
            "effort": "1 to 3 left in the tank, the last set near failure, each arm on one-arm rows",
            "rule": "fixed_load"
          }
        ]
      }
    ]
  }
}
```
