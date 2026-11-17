# TMR-4/068: High reconvergence and long dependency span with a constant charged live frontier

Date: November 17, 2026, America/Los_Angeles. Owner: TMR-4 / PNP Cost-Sound Abstraction. Named dependency: D4-CHARGED-LOW-LIVE-SEPARATOR-DISCOVERY. Status: PROVED/EXACT for the specified infinite source family, external mathematical review OPEN. Tests COMPUTATIONAL. P versus NP OPEN.

## Candidate, exact model, and falsifiers

For every integer m>=1 construct one complete canonical version-1 ASCII JSON source (fields exactly version,n,gates,root) using original binary truth-table gates and n=2m+2 Boolean input identities, g=5m+3 gate identities. The actual binary shared-component graph H has maximum two DISTINCT shared predecessors per target. The goal is to recognize a source-derived topological schedule whose simultaneously live shared outputs q<=3, even though both the number z of multi-consumer shared-core targets and the maximum producer-to-last-consumer order span delta grow linearly. This explicitly tests whether the prior z and delta upper certificates are necessary for low-width compilation.

The predeclared falsifiers: duplicate operand uses wrongly collapsed to one physical REF; the deliberately long a_0 -> root dependency dropped prematurely; noncommutative gate operand order silently reversed; and merging parallel labelled OBDD branches losing exact counts. Malformed source/header failures must reject as INVALID, not UNSAT. Legal cheap semantic alternatives remain allowed.

## Source construction

Using gate opcode indexing 2a+b, opcode 6 is XOR, opcode 4 is a AND (NOT b), opcode 8 AND, and opcode 14 OR. Define a_0=x_0 XOR x_1. For each i=0,...,m-1 introduce two fresh original inputs u_i,v_i and five new genuine original gates:
 
    b_i = a_i XOR u_i;
    c_i = a_i AND (NOT v_i);
    t_i = b_i AND b_i;
    s_i = c_i OR c_i;
    a_(i+1) = t_i XOR s_i = u_i XOR (a_i AND v_i).

Finally set t_final=a_m AND a_m and root=t_final XOR a_0. The two repeated b_i / c_i operands are two real operand occurrences, though each value has exactly one distinct consuming COMPONENT. They create authentic shared identities and charged REF accesses, rather than a source-level algebraic rewrite. Original records are deterministically shuffled after being built and all original vertices are reachable. The long final consumer of a_0 is genuine. The Boolean identities above explain one legal compact shortcut but are not used by the actual compiler.

There are k=3m+1 operand-shared original identities a_0,...,a_m, b_0,...,b_(m-1), c_0,...,c_(m-1). Component target count K=k+1=3m+2. The multi-DISTINCT-consumer set is Z={a_0,...,a_(m-1)}, so z=m. The original core has genuine reconvergence, with edges a_i -> b_i,c_i and b_i,c_i -> a_(i+1); additionally a_0 -> root and a_m -> root. Thus core indegree is at most 2.

## Theorem: constant-live certificate despite unbounded z and span

There is a uniform paid source-derived schedule of the original shared-component targets in order

    a_0, (b_0,c_0),a_1,(b_1,c_1),a_2,...,(b_(m-1),c_(m-1)),a_m,root,

where each sibling pair may be interchanged. The original source dependency topology itself forces this module order, apart from the sibling tie; no schedule is supplied as advice. Record use counts, actual distinct consumers, the component DAG and a deterministic topological order, then compute last-consumer positions. The maximum original-core producer-to-last-consumer span satisfies delta>=3m+1 because a_0 remains required by root, and z=m is linear in K. Yet the peak genuine cached-output count is q<=3. The ordinary local stack peak r<=3. Hence the *actual* cache-plus-stack Boolean tuple width satisfies W<=6 and the complete labelled OBDD has V<=n*2^6=64(2m+2) internal nodes. This is a uniform polynomial-time, polynomial-peak-space construction for the declared source family despite z=Theta(K) and delta=Theta(K).

Proof of the cache claim: after a_0, only a_0 is cached. Completing b_0 and c_0 may temporarily retain {a_0,b_0,c_0}. For i>=1, just before the i-th pair the live set is {a_0,a_i}; after b_i it is {a_0,a_i,b_i}; after c_i the final local use of a_i has occurred, so the live set is {a_0,b_i,c_i}; after a_(i+1), both b_i and c_i are consumed/dropped and the live set is {a_0,a_(i+1)}. The final root consumes a_0 and a_m. Thus no more than three completed shared values coexist. Each local binary fragment uses at most three scratch values; the two duplicate-REF leaf pairs in the a_(i+1) fragment generate the only size-three stack. Each original gate runs exactly once, every original input READs once, and each REF is a separate charged operation.

Proof of semantic/count preservation: source authentication and the original source's exact operand order determine the fragments and schedule. Induct on all original READ, REF, GATE, STORE and DROP instructions. Every gate consumes the authentic intended predecessor bits and applies its original four-entry table; every value remains cached through its final genuine REF. The initial cache and stack are empty; terminal root bit equals the original circuit bit for every complete input. At each original READ boundary the next instructions depend only on the actual <=6 Boolean tuple and public instruction pointer. Complete BFS emits both 0/1-labelled arcs for every reachable tuple, retaining parallel arcs. Every original input vector has exactly one complete labelled path and conversely. Consequently the integer accepted-path count equals #C. Over every field, each prefix assignment-evaluation matrix for the resulting input order factors through <=64 boundary tuples, so its rank is at most 64. The last new u_(m-1) enters by XOR, so independently #C=2^(n-1). This count shortcut is admissible and **not** evidence of necessary work.

