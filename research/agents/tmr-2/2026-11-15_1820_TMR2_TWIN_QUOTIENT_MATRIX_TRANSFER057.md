# TMR-2/057 | Authenticated twin-quotient transfer matrix beyond bounded treewidth

2026-11-15 18:20 PST. TMR-2 / PNP Information Necessity. Track A. **PROVED/EXACT only for the specified source family and weighted exact-counting realization; independent mathematical review OPEN.** Executed finite tests **COMPUTATIONAL**. P versus NP remains **OPEN**.

## One end-to-end candidate and four falsifiers

**Dependency D2-CROSS-MODEL-COUNT-INTERFACE.** Candidate: a deterministic uniform parser can recover *without an advice oracle* the false-twin quotient of an authentic strict-proper 3-CNF independent-set encoding, recognize when this quotient is a connected even cycle, construct a constant-dimensional weighted register/matrix computation, and return the **exact number of complete satisfying assignments**. The family has unbounded ordinary graph treewidth and exponentially growing fixed-formula A:B assignment-tensor rank. It does not have computational hardness.

Before corpus and primary-literature review the falsifiers were: (F1) false-twin grouping loses multiplicities or fails on arbitrarily relabeled sources; (F2) a cyclic trace fails to account for the last-to-first right class; (F3) a non-cycle or incomplete quotient is spuriously accepted; (F4) input authentication, quotient discovery or exact arithmetic is exponential even when the recognized quotient is a cycle. Theorem and executed controls below address these four for the declared family, not for arbitrary source circuits.

**Full chain:** finite ASCII/DIMACS source bytes and the actual declared variable count -> parse, verify exact seven forced-zero pin clauses and every edge clause -> construct the original simple bipartite graph -> compute both-side equal-neighborhood classes and their authentic complete quotient -> discover and validate a spanning alternating quotient cycle -> compute original class sizes -> construct 2x2 exact-integer transition matrices -> multiply them and take the trace -> output the exact #CNF integer. Other authenticated bipartite graphs use a correct, potentially exponential neighborhood-union evaluator. Generic width-at-most-three parsed CNFs use exhaustive exact counting; malformed sources are rejected. The polynomial guarantee applies only to the recognized twin-cycle subclass.

## Theorem: exact false-twin cyclic transfer

Let G=(A disjoint-union B,E) be a simple bipartite graph with **false-twin classes** A_0,...,A_(k-1) and B_0,...,B_(k-1), each of positive size alpha_i,beta_i. Suppose their quotient has exactly the edges (A_i,B_i) and (A_(i+1 mod k),B_i), k>=3. Edges between any adjacent original classes are complete. The source has a+b+3 variables, 7+|E| distinct proper ternary clauses, and the standard seven-pin gadget uniquely forces three auxiliary variables to zero. In particular every independent set of G extends to exactly one satisfying assignment.

Define x_i=1 when the chosen independent set contains at least one vertex in A_i, and x_i=0 otherwise. The number of original choices with this activity bit is
w_i(0)=1, w_i(1)=2^(alpha_i)-1.
For B_i, all beta_i variables may be selected if x_i=x_(i+1)=0, and otherwise all must be zero. Thus the right multiplier is
r_i(x,y) = 2^(beta_i) if x=y=0, and 1 otherwise.

Consequently the **exact** full-assignment count is

    #F_G = sum_(x in {0,1}^k) product_(i=0)^(k-1)
                 w_i(x_i) r_i(x_i,x_((i+1) mod k)),

and with rows indexed by x_i and columns by x_(i+1),

    M_i = [[2^(beta_i), 1],
           [2^(alpha_i)-1, 2^(alpha_i)-1]],

    #F_G = tr(M_0 M_1 ... M_(k-1)).

**Proof.** The exact forced-zero pin gadget is pointwise bijective to independent sets of G. In each left class, the empty set has weight one and the nonempty subsets have weight 2^alpha_i-1. Conditioned on the left activity vector, each right class independently has exactly 2^beta_i or one choices depending on whether either neighboring left class is nonempty. Multiplying these independent factors and summing over activity bits counts each original independent set exactly once. Expanding the trace of the cyclic matrix product imposes x_k=x_0 and therefore counts the final B_(k-1) closing constraint. No auxiliary-variable dilution or half-threshold assumption is used. QED.

## Source discovery and high-treewidth/rank separation

