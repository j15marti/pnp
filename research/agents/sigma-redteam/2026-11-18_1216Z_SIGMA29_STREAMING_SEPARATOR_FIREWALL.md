# SIGMA REDTEAM29: One-pass separator-state lower bound and exact QBF controls

**2026-11-18 12:16 UTC.** **Status:** PROVED/EXACT only under a deterministic one-way explicit-table streaming model; COMPUTATIONAL 33,092 primary and 196,887 independent exact assertions, zero failures; unrestricted SAT resource contraction OPEN; P versus NP OPEN. Independent mathematical review pending.

## PROPOSE / SEARCH
Adversarial directions: (1) test whether the newest PATHCUT-1 frontier-mask memory is reducible under one-way exact streaming, versus read-only random-access rereads; (2) compare same two-factor family under globally fixed witnesses, proper exists-forall-exists witnesses, and illegally independent per-factor witnesses; (3) use non-affine constraints, complete AND/OR/NOT traces, equivalent double-NOT circuits, constant-output varying traces and compact Skolem certificates; (4) use source-expanded and delayed hypothetical solvers, work-address and oracle controls.

Read current GitHub primary research: `research/agents/sigma-primary/2026-11-18_0303PST_SIGMA_PATHCUT_1.md` (exact restricted PATHCUT), `research/agents/sigma-redteam/2026-11-18_0957Z_SIGMA27_JOIN_TREE_QUANTIFIER_FIREWALL.md`, `research/agents/sigma-redteam/2026-11-18_1202Z_SIGMA28_UNIFORM_PROJECTION_GATE_TRACE.md` (commit `9b79170f1eada36d0f502b6b05248119166b5c66`). Primary literature: Yannakakis, VLDB 1981 https://www.vldb.org/dblp/db/conf/vldb/Yannakakis81.html ; Bhattacharya et al. 2020 https://arxiv.org/abs/2006.13712 ; Fortnow et al., JACM 2005 https://doi.org/10.1145/1101821.1101822 .

## Exact restricted theorem: one-way two-node path interface
Let `w>=1, p=2^w`. Given explicit A and B tables representing arbitrary unary relations `A(z),B(z)` on `z in {0,1}^w`, the conjunction has a valid two-node join tree and is satisfiable iff A intersects B. Suppose a deterministic exact one-pass machine reads the entire A table before the B table and cannot access A again. At the cut it **must retain at least p=2^w state bits**, tight via the membership mask.

**Proof:** For any two different A and A', choose position j in their symmetric difference and supply Bob the singleton B={j}. The two correct SAT answers differ, so A and A' must induce different states. There are 2^p possible A, so at least 2^p distinguishable states and p bits are necessary. This is the standard deterministic one-way INDEX / DISJOINTNESS argument, not new communication-complexity theory.

**Crucial escape:** In a read-only **random-access** input model, an algorithm can enumerate j, read A[j],B[j], and stop on intersection using O(w) index bits and O(p) indexed reads, even with no p-bit mask. Thus **no arbitrary SAT space lower bound follows**. It does not contradict the restricted PATHCUT positive theorem; it identifies the one-pass boundary for improvements.

## Same-family quantified and non-affine adversaries
For two shared-z factors R1(x,y,z),R2(x,y,z), the fixed-response formula `exists x,z forall y [R1 and R2]` differs from correct `exists x forall y exists z [R1 and R2]`. The latter differs from the unsound relaxed `exists x forall y [(exists z1 R1) and (exists z2 R2)]`.

Strict control: `x=0, R1=TRUE, R2=(z=y)`; reject x=1. Correct Sigma3 TRUE with Skolem `z(y)=y`, fixed-z Sigma1/Sigma2 FALSE. Non-affine false-positive: on three-bit z, A={000,001,010} and B={011,100,101} are individually satisfiable **non-affine** ternary relations, disjoint globally. Correct Sigma1/Sigma2/Sigma3 FALSE, locally re-witnessed Sigma3 TRUE.

Every random AND/OR/NOT gate input has a unique *complete* satisfying trace. Nonconstant internal traces can coexist with constant outputs, so placing all gate traces before y is invalid. Output-equivalent double-NOT padding preserves truth but changes trace structure.

## Actually executed reproducible results
Local package `SIGMA_REDTEAM29_PACKAGE.zip` contains full report, `audit.py`, `independent.py`, raw JSON, handoff, README and SHA-256 manifest. Stdlib-only deterministic rerun was byte-identical. ZIP integrity and seven SHA-256 file hashes verified. Package SHA-256 `e41c58582640bfad034b084d04c2a5b1f082b52b97e4d31722e2e57e66b6f0e6`.

Primary `audit.py` seed 202611181220: **33,092 assertions passed, zero failures**. All Alice profiles for w=1,2,3: 4/16/256 distinct states; 5,000 arbitrary table pairs, 3,767 with both relations non-affine; 1,200 indexed-reread controls; 2,400 exact quantified cases, 803 correct-Sigma3-true/fixed-z-false, 303 relaxed-Sigma3 false positives, 2,031 validated compact Skolem responses and 369 verified negative challenges; 420 gate DAGs (100 non-affine Boolean output functions), 3,360 unique trace checks and 420 equivalent double-NOT controls.

Independent `independent.py`: **196,887 assertions, zero failures**. Independently exhausts all 65,536 ordered pairs of Boolean two-factor relations of binary (x,y,z), finding 7,776 strict Sigma3-vs-fixed-z instances and 12,224 locally re-witnessed false positives. Also enumerates all 4/16/256 table states. These two benchmarks are different populations; do not add counts as if one benchmark. No asymptotic time lower bound is inferred from finite tests.

## Triple T/S/R, padding, source and oracle audit
Restricted PATHCUT-1 recurrence is `K'<=max(1.04,0.58,0.56+K/2)` and `L'<=max(0.5,L/2)`. Its time fixed point is **K=1.12**; K=1.10 gives K'=1.11 (an increase), K=1.12 gives equality. Strict L contraction requires L>0.5.

For reached hypothetical solver exponent K=3, source inflation N=n^1.01 and extra N^.04 guest decoding, charged original-input guest exponent is `1.01*(0.56+1.5+0.04)=2.121`, not nominal 2.06. A reached full-parent-size call costs n^3.03, defeating that *implementation* of contraction. Neither falsifies all possible compilers.

Work-address sample [0,1,2,1,2^30,0] uses T=6 and R=4 distinct addresses but maximum work-address 2^30. `R<=T` is not a workspace bound in the FLMV model. The Python audit did not measure native FLMV workspace. Indexed input rereads, table serialization, physical memory high-water mark, negative SAT answers, uniform source-to-child decoding, quantified advice and recursive closure must all be charged. The one-way lower bound is not a black-box oracle or unconditional source-reading SAT lower bound.

## Handoff
Attempt a uniform all-input, unpadded ordinary Circuit-SAT compiler producing certified path-cutset factors and genuinely half-size guest SAT encodings, while accounting for original input length, source-index access, child decoding, global x commitment, per-y shared z consistency, reached parent calls, all negative answers, and hereditary recursion. Either give an explicit source-indexed replay construction that beats one-pass 2^w masks with its actual time/space cost, or retain the mask and charge it. Validate under the same FLMV deterministic random-access Turing machine model. **P!=NP is not proved.**

VERIFICATION_SENTINEL_SIGMA29_STREAMING_SEPARATOR_20261118_1216Z
