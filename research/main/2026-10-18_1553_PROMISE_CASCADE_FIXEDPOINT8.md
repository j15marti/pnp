# PROMISE-CASCADE-FIXEDPOINT8 | 2026-10-18 15:53 Asia/Seoul

**Status:** PROVED/EXACT elementary theorem under its explicit partial-function model; pending independent review. Computational finite control separately marked. No P-versus-NP separation. P versus NP remains OPEN.

## Inputs and workflow: propose -> search -> build/decide

Read the latest currently published work: research/main/2026-10-18_LOSSY_PROMISE_CASCADE6.md; research/main/2026-10-18_PARTIAL_SAMPLE_WEDGE7.md; research/main/2026-10-18_ASYMPTOTIC_CONE5.md; research/main/2026-10-18_K_ELIMINATION_TRANSFER4.md; research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex; research/agents/clock-gate/2026-10-18_1510_CLOCKFEATURE5.tex; research/agents/resource-directsum/2026-10-18_1520_RESOURCE_GAUGE5.tex and its errata; research/agents/magnification-redteam/2026-10-18_1433_MAGRED_HASHSTREAM4.md and 2026-10-18_1340_MAGRED_TAPEFUSION3.md; and root main.tex (last update 15:16 KST). Root main is owned by other proof spines and was not changed.

Proposed three combinations BEFORE selecting a construction:
(A) source-adaptive Partial-MCSP anti-checker + lossy promise cascade + recovered cofinal K absorption;
(B) nonlinear image-label quotient + jointly low verifier + near-linear one-tape source sweep;
(C) MCSP/Gap-MCSP threshold/slope transport with fully charged one-work-tape fusion.

Primary literature checked: Cheraghchi-Hirahara-Myrisiotis-Yoshida, STACS 2021 (randomized two-sided error on one work tape with one-way read-only input); Oliveira-Pich-Santhanam, Theory of Computing 2021 (anti-checkers and **circuit**, not one-tape, magnification); Hirahara, FOCS 2022 (randomized NP-hardness of Partial-MCSP). Relevant published sources are linked below.

## NEW THEOREM: ADAPTIVE-PARTIAL-CASCADE-FLOOR1

Fix a constant beta>0 and original truth-table length N=2^n. Consider ANY (even computationally unbounded, randomized, source-adaptive) cascade that on a promised source input produces a well-formed partial function P_j consisting of m_j consistently labeled, distinct points of a Boolean domain of address width n_j <= N^{o(1)}, for each fixed stage j. Let output serialization length be L_j >= m_j. The output's target is ordinary Partial-MCSP with size threshold t_j.

**Universal interpolation premise:** For a standard complete basis there is an absolute C such that each valid partial table P_j admits a circuit of size at most C(m_j+1)n_j. A point-indicator DNF for all positively labeled points proves this.

**Necessary threshold-capacity inequality:** If a promised source NO must map to a NO of Partial-MCSP[t_j] with positive probability, then some possible output must satisfy C(m_j+1)n_j > t_j. Therefore, for t_j=N^{tau_j+o(1)} and n_j=N^{o(1)}, the output size must have exponent at least tau_j-o(1). In particular if L_j<=N^{a_j+o(1)}, a necessary condition is

    tau_j <= a_j   (asymptotically, to within vanishing slack).

This holds regardless of how the sample points were selected, including full source-adaptive anti-checkers, and regardless of source Hamming-distance promises. It does not impose any runtime assumption.

**Cofinal no-go:** Suppose there are constants beta>0 and 0<lambda<1 such that for every fixed j,

    t_j >= N^{beta-o(1)},
    L_j <= N^{lambda^j+o(1)},
    n_j <= N^{o(1)}.

Choose a single fixed j with lambda^j<beta, possible since lambda^j tends to zero. Then the interpolation bound gives circuit size <= C(L_j+1)n_j = N^{lambda^j+o(1)} < t_j. Consequently EVERY well-formed possible partial-function output is a YES instance of the target. A promised source NO cannot be preserved even with tiny positive probability, contradiction. Therefore **a repeated Partial-MCSP sampling cascade retaining an essentially fixed original size threshold cannot cofinally contract target length.**

