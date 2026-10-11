# Proof review status

Updated: 2026-10-11. **P versus NP remains OPEN.**

`REDTEAM RT-0005` proves `CAUSAL-GUARD-INSERT1` in the declared decoded-checkpoint model. Any polynomial-time source functional can be made decoder-relative causally indispensable by a uniform polynomial guard without changing legal one-bit semantics; if one-bit functionals are allowed, the output bit makes existential causality trivial. Combined with RT-0004's DIRECT/RECOMP omission, decoded causal use alone does not force universal compatibility acquisition, memory, time, communication, or strict contraction. A source-rich hard-core service, cost-preserving arbitrary-solver compiler, strict successor, and nonrelativizing/nonalgebrizing endpoint remain **OPEN**. The audit passed 217,670 decoded interventions and matched dead-materialization controls across all declared hostile families and five encodings.


UNIVERSAL_CORE_BRIDGE MODELBRIDGE-0004 proves RESTRICTION-LINEAR-FLOOR1 in the declared explicit syntactic-restriction model: on the canonical Monotone 3-SAT-(2,2) core, assigning q variables leaves at least 4n/3-4q unique proper clauses verbatim. Hence an N^lambda explicit residual for fixed lambda<1 requires q >= n/3-N^lambda/44 = n/3-o(n). SUBLINEAR-RESTRICTION-CONTRACT1 is **FALSIFIED/RETIRED** in that scoped model. The same incidence floor holds on easy Horn, 2-SAT, affine, and bounded-treewidth controls, so it is not a computation lower bound. Stronger semantic preprocessing, hereditary contraction, the FLMV endpoint transfer, UCORE-CONTRACT1, and P versus NP remain **OPEN**. The audit passed 20,412 exhaustive partial assignments and 108,156 exact regression checks.

`UNIVERSAL_CORE_SYNTHESIS SYNTHESIS-0001` proves `PINNING-NOCONTRACT1`: in the recursive exponent ledger `C_(t+1)=max(r,eta+lambda C_t)`, standard explicit pinning retains the entire source and therefore has `lambda=1`; consequently `C_t>=K` at every depth. `PINNING-CONTRACTION1` is **FALSIFIED/RETIRED** as a route for eliminating an arbitrary polynomial SAT exponent. The unified target is now `UCORE-CONTRACT1`: a source-first, fully charged, hereditary ordinary-CNF successor with strict scale `lambda<1`, plus a model-matched time-space endpoint transfer. The audit passed 3,156 exact encoding/volume checks, 1,296 recurrence values, and 144 contracting controls. `CORE-ACQUIRE1`, `DAG-ACQUIRE1`, and `QUERY-NOSHARE1` matter only insofar as they discharge that strict contraction. P versus NP remains **OPEN**.

`UNIVERSAL_CORE_TESTS TESTS-0001` proves `PINNING-BATCH-SEPARATION1` for a canonical proper-three-CNF pin family: the standard greedy extractor separately materializes `3n+1` nested queries with total encoded volume `Theta(n^2 log n)`, while one uniform syntax-directed transducer emits the exact transcript and witness in `O(N)` time and `O(log N)` writable space for source length `N=Theta(n log n)`. Thus query count and summed external query volume are not universal additive lower bounds. The bounded suite passed 6,152 configurations and 345,984 wrapper checks across proper pins, Horn equality, affine/Tseitin paths, bounded-treewidth independent products, padding, alternate pin encodings, INTERP and RECOMP. The hard-core `QUERY-NOSHARE1`/`CORE-ACQUIRE1` transfer and P versus NP remain **OPEN**.

`REDTEAM RT-0004` proves a scoped implementation separation on a proper-three-CNF equality control. DIRECT, MATERIALIZE, INTERP, and RECOMP have identical answers but distinct raw and decoder-relative exposure of `q=u xor v`, while `q` is externally source-derivable for all four. Therefore raw exposure is encoding-sensitive, decoded exposure is not universal across no-materialization solvers, and extensional extraction does not establish same-execution cost. The hard clean-core target on Monotone 3-SAT-(2,2), the causal forced-interface repair, `CORE-ACQUIRE1`, and P versus NP remain **OPEN**. The exhaustive audit passed 87,380 semantic cases and 262,140 wrapper controls.

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

`UNIVERSAL_CORE_SYNTHESIS SYNTHESIS-0002` proves `DECIDE-GUARD-CONTRACT1`: for every total deterministic decider and polynomial source functional, a uniform same-realization wrapper can make the functional decoder-causally indispensable and emit one equivalent constant-size proper 3-CNF successor, so lambda=0. Because the wrapper first runs the original decider, its fully charged local exponent r retains the unknown K; strict size contraction and causal use therefore do not imply K elimination. `CAUSAL-STRICT-SUCCESSOR-IMPLIES-K-ELIMINATION1` and decide-then-emit contraction are **FALSIFIED/RETIRED**. The surviving target is `PREDECISION-CONTRACT1`: a K-independent, fully charged, all-input strict-successor constructor with hereditary access and a model-matched endpoint. The audit passed 110 source cases, 1,100 legal semantic/length checks, 550 encoding round trips, 1,100 decoded interventions, and 64 recurrence checks. P versus NP remains **OPEN**.