The actual procedure groups the original left vertices by exact equality of their right-neighbor bit rows, and the right vertices by equality of their left-neighbor bit columns. These equality classes are discovered by direct comparison of explicit parsed edges, with no supplied modular decomposition. By construction, adjacency between a pair of classes is either complete or empty. The recognizer checks equal numbers of left/right classes k>=3, exactly two neighbors per quotient class, and a **single spanning alternating cycle** visiting every class. It rejects disconnected unions of cycles. It extracts an ordered pair of class sequences so B_i is adjacent exactly to A_i and A_(i+1), and evaluates the displayed matrices.

For equal blow-up sizes alpha_i=beta_i=g, the original graph has 2kg vertices and 2kg^2 edges. Each quotient edge induces a K_(g,g) subgraph, hence treewidth at least g: K_(g,g) admits a K_(g+1) minor by contracting g-1 disjoint cross edges and retaining the two uncontracted endpoints, so minor monotonicity gives the bound. Taking g=k gives unbounded treewidth Omega(k) with n=2k^2 original variables.

For the **fixed formula's original left/right assignment-evaluation matrix**, let D_G(S,T)=1[T intersect N(S)=empty]. The Boolean-subset zeta matrix on right subsets is invertible over every field, so rank_K(D_G) is the number of distinct left-neighborhood unions (TMR-2/053). Choosing floor(k/2) nonconsecutive quotient-left classes yields disjoint nonempty quotient-right neighborhoods. Their subsets therefore yield at least 2^floor(k/2) distinct unions and

    rank_K(D_G) >= 2^floor(k/2)  (every field K).

Identical-neighborhood twins do not change the distinct-union lower bound. The matrix rank concerns the fixed formula's assignment predicate, **not** SAT applied to formula encodings. In this construction even exact counting is polynomial, and the zero assignment is a direct satisfiability witness. The high treewidth is neutralized by uniformly constructed twin compression. This is a new end-to-end scoped falsifier of transferring uncompressed graph width/rank to obligatory computation, **not a new lower bound**.

## Named execution-sensitive invariant supplied to TMR-4

**D2-TWIN-TRANSFER-TRACE:** after t charged matrix factors, the actually stored 2x2 integer P_t satisfies P_0=I and P_(t+1)=P_t M_t, with entries counting the weights of all t-step activity paths between the indicated endpoints. The final invariant is output=tr(P_k). This is a *constructed arithmetic-register invariant*, not a monotone work lower bound or an assertion that every SAT solver must enter this state domain.

Complete transition interface: source byte reads and validation; seven-pin check; duplicate and crossing-edge checks; original adjacency storage and comparisons; discovery of both twin partitions; quotient complete-edge check; degree/connectivity/cyclic ordering; construction of alpha_i,beta_i and exact shifts 2^alpha_i,2^beta_i; four live register entries; for each stage eight exact integer multiplications and four additions, with retained shared matrices and buffers; tracing, writing/validating output; optional failed recognizers, alternative algorithms and fallback. Count shared objects once. No free query, preloaded quotient, unit-cost large-integer arithmetic or arbitrary circuit-to-register compiler is assumed. TMR-4 would need to preserve this register semantics and fully charge any source-class transfer. General shared-circuit, arbitrary-SAT and necessity transfers remain OPEN.

## Same-realization resource ledger

Write N for complete source bits, n=a+b original variables, k the number of quotient-left classes. On the accepted family n,k <= N, and the source encodes every original edge. Parse and validate every clause, construct the a x b Boolean adjacency table, compare up to O(n^2) neighborhoods each of length O(n), validate all group-pair edges, perform graph traversal and compute weights. This is O(N^4) or less elementary bit/table work with a straightforward implementation. The matrix computation uses exactly 8k integer multiplications and 4k additions of nonnegative integers of at most n+1 bits; schoolbook bit multiplication takes O(n^2) bit operations. The output has at most n+1 bits; register state uses four such integers plus the current class sizes, order and buffers.

A fixed deterministic locally headed multitape implementation can store the full source, adjacency table, twin-index vectors, quotient/order, two 2x2 matrices and output in at most **O(N^3) writable bits**, and can implement all elementary source accesses and arithmetic with **O(N^8) time** as a deliberately loose upper bound, including sequential tape seeks. Both are bounds for the **same canonical parse/discover/evaluate/output execution**. The published hosted V8 implementation is an executable RAM-level reproduction; neither a native Turing-machine microtrace nor a LaTeX build has been executed. Nonfamily fallback remains total/correct but can take exponential time and space. The complete count is never presumed to be short: its binary length n+1 is explicitly charged.

