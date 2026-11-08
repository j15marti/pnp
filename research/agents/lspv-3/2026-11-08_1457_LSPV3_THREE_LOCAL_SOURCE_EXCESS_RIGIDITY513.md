# LSPV-3/513 | A three-LOCAL exact minimum and source-excess rigidity for the existing bridge-star certificate

**2026-11-08 14:57 PST | Route B | PROVED/RESTRICTED mathematical specialization of LSPV-1/349; COMPUTATIONAL independent replay | P versus NP OPEN.**

**Tracker IDs:** new [P2-L3-513], refining [P2-L3-512], [P2-L1-349] (the prior project source-excess theorem; where not separately indexed, see its exact report), [P2-D2], [P2-D3], [P2-D1], [P2-C3]. [P2-B1], [P2-B2] remain OPEN. Route A and [P1-01]/[P1-03]/[P1-04] unchanged.

## IDEA: falsifiable hypothesis and four controls

**Hypothesis.** The newly constructed 57-node, three-unary-LOCAL, original-source-authenticated bridge-star proof in LSPV-3/512 is not merely a short upper bound. It attains the absolute minimum among *all sound, source-explicit, unit-weight, at-most-two-premise refutation DAGs of the same formula whose ancestry contains at least three unary inference nodes*. This conclusion must survive free optimal DAG choice, alternative branching/reconvergence, and arbitrary conservative auxiliaries without asserting the unrestricted full-mixed minimum.

**Falsifiers:** F1, one of the claimed 55 indispensable original clauses can be deleted while preserving UNSAT; F2, the 512 sink actually depends on fewer than 55 original clause IDs; F3, the proof has fewer than three unary nodes or different total paid inference/edge count; F4, the source-excess identity miscounts shared subproofs, zero-premise definitions, or inference arity. These four were checked and did not fire under the stated model. Deliberately corrupted source/inference records were separately rejected by the independent, nonauthoritative declared-semantic validator.

## SEARCH: actual predecessor, primary sources, external and peer code

**Historical source and immediate predecessors:** LSPV-2/341 original declaration at research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb; the recovered historical checker experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, accepts only AND3/XOR tags. LSPV-5/413 recovered and replayed this scope in research/main/2026-11-07_0901_MAIN_HISTORICAL_341_CHECKER_SCOPE_REFEREE413.md, blob a80ba04046046f7b2c71aa451547474bea62d269. LSPV-3/512 certificate and 55-essential-source theorem at research/agents/lspv-3/2026-11-08_1429_LSPV3_THREE_ARM_UNIQUE_CORE_LOCAL_RES_PORT512.md, blob 9dddd8c343ffe5d086fc6a5128ca4931969fcc4d, source SHA-256 dc62a4995250bb6922d31e711562fa7408e67968e097289fe8a5cb8c9c55dc20. Independently read LSPV-1/516 (observable-affine recognition barrier), LSPV-3/477 (historical restricted first-inference barrier), active issue #3, both complete root proof trackers, AGENTS.md, CODEX.md, the research skill, November 2 governing handoff, GROKPROOF/2026-11-06_2316_PROGRESS.md and Claude's 2026-10-28 world ledger.

**Crucial nonnovel precedent found:** LSPV-1/349 already proved the exact general source-ancestry Euler/excess identity, research/agents/lspv-1/2026-11-02_1804_LSPV-1_SOURCE_EXCESS_EULER349.tex, including its binary unit-premise corollary. This run is an **exact new application /512**, not a rediscovery of that identity or a claim of a new independent combinatorial theorem.

**Change-aware exact repository reads:** konard/p-vs-np scripts/proof_status.json blob 93b77ed3 and proofs/complexity/README.md 7ee9a11e (finite-machine P subset NP, no historical mixed port); blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea and REVIEW_ADDENDUM.md 6a7cc2f8 (scoped relaxation controls); meelgroup/frat-xor format.md 986a21aa (XLRUP is a different authenticated cross-theory syntax); tanyongkiam/cake_lpr README.md e94f45e9 (LPR checker, different grammar); peitl/short-proof README.md 93d2090d (ordinary Resolution optimum); openai/math README.md cc5b0a03 (raw manuscripts, not /341 authority). No changes in these pinned files that close P2-D1. The primary literature examined included Urquhart 1987 JACM 34:209-219, Cook–Reckhow 1979 JSL 44:36-50, and Ben-Sasson–Wigderson 2001 JACM 48:149-169. An indexed scholarly web search was run; no separately branded Google interface was used. The three-arm bridge fixture is **not claimed** to be a published hard expander; published cubic-expander odd Tseitin strict 3-CNF is only a distinct ordinary Resolution-hard control.

## ITERATE: exact conditional-inference-count theorem

Let F denote the *existing*, original signed strict three-CNF from LSPV-3/512: a central degree-three odd-charge vertex joined by three five-vertex subdivided-K4 blocks, total h=16 vertices, n=24 edge variables, m=64 source clauses. Let μ(F) be the size of a smallest UNSAT subset of the **literal signed original source clause records**. The /512 construction uses exactly the 55 individually essential clauses. Each of those 55 is indispensable in every UNSAT subset, and the 55-clause subset is UNSAT by the exhibited refutation. Therefore

$$
\boxed{\mu(F)=55.}
$$

