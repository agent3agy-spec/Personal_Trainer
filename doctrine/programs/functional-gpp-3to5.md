# Functional fitness, general physical preparedness · functional-gpp-3to5

**What it is.** CrossFit-style general fitness, run on a normal week. Every session is two parts: one lift or one skill done fresh, then a short timed workout (a metcon) that mixes the three modalities CrossFit names: M for cardio machines and running, G for bodyweight and gymnastics, W for weights. Some days are one modality, some two, some three. You get fit across short, middle and long efforts instead of one thing.

**Who it is for.** Novice to advanced. Wants to be good at a bit of everything, likes a clock and a score. Has at least kettlebells, dumbbells or a barbell. 3 to 5 days a week, 45 to 60 minutes.

**The week.** Five sessions, A to E, done in order whatever your days a week: on 3 days you go round the five in under two weeks, on 5 days you do the full lap every week. CrossFit's own 2003 template runs 3 days on and 1 off, and the article itself admits that does not fit a gym's 5 on 2 off week [snippet: CrossFit Journal, Theoretical Template, Feb 2003], so here the single, double and triple modality days rotate inside a normal week instead.

| session | lift or skill, fresh | then the metcon |
|:-|:-|:-|
| A | squat 5 x 3 to 5 | 12 min AMRAP, a couplet (two modalities) |
| B | overhead press 5 x 3 to 5 | 3 rounds for time, 12 min cap, a triplet (three modalities) |
| C | deadlift 3 x 3 to 5 | 12 min EMOM, one modality |
| D | bench or push-up 5 x 3 to 5 | 16 min AMRAP, a triplet |
| E | hang power clean, light and fast, 5 x 2 to 3 | a chipper for time, 14 min cap |

Each metcon has four versions that rotate one per outing, so you meet the same piece again about every four weeks and can beat it.

**Scaling.** Every metcon is written to be scaled, never skipped. The order is load first, then reps, then the movement, so the piece still feels the way it is meant to (fast stays fast, long stays long) [snippet: Rx, Scaled and Foundations explainers, research/02]. The sheet prints this on every piece.

**How it climbs.** The lift: double progression. Hit the top of the rep range on every set and the weight goes up next time, otherwise add a rep. The metcon: a benchmark. Your best on each version is stored and the sheet asks you to beat it. Benchmarks only count if the movement standards stay the same between attempts [snippet: RitFit, research/02].

**Deload.** After 8 weeks, a lighter week: half the sets, 90% of the load, 4 reps left in the tank. Retesting benchmarks every 8 to 12 weeks is the usual CrossFit habit [believe].

**Safety.** Novices: no high-skill move under fatigue. No Olympic lift from the floor and no kipping inside a metcon until the move is stable fresh; that is why the clean lives in the fresh block of session E and the metcons use swings, thrusters and dumbbells. CrossFit-style training gets hurt at about 2 to 4 injuries per 1000 hours, in the same range as weight training and running, mostly shoulders then low back [snippet: Hak 2013, Montalvo 2017, Klimek 2018; region order believe]. Tell the trainer about any shoulder or back history.

**Graduates to.** `hyrox-prep-4` when you want a race, `hybrid-strength-endurance-4to6` when you want to lift heavier and run further.

**Evidence: C.** The fitness model is coach consensus; whether constant variation beats planned periodisation has no trial behind it [believe]. The injury numbers are observational [snippet].

**Credit.** The method is CrossFit's: Greg Glassman, "What Is Fitness?", CrossFit Journal, October 2002, and the theoretical template of February 2003 (crossfit.com). If you want daily coached programming, the paid options are CompTrain (Ben Bergeron), Mayhem Athlete (Rich Froning), PRVN (Shane Orr), HWPO (Mat Fraser) and Invictus (CJ Martin). None of their workouts is copied here, and their prices change, so check their sites.

## The data (the engine reads this block)

