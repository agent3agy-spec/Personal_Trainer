# Hybrid strength and endurance · hybrid-strength-endurance-4to6

**What it is.** Lift and run in the same week without one wrecking the other. The rule is the minimum effective dose: 2 to 3 strength sessions on the big lifts and 2 to 3 runs, never a full strength plan stacked on a full running plan, and the easy runs stay truly easy [snippet: Viada, secondary write ups, research/02].

**Who it is for.** Novice to advanced lifters who can already run 30 minutes, want to get stronger and fitter at once, and have a barbell, a rack and a place to run. 4 to 6 days a week, 45 to 75 minutes.

**The week.** Sessions in this order, round and round:

| days | rotation |
|:-|:-|
| 4 | lower strength · easy run · quality run · upper strength |
| 5 | lower strength · easy run · quality run · upper strength · long run |
| 6 | lower strength · easy run · quality run · upper strength · full body strength · long run |

| session | what |
|:-|:-|
| L | squat 3 x 4 to 6 · Romanian deadlift 3 x 6 to 8 |
| U | bench 3 x 4 to 6 · row 3 x 6 to 10 · chin-up 3 x 5 to 8 |
| F | deadlift 3 x 5 · overhead press 3 x 5 to 8 · split squat 2 x 8 to 12 |
| E | easy run by the talk test, starts at 30 min |
| Q | one quality run: tempo, cruise intervals, VO2 intervals or strides |
| G | long run, starts at 45 min, never past 150 min |

**Keep heavy legs and hard runs apart.** The order already puts an easy session between them. If you ever do both on one day, at least 3 hours apart with the priority one first; a separate day is better. Adding cardio does not cost most people muscle or max strength, but explosive strength suffers when both are crammed into one session, and trained lifters lose some 1RM gain only in the same session [snippet: Schumann 2022, 43 studies; Petré 2021, 27 studies]. If leg size is your goal, swap the easy run for the bike now and then [snippet: Wilson 2012, Lundberg 2022, a low cost hedge].

**How it climbs.** The lifts: double progression, the deadlift linear (+5 kg each clean session, three misses and it drops 10%). The easy and long runs: hold the minutes about 3 weeks, then add about 10% [seen, secondary: Daniels]. The quality run is a benchmark. Daniels' caps, kept in prose because they depend on your weekly total [seen, secondary summaries]: threshold work about 10% of weekly volume (a steady 20 min tempo), intervals at most 8%, the long run at most 25 to 30% of the week and never past 150 min. Most of the week is easy.

**Deload.** After 6 weeks, a lighter week: half the sets, 90% of the load, 4 reps left. The runs hold their minutes.

**Graduates to.** Nothing above it in this folder: keep running blocks, or move to a race module (`run-race`) next to a pure strength program.

**Evidence: B.** The interference findings are meta-analyses, the strongest evidence in the whole research cluster [snippet: Schumann 2022, Petré 2021, Wilson 2012]. The minimum dose idea is coach consensus [snippet]. The Daniels caps are expert heuristics [seen].

**Credit.** Alex Viada, *The Hybrid Athlete* and *The Ultimate Hybrid Athlete* (Victory Belt, completehumanperformance.com). Nick Bare's free 16 week BPN hybrid plan is a good worked example (each lift once a week, runs in the morning, lifts later); his paid Hybrid Athlete 1.0 is on Playbook. Jack Daniels, *Daniels' Running Formula*, 4th edition, Human Kinetics 2021. Nothing paid is copied here.

## The data (the engine reads this block)

