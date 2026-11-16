# TMR-4/058 | 2026-11-15 18:41 PST | Uniform wavefront-local shared-DAG compiler

**Status:** PROVED/EXACT RESTRICTED mathematical transfer, independent mathematical review OPEN. Finite V8 checks COMPUTATIONAL. P versus NP OPEN. **Named dependency D4-DAG-LAYOUT-RECONSTRUCTION** is closed ONLY for a strictly specified adjacent-level shared-gate DAG class. This is not an all-circuit layout algorithm or lower bound on arbitrary algorithms.

## Candidate, original source, falsifiers

Candidate: for EVERY valid canonical source in the model below, with no supplied schedule/layers, construct and authenticate a topological once-only gate schedule whose maximum number of distinct retained values is at most three times the calculated layer width; compile this actual original source through the existing /056 register-stage bridge to a complete OBDD; prove both-label and exact-count semantics and transfer prefix rank back only to this schedule.

**Four pre-search falsifiers:** (1) a long gate edge keeps older wire values alive; (2) one input used in different layers invalidates single-visit introduction; (3) source fan-out is erroneously duplicated or prematurely discarded; (4) cheap equivalent DISJ, affine, Horn, AND and compact circuits falsify any unrestricted hardness inference. The first two are rejected as OUT-OF-CLASS, not as UNSAT. The third is addressed by identity-preserving all-step simulation. The fourth remains a legitimate alternative.

A complete source word is canonical ASCII JSON with exactly n,gates,out keys. There are n>=1 original input identities x0,...,x(n-1) and g>=1 unique gate identities g0,...,g(g-1). Gate records have exactly id,a,b,op, with op in the 16 ordered binary truth-table codes, and a,b referencing actual input or gate IDs. Gate records can arrive in arbitrary order. The output is one gate. Authenticate complete bytes by canonical roundtrip, syntactic structure, IDs, all references, cycles, original input coverage, a designated output and that every gate is an ancestor of output. Duplicate JSON keys cannot be canonical. The separate original input x has n real bits. Invalid syntax is rejected; syntactically valid but nonconforming DAGs are reported OUT-OF-CLASS.

Compute the gate-only depth
\[
d(g)=1+\max(\{d(h):h\text{ is a gate predecessor of }g\}\cup\{0\}).
\]
Accept the wavefront-local class iff every actual gate-to-gate edge h to g satisfies d(g)=d(h)+1, and all occurrences of a fixed original input x_j feed gates of one common depth d_j. These levels are DISCOVERED from the authenticated original graph, not supplied layout advice. Let G_d be gates at depth d; let X_d be original inputs first needed at depth d, and k=max_d max(|G_d|,|X_d|). Gate fan-out and reconvergence are genuine and unrestricted inside adjacent depths, including repeated operands and multiple distinct gate consumers.

## Constructive all-step theorem and the actual input-to-output pipeline

Emit for each increasing level d every ORIGINAL x_j in X_d (numeric ID order), followed by every ORIGINAL g_i in G_d (numeric ID order). This is a topological original-source schedule. Within one layer, any retained old value is a prior-level gate result, a current-level newly introduced original input, or a current-level gate result. All other values are dead by the authenticated adjacency conditions. Each category contains at most k different physical wire IDs. Therefore for the actual last-consumer live set L_t,

\[
w=\max_t |L_t|\le3k.
\]

No original gate identity is expanded for multiple fan-out consumers, and every original input bit is introduced exactly once. At each introduced original input, create one register-stage boundary, with authentic gate records in the intervening segment. A predecessor of a gate is either a local earlier value or a live register from the preceding boundary, since the current use would otherwise contradict genuine last use. Inducting on EACH original source schedule step proves all source intermediate values, both output labels, and terminal correspondence. Discover the original input-read permutation rho, do not rename its variables, and charge physical reads and seeks.

Enumerate all reachable stage-register states; retain TWO separately labeled input arcs even if they converge; merge states only when both layer and live register tuple are equal. There is a bijection between complete labeled OBDD paths and the 2^n original assignments. Thus the complete n-stage OBDD has V<=n*2^w<=n*2^(3k), and its exact accepting-path integer count equals #C. For every field K and every prefix i of the ACTUAL rho,

\[
\operatorname{rank}_K M_{\rho_{\le i},\rho_{>i}}(f_C)
\le2^{|L_{\mathrm{boundary},i}|}\le2^{3k}.
\]

Conversely a rank-R prefix forces at least ceil(log2 R) values live in this particular source schedule. This is NOT a lower bound on the width of other layouts, circuit size, arbitrary SAT machines or decision work. Original-gate evaluation with direct caching and compact algebra remains legal.

## SAME_REALIZATION ledger and declared consequence

Let L count full source bits, M=n+g, w<=3k. The shared original gate/stage records, actual selector indices, live slots and references require

\[
B=O\bigl(L+(g+nw+n)\lceil\log_2(M+w+2)\rceil\bigr).
\]

The explicitly materialized OBDD and its two arcs per node, stage queues, actual retained wire arrays, addresses and (n+1)-bit exact accepting-path counters fit within

\[
D_*=1+L+B+
O\bigl(n2^{3k}(3k+n+\log_2(n2^{3k}+2))\bigr)
\]

