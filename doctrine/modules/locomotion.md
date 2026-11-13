# Locomotion · locomotion

GMB-style crawls: bear (shoulders, overhead strength), monkey (lateral control), frogger (links upper and lower body), crab (hips and core, face up) [seen: GMB Elements, research/03]. Used as a finisher, or as the first 2 to 4 weeks for a deconditioned, older or returning person before ladders [seen for the content, believe for the 2 to 4 week bridge]. About 10 minutes here; GMB's own sample uses 15 minute blocks [seen]. Fixed work: the challenge goes up when you choose a harder variation, not by rule.

## The data (the engine reads this block)

```json
{
  "id": "locomotion",
  "name": "Locomotion",
  "when": "finisher",
  "minutes": 10,
  "session": {
    "title": "Locomotion",
    "tags": [],
    "blocks": [
      {
        "name": "Crawls",
        "kind": "finisher",
        "format": "circuit",
        "minutes": 10,
        "slots": [
          {
            "key": "mod_loco_bear",
            "pattern": "locomotion",
            "prefer": [
              "bear_crawl"
            ],
            "sets": 2,
            "reps": "30 s",
            "rest": 30,
            "effort": "knees low, back flat, slow",
            "rule": "fixed"
          },
          {
            "key": "mod_loco_monkey",
            "pattern": "locomotion",
            "prefer": [
              "monkey_walk"
            ],
            "sets": 2,
            "reps": "30 s",
            "rest": 30,
            "effort": "each direction, hips low",
            "rule": "fixed"
          },
          {
            "key": "mod_loco_frogger",
            "pattern": "locomotion",
            "prefer": [
              "frogger"
            ],
            "sets": 2,
            "reps": "5",
            "rest": 30,
            "effort": "hands down first, soft landing",
            "rule": "fixed"
          },
          {
            "key": "mod_loco_crab",
            "pattern": "locomotion",
            "prefer": [
              "crab_walk"
            ],
            "sets": 2,
            "reps": "30 s",
            "rest": 30,
            "effort": "hips up, shoulders away from the ears",
            "rule": "fixed"
          }
        ]
      }
    ]
  }
}
```
