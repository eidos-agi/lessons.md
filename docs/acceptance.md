# Acceptance — telos leftovers

Status: ⬜ todo · 🔧 in progress · ✅ done+verified · 🐛 known bug

Metric: `proven_acceptance_criteria` count, target 4.

- ✅ **AC-1 Weighted scores.** `research/make-it-better/.research/evaluations/scoring-matrix.md` shows weighted totals from locked weights. DECISION.md does not treat unweighted 40 as authority. Verify: file contains weighted totals; ranking still retrieve-on-boot first. Proof: scoring-matrix.md "Weighted totals" table (76 / 67 / 54 / 44 / 37 / 21); DECISION.md now cites 76.

- ✅ **AC-2 Cold review 0006/0007.** `research/make-it-better/.research/evaluations/peer-review.md` attests findings 0006 and 0007 after they existed. Verify: `rg "0006|0007" peer-review.md`. Proof: addendum in peer-review.md — 0006 CHALLENGED, 0007 DISPUTED (circular promote/cite).

- ✅ **AC-3 Independent apply-rate.** A later task that is not `lesson-create`, whose action changed because an active lesson was printed. Recorded in `docs/apply-rate-proof.md`, not only in LESSON-0002/0003. Verify: that file exists and names the task, the lesson id, the action taken instead, and the artifact. Proof: `docs/apply-rate-proof.md` — M1 edited scoring-matrix + DECISION because LOOK-0001 F-0004 / LESSON-0004, not another lesson-create.

- ⬜ **AC-4 Secondlook ≥2 harnesses.** A look after this charter has at least two harnesses with findings. Verify: latest `.secondlook/runs/LOOK-*/run.json` (or look JSON) shows two `n_findings > 0`. Proof: —

Out of scope: PyPI publish (owner approval gate). Embeddings. More research.md ceremony.
