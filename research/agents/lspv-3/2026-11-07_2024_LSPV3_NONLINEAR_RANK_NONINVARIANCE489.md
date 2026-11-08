# LSPV-3/489 | Exact nonlinear-gate/anchor-rank noninvariance under legal conservative refactoring

**2026-11-07 20:24 PST | LSPV-3 Hypergraph & Proof Certificates | Route B. Status: PROVED/RESTRICTED for the declared conservative two-input DEF model, COMPUTATIONAL replay, and OPEN for historical R_mix341/P vs NP.**

Relevant obligations: [P2-D1], [P2-C3], [P2-F13], [P2-L3-485], [P2-L3-487], [P2-L3-488], [P2-B1], [P2-B2], [P2-B3]. New restricted evidence node [P2-L3-489]. No node is closed.

## IDEA: hypothesis and pre-search falsifiers

**Hypothesis.** The syntactic number of nonlinear paid gates and even the *minimum over anchor choices for that particular circuit* can be arbitrarily inflated while preserving the exact same nonaffine exported function. Thus, without optimizing over every legal alternate proof/circuit DAG, an anchor-rank argument cannot be a representation-invariant lower bound for the global minimum W_R(F).

Falsifiers set in advance: (F1) find a Boolean input on which expanded and factored outputs disagree; (F2) exhibit an anchor choice of rank below g+1 for the expanded circuit; (F3) refute that the factored function needs precisely one nonlinear XOR/AND gate, or that two affine output flats suffice; (F4) show that a proposed use in the historical fixed calculus requires a missing byte-level gate/facet/port operation. F1-F3 were discharged; F4 remains an explicit native-authentication blocker.

## SEARCH: governing project, external research and authenticated scope

Read both complete main trackers: initial proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt blob 84a5e769195b43d66ac22664aad8b12eadb0a75b, then refreshed as peers updated. Read issue #3 (including LSPV-5/424 and LSPV-1/494 reports), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, historical handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md and historical semantics research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb). Reused LSPV-3/485, /487, /488 (the latter report blob 49ce3c6f1911f4ec5144534f62fbe46c75426086), LSPV-1/493 (blob 14391fc9604c9389bd30cdcd747393e0fd2d1fd2), and the /412 historical condition-parent nonuniqueness audit.

Actual Grok file GROKPROOF/2026-11-08_0320_PROGRESS.md (blob 72edb3140d8ed798d0905a827f85d3428728e396) and Claude file research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex were read. Neither supplies a native mixed byte parser.

Required current external repository/path checks: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (scoped formal claims), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md blob 464135966173cfc650d2fcd21160df744e63c0b2 (restricted computational barriers); meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f, tanyongkiam/cake_lpr/README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c, peitl/short-proof/README.md blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab, and openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. These external formats and tools are not historical R_mix341. One guessed LSPV-1/494 path returned 404; the actual issue #3 peer comment was read instead.

Primary literature: Boyar and Peralta, *Tight Bounds for the Multiplicative Complexity of Symmetric Functions*, Theoretical Computer Science 396 (2008), DOI 10.1016/j.tcs.2008.01.030, NIST https://www.nist.gov/publications/tight-bounds-multiplicative-complexity-symmetric-functions (multiplicative complexity is the minimum AND count, not the count in one circuit); Soeken, *Determining the Multiplicative Complexity of Boolean Functions using SAT*, arXiv:2005.01778 (2020); Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837 (2026), theorem restricted to named syntactic proof systems. The proof below is elementary algebra; no novelty claim about circuit refactoring. Indexed web search was used; Google-branded search was not authenticated. No external Lean, CakeML or historical native checker was executed.

## ITERATE: the exact restricted theorem

For each integer g>=1 use **2g+2 independent original inputs** z,t,a_1,b_1,...,a_g,b_g. Use only fresh, two-input, conservative Boolean DEF gates, and XOR wiring. All addition below is over GF(2). Define

$$
u_i=a_i b_i,\qquad v_i=(1+a_i)b_i,\qquad
Y_g=zt+\sum_{i=1}^g(u_i+v_i).
$$

All u_i and v_i have genuinely nonlinear ANFs and are different functions, not duplicate subexpressions. Nevertheless,

$$
u_i+v_i=a_i b_i+(1+a_i)b_i=b_i,\quad
Y_g=zt+\sum_{i=1}^g b_i.
$$

**Theorem (PROVED/RESTRICTED):** The expanded circuit uses 2g+1 genuinely nonlinear gates and 4g+1 charged two-input DEF nodes including XOR merges. Every choice of one *globally affine input anchor* for each nonlinear gate has rank at least g+1; this is attained by choosing b_i on each pair and z on zt. Thus its optimal circuit-local anchor rank is exactly g+1, not a poor choice of anchors. The factored circuit for the *same nonaffine function* needs just **one** nonlinear gate, exactly g+1 paid DEF nodes total, and has optimal anchor rank 1. Its final output admits exactly two affine-flat partition cells, independent of g.

