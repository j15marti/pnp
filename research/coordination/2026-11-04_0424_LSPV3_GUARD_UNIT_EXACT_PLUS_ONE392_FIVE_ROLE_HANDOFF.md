# LSPV-3/392: One exact paid guard-unit step in strict Extended Resolution

**November 4, 2026, 04:24 PST.** No change to original R_mix341, five roles, hourly schedules, identities, weights, or verified prior results. **P versus NP OPEN.**

## New theorem and precise dependence

Previous LSPV-2/381 (blob \`671d56bfb6448ee6867b053169967e4e2bdb01b6\`) proved a cost-preserving guarded-unit transport for the fixed strict paid signed-AND2/Resolution subcalculus E_AND2, allowing **guard-dependent** conservative gate definitions:

$$
D_E(F\vdash\bot)=D_E(G_t(F)\vdash\neg t), \qquad
G_t(F)=\bigwedge_{C\in F}(\neg t\lor C).
$$

This run strengthens that result to the **complete guarded refutation** including the unit source t, with exact additive rather than merely polynomial proof-cost accounting:

$$
\boxed{\forall F\in\mathrm{UNSAT}:\quad
D_E(G_t(F)\land t\vdash\bot)=D_E(F\vdash\bot)+1.}
$$

Upper: use the /381 guard-preserving lift and one strict Resolution step with t. Lower: every sound proof must use the authenticated source t, because G_t(F) is SAT at t=0 and all signed-AND2 definitions are conservative. In strict E_AND2, the first Resolution step consuming source (t) pivots on t. Under the /381 guard-dependent topological cofactor normalizer at t=1, that specific paid inference is redundant: its opposite parent already gives the needed restricted subclause. All other surviving DEF/RES nodes cost no more than originally, hence the transformed original refutation has at most q-1 paid steps. This applies to every legal shared DAG and any adaptive order, including gate definitions mentioning t. The theorem is about E_AND2, **not yet full R_mix341**.

Independently, for the minimally UNSAT Horn chain

$$
F_h=(x_1)\wedge\bigwedge_{i=1}^h(\neg x_i\vee x_{i+1})\wedge(\neg x_{h+1}),
$$

all original sources and the guarded source plus t are individually essential. The previously established at-most-binary-premise source-ancestry lower bound, plus matching strict Resolution proofs, yields **global exact optima in the full unchanged R_mix341** for all h >= 1:

$$
\boxed{W_{R_{\rm mix341}}(F_h)=h+1,\qquad
W_{R_{\rm mix341}}(G_t(F_h)\land t)=h+2.}
$$

This is a **linear calibration** only, not a superpolynomial lower bound, not a shortest-proof optimizer extrapolation, and not a machine-time bound.

## Verification and hostile controls

The producer independently reconstructs source-labelled signed Resolution DAGs for h = 2,3,4,6,8,12,24,64, all deletion and sign-flip SAT neighbors, t=0 controls, 16 guard-dependent AND2 cofactor valuations, and three deliberately corrupted proofs. **1,291 checks; three corruptions rejected.** Separate JavaScript verifier exhaustively enumerated all assignments of both original and guarded sources for h = 1,...,7, checked every single-source deletion, replayed both derivations and rejected an invalid pivot: **133 checks; one corruption rejected**. These tests certify specific finite upper constructions and controls; the all-size mixed minima are established by the mathematical lower/upper proof, not finite enumeration.

Published role-owned artifacts:
- \`research/agents/lspv-3/2026-11-04_0424_LSPV-3_GUARD_UNIT_EXACT_PLUS_ONE392.tex\`
- \`experiments/arc/lspv3_392_guarded_er_exact_plus_one.js\`
- \`experiments/arc/lspv3_392_independent_chain_checker.js\`
- \`results/raw/arc/2026-11-04_0424_LSPV3_GUARD_ER_EXACT_PLUS_ONE392_raw.json\`

All new files were committed and read back character-for-character. Root \`main.tex\` is handled separately under LSPV-3 owner-only authorization; no incomplete rewrite is allowed.

## Starting theorem, corpus, duplication, and independent reviews

Haken 1985: for standard unary PHP(h+1,h), with h(h+1) variables, (h+1)+h*C(h+1,2) signed clauses and explicit fixed-index input N(h)=Theta(h^3 log(h+2)) bits, there are c>0,h0 so **for every** h>=h0 and **every ordinary shared-DAG Resolution** refutation, length >=2^(ch). Cook 1976 gives polynomial Extended Resolution PHP proofs. Neither is an all-algorithm SAT lower bound or a lower bound on mixed R.

Read the approved November 2 12:04 focus at commit 4e29ed7, issue #3, AGENTS.md, CODEX.md, pnp-research skill, original LSPV-2/341 (blob c87acd11), LSPV-2/381 (blob 671d56bf), LSPV-3/385 and /391, LSPV-4/379. Searched Haken, Cook, guarded Extended Resolution, resolution restriction/substitution, and project guard reports. Duplication check: /381 already proved guarded-unit exact equality; **the new result is the unavoidable +1 paid cost after adding the guard unit t to form a refutation**. No novelty claim for classical restrictions is made.

Actual folders inspected: \`GROKPROOF/2026-11-04_1217_PROGRESS.md\` (blob cae0560d), and \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\` (blob 1f9fc727). Grok's fully charged all-input circuit-cut/FLMV selector is unproved, and its asserted necessary cut width depends on enumeration assumptions; Claude's alternation-trading portfolio analysis concerns a restricted model. Neither implies B3.

## Next tests for all five active roles

LSPV-1: audit B1/B2/B3 quantifiers and what extra paid step says about only E_AND2. LSPV-2: implement exact guard cofactors for each original R_mix341 AND3/XOR/LOCAL-CONVERT rule or exhibit a legal shortest counterexample. LSPV-3: test authenticated local circuit payload and signed-source DAG provenance under such cofactors. LSPV-4: charge every source/index read, topological gate simplification, verification, output and all-phase peak space, including implicit/lazy alternatives. LSPV-5: attack the first paid-use argument with arbitrary guard-dependent conservative extensions and adversarial sharing.

The uniform physical bound for explicitly encoded certificates of lengths N,L is polynomial, not unit cost; conservatively O((N+L)^2) bit-time and writable peak-space for the inherited translator. Exponential intermediate payloads must be paid; proof search and verification are separate.

**Remaining open:** superpolynomial \`Wbar_Rmix341(N)\`, B1, B2, B3 and P != NP. No administrative automation changes.
