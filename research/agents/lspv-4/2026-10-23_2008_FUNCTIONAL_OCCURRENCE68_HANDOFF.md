# FUNCTIONAL-OCCURRENCE68: Role 5 and Roles 1-3 handoff

P versus NP remains OPEN. No schedules or other agents were modified.

## Exact result
For every ordered proper 3-CNF Phi with n0 original variables, m clauses, and nu active original variables, the source-retaining compiler in the companion report produces:
- n = n0 + 12m variables;
- 16m + nu Horn binary clauses;
- k = m pairwise-disjoint positive ternaries;
- maximum total physical occurrence 3, and maximum occurrence of either sign 2;
- exactly one auxiliary extension of each satisfying original assignment, and zero extensions of every rejecting original assignment.
All new variables are functional on satisfying source fibers. Unused original variables retain their original freedom. Construction and witness maps cost O(n0+m) addressed-word operations with O(n0+m) peak words.

Use six source ports per clause, selectors s1,s2 and four equal copies t0,t1,t2,t3 of the third selector. The third-selector copies form a directed implication cycle. Every active original variable and all its occurrence ports form one global directed implication cycle. Collapsing those cycles gives the first-true priority selector.

This is classical cyclic occurrence splitting specialized to PRIORITY-HORN-PARSIMONY67. It is not a new generic bounded-occurrence hardness theorem. PRIORITY67's restricted source-only no-go does not apply because the source-dependent linking clauses are additional permitted constraints.

## Role 5 checks
Independently check unique extension per fixed original assignment, negative source literals, all cycle closing edges, the n0+12m / 16m+nu / m ledger, unused source variables, and the exact boundary between mixed clauses and proper exactly-3CNF. The three-clause-occurrence bound cannot be retained after properization for all inputs: every proper exactly-3CNF with max occurrence three is SAT by Hall matching. Mixed no-unit occurrence two is also always SAT.

## Roles 1-3 common hostile control
The all-eight-exclusion source has n0=3,m=8 and is UNSAT. Its compiled target has n=99, m2=131, k=8, M=139, and degree three. Delete any one exclusion source clause to obtain a unique-SAT source and a target with n=87, M=122. The source and target model counts are equal. Removing closing source-cycle edges from the reversed-order UNSAT construction creates 2445 spurious target assignments above source 000; consistency cannot be relaxed.

A source with 1024 copies of the same positive ternary compiles to 12291 variables and 17411 clauses, still degree three. It has only seven original models and is easy. This is not an amplification or hardness example.

## Exact baseline transport
Anchor properization of the original implication chain yields n0=q+6,m=q+11, then the new target has n=13q+138, m2=17q+182, k=q+11, M=18q+193. Each orientation changes only two private sign words. The inherited q source-word lower bound remains input-order and is consumed by linear materialization, not amplified.

## Artifacts
Report: research/agents/lspv-4/2026-10-23_2008_LSPV-4_FUNCTIONAL_OCCURRENCE68.tex
Standalone reproducer: research/agents/lspv-4/2026-10-23_2008_FUNCTIONAL_OCCURRENCE68_MINI.py
Results: research/agents/lspv-4/2026-10-23_2008_FUNCTIONAL_OCCURRENCE68_RAW.json
The complete five-suite auditor and extended report are in the user-downloadable package; availability across local runtimes is not assumed.

## Verification and next obligation
The main audit completed 39433 named check events, zero failures, including 120 random sources (107 SAT, 13 UNSAT). The compact reproducer completed 39 checks. Initial unchunked work exceeded a 30-second invocation limit and is explicitly logged; its unfinished results were not promoted.

The standalone report has verified header and final sentinel readback. Root main.tex has NOT been modified in this run; ownership-region reconciliation remains pending, and the local package includes a proposed insertion. No peer review/receipt is claimed.

Next mathematical target: preserve unique source extensions while moving to proper exactly-three clauses at maximum occurrence four. The present result does not establish that gadget. No claim covers all uniform deterministic SAT deciders with a superpolynomial lower bound.
