# Older and strong · older-strong-3

**What it is.** The WHO multicomponent week for people over 60: strength, a little power and balance, in every session. Getting up from a chair, carrying the shopping, catching yourself when you trip. Each session opens with a short balance block, then four or five strength moves where you lift fast and lower slow.

**Who it is for.** 60 and over, any experience, at home or in a gym. Dumbbells, a band or a chair is enough to start. 2 or 3 days a week, 30 to 60 minutes.

**Why it is built like this.**

- Older adults: varied multicomponent activity that emphasises functional balance and strength, at moderate or greater intensity, 3 or more days a week, to improve function and prevent falls. That was the new part of the 2020 guidelines, and it applies with chronic conditions or disability too [checked: WHO 2020].
- Exercise cuts the rate of falls by 23% (rate ratio 0.77, 59 trials, 12,981 people, high certainty); balance plus functional plus resistance work did best, about 34% lower [checked: Sherrington 2019, Cochrane].
- Fast lifting at light to moderate loads builds power as well as heavy loads do, and power tracks daily function better than strength [checked, research/04]. That is the "lift fast, lower slow" on every lift.
- Resistance training is recommended for every older adult, not only those who have lost muscle [checked: ICFSR 2021].

**The week.** A, B, C in order, round and round, a rest day between when you can.

| session | balance, about 6 min | strength, 2 to 3 sets of 8 to 12 |
|:-|:-|:-|
| A | single leg stand · heel to toe walk · clock reach | sit to stand · incline push-up · row · farmer carry |
| B | tandem stance · step over · clock reach | goblet squat · shoulder press · pulldown · hip hinge · calf raise |
| C | single leg stand · heel to toe walk · floor get-up | step-up · incline push-up · row · suitcase carry |

Balance work is next to something solid you can grab. The sheet also adds the `balance` module: from 60 it is mandatory, never cut.

**How it climbs.** Double progression: every set at 12 reps, then one step heavier and back to 8. With fixed weights the sheet gives you the harder variant (a lower step, a lower incline). Balance holds do not progress by rule: you make them harder yourself (eyes closed, softer surface) only when steady.

**Deload.** None scheduled, the loads are moderate. After 8 weeks the block review checks in.

**Two things this program does not do.** Heavy lifting for low bone density: the LIFTMOR trial got bone gains with 5 x 5 above 85% of max, but **supervised** and progressed from a low start [checked: Watson 2018]. Take that to a physiotherapist or a qualified coach, never alone. And if you have fallen, or are afraid of falling, ask your doctor for a falls programme led by a health professional: those did better than ones led by fitness leaders (rate ratio 0.69 vs 0.82) [checked: Sherrington 2019].

**Graduates to.** Nothing by force. Keep going: strength fades without it.

**Evidence: A.** Guidelines and a high certainty Cochrane review [checked].

**Credit.** WHO 2020 guidelines on physical activity and sedentary behaviour (who.int, free). Sherrington et al. 2019, Cochrane review CD012424. UK Chief Medical Officers' guidelines 2019.

## The data (the engine reads this block)

