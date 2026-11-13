# Conditioning finisher · conditioning

6 to 10 minutes of intervals on whatever cardio machine is there, or bodyweight when there is none. Four versions rotate, each one a benchmark: your best score on it is the one to beat. Hard but repeatable, the last interval as good as the first. When leg size is a goal, the bike or the rower is the better choice than running [snippet: Wilson 2012, Lundberg 2022, research/02], so they come first in the lists. Not after a heavy leg day if a hard run is tomorrow.

## The data (the engine reads this block)

```json
{
  "id": "conditioning",
  "name": "Conditioning finisher",
  "when": "finisher",
  "minutes": 8,
  "session": {
    "title": "Conditioning finisher",
    "tags": [
      "hard_cardio"
    ],
    "blocks": [
      {
        "name": "Intervals",
        "kind": "finisher",
        "format": "intervals",
        "minutes": 8,
        "slots": [
          {
            "key": "mod_conditioning",
            "kind": "piece",
            "format": "emom",
            "minutes": 8,
            "rule": "benchmark",
            "score": true,
            "effort": "hard but repeatable. Score: total calories, metres or reps",
            "pieces": [
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "bike_erg",
                    "row_erg",
                    "ski_erg",
                    "jump_rope",
                    "burpee"
                  ],
                  "reps": "8 x (20 s hard, 40 s easy)"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "row_erg",
                    "bike_erg",
                    "ski_erg",
                    "burpee"
                  ],
                  "reps": "4 x (60 s hard, 60 s easy)"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "ski_erg",
                    "row_erg",
                    "bike_erg",
                    "jump_rope"
                  ],
                  "reps": "8 x (30 s hard, 30 s easy)"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "burpee",
                    "jump_rope"
                  ],
                  "reps": "8 min: 6 every minute on the minute"
                },
                {
                  "pattern": "squat",
                  "prefer": [
                    "bodyweight_squat"
                  ],
                  "reps": "10 in the same minute"
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
