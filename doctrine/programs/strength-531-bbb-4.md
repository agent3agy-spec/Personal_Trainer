# 5/3/1 Boring But Big · strength-531-bbb-4

**What it is.** The best known 5/3/1 template. One main lift a day on the 5/3/1 waves of a training max, then the big part: 5 sets of 10 of the same lift at a light weight. Then one pull. Strength from the waves, size from the 50 reps.

**Who it is for.** A novice who has finished a linear progression, up to an advanced lifter who wants a simple block of size and strength. 2 or 4 days a week, 50 to 75 minutes, a barbell, a rack, a bench and plates.

**The week.** Four sessions, one per main lift, done in order.

| session | main block (5/3/1 waves) | BBB | then |
|:-|:-|:-|:-|
| Squat | squat | squat 5 x 10 | chin-ups 4 x 8 to 12 |
| Bench | bench press | bench 5 x 10 | rows 4 x 8 to 12 |
| Deadlift | deadlift | deadlift 5 x 10 | chin-ups 4 x 8 to 12 |
| Press | overhead press | press 5 x 10 | rows 4 x 8 to 12 |

There is no 3 day week: four sessions are never squeezed into three days, so a 3 day week gets a 3 day plan. On 2 days a week two sessions carry two main lifts each, squat with bench and deadlift with press, and the 5 x 10 goes to the upper lift so the lower back is not buried.

**How it climbs.** Training max at 90% of the estimated max from your first set of 5 [checked: research/01]. Waves: 65, 75, 85% for 5, 5, 5+ · 70, 80, 90% for 3, 3, 3+ · 75, 85, 95% for 5, 3, 1+ · then a deload wave at 40, 50, 60% for 5 [believe, standard across sources]. After each four week cycle the TM goes up +2.5 kg upper and +5 kg lower; a missed minimum on a last set drops the TM 10% [checked]. BBB is 5 x 10 at 50 to 60% of the TM of the same lift; Wendler says from the third cycle you can stay at 60% [checked: jimwendler.com excerpt]. The engine does not compute it from the TM, so the sheet tells you the percentage and you load it. The pull climbs by double progression.

**Deload.** The fourth wave is the deload (40, 50, 60%), so no separate deload week. On the deload, the 5 x 10 can drop to 3 x 10 [checked].

**Graduates to.** `strength-rpe-4` for an intermediate who reads effort well, or `powerbuild-phat-5` with more days.

**Evidence: B.** Submaximal training max, an AMRAP last set as autoregulation, slow increments, and 10+ hard sets per muscle per week from the BBB work, which sits on the volume dose response (Schoenfeld 2017, Pelland) [checked, research/01]. No trial of 5/3/1 itself.

**Credit.** 5/3/1 and Boring But Big are Jim Wendler's (*5/3/1 Forever*, and the BBB article at jimwendler.com). This file uses the public outline only. Buy the book.

## The data (the engine reads this block)

```json
{
  "id": "strength-531-bbb-4",
  "name": "5/3/1 Boring But Big",
  "family": "strength",
  "draws_from": [
    "5/3/1 Boring But Big",
    "5/3/1 Forever"
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
    "intermediate",
    "advanced"
  ],
  "days": [
    2,
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
    "strength-rpe-4",
    "powerbuild-phat-5"
  ],
  "block_weeks": 4,
  "deload": null,
  "meso": null,
  "layouts": {
    "2": [
      "Squat_Bench",
      "Deadlift_Press"
    ],
    "4": [
      "Squat",
      "Bench",
      "Deadlift",
      "Press"
    ]
  },
  "modules": [
    "core"
  ],
  "sessions": {
    "Squat": {
      "title": "Squat · extra squat sets",
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
              "reps": "5/3/1",
              "rest": 210,
              "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": true,
              "inc": 5,
              "score": true
            }
          ]
        },
        {
          "name": "Extra sets, lighter",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "squat_bbb",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 5,
              "reps": "10",
              "rest": 90,
              "effort": "50 to 60% of your working weight, same lift. Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "chin",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "pull_up",
                "lat_pulldown",
                "negative_pull_up"
              ],
              "sets": 4,
              "reps": "8-12",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Bench": {
      "title": "Bench · extra bench sets",
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
                "bench_press"
              ],
              "sets": 3,
              "reps": "5/3/1",
              "rest": 210,
              "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": true,
              "inc": 2.5,
              "score": true
            }
          ]
        },
        {
          "name": "Extra sets, lighter",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "bench_bbb",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 5,
              "reps": "10",
              "rest": 90,
              "effort": "50 to 60% of your working weight, same lift. Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "db_row",
                "barbell_row",
                "inverted_row"
              ],
              "sets": 4,
              "reps": "8-12",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Deadlift": {
      "title": "Deadlift · extra deadlift sets",
      "tags": [
        "hinge_heavy"
      ],
      "blocks": [
        {
          "name": "The main lifts",
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
              "rest": 210,
              "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": true,
              "inc": 5,
              "score": true
            }
          ]
        },
        {
          "name": "Extra sets, lighter",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "deadlift_bbb",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift"
              ],
              "sets": 5,
              "reps": "10",
              "rest": 90,
              "effort": "50 to 60% of your working weight, same lift. Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "chin",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "pull_up",
                "lat_pulldown",
                "negative_pull_up"
              ],
              "sets": 4,
              "reps": "8-12",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Press": {
      "title": "Press · extra press sets",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 3,
              "reps": "5/3/1",
              "rest": 210,
              "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": true,
              "inc": 2.5,
              "score": true
            }
          ]
        },
        {
          "name": "Extra sets, lighter",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "press_bbb",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 5,
              "reps": "10",
              "rest": 90,
              "effort": "50 to 60% of your working weight, same lift. Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "db_row",
                "barbell_row",
                "inverted_row"
              ],
              "sets": 4,
              "reps": "8-12",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Squat_Bench": {
      "title": "Squat · Bench · extra bench sets",
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
              "reps": "5/3/1",
              "rest": 210,
              "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": true,
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
              "rest": 210,
              "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": true,
              "inc": 2.5
            }
          ]
        },
        {
          "name": "Extra sets, lighter",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "bench_bbb",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 5,
              "reps": "10",
              "rest": 90,
              "effort": "50 to 60% of your working weight, same lift. Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "chin",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "pull_up",
                "lat_pulldown",
                "negative_pull_up"
              ],
              "sets": 4,
              "reps": "8-12",
              "rest": 75,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Deadlift_Press": {
      "title": "Deadlift · Press · extra press sets",
      "tags": [
        "hinge_heavy"
      ],
      "blocks": [
        {
          "name": "The main lifts",
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
              "rest": 210,
              "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": true,
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
              "rest": 210,
              "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
              "rule": "tm_wave",
              "tm_pct": 0.9,
              "deload_wave": true,
              "inc": 2.5
            }
          ]
        },
        {
          "name": "Extra sets, lighter",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "press_bbb",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 5,
              "reps": "10",
              "rest": 90,
              "effort": "50 to 60% of your working weight, same lift. Load it yourself",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "db_row",
                "barbell_row",
                "inverted_row"
              ],
              "sets": 4,
              "reps": "8-12",
              "rest": 75,
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
            "reps": "5/3/1",
            "rest": 210,
            "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
            "rule": "tm_wave",
            "tm_pct": 0.9,
            "deload_wave": true,
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
            "rest": 210,
            "effort": "3 sets, each heavier; on the last, as many clean reps as you can",
            "rule": "tm_wave",
            "tm_pct": 0.9,
            "deload_wave": true,
            "inc": 2.5
          }
        ]
      }
    ]
  }
}
```
