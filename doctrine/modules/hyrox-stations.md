# HYROX stations · hyrox-stations

One station piece at the end of a session in a HYROX block, timed and scored. This file is the one place the station weights live: programs point here and never hard code a weight.

**The race stations and weights** [snippet: Red Bull, Roxlyfe, Fitness Volt, Hyranking, research/02]. **Confirm against the current season's rulebook** on hyrox.com before you train at race weight: it could not be reached when this was written, and sources disagree on wall ball target heights. Sled weights include the sled.

| # | station | Women Open | Women Pro | Men Open | Men Pro |
|:-|:-|:-|:-|:-|:-|
| 1 | SkiErg 1000 m | bodyweight | bodyweight | bodyweight | bodyweight |
| 2 | Sled push 50 m | 102 kg | 152 kg | 152 kg | 202 kg |
| 3 | Sled pull 50 m | 78 kg | 103 kg | 103 kg | 153 kg |
| 4 | Burpee broad jump 80 m | bodyweight | bodyweight | bodyweight | bodyweight |
| 5 | Row 1000 m | machine | machine | machine | machine |
| 6 | Farmers carry 200 m | 2 x 16 kg | 2 x 24 kg | 2 x 24 kg | 2 x 32 kg |
| 7 | Sandbag lunges 100 m | 10 kg | 20 kg | 20 kg | 30 kg |
| 8 | Wall balls 100 reps | 4 kg, 2.70 m | 6 kg, 2.70 m [believe] | 6 kg, 3.00 m | 9 kg, 3.00 m |

Doubles: men's and mixed doubles use Men Open weights, women's doubles Women Open [snippet for mixed, believe for the rest]. Relay: Open weights [believe].

**No sled.** The pieces below keep a sled-free version in the rotation: a heavy farmer carry stands in for the push and pull, walking lunges for the sandbag. Get at least 2 to 3 sessions on a real sled, SkiErg and wall ball target before race day [snippet: Genesis Fitness, The Gym Group].

**How it climbs.** A benchmark: your best time on each version is the score. Weight goes up towards race weight by your choice, never by rule.

## The data (the engine reads this block)

```json
{
  "id": "hyrox-stations",
  "name": "HYROX station piece",
  "when": "finisher",
  "minutes": 10,
  "session": {
    "title": "HYROX station piece",
    "tags": [
      "hard_cardio"
    ],
    "blocks": [
      {
        "name": "Station piece",
        "kind": "finisher",
        "format": "fortime",
        "minutes": 10,
        "slots": [
          {
            "key": "mod_hyrox_station",
            "kind": "piece",
            "format": "fortime",
            "minutes": 10,
            "reps": "2 rounds",
            "rule": "benchmark",
            "score": true,
            "effort": "race weight from the table in this module, or lighter while you learn the station",
            "pieces": [
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "sled_push"
                  ],
                  "reps": "25 m"
                },
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "sled_pull"
                  ],
                  "reps": "25 m"
                },
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "ski_erg",
                    "row_erg"
                  ],
                  "reps": "250 m"
                }
              ],
              [
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "burpee_broad_jump",
                    "burpee"
                  ],
                  "reps": "20 m"
                },
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "row_erg",
                    "ski_erg",
                    "bike_erg"
                  ],
                  "reps": "250 m"
                }
              ],
              [
                {
                  "pattern": "carry",
                  "prefer": [
                    "farmer_carry",
                    "suitcase_carry"
                  ],
                  "reps": "100 m"
                },
                {
                  "pattern": "lunge",
                  "prefer": [
                    "sandbag_lunge",
                    "walking_lunge"
                  ],
                  "reps": "25 m"
                },
                {
                  "pattern": "throw",
                  "prefer": [
                    "wall_ball",
                    "med_ball_slam"
                  ],
                  "reps": "25"
                }
              ],
              [
                {
                  "pattern": "carry",
                  "prefer": [
                    "farmer_carry",
                    "sandbag_carry"
                  ],
                  "reps": "100 m heavy, in place of the sled"
                },
                {
                  "pattern": "lunge",
                  "prefer": [
                    "walking_lunge",
                    "db_reverse_lunge"
                  ],
                  "reps": "25 m"
                },
                {
                  "pattern": "cyclic",
                  "prefer": [
                    "ski_erg",
                    "row_erg",
                    "bike_erg"
                  ],
                  "reps": "250 m"
                }
              ]
            ]
          }
        ]
      }
    ]
  }
}
```
