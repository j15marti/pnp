# TMR-2/026: Gap-MCSP Hamming-cylinder frontier and deterministic-versus-randomized query contrast

**Date:** November 14, 2026, 11:23 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity. **Status:** new elementary all-length statements PROVED/RESTRICTED in the declared point-query and circuit model, pending independent TMR-5/TMR-1 review; exact finite evidence COMPUTATIONAL. **P versus NP remains OPEN.**

## 1. Actual contribution and prior-art firewall

This run distinguishes two information costs of **approximation-promise MCSP**: the number of queried truth-table coordinates required on a YES input by a deterministic exact promise decider, and the much smaller number sufficient with random-access randomized samples **when computational enumeration is free of time constraints**. The result extends the earlier team's *ordinary exact-MCSP* sparse-fiber argument to the Hamming neighborhoods of the YES language and gives an exact all-length separation for threshold zero. It is not claimed as a new property-testing technique in the literature.

**PRIOR, not rediscovered:** [FIBER27](../../main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md) already proves that an ordinary MCSP label-pure deterministic output fiber containing zero needs at least N-O(N^mu log N) **distinct coordinate accesses**. TMR-2/024 established an all-cut nonuniform residual-width ceiling. TMR-2/025 established an **all-NO** point-query lower bound of Omega(s/n) and an **exists-NO** short certificate. This run concerns **all YES inputs**, a Hamming-gap promise, a randomized comparison, and an exact sparse threshold-zero example. October 19 REPRESENTATIVE-MAINTENANCE-CEILING5 already supplied an exact small-memory but exponentially slow search-MCSP update algorithm; no space-only novelty is claimed. TMR-1/025's normalized-distance padding identity receives a separate restricted peer audit below.

## 2. Model and theorem GAPCYL26

Let n>=2, N=2^n, and s>=0 be an **integer** circuit gate threshold. Let C=C(n,s) be the N-bit truth tables of functions computed by at most s gates in the fan-in-at-most-two AND/OR, unary NOT basis with free input wires, constants and arbitrary fan-out. Set M=|C|. A standard generous ordered-gate description bound is

$$
M\le D(n,s):=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$

For a Hamming gap eta with 0<eta<=1/2, let r=ceil(eta N)-1, V(N,r)=sum_{j=0}^r binom(N,j). The **promise** eta-MCSP[s] has YES=C and NO={x: d_H(x,C)>=eta N}; the remaining strings are unpromised. This is **not** ordinary exact MCSP unless eta<=1/N. The algorithm has adaptive **point-query** access to one truth-table coordinate per query, arbitrary finite computation and memory between queries, and correctness on both promised labels. Its query count includes distinct coordinates, not physical one-tape transitions.

**Theorem GAPCYL26-A (deterministic YES certificate lower bound).** For every deterministic adaptive point-query promise decider A and every YES source x in C, if q distinct coordinates were queried before A accepted x, then

$$
2^{N-q}\le M V(N,r)\le D(n,s)V(N,r),
\qquad
q\ge N-\log_2 D(n,s)-\log_2 V(N,r).
$$

For 0<eta<=1/2, the standard binomial-tail estimate V(N,r)<=2^{NH_2(eta)} gives

$$
q\ge N(1-H_2(eta))-\log_2 D(n,s).
$$

**Proof.** Follow A on fixed YES source x. Its adaptive queries and answers determine a complete accepting transcript on some set Q of q distinct coordinates. Every one of the 2^{N-q} full truth tables agreeing with x on Q follows that same transcript and is accepted. Because A is correct on the promise, NONE can be a promised NO. Therefore all 2^{N-q} tables belong to the union of Hamming radius-r balls around C, whose cardinality is at most M V(N,r). Counting yields the inequality. Repeated queries cannot improve the count. The entropy bound is the standard binomial-volume inequality. **The machine can read the whole table; the theorem does not forbid that.** QED.

**Theorem GAPCYL26-B (random-access randomized query upper bound, no time guarantee).** Take q independent uniformly random truth-table positions WITH replacement. Evaluate every function in C on the sampled coordinates and accept if at least one is consistent. Every YES input is accepted with certainty. Every promised NO input is falsely accepted with probability at most

$$
M(1-eta)^q\le D(n,s)e^{-eta q}.
$$

Thus q>=ceil((ln D+ln(1/delta))/eta) suffices for error at most delta. This algorithm is uniform only with a **fully charged, potentially exponential** enumeration of all candidate circuits; it is not a polynomial-time MCSP decider. Randomly sampling arbitrary coordinates is not the physical one-way input access of CHMY or MMW. **Proof:** every g in C disagrees with a promised NO on at least eta N positions, so it matches all q independent samples with probability at most (1-eta)^q. Union-bound over C. On YES, the actual matching circuit is always consistent. QED.

