# GZCLP · strength-gzclp-4

**What it is.** Cody Lefever's linear progression built on tiers. Each day has one heavy main lift (T1), one lighter secondary compound (T2) and one high rep accessory (T3). When you fail, the lift does not drop: it changes its set and rep scheme first, and only resets after the last stage.

**Who it is for.** A late novice to early intermediate who wants strength and size together. 3 or 4 days a week, 60 to 75 minutes, a barbell, a rack, a bench, plates, and either a pulldown or a bar for chin-ups.

**The week.** Four sessions done in order. On 3 days a week the same rotation keeps going.

| session | T1 (heavy) | T2 (lighter) | T3 (pump) |
|:-|:-|:-|:-|
| A1 | squat 5 x 3+ | bench press 3 x 10 | lat pulldown 3 x 15 to 25 |
| B1 | overhead press 5 x 3+ | deadlift 3 x 10 | dumbbell row 3 x 15 to 25 |
| A2 | bench press 5 x 3+ | squat 3 x 10 | lat pulldown 3 x 15 to 25 |
| B2 | deadlift 5 x 3+ | overhead press 3 x 10 | dumbbell row 3 x 15 to 25 |

**How it climbs.** T1 starts around 85% of your 5RM (the first outing finds it) and the last set is as many as you have. Every session with all reps done, the load goes up [checked, secondary: research/01]: +5 kg on squat and deadlift, +2.5 kg on bench and press, the house steps, since the research gives no number. The tiers keep the 1:2:3 rep ratio T1:T2:T3 [checked, secondary]. On a failure:

- T1 moves 5 x 3, then 6 x 2, then 10 x 1, then back to the first stage at 85% of the load.
- T2 moves 3 x 10, then 3 x 8, then 3 x 6, then back to the first stage at 85%.
- T3 adds weight when the sets reach 25 reps.

**The stage sequence is [believe]**: it is the widely published GZCLP sequence, not confirmed against Lefever's own text in this research. **Verify at milestone 2.**

**Deload.** None scheduled. The stage changes and the 85% reset are the deload, per lift. The 6 week block review asks whether two lifts have reset, and offers the next program.

**Graduates to.** `strength-531-bbb-4` or `strength-rpe-4`.

**Evidence: B.** Session to session progression with a built in fallback suits late novices, and the T2 and T3 volume brings each muscle near the 10 weekly sets the volume research favours (Schoenfeld 2017) [checked, research/01]. No trial of GZCLP itself.

**Credit.** GZCLP and the GZCL method are Cody Lefever's (the GZCL blog and the GZCL substack, gzcl.substack.com). This file uses the public outline only. Read the original and support the author.

## The data (the engine reads this block)

