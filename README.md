# lessons.md

[![CI](https://github.com/eidos-agi/lessons.md/actions/workflows/ci.yml/badge.svg)](https://github.com/eidos-agi/lessons.md/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

The learning forge. Durable, queryable, supersedable lessons from execution. A lesson is allowed to stay un-binding until earned. `CONFIRMED` is illegal until a research.md finding earned it.

## The loop

```
research.md  →  governor.md  →  docket.md  →  lessons.md  →  research.md
  DECIDE         CONTRACT        EXECUTE        LEARN
```

Do not name this "learning." The noun is **lesson**. IDs are `LESSON-0001`. State lives in `.lessons/` (or `.eidos/lessons/` inside an eidos). Commit it.

## What it enforces

| Gate | Trigger |
|------|---------|
| CONFIRMED is earned | `lesson-create` / `lesson-update` fail if confidence is CONFIRMED without a research.md promotion |
| Promote needs a target | `lesson-promote` fails unless `--research-id` and/or `--adr` is set |
| Claim cannot be empty | create/update reject a blank claim |
| Integrity vs disk | `status` errors when a superseded lesson is still in `lessons/`, or CONFIRMED was written by hand |

Advisories (not hard fails): missing `--origin-task`; REASONED that has not been promoted.

## Install

```bash
pip install -e ".[dev]"
```

From the repo:

```bash
git clone https://github.com/eidos-agi/lessons.md
cd lessons.md
pip install -e ".[dev]"
```

## MCP configuration

Add to your Claude Code config:

```bash
claude mcp add lessons-md --scope user -- lessons-md
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "lessons-md": {
      "command": "lessons-md"
    }
  }
}
```

MCP is razor-thin help. Real work is Bash: `lessons-md <command>`.

## Agent workflow

```
project_set            Register project, get project_id
    |
status                 Health + integrity (start every session here)
    |
lesson_create          Record what execution taught (default LOW)
    |                  Advisory: pass --origin-task if a docket.md task produced this
lesson_update          Revise the claim, append body, raise confidence to REASONED
    |
lesson_promote         Link a research.md finding and/or an ADR
    |                  Gate: CONFIRMED is now legal
lesson_supersede       Replace a lesson that turned out wrong
```

### Confidence ladder

| Grade | Meaning | Requirements |
|-------|---------|--------------|
| `UNVERIFIED` | Noted, not examined | None |
| `LOW` | First take from one run | A claim another agent can act on |
| `REASONED` | Holds up across runs, still un-binding | Still not CONFIRMED |
| `CONFIRMED` | Earned | `lesson-promote --research-id` first |

## Trilogy conventions

lessons.md follows shared conventions with [research.md](https://github.com/eidos-agi/research.md), [governor.md](https://github.com/eidos-agi/visionlog.md), and [docket.md](https://github.com/eidos-agi/docket.md). See [CONVENTIONS.md](CONVENTIONS.md).

- **research.md** — decide with evidence
- **governor.md** — record the decision as a contract
- **docket.md** — execute tasks within those contracts
- **lessons.md** — keep what execution taught (this tool)

## Targeting pattern: project_set + project_id

Every write requires a `project_id` — the GUID from `.lessons/lessons.json`.

1. Call `project-set` with the project's path
2. It returns the `project_id`
3. Pass that `project_id` on every subsequent call

If the GUID is unknown, the error tells you to call `project-set`. No silent failures.

Inside an eidos, boot finds `.eidos/lessons/` the same way research.md finds `.eidos/research/`.

## Commands

### Session

| Command | Description |
|---------|-------------|
| `project-set` | Register a project path, returns its GUID |
| `project-get` | List registered projects (alias of `project-list`) |
| `status` | Health: each lesson, promotions, integrity vs disk |

### Project

| Command | Description |
|---------|-------------|
| `project-init` | Initialize `.lessons/` and write the GUID |
| `project-list` | List projects registered this session |
| `project-info` | Counts by status plus an integrity one-liner |

### Lessons

| Command | Description |
|---------|-------------|
| `lesson-create` | Create a lesson. CONFIRMED rejected until promoted |
| `lesson-list` | List lessons (`--include-superseded`) |
| `lesson-view` | Full frontmatter and body |
| `lesson-update` | Update fields or append body |
| `lesson-supersede` | Archive the old file, create the replacement |
| `lesson-promote` | Link `research_id` and/or `adr` |

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check lessons_md tests
```

## License

MIT — see [LICENSE](LICENSE).
