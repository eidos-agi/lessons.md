# lessons.md

> **The learning forge.** Durable lessons from execution.

## The loop

```
research.md  →  visionlog  →  docket.md  →  lessons.md  →  research.md
  DECIDE        CONTRACT      EXECUTE        LEARN
```

A lesson is a durable, queryable, supersedable record of what execution taught. It is allowed to stay un-binding until earned. CONFIRMED confidence is illegal until a research.md finding earned it.

Do not name this "learning." The noun is **lesson**. IDs are `LESSON-0001`. State lives in `.lessons/`. Commit `.lessons/`.

## v0 commands

| Command | What |
|---------|------|
| `project-init` | Initialize `.lessons/`, get GUID |
| `project-set` | Register an existing project for this session |
| `project-list` | List registered projects |
| `project-info` | Lesson counts by status |

Lesson CRUD lands later.

## MCP

MCP is razor-thin help. Real work is Bash: `lessons-md <command>`.
