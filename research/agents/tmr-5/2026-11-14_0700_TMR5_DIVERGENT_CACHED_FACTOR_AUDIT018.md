# TMR-5/018: divergent-head cached factor, independent peer audit and falsifier

**Date:** November 14, 2026, 07:00 PST (America/Los_Angeles). **Repository:** j15marti/pnp main. **Role:** TMR-5 machine bottleneck redteam and canonical manuscript synthesis. **Status:** Peer TMR-4/021 independent mathematical support PROVED/RESTRICTED under its exact hypotheses; NEW TMR5-CF18 CANDIDATE/RESTRICTED pending TMR-1/TMR-4 independent review; finite evidence COMPUTATIONAL; all-machine superpolynomial 3-SAT bound OPEN.

## Peer theorem actually reviewed

I independently checked TMR-4/021's finite all-transition certificate, separately from its executed source. Fix two real writable tapes B,C with a blank-preserving fixed finite map f and fixed integer data displacement d:

$$
B[j]=f(C[j+d])\quad\text{for all }j,\qquad
\delta=h_C-h_B-d\in D.
$$

The offset of *stored contents* d is constant; the actual head separation delta may vary in a finite, control-tracked set D. On aligned heads (delta=0), B's scanned symbol equals f of C's physically scanned symbol, and paired writes must satisfy w_B=f(w_C). On divergent heads (delta nonzero), the original TMR-4/021 certificate requires all transitions to be independent of B's scanned symbol, B to remain unchanged, and C writes to satisfy f(w_C)=f(c). Thus both updated cells preserve the factor. Source-head reads and every other tape action are copied. A physical blank dummy B tape keeps all its head moves and visited-cell charges, even though B symbol information is reconstructed or ignored. Starting from standard blank tapes or a separately charged prefix, initial binding, every concrete and abstract successor and SAT/UNSAT/MALFORMED terminal labels are exact. The full-tape factor supplies reverse replay. In this certified class, time and peak visited writable cells are equal on the same input and execution. The original peer source was inspected, not independently executed natively; the review is a symbolic induction, not promotion of finite tests to proof.

## New TMR5-CF18 finite-control cached-symbol certificate

A stricter B-blind condition is NOT necessary. Allow the original machine to branch on the scanned B symbol while B and C heads are separated, provided a finite register of that symbol is inductively authentic.

Assume the same fixed whole-tape factor, finite head-separation control, all charged physical heads, and the following finite, all-symbol transition certificate:

1. Upon leaving aligned heads, B's head stays at its present cell. Set a finite abstract-control register R to the post-write scanned B value f(w_C), obtainable from the currently scanned C symbol and legal paired write.
2. During all divergent steps, B's physical head remains stationary and B's scanned cell is never changed. Every C write satisfies f(w_C)=f(c). The original program may nonetheless branch arbitrarily on B's scanned symbol; the abstract finite transition reads R, not any uncharged remote C cell.
3. Every divergent step updates actual head separation by physical movement and keeps it inside an explicitly finite certified set. Upon returning to aligned heads, discard R and use the locally scanned value f(c).
4. Preserve every original source read, work-tape action, control/output label and visited-cell footprint. All assertions are finite transition-table checks, not presumed properties of all SAT programs.

**Candidate theorem:** For any fixed finite total deterministic multitape program satisfying this certificate from its initial blank configuration, a physically implementable finite-state quotient erases B symbol contents, retains B's real dummy head and visited cells, and uses R only during divergence. Every concrete unit transition is represented by exactly one abstract unit transition, and every related abstract transition reconstructs the corresponding concrete transition. Therefore for each source x,

$$
\boxed{T_{\widehat A}(x)=T_A(x),\qquad S_{\widehat A}(x)=S_A(x).}
$$

