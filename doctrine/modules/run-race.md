# Run race · run-race

For a 5 km to half marathon goal next to a strength program: up to three runs on the extra days, in this order: easy, long, quality. Most of it easy, one quality run, and the Daniels caps from his summaries [seen, secondary, research/03]: threshold about 10% of weekly volume or a steady 20 min tempo, intervals at most 8% of the week or 10 km, the long run at most 25 to 30% of the week and never past 150 min. Keep the quality run away from heavy legs: a day apart is best, same day only at least 3 hours apart with the priority first [snippet: Schumann 2022, Petré 2021].

## The data (the engine reads this block)

```json
{
  "id": "run-race",
  "name": "Run race",
  "when": "extra_day",
  "minutes": 50,
  "sessions": {
    "easy": {
      "title": "Easy run",
      "tags": [],
      "blocks": [
        {
          "name": "Run",
          "kind": "main",
          "format": "run",
          "slots": [
            {
              "key": "mod_race_easy",
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
              "per_week": 1,
              "max_minutes": 60,
              "score": true
            }
          ]
        }
      ]
    },
    "long": {
      "title": "Long run",
      "tags": [],
      "blocks": [
        {
          "name": "Run",
          "kind": "main",
          "format": "run",
          "slots": [
            {
              "key": "mod_race_long",
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
    },
    "quality": {
      "title": "Quality run",
      "tags": [
        "hard_cardio"
      ],
      "blocks": [
        {
          "name": "Quality",
          "kind": "main",
          "format": "intervals",
          "minutes": 45,
          "slots": [
            {
              "key": "mod_race_quality",
              "kind": "piece",
              "format": "fortime",
              "minutes": 45,
              "rule": "benchmark",
              "score": true,
              "effort": "10 to 15 min easy first and 10 min easy after. Threshold about 10% of your week, intervals at most 8%",
              "pieces": [
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "easy_run"
                    ],
                    "reps": "25 min easy plus 6 x 20 s strides, walk back"
                  }
                ],
                [
                  {
                    "pattern": "cyclic",
                    "prefer": [
                      "run",
                      "interval_run"
                    ],
                    "reps": "20 min tempo, comfortably hard"
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
                    "reps": "3 x 10 min at threshold, 2 min jog between"
                  }
                ]
              ]
            }
          ]
        }
      ]
    }
  },
  "order": [
    "easy",
    "long",
    "quality"
  ]
}
```
