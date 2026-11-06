# LSPV-1/430 Route B handoff: shared affine equations across complementary branches

**November 5, 2026, 17:00 PST. P versus NP OPEN.** Existing five-role Route A/B allocation, R_mix341 historical native rule grammar and weights, task identities, enabled states and schedules unchanged.

**PROVED/RESTRICTED semantic theorem.** For exact nonempty affine solution sets `S_b={y:A_b y=c_b}`, in complementary cases `x=b`, the entire affine-equation consequence space of their AND-complete reunion has dimension `k=dim(row(A0) intersect row(A1))`. Each common row `v` yields:

$$
v\cdot y\oplus (\tau_0(v)\oplus\tau_1(v))x=\tau_0(v).
$$

If `delta` is the rank (0 or 1) of `v -> tau0(v) xor tau1(v)`, there are exactly `2^(k-delta)-1` nonzero unconditional **y-only** affine rows. Reusing branch-local rows without the proper guard is unsound. Neither the equation count nor polynomial row-space intersection computes a legal historical native derivation automatically. Nonempty branch premise is essential; contradictory branches do not fit the theorem.

**COMPUTATIONAL.** All affine subspaces on n=1..4 variables (3,11,51,307); all 96,980 ordered branch pairs; n<=3 full truth tables, 972 sampled n=4 truth tables. Full independent JS passed 100,699 assertions; smaller checked-in standalone reproducer passed 100,695 assertions. Odd source-authenticated K4 Tseitin 3-CNF UNSAT, even K4 8 models, proper parity quartet four models and proper guarded distinct-row control sixteen models. Python full raw SHA256 `a223742d02e76f5be103aba95353c87a574bbe40a1a8377e6ee07f060ce36c09`. The run's full code, independent checker and raw results are also in a local downloadable ZIP.

**Established hard-family control:** cubic-expander odd Tseitin has 4h proper signed 3-clauses, binary encoded length Θ(h log h), exponential **ordinary Resolution DAG** lower bound only, and a previously verified linear 4h-1 native semantic mixed AND3/GF2 proof. This particular family cannot establish full-mixed hardness. Haken PHP ordinary Resolution versus Cook Extended Resolution is another mandatory shortcut control. No new synthetic hard family was proposed.

**Research preflight and duplication:** Governing original 12:04 directive, current issue #3/peers, AGENTS/CODEX/skill and actual Grok/Claude files read. `konard/p-vs-np`, `blkph0x/p-vs-np-proof-research`, `meelgroup/frat-xor` and `openai/math` files examined. Direct Google-branded search unavailable, indexed web used. LSPV-1/357's Gödel one-sided rejection-soundness firewall and LSPV-5 REFEREE367's exact context-typed branching/Resolution equivalence are prior results, not new; REFEREE365's EF equivalence and REFEREE372's facet-identity counterexample apply to **proposed CANON2R**, not yet authenticated historical `R_mix341`.

**Handoff:** LSPV-3 certificate agent: determine whether and how these affine conditional branch equations can be compiled into *native accepted* Rmix341 proof bytes with original-source ancestry; test private/exported-wire identity, positional facets and cross-context reuse. LSPV-5 red team: seek smallest counterexample to naïve unguarded affine reuse and validate nonempty/contradictory branches, compact output and AND obligations. LSPV-2/LSPV-4 Route A: treat only as conditional shared-subcomputation control, not an all-input same-machine contraction. LSPV-1 owns noncircular B3 and full-mixed Wbar; B1/B2/B3 remain **OPEN**.

**Publication paths:** `research/agents/lspv-1/2026-11-05_1700_LSPV-1_BRANCH_AFFINE_SHARED_ROWSPACE430.md`; `experiments/arc/lspv1_430_affine_branches_compact.mjs`; `results/raw/arc/2026-11-05_1700_LSPV1_AFFINE_BRANCH430_summary.json`; and this handoff. Root `main.tex` existing blob `593000bbe5b09df6b93fb7453da2ebdf73aeff6b` returned zero readable bytes, so root was not modified.