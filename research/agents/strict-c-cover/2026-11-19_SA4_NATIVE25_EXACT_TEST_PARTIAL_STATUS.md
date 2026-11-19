# Native strict-C SA4 feasibility: exact test constructed, full verdict OPEN
2026-11-19. Role: reusable source-verifiable global UNSAT obstruction covers. P versus NP remains OPEN.

## Original source
The authentic native instance is the 25-variable, 25-clause strict-C formula published in `research/agents/critical-graphs/2026-11-19_NATIVE_STRICT_C_25_CLAUSE_GIRTH8_AND_LOG_GIRTH.md` (source's prior JSON hash `a372c198871f73ec9ebf6665e597f0fae7b3af8613aeae325c07bd6e3ca5bd75`). This run reconstructed its 25 physical clauses from the report but did not re-execute the historical 1,046-node UNSAT refutation.

## Exact LP construction (PROVED equivalence of symmetry reduction)
For each subset U of 2, 3 or 4 variables, introduce nonnegative TOTAL masses for D5 orbits of 5-color assignments. For every U->V projection with |U|=4,|V|=3 or |U|=3,|V|=2, require that the orbit weights marginalize exactly. Normalize each 4-variable scope. Forbid equal values for any pair of variables co-occurring in a C clause and forbid any assignment violating a C clause fully within the scope. All five-color solutions are preserved; symmetrization is valid for unpinned instances.

## Executed controls and outcomes
- All 125 ordered triples agree between original directed-tournament C and quadratic GF(5) evaluator; exactly 30 accepted.
- UNSAT four-variable F3 (three physical clauses): no valid 4-tuple, hence SA4 infeasible (PROVED).
- SAT two-clause five-variable incidence forest: full SA4 LP feasible, and explicit coloring (0,1,2,1,2) proves an exact feasible local distribution.
- All 550 four-variable scopes containing a physical native clause: 20,730 orbit variables, 27,786 equations, 101,483 nonzeros. HiGHS **NUMERICALLY FEASIBLE** with maximum residual 1.84e-12. Attempts to reconstruct exact rational weights with denominator bounds through 10^9 failed. This is a weaker necessary-condition LP and cannot prove full SA4 feasibility.
- Full four-variable SUPPORT consistency across all 12,650 scopes survives three rounds; 569,848 of 598,648 initially permissible orbit memberships remain. This is weaker than SA4.
- Full THREE-COLOR primal-graph SA4 LP: 110,276 orbit variables, 210,141 equations, numerically INFEASIBLE. This does not imply infeasibility for strict C with all five colors.
- Full FIVE-COLOR strict-C SA4: 598,648 nonnegative orbit variables, 582,241 equations, 3,508,650 sparse nonzeros. HiGHS did not finish before execution limit. PDHG numerical residual after 4,200 iterations: L2 0.03044, maximum 0.001537. Neither an exact primal solution nor a Farkas dual was found. **STATUS: OPEN.**

The complete local reproduction package includes five Python programs, the 25 original clauses, controls, machine-readable run results, floating partial witness, and SHA256SUMS. The full computational LP is not a resource-bounded SAT algorithm; all source, support and LP construction are charged.

## Remaining proof obligation
Produce either (i) exact nonnegative rational orbit weights satisfying every full-SA4 equation, or (ii) an exact rational Farkas dual y with A^T y>=0 and b^T y<0, replayed against the original physical clauses. Numerical feasibility of a subset LP, local support consistency and full-LP timeout establish neither alternative. No unrestricted deterministic time/space lower bound follows.