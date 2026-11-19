# CLAUDE scheduled run | 2026-11-19 07:50 PST | WMC-of-3CNF permanent formula transfer (0001)

Authority: AGENTS.md, END_TO_END_AGENT_MANUSCRIPTS. This is a Claude-routine **additive report**. It is not a TMR role. It does not edit any main*_PNP_*.tex manuscript, handoff, retired tracker or schedule. P versus NP is OPEN. /341 is FAIL as a full UNSAT authority. /386 is RESTRICTED.

## 1. Inputs reviewed this run

The user-linked Google Doc "P vs. NP Proof Attempts" (Drive id 1b2SYjJJ...Sqdds, 62,596 chars). It was read in full except §3.1–3.2 (GCT, IPS lower bounds), which were skimmed. It is a secondary survey with no new constructions. Corrections relevant to repo status (from memory; primary-source re-check pending):

- §2.3 says "VP=VNP implies P=NP unconditionally over finite fields (Bürgisser)". **Wrong as stated.** Bürgisser (Cook's versus Valiant's hypothesis, TCS 2000) gives only a *nonuniform* Boolean collapse. In contrapositive form, #P/poly ≠ NC/poly (resp. P/poly) implies VP ≠ VNP over finite fields, and over C under GRH. Reading it as "P=NP" is a uniformity error.
- §3.3 cites (3+1/86)n as the best explicit full-binary-basis bound. That is outdated: Li–Yang (STOC 2022) reach 3.1n − o(n). The "2n−2 probabilistic bound for an O(n)-sparse language in P" is UNVERIFIED.
- §2.2 says "exact bond dimension ≥ 2^Ω(tw)". As an algorithmic lower bound this is already falsified by the repo controls. DISJ has full cut rank but linear size. Unique-solution indicators have rank one. Affine/XOR systems have exponential cut rank but are solved in polynomial time by Gaussian elimination. Cut rank lower-bounds only contraction schemes, not SAT algorithms.

Repository search, OpenAI/Google orgs (gh search/repositories, 2026-11-19): relevant hits were openai/ten-proofs, google-deepmind/formal-conjectures, google-deepmind/alphaevolve_repository_of_problems and google/or-tools. Only **openai/ten-proofs @ 94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6** (Lean v4.32.0, formalization.yaml: sorry_count 0, axioms propext/Classical.choice/Quot.sound) contains a complexity lower bound. It is `Permanent.lean`, 27,563 lines.

## 2. Candidate, model, falsifiers

**Named dependency:** TMR-1 Track C asks for a "source-verified pinned formal restricted circuit conclusion" plus an exact transfer with failed premises stated. This run supplies a pinned external formal source and a fully explicit transfer into a SAT-encoded object. Its integration point is the restricted-conclusion slot of the TMR-1 chain, not an NP-hardness step.

**Source theorem (EXTERNAL FORMAL CLAIM, Lean kernel NOT re-run here).** The declaration is `PermanentFormulaLowerBound.permanent_divisionFree_formula_lower_bound` (Permanent.lean l.27509). For n ≥ 32 and every `f : Formula (Fin n × Fin n) ℂ` with `Formula.eval f = permanentPolynomial n`, it gives n^4/(128 log2 n) ≤ variableLeaves f, ≤ leafCount f and ≤ vertexCount f, and n^4/(256 log2 n) ≤ internalGateCount f. `Formula` is a tree over var/const/add/sub/mul with complex constants (l.20405). A division version with constant 192 is `permanent_rational_formula_lower_bound`.

**Candidate (PROVED/EXACT restricted, independent review OPEN).** Let psi_n be the width-≤3 CNF built by `experiments/claude/wmc_perm_3cnf_transfer.py::build`. It has variables x_ij (i,j in [n]) and, for each of the 2n rows and columns L, private auxiliaries s_{L,0..n-1}. It has clauses s0↔x0; s_t↔(s_{t-1}∨x_t) as three clauses; at-most-one (¬s_{t-1}∨¬x_t); and the unit s_{n-1}. Totals: V = 3n^2 variables, m = 2n(4n−1) clauses, encoding length Θ(n^2 log n).

Define WMC_psi(X,Y) = Σ over a in SAT(psi) of Π_{v: a_v=1} Z_v (X on x vars, Y on aux). **Then every ℂ-arithmetic formula F with eval F = WMC_psi_n has variableLeaves(F) ≥ n^4/(128 log2 n) = Ω(V^2/log V) for n ≥ 32. The same bound holds for leafCount and vertexCount, and internalGateCount ≥ n^4/(256 log2 n).**

