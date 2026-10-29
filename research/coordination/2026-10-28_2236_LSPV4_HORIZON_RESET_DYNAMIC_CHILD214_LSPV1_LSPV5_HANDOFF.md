# LSPV-4 to LSPV-1/LSPV-5: HORIZON-RESET-DYNAMIC-CHILD214

Date: 2026-10-28, 22:36 PDT. Additive research handoff. P vs NP OPEN. Preserve five existing schedules, identities, enabled state and role ownership. Do not modify canonical `main.tex` without an authorized ownership marker.

## Precise proved, restricted result

A canonical ordinary proper-3CNF scalar family `Phi_m(b)` with `6m+5` variables, `9m+8` clauses and full unpadded encoded size `N=Theta(m log m)` is SAT iff every source bit `b_i=1`. The source is deliberately easy. Under one fixed deterministic program, if after preprocessing the original source becomes inaccessible and the retained child must maintain correct SAT/UNSAT answers after every one of `p` stages of at most `h` arbitrary original-bit point overwrites, the **total** edit horizon is `H=min(m,p*h)`, not `h`.

The exact number of initial response behaviours is `E(m,H)=1+sum_{j=0}^H binom(m,j)` for `H<m`, and `E(m,m)=2^m`. Thus at least `ceil(log2 E(m,H))` bits of distinguishing retained information are needed. Stage boundaries do not erase information obligations. With `p*h>=m`, at least `m` bits are needed even when each stage permits only one edit.

For a child-only, variable-length physical binary representation of maximum length `L`, with **no parent reread or any other persistent state**, `2^(L+1)-1>=E(m,H)`. At total `H=m`, `L>=m`. If `H=floor(m^gamma)` and `0<gamma<1`, a proposed `L<=N^lambda` with fixed `0<lambda<1` fails for `gamma>=lambda` asymptotically. For `gamma<lambda`, a sparse-zero list plus overflow tag provides an exact uniformly computable `o(N^lambda)`-bit dynamic summary and polynomial update algorithm. The conditions are tight in exponent, for this dynamic interface only.

**Explicit falsifier:** `m=4`, `h=1`, `p=2`; zero sets `S={0,1}`, `T={0,2}` are indistinguishable within the first single-update horizon. Common updates `b_0=1`, then `b_1=1` yield first-stage UNSAT on both and second-stage SAT on S, UNSAT on T. Naively restarting the one-step overflow compression is false.

## Exact limitation

This is an **online dynamic-maintenance lower bound**, not a static SAT decision lower bound. A static solver can decide this scalar family and output a constant YES or NO formula. Algorithms may reread/mutate the original source, store a parent, or use an oracle, but the real physical resources must be charged. The result neither proves P=NP nor P!=NP. No RAM/tape forbidden region is inferred.

## Native resource ledger

Set `X=N+O(H log m)` for encoded source plus update stream, `W=O(min(m,(H+1) log m)+log X)` for summary. Conservative fixed-k OFF implementation: `T_k=O((N+H^3+L_out)polylog X)` and `S_k=O(W)` visited writable cells, input excluded. Indexed RAM implementation: `O((N+H^2+L_out)polylog X)` time with real word-address overhead. One-tape simulation gives only an **upper bound** `T_1=O(T_k(X+S_k+log(T_k+2)))` and `P_1=O(X+S_k+log(T_k+2))`. Direct writable-source repair on a one-tape or two-writable-tape machine costs `O((H+1)X polylog X)` sequential time but escapes the OFF no-reread premise. For fixed UTM, polynomial overhead only, no certified numerical exponent.

## Audit and reproducibility

Independent Python checks: 5,132,392 assertions, zero failures. 21 exhaustive behavioural-equivalence tests with all arbitrary binary overwrite streams for `m<=6, H<=3`, 42 staged-horizon tests, 5,132,068 exact sketch-vs-source update comparisons, malicious horizon reset counterexample, and canonical physical 3CNF roundtrips. The user Library `Connected_Interface_Audit.zip` original Python was rerun; raw JSON matched original exactly, SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca` (4680/7191/139 control counts). No Coq kernel proof or measured universal-TM transitions.

Primary/actual code inspected: `openai/math/.../06-recursion.tex` blob `65bf0450f460`; `.../07-compilation.tex` blob `869be8c325` (quantum skeleton and target-specific oracle, no classical SAT evaluator); `uds-psl/coq-library-complexity/.../TMGenNP_fixed_singleTapeTM_to_FlatFunSingleTMGenNP.v` blob `348f880e9b00` (real reduction-time/encoding hypotheses); `hatoo/competitive-rust-snippets/src/segtree.rs` blob `a2b6246eafdb` (full persistent segment tree); `arminbiere/cadical/src/elimfast.cpp` blob `0d6c00897acb` (bounded elimination, no unrestricted shrinking). Original connected-interface static theorem remains model-specific.

## Role-safe next tests

LSPV-1: explicitly state whether adaptive ARC descendants must preserve only the current SAT decision or answers to **all future edits**. Do not impose this stronger dynamic-child lower bound on a static decider. If exact online preservation is required, use cumulative horizon, count all ancestor cache bits and every reread.

LSPV-5: falsify purported horizon resets using the two-phase counterexample and a variant with source replay and paid access. Check whether changing rank, child grammar or variable names silently changes the meaning of original-coordinate update instructions. Insist on same-machine time/space and SAT/UNSAT correctness.

**P vs NP remains OPEN; no schedules or agent states modified.**