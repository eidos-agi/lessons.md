# Second-look debate

This is analysis only. Do NOT edit, create, or delete any files. Do NOT commit. Do NOT run destructive commands. stdout is the review.

Topic: lessons.md 0.4.0 retrieve-on-boot: project-set/relevant, applies-when, research/make-it-better (GAO/Wharton/Tsinghua, peer CHALLENGED every finding), dogfood LESSON-0001/0002/0003. Is this actually better? Did we follow our own lessons? What is still theater?
Target: /Users/dshanklinbv/repos-eidos-agi/lessons.md

You are one outside reviewer in a multi-harness debate. Other harnesses already wrote independent looks. Argue. Agree or dissent with citations. Do not be polite. Do not invent files.

## Independent looks

### ai-practices/claude

Client.listTools() called but server does not advertise tools capability - returning empty list

### cleanliness/grok

(empty stdout, rc=124) timed out after 180s

### simplicity/cursor-agent

⚠ Workspace Trust Required

  Cursor Agent can execute code and access files in this directory.
  Do you trust the contents of this directory?

    /Users/dshanklinbv/repos-eidos-agi/lessons.md

  To proceed, you can either:
    • Run 'agent' interactively to decide
    • Pass --trust, --yolo, or -f if you trust this directory

### socratic/codex

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
  Why is creating another lesson evidence that retrieval improved subsequent work? Why does finding 0007 cite only LESSON-0003, which itself asserts that reuse happened? Why call this application rather than another capture cycle when the decision says success requires a later session actually using the lesson? A separate task record showing the retrieved lesson changed an acti

[truncated]

Return markdown with exactly these headings:

## Agreements
Where two or more looks converge. Cite the lens names.

## Dissents
Where you disagree, and why, with a path:line.

## What the calling agent should do next
Numbered, smallest next steps. No CONFIRMED claims. No "consider exploring."
