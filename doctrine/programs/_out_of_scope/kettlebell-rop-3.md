# Kettlebell Rite of Passage · kettlebell-rop-3

**What it is.** Pavel Tsatsouline's Rite of Passage from Enter the Kettlebell: clean and press ladders alternated with pull-up ladders, three days a week as heavy, light and medium days, with swings on the non-heavy days [seen, research/03 C2].

**Who it is for.** Novice to intermediate, one kettlebell and a pull-up bar, wants pressing strength and a strong back with conditioning on the side. Exactly 3 days a week, 30 to 60 minutes.

**The week.** Heavy, Light, Medium, in that order.

| session | ladders | then |
|:-|:-|:-|
| Heavy | clean and press ladders, up to 5 ladders of 1, 2, 3, 4, 5 · a pull-up ladder after each | nothing |
| Light | the same number of ladders, stopping 2 rungs lower | swings, minutes by a die roll |
| Medium | the same number of ladders, stopping 1 rung lower | swings, minutes by a die roll |

A ladder is a set of 1, a short rest, a set of 2, a rest, a set of 3, and so on: then start again. Press one arm and switch to the other each rung. Do one ladder of pull-ups after each press ladder, matched rung for rung. Light days run at about 50 to 60% of the heavy day's reps [seen]. Variety days for other drills are allowed [seen], the engine leaves them to you.

**How it climbs.** Add a ladder each week until you can do 5 ladders, then add rungs up to 5 (5 ladders of 1 to 5) [seen]. The engine reads it as double progression: the sets are ladders, the reps are the top rung, and when all 5 ladders reach the fifth rung it offers the next bell. The rung counts differ a little between sources [seen], so treat the rung plan as a guide.

The goals the book sets: press a bell half your bodyweight, and for men snatch 24 kg 200 times in 10 minutes [seen].

**Deload.** None scheduled: the light and medium days are the deload built into every week.

**Graduates to.** `kettlebell-ss-5` for a lower-skill daily practice, or a heavier bell and a second round of the same program.

**Evidence: C.** Coach method from a book; no trial [research/03 C2].

**Credit.** Rite of Passage is from Enter the Kettlebell! by Pavel Tsatsouline (Dragon Door, 2006). Buy the book, and learn the clean and press from a StrongFirst instructor (strongfirst.com). This file only describes the public outline of the plan.

## The data (the engine reads this block)

