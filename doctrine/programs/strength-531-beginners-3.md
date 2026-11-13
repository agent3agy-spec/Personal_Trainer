# 5/3/1 for Beginners · strength-531-beginners-3

**What it is.** Jim Wendler's three day full body version of 5/3/1. Each session has two main lifts done on the 5/3/1 waves of a training max, then 5 more sets of 5 at the first set's weight (First Set Last, FSL), then a little push, pull and single leg or core work. Three sessions, A, B, C, done in order.

**Who it is for.** A novice whose linear progression has stalled, or an early intermediate who wants a slow, steady climb. 2 or 3 days a week, 50 to 70 minutes, a barbell, a rack, a bench and plates.

**The week.** A, B, C. On 2 days a week the rotation simply continues, so each session comes every week and a half.

| session | main block (5/3/1 waves) | FSL | assistance |
|:-|:-|:-|:-|
| A | squat · bench press | 5 x 5 squat · 5 x 5 bench | push 3 x 10 to 15 · chin-ups 3 x 10 to 15 · single leg 3 x 10 to 15 |
| B | deadlift · overhead press | 5 x 5 deadlift · 5 x 5 press | push · row · core |
| C | bench press · squat | 5 x 5 bench · 5 x 5 squat | push · chin-ups · single leg |

**How it climbs.** The training max starts at 90% of an estimated max from your first set of 5 [checked: research/01]. The waves: week 1 at 65, 75, 85% of the TM for 5, 5, 5+ · week 2 at 70, 80, 90% for 3, 3, 3+ · week 3 at 75, 85, 95% for 5, 3, 1+ [believe, standard and consistent across sources]. The last set is as many clean reps as you have. After each 3 week cycle the TM goes up +2.5 kg on bench and press, +5 kg on squat and deadlift. Miss the minimum on a last set and that TM drops 10% at the end of the cycle [checked: 5/3/1 Beginners rules]. FSL is 5 x 5 at the weight of your first set that day (65, 70, 75% of the TM by week): the engine cannot work that out from another slot, so the sheet tells you in words and you load it yourself. Assistance climbs by double progression.

Squat and bench appear twice a week, so the A and C versions are tracked as separate lifts, each walking its own three weeks. They start from the same first test, so they stay close.

**Deload.** No deload week: Beginners has none built in [checked]. Wendler suggests a deload or a TM test every few cycles, so the 9 week block review (three cycles) asks how the last sets went and offers one.

**Graduates to.** `strength-531-bbb-4` for more size work, or `strength-rpe-4` once you read effort well.

**Evidence: B.** A submaximal training max, an AMRAP last set as autoregulation and slow cycle by cycle increments all match the principles in research/01; there is no trial of 5/3/1 itself. The 50 to 100 assistance reps per category per session [checked, research/01] are what keep this from being a strength only plan.

**Credit.** 5/3/1 and 5/3/1 for Beginners are Jim Wendler's (*5/3/1 Forever*, jimwendler.com). This file uses the public outline only. Buy the book: it is cheap and it is the real thing.

## The data (the engine reads this block)