```json
{
  "id": "older-strong-3",
  "name": "Older and strong",
  "family": "older",
  "draws_from": [
    "WHO 2020",
    "Sherrington 2019 Cochrane",
    "ICFSR 2021",
    "ACSM 2009",
    "UK CMO 2019"
  ],
  "goals": {
    "muscle": 1,
    "strength": 2,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 2,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 1,
    "health": 3,
    "independent": 3
  },
  "experience": [
    "none",
    "novice",
    "intermediate",
    "advanced"
  ],
  "days": [
    2,
    3
  ],
  "sweet_days": [
    3
  ],
  "minutes": [
    30,
    60
  ],
  "express_minutes": 20,
  "equipment_all": [],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [
    "under_60"
  ],
  "evidence": "A",
  "simplicity": 2,
  "graduates_to": [],
  "block_weeks": 8,
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
  "modules": [
    "balance"
  ],
  "sessions": {
    "A": {
      "title": "Balance · Sit to stand · Push · Row · Carry",
      "tags": [],
      "blocks": [
        {
          "name": "Balance",
          "kind": "main",
          "format": "circuit",
          "minutes": 6,
          "slots": [
            {
              "key": "bal_stand",
              "pattern": "balance",
              "prefer": [
                "single_leg_stand",
                "tandem_stance"
              ],
              "sets": 2,
              "reps": "30 s",
              "rest": 20,
              "effort": "each leg, next to something solid you can grab",
              "rule": "fixed"
            },
            {
              "key": "bal_walk",
              "pattern": "balance",
              "prefer": [
                "heel_to_toe_walk",
                "tandem_stance"
              ],
              "sets": 2,
              "reps": "10 steps",
              "rest": 20,
              "effort": "slow, eyes ahead, along a wall",
              "rule": "fixed"
            },
            {
              "key": "bal_reach",
              "pattern": "balance",
              "prefer": [
                "clock_reach",
                "single_leg_stand"
              ],
              "sets": 2,
              "reps": "5",
              "rest": 20,
              "effort": "each leg, reach only as far as you stay steady",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Strength",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "sts",
              "pattern": "squat",
              "prefer": [
                "sit_to_stand",
                "box_squat",
                "goblet_squat"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 90,
              "effort": "lift fast, lower slow: stand up quickly, sit down over 3 s. 2 or 3 left",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "hpush",
              "pattern": "h_push",
              "prefer": [
                "incline_push_up",
                "wall_push_up",
                "db_bench_press",
                "chest_press_machine",
                "seated_band_chest_press"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "lift fast, lower slow. 2 or 3 left",
              "rule": "double_progression"
            },
            {
              "key": "hpull",
              "pattern": "h_pull",
              "prefer": [
                "seated_cable_row",
                "db_row",
                "band_row",
                "seated_band_row"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "lift fast, lower slow. 2 or 3 left",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Carry",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "farmer",
              "pattern": "carry",
              "prefer": [
                "farmer_carry",
                "suitcase_carry"
              ],
              "sets": 2,
              "reps": "20-40 m",
              "rest": 60,
              "effort": "tall and steady, a weight you could carry a bit further",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "B": {
      "title": "Balance · Squat · Press · Pulldown · Hinge",
      "tags": [],
      "blocks": [
        {
          "name": "Balance",
          "kind": "main",
          "format": "circuit",
          "minutes": 6,
          "slots": [
            {
              "key": "bal_tandem",
              "pattern": "balance",
              "prefer": [
                "tandem_stance",
                "single_leg_stand"
              ],
              "sets": 2,
              "reps": "30 s",
              "rest": 20,
              "effort": "each foot in front, next to something solid",
              "rule": "fixed"
            },
            {
              "key": "bal_stepover",
              "pattern": "balance",
              "prefer": [
                "step_over",
                "heel_to_toe_walk"
              ],
              "sets": 2,
              "reps": "8",
              "rest": 20,
              "effort": "each leg, a low object, lift the knee",
              "rule": "fixed"
            },
            {
              "key": "bal_reach",
              "pattern": "balance",
              "prefer": [
                "clock_reach",
                "single_leg_stand"
              ],
              "sets": 2,
              "reps": "5",
              "rest": 20,
              "effort": "each leg, reach only as far as you stay steady",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Strength",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat",
              "pattern": "squat",
              "prefer": [
                "goblet_squat",
                "box_squat",
                "leg_press",
                "sit_to_stand"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 90,
              "effort": "lift fast, lower slow. 2 or 3 left",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "vpush",
              "pattern": "v_push",
              "prefer": [
                "seated_db_press",
                "db_shoulder_press",
                "band_overhead_press"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "lift fast, lower slow. 2 or 3 left",
              "rule": "double_progression"
            },
            {
              "key": "vpull",
              "pattern": "v_pull",
              "prefer": [
                "lat_pulldown",
                "band_lat_pulldown",
                "single_arm_cable_pulldown"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "lift fast, lower slow. 2 or 3 left",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Hips and calves",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "hinge",
              "pattern": "hinge",
              "prefer": [
                "db_romanian_deadlift",
                "kb_deadlift",
                "hip_hinge_drill",
                "glute_bridge"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "flat back, 2 or 3 left",
              "rule": "double_progression"
            },
            {
              "key": "calves",
              "pattern": "calves",
              "prefer": [
                "calf_raise",
                "seated_calf_raise"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "up fast, down slow, hold a support",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "C": {
      "title": "Balance · Step-up · Push · Row · Carry",
      "tags": [],
      "blocks": [
        {
          "name": "Balance",
          "kind": "main",
          "format": "circuit",
          "minutes": 6,
          "slots": [
            {
              "key": "bal_stand",
              "pattern": "balance",
              "prefer": [
                "single_leg_stand",
                "tandem_stance"
              ],
              "sets": 2,
              "reps": "30 s",
              "rest": 20,
              "effort": "each leg, next to something solid you can grab",
              "rule": "fixed"
            },
            {
              "key": "bal_walk",
              "pattern": "balance",
              "prefer": [
                "heel_to_toe_walk",
                "tandem_stance"
              ],
              "sets": 2,
              "reps": "10 steps",
              "rest": 20,
              "effort": "slow, eyes ahead, along a wall",
              "rule": "fixed"
            },
            {
              "key": "bal_getup",
              "pattern": "balance",
              "prefer": [
                "floor_get_up",
                "step_over"
              ],
              "sets": 2,
              "reps": "2",
              "rest": 30,
              "effort": "down to the floor and back up, any way that works, a chair beside you",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Strength",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "stepup",
              "pattern": "lunge",
              "prefer": [
                "step_up",
                "reverse_lunge",
                "db_reverse_lunge"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 90,
              "effort": "each leg, step up fast, lower slow, hold a rail. 2 or 3 left",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "hpush",
              "pattern": "h_push",
              "prefer": [
                "incline_push_up",
                "wall_push_up",
                "db_bench_press",
                "chest_press_machine",
                "seated_band_chest_press"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "lift fast, lower slow. 2 or 3 left",
              "rule": "double_progression"
            },
            {
              "key": "hpull",
              "pattern": "h_pull",
              "prefer": [
                "seated_cable_row",
                "db_row",
                "band_row",
                "seated_band_row"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "lift fast, lower slow. 2 or 3 left",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Carry",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "suitcase",
              "pattern": "carry",
              "prefer": [
                "suitcase_carry",
                "farmer_carry"
              ],
              "sets": 2,
              "reps": "20-40 m",
              "rest": 60,
              "effort": "one hand, each side, do not lean",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · Balance · Sit to stand · Push · Row",
    "tags": [],
    "blocks": [
      {
        "name": "Balance",
        "kind": "main",
        "format": "circuit",
        "minutes": 4,
        "slots": [
          {
            "key": "bal_stand",
            "pattern": "balance",
            "prefer": [
              "single_leg_stand",
              "tandem_stance"
            ],
            "sets": 2,
            "reps": "30 s",
            "rest": 20,
            "effort": "each leg, next to something solid you can grab",
            "rule": "fixed"
          },
          {
            "key": "bal_walk",
            "pattern": "balance",
            "prefer": [
              "heel_to_toe_walk",
              "tandem_stance"
            ],
            "sets": 2,
            "reps": "10 steps",
            "rest": 20,
            "effort": "slow, eyes ahead, along a wall",
            "rule": "fixed"
          }
        ]
      },
      {
        "name": "Strength",
        "kind": "main",
        "format": "straight",
        "slots": [
          {
            "key": "sts",
            "pattern": "squat",
            "prefer": [
              "sit_to_stand",
              "box_squat",
              "goblet_squat"
            ],
            "sets": 2,
            "reps": "8-12",
            "rest": 60,
            "effort": "lift fast, lower slow. 2 or 3 left",
            "rule": "double_progression",
            "score": true
          },
          {
            "key": "hpush",
            "pattern": "h_push",
            "prefer": [
              "incline_push_up",
              "wall_push_up",
              "db_bench_press",
              "chest_press_machine",
              "seated_band_chest_press"
            ],
            "sets": 2,
            "reps": "8-12",
            "rest": 60,
            "effort": "lift fast, lower slow. 2 or 3 left",
            "rule": "double_progression"
          },
          {
            "key": "hpull",
            "pattern": "h_pull",
            "prefer": [
              "seated_cable_row",
              "db_row",
              "band_row",
              "seated_band_row"
            ],
            "sets": 2,
            "reps": "8-12",
            "rest": 60,
            "effort": "lift fast, lower slow. 2 or 3 left",
            "rule": "double_progression"
          }
        ]
      }
    ]
  }
}
```
