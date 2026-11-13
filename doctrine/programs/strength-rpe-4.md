# RPE upper lower · strength-rpe-4

**What it is.** Strength training run by effort instead of by a fixed percentage. Each main lift works up to one top set at RPE 8 (two reps left), the engine turns it into an estimated max, then three back off sets about 10% lighter. Four sessions, upper, lower, upper, lower.

**Who it is for.** Intermediate and advanced lifters who can tell honestly how many reps they had left. Novices misjudge that near a max (Zourdos 2016) [checked], so they are not offered this one. 3 or 4 days a week, 60 to 90 minutes, a barbell, a rack, a bench and plates.

**The week.** Upper A, Lower A, Upper B, Lower B, in order. On 3 days the rotation simply keeps going.

| session | main block | second lift | accessories |
|:-|:-|:-|:-|
| Upper A | bench press 3 @ RPE 8, then 3 x 3 | overhead press 3 x 6 to 8 | row 3 x 8 to 12 · triceps 3 x 10 to 15 |
| Lower A | squat 3 @ RPE 8, then 3 x 3 | Romanian deadlift 3 x 6 to 8 | split squat 3 x 8 to 12 · ab wheel 3 x 8 to 12 |
| Upper B | bench press 5 @ RPE 8, then 3 x 5 | close grip bench 3 x 6 to 8 | chin-ups 3 x 6 to 10 · lateral raise 3 x 12 to 15 |
| Lower B | deadlift 3 @ RPE 8, then 3 x 3 | front squat 3 x 5 to 8 | leg curl 3 x 10 to 15 · calves 3 x 10 to 15 |

**How it climbs.** The top set is read off the RTS chart: 3 reps at RPE 8 is about 86% of your max, 5 at RPE 8 about 81% [checked: RTS chart, research/01]. Each logged top set updates the estimated max, so the next prescription follows what you actually did, not a plan written weeks ago. The chart is a guide and drifts across a cycle, Tuchscherer says so himself [checked]. The back off sets sit 10% under the top set; RTS uses fatigue percents, often 3 to 9% [believe, not found in the research], so 10% is the conservative round number. The second lifts and accessories climb by double progression: top of the range on every set, then the smallest jump.

**Deload.** After 6 weeks, one week at half the sets, 90% of the load, 4 reps left. SBS templates deload at weeks 7 and 14 [checked via a review, research/01].

**Graduates to.** `powerbuild-phat-5` with more days, or a coach.

**Evidence: A to B.** RPE and RIR as a way to set daily load is backed by Zourdos 2016 and Helms 2018: in trained men, RPE loading matched %1RM for strength and muscle, with a small 1RM edge for RPE in most people [checked, research/01]. The fatigue percent method is coach practice.

**Credit.** The RPE method and chart are Mike Tuchscherer's (Reactive Training Systems, reactivetrainingsystems.com). The upper lower shape with RIR based progression borrows from Greg Nuckols' Stronger by Science programs (strongerbyscience.com). This file uses the public principles only. Buy their programs for the full thing.

## The data (the engine reads this block)

