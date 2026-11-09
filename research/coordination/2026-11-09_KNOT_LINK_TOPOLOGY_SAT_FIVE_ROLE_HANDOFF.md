# User-requested five-role handoff: knot/link topology and SAT proof complexity
Date: 2026-11-09 America/Los_Angeles (PST).
Status: CANDIDATE RESEARCH DIRECTION; P = NP and P != NP OPEN.

## Purpose and scope
The user requests that all five existing PNP agents investigate whether topology of knots and multi-component links can help construct an **all-rule, shared-DAG robust obstruction** for the project, particularly Route B ([P2-D1], [P2-C3], [P2-B1], [P2-B2]), while evaluating any genuine same-machine link to Route A ([P2-A2], [P2-A4], [P2-A5]). This is an additive idea-sharing directive, NOT an agent-role, schedule, resource-model, inference-rule, or proof-status change. Retain exactly five agents and the existing TWO Route A / THREE Route B division. Keep both proof-chain trackers and `main.tex` unchanged unless subsequent new results independently justify a scoped update.

## Verified topology literature to check at source
1. D. Koenig and A. Tsvietkova, "NP-hard problems naturally arising in knot theory," Trans. Amer. Math. Soc. Ser. B 8 (2021), 420–441, https://doi.org/10.1090/btran/71 . Gives polynomial-time 3-SAT reductions to knot/link decision problems, including trivial/unlink sublink. Independently verify the precise link construction and all quantifiers, component and crossing counts, and whether its clause gadget actually uses Brunnian/Borromean structure. A Boolean assignment corresponds to a choice of components; DO NOT confuse SAT-witness sublink selection with an UNSAT refutation or a bounded Reidemeister sequence.
2. S. Cheng, A. Chlopecki, S. Nazar, and E. Samperton, "An elementary proof that linking problems are hard" (2025), https://arxiv.org/abs/2509.13120 . Alternative reduction from INDEPENDENT SET to TRIVIAL SUBLINK using only mod-2 *pairwise* linking. It explicitly avoids Brunnian links. This is a high-priority counterexample to claims that higher-order Milnor invariants are necessary to encode hardness.
3. A. de Mesmay, J. Purcell, S. Schleimer, E. Sedgwick, "On the tree-width of knot diagrams," J. Comput. Geom. 10 (2019), 164–180, https://doi.org/10.20382/jocg.v10i1a6 . Gives knots whose diagrams all have high treewidth; nevertheless high diagram treewidth alone is not a general SAT decision-time lower bound.
4. M. Lackenby, "A polynomial upper bound on Reidemeister moves," Ann. Math. 182 (2015), 491–564, https://doi.org/10.4007/annals.2015.182.2.3 . Unknot diagram with c crossings admits <=(236c)^11 moves to trivial diagram; distinguished from the complexity of *finding* a sequence and recognizing a general SAT input. Also note Lackenby's 2026 fixed-link-type polynomial result https://arxiv.org/abs/2602.09923 and verify hypotheses before using.
5. F. Jaeger, D. Vertigan, and D. Welsh, "On the computational complexity of the Jones and Tutte polynomials," Math. Proc. Cambridge Philos. Soc. 108 (1990), 35–53, https://doi.org/10.1017/S0305004100068936 . Computing Jones polynomial of alternating links is #P-hard. The exponential Kauffman-state expansion is an *upper construction*, NOT a worst-case bound on every algorithm.
6. A. de Mesmay, Y. Rieck, E. Sedgwick, M. Tancer, "The unbearable hardness of unknotting," Adv. Math. 381 (2021), 107648, https://doi.org/10.1016/j.aim.2021.107648 . Length-bounded Reidemeister simplification is NP-hard; carefully distinguish minimum-move optimization from feasibility and machine lower bounds.

## Proposed conceptual correspondence (ANALOGY, not theorem)
- Hopf pair: binary dependency or opposing literal choice.
- Brunnian/Borromean multi-link: genuine three-way interaction invisible to ordinary pairwise linking; Milnor triple linking can detect it while pairwise linking numbers vanish.
- Higher-order Milnor invariants or link complement topology: candidate higher-order dependency measures.
- Ambient isotopy/Reidemeister moves: topology-preserving presentation changes, **NOT** inherently the same thing as RES, AND3, GF(2), LOCAL-CONVERT, DEF, context discharge, or general computation.
- Crossing-state/Kauffman expansion: branching and possible DAG reuse, but no proven lower bound from the number of naive states.
- Satisfiable assignment selecting a trivial sublink: positive witness; nonexistence of trivial sublinks is a separate negative claim requiring a proof.

## Three proposed experiments
### A. Exact 3-SAT -> link compiler and paired controls
Implement or precisely restate a published reduction (Koenig–Tsvietkova, with explicit crossing/component bit complexity and SAT iff link property), then independently verify *small original signed 3-CNF* SAT and UNSAT instances. Compare a Brunnian-style construction with the mod-2-only alternative, noting they start from different NP-hard problems and need not be gadget-equivalent. Use ordinary-CNF gadgets only if the exact reduction accepts them. Hard controls: odd-charge 3-regular expander Tseitin (ordinary DAG Resolution-hard **but GF(2)-easy**), 2026 project modulo-3 one-hot sources (GF(2) affine hull may be trivial **but F_3 shortcuts possible**), and published random strict3 sources where feasible. Easy controls: 2-SAT, Horn, affine/XOR, bounded treewidth, padding, renaming, extension variables, direct products.

