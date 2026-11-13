# Easy running · easy-running

An easy run on the days a person trains beyond what their program uses. Easy by the talk test: full sentences the whole way [seen: talk test validity, research/03]. Starts at 20 minutes, holds about 3 weeks, then adds about 10%, never past 60 minutes here [seen, secondary: Daniels]. Not on the day after heavy legs if it can be helped; same day only at least 3 hours apart [snippet: Schumann 2022].

## The data (the engine reads this block)

```json
{
  "id": "easy-running",
  "name": "Easy run",
  "when": "extra_day",
  "minutes": 30,
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
              "key": "mod_easy_run",
              "pattern": "cyclic",
              "prefer": [
                "easy_run",
                "run",
                "bike_erg"
              ],
              "sets": 1,
              "reps": "20 min",
              "rest": 0,
              "effort": "talk test: full sentences the whole way",
              "rule": "run_volume",
              "start_minutes": 20,
              "per_week": 1,
              "max_minutes": 60,
              "score": true
            }
          ]
        }
      ]
    }
  },
  "order": [
    "easy"
  ]
}
```
