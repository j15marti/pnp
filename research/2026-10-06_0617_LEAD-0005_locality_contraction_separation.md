# LEAD-0005 - Locality is not contraction

Agent: LEAD
Global status: P versus NP remains OPEN.

## Result 1: LOCALITY-NOT-CONTRACTION1
Status: PROVED/EXACT as a logical accounting separation.

If every requested coordinate of an output object can be reconstructed in subpolynomial time and space, this does not imply that the total output or source has sublinear polynomial scale. Locality constrains the coordinate map, not the number of legal output coordinates. For any fixed q>0, an object can expose N^q locally computable coordinates. Thus exponent-level local reconstruction overhead lambda=0 is compatible with global exponent theta=q, including theta>=1.

Therefore LOCAL-ADDRESSABILITY and CSE contraction theta<1 are independent obligations.

Agrawal-Allender-Rudich (JCSS 1998) is a literature control: very local nonuniform reductions can preserve NP completeness. Their strong-uniform caveat means this is not a uniform CSE construction.

## Result 2: LOCAL-COOK-LEVIN-GUARD1
Status: PROVED/EXACT architectural guard.

A fixed-machine Cook-Levin/tableau encoding can be locally described once a time bound T is fixed, but its global size is polynomial in T. If a hypothetical SAT decider has T(N)=N^k, encoding its computation has scale depending positively on the unknown k. It therefore does not by itself yield recursively consumable children of scale N^theta with fixed theta<1 independent of k.

On-the-fly tableau generation may solve virtual-input addressability while failing the load-bearing contraction requirement.

## Consequence
A Williams-targeting CSE candidate must independently prove contraction, local addressability, charged fanout/local work, charged workspace, recursive closure, and machine-model match. Under LEAD-0004, a candidate with lambda=0 but theta>=1 cannot enter the contraction recurrence.

## Hostile controls
Identity and replicated identity are perfectly local but noncontractive. Cook-Levin/tableau is locally generable but its global scale follows simulated time. Very-local completeness reductions show locality does not imply length decrease. Ordinary SAT restrictions are local but generally only additively smaller and remain oracle-shadowable.

## Barrier audit
These statements relativize and do not escape algebrization. They are not the missing hinge. Arbitrary-algorithm CSE remains OPEN. A separate nonalgebrizing hinge remains missing.

## Next target
CONTRACTION-FORCING1 - CANDIDATE/OPEN.

Find a SAT-specific theorem forcing, from every hypothetical polynomial-time exact SAT decider, recursively consumable source objects of scale N^theta with theta<1, without deciding the parent, hiding a current-scale SAT call, assuming a solver representation, or merely invoking a local/tableau reduction. It must survive DEAD/COPY/DELAY/INTERP/RECOMP and be fully charged.

## Handoffs
PROOF: keep theta<1 independent from local-addressability lambda.
RED: build maximally local but noncontractive controls: identity, replicated identity, tableau, and very-local completeness reductions.
RESEARCH: search specifically for uniform exact worst-case local-and-length-decreasing self-reductions for SAT/3-SAT, and record whether any achieves N to N^theta with theta<1 without deciding the parent.
WRITE: integrate only after verification.

## Status ledger
LOCALITY-NOT-CONTRACTION1: PROVED/EXACT.
LOCAL-COOK-LEVIN-GUARD1: PROVED/EXACT architectural guard.
CONTRACTION-FORCING1: CANDIDATE/OPEN.
Arbitrary-algorithm CSE: OPEN.
Nonrelativizing hinge: OPEN.
Nonalgebrizing hinge: OPEN.
P versus NP: OPEN.

## References
1. Agrawal, Allender, Rudich, Reductions in Circuit Complexity: An Isomorphism Theorem and a Gap Theorem, JCSS 57(2), 1998.
2. Williams, Alternation-Trading Proofs, Linear Programming, and Lower Bounds, STACS 2010 / TOCT 2013.
