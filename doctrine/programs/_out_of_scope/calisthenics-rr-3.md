# Bodyweight Recommended Routine · calisthenics-rr-3

**What it is.** The r/bodyweightfitness Recommended Routine shape: one session, the same every time, built from three pairs of moves and a core triplet. Each move is a ladder of steps from easy to hard. You find your step, climb reps, then climb a step.

**Who it is for.** Beginners to early intermediates who want strength and muscle with a pull-up bar and their own weight. Dip bars or rings help but are optional: the dip slot falls back to negatives, a support hold, then push-ups. 3 days a week on non-consecutive days is the standard [believe, wiki]; 2 also works. 45 to 75 minutes with the warm-up the engine writes.

**The week.** The same session each time: RR, RR, RR.

| block | pair | sets x reps |
|:-|:-|:-|
| pair 1 | pull-up ladder + squat ladder | 3 x 5 to 8 each [seen] |
| pair 2 | dip ladder + hinge ladder | 3 x 5 to 8 each [seen] |
| pair 3 | row ladder + push-up ladder | 3 x 5 to 8 each [seen] |
| core | anti-extension · anti-rotation · extension | 3 x 8 to 12 [seen] |

Do the pair back to back, then rest about 90 s before the next round [seen]. Core rounds rest 60 s. The strength part runs 40 to 60 minutes [seen].

The ladders [believe, from the wiki as remembered]:

| slot | steps, easiest to hardest |
|:-|:-|
| pull-up | dead hang, scapular pulls, negatives, assisted, pull-up, chin-up |
| squat | assisted squat, squat, split squat, shrimp squat, pistol |
| dip | push-up, support hold, negative dip, dip |
| hinge | hip hinge drill, glute bridge, single-leg bridge, single-leg Romanian deadlift |
| row | incline row, inverted row, ring row, archer row |
| push-up | wall, incline, knee, full, decline, archer, pseudo planche |

**How it climbs.** Start at the hardest step you can do 3 x 5 with good form. Add reps until all three sets hit 8. Then move up one step and start again at 5 [seen, research/03 B1 and rule 1]. If you cannot get 5 on the easiest step, do 3 to 5 negatives of about 5 s or holds instead [believe]. A set only counts if it is hard, 0 to 3 in reserve, because low-load sets near failure build muscle like heavy ones [seen, Schoenfeld 2017, Kikuchi 2017, Refalo 2023]. Overwhelmed at the start: cut sets first, add them back later [seen]. With a barbell and rack, the wiki swaps the squat and hinge ladders for barbell squat and deadlift [seen].

**Deload.** After 6 weeks, a week at half the sets. Overcoming Gravity's advice is a deload every 4 to 8 weeks because tendons adapt slower than muscle [believe].

**Graduates to.** Overcoming Gravity style self-built routines, skill work (`skill-blocks` module), or `muscle-fullbody-3` if a gym appears. No program file for those yet beyond the gym one.

**Evidence: B.** The routine is community consensus distilled from Overcoming Gravity [research/03 B1]; the principle under it (hard sets at any load grow muscle) is meta-analysis level.

**Credit.** The Recommended Routine belongs to the r/bodyweightfitness community (reddit.com/r/bodyweightfitness/wiki/kb/recommended_routine), free to read. The progression thinking is from Steven Low's Overcoming Gravity, 2nd ed. 2016 (stevenlow.org), buy the book. GMB Fitness (gmb.io) for the locomotion and wrist prep that suits deconditioned starters.

## The data (the engine reads this block)

