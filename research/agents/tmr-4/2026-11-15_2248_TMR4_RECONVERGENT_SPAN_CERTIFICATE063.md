# TMR-4/063: source-certified reconvergent core span and exact OBDD transfer

**Pacific timestamp:** November 15, 2026, 22:48 PST. **Owner:** TMR-4, PNP Cost-Sound Abstraction. **Status:** PROVED/EXACT for a restricted source-derived schedule certificate, independent external mathematics review OPEN; executed finite audit COMPUTATIONAL. **P versus NP OPEN.**

## Candidate fixed before source search; named dependency

D4-RECONVERGENT-CORE-DISCOVERY. For every valid version-one canonical ASCII shared-gate source from TMR-4/062, use its *actual constructed* shared-component dependency graph, not an advised schedule. Write K for its component count, k=K-1 for original shared vertices, and let t_1,...,t_K be the deterministic public topological component order actually constructed by the existing /062 source compiler. For each genuine shared vertex v, let lambda(v) be the position of its **last distinct component consumer**. Define the authenticated span certificate

    delta = max_{v shared} (lambda(v) - position(v)),   max(empty)=0.

Claim: source authentication and delta are discoverable with polynomial input-bit work. The existing no-recomputation compiler, charged through to its full labelled OBDD, has q <= delta+1 simultaneously live cached values. If delta = O(log L) for complete source-bit length L, it constructs an explicit polynomial-size OBDD and emits exact original-input counts on a polynomial-time/space same-execution machine. This is a sufficient certificate for the **computed order**, not a claim about minimum schedule width or arbitrary equivalent algorithms.

Falsifiers selected before primary-source/corpus review: (1) a shared value with two distinct later consumers is prematurely dropped after the first; (2) component order is supplied without authentication or omits cost of finding the last consumer; (3) state merging drops a second labelled arc and changes #SAT; (4) a grouped DISJ rank is misused to conclude general circuit hardness. A high-span yet low-live-cache family additionally tests whether delta is only sufficient, not necessary.

## Exact domain, model and complete pipeline

The original bytes are canonical ASCII JSON with exactly `version=1,n,gates,root`, n>=1 original named Boolean inputs, g>=1 distinct arbitrary binary-table original gates (0..15), arbitrary source record order, DAG dependencies and one designated output. Every original gate and every input is root-reachable, cycles/invalid references/duplicate keys/dead records rejected as malformed, not UNSAT. The parser checks n<=2g before any n-indexed allocation. A shared source vertex has at least two real operand occurrences, including repeated operands in one gate. All original input assignments are counted once. No CNF conversion or auxiliary-variable count is required.

The actual chain is complete bytes -> all-input parser/authentication -> original sharing and component-fragment construction -> polynomial public topological schedule and last-distinct-consumer span calculation -> one original READ and GATE per original vertex, plus authentic REF/STORE/DROP -> complete true-transition labelled OBDD -> exact integer path count and optional original-input decision -> actual-input-order prefix rank bound. There is no answer oracle, borrowed schedule, input reread, hidden failed search, or unfolding of the original shared DAG.

## Theorem 8 (authentic reconvergent span transfer)

Fix every valid source C and the deterministic component ordering `pi` produced by the TMR-4/062 fallback whenever its shared-core dependency graph is not a rooted in-tree. Let pos(v) denote the unique index of the component that computes v. For every shared v define

    lambda(v)=max{pos(t) : the local component t contains a genuine REF to v}
    delta=max_v(lambda(v)-pos(v)),  or 0 if k=0.

Each consuming component is strictly later than its producer, since the authenticated component graph is acyclic and the order is topological. A shared result v is live after component i precisely when pos(v)<=i<lambda(v). Only the terminal output may additionally remain stored at the final boundary. Consequently the counted cache frontier q satisfies

    q <= delta + 1.

**Proof:** At any completed component index i, a live producer v has pos(v)>=i-delta+1, since lambda(v)>i and lambda(v)-pos(v)<=delta. At most delta distinct producer components lie in positions i-delta+1,...,i; each produces at most one shared source vertex. The terminal root accounts for at most one extra slot. During a component, its existing input cache is retained until its last actual consumer completes, and the local Sethi-Ullman stack is charged separately. This argument counts distinct physical stored values once, not every REF edge. All of the interval endpoints are computed from the original source's authenticated component dependencies. It does not require that this topological order minimize q. QED.

