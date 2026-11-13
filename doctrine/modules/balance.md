# Balance finisher · balance

Three balance moves, about 6 minutes, next to something solid you can grab. **Mandatory from 60:** the engine adds it to every session of anyone 60 or over, whatever the program, and never cuts it for time. The WHO asks older adults for multicomponent activity emphasising functional balance and strength on 3 or more days a week [checked: WHO 2020], and exercise cuts the rate of falls by 23% [checked: Sherrington 2019, Cochrane, 59 trials]. About 3 hours a week of balance challenging work has the largest effect [believe: Sherrington 2017/2019]. Holds do not progress by rule: make them harder yourself (eyes closed, a softer surface, a head turn) only when steady.

## The data (the engine reads this block)

```json
{
  "id": "balance",
  "name": "Balance finisher",
  "when": "finisher",
  "minutes": 6,
  "session": {
    "title": "Balance finisher",
    "tags": [],
    "blocks": [
      {
        "name": "Balance",
        "kind": "finisher",
        "format": "circuit",
        "minutes": 6,
        "slots": [
          {
            "key": "mod_bal_stand",
            "pattern": "balance",
            "prefer": [
              "single_leg_stand",
              "tandem_stance"
            ],
            "sets": 2,
            "reps": "30 s",
            "rest": 20,
            "effort": "each leg, a hand near the support",
            "rule": "fixed"
          },
          {
            "key": "mod_bal_walk",
            "pattern": "balance",
            "prefer": [
              "heel_to_toe_walk",
              "step_over",
              "tandem_stance"
            ],
            "sets": 2,
            "reps": "10 steps",
            "rest": 20,
            "effort": "slow, eyes ahead, along a wall",
            "rule": "fixed"
          },
          {
            "key": "mod_bal_reach",
            "pattern": "balance",
            "prefer": [
              "clock_reach",
              "turkish_get_up",
              "single_leg_stand"
            ],
            "sets": 2,
            "reps": "5",
            "rest": 20,
            "effort": "each side, only as far as you stay steady",
            "rule": "fixed"
          }
        ]
      }
    ]
  }
}
```
