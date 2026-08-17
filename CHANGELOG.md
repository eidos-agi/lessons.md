# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-08-17

### Added
- Forced retrieval at session start (`project-set` prints open lessons; new `relevant [query]` command). Decision: `research/make-it-better`.
- Optional `--applies-when` on create/update so matching is not only title keywords.

### Research
- New research.md project at `research/make-it-better` with external sources (GAO-01-1015R, Wharton/Senge AAR, Tsinghua agent-memory taxonomy), content hashes, disconfirmation, locked criteria, cold peer review (all CHALLENGED), scores, and DECISION.md.

## [0.3.0] - 2026-08-17

### Added
- `lesson-promote` shells out to **research-md** (the CLI), same composition as docket.md → shipr. Creates a finding from the lesson, or verifies a `0001`-style id. Placeholder strings like `RES-0099` are rejected.
- `--research/--no-research` and `--research-path`.
- This repo now has a committed `.research/` project that asked the question this release answers.

### Changed
- `promotes_to` stores both the research project GUID and the finding id returned by research-md.

## [0.2.0] - 2026-08-17

### Added
- `status` — project health: each lesson, promotions, integrity vs disk (research.md analog).
- `gates.py` — CONFIRMED is earned by a research.md promotion; promote requires a target.
- `integrity.py` — recorded status must match the files on disk.
- `errors.py` — `LessonGateError`, `LessonValidationError`, `LessonNotFoundError`.
- Eidos-aware boot: `.eidos/lessons/lessons.json` is found the same way research.md finds `.eidos/research/`.
- `project-get` alias of `project-list`.
- Advisories on create: missing `origin_task`, unpromoted REASONED.
- GitHub Actions CI (ruff + pytest 3.11/3.12/3.13 + wheel install).

### Changed
- README rewritten to match the research.md product surface (install, MCP, workflow, gates). CRUD is documented — it already shipped in 0.1.0.
- `__version__` is read from package metadata.
- MCP `help` tree now starts at `status` (research.md session shape). Constructor hooks match the current MCP SDK; the decorator API research.md still uses is gone here.

## [0.1.0] - 2026-08-17

### Added
- Initial public release: CLI + razor-thin MCP for `LESSON-NNNN` records.
- Project GUID routing (`project-init` / `project-set` / `project-list` / `project-info`).
- Lesson create, list, view, update, supersede, promote.
- CONFIRMED rejected until `lesson-promote --research-id`.