Let F=n+2g and r be the maximum Sethi-Ullman local component-tree label. Since each local tree has at most F leaf occurrences, r<=1+floor(log2 F). Under the /062 compiler W=q+r+1 is a conservative Boolean cache-plus-stack bound. Therefore

    W <= delta+3+floor(log2 F),
    V <= n*2^W <= 8*n*F*2^delta
       <= 16*n*(F+2)*2^delta.

Every path evaluates the original binary truth tables once each, reads each original input once, retains both 0/1 labelled arcs after merges, and preserves accepting/rejecting terminal values. Full assignments are in bijection with length-n labelled target paths, so #B=#C. Across each prefix of the derived read order, the suffix function depends only on the public instruction point and at most W retained bits: rank_K(M_prefix) <=2^W over every field K. This implication is restricted to this representation/source schedule. It neither lower-bounds the resources of an arbitrary equivalent circuit nor proves anything about general SAT machines.

The certificate is constructed and checked in polynomial bit-time from the finite source DAG. If delta<=c log2 L for a fixed c, then V and the complete input-to-output realization below are polynomial in L. The fast-path recognizer may decline large delta and the correct general /062 compiler remains available, potentially exponentially costly.

## Strict extension beyond the in-tree certificate

For each m>=3, let a_0=x_0, then emit three *original* binary gates for each i=1,...,m:

    p_i = a_(i-1) AND x_i,
    q_i = (a_(i-2) if i>=2 else a_0) XOR x_i,
    a_i = p_i OR q_i.

The output is a_m, original gate records are deliberately shuffled, and the source length includes all IDs and records. For all sufficiently large m, each a_i has two **distinct** later consumer components (the following AND module and the XOR module two stages later). Thus the shared-core graph reconverges and fails /062's one-consumer in-tree certificate. The authenticated DFS-derived source topological component order visits the local modules chronologically; each genuine consumer occurs within five component positions after its shared producer. This is checked directly from the recurrence and may also be read off from the finite, uniformly generated component topology. Hence delta<=5 for all m, q<=6, W=O(log m), and the labelled OBDD compiler is polynomial for this infinite family with k=Theta(m). Concrete tests show q=4 and, for m=128, n=129, g=384, k=255, 126 vertices with multiple distinct consumer components, delta=5 and 514 actual OBDD nodes. The modules have legal Boolean simplifications and this construction is not a hardness witness.

A separate authentic long-span control references one old input in arbitrarily many components: at m=24, delta=24 while q=2 and only 99 constructed nodes. This demonstrates the certificate is sufficient but **not necessary**, so rejecting a fast certificate is never a statement that the input is computationally hard. A DISJ_4 source has 81 accepted assignments and a 21-node OBDD in the actual local run. Its grouped assignment matrix has rank 16 over every field, yet a linear-size circuit exists.

## Same-realization bit-machine budget

Let M=n+g, A=n2^W, and L count the complete original input bytes, plus n original assignment bits when pointwise evaluation is requested. The earlier certified /062 compiler has at most n+g+R+2k+2 instructions, where R<=2g is the number of genuine shared operand references; it never computes an original gate twice. Its entire physical live bit budget can conservatively be taken as

    D=1+L+O(M^2 log(M+2)+A(W+n+log(A+2))).

One fixed ordinary locally headed deterministic multitape machine authenticates the complete bytes, checks failures, discovers core IDs/dependencies/order/last consumers/span, writes genuine instructions, builds BFS layers with both arc labels, runs exact integer path-count additions (at most n+1 bits per counter), optionally reads an original x, and emits decision/count. Identifiers, pointer and cache addresses, source seeks, stage scratch, output storage, failed discovery checks and sharing are included in the same execution. Conservative simultaneous bounds are

    T_total=O(D^5+n^2),   S_peak=O(D).

These are coarse justified **upper** bounds on the same physical realization, not machine microtrace measurements or a forbidden DTISP consequence. No network or quantum operations are used. Input cut switches are determined by the fixed public read order; an arbitrary chosen partition can have up to n-1 changes and does not license a rank-to-general-work inference.

