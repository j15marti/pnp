# LSPV-2 GENERAL-PINNED-NAE-TUTTE330
**2026-11-02 01:41 PST | PROVED/EXACT restricted, independently COMPUTATIONAL | P versus NP OPEN**

## Exact obstruction and falsifiable approaches
The canonical target is **all** valid duplicate-free proper Döcker monotone 3-SAT-(2,2) originals. Residual CNF, auxiliary graphs, forward circuits and Tseitin formulas are not canonical hereditary children. A polynomial forward evaluator of (F(x)) does not decide (exists x,F(x)).

This run tested (F1) whether the paired-NAE pinned terminal from 329 extends beyond bipartite dual graphs, (F2) whether a complete polynomially checkable nonbipartite UNSAT certificate can be transported to the original, (F3) whether matching entails a total-work advantage over source UP-DPLL, and (F4) whether current SAT-label equivalence is sufficient for forward/reverse Shannon memoization. **F1/F2 proved, F3/F4 falsified as general inferences.**

## General matching and Tutte theorem
Suppose each positive source clause has exactly its complementary negative clause. The positive clause IDs are cubic-dual vertices, original variables are dual edges, and pins prescribe selected/unselected edges. At dual vertex (v), let (t_v) be the number of pinned-true incident edges and (r_v) the remaining free edges. Both original source clauses hold exactly when
[
ell_v=max(0,1-t_v) le sum_{e
i v, e mathrm{free}} y_e le u_v=min(r_v,2-t_v).
]
Local (ell_v>u_v) is a source-clause contradiction.

**Theorem.** For every valid canonical complemented-pair original, on **any** loopless cubic dual multigraph, including nonbipartite and parallel-edge cases, and every coherent pin configuration, one can construct an exact simple auxiliary graph (H) with at most (6n+1) vertices and (O(n^2)) edges such that (F|p) is SAT iff (H) admits a perfect matching. The construction is effective with paid original-source authentication, incidence reads and all graph materialization.

**Explicit gadget.** Each free dual edge receives two endpoint ports joined by a cross edge. At (v), create (r_v-ell_v) dummy vertices adjacent to all local ports, and (u_v-ell_v) slack vertices adjacent to the local dummies. Join all slack vertices globally into a clique. Add one global parity vertex, adjacent to every slack vertex, iff (sum_v(u_v-ell_v)-sum_vell_v) is odd. A perfect matching uses a cross edge exactly when its original variable is selected. The number of selected edges at (v) is between (ell_v) and (u_v) because unused ports consume local dummies and leftover dummies consume local slack. Conversely, from any feasible degree-constrained selection construct local matches and pair the remaining slack vertices, including the parity vertex when required. Their remaining count has even parity because (sum_vdeg_M(v)=2|M|).

A maximum-cardinality general matching is polynomially computable. If (H) is not perfectly matchable, compute (D={z:
u(H-z)=
u(H)}) by at most (|V(H)|+1) paid matching calls and (A=N(D)setminus D). Gallai-Edmonds gives (o(H-A)>|A|). This **Tutte odd-component barrier** is an independently checkable complete UNSAT certificate: reconstruct (H) from authenticated source and pins; check its components and inequality. It is not a bipartite min-cut. The original-source SAT witness is verified clause by clause when materialized, but injective original-variable-key storage is not required for decision.

**Prior art:** Cornuéjols's general-factor theorem and LSPV-1 INTERVAL-FACTOR134 already imply polynomial decidability of a broader occurrence-two interval grammar. This run claims an explicit independent perfect-matching gadget and source-indexed certificate integration, not a novel general-factor complexity theorem.

## Both-label, same-original nonbipartite control
Canonical Z6 has original positive source clauses ((1,2,3),(1,4,5),(2,4,6),(3,5,6)), their four complementary negatives, and dual (K_4), which is nonbipartite. On this **same original**, pins ((x_4,x_5,x_6)=(0,0,0)) are UNSAT with a complete certified auxiliary barrier: (|V(H)|=10,
u(H)=4, |A|=4, o(H-A)=6). Flipping only (x_4) yields SAT with three satisfying completions, including ((1,0,1,1,0,0)). Direct original-source unit propagation also refutes the UNSAT case. Matching is an exact alternative, not a necessary computational bottleneck.

| Valid canonical original | Coherent pin cubes tested | SAT | Local UNSAT | Tutte UNSAT |
|---|---:|---:|---:|---:|
| Z6 nonbipartite, **exhaustive** | 729 | 475 | 186 | 68 |
| PRISM3 nonbipartite, deterministic sample | 1,200 | 664 | 454 | 82 |
| PRISM4 bipartite, deterministic sample | 900 | 452 | 385 | 63 |
| K33 bipartite, deterministic sample | 900 | 519 | 352 | 29 |

