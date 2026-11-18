# CLOCKADAPTIVEPOLY31: adaptive transcript plus branch-polynomial canonical section
**2026-11-18 00:35 PST. PROVED/EXACT restricted semantic obstruction using a classical algebraic principle; independent mathematical review OPEN. P versus NP OPEN.**

## Named dependency, proposed mechanisms, falsifiers
The load-bearing dependency from CLOCKASYMTRANSFER24 is universal source-MCSP NO-image exclusion while retaining compressed YES-only witnesses, a joint fixed-PH verifier and near-linear headerless one-tape compilation. The present run tests three mechanisms: (M1) adaptive raw-source probes selecting branch-specific polynomial sketches; (M2) source-selected affine/hash features with arbitrary nonlinear target decoding; (M3) global high ANF degree produced by source-adaptive branch selection. Predeclared falsifiers: (F1) the reconstructed source changes an adaptive probe address; (F2) polynomial degree is accidentally measured before necessary original-source provenance or after omitting the branch constraint; (F3) nonlinear postprocessing secretly reads raw source bits; (F4) a source output has no representative within the claimed support bound. We address F1-F4 for precisely the stated model, not arbitrary full-source nonlinear quotients.

## Theorem ADAPTIVE-TRANSCRIPT-POLYSECTION31
Fix N=2^n. Let an arbitrary deterministic decision tree query at most q individual authentic source bits f[i], with each next address permitted to depend on all previous addresses and replies. A complete transcript tau selects an arbitrary finite collection of Boolean ANF polynomials P_(tau,1),...,P_(tau,B(tau)) in the original N source bits, of degrees d_(tau,l). The output is

H(f)=Phi(tau(f), P_(tau(f),1)(f),...,P_(tau(f),B(tau(f)))(f)),

where Phi is any fixed deterministic function; the selected polynomials and Phi need not have efficient descriptions or evaluations for this *semantic* statement. Let D_tau=sum_l d_(tau,l), including any source dependence occurring inside the selected polynomials, and D=max_tau D_tau over reachable branches.

For every f there exists one g satisfying

tau(g)=tau(f), P_(tau,l)(g)=P_(tau,l)(f) for every l, H(g)=H(f),
wt(g)<=q+D_tau,
CC(g)<=C(n+1)(q+D_tau+1).

No assumption of a position-independent or regular address schedule, low global ANF degree of H, a linear decoder, or an efficient source-reconstruction algorithm is needed.

