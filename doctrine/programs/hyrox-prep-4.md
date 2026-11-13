# HYROX preparation, beginner week · hyrox-prep-4

**What it is.** The four session week most beginner HYROX plans agree on: an easy run, a lower body strength day with short station practice, an interval run, and a compromised running day where you run straight off a station, the way the race feels. A HYROX race is 8 x (1 km run plus 1 station), always in the same order [snippet: Red Bull, Roxlyfe, research/02].

**Who it is for.** Novice or intermediate, already able to run 30 minutes without stopping, which is the entry bar third party plans set [snippet: Men's Fitness AU 8 week plan, Centr beginner plan]. Can run outside or on a treadmill and has something to carry (dumbbells, kettlebells or a sandbag). 3 to 5 days a week, 45 to 75 minutes. Can't run 30 minutes yet: start with `run-c25k-3`.

**The week.** Strength, easy run, intervals, compromised run, in that order and round again. The order keeps the heavy leg day and the interval day apart, so your legs get about 48 hours between them as in the template [snippet: research/02 rule 8; Schumann 2022]. On 5 days a second, shorter easy run goes in after the intervals. On 3 days the easy run is left out (strength, intervals, compromised run) and the plan says so.

| session | what | tag |
|:-|:-|:-|
| S | squat 4 x 5 to 8 · lunge 3 x 8 to 12 · 10 min station practice | heavy legs |
| E | easy run by the talk test, starts at 30 min | |
| I | interval run, for example 6 x 1 km at goal race pace | hard cardio |
| C | compromised running: 1 km run, then a station, 4 rounds to start | |
| R (5 days only) | a second easy run, starts at 25 min | |

**Station weights.** Not written in the sessions. They live in the `hyrox-stations` module with the full table per division (Women Open, Women Pro, Men Open, Men Pro), because the rulebook changes by season and the agent never guesses a weight. Train light first and work up to race weight. Try to get at least 2 to 3 sessions on a real sled, SkiErg and wall ball target before race day [snippet: Genesis Fitness, The Gym Group].

**How it climbs.** The lifts: double progression. The easy runs: hold the minutes about 3 weeks, then add about 10% [seen: Daniels summaries, research/03]. The intervals and the compromised runs: benchmarks, your best time on each version is the score to beat. Compromised running weekly from about week 5 [snippet]; before that keep session C controlled, a station practice with easy running between.

**Deload.** After 8 weeks, a lighter week: 60% of the sets, 90% of the load. Most beginner plans run 4 to 20 weeks [believe], so 8 weeks is one block.

**Graduates to.** `hybrid-strength-endurance-4to6` after the race, if you want to keep both qualities.

**Evidence: C.** Coach consensus and published plans; no trial on HYROX preparation that the research found [believe]. The spacing of hard legs and hard running rests on meta-analyses [snippet: Schumann 2022, Petré 2021].

**Credit.** HYROX is a registered race format (hyrox.com): read the current season's rulebook. The week is built from free third party beginner plans (Men's Fitness AU, Centr, Genesis Fitness). HWPO HYROX (Mat Fraser) is a paid 3 day a week option; nothing from it is copied here.

## The data (the engine reads this block)

