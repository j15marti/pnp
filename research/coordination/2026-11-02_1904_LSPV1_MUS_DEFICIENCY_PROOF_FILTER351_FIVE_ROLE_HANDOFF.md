# LSPV-1 MUS-DEFICIENCY-PROOF-FILTER351 | 2026-11-02 19:04 PST

**PROVED/EXACT**: For clause-minimally UNSAT U, a direct Hall-matching argument gives strict deficiency stability: every proper clause subset H has delta(H)<delta(U); thus the known maximum deficiency delta*(U)=delta(U)=m-v. This is known structural mathematics with a self-contained proof, NOT an academic novelty claim. For general UNSAT F, let kappa(F) be the **minimum deficiency of any MUS subcore**. Szeider (JCSS 2004, ECCC TR03-002) gives a KNOWN constructive algorithm outputting a regular binary Resolution refutation within 2^k poly(N) time when maximum deficiency is k. The resulting proof, with one unit-cost paid RES node per inferred clause, is valid in our unchanged Rmix341. Hence **mu(F)-1 <= W_Rmix341(F) <= C(N+1)^a 2^kappa(F)** for absolute constants C,a and encoded input bit length N.

**Necessary candidate condition:** For every fixed c>0, if kappa(F)<=c log2(N+1), W_R(F) is polynomial. Together with LSPV-1 MUS-WORSTCASE-QUOTIENT350, superpolynomial Wbar_R requires an unbounded sequence of maximizing MUSes with delta(U_N)>c log2(N+1) for each c. High deficiency is NOT sufficient. Do not interpret this as B3, as a lower bound on arbitrary machines, or as an efficient MUS extractor. Even extremely large cores with O(log N) deficiency are excluded as superpolynomial mixed-hard candidates.

**CORPUS DUPLICATION:** LSPV-4 HALL-DEFICIENCY-TRANSPORT62 already used Szeider 2004 for parameterized decision time, Hall maximum deficiency, and Horn-selector transports. The new project increment is applying stable-MUS parameterization to the *exact worst-case signed MUS quotient 350* to obtain a global proof-cost upper filter in the SAME fixed mixed calculus, not a new parameterized algorithm.

**COMPUTATIONAL:** Independently implemented Python and no-import JS checked all 512 two-variable subformula selections (417 UNSAT, 95 SAT, 12 MUS, eleven delta=1 and one delta=2). Python seed351 sampled 305 additional distinct 3-variable deletion-minimal UNSAT formulas with delta distribution 216/75/11/3 for deltas 1/2/3/4; all strict-stability checks passed. Positive/full blocking 3-variable MUS delta5, Peitl authentic rsmu_4_6_1.cnf delta2, Horn chain n2..8 delta1, and redundant UNSAT counterexample to MUS stability passed. Szeider's algorithm was not independently implemented or replayed; its theorem is cited from the ECCC/JCSS primary source. Native matched T/S not measured.

**ROLE FOLLOW-UPS (no identity/schedule/state changes):**
- LSPV-1: Continue weakest conditional B3 / noncircular reflection and worst-case Wbar. Screen core-signature atlas by (N,m,v,delta,mu,kappa) but do NOT assume efficient core acquisition.
- LSPV-2: Label authentic Peitl-Szeider and new nonaffine exact signed MUS sources with delta and certified W; validate fixed-R proof identifiers including charged DEF, preserving distinct 3-CNF transformations.
- LSPV-3: Exclude all O(log N)-deficiency MUS families from hard-target claims, even with high treewidth/large core/non-Horn signed incidence. Seek growing high-deficiency, extension-resistant nonaffine candidate.
- LSPV-4: Independently audit Szeider regular Resolution certificate output length against encoded bit length and all-phase charged generator work; distinguish proof cost upper from machine-time lower.
- LSPV-5: Red-team Hall proof and the premise that the FPT UNSAT branch emits authentic regular Resolution certificates. Test malformed, signed renaming, redundant formula, known short-proof high-deficiency controls. Audit B3 quantifiers.

**REPRODUCIBLE ARTIFACTS**
- Formal report: research/agents/lspv-1/2026-11-02_1904_LSPV-1_MUS_DEFICIENCY_PROOF_FILTER351.tex
- References: research/agents/lspv-1/2026-11-02_1904_LSPV-1_MUS_DEFICIENCY_PROOF_FILTER351.bib
- Independent Python: experiments/arc/lspv1_351_mus_deficiency_python.py
- Independent JS: experiments/arc/lspv1_351_deficiency_stability_independent.js
- Raw data: results/raw/arc/2026-11-02_1904_LSPV1_MUS_DEFICIENCY_PROOF_FILTER351.json
- Root main.tex LSPV-1-only change commit 3eed48a2bb6738d20aec231f2c6e9f3c77da7bae, full readback blob 0cf15b0ead938cc3100832fa18f9b02517368f63, all outside bytes unchanged.

The fixed calculus, free best-DAG selection, B1/B2/B3, source-authentication, all-phase space ledger and user-approved 12:04 priority remain unchanged. P versus NP OPEN.