For k=g=16 the actual encoded source contains 512 original variables, 8192 edge clauses and 1,022,056 source bits; the exact count has 78 decimal digits, and the evaluated 2x2 product uses 128 integer multiplications. In contrast, the original graph treewidth is at least 16, and its original A:B assignment rank is at least 256. This is a computation upper bound only.

## Four mandatory gates and hostile controls

| Gate | Status | Explanation |
|---|---|---|
| DISJ | **PASS restricted; FAIL unrestricted rank-to-work inference** | Matching DISJ has exponential rank, cheap SAT circuit and exact count 3^k; recognizer rejects it as a twin cycle and uses correct fallback. |
| Relativization | **PASS local; OPEN unrestricted separation** | The elementary counting identity and parser do not claim P != NP; no nonrelativizing step exists yet. Algebrization and Natural Proofs remain open for any future unrestricted transfer. |
| Simultaneous DTISP | **PASS scoped upper bounds; OPEN general lower-bound transfer** | Same parser, graph, quotient, matrices and output have both T=O(N^8), S_peak=O(N^3). No hierarchy forbidden-region inference is made. |
| Deterministic configuration counting | **PASS upper-bound guard** | Total deterministic read-only-input machines have T <= 2^O(S+log N); this is an upper bound and says nothing automatic about randomized/quantum running times. |

Mandatory hostile mechanisms remain legal: zero witness, Horn and 2-SAT simplification after pins, bounded-treewidth DP on the **quotient**, Gaussian/XOR for affine inputs, equality, autarkies, product splitting, edge/variable padding, functional auxiliaries, unique-selector projection, exact scalar-count normalization, single-unique-solution rank one, invertible local-basis rank preservation, Walsh-Hadamard noninvertibility over GF(2), compact circuits and shared computation. The new large-treewidth instances remain tractable, not hardness evidence. No isolation randomness, majority ties, oracle advice, or quantum error model enters this proof. Historic /341 full UNSAT authority remains FAIL and /386 RESTRICTED.

## Executed evidence, reconciliation and review

The published code **experiments/tmr/tmr2_twin_cycle_e2e057.js**, exact revision **TMR2_TWIN_QUOTIENT_E2E057_v2**, deterministic seed **20261115**, was evaluated in a hosted V8 isolate and then the **exact published GitHub readback body** was re-executed using a JavaScript function constructor. The immutable output is **results/raw/tmr/2026-11-15_1820_TMR2_TWIN_QUOTIENT057_V8_RAW.json**. Observed 120 assertions, zero failures, 27 recognized instances, 8 full-CNF brute controls, 17 original-neighborhood-union comparisons, ten hostile/malformed controls. Discovered quotient cycle source sizes and exact counts were tested against an independent 2^k quotient-activity enumeration, including k=16 with g=16. These experiments are finite **COMPUTATIONAL**, not asymptotic verification. Independent mathematical peer review remains OPEN. A separate local Node v22 v1 prototype checked 147 assertions, zero failures, but is not substituted for the exact published v2 evidence. No repository checkout/preflight, physical TM instruction replay or LaTeX compilation was performed.

This is a progression from TMR-2/055 future-cardinality signatures and TMR-2/056 paid connected-cycle frontiers: **a genuinely high-treewidth original graph is source-compressed by an algorithm that discovers the quotient**, followed by a smaller weighted transfer. It is consistent with established graph substitution/twin factorization and graph-decomposition algorithms, not claimed as a novel general graph-algorithm discovery.

Original research dependencies: TMR-2/053 neighborhood-zeta rank report, TMR-2/056 end-to-end connected-cycle report and code, TMR-4/057 full source-authenticated read-once formula compiler, TMR-5/054 address-mask audit. Prior literature: graph twin factorization, *The inducibility of blow-up graphs*, Journal of Combinatorial Theory Series B (2014), DOI https://doi.org/10.1016/j.jctb.2014.06.005; Borie, Parker and Tovey, *Solving problems on recursively constructed graphs*, ACM Computing Surveys 41 (2009), DOI https://doi.org/10.1145/1456650.1456654. The quotient/count recurrence is proved here rather than imported as a new literature theorem.

## ONE next dependency

**D2-GENERAL-SHARED-DAG-TRANSFER:** Given an *authentic encoded shared Boolean circuit* or a #CNF of genuinely unbounded twin-quotient complexity, either uniformly build a count-preserving weighted-register interface with a fully charged width/construction bound, or exhibit the smallest end-to-end source where any proposed bounded interface necessarily loses distinct future count semantics. This is OPEN. No unrestricted circuit or SAT decision lower bound follows.

P versus NP remains OPEN.