```json
{
  "id": "calisthenics-rr-3",
  "name": "Bodyweight Recommended Routine",
  "family": "calisthenics",
  "draws_from": [
    "r/bodyweightfitness Recommended Routine",
    "Overcoming Gravity (Steven Low)",
    "GMB Fitness"
  ],
  "goals": {
    "muscle": 2,
    "strength": 2,
    "powerlifting": 0,
    "weightlifting": 0,
    "functional": 2,
    "hyrox": 0,
    "run": 0,
    "skills": 2,
    "fat_loss": 2,
    "health": 2,
    "independent": 3
  },
  "experience": [
    "none",
    "novice",
    "intermediate"
  ],
  "days": [
    2,
    3
  ],
  "sweet_days": [
    3
  ],
  "minutes": [
    45,
    75
  ],
  "express_minutes": 25,
  "equipment_all": [
    "pullup_bar"
  ],
  "equipment_any": [],
  "skills_required": [],
  "excluded_for": [
    "seated"
  ],
  "evidence": "B",
  "simplicity": 2,
  "graduates_to": [],
  "block_weeks": 6,
  "deload": {
    "sets_factor": 0.5,
    "load_factor": 1.0,
    "rir": "3 to 4"
  },
  "meso": null,
  "layouts": {
    "2": [
      "RR"
    ],
    "3": [
      "RR"
    ]
  },
  "modules": [],
  "sessions": {
    "RR": {
      "title": "Recommended Routine · three pairs and core",
      "tags": [],
      "blocks": [
        {
          "name": "Pair 1 · pull-up and squat",
          "kind": "main",
          "format": "superset",
          "rest_after_round": 90,
          "slots": [
            {
              "key": "pullup",
              "pattern": "v_pull",
              "prefer": [
                "pull_up",
                "chin_up",
                "negative_pull_up",
                "assisted_pull_up",
                "scap_pull",
                "dead_hang"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 0,
              "effort": "clean form, find your step: the hardest you can do 3 x 5",
              "rule": "ladder_step",
              "score": true
            },
            {
              "key": "squat",
              "pattern": "squat",
              "prefer": [
                "bodyweight_squat",
                "assisted_squat",
                "split_squat",
                "shrimp_squat",
                "pistol_squat"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 0,
              "effort": "clean form, find your step: the hardest you can do 3 x 5, each leg on one-leg steps",
              "rule": "ladder_step"
            }
          ]
        },
        {
          "name": "Pair 2 · dip and hinge",
          "kind": "main",
          "format": "superset",
          "rest_after_round": 90,
          "slots": [
            {
              "key": "dip",
              "pattern": "h_push",
              "prefer": [
                "dip",
                "negative_dip",
                "support_hold",
                "push_up"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 0,
              "effort": "clean form, find your step: the hardest you can do 3 x 5, holds count in 10 s chunks",
              "rule": "ladder_step"
            },
            {
              "key": "hinge",
              "pattern": "hinge",
              "prefer": [
                "single_leg_rdl",
                "hip_hinge_drill",
                "single_leg_glute_bridge",
                "glute_bridge"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 0,
              "effort": "clean form, find your step: the hardest you can do 3 x 5, each leg",
              "rule": "ladder_step"
            }
          ]
        },
        {
          "name": "Pair 3 · row and push-up",
          "kind": "secondary",
          "format": "superset",
          "rest_after_round": 90,
          "slots": [
            {
              "key": "row",
              "pattern": "h_pull",
              "prefer": [
                "inverted_row",
                "ring_row",
                "incline_inverted_row",
                "archer_row"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 0,
              "effort": "clean form, find your step: the hardest you can do 3 x 5",
              "rule": "ladder_step"
            },
            {
              "key": "pushup",
              "pattern": "h_push",
              "prefer": [
                "push_up",
                "incline_push_up",
                "wall_push_up",
                "knee_push_up",
                "decline_push_up",
                "archer_push_up",
                "pseudo_planche_push_up"
              ],
              "sets": 3,
              "reps": "5-8",
              "rest": 0,
              "effort": "clean form, find your step: the hardest you can do 3 x 5",
              "rule": "ladder_step"
            }
          ]
        },
        {
          "name": "Core triplet",
          "kind": "accessory",
          "format": "superset",
          "rest_after_round": 60,
          "slots": [
            {
              "key": "antiext",
              "pattern": "anti_ext",
              "prefer": [
                "ab_wheel",
                "body_saw",
                "long_lever_plank",
                "plank",
                "dead_bug"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 0,
              "effort": "8 to 12 reps, or 20 to 30 s on a hold",
              "rule": "ladder_step"
            },
            {
              "key": "antirot",
              "pattern": "anti_rot",
              "prefer": [
                "band_pallof_press",
                "pallof_press",
                "side_plank"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 0,
              "effort": "8 to 12 each side, or 20 to 30 s on a hold",
              "rule": "ladder_step"
            },
            {
              "key": "ext",
              "pattern": "hinge",
              "prefer": [
                "back_extension",
                "single_leg_glute_bridge",
                "glute_bridge"
              ],
              "sets": 3,
              "reps": "8-12",
              "rest": 0,
              "effort": "8 to 12, squeeze at the top",
              "rule": "ladder_step"
            }
          ]
        }
      ]
    }
  },
  "express": {
    "title": "Express · pull-up and squat, row and push-up",
    "tags": [],
    "blocks": [
      {
        "name": "Pair 1 · pull-up and squat",
        "kind": "main",
        "format": "superset",
        "rest_after_round": 90,
        "slots": [
          {
            "key": "pullup",
            "pattern": "v_pull",
            "prefer": [
              "pull_up",
              "chin_up",
              "negative_pull_up",
              "assisted_pull_up",
              "scap_pull",
              "dead_hang"
            ],
            "sets": 2,
            "reps": "5-8",
            "rest": 0,
            "effort": "clean form, find your step: the hardest you can do 3 x 5",
            "rule": "ladder_step",
            "score": true
          },
          {
            "key": "squat",
            "pattern": "squat",
            "prefer": [
              "bodyweight_squat",
              "assisted_squat",
              "split_squat",
              "shrimp_squat",
              "pistol_squat"
            ],
            "sets": 2,
            "reps": "5-8",
            "rest": 0,
            "effort": "clean form, find your step: the hardest you can do 3 x 5, each leg on one-leg steps",
            "rule": "ladder_step"
          }
        ]
      },
      {
        "name": "Pair 3 · row and push-up",
        "kind": "main",
        "format": "superset",
        "rest_after_round": 90,
        "slots": [
          {
            "key": "row",
            "pattern": "h_pull",
            "prefer": [
              "inverted_row",
              "ring_row",
              "incline_inverted_row",
              "archer_row"
            ],
            "sets": 2,
            "reps": "5-8",
            "rest": 0,
            "effort": "clean form, find your step: the hardest you can do 3 x 5",
            "rule": "ladder_step"
          },
          {
            "key": "pushup",
            "pattern": "h_push",
            "prefer": [
              "push_up",
              "incline_push_up",
              "wall_push_up",
              "knee_push_up",
              "decline_push_up",
              "archer_push_up",
              "pseudo_planche_push_up"
            ],
            "sets": 2,
            "reps": "5-8",
            "rest": 0,
            "effort": "clean form, find your step: the hardest you can do 3 x 5",
            "rule": "ladder_step"
          }
        ]
      }
    ]
  }
}
```
