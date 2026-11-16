# TMR-5 current handoff | 2026-11-16 05:48 PST | worst-case derivation bridge red team /058

**Authority and ownership:** END_TO_END_AGENT_MANUSCRIPTS read first; compatible SAT-compression directive retained. TMR-5 owns main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex, role reports/code/raw and this handoff only. Prior /057 handoff archived byte-exact at research/agents/tmr-5/archive/handoff_pre_2026-11-16_0548.md (blob 7cd59c60b929b9e805c012363df21b9c2d84cce0). Peer manuscripts, retired proof trackers, historical root files, identities and schedules untouched. P versus NP OPEN.

**Target audited:** the user's shared objective Wbar_R(N) = max_{UNSAT F, |F|<=N} min_{pi:F|-_R bot} cost_R(pi) and the bridge B_R: SAT in P => Wbar_R(N) <= poly(N). The referenced "shared worst-case research directive on GitHub" was NOT found in the repository; nothing was invented in its place.

**Results (PROVED/EXACT elementary, external review OPEN):**
- T1 bridge collapse: for every R with an already-known superpolynomial lower bound (Res, tree-Res, PC over any field, CP, bounded-depth Frege), B_R is logically equivalent to P != NP. That is not a weakening: it inherits BGS, Natural Proofs and algebrization.
- T2 pointwise transfer FALSIFIED: a correct total decider that recognizes a P-uniform hard family (PHP, explicit-expander Tseitin, Tseitin mod q, clique-colouring) runs in poly time on it, while R-refutations are superpolynomial. Non-cheating control: Tseitin is decided by GF(2) Gaussian elimination in O(N^3). "Every algorithm implicitly performs an R-derivation" is the failed premise.
- T3 exact content for R >= EF: B_R <=> [SAT in P => some poly correct A has poly-size R-proofs of its correctness tautologies Corr_A,n]. This holds if P=NP is PV-provable (Cook 1975) but is not known to follow from P=NP. KP89: E=NE gives a p-optimal system, but it does not fix EF in advance.
- Combined Res ∪ PC_F2 ∪ CP: PHP (CP-easy, CCT87) and Tseitin (PC_F2-easy; CP quasipoly, Dadush–Tiwari 2020) are both FALSIFIED as hard instances.

**Executed:** preflight --check --json (document/ownership OK; mathematical_validation NOT_PERFORMED). CPython experiments/tmr/tmr5_pointwise_transfer_falsifier058.py, rev tmr5-pointwise-transfer058.v1, deterministic, blob 1dcace91efbca6fb32c05de700999a78e6bbca0d, 16 s. Brute-force UNSAT and exact min decision-tree leaves: PHP n=1..3 gave 3/11/43; Tseitin K4/K33/prism/cube gave 28/76/48/128. Raw results/raw/tmr/2026-11-16_0548_TMR5_POINTWISE_TRANSFER058_PY_RAW.json blob a2f1be8c76a4cdbe4c4e580703097785808031cd. COMPUTATIONAL only. PHP_4^5 not run. No pdflatex available (brace/document structure check only), no Lean.

**Gates:** DISJ NOT APPLICABLE; relativization OPEN/blocking for any proof of B_R; DTISP NOT APPLICABLE (proof-size measure); config counting upper-bound guard only. /341 FAIL, /386 RESTRICTED.

**Ranked pipelines (unchanged from /057):** TMR-1 E^NP conditional chain (Lean kernel OPEN) > TMR-2 restricted exact counts > TMR-3 restricted checkpoint services > TMR-4 restricted compiler. New Wbar_R program: lower-bound half is done for weak R; the bridge carries all the difficulty.

**Paths:** main5 (updated in place, new section sec:wr); research/agents/tmr-5/2026-11-16_0548_TMR5_WORST_CASE_DERIVATION_BRIDGE_REDTEAM058.md; executable; raw; archive; this handoff. Branch ccr-1695bd63-vuamj6 pushed; NOT merged to main (no PR opened by this run).

**ONE next lemma:** does any known consequence of P=NP (E=NE, PH collapse, p-optimal systems) give poly-size EF proofs of Corr_A,n for a fixed A? Otherwise record B_EF as an independent assumption.

END_OF_HANDOFF::TMR5::2026-11-16_0548_PST
