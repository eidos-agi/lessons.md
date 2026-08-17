## Philosophy

A lesson that is only written has not been used. That is the belief that stays
true when the rest of this product changes. lessons.md exists so that what
execution taught survives the session and is handed to the next agent at the
moment of the next decision. Capture without retrieval is a filing cabinet.
Retrieval without a later changed action is still capture, dressed as reuse.

We believe the LEARN leg of the trilogy is not a markdown CRUD wrapper and is
not a clone of research.md. research.md earns decisions. governor locks them.
docket executes. lessons.md is what execution taught, allowed to stay un-binding
until research.md earns CONFIRMED. Copying another forge's internals is not
using it. Calling a sibling CLI is using it. Calling a secondlook panel and
reading the files is using it. Writing the outcome only in chat is not a lesson.

We believe an agent will not remember to retrieve. Forced handoff on the first
command from a `.lessons/` tree is therefore not a convenience; it is the
product. We also believe one Codex look is one look. Consensus requires more
than one harness that actually produced findings.

## The Friction

This loop was opened because the operator asked whether the work was finished
and was told no, then said to use telos to fix what remained. The remaining
failures were not missing features. They were honesty failures we had already
named and then left sitting.

LOOK-0001 (Codex, socratic) said retrieve-on-boot was false advertising: boot
registered and printed nothing; the agent still had to remember `project-set`.
We patched first-command stderr handoff. That P1 is the only remaining item
that already has a proof artifact in this repo (`lessons-md project-list`
emitting active lessons on stderr). The rest were left as notes.

The same look said LESSON-0003 is another capture cycle, not apply-rate.
Finding 0007 cites LESSON-0003 which asserts reuse happened. Closed paperwork.
GAO-01-1015R (hash e659b4ed) said NASA managers could not retrieve the right
lesson at the right time; we treated that as a product law; a cold peer review
CHALLENGED every finding; we still have no later unrelated task whose action
changed because a lesson was printed.

The scoring matrix in `research/make-it-better` added five raw scores and
called the total "40" the decision authority. Locked weights were never
applied. Debate later showed weighted ranking still puts retrieve-on-boot
first (76 vs 67). The decision survives; the claimed arithmetic does not.

Findings 0006 and 0007 were added after the cold review of 0001–0005 and were
never challenged. CHANGELOG still said every finding was challenged.

Three of four secondlook harnesses failed (Claude stdin, Grok timeout, Cursor
trust). Calling LOOK-0001 a panel is theater. PyPI remains an explicit
approval gate and is not a completion criterion unless the owner says publish.

## The Cost of Not

If these leftovers stay open, the next session will treat 0.4.0 as done and
build more ceremony. That is how we got 0.2.0 (cloned research.md internals)
after being told to use the tool. The cost is founder attention spent
correcting the same class of lie: we said we retrieved, reviewed, reused, or
consensed, and the artifact shows we filed.

Without a later-task apply proof, "lessons change the next agent" is a slogan.
Without weighted totals, research.md scoring is a ritual the decision does not
depend on. Without a second live harness, outside review is one model grading
our homework. Without cold review of 0006/0007, promotion is two files nodding
at each other.

The compounding cost is trust in the trilogy. If lessons.md cannot use
research.md, secondlook-md, and telos-md honestly on itself, no other repo
should adopt it. Agents will keep writing chat recaps. The LEARN leg stays
empty. The operator keeps asking "is it done?" because the record cannot
answer.

## Why Not The Alternatives

- **Keep grinding features without telos.** — insufficient because that is
  what produced 0.2.0, 0.3.0, and 0.4.0 as a pile of green parts. Each piece
  had tests. The whole still had false claims (forced retrieval, consensus,
  every finding challenged). Telos exists to stop adding parallel pieces when
  the leftovers are integration and honesty. (research: make-it-better
  DECISION.md; LOOK-0001 debate.md)

- **Clone more research.md ceremony (phases, scoring, integrity clones).** —
  insufficient because 0.2.0 did that and the operator said no, use the CLI.
  More ceremony does not raise apply-rate. It raises the appearance of rigor.
  Candidate `more-ceremony` scored last (14 unweighted, still last weighted).
  (research: make-it-better candidate more-ceremony.md)

- **Become an embedding / Mem0-style memory product.** — insufficient because
  it is a different product, needs infra, and was eliminated in the same
  landscape. Retrieval-at-decision-time can be a printed list. (research:
  make-it-better candidate embeddings.md)

- **Declare PyPI publish as the done condition.** — insufficient because
  shipr's committed model lists PyPI as an explicit human approval gate.
  Publishing without that approval is the 84-month loan: the metric moved,
  the outcome is the wrong kind of shipped. GitHub main is the current
  distribution. (research: .shipr/product-release-model.json approval_gates)

