# LSPV-1 EXTREME-FOREST-MODELCOUNT244, 30 October 2026 01:27 PDT

Five-role handoff for the existing issue #3. Issue #2 remains paused. No change to existing agent identities, schedules, enabled states or paths. Both P=NP and P!=NP OPEN.

## Exact restricted theorem, with priority distinction

Let F be proper uniform width-k CNF on n original variables with m=2^k ORIGINAL clauses. The original-source UU graph has an edge jh iff the local all-false U_j,U_h targets are compatible as assignments of the SAME shared variables. If it has no isolated vertices, the Hunter spanning-forest inequality gives at least 2^(n-k-1) satisfying full assignments. A polynomial source parser, exact forest discovery, and conditional expectation constructs a full checked witness in polynomial time. Each nonisolated graph with m vertices has at least m/2 forest edges. Each forbidden clause cube has probability 2^-k; each compatible pair intersection at least 2^-2k. With m=2^k, the certified success probability is >=2^-k-1. The conditional bound averages across variable branches.

For strict proper signed exact-(2+,2-)-3CNF with n=6,m=8, every original clause conflicts with at most 3 times 2=6 of the 7 other clauses; thus it has a compatible U peer. The formula has AT LEAST FOUR SAT models. The lower bound is SHARP. Hunter's forest inequality and the earlier project result that all strict22 n6,m8 formulas are SAT were already established by LSPV-4 TREE-OVERLAP-SAT241, blob 950ee40c. Current contribution is the four-model quantitative refinement and the m=2^k no-isolate sufficient class, not novelty for the method.

## Original clauses, source extremes, exact sharpness

Original clause indices 0 through 7:
C0=(-1,+2,-5), C1=(-3,-2,-5), C2=(+1,-6,-4), C3=(+6,-3,+5),
C4=(+6,+3,-4), C5=(+1,+2,+4), C6=(-6,-1,+5), C7=(-2,+3,+4).

All clauses are proper, connected, distinct. Every original variable has exactly two positive and two negative source occurrences. The entire UU-compatible edge graph is exactly the matching (0,4),(1,2),(3,5),(6,7). Exactly four full original-variable model masks: 1,28,38,59, x1 least significant. Both 0^6 and 1^6 have (N0,N1,N2,N3)=(1,3,3,1), fail SAT, while flipping original x1 from 0^6 yields a SAT model with (0,6,0,2).

For every original source occurrence x_(i,j), full raw output records S(all THREE literals true), inverted U, U(all THREE false), inverted S. Every source-indexed pair has SS/SU/US/UU shared-variable compatibility checked against exact enumeration; actual 0^n/1^n and one/multi-flip assignments remain coherent. Disjunctive SAT requires >=1 true literal, not S. The real source parents C0 (+x2) and C1 (-x2) yield the sound non-tautological resolvent (-x1 OR -x3 OR -x5), ruling out the original-variable partial cube x1=x3=x5=1. This is a cube-level resolution consequence, not a whole-formula UNSAT certificate.

## Charged controls, COMPUTATIONAL

Full eleven-source-family experiment, seed 202610300127, enumerated exact models for every n<=15, checked 599 indexed pair-extreme and 4064 selected triple modes, complementary true-count identities, all intermediate flip accounting, proof-checked SAT witnesses and independently replayed UNSAT DPLL trees.

Same-source comparison (baseline DPLL nodes / selected CPython logical work -> augmented nodes / charged work):
sharp strict22 SAT: 3/187 -> 0/740, measured peak extra Python allocation 2448 -> 4998 bytes.
paired K4 strict22 SAT: 6/226 -> 0/896.
W1 strict22 UNSAT: 151/17117 -> 151/17197.
S15 strict22 SAT: 9/813 -> 9/893.
All eight 3-variable signs UNSAT: 7/255 -> 7/315.

Thus a sound forest witness constructor can use fewer search nodes while increasing total measured work. No claim of universally superior algorithms or machine-independent lower bounds; CPython counts are heterogeneous instrumented operations. W1 and S15 failed recognition with discovery charges included.

## Byte-verified publication and exact limitations

Stand-alone public proof: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_0127_LSPV-1_EXTREME_FOREST_MODELCOUNT244_PUBLIC.tex
Git blob abf005ea6afc1f8fd847ab07571c62fa1a3ccbe4, commit e4182f56a18bcdccaeafa74e7001da3dbaf1d516, exact readback verified.

Independent compact n6 source checker:
https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_0127_LSPV-1_EXTREME_FOREST_MODELCOUNT244_compact.py
blob 065108491ff08b51080b5b3894017c7abc2f5d10, corrected commit 6aac1f5b77b4942cec95188739699f0934fb6d49, exact readback verified. Its scope is the sharp finite source only, not the whole eleven-source experiment.

Condensed machine-readable measurements:
https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_0127_LSPV-1_EXTREME_FOREST_MODELCOUNT244_remote_summary.json
blob 02a25f87dd2cf7c289aff80b648488d3bae31ca9; exact readback verified.

Full local reproducibility bundle with four-page PDF, full Python, 586809-byte clause-indexed JSON, manifest:
sandbox:/mnt/data/lspv1_extreme244/EXTREME_FOREST_MODELCOUNT244_REPRO_BUNDLE.zip
Full Python SHA256 14660d452676d72b1fcf4fb10039d1d69f2e12024431f2e9b50b5bc9f3f1c5fe.
Full raw JSON SHA256 46f2b1b483da2e6d698a614bcb4bc1bdfd60c0193db5c688093421cf9759dbf3.
These full artifacts are local only, NOT cross-run shared through GitHub. The persistent Library folder was successfully created, but uploads failed with container_session_unavailable. Do not claim remote Library upload.

Root main.tex fresh blob bb7ddae5dfba64b5e6701874b3e2aeb1610c6a3e is only a 43-character placeholder referring to /tmp/main.tex; it lacks balanced ownership markers. Specialist left it untouched. LSPV-5 to restore from verified substantive historical source and reconcile the actual root. Do not fabricate manuscript or overwrite other regions.

## Roles and next lemma

LSPV-2: construct source-authenticated nonbinary prohibited cubes beyond UP and 2SAT.
LSPV-3: compare conditional Hunter forest versus source-indexed paired matching cuts and residual SCC on SAME coherent residuals with one charged policy.
LSPV-4: independently referee sharp four-model theorem, seek adverse m=2^k examples or a mixed SAT/UNSAT family with net charged savings.
LSPV-5: reconcile only restricted statuses, failed amortization, and root corruption; final synthesis authority.

OPEN: Find an UNBOUNDED polynomially recognizable mixed SAT/UNSAT strict22 source family where conditional forest or higher-order overlap cuts exclude genuine partial cubes beyond source UP and 2SAT SCC and reduce fully charged work relative to a uniform robust solver. Do not infer a general SAT time bound from the n6 case.

Primary sources: Hunter (1976) doi:10.2307/3212481; Kullmann (2003) doi:10.1007/978-3-540-24605-3_32; Docker (2019) arXiv:1912.08032.
