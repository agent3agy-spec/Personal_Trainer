# Texas Method · strength-texas-3

**What it is.** The step after a novice linear progression stops working session to session. The week becomes the unit: one hard volume day that tires you, one light day that keeps you moving, one intensity day where you set a new 5 rep max. Three sessions, always in that order.

**Who it is for.** Post-novice. You ran a linear progression until it stalled twice, you want to keep getting stronger on the barbell, and you have 3 days a week, 60 to 90 minutes, a barbell, a rack, a bench and plates.

**The week.** Volume, Recovery, Intensity. Ideally Monday, Wednesday, Friday, with a rest day after each.

| session | main block | then |
|:-|:-|:-|
| Volume | squat 5 x 5 at about 90% of the intensity day 5RM · bench press 5 x 5 | chin-ups 3 x 5 to 8 |
| Recovery | light squat 2 x 5 at about 80% of the volume day weight · overhead press 3 x 5 | back extension 2 x 10 to 15 |
| Intensity | squat 1 x 5, a new 5RM · bench press 1 x 5 · deadlift 1 x 5 | barbell row 3 x 5 to 8 |

**How it climbs.** Once a week, not once a session. The intensity day is the score: a new 5RM on the squat each Friday, +2.5 kg when all five reps went up. The volume day squat is tracked as its own lift and climbs by +2.5 kg too, so it stays near 90% of the Friday number. The structure is [checked: startingstrength.com, research/01]. The 90% volume load and the 80% recovery load are [believe]: the sources agree on the shape, not on the exact percentages. The recovery squat does not progress on its own: it follows whatever Monday is.

**Deload.** None scheduled. Three missed weeks in a row on a lift drop that lift 10% and it climbs again. The 6 week block review asks whether Friday PRs have stopped on two lifts, and offers the next program.

**Graduates to.** `strength-531-bbb-4` or `strength-rpe-4`, when the intensity day stops moving for a few weeks even after a reset.

**Evidence: B to C.** The weekly stress, recover, express shape fits what is known about intermediate lifters needing more than one session to recover from a hard stimulus. The program itself has no trial, and startingstrength.com itself argues the Texas Method is not the best next step for most people finishing a linear progression [checked, sources conflict, research/01]. The low arm and upper back volume is why chin-ups and rows sit at the end.

**Credit.** The Texas Method comes from the Starting Strength school (Mark Rippetoe and Glenn Pendlay, described in *Practical Programming for Strength Training*, startingstrength.com). This file only uses its public outline. Buy the book for the full method and the coaching.

## The data (the engine reads this block)

```json
{
  "id": "strength-texas-3",
  "name": "Texas Method",
  "family": "strength",
  "draws_from": [
    "Texas Method",
    "Practical Programming for Strength Training"
  ],
  "goals": {
    "muscle": 1,
    "strength": 3,
    "powerlifting": 3,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 1,
    "health": 1,
    "independent": 1
  },
  "experience": [
    "intermediate"
  ],
  "days": [
    3,
    3
  ],
  "sweet_days": [
    3
  ],
  "minutes": [
    60,
    90
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
  "simplicity": 1,
  "graduates_to": [
    "strength-531-bbb-4",
    "strength-rpe-4"
  ],
  "block_weeks": 6,
  "deload": null,
  "meso": null,
  "layouts": {
    "3": [
      "Volume",
      "Recovery",
      "Intensity"
    ]
  },
  "modules": [],
  "sessions": {
    "Volume": {
      "title": "Hard day · Squat · Bench",
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
              "key": "squat_volume",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 240,
              "effort": "about 90% of your Friday best for 5, all 25 reps clean",
              "rule": "linear_session",
              "inc": 2.5,
              "score": true
            },
            {
              "key": "bench_volume",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 5,
              "reps": "5",
              "rest": 180,
              "effort": "every rep clean, 1 rep spare",
              "rule": "linear_session",
              "inc": 2.5
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
                "lat_pulldown",
                "negative_pull_up"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 90,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Recovery": {
      "title": "Easy day · Light squat · Press",
      "tags": [],
      "blocks": [
        {
          "name": "The main lifts",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat_light",
              "pattern": "squat",
              "prefer": [
                "back_squat",
                "front_squat"
              ],
              "sets": 2,
              "reps": "5",
              "rest": 150,
              "effort": "about 80% of Monday's weight, fast and easy: this day recovers you, it does not test you",
              "rule": "fixed"
            },
            {
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "overhead_press"
              ],
              "sets": 3,
              "reps": "5",
              "rest": 180,
              "effort": "every rep clean, 1 or 2 reps spare",
              "rule": "linear_session",
              "inc": 2.5,
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
              "key": "backext",
              "pattern": "hinge",
              "prefer": [
                "back_extension",
                "db_romanian_deadlift",
                "glute_bridge"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 75,
              "effort": "2 or 3 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Intensity": {
      "title": "Test day · Squat, a new best for 5 · Bench · Deadlift",
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
              "sets": 1,
              "reps": "5",
              "rest": 240,
              "effort": "work up to one set of 5, a new best for 5, every rep clean",
              "rule": "linear_session",
              "inc": 2.5,
              "score": true
            },
            {
              "key": "bench",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 1,
              "reps": "5",
              "rest": 240,
              "effort": "one set of 5, a new best for 5",
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
              "rest": 240,
              "effort": "one set of 5, flat back",
              "rule": "linear_session",
              "inc": 2.5
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
                "barbell_row",
                "pendlay_row",
                "db_row"
              ],
              "sets": 3,
              "reps": "5-8",
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
    "title": "Short version · Squat, a new best for 5 · Bench",
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
            "sets": 1,
            "reps": "5",
            "rest": 210,
            "effort": "one set of 5, a new best for 5",
            "rule": "linear_session",
            "inc": 2.5,
            "score": true
          },
          {
            "key": "bench",
            "pattern": "h_push",
            "prefer": [
              "bench_press"
            ],
            "sets": 1,
            "reps": "5",
            "rest": 180,
            "effort": "one set of 5",
            "rule": "linear_session",
            "inc": 2.5
          }
        ]
      }
    ]
  }
}
```
