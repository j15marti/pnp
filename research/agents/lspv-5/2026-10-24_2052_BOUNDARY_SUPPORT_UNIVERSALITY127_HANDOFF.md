# LSPV-5 BOUNDARY-SUPPORT-UNIVERSALITY127 handoff

Status: **PROVED/EXACT** for the comparator/guard family; **COMPUTATIONAL** finite audit; all-input ARC successor **OPEN**; P versus NP **OPEN**.

## Exact theorem

For every proper 3CNF `F`, boundary dimension `d>=1`, and
`1<=h<=2^d`, a uniform linear-record proper-3CNF construction has exact
boundary projection

`Q(b) = [unsigned(b) < h] OR SAT(F)`.

The root is always SAT via `b=0`. If `F` is UNSAT, exactly `h` boundary
points are feasible and exactly `2^d-h` pinned memberships carry the source
SAT bit. Hence every hard-membership count from zero through `2^d-1`
coexists with a source-independent root witness.

One source bit `SAT(F)` determines every hard membership, so multiplicity
does not imply independent SAT work. A hard pinned ordinary child has the
same asymptotic encoded size as the parent (`lambda=1`), yielding only
`t'<=max(r,t)`.

Role 1 DENSE-BOUNDARY-BYPASS128 is the `h=1` endpoint. Role 5
GUARD-CONTINUATION-FIXEDPOINT126 is the `h=2^d-1` endpoint after boundary
renaming. The new comparator construction interpolates all densities.

## Peer red-team

- Role 3 SELECTOR-ERASURE-PRISM91 is exact for its detached projection
  calculus, but its source-aware parity scan prevents all-decider transfer.
- Role 4 REPLAY-ENTROPY86 is exact for a complete replay service, not for a
  one-bit parent SAT decider.
- Role 2 SCC-ODD-ORBIT120 remains a constructive polynomial control for one
  parity row, not a rank-growing ARC edge.

## Reproducibility

`experiments/boundary_support_universality127.py` constructs the actual
proper comparator/guard formulas. It checked 326 base formulas, 4,138
constructed roots, 40,380 boundary restrictions, 4,138 support counts, and
2,976 hard corners: 52,284 assertion-accounted checks, zero failures.
Controls include affine SAT/UNSAT, proper Horn and dual-Horn SAT,
padded-2SAT SAT/UNSAT, and independent components.

Script SHA-256:
`a54d27d76a7e2c6a58a29b364f96c48d64b880f0f1a44bb379cf055ad657896a`.

## Archive status and next obligation

HEREDITARY-SCOPED10 remains available only as a continuity-log summary; no
original proof body or executable was recovered. Do not invent its exact
generator. Any replacement boundary contractor should be tested on the
entire threshold family above, with parent decision, ordinary child bytes,
source reads, failed trials, switching, caches, gluing and peak space all
charged.

The remaining theorem is an all-input uniform jointly charged achievable-
pair successor, or cofinal finite route, into a verified FLMV forbidden box.
