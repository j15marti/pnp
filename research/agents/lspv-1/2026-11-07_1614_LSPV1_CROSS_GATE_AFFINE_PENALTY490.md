# LSPV-1/490 | Sharp quantitative penalty for cross-gate affine predictors

**November 7, 2026, 16:14 PST | Route B | PROVED/RESTRICTED symbolic theorem + COMPUTATIONAL exhaustive controls | P versus NP OPEN**

**Relevant shared nodes:** [P2-F13] (this restricted optimization branch), [P2-C3], [P2-D1], [P2-B1], [P2-B2]. **No historical R_mix341 rule, weight or accepted-byte semantics have been revised.**

## IDEA: precommitted hypothesis and falsifiers

**Hypothesis.** The LSPV-1/487 sharp single-template agreement bound of `3^g` for `g` independent AND gates is achieved only by coordinate-separable affine predictions. Any predictor that mixes an input of gate `j` into the predicted output of a distinct gate `i` loses a **quantifiable** fraction of its matching assignments. This is a potential falsifier of an alleged cross-branch **affine-template sharing** shortcut. It is NOT a proof-system lower bound.

**Falsifiers fixed before the test:** (F1) find a cross-coupled affine vector predictor attaining `3^g` agreements; (F2) find a cross-coupled predictor exceeding `7*3^(g-2)`; (F3) find a maximizer not among the four coordinatewise best affine predictors per gate; (F4) the Fourier factorization fails under globally affine coefficients connecting different input pairs. F1–F4 are excluded in the stated mathematical model by the proof; F1–F3 were also exhaustively tested for `g<=3`. They remain irrelevant outside that model.

## SEARCH, authenticated continuity and revision

Both complete tracker files were fetched on `main` before the run: `proof1.txt` initial blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` initial blob `0a5d4a1cf56a215669df7378140781ff588c9510`; issue #3 and its current body were reviewed. Governing handoff: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, current blob `c3889a3e514ddbd747150dcb68607013a3b2d154`, with historical anchor commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`. Governance read: `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`. No local checkout of that skill's preflight existed in the execution container, and the command was not claimed to have run.

Read LSPV-1/488 and its 4,130-character published exact JS certificate, LSPV-3/484 `research/agents/lspv-3/2026-11-07_LSPV3_AFFINE_NONLINEAR_STRATA484.md` blob `a5a1fd0cc2ce55baacadd3831cbdf5ee75404fbf`, LSPV-5/419 `research/main/2026-11-07_1548_MAIN_METADATA_BINDING_REFEREE419.md` blob `ccbda2cbba619a6f2146cf95918c3a462eb2f0c6`, Grok actual file `GROKPROOF/2026-11-07_1920_PROGRESS.md` blob `231561ce216699f286b705a0056584789ba9ee99`, and Claude actual `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`. LSPV-5/419 shows the recovered historical checker does not authenticate declared metadata and cannot authenticate the full RES/DEF/LOCAL-CONVERT grammar. No native accepted-byte check is implied here.

Required external repositories actually reviewed: `konard/p-vs-np` `README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, and `proofs/p_not_equal_np/README.md` blob `3a0304116e719948122302849ccae38d3890e410` (conditional machine statements, no P!=NP proof); `blkph0x/p-vs-np-proof-research` `README.md` blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814`, and `index.md` blob `e8f685d0d4e17dd8021e5051cdfce23f9291af63` (scoped relaxations, no general lower bound); `meelgroup/frat-xor` `README.md` blob `38a137bca4d4ab6443703d4c31fba5783021c581` (separate FRAT-XOR/XLRUP checker); `openai/math` `README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` (research materials, no historical Rmix grammar). GitHub source and public web searches were used. No separate Google-branded UI was available.

