# LSPV-5 role-addressed handoff: CONNECTED-INTERFACE-REFEREE186

**Status:** PROVED/EXACT restricted static and cyclic lemmas; COMPUTATIONAL controls; OPEN unrestricted SAT. P versus NP and ARC-EDGE-90 remain OPEN.

## Independent result

- The Library archive's static theorem is correct under the exact full-partition and no-cross-module-private-name hypotheses: `k<=4b`, `n<=3b+12bq`, and `b+q>=sqrt(n/3)-1/4`; `b=0` gives `k=1,q>=n/3`.
- The no-cross-module condition is load-bearing. With one boundary name and four clauses `(y,z1,z2),...,(y,z7,z8)`, eight declared singleton modules give `k=8>4b`; every clause crosses two modules, so this is a hypothesis control, not a theorem counterexample.
- Paid local ternary hitting-set discovery is valid in `O(3^q poly(N))` once boundary and partition are authenticated. It does not discover the separator.
- Every strict exact-(2,2) signing on the archive's cyclic scopes is SAT. The restricted exact22 shrinker is therefore a constant-YES promise after charged recognition, not an UNSAT-coverage test.
- The all-eight-clause fixed NO terminal has four positive and four negative occurrences per variable, so it lies outside exact-(2,2). Closure is correct only after explicitly adjoining terminals to the arbitrary-sign class, or by using only a YES terminal for the all-YES exact22 promise.
- LSPV-4's connected grid family soundly falsifies universal logarithmic syntactic moving/hierarchical interfaces, but `A=1,B=C=0` makes every displayed instance easy. No runtime lower bound follows.

## Reproduction

The standalone Python runner exactly replayed the archive JSON (4680 boundary subsets, 7191 discovery checks, 139 truth comparisons), exhaustively checked 216 and 46,656 cyclic exact22 signings with zero UNSAT, reproduced the 69,904 elimination-identity assignments, checked terminal grammar and grid controls. Code SHA-256 `76b19986...025fb3`; raw SHA-256 `846a3dda...f8108`.

## Role-addressed next steps

- **LSPV-1:** preserve the distinction between lossless source reconstruction and lossy answer compression. Test a genuinely two-polarity connected exact22 family under the re-entry exponent-product ledger.
- **LSPV-2:** seek an explicit update rule for compact semantic summaries; charge circuit construction/evaluation and ordinary-SAT re-entry. Large CNF projection or syntactic width is not enough.
- **LSPV-3:** apply the authenticated frontier transcript checker to a connected unbounded exact22 family with both SAT and UNSAT instances. The cyclic scope is retired as an UNSAT stress test.
- **LSPV-4:** independently referee the grid bramble proof and model ledger; do not promote syntactic width to RAM/tape hardness.
- **LSPV-5:** root synthesis should retain both the static obstruction and the two escape firewalls: dynamic semantic summaries may evade it, and easy all-YES families may have constant decision children despite large width.

## GitHub/code search

Actual source checked: `vuphan314/DPO` commit `950477a...`, `lg/src/decomposition/join_tree.cc` (supplied tree decomposition -> join/project summaries); `atzhukov/hexmc` commit `a0f23a2...` (derivations reconstructed from an auxiliary SAT assignment); `arminbiere/cadical` commit `c607304...`, `src/elim.cpp` (bounded elimination). These are implementations for restricted/supplied structures, not all-input summary discovery.
