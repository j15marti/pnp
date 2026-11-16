# TMR-4/061: source-certified logarithmic frontier for bounded-sharing circuit DAGs

**Date:** 2026-11-15 20:36 PST (America/Los_Angeles). **Owner:** TMR-4, PNP Cost-Sound Abstraction, Tracks A/C. **Scientific status:** PROVED/EXACT in the declared restricted model, independent mathematical review OPEN; separate finite tests COMPUTATIONAL. P versus NP OPEN.

**Governing first directive:** research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md, main blob 8451d955f6cd5397de0895f8ebb46e30818842c3. Scientific directive: 2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md. This is a connected extension of the original TMR-4/055 to /060 authentic circuit-to-OBDD pipeline, not a theorem about unrestricted SAT.

## Candidate and falsifiers fixed before literature/project search

**D4-LOW-CONGESTION-CERTIFICATION.** For every finite canonical binary-gate single-output source DAG with all original inputs/gates root-reachable, let **k be the number of ORIGINAL vertices, including input vertices, used in two or more operand positions**. Repeated operands count as two uses. Can a uniform source-derived compiler, without supplied schedule or uncharged formula expansion, produce a read-once register evaluation with retained Boolean values at most k+O(log(n+g)), then construct a complete labelled OBDD that preserves every original gate, every accepting/rejecting result and exact original-input #SAT? Prove both time and peak space for one physical realization, and maintain rank implications limited to the compiler's actual input order.

Falsifiers:
1. A shared gate used by many downstream gates or across arbitrarily long edges is accidentally recomputed, multiplied by fan-out, or discarded before its last use.
2. An original input reused many times is reread as a fresh branch, breaking read-once and path multiplicity.
3. A high grouped DISJ cut, Horn, affine, unique selector, redundant gate, auxiliary gadget or compact direct algorithm is incorrectly promoted to an all-circuit lower bound.
4. Invalid or adversarial huge declared n, cyclic/dead gates, and repeated operand positions defeat the parser or undercharge allocation.

All four remain legal hostile controls. No false abstract-free answer is asserted.

## Exact source domain and uniformity