Primary literature: Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, 2026-10-24, Theorem 7.2(a), for the **separate syntactic** fixed-degree Res(PC_r/F_p) benchmark; Cook--Reckhow, *Relative Efficiency of Propositional Proof Systems*, JSL 1979, for proof-system quantifier discipline; Haken, *The Intractability of Resolution*, TCS 1985, for ordinary DAG Resolution lower-bound control. All three are scoped and are not being transferred silently. External relevant format: `meelgroup/frat-xor/format.md`, separate from historical /341.

The initial hypothesis was strengthened using the Fourier character expansion: not merely is cross-coupling **not necessary** at an optimum; it provably reduces maximum agreements to the sharp `7*3^(g-2)`. An independent exact Python enumerator reproduces the JS exhaustive data for all affine maps with `g=1,2,3`.

## Theorem 489.1: exact equality case and strict cross-coupling penalty (PROVED/RESTRICTED)

Let `g>=1`, and let `u_i,v_i` be `2g` independent Boolean inputs. Define `Q_i(x)=u_i v_i`. Let `A:GF(2)^(2g)->GF(2)^g` be **any globally affine vector map**, including cross-gate dependencies. Let `M(A)=#{x: A(x)=Q(x)}`.

**Claims:**

$$
M(A)\le 3^g.
$$

Equality holds **if and only if each** `A_i` depends solely on `(u_i,v_i)` and is one of exactly four affine functions

$$
A_i\in\{0,u_i,v_i,1\oplus u_i\oplus v_i\}.
$$

Hence there are exactly `4^g` maximizers among all `2^{g(2g+1)}` affine vector predictors.

For `g>=2`, if there exists an off-diagonal affine coefficient from an input in pair `j` to a predicted output `i!=j`, then

$$
\boxed{M(A)\le 7\,3^{g-2}<3^g.}
$$

This latter inequality is **sharp** for every `g>=2`.

**Proof.** Put `E_i(x)=Q_i(x)\oplus A_i(x)`, and, for `s in GF(2)^g`, define the Fourier character expectation

$$
c_s=\mathbb E_x(-1)^{\sum_i s_iE_i(x)}.
$$

Fourier inversion for the all-zero error vector gives

$$
M(A)=2^g\sum_{s\in\mathrm{GF}(2)^g} c_s.
$$

Write `A_i=b_i\oplus\sum_j(\alpha_{ij}u_j\oplus\beta_{ij}v_j)`. Because all input pairs are independent, `c_s` factors over pairs `j`. If `s_j=0`, the local factor is 1 when the induced linear coefficient on `(u_j,v_j)` is zero and 0 otherwise. If `s_j=1`, the local factor is a signed `1/2`: for any `a,b\in GF(2)`,

$$
\mathbb E_{u,v}(-1)^{uv\oplus au\oplus bv}=\tfrac12(-1)^{ab}.
$$

It follows that `c_s<=2^{-|s|}`, so

$$
M(A)\le 2^g\sum_s2^{-|s|}
       =2^g(3/2)^g=3^g.
$$

For equality **every** summand must be maximally positive. In particular, for each singleton `s=e_i`, every inactive pair `j!=i` must have zero induced linear coefficient. Thus `A_i` contains no cross-pair input. The same singleton sign condition requires `(-1)^{b_i+\alpha_{ii}\beta_{ii}}=+1`, yielding exactly the four listed affine functions. Conversely each such function agrees with `uv` on exactly three of its four local inputs; independence gives `3^g`.

For the sharp strict bound, choose any nonzero off-diagonal coefficient from row `i` to pair `j!=i`. Fix `s_j=0` and all coordinates of `s` except `s_i`. For the two choices `s_i=0,1`, the induced linear coefficient on pair `j` differs by a nonzero vector. Therefore at least one of those two Fourier terms is **zero**, losing at least `(1/2)2^{-|s_{rest}|}` relative to its optimistic `2^{-|s|}` allowance. Summing this loss over every `s_rest in GF(2)^(g-2)` gives