- **Treat LOOK-0001 Codex findings as CONFIRMED and stop.** — insufficient
  because secondlook's own rule is LOW until research-md earns more, and
  three harnesses never reviewed. Acting on P1 was right. Calling the look
  finished science is the same theater the look accused us of. (research:
  .secondlook/runs/LOOK-0001 findings.md; LESSON-0004)

- **Write another lesson instead of proving apply-rate.** — insufficient
  because that is exactly LESSON-0003. Capture is not reuse. The next
  "lesson" that only records we retrieved is more capture. (research:
  LOOK-0001 F-0003; LESSON-0003)

## The Unique Offer

This loop is not a new product. It is custody over finishing the honesty
gaps in lessons.md so the LEARN leg can be adopted without lying. What
nothing else offers here is a north star whose metric is *proven leftover
count*, not "feels complete," and whose requirements are the four leftovers
the operator already accepted as not done: weighted scoring record, cold
review of post-review findings, an independent apply-rate artifact, and a
secondlook in which at least two harnesses produce findings.

The unique offer of lessons.md itself stays: first-command handoff of
active lessons, CONFIRMED only via research-md, promote shells out to
research-md. This charter does not invent a fifth offer. It refuses to
call those offers complete while the leftovers contradict them. The loop
ends when four acceptance criteria have named proof artifacts, not when
the chat feels finished.

## How It Grows

Each accepted telos tick writes a lessons-md lesson (LOW) automatically.
That is retain. We do not also lesson-create on every subtask. After each
milestone we run `secondlook-md look` on what that milestone changed and
read the files. We tick with a measurement that is a count of proven
acceptance criteria, never a vibe.

Growth after this north star closes is not more forges. It is other repos
running `lessons-md project-set` and being handed a lesson that changes
their next command. That cannot be claimed until AC-3 exists. If a tick
says pivot, we stop adding harness workarounds and integrate the proofs we
have. If stop fires three times after we addressed it, we hand the leftover
to the owner instead of grinding.

## Metric

name: proven_acceptance_criteria
kind: count
target: 4

## Serves

parent: root
how: lessons.md is the LEARN leg of the Eidos trilogy. This north star
  serves that product by closing the honesty gaps that currently prevent
  adoption. It does not serve PyPI publish, embeddings, or a second clone
  of research.md.

## Invariants

### confirmed_only_via_research_md
must: No lesson in this repo is written or updated to CONFIRMED except after lesson-promote has a real research-md finding id.
case: rg -l "confidence: CONFIRMED" .lessons/lessons && test that each such file has promotes_to.finding_id
irreversible: false

### no_pypi_without_owner
must: This loop does not publish to PyPI. PyPI remains a shipr approval gate.
case: no `twine upload` or `uv publish` in the tick record; .shipr model still lists PyPI publish as an approval gate
irreversible: true

### tick_measurement_is_observed
must: Every telos-md tick measurement is a count of ACs with a named proof artifact, not a hope.
case: docs/acceptance.md shows N of 4 with Verify citations; tick --measurement equals that N
irreversible: false

## Requirements

### ac_weighted_scores
must: research/make-it-better scoring-matrix.md shows weighted totals using the locked weights; DECISION.md no longer treats unweighted 40 as the authority.
case: python3 -c "assert 'weighted' in open('research/make-it-better/.research/evaluations/scoring-matrix.md').read().lower()"
irreversible: false

### ac_cold_review_0006_0007
must: Findings 0006 and 0007 in research/make-it-better have cold peer-review attestations in evaluations/peer-review.md (or an appended review dated after they existed).
case: rg "0006|0007" research/make-it-better/.research/evaluations/peer-review.md
irreversible: false

### ac_independent_apply
must: An artifact exists for a later task that is not lesson-create, whose chosen action changed because an active lesson was printed, with the task and outcome recorded outside LESSON-0002/0003.
case: test -f docs/apply-rate-proof.md && rg -v "LESSON-0002|LESSON-0003" docs/apply-rate-proof.md | rg -q "changed|instead|because"
irreversible: false

### ac_secondlook_two_harnesses
must: A secondlook run after this charter has at least two harnesses with n_findings > 0.
case: python3 -c "import json,pathlib; p=sorted(pathlib.Path('.secondlook/runs').glob('LOOK-*/run.json'))[-1]; r=json.loads(p.read_text()); print(r)"
irreversible: false

## Preferences

- Prefer fixing the record (weights, reviews) before adding product surface
- Prefer one independent apply proof over another dogfood lesson
- Prefer making existing harnesses land over inventing a fifth harness
- Leave P3 and embeddings alone