**Asymptotic parameter comparison.** Let s=floor(N^mu), eta=N^{-lambda}, with fixed 0<mu,lambda<1. Then

$$
q_{\mathrm{det},\mathrm{YES}}\ge N-O(N^\mu\log N+N^{1-\lambda}\log N)=N-o(N),
$$

while the randomized **query-only** construction uses at most O(N^{mu+lambda}log N) samples for fixed error. When mu+lambda<1, this is o(N) queries. Candidate-circuit enumeration can still take 2^{O(s log(n+s))} time or more in the physical access model. These observations falsify any proposed superlinear **decision-time** implication obtained from YES-query counting or randomized sample counts alone.

### Exact every-YES example at circuit threshold zero

With s=0, C consists of the two constants and n coordinate projections, M=n+2. For n>=2, distinct members have truth-table Hamming distance at least N/2. Fix eta=1/4.

**Theorem GAPCYL26-C.** For **every** YES table x in C, the minimum deterministic accepting transcript depth of any exact promise decider on x equals

$$
\boxed{3N/4+1}.
$$

**Lower bound:** If at most 3N/4 distinct coordinates have been queried on x, at least N/4 remain unknown. Flip exactly N/4 unqueried bits to obtain y. Then d_H(x,y)=N/4. For any other h in C, d_H(y,h)>=d_H(x,h)-N/4>=N/4. Hence y is a promised NO with the same accepting transcript, a contradiction. **Upper bound:** Read any 3N/4+1 coordinates. If all agree with a designated YES x, accept because every possible completion is within strictly less than N/4 of x and cannot be a promised NO; otherwise query the remaining truth-table bits and decide the promise by exhaustive finite circuit enumeration. This is one fixed algorithm across lengths, with full fallback computation charged, not a claim of efficient time. QED.

For this same s=0 promise, the randomized query tester needs only

$$
q\ge \left\lceil\frac{\ln(n+2)+\ln(1/delta)}{1/4}\right\rceil
=O(\log n+\log(1/delta))
$$

for one-sided error delta. Thus a deterministic Theta(N) versus randomized O(log log N) **query** gap exists, while both still may use expensive computation in the unrestricted machine model. The exact example uses s=0 only and is NOT the CHMY small-positive-mu magnification threshold.

## 3. Independent audit of TMR-1/025

TMR-1's normalized-distance dummy-padding theorem survives an independent restricted mathematical check: for E_t f(x,z)=f(x), the upper bound extends an optimal approximator ignoring z, and the lower bound fixes each z-slice of any padded circuit, which cannot increase its gate count. Averaging the slice distances gives

$$
\Delta_{n+t,s}(E_t f)=\Delta_{n,s}(f).
$$

The proof needs **free named inputs/constants and the same integer s**, as in TMR-1's statement. It preserves NO when the target approximation gap is no larger than the source gap; it does not preserve the opposite implication for arbitrary mismatched promises. The executed independent finite tests cover n=2,3, s=0,1, t=1, 544 complete source-table cases. This is favorable peer verification at the declared gate basis, not a new MCSP computational lower bound.

## 4. Primary-source theorem/model matrix

| Primary source, exact location | Input, threshold, model | Premise and conclusion | Our non-transfer |
| --- | --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, printed p.23:3 | Full N=2^n truth table, ordinary MCSP[2^(mu_1 n)] for some sufficiently small fixed mu_1>0; deterministic **one-way read-only input plus one two-way work tape** | If outside DTIME_1[N^1.01] in that exact model, P != NP | Our query lower bound is <=N and does not prove N^1.01 one-tape time |
| Same, Theorem 2, printed p.23:3 | Ordinary MCSP at a **different larger** mu_2; two-sided-error randomized one-way input/one-work-tape model | Unconditional exclusion of BPTIME_1[N^1.99] | Different size-threshold language and model; no transfer to low mu_1 |
| McKay, Murray, Williams, STOC 2019, Theorem 1.3, pp. 1-3 | One-pass **search-MCSP^A** on N bits; size s(n)>=n, oracle A from suitable PH scope; poly(s) workspace and poly(s) update | Appropriate simultaneous update+workspace impossibility implies P != NP | Our s=0 example and randomized point sampling are not this search problem; exponential enumeration does not satisfy the update premise |
| Atserias, Müller, arXiv:2503.24061v2, 21 June 2025, Theorem 27 p.17 | Approximation-promise N^(-epsilon)-MCSP[sigma], sigma(n)<=2^(gamma n); **P-uniform circuit families**, not physical one-work-tape time | For all delta,epsilon>0 a gamma>0 exists: the specified P-uniform-SIZE[N^(1+epsilon+delta)] exclusion yields **P != NP^(oplus P)** | Not an ordinary-MCSP lower bound, not direct P != NP, and enumeration-based property testing does not meet its uniform circuit-size premise |

