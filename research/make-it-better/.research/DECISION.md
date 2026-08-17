# Decision

**Date:** 2026-08-17
**Status:** Decided

## Decision

Ship forced retrieval at session start: project-set and a relevant command must print matching open lessons. Add an optional applies-when field so matching is not only title keywords. Do not build embeddings. Do not add more research.md ceremony. Outcome ticks wait.

## Rationale

Highest *weighted* score (**76**) on the locked criteria (retrieval×3 + application×3 + cheap×2 + fit×1 + ship×1). Raw sum was 40; LOOK-0001 noted that 40 ignored the weights. Weighted ranking is the same order. Findings 0001/0002 (CONFIRMED, peer-CHALLENGED) say the failure is retrieval-at-decision-time and apply-rate, not missing write features. retrieve-on-boot is the cheapest thing that puts lessons in front of the next agent. applies-when is a cheap matcher, not a standalone product. Peer review forbids treating the NASA survey as a universal law — so this is a bet, not a proof. We will know it worked only if a later session actually uses a printed lesson.
