# Travel day · travel

The day the main block cannot be filled: a hotel room, no kit, a broken machine. A full body bodyweight session, about 30 minutes, the same every time, and nothing progresses: the program's loads are kept for when you are back. Three rounds of a circuit, 2 or 3 reps left on every set. Seated people get seated moves where the bank has them.

## The data (the engine reads this block)

```json
{
  "id": "travel",
  "name": "Travel day",
  "when": "replace",
  "minutes": 30,
  "session": {
    "title": "Travel day · bodyweight full body",
    "tags": [],
    "blocks": [
      {
        "name": "Circuit",
        "kind": "main",
        "format": "circuit",
        "minutes": 25,
        "slots": [
          {
            "key": "mod_travel_squat",
            "pattern": "squat",
            "prefer": [
              "bodyweight_squat",
              "split_squat",
              "sit_to_stand"
            ],
            "sets": 3,
            "reps": "15",
            "rest": 30,
            "effort": "2 or 3 left",
            "rule": "fixed"
          },
          {
            "key": "mod_travel_push",
            "pattern": "h_push",
            "prefer": [
              "push_up",
              "incline_push_up",
              "knee_push_up",
              "seated_band_chest_press"
            ],
            "sets": 3,
            "reps": "10",
            "rest": 30,
            "effort": "2 or 3 left",
            "rule": "fixed"
          },
          {
            "key": "mod_travel_hinge",
            "pattern": "hinge",
            "prefer": [
              "single_leg_glute_bridge",
              "glute_bridge",
              "hip_hinge_drill"
            ],
            "sets": 3,
            "reps": "12",
            "rest": 30,
            "effort": "2 or 3 left, pause at the top",
            "rule": "fixed"
          },
          {
            "key": "mod_travel_pull",
            "pattern": "h_pull",
            "prefer": [
              "inverted_row",
              "band_row",
              "seated_band_row",
              "incline_inverted_row"
            ],
            "sets": 3,
            "reps": "10",
            "rest": 30,
            "effort": "2 or 3 left. A sturdy table edge works",
            "rule": "fixed"
          },
          {
            "key": "mod_travel_lunge",
            "pattern": "lunge",
            "prefer": [
              "reverse_lunge",
              "walking_lunge",
              "step_up"
            ],
            "sets": 3,
            "reps": "10",
            "rest": 30,
            "effort": "each leg, 2 or 3 left",
            "rule": "fixed"
          },
          {
            "key": "mod_travel_core",
            "pattern": "anti_ext",
            "prefer": [
              "plank",
              "dead_bug",
              "bird_dog"
            ],
            "sets": 3,
            "reps": "30 s",
            "rest": 30,
            "effort": "low back still",
            "rule": "fixed"
          }
        ]
      }
    ]
  }
}
```
