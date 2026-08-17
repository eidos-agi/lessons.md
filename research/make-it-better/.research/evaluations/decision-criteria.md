---
locked: true
locked_date: '2026-08-17'
---

## Decision Criteria

| # | Criterion | Weight | Rationale |
|---|-----------|--------|-----------|
| 1 | Forces retrieval at next decision | 3 | Finding 0001: stores fail when the next actor does not see the lesson at decision time. |
| 2 | Raises application, not just capture | 3 | Finding 0002: scarce metric is apply-rate. |
| 3 | Cheap enough an agent will actually run it | 2 | GAO: time pressure was a named barrier; ceremony that adds steps will be skipped. |
| 4 | Fits the trilogy without becoming research.md or a memory product | 1 | lessons.md is the LEARN leg. Do not absorb scoring, embeddings, or evidence gates. |
| 5 | Shippable this week without new infra | 1 | No vector DB, no new service. |

Weights are relative 1–3. Scoring is 0–10 per criterion.
