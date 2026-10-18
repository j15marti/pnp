# MAGRED-DISTANCE-OVERLAP9 | 2026-10-18 19:09 Asia/Seoul

**Status:** Exact combinatorial/probabilistic theorem under a fixed standard fan-in-two circuit model, independent review pending. Finite tests are COMPUTATIONAL. No unrestricted time lower bound. No efficient threshold descent or P versus NP separation; **P versus NP OPEN**.

## PROPOSE ATTACKS -> SEARCH -> BUILD

Attacks proposed before literature: (A) seek source YES functions that are very far in Hamming distance from every smaller-threshold circuit, despite admitting tiny lower-threshold anti-checkers; (B) test whether the *existence* of a small anti-checker distinguishes exact MCSP at threshold s rather than MCSP at t; (C) falsify "distance-Gap to t" as a substitute for the published CHMY exact-MCSP promise; (D) seek a finite concrete opposite-source-label pair exhibiting the same t-anti-checker property; (E) stress-test fixed-sample randomness, output length, model fusion, and stage-dependent witness budgets.

Corpus read: research/main/2026-10-18_LOSSY_PROMISE_CASCADE6.md, PARTIAL_SAMPLE_WEDGE7.md, 1553_PROMISE_CASCADE_FIXEDPOINT8.md, 1757_SOURCEQUERY_SYNTHESIS10.md, K_ELIMINATION_TRANSFER4.md, root main.tex; threshold-descent/1832_THRES_ADAPTIVE_LHL8.tex; clock-gate/1510_CLOCKFEATURE5.tex; resource-directsum/1643_RESOURCE_KPIPRODUCT6.tex; magnification-redteam/1751_MAGRED_KWISE_YESBUDGET7.md and 1821_MAGRED_EDGEADAPT8.md. Neither the current main spine nor other agents' files were changed.

Primary literature: Schmidt--Siegel--Srinivasan 1995 limited-independence tail bounds; Cheraghchi--Hirahara--Myrisiotis--Yoshida 2021 one-work-tape exact MCSP; Oliveira--Pich--Santhanam 2021 circuit-model hardness magnification / small-beta anti-checkers; Hirahara 2022 Partial-MCSP under randomized reductions; Moran--Yehudayoff 2016 sample compression (different objective). This report proves its stated overlap lemma using an elementary moment argument rather than claiming novelty for k-wise independence or moment bounds.

## THEOREM: LOW-SIZE-HALFDISTANCE9 (PROVED/EXACT in declared model)

Fix a standard finite complete Boolean circuit basis with free input wires and fan-in at most 2; constants/basis conventions affect only absolute constants. Let N=2^n and let 0<tau<beta<1 and 0<delta<1/2 be fixed. Put s=floor(N^beta), t=floor(N^tau). Define C_v={f on n inputs: CC(f)<=v}. Then for all sufficiently large N there exists a Boolean f such that

    CC(f) <= s,

but simultaneously for EVERY g in C_t,

    d_H(f,g) > (1/2-delta)*N.                             (1)

Indeed, the proportion of functions from a specific small-circuit k-wise independent ensemble having (1) tends to one, where

    k = 2*floor(s/(2*A*n^2))

and A is a sufficiently large fixed circuit-gate constant. The original source YES class thus contains functions almost maximally distant from all t-size circuits. This is optimal in the limiting factor 1/2 because constant-zero and constant-one functions belong to C_t and min(d(f,0),d(f,1))<=N/2 for every f.

**Proof: low-size k-wise ensemble.** Identify inputs with GF(2^n). Choose a_0,...,a_(k-1) independent uniform elements of GF(2^n) and put f_a(x)=Tr(sum_{j<k} a_j x^j). For any k distinct field points, evaluations of this polynomial are independent uniform field elements by Vandermonde invertibility, and their traces are independent fair bits. Horner evaluation over GF(2^n) with schoolbook field arithmetic computes each f_a with <=Akn^2<=s fan-in-two gates (constants hardwired into the circuit). Thus all support functions are in C_s.

**Proof: strong Hamming separation.** Fix ANY g in C_t and set Z_x=(-1)^(f_a(x) XOR g(x)), so Z_x are k-wise independent mean-zero Rademacher variables. For even k their k-th sum moment equals that for fully independent fair signs and

    E[(sum_x Z_x)^k] <= (k*N)^(k/2).

