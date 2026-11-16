# TMR-2/056: Authenticated connected-cycle CNF and constructed future-count frontier

November 15, 2026, 17:13 PST. Track A, TMR-2 / PNP Information Necessity. Status PROVED/EXACT only for the specified weighted-counting model, independent mathematical review OPEN; executed finite tests COMPUTATIONAL. P versus NP OPEN.

## Candidate, falsifiers, and exact dependency

D2-QUOTIENT-CONSTRUCTION (OPEN in TMR-2/055) is now CLOSED for the authenticated connected even-cycle source family. Candidate: on any simple bipartite graph G=(A,B,E) with a specified left vertex order, the following explicitly constructed key is a sufficient future-count-continuation signature:
\[
P_t=\bigcup_{i\le t}N(a_i),\quad Q_t=\bigcup_{i>t}N(a_i),\quad B_t=P_t\cap Q_t,\quad
\kappa_t(U)=(|U|,U\cap B_t).
\]
Here U is a realized neighborhood union of selected left-prefix vertices. The actual implementation discovers the order on connected cycles from encoded source bytes. The key is a canonical sufficient REFINEMENT of the full future-signature equivalence for that fixed order; minimality is not claimed.

Pre-search falsifiers: (F1) a discarded right-side bit outside B_t could affect a suffix; (F2) both include/exclude transitions might require full U; (F3) disjoint cycles might be accepted as one connected cycle; (F4) graph ordering, key construction or exact counts might hide exponential preprocessing or auxiliary multiplicity. The first two are disproved by the identities below, the third by full-cycle traversal, and the fourth by an explicit same-run ledger and unique pins. A future unrestricted solver may still take any inexpensive alternative.

The end-to-end model is genuine DIMACS CNF bytes (canonical c split a b, p cnf header, seven ternary clauses forcing three fresh pins to 000, and each graph edge as a distinct proper ternary clause) -> parser and authentication -> graph extraction -> polynomial connected-cycle recognition/left order -> computed frontiers -> two paid weighted transitions per materialized state -> exact integer #CNF output. Other authenticated sources use prior exact matching-product or uncompressed union-state routes; generic parsed CNFs retain the exponential brute-force fallback. Invalid inputs are rejected under the declared parser grammar. This is an all-input correctness claim only for the implemented parser's language, and a polynomial bound only for the connected-cycle subclass.

## Theorem A: no exponential future signatures need to be built

For any suffix left subset S, N(S) subset Q_t and U subset P_t. Therefore
\[
U\cap N(S)=(U\cap B_t)\cap N(S)
\quad\Longrightarrow\quad
|U\cup N(S)|=h+|N(S)|-|X\cap N(S)|,
\]
where (h,X)=\kappa_t(U). Equal keys imply equality of the ENTIRE TMR-2/055 future-cardinality signature, not just the final output.

For the next neighbor mask H=N(a_{t+1}), with next frontier B_{t+1}, exact successor keys are
\[
\begin{array}{lll}
\text{exclude:}&(h,X\cap B_{t+1});\\
\text{include:}&(h+|H|-|X\cap H|,(X\cup H)\cap B_{t+1}).
\end{array}
\]
Proof: H subset Q_t, hence U intersect H=X intersect H. Moreover U intersect B_{t+1}=X intersect B_{t+1}, because every previously reached right vertex that is still reached by some later left vertex was already in B_t. Thus neither branch needs the discarded full U. Each old integer weight is deposited on both arcs, with collisions summed, so exact multiplicity survives. At t=a the frontier is empty, and each key (h,empty) contributes the exact integer 2^(b-h) times its weight. Induction from (0,empty,1) proves the output is #F_G. There are at most (b+1)2^f keys per layer and 2a(b+1)2^f paid branch arcs for f=max_t |B_t|. Weights never exceed 2^a; the final count is at most 2^(a+b), so exact bit precision is polynomial for f=O(log N).

This is an upper-bound algorithm for a restricted representation. It is not a necessary-work or SAT-time lower bound.

