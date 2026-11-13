# How it works

_Every step, in plain words, with a picture. For the rules themselves, `TRAINER.md` names the file that owns each one._

## 1 · The first time

```mermaid
sequenceDiagram
    actor You
    participant C as Claude (your trainer)
    participant E as The engine (engine/plan.py)
    participant R as Your copy (me/)
    You->>C: /train
    C->>E: status
    E->>C: new
    C->>You: hello + 12-item safety check + your age
    You->>C: "none, 30"
    C->>E: screen
    E->>C: clear
    C->>You: round 1: your goal and experience
    C->>You: round 2: days, minutes, place, kit (taps)
    C->>You: round 3: likes, limits, an area to bring up, numbers
    C->>E: profile, then match
    E->>C: top 3 programs with scores
    C->>You: three options, one recommended, one line each
    You->>C: picks one
    C->>E: choose
    E->>R: PROFILE.md, PLAN.md, state.json, committed
    C->>You: your week in two lines. First session now?
```

**What can stop it:** any of the first seven safety items (heart, chest pain, fainting, a long-term condition, its medication, a joint problem activity could worsen, a doctor's supervision order) means no program until a professional says yes. Pregnancy and diabetes with low-sugar risk need their midwife's or doctor's go-ahead. Under 18 is not served yet. The rules: `doctrine/01_SAFETY.md`.

## 2 · How the program is picked

```mermaid
flowchart LR
    A["24 programs"] ==> B["Hard filters<br/>experience · days · minutes ·<br/>equipment · skills · safety ·<br/>can every main lift be filled for you"]
    B ==> C["Score<br/>3 x main goal + second goal +<br/>evidence + styles you like or hate +<br/>days in its sweet spot"]
    C ==> D["Tie-breaks<br/>simpler for beginners ·<br/>stronger evidence · shorter"]
    D ==> E["Top 3<br/>you choose"]
    B -. nothing fits .-> F["Never empty: the one change<br/>that opens a better fit"]
```

The rule is written in `doctrine/03_MATRIX.md` and run by `engine/match.py`, and `tests/test_engine.py` proves the worked examples. A second goal never stacks a second program: it adds a module (a running add-on, conditioning, HYROX stations, skills, balance). Everyone 60 and over gets balance work.

## 3 · Every session

```mermaid
flowchart TB
    A["Readiness, 4 taps<br/>energy · pain · minutes · anything unusual"] ==> B["Which session<br/>the next in your rotation, never by weekday"]
    B ==> C["The dose<br/>energy sets full, normal, light or rest"]
    C ==> D["The exercises<br/>from the bank, for today's kit, around any pain,<br/>the same all block so weights can climb"]
    D ==> E["The weights<br/>from your log, or 'find your weight' the first time"]
    E ==> F["The clock<br/>every rest counted, cut to your minutes,<br/>the main block never cut"]
    F ==> G{{"Session auditor<br/>every number traces to a rule"}}
    G ==> H["Your language"]
    H ==> I["One-page PDF"]
    I ==> J{{"Athlete's eye<br/>could you do it without a question?"}}
```

**Readiness lowers the dose, it never swaps the session.** Otherwise everyone ends up on the session they like. Four things do change the day: pain (that area is left out), being ill or wrecked (a rest day), different kit (swaps, or the travel session), and the spacing rule (no heavy legs within 24 hours of hard cardio).

## 4 · After the session

```mermaid
flowchart LR
    A["You: 'done, last set of squats 3 reps,<br/>knee a bit sore 2/10'"] ==> B["Claude turns it into<br/>the engine's report"]
    B ==> C["The engine applies<br/>your program's progression rule"]
    C ==> D["log.jsonl + LOG.md + state.json"]
    D ==> E["Checked, committed, pushed"]
    E ==> F["'Logged. Squat stays at 60 next time,<br/>bench goes to 42.5.'"]
```

**The progression rules are code** (`engine/progress.py`), one per kind: linear (StrongLifts), double progression, 5/3/1 training-max waves, GZCLP stages, RPE top sets, bodyweight ladders, kettlebell timed standards, benchmark pieces, running volume, Couch to 5K weeks. The trainer never invents one.

**Weeks and blocks** close by themselves. A deload comes on schedule, or early if two warning signs show up (low energy three sessions out of four, a score dropping twice, sore or flat three times running).

## 5 · Who checks the work

Fresh reviewers (subagents in `.claude/agents/`) that see the files, never the trainer's reasoning:

| reviewer | when | checks |
|:-|:-|:-|
| school auditor | after picking a program | your profile says what you said, the safety rules held, the options were explained honestly |
| pick auditor | first sessions, new blocks, after pain | your energy and pain were read right |
| session auditor | every session | every exercise, number and rest traces to a rule |
| athlete's eye | first sessions, new blocks, after pain | you could do the sheet without a question |
| cycle auditor | end of a block, early deload | what improved, what stalled, whether the program still fits |

## 6 · Where your data lives

Only in your copy: `me/` and `sessions/`. The engine commits after every change and pushes to GitHub so your sheets are on your phone and nothing is lost. Keep the copy **Private**. `/train forget` explains how to erase it all (the only full erase is deleting the repository).
