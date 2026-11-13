# Core finisher · core

Two trunk moves, 2 to 3 rounds, about 6 minutes at the end of a session: one that resists the low back arching (anti-extension), one that resists twisting (anti-rotation). Slow reps, the trunk stays still. Double progression: reach the top of the range on every set and the sheet gives the harder variant next time. Floor and seated versions exist, so it works anywhere.

## The data (the engine reads this block)

```json
{
  "id": "core",
  "name": "Core finisher",
  "when": "finisher",
  "minutes": 6,
  "session": {
    "title": "Core finisher",
    "tags": [],
    "blocks": [
      {
        "name": "Core",
        "kind": "finisher",
        "format": "superset",
        "rest_after_round": 45,
        "slots": [
          {
            "key": "mod_core_ext",
            "pattern": "anti_ext",
            "prefer": [
              "dead_bug",
              "plank",
              "hollow_hold",
              "ab_wheel",
              "bird_dog"
            ],
            "sets": 3,
            "reps": "8-12",
            "rest": 30,
            "effort": "slow, low back still, 2 left",
            "rule": "double_progression"
          },
          {
            "key": "mod_core_rot",
            "pattern": "anti_rot",
            "prefer": [
              "pallof_press",
              "band_pallof_press",
              "side_plank",
              "seated_band_rotation"
            ],
            "sets": 3,
            "reps": "8-12",
            "rest": 30,
            "effort": "each side, no twist, 2 left",
            "rule": "double_progression"
          }
        ]
      }
    ]
  }
}
```
