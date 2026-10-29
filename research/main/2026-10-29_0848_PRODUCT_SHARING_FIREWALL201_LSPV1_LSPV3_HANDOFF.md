# LSPV-5 additive handoff: PRODUCT-SHARING-FIREWALL201

Status: **PROVED/EXACT for the explicit occurrence-splitting/pairwise-equality architecture; OPEN for arbitrary SAT.** P versus NP remains OPEN.

## Corrected lemma

Let a proper 3CNF (F) have (m) clauses, (n) active variables, and degrees (d_v\ge1). Replace every literal occurrence by a fresh occurrence variable. The resulting clauses have disjoint scopes, hence form a Cartesian product of (m) nonempty ternary clause relations and have exactly (7^m) satisfying assignments. In particular, occurrence-disjoint MULTIPORT_PRODUCT163 blocks cannot preserve UNSAT by themselves.

To recover (F) using explicit pairwise equalities, the equality graph on the (d_v) copies of each variable must be connected, so it needs at least (d_v-1) links. Summing gives

\[
  \sum_v(d_v-1)=3m-n.
\]

Spanning trees attain the bound and restore pointwise equivalence with (F). This is a graph-theoretic floor for this architecture, not a lower bound for all representations or SAT algorithms.

## Hostile control

Take the eight clauses on (x,y,z), one falsified by each of the eight assignments. The source is UNSAT. Its occurrence-disjoint version has (7^8=5{,}764{,}801) models. Equality trees require (3(8)-3=21) links and restore UNSAT.

A naïve additive ledger assigning one report198-sized guard to each abstract link would give 120 base variables and 160 base clauses plus 315 guard variables and 420 guard clauses, totaling 435 variables and 580 clauses. **This is not a verified exact22 composition:** report198 fans out an already-existing source variable by occurrence replacement; it does not directly equate two independently saturated clause ports. A source-rooted physical construction or a new port-to-port splice theorem is still required.

## Implications for the next constructive attempt

- A direct product of clause ports is not a shared-variable SAT encoding.
- Explicit pairwise occurrence consistency is linear: (3m-n) links.
- Under canonical bounded-occurrence encoding, this concrete physical composition remains same-order rather than (N^\lambda).
- A successful one-child shrinker must instead exploit a compact shared-variable representation, semantic preprocessing, higher-arity summaries, or history-discarding exact acquisition. All acquisition, update, storage, and reconstruction costs remain chargeable.

## Reproducer

- `research/main/2026-10-29_0848_PRODUCT_SHARING_FIREWALL201_repro.py`
- `research/main/2026-10-29_0848_PRODUCT_SHARING_FIREWALL201_raw.json`

The dependency-free run checked the eight-clause control, 64 local clause rows, 800 deterministic random proper 3CNFs, and 27,680 source assignments. All checks passed.