```json
{
  "id": "strength-531-beginners-3",
  "name": "5/3/1 for Beginners",
  "family": "strength",
  "draws_from": [
    "5/3/1 for Beginners",
    "5/3/1 Forever"
  ],
  "goals": {
    "muscle": 2,
    "strength": 3,
    "powerlifting": 2,
    "weightlifting": 0,
    "functional": 2,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 1,
    "health": 2,
    "independent": 2
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
    50,
    70
  ],
  "express_minutes": 30,
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
  "simplicity": 3,
  "graduates_to": [
    "strength-531-bbb-4",
    "strength-rpe-4"
  ],
  "block_weeks": 9,
  "deload": null,
  "meso": null,
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
  "modules": [],
  "sessions": {
    "A": {
      "title": "Squat · Bench",
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
              "reps": "5/3/1",
              "rest": 180,
              "effort": "the 5/3/1 waves of your training max; last set as many clean reps as you have",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": false,
              "inc": 5,
              "score": true
            },
            {
              "key": "bench",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 3,
              "reps": "5/3/1",
              "rest": 180,
              "effort": "the 5/3/1 waves of your training max; last set as many clean reps as you have",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": false,
              "inc": 2.5
            }
          ]
        },
        {
          "name": "First set last",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "squat_fsl",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 120,
              "effort": "5 x 5 at the first set's weight of today's squat (65, 70, 75% of the TM by week). Load it yourself",
              "rule": "fixed"
            },
            {
              "key": "bench_fsl",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 120,
              "effort": "5 x 5 at the first set's weight of today's bench (65, 70, 75% of the TM by week). Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Assistance",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "push",
              "pattern": "h_push",
              "prefer": [
                "dip",
                "push_up",
                "db_bench_press"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "pull_v",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "lat_pulldown",
                "negative_pull_up"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left, any mix of sets that reaches the reps",
              "rule": "double_progression"
            },
            {
              "key": "single_leg",
              "pattern": "lunge",
              "prefer": [
                "bulgarian_split_squat",
                "db_reverse_lunge",
                "step_up"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left, each leg",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "B": {
      "title": "Deadlift · Press",
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
              "key": "deadlift",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift"
              ],
              "sets": 3,
              "reps": "5/3/1",
              "rest": 180,
              "effort": "the 5/3/1 waves of your training max; last set as many clean reps as you have",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": false,
              "inc": 5,
              "score": true
            },
            {
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 3,
              "reps": "5/3/1",
              "rest": 180,
              "effort": "the 5/3/1 waves of your training max; last set as many clean reps as you have",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": false,
              "inc": 2.5
            }
          ]
        },
        {
          "name": "First set last",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "deadlift_fsl",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 120,
              "effort": "5 x 5 at the first set's weight of today's deadlift (65, 70, 75% of the TM by week). Load it yourself",
              "rule": "fixed"
            },
            {
              "key": "press_fsl",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 120,
              "effort": "5 x 5 at the first set's weight of today's press (65, 70, 75% of the TM by week). Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Assistance",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "push",
              "pattern": "h_push",
              "prefer": [
                "dip",
                "push_up",
                "db_bench_press"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "pull_h",
              "pattern": "h_pull",
              "prefer": [
                "inverted_row",
                "db_row",
                "barbell_row"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "core",
              "pattern": "anti_ext",
              "prefer": [
                "ab_wheel",
                "dead_bug",
                "plank"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "slow, ribs down",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "C": {
      "title": "Bench · Squat",
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
              "key": "bench_c",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 3,
              "reps": "5/3/1",
              "rest": 180,
              "effort": "the 5/3/1 waves of your training max; last set as many clean reps as you have",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": false,
              "inc": 2.5,
              "score": true
            },
            {
              "key": "squat_c",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 3,
              "reps": "5/3/1",
              "rest": 180,
              "effort": "the 5/3/1 waves of your training max; last set as many clean reps as you have",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": false,
              "inc": 5
            }
          ]
        },
        {
          "name": "First set last",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "bench_c_fsl",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 120,
              "effort": "5 x 5 at the first set's weight of today's bench (65, 70, 75% of the TM by week). Load it yourself",
              "rule": "fixed"
            },
            {
              "key": "squat_c_fsl",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 120,
              "effort": "5 x 5 at the first set's weight of today's squat (65, 70, 75% of the TM by week). Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Assistance",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "push",
              "pattern": "h_push",
              "prefer": [
                "dip",
                "push_up",
                "db_bench_press"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "pull_v",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "lat_pulldown",
                "negative_pull_up"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left, any mix of sets that reaches the reps",
              "rule": "double_progression"
            },
            {
              "key": "single_leg",
              "pattern": "lunge",
              "prefer": [
                "bulgarian_split_squat",
                "db_reverse_lunge",
                "step_up"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 left, each leg",
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
            "reps": "5/3/1",
            "rest": 180,
            "effort": "the 5/3/1 waves of your training max; last set as many clean reps as you have",
            "rule": "tm_wave",
            "tm_pct": 0.9,
            "deload_wave": false,
            "inc": 5,
            "score": true
          },
          {
            "key": "bench",
            "pattern": "h_push",
            "prefer": [
              "bench_press"
            ],
            "sets": 3,
            "reps": "5/3/1",
            "rest": 180,
            "effort": "the 5/3/1 waves of your training max; last set as many clean reps as you have",
            "rule": "tm_wave",
            "tm_pct": 0.9,
            "deload_wave": false,
            "inc": 2.5
          }
        ]
      }
    ]
  }
}
```