```json
{
  "id": "kettlebell-rop-3",
  "name": "Kettlebell Rite of Passage",
  "family": "kettlebell",
  "draws_from": [
    "Enter the Kettlebell, Rite of Passage (Pavel Tsatsouline, 2006)"
  ],
  "goals": {
    "muscle": 2,
    "strength": 2,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 2,
    "hyrox": 0,
    "run": 0,
    "skills": 1,
    "fat_loss": 2,
    "health": 2,
    "independent": 3
  },
  "experience": [
    "novice",
    "intermediate"
  ],
  "days": [
    3,
    3
  ],
  "sweet_days": [
    3
  ],
  "minutes": [
    30,
    60
  ],
  "express_minutes": 20,
  "equipment_all": [
    "kettlebell",
    "pullup_bar"
  ],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [
    "seated"
  ],
  "evidence": "C",
  "simplicity": 2,
  "graduates_to": [
    "kettlebell-ss-5"
  ],
  "block_weeks": 6,
  "deload": null,
  "meso": null,
  "layouts": {
    "3": [
      "Heavy",
      "Light",
      "Medium"
    ]
  },
  "modules": [],
  "sessions": {
    "Heavy": {
      "title": "Heavy · clean and press ladders · pull-ups",
      "tags": [],
      "blocks": [
        {
          "name": "Ladders",
          "kind": "main",
          "format": "superset",
          "rest_after_round": 60,
          "slots": [
            {
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "kb_press"
              ],
              "sets": 5,
              "reps": "3-5",
              "rest": 60,
              "effort": "clean before every press. A ladder is 1 rep, rest, 2 reps, rest, 3 reps, then start again: the sets are ladders, the reps are the top rung. Week 1 do 3 ladders, add one a week to 5, then add rungs up to 5",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "pull",
              "pattern": "v_pull",
              "prefer": [
                "pull_up",
                "chin_up",
                "negative_pull_up",
                "assisted_pull_up",
                "band_lat_pulldown"
              ],
              "sets": 5,
              "reps": "3-5",
              "rest": 60,
              "effort": "same ladders as the press, one ladder of pull-ups after each press ladder",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "Light": {
      "title": "Light · short ladders · swings",
      "tags": [
        "hinge_heavy"
      ],
      "blocks": [
        {
          "name": "Ladders",
          "kind": "main",
          "format": "superset",
          "rest_after_round": 60,
          "slots": [
            {
              "key": "press_l",
              "pattern": "v_push",
              "prefer": [
                "kb_press"
              ],
              "sets": 5,
              "reps": "2-3",
              "rest": 60,
              "effort": "your heavy day bell, ladders stopping 2 rungs below heavy day, clean before every press",
              "rule": "fixed"
            },
            {
              "key": "pull_l",
              "pattern": "v_pull",
              "prefer": [
                "pull_up",
                "chin_up",
                "negative_pull_up",
                "assisted_pull_up",
                "band_lat_pulldown"
              ],
              "sets": 5,
              "reps": "2-3",
              "rest": 60,
              "effort": "ladders to match today's press",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Swings",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "swings",
              "pattern": "hinge",
              "prefer": [
                "kb_swing"
              ],
              "sets": 1,
              "reps": "minutes by a die roll",
              "rest": 0,
              "effort": "roll a die for the minutes, swing in easy sets, alternate hands, stop before form slips",
              "rule": "fixed"
            }
          ]
        }
      ]
    },
    "Medium": {
      "title": "Medium · ladders · swings",
      "tags": [
        "hinge_heavy"
      ],
      "blocks": [
        {
          "name": "Ladders",
          "kind": "main",
          "format": "superset",
          "rest_after_round": 60,
          "slots": [
            {
              "key": "press_m",
              "pattern": "v_push",
              "prefer": [
                "kb_press"
              ],
              "sets": 5,
              "reps": "3-4",
              "rest": 60,
              "effort": "your heavy day bell, ladders stopping 1 rung below heavy day, clean before every press",
              "rule": "fixed"
            },
            {
              "key": "pull_l",
              "pattern": "v_pull",
              "prefer": [
                "pull_up",
                "chin_up",
                "negative_pull_up",
                "assisted_pull_up",
                "band_lat_pulldown"
              ],
              "sets": 5,
              "reps": "3-4",
              "rest": 60,
              "effort": "ladders to match today's press",
              "rule": "fixed"
            }
          ]
        },
        {
          "name": "Swings",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "swings",
              "pattern": "hinge",
              "prefer": [
                "kb_swing"
              ],
              "sets": 1,
              "reps": "minutes by a die roll",
              "rest": 0,
              "effort": "roll a die for the minutes, swing in easy sets, alternate hands, stop before form slips",
              "rule": "fixed"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · three short ladders and swings",
    "tags": [
      "hinge_heavy"
    ],
    "blocks": [
      {
        "name": "Ladders",
        "kind": "main",
        "format": "superset",
        "rest_after_round": 60,
        "slots": [
          {
            "key": "press_l",
            "pattern": "v_push",
            "prefer": [
              "kb_press"
            ],
            "sets": 3,
            "reps": "2-3",
            "rest": 60,
            "effort": "your heavy day bell, ladders stopping 2 rungs below heavy day, clean before every press",
            "rule": "fixed"
          },
          {
            "key": "pull_l",
            "pattern": "v_pull",
            "prefer": [
              "pull_up",
              "chin_up",
              "negative_pull_up",
              "assisted_pull_up",
              "band_lat_pulldown"
            ],
            "sets": 3,
            "reps": "2-3",
            "rest": 60,
            "effort": "ladders to match today's press",
            "rule": "fixed"
          }
        ]
      },
      {
        "name": "Swings",
        "kind": "secondary",
        "format": "straight",
        "slots": [
          {
            "key": "swings",
            "pattern": "hinge",
            "prefer": [
              "kb_swing"
            ],
            "sets": 1,
            "reps": "5 min",
            "rest": 0,
            "effort": "roll a die for the minutes, swing in easy sets, alternate hands, stop before form slips",
            "rule": "fixed"
          }
        ]
      }
    ]
  }
}
```
