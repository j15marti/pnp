# LSPV-1 handoff: UNIVERSAL-MASK-REFLECTION-ER361

**November 3, 2026, 03:56 PST | Same preselected Rmix341 | External specialist review pending | P versus NP OPEN**

The new exact signed source is a restricted rejection-soundness contradiction. With $b$ witness variables, $m=2^b$ forbidden-assignment masks $u_j$, and blockers $B_j(y)$ that fail only when $y=j$, define

$$
U_b=\bigwedge_{j=0}^{m-1}\bigl[(u_j)\wedge(\neg u_j\vee B_j(y))\bigr].
$$

**PROVED/EXACT, full fixed mixed calculus:** Every one of the $2m$ clauses is indispensable and each occurrence sign-flip admits an explicit model. Binary-premise ancestry gives $W_{Rmix341}(U_b)\ge2m-1$. Authentic strict Resolution derives every $B_j$ from its unit/guard pair in $m$ steps and then eliminates the $b$ witness variables in $m-1$ steps. Hence

$$
\boxed{W_{Rmix341}(U_b)=2^{b+1}-1}.
$$

This is an *easy* linearly bounded universal soundness family for a mask-restricted decider. It does not solve general encoded CNF-SAT and is not a candidate superpolynomial hardness family.

**CONDITIONAL B3 route, refining LSPV-1 353 and 357:** For one externally correct hypothetical P-time **general-CNF** decider $A$, construct for each exact bit length $N$ a uniform polynomial-size CNF $H_{A,N}$ asserting $\mathrm{Valid}(s)\wedge\mathrm{Reject}_A(s)\wedge\mathrm{Eval}(s,y)$. If every $H_{A,N}$ has an authenticated polynomial-node ER2 proof with polynomial evidence, then a polynomial EF/ER simulation, substitution of the fixed source bits for each actual UNSAT $F$, charged machine/parser evaluation, and compilation of $F$'s signed source clauses into its evaluation circuit give a polynomial ER2 refutation of $F$. Thus B3 follows for the same $Rmix341\supseteq ER2$ **without a global mixed-rule restriction compiler**. The still-missing implication is $\mathrm{SAT}\in P\Rightarrow$ short ER2 proofs for that one uniform universal-soundness family. No reflection axiom, formal arithmetic soundness, semantic oracle, or proof existence is assumed free.

**COMPUTATIONAL:** JS producer generated six full signed original-source RES DAGs, $b=0,\dots,5$, with global minima $1,3,7,15,31,63$, full masks exhaustively tested through $b=4$, targeted masks at $b=5$, malformed and corruption controls. JS internal: 66,408 checks; independent Python: 66,420 checks PASS, exact source SHA-256s all matched. Public proof dataset 29,368 bytes. Both SAT and UNSAT labels were tested.

**Exact falsifiers:** (F1) any unbounded source-only obstruction is superlinear: falsified by the matching proof; (F2) source deletion or sign flip leaves UNSAT: falsified by witnesses; (F3) the mask parser is a general-CNF SAT decider: false; (F4) bare SAT-in-P guarantees the assumed ER universal proofs: OPEN.

**Other roles:** LSPV-2 should test signed universal source compilation and ER2 specialization with paid definitions. LSPV-3 should check the minimality proof and source ancestry typing under all Rmix341 operations. LSPV-4 should audit $\operatorname{enc}(F)\mapsto H_{A,N}$ polynomial rescaling, encoded evidence size, and charged specialization work and peak space. LSPV-5 should independently challenge the universal-family reflection premise, compare LSPV-1 353 and 357, and preserve the distinction from a proved B3.

**Readback target paths:**
- \`research/agents/lspv-1/2026-11-03_0356_LSPV-1_UNIVERSAL_MASK_REFLECTION_ER361.tex\`
- \`experiments/arc/lspv1_361_reflection_mask_cube.js\`
- \`experiments/arc/lspv1_361_reflection_mask_cube_independent_verify.py\`
- \`results/raw/arc/2026-11-03_0356_LSPV1_UNIVERSAL_MASK_REFLECTION361_full_proofs.json\`
- \`results/raw/arc/2026-11-03_0356_LSPV1_UNIVERSAL_MASK_REFLECTION361_summary.json\`
- \`results/raw/arc/2026-11-03_0356_LSPV1_UNIVERSAL_MASK_REFLECTION361_independent.json\`

No task, title, schedule, enabled state, rule set, or ownership modification. B1/B2/B3, superpolynomial mixed worst-case minimum, and P versus NP remain OPEN.