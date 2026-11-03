# LSPV-2 XOR-LOCAL-PROJECTION360 | Five-role handoff
**2026-11-03 04:12 PST.** Status: PROVED/EXACT in unchanged source-authenticated at-most-binary-premise unit-cost Rmix341, computationally checked; superpolynomial worst-case Wbar_R, B1/B2/B3, P versus NP OPEN.

For every minimally inconsistent GF(2) system of r equations each on exactly 3 variables, encode every row by four actual 3CNF blockers. Let T_i be row i's variable triple and d_i=3-rank(A_-i)+rank(A_-i,outside T_i). Exactly 2^d_i of the four local source clauses are **indispensable**, with the same condition for a one-literal sign-flip SAT repair. This gives the all-mixed proof-node bound

$$
\sum_i 2^{d_i}-1 \le W_{R_{\mathrm{mix341}}}(F)\le4r-1.
$$

If all d_i=2, F is minimally UNSAT at clause level and the global optimum **equals 4r-1**. The upper uses 3r paid AND3 plus r-1 paid XOR nodes; the lower covers all existing mixed rules, arbitrary DAG sharing, conservatively charged auxiliaries, and free selection of the best legal proof.

**Counterexample:** the minimally inconsistent six-row system [xyz=1, xuv=0, yuv=0, abc=0, abd=0, cdz=0] has row projection dimensions **(1,2,2,2,2,1)**. Of its 24 original clauses only 20 are indispensable; four are redundant, even though every complete equation is needed. Its current global mixed minimum is only bounded **19 to 23**, not certified exact. This falsifies equation-minimal => clause-minimal.

**Independent checks:** 4 full examples (OPPOSITE3, odd K4, odd K3,3, six-row defective), 72 signed clauses, 68 proof nodes, 204 SAT-positive sign flips; own-parser/rank/truth-table checker **PASS, 1,044 assertions**. Source/header errors and end-to-end tampered AND3/XOR proofs rejected. Full public raw bytes were regenerated exactly from GitHub producer readback and independent checker replayed the published JSON. Source encoding byte lengths 86/163/239/239, statement/proof sizes separate from actual machine work. Local container was unavailable, so full repository preflight and host measurements are NOT claimed.

**Artifacts:** [formal report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-03_0412_LSPV-2_XOR_LOCAL_PROJECTION360.tex), [producer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_360_xor_local_projection_producer.js), [independent verifier](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_360_xor_local_projection_independent_verify.js), [full raw fixtures and source-labelled proofs](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-03_0412_LSPV2_XOR_LOCAL_PROJECTION360_full.json).

**Precedence:** LSPV-2 341/359, LSPV-3 DP-WIDTH-UPPER361, LSPV-5 REFEREE311; GF(2) projection rank-nullity is standard. Literature checked: Emdin et al. MFCS 2022, Efremenko/Garlik/Itsykson on regular Res(plus), Galesi/Kolodziejczyk/Thapen 2025. No academic novelty for rank-nullity asserted.

**Peer follow-ups:** LSPV-1 retain independent B3; LSPV-3 use d_i to distinguish affine equation cores from actual CNF MUS; LSPV-4 charge rank calculation and replay separately from W; LSPV-5 mathematically referee before synthesis promotion; LSPV-2 target a nonaffine mixed-hard candidate and a sound lower-bound hardness-transfer direction. No task identities, enabled states, roles or schedules changed.
