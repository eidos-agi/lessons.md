---
id: '0002'
title: docket.md shells out to sibling CLIs
status: open
evidence: LOW
sources:
- text: 'docket.md/docket_md/hooks/shipr_hook.py record_milestone_attempt runs shipr
    attempt via subprocess (content_hash:9061792e)'
  tier: SECONDARY
created: '2026-08-17'
---

## Claim

The trilogy pattern for composing tools is a subprocess hook, not a cloned module: docket.md calls shipr on milestone-close.

## Supporting Evidence

> **Source [SECONDARY]:** docket.md/docket_md/hooks/shipr_hook.py record_milestone_attempt runs shipr attempt via subprocess (content_hash:9061792e), retrieved 2026-08-17

## Caveats

None identified yet.
