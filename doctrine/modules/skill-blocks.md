# Skill blocks · skill-blocks

About 10 minutes of skill work for calisthenics: a handstand line, a pull line and a single leg squat line. Each slot is a ladder: start at the hardest step you can do for 3 sets of 5 with clean form, add reps until 3 sets of 8, then move to the next step [seen: Bodyweight Fitness Recommended Routine, research/03]. Done fresh if it can be, as a finisher otherwise. Skill work stops while it is still clean, never to failure.

## The data (the engine reads this block)

```json
{
  "id": "skill-blocks",
  "name": "Bodyweight skills",
  "when": "finisher",
  "minutes": 10,
  "session": {
    "title": "Bodyweight skills",
    "tags": [],
    "blocks": [
      {
        "name": "Skills",
        "kind": "finisher",
        "format": "straight",
        "slots": [
          {
            "key": "mod_skill_handstand",
            "pattern": "v_push",
            "prefer": [
              "wall_handstand_hold",
              "pike_push_up",
              "handstand_push_up_wall"
            ],
            "sets": 3,
            "reps": "5-8",
            "rest": 60,
            "effort": "clean every rep, stop before it gets ugly",
            "rule": "ladder_step"
          },
          {
            "key": "mod_skill_pull",
            "pattern": "v_pull",
            "prefer": [
              "scap_pull",
              "negative_pull_up",
              "pull_up"
            ],
            "sets": 3,
            "reps": "5-8",
            "rest": 60,
            "effort": "full hang to full height, slow down",
            "rule": "ladder_step"
          },
          {
            "key": "mod_skill_pistol",
            "pattern": "squat",
            "prefer": [
              "assisted_squat",
              "shrimp_squat",
              "pistol_squat"
            ],
            "sets": 3,
            "reps": "5-8",
            "rest": 60,
            "effort": "each leg, hold a support as needed",
            "rule": "ladder_step"
          }
        ]
      }
    ]
  }
}
```
