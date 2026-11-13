# 05 · Loads · the first outing, known numbers, rounding

_This file owns: how a load is found the first time, how known numbers enter, and how loads are rounded. Code: `engine/progress.py` (`first_outing_text`, `epley`), `engine/build.py` (`seed_from_numbers`, `load_ctx`)._

## The first-outing protocol (no numbers yet)

Every lift is marked "first time" until a weight is logged for it. [Components checked: ACSM 2009, Halperin 2022; the protocol as a whole believe]

1. **No session before a clean screen.**
2. **Barbell lifts:** the empty bar first, sets of 5, adding a little each set. The first set of 5 that feels like 3 left in the tank is the working weight. Write it down.
3. **Dumbbells, kettlebells, machines, cables:** start with a weight you could lift 15 times, do the target reps, go a little heavier each set until the target reps leave 3 or 4 in the tank.
4. **Bands:** the band that makes the target reps hard but clean. The colour is logged.
5. **Bodyweight ladders:** the hardest version you can do for 3 sets of 5 with clean form is your step. Below the easiest step: holds or 5-second lowering.
6. **5/3/1 and RPE programs:** find a 5 (or the top set) the same way; the engine turns it into a training max (90% of the estimated max) or an estimated max.
7. **Session one is short on purpose:** at most 2 working sets per exercise, effort "about 3 left", so next-day soreness does not end the habit.
8. **Never a max test for a newcomer.** When a number is needed: Epley, max = load x (1 + reps / 30), from a set of 10 or fewer [believe, verified at milestone 2].
9. **The trainer asks for the weights found on the main lifts** when the session is logged. Accessories stay "find your weight" until a weight is reported.

## Known numbers

A number given at the interview ("squat 80 kg for 5", recent) becomes an estimated max. **The discount is applied once:** a training max at 90% of it (85% when unsure) for 5/3/1, or a first working weight at 90% of what the estimate gives for the program's reps. Never both.

## Rounding

Always down. Barbell: to the plate step (2.5 kg by default, never under the 20 kg bar). Dumbbells and kettlebells: to the nearest weight they actually have (the list in the profile, or a standard gym rack). Machines and cables: 2.5 kg. Pounds: a pound user trains on a pound grid (5 lb plates, a 45 lb bar, 5 lb steps on machines, a US dumbbell and kettlebell rack, or the weights they own, said in pounds and kept as said in `dumbbells_lb`). Every number printed back to them (the sheet, the score line, next time's load) is in pounds, whole pounds or the half pound they typed; the engine stores kilograms.

## When a fixed weight is too light

Home users with fixed dumbbells progress by reps, then the next harder variant in the bank (`harder` column), then tempo and pauses, then single-limb work. Past about 30 reps the trainer suggests the next weight [research/03 C5, believe for the order].