A **separately written no-producer-import verifier** checked all 3,729 labels against exhaustive original-source completions; checked 243 fully materialized Tutte odd-component barriers, 61 recorded source SAT witnesses, two deliberately corrupted barrier rejections, 34,752 source/circuit input rows, 2,035,776 gate events and 209 single-gate corrupted forward traces. The producer rejected ten malformed originals. Valid F9/Y6/F15/U198/V198 fail the paired recognizer and return **UNRESOLVED**, not UNSAT. A fresh replay of the inherited 302/328 source refutation covered 384 U198 boundary probes and 19,488 local DPLL nodes; the V198 witness was checked against 264 source clauses. No (2^{198}) exhaustive evaluation is claimed.

## Exact forward/reverse comparison and adverse work
The source-authenticated general fan-in-two AND/OR/NAND clause compiler has exactly (3m-1=4n-1) gates in its declared unshared architecture; the paired XOR/OR/AND terminal uses (8n/3-1). Tseitin biconditionals have a unique gate trace per original input. Fully exhaustive circuit comparisons covered Y6, F9, F15, Z6, PRISM3 and K33. The U198/V198 circuits were sampled. Neither architecture is an unrestricted circuit minimum.

Paid offline Shannon/cofactor truth-signature acquisition uses ((n+1)2^n) original evaluations per variable order. Z6 forward continuation classes are ((1,2,4,7,9,4,2)); K33 gives ((1,2,4,7,13,23,20,11,4,2)), PRISM3 ((1,2,4,8,16,25,21,10,4,2)). Z6 prefixes (x_1=0) and (x_1=1) are both currently SAT but disagree on the common future continuation ((0,0,0,0,1)). Current decision equivalence does not imply continuation equivalence.

Fresh common-policy source-CNF versus compiled Circuit-SAT UP-DPLL literal inspections were Z6 UNSAT **61 vs 1,947** and SAT **55 vs 2,037**; K33 UNSAT **48 vs 2,969**, SAT **139 vs 4,857**; F9 SAT **74 vs 7,922**, UNSAT **56 vs 7,629**; F15 SAT **313 vs 23,312**. Circuit acquisition and gate/Tseitin materialization add positive work and were separately counted. No universal circuit-decision advantage or lower bound follows.

## Fully charged resources and gap
At each adaptive residual state (R), account for grammar, source/index/head reads, representation discovery, **all** failed recognizers, strategy selection and switching, circuit/Tseitin compilation, semantic quotient acquisition, proof/GE checking, caches and replay, source certificate validation, child/output-bit access, all evaluated successor recurrences and guest DELAY/COPY/RECOMP. Peak writable space is the maximum **simultaneous** source index, gate, cache, ancestor, matching graph, blossom, proof, child and guest state. The restricted matching graph has (O(n^2)) explicit edges and (O(n^2log n)) logical bits; the deliberately simple Gallai-Edmonds witness extractor calls matching (O(n)) additional times, conservatively (O(n^4)) word operations with cubic blossom. This is **not** a native same-machine FLMV transition or exponent result.

**OPEN:** all-input uniform polynomial **total** SAT work; hereditary power-short universal arbitrary-decider (AmapstoPhi(A)); strict numerical same-machine FLMV transfer. **P=NP and P≠NP remain OPEN.** No existing task identity, schedule, enable state or ownership is changed.

### References and reproducibility
[1] Cornuéjols, *General factors of graphs*, JCTB 1988: https://dblp1.uni-trier.de/rec/journals/jct/Cornuejols88.html. [2] General-factor algorithms: https://doi.org/10.1007/s00453-025-01350-8 and https://arxiv.org/abs/1304.6740. [3] D{"o}cker canonical language: https://arxiv.org/abs/1912.08032. [4] Prior project: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-25_0058_LSPV-1_INTERVAL_FACTOR134.tex; prior LSPV-2 328 and 329. [5] OpenAI perfect matching formalization: https://github.com/openai/math/tree/main/lean/OAI/Combinatorics/PerfectMatching.

[Compact standalone matching and source control](../../experiments/arc/lspv2_330_compact.py) | [GitHub raw counts](../../results/raw/arc/2026-11-02_0141_LSPV2_GENERAL_NAE_TUTTE330_summary.json). Full 52-file producer, no-producer-import verifier, all pin records, source-labeled circuits, formal 5-page LaTeX/PDF, bibliography, U198/V198 replay, and SHA-256 integrity manifest are supplied in the run's user-facing reproducibility archive. Repository root `main.tex` was left unchanged: its authenticated contents response again returned zero text bytes despite a nonempty blob SHA. No unsafe update was attempted.
