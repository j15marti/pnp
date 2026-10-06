# FP–FNP Revised Proof Track

Timestamp: 2026-10-06 11:46 PT  
Status: OPEN.  
Global implication: under the standard polynomially balanced search convention, FP = FNP iff P = NP.

## Why this track exists

The October 6 WRAPPED-CSE audit changed the decision-track front end. A canonical SAT wrapper now exposes an answer-preserving restriction path for every exact decider, so internal path extraction is no longer the principal decision-side obstacle.

The function/search track is still worth maintaining separately because Search-SAT requires an explicit witness output. This removes the need to manufacture a rich output object from a one-bit decision answer.

## Starting contradiction

Assume

FP = FNP.

Fix one FNP-complete relation R*(x,y). Then there is a deterministic polynomial-time selector S such that whenever a valid witness exists,

R*(x,S(x)) = 1.

For Search-SAT, S(F) is an explicit satisfying assignment.

## What this removes relative to the decision track

### PROVED/EXACT simplification: output-object exposure

The computation specification itself requires a polynomial-length witness. Therefore the track does not need WRAPPED-SELFRED1 merely to expose an assignment-related object.

Path exposure / "does the arbitrary algorithm ever construct a witness-like object?" is no longer an open interface.

### Important guard

A polynomial-length witness is not itself a superpolynomial resource.

|y| = poly(|x|)

only forces polynomial output work/storage.

The lower bound must come from dependency, acquisition, sequentiality, reacquisition, source constraints, or some other implementation-independent theorem.

## What replaces decision-track consumer-validity

Ordinary FNP permits any valid witness.

Therefore the key structural target is not "find a consumer U" but:

WITNESS-ROBUST1 (OPEN):
for one fixed FNP-complete relation R*, every valid witness y for selected hard instances x induces the required resource-bearing property H(D(x,y)).

Formally, for a hard family x_n,

for all y, R*(x_n,y)=1 => H(D(x_n,y)).

If even one easy valid witness exists, an arbitrary selector may choose it.

Thus the decision-track KAPPA-MISMATCH problem is partially replaced by an all-witness robustness problem.

## Core load-bearing theorem

OUTPUT-TO-RESOURCE1 (OPEN):

For every deterministic polynomial-time candidate selector S, every valid output y=S(x), and every legal implementation/representation,

producing y (or satisfying the declared source-dependent obligations attached to y) forces resource

R(S,x) >= L(D(x,y)).

The theorem must survive:
- direct computation of y without traversing the intended D;
- reread/recomputation;
- DAG sharing/memoization;
- alternative representations;
- DEAD/COPY/DELAY/INTERP/RECOMP;
- semantic and algebraic oracles;
- easy controls (Horn, 2-SAT, affine/Tseitin, bounded treewidth).

## Superpolynomial family target

SUPER-WITNESS1 (OPEN):

Construct one fixed FNP relation R* and instances x_n such that every valid witness satisfies

L(D(x_n,y)) = n^{omega(1)}

in the exact ordinary computational model used by OUTPUT-TO-RESOURCE1.

Together:

FP = FNP
=> polynomial selector S for R*
=> WITNESS-ROBUST1
=> OUTPUT-TO-RESOURCE1
=> SUPER-WITNESS1
=> S is not polynomial
=> contradiction
=> FP != FNP
=> P != NP.

## Relation to the decision route

Decision route:
- canonical path exposure is now solved by WRAPPED-SELFRED1;
- open: consumer-valid K_U or direct wrapped-process lower bound.

Function route:
- explicit witness exposure is intrinsic;
- open: all-witness robustness and output-to-resource lower bound.

Neither route currently removes the ordinary-source acquisition/use lower bound, nonrelativization, nonalgebrization, or endpoint/model matching.

## Canonical-output subtrack

A canonical function such as lexicographically first satisfying assignment removes witness-choice freedom.

However this is not ordinary multivalued FNP search. It naturally belongs to an optimization/oracle-function framework such as FP^NP under standard formulations.

Under P=NP it becomes polynomial-time computable, so it remains a legitimate contradiction descendant, but it must not be mislabeled as ordinary FNP.

Potential advantage:
- no all-witness quantifier.

Remaining burden:
- prove computing the canonical output forces a superpolynomial ordinary resource.

## Relation to prior October 1 search spine

This document updates, rather than retires:
- research/explorations/search-spine/2026-10-01_FP-FNP_PARALLEL-PROOF-SPINE.tex
- research/explorations/search-spine/2026-10-01_FP-FNP_G-PRECOMMITMENT-SPINE.md
- tasks/TASK-007_Search-G-precommitment-resource.md

The older STORE-or-REACQUIRE and delayed-audit lemmas remain valid at their stated interface scope. The present revision makes clear that the central unrestricted gap is still the superpolynomial output/acquisition theorem, not exposure of a witness object.

## Status

PROVED/EXACT:
- FP=FNP iff P=NP under the declared search convention.
- Search-SAT exposes an explicit witness output.
- output length alone yields at most polynomial cost.

OPEN:
- WITNESS-ROBUST1.
- OUTPUT-TO-RESOURCE1.
- SUPER-WITNESS1.
- nonrelativizing ordinary-source hinge.
- nonalgebrizing discharge.
- exact model-matched endpoint.

P vs NP remains OPEN.
