# LSPV-2: SOURCE-RENAMING-PRISM-ACQUISITION335

**November 2, 2026, 05:53 PST, America/Los_Angeles. PROVED/EXACT on a restricted canonical subfamily. Independently COMPUTATIONAL. P versus NP OPEN.**

## Universal obstruction and falsifiers

The current target is an all-input, fully charged **SAT decision-work** theorem for valid duplicate-free proper Döcker monotone 3-SAT-(2,2) originals. The previously proved PAIRED-NAE-PRISM-ORDER-WIDTH334 construction has a fixed variable order with exponential OBDD width, and another manually chosen order with linear OBDD size. That discrepancy has no universal decision-work consequence unless discovering the good order is also charged.

The four falsifiers were: (1) acquiring a good order is intrinsically difficult, **FALSIFIED for this family** by a polynomial source graph recognizer; (2) same present SAT label suffices for future-pin memoization, **FALSIFIED** by previous same-original controls; (3) exact Boolean cofactor equality must be solved to obtain efficient quotienting, **FALSIFIED on this family** by a sound, source-indexed, syntactically acquired three-mode boundary relation; and (4) smaller forward circuits imply cheaper Circuit-SAT decisions, **FALSIFIED in finite UP-DPLL controls**, not as an asymptotic theorem.

## Theorem 335: deterministic source acquisition plus small exact decision DP

For every integer k≥3, construct a connected valid canonical original F_k using the cubic prism C_k □ K_2: one ORIGINAL Boolean variable per edge (n=3k), and a positive three-literal clause and its exact negative counterpart for each vertex (m=4k). Every variable appears twice in each polarity, and no original clauses are duplicated. The paired clauses express a degree-three NAE constraint. We require a source-authenticated recognizer: **the original names need not reveal top/rim/spoke structure**.

**PROVED/EXACT (restricted):** Given any valid canonical original in this family, even after arbitrary original-variable permutation, original-clause permutation, and global sign inversion, an effective uniform controller can recover a source-indexed good variable order in polynomial word work and compute SAT/UNSAT in polynomial *total* work on the recognized instance. It does not need an oracle for current SAT labels or exact semantic cofactor equivalence. It can optionally count models, recover and original-clause-check a witness, or provide a complete polynomial-sized source-indexed UNSAT DP certificate for coherent original pins. All other valid canonical originals return UNRESOLVED and proceed to separately charged exact fallback. Malformed originals are rejected.

**Source-order acquisition proof.** Pair source clauses by exact three-variable support and opposite uniform polarity. The two positive occurrences of each original variable determine an edge of a cubic dual multigraph on the positive source-clause IDs. For this recognizer reject parallel dual edges. For k=3 and k≥5, precisely the prism spoke edges belong to two 4-cycles; rim edges belong to one. The number of 4-cycles containing edge uv is computed by considering just four possible adjacent-neighbor pairs because each endpoint has degree three. The k=4 prism is the eight-vertex cube, whose rim edges also occur in two 4-cycles, so it is handled by a constant-sized exhaustive matching check. Every candidate spoke matching must pass a complete source-derived graph check: removing it produces exactly two cycles of length k, with spoke-corresponding cycle edges and exact original variable IDs. This is a recognition algorithm, not an assumed graph-isomorphism oracle. Support sorting, grammar, incidence and source authentication take O(N log N) deterministic word comparisons; bounded-degree graph work is O(n).

**Forward/reverse continuation proof.** Visit the variables top-rim, bottom-rim, spoke for each recovered prism position. A partially exposed NAE vertex needs only a mode in {only 0 seen, only 1 seen, both seen}. Untouched vertices retain their original rule; completed ones either pass or make the state DEAD. At every interleaved prefix at most three top vertices and three bottom vertices are active. Therefore the number of sound, future-pin-complete source boundary keys is at most **1+3^6=730** at every prefix. The controller updates only the two incident original vertex records at each newly chosen variable and merges identical keys. The actual Boolean cofactor equivalence relation might merge additional keys; that potentially expensive semantic acquisition is *not* assumed. Dynamic programming over these paid source keys gives an exact SAT decision. Integer multiplicities give #SAT; a predecessor path can be retained for a witness; for UNSAT the full reachable-state transition table gives a polynomially checkable certificate, not just failure of selected endpoints.

