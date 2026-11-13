# Health baseline · health-baseline-2to3

**What it is.** The start-here plan: the public health dose, made into gentle gym sessions. Two or three full body strength sessions a week with a few big movements, plus a brisk walk or easy cardio that grows towards 150 minutes a week. Nothing fancy, and that is the point: this is what the World Health Organization and the American College of Sports Medicine say an adult needs.

**Who it is for.** A first-timer in a gym, or someone coming back after a long break or short on time. It runs on machines, dumbbells or a home gym, and every slot has a seated version, so it is also the plan for training seated and, once their provider says yes, during pregnancy. It is not a bodyweight-only home plan. 2 or 3 days a week, 20 to 60 minutes.

**The numbers it is built on.**

- Adults: 150 to 300 minutes a week of moderate activity, or 75 to 150 vigorous, plus muscle strengthening on 2 or more days for all major muscle groups [checked: WHO 2020, Bull et al., BJSM]. Less sitting, too.
- Beginners: full body, 2 to 3 non consecutive days, 4 to 6 multi joint exercises, 1 to 3 sets of 8 to 12 [checked: ACSM 2009 position stand].
- Progress: add 2 to 10% load when you beat the target by 1 to 2 reps [checked: ACSM 2009].

**The week.** A and B alternate, never two days in a row if you can help it.

| session | strength, 2 sets of 8 to 12 | then |
|:-|:-|:-|
| A | chest press · row · squat · hip hinge · anti-rotation | brisk walk or easy cardio, starts at 15 min |
| B | shoulder press · pulldown · step-up or lunge · bridge or deadlift · trunk hold | brisk walk or easy cardio |

The walks in the sessions are the start. The 150 minutes a week is reached with walks on the other days too, and any bout counts [believe: UK CMO coverage].

**How it climbs.** Double progression: when every set reaches 12 reps, the weight goes up one step (2 to 10%) and you start again at 8. With fixed weights at home, the sheet gives you the harder variant instead. The cardio holds about 3 weeks, then adds about 10%, up to 40 minutes a session.

**Deload.** None scheduled: the loads are moderate and the rule is gentle. After 8 weeks the block review asks how it is going and offers the next step.

**Pregnancy.** This is also the program used in pregnancy, once the person's obstetric provider has said yes [checked: ACOG Committee Opinion 804, 2020]. The aim is the same 150 minutes of moderate activity plus strength work [checked: WHO 2020]. The engine enforces the pregnancy overrides on top of this file: no lying on the back after the first trimester, no impact, no maximal efforts, and it stops the session on any ACOG warning sign (bleeding, fluid leak, regular painful contractions, chest pain, dizziness, headache, unusual breathlessness) [checked partially, research/04].

**Graduates to.** `strength-lp-3` for strength, `muscle-fullbody-3` for muscle, `functional-gpp-3to5` for broad fitness.

**Evidence: A.** International guidelines and a position stand, built on large bodies of trials [checked].

**Credit.** WHO 2020 guidelines on physical activity and sedentary behaviour (who.int, free). ACSM 2009 position stand, Progression models in resistance training, Med Sci Sports Exerc 41(3). Note: a 2026 ACSM update exists and supersedes the 2009 stand; its numbers still need reading [checked that it exists].

## The data (the engine reads this block)