```json
{
  "id": "functional-gpp-3to5",
  "name": "Functional fitness, general preparedness",
  "family": "functional",
  "draws_from": [
    "CrossFit, What Is Fitness 2002",
    "CrossFit theoretical template 2003",
    "ACSM 2009"
  ],
  "goals": {
    "muscle": 1,
    "strength": 2,
    "powerlifting": 0,
    "weightlifting": 1,
    "functional": 3,
    "hyrox": 2,
    "run": 1,
    "skills": 1,
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
    3,
    5
  ],
  "sweet_days": [
    4,
    5
  ],
  "minutes": [
    45,
    60
  ],
  "express_minutes": 25,
  "equipment_all": [],
  "equipment_any": [
    [
      "kettlebell",
      "dumbbell",
      "barbell"
    ]
  ],
  "skills_required": [],
  "excluded_for": [
    "pregnancy",
    "seated"
  ],
  "evidence": "C",
  "simplicity": 2,
  "graduates_to": [
    "hyrox-prep-4",
    "hybrid-strength-endurance-4to6"
  ],
  "block_weeks": 8,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 0.9,
    "rir": "4"
  },
  "meso": null,
  "layouts": {
    "3": [
      "A",
      "B",
      "C",
      "D",
      "E"
    ],
    "4": [
      "A",
      "B",
      "C",
      "D",
      "E"
    ],
    "5": [
      "A",
      "B",
      "C",
      "D",
      "E"
    ]
  },
  "modules": [
    "mobility"
  ],
  "sessions": {
    "A": {
      "title": "Squat · Couplet AMRAP",
      "tags": [
        "heavy_legs",
        "hard_cardio"
      ],
      "blocks": [
        {
          "name": "Strength",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat",
              "pattern": "squat",
              "prefer": [
                "back_squat",
                "front_squat",
                "goblet_squat"
              ],
              "sets": 5,
              "reps": "3-5",
              "rest": 150,
              "effort": "2 left, every rep clean",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Metcon",
          "kind": "finisher",
          "format": "amrap",
          "minutes": 12,
          "slots": [
            {
              "key": "metcon_a",
              "kind": "piece",
              "format": "amrap",
              "minutes": 12,
              "rule": "benchmark",
              "score": true,
              "effort": "hard but steady. Scale load first, then reps, then the movement. Novices: no high-skill move once you are tired",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "row_erg",
                      "bike_erg",
                      "run"
                    ],
                    "reps": "12 cal"
                  },
                  {
                    "pattern": "h_push",
                    "prefer": [
                      "push_up",
                      "incline_push_up",
                      "knee_push_up"
                    ],
                    "reps": "10"
                  }
                ],
                [
                  {
                    "pattern": "hinge",
                    "prefer": [
                      "kb_swing"
                    ],
                    "reps": "15"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "burpee"
                    ],
                    "reps": "10"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "db_thruster",
                      "thruster"
                    ],
                    "reps": "10"
                  },
                  {
                    "pattern": "v_pull",
                    "prefer": [
                      "pull_up",
                      "assisted_pull_up",
                      "band_lat_pulldown"
                    ],
                    "reps": "6"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "row_erg",
                      "bike_erg"
                    ],
                    "reps": "200 m"
                  },
                  {
                    "pattern": "squat",
                    "prefer": [
                      "bodyweight_squat"
                    ],
                    "reps": "20"
                  }
                ]
              ]
            }
          ]
        }
      ]
    },
    "B": {
      "title": "Press · Triplet for time",
      "tags": [
        "hard_cardio"
      ],
      "blocks": [
        {
          "name": "Strength",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "overhead_press",
                "push_press",
                "db_shoulder_press",
                "kb_press"
              ],
              "sets": 5,
              "reps": "3-5",
              "rest": 150,
              "effort": "2 left, ribs down",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Metcon",
          "kind": "finisher",
          "format": "fortime",
          "minutes": 12,
          "slots": [
            {
              "key": "metcon_b",
              "kind": "piece",
              "format": "fortime",
              "minutes": 12,
              "reps": "3 rounds",
              "rule": "benchmark",
              "score": true,
              "effort": "3 rounds, 12 min cap. Scale load first, then reps, then the movement. Novices: no high-skill move once you are tired",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "row_erg",
                      "run",
                      "bike_erg"
                    ],
                    "reps": "500 m"
                  },
                  {
                    "pattern": "squat",
                    "prefer": [
                      "goblet_squat",
                      "bodyweight_squat"
                    ],
                    "reps": "15"
                  },
                  {
                    "pattern": "h_push",
                    "prefer": [
                      "push_up",
                      "incline_push_up"
                    ],
                    "reps": "10"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "row_erg",
                      "bike_erg"
                    ],
                    "reps": "400 m"
                  },
                  {
                    "pattern": "hinge",
                    "prefer": [
                      "kb_swing",
                      "db_romanian_deadlift"
                    ],
                    "reps": "20"
                  },
                  {
                    "pattern": "flexion",
                    "prefer": [
                      "hanging_knee_raise",
                      "reverse_crunch"
                    ],
                    "reps": "10"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "bike_erg",
                      "row_erg",
                      "run"
                    ],
                    "reps": "15 cal"
                  },
                  {
                    "pattern": "throw",
                    "prefer": [
                      "wall_ball",
                      "med_ball_slam"
                    ],
                    "reps": "15"
                  },
                  {
                    "pattern": "lunge",
                    "prefer": [
                      "walking_lunge",
                      "reverse_lunge"
                    ],
                    "reps": "20"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "ski_erg",
                      "row_erg",
                      "bike_erg"
                    ],
                    "reps": "12 cal"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "devil_press",
                      "db_thruster"
                    ],
                    "reps": "6"
                  },
                  {
                    "pattern": "jump",
                    "prefer": [
                      "box_jump",
                      "squat_jump"
                    ],
                    "reps": "10"
                  }
                ]
              ]
            }
          ]
        }
      ]
    },
    "C": {
      "title": "Deadlift · Single modality EMOM",
      "tags": [
        "hinge_heavy",
        "hard_cardio"
      ],
      "blocks": [
        {
          "name": "Strength",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "deadlift",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift",
                "kb_deadlift",
                "db_romanian_deadlift"
              ],
              "sets": 3,
              "reps": "3-5",
              "rest": 180,
              "effort": "2 left, flat back",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Metcon",
          "kind": "finisher",
          "format": "emom",
          "minutes": 12,
          "slots": [
            {
              "key": "metcon_c",
              "kind": "piece",
              "format": "emom",
              "minutes": 12,
              "rule": "benchmark",
              "score": true,
              "effort": "every minute on the minute, 15 to 20 s of rest left each minute. Scale reps before you drop the movement",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "row_erg",
                      "bike_erg",
                      "ski_erg"
                    ],
                    "reps": "12 cal"
                  }
                ],
                [
                  {
                    "pattern": "h_push",
                    "prefer": [
                      "push_up",
                      "incline_push_up",
                      "knee_push_up"
                    ],
                    "reps": "10"
                  },
                  {
                    "pattern": "squat",
                    "prefer": [
                      "bodyweight_squat"
                    ],
                    "reps": "15"
                  }
                ],
                [
                  {
                    "pattern": "hinge",
                    "prefer": [
                      "kb_swing"
                    ],
                    "reps": "15"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "db_thruster",
                      "thruster"
                    ],
                    "reps": "8"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "jump_rope",
                      "bike_erg"
                    ],
                    "reps": "40 s"
                  }
                ]
              ]
            }
          ]
        }
      ]
    },
    "D": {
      "title": "Bench · Triplet AMRAP",
      "tags": [
        "hard_cardio"
      ],
      "blocks": [
        {
          "name": "Strength",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "bench",
              "pattern": "h_push",
              "prefer": [
                "bench_press",
                "db_bench_press",
                "db_floor_press",
                "push_up"
              ],
              "sets": 5,
              "reps": "3-5",
              "rest": 150,
              "effort": "2 left, feet planted",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Metcon",
          "kind": "finisher",
          "format": "amrap",
          "minutes": 16,
          "slots": [
            {
              "key": "metcon_d",
              "kind": "piece",
              "format": "amrap",
              "minutes": 16,
              "rule": "benchmark",
              "score": true,
              "effort": "a pace you can hold for 16 min. Scale load first, then reps, then the movement. Novices: no high-skill move once you are tired",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "row_erg",
                      "bike_erg"
                    ],
                    "reps": "400 m"
                  },
                  {
                    "pattern": "lunge",
                    "prefer": [
                      "db_reverse_lunge",
                      "reverse_lunge"
                    ],
                    "reps": "12"
                  },
                  {
                    "pattern": "v_pull",
                    "prefer": [
                      "pull_up",
                      "assisted_pull_up",
                      "band_lat_pulldown"
                    ],
                    "reps": "6"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "row_erg",
                      "bike_erg",
                      "run"
                    ],
                    "reps": "15 cal"
                  },
                  {
                    "pattern": "hinge",
                    "prefer": [
                      "kb_swing",
                      "db_romanian_deadlift"
                    ],
                    "reps": "15"
                  },
                  {
                    "pattern": "h_push",
                    "prefer": [
                      "push_up",
                      "incline_push_up"
                    ],
                    "reps": "12"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "bike_erg",
                      "row_erg",
                      "run"
                    ],
                    "reps": "12 cal"
                  },
                  {
                    "pattern": "squat",
                    "prefer": [
                      "goblet_squat",
                      "bodyweight_squat"
                    ],
                    "reps": "12"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "burpee"
                    ],
                    "reps": "8"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "ski_erg",
                      "row_erg",
                      "bike_erg"
                    ],
                    "reps": "12 cal"
                  },
                  {
                    "pattern": "throw",
                    "prefer": [
                      "med_ball_slam",
                      "wall_ball"
                    ],
                    "reps": "12"
                  },
                  {
                    "pattern": "flexion",
                    "prefer": [
                      "hanging_knee_raise",
                      "reverse_crunch"
                    ],
                    "reps": "10"
                  }
                ]
              ]
            }
          ]
        }
      ]
    },
    "E": {
      "title": "Power clean · Chipper",
      "tags": [
        "power",
        "hard_cardio"
      ],
      "blocks": [
        {
          "name": "Skill",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "clean",
              "pattern": "olympic",
              "prefer": [
                "hang_power_clean",
                "db_hang_clean",
                "kb_snatch"
              ],
              "sets": 5,
              "reps": "2-3",
              "rest": 120,
              "effort": "light, fast and crisp. End the set when the bar slows or the catch gets messy",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Metcon",
          "kind": "finisher",
          "format": "fortime",
          "minutes": 14,
          "slots": [
            {
              "key": "metcon_e",
              "kind": "piece",
              "format": "fortime",
              "minutes": 14,
              "reps": "1 round",
              "rule": "benchmark",
              "score": true,
              "effort": "one pass, top to bottom, 14 min cap. Break the sets early. Scale load first, then reps, then the movement",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "row_erg",
                      "bike_erg",
                      "run"
                    ],
                    "reps": "30 cal"
                  },
                  {
                    "pattern": "hinge",
                    "prefer": [
                      "kb_swing"
                    ],
                    "reps": "30"
                  },
                  {
                    "pattern": "lunge",
                    "prefer": [
                      "walking_lunge",
                      "reverse_lunge"
                    ],
                    "reps": "30"
                  },
                  {
                    "pattern": "h_push",
                    "prefer": [
                      "push_up",
                      "incline_push_up"
                    ],
                    "reps": "30"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "burpee"
                    ],
                    "reps": "15"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "row_erg",
                      "bike_erg"
                    ],
                    "reps": "800 m"
                  },
                  {
                    "pattern": "squat",
                    "prefer": [
                      "goblet_squat",
                      "bodyweight_squat"
                    ],
                    "reps": "40"
                  },
                  {
                    "pattern": "v_pull",
                    "prefer": [
                      "pull_up",
                      "assisted_pull_up",
                      "band_lat_pulldown"
                    ],
                    "reps": "20"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "bike_erg",
                      "row_erg",
                      "run"
                    ],
                    "reps": "30 cal"
                  },
                  {
                    "pattern": "throw",
                    "prefer": [
                      "wall_ball",
                      "med_ball_slam"
                    ],
                    "reps": "30"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "db_thruster",
                      "thruster"
                    ],
                    "reps": "20"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "ski_erg",
                      "row_erg",
                      "bike_erg"
                    ],
                    "reps": "25 cal"
                  },
                  {
                    "pattern": "jump",
                    "prefer": [
                      "box_jump",
                      "squat_jump"
                    ],
                    "reps": "20"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "devil_press",
                      "kb_clean_and_press"
                    ],
                    "reps": "10"
                  }
                ]
              ]
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · Squat · 8 min AMRAP",
    "tags": [
      "heavy_legs",
      "hard_cardio"
    ],
    "blocks": [
      {
        "name": "Strength",
        "kind": "main",
        "format": "straight",
        "slots": [
          {
            "key": "squat",
            "pattern": "squat",
            "prefer": [
              "back_squat",
              "front_squat",
              "goblet_squat"
            ],
            "sets": 3,
            "reps": "3-5",
            "rest": 120,
            "effort": "2 left, every rep clean",
            "rule": "double_progression",
            "score": true
          }
        ]
      },
      {
        "name": "Metcon",
        "kind": "finisher",
        "format": "amrap",
        "minutes": 8,
        "slots": [
          {
            "key": "metcon_express",
            "kind": "piece",
            "format": "amrap",
            "minutes": 8,
            "rule": "benchmark",
            "score": true,
            "effort": "hard but steady. Scale load first, then reps, then the movement",
            "pieces": [
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "row_erg",
                    "bike_erg",
                    "run"
                  ],
                  "reps": "10 cal"
                },
                {
                  "pattern": "hinge",
                  "prefer": [
                    "kb_swing"
                  ],
                  "reps": "12"
                },
                {
                  "pattern": "h_push",
                  "prefer": [
                    "push_up",
                    "incline_push_up"
                  ],
                  "reps": "8"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "burpee"
                  ],
                  "reps": "8"
                },
                {
                  "pattern": "squat",
                  "prefer": [
                    "goblet_squat",
                    "bodyweight_squat"
                  ],
                  "reps": "12"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "db_thruster",
                    "thruster"
                  ],
                  "reps": "8"
                },
                {
                  "pattern": "v_pull",
                  "prefer": [
                    "pull_up",
                    "assisted_pull_up",
                    "band_lat_pulldown"
                  ],
                  "reps": "5"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "run",
                    "row_erg",
                    "bike_erg"
                  ],
                  "reps": "200 m"
                },
                {
                  "pattern": "lunge",
                  "prefer": [
                    "walking_lunge",
                    "reverse_lunge"
                  ],
                  "reps": "16"
                }
              ]
            ]
          }
        ]
      }
    ]
  }
}
```
