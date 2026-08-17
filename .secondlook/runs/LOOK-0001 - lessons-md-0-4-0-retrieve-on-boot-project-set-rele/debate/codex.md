## Agreements

There is no substantive multi-look convergence. `ai-practices/claude`, `cleanliness/grok`, and `simplicity/cursor-agent` all failed before reviewing the product; only `socratic/codex` produced findings. Calling that consensus would itself be theater. ([Claude](/Users/dshanklinbv/repos-eidos-agi/lessons.md/.secondlook/runs/LOOK-0001%20-%20lessons-md-0-4-0-retrieve-on-boot-project-set-rele/lenses/ai-practices-claude.md:1), [Grok](/Users/dshanklinbv/repos-eidos-agi/lessons.md/.secondlook/runs/LOOK-0001%20-%20lessons-md-0-4-0-retrieve-on-boot-project-set-rele/lenses/cleanliness-grok.md:1), [Cursor](/Users/dshanklinbv/repos-eidos-agi/lessons.md/.secondlook/runs/LOOK-0001%20-%20lessons-md-0-4-0-retrieve-on-boot-project-set-rele/lenses/simplicity-cursor-agent.md:1))

The sole real look is basically right: 0.4.0 adds a useful retrieval command, but “forced retrieval at session start” is false advertising. Boot registers silently; only an explicit `project-set` prints lessons. Worse, `project_set()` promises it “always” returns lessons and then suppresses every retrieval exception. ([session.py](/Users/dshanklinbv/repos-eidos-agi/lessons.md/lessons_md/_logic/_session.py:31), [project.py](/Users/dshanklinbv/repos-eidos-agi/lessons.md/lessons_md/_logic/project.py:40))

The dogfood proves capture and promotion, not changed behavior. LESSON-0003’s “second action” is another lesson; finding 0007 merely cites that lesson back to itself. That is a closed paperwork loop, not outcome evidence. ([LESSON-0003](/Users/dshanklinbv/repos-eidos-agi/lessons.md/.lessons/lessons/LESSON-0003%20-%20reuse-means-retrieve-then-act.md:22), [finding 0007](/Users/dshanklinbv/repos-eidos-agi/lessons.md/research/make-it-better/.research/findings/0007-reuse-means-retrieve-then-act.md:6))

The “every finding CHALLENGED” claim is also stale theater. The cold review covers 0001–0005; findings 0006 and 0007 were added without that review. ([peer-review.md](/Users/dshanklinbv/repos-eidos-agi/lessons.md/research/make-it-better/.research/evaluations/peer-review.md:6), [CHANGELOG.md](/Users/dshanklinbv/repos-eidos-agi/lessons.md/CHANGELOG.md:22))

## Dissents

I dissent from `socratic/codex` saying agents must remember registration. Every CLI command does automatically run `boot_from_cwd()`. The actual missing behavior is lesson exposure: registration happens, but nothing is printed until the agent explicitly chooses `project-set` or `relevant`. ([\_app.py](/Users/dshanklinbv/repos-eidos-agi/lessons.md/lessons_md/cli/_app.py:18), [\_session.py](/Users/dshanklinbv/repos-eidos-agi/lessons.md/lessons_md/_logic/_session.py:31))

I dissent from filtering retrieval to literal `status: open`. Promotion is evidence lineage, not retirement: `lesson_promote()` deliberately leaves the lesson in the active lessons directory and changes its status to `promoted-research` or `promoted-adr`. Filtering strictly to `open` would hide every promoted dogfood lesson. The real defect is calling the result “Open lessons” while mixing lifecycle and epistemic statuses; `retired` should not appear, while promoted-but-active lessons probably should. ([lesson.py](/Users/dshanklinbv/repos-eidos-agi/lessons.md/lessons_md/_logic/lesson.py:324), [project.py](/Users/dshanklinbv/repos-eidos-agi/lessons.md/lessons_md/_logic/project.py:18))

I dissent from treating the unweighted scoring error as decision-changing. The published totals ignore the locked weights, which is sloppy ceremony, but applying the weights still leaves retrieve-on-boot first: 76 versus applies-when 67 and outcome-tick 54. The decision survives; its claimed “40” rationale does not. ([decision-criteria.md](/Users/dshanklinbv/repos-eidos-agi/lessons.md/research/make-it-better/.research/evaluations/decision-criteria.md:8), [scoring-matrix.md](/Users/dshanklinbv/repos-eidos-agi/lessons.md/research/make-it-better/.research/evaluations/scoring-matrix.md:17))

`applies_when` is only an extra lexical haystack. `project-set` supplies no task query, and `relevant` requires the agent to invent one. Calling that situational retrieval overstates what is merely substring filtering. ([lesson.py](/Users/dshanklinbv/repos-eidos-agi/lessons.md/lessons_md/_logic/lesson.py:192))

## What the calling agent should do next

1. Rename the release claim to “automatic project registration plus explicit retrieval,” unless the first CLI/MCP interaction actually emits applicable lessons.
2. Stop swallowing retrieval failures in `project_set()` and add one failure-path check.
3. Define “active” separately from promotion; exclude `retired` and `superseded`, retain promoted lessons unless explicitly retired, and test mixed statuses.
4. Replace raw totals with weighted totals. Keep the same decision, minus the fake precision.
5. Run one unrelated later task where a retrieved lesson changes an action; record the task and outcome outside LESSON-0002/0003.
6. Cold-review findings 0006/0007 after independent evidence exists. Until then, leave them LOW and stop claiming every finding was challenged.