**Proof.** (i) Within one block, the clauses force s_0=x_0 and s_t = s_{t-1} ∨ x_t. The at-most-one clauses forbid a second true literal and the final unit forbids zero. So a block is satisfiable iff exactly one of its literals is true, and then the auxiliary extension is unique. Blocks have disjoint auxiliaries, so SAT(psi_n) is in bijection with the n×n permutation matrices. (ii) Hence WMC_psi(X,1) = Σ_σ Π_i X_{i,σ(i)} = perm_n(X). (iii) Replace each aux leaf var y by const 1. This preserves leafCount, vertexCount and internalGateCount, does not increase variableLeaves, and commutes with eval, since eval is a ring hom and aeval is applied structurally. The result is a Formula over Fin n × Fin n evaluating to perm_n. Applying the source theorem finishes the proof. ∎

**Falsifiers stated before the check.** (F1) Some x has 0 or ≥2 auxiliary extensions off the permutations, i.e. the encoding is not parsimonious. (F2) The pinned theorem has different hypotheses or a different field or model. (F3) Substitution could raise the measured size. (F4) The source theorem is vacuous or relies on extra axioms. Results: F1 was tested and survived. F2 was checked against the source text and survived. F3 is excluded by the structural argument. F4 is OPEN, because the Lean kernel and Comparator were not executed: no Lean toolchain here, and a mathlib build exceeds the 30 s stage limit.

## 3. Executed evidence (COMPUTATIONAL)

Command: `python3 -I experiments/claude/wmc_perm_3cnf_transfer.py results/raw/claude/2026-11-19_0750_WMC_PERM_TRANSFER_RAW.json`. Revision CLAUDE_WMC_PERM_TRANSFER_v1, no randomness, 3.26 s. Raw sha256 517499e88dbb1825cc1a459cc51d194d809903e7a37918ce5cba1a358e427eae.

For n = 1..4 the script enumerated all 2^(n^2) x-assignments and every per-block auxiliary assignment. The extension count is 1 on exactly n! assignments and 0 elsewhere (n=4: 24 vs 65,512). WMC monomials equal perm monomials with coefficient 1 in every case, and the max clause width is 3. These finite checks support step (i) but do not replace its symbolic proof.

## 4. Scope, gates and controls

What this is **not**:
- It is not a SAT-decision lower bound: psi_n is satisfiable, and bipartite matching is polynomial.
- It is not a #SAT-algorithm or Boolean-circuit lower bound. Numeric #PM is #P-complete (Valiant 1979), but Boolean circuits are not ℂ-formulas over weights.
- It is not superpolynomial. Ryser gives O(2^n n^2)-size formulas, and arithmetic *circuit* lower bounds for perm stay at the Baur–Strassen/VP-vs-VNP frontier.

**Field control:** over GF(2), perm = det and has poly-size circuits. The bound is characteristic-0 specific, as stated in the ℂ-only source, and is not transferable to char 2 without new proof.

**Monotone control:** monotone circuits for perm already need 2^Ω(n) (Jerrum–Snir 1982), so the new content is non-monotone formulas only.

**Four gates:**
- DISJ: PASS as sanity. ∏(1−x_i y_i) has a linear formula and the method is specific to perm, with no static-rank inference.
- Relativization: NOT APPLICABLE (nonuniform algebraic, no oracle machine).
- Simultaneous DTISP: NOT APPLICABLE (no machine bound claimed).
- Deterministic configuration counting: NOT APPLICABLE (no uniform machine).

Algebrization is NOT APPLICABLE. Algebraic Natural Proofs (Forbes–Shpilka–Volk; Grochow–Kumar–Saks–Saraf) target superpolynomial bounds, and whether the transcendence-degree measure is natural is OPEN.

Independent review: none. Lean replay is not executed.

## 5. One next load-bearing lemma

Kernel-replay the pinned declaration with Lean v4.32.0 plus the lake-manifest mathlib (`lake build Permanent`, `#print axioms PermanentFormulaLowerBound.permanent_divisionFree_formula_lower_bound`, Comparator config C_PermanentFormulaLowerBound.json). Then formalize step (iii), the constant-substitution lemma, in Lean against the same `Formula` type. Until then, the transfer is PROVED on paper and the source is an UNREPLAYED EXTERNAL FORMAL CLAIM.
