# Couch to 5K · run-c25k-3

**What it is.** The NHS plan that takes you from not running at all to running 30 minutes without stopping, in 9 weeks. Three runs a week, each one mixing running and walking, with the running share growing week by week. Nothing else: no lifting, just a short mobility finisher.

**Who it is for.** Anyone who can walk briskly for 30 minutes and wants to start running. No experience needed. Outside or on a treadmill. 2 or 3 days a week, 25 to 45 minutes including the walks.

**The week.** Three runs, with a rest day between them [seen: NHS plan, research/03]. On 2 days a week it is the same run, the week just takes longer to finish.

**The runs.** Every run starts and ends with 5 minutes of brisk walking.

| week | run 1 | run 2 | run 3 |
|:-|:-|:-|:-|
| 1 | 8 x (1 min run, 1:30 walk) | same | same |
| 2 | 6 x (1:30 run, 2 min walk) | same | same |
| 3 | 2 x (1:30 run, 1:30 walk, 3 min run, 3 min walk) | same | same |
| 4 | 3 min run, 1:30 walk, 5 min run, 2:30 walk, 3 min run, 1:30 walk, 5 min run | same | same |
| 5 | 3 x (5 min run, 3 min walk) | 2 x (8 min run, 5 min walk) | 20 min run |
| 6 | 5 min run, 3 min walk, 8 min run, 3 min walk, 5 min run | 2 x (10 min run, 3 min walk) | 25 min run |
| 7 | 25 min run | same | same |
| 8 | 28 min run | same | same |
| 9 | 30 min run | same | same |

Week 1 is [seen] in the NHS plan's own text (run 1 min, walk 90 s, about 20 min of intervals, 5 min walk either side). Weeks 2 to 9 are [believe]: written from the NHS plan as best remembered, to verify against nhs.uk before they are hard rules.

**How it climbs.** Finish all three runs of a week and the next run is the next week. Miss one, or have to stop, and you repeat the week: the NHS says any week can be repeated until you are ready [seen]. Run slowly enough to talk. No speed work until 20 to 30 minutes continuous is comfortable [seen: research/03 rule 2].

**Why so gentle.** Novice runners get hurt about 17.8 times per 1000 hours, more than twice the rate of recreational runners [seen: Videbæk 2015]. The 10% rule itself did not protect novices in a trial [seen: Buist 2008], but jumps of more than about 30% over two weeks are a plausible warning sign [seen: Nielsen 2014]. Repeating a week costs nothing.

**Deload.** None scheduled: repeating a week is the deload.

**Graduates to.** `run-base-3to5` once you can run 30 minutes.

**Evidence: C.** A public health programme with huge uptake, not a trial; the injury numbers behind the gentle pace are a meta-analysis and a cohort [seen].

**Credit.** NHS Couch to 5K (nhs.uk, Better Health), free, with an app that talks you through every run.

## The data (the engine reads this block)