```json
{
  "id": "hybrid-strength-endurance-4to6",
  "name": "Hybrid strength and endurance",
  "family": "hybrid",
  "draws_from": [
    "Alex Viada, The Hybrid Athlete",
    "Nick Bare BPN 16 week plan",
    "Daniels' Running Formula",
    "Schumann 2022",
    "Petré 2021"
  ],
  "goals": {
    "muscle": 2,
    "strength": 2,
    "powerlifting": 1,
    "weightlifting": 0,
    "functional": 2,
    "hyrox": 2,
    "run": 2,
    "skills": 0,
    "fat_loss": 2,
    "health": 3,
    "independent": 1
  },
  "experience": [
    "novice",
    "intermediate",
    "advanced"
  ],
  "days": [
    4,
    6
  ],
  "sweet_days": [
    5
  ],
  "minutes": [
    45,
    75
  ],
  "express_minutes": 30,
  "equipment_all": [
    "barbell",
    "rack",
    "plates"
  ],
  "equipment_any": [
    [
      "outdoors",
      "treadmill"
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
  "evidence": "B",
  "simplicity": 2,
  "graduates_to": [],
  "block_weeks": 6,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 0.9,
    "rir": "4"
  },
  "meso": null,
  "layouts": {
    "4": [
      "L",
      "E",
      "Q",
      "U"
    ],
    "5": [
      "L",
      "E",
      "Q",
      "U",
      "G"
    ],
    "6": [
      "L",
      "E",
      "Q",
      "U",
      "F",
      "G"
    ]
  },
  "modules": [
    "mobility"
  ],
  "sessions": {
    "L": {
      "title": "Squat · Romanian deadlift",
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
              "sets": 3,
              "reps": "4-6",
              "rest": 180,
              "effort": "1 or 2 reps spare, every rep clean",
              "rule": "double_progression",
              "inc": 5,
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
              "key": "rdl",
              "pattern": "hinge",
              "prefer": [
                "romanian_deadlift",
                "db_romanian_deadlift"
              ],
              "sets": 3,
              "reps": "6-8",
              "rest": 120,
              "effort": "2 reps spare, flat back, feel the hamstrings",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Extra work",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "calves",
              "pattern": "calves",
              "prefer": [
                "calf_raise",
                "single_leg_calf_raise"
              ],
              "sets": 2,
              "reps": "10-15",
              "rest": 60,
              "effort": "2 reps spare, full stretch at the bottom",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "U": {
      "title": "Bench · Row · Chin-up",
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
                "bench_press",
                "db_bench_press"
              ],
              "sets": 3,
              "reps": "4-6",
              "rest": 180,
              "effort": "1 or 2 reps spare",
              "rule": "double_progression",
              "inc": 2.5,
              "score": true
            }
          ]
        },
        {
          "name": "Second exercises",
          "kind": "secondary",
          "format": "superset",
          "rest_after_round": 90,
          "slots": [
            {
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "barbell_row",
                "chest_supported_row",
                "db_row"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            },
            {
              "key": "vpull",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "pull_up",
                "lat_pulldown",
                "negative_pull_up"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 60,
              "effort": "2 reps spare",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "F": {
      "title": "Deadlift · Press · Split squat",
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
              "reps": "5",
              "rest": 180,
              "effort": "1 or 2 reps spare, flat back",
              "rule": "linear_session",
              "inc": 5,
              "inc_after_100": 2.5,
              "score": true
            }
          ]
        },
        {
          "name": "Second exercises",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "overhead_press",
                "db_shoulder_press"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 120,
              "effort": "2 reps spare, ribs down",
              "rule": "double_progression"
            },
            {
              "key": "split_squat",
              "pattern": "lunge",
              "prefer": [
                "bulgarian_split_squat",
                "db_reverse_lunge",
                "reverse_lunge"
              ],
              "sets": 2,
              "reps": "8-12",
              "rest": 90,
              "effort": "2 reps spare, each leg",
              "rule": "double_progression"
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
                "bike_erg"
              ],
              "sets": 1,
              "reps": "30 min",
              "rest": 0,
              "effort": "talk test: full sentences. Truly easy, never power through it",
              "rule": "run_volume",
              "start_minutes": 30,
              "per_week": 1,
              "max_minutes": 70,
              "score": true
            }
          ]
        }
      ]
    },
    "Q": {
      "title": "Quality run",
      "tags": [
        "hard_cardio"
      ],
      "blocks": [
        {
          "name": "Faster run",
          "kind": "main",
          "format": "intervals",
          "minutes": 45,
          "slots": [
            {
              "key": "quality_run",
              "kind": "piece",
              "format": "fortime",
              "minutes": 45,
              "rule": "benchmark",
              "score": true,
              "effort": "10 to 15 min easy first and 10 min easy after. Keep the fast running a small part of your week",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "interval_run"
                    ],
                    "reps": "20 min steady, comfortably hard"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "interval_run",
                      "run"
                    ],
                    "reps": "5 x 3 min hard, 2 min jog between"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "interval_run",
                      "run"
                    ],
                    "reps": "4 x 1.6 km at a hard pace you could hold for an hour, 1 min jog between"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "easy_run"
                    ],
                    "reps": "30 min easy plus 6 x 20 s short fast bursts, walk back"
                  }
                ]
              ]
            }
          ]
        }
      ]
    },
    "G": {
      "title": "Long run",
      "tags": [],
      "blocks": [
        {
          "name": "Run",
          "kind": "main",
          "format": "run",
          "slots": [
            {
              "key": "long_run",
              "pattern": "cyclic",
              "prefer": [
                "easy_run",
                "run"
              ],
              "sets": 1,
              "reps": "45 min",
              "rest": 0,
              "effort": "talk test the whole way. At most 25 to 30% of your week",
              "rule": "run_volume",
              "start_minutes": 45,
              "per_week": 1,
              "max_minutes": 150,
              "score": true
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
              "back_squat",
              "front_squat",
              "goblet_squat"
            ],
            "sets": 2,
            "reps": "4-6",
            "rest": 150,
            "effort": "1 or 2 reps spare",
            "rule": "double_progression",
            "inc": 5,
            "score": true
          },
          {
            "key": "bench",
            "pattern": "h_push",
            "prefer": [
              "bench_press",
              "db_bench_press"
            ],
            "sets": 2,
            "reps": "4-6",
            "rest": 150,
            "effort": "1 or 2 reps spare",
            "rule": "double_progression",
            "inc": 2.5
          }
        ]
      }
    ]
  }
}
```
