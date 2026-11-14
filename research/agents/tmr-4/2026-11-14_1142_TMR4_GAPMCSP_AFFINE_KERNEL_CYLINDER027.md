# TMR-4/027: Robust Gap-MCSP affine-kernel collision and threshold-descent firewall

**Date:** November 14, 2026, 11:42 PST (America/Los_Angeles). **Role:** TMR-4 Cost-Sound Abstraction. **Scientific status:** elementary **PROVED/RESTRICTED** derivation, pending independent TMR-2/TMR-5 mathematical peer review. **Finite experiments:** COMPUTATIONAL native CPython, no asymptotic inference. **P versus NP: OPEN.**

## 1. Exact question and novelty audit

Can a fully explicit N=2^n-bit ordinary MCSP or Hamming-gap MCSP truth table be compressed using a fixed GF(2)-linear sketch, possibly with **arbitrary deterministic nonlinear postprocessing**, while preserving **both** the YES and NO labels at another MCSP threshold? The source length is N bits; its circuit-input arity is n; SAT encoded source length L is distinct and absent here.

**PRIOR, NOT NEW:** The project's October 18 **AFFINE-KERNEL4**, in research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex, already proves exact-MCSP kernel collisions for fixed affine sketches when kernel dimension exceeds log_2 of the source YES set. research/agents/threshold-descent/2026-10-18_1902_THRES_HASHIMAGE_SATURATION9.md independently studies rank-bounded hash images and low-size representatives; research/main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md proves a deterministic source-query cylinder barrier. TMR-2/026 proves the Hamming-neighborhood cylinder count for adaptive point-query deciders. This is **not a rediscovery of the exact kernel theorem**.

**NEW RELATIVE TO THESE ORIGINAL PROJECT FILES:** Extend the fixed-affine-kernel obstruction to **promised Hamming-far NO instances** using a full, explicitly parameterized Hamming-ball volume. The extension applies to any fixed matrix, any affine offset, and any arbitrary deterministic output decoder of the sketch, and yields distinct quantitative rank frontiers for exact MCSP and Gap-MCSP. It is an elementary conjunction of prior kernel and Hamming-volume methods, not a general circuit lower bound and not claimed novel in external mathematical literature. Explicit independent exact finite examples include a 64-bit truth table 25 bits away from the threshold-zero YES set, despite the same eight-bit sketch as the all-zero YES source.

Other original restrictions preserved: TMR-1/025 approximation padding preserves distance only at the same integer circuit threshold; TMR-4/024 showed SAT satisfaction truth tables have O(n^3)-gate descriptions; TMR-4/026 and TMR-5/022 prove ordered-output *transport* costs, not decision hardness; TMR-3/026 shows a length-blind transducer restriction; original Claude ONETAPE/TPORT/DIRECTPRODUCT and historical compact Walsh/GF(2)/Horn/2-SAT examples warn against transforming model-specific costs into universal SAT costs.

## 2. Complete model and theorem

Fix a finite fan-in-two AND/OR/NOT gate basis, with unrestricted fan-out and free constants, and let C_{n,s} subseteq {0,1}^N contain every full truth table of an n-input function computed with at most s gates. Let

$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s,
\quad
V(N,t)=\sum_{i=0}^{t}\binom Ni.
$$

The elementary ordered-circuit-description count gives |C_{n,s}|<=D(n,s). Let eta in (0,1), d=ceil(eta N), and define the **promise**:

$$
Y=C_{n,s},\qquad
Z_\eta=\{x:\min_{g\in C_{n,s}}d_H(x,g)\ge d\}.
$$

Inputs with distance 1,...,d-1 are *outside the promise*; an exact deterministic promise reduction must preserve all Y as YES and all Z_eta as NO, without conditions on unpromised strings.

Consider a **fixed**, source-independent affine sketch A x + u, over GF(2), where A has rank r and any number b of rows, followed by any deterministic function psi into a target space (a full target truth table, a bit, a description, or another object). Thus R(x)=psi(Ax+u). No restriction on psi's complexity is needed for the impossibility statement.

**Theorem AFFGAP27 (scope: source-independent affine sketch).**

(i) If 2^(N-r)>|C_{n,s}|, then there exists an exact-MCSP NO word x with Ax=A0=0, so R(x)=R(0). Since 0 is a YES word, no R of this form can preserve both ordinary MCSP labels for any target decision problem.

(ii) If

$$
\boxed{\quad 2^{N-r}>D(n,s)\,V(N,d-1)\quad}
$$

then there exists a promised Gap-MCSP NO word x in ker(A) with Hamming distance at least d from every member of C_{n,s}. Again R(x)=R(0). Such an R cannot preserve both promised labels for **any** target decision problem, including ordinary MCSP at any target integer threshold, Gap-MCSP with specified promise, or a succinct decision bit.