## Theorem B: uniform cycle order discovery; exponential rank with polynomial count

For any k>=3 and ANY relabeling of the bipartite even cycle C_{2k}, the recognizer requires a=b=k, m=2k, every original left and right vertex of degree two, and an alternating traversal that visits exactly k distinct left vertices before returning to its start. Disconnected unions of cycles are rejected by the all-vertex traversal. The traversal gives the left order; its processed/future neighborhood intersection has size exactly two at t=1,...,k-1 and zero at endpoints. Hence the previous theorem gives no more than 4(k+1) states per stage and O(k^2) genuine weighted arcs. No supplied decomposition or lookahead oracle is used.

The output is the known independent-set count L_(2k), the Lucas number defined by L_0=2, L_1=1, L_(n+2)=L_(n+1)+L_n. The implemented DP DOES NOT look up this formula; it computes the exact count by its own transitions. The equality is checked independently as a finite hostile/validation control and follows symbolically from the classical cycle independent-set recurrence [2]. The strict 3-CNF pins have exactly ONE satisfying extension for each independent set, so no count dilution occurs.

Despite polynomial counting, the fixed-formula assignment matrix across original A:B has exponential rank over EVERY field: choose floor(k/2) pairwise nonadjacent left vertices with disjoint neighborhoods. Their 2^floor(k/2) subsets have distinct neighborhood unions, and by the earlier TMR-2/053 subset-zeta theorem,
\[
\operatorname{rank}_K(D_{C_{2k}})=|\{N(S):S\subseteq A\}|\ge 2^{\lfloor k/2\rfloor}.
\]
This is a fixed-formula assignment tensor, NOT the SAT decision function on encoded formulas. Connected cycles are cheap because they have treewidth two and an obvious satisfying assignment. Static rank therefore cannot imply compulsory exact counting or general circuit work.

## Exact source implementation and same-run resource ledger

Executable revision TMR2_FRONTIER_CYCLE_E2E056_v1: experiments/tmr/tmr2_cycle_frontier_e2e056.js. The code reuses the TMR-2/055 DIMACS parser/pin checker and exhaustive controls, while adding cycle recognition, discovered vertex ordering, frontier-mask precomputation and a weighted frontier DP. For the precise declared source grammar this is a full executable chain, not a schematic evaluator.

Let N be COMPLETE encoded source bits, R=(b+1)2^f, and count all source reads, graph/degree/ordering attempts, bitmask frontiers, exact key comparisons, two state tables, integer-weight operations, error/fallback paths, indexing, input seeks and output. A conservative uniform locally-headed deterministic multitape implementation of the SAME pipeline (using ordinary ordered dictionaries instead of ideal unit-cost hash maps) satisfies
\[
T=O(N^3+aR(N+a+b)^3),\qquad
S_{\rm peak}=O(N^2+R(N+a+b)^2)
\]
bits. Each key stores a cardinality, frontier mask, and at most a+1-bit weight; the full source graph/order/frontiers fit in O(N^2) bits. The two tables together store at most 2R entries, all counted. Exponential fallback for non-family cases is excluded from the special-family polynomial bound, not excluded from correctness. For cycles f=2,a=b=k<=N: T=O(N^6), S=O(N^4). These are deliberately loose implementability upper bounds; the V8 Map runtime is not a native tape microtrace. All physical work, number of queries, integer precision and peak live buffers belong to ONE realization, not disjoint optimizations.

TMR-4 receives named invariant D2-CERTIFIED-COUNT-FRONTIER: the real materialized weighted (h,X) states plus source parser, authenticated graph, discovered order, B_t masks, exact updates and output, not the number of latent semantic classes. Complete transition interface: source read/authentication; edge/degree/order discovery; suffix frontier-mask generation; each zero/one weighted successor with bit costs; state collision and additions; switches, caches, sharing/recomputation, fallback, and output. An alternate Lucas recurrence, Gaussian elimination, Horn/Krom unit simplification, bounded-treewidth DP, equality/autarky and compact circuit are LEGAL, so no compulsory tariff is inferred. No nonrelativizing transfer theorem to arbitrary circuit computation has been built.

