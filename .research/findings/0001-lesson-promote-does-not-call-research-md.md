---
id: '0001'
title: 'lesson-promote does not call research-md'
status: open
evidence: LOW
sources:
- text: 'lessons.md/lessons_md/_logic/lesson.py lesson_promote docstring: ''Link a
    lesson to research and/or an ADR. Does not create either.'' (content_hash:1db98b58)'
  tier: SECONDARY
created: '2026-08-17'
---

## Claim

lesson-promote writes promotes_to.research_id as a free string and never invokes the research-md CLI.

## Supporting Evidence

> **Source [SECONDARY]:** lessons.md/lessons_md/_logic/lesson.py lesson_promote docstring: 'Link a lesson to research and/or an ADR. Does not create either.' (content_hash:1db98b58), retrieved 2026-08-17

## Caveats

None identified yet.