## Actual execution, provenance and status

Local CPython 3 audit, seed 202611152244, `tmr4-reconvergent-span063.v2` and exact script Git blob `7c99b71c06d66ceb96cf3dd25b88bb999669d593`: 46 canonical sources, 6,276 exhaustive original-input assignments, 12,660 charged harness assertions, 0 failures, two identical runs. Includes 12 fixed reconvergent ladders through m=128, 24 random-opcode ladders, six long-span controls, four DISJ controls. Source and target labelled paths were compared to a separate readiness-scan original gate evaluator, not an assignment-table oracle. The 129-input example was checked by construction/count arithmetic, not 2^129 brute force. No fresh malformed-input suite: /062's existing grammar/audits supply that separately. New code imports the unchanged /062 Python compiler.

**Exact provenance caveat:** the locally executed imported /062 implementation was the archived `tmr4-live-core062.release1` package (local Git blob `8f9ee912b575de17d153d601edddab6a574548d4`), not the merged repository's `tmr4-live-core062.v1` (blob `cccf879676960f57de141e74816ad77b75946349`). Both implement the same declared authenticated live-core interface, and the /063 audit adapter checks either schema, but a native execution with the merged imported file was NOT run. Do not describe this evidence as main-branch interpreter reexecution. Published raw source Git blob `f3b53488f75f2039b5b34eca7a2febe2e61dccd2` matches actual locally executed raw bytes. Finite audit remains COMPUTATIONAL.

The source-to-OBDD symbolic argument is PROVED/EXACT at this restricted scope. Independent external mathematics review, whole-repository preflight (no checkout, GitHub DNS blocked), physical machine microtrace, and LaTeX build for this new section were NOT executed. Historical source and raw evidence are not rewritten.

## Mandatory four gates

| Gate | Verdict | Reason |
|---|---|---|
| DISJ sanity | PASS restricted | Explicit small DISJ instances have cheap circuits and rank does not imply general hardness. |
| Relativization | PASS intermediate; unrestricted OPEN | Compiler is combinatorial and relativizing; no nonrelativizing NP step. Algebrization/Natural Proofs remain unresolved. |
| Simultaneous DTISP | PASS for the matched upper-bound execution; unrestricted lower bridge OPEN | The same D governs charged T and S; no strict forbidden resource pair. |
| Deterministic configuration counting | PASS upper-bound guard | T<=2^{O(S+log L)} for total deterministic machines is a maximum-halt-run bound, not required computational work or a quantum/probabilistic theorem. |

Horn, dual-Horn, 2-SAT, Gaussian/affine, bounded treewidth, equality, products, autarky, padding, selector projection, unique-solution full-indicator rank one, auxiliary normalization, invertible local-basis field restrictions, Valiant-Vazirani randomized isolation and compact/recomputation alternatives remain legitimate. These are safeguards; not all were reexecuted in this run. /341 remains FAIL as a full UNSAT authority and /386 remains RESTRICTED. P versus NP OPEN.

## ONE next load-bearing dependency

**D4-ADVICE-FREE-LAYOUT-IMPROVEMENT (OPEN):** a uniformly polynomial-cost method that searches multiple legal topological shared-core orders and certifies low *actual live-frontier* q when the fixed DFS order has large delta, even on reconvergent DAGs. It must charge all candidate searches, failed schedules, retained values and any recomputation, and must not assert a reverse all-algorithm lower bound. A nonrelativizing arbitrary-SAT bridge is separately OPEN.

## Primary sources

Sethi, *Complete Register Allocation Problems*, SIAM J. Comput. 4(3) (1975), DOI 10.1137/0204020, confirms optimal general DAG register allocation is a different, computationally difficult task. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Trans. Comput. 35(8) (1986), DOI 10.1109/TC.1986.1676819, establishes ordered BDD background. Sethi and Ullman, JACM 17(4) (1970), DOI 10.1145/321607.321620, supplies the known local tree scheduling. Earlier /062 full proof and actual authentic compiler are preserved unchanged. No new optimum-general-DAG theorem is claimed.