bits. One fixed deterministic locally headed multitape execution, on the full source plus separate original x, can authenticate, traverse/sort levels, reject invalid and out-of-class inputs, discover last uses, compile all authentic shared gates once, enumerate reachable OBDD states and both arcs, follow the actual original x, count exact accepting labeled paths with integer arithmetic, and output the bit and count with

\[
T_{\mathrm{total}}=O(D_*^5+n^2),\qquad
S_{\mathrm{peak}}=O(D_*).
\]

The conservative polynomial covers parsing, all attempted graph checks, source and graph rereads, indexing, cache allocation, sorting, source head moves in permuted rho (at most O(n^2)), full stage gate evaluation, transient wire storage, sharing, output, repeated table scans, every state transition and exact arithmetic. This is one and the SAME machine realization. For k=O(log L) the produced compiler has polynomial time AND peak space in L. It does not achieve a forbidden DTISP region. No CNF conversion is used: n original inputs and g shared source gate records are retained, and any later functional Tseitin composition with TMR-1 MUST separately charge its gate/variable/wire growth and exact counting promise.

## Actual code and finite evidence

Executed authored V8 Function, revision tmr4-wavefront-dag058.v1, xorshift32 seed 20261115, checked 137 full canonical source circuits including 125 with genuine shared INTERNAL gates and DISJ_3, 4,440 complete assignment comparisons, 35,534 replayed original gate/stage operations, 1,526 exact GF(2) and GF(101) rank checks, 2,324 actual materialized OBDD nodes, 4,648 labeled arcs, 82,167 assertions, zero failures. Seven adversarial sources were correctly rejected (long gate edge, cross-level input, dead gate, cycle, duplicate gate identity, duplicate/noncanonical JSON key, bad opcode). DISJ_3 grouped input partition has exact rank 8 over both fields and a compact circuit. Max observed actual w=6, k=6, nodes per instance 63. Every source encoding is included IN FULL in the immutable raw evidence. Branch readback, followed by a separate V8 reexecution against fetched executable and JSON, gave identical structured data with zero failures. This is COMPUTATIONAL and NOT a physical TM microstep trace, formal kernel check, native Node CLI test, LaTeX compilation, project preflight or independent mathematics review.

Branch: research/tmr4-wavefront-dag058-20261115.
Source: experiments/tmr/tmr4_wavefront_dag_e2e058.js (Git blob ea4069a87820fa76484777313bdb8c705fadfc00).
Raw: results/raw/tmr/2026-11-15_1841_TMR4_WAVEFRONT_DAG058_V8_RAW.json (Git blob 9ef85640f3c1a42ece6852856afa5bd5dc31f3f8).

Original research compared: TMR-4/056 actual supplied-live frontier (original report eab0cecefaf7220eda6db46e77ed7fb552f35b28); TMR-4/057 actual no-advice Ershov tree theorem (original report 980ea2a862f6c935598e7ae575b1b6721208ea07); TMR-1/057 circuit-to-CNF source costs; TMR-2/057 actual weighted-register shortcuts; all five compact handoffs and issue #3. Primary literature: Ravi Sethi, Complete Register Allocation Problems, SIAM J. Comput. 4 (1975), https://doi.org/10.1137/0204020; Randal Bryant, Graph-Based Algorithms for Boolean Function Manipulation, IEEE Trans. Comput. 35 (1986), https://doi.org/10.1109/TC.1986.1676819; Baker, Gill and Solovay, Relativizations of the P =? NP Question, SICOMP 4 (1975), https://doi.org/10.1137/0204037. No new general-circuit optimal register algorithm is claimed.

## Mandatory four gates

| Gate | Verdict | Exact reason |
|---|---|---|
| DISJ sanity | PASS restricted | Genuine DISJ_3 has rank 8 grouped, linear-size circuit and legal cheap representations; no rank-to-all-circuits hardness inference. |
| Relativization | PASS intermediate, unrestricted OPEN | Combinatorial compiler relativizes. Any NP separation needs a genuinely nonrelativizing additional ingredient; algebrization and Natural Proofs still open. |
| Simultaneous DTISP | PASS costed upper bound; forbidden region OPEN | One physical execution has both T_total and S_peak; there is no strict FLMV contradiction. |
| Configuration counting | PASS upper-bound guard only | For total deterministic read-only-input machines T<=2^{O(S+log N)}, or 2^{O(S)} for S>=log N; not a work lower bound or random/quantum claim. |

Hostile controls retained: Horn/2-SAT, affine/Gaussian, bounded-treewidth, equality, autarky, products, padding, auxiliary variables, selector, unique-solution rank-one assignment tensors, compact circuits, local-basis invariance and field restrictions (Walsh-Hadamard not invertible in F_2), randomized Valiant-Vazirani isolation, exact counting vs decision vs parity, legitimate source rereading/caching/recomputation. /341 remains FAIL as full logical UNSAT authority; /386 remains RESTRICTED.

**ONE next load-bearing lemma D4-LONG-EDGE-SPILL (OPEN):** permit charged gate edges crossing multiple discovered levels and original inputs reused across levels, proving a genuinely paid interval-congestion frontier bound and whole-pipeline cost, or exhibit a compact legal counterexample to the proposed parameter. General circuit-to-low-frontier transfer, all SAT-machine lower bounds, and P versus NP remain OPEN.
