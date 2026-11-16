# TMR-4/059 | 2026-11-15 19:09 PST | General shared DAG, charged long-edge spill

**Owner:** TMR-4 / PNP Cost-Sound Abstraction. Governing authority: research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md. **Scientific status: PROVED/EXACT, model-scoped elementary mathematical transfer; independent mathematical review OPEN.** Actually executed finite tests: COMPUTATIONAL. No unconditional SAT or general-circuit lower bound. **P versus NP remains OPEN.**

## Selected end-to-end dependency, model and falsifiers

The prior /058 result compiled **wavefront-local** source DAGs, rejecting long gate edges and input reuse across depths. The named target **D4-LONG-EDGE-SPILL** was to remove both syntactic promises while preserving authentic input-to-output semantics, sharing, signed computation cost and exact source-count meaning. This report closes that **construction dependency**, not efficient low-width layout discovery.

**Candidate, stated before corpus/primary-source review:** For every canonical, authenticated, finite, acyclic, single-output binary truth-table circuit DAG with every original gate output-reachable and every input identity used, including arbitrarily long dependency edges, construct *without supplied schedule* a public input order, once-only original-vertex schedule and complete layered OBDD, preserving both decisions and exact counts. Define a paid spill parameter c directly from actual future uses, not a prescribed abstract DAG, and prove w <= c+3k, V <= n2^w. The lower bound from rank transfers only to the discovered **scheduled source/frontier representation**, not all algorithms.

**Four falsifiers:** (F1) a gate edge jumping more than one depth leaves an uncharged old intermediate; (F2) a repeatedly used input introduced at depth d-1 remains needed at depth d, but an earlier proposed c excluded it; (F3) duplicated fan-out or a prematurely dropped shared signal corrupts a gate or path count; (F4) legal compact/equivalent DISJ, Horn, affine or identity computations contradict unrestricted rank-to-work conclusions. All four must remain legal, not be removed as spurious CEGAR paths.

Original source literature reviewed: Sethi, *Complete Register Allocation Problems*, SIAM J. Comput. 4(3), 226–248 (1975), DOI 10.1137/0204020, studies nontrivial DAG register allocation; Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Trans. Computers C-35(8), 1986, DOI 10.1109/TC.1986.1676819, develops reduced ordered BDDs. This work does **not** claim optimal layout or novel BDD foundations. Materially relevant originals include /056 circuit-to-frontier compiler, /057 no-advice tree, /058 wavefront DAG and its canonical arity correction v2, TMR-1's authenticated shared-circuit/functional-CNF interface, TMR-2's exact-count four-integer quotient (different representation/semantics), and pending PR #158's cut interface. Sources/authentication from these are kept separate from the new restricted proof.

## Exact authentic source and full pipeline

