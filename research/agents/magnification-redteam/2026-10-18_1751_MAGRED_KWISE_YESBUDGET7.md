# MAGRED-KWISE-YESBUDGET7 | 2026-10-18 17:51 Asia/Seoul

**Status:** PROVED/EXACT elementary restricted-model lemmas, pending independent review. Finite-field tests are COMPUTATIONAL. No same-model MCSP exponent transport or P versus NP separation. **P versus NP OPEN.**

## PROPOSE ATTACKS -> SEARCH -> BUILD

**Attacks proposed before checking sources:** (A) lower the Partial-MCSP circuit budget (s=N^\beta\mapsto t=N^\tau), test YES-side false negatives even for source circuits of size at most (s); (B) compare source-adaptive partial-query transcripts against distributions that look completely random on many coordinates but have small circuits; (C) repair only the NO hitting-set clause using point corrections and a union bound; (D) check whether explicit Partial-MCSP really suffers the claimed stage-j NP-uniformity problem; (E) audit seed independence, output length, work-tape fusion and actual source promises.

**Project corpus checked:** research/main/2026-10-18_LOSSY_PROMISE_CASCADE6.md, PARTIAL_SAMPLE_WEDGE7.md, 1553_PROMISE_CASCADE_FIXEDPOINT8.md, K_ELIMINATION_TRANSFER4.md, root main.tex (17:16 KST), threshold-descent/1416_THRES_HASHBRIDGE4.tex, clock-gate/1510_CLOCKFEATURE5.tex, resource-directsum/1643_RESOURCE_KPIPRODUCT6.tex, and magnification-redteam/1634_MAGRED_DIMFREE6.md. Main proof spines unchanged.

**Primary literature checked:** Cheraghchi--Hirahara--Myrisiotis--Yoshida STACS 2021 (randomized **one-work-tape exact MCSP** lower bound); Oliveira--Pich--Santhanam Theory of Computing 2021, Lemma 4.1 (small-beta **nonuniform circuit** anti-checker producing about (N^{10\beta}) examples, with target Gap-MCSP threshold (N^\beta/(10n))); Hirahara FOCS 2022 (randomized hardness of Partial-MCSP, not one-tape transport); classical finite-field polynomial/Vandermonde k-wise independence. None implies the desired compiler.

## Theorem 1: KWise-LOW-CIRCUIT7 (elementary)

Put (N=2^n). There is an absolute constant (A>0), depending only on the fixed fan-in-two Boolean basis, such that for every (1\le k\le N) there exists a distribution \(\mathcal D_{n,k}\) over Boolean functions on (n) variables satisfying:

1. **Every support function has (CC(f)\le A k n^2)**.
2. On every collection of at most (k) distinct truth-table coordinates, the function values are exactly independent uniform bits.
3. Consequently every adaptive, randomized algorithm which probes at most (k) distinct truth-table positions has **exactly the same distribution of full transcripts** on \(\mathcal D_{n,k}\) as on a completely uniform random (N)-bit truth table.

**Proof.** Work over \(\mathbb F_{2^n}\). Take independent uniform coefficients \(a_0,\ldots,a_{k-1}\in\mathbb F_{2^n}\), and define
\[
f_a(x)=\operatorname{Tr}_{\mathbb F_{2^n}/\mathbb F_2}\left(\sum_{i=0}^{k-1}a_i x^i\right).
\]
The Vandermonde evaluation matrix at any (q\le k) distinct (x)'s has full row rank, so the evaluated field values are independent uniform field elements. Trace is an onto \(\mathbb F_2\)-linear map, hence their traced bits are independent uniform. Horner evaluation requires (k-1) general binary-field multiplications and additions; schoolbook field arithmetic has Boolean-circuit size (O(n^2)) per multiplication, giving (O(kn^2)) gates. Adaptive transcript identity follows by induction on queries, conditioned on all previous queried coordinates and answers. Repeated queries reveal no new information. QED.

This uses **nonuniform circuits as the definition of source YES**, not as a claimed fast one-work-tape sampler, and requires no efficient construction of irreducible polynomials.

## Theorem 2: ADAPTIVE-SOURCE-PROBE-FLOOR7

