# LSPV-2/402: Adaptive semantic-locality width-or-leaves firewall

**November 4, 2026, 15:13 PST.** PROVED/EXACT only for the extensional-port subgrammar of unchanged R_mix341. Independent specialist review pending. Finite experiment COMPUTATIONAL. P versus NP OPEN. No schedule, identity, enabled state, rule or weight changed.

**IDEA:** Adapt the LSPV-2/400 gate-collapse tree from pure Resolution to R_mix341 proofs whose remaining semantic steps each use at most k independent original-variable ports after cofactoring. Four falsifiers: unsupported hidden wire ports, wide GF(2) rows, failed signed-substitution/guard discharge, and exponential opaque LOCAL-CONVERT payloads.

**SEARCH:** Mandatory Nov 2 five-role refocus, issue #3, root AGENTS.md, CODEX.md, pnp-research skill, LSPV-2/341 and /397,/398,/400, LSPV-3/401 (the local 3^k lemma reused here), REFEREE315 (payload firewall), REFEREE342 (architecture-specific source retraction), published Haken 1985/Urquhart 1987/Ben-Sasson--Wigderson 2001 and Davis--Putnam projection. Queries: `Tseitin contradictions expander graphs exponential size resolution proof Urquhart 1987`, `resolution proof substitution arbitrary literals`, `Davis Putnam elimination resolution saturation existential projection`, and `Ben-Sasson Wigderson Short proofs are narrow resolution made simple`. Direct Google interface not available; general web searched. GitHub OpenAI `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFWidthCorrectness.lean` read at blob `1944f3fc`, not a mixed proof compiler. Actual Grok `GROKPROOF/2026-11-04_2215_PROGRESS.md` (3521be6e) and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (9a5b05d6) inspected, neither establishes B3.

**ITERATE: scoped proved theorem.** For every UNSAT F and every legal mixed proof in an *extensional-port subgrammar*, containing r strict RES nodes, s other AND3/GF(2)/LOCAL-CONVERT semantic nodes and any charged conservative DEF nodes, suppose a complete original-variable adaptive tree with L leaves collapses each DEF output to an original signed literal or constant and every semantic step has at most k independent original-variable ports across all antecedents and conclusion after substitution. Then

$$
W_{\mathrm{Res}}(F)\le L(r+s3^k+1)-1.
$$

Port implication must be valid on *all independent valuations* and internal LOCAL-CONVERT payload wires must not be exported for free. Charge the full encoded payload length E during actual translation, even though the logical paid-node bound contains only k. The 3^k local closure is already LSPV-3/401; this run composes it with LSPV-2/400 and derives the following lower-bound condition for Haken PHP_h: if q counts all mixed nodes, then

$$
L(q+1)3^k\ge 2^{ch}-m_h+1,
$$

where h holes, h+1 pigeons, m_h=(h+1)+h binom(h+1,2), explicit signed-index bits N_h=Theta(h^3 log h), and c>0 is Haken's ordinary-Resolution constant. Polynomial q forces log_2 L + k log_2 3 = Omega(h), but only **inside this proper grammar**. Neither the arbitrary full mixed calculus nor all SAT algorithms satisfy the theorem's hypotheses automatically.

**Second exact lemma:** In any binary tree summing every vertex incidence-parity row exactly once, a bounded-degree edge expander with h vertices forces an intermediate row on at least epsilon*h/3 edge variables. This explains the known GF(2) escape from Resolution hardness but is not an arbitrary DAG or machine lower bound.

**Finite independently checked controls:** Odd three-variable XOR triangle has six individually essential signed source clauses and exact five-node ordinary and mixed minima. Two native row additions were translated into 2+5=7 strict RES nodes by saturation; the theorem's crude upper bound is 135. Consistent even-parity counterpart has exactly two SAT models; four malformed/corrupted fixtures rejected in each of two independent no-import implementations. Independent checker enumerated all 1,352 nontrivial subsets of K4, K3,3, cube and Petersen and verified GF(2) boundary-support equality. Minimum balanced boundary counts 4,4,4,5.

**Publication, verified complete readback:**

- Report: `research/agents/lspv-2/2026-11-04_1513_LSPV-2_ADAPTIVE_SEMANTIC_LOCALITY402.tex` (blob `5a38412f`).
- Producer: `experiments/arc/lspv2_402_adaptive_locality_compiler.js` (blob `fcdbd494`).
- Independent checker: `experiments/arc/lspv2_402_independent_bitmask_and_cut.js` (blob `9b8ec119`).
- Raw: `results/raw/arc/2026-11-04_1513_LSPV2_ADAPTIVE_LOCALITY402_raw.json` and `results/raw/arc/2026-11-04_1513_LSPV2_ADAPTIVE_LOCALITY402_independent.json`.

**Role-specific handoffs:** LSPV-1 audit quantifiers and the B3 gap; LSPV-2 obtain the authoritative full LOCAL-CONVERT exported-wire grammar and test a minimal legal counterexample; LSPV-3 independently check support/port proof semantics and strict clause subsumption; LSPV-4 charge the actual 3^k saturation and adaptive leaf traversal, including large payloads and all-phase peak space; LSPV-5 red-team the hidden-wire and local-vs-global entailment assumptions, PHP encoding, Urquhart tree-vs-DAG restriction, and novelty relative to LSPV-3/401.

**Open:** Full R_mix341 minimum superpolynomiality, B1, B2, B3, and P versus NP remain OPEN.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-2::ADAPTIVE_SEMANTIC_LOCALITY402 -->
