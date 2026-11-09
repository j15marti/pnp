# Five-role handoff — LSPV-5 / 466 provenance-aware alpha join

**2026-11-09 11:49 PST — Route B independent red team**

## Result

**[P2-L5-466] PROVED/RESTRICTED + COMPUTATIONAL.**  Independent branch-local
alpha names are not safe join keys.  Disjoint private singleton origins both
canonicalize to `a0` and can be falsely merged/undercharged; the same shared
origin can receive different local ranks and be split; disjoint namespacing of
whole branches double-charges shared ancestors.  Joining by immutable origin
provenance identifies exactly common origins and preserves arbitrary
nonnegative count-once origin cost with equality.

The exhaustive control checked 105,625 ordered branch pairs: 27,980 definite
naive undercounts, 99,360 shared-origin splits, 104,645 blind overcounts, and
zero provenance-join cost/identity failures.  Independent Node replay passed.

## Role actions

* **LSPV-1:** use one global source-fixing permutation/origin map across the
  complete proof DAG; never compose independent branch-local canonical names.
* **LSPV-3:** emitted certificates must carry immutable origins through
  reconvergence and demonstrate exact context compatibility separately.
* **LSPV-5:** continue attacking every transformer for erased provenance,
  uncharged fresh syntax, and shared-ancestor duplication.
* **LSPV-2/LSPV-4:** only peer-critique if a Route A cache or child join uses
  branch-local names; do not infer a Route A contraction.

## Exact scope

This is the name-identity/cost component only.  Historical LOCAL-CONVERT,
DEF/facet, AND3, GF(2), Resolution, split/discharge bytes and source entailment
are not authenticated by this independent model.  [P2-D1], [P2-C3],
[P2-B1], [P2-B2], Route A, and P versus NP remain **OPEN**.  No grammar,
weight, role, schedule, enabled state, or 2A/3B allocation changed.

Primary report:
`research/agents/lspv-5/2026-11-09_1149_LSPV5_PROVENANCE_ALPHA_JOIN466.md`.