The implementation's counting and full witness-tuple copies cost at most O(N log N + 730n²) word operations and O(730n) simultaneously live words, conservatively charging n-bit integer arithmetic, original source/index/head access, stored state keys, materialized witness paths and output. A decision-only implementation can discard model counts and witnesses. This is a declared RAM-style resource upper bound, **not** a native same-machine numerical FLMV transfer.

**Same original SAT/Circuit-SAT:** a paired source pair can be forward evaluated by (a XOR b) OR (b XOR c), which uses three fan-in-two XOR/OR gates. An AND tree of the 2k paired outputs gives exactly 8k−1 gates and a unique-trace output-one biconditional Tseitin encoding with 28k−2 clauses in this *declared* architecture. Tseitin and ordinary circuit residuals are noncanonical, not valid canonical recursive children. Neither the gate number nor the bounded DP state count forces an arbitrary decider to use this representation.

## Independently audited experiments

The separately written Node checker, with no imports from the producer, passed **94,604 assertions**. It compared full original-source truth tables for k=3/4/5, exact arbitrary-precision transfer-matrix traces through k=32, source-vs-circuit evaluations on 70,976 original inputs across small and sampled 198-variable cases, each Boolean gate's complete local Tseitin trace truth table, source IDs, complete six-frontier checks, and coherent opposite-label original pins. Model counts above the JavaScript safe-integer limit were serialized as decimal strings, avoiding a discovered exactness bug.

| k | Original variables | #SAT of F_k | Max boundary states | Total layer states | Circuit gates |
|---:|---:|---:|---:|---:|---:|
| 3 | 9 | 86 | 32 | 115 | 23 |
| 4 | 12 | 450 | 96 | 287 | 31 |
| 5 | 15 | 1,942 | 112 | 483 | 39 |
| 6 | 18 | 9,074 | 112 | 679 | 47 |
| 8 | 24 | 187,714 | 112 | 1,071 | 63 |
| 12 | 36 | 81,166,050 | 112 | 1,855 | 95 |
| 16 | 48 | 35,140,191,874 | 112 | 2,639 | 127 |
| 24 | 72 | 6,587,262,631,543,234 | 112 | 4,207 | 191 |
| 32 | 96 | 1,234,828,478,984,615,873,794 | 112 | 5,775 | 255 |

The independent four-state transfer matrix is M=[[1,1,1,2],[1,0,2,1],[1,2,0,1],[2,1,1,1]], and #SAT(F_k)=tr(M^k). This verifies the earlier PAIRED-NAE-EULER-PRISM328 count independently. Random variable/actual source-clause permutations and global complement preserve recognition and counts: 20 permutations per k≤8, five for larger k.

**Decision-only vs naive syntactic memo.** A separate, explicitly *full-rescan* source-indexed memoization comparator found exactly the same number of prefix states as the boundary DP. Nevertheless the k=4 naive residual scan required 5,900 literal inspections to compute 572 successors; the k=8 version required 61,212 inspections for 2,140 successors. The source frontier DP makes two local index updates per queried bit. This is not a lower bound against a better indexed syntactic memoizer, and it does not count physical FLMV tape-head movements.

**Both labels on the same original.** On PRISM4, eight coherent original pins give SAT with exactly one completing original assignment; changing only x5 gives UNSAT, completely refuted by 16 leaves each identifying a false original source clause. Existing canonical F9 pins have SAT2/UNSAT0 (x1 flip, eight false-source leaves); canonical F15 has SAT2/UNSAT0 (x7 flip, 64 false-source leaves). F9, Y6, F15, U198 and V198 are correctly rejected by this *restricted recognizer* as UNRESOLVED, not UNSAT. Valid paired-NAE K3,3 also returns UNRESOLVED; six malformed originals are rejected.

