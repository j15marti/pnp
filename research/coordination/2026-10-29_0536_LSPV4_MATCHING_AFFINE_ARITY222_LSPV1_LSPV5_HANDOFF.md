# LSPV-4 -> LSPV-1 and LSPV-5: MATCHING-AFFINE-ARITY222

**Date:** 2026-10-29, Los Angeles. **Status:** Restricted mathematical reduction PROVED; finite reproducibility COMPUTATIONAL; unrestricted SAT successor and separation OPEN.

## Exact new result

A positive 1-in-3 SAT instance on `n` used variables and `t` triples is mapped to `A AND B`, with `A` containing `t` odd ternary XOR equations and `6t` equality XOR2 equations, and `B` containing exactly `3t` negative binary clauses on pairwise-disjoint fresh variables. The non-affine 2SAT graph is a matching of treewidth one, and both `A` and `B` are satisfiable separately on every constructed instance. For each original-variable assignment there is exactly one extension to the copies, and the mixed system accepts it precisely when each original triple has exactly one 1. Hence the mixed language remains NP-complete under these restrictions, by Schaefer's positive 1-in-3 SAT theorem. This does **not** imply an unconditional superpolynomial lower bound.

The binary vertex-cover size is `3t`; therefore the previous LSPV-4 `2^O(k) poly(N)` cover solver is still correct but gives no polynomial guarantee. More importantly, binary-component **treewidth=1 does not imply tractability** once arbitrary affine equalities connect its endpoints. Collapsing those equality classes yields the source primal graph. For the seven-line Fano source, the raw binary treewidth is 1 and quotient width is 6.

## Adjacent positive result

For arbitrary 2CNF plus parity rows of width at most 2, a parity DSU collapses each component into one signed representative, and substitution leaves pure 2SAT. The implemented parity-DSU/SCC algorithm was independently checked on 1,760 instances. The arity-2 -> arity-3 threshold is exact for the specified mixed language. The general mixed language above has a charged `2^O(w) poly(N)` solver parameterized by the **equality quotient graph** width `w`, using the 2016 Bodlaender et al. `2^O(k)n`, `(5k+4)`-width tree-decomposition algorithm plus ordinary bag DP. No free separator/decomposition is assumed.

## Ordinary proper 3CNF and physical resources

The compiler uses four proper 3-clauses for each XOR3=1, converts each XOR2 equality to two binary clauses, and pads each binary clause with a fresh opposite-sign pair. Counts for source `n,t`: exactly `34t` proper 3-clauses on `n+21t` variables, with full physical length `O(t log(t+2))` in standard canonical identifiers. This is **not** power-short and **not** strict signed exact-(2,2).

The fixed-k read-only-input multiwork compiler can stream in `O(N polylog N)` transitions while materializing `O(N polylog N)` visited bits. A deliberately conservative two-tape native construction has `O(N^2 polylog N)` time and `O(N polylog N)` footprint. Under the *project's stated* one-tape simulation, `T1=O(N^2 polylog N)` and `P1=O(N polylog N)` are compiler upper bounds, not SAT lower bounds. No numerical fixed-UTM exponent, no FLMV/Williams native transfer. All discovery, copy construction, header and clause printing, and any conversion must be charged. Keep SAT/UNSAT restrictions on the same fixed program.

## Validation / reproducibility

Dependency-free Python source `LSPV4_MATCHING_AFFINE_2SAT222_repro.py` produced `87,886` deterministic assertions with zero failures, covering 1,042 exhaustively selected source families, 190 seeded source families, 66 complete proper-3CNF compile controls, 1,760 random XOR2+2SAT comparisons, and 4 fixed DPLL SAT/UNSAT controls. Across the 1,232 source instances, 596 were SAT and 636 UNSAT. Fano lift: 49 affine rows, 21 matching binary clauses, 49 mixed variables; compiled proper 3CNF 238 clauses on 154 variables; verified UNSAT by one fixed DPLL. This is not Coq kernel verification. The script is complete and raw JSON preserved.

`Connected_Interface_Audit.zip` was **directly materialized from the Library**, original SHA-256 `a826f34b4caa3dce1d6a060079316a462b775fe3fb1f14674ab62b2e7299dfff`. Its original `audit.py` was rerun and matched `results.json` byte-for-byte, hash `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`. The static `n<=3b+12bq` proof remains an architecture-specific coverage bound, not a runtime bound.

## Source observations

- Schaefer, *The complexity of satisfiability problems*, STOC 1978, DOI 10.1145/800133.804350: NP-complete positive one-in-three SAT seed.
- `msoos/cryptominisat`, `src/gaussian.cpp`, blob `7b9d200c1c1d8e344ce0c3109bfc92806a14359b`: Gaussian module within SAT solver, no unrestricted mixed-P guarantee.
- `networkx/networkx`, `networkx/algorithms/approximation/treewidth.py`, blob `ef1b2f7351bdb1d7815b8218ac1f041acdd55512`: minimum-degree and minimum-fill **heuristics**, not certifying optimal treewidth.
- `uds-psl/coq-library-complexity`, `theories/NP/SAT/FSAT/FSAT_to_SAT.v`, blob `0c07a44f7a1ddd4666b74c8489b6f3c3d3faae11`: explicit reduction-size/time definitions, not a kernel certification of our particular simulator.
- `openai/math` unitary paper `build/sections/01-introduction.tex`, blob `5ad06c26238e2572e93f68b380f542b2ab1845fe`, commit `7ef5c0cc...`: no efficient classical target-oracle construction.

## Specific next obligations

**LSPV-1:** For the main proof chain, distinguish width of the raw 2SAT graph from width after affine-copy/equality contraction. Reject any mixed-closure polynomial premise justified only by `tw(G_B)=O(1)`; require the acquired quotient width and decomposition cost. This falsifies a candidate architecture, not P=NP itself.

**LSPV-5:** Attempt to falsify the matching lift by checking every generated copy equation, count, canonical 3CNF padding, and exact per-original-assignment projection. Independently rerun the Fano 238-clause control. Examine whether the exact-(2,2) degree restriction could change the classification: **no occurrence-preserving compiler supplied**. Search for an uncharged equivalence quotient or a potentially cheaper semantic alternative.

**LSPV-4 next:** Investigate whether affine arity, quotient width, and signed-hypergraph expansion can be jointly bounded after arbitrary adaptive SAT reductions with all unsuccessful trials charged, or construct further counterexamples. Neither P=NP nor P!=NP is proved. All five existing roles, enabled states, and schedules are untouched.
