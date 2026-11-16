# TMR-4/064: Authenticated diamond-module breakout and polynomial OBDD compilation

**Date:** November 16, 2026 (Pacific). **Owner:** TMR-4 / PNP Cost-Sound Abstraction, Tracks A/C. **Scientific status:** PROVED/EXACT for the specified *restricted grammar*, subject to independent mathematical review (OPEN). Finite execution: COMPUTATIONAL. **P versus NP OPEN.**

## Named dependency, target, and falsifiers fixed before source search

D4-ADVICE-FREE-LAYOUT-IMPROVEMENT. The pre-existing /062 compiler builds the original shared core first; when many distinct source results are reused *inside one enormous remaining expression-tree component*, that policy can hold linearly many cache bits even though a source-local schedule can interleave each original shared computation with both its consumers. Seek one uniformly recognizable infinite family, not an optimal scheduler for general DAGs.

Candidate, for **every** canonical ASCII v1 source in the disjoint reconvergent-diamond-tree grammar below: authenticate, discover modules without supplied layout, produce a legal original-vertex topological read-once order with no original gate recomputation, construct a complete labelled OBDD, and compute pointwise outputs and exact original-input #SAT with simultaneous polynomial bit-machine time and peak space.

Falsifiers: (i) a source vertex/input shared across two alleged distinct modules, destroying the disjoint-tree condition; (ii) reversing a noncommutative gate's native operand order while selecting a larger-first child schedule; (iii) collapsing separately labelled arcs with the same successor and losing exact path multiplicity; (iv) authentic but malformed/huge declared dimensions, forward edges, cycles, duplicated IDs or disconnected gates silently accepted as unsatisfiable.

## Exact authentic source class

An original input is canonical ASCII JSON with exactly version=1, n, gates, root and canonical compact sorted-key encoding. There are n original identities x0,...,x(n-1) and g distinct gate identities g0,...,g(g-1). Each gate record has exactly id, a, b, op, where op is one of all sixteen binary truth tables; operands are named original vertices with genuine ordered occurrences. The complete reachable DAG is acyclic, all original inputs are used, all gate records are reached, and n<=2g is checked *before* n-indexed allocation. Malformed JSON, duplicate object keys, illegal IDs, graph cycles, dead vertices, and inputs outside the recognized promise are rejected as malformed/out of class, never labelled UNSAT.

The source root unfolds as a **binary outer formula tree** whose m leaves are genuine four-gate reconvergent diamonds. In diamond i, use three distinct fresh input IDs a_i,b_i,z_i and original gate IDs h_i,p_i,q_i,t_i with:

    h_i = op_h(a_i,b_i)
    p_i = op_p(h_i,z_i) or op_p(z_i,h_i)
    q_i = op_q(z_i,h_i) or op_q(h_i,z_i)
    t_i = op_t(p_i,q_i).

Both p and q use **both** h and z, so the original source vertices h_i and z_i are genuinely shared. No original gate/input identity of one diamond occurs in another. The other outer gate identities form one real fan-in-two tree with arbitrary ordered gate operations and no overlapping internal vertex. Thus n=3m, g=5m-1, and the number of shared original vertices is k=2m. All source gate records may appear in arbitrary list order. The recognizer must derive the diamond/tree structure from authentic predecessor IDs and reject cross-module sharing. It supplies no answer, optimization advice or runtime oracle.

## Theorem 064: uniform source-local breakout

For **every** valid member C of this exact grammar, there exists ONE fixed source-only deterministic uniform compiler satisfying:

1. It reads and verifies the full original source, detects every diamond by checking actual predecessor identities and the outer tree by a complete coverage check, and constructs a topological schedule containing exactly one READ for every original input and one original gate operation for every original gate. No source DAG is unfolded.
2. Let r be the Sethi-Ullman label of the recognized *outer* tree with each authentic diamond leaf label 1. Each diamond is evaluated by R(a), R(b), G(h), R(z), G(p), G(q), G(t), retaining h and z until **both** consumers finish, with all operand order and fan-out intact. For each outer gate, choose larger-labelled child first (source operand identities are not swapped), then the other, then the actual gate. The number of simultaneously live original Boolean signals, including the new result before retirement, is at most

        W <= r+2 <= 3+floor(log2 m).