```json
{
  "id": "health-baseline-2to3",
  "name": "Health baseline",
  "family": "health",
  "draws_from": [
    "WHO 2020",
    "ACSM 2009",
    "UK CMO 2019",
    "ACOG 804"
  ],
  "goals": {
    "muscle": 1,
    "strength": 1,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 2,
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
    20,
    60
  ],
  "express_minutes": 15,
  "equipment_all": [],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [],
  "evidence": "A",
  "simplicity": 2,
  "graduates_to": [
    "strength-lp-3",
    "muscle-fullbody-3",
    "functional-gpp-3to5"
  ],
  "block_weeks": 8,
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
    "mobility"
  ],
  "sessions": {
    "A": {
      "title": "Press · Row · Squat · Hinge",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "superset",
          "rest_after_round": 90,
          "slots": [
            {
              "key": "hpush",
              "pattern": "h_push",
              "prefer": [
                "db_bench_press",
                "chest_press_machine",
                "incline_push_up",
                "wall_push_up",
                "seated_band_chest_press"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 60,
              "effort": "2 or 3 left, smooth reps",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "hpull",
              "pattern": "h_pull",
              "prefer": [
                "seated_cable_row",
                "machine_row",
                "db_row",
                "band_row",
                "seated_band_row"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 60,
              "effort": "2 or 3 left, squeeze the shoulder blades",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Legs and hips",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "squat",
              "pattern": "squat",
              "prefer": [
                "goblet_squat",
                "leg_press",
                "sit_to_stand",
                "box_squat",
                "bodyweight_squat"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "2 or 3 left",
              "rule": "double_progression"
            },
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
              "effort": "2 or 3 left, flat back",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Trunk",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "antirot",
              "pattern": "anti_rot",
              "prefer": [
                "pallof_press",
                "band_pallof_press",
                "seated_band_rotation"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 45,
              "effort": "slow, no twist",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Brisk walk or easy cardio",
          "kind": "secondary",
          "format": "run",
          "slots": [
            {
              "key": "cardio",
              "pattern": "cyclic",
              "prefer": [
                "walk",
                "incline_walk",
                "bike_erg",
                "row_erg",
                "arm_ergometer"
              ],
              "sets": 1,
              "reps": "15 min",
              "rest": 0,
              "effort": "brisk: you can talk, not sing",
              "rule": "run_volume",
              "start_minutes": 15,
              "per_week": 2,
              "max_minutes": 40
            }
          ]
        }
      ]
    },
    "B": {
      "title": "Press up · Pull down · Lunge · Bridge",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "superset",
          "rest_after_round": 90,
          "slots": [
            {
              "key": "vpush",
              "pattern": "v_push",
              "prefer": [
                "db_shoulder_press",
                "seated_db_press",
                "landmine_press",
                "band_overhead_press"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 60,
              "effort": "2 or 3 left, ribs down",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "vpull",
              "pattern": "v_pull",
              "prefer": [
                "lat_pulldown",
                "band_lat_pulldown",
                "single_arm_cable_pulldown",
                "assisted_pull_up"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 60,
              "effort": "2 or 3 left, elbows to the ribs",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Legs and hips",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "lunge",
              "pattern": "lunge",
              "prefer": [
                "step_up",
                "db_reverse_lunge",
                "reverse_lunge",
                "lateral_lunge"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "2 or 3 left, each leg, hold something for balance if you need",
              "rule": "double_progression"
            },
            {
              "key": "bridge",
              "pattern": "hinge",
              "prefer": [
                "hip_thrust",
                "glute_bridge",
                "kb_deadlift",
                "band_good_morning"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "2 or 3 left, pause at the top",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Trunk",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "antiext",
              "pattern": "anti_ext",
              "prefer": [
                "dead_bug",
                "bird_dog",
                "plank"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 45,
              "effort": "slow, low back stays still",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Brisk walk or easy cardio",
          "kind": "secondary",
          "format": "run",
          "slots": [
            {
              "key": "cardio",
              "pattern": "cyclic",
              "prefer": [
                "walk",
                "incline_walk",
                "bike_erg",
                "row_erg",
                "arm_ergometer"
              ],
              "sets": 1,
              "reps": "15 min",
              "rest": 0,
              "effort": "brisk: you can talk, not sing",
              "rule": "run_volume",
              "start_minutes": 15,
              "per_week": 2,
              "max_minutes": 40
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · Press · Row · Squat · Walk",
    "tags": [],
    "blocks": [
      {
        "name": "Main block",
        "kind": "main",
        "format": "superset",
        "rest_after_round": 60,
        "slots": [
          {
            "key": "hpush",
            "pattern": "h_push",
            "prefer": [
              "db_bench_press",
              "chest_press_machine",
              "incline_push_up",
              "wall_push_up",
              "seated_band_chest_press"
            ],
            "sets": 2,
            "reps": "8-12",
            "rest": 45,
            "effort": "2 or 3 left",
            "rule": "double_progression",
            "score": true
          },
          {
            "key": "hpull",
            "pattern": "h_pull",
            "prefer": [
              "seated_cable_row",
              "machine_row",
              "db_row",
              "band_row",
              "seated_band_row"
            ],
            "sets": 2,
            "reps": "8-12",
            "rest": 45,
            "effort": "2 or 3 left",
            "rule": "double_progression"
          }
        ]
      },
      {
        "name": "Legs",
        "kind": "secondary",
        "format": "straight",
        "slots": [
          {
            "key": "squat",
            "pattern": "squat",
            "prefer": [
              "goblet_squat",
              "leg_press",
              "sit_to_stand",
              "box_squat",
              "bodyweight_squat"
            ],
            "sets": 2,
            "reps": "8-12",
            "rest": 60,
            "effort": "2 or 3 left",
            "rule": "double_progression"
          }
        ]
      },
      {
        "name": "Brisk walk",
        "kind": "finisher",
        "format": "run",
        "slots": [
          {
            "key": "walk_express",
            "pattern": "cyclic",
            "prefer": [
              "walk",
              "incline_walk",
              "bike_erg",
              "arm_ergometer"
            ],
            "sets": 1,
            "reps": "5 min",
            "rest": 0,
            "effort": "brisk: you can talk, not sing",
            "rule": "fixed"
          }
        ]
      }
    ]
  }
}
```