(iii) These statements remain true for any *fixed* nonlinear psi and any fixed affine offset u. They do **not** cover matrices chosen adaptively from the source x, randomized constructions whose seed depends on x, a general nonlinear compression performed before the sketch, or a transducer whose output retains x outside the sketch. A complete original-input scan does not invalidate this mathematical fiber collision; however its computational expense alone neither proves nor refutes MCSP hardness.

**Proof.** By rank-nullity |ker A|=2^(N-r). For (i), there are fewer than |ker A| low-circuit tables, hence ker A contains some x outside C. For (ii), each Hamming ball of radius d-1 contains at most V(N,d-1) tables, so the union of balls around C has size at most |C|V <= D V. The stated strict inequality guarantees a kernel element outside the union, exactly a promised NO. The zero vector lies in C, and both x and zero have the same sketch Ax+u=u, hence the same postprocessed target. No function of a common target value can give both required labels. QED.

**Asymptotics.** For s=floor(N^mu), 0<mu<1, log_2 D=O(N^mu log N)=o(N). Thus any fixed-rank-loss sequence with N-r=omega(N^mu log N) defeats exact labels (the precise sufficient condition remains N-r>log_2D). For any fixed eta<1/2, log_2 V(N,ceil(eta N)-1)<=N H_2(eta)+o(N); rank r <=(1-H_2(eta)-epsilon)N guarantees promised-NO collision for large N. For eta=N^(-lambda) with fixed 0<lambda<1, log_2 V=o(N) and **any** rank r<=(1-epsilon)N is eventually insufficient for promised-label preservation. The constants epsilon>0 are fixed, and n=log_2N.

The collision theorem is **not** a statement that all near-injective maps must fail, nor does it constrain a non-affine threshold-changing reduction at all.

## 3. Explicit cost and reduction direction

**Target attempted:** source MCSP[N^mu2] or its distance promise on an N=2^n-bit input -> target ordinary or promised MCSP on M=2^m-bit truth tables, using a fixed affine sketch with rank r<=M, followed by arbitrary deterministic decoding. YES and NO preservation is *required*, not assumed. For M<=N/2, and any fixed mu2<1, exact obstruction holds for all sufficiently large N. For a constant Hamming fraction eta<1/2, the stronger robust obstruction holds when M<(1-H_2(eta)-epsilon)N for suitable fixed epsilon>0. This is a **failure of label preservation**, independent of runtime accounting.

A concrete first-eight-coordinate extraction on N=64, M=8, n=6, m=3 has source threshold s=0. Both the zero truth table (YES) and the explicit source word 0xc28affa6574e6000 (NO and 25 Hamming bits from the nearest size-0 circuit truth table) produce the identical all-zero 8-bit target. The target is ordinary MCSP-YES at every nonnegative threshold. The original formula/circuit describing a 64-bit source is **not** the same object as its full truth table.

A uniform finite transducer may compute a specified rank-r parity sketch via an explicit circuit or a charged stream, but no charge, even arbitrarily large, restores missing labels. Conversely, a positive result for a *different* source-sensitive reduction would require the exact source/target lengths, construction time, one-way input head, one work tape, output, promises, and exponent conversion. No free circuit-minimization oracle or source-specific advice is assumed.

## 4. Independent finite execution and hostile controls

Native CPython 3, no external dependencies: experiments/tmr/tmr4_affine_kernel027.py. Raw exact JSON: results/raw/tmr/2026-11-14_1142_TMR4_AFFINE_GAP_KERNEL027_RAW.json.

- Exhaustive binary truth-table YES/NO classification at n=2,3,4 for gate thresholds s<=2 (n=4 restricted to s<=1), with fixed AND/OR/NOT circuit enumeration, free constants, both terminal labels.
- Six independent full-row-rank 8x16 parity matrices, **all 256 kernel elements** each, at n=4 and s=0,1. In every case, explicit NO elements collide with zero and with all three tested nonlinear decoders.
- At n=4, the first-eight-coordinate rank-eight sketch has 254 exact-NO kernel elements for s=0 and 251 for s=1; it also has 70 and 30 Hamming-far (eta=1/4) kernel elements, respectively. The robust *counting sufficient condition* does not yet hold for this tiny case; the witnesses are found by exhaustive enumeration.
- At n=6, N=64, s=0 and eta=1/4, the independent volume bound is certified: kernel exponent 56 > log_2(DV) ~50.675. An explicit full 64-bit promised NO witness has distance 25 from the nearest size-zero circuit table and the same eight source-sketch bits as zero. Tests checking the larger n=8 numeric bounds were **integer-arithmetic fixtures**, not exhaustive n=8 circuit enumeration.
- Total **135,015 recorded checks**, zero assertion failures. Original source SHA256 62cb176296c17d4cdeaaab662df8d28a2b4323c4e1eb35c7b073f9fc59331bbe; original raw SHA256 ff7f4cd27d7f646d56b502fcdaea638f6c2299aec073e4b97c092eb18fe369d0. Reproducible locally under native CPython in one <25-second chunk. No JavaScript/V8 implementation, arbitrary-TM compiler, source-distribution experiment, or TeX CI executed.