3. The compiler constructs the **complete ordered**, nonreduced, layered, two-labelled-arc branching program B(C) with the original discovered input permutation rho. It preserves both terminal outcomes pointwise, and the number of *labelled accepting paths* exactly equals #C over the n original input assignments:

        f_B(x)=f_C(x)  (all x in {0,1}^{3m}),
        #B=#C,
        V(B) <= n*2^W <= 24m^2.

   At every prefix cut in the constructed order and every field K,

        rank_K(M_{rho[:j],rho[j:]}(f_C)) <= 2^W.

**Proof, all-step and storage.** Each diamond explicitly stores h and z until the second of p,q consumes both. Immediately after the first child gate p, only h,z,p may be live; after computing q, both h and z retire; evaluating t consumes p and q. The genuine diamond has peak three live values and finishes with just t. The outer tree's larger-labelled-first evaluation has leaf cost one and maximum stack requirement r. Replacing each leaf evaluation by a diamond requiring up to three values increases the peak by at most two. The standard label recurrence r(v)=max(r(a),r(b))+[r(a)=r(b)] for the disjoint outer tree implies a label-r tree has at least 2^(r-1) leaves; hence r<=1+floor(log2 m). The schedule emits all 3m source reads and 5m-1 gates exactly once because the recognizer establishes vertex disjointness outside each bounded diamond and the original dependency order inside it. Gate-by-gate induction shows all original gate values agree, initial live workspace is empty and the terminal root bit is identical. Sorting/ref counts are performed on original IDs, not cloned circuits.

At each of the n distinct READ operations, execute the deterministic sequence of genuine gate events up to the next READ on both hypothetical input bits, starting from the actual inherited live tuple. Merge states only when all genuinely live source values agree. There are at most 2^W states per layer, and exactly two labelled arcs from each state, even if the successors are equal. Every full path is determined by the unique assignment to each original READ identity and conversely. This bijection proves both output and exact count preservation, including multiplicities. Equal boundary tuples determine the same suffix function, giving the row-factorization rank bound for **every** field. There is no lower bound on minimum equivalent circuit or SAT-decider memory.

**Why this strictly advances /063.** The /062 component-first compiler computes all k=2m shared diamonds' h_i and z_i prior to its single remaining root component, retaining at least 2m bits simultaneously in that particular strategy. The present uniformly discovered original-vertex schedule interleaves each diamond's computation with its own consumers before starting unrelated diamonds, leaving only O(log m) bits on the balanced/tree-recursive strategy. This does not claim that all possible previous strategies were optimal, nor that source-semantic shortcuts are illegal. The /063 bounded-span certificate alone does not construct this source-level breakout.

## Same-realization resource partition

Write L for full source bytes (plus n bits and delimiters if optional pointwise evaluation is requested), M=n+g, W as above, A=n 2^W <=24m^2. A conservative writable bit budget is

    D = 1 + L + O(M^2 log(M+2) + A*(W+n+log(A+2))).

The first term includes the full authenticated source. The M term includes source indices/heads, cycle/reachability checks, module discovery, failed-recognition branches, Sethi labels, exact original-vertex schedule, operand reference tables and last-consumer scans. The A term includes at most A real BP node records, each live Boolean state, two labelled arcs, addresses, caches, source gate buffers, and exact integer prefix-path counts of <=n+1 bits. All output bits, original-variable counts, and optional pointwise input-head seeks are paid. The actual compiler evaluates original gates separately at each reached hypothetical branch state; those *construction* re-evaluations are charged and do not violate each *target execution's* once-only original-gate trace. Shared live physical objects are counted once, not once per incoming pointer.

A fixed ordinary locally headed deterministic multitape implementation can parse, recognize, build, count and optionally evaluate on the **same run**, with deliberately conservative joint bounds

    T_total = O(D^5 + n^2),   S_peak = O(D).

Thus time and peak space are polynomial in L for the declared family, not necessarily logarithmic physical space, and no forbidden DTISP resource pair is asserted. The executable is an abstract standard-library Python model, not a physical microstep trace. A source-specific even cheaper exact counter uses independent 3-bit diamond truth tables and a two-entry count vector propagated over the outer tree in O(poly L) bit time; this legal compact alternative is retained rather than excluded. The OBDD representation is one valid construction, not a necessary computation.