**All-step proof.** Initially f(blank_C)=blank_B ensures the whole-tape relation. Aligned transitions reconstruct B from C's physically scanned cell and preserve the paired post-write relation. When departure makes the heads divergent, stationary B and the known paired write establish R=B[h_B]. During divergence, unchanged B cell/head preserve R, and fiber-preserving C writes preserve every global B/C cell relation. Thus any original B-dependent branch is replayed using R without a remote lookup or extra TM step. Upon return, aligned scanning recovers B from the current C cell. Every extra tape and source transition was copied exactly. A converse concrete state can be reconstructed mathematically from full C contents through f (this reconstruction is a proof relation, NOT a runtime abstract-machine operation). Both labels and malformed outcomes are preserved. The finite R is a constant-size control-state refinement, not an unbounded-word unit operation. This strictly extends B-blind DHF21, but remains an optional certificate for a narrow class, not a universal solver theorem.

## Concrete counterexample, physical charges, and repair

Use E3, the 3-bit-per-clause proper 3-CNF language over fixed variables x,y,z. A three-bit signature excludes exactly that Boolean assignment; lengths not divisible by three are malformed. One locally moving read-only source head and two local writable heads operate with C alphabet 0,1,2,3, B alphabet 0,1 and f(c)=c mod 2. A first physical source scan records input-one count modulo four in C[0], parity in B[0]. At the source right marker, C moves one cell right and B remains at cell 0. In that divergent state the ORIGINAL program reads B[0] and writes C[1] to (C[1]+2) mod 4, a same-fiber update for ALL four possible C symbols. If the scanned B[0] is 1, the source head makes a charged right-to-left-to-right trip. Then C rejoins B, the source head rewinds, and a finite-control eight-signature mask correctly classifies SAT, UNSAT or MALFORMED.

The old B-blind criterion correctly rejects this particular original program because the divergent branch DOES depend on B. CF18 accepts it: R is copied before C moves and B remains parked. Naively replacing the divergent scanned B symbol with f(C[1]) is WRONG. For valid SAT input x=001, real B[0]=1 and physically scanned C[1]=0. The original program takes 24 charged steps; the invalid quotient takes 16, omitting eight real transitions. On x=1 (MALFORMED), the corresponding costs are 14 versus 10. The bad quotient fails same-program step simulation. Its shorter behavior may nonetheless describe another legitimate E3 algorithm; never erase genuine cheap algorithms from an all-machine lower-bound argument.

For input bit length L and total input parity z(x), both the actual source program and its CORRECT cached quotient have

$$
\boxed{T(x)=3(L+1)+4+2(L+1)z(x)},\qquad \boxed{S(x)=3}.
$$

Space includes real visited cells B[0], C[0], C[1]. All input rereads, B/C movements, parsing and final output transitions are included. There is no promise of an all-input *general* 3-SAT polynomial solver; the linear classifier is limited to E3.

## All-edge Bellman potential, no hidden oracle

Let n=L+1 and h be the actual input-head coordinate. Define the following SOURCE-FIXED mathematical potential on the complete restricted abstract phase graph, where z is the parity of the immutable source:

$$
\begin{aligned}
\Phi(\mathrm{SCAN},h)&=3n+4+2nz-h,\\
\Phi(\mathrm{BRANCH})&=2n+3+2nz,\\
\Phi(\mathrm{DL},h)&=3n+2+h,\\
\Phi(\mathrm{DR},h)&=3n+2-h,\\
\Phi(\mathrm{JOIN})&=2n+2,\\
\Phi(\mathrm{REWIND},h)&=h+n+1,\\
\Phi(\mathrm{PARSE},h)&=n-h+1,\\
\Phi(\mathrm{HALT})&=0.
\end{aligned}
$$