### B. Representation invariance versus proof-rule shortcuts
For each candidate invariant I of L(F) (linking numbers, Milnor numbers, Jones/Alexander coefficients, diagram treewidth, complement homology, geometric width), specify:
- actual object and algorithmic input encoding; invariant under exactly what class of moves;
- whether cheap calculation or a compact bypass exists;
- how one ORIGINAL-SOURCE-authenticated legal inference in fixed R_mix341 acts on F, its link encoding and invariant;
- whether sharing/reconvergence, arbitrary branching and assumption discharge, GF(2) and other fields, LOCAL-CONVERT, paid definitions/extension gates can defeat it;
- whether invariance survives re-encoding with auxiliary variables (which changes links).
Find the smallest explicit legal counterexample before attempting a bound. Existing project graph-topology edit results LSPV-2/449 concern graph connectivity, not knot topology; compare them, do not claim novelty from a shared word.

### C. A genuinely charged topological potential / lower-bound bridge
A possible goal **to be proved or falsified**, for one FIXED R, is
$$
\forall F\in\mathrm{UNSAT}\cap\mathrm{CNF}_3:\quad W_R(F)\ge g(I(L(F))),
$$
where W_R is the minimum number/weighted sum of *distinct paid nodes* of the globally cheapest complete legal source-authenticated branching/shared DAG, allowing extensions, all algebraic shortcuts and ideal free after-the-fact choice of derivation. To imply P != NP via Route B, show that g(I(L(F_n))) dominates every polynomial for an infinite explicit ORIGINAL hard family, **AND** independently prove noncircular B3: SAT in P => polynomial Wbar_R for the SAME R. Neither arrow currently exists.

Alternative local-potential form: define Phi on actual certified proof states and show *for every legal rule* (including extensions and sharing) its maximum paid-step progress is bounded; account for node fan-out, algebraic cancellation, certificate bit length and alternative representations. Reidemeister-invariance alone does not give per-RES cost: a legal proof step is not an ambient-isotopy move.

## Role-specific immediate targets
- **LSPV-1 (:00, Route B, formal lead)**: formalize both quantifier chains, seek an exact topological potential lemma for fully legal R_mix341, test against previous modulo-3/GF(2) affine-hull result [P2-L1-530], and give one counterexample or verified restricted theorem. Audit the B3 implication separately. Do not equate NP-hardness of topological decision with a superpolynomial refutation lower bound.
- **LSPV-2 (:12, Route A, reduction builder)**: recover the source-authenticated polynomial encoding and component selection semantics; write a small strict3 original-source compiler or formal gadget ledger; track true input length, crossing count, and decision-vs-search properties. Investigate any solver-independent contraction claims under [P2-A2], and explicitly falsify source-only shortcuts with the existing expander/Tseitin and FLMV controls.
- **LSPV-3 (:24, Route B, proof certificates)**: work through concrete link examples against accepted source clauses and OR/AND shared proof DAGs. Build an explicit move/derivation type table; refuse to assign any actual historical R_mix341 semantics without accepted-byte grammar. Check any topological certificate for provenance and illegal free rewrites; identify first unsupported rule.
- **LSPV-4 (:36, Route A, resources)**: charge full size/time/space of link construction, evaluation of proposed invariants, storage/recomputation of shared states, diagram normalizations, and any same-FLMV-machine compiler. Compare genuine topological width obstructions to *fully charged* ordinary SAT algorithms; include full-cost algebraic easy controls and hidden high-water work.
- **LSPV-5 (:48, Route B, independent red team)**: search older project and primary topology literature, including 2025 mod-2-only reduction; attack with trivial links, easy XOR/Tseitin, graph simplifications, changing presentation/auxiliaries, polynomial unknot simplification, and legal full-mixed short proofs. Provide the smallest explicit falsifier to any unproven universal claim and verify certificates independently.

## Output and promotion protocol
Each role may pursue ONE sharp subproblem per scheduled run, searching the source literature before novelty claims and reporting EXACT theorem statement, assumptions, quantifiers, counterexamples, scoped proof status, reproducible code/raw controls and any changed node IDs. Commit only genuinely new verified results to role-owned reports and (if material) the relevant proof tracker with readback/optimistic concurrency. Share handoffs to GitHub issue #3. Do not overwrite root main.tex or another role's region; follow AGENTS.md and repository skill. If no rigorous new claim, state "TRACKERS REVIEWED; NO MATERIAL CHANGE" in the role report.

This note is NOT itself a theorem, NOT a new accepted calculus, NOT a proof of P != NP, and NOT authorization to divert all agents from their existing Route A/B work. The first deliverable should be a literature-correct, falsification-first map of candidate invariants to real legal proof rules, not an unsupported asymptotic claim.
