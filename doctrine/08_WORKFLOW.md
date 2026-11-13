# 08 · Workflow · the order of work and the audits

_This file owns: the steps of every `/train`, and the audit subagent after each decision. The words the coach uses are in `.claude/skills/train/SKILL.md`; the auditors' prompts are in `.claude/agents/`._

## The audit law (from Adam's trainer)

Every decision is checked by a fresh subagent that gets the files and the facts, never the coach's reasoning, so it can disagree. When it does, the coach fixes what the rules allow or answers with the exact rule (file and section). The code-owned decisions (the match, the pick, the loads, the clock) are covered by tests (`tests/`), so the auditors check what code cannot: that the person was heard right, that the safety rules held, that the sheet reads clearly.

## Onboarding

| step | the coach | the check |
|:-|:-|:-|
| screen | `plan.py screen` | the rule is code |
| interview | rounds 1 to 3, `plan.py profile` | `checks.py` validates every field |
| match | `plan.py match`, offers the top three | the score is code, tested |
| choose | `plan.py choose` | **school-auditor**: the profile says what they said, safety flags applied, the explanation honest |
| adopt (improve path) | `plan.py adopt`, then `plan.py improve accept <id>` or `decline <id>` | **school-auditor**: the routine on the sheet is the routine they described, every exercise, set and rep traceable to their words or to a yes |

## Every session

| step | the coach | the check |
|:-|:-|:-|
| readiness | four questions, `me/today.json` | |
| build | `plan.py build` | **pick-auditor** (full mode): readiness and pain read right · **session-auditor** (every session): every exercise, number and rest traces to a rule |
| words | translate the words only, if needed | the session-auditor checks numbers were untouched |
| sheet | `plan.py render` | **athletes-eye** (full mode): the person can do it without a question |
| log | `plan.py log` | `checks.py` before every commit |
| block end or early deload | | **cycle-auditor** |
| the coach's turn (`status` → `coach.next_turn`) | the starting numbers (`plan.py tests`), the weekly check-in (`plan.py checkin`), the block review (`plan.py blockreview`), each one turn, never before a session they want now | the rules are code, tested (`tests/test_engine.py` CoachHabits) |
| any change to doctrine or engine | maintainers | **collision-auditor**, `checks.py template`, `tests/` |

## Full or light

`audits` in the profile. **Full** for the first three sessions, the first session of every block, any session after a pain report, or if they ask. **Light** otherwise: the session-auditor alone, also doing the athlete's eye. This keeps the cost low on small Claude plans. If subagents cannot be spawned, each audit runs as a separate pass and the sheet says "audits not independent".

## Memory

Every write goes through `plan.py`, which runs `checks.py`, commits `me/` and `sessions/`, and pushes. On Claude Code on the web it also pushes to `main`, because a new web session starts from `main`. The log (`me/log.jsonl`) is the truth: `plan.py rebuild` recomputes the state from it.