Every charged reachable abstract edge satisfies Phi(a)=1+Phi(a'), including the two parity branch choices, left/right endmarker reversals, source rewind, parsing and terminal label. Phi(start)=3n+4+2nz is LINEAR; its source parity is used to *verify* the potential and is NOT supplied to the abstract program as a free oracle. No superpolynomial abstract initial value and no unrestricted abstract-machine coverage have been established.

## Executed evidence and exact reproducibility

New, independently authored standalone CommonJS was executed in hosted V8 before upload, NOT under native Node. Exhaustive binary sources at lengths 0..11 plus twelve longer, SAT/UNSAT and malformed controls produced 4,107 complete paired concrete/cached runs, 199,871 matching fully charged transitions and Bellman equalities, 589 SAT, 4 UNSAT, 3,514 MALFORMED and zero failures. The test also checked sixteen all-symbol factor obligations and three hostile invalid remote-substitution examples. The source is a restricted physical current-cell emulator, not a general arbitrary-TM compiler. A separately authored native CPython reimplementation was ACTUALLY executed locally, with the identical 4,107 / 199,871 / 589 / 4 / 3,514 counts and three counterexamples, zero failures, but remains LOCAL-ONLY and is not part of the published reproducibility claim.

GitHub paths:
- research/agents/tmr-5/2026-11-14_0700_TMR5_DIVERGENT_CACHED_FACTOR_AUDIT018.md (report)
- experiments/tmr/tmr5_cached_divergent_factor018.cjs (executed hosted source)
- results/raw/tmr/2026-11-14_0659_TMR5_CACHED_FACTOR018_RAW.json (immutable raw)
- research/agents/tmr-5/handoff.md (compact current handoff)

## Whole-team synthesis, primary literature, and next obstruction

TMR-1/020's multiple-source-head delayed-INDEX bound and TMR-3/019's stronger unlimited-workspace locality bound concern a post-preprocessing EXTERNAL INDEX service. TMR-2/020 provides an exact E3 single-sign-bit sensitivity characterization and an O(L) finite-state parser, not superlinear SAT hardness. TMR-4/021 and the present CF18 are optional representations of actual fixed-program computations, with cost-exact replay but without a required superpolynomial Bellman potential. Horn/2-SAT, Gaussian elimination on XOR/Tseitin, bounded-treewidth DP, products, sharing, padding, renaming, auxiliary variables, compact circuits, full caching and recomputation remain possible for unrestricted SAT. None is universally excluded by these restricted statements. The strongest surviving implication is **verified invariant plus complete charged simulation implies a restricted cost-exact quotient**, not a new all-machine lower bound.

Unresolved central arrow: every one fixed correct uniform all-length deterministic 3-SAT decider A, for every integer k>=1, C>0 and L0, must have some VALID encoded 3-CNF F with |F|>=L0 and T_A(F)>C(|F|+1)^k. Hard inputs may depend on A,k,C,L0. Arbitrary polynomial workspace is allowed and must be counted on that same machine. A universal late query, finite-state factor, prescribed proof calculus or assignment count is NOT a necessary property of A. No relativization, algebrization or natural-proofs restriction is silently assumed away. The fully correct general polynomial-algorithm alternative remains legitimate. **P versus NP remains OPEN.**

Primary literature freshly checked at actual model scope:
1. P. Cousot and R. Cousot, Abstract Interpretation, POPL 1977, pp. 238-252, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml . Methodological, not a SAT lower bound.
2. E. Clarke et al., Counterexample-Guided Abstraction Refinement, CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15 . Genuine concrete paths must not be called spurious.
3. L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6), 835-865 (2005), https://doi.org/10.1145/1101821.1101822 . Its n^c time exclusions require sufficiently small simultaneous workspace, not all polynomial workspace.

**Preflight:** First read and rechecked the TMR replacement directive, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Fully read proof1.txt (28,714 chars, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and recovered full proof2.txt via authentic blob (1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c, rather than misreading a blank file endpoint). Read full canonical main.tex via blob f0054c990e11602b4b60ead3bccffa73f11d0d7b (2,536,131 chars), issue #3 through TMR-4/021, AGENTS.md, CODEX.md, repo pnp-research SKILL.md, five newest TMR handoffs, original TMR-1/020, TMR-2/020, TMR-3/019, TMR-4/021 reports and relevant code/raw. Historical findings and old checker counterexamples untouched.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to root proof1/proof2. Canonical main.tex belongs to TMR-5 and receives only a conservative new TMR-5 synthesis insertion, retaining all old bytes. No scheduled tasks created, revived or modified.

**ONE NEXT TARGET:** Obtain independent TMR-1/TMR-4 review of CF18, then test a B-dependent branch where the parked B cell changes or moves, to delimit the next necessary physically charged reconstruction. The unrestricted all-exponent SAT-processing lower bound remains OPEN.

END_OF_REPORT::TMR5::018::2026-11-14_0700_PST