Both previous sufficient certificates fail to establish the guarantee on this family: /067's permanent Z cache incurs z=m and /063's coarse span bound uses delta>=3m+1. The new result uses the *actual source-derived last-consumer frontier*, not a mandatory minimum frontier of every equivalent computation. It is a restricted upper construction, not an NP or general Circuit-SAT lower bound.

## One same-execution physical cost ledger

Let L be the actual canonical source bit length including operands, IDs, authentication and optional assignment; M=n+g; A=n*2^W <=64n. One fixed ordinary locally headed deterministic multitape parse -> authenticate -> count operand occurrences -> discover H and distinct consumers -> discover true last consumers -> record READ/GATE/REF/STORE/DROP -> materialize both actual OBDD branches -> exact integer count and optional pointwise answer -> serialize result run has conservative writable budget

    D = 1+L+O(M^2 log(M+2)+A*(W+n+log(A+2))),
    T_total = O(D^5+n^2), S_peak = O(D).

This single execution charges every source byte and failed parse, graph/schedule discovery, rejected strategy work if any, head/index/address/sort work, repeated REF copies, cache retention/eviction, gates, label positions, input reread-head movement by source-aware target, 0/1 arcs, <=n+1-bit counters, and output. Each original object counts once, distinct temporary copies count separately. There is no parallel-worker discount, oracle, uniform SAT lower bound, or simultaneous forbidden DTISP pair. Because n,g=O(m) and L=Theta(m log m), D and T_total are polynomial in L.

## Actually executed finite audit and revision

Native CPython finite audit of the archived original TMR-4/062 canonical-source compiler and an independent direct original-gate interpreter. Revision `tmr4-ladder068.audit1`, deterministic source shuffle seed 20261117068. Valid encoded sources for every m=1,...,64. Their actual source-derived core order and last consumers were inspected, the fully labelled OBDD was constructed and integer paths propagated. Exhaustive original assignment comparison for n<=10; deterministic structured and random assignments on larger sources. Actual results: 64 sources, 7,180 source/target assignment replays, 1,230,480 individual original-gate value comparisons, 497,936 actual stage-transition checks, six malformed-source rejection controls, zero unexpected failures. The complete raw JSON was rerun byte-identically, SHA-256 `a94e4f96ceb833bf092a76f60942415ef0bdbd8393c9a6688b9924e4fe801f54`. Exact executed Python source SHA-256 `c4a19809895cdb06b0dcc95e4f3c6563b0bb36be70d66287b4573e981fe38408`. On m=64: n=130, g=323, k=193, z=64, delta=193, q=3, W_actual=6, OBDD internal nodes=765, #C=2^129. The source SHA-256 for that final case is `fb685ffefc6e37f2395a895cf8c9ea5e244db621abdc9791ce405c631a785589`.

The archived Python source was physically executed. It is not a separate formally verified compiler, nor a TM microstep trace, and the audited code uses an exact local /062 implementation rather than a fresh repository checkout. Complete native project checkout/preflight, full manuscript LaTeX build, independent external mathematical proof review and source-equivalent hardware microstep measurement were not executed. The complete executable and raw 64-case JSON are provided in the present run's local artifact package. Repository publication of the report/manuscript and of any reconstruction loader must be distinguished from actual execution and from main merge.

## Mandatory gates

| Gate | Verdict | Reason |
|---|---|---|
| DISJ sanity | PASS restricted | Real-prefix rank only. DISJ's cheap interleaved evaluation remains legal; no grouped-rank hardness transfer. |
| Relativization | PASS intermediate / OPEN unrestricted | Purely combinatorial model transfer, no nonrelativizing NP step. Algebrization and Natural Proofs challenges remain open. |
| Simultaneous DTISP | PASS upper-only / OPEN lower-bound | One construction has matched T and S; it is not a forbidden-time-space-pair proof. |
| Deterministic configuration counting | PASS upper-bound guard only | A fixed total deterministic machine obeys T<=2^O(S+log L), not a required-work lower bound or quantum/probabilistic claim. |

Controls: Horn/dual-Horn, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarky, independent product, padding and auxiliary-extension counts, selectors, unique-solution rank-one tensors, local-basis/field effects, compact algebra and legitimate recomputation are admitted. Randomized isolation is not free. Historical /341 remains FAIL as a complete UNSAT authority and /386 remains RESTRICTED.

## ONE next load-bearing lemma

D4-SCHEDULE-PORTFOLIO-CERTIFICATE (OPEN): from arbitrary authentic shared-core DAGs with large Z and large span, construct a polynomial-cost portfolio of source-derived topological layouts and certify its *actual* maximum simultaneously live physical shared frontier, rather than an exponent based on Z or span alone. Prove one general structural family beyond the forced ladder, including charged failed layout attempts and fallback. A minimal legal source counterexample to the proposed uniform method is equally useful. The separate universal algorithmic necessity/model-transfer arrow remains OPEN.

Sources: current TMR-4/062 and /067 full original reports/manuscript, current November 15 end-to-end directive, November 17 Hostage Review; Sethi and Ullman (1970), Appel and Supowit (1987, DOI 10.1002/spe.4380170607), Sethi (1975, DOI 10.1137/0204020). The last two register-scheduling theorems concern prescribed graph models; no general circuit lower bound follows.
