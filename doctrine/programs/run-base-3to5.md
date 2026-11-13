# Running base, 80/20 · run-base-3to5

**What it is.** A running week built the way endurance athletes actually train: most of the time easy, one quality session, one long run. Easy means you can talk in full sentences. The quality session is the only one that is hard, and it is capped so it never takes over the week.

**Who it is for.** Anyone who can already run 20 to 30 minutes without stopping and wants to run further or faster. Outside or on a treadmill. 2 to 5 days a week, 30 to 90 minutes (2 days only inside a mixed week: an easy run and the long run). Can't run 20 minutes yet: `run-c25k-3` first.

**The week.** In order, round and round:

| days | rotation |
|:-|:-|
| 2 | easy · long (only inside a mixed week, next to other days) |
| 3 | easy · quality · long |
| 4 | easy · quality · easy · long |
| 5 | easy · quality · easy · long · easy |

| session | what |
|:-|:-|
| E | easy run by the talk test, starts at 25 min |
| Q | one quality run: strides, tempo, cruise intervals or short VO2 intervals |
| L | long run, starts at 40 min, never past 150 min |

**Easy is the whole game.** About 80% of training time easy, 20% moderate or hard [seen: Fitzgerald 80/20]. That share is Seiler's description of how elite athletes already train, and it is often counted in sessions, not minutes [seen], so do not chase the number: just keep the easy days easy. For recreational runners, whether the hard 20% is mostly threshold (pyramidal) or mostly intervals (polarised) matters little, and pyramidal may suit you slightly better [seen: Rosenblat 2025]. This plan leans pyramidal: more tempo than all-out.

**The caps on the quality run.** From Daniels' summaries [seen, secondary]: threshold about 10% of weekly volume, or a steady 20 min tempo; intervals at most 8% of the week or 10 km; the long run at most 25 to 30% of the week and 150 min. At most one quality session a week [seen: research/03 rule 3].

**How it climbs.** Easy and long runs: hold the minutes about 3 weeks, then add about 10% [seen, secondary: Daniels holds a level at least 3 weeks]. The 10% rule did not prevent injury in a novice trial [seen: Buist 2008]; what looks risky is jumping more than about 30% over two weeks [seen: Nielsen 2014], so the engine never does. The quality run is a benchmark: your best on each version is the score.

**Deload.** None scheduled: the volume rule holds you 3 weeks at a time. If a week goes badly, repeat it. After 6 weeks the block review checks the long run is still under its cap.

**Graduates to.** `hybrid-strength-endurance-4to6` to add lifting, `hyrox-prep-4` for a race, or the `run-race` module next to a strength program for a 5 km to half marathon goal.

**Evidence: B.** Polarised and pyramidal distributions are backed by trials and meta-analyses [seen: Stöggl 2014, Rosenblat 2019, Rosenblat 2025]; the per session caps are expert heuristics [seen].

**Credit.** Matt Fitzgerald, *80/20 Running* (8020endurance.com). Stephen Seiler's research on training intensity distribution. Jack Daniels, *Daniels' Running Formula*, 4th edition, Human Kinetics 2021. Buy the books for the full plans and pace tables.

## The data (the engine reads this block)

```json
{
  "id": "run-base-3to5",
  "name": "Running base, 80/20",
  "family": "run",
  "draws_from": [
    "Matt Fitzgerald, 80/20 Running",
    "Stephen Seiler",
    "Daniels' Running Formula",
    "Rosenblat 2025"
  ],
  "goals": {
    "muscle": 0,
    "strength": 0,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 2,
    "run": 3,
    "skills": 0,
    "fat_loss": 2,
    "health": 3,
    "independent": 3
  },
  "experience": [
    "novice",
    "intermediate",
    "advanced"
  ],
  "days": [
    2,
    5
  ],
  "sweet_days": [
    4
  ],
  "minutes": [
    30,
    90
  ],
  "express_minutes": 20,
  "equipment_all": [],
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
  "simplicity": 1,
  "graduates_to": [
    "hybrid-strength-endurance-4to6",
    "hyrox-prep-4"
  ],
  "block_weeks": 6,
  "deload": null,
  "meso": null,
  "layouts": {
    "3": [
      "E",
      "Q",
      "L"
    ],
    "4": [
      "E",
      "Q",
      "E",
      "L"
    ],
    "5": [
      "E",
      "Q",
      "E",
      "L",
      "E"
    ],
    "2": [
      "E",
      "L"
    ]
  },
  "modules": [
    "mobility"
  ],
  "sessions": {
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
                "run"
              ],
              "sets": 1,
              "reps": "25 min",
              "rest": 0,
              "effort": "talk test: full sentences the whole way",
              "rule": "run_volume",
              "start_minutes": 25,
              "per_week": 2,
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
                      "easy_run"
                    ],
                    "reps": "25 min easy plus 6 x 20 s short fast bursts, walk back"
                  }
                ],
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
                    "reps": "4 x 1.6 km at a hard pace you could hold for an hour, 1 min jog between"
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
                ]
              ]
            }
          ]
        }
      ]
    },
    "L": {
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
              "reps": "40 min",
              "rest": 0,
              "effort": "talk test the whole way. At most 25 to 30% of your week",
              "rule": "run_volume",
              "start_minutes": 40,
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
    "title": "Short version · 20 min easy run",
    "tags": [],
    "blocks": [
      {
        "name": "Run",
        "kind": "main",
        "format": "run",
        "slots": [
          {
            "key": "express_run",
            "pattern": "cyclic",
            "prefer": [
              "easy_run",
              "run"
            ],
            "sets": 1,
            "reps": "20 min",
            "rest": 0,
            "effort": "talk test: full sentences",
            "rule": "run_volume",
            "start_minutes": 20,
            "per_week": 1,
            "max_minutes": 20,
            "score": true
          }
        ]
      }
    ]
  }
}
```