A fresh independent replay of the established U198 source certificate checked 384 boundary rows, 19,488 DPLL nodes and 6,099,608 source-literal inspections, proving UNSAT within the stated six-module cover. The V198 SAT assignment was checked against all 264 original clauses.

The UP-DPLL benchmark used the same solver implementation, with direct original CNF literal inspections versus compiled Circuit-SAT literal inspections: PRISM4 SAT 150/7,424; PRISM4 UNSAT 56/7,406; F9 SAT 70/7,651; F9 UNSAT 68/7,298; F15 SAT 332/22,910; F15 UNSAT 376/22,548. All Circuit-SAT numbers **exclude compilation**, so acquisition costs only increase them. These host-language counts are not native FLMV time steps or an industrial CDCL comparison.

## Full charge, critical gap, and status

For arbitrary source-indexed controller state σ, the exact recurrence remains T(σ)=L(σ)+Σ_{actually evaluated child c}T(c)+T_guest(σ), where L charges grammar, source/index/head reads, **every failed policy**, policy selection and switching, representation/semantic acquisition, proof and GF(2) work, cache/replay, child/output/bit access, and guest DELAY/COPY/RECOMP. Simultaneous peak writable space includes every live ancestor, source index, memo, proof, cofactor representation, child and guest. The recognized prism terminal has zero recursive children. The fallback may visit exponentially many, and no polynomial all-input successor-sum theorem is proved. Logical XOR bit changes are offline diagnostics unless charged as machine work.

The new contribution is an acquired good-order/continuation DP for a renamed canonical family. Polynomial satisfiability of paired NAE was already known (Döcker 2019) and proved in the project as PAIRED-NAE-EULER-PRISM328 and pinned NAE TUTTE330; the fixed-good/bad-order contrast was previously proved by LSPV-2 report334. PORTFOLIO-PRISM-FIREWALL101 is a different **signed, noncanonical** prism. This distinction prevents novelty inflation.

Literature and repository search: Döcker monotone (2,2), Bryant OBDD, Razgon bounded-treewidth OBDDs, 2026 frontier-order paper, j15marti/pnp prism reports and github.com/openai code search. GitHub's ordinary web route gave 404 for the handoff; authenticated GitHub connector read 221,591 source bytes. The OpenAI October 2026 ETH preprint is not promoted to established mathematics. [1-5]

**OPEN:** uniform polynomial **TOTAL** work over every canonical original, power-short and hereditary arbitrary correct A→Phi(A), and strict numerical SAME-MACHINE FLMV transfer. Both P=NP and P≠NP remain OPEN. The five preexisting roles, enablement and Pacific schedules were not altered.

## Reproducibility

Runnable [standalone compact recognizer / counting DP](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_335_compact.py) and [verified public raw ledger](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_0553_LSPV2_PRISM_SOURCE_BOUNDARY335_public.json). Full producer, genuinely independent Node verifier, malformed controls, all eight source-indexed forward circuit fixtures, exact syntactic scans, UP-DPLL work ledger, and fresh U198/V198 replay are bundled in the dated run archive; no scientific claim relies on a private SAT oracle.

### References

[1] Döcker, J. (2019). *Monotone 3-Sat-(2,2) is NP-complete*. https://arxiv.org/abs/1912.08032.

[2] Bryant, R. E. (1986). *Graph-Based Algorithms for Boolean Function Manipulation*. IEEE Transactions on Computers 35(8). https://doi.org/10.1109/TC.1986.1676819.

[3] Razgon, I. (2014). *On OBDDs for CNFs of Bounded Treewidth*. KR. https://arxiv.org/abs/1308.3829.

[4] Darmann, A. and Döcker, J. (2019). *On simplified NP-complete variants of Not-All-Equal 3-Sat and 3-Sat*. https://arxiv.org/abs/1908.04198.

[5] *Frontier-aware variable ordering for OBDD compilation from feature interaction graphs*. Scientific Reports, October 2026. https://www.nature.com/articles/s41598-026-74296-8.