```json
{
  "id": "strength-rpe-4",
  "name": "RPE upper lower",
  "family": "strength",
  "draws_from": [
    "Reactive Training Systems",
    "Stronger by Science",
    "Helms 2018",
    "Zourdos 2016"
  ],
  "goals": {
    "muscle": 2,
    "strength": 3,
    "powerlifting": 3,
    "weightlifting": 0,
    "functional": 1,
    "hyrox": 0,
    "run": 0,
    "skills": 0,
    "fat_loss": 1,
    "health": 1,
    "independent": 1
  },
  "experience": [
    "intermediate",
    "advanced"
  ],
  "days": [
    3,
    4
  ],
  "sweet_days": [
    4
  ],
  "minutes": [
    60,
    90
  ],
  "express_minutes": 40,
  "equipment_all": [
    "barbell",
    "rack",
    "bench",
    "plates"
  ],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [
    "pregnancy",
    "seated"
  ],
  "evidence": "B",
  "simplicity": 4,
  "graduates_to": [
    "powerbuild-phat-5"
  ],
  "block_weeks": 6,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 0.9,
    "rir": "4"
  },
  "meso": null,
  "layouts": {
    "3": [
      "UpperA",
      "LowerA",
      "UpperB",
      "LowerB"
    ],
    "4": [
      "UpperA",
      "LowerA",
      "UpperB",
      "LowerB"
    ]
  },
  "modules": [],
  "sessions": {
    "UpperA": {
      "title": "Upper A · Bench top set · Press",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "bench",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 4,
              "reps": "3",
              "rest": 210,
              "effort": "top set of 3 with 2 left in the tank, then 3 x 3 about 10% lighter",
              "rule": "rpe_top_set",
              "top_reps": 3,
              "rpe": 8,
              "backoff_sets": 3,
              "fatigue_drop": 0.1,
              "score": true
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "press",
              "pattern": "v_push",
              "prefer": [
                "overhead_press",
                "db_shoulder_press"
              ],
              "sets": 3,
              "reps": "6-8",
              "rest": 150,
              "effort": "2 left",
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
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "chest_supported_row",
                "barbell_row",
                "db_row"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 90,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "triceps",
              "pattern": "triceps",
              "prefer": [
                "skull_crusher",
                "rope_pushdown",
                "overhead_db_triceps_extension"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LowerA": {
      "title": "Lower A · Squat top set · RDL",
      "tags": [
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "squat",
              "pattern": "squat",
              "prefer": [
                "back_squat"
              ],
              "sets": 4,
              "reps": "3",
              "rest": 210,
              "effort": "top set of 3 with 2 left in the tank, then 3 x 3 about 10% lighter",
              "rule": "rpe_top_set",
              "top_reps": 3,
              "rpe": 8,
              "backoff_sets": 3,
              "fatigue_drop": 0.1,
              "score": true
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "rdl",
              "pattern": "hinge",
              "prefer": [
                "romanian_deadlift",
                "db_romanian_deadlift"
              ],
              "sets": 3,
              "reps": "6-8",
              "rest": 150,
              "effort": "2 left",
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
              "key": "split_squat",
              "pattern": "lunge",
              "prefer": [
                "bulgarian_split_squat",
                "db_reverse_lunge"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 90,
              "effort": "2 left, each leg",
              "rule": "double_progression"
            },
            {
              "key": "core",
              "pattern": "anti_ext",
              "prefer": [
                "ab_wheel",
                "dead_bug",
                "plank"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 60,
              "effort": "slow, ribs down",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "UpperB": {
      "title": "Upper B · Bench top set of 5 · Close grip",
      "tags": [],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "bench",
              "pattern": "h_push",
              "prefer": [
                "bench_press"
              ],
              "sets": 4,
              "reps": "5",
              "rest": 210,
              "effort": "top set of 5 with 2 left in the tank, then 3 x 5 about 10% lighter",
              "rule": "rpe_top_set",
              "top_reps": 5,
              "rpe": 8,
              "backoff_sets": 3,
              "fatigue_drop": 0.1,
              "score": true
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "close_grip",
              "pattern": "h_push",
              "prefer": [
                "close_grip_bench",
                "incline_bench_press"
              ],
              "sets": 3,
              "reps": "6-8",
              "rest": 150,
              "effort": "2 left",
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
              "key": "chin",
              "pattern": "v_pull",
              "prefer": [
                "chin_up",
                "pull_up",
                "lat_pulldown"
              ],
              "sets": 3,
              "reps": "6-10",
              "rest": 90,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "delts",
              "pattern": "delts",
              "prefer": [
                "lateral_raise",
                "cable_lateral_raise"
              ],
              "sets": 3,
              "reps": "12-15",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            }
          ]
        }
      ]
    },
    "LowerB": {
      "title": "Lower B · Deadlift top set · Front squat",
      "tags": [
        "hinge_heavy",
        "heavy_legs"
      ],
      "blocks": [
        {
          "name": "Main block",
          "kind": "main",
          "format": "straight",
          "slots": [
            {
              "key": "deadlift",
              "pattern": "hinge",
              "prefer": [
                "deadlift",
                "trap_bar_deadlift"
              ],
              "sets": 4,
              "reps": "3",
              "rest": 210,
              "effort": "top set of 3 with 2 left in the tank, then 3 x 3 about 10% lighter",
              "rule": "rpe_top_set",
              "top_reps": 3,
              "rpe": 8,
              "backoff_sets": 3,
              "fatigue_drop": 0.1,
              "score": true
            }
          ]
        },
        {
          "name": "Second lift",
          "kind": "secondary",
          "format": "straight",
          "slots": [
            {
              "key": "front_squat",
              "pattern": "squat",
              "prefer": [
                "front_squat",
                "hack_squat",
                "goblet_squat"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 150,
              "effort": "2 left",
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
              "key": "leg_curl",
              "pattern": "hamstrings_iso",
              "prefer": [
                "seated_leg_curl",
                "lying_leg_curl",
                "slider_leg_curl"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            },
            {
              "key": "calves",
              "pattern": "calves",
              "prefer": [
                "calf_raise",
                "single_leg_calf_raise"
              ],
              "sets": 3,
              "reps": "10-15",
              "rest": 60,
              "effort": "2 left",
              "rule": "double_progression"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · Squat and bench top sets",
    "tags": [
      "heavy_legs"
    ],
    "blocks": [
      {
        "name": "Main block",
        "kind": "main",
        "format": "straight",
        "slots": [
          {
            "key": "squat",
            "pattern": "squat",
            "prefer": [
              "back_squat"
            ],
            "sets": 3,
            "reps": "3",
            "rest": 180,
            "effort": "top set of 3 at 2 left, then 2 x 3 about 10% lighter",
            "rule": "rpe_top_set",
            "top_reps": 3,
            "rpe": 8,
            "backoff_sets": 2,
            "fatigue_drop": 0.1,
            "score": true
          },
          {
            "key": "bench",
            "pattern": "h_push",
            "prefer": [
              "bench_press"
            ],
            "sets": 3,
            "reps": "3",
            "rest": 180,
            "effort": "top set of 3 at 2 left, then 2 x 3 about 10% lighter",
            "rule": "rpe_top_set",
            "top_reps": 3,
            "rpe": 8,
            "backoff_sets": 2,
            "fatigue_drop": 0.1
          }
        ]
      }
    ]
  }
}
```