Since d_H(f_a,g)=(N-sum_x Z_x)/2, Markov gives

    Pr[d_H(f_a,g) <= (1/2-delta)N]
       <= (k/(4*delta^2*N))^(k/2).                       (2)

There are at most M_t=2^{O(t*log(n+t))} functions in C_t by gate-description counting. A union bound multiplies the RHS of (2) by M_t. Its logarithm is

    O(N^tau*log N) - Omega(N^beta/log N) --> -infinity,

because fixed beta>tau. Hence an overwhelming fraction of ensemble functions satisfy (1). QED.

## COROLLARY: FALSE-YES-ANTICHECKERS9

For every fixed epsilon>0, an f in source YES satisfying (1) has the following property: if a sample S of m distinct uniformly random source coordinates is taken, then

    Pr[f|S is consistent with some size-t circuit]
       <= M_t * (1-(1/2-delta))^m
       = M_t*(1/2+delta)^m.

Consequently if

    m >= (ln M_t + ln(1/epsilon))/(-ln(1/2+delta)),       (3)

then with probability >=1-epsilon the sampled table is a valid **NO** instance of sparse-list Partial-MCSP[t], even though f is a true source **YES** instance of exact MCSP[s]. Because ln M_t=O(t log(n+t)), formula (3) permits

    m=O(t*log(n+t))=N^{tau+o(1)},
    L=O(m*n)=N^{tau+o(1)}.

These anti-checkers fit the **same exponent** tau as the interpolation floor tau<=a, so satisfying the earlier capacity inequality does NOT imply original-source promise preservation. The output probability is pointwise for this fixed easy f, not a single globally good seed claim.

Uniformly random source truth tables are source NO with probability 1-o(1) (|C_s|=2^{o(N)}) and also (1/2-delta)N-far from C_t with probability 1-o(1). Thus source YES and source NO both possess short t-anti-checkers.

## EXACT CHARACTERIZATION: WRONG-THRESHOLD CERTIFICATE9

For any fixed Boolean f and finite circuit family C_t,

    EXISTS finite S such that f|S is inconsistent with every C in C_t
    IFF f is NOT in C_t.

Proof: if f in C_t, its own circuit agrees with every subset. If f not in C_t, for each member g of C_t choose one coordinate where g differs from f, and take the union of those coordinates. The set has size at most |C_t|. QED.

This is a certificate for **MCSP[t]**, not MCSP[s]. The strict gap t<s has many instances t<CC(f)<=s, and the previous theorem shows that some have robust, very short anti-checkers, not merely pathological size-|C_t| certificates. Any proposal using "an anti-checker exists" or "uniform samples are t-inconsistent" to stand in for MCSP[s] retires here. This does NOT rule out a genuinely source-adaptive, full-reading transducer that chooses t-consistent samples specifically on all C_s, and t-inconsistent ones specifically on all not-C_s.

## FINITE FALSIFIER: 64-BIT TRUTH TABLES

Exhaustive enumeration of all outputs of AND/OR/NOT circuits with up to 1 or 2 gates and 6 input variables yielded 44 and 294 distinct truth tables respectively (input wires and constants free). With source size s=3 and target t=1:

* Source YES: f=(x0 AND x1) OR (x2 AND x3), exactly 3 gates. Its minimum distance to every size-1 target circuit is 12 of 64 bits. Its **smallest** size-1 inconsistent labeled set has four addresses: [1,2,3,12].
* Source NO: g=x0 XOR x1 XOR x2 XOR x3 XOR x4 XOR x5. It depends on six essential variables and therefore cannot be computed using 3 fan-in-two gates (at most four source inputs can influence a connected three-gate output). Its distance to every size-1 target circuit is 32 of 64 bits. Its **smallest** size-1 inconsistent labeled set has three addresses: [0,1,3].

Both source labels therefore admit a tiny target NO sample. Exact minimality was checked by exhaustively enumerating all address subsets of smaller cardinality.

