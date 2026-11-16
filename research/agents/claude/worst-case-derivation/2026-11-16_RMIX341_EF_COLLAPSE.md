# The fixed mixed calculus R_mix341 is polynomially equivalent to Extended Frege

Run: 2026-11-16, second pass (scheduled Claude routine, follow-up "work on this"). Branch `ccr-1695bd63-jady22`, base `9ae84900`.
Status summary: one PROVED/EXACT simulation (Theorem 5, standard techniques, proof at sketch level, unreviewed), one COMPUTATIONAL finite check of its constant-size local lemmas, two corollaries. **P versus NP remains OPEN.** No lower bound and no bridge is proved.

Scope: the *mathematical* calculus R_mix341 as written in `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (rules RES, AND3, XOR, LOCAL-CONVERT, DEF; unit cost per derived shared-DAG node; free source clauses). Nothing here concerns the native checker implementation; /341 remains FAIL as a full UNSAT authority and /386 remains RESTRICTED.

## 0. Correction and duplication disclosure for the first report of this date

- Theorem 3 of `2026-11-16_WR_BRIDGE_REFLECTION_REDUCTION.md` (EF bridge ⟺ short proofs of solver-correctness tautologies) substantially duplicates LSPV-1/361 (`research/agents/lspv-1/2026-11-03_0412_LSPV-1_ER2_UNIVERSAL_REFLECTION_COMPLETENESS361.tex`), which proves the same equivalence for the E = RES+VARDEF fragment with the family H_{A,ℓ}, and LSPV-1/336. I found these only after publishing. No priority is claimed for Theorem 3. Theorems 1, 2 and 4 are elementary and probably also implicit in earlier reports (codex 2026-11-11, LSPV-3/370).
- The first report said Pich–Santhanam give "EF-lower-bound ⟹ NP ⊄ P/poly transfers". That wording came from a search summary and is not what the abstract says. The corrected statement is in section 3.
- The first report's "next lemma" said to *define* R_H. The repository already fixed it: it is R_mix341. This report settles the lemma for that calculus.

## 1. Candidate and falsifiers (stated before the proof)

Candidate: EF p-simulates R_mix341, so W_R, W_E and EF refutation size are polynomially related pointwise.

Falsifiers:
- (F1) An XOR node can carry an equation on Θ(n) variables, which has no polynomial-size clause form. **Handled:** EF represents it with prefix-parity extension variables, not clauses.
- (F2) Unit node cost could hide superpolynomial bit content (the proof-packing trap of LSPV-5/REFEREE334). **Checked against the 341 rule text:** every node is a clause over at most M+q variables, an 8-bit factor, a GF(2) mask of at most M+q bits plus a right-hand side, a constant-support condition, or one two-input gate. Each has poly(M+q) bits. No packing rule exists in this fixed R.
- (F3) AND3 or LOCAL-CONVERT could act as a semantic oracle. **Checked:** both are restricted to constant support and verified by an explicit truth table, so each is a constant-size case analysis.
- (F4) The simulation could fail for equations mentioning DEF variables. **Handled:** the global variable order includes all original and defined variables.

## 2. Theorem 5 (collapse). PROVED/EXACT, standard techniques, unreviewed

Let F be a valid UNSAT source with M encoded bits and let π be an R_mix341 refutation with q paid nodes. Then F has an EF refutation of size poly(M+q), hence an E-refutation (strict RES plus signed two-input AND VARDEF) with poly(M+q) paid nodes. Since E is a subcalculus of R:

    W_R(F) ≤ W_E(F) ≤ (M + W_R(F) + 1)^{O(1)},
    W̄_R(N) ≤ W̄_E(N) ≤ (N + W̄_R(N) + 1)^{O(1)}.

Proof sketch. Fix a global order v_1..v_n of all variables, n ≤ M+q. Translate each node to an EF line:
- Clause: itself, O(n) symbols.
- 8-bit factor or bounded-support condition: a constant-size formula.
- DEF node: one extension axiom.
- GF(2) equation e with mask c^e and right-hand side b: introduce extension variables q^e_0 = 0 and q^e_j ↔ q^e_{j-1} ⊕ (c^e_j ∧ v_j). The line is the literal asserting q^e_n = b.

Rules:
- RES: one resolution step, simulated by EF in O(n) symbols.
- XOR from e1, e2 to e3 (mask c^{e1} ⊕ c^{e2}): prove q^{e3}_j ↔ q^{e1}_j ⊕ q^{e2}_j for j = 0..n by induction on j. Each step is a fixed implication over 7 variables (verified exhaustively, section 4), so it has a constant-size EF derivation. The final step gives q^{e3}_n = b1 ⊕ b2. Cost: O(n) constant-size lines per XOR node. If the sum is 0 = 1, the mask is zero, q^{e3}_n = 0 is provable in O(n) lines, and this contradicts the derived line.
- AND3, LOCAL-CONVERT and the GF(2) annotation of a factor: support is constant (at most three original variables for AND3). When a premise or conclusion is an equation in prefix-parity form, first prove in O(n) lines that q^e_n equals the explicit parity of its at most constantly many support variables (all other mask bits are 0, so q^e_j ↔ q^e_{j-1} there). The remaining step is a truth-table case analysis of constant size.

Total EF size: O(q · n) lines of O(n) symbols, with O(log n) bits per variable index. EF-to-E conversion with polynomial overhead is the standard Cook–Reckhow ER simulation, in the paid-node form already used in LSPV-1/361. The first inequality holds because every E-proof is an R-proof. ∎

Remark. The theorem's own text in 341 notes that its 4h−1 optimum "applies even if any further conservative, charged, at-most-binary-premise rules" are added. Theorem 5 is consistent with that: exact node optima such as 4h−1 versus 2h−1 live entirely inside the polynomial slack.

## 3. Corollaries

**Corollary 6 (the lower-bound target is exactly the EF problem).** W̄_{R_mix341} is superpolynomial iff EF is not polynomially bounded on CNF refutations.
- Every family with known polynomial EF refutations is polynomial in R_mix341. That covers PHP and its variants (Cook–Reckhow 1979; Buss 1987 for Frege), Tseitin over any field or modulus, clique–coloring, and parity/counting principles.
- So assignment priority 4 ("survive resolution, algebraic reasoning, circuit compression, shared DAGs, switching") has a sharp answer for this calculus: a family survives iff it is hard for EF. No unconditional EF-hard family is known. The published *candidates* are random k-CNFs, circuit-lower-bound formulas, finite consistency/reflection formulas, and proof-complexity generators (Krajíček; Razborov). These candidate lists are recalled from the literature, not re-verified this run.

**Corollary 7 (the bridge is exactly the EF bridge).** B(R_mix341) ⟺ B(EF) ⟺ B(E). In contrapositive form the bridge reads

    EF not polynomially bounded  ⟹  P ≠ NP.

This is the exact shape of the conditional results in Pich–Santhanam, "Towards P≠NP from Extended Frege lower bounds" (arXiv 2312.08163; abstract read this run through a fetch agent, body not read). According to the abstract, if EF is not p-bounded then P≠NP follows from any one of:
1. feasible anticheckers: S^1_2 proves that a p-time function generates anticheckers for SAT;
2. witnessing NP ⊄ P/poly: S^1_2 proves that a p-time function witnesses an error of each p-size circuit that fails to solve SAT;
3. S^1_2 proves a concrete function in E is hard to approximate by subexponential-size circuits, and S^1_2 proves a p-time reduction from circuits breaking one-way functions to p-size circuits computing SAT.

Their main theorem uses a different premise (unprovability in EF of p-size circuit lower bounds for a hard-to-approximate function, under two S^1_2-provability conditions).

**Program-level consequence.** For the fixed calculus, the whole plan is equivalent to two statements about one standard system:
- (LB) EF is not polynomially bounded. OPEN, and by itself it does not even give NP ≠ coNP.
- (BR) EF not p-bounded ⟹ P ≠ NP. OPEN; best published form is conditional on one bounded-arithmetic hypothesis above.

Mixed rules, shared DAGs and free strategy choice cannot change either statement by more than a polynomial.

## 4. Evidence

- Code: `xor_step_local_check.py` (this directory), deterministic; raw output `xor_step_local_check_raw.json`.
- Step lemma checked on all 4 mask patterns × 128 assignments = 512 cases: holds. Final-step lemma: holds. Random end-to-end parity consistency, 2000 trials, seed 20261116: holds.
- This verifies only the constant-size local implications. The polynomial bound is the symbolic induction above. No EF proof object was generated or machine-checked. Not executed: any proof-assistant check, any native 341 checker run, LaTeX compilation.

## 5. Gates

- DISJ: NOT APPLICABLE WITH REASON (proof-system simulation; no communication claim).
- Relativization: PASS / NOT A SEPARATION (a syntactic simulation; nothing is separated).
- Simultaneous DTISP: NOT APPLICABLE (size only; the simulation's proof *space* is not analysed and no space claim transfers).
- Deterministic configuration counting: NOT APPLICABLE (no machine-time bound claimed).
- Natural Proofs / algebrization: NOT APPLICABLE (no lower bound claimed).
- Easy-family controls: Horn, 2-SAT, affine, Tseitin, PHP are all polynomial on both sides of the equivalence, as required.

## 6. One next load-bearing lemma

Reproduce, in the project's notation and with explicit sizes, the Pich–Santhanam derivation of (BR) from hypothesis 2 (S^1_2-provable witnessing of NP ⊄ P/poly), and identify which step replaces the missing "feasible UNSAT-soundness" premise of LSPV-1/361. Deliverable: either a dependency-complete conditional bridge for E with the hypothesis stated as a single S^1_2-provability claim, or the exact step that cannot be reproduced from the abstract-level statement (the paper body must be read first; it was not readable this run).