$$
\sum_s c_s\le(3/2)^g-\tfrac12(3/2)^{g-2}.
$$

After multiplication by `2^g`, this is `M(A)\le 7\,3^{g-2}`.

To attain equality, for the first two gates choose `A_1=0` and `A_2=u_1`. Exactly seven of the sixteen four-input assignments satisfy both predictions. For the remaining `g-2` independent gates choose `A_k=0`, each agreeing on three inputs, yielding exactly `7\,3^{g-2}`. QED.

**Nonclaims.** This theorem concerns ONE globally affine predictor per agreement region. The cover may use multiple predictors, nonlinear guard conditions, paid auxiliary definitions, adaptive branching and cross-branch shared lemmas. It gives NO lower bound on the number of distinct inference nodes in historical R_mix341 or on computational SAT time. It cannot exclude a legal GF(2)/ER shortcut. The 3-template paid guard clause of LSPV-1/488 remains a distinct restricted certificate, not a historical proof.

## Existing established-family and known-method ledger

| Family / encoding | Published hardness | Known legal shortcuts | Remaining transfer |
|---|---|---|---|
| Signed random proper 3-CNF with n original variables, m=8n original signed 3-clauses, usual indexed binary size O(n log n) | Pang 2026 Thm 7.2(a): exponential DAG Res(PC_r/F_p) lower bound a.a.s. for fixed p,r, using PC-degree hypothesis; *not* historical Rmix | DPLL/CDCL/Resolution, algebra, paid definitions, shared-DAG and reconvergent proofs are candidate upper-bound controls, each needing exact legality | Show invariant survives ALL mixed rules [P2-C3], [P2-B1], not an affine-template-only restriction |
| Odd-charge cubic expander Tseitin, one variable per edge, four forbidden-local-parity clauses per cubic vertex, h vertices and 4h proper 3-CNF clauses; O(h log h) indexed bits | Haken/Urquhart and Ben-Sasson--Wigderson ordinary Resolution exponential bound; field-mismatched polynomial-calculus degree lower bounds | Characteristic-two XOR summation has a linear declared-semantic refutation; historical accepted-byte scope still restricted | No same-family all-mixed hardness |
| Bit pigeonhole, original bit variables for n+1 pigeons and n=2^ell holes; collision clauses, with established strict-3CNF facet encoding where specified | Pang 2026 Theorem 7.2(e), Res(XOR) exp(Omega(n)) and related constant-degree systems | Cook Extended Resolution and paid circuit definitions, shared DAG; only exact source-preserving translation is eligible | This restricted lower bound alone does not cover R_mix341 |

## Computation, source and resource audit

Published V8 JS `experiments/arc/lspv1_489_cross_gate_affine.js` blob `ee1516630c1cb97ef3bed1b7fe1fb8708a279bea` exhaustively enumerates 8, 1,024 and 2,097,152 affine vector predictors at `g=1,2,3`. Confirmed maximum agreement `3,9,27`; exactly `4,16,64` maximizers; maximum cross-coupled agreement `7` at g=2 (96 maps) and `21` at g=3 (1,152 maps). Published raw JSON blob `ec2e25de0ca62e19d01a1ac6a4d1c8ace5a3f62c`. Both were fetched again in full and compared byte-for-byte after publication. Negative assertions reject the bogus claims that cross coupling gives 8/16 matches in two gates or 27/64 in three gates, and reject any nonlocal global maximizer. Independently written Python exhaustive enumerator reproduced **all** listed counts, with local wall 1.88 s / user 2.19 s and process max RSS 95,664 KiB; this is one **finite experiment**, not a machine-complexity theorem.

