## Verdict

The documented weights were correctly applied: all six weighted totals recompute exactly, including 76 for retrieve-on-boot. The winner did not change, but the full ranking did: weighting broke the raw 30–30 tie between outcome-tick and status quo.

## Findings

- [P2] Do not conflate an unchanged winner with an unchanged ranking — research/make-it-better/.research/evaluations/scoring-matrix.md:40  
  Why call the ranking unchanged when the raw ranking contains a tie that the weighted ranking resolves? Why treat displayed row order as mathematical rank? Why trust “same order” if ties are invisible? A documented pre-existing tie-breaker—or an explicit definition of “ranking” as winner-only—would falsify this finding.

## What you would not change

Keep the weighted calculations in `scoring-matrix.md:31-38`; each total is correct. Keep `DECISION.md:12` citing weighted 76 rather than raw 40. Keep the decision itself: retrieve-on-boot remains first, ahead of applies-when 67 and outcome-tick 54.

## Questions for the other reviewers

1. Can any weighted total be recomputed to a value different from the published table?
2. Was a tie-breaker between outcome-tick and status quo established before weighting?
3. Does any project convention define “ranking unchanged” as “winner unchanged”?
