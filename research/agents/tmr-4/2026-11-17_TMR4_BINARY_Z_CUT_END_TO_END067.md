# TMR-4/067: source-authenticated binary shared-core Z-cut compiler

Date: 2026-11-17 Pacific. Owner: TMR-4, Tracks A/C. Named dependency: **D4-RECONVERGENT-CORE-DISCOVERY / D4-BINARY-Z-CUT067**. Scientific status: **PROVED/EXACT restricted, independent external mathematical review OPEN**. Finite results **COMPUTATIONAL**. P versus NP OPEN.

## End-to-end candidate, quantifiers, and falsifiers

For **every valid original canonical ASCII JSON shared binary-gate DAG**, use the /062 genuine component core H. Each component target t has a set D(t) of DISTINCT shared predecessor target IDs, although original reference multiplicities are preserved independently. Assume max |D(t)| <= 2. Let S denote all original vertices with at least two original gate operand-use occurrences, k=|S|, K=k+1 counting the root target, and Z={s in S: at least two DISTINCT consumer targets of s}, z=|Z|. Claim a source-discovered, fully charged schedule retaining permanent Z results and computing the other targets in unique-consumer trees with logarithmic live cache. The result is a complete original-input read-once OBDD with exact original decision and counting semantics, not an unrestricted SAT algorithm.

Falsifiers chosen prior to primary-source review and the code audit: (1) collapse two genuine consumer targets into one because of duplicate operand positions; (2) drop a non-Z shared value before the last real REF in its consuming fragment; (3) change a noncommutative gate's operand order or reread an original input; (4) erase 0/1 branch multiplicity when target states merge or treat invalid sources as UNSAT. All were considered in the proof and finite test design.

## Authentic input -> exact output pipeline

Source fields are exactly version=1, n, gates, root; n>=1, every gate record has original id, a, b and 4-bit opcode, every input and gate is root-reachable and the graph acyclic, and records may be shuffled. Reject noncanonical bytes/keys, wrong types, cycles, dead gates, invalid gates/opcodes and huge declared n. Enforce n<=2g before n-indexed allocation. Count complete source length L including IDs, operands, opcodes and optional supplied assignment bits.

Authenticate -> count original operand uses -> partition every original READ/GATE into a unique local fragment, retaining every REF occurrence -> discover distinct consumer sets and binary H -> derive Z -> topologically order Z and schedule each residual in-tree larger-label-first -> emit all original READ/REF/GATE/STORE/DROP operations -> execute actual instructions in a complete 2-labelled OBDD BFS -> exact integer path count and optional pointwise evaluation -> actual-order rank/width upper consequence. Unsupported higher-arity cores use the old correct unrestricted fallback without a certified low-width claim.

## Symbolic theorem and proof

For every valid source with max_t |D(t)|<=2, a deterministic uniformly constructed actual-source evaluation program reads every original input exactly once, evaluates each original gate once, and performs exactly R<=2g source REF occurrences, k shared-result STORE operations and k subsequent DROP operations, preserving all original gate values, both terminal labels and exactly the same number of accepting original assignments. Let q be the peak simultaneously cached original shared-target values and r the maximum genuine local stack occupancy. Then

    q <= z + 1 + floor(log2(2K))
    r <= 1 + floor(log2(n+2g))
    W <= q + r + 1
    V <= n*2^W <= 16*n*K*(n+2g)*2^z

The OBDD respects a source-computed public original-variable permutation, has both outgoing labelled arcs at each node, f_B=f_C pointwise and #B=#C including parallel arcs. For every field, each prefix/suffix assignment-matrix rank for that discovered permutation is <=2^W. z=O(log L) implies polynomial time and peak space for THIS compiler.

Proof: every original nonshared source vertex has exactly one fragment owner; each original shared vertex is computed once at its own target and elsewhere appears as an original-source REF leaf. Since a non-Z target has at most one distinct later target consumer, cutting outgoing Z edges FOR SCHEDULING leaves a unique-consumer directed forest. Each non-Z target belongs to one such tree. Process Z targets in their original topological order, treating earlier Z results as permanently cached leaves, then process the root. Binary-tree larger-child-first register labels bound completed non-Z target values by 1+floor(log2(2K)); there are at most K original core targets and at most 2K cut-reference leaf occurrences. At most z Z values are retained permanently. A non-Z target is dropped after its unique parent fragment has consumed ALL genuine repeated REF occurrences; those repeated REF accesses contribute time and local stack copies but do not create new distinct parent components. Hence q is bounded.

Within each genuine original local fan-in-two fragment, classical larger-first scheduling uses at most r scratch bits because its leaf occurrence count is bounded by n+2g. The program restores operand order at noncommutative truth-table gates. Induction over all actual original READ/REF/GATE/STORE/DROP events proves every value, initial/terminal state and liveness. The resulting public input-read stages have at most 2^W live Boolean tuples per stage. Actual-BFS labelled paths are in bijection with full assignments, even if both labels enter one merged successor, so exact integer path counting preserves #SAT. Future suffix functions factor through these real stage states, giving the rank bound. Neither a large prescribed OBDD nor its cut rank forces hardness for arbitrary equivalent circuits.

## Same-realization resource ledger

Let M=n+g and A=n2^W. A fixed ordinary locally headed deterministic multitape source parser, validator, component compiler, complete-O/BDD constructor, exact counter and optional evaluator fits a simultaneous conservative ledger

    D=1+L+O(M^2 log(M+2)+A(W+n+log(A+2)))
    T_total=O(D^5+n^2),  S_peak=O(D).

D counts encoded source, parser, failed recognition work, distinct consumer graph construction, source-derived choices and Sethi labels, all cache reads/writes/copies, gate buffers, output-node IDs, both arc pointers, original input head movements and addresses, exact counters of <=n+1 bits, and complete serialized output. Sharing is one physical source object, while physically distinct temporary copies and access operations are charged. All costs are on the SAME machine execution. The output may be exponentially large in z. This is not a measured Turing-machine microstep trace, a forbidden DTISP resource pair or a lower bound on other algorithms.

## Executed evidence and provenance

Local archived /062 standard-library compiler was extended without accessing a native GitHub checkout. Local actual Python 3 execution, deterministic seed **20261117067**, exact compiled sources SHA-256:

- `experiments/tmr/tmr4_reconvergent_zcut067.py`: `4714931fdd6cd730830d826b194c23080bcd83037eb327a1a1f48fb962cc9c95`
- `experiments/tmr/audit_reconvergent_zcut067.py`: `570623036442f388103a0d5d2ffbe865150e3559f92f9e3ba54bf6313bd1d4f1`

Small stage: 31 authentic sources, 3,656 original assignment replays, 94,904 independent original-gate comparisons, 28,328 original-compiled stage-transition checks, six malformed-input rejections, no unexpected failures. Large stage: 15 authentic sources, 960 deterministic seed/structured assignment replays, 50,112 independent original-gate comparisons, 14,464 stage-transition checks, no unexpected failures. Combined: **46 sources, 4,616 assignments, 145,016 gate comparisons and 42,792 stage-transition checks**, all passed. Complete two-labelled OBDD arcs and output counts were built in each case; exact counts were checked against exhaustive original-input enumeration for n<=10. The small stage reproduced byte-identical JSON on repeat. Largest observed Z=7, q=9, explicit OBDD nodes=189. The full tested code and immutable JSON exist separately in the user's locally generated TMR4_067_ZCUT_PACKAGE.zip; they have **not** been uploaded to this branch, so remote code execution cannot be claimed. The local isolated LaTeX section compiled twice. The updated full manuscript is GitHub-readback verified, but full repository preflight, full manuscript build, formal kernel, physical machine trace and external independent mathematical review were not executed.

## Four gates and required controls

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS restricted; grouped static-rank hardness transfer FAIL |
| Relativization | PASS intermediate; nonrelativizing NP bridge OPEN, with algebrization/Natural Proofs |
| Simultaneous DTISP | PASS one combined upper-bound ledger; lower-bound contradiction OPEN |
| Deterministic configuration counting | PASS as upper bound only T<=2^O(S+log L), never necessary work |

Preserve Horn, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarkies, products, padding, auxiliary/selector and unique-solution rank-one controls, field/local basis and all compact/recomputation alternatives. /065's all-order OBDD/HWB obstruction and /066's polynomial adaptive FBDD remain distinct. /341 FAIL as full UNSAT authority and /386 RESTRICTED. P versus NP OPEN.

## ONE next load-bearing lemma

**D4-CHARGED-LOW-LIVE-SEPARATOR-DISCOVERY (OPEN):** For authentic large-Z cores, construct and certify a genuinely lower actual simultaneous live frontier by a paid schedule, decomposition, eviction or recomputation, or exhibit a rigorous counterexample. A reverse source-to-ALL-equivalent-machines necessity theorem remains separately OPEN.

## Primary references

Sethi-Ullman (JACM 1970, DOI 10.1145/321607.321620), Appel-Supowit (1987, DOI 10.1002/spe.4380170607), Sethi (1975, DOI 10.1137/0204020), Bryant HWB (1991, DOI 10.1109/12.73590). November 15 repository coordination directive and November 17 Hostage review. This is a restricted use of prior tree register scheduling with a new authenticated cut, not a new unrestricted DAG allocation theorem.
