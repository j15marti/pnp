# PROOF-0011 — VIRTUAL-CHILD-SPACE1

**Agent:** PROOF
**Global status:** P versus NP remains OPEN.
**Status:** PROVED/EXACT as an accounting theorem in the stated deterministic random-access recursive model. The CSE application is CONDITIONAL because arbitrary-algorithm CSE remains open.

## Formal model

For source length N, let parent source X be read-only random-accessible. A legal child is specified by metadata mu of length N^{o(1)} and has encoding Y=Child(X,mu) of length M<=N^{theta+o(1)}, 0<=theta<1. Assume a deterministic bit transducer B computes every requested Y_i from (X,mu,i) in N^{o(1)} time and N^{o(1)} work space. Let A be a deterministic random-access algorithm on explicit Y with time T(M), work space S(M), and read-only input excluded from work-space accounting.

## VIRTUAL-CHILD-SPACE1

There is an exact deterministic virtual-input simulation with

S_virt(N) <= S(M)+N^{o(1)}

and

T_virt(N) <= T(M) N^{o(1)}.

### Proof

Simulate A instruction by instruction. For each read of Y_i, run B on (X,mu,i), return that bit, and discard B's temporary workspace. Induction on simulated steps gives exactly the same state sequence and output as A(Y). Live memory is A's workspace plus metadata/address state plus one B invocation, so space is additive. At most T(M) input reads/instructions each incur N^{o(1)} overhead, giving T(M)N^{o(1)} time.

## Recursive virtualization corollary

For depth-first recursive CSE with N -> N^{theta+o(1)}, N^{o(1)} local workspace, and the same N^{o(1)} per-bit local-addressability at every scale, explicit child materialization is unnecessary. The O(log log N) active-level metadata/transducer stack remains N^{o(1)} space. N^{o(1)} per-access overhead does not change a fixed polynomial time exponent C.

Conditional on a valid CSE extraction and C<2cos(pi/7), this gives one exact route to the N^{o(1)}-space premise required by the Williams small-space SAT endpoint.

## Limits

The theorem does not construct CSE or prove local addressability. If a child bit requires N^sigma workspace for fixed sigma>0, explicit materialization, uncharged SAT queries, or retained parallel siblings, the premise/space conclusion fails or those costs must be charged. If the parent is itself virtual, transducers must be recursively composed with all overhead charged. Machine conventions must match the lower-bound model.

## Barrier audit

The theorem relativizes: giving simulator and transducer the same oracle preserves the proof. It likewise survives a common algebraic-oracle extension. It is not the nonrelativizing or nonalgebrizing hinge.

## Hostile controls

COPY is unnecessary under the premise. RECOMP is permitted and charged in time. DELAY only increases time. MEMO can increase space and is unnecessary. INTERP is allowed only with charged overhead. Padding is measured against the final parent input length. Easy 2-SAT, Horn, XOR/Tseitin, and bounded-treewidth controls also satisfy the simulation principle, confirming this is accounting rather than hardness.

## New proof obligation

A CSE route targeting Williams should prove LOCAL-ADDRESSABILITY:

For every extracted child and requested child address i, a uniform ordinary transducer computes that child bit from the still-accessible parent source and charged metadata in N^{o(1)} time and space.

This is stronger than semantic existence of a smaller child and weaker than explicit materialization.

## Handoffs

LEAD: add LOCAL-ADDRESSABILITY to CSE routes targeting Williams small-space.
RED: attack local addressability via global canonicalization/minimization, SAT-query dependence, and recursive transducer composition.
RESEARCH: search on-the-fly Cook-Levin, succinct/local reductions, and random-access simulations with polylogarithmic per-bit reconstruction.
WRITE: integrate VIRTUAL-CHILD-SPACE1 as PROVED/EXACT accounting; keep CSE local addressability OPEN.

## Status ledger

VIRTUAL-CHILD-SPACE1: PROVED/EXACT accounting.
Recursive virtualization: PROVED/EXACT under stated hypotheses.
CSE local addressability for arbitrary SAT algorithms: OPEN.
Arbitrary-algorithm CSE/source extraction: OPEN.
FSC: OPEN.
Nonrelativizing/nonalgebrizing transfer: OPEN.
P versus NP: OPEN.
