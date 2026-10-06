# RED-0003 — Canonical-source / minimization attack

**Agent:** RED
**Global status:** P versus NP remains OPEN.
**Target status:** ASCS fixed-machine lemmas survive; canonical-source repair narrowed.

## Finding

A free "canonical/minimum equivalent source" is not a valid repair for ASCS wrapper dependence.

There is a trilemma.

1. If canonicalization is syntactic and efficiently computable, arbitrary semantics-preserving wrappers such as INTERP, RECOMP, DELAY, padding, DEAD and COPY need not disappear unless the wrapper class is explicitly typed and restricted.

2. If canonicalization is extensional across all equivalent implementations, it becomes a program/circuit minimization or equivalence problem. This lands close to MCSP/MKTP/Kt meta-complexity. Such minimization cannot be assumed free.

3. If the canonical source is fixed by the proof architecture rather than the candidate implementation, one still needs a charged compiler from an arbitrary SAT decider to that canonical source. This is essentially a strengthened CSE/source-extraction obligation, so the missing bridge is relocated rather than removed.

Quantifier warning: "forall A,F exists Q" is insufficient. Existence of an equivalent canonical realization is not acquisition. A useful theorem needs an explicit charged transformation with no hidden SAT/minimization oracle.

## Proposed replacement

**SOURCE-TRANSPORT1 (CANDIDATE).** Fix a typed source language, conditioning schema, and allowed wrapper monoid W. For each w in W, require an explicit polynomial-time transport map on source certificates with bounded additive description overhead and bounded verification-time/circuit overhead. Do not minimize over all semantically equivalent programs.

This is more plausible than semantic canonicalization but still does not solve arbitrary-algorithm CSE. The proof must establish coverage of arbitrary relevant implementations.

## Natural-proofs audit

If an ASCS-to-Boolean/circuit transfer yields an efficiently recognizable large property separating small circuits, a Razborov-Rudich audit becomes mandatory. ASCS itself does not automatically instantiate a natural property, but a later truth-table/circuit transfer may.

## P=NP-compatible controls

No evidence for P=NP found. Polynomial universal residual evaluation, replay/recomputation, algebraic compression on affine controls, and semantic minimization granted as an uncharged primitive all remain compatible with P=NP and therefore cannot alone yield the contradiction.

## Handoffs

LEAD: do not use semantic canonicalization as a free ASCS repair.
PROOF: formalize SOURCE-TRANSPORT1 and composition overhead.
RESEARCH: compare with resource-bounded Kolmogorov and MCSP/MKTP minimization/search-to-decision barriers.
WRITE: add warning to main2/main3 while preserving fixed-U ASCS theorem status.

## Next RED target

Attack SOURCE-TRANSPORT1 under composed wrappers. Determine whether preserving same-realization source identity forces enough accumulated description/time overhead to erase ASCS density or verifier-size slack, or whether restricting the wrapper monoid enough to preserve slack makes the theorem too weak for arbitrary SAT implementations.
