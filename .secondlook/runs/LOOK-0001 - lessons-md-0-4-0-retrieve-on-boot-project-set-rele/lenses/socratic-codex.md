## Verdict

0.4.0 is directionally better: it adds a cheap retrieval surface, situational matching, external research, and honest LOW-confidence dogfood records. But “forced retrieval at session start” is not yet true. Boot silently registers; agents must still remember the retrieval ritual. The research process also contains scoring and review ceremony that its own artifacts do not substantiate.

## Findings

- [P1] Prove retrieval occurs without the agent remembering it — lessons_md/_logic/_session.py:31  
  Why call this retrieve-on-boot when boot only registers and returns no lessons? Why expect the next agent to invoke `project-set` or `relevant` if forgetting retrieval is the diagnosed failure? Why would documentation correct that behavioral failure? An end-to-end fresh CLI or MCP session whose first interaction exposes the applicable lesson without an explicit retrieval command would falsify this finding.

- [P1] Return only lessons that are actually open — lessons_md/_logic/lesson.py:201  
  Why does “Open lessons” exclude only `superseded`, thereby admitting `promoted-research`, `promoted-adr`, and `retired`? Why should increasingly stale or retired records be forced into every session? Why will agents trust retrieval after irrelevant records accumulate? A mixed-status test proving that only `status: open` is returned would falsify this finding; the repository’s three promoted dogfood lessons currently demonstrate the opposite.

- [P2] Reconcile the decision with its locked weights — research/make-it-better/.research/evaluations/scoring-matrix.md:17  
  Why lock weighted criteria if each displayed total is merely the five raw scores added together? Why cite “highest score (40)” as decision authority when the stated weights were not applied? Why should the ceremony be trusted if its central calculation is unaudited? A reproducible weighted calculation, with the resulting ranking and decision explicitly reconciled, would falsify this finding.

- [P2] Demonstrate reuse with an independently observed outcome — .lessons/lessons/LESSON-0003 - reuse-means-retrieve-then-act.md:22  
  Why is creating another lesson evidence that retrieval improved subsequent work? Why does finding 0007 cite only LESSON-0003, which itself asserts that reuse happened? Why call this application rather than another capture cycle when the decision says success requires a later session actually using the lesson? A separate task record showing the retrieved lesson changed an action and affected its outcome would falsify this finding.

- [P2] Subject the dogfood findings to the claimed cold challenge — research/make-it-better/.research/evaluations/peer-review.md:8  
  Why does the “all findings CHALLENGED” review cover only 0001–0005 while the research project now contains 0006 and 0007? Why are those two findings sourced solely from the lessons they promote? Why does promotion add epistemic value if lesson and finding validate each other? Cold review entries for 0006/0007 plus evidence independent of LESSON-0002/0003 would falsify this finding.

## What you would not change

Keep the deliberately small product decision: `project-set`, `relevant`, and `applies_when` are proportionate, reuse existing storage, and avoid embedding infrastructure. Keep the research decision’s explicit statement that retrieve-on-boot is a bet rather than proof. Keep LESSON-0002 and LESSON-0003 at LOW confidence; that honestly reflects the absence of outcome validation. Keep the tests that establish `project-set` output and `applies_when` matching—they prove those narrower behaviors even though they do not prove session-start retrieval.

## Questions for the other reviewers

1. Can anyone identify a real entry path where a fresh agent receives lessons without first choosing `project-set` or `relevant`?
2. Does applying the documented weights change any candidate ranking or expose further unsupported score judgments?
3. Is there durable evidence outside LESSON-0002/0003 and findings 0006/0007 that either lesson changed a later task’s behavior or outcome?
