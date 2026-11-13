# Novice weightlifting · weightlifting-novice-3

**What it is.** A first program for the snatch and the clean and jerk, built the way Catalyst Athletics lays out a session: a classic lift variant first, then a pull, then a squat. Hang and power variants come first, the full lifts from the floor only once they are clean. Light day, clean and jerk day, heavier day, and a fourth jerk and squat day on 4 days a week.

**Who it is for.** Someone who has been taught the lifts by a coach, or has had their lifts checked on video. That is a hard gate: without it this program is never served, and the trainer teaches the lifts top down with PVC and the high hang instead [research/02, rule 1]. 3 or 4 days a week, 60 to 90 minutes, a barbell, a rack and plates (bumpers if you will drop the bar).

**The week.** A, B, C on 3 days. A, B, C, D on 4 days.

| session | classic lift first | then a pull | then a squat |
|:-|:-|:-|:-|
| A | hang power snatch 6 x 3 | snatch pull 4 x 3 | front squat 4 x 3 to 5 |
| B | hang power clean 5 x 3 · push jerk 5 x 2 | clean pull 4 x 3 | back squat 4 x 5 |
| C | power snatch 6 x 2 · power clean 6 x 2 | clean pull 4 x 3 | front squat 4 x 3 to 5 |
| D | push jerk 5 x 2 | snatch pull 4 x 3 | back squat 4 x 5 · overhead squat 3 x 3 |

When the full lift is not available (no coaching yet on it, or no room to drop), each slot falls back down its list: power and hang variants, then the muscle snatch, then the PVC snatch drill.

**How it climbs.** Most work sits at 70 to 85% of your best [snippet: Soviet summaries, research/02]. The volume per lift per session is capped by Prilepin's chart: at 70 to 80%, 3 to 6 reps a set and about 18 in total; at 80 to 90%, 2 to 4 reps a set and about 15 in total [snippet, research/02]. Session A's 6 x 3 is the 18 rep day, session C's 6 x 2 sits inside the 10 to 20 range of the heavier row. The chart is a guide from Soviet lifter logs, not a trial, and its 90%+ row disagrees across copies, so this program does not go there. Every slot climbs by double progression: when every rep of every set was fast and clean, the weight goes up next time. Speed is the test, not grinding: stop the set when the bar slows.

**Deload.** Catalyst uses 4 week blocks with a lighter week [believe, research/02]: three weeks of work, then one week at half the sets, 90% of the load, 4 reps left in the tank.

**Graduates to.** A coach, or a paid Catalyst program for your level (Everett: an advanced program will not make you advanced [snippet]).

**Evidence: C.** Coach consensus (Catalyst, USAW teaching, Prilepin) built on large observational datasets of Soviet lifters, some of them confounded by doping [snippet, research/02]. No trial of a novice weightlifting template. Technique is the limiter, and a coach or video review is the consensus [research/02].

**Credit.** The session shape follows Greg Everett's Catalyst Athletics (catalystathletics.com, and *Olympic Weightlifting: A Complete Guide for Athletes and Coaches*). The real programs are paid, on TrainHeroic; nothing here is copied from them. Buy the book or a Catalyst program for the real thing.

## The data (the engine reads this block)