## Executed finite evidence, source reconciliation, and limitations

Hosted V8 executed the exact file body before branch creation, deterministic LCG seed 20261115, with results written without changes to results/raw/tmr/2026-11-15_1713_TMR2_CYCLE_FRONTIER056_V8_RAW.json. Twenty relabeled connected cycles k=3..22; k<=5 full original CNF assignment enumeration; k<=12 uncompressed union DP; k<=7 full exponentially enumerated future-signature quotient; five authentic hostile graphs including matching DISJ, complete bipartite, star, noncycle and isolated; two malformed sources. There were 195 counted assertions and ZERO failures. At k=22 the graph has 44 original variables, 44 edges and three uniquely pinned auxiliaries; exact #CNF=1,568,397,607, rank lower bound 2048, at most 79 observed nonfinal frontier keys and 1648 actual two-branch transitions. Note that finite tested cases are COMPUTATIONAL and not evidence of unrestricted hardness.

Local repository checkout and preflight were unavailable because github.com DNS cannot be resolved in the container. No compiled LaTeX, instruction-level deterministic TM trace, Lean kernel build or independent mathematical peer review is claimed. Current issue #3 entries, governing directives, five handoffs, full owned manuscript, TMR-2/055 original report/executable/raw, TMR-2/053 rank proof and TMR-4/056 circuit-layout paper and original report were consulted. Unmerged TMR-3 PR #164/#169 were not conflated with main.

Primary references: [1] Cheng and Rosenbaum, Simple Counting and Sampling Algorithms for Graphs with Bounded Pathwidth, arXiv:2008.08479 (2020), source of standard exact pathwidth-DP context, NOT a novel discovery attributed here. [2] Alexander and Hearding, A Graph-Theoretic Encoding of Lucas Sequences, Fibonacci Quarterly 53(3), 237-240, arXiv:1501.00061, which attributes the known cycle independent-set count to Prodinger and Tichy. [3] Bryant, Graph-Based Algorithms for Boolean Function Manipulation, IEEE Transactions on Computers (1986), DOI 10.1109/TC.1986.1676819.

## Four-gate table

| Gate | Status | Reason |
| --- | --- | --- |
| DISJ sanity | PASS scoped; FAIL naive unrestricted rank transfer | Matching DISJ retains its O(N^3) exact product route. The connected example has large rank but a cheap constructed count. |
| Relativization | PASS for local identities, OPEN for separation | Pure set identities cannot resolve P vs NP; any unrestricted theorem needs a precise nonrelativizing step plus algebrization/Natural Proofs audit. |
| Simultaneous DTISP | PASS for one source-counting upper-bound realization; OPEN for SAT lower-bound transfer | All discovery, arithmetic and storage have simultaneous T and S bounds, but no FLMV contradiction is claimed. |
| Configuration count | PASS upper-bound-only | A deterministic total read-only-input machine has T<=2^O(s+log N), not a lower bound; no quantum/randomized import. |

Additional controls: Horn, Krom/2SAT, affine/Gaussian, treewidth two, equality, certified autarky, products, padding, unique-zero pins, unique-selector projection, unique-solution rank-one full tensor, alternative order, count normalization, shared circuits, local invertible basis, singular GF(2) Walsh-Hadamard, charged Valiant-Vazirani isolation, caching and recomputation. /341 is FAIL as unrestricted UNSAT authority, /386 is RESTRICTED. P versus NP OPEN.

## ONE next load-bearing lemma

D2-CROSS-MODEL-COUNT-INTERFACE: construct a paid count-preserving register/branching representation from actual encoded graph sources with a DISCOVERED O(log N) frontier in a connected family beyond bounded-treewidth cycles, or exhibit the smallest correct-model failure. Bound all description, access, retained weight and path multiplicity costs. No unrestricted circuit or SAT work claim.