Fix (0<\beta<1), let (s=N^\beta), and put
\[
k=\left\lfloor\frac{s}{A(\log_2 N)^2}\right\rfloor .
\]
Any randomized (q)-bit-probe transformation followed by *any* classifier, where the output depends on source (f) only through those probes, and which correctly separates **every** source exact-MCSP YES input (CC(f)\le s) from every NO input (CC(f)>s) with error at most (1/3), must have \(q>k\) for sufficiently large (N). The conclusion also holds for a NO promise consisting of truth tables at Hamming distance at least \(\gamma N\) from **all** size-(s) circuit functions, for any fixed \(0<\gamma<1/2\).

**Proof.** By Theorem 1, the low-circuit distribution \(\mathcal D_{n,k}\) lies entirely in source YES. A uniformly random truth table lies in source NO with probability (1-\delta_N\), where
\[
\delta_N\le 2^{O(s\log(n+s))-N}=o(1)
\]
by circuit counting. For the distance-gap variant, replace this with \(\delta_N\le 2^{O(s\log(n+s))-(1-H_2(\gamma))N}=o(1)\). If (q\le k), every adaptive transcript (including sampler randomness and source-dependent sampled addresses) is identically distributed under these two input distributions. Per-source error (\le 1/3\) would force acceptance probability at least (2/3) on \(\mathcal D_{n,k}\) but at most (1/3+\delta_N\) on uniform tables, contradiction. Target promises and their bad seeds can be handled by extending the target label arbitrarily off-promise. QED.

**Interpretation:** an adaptive threshold-aware quotient must inspect more than \(N^{\beta-o(1)}\) source positions. It says nothing about a reduction that scans all (N) source positions, and cannot be converted into a (N^{1.99}) one-tape lower bound. For a one-pass stream, reading (N) bits already exceeds this probe floor.

## Theorem 3: OBLIVIOUS-THRESHOLD-DROP-NOGO7

Fix (0<\tau<\beta<1), source exact MCSP threshold (s=N^\beta), and target ordinary Partial-MCSP threshold (t\le N^\tau). A purported quotient that chooses a (possibly random, variable-size) list of **distinct** sample coordinates (S) independently of source values and outputs *only* the explicit list \((S,f|_S)\) cannot preserve both source promise classes with error (\le1/3\), regardless of how many coordinates it selects.

**Proof.** Let \(M_t\le 2^{B(t+1)\log_2(n+t+2)}\) be the number of size-(t) circuit functions, for a basis-dependent constant (B). Choose \(h=\lceil\log_2M_t\rceil+8\). Because (\tau<\beta\), we have (h\le k\) for all sufficiently large (N), with (k) from Theorem 2. Let (A) denote the event \(|S|<h\).

On (A), the entire quotient output (including the independently chosen sample addresses and seed) has exactly the same distribution when (f\sim\mathcal D_{n,k}\) as when (f) is uniform. Soundness for uniform NO sources therefore bounds the joint probability of (A) and target-YES acceptance by (1/3+\delta_N\).

On (A^c), consider any (h) sampled addresses. Under \(\mathcal D_{n,k}\) their labels are uniformly random. A union bound over all size-(t) circuit functions gives
\[
\Pr_{f\sim\mathcal D_{n,k}}[\exists C, |C|\le t: C|_S=f|_S]\le M_t2^{-h}\le2^{-8}.
\]
Combining the two events, acceptance probability averaged over source YES functions is at most \(1/3+\delta_N+2^{-8}<2/3\). Thus at least one promised source YES function violates required completeness. QED.

**Consequence:** merely adjusting the target threshold fails for **every source-oblivious explicit-coordinate sampler**, not just for sample sizes above the interpolation floor. This does NOT rule out a source-adaptive sampler that examines more than (k) bits, a nonlinear hash image, a different target label language, or a sampler that emits additional source-derived information.

## Repaired one-sided NO clause: POINT-CORRECTION-HITTING7

There is a constant (D) such that if (C) has at most (t) gates and (f) differs from (C) at (d) truth-table positions, then
\[
CC(f)\le t+D(nd+n).
\]
Construct a point-indicator circuit for each disagreement, OR them, and XOR the correction mask with (C). Thus for source (CC(f)>s>t+Dn\), each size-(t) circuit disagrees with (f) on at least
\[
d_*=(s-t-Dn)/(Dn)
\]
coordinates (up to harmless integer rounding). A uniformly random sample of
\[
m\ge\frac{N}{d_*}\bigl(\ln M_t+\ln(1/\epsilon)\bigr)
\]
distinct coordinates is therefore inconsistent with **all** size-(t) circuits with probability at least (1-\epsilon\), by a union bound. For (s=N^\beta, t=N^\tau, \tau<\beta\), this sufficient sampling length scales as
\[
m=N^{1-\beta+\tau+o(1)}.
\]
This is a valid **NO-soundness-only** repair for exact MCSP, with no source promise drift. Theorem 3 proves that it does not simultaneously provide YES preservation. The construction is a random-coordinate argument, not a same-tape time upper bound: sample generation, sorting, output serialization and fusion remain chargeable.

