# SHORTCHALLENGE1: bounded universal transcripts collapse to NP

Date: 2026-10-21
Status: PROVED (standard QBF/CNF model) with finite reproducibility checks; no P vs NP separation.

## Theorem: strategy-unrolling bound

Let Phi be a polynomial-size prenex QBF with arbitrary polynomially many alternating quantifier blocks, polynomial-time matrix V, and q universally quantified Boolean bits in total. There is a deterministic reduction to ordinary SAT, with construction cost and output size at most 2^q poly(N), where N is the encoded input length. Thus q=O(log N) implies the restricted QBF family belongs to NP, even with polynomially many alternating blocks.

For a 3-CNF matrix F with n original variables and m clauses, write a fresh SAT variable s_(e,h) for every existential variable e and assignment h to all universal variables occurring *before* e. For each complete universal choice beta, copy F, substitute its universal bits, and substitute s_(e,beta|U_before_e) for e. Conjoin all 2^q copies. The output has at most n*2^q strategy variables and m*2^q clauses, of width at most 3.

Truth implies a causal Skolem strategy satisfying the unrolled CNF. A satisfying assignment to the unrolled CNF supplies a causal strategy, since earlier existential choices cannot depend on later universal bits. This proves equivalence.

Short clauses can be converted to proper width-3 CNF using one fresh variable for width 2 and two for width 1; empty clauses yield a fixed unsatisfiable proper 3-CNF. Then the existing seven-clause balancing/clone-cycle/Q-port compiler gives a signed exact-(2,2) 3-CNF with at most constant-factor overhead. This is an ordinary SAT reduction, NOT a preservation of higher-level hardness.

## Implication for iterative hashes and the time-sampled WRAPPER

For r stages with at most h universal challenge bits per stage, q<=rh. If rh=O(log N), the complete QBF can be compiled into ordinary SAT in polynomial time irrespective of its nominal number of alternating quantifiers. Six- and eight-character base-62 outputs are fixed-width labels (<36 and <48 bits respectively); their FNV-1a implementations do not establish one-wayness or a computation lower bound. If the bitstream, timestamp, or state requires more than a polynomially verifiable discrete predicate, standard PH/QBF classifications cannot simply be applied.

For r=Theta(N), q can grow linearly and this unrolling can be exponential. That does NOT prove difficulty: the easy roundwise identity game forall y1 exists z1 ... forall yr exists zr AND_i(zi=y_i) has a linear-size winning strategy but an explicit strategy table with 2^(r+1)-2 variables.

## Exact finite audits

- 2,040 exhaustive small QBFs: every nonempty subset of the eight width-3 clauses on three variables, times all eight quantifier patterns. Source QBF oracle and independent DPLL solver of the Skolem unrolling agreed.
- 154 seeded random QBFs on 3-8 variables: 76 true, 78 false, with zero mismatches.
- Seven alternating identity games: r=1..7; explicit strategy variable count 2^(r+1)-2 verified.
- Independent MILP/HIGHS solved an exact-(2,2) target of 576 variables/768 clauses as SAT and another of 144 variables/192 clauses as UNSAT, matching the original QBFs.
- An additional forall-exists-forall-exists source compiled to 288-variable/384-clause exact-(2,2) matrix: all 16 original-assignment canonical fibers matched; two independent challenge-wise MILP checks agreed (one winning, one losing).
- Source code in the present conversation: qbf_short_challenge_audit.py, qbf_independent_exact22_check.py, QBF_SHORT_CHALLENGE_THEOREM.md, and the prior qbf_exact22_lift.py.

## Research implications and strict caveat

The previously verified unrestricted 3-block exact-(2,2) QBF remains Sigma_3^P complete when universal blocks are unrestricted. A log-total-universal-bits subfamily cannot inherit that classification unless PH collapses. With unbounded alternation and poly(N) universal bits, standard TQBF can be PSPACE-complete; the existing fiberwise compiler moves all auxiliaries to a final existential block while preserving original quantifier order.

Cai-Watanabe gives explicit Sigma_2^P languages with circuit-size lower bounds >n^k and an available quantified deciding exponent k^2+k. Strategy unrolling does not remove a polynomial-sized universal block efficiently, and no exponent-preserving quantified-to-ordinary-SAT transformation follows from these observations. Neither representation growth nor hash labels imply a general SAT runtime lower bound.

Next research target: q=omega(log N), genuine adversarial-history-dependent predicates, and unconditional compact-strategy circuit lower bounds or a fully charged bridge to an existing time-space lower bound. For every attempt, distinguish output/table size from any required all-algorithm work.