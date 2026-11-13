# Mobility finisher · mobility

5 to 8 minutes for the joints the session used: hips, thoracic spine, ankles, shoulders. Slow, easy, never forced: move to tightness, not to pain. Fixed work, nothing progresses. Seated versions exist for anyone training in a chair. Static holds of 10 to 30 s (30 to 60 s for older adults) are the long standing ACSM value [believe: research/04].

## The data (the engine reads this block)

```json
{
  "id": "mobility",
  "name": "Mobility finisher",
  "when": "finisher",
  "minutes": 6,
  "session": {
    "title": "Mobility finisher",
    "tags": [],
    "blocks": [
      {
        "name": "Mobility",
        "kind": "finisher",
        "format": "circuit",
        "minutes": 6,
        "slots": [
          {
            "key": "mod_mob_hips",
            "pattern": "mobility",
            "prefer": [
              "worlds_greatest_stretch",
              "hip_90_90",
              "couch_stretch"
            ],
            "sets": 1,
            "reps": "5 each side",
            "rest": 0,
            "effort": "slow, to tightness, never pain",
            "rule": "fixed"
          },
          {
            "key": "mod_mob_spine",
            "pattern": "mobility",
            "prefer": [
              "thoracic_rotation",
              "cat_cow",
              "seated_thoracic_rotation"
            ],
            "sets": 1,
            "reps": "8 each side",
            "rest": 0,
            "effort": "breathe out as you turn",
            "rule": "fixed"
          },
          {
            "key": "mod_mob_ankles",
            "pattern": "mobility",
            "prefer": [
              "ankle_rocks",
              "couch_stretch"
            ],
            "sets": 1,
            "reps": "10 each side",
            "rest": 0,
            "effort": "knee over the toes, heel down",
            "rule": "fixed"
          },
          {
            "key": "mod_mob_shoulders",
            "pattern": "mobility",
            "prefer": [
              "band_shoulder_dislocate",
              "cat_cow",
              "seated_thoracic_rotation"
            ],
            "sets": 1,
            "reps": "10",
            "rest": 0,
            "effort": "wide grip, slow, arms straight",
            "rule": "fixed"
          }
        ]
      }
    ]
  }
}
```