## Joint NP repair for the explicit partial target

The language of well-formed explicitly serialized partial tables \((n,t,(x_i,b_i)_{i\le m})\) consistent with some \(t\)-gate circuit is **uniformly in NP for binary-encoded (t)**, independently of cascade stage (j). If (t\ge4m+O(1)\), every consistent list is trivially YES by the DIMFREE6 decision-tree interpolation theorem; malformed contradictory duplicates are handled deterministically. Otherwise (t=O(m)\) and an ordinary size-(t) circuit certificate uses \(O(t\log(n+t))=\operatorname{poly}(L)\) bits, where (L) is the explicit input length, and verification takes \(\operatorname{poly}(L)\) time with an exponent independent of (j). Hence the **joint NP-uniformity arrow is closed for standard explicit Partial-MCSP**, but not for novel hash-image languages or implicitly encoded examples. Under (P=NP) this yields one fixed polynomial exponent (K); the missing arrows are promise-preserving cheap source-adaptive extraction and one-work-tape fusion.

## Exact exponent/model ledger and nonclaims

For \(s=N^\beta, t=N^\tau, m=N^a\): explicit samples require \(L=\Omega(mn)=N^{a+o(1)}\) bits (plus seed/metadata). Interpolation requires \(a\ge\tau-o(1)\) to admit promised target NO. The NO-only hitting lemma gives a **sufficient** exponent \(a_{NO}=1-\beta+\tau\). The source-adaptive probe lower bound gives \(q>N^{\beta-o(1)}\), so reduction time exponent (r\ge\beta\) in a unit-cost probe model, but not (r\ge1.99\). Source-oblivious sampling fails for every (a), even when (a\ge a_{NO}\). No \(\rho>\lambda\) exponent-transport compiler is established. CHMY applies to one-way input/one-work-tape randomized exact-MCSP; generic work-tape fusion with quadratic overhead can erase the (c<2) source lower-bound margin. The OPS anti-checker applies to circuit synthesis under (NP\subseteq P/poly), not to this same-tape source. The KPI product projection is reconstructible on its polynomial promise and does not solve exact MCSP by itself. A fixed/c-dependent clock gate cannot bypass these requirements.

**Highest-value next step:** SOURCE-ADAPTIVE-YESCOMPRESS8: after an explicit full source read, construct a sublinear list of labeled examples consistent with a (t\ll s\) circuit on every source YES instance, while making every source NO instance (t)-inconsistent, with (r<1.99), exact source promise, source-independent uniform algorithm, and direct one-tape composition. Test smallest examples of adaptive witness selection before extrapolating. **P versus NP OPEN.**

## Exact finite control

Script locally: `/mnt/data/magred_threshold_aware7_test.py`. Finite GF(8), (k=3): 512 coefficient vectors, 92 distinct-coordinate subsets, 576 uniform-pattern checks; every one of eight depth-3 adaptive transcript patterns occurred exactly 64 times. Finite GF(16), (k=3): 4,096 vectors, 696 subsets, 4,992 uniform-pattern checks; eight adaptive patterns occurred 512 times each. Three-sample consistency with a **toy constant-only target** was exactly 1/4 for both families; this is not a standard gate-threshold MCSP test. All checks passed. Proofs are analytical; numbers are COMPUTATIONAL only.

## References

1. M. Cheraghchi, S. Hirahara, D. Myrisiotis, Y. Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23
2. I. Oliveira, J. Pich, R. Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, Theory of Computing 17(11), 2021. https://theoryofcomputing.org/articles/v017a011/
3. S. Hirahara, *NP-Hardness of Learning Programs and Partial MCSP*, FOCS 2022. https://eccc.weizmann.ac.il/report/2022/119/
4. Classical Vandermonde construction of k-wise independent finite-field random polynomials; used here only in a standard elementary lemma.

% END_OF_VERIFIED_REPORT::MAGRED-KWISE-YESBUDGET7::P_VS_NP_OPEN
