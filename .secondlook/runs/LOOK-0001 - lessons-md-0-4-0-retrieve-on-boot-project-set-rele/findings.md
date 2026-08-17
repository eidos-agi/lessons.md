# Findings

Extracted from lens files. Evidence grade is LOW until research-md earns more.
The calling agent reads this, then acts. Do not CONFIRMED from a second look alone.

## F-0001

- severity: P1
- title: Prove retrieval occurs without the agent remembering it
- locus: lessons_md/_logic/_session.py:31
- lens: socratic
- harness: codex

## F-0002

- severity: P1
- title: Return only lessons that are actually open
- locus: lessons_md/_logic/lesson.py:201
- lens: socratic
- harness: codex

## F-0003

- severity: P2
- title: Demonstrate reuse with an independently observed outcome
- locus: .lessons/lessons/LESSON-0003 - reuse-means-retrieve-then-act.md:22
- lens: socratic
- harness: codex

## F-0004

- severity: P2
- title: Reconcile the decision with its locked weights
- locus: research/make-it-better/.research/evaluations/scoring-matrix.md:17
- lens: socratic
- harness: codex

## F-0005

- severity: P2
- title: Subject the dogfood findings to the claimed cold challenge
- locus: research/make-it-better/.research/evaluations/peer-review.md:8
- lens: socratic
- harness: codex