Cheap satisfiable subclasses (Horn, 2-SAT, GF(2) linear systems, bounded treewidth, products, factored circuits, sharing, cache/recompute, padding, variable renaming and auxiliary variables) remain possible for generic SAT solvers. They are **not claimed to be executed as SAT tests** by this finite MCSP script. The proof does not force compulsory assignment enumeration, storage of the circuit class, or a uniform update cost.

## 5. Primary-source theorem/model audit

| Paper/version, theorem | Exact relevant scope | Why it does NOT follow here |
|---|---|---|
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, ECCC TR20-103 / STACS 2021, Theorem 1, p.3 | For some **small** mu1>0, ordinary MCSP[2^(mu1 n)] outside deterministic one-way-read-only-input PLUS one two-way-work-tape time O(N^1.01) implies P!=NP; uniform finite TM, N=2^n. | No such lower bound here; source compression collides semantically. |
| CHMY, Theorem 2, p.3 | For a **larger** mu2 in (0,1), ordinary MCSP[2^(mu2 n)] is outside randomized two-sided-error one-work-tape time O(N^1.99), same declared input interface. | It concerns another threshold language. The current kernel theorem cannot transfer its hardness. |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2 and 1.3, pp.1-2 | Full one-pass **search-MCSP^A**, s(n)>=n, with oracle Sigma_3SAT^A, oracle-assisted O~(s^2) update, O~(s) space, O~(N s) total; a simultaneous uniform polynomial-in-s update/space lower bound for suitable A in PH implies P!=NP. | Here no search synthesis, oracle/update lower bound or physical streaming simulator is proved. |
| Oliveira, Pich, Santhanam, Theory of Computing 17 (2021), article 11 | Nonuniform circuit magnification for explicit Gap-MCSP with two threshold parameters/promise, hypothesis of weak circuit lower bounds, conclusion NP not subset P/poly under theorem's precise quantifiers. | Our eta-distance-to-size-s promise is not automatically that paper's two-threshold Gap-MCSP; no unproved conversion is imported. |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, ITCS 2020 | Locality-barrier analysis for several magnification proof methods, not a universal prohibition. | The present low-information sketch failure does not overcome any locality barrier. |

Primary URLs: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23 ; https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf ; https://theoryofcomputing.org/articles/v017a011/ ; https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2020.70 . The 2025 Atserias-Mueller approximation-uniform magnification work is a **distinct** theorem/model with conclusion P!=NP^(oplus P), per TMR-1/025; no such hypothesis is invoked here. Ordinary MCSP's NP-completeness is not assumed, and no ETH/SETH/cryptographic hypothesis is invoked.

## 6. Remaining load-bearing gap and peer request

**OPEN:** Find a source-sensitive, nontrivial high-threshold-to-low-threshold MCSP transformation that preserves YES and NO, pays explicit target truth-table length and construction/simulation costs in the CHMY tape model, and meets the exact exponents. Equally legitimate: establish a direct small-threshold one-work-tape lower bound with the correct quantifiers. A kernel collision for a prescribed sketch family does not prove any unrestricted deterministic SAT lower bound.

**Next target:** test whether allowing a **source-dependent chosen affine sketch** defeats the fixed-kernel proof while still permitting uniform construction, bounded output length, label-purity, and one-work-tape time O(N^r), and extract a concrete both-label candidate or a failing counterexample. TMR-2 should independently audit the union-of-balls distance convention (ceil eta N) and bound; TMR-5 should peer-review rank-nullity, compare to October AFFINE-KERNEL4, and reject any novelty overclaim. TMR-1 should audit use against exact CHMY mu1/mu2; TMR-3 should charge any candidate transducer.

**Read integrity:** Read newest November 14 MCSP directive first (blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), November 13 replacement, AGENTS.md/CODEX.md/skill, all five current TMR handoffs and issue #3 through TMR-3/026. Root proof1 complete 28,714 characters (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343); root proof2 complete 1,051,196 characters via authentic blob 930c5eeddafce656717f28055a7a9a755f44737c; canonical main.tex complete 2,545,859 characters via authentic blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. No permission to edit root main.tex, and no tracker or scheduled-task changes. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

END_OF_REPORT::TMR4::027::2026-11-14_1142_PST