Input is a **complete canonical ASCII JSON byte string** with precisely the keys \`gates,n,out\`, an integer n >= 1, a nonempty array containing exactly g distinct gate records with keys \`a,b,id,op\`, gate IDs \`g0,...,g(g-1)\` in *arbitrary record order*, original input IDs \`x0,...,x(n-1)\`, and op in {0,...,15} encoding the four-entry binary Boolean truth table. The sole output is a gate. References and all keys must be canonical; every declared input must occur; all gates must reach the output; cycles, duplicate keys or IDs, missing/out-of-range references and malformed encodings are rejected **before** declaring a mathematical output. A canonical source outside this valid model is rejected as invalid, **never called UNSAT**. Crucially n <= 2g is checked **before n-indexed storage allocation**, since g binary gate records contain only 2g operand occurrences.

The actual pipeline is:
complete source bytes -> canonical parse and rejection -> graph identifiers/edges and cycle/output-reachability authentication -> depth and first-input-use discovery -> deterministic schedule -> exact last-consumer live intervals -> authenticated original-step stage evaluator -> merged shared *labelled* OBDD -> DP over both outgoing 0/1 arcs with integer multiplicity -> print exact #C and the decision bit [#C > 0].

All operators are original source truth tables. No SAT, #SAT, PC or arbitrary hierarchy oracle, free dynamic-rank oracle, externally provided layout, CNF auxiliary or one-sided answer shortcut appears in the compiler.

## Definitions and theorem

Let d(g) = 1+max({d(h): h is an original gate predecessor of g} union {0}). Thus every original gate predecessor h of g satisfies d(h)<d(g), although d(g) need not equal d(h)+1. For each original input x, let beta(x) be the **minimum** d(g) among consuming gates. For a gate g, beta(g)=d(g). Let ell(v) be the maximum depth of an actual consumer of v; the sole original output has the pseudo-consumer depth D+1, where D is the maximum gate depth. For each depth d let X_d={x: beta(x)=d}, G_d={g:d(g)=d}, k=max_d max(|X_d|,|G_d|).

Define the **long-lived spill set** at entry to depth d:

\[
S_d = \{x: \beta(x)\le d-1,\;\ell(x)\ge d\}
\;\cup\;
\{g:\beta(g)\le d-2,\;\ell(g)\ge d\},\qquad
c=\max_{1\le d\le D}|S_d|.
\]

The first summand *includes* original input bits first read at the **immediately preceding** depth if subsequently reused. Unlike the preliminary v1 audit, this corrected definition excludes only gates from the preceding layer, which are separately budgeted below. Every distinct identity, not each fan-out edge, is counted once.

**Theorem (uniform discovered-layout DAG transfer).** For every valid source in this exact class, uniformly discover and emit in depth order each x in X_d once followed by each g in G_d once, using numeric order within each group. The schedule is a true topological once-only evaluation of every original source vertex. Let w denote the largest number of distinct source signals retained after any event because of a future consumer or terminal output. Then

\[
w\le c+3k,\qquad V\le n2^w\le n2^{c+3k}.
\]

An authenticated deterministic compiler constructs a complete n-stage OBDD respecting the emitted input permutation rho, retains both outgoing labelled arcs even when both share one successor, and for every original assignment a follows exactly one terminal path with label f_C(a). Accordingly #accepting *labelled paths* = #C, and for every field K and every prefix j of rho,

\[
{\rm rank}_K M_{\rho_{\le j}:\rho_{>j}}(f_C)
\le \#(\text{actual reachable frontier tuples at j})\le 2^w .
\]

**Proof, without hidden representation assumptions.** An original gate input is either x whose first-use depth is <= gate depth, or a gate predecessor whose discovered depth is smaller; thus the schedule places **both real operands** before the gate. At an arbitrary event within depth d, any still-live original identity belongs to (i) S_d, (ii) original gate layer G_(d-1), (iii) newly introduced original inputs X_d, or (iv) computed original gates G_d. These categories contain <=c,k,k,k distinct identities respectively; extra physical gate scratch is O(1) and is not misreported as a source signal. In particular a repeatedly used preceding-depth input is in S_d, while an adjacent parent gate is separately in G_(d-1). This proves the width bound. Maintain a tuple containing precisely the original signals whose last authentic consumer has not yet executed. Original input introductions write their authentic x bit; gate events read each actual operand and apply the exact source truth table; retire a signal only after its final consumer. Induction over *all n+g actual events* gives original gate equality and final output equality for each a. Collapse intervening gate-only events into the transition between adjacent input-reading stages. The emitted read order is a permutation of the original n variables, so no input is reread and the state is a complete retained tuple of <=w bits at each stage. Enumerate all reachable tuple transitions; there are at most 2^w tuples per stage and n stages, with at most 2V labelled arcs. Parallel arcs are genuine different input assignments, not an instruction to add one distinct successor once. Exactly one complete labelled path corresponds to each original assignment, proving exact count. For any prefix assignment, its complete future Boolean cofactor is determined solely by the tuple at the corresponding stage; rows with equal tuples coincide. The factorization through <=2^w distinct rows proves rank over every field. QED.

A rank-R prefix gives **ceil(log_2 R)** live original values only for this schedule/frontier representation. It gives no lower bound on other layouts, circuits, direct SAT deciders, exact algebraic counting or machines using semantic simplifications/recomputation. Computing k,c,w from the original source is polynomial, but they may be Theta(g); there is no uniform promise that c+3k = O(log L).

## SAME_REALIZATION bit-machine ledger and explicit loss

Let L be all original input bits and M=n+g. The source uses O(L) bits. The graph, depth tables, sorted genuine event schedule, last-use identifiers and shared fan-out maps require at most
B=O(L+(M+nM)ceil(log_2(M+2))) bits, including any authentication and temporary buffers. Put A=n2^w, and define
D_*=1+L+B+O(A(w+n+ceil(log_2(A+2)))).
One fixed deterministic locally headed multitape machine can parse, validate, authenticate, derive the layout and actual live intervals, allocate the full OBDD, enumerate the **two** genuine arcs from every reachable state, evaluate actual assigned inputs through the same source representation, maintain path counts of at most n+1 bits, combine integer counts with bit-costed additions, print both outputs, and reclaim scratch. A deliberately loose simultaneous bound for **this one complete execution** is

\[
T_{\rm total}=O(D_*^5),\qquad S_{\rm peak}=O(D_*).
\]

The same machine and the same allocated OBDD are accounted for in both bounds. Every source/head move, address/index, gate lookup/evaluation, sorting/selection, rejected candidate, graph/depth discovery, repeated access, fan-out retention, caching, arc/state deduplication, integer bit operation, output and print buffer is covered by the polynomial overhead. Source gate objects are stored once; output graph states/arcs are separately real objects. No parallel-span shortcut or uncharged input oracle is used. Malformed encodings are rejected in polynomial(L) time/space; the necessary n<=2g preallocation check avoids a tiny source causing an enormous declared-input table.

This explicit construction is polynomial in L if w=O(log L), including computed-layout discovery. Otherwise **it can be exponential**. A generic Turing-machine lower bound does not follow from this upper bound. A physically exact microstep trace has not been run; the finite implementation is an ECMAScript semantic/operation-level audit, with the conservative ordinary multitape existence/upper bound proved abstractly, not an observed instruction count. A future CNF/Tseitin translation would require separate charged wire/variable and exact-count normalization and is not present here.

## Correction to preliminary v1: previous-level input spill

The preliminary executed source \`tmr4-long-edge-spill059.v1\` used the narrower old spill set {v: beta(v)<=d-2 and ell(v)>=d}, which **omitted input identities introduced at d-1 and reused at d**. That set is not sufficient for the stated four-category accounting. This is a theoretical coverage defect, regardless of its finite tests passing; **v1 is retained as historical provisional evidence, not the final theorem certificate**. V2 includes all prior-layer retained input identities while excluding prior-layer gate identities already budgeted by G_(d-1). A new authentic two-gate circuit \`g0=AND(x0,x1);g1=XOR(g0,x0)\` explicitly has corrected c=1 and old cOld=0. This repairs the formal resource partition; it is not described as a newly discovered circuit lower bound.

## Exact executed evidence and scientific limits

Actually executed in hosted V8, then exact *fetched-source* V8 reexecution: \`tmr4-long-edge-spill059.v2\`, xorshift32 seed 20261115, **53** authentic canonical circuits, **1,340** complete assignment replays, **15,110** actual source gate/stage events, **532** finite-field rank calculations in F_2 and F_101, **38,420 assertions**, **7** malformed/rejected sources, **zero failures**. All 53 raw canonical source strings and observed k,c,w, width states, accepting counts and exact source sizes are published, with the added input-spill countercontrol. The original v1 executed 52 valid cases and 38,309 assertions; do not cite it as the final spill definition.

Executed v2 source, Git blob \`073e6d01cf3aaea9c58c8c89f788389219722ae7\`:
\`experiments/tmr/tmr4_long_edge_spill_e2e059_v2.js\`.
Exact raw, Git blob \`1022f1c93fd0839f13e0798b55edbe2fd834687b\`:
\`results/raw/tmr/2026-11-15_1909_TMR4_LONG_EDGE_SPILL059_V2_V8_RAW.json\`.
The source was fetched **from the branch** and reexecuted in hosted V8, and its JSON output matched the published raw bytes exactly. Native Node CLI, project checkout/preflight, complete TeX build, independent peer mathematical review and physical TM microtrace were **not** performed at this stage.

## Mandatory four-gate table

| Verification gate | Verdict | Exact scope |
|---|---|---|
| DISJ sanity | **PASS restricted**, unrestricted static-rank-to-circuit inference **FAIL** | Original DISJ_3 source is 5 gates, grouped assignment rank 8 in F_2 and F_101, yet linear-size depth-two circuit exists. This theorem bounds a particular discovered OBDD only. |
| Relativization | **PASS intermediate**; unrestricted NP bridge **OPEN** | All source semantic/OBDD claims are combinatorial and relativizing. Any P-vs-NP argument would need a specified nonrelativizing ingredient; algebrization and Natural Proofs audits remain OPEN. |
| Simultaneous DTISP | **PASS for a single charged upper-bound execution**; forbidden-region implication **OPEN** | One fully materialized machine has both reported T and peak S. It does not attain any strict hierarchy-forbidden pair. |
| Deterministic configuration counting | **PASS as upper-bound guard only** | For total fixed deterministic read-only-input machines T<=2^{O(S+log L)}; not a work lower bound or a randomized/quantum claim. |

Controls explicitly executed: DISJ grouped cut and actual compact source, authentic long gate edges, shared fan-out/reconvergence, repeated input use including from immediately preceding layer, malformed bytes, huge declared n, duplicate keys, cycles, dead gates, unused input, illegal opcode and bad references. Other controls **admitted but not independently executed here**: Horn/dual-Horn, 2-SAT, affine/Gaussian, bounded-treewidth, equality, autarkies, independent product, padding, auxiliary wires, selector, unique-satisfying-assignment rank-one tensor, compact algebra and source recomputation; no inference against their real cheap paths. Invertible local bases preserve rank; Walsh-Hadamard is singular over F_2. Randomized Valiant-Vazirani isolation is not a free deterministic transfer. /341 **FAIL** as full logical UNSAT authority; /386 **RESTRICTED**.

**ONE next load-bearing lemma D4-LOW-CONGESTION-DISCOVERY (OPEN):** Find a uniform costed alternative layout/ordered read strategy for a genuinely nontrivial shared-DAG subclass, with proved width better than the fixed depth schedule *and* acquisition/evaluation costs, or establish a model-matched obstruction to efficient discovery. Any inference about every equivalent circuit requires a separately proved reverse-reconstruction or nonrelativizing resource lemma. P versus NP remains OPEN.