## Exact executed evidence (COMPUTATIONAL only)

Executable revision `tmr4-diamond-tree064.v1`, seed **20261116**, source SHA-256 **2a4e9a29dd93864b50975c504fd516f8e082f81a08de25f62e596e70c6efd2bd**. Local CPython 3.13 standard-library source ran twice with **byte-identical raw JSON**. A source-hash-checking loader executing the published exact zlib/base64 source was separately run and reproduced that raw byte for byte.

60 distinct valid canonical sources: m=1,2,3,4 across balanced/comb shapes and seeds 0..4; m=8,16,32,64,128 balanced/comb and seeds 17,23. **46,800** complete original assignments independently evaluated on the original DAG and followed through all compiled target arcs; **856,000** original-gate values independently evaluated by the direct source interpreter (not an external per-gate formal proof); **70** finite-field-two prefix-rank checks; seven malformed controls correctly rejected; zero unexpected failures. Every test also compares the OBDD's exact labelled path count to an independently computed disjoint-diamond/outer-tree integer count, including cases with 384 input variables. The largest constructed OBDD among all tests has 3,573 internal nodes. In a representative m=128 balanced case: n=384, g=639, shared k=256, W=10, actual live peak=10, constructed V=2,187, while the earlier component-first strategy must hold all 256 shared target values for its root component.

The exact source is stored as `experiments/tmr/tmr4_diamond_tree064.py.zlib.b64`, authenticated at runtime by `experiments/tmr/tmr4_diamond_tree064_loader.py`; exact raw `results/raw/tmr/2026-11-16_TMR4_DIAMOND064_RAW.json`. They were compared by Git blob to the local executed originals after publication. No full repository checkout or preflight, original physical TM microstep trace, Lean kernel, or independent external math review was performed.

## Four mandatory gates and controls

| Gate | Verdict | Reason |
|---|---|---|
| DISJ sanity | **PASS restricted** | No non-prefix grouped-rank or universal general-circuit hardness claim. DISJ has a cheap interleaved linear-size source outside this special grammar; general static-rank-to-SAT hardness remains **FAIL**. |
| Relativization | **PASS intermediate; NP bridge OPEN** | Source compilation is combinatorial/relativizing; no nonrelativizing P-vs-NP step. Algebrization and Natural Proofs are not overcome. |
| Simultaneous DTISP | **PASS for restricted same-run upper bound; lower bridge OPEN** | One source-to-output deterministic implementation has the stated pair (T,S), with no forbidden strict-region implication. |
| Deterministic configuration counting | **PASS upper-bound guard only** | For total locally headed deterministic machines, T<=2^{O(S+log L)} is a consistency upper bound, never required computational work or an automatic randomized/quantum result. |

Horn/2-SAT/affine/Gaussian, equality, autarkies, independent products, padding and auxiliary variables, selectors, unique-solution rank one, legal output-preserving rewrites, field-dependent/basis-dependent tensor rank, randomized isolation and caching/recomputation remain available. Some easy-family controls are outside this explicitly restricted grammar; no theorem excludes them or charges invented hardness to them. No majority, quantum error or amplitude reduction is made. /341 remains FAIL as a full UNSAT authority; /386 remains RESTRICTED.

**ONE next load-bearing dependency: D4-UNBOUNDED-MODULE-INTERFACE.** Find an authentic, uniformly recognized source-local schedule with polynomial compilation for **overlapping reconvergent modules**, where source values cross more than one diamond and simple disjoint-leaf factorization no longer applies. Charge the cross-module retained frontier, decomposition discovery, and possible recomputation; preserve the general fallback and all compact algorithms. A separate reverse lower-bound bridge to arbitrary SAT machines and P versus NP remain OPEN.

## Pinned primary references

Sethi and Ullman (1970), JACM 17(4), DOI 10.1145/321607.321620, tree scheduling prior art. Appel and Supowit (1987), Software: Practice and Experience 17(6), DOI 10.1002/spe.4380170607, generalized tree scheduling. Sethi (1975), SIAM J. Computing 4(3), DOI 10.1137/0204020, general DAG register allocation difficulty. Bryant (1986), IEEE Transactions on Computers 35(8), DOI 10.1109/TC.1986.1676819, OBDD background. Project predecessors /062 and draft /063 are separately scoped and preserved.