```json
{
  "id": "run-c25k-3",
  "name": "Couch to 5K",
  "family": "run",
  "draws_from": [
    "NHS Couch to 5K",
    "Videbæk 2015",
    "Nielsen 2014"
  ],
  "goals": {
    "muscle": 0,
    "strength": 0,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 1,
    "run": 3,
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
    25,
    45
  ],
  "express_minutes": 20,
  "equipment_all": [],
  "equipment_any": [
    [
      "outdoors",
      "treadmill"
    ]
  ],
  "skills_required": [],
  "excluded_for": [
    "pregnancy",
    "seated",
    "low_bone_density"
  ],
  "evidence": "C",
  "simplicity": 1,
  "graduates_to": [
    "run-base-3to5"
  ],
  "block_weeks": 9,
  "deload": null,
  "meso": null,
  "layouts": {
    "2": [
      "A"
    ],
    "3": [
      "A"
    ]
  },
  "modules": [
    "mobility"
  ],
  "sessions": {
    "A": {
      "title": "Run and walk",
      "tags": [],
      "blocks": [
        {
          "name": "Run",
          "kind": "main",
          "format": "run",
          "slots": [
            {
              "key": "c25k",
              "pattern": "cyclic",
              "prefer": [
                "run_walk",
                "run"
              ],
              "sets": 1,
              "reps": "the week's run",
              "rest": 0,
              "effort": "slow enough to talk. Walk where it says walk",
              "rule": "c25k_week",
              "score": true,
              "table": [
                [
                  "8 x (1 min run, 1:30 walk), 5 min brisk walk before and after",
                  "8 x (1 min run, 1:30 walk), 5 min brisk walk before and after",
                  "8 x (1 min run, 1:30 walk), 5 min brisk walk before and after"
                ],
                [
                  "6 x (1:30 run, 2 min walk), 5 min brisk walk before and after",
                  "6 x (1:30 run, 2 min walk), 5 min brisk walk before and after",
                  "6 x (1:30 run, 2 min walk), 5 min brisk walk before and after"
                ],
                [
                  "2 x (1:30 run, 1:30 walk, 3 min run, 3 min walk), 5 min brisk walk before and after",
                  "2 x (1:30 run, 1:30 walk, 3 min run, 3 min walk), 5 min brisk walk before and after",
                  "2 x (1:30 run, 1:30 walk, 3 min run, 3 min walk), 5 min brisk walk before and after"
                ],
                [
                  "3 min run, 1:30 walk, 5 min run, 2:30 walk, 3 min run, 1:30 walk, 5 min run, 5 min brisk walk before and after",
                  "3 min run, 1:30 walk, 5 min run, 2:30 walk, 3 min run, 1:30 walk, 5 min run, 5 min brisk walk before and after",
                  "3 min run, 1:30 walk, 5 min run, 2:30 walk, 3 min run, 1:30 walk, 5 min run, 5 min brisk walk before and after"
                ],
                [
                  "3 x (5 min run, 3 min walk), 5 min brisk walk before and after",
                  "2 x (8 min run, 5 min walk), 5 min brisk walk before and after",
                  "20 min run, 5 min brisk walk before and after"
                ],
                [
                  "5 min run, 3 min walk, 8 min run, 3 min walk, 5 min run, 5 min brisk walk before and after",
                  "2 x (10 min run, 3 min walk), 5 min brisk walk before and after",
                  "25 min run, 5 min brisk walk before and after"
                ],
                [
                  "25 min run, 5 min brisk walk before and after",
                  "25 min run, 5 min brisk walk before and after",
                  "25 min run, 5 min brisk walk before and after"
                ],
                [
                  "28 min run, 5 min brisk walk before and after",
                  "28 min run, 5 min brisk walk before and after",
                  "28 min run, 5 min brisk walk before and after"
                ],
                [
                  "30 min run, 5 min brisk walk before and after",
                  "30 min run, 5 min brisk walk before and after",
                  "30 min run, 5 min brisk walk before and after"
                ]
              ]
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Short version · run and walk, short walks",
    "tags": [],
    "blocks": [
      {
        "name": "Run",
        "kind": "main",
        "format": "run",
        "slots": [
          {
            "key": "c25k",
            "pattern": "cyclic",
            "prefer": [
              "run_walk",
              "run"
            ],
            "sets": 1,
            "reps": "the week's run",
            "rest": 0,
            "effort": "the week's run as written, with the walks before and after cut to 3 min. Slow enough to talk",
            "rule": "c25k_week",
            "score": true,
            "table": [
              [
                "8 x (1 min run, 1:30 walk)",
                "8 x (1 min run, 1:30 walk)",
                "8 x (1 min run, 1:30 walk)"
              ],
              [
                "6 x (1:30 run, 2 min walk)",
                "6 x (1:30 run, 2 min walk)",
                "6 x (1:30 run, 2 min walk)"
              ],
              [
                "2 x (1:30 run, 1:30 walk, 3 min run, 3 min walk)",
                "2 x (1:30 run, 1:30 walk, 3 min run, 3 min walk)",
                "2 x (1:30 run, 1:30 walk, 3 min run, 3 min walk)"
              ],
              [
                "3 min run, 1:30 walk, 5 min run, 2:30 walk, 3 min run, 1:30 walk, 5 min run",
                "3 min run, 1:30 walk, 5 min run, 2:30 walk, 3 min run, 1:30 walk, 5 min run",
                "3 min run, 1:30 walk, 5 min run, 2:30 walk, 3 min run, 1:30 walk, 5 min run"
              ],
              [
                "3 x (5 min run, 3 min walk)",
                "2 x (8 min run, 5 min walk)",
                "20 min run"
              ],
              [
                "5 min run, 3 min walk, 8 min run, 3 min walk, 5 min run",
                "2 x (10 min run, 3 min walk)",
                "25 min run"
              ],
              [
                "25 min run",
                "25 min run",
                "25 min run"
              ],
              [
                "28 min run",
                "28 min run",
                "28 min run"
              ],
              [
                "30 min run",
                "30 min run",
                "30 min run"
              ]
            ]
          }
        ]
      }
    ]
  }
}
```