**Theorem 513.1 (PROVED/RESTRICTED: three-unary exact minimum).** In every sound, conservative, original-source-authenticated, unit-paid refutation proof-DAG calculus with explicitly identified premises, at most two premises per charged node, and no uncharged higher-fan-in jump, write r for distinct source clauses in the pruned contradiction ancestry, q for distinct charged nodes, u for unary-premise nodes, d_0 for zero-premise nodes, and β for undirected cycle excess of the *distinct node* dependency graph. Then LSPV-1/349 gives exactly

$$
\boxed{q-(\mu(F)-1)=(r-\mu(F))+\beta+u+2d_0.}
$$

Because r≥55, β≥0 and d_0≥0, for **every valid proof with u≥3**,

$$
\boxed{q\ge54+3=57.}
$$

The existing /512 declared-semantic 57-node certificate has r=55, u=3, d_0=0, q=57, 54 binary-premise nodes and E=111 premise edges, so β=111-(55+57-1)=0. It attains the lower bound **within the u≥3 class**, while allowing any other legal proof strategy and shared-DAG topology that satisfies the arity, soundness and explicit-source requirements.

**Corollary 513.2 (near-minimum search obstruction).** Any authenticated 56-or-fewer-unit-node proof in any such calculus must have **at most two unary inference nodes**. In particular, the three-LOCAL bridge-unit strategy cannot be shortened by reconvergence, lemma reuse, or a different binary tree while retaining its three mandatory unary exports. To beat 57 one must change the inference mix (e.g. use ≤2 unary conversions, an alternative valid binary shortcut, or a conservative zero-premise definition); no forbidden rule is introduced by this statement. For q=57 and u≥3 equality forces r=55, u=3, d_0=0 and β=0: there is no residual source/proof-cycle/excess budget, even though a distinct alternative proof could exist with fewer unary nodes.

**Proof.** In a pruned dependency DAG with r original-source vertices and q charged vertices, the underlying undirected graph is connected and has E=∑ indegree(v) edges. Therefore β=E-(r+q-1)≥0, and since every used-source set must itself be UNSAT, r≥μ. With q=q_0+q_1+q_2 and E=q_1+2q_2, rearranging E=r+q-1+β gives q=(r-1)+β+q_1+2q_0. Substitute μ=55. The explicitly listed /512 node and edge counts achieve equality. DAG sharing is counted by distinct nodes and edges, not copied unfolding. No proof discovery cost is part of this lower-bound relaxation. QED.

## Independent source and proof checks; resource ledger

An **independently written Python source/typed-proof auditor** in the conversation artifact reconstructed every original signed 3-CNF clause in the specified order and verified its complete DIMACS SHA-256. A GF(2) elimination calculation for all 64 one-clause deletions found exactly **55 SAT deletions and 9 nonessential clauses**. It reconstructed the 57 paid AND3/XOR/LOCAL/RES nodes, checked every bounded-support factor and exact parity annotation, each local implication and each correctly oriented Resolution step, and verified the 55-source sink ancestry, 111 directed premise edges, β=0, depth 9. Twelve deliberately corrupted source/certificate controls were rejected: source/hash tampering, parent alias/missing/backedge, support overflow, bad XOR row, nonconsequence LOCAL, bad RES pivot/output, omitted AND premise and required-source substitution.

A **separately written compact Python topology/GF(2) reproducer** (published below) passed the same original-source hash, all 64 deletion controls, q/u/binary/edge/β counts, and exact source-set equality. This compact replay verifies **only source arithmetic and topology**, not every typed inference. Neither executable is the unavailable historical complete mixed checker.

Source is 740 ASCII DIMACS bytes. The full constructed certificate serialized as compact JSON is 4,329 bytes in the independent local producer. Exact proof logical work is 57 unit-paid nodes, with separately recorded weighted critical-path depth 9 in the unlimited-processor dependency model. The executed independent Python measured ~0.132 seconds wall time and ~380,697 bytes Python-tracemalloc peak (host/runtime overhead not included); these are **finite-host measurements**, not all-phase same-machine asymptotic bounds. The compact verifier separately charges source parsing, 64 Gaussian checks, explicit proof construction, ancestor traversal, JSON output, and negative-control replay; GitHub head reads/publication are not included in logical W_R and are not claimed free in a realizable upper-bound machine implementation. No input-size-uniform computation theorem follows.

## Publication, fixed-grammar limitation, and next exact gap

The new result is **rigidity of a particular three-LOCAL normal form** and a necessary search constraint for a cheaper full-mixed refutation. It does **not** prove W_R(F)=57 across all historical legal rules, nor show any accepted byte trace containing LOCAL or RES. The independent checker explicitly permits the previously declared semantic interpretation of row-to-AND3 conditions and treats original SOURCE clauses as clauses in RES and as bounded-support factors in AND3; neither permission authenticates the incomplete historical byte grammar. The only recovered historical verifier still recognizes the AND3/XOR sublanguage; a full historical accepted-byte RES/DEF/LOCAL/port/assumption-discharge grammar remains missing.

**OPEN:** P2-D1 (native complete historical syntax), P2-C3 (mixed all-rule transfer), P2-B1 (superpolynomial full-system minimum), P2-B2 (same-system noncircular B3). Root main.tex returned zero readable bytes and was not edited. All five roles, titles, schedules, weights, enabled states and two Route A / three Route B allocation are unchanged. P versus NP OPEN.

References: [1] LSPV-1/349, exact predecessor path above. [2] Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), DOI 10.1145/7531.8928. [3] Ben-Sasson & Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), DOI 10.1145/375827.375835. [4] Cook & Reckhow, *Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702.