This is an unconditional NO-GO **only** for stages whose target is an ordinary partial-function consistency problem with subpolynomial-in-N address width and explicit well-formed labeled examples. It does NOT cover arbitrary nonlinear image languages, exponentially wide implicitly addressed samples, or reductions that themselves compress the circuit-size witness budget.

### Parameter accounting and controls

For output exponent a_j and threshold exponent tau_j the universal capacity condition is tau_j <= a_j. Thus any viable cofinal partial-sample cascade with a_j <= lambda^j necessarily has tau_j <= lambda^j+o(1). In particular it MUST lower the effective Partial-MCSP circuit budget; pure lossy sampling without witness-budget descent cannot replace THRESHOLD-DESCENT1.

Numerical exact-rational illustration: beta=4/5 and lambda=9/10. At stages j=1,2,3 output upper exponents are 9/10, 81/100, 729/1000. Since 729/1000 < 4/5, stage 3 is asymptotically incapable of producing a NO Partial-MCSP instance with t_j>=N^{4/5-o(1)}.

Finite exhaustive interpolation control: checked all 3^8=6,561 partial functions on 3-bit inputs, each input address labeled absent/0/1. Construct the DNF of positively labeled points and test agreement on every defined coordinate. 6,561/6,561 passed; 256 fully defined cases; 1 empty case; 0 disagreements. Computational control only; theorem is the analytical interpolation proof.

## Source promise, anti-checker and model reconciliation

1. The previously established PARTIAL-SAMPLE-WEDGE7 has two barriers for **source-independent uniform coordinates**: exact MCSP demands Omega(N) samples due to a one-coordinate YES/NO boundary; same-threshold Gap-MCSP requires tilde-Omega(N^{max(beta,1-beta)}) samples due to sparse hard tables and interpolation. RETIRE naive random coordinate sampling.

2. This report adds something different: interpolation alone rules out *any* cofinal fixed-threshold Partial-MCSP cascade, INCLUDING source-adaptive coordinate choices and far-from-small-circuit promises. Adaptivity can repair the Hamming detection barrier, but not the unavoidable representation-capacity floor.

3. The published Cheraghchi et al. N^{1.99} MCSP bound concerns **exact** MCSP in a randomized one-work-tape/one-way-input model at a high size exponent. It cannot be imported without proof into the **far-from-small-circuits Gap** promise, which restricts the NO set. A new source-model lower bound or an exact-promise reduction is necessary.

4. Oliveira-Pich-Santhanam's Anti-Checker Lemma assumes NP subset P/poly, yields a **nonuniform circuit** generating N^{10 beta} samples for sufficiently small beta, and targets a distinct Gap-MCSP pair. For beta>1/2 the formal expression N^{10 beta} exceeds N^5, and the published lemma does not cover that regime anyway. It does not supply a near-linear one-tape anti-checker for the high-beta exact-MCSP seed.

5. CLOCKFEATURE5 proves a restricted bijunctive functional-graph obstruction for exact two-probe witness/digest consistency; an arbitrary nonlinear digest factored through a <=S-bit seed can be bypassed by simply guessing that seed. A semantic gate must be decision-only and defeat arbitrary alternative decoder representations. P-vs-PSPACE clock results cannot silently be used for P-vs-NP.

6. RESOURCE-GAUGE5 demonstrates complete multi-block shared-gauge information collapse: many separately rank-rich two-probe blocks can share one small latent state, so generic additive direct-sum claims are RETIRED. Frozen-path subset selection NP-completeness is only a selector-cost fact, not a universal representation lower bound.

7. MAGRED-TAPEFUSION3: generic theta=2 one-work-tape fusion destroys positive transported excess when source c<2 and the compiler must sweep the source in time exponent >=1. A special theta-near-1 implementation remains OPEN. MAGRED-HASHSTREAM4: polynomial-hash b-bit workspace alone yields slope g(beta)/beta approximately 1; image-label verification exponents currently diverge as beta->0, so joint uniformity remains OPEN.

