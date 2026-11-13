# Novice linear progression · strength-lp-3

**What it is.** The classic way a beginner gets strong fast: three full-body barbell sessions a week, the same few big lifts, a little more weight every session while it keeps going up. Two sessions, A and B, alternate.

**Who it is for.** Never lifted, or under six months in. Wants to get stronger first. Has a barbell, a rack, a bench and plates. 2 or 3 days a week, 45 to 75 minutes (rests are long on purpose).

**The week.** A, B, A, then B, A, B the week after. Never two days in a row if you can help it.

| session | main block | then |
|:-|:-|:-|
| A | squat 5 x 5 · bench press 5 x 5 | barbell row 5 x 5 · a core finisher |
| B | squat 5 x 5 · overhead press 5 x 5 | deadlift 1 x 5 · chin-ups or pulldowns 3 x 6 to 10 |

**How it climbs.** Every set done at the written reps: next time +2.5 kg on the upper lifts and +5 kg on squat and deadlift (+2.5 kg on the deadlift past 100 kg). A miss: same weight next time. Three misses in a row on a lift: that lift drops 10% and climbs again. [checked: StrongLifts support docs, research/01]

**Deload.** None scheduled: the 10% reset is the deload, per lift. After 6 weeks the block review asks whether progress has slowed (two resets on the same lift), and if so it offers the next program.

**Graduates to.** `strength-531-beginners-3` or `strength-gzclp-4`, when session-to-session gains stop on two lifts.

**Evidence: B to C.** Fast novice progress on a linear plan is well established in practice; the program itself has no trial, and its low volume is weak for muscle compared with the volume research. That is why session B carries a pull-up slot and A a core finisher. [research/01]

**Credit.** Built from the public rules of StrongLifts 5x5 (stronglifts.com) and Starting Strength (Mark Rippetoe, startingstrength.com). Buy the book if you want the full coaching.

## The data (the engine reads this block)

```json
{
  "id": "strength-lp-3",
  "name": "Novice linear progression",
  "family": "strength",
  "draws_from": [
    "StrongLifts 5x5",
    "Starting Strength",
    "ACSM 2009"
  ],
  "goals": {
    "muscle": 2,
    "strength": 3,
    "powerlifting": 2,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 1,
    "health": 2,
    "independent": 1
  },
  "experience": [
    "none",
    "novice"
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
  "simplicity": 1,
  "graduates_to": [
    "strength-531-beginners-3",
    "strength-gzclp-4"
  ],
  "block_weeks": 6,
  "deload": null,
  "meso": null,
  "layouts": {
    "2": [
      "A",
      "B"
    ],
    "3": [
      "A",
      "B"
    ]
  },
  "modules": [
    "core"
  ],
  "sessions": {
    "A": {
      "title": "Squat · Bench · Row",
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
              "sets": 5,
              "reps": "5",
              "rest": 180,
              "effort": "every rep clean, 1 or 2 reps spare",
              "rule": "linear_session",
              "inc": 5,
              "score": true
            },
            {
              "key": "bench",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 180,
              "effort": "every rep clean, 1 or 2 reps spare",
              "rule": "linear_session",
              "inc": 2.5
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
                "barbell_row",
                "db_row"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 120,
              "effort": "1 or 2 reps spare",
              "rule": "linear_session",
              "inc": 2.5
            }
          ]
        }
      ]
    },
    "B": {
      "title": "Squat · Press · Deadlift",
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
                "back_squat"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 180,
              "effort": "every rep clean, 1 or 2 reps spare",
              "rule": "linear_session",
              "inc": 5,
              "score": true
            },
            {
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 180,
              "effort": "every rep clean, 1 or 2 reps spare",
              "rule": "linear_session",
              "inc": 2.5
            }
          ]
        },
        {
          "name": "Second exercise",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "deadlift",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift"
              ],
              "sets": 1,
              "reps": "5",
              "rest": 180,
              "effort": "1 or 2 reps spare, flat back",
              "rule": "linear_session",
              "inc": 5,
              "inc_after_100": 2.5
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "vpull",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "lat_pulldown",
                "negative_pull_up"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 90,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Short version · Squat · Press or Bench",
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
            "reps": "5",
            "rest": 150,
            "effort": "every rep clean, 1 or 2 reps spare",
            "rule": "linear_session",
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
            "reps": "5",
            "rest": 150,
            "effort": "1 or 2 reps spare",
            "rule": "linear_session",
            "inc": 2.5
          }
        ]
      }
    ]
  }
}
```
