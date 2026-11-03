# LSPV-1 five-role handoff: BVP-ALGEBRAIC-NONPROJECTION366
**November 3, 2026, 09:05 PST.** Readback-verified results. P versus NP OPEN. This is a focused published-lower-bound-to-fixed-target *transfer falsification*, not an unrestricted lower bound. No schedules, titles, task enabled states, rule changes or role ownership changes.

## Published theorem and source-faithful obstruction
**KNOWN** [Y. Alekseev, *A Lower Bound for Polynomial Calculus with Extension Rule*, Theory of Computing 22, Article 4, June 21 2026, Theorem 1.1, DOI 10.4086/toc.2026.v022a004]. The rational-algebraic BVP system P_n: 1+sum_{i=1}^n 2^{i-1} x_i = 0, x_i^2-x_i=0 has 2^{Omega(n)} BIT-SIZE lower bound in the specific Ext-PC-with-extension-and-square-root calculus. This source is not the standard arithmetization of a polynomial-size CNF, and the claim does not imply Frege/Extended Frege CNF lower bounds.

**PRIOR EXACT** [LSPV-3 354, 2026-11-02 22:24 PST]: The natural equisatisfiable carry-CNF B_n (5n+2 clauses, 2n+1 variables, N=Theta(n log n)) has exact GLOBAL minimum W_Rmix341(B_n)=2n+1, obtained with genuine Resolution; 2n+2 sources indispensable.

**PROVED/EXACT scoped theorem:** For every polynomial p, for all sufficiently large n, every algebraic refutation rho of *P_n* requires |rho|_bits > p(|P_n|_bits + |enc(B_n)|_bits + |pi_n|_bits + 1), where pi_n is the explicit short signed-CNF certificate. Thus even a nonuniform/uncomputable polynomial-output translator from the short *B_n* proof to the original *P_n* algebraic proof cannot exist. This **does not forbid** a short algebraic proof of a different source Arith(B_n), and does not establish any hard family for full mixed R. Extensional equisatisfiability is insufficient to infer an efficiency-preserving proof map.

## Independently reconstructed controls and status
**COMPUTATIONAL** standalone, no-import JS rebuilt prior sources, authentic strict Resolution pivots, essential-source deletion witnesses at n=1,2,3,4,8,16,32,64, malformed source-clause/forged pivot rejections and odd/even K4 parity 0/8 models: **1,264 assertions PASS**. These are not a new asymptotic lower-bound verification. Optimizer discovery, evidence bits, verification work, source/index/head accesses, all-phase space, and charged DAG node count remain separate.

**Falsifiers** F1 carry-CNF inherits published algebraic BVP exponential lower bound: FALSE, already exact linear. F2 even uncomputable polynomial-output backtranslation possible: FALSE, source-specific theorem. F3 T_A(M) <= M^K forces Omega(M^K) per query: FALSE, the actual GROKPROOF 2026-11-03_1217 lemma reverses inequality. F4 AI=1 entails affine: FALSE, f=x1*x2 is nonlinear but annihilator 1+x1 is linear.

## Actual Grok and Claude material examined
Actual folders found via repository search: `GROKPROOF/`, `research/agents/grok/`, and `research/agents/claude/`. Grok `GROKPROOF/2026-11-03_1217_PROGRESS.md` (blob acf9fbee) and `GROKPROOF/2026-11-03_1518_PROGRESS.md` (blob 234fc189) have OPEN all-input charged ARC/FLMV contract; numerical forbidden-region membership alone is conditional and there is an explicit 1217 proof error (upper-runtime bound reversed). Claude `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` and `...1452_CLAUDE_TPORT-0002.tex` prove scoped alternation-trading portfolio statements, not B3; `research/agents/claude/onetape/README.md` assumes sequential access; `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` contains the false AI=1/affine claim. Read AGENTS.md, CODEX.md, pnp research skill, current 1204 directive and issue #3, LSPV-1 365, peer LSPV-2 364/365, LSPV-3 354/367, LSPV-4 364, LSPV-5 316. The original BVP construction is explicitly credited, not duplicated as new.

## Exactly shared output paths and repository controls
- Formal report: `research/agents/lspv-1/2026-11-03_0905_LSPV-1_BVP_ALGEBRAIC_NONPROJECTION366.md`
- Reproducer: `experiments/arc/lspv1_366_bvp_nonprojection_controls.js`
- Raw results: `results/raw/arc/2026-11-03_0903_LSPV1_BVP_NONPROJECTION366.json`
- This handoff: `research/coordination/2026-11-03_0905_LSPV1_BVP_ALGEBRAIC_NONPROJECTION366_FIVE_ROLE_HANDOFF.md`

Source readback matched every newly written file. Root `main.tex` was read through the full Git blob because the contents API returned empty text (1,455,410 characters). An LSPV-1-only insertion was committed with SHA `28348859c40c882d10903df4f4aa5bd8e2a77ec4`; new full Git blob SHA `441f856afd77000f42d0e145a4ae17f059c4dc24`, length 1,457,644. Exact full readback was compared, and every outside-region byte was preserved. No partial-file overwrite.

## Peer-specific follow-up
LSPV-2: Prioritize established published lower bounds under a calculus that **contains** all of Rmix341, or a mathematically valid backwards translation in the correct cost direction; do not reuse Haken PHP or Alekseev algebraic BVP without the known ER/carry escapes. LSPV-3: Test any proposed restriction-preserving invariant against actual paid auxiliaries, circuit payloads, and both-label controls. LSPV-4: Correct Grok per-query lower-time reversal and retain all-source/read/space charges. LSPV-5: Independently challenge the exact statement and any alleged source-equivalence from P_n to Arith(B_n), including the AI=1 counterexample.

**B1, B2, weakest sufficient B3 for same preselected R, superpolynomial worst-case Wbar_R and P versus NP remain OPEN.** The immediate missing sufficient implication is SAT in P => Wbar_R polynomial for the unchanged R, without assuming the formal correctness of an algorithm or polynomial proofs in advance.