A valid source is a complete canonical ASCII JSON byte string with precisely the keys **version=1,n,gates,root**. There are n>=1 original input IDs x0,...,x(n-1), g>=1 distinct gate IDs g0,...,g(g-1) (or, in the executable's canonical identifier check, distinct nonnegative canonical decimal gate IDs), one designated gate root, and a list in arbitrary order of records each having exactly **id,a,b,op**. Opcode op in 0..15 is a binary truth table indexed by (2a+b). All n input IDs occur in the reachable source, every gate is root-reachable, the gate dependency graph is acyclic, and each operand is a gate or original input. Actual gate IDs are authenticated; no layout, advice or hidden oracle is supplied. The general symbolic theorem permits either canonical dense IDs or explicitly authenticated sparse IDs. Source encoding length is L bits, and n<=2g is checked **before** any n-sized allocation because there are 2g operand occurrences.

Invalid strings are rejected as **malformed**, not called UNSAT. A conceptual fixed multitape implementation handles all byte lengths using iterative DFS and bounded-memory integer decoding; the executed Python 3 prototype uses recursion and establishes only finite test behavior, not Python runtime totality on arbitrarily deep valid DAGs. If source and assignment are both supplied, add n bits and delimiter to L. The exact-count calculation needs no assignment advice.

## Constructed low-width schedule and source-to-OBDD theorem

Let U be the set of source vertices with at least two outgoing operand occurrences. Let k=|U|, counting each source identity once, not each wire or each fan-out occurrence. The pseudo-consumer of the designated output is counted only for output liveness and not as a second gate-use. The emitted source is a **public deterministic read-once instruction program**, whose instructions are READ original input x_i once; REF cached source vertex; GATE original 16-table operation once; STORE one shared result. The source graph is not unfolded, and all cache REF operations and their accesses are charged.

**Theorem /061 (authenticated shared-core end-to-end transfer).** For every valid source C in this exact model, a single uniform compiler can:

(a) discover the shared set U and a topological order of its members, compute a structural evaluation schedule containing exactly one READ per source input and exactly one GATE per original gate, maintain a cache of at most k shared values, and evaluate each remaining tree component using the larger-first Sethi-Ullman/Ershov rule;

(b) retain at most
     
    w = k + 2 + ceil(log2(n+2g+2))

Boolean values in the shared cache and temporary stack simultaneously, on every actual assignment, with all shared result references served from the cache;

(c) compile its deterministic read-once stages into a complete, layered, labelled OBDD B with

    V(B) <= n*2^w <= 8*n*2^k*(n+2g+2),

two actual 0/1-labelled outgoing arcs per internal node, pointwise B(x)=C(x), and exact accepting labelled-path count #B=#C, with multiplicity through merged states;

(d) for every field K and every prefix of the **constructed input order rho**,

    rank_K(M_rho-prefix,rho-suffix(C)) <= 2^w.

The pipeline is source bytes -> authentication -> discovery of U -> guarded Sethi-Ullman component decomposition -> public physical instruction schedule -> authentic gate values and fixed original input order -> BFS of real stage configurations with both labelled arcs -> integer path-count DP and optional supplied-x evaluation -> exact output bit and #C -> *restricted* rank/width consequence.

**Proof of all-step construction and cache bound.** Every nonshared vertex has at most one operand-use consumer. Deleting the outgoing edges of U exposes a directed forest of rooted binary expression trees; each tree root feeds either one shared vertex or the designated output. A topological ordering of all original vertices induces a topological ordering of U. For each u in that order, recursively evaluate its two predecessors until a shared predecessor is reached. That predecessor is already stored; it is read through REF as a leaf, not recomputed. Evaluate nonshared predecessor trees using the larger-Sethi-label child first and the original truth-table opcode, then STORE u. Finally evaluate the output component. Each nonshared original vertex has exactly one consumer and therefore appears in exactly one component. Each shared original vertex is computed once at its target. Induction over original DAG vertices establishes that the stored/stacked value equals the actual original source gate/input value after *every* instruction and at both terminal labels. This also establishes initial empty-stack/initialized-cache correspondence. It establishes that no original input is read twice; a shared original input is read once when its own shared target is evaluated, then obtained via cache later. Since all original inputs are reachable and every actual vertex is emitted once, every x_i is read exactly once.

Replace all shared predecessors in a component by cache-REF leaves. These components are true binary trees even when the original shared gate has unbounded downstream fan-out; each reference contributes only a leaf occurrence, not a new source computation. The usual Sethi-Ullman recurrence r(leaf)=1, r(g)=max(r(a),r(b))+[r(a)=r(b)] bounds temporary stack usage for the larger-first postorder. A binary expression tree of label r has at least 2^(r-1) leaves. The total number of fresh-input leaves plus shared-reference occurrences over all components is at most n+2g, so each component needs no more than 1+floor(log2(n+2g)) stack values. Keeping all k shared slots, including those not yet written, plus conservative staging/swap slack gives the stated w. Gate inputs and repeated children are genuine stack values; no algebraic simplification, original-node duplication or uncharged recomputation occurs. A physically printed instruction program is deterministic and has O(n+g) source operations plus O(g) REF events (the number of source operand positions), even if one cached node has arbitrarily many consumers.

**Proof of representation/semantic/count transfer.** Split the public instruction schedule at its n distinct READ operations; before each READ the source has a public program counter and a cache/temporary stack of at most w bits. Starting at the authentic empty state, BFS computes each reachable layer state under the two hypothetical bits by actually executing the intervening original source instructions and REF/STORE accesses. Equal next-layer states are merged once. The two labelled outgoing arcs, including parallel arcs to the same successor, remain distinct. Induct on layer and on internal instructions: on every original input x, source and OBDD have identical gate values, cache/stack, program counter, and terminal output. Each length-n labelled path corresponds to exactly one original input vector because every original x_i is read once in the fixed public order. Conversely every input vector generates one path. Integer DP with an n+1-bit count per reachable state preserves multiplicity, so #B=#C. Each prefix induces at most 2^w possible cached/stack configurations, so its row matrix factors through at most 2^w distinct suffix functions over every field. Neither this factorization nor any static nonprefix rank is a lower bound on equivalent algorithms.

If k<=c log2(L+2) for a fixed c, then w=O(log L), V<=poly(L), and the fully instantiated compiler is polynomial-time **and polynomial peak space**, with costs paid rather than supplied as advice. The input family may have genuinely shared long edges, repeated original inputs and fan-out linear in g. No claim of an improved *sublinear-space* algorithm, a source circuit lower bound, or SAT lower bound follows.

## One-realization physical resource ledger

Let M=n+g, A=n2^w, L complete authenticated input bits (plus n if a particular x is supplied). The full source table, canonical parser, all use-counts, graph topological certificate, each component's Sethi label, visited flags, event list, public order, shared-slot map, last-use/fan-out pointers, failed authentication work, indices and explicit original input-head seeks fit in a conservative O(L+M^2 log(M+2)) work-bit budget. Stage boundary cache plus stack has at most w Boolean bits, while its program counter, decoded wire indices, source-read addresses and tabular maps are additional logarithmic/control storage, never called zero-cost. At most A labelled OBDD states are materialized, each with public layer/index, w data bits, two target indices, both distinct arc labels, and an n+1-bit exact path-count counter. A conservative simultaneous workspace bound is

    D = 1+L + O(M^2 log(M+2) + A*(w+n+log(A+2))).

A fixed locally headed deterministic multitape implementation with sequential scans, explicit graph/queue storage, source input rereads as needed, bit-level integer additions and full output writes admits, on the **same** combined parse+construction+count+(optional) evaluation execution,

    T_total = O(D^5+n^2),   S_peak = O(D).

These bounds deliberately overcharge access, decimal parsing, table lookup, stage simulation, source authentication, failed candidate checks, cache writes/reads, sharing, fan-out, recomputation (none of the original gates), reads, head/address tracking, output and arithmetic precision. They do not silently replace total sequential work with parallel span or per-worker space. The exact count uses at most n+1 bits and is included in D. The upper bounds can be exponential when k is large. This is a deterministic existence proof for a fixed implementation, **not** a measured Python instruction trace or an optimal polynomial exponent.

## Executed finite evidence, exact revision and controls

ACTUALLY EXECUTED CPython 3.13.5 locally on the same complete Python source subsequently published as **tmr4_fanout_core061.py**, revision **release1**, deterministic RNG seed **20261115**. Every test source is canonical ASCII JSON with source SHA-256 listed for three sample instances in raw output; gate records are deliberately shuffled, not pre-topologically laid out.

Five genuine families: fanout_hub (28 cases), shared_input (28), long_edge (28), two_hubs (20), DISJ (16). n=4..10 where appropriate; 120 distinct encoded cases; 37,760 complete original assignments; 765,643 assertions with zero failures; seven malformed variants rejected (huge_n, bad_op, dead_gate, bad_ref, cycle, duplicate_id, noncanonical). The executable independently runs original source truth-table evaluation, a compiled public cache+stack schedule, **BFS of real stage transitions without an assignment oracle**, labelled-arc exact count DP, and GF(2) rank at every nontrivial prefix. Across those cases the maximum actual shared cache was two slots and maximum constructed OBDD size 59 nodes. All assertions passed. Tests validate the finite implementation; the unbounded quantified theorem is the separately supplied symbolic proof.

Executable: experiments/tmr/tmr4_fanout_core061.py. Immutable raw: results/raw/tmr/2026-11-15_2036_TMR4_SHARED_CORE061_PY_RAW.json. Original literature: Sethi and Ullman, *The Generation of Optimal Code for Arithmetic Expressions*, J. ACM 17 (1970) 715-728, DOI 10.1145/321607.321620 (tree scheduling); Sethi, *Complete Register Allocation Problems*, SIAM J. Computing 4(3), 1975, DOI 10.1137/0204020 (DAG allocation hardness); Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Trans. Computers 35(8), 1986, DOI 10.1109/TC.1986.1676819 (ordered BDDs). These are established ingredients, not claimed new universal DAG scheduling algorithms. Original project /055, /056, /057, /059, /060 were consulted; TMR-1's source/count preservation and TMR-2's dynamic invariant remain separate interfaces.

**Verification not executed:** no local Git repository checkout, so updated repository preflight not run; no LaTeX compilation, physical TM microstep replay or independent mathematical peer review. This does not affect the actual local CPython execution statement.

## Mandatory gates and hostile controls

| Gate | Verdict | Exact reason |
|---|---|---|
| DISJ sanity | **PASS restricted** | DISJ_d has rank 2^d on the grouped x:y cut and a linear-size fan-in-two formula; k=0 in its formula DAG, and the compiler selects a cheap interleaved/pairwise order. General-circuit hardness from static grouped rank is **FAIL**. |
| Relativization | **PASS intermediate; unrestricted promotion OPEN** | This is a relativizing combinatorial compilation with no nonrelativizing NP step. An NP separation would require a different step, with algebrization and Natural Proofs audited. |
| Simultaneous DTISP | **PASS for constructed upper bound; lower-bound bridge OPEN** | One fixed physical construction has jointly T=O(D^5+n^2), S=O(D); no strict forbidden pair and no all-algorithm lower bound. |
| Deterministic configuration counting | **PASS upper-bound guard** | A total deterministic read-only-input machine obeys T<=2^{O(S+log L)}, and if S>=log L, T<=2^{O(S)}. Not a necessary-work lower bound and not applied to quantum/randomized stopping time. |

Additional guards: Horn, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarkies, independent products, padding, auxiliary variables, selector, unique satisfying assignment's rank-one full indicator, general compact circuits and recomputation all remain legal. Invertible local basis transformations preserve cut rank and Walsh-Hadamard is not invertible over GF(2). Valiant-Vazirani isolation is randomized and promise-sensitive. Exact #SAT counts on original variables only; any CNF auxiliary would require a parsimonious bijection or separately charged normalization. /341 remains FAIL full logical UNSAT authority and /386 remains RESTRICTED. No P versus NP inference.

## ONE next load-bearing dependency

**D4-SHARED-CORE-EXTENSION (OPEN):** derive and test an authentic source-local decomposition allowing *many* shared nodes but a low-width quotient of shared dependencies, with a uniform schedule finder and an all-step charge. It must strictly generalize k=O(log L) without replacing the source by an equivalent easy circuit without cost. The separate reverse necessity theorem for all equivalent SAT machines remains OPEN.

**Publication status:** additive role-owned report; only the TMR-4 living manuscript and compact handoff may be modified. Retired proof trackers and peer manuscripts remain untouched. Verify Git blob readback and branch/main status separately.