### Proof
Fix f and its complete transcript tau. Let I be the set of distinct probed source positions, of cardinality r<=q. Pin each f[i] for i in I; every source word respecting these pins replays tau exactly by induction on decision-tree depth, including adaptive and repeated addresses. Substitute these pinned bits into all branch polynomials, and regard the resulting B polynomials on the unpinned coordinates U. Their degrees cannot increase; total degree D'<=D_tau. Fix the realized feature-value vector v. Among all unpinned assignments attaining v, choose one z with inclusion-minimal 1-support S. Consider its fiber indicator Q(z')=product_l (1+P_l(z')+v_l), over GF(2). Set all unpinned coordinates outside S to zero. By minimality, the resulting Boolean polynomial is 1 exactly at the all-ones point of {0,1}^S. Its unique multilinear ANF is product_(i in S) z_i, of degree |S|, whereas substitution cannot increase degree above D'. Hence |S|<=D'. Add the r pinned ones (at most r), obtaining wt(g)<=r+D'<=q+D_tau. Point-DNF on the at most q+D_tau nonzero truth-table entries yields an ordinary n-input circuit of size at most C(n+1)(q+D_tau+1). The pins make every adaptive query replay, the feature vector v is identical, and Phi therefore produces the exact same output. QED.

This is a quantified strengthening *for adaptive raw probes* of the earlier project THRES-POLYFIBER10 sparse polynomial section: the decision-tree provenance costs q additively rather than the sum of potentially very large degrees of separately encoded seed-output coordinates. Its algebraic sparse-support ingredient is classical. It does NOT claim discovery of a new general Chevalley-Warning theorem.

## Stronger theorem: ALL attained transcript-feature fibers have large mass
For each fixed *reachable* transcript tau with r distinct probed addresses, and for each attainable complete feature vector v, let B_(tau,v) be the set of authentic N-bit source words that replay tau and have P_tau=v. Its size satisfies the **uniform** bound

|B_(tau,v)| >= 2^{max(0,N-r-D_tau)}.

**Proof:** Pin the r queried addresses as in the sparse-section proof. On the remaining M=N-r Boolean variables, the fiber indicator Q(z)=product_l (1+P_(tau,l)(z)+v_l) is nonzero, has ANF degree at most D_tau, and equals 1 precisely on the desired completions. The classical binary Reed-Muller minimum-weight inequality (equivalently the basic finite-field polynomial nonzero-support bound) yields at least 2^{M-D_tau} solutions when D_tau<=M, and at least one solution in the remaining case. Every completion replays the exact adaptive transcript because all queried replies remain pinned. QED.

Let U(n,s) be the number of n-input Boolean functions of ordinary circuit size at most s, with log2 U(n,s)<=C_0 s log(n+s+2) by standard circuit counting. When

s>=C_1(n+1)(q+D+1) and N-q-D>log2 U(n,s),

**EVERY reachable output label has both a source YES_s preimage and a source NO_s preimage**:
H(Y_s)=H(NO_s)=im(H).

The first part follows from the sparse section; the second follows because every attained output label contains at least one attained transcript-feature cell of cardinality larger than the entire source YES_s class. This is stronger than merely exhibiting one mixed fiber. For s=N^beta with fixed 0<beta<1 and q+D=o(s/n), both inequalities eventually hold. If D>=N-q, the mass bound becomes one and is not strong enough for this conclusion.

## Promise and cofinal consequence
Let Y_s={f:CC(f)<=s} and NO_s={f:CC(f)>s}. If s >= C(n+1)(q+D+1), then H(Y_s)=im(H), and any existing source NO image collides with a source YES image; exact two-sided MCSP promise preservation fails. Under the additional Reed-Muller mass inequality N-q-D>log2 U(n,s), every single attained label is mixed, as proved above. If all source functions are YES at a finite n, the NO-collision sentence is vacuous. For s=N^beta with fixed beta<1, NO sources exist for all sufficiently large n by standard circuit counting.

For a cofinal family with 0<lambda<1, q_j<=N^(a lambda^j+o(1)), branch feature count B_j<=N^(b lambda^j+o(1)), and all branch polynomial degrees <=N^(delta+o(1)), if delta<beta then any fixed j with max(a lambda^j,b lambda^j+delta)<beta eventually forces saturation. This j is independent of any later conjectural PH-decoder clock exponent. All counts refer to the actual selected *intermediate* feature bits, not merely the shorter serialized target.

For affine branch sketches, every d_l<=1, so the simpler bound wt(g)<=q+B follows even if an arbitrarily complicated seed-dependent matrix and nonlinear final decoder are used.

## Controls and sharpness
Tight example: two distinct adaptive probes fix source bits 0,1 to 1, and one selected polynomial is f[2]f[3]f[4] of degree 3. The corresponding transcript/feature output requires five source ones; q+D=2+3=5 is attained. A high-global-degree control chooses q probe bits and returns the unprobed bit f[q] iff all probes are 1, otherwise 0. Every branch polynomial has degree at most 1, while the complete output H(f)=product_(i=0)^q f[i] has global ANF degree q+1. The finite N=8 audit verified q=5 and global degree 6. This defeats using final output ANF degree as a substitute for measured *branch* degree.

The theorem does NOT cover branch selection by an arbitrary full-source function, extra unreported source-dependent provenance, nonlinear features of large branch degree, an independent random-seed soundness claim, or arbitrary postprocessing that accesses the original input again. An equality-to-a-nonuniform-high-circuit-complexity source word is an existential counterexample to a generic all-functions canonical-section claim, but no efficient uniform compiler is inferred from that example.

## Full source-to-target ledger, gates
Source authentication: exact N original truth-table bits, ordered as addresses 0..N-1. Decision-tree queries: at most q semantic random-access bits; random access is NOT automatically legal on a one-way tape. Feature acquisition: potentially full-source scans with unspecified polynomial descriptions, construction, time and space, so an actual uniform near-linear one-work-tape compiler is OPEN. Target serialization: output Phi length unspecified and must be charged in a real construction. Supplied-circuit equality: fixed-PH membership NOT established for arbitrary branch polynomials, and no PH-to-one-tape transfer is claimed. The sparse-section argument is existential/nonuniform; finding the representative, its polynomial coefficients and all address choices is not free in a physical execution.

Four gates: DISJ NOT APPLICABLE, no general SAT circuit lower bound; relativization SCOPED combinatorial conclusion only, unrestricted P-vs-NP OPEN; simultaneous DTISP FAIL for promise-pure use of the covered family, full same-machine implementation OPEN; deterministic configuration counting NOT APPLICABLE as a runtime lower bound, no declared total machine. Algebrization and Natural Proofs barriers are not bypassed. Existing Partial-MCSP, histogram, q-query, parity, free-seed, exceptional-seed and all-decoder controls retained. /341 remains FAIL as full UNSAT authority; /386 remains RESTRICTED.

## Computational audit and independent reproduction
Executed local standard-library Python audit seed 202611180035: 132 deterministic seeded models on N=4 and N=8 original source-bit dimensions; 21,312 exhaustive source/section pairs, 87,438 assertions and zero failures, including 1,922 exact reached transcript-feature fiber-mass checks. Checked adaptive transcript replay, branch feature equality, final nonlinear output equality and wt<=q+D in all cases, plus exact tight q=2,D=3, pinning necessity and global-degree-six controls. Full executed source SHA256 d7a1c122c5875456232832615c05af285a364e1e40116f4bb1260425b7eda454; executed-results JSON SHA256 aa193996b07d17d285233706f69518fef67bf7587ce11a3b6f1804fa188bcba9. A distinct compact reproducer was independently executed for 256 inputs, 1,024 assertions, 0 failures; its source SHA256 ce2f8156abc7233911d896995785bef736f762bf8ede1e4093a6b2023730205a. Full local audit and raw are NOT claimed to be the GitHub compact script.

No local Git checkout/preflight was available: container git ls-remote failed network name resolution. Research recovered via connected GitHub main reads. Five TMR manuscripts/schedules and retired trackers untouched. Independent review open; finite tests do not prove the asymptotic result.

## Corpus and original sources
Relevant recovered main: LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, K_ELIMINATION_TRANSFER4, SOURCEQUERY_SYNTHESIS10 and PUBLICSEED_PLOTKIN14; clock histories CLOCKSAT1/CLOCKFEATURE5/CLOCKSEED9/CLOCKEXCEPT10/CLOCKPARITY12/CLOCKHIST18/CLOCKMIXEDCORE17, CLOCKASYMTRANSFER24, CLOCKRMFIBER25, CLOCKMONOCHAIN26, CLOCKAUTOMATON27, CLOCKDFAO28, CLOCKSLP29, CLOCKRESIDUAL30; THRES-POLYFIBER10 is explicitly credited as prior sparse-polynomial work. Followed 2026-11-15 end-to-end directive, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; surveyed latest main and TMR issue #3 updates. No exact duplicate for the additive adaptive-transcript theorem found in targeted search. Primary literature: Cheraghchi et al., STACS 2021, https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; Warning's 1935 finite-field zero-count principle and Reed-Muller minimum-distance principle, e.g. Carlet, Boolean Functions for Cryptography and Coding Theory, https://www.math.univ-paris13.fr/~carlet/book-fcts-Bool-vect-crypt-codes.pdf . No claim of new algebraic priority.

**ONE NEXT: HIGH-BRANCH-DEGREE-PURE32.** A candidate must escape the additive q+D sparse section by genuinely high branch-total degree while satisfying *both* asymmetric short YES-image witnesses and universal NO exclusion, a one-fixed-PH supplied-circuit equality predicate, and an authenticated, fully costed headerless one-tape compiler. Do not infer a hard fiber from high degree alone. P versus NP OPEN.
