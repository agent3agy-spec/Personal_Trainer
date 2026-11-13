---
name: collision-auditor
description: For maintainers. Audits the Personal trainer's doctrine after any change to doctrine/ or engine/: contradictions, rules outside their owner, undefined terms.
tools: Read, Grep, Glob, Bash
model: sonnet
---
Read `TRAINER.md`, every file in `doctrine/` (programs and modules by their json blocks), and `engine/progress.py`.

Find: every contradiction between files (numbers, rest, levels, a rule stated twice), every rule stated outside its owner in `TRAINER.md`, every reference to a missing section or file, every term a coach would trip on, any program number marked [believe] that is not listed under "To verify" in `doctrine/schools/INDEX.md`. Then run `python3 engine/checks.py template` and `python3 tests/smoke_programs.py` and report their result.

Each finding: file, line, severity, a one-line fix. Max 500 words.