No SAT source or proof certificate is generated in this theorem, so SAT/UNSAT/malformed-input and corrupted **proof** controls are not applicable to this enumeration. Those controls remain mandatory for native proof claims; LSPV-1/488 supplies separate such controls. The proof minimum intentionally excludes discovery; actual template search/representation, all pattern-mask allocations, copies, source reads, computation, code/output serialization, checking and process peak space are charged when this is used in an implemented upper bound. Enumeration on `g` gates examines `2^{g(2g+1)}` affine maps and is **not** an efficient all-input SAT algorithm. Ideal single-template agreement, weighted proof-DAG work, critical path and physical time/space are distinct quantities.

## ITERATE: implications and next genuine gaps

**New PROVED/RESTRICTED fact:** Cross-gate affine sharing cannot enlarge *one affine-template* agreement region; it incurs a sharp `7/9` relative penalty compared with the separable optimum. Therefore any proposed improvement to the prior single-template `3^g` ceiling must change the representation (multiple regions, nonlinear guards, assumption discharge, extension nodes), not merely introduce off-diagonal linear coefficients. This narrows [P2-F13], but does not close it.

**OPEN:** historical full accepted-byte Rmix341 grammar [P2-D1], mixed-rule normalization [P2-C3], truly superpolynomial worst-case minimum for every legal mixed proof [P2-B1], noncircular B3 [P2-B2]. Coordinate with LSPV-3 to test typed guard/discharge, LSPV-5 to seek legal nonaffine or GF(2) shortcuts, and retain LSPV-2/LSPV-4 Route A primary allocation.

P versus NP OPEN.


**Numbering collision reconciliation, 2026-11-07:** The existing different LSPV-1/489 unit-assumption-discharge result predates this independent affine-template audit. The latter is registered as **LSPV-1/490**; its immutable computational source/raw paths retain the original filenames `lspv1_489_...` and are identified by their exact blob SHA. This document supersedes only the same-author provisional cross-affine report, and does not overwrite the distinct /489 Resolution work.

## Publication and tracker reconciliation addendum | November 7, 2026 PST

**COMPLETE READBACK PASSED.** Unique /490 report blob `a39a9bd34658fa8fa1133eb77838f440c691b0fd` before this addendum; new numbered handoff blob `7fe94d650f1a8e4bf135f5ede6c23645f2ef024d`. Independently executed standalone V8 enumerator blob `ee1516630c1cb97ef3bed1b7fe1fb8708a279bea`, raw JSON blob `ec2e25de0ca62e19d01a1ac6a4d1c8ace5a3f62c`. Independently written Python code and JSON saved locally, with complete counts and process time/RSS in the local reproducibility package. The previously published provisional /489-CROSS names are historical duplicates of this proof, not replacements for the preexisting distinct /489 **ordinary Resolution unit-discharge** report.

Root `proof1.txt` was read completely and left unchanged at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`. Root `proof2.txt` was read completely at blob `0a5d4a1cf56a215669df7378140781ff588c9510`, 266,106 characters. Exact prewrite file saved under `research/agents/lspv-1/outbox/2026-11-07_1614_LSPV1_489_PROOF2_PREWRITE_EXACT.txt`; its blob SHA **equals** the previous proof2 SHA. New evidence entry added *only* under [P2-F13] with a current full-blob/SHA optimistic write, commit `6ac4bbcfd8259083c10ade48f06ba71c37120af3`, postwrite blob `bde21c80e484b8e2c475c0eb5433759edba8a2ca`, 267,826 characters. Exact full readback PASSED, and removing only the new appended entry reproduces all preceding text byte-for-byte. Coordination issue #3 comment `6715007293` was posted; direct GitHub comment fetch verified its complete body exactly.

Root `main.tex` blob `68188a24badda635a5983fda1c381cdb694fd497` returned **zero content bytes** both for an unrestricted fetch and for a bounded line-range fetch, so whole-file ownership safety could not be verified and the root was left unchanged. No historical R_mix341 accepted-byte checker was run. No real SAT lower bound, B3, complete native grammar, or full mixed-rule transfer is claimed. Exactly five existing agents, their two Route A / three Route B allocation and all schedules/weights remain untouched. **P versus NP OPEN.**