Second control: 6-input parity has a circuit of at most 20 AND/OR/NOT gates (five four-gate XOR compositions), and is distance exactly 32/64 from every target circuit of size at most 2, as each such target circuit depends on at most three inputs. Against all 294 distinct two-gate truth tables the minimum inconsistent sample is four addresses [0,1,2,3]. Seeded uniform sampling of 1500 subsets each yielded successes of 1215, 1414, 1483, 1495, 1500, 1500 for m=8,10,12,14,16,20. These are finite computational checks, NOT an asymptotic lower bound or a simulation of a one-tape reduction.

Reproducible Python source: experiments/meta/2026-10-18_magred_distance_overlap9_test.py. Raw data: results/raw/meta/2026-10-18_MAGRED_DISTANCE_OVERLAP9_raw.json.

## CHARGED LEDGER AND REPAIRED SUFFICIENT CONDITIONS

Source s=N^beta; target t=N^tau; short anti-checker for a near-half-distant **source YES** has m=N^{tau+o(1)} records and output length L=N^{tau+o(1)} bits, with address serialization included. This meets the dimension-free interpolation floor yet carries the **wrong** source label. An actual promise-pure translator must use a selection rule which outputs a small-t-consistent sample for EVERY source CC(f)<=s, despite some of those sources being strongly anti-checker-positive, and t-inconsistent for EVERY source CC(f)>s. That choice is equivalent at the output-label level to distinguishing the original source threshold, so hiding an exhaustive source MCSP decider inside selection is circular.

The exact adaptive query floor from MAGRED-EDGEADAPT8 remains: any bounded-error standalone quotient of total exact MCSP requires Omega(N) source probes on a worst-case source YES. A full N-bit scan is still not excluded by this theorem or the query lower bound. The published CHMY randomized one-work-tape N^1.99 lower bound holds for its particular threshold s=N^mu and tape model, not for all beta. There is NO same-tape cheap full-scan t-selector here and NO transported exponent rho>lambda.

**Finite-depth guard:** if a proposed cascade carries an original size-s witness as the explanation for target YES after d contractions, the obvious certificate has size Theta(s log N)=N^{beta+o(1)}. Relative to an output of length L_d<=N^{lambda^d+o(1)}, the witness-verification exponent grows like beta/lambda^d. Thus *this explicit-witness implementation* is not a jointly NP-uniform target with a stage-independent exponent. This is not a proof that no alternative joint encoding/verifier exists. Similarly, an anti-checker at size t_j witnesses hardness only above t_j, not above the original source s.

MODEL WARNING: the output is sparse-list Partial-MCSP, not a dense length-N wildcard truth table; model-fusion, work-tape position, one-way input, random seeds and any target execution must still be charged. Known cell-probe, formula, proof-system and anti-checker **circuit** lower bounds do not supply those charges.

### Surviving target: SELECTIVE-YES-GUARD10

Find a genuinely computationally cheap same-one-tape source-adaptive selector which (i) reads N bits in declared machine model, (ii) chooses a t-consistent sample on every CC(f)<=s including the far-from-C_t functions in this theorem, (iii) chooses a t-inconsistent sample on every CC(f)>s with bounded error, (iv) has total time below the CHMY c=1.99 exponent at its actual mu, including serialization and fusion, and (v) gives a jointly uniformly low iterated target language with no increasing verifier exponent. Test strategies first against the 64-bit f_yes/f_no pair above and the far-from-C_t k-wise ensemble.

**Proof status:** elementary restricted theorem and finite check, independent review pending; no efficient selective compiler; no P versus NP separation. P versus NP OPEN.

## References

1. J.P. Schmidt, A. Siegel, A. Srinivasan, *Chernoff-Hoeffding Bounds for Applications with Limited Independence*, SIAM J. Discrete Math. 8(2), 1995. https://doi.org/10.1137/S089548019223872X
2. M. Cheraghchi, S. Hirahara, D. Myrisiotis, Y. Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23
3. I. Oliveira, J. Pich, R. Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, Theory of Computing 17(11), 2021. https://theoryofcomputing.org/articles/v017a011/
4. S. Hirahara, *NP-Hardness of Learning Programs and Partial MCSP*, FOCS 2022. https://eccc.weizmann.ac.il/report/2022/119/
5. S. Moran, A. Yehudayoff, *Sample Compression Schemes for VC Classes*, JACM 2016. https://doi.org/10.1145/2890490

<!-- END_OF_VERIFIED_REPORT::MAGRED-DISTANCE-OVERLAP9::P_VS_NP_OPEN -->
