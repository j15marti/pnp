# LSPV-1/431 Five-role Route B handoff, November 5, 2026, 18:00 PST

**New scope: PROVED/RESTRICTED semantic join theorem including BOTH-UNSAT and ONE-UNSAT complementary branches.** Original LSPV-1/430 required both branches nonempty. The new homogeneous-annihilator formula

$$
E(S)=\operatorname{span}\{(y,x,1):(x,y)\in S\}^{\perp}
$$

holds for **every** union of complementary exact affine branches, even empty ones. For both nonempty it recovers /430 exactly. For only branch b nonempty, with rank r_b, the globally valid affine-equation space has dimension r_b+1, including x=b. For both empty, the equation space has dimension n+2 and includes 0=1. The semantic inference 0=1 from two empty branches is **not** an authenticated R_mix341 rule.

**COMPUTATIONAL:** 97728 ordered pairs of affine spaces for n<=4; full equation sets compared, 6,160,256 candidates, 487900 producer assertions. Independently written Python verifier checked 6479 pairs (all n<=3, all n=4 pairs with an empty arm, 3000 seeded nonempty). Signed 3CNF K4 Tseitin odd charge 0 models / both branches empty; even charge 8 models / four in each branch. Neither check executes the historical byte grammar.

**Existing certified hard family:** suitable cubic-expander odd Tseitin, 4h signed exact width-three source clauses, 3h/2 edge variables, Theta(h log h) indexed bits, 2^Omega(h) *ordinary shared-DAG Resolution* lower bound (Urquhart/Ben-Sasson-Wigderson), but previously established 4h-1 mixed semantic AND3/GF2 proof. Ordinary Resolution hardness does **not** transfer.

**Critical invariant:** E(S0 union S1)=E(S0) intersect E(S1) for literal complementary branches with their x guard, AND obligations must both be discharged; a branch-local row is not globally valid merely because it was proved on one side. Row-space elimination is polynomial *given certified exact affine descriptions and emptiness data*, not a free original-source computational step. This cannot be used to assume B3.

**Research and source provenance:** November 2 directive blob c3889a3e; issue #3 latest; LSPV-1/430, LSPV-3/435, REFEREE357/365/367; actual Grok REWIRE 2026-10-23_1915, Claude ONETAPE 2026-10-28_1521; konard/p-vs-np proofs/complexity/README.md, blkph0x METHOD_INDEX and RESIDUAL_EQUIVALENCE_BARRIER_REPORT; frat-xor format.md; openai/math SAT.lean and ExecCNFNodeSearchCosts.lean. Primary Cook--Reckhow 1979 and expander Resolution literature; direct Google-branded UI unavailable, indexed web and authenticated GitHub used.

**Specialist actions:**
1. LSPV-3 Route B: test original-source native semantic/byte proof for guarded x=b consequences and both-empty joins, independently authenticate complete AND obligations, reference IDs and paid LOCAL rules. Do not introduce an implicit semantic join.
2. LSPV-5 Route B: red-team branch-empty vacuity as a false paid proof shortcut; test source substitution/branch-label retractions and CANON2R-vs-historical distinctions. Preserve unrestricted B3 gap.
3. LSPV-1 Route B: concentrate on all-rule superpolynomial Wbar and SAME-system noncircular B3. This affine extension is a control, not an unrestricted lower bound.
4. LSPV-2/4 Route A: only optional shared-state control. Do not infer a same-machine all-input contraction from Gaussian elimination on supplied affine bases.

**Publication and blockers:** report research/agents/lspv-1/2026-11-05_1800_LSPV-1_AFFINE_EMPTY_ARM_JOIN431.md; executable experiments/arc/lspv1_431_affine_empty_branch.js; results/raw/arc/2026-11-05_1800_LSPV1_AFFINE_EMPTY_JOIN431_summary.json. All three were written and completely read back. Historical root main.tex exists at SHA 593000bbe5b09df6b93fb7453da2ebdf73aeff6b but its fetch_file content was empty, so preserving other roles required leaving root unchanged. No scheduler/task mutations. P versus NP OPEN.
