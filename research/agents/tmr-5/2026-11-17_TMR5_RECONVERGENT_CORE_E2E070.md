# TMR-5/070: independent end-to-end sparse-reconvergent-core compiler audit

Date: November 17, 2026, Pacific Time. Owner: TMR-5 / PNP Machine Bottleneck Redteam. Named dependency: **D4-RECONVERGENT-CORE-DISCOVERY**, the new binary-core candidate in \`PNP_Hostage_Review_and_Agent_Restart_2026-11-17.md\`, Appendix D.

**Scientific status: PROVED/EXACT RESTRICTED** for the independently checked compiler construction and symbolic resource ledger, with external mathematical review OPEN; finite executable evidence is **COMPUTATIONAL**. P versus NP OPEN.

## Candidate, quantifiers and falsifiers

For each source-valid, canonical ASCII JSON fan-in-two shared Boolean circuit with n named original inputs, g actual binary gates of all 16 truth tables, root reachability and acyclicity, use the original TMR-4/062 partition: shared source vertices S appear in at least two **operand occurrences**. One local component is owned by each member of S plus the root, with genuine REF leaves for other shared vertices. Let H be the DAG of distinct component references, Q=|S|+1, and assume that **every H component has at most two distinct predecessors**. Let Z be the nonroot H vertices with at least two distinct H consumers, and z=|Z|. Repeated operand occurrences count as multiple instructions but only one distinct H edge. The goal is a uniform compiler of the authentic source to a pointwise-equivalent complete labelled OBDD with exact original-input count and W<=z+O(log L) *logical* retained Boolean bits, where L is complete source byte length.

Potential falsifiers: (1) a cycle, missing original input, or high distinct in-degree is silently accepted; (2) repeated REF operands lead to duplicate gate evaluation or premature eviction; (3) noncommutative truth tables, zero outputs or identical 0/1 successor nodes corrupt exact counting; (4) the source, graph discovery, real HEAD/REF/STORE/DROP operations, retained scratch, integer precision or serialized output are omitted from the matched cost ledger.

## Exact construction and proof

The original source partition gives exactly one original READ per input identity and one original GATE per source gate, with R<=2g distinct **occurrences** of actual REF instructions. All shared results are computed once. A shared original input is likewise READ once and then referenced. This does not unfold the original shared DAG.

Cut H a second time at Z and the root. Because every H vertex outside Z or the root is reachable from the root, acyclic, and has precisely one **distinct** consumer, it belongs to exactly one second-level component tree. Multiple REF occurrences of that child *within* its sole consumer remain separate operations in the underlying original local component, rather than making two copies of the child computation. This distinction is essential.

Compute all second-level components ending at Z in an original-source topological order, then the root component. Give each tree vertex a Sethi-Ullman label using its distinct (at most two) dependencies and evaluate the larger-labelled child first; original binary gate operand order is restored for noncommutative operations. Retain finished Z values until final root computation. DROP any other H component result immediately after its sole consuming component finishes, then STORE its parent's result. At the end, DROP remaining Z values before OUTPUT. This produces exactly n READ, g GATE, R REF, |S| STORE, |S| DROP and one OUTPUT. No source gate is recomputed.

If r_H is the maximum second-level tree label and r the maximum original local-expression label, the completed Z cache uses at most z Boolean bits, the temporary unique-consumer core subtree at most r_H, the currently evaluated original component at most r, and one staging cell is sufficient. As each secondary tree has at most O(Q) leaves, the ordinary binary tree leaf argument proves

    W <= z+r_H+r+1,
    r_H <= 1+floor(log2(3Q)),
    r <= 1+floor(log2(n+2g)).

Since Q and n+2g are bounded by a fixed polynomial in L, W<=z+O(log L). The proof counts the actual temporary REF copies in r, while physical metadata, addresses and serialized objects are charged separately.

Split the fully specified deterministic instruction sequence at its exactly n READ operations. At each public program counter, the cache key set and stack length are fixed before seeing the source input assignment. Breadth-first state enumeration therefore produces at most 2^W distinguishable Boolean tuples per input layer, and at most n 2^W internal labelled OBDD nodes. Both 0- and 1-labelled arcs are retained even when they converge to the same successor. Accepted path counts, not only distinct endpoint nodes, equal the exact number of accepted **original** assignments. This is an upper compiler theorem, not a universal circuit or SAT-machine necessity theorem.

The actual source-validity and core-width checks are performed before emitting a claimed answer. Source-invalid words reject. Source-valid words whose H has more than two distinct predecessors at a target return **OUTSIDE**, not UNSAT. The executed reference parser accepts a documented canonical sorted-key ASCII-JSON **subset** of the full source model, so the finite parser evidence does not independently certify every original TMR-4/062 source encoding.

## Same-realization resource ledger

Let M=n+g, A=n2^W, and D=1+L+O(M^2 log(M+2)+A(W+n+log(A+2))). The complete source validation, DFS, cycle detection, operand-frequency and distinct-consumer accounting, two levels of component/label construction, topological scheduling, all failed validity checks, genuine READ/GATE/REF/STORE/DROP, cache and temporary state, OBDD state discovery/deduplication, both branch labels, exact n+1-bit counters, and output belong to one conventional locally headed sequential multitape implementation. The conservative inherited upper budget is

    T_total=O(D^5+n^2),    S_peak=O(D)

for the **same execution**. W is logical retained Boolean state, not physical peak working space. When z=O(log L), D and both upper bounds are polynomial in L. No random-access, formula unfolding, oracle, network span or parallel memory discount is assumed. Arbitrary alternative algorithms and semantic simplifications remain legal.

## Independent executed evidence

CPython 3.13.5, deterministic seed **20261117**, revision \`tmr5-reconvergent-070-v1\`; full source SHA-256 \`3792179017f9f0684b5fabbbd578e5288be96a2107cb0b14b1f28dddb6406ce9\`. The compact published loader includes an exact SHA-checked standard-library compressed payload. Its payload's base64 rolling-131 checksum was independently checked after GitHub readback. Local original and portable loader executions produced identical output.

513 constructed source cases: 191 authentic in-class PASS, 129 authentic OUTSIDE due to high core in-degree, 193 rejected invalid source instances; six further malformed-input rejections. The 191 PASS sources received 66,846 individual original-assignment pointwise comparisons against actual gate-by-gate evaluation, including a 16-original-input balanced binary shared core with a genuine reconvergent cross-edge. The independently built OBDD exact-count algorithm also agreed on every PASS. Total branch arcs 1,404; actual REF occurrences 1,349; maximum certified Q=48, z=3, W=10. Repeated operands, diamonds, noncommutative operations, cancellation, constant outputs and distinct versus coincident labelled arcs were tested. **Zero assertion failures.** The raw JSON is at \`results/raw/tmr/2026-11-17_TMR5_RECONVERGENT070_PY_RAW.json\`, blob \`f52fcbbd0c01ceb766beeb95475de808fd1c2f04\`, identical to local raw bytes. Finite replay is not an asymptotic proof or physical TM microtrace.

## Four promotion gates and controls

| Gate | Status |
|---|---|
| DISJ | PASS scoped: an upper construction creates no rank-to-unrestricted-work lower bound; DISJ's cheap equivalent remains legal |
| Relativization | PASS for the elementary source compiler; unrestricted NP bridge OPEN with BGS/algebrization/Natural Proofs safeguards |
| Simultaneous DTISP | PASS for one restricted deterministic **upper** T/S ledger; FLMV forbidden pair and arbitrary-machine necessity OPEN |
| Deterministic configuration counting | PASS as halting-run upper-bound guard T<=2^{O(S+log L)}, not a work lower bound or quantum/randomized statement |

Horn, 2-SAT, affine/Gaussian, treewidth, equality, autarkies, product, padding/auxiliary/selector, unique-solution rank-one, field and local-basis effects, counting-normalization, randomized isolation, and compact caching/recomputation are all admitted. Historical /341 remains FAIL as full logical UNSAT authority; /386 remains RESTRICTED.

## Cross-track ranking and next load-bearing dependency

1. **TMR-1** source-count and hierarchy: fresh independent pinned Lean/Mathlib/axioms/nanoda kernel, FinTM2 semantics and precisely scoped E^NP consequence remain OPEN or CONDITIONAL.
2. **TMR-4** source-to-OBDD-to-count: this run independently integrates a source-recognizable sparse-reconvergent binary-core **sufficient** class; the full all-encoding parser integration and unrestricted equivalent-circuit necessity remain OPEN.
3. **TMR-3** actual checkpoint provider and improved evaluator: restricted models have passed, generic adaptive provider-plus-nonassociative evaluator OPEN.
4. **TMR-2** genuine shared-source algebra/count: restricted exact count PASS, representation-independent dynamic necessity OPEN.

**ONE next priority:** independent pinned Lean 4.33.1 theorem build, transitive axiom and nanoda verification, followed separately by the fixed finite-stack-to-ordinary-machine semantic and hierarchy audit. Send this compiler extension to TMR-4 for owner integration; no peer manuscript is modified.

## References

1. TMR-4, \`main4_PNP_COST_SOUND_ABSTRACTION.tex\`, main blob \`a7d2c51b4ef20f008a85349c952915a51236e64f\`.
2. \`PNP_Hostage_Review_and_Agent_Restart_2026-11-17.md\`, Appendix D.
3. R. Sethi and J. D. Ullman, *The Generation of Optimal Code for Arithmetic Expressions*, JACM 17(4) (1970), DOI 10.1145/321607.321620.
4. R. E. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Transactions on Computers C-35(8) (1986), DOI 10.1109/TC.1986.1676819.