8. LOSSY-PROMISE-CASCADE6 remains a valid **conditional exponent lemma** if every stage has actual promise purity, reduction exponent r<c, shrinking length lambda, error budget, one model, and one jointly low promise-label algorithm with exponent K independent of j. These load-bearing existence hypotheses are NOT established by partial sampling.

## Proof DAG: status and dependencies

- ESTABLISHED: Boolean point-DNF interpolates every well-formed m-sample partial function with O(m n) gates; ADAPTIVE-PARTIAL-CASCADE-FLOOR1 and cofinal same-threshold no-go in precisely this model; CHMY randomized one-tape exact-MCSP high-threshold lower bound; source-independent PARTIAL-SAMPLE-WEDGE7 bounds (project proof, pending independent review).
- CONDITIONAL: LOSSY-PROMISE-CASCADE1 uses a genuinely iterated same-model r<c length contraction and a jointly NP/PH-low label family with one K; recovered cofinal K absorption only under joint uniformity and appropriate collapse.
- OPEN: THRESHOLD-AWARE-ANTICHECKER1; near-linear one-tape source-adaptive extraction; smaller target threshold on YES samples without semantic false positives; NO preservation under correct promise; source lower bound for distance-Gap-MCSP; nonlinear image-label bridge with beta-uniform verifier; fusion theta near one; P vs NP.
- RETIRED: source-independent short coordinate sampling; repeat fixed-threshold Partial-MCSP sampling as a cofinal K-elimination mechanism; using OPS circuit anti-checker as a one-tape generator; generic shared-block resource direct sum; hash digest exact two-probe witness consistency; general-purpose quadratic one-tape fusion as a positive-margin transport.

## Allocation and one highest-value next lemma

**Next lemma: THRESHOLD-AWARE-ANTICHECKER1.** Demand a single precise implementation on the high-beta source: a (possibly randomized) source-adaptive generator, in the same one-way-input/one-work-tape model, computing m=N^{a+o(1)} labeled examples with reduction time N^{r+o(1)} where r<c (published c approximately 1.99), target threshold t=N^{tau+o(1)} with tau<=a<1, and two promise-preservation clauses:
  * ALL source YES truth tables must restrict to a partial table consistent with some size-t circuit, although their source witness may require size s=N^beta, beta>a.
  * ALL source NO truth tables (or a separately proved hard NO-distance promise) must produce partial tables inconsistent with every size-t circuit, with bounded error.
The first bullet is a genuinely new *YES witness-budget compression* requirement, not automatic anti-checker behavior. Require correct error allocation, uniform presentation of parameters, output-address serialization and one-tape fusion. Seek a one-step counterexample before claiming iteration.

If no such witness compression exists, shift to a nonlinear promise-pure image-label Q where interpolation does not apply, but require one NP/PH jointly uniform image verifier before invoking P=NP. Do not infer any unrestricted separation from restricted lower bounds.

**Comparative allocation:** A has an unambiguous new obstruction and precise target; B is a potential escape from the explicit-partial-function floor but image-label joint uniformity remains unproved; C already has a hard source and magnification endpoints but no same-model rho>lambda compiler. Pursue A as a sharply falsifiable transport experiment, B as the alternate language design, and C as the audit standard for quantitative success.

P versus NP remains OPEN. No counterfactual lower-bound exponent K has been eliminated for an actual constructed reduction.

## Primary sources

[1] Cheraghchi, Hirahara, Myrisiotis, Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23
[2] Oliveira, Pich, Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, Theory of Computing 17(11), 2021. https://theoryofcomputing.org/articles/v017a011/
[3] Hirahara, *NP-Hardness of Learning Programs and Partial MCSP*, FOCS 2022 / ECCC TR22-119. https://eccc.weizmann.ac.il/report/2022/119/