```json
{
  "id": "weightlifting-novice-3",
  "name": "Novice weightlifting",
  "family": "weightlifting",
  "draws_from": [
    "Catalyst Athletics",
    "Prilepin's chart",
    "USAW top down teaching"
  ],
  "goals": {
    "muscle": 1,
    "strength": 2,
    "powerlifting": 0,
    "weightlifting": 3,
    "functional": 2,
    "hyrox": 0,
    "run": 0,
    "skills": 1,
    "fat_loss": 1,
    "health": 1,
    "independent": 1
  },
  "experience": [
    "novice",
    "intermediate"
  ],
  "days": [
    3,
    4
  ],
  "sweet_days": [
    3
  ],
  "minutes": [
    60,
    90
  ],
  "express_minutes": 35,
  "equipment_all": [
    "barbell",
    "rack",
    "plates"
  ],
  "equipment_any": [],
  "skills_required": [
    "olympic_coached"
  ],
  "excluded_for": [
    "pregnancy",
    "seated"
  ],
  "evidence": "C",
  "simplicity": 2,
  "graduates_to": [],
  "block_weeks": 3,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 0.9,
    "rir": "4"
  },
  "meso": null,
  "layouts": {
    "3": [
      "A",
      "B",
      "C"
    ],
    "4": [
      "A",
      "B",
      "C",
      "D"
    ]
  },
  "modules": [
    "mobility"
  ],
  "sessions": {
    "A": {
      "title": "Snatch · Snatch pull · Front squat",
      "tags": [
        "power",
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "Classic lift",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "snatch",
              "pattern": "olympic",
              "prefer": [
                "hang_power_snatch",
                "power_snatch",
                "snatch",
                "muscle_snatch",
                "pvc_snatch_drill"
              ],
              "sets": 6,
              "reps": "3",
              "rest": 150,
              "effort": "fast every rep: stop the set when the bar slows. About 70 to 80%, 18 reps in all",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Pull",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "snatch_pull",
              "pattern": "olympic",
              "prefer": [
                "snatch_pull"
              ],
              "sets": 4,
              "reps": "3",
              "rest": 150,
              "effort": "snatch grip, finish tall and fast, a little heavier than your best snatch",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Squat",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "front_squat",
              "pattern": "squat",
              "prefer": [
                "front_squat",
                "goblet_squat"
              ],
              "sets": 4,
              "reps": "3-5",
              "rest": 180,
              "effort": "2 left, elbows high",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "B": {
      "title": "Clean · Jerk · Clean pull · Back squat",
      "tags": [
        "power",
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "Classic lift",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "clean",
              "pattern": "olympic",
              "prefer": [
                "hang_power_clean",
                "power_clean",
                "clean",
                "db_hang_clean"
              ],
              "sets": 5,
              "reps": "3",
              "rest": 150,
              "effort": "fast every rep: stop the set when the bar slows. About 70 to 80%",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "jerk",
              "pattern": "olympic",
              "prefer": [
                "push_jerk",
                "split_jerk"
              ],
              "sets": 5,
              "reps": "2",
              "rest": 150,
              "effort": "fast every rep: stop the set when the bar slows. Dip straight down, drive straight up",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Pull",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "clean_pull",
              "pattern": "olympic",
              "prefer": [
                "clean_pull"
              ],
              "sets": 4,
              "reps": "3",
              "rest": 150,
              "effort": "clean grip, finish tall and fast, a little heavier than your best clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Squat",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "back_squat",
              "pattern": "squat",
              "prefer": [
                "back_squat",
                "front_squat"
              ],
              "sets": 4,
              "reps": "5",
              "rest": 180,
              "effort": "2 left, upright",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "C": {
      "title": "Heavier snatch and clean · Clean pull · Front squat",
      "tags": [
        "power",
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "Classic lift",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "snatch_heavy",
              "pattern": "olympic",
              "prefer": [
                "power_snatch",
                "hang_power_snatch",
                "snatch",
                "muscle_snatch",
                "pvc_snatch_drill"
              ],
              "sets": 6,
              "reps": "2",
              "rest": 180,
              "effort": "fast every rep: stop the set when the bar slows. About 80 to 85%, 12 reps in all",
              "rule": "double_progression",
              "score": true
            },
            {
              "key": "clean_heavy",
              "pattern": "olympic",
              "prefer": [
                "power_clean",
                "hang_power_clean",
                "clean_and_jerk",
                "clean",
                "db_hang_clean"
              ],
              "sets": 6,
              "reps": "2",
              "rest": 180,
              "effort": "fast every rep: stop the set when the bar slows. About 80 to 85%, 12 reps in all",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Pull",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "clean_pull",
              "pattern": "olympic",
              "prefer": [
                "clean_pull"
              ],
              "sets": 4,
              "reps": "3",
              "rest": 150,
              "effort": "clean grip, finish tall and fast, a little heavier than your best clean",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Squat",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "front_squat",
              "pattern": "squat",
              "prefer": [
                "front_squat",
                "goblet_squat"
              ],
              "sets": 4,
              "reps": "3-5",
              "rest": 180,
              "effort": "2 left, elbows high",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "D": {
      "title": "Jerk · Snatch pull · Back squat · Overhead squat",
      "tags": [
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "Classic lift",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "jerk",
              "pattern": "olympic",
              "prefer": [
                "push_jerk",
                "split_jerk"
              ],
              "sets": 5,
              "reps": "2",
              "rest": 150,
              "effort": "fast every rep: stop the set when the bar slows. Dip straight down, drive straight up",
              "rule": "double_progression",
              "score": true
            }
          ]
        },
        {
          "name": "Pull",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "snatch_pull",
              "pattern": "olympic",
              "prefer": [
                "snatch_pull"
              ],
              "sets": 4,
              "reps": "3",
              "rest": 150,
              "effort": "snatch grip, finish tall and fast, a little heavier than your best snatch",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Squat",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "back_squat",
              "pattern": "squat",
              "prefer": [
                "back_squat",
                "front_squat"
              ],
              "sets": 4,
              "reps": "5",
              "rest": 180,
              "effort": "2 left, upright",
              "rule": "double_progression"
            }
          ]
        },
        {
          "name": "Accessory",
          "kind": "accessory",
          "format": "straight",
          "slots": [
            {
              "key": "ohs",
              "pattern": "olympic",
              "prefer": [
                "overhead_squat",
                "pvc_snatch_drill"
              ],
              "sets": 3,
              "reps": "3",
              "rest": 120,
              "effort": "slow down, pause at the bottom, bar over the middle of the foot",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · Snatch · Front squat",
    "tags": [
      "power",
      "heavy_legs"
    ],
    "blocks": [
      {
        "name": "Classic lift",
        "kind": "main",
        "format": "straight",
        "slots": [
          {
            "key": "snatch",
            "pattern": "olympic",
            "prefer": [
              "hang_power_snatch",
              "power_snatch",
              "snatch",
              "muscle_snatch",
              "pvc_snatch_drill"
            ],
            "sets": 4,
            "reps": "3",
            "rest": 150,
            "effort": "fast every rep: stop the set when the bar slows. About 70 to 80%",
            "rule": "double_progression",
            "score": true
          }
        ]
      },
      {
        "name": "Squat",
        "kind": "secondary",
        "format": "straight",
        "slots": [
          {
            "key": "front_squat",
            "pattern": "squat",
            "prefer": [
              "front_squat",
              "goblet_squat"
            ],
            "sets": 3,
            "reps": "3-5",
            "rest": 150,
            "effort": "2 left, elbows high",
            "rule": "double_progression"
          }
        ]
      }
    ]
  }
}
```
