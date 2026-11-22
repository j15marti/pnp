# CHARGED-DECISION-VERIFY1 note

**Date:** 2026-11-21 ~20:00 PT

Small computational test for the decision relation in CHARGED-UNSAT-TRANSPORT1.

For r=5, exhaustive check over all 120! pairs of permutations of {0..4}:

- 120 diagonal inputs are the UNSAT cases (pi=sigma).
- 14280 off-diagonal hybrids each receive a constructive SAT assignment that satisfies the source F0 (left implications, middle OR, right contradictions avoided).

Verification fraction = 1.0.

This confirms Lemma 1 and the preservation under the proper 3-CNF conversion and adjacent-witness compiler for the small case. The matching upper bound and static ceiling of the report remain the scope limit; no superpolynomial claim is made.

P vs NP OPEN. SAT-LOCAL-ERROR1 OPEN.

Next: DYNAMIC-COMPATIBILITY-OBLIGATION1 or further charged accounting on the same family.
