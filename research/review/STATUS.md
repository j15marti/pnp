# Proof review status

Updated: 2026-10-11. **P versus NP remains OPEN.**

`MODELBRIDGE-0003` proves the exact universal positive boundary for an
arbitrary uniform deterministic 3-SAT decider: external pinning recovers one
satisfying assignment with at most `n+1` calls on canonical 3-CNF inputs of
length `L=N+gamma_len(m+n+1)-gamma_len(m+1)+3n(1+w)`. This extracts one
nonzero entry of the semantic compatibility core, not the full matrix or an
internal solver representation. Free promotion to compatibility-table,
rank, residual-DAG, OBDD, d-DNNF, provenance, memory, or time necessity is
**FALSIFIED/RETIRED**. `CORE-ACQUIRE1` remains **OPEN**.

`PROOFMAP-0004` integrates CC-0005 and RT-0003 and falsifies a free
minimal-DAG transfer. For the treewidth-one equality 2-CNF, the exact
grouped-order ROBDD size is `3*(2^n-1)`, the interleaved-order size is `3n`,
and the fixed-instance SAT decision DAG has at most one constant node.
Therefore OBDD, d-DNNF, pebbling, treewidth, rank, or residual-DAG lower
bounds remain representation/interface-specific until `DAG-ACQUIRE1` forces
every uniform SAT decider into the same charged model.

`PROOFMAP-0003` integrates REDTEAM RT-0002. The prior shared-input acquirer omitted writable-verifier reset. A reset-aware direct explicit-input theorem is now proved at its declared scope; recursive implicit acquisition and every separation-bearing construction remain open.

## Current route ranking

1. **Strict successor / charged wrapper — CONDITIONAL.** Exact composition is available, but the solver-independent all-input ordinary-CNF successor with strict shrink, descendant closure, physical access, and simultaneous same-machine resources is OPEN.
2. **Bounded-list PFCERT — CONDITIONAL.** Counting and the immunity endpoint are exact. A globally bounded accepted-output verifier with extensional endpoint binding remains OPEN. Direct enumeration is no longer the bookkeeping gap once reset is charged; verifier construction is.
3. **LSPV Boolean separator — OPEN.** Representation and restricted source-probe theorems exist. Arbitrary-SAT extraction/reconstruction and a nonrelativizing model-matched lower-bound hinge do not.
4. **ARC15 / finite portfolios — COMPUTATIONAL.** Finite positive coverage does not close UNSAT/fallback or prove an all-input joint bound.
5. **Minimal DAG / pebbling — RESTRICTED-MODEL EXACT, arbitrary transfer OPEN.** Fixed-DAG tradeoffs are genuine; the unavoidable same-execution compiler is not known.

## New synthesis result

- **G1 PROVED/EXACT scoped:** equality 2-CNF has grouped ROBDD size
  `3*(2^n-1)` and interleaved size `3n`; fixed-instance decision-only size is
  at most one.
- **FALSIFIED/RETIRED:** large minimal DAG in one declared representation
  implies large cost for every exact SAT decider.
- **G2 / DAG-ACQUIRE1 OPEN:** obtain an unavoidable, same-execution mapping
  from every uniform SAT decider to one fixed lower-bound DAG/query model,
  charging compilation, order search, local access, replay and peak space.

- **C2a PROVED/EXACT scoped:** if a deterministic verifier has shared read-only input, a computable writable-cell visitation bound `b(M)`, and blank-start semantics, exhaustive acquisition can explicitly clear that workspace before each candidate. Its time is
  `O((2^(w+1)-1)(q+r+w+log(M+2))+w)` and writable space is `O(s+w+log M)`, with conservative reset `r=O(b log(b+2))`.
- If `b<=q`, `w=kappa log_2 M+o(log M)`, and `q=M^(v+o(1))`, reset preserves exponent `kappa+v`.
- **C2b OPEN:** implicit descendants, local source access, reset/replay, ancestor/transient space, and current-scale calls still require one charged recursive realization.
- The old CC-0003 state-persistent proof and stateless harness are **FALSIFIED/RETIRED as a reset proof**. RT-0002's one-cell counterexample is accepted.

## Highest-value next links

- MODEL_BRIDGE: prove or falsify `CORE-ACQUIRE1`, a same-execution transfer
  from every 3-SAT decider to one fixed lower-bound interface; external
  search-to-decision alone is now closed and insufficient.
- LOWER_BOUND: test arbitrary-decider acquisition against the reset-aware acquirer and matched oracle replacement.
- COST_CERTIFICATES: incorporate the reset premise, then construct or refute a globally two-valued PFCERT verifier for `t(n)=n^(log n)` with exact witness and verifier exponents.
- REDTEAM: audit computable `b`, tape separation, and the exclusion of implicit-child access.
- All roles: test `DAG-ACQUIRE1` against direct decision, interleaved order,
  affine elimination, padding, and INTERP/RECOMP before using any DAG size or
  pebbling lower bound.

## Reproducibility and scope

The new bounded harness passed 18 dirty-state counterexamples, 18 reset controls, 108 exact-integer exponent cases, and an invalid `b>q` control under a 25-second cooperative budget. Five additional Drive artifacts and current primary sources were read. This is cumulative targeted review, not an assertion that all chats, repository history, Drive files, or literature were exhausted.

The universal cosine-product bound remains retired. Finite 12/13 coverage does not close UNSAT/fallback. Formal LaTeX is not machine-checked unless an actual proof assistant verifies it.