```json
{
  "id": "hyrox-prep-4",
  "name": "HYROX preparation, beginner week",
  "family": "hyrox",
  "draws_from": [
    "Men's Fitness AU 8 week HYROX plan",
    "Centr HYROX beginner plan",
    "Genesis Fitness",
    "Daniels' Running Formula",
    "Schumann 2022"
  ],
  "goals": {
    "muscle": 1,
    "strength": 1,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 2,
    "hyrox": 3,
    "run": 2,
    "skills": 0,
    "fat_loss": 2,
    "health": 2,
    "independent": 1
  },
  "experience": [
    "none",
    "novice",
    "intermediate",
    "advanced"
  ],
  "days": [
    3,
    5
  ],
  "sweet_days": [
    4
  ],
  "minutes": [
    45,
    75
  ],
  "express_minutes": 30,
  "equipment_all": [],
  "equipment_any": [
    [
      "outdoors",
      "treadmill"
    ],
    [
      "dumbbell",
      "kettlebell",
      "sandbag",
      "barbell"
    ]
  ],
  "skills_required": [
    "run_30min"
  ],
  "excluded_for": [
    "pregnancy",
    "seated",
    "low_bone_density"
  ],
  "evidence": "C",
  "simplicity": 2,
  "graduates_to": [
    "hybrid-strength-endurance-4to6"
  ],
  "block_weeks": 8,
  "deload": {
    "sets_factor": 0.6,
    "load_factor": 0.9,
    "rir": "3"
  },
  "meso": null,
  "layouts": {
    "3": [
      "S",
      "I",
      "C"
    ],
    "4": [
      "S",
      "E",
      "I",
      "C"
    ],
    "5": [
      "S",
      "E",
      "I",
      "R",
      "C"
    ]
  },
  "modules": [
    "mobility"
  ],
  "sessions": {
    "S": {
      "title": "Legs, heavy · race stations",
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
                "front_squat",
                "goblet_squat"
              ],
              "sets": 4,
              "reps": "5-8",
              "rest": 150,
              "effort": "2 reps spare, every rep clean",
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
              "key": "lunge",
              "pattern": "lunge",
              "prefer": [
                "sandbag_lunge",
                "walking_lunge",
                "db_reverse_lunge"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 90,
              "effort": "2 reps spare, each leg",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Race stations",
          "kind": "finisher",
          "format": "circuit",
          "minutes": 10,
          "slots": [
            {
              "key": "station_practice",
              "kind": "piece",
              "format": "fortime",
              "minutes": 10,
              "reps": "2 rounds",
              "rule": "benchmark",
              "effort": "technique, not a race: light first, working up to your race weight",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "sled_push",
                      "sled_pull"
                    ],
                    "reps": "25 m"
                  },
                  {
                    "pattern": "throw",
                    "prefer": [
                      "wall_ball",
                      "med_ball_slam"
                    ],
                    "reps": "15"
                  }
                ],
                [
                  {
                    "pattern": "carry",
                    "prefer": [
                      "farmer_carry",
                      "suitcase_carry"
                    ],
                    "reps": "50 m"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "burpee_broad_jump",
                      "burpee"
                    ],
                    "reps": "10"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "sled_pull",
                      "sled_push"
                    ],
                    "reps": "25 m"
                  },
                  {
                    "pattern": "lunge",
                    "prefer": [
                      "sandbag_lunge",
                      "walking_lunge"
                    ],
                    "reps": "20 m"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "ski_erg",
                      "row_erg"
                    ],
                    "reps": "250 m"
                  },
                  {
                    "pattern": "carry",
                    "prefer": [
                      "farmer_carry",
                      "sandbag_carry"
                    ],
                    "reps": "50 m"
                  }
                ]
              ]
            }
          ]
        }
      ]
    },
    "E": {
      "title": "Easy run",
      "tags": [],
      "blocks": [
        {
          "name": "Run",
          "kind": "main",
          "format": "run",
          "slots": [
            {
              "key": "easy_run",
              "pattern": "cyclic",
              "prefer": [
                "easy_run",
                "run",
                "bike_erg",
                "row_erg"
              ],
              "sets": 1,
              "reps": "30 min",
              "rest": 0,
              "effort": "talk test: full sentences the whole way",
              "rule": "run_volume",
              "start_minutes": 30,
              "per_week": 1,
              "max_minutes": 75,
              "score": true
            }
          ]
        }
      ]
    },
    "I": {
      "title": "Interval run",
      "tags": [
        "hard_cardio"
      ],
      "blocks": [
        {
          "name": "Intervals",
          "kind": "main",
          "format": "intervals",
          "minutes": 40,
          "slots": [
            {
              "key": "intervals",
              "kind": "piece",
              "format": "fortime",
              "minutes": 40,
              "rule": "benchmark",
              "score": true,
              "effort": "10 min easy first. Goal race pace, even splits, the last rep as fast as the first",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "interval_run",
                      "run",
                      "row_erg"
                    ],
                    "reps": "6 x 1 km, 90 s walk between"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "interval_run",
                      "run",
                      "row_erg"
                    ],
                    "reps": "8 x 500 m, 60 s walk between"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "interval_run",
                      "run",
                      "row_erg"
                    ],
                    "reps": "5 x 1200 m, 2 min walk between"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "interval_run",
                      "run",
                      "row_erg"
                    ],
                    "reps": "8 x 1 km, 90 s walk between"
                  }
                ]
              ]
            }
          ]
        }
      ]
    },
    "C": {
      "title": "Running straight off a station",
      "tags": [],
      "blocks": [
        {
          "name": "Run straight off a station",
          "kind": "main",
          "format": "fortime",
          "minutes": 40,
          "slots": [
            {
              "key": "compromised",
              "kind": "piece",
              "format": "fortime",
              "minutes": 40,
              "reps": "4 rounds",
              "rule": "benchmark",
              "score": true,
              "effort": "4 rounds to start, up to 8 by race week. Stations light first, up to race weight. Before week 5 keep it controlled",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "interval_run"
                    ],
                    "reps": "1 km"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "ski_erg",
                      "row_erg",
                      "bike_erg"
                    ],
                    "reps": "500 m"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "interval_run"
                    ],
                    "reps": "1 km"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "sled_push",
                      "sled_pull"
                    ],
                    "reps": "25 m"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "interval_run"
                    ],
                    "reps": "1 km"
                  },
                  {
                    "pattern": "carry",
                    "prefer": [
                      "farmer_carry",
                      "suitcase_carry"
                    ],
                    "reps": "100 m heavy"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "interval_run"
                    ],
                    "reps": "1 km"
                  },
                  {
                    "pattern": "lunge",
                    "prefer": [
                      "sandbag_lunge",
                      "walking_lunge"
                    ],
                    "reps": "50 m"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "interval_run"
                    ],
                    "reps": "1 km"
                  },
                  {
                    "pattern": "throw",
                    "prefer": [
                      "wall_ball",
                      "med_ball_slam"
                    ],
                    "reps": "25"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "interval_run"
                    ],
                    "reps": "1 km"
                  },
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "burpee_broad_jump",
                      "burpee"
                    ],
                    "reps": "20 m"
                  }
                ]
              ]
            }
          ]
        }
      ]
    },
    "R": {
      "title": "Second easy run",
      "tags": [],
      "blocks": [
        {
          "name": "Run",
          "kind": "main",
          "format": "run",
          "slots": [
            {
              "key": "easy_run_2",
              "pattern": "cyclic",
              "prefer": [
                "easy_run",
                "run",
                "bike_erg",
                "row_erg"
              ],
              "sets": 1,
              "reps": "25 min",
              "rest": 0,
              "effort": "talk test: full sentences, slower than you think",
              "rule": "run_volume",
              "start_minutes": 25,
              "per_week": 1,
              "max_minutes": 50,
              "score": true
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Short version · a short run off a station",
    "tags": [],
    "blocks": [
      {
        "name": "Run straight off a station",
        "kind": "main",
        "format": "fortime",
        "minutes": 25,
        "slots": [
          {
            "key": "compromised_express",
            "kind": "piece",
            "format": "fortime",
            "minutes": 25,
            "reps": "3 rounds",
            "rule": "benchmark",
            "score": true,
            "effort": "5 min easy jog first. Stations light first, up to race weight",
            "pieces": [
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "run",
                    "interval_run"
                  ],
                  "reps": "500 m"
                },
                {
                  "pattern": "throw",
                  "prefer": [
                    "wall_ball",
                    "med_ball_slam"
                  ],
                  "reps": "15"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "run",
                    "interval_run"
                  ],
                  "reps": "500 m"
                },
                {
                  "pattern": "carry",
                  "prefer": [
                    "farmer_carry",
                    "suitcase_carry"
                  ],
                  "reps": "50 m"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "run",
                    "interval_run"
                  ],
                  "reps": "500 m"
                },
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "ski_erg",
                    "row_erg",
                    "bike_erg"
                  ],
                  "reps": "250 m"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "run",
                    "interval_run"
                  ],
                  "reps": "500 m"
                },
                {
                  "pattern": "lunge",
                  "prefer": [
                    "sandbag_lunge",
                    "walking_lunge"
                  ],
                  "reps": "20 m"
                }
              ]
            ]
          }
        ]
      }
    ]
  },
  "layout_notes": {
    "3": "On 3 days the easy run is the session left out. One easy 30 minutes on a free day is the best thing to add."
  }
}
```