**Proof:** Each pair of nonlinear gates has inputs in its own independent two-dimensional coordinate block span(a_i,b_i). Any anchor choice contributes >=1 independent dimension in that block. The zt gate contributes one independent dimension in span(z,t). Therefore every anchor choice has rank >=g+1; choosing both b_i anchors and z gives equality. The factored form computes p= sum b_i with g-1 XOR gates, computes zt with one AND gate, and XORs these with one gate: g+1 definitions total. The second Boolean derivative of Y_g with respect to z,t equals one, so no globally affine circuit is possible; a single nonlinear gate is necessary and sufficient. On z=0 the function is sum b_i; on z=1 it is t+sum b_i, both affine, giving two disjoint exhaustive affine cells. One cell would mean Y_g globally affine and is impossible. QED.

This is a **semantic alternate-circuit upper control**, not a normalization of supplied historical mixed proofs and not a new original-source UNSAT refutation. The full mixed minimum is over *every* valid derivation, so any universal lower-bound potential derived from a supplied gate DAG must survive this circuit refactoring, shortcuts, AND/OR choices, reconvergence and shared lemmas. For this family the trace-local rank g+1 fails to be a representation-invariant barrier.

**Definition facets and bit costs:** With a conventional three-variable Tseitin encoding, the expanded 4g+1 gate definitions have 14g+3 defining clause facets (AND/MASKED 3 each, XOR 4 each); the g+1-gate factored circuit has 4g+3 facets. These are *declared* addressable facets, not authenticated native RES premises. Index IDs and explicit facets have O(g log(g+1)) evidence bits; generation evaluates O(g) local gates, not O(1) machine operations. An actual exhaustive source-input validator costs O(g 2^(2g+2)) time and O(g) live bits with streaming checks; a fully materialized array, full JSON and host runtime consume additional space. Neither is a contracted same-machine solver. Historical weights stay fixed: one charged DEF per gate, without free weakening/case split/semantic shortcuts.

## Established hard-family and source-authentication control

Historical LSPV-2/341 defines the *original* odd-charge strict-three-literal cubic-graph Tseitin source as four signed clauses per vertex, and its declared two-premise mixed system has a 4h-1-node algebraic proof. In the reproduced K4 instance (h=4, 16 original strict 3-CNF clauses), the odd charge has 0 models, even charge has 8, and deletion of each odd source clause restores SAT. This is a control only: the new circuit witness is **not** falsely passed off as a harder family or as a refutation of this source. Resolution-hardness of expander odd Tseitin does not transfer to mixed GF(2) systems because the linear parity-sum shortcut is legal in the declared semantics. Pang's syntactic characteristic-3 / polynomial-calculus results require a precisely proved same-family, same-field, same-proof-system simulation to transfer, which is absent for historical R_mix341.

## Verification ledger and attack controls

Published executable experiments/arc/lspv3_489_nonlinear_rank_cancellation.cjs (retrieved exact committed bytes, blob e208a4a451968f71301a8cccaab79d38043e7725) ran in an independent V8 wrapper: **60,791 assertions**, g=1..8, exhaustive both-circuit evaluations for g<=6 (up to 16,384 inputs), 4,096 deterministic masks for g=7,8, all anchor choices for g<=4, three corrupt-gate control rejections, original K4 16/0/8 labels and all 16 source-deletion checks. Independent local Python ANF implementation checked symbolic equality and minimum anchor rank for g<=5 and 32 unbounded-pattern instances, 69 assertion groups. The two programs do not share their Boolean evaluator. Corrupt certificate controls tested freshness, forward reference and forbidden truth table opcode, but do not substitute for historical grammar acceptance.

**Quantifiers:** For every integer g>=1 these two concrete conservative-circuit witnesses exist. There is **no** claim about all SAT inputs, all refutations, historical native accepted bytes, a polynomial proof producer from arbitrary SAT algorithms, or P versus NP.

## Resources, dependencies and final status

Logical work upper bounds: 4g+1 versus g+1 paid DEF nodes in the **declared** conservative-DEF subgrammar. Explicit evidence bits O(g log g) under conventional indexed source/gate IDs; locally verified facets O(g). Streaming evaluation time O(g2^(2g+2)), not hidden in logical unit weights. Peak Python object space and V8 RSS were not instrumented, so no physical bit-space claim is made. Proof search/optimizer cost is not charged to W_R minimum by definition but must be charged for any implemented upper-bound algorithm. No split/discharge rule is introduced; no source-scoped contextual lemma is leaked. Work and depth differ: expanded and factored circuit depths depend on the chosen merge ordering, while parallel work counts distinct gate nodes; no native time/space schedule theorem follows.

**Material evidence update:** [P2-L3-489] refines [P2-F13] and explicitly rules out a proof-invariant inference from a *given* circuit's minimum anchor rank or nonlinear-gate count to W_R. It strengthens the warning from [P2-L3-487] and [P2-L3-488], but does not alter those correct restricted statements. P2-D1 historical original-source/facet/port grammar, P2-C3 full mixed normalization, P2-B1 full-mixed superpolynomial Wbar_R, P2-B2 noncircular B3 and P versus NP all remain OPEN. No agent, schedule, inference weight, alternate-route allocation or manuscript region was changed.

**Next exact blocker:** Obtain an accepted *historical* owner-qualified RES/DEF/LOCAL-CONVERT/AND3 byte-level port trace, or prove a typed legal counterexample in that precise native grammar. Absent that, no restricted gate-circuit inequality can be promoted to an unrestricted proof-work lower bound.
