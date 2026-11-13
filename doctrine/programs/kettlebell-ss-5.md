# Kettlebell Simple and Sinister · kettlebell-ss-5

**What it is.** One kettlebell, two moves, the same session most days: 100 one-arm swings (10 sets of 10, alternating hands) and 10 Turkish get-ups (alternating sides) [seen, research/03 C1]. The engine writes the warm-up (StrongFirst uses prying goblet squats, halos and hip bridges [believe]).

**Who it is for.** Anyone with a kettlebell and a few square metres who wants strength, conditioning and resilience without thinking about programming. 3 to 6 days a week, 5 is the sweet spot; 20 to 40 minutes. Learn the swing and the get-up from a coach or the book first: both are technical.

**The week.** SS every training day. It is meant to be done often, at an effort that leaves you fresher than you started [believe].

| block | work | the clock [seen] |
|:-|:-|:-|
| swings | 10 x 10 one-arm, alternate hands | a set every 30 s, 100 inside 5 min |
| rest | 1 min | |
| get-ups | 10 x 1, alternate sides | one a minute, 10 inside 10 min |

**How it climbs.** Stay at a bell until the whole session feels comfortable inside the times, then step up a size [seen]. The engine counts it: 3 sessions in a row inside the standard and the next bell is offered. The standards to aim for [seen, strongfirst.com via search extract]:

| | swing | get-up |
|:-|:-|:-|
| Simple, men | 32 kg | 32 kg |
| Simple, women | 24 kg | 16 kg |
| Sinister, men | 48 kg | 48 kg |
| Sinister, women | 32 kg | 24 kg |

StrongFirst's later advice mixes heavier and lighter bells inside a session on the way to the next size [believe]. The engine keeps it simple: one bell per move.

**Deload.** None scheduled. The program is built to be repeatable, and the light days are the ones where you do not chase the clock.

**Graduates to.** `kettlebell-rop-3` if you want pressing strength, or keep chasing Sinister.

**Evidence: C.** Coach method with no trial on Simple and Sinister itself [believe]; swing training has small trials for strength and power [believe].

**Credit.** Simple and Sinister is Pavel Tsatsouline's, StrongFirst. Read the book and the official page (strongfirst.com/sinister) and learn the moves at a StrongFirst course. This file only names the public session and standards.

## The data (the engine reads this block)

```json
{
  "id": "kettlebell-ss-5",
  "name": "Kettlebell Simple and Sinister",
  "family": "kettlebell",
  "draws_from": [
    "StrongFirst Simple and Sinister (Pavel Tsatsouline)"
  ],
  "goals": {
    "muscle": 1,
    "strength": 2,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 2,
    "hyrox": 1,
    "run": 0,
    "skills": 0,
    "fat_loss": 2,
    "health": 3,
    "independent": 3
  },
  "experience": [
    "novice",
    "intermediate",
    "advanced"
  ],
  "days": [
    3,
    6
  ],
  "sweet_days": [
    5
  ],
  "minutes": [
    20,
    40
  ],
  "express_minutes": 15,
  "equipment_all": [
    "kettlebell"
  ],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [
    "seated"
  ],
  "evidence": "C",
  "simplicity": 1,
  "graduates_to": [
    "kettlebell-rop-3"
  ],
  "block_weeks": 6,
  "deload": null,
  "meso": null,
  "layouts": {
    "3": [
      "SS"
    ],
    "4": [
      "SS"
    ],
    "5": [
      "SS"
    ],
    "6": [
      "SS"
    ]
  },
  "modules": [],
  "sessions": {
    "SS": {
      "title": "Simple and Sinister · swings · get-ups",
      "tags": [
        "hinge_heavy"
      ],
      "blocks": [
        {
          "name": "Swings",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "swing",
              "pattern": "hinge",
              "prefer": [
                "kb_swing"
              ],
              "sets": 10,
              "reps": "10",
              "rest": 15,
              "effort": "one-arm, alternate hands, a set every 30 s, 100 inside 5 min",
              "rule": "timed_standard",
              "standard": "100 swings in 5 min",
              "sessions_to_move": 3,
              "score": true
            }
          ]
        },
        {
          "name": "Get-ups",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "getup",
              "pattern": "balance",
              "prefer": [
                "turkish_get_up"
              ],
              "sets": 10,
              "reps": "1",
              "rest": 30,
              "effort": "alternate sides, one every minute, 10 inside 10 min",
              "rule": "timed_standard",
              "standard": "10 get-ups in 10 min",
              "sessions_to_move": 3
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · swings and a few get-ups",
    "tags": [
      "hinge_heavy"
    ],
    "blocks": [
      {
        "name": "Swings",
        "kind": "main",
        "format": "straight",
        "slots": [
          {
            "key": "swing",
            "pattern": "hinge",
            "prefer": [
              "kb_swing"
            ],
            "sets": 10,
            "reps": "10",
            "rest": 15,
            "effort": "one-arm, alternate hands, a set every 30 s, 100 inside 5 min",
            "rule": "timed_standard",
            "standard": "100 swings in 5 min",
            "sessions_to_move": 3,
            "score": true
          }
        ]
      },
      {
        "name": "Get-ups",
        "kind": "secondary",
        "format": "straight",
        "slots": [
          {
            "key": "getup_express",
            "pattern": "balance",
            "prefer": [
              "turkish_get_up"
            ],
            "sets": 4,
            "reps": "1",
            "rest": 30,
            "effort": "alternate sides, your get-up bell or one lighter, no clock",
            "rule": "fixed"
          }
        ]
      }
    ]
  }
}
```
