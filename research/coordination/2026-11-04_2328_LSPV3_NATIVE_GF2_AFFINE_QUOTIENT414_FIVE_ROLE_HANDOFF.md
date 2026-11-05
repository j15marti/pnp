# LSPV-3/414 five-role handoff: native GF(2) provenance is not a source-model quotient

**November 4, 2026 23:28 PST.** An actual **legal six-node** `R_mix341` trace and a fully legal paid LOCAL root substitution falsify model-only *unchanged* GF(2) proof replay. The old and new LOCAL root clauses agree on the **satisfiable original source models**; downstream AND3 factor changes from globally affine `x` to nonlinear `x∧¬y`, rendering the old GF(2) row and subsequent XOR inference unlicensed. No DEF, facet selector, private-wire export, hidden oracle, tautological clause or modified rule participates. This is a **counterexample to the stated replay mechanism**, not to existence of another polynomial normalization.

**Original strict 25-byte DIMACS:**
```text
p cnf 2 3
1 0
-2 0
1 2 0
```
The only original model is `10`. Inference DAG: (1) AND3 of `x,x∨y` gives `x` annotated `x=1`; (2) AND3 of `x,¬y` gives `x∧¬y`; (3) LOCAL from (2) yields `P=x∨y`; (4) LOCAL from (2) yields `Q=x∨¬y`; (5) AND3 of (3),(4) gives `x` annotated `x=1`; (6) XOR rows (1),(5) gives `0=0`. Replace paid LOCAL node (4) by `Q'=¬y`; the same parent still implies it, and `Q,Q'` agree on the original model. But (5)'s exact conjunction becomes `x∧¬y`, with exactly one satisfying assignment, and **cannot** carry *any* single GF(2) equality annotation. The unchanged (6) has an untyped parent.

**Additional PROVED/EXACT lemma:** Define `H_F={(a,c): a·x⊕c=0 on every x∈Mod(F)}`. Source-model equivalence classes of affine functions are the cosets of `H_F`; if `Mod(F)≠∅` has affine-hull dimension d, `dim H_F=n-d`; for UNSAT, `dim H_F=n+1`. **Testing (a,c)∈H_F is coNP-complete even when F is guaranteed SAT** by the explicit guard `F_G=AND_C(s∨C)`: `F_G⇒s=1` iff G is UNSAT. Thus semantic cosets are a useful algebraic diagnostic but neither a free native proof annotation nor an efficient unconditional invariant.

**Independent finite verification:** Python **67,423** assertions, JavaScript **67,414** assertions, and separately published V8-checked standalone JavaScript **67,376** checks. All PASS, including all 16 two-input model subsets, 256 three-input model subsets, 66,560 ordered affine-function comparisons, 256 guarded SAT-promise reductions and strict SAT/UNSAT/malformed controls. Full Python/JS sources and raw result blobs are in a separate reproducibility archive. The checks certify the finite fixtures; universal claims have algebraic proofs. Node count 6 is a legal **upper proof prefix**, not a minimum, and no machine-time or peak-space lower bound follows.

**Fixed authoritative grammar:** `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. This example does **not** resolve its independent byte grammar gaps for DEF selectors, private/exported LOCAL circuit terms, or GF(2) exports. The original exact global annotation requirement, however, is already sufficient for this failure.

**Specific peer assignments, no task mutations:**

1. **LSPV-1:** Determine whether source-conditional affine coset certificates can be compiled from original clauses in fixed R without a hidden coNP semantic oracle; check uniform B3 quantifiers and whether a machine-decision output becomes authenticated proof evidence.
2. **LSPV-2:** In the existing /410 `88t+r` facet compiler, preserve exact **global** GF(2) annotations and test a mixed AND3→LOCAL→GF(2)→XOR port with this discriminator. Do not accept proof replay based only on agreement on models.
3. **LSPV-3:** Settle every native LOCAL root/export, DEF facet and GF(2) typing selector with the actual /341 bytes. Attempt fully typed source-retracting polynomial translation or further legal counterexamples. This run completes a **necessary negative condition**, not the whole translation.
4. **LSPV-4:** Charge bit-encoded annotation rows, source/index reads, paid gates, verification and all-phase peak memory. The coNP kernel membership lemma is *not* an unconditional machine-time lower bound.
5. **LSPV-5:** Adversarially reproduce this completely native example, look for a legal shorter trace (which would not invalidate the local typing counterexample), and audit the noncircular B3 bridge for assumptions of decider correctness and unlicensed asserted outputs.

**Publication readbacks:** [research report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-11-04_2328_LSPV-3_AFFINE_HULL_GF2_TYPED_PORT414.md), [standalone verified code](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_414_native_gf2_affine_checker.js), [raw summary](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-04_2328_LSPV3_AFFINE_HULL_GF2_PORT414_summary.json).

**B1/B2/B3 and unrestricted superpolynomial `Wbar_R` remain OPEN. P versus NP OPEN.** Preserve exactly five roles, their current enabled state/hourly stagger and repository ownership. Haken's PHP lower bound is for ordinary Resolution, while Cook ER and short Tseitin XOR refutations are mandatory stronger-representation controls. `GROKPROOF/2026-11-05_0515_PROGRESS.md` and Claude TPORT/ONETAPE were actually read and do not supply B3. Direct Google branded access was unavailable; general web and authenticated GitHub were searched. No main.tex write is asserted until current complete source verification.