Primary originals checked: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23 ; https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf ; https://www.cs.upc.edu/~atserias/papers/magnification/magnification.pdf . CHMY and Atserias-Müller printed theorem pages were visually checked. The standard Hamming-ball/union-bound arguments above are elementary self-contained, not attributed to a new external theorem.

## 5. Reproducible finite execution and hostile controls

**ACTUALLY EXECUTED native CPython:** experiments/tmr/tmr2_gap_certificate026.py, SHA256 bcfb9b1b503e3ff47ad3eacfb2be037ac70518cf6335c3a87701991cce2dfc22, Git blob ae40c89df048363a1ab1177b7d14444a093877d7. Exact raw stdout JSON: results/raw/tmr/2026-11-14_1123_TMR2_GAP_QUERY026_RAW.json, SHA256 2a90682e1e664d273ed8c8c48152028eda9ff6544c23377236a25b1a424fd4f4.

For n=4, N=16, s=0, eta=1/4: exhaustively classified all 65,536 truth tables; six YES tables, 61,354 far-NO tables and exactly 4,182 near-or-YES tables. Hamming radius-three volume 697 and six disjoint balls account for all 4,182. The independent subset-zeta certificate verifier found **depth exactly 13 on ALL six YES tables**. Every one of the 1,820 four-hidden-bit adversarial completions was checked as far-NO. The crude general counting lower bound gives four queries at this tiny length, while the exact s=0 argument gives thirteen. At q=20 replacement samples, the maximum individually computed union-bound failure probability over all 61,354 far-NO tables was 0.009516496839751198, below the target 0.05. The same script checked 544 TMR-1 padding-gap equalities for n=2,3 and s=0,1. **Zero assertion failures.** Tests are COMPUTATIONAL only.

Hostile controls: free constants, projections and one-gate enumeration, all YES labels, every full NO promised classification, coordinate subsets, randomized sample reuse, independent padding-slice minimum checks. Horn/2-SAT/GF(2), products, sharing, rereading, arbitrary polynomial workspace and compressed circuit representations remain allowable in **general SAT deciders**; no test here asserts their runtime is hard. Random-access query counts do not become random-access-free physical one-tape time, nor do samples become exact deterministic certificates.

## 6. Exact unrestricted separation gap, next target and peer request

A standard fixed uniform deterministic multitape 3-SAT decider has L-bit *encoded 3-CNF input*, not an N-bit explicit MCSP truth table. The desired target quantifies over every correct finite total machine A and every polynomial exponent k and demands some arbitrarily long encoded F with T_A(F)>C(L+1)^k. Nothing above creates an SAT reduction from a full explicit MCSP table or proves time beyond N, let alone all polynomial exponents in L. A physical one-way scan of an N-bit truth table is a legitimate O(N) acquisition strategy; no extra post-scan processing necessity has been established.

**Next specific target:** Test a uniform low-threshold MCSP representative-transition/update lower-bound candidate **after the complete input has been acquired**, against small-circuit sharing, factored representations and all polynomial workspace; require actual one-work-tape transition cost or the matching MMW simultaneous search-update premise. Do not repeat source-query counts. **Peer review:** TMR-5 verify the general Hamming-cylinder theorem and exact s=0 depth; TMR-1 check normalized-distance audit and approximation magnification premise; TMR-3 check any attempted promotion of query cost to physical tape time.

## 7. Preflight and integrity

Read FIRST Nov14 authoritative MCSP directive (Git blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then Nov13 replacement (47459817e66dccf1f3079e6c724c0fd2643e7bc4); AGENTS.md, CODEX.md, pnp research skill, all five current TMR handoffs (including new TMR-1/025), full issue #3 through TMR-1/025; complete proof1.txt 28,714 characters (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), complete proof2.txt 1,051,196 characters via authenticated Git blob (930c5eeddafce656717f28055a7a9a755f44737c), and full canonical main.tex 2,545,859 characters via Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Read original October FIBER27, representative-maintenance theorem, TMR-2/025, TMR-1/025, TMR-5/022, relevant Claude ONETAPE/TPORT/DIRECTPRODUCT and Grok status plus cited primary literature. Historical proof statuses preserved.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex is owned by TMR-5 and was not edited. No scheduled agents, identities or tasks were changed. No all-exponent unconditional lower bound and no complete P=NP algorithm were found. **P versus NP OPEN.**

END_OF_REPORT::TMR2::026::2026-11-14_1123_PST
