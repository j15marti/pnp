# MINUNSAT-BOUNDARY-WITNESS-PROBE1

**Date:** 2026-10-20 09:45 UTC. **Status:** P versus NP remains OPEN.

## Corpus reviewed (bounded)
Git log/tree survey; `main.tex` header/executive status; `research/main/2026-10-20_1748_MAIN_MINIMAL_UNSAT_PROJECTION20.md`; `research/agents/threshold-descent/2026-10-20_1800_MCSP_SPARSE_TEMPLATE_NOGO5_BRIEF.md`. Not a full AGENTS.md corpus reconciliation; `main.tex` was not edited.

## New since last check
MINIMAL-UNSAT-PROJECTION20 (matched minimal-UNSAT collision `F_m` vs `G_m`), MCSP sparse-template KT no-go (ordinary KT polylog for sparse templates), Grok 4.7 review annotation.

## Result (COMPUTATIONAL, m = 2..6)
Independently re-checked PROJECTION20's theorem by brute force: `F_m` UNSAT, `G_m` SAT, 2m+6 clauses / 2m+3 vars in both, all one-clause deletions SAT.

Item 3 of its idea list (boundary-witness repair), probed: for `F_m` every deletion witness violates **exactly** the deleted clause (`F_exact` true for all m tested); `G_m` has a zero-violation full witness. So a *full-assignment* witness per child does separate the twins, via a "violates exactly the deleted clause" check. Scripts: `experiments/2026-10-20_minunsat_exact_violation_probe.py`, output `results/2026-10-20/2026-10-20_minunsat_exact_violation_probe.json` (runs in <1 s).

## Interpretation (CANDIDATE, not proved)
This repair costs a full n-bit witness per child, i.e. it exceeds the square-root space budget the projection route needs. Open arrow: is there a compressed boundary/separator witness of size o(n) per child that still distinguishes the twins for *all* proper 3-CNF families, not only this chain? The chain family itself has width-O(1) separators, so it is not evidence either way. Status: OPEN.

## Next
Test a family with large-treewidth minimal-UNSAT cores (e.g. Tseitin-on-expander minimal subformulas) against separator-size-bounded witnesses.

% END_OF_VERIFIED_REPORT::CLAUDE::MINUNSAT-BOUNDARY-WITNESS-PROBE1