```json
{
  "id": "strength-gzclp-4",
  "name": "GZCLP",
  "family": "strength",
  "draws_from": [
    "GZCLP",
    "GZCL method"
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
    "plates"
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
    "strength-531-bbb-4",
    "strength-rpe-4"
  ],
  "block_weeks": 6,
  "deload": null,
  "meso": null,
  "layouts": {
    "3": [
      "A1",
      "B1",
      "A2",
      "B2"
    ],
    "4": [
      "A1",
      "B1",
      "A2",
      "B2"
    ]
  },
  "modules": [],
  "sessions": {
    "A1": {
      "title": "T1 squat · T2 bench",
      "tags": [
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "T1",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat_t1",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 5,
              "reps": "3+",
              "rest": 210,
              "effort": "T1: heavy, last set as many clean reps as you have",
              "rule": "tier_stages",
              "tier": "T1",
              "inc": 5,
              "score": true
            }
          ]
        },
        {
          "name": "T2",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "bench_t2",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 3,
              "reps": "10",
              "rest": 150,
              "effort": "T2: lighter, 2 or 3 left on the first sets",
              "rule": "tier_stages",
              "tier": "T2",
              "inc": 2.5
            }
          ]
        },
        {
          "name": "T3",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "pulldown_t3",
              "pattern": "v_pull",
              "prefer": [
                "lat_pulldown",
                "band_lat_pulldown",
                "assisted_pull_up",
                "chin_up"
              ],
              "sets": 3,
              "reps": "15-25",
              "rest": 75,
              "effort": "T3: last set as many as clean; at 25 the weight goes up",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "B1": {
      "title": "T1 press · T2 deadlift",
      "tags": [
        "hinge_heavy"
      ],
      "blocks": [
        {
          "name": "T1",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "press_t1",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 5,
              "reps": "3+",
              "rest": 210,
              "effort": "T1: heavy, last set as many clean reps as you have",
              "rule": "tier_stages",
              "tier": "T1",
              "inc": 2.5,
              "score": true
            }
          ]
        },
        {
          "name": "T2",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "deadlift_t2",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift"
              ],
              "sets": 3,
              "reps": "10",
              "rest": 150,
              "effort": "T2: lighter, 2 or 3 left on the first sets",
              "rule": "tier_stages",
              "tier": "T2",
              "inc": 5
            }
          ]
        },
        {
          "name": "T3",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "row_t3",
              "pattern": "h_pull",
              "prefer": [
                "db_row",
                "seated_cable_row",
                "chest_supported_row"
              ],
              "sets": 3,
              "reps": "15-25",
              "rest": 75,
              "effort": "T3: last set as many as clean; at 25 the weight goes up",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "A2": {
      "title": "T1 bench · T2 squat",
      "tags": [
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "T1",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "bench_t1",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 5,
              "reps": "3+",
              "rest": 210,
              "effort": "T1: heavy, last set as many clean reps as you have",
              "rule": "tier_stages",
              "tier": "T1",
              "inc": 2.5,
              "score": true
            }
          ]
        },
        {
          "name": "T2",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "squat_t2",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 3,
              "reps": "10",
              "rest": 150,
              "effort": "T2: lighter, 2 or 3 left on the first sets",
              "rule": "tier_stages",
              "tier": "T2",
              "inc": 5
            }
          ]
        },
        {
          "name": "T3",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "pulldown_t3",
              "pattern": "v_pull",
              "prefer": [
                "lat_pulldown",
                "band_lat_pulldown",
                "assisted_pull_up",
                "chin_up"
              ],
              "sets": 3,
              "reps": "15-25",
              "rest": 75,
              "effort": "T3: last set as many as clean; at 25 the weight goes up",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "B2": {
      "title": "T1 deadlift · T2 press",
      "tags": [
        "hinge_heavy"
      ],
      "blocks": [
        {
          "name": "T1",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "deadlift_t1",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift"
              ],
              "sets": 5,
              "reps": "3+",
              "rest": 210,
              "effort": "T1: heavy, last set as many clean reps as you have",
              "rule": "tier_stages",
              "tier": "T1",
              "inc": 5,
              "score": true
            }
          ]
        },
        {
          "name": "T2",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "press_t2",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 3,
              "reps": "10",
              "rest": 150,
              "effort": "T2: lighter, 2 or 3 left on the first sets",
              "rule": "tier_stages",
              "tier": "T2",
              "inc": 2.5
            }
          ]
        },
        {
          "name": "T3",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "row_t3",
              "pattern": "h_pull",
              "prefer": [
                "db_row",
                "seated_cable_row",
                "chest_supported_row"
              ],
              "sets": 3,
              "reps": "15-25",
              "rest": 75,
              "effort": "T3: last set as many as clean; at 25 the weight goes up",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · T1 squat · T2 bench",
    "tags": [
      "heavy_legs"
    ],
    "blocks": [
      {
        "name": "T1",
        "kind": "main",
        "format": "straight",
        "slots": [
          {
            "key": "squat_t1",
            "pattern": "squat",
            "prefer": [
              "back_squat"
            ],
            "sets": 5,
            "reps": "3+",
            "rest": 210,
            "effort": "T1: heavy, last set as many clean reps as you have",
            "rule": "tier_stages",
            "tier": "T1",
            "inc": 5,
            "score": true
          }
        ]
      },
      {
        "name": "T2",
        "kind": "secondary",
        "format": "straight",
        "slots": [
          {
            "key": "bench_t2",
            "pattern": "h_push",
            "prefer": [
              "bench_press"
            ],
            "sets": 3,
            "reps": "10",
            "rest": 150,
            "effort": "T2: lighter, 2 or 3 left on the first sets",
            "rule": "tier_stages",
            "tier": "T2",
            "inc": 2.5
          }
        ]
      }
    ]
  }
}
```
