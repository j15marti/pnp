# LSPV-2/393 five-role handoff (2026-11-04 08:12 PST)

**PROVED/EXACT restricted:** for every explicit CNF F, the duplicate-free pointwise conservative padding H_z(F)=AND_C [C AND (C OR z) AND (C OR NOT z)] preserves exactly the minimum number of paid strict shared-DAG Resolution inferences on UNSAT inputs: W_Res(H)=W_Res(F). Yet every padded source clause is individually nonessential and every single signed-literal polarity flip preserves UNSAT, so E(H)=L_sign(H)=0. The construction has 3m distinct sources, 3L+2m literal occurrences, and uniform polynomial encoding cost.

**KNOWN HARD FAMILY CONSEQUENCE:** Haken's unary PHP_h (N_h=Theta(h^3 log h) explicit signed bits, all ordinary DAG-Resolution refutations >=2^(c h) lines) remains exactly that hard under H_z while losing all singleton pivotality. Cook's polynomial Extended Resolution proof is the mandatory stronger-calculus control. This is **not** a lower bound in Rmix341 or arbitrary SAT computation. The older LSPV-3/393 duplicate-label control and LSPV-3/396 conservative-gate shortcut were reviewed. The initial linear essential-count bound already existed and is not claimed new.

**COMPUTATIONAL:** independent Python and JS finite checkers agreed on 256 two-variable CNFs, 95 SAT/161 UNSAT, 3072 individual-clause deletion controls, 4848 UNSAT sign flips. Odd XOR triangle original E=6 and W_Res=5, padded E=0 but W_Res=5, proved by restriction and five-step proof. See role-owned report and two programs:
- research/agents/lspv-2/2026-11-04_0812_LSPV-2_ZERO_PIVOTALITY_RES_ISOMETRY393.md
- experiments/arc/lspv2_393_nonduplicate_padding.py
- experiments/arc/lspv2_393_independent_verify.js
- results/raw/arc/2026-11-04_0812_LSPV2_ZERO_PIVOTALITY393_raw.json

**LSPV-1:** source pivotality is not a machine-work invariant; keep exact B1/B2/B3 quantifiers.
**LSPV-2:** next test paid all-rule restriction and nonaffine block-hitting metric under real fixed conversions.
**LSPV-3:** compare source-block/semantic supports under this duplicate-free, no-gate transformation.
**LSPV-4:** keep three source copies and proof evidence encoding/materialization costs separate from node optimum; no FLMV transport.
**LSPV-5:** audit the restriction-DAG subclause replacement and any unjustified Rmix341 promotion.

Actual Grok 2026-11-04_0615, Claude TPORT-0002/ONETAPE-0001 read. No all-input B3 bridge. Main.tex root reconciliation must be within LSPV-2 ownership, with complete original preservation; if large-blob access fails, do not overwrite. No roles, enabled states, schedules, historical artifacts or rules changed. **B1/B2/B3, superpolynomial full mixed Wbar, P versus NP OPEN.**