# MAGRED-EDGEADAPT8 | 2026-10-18 18:21 Asia/Seoul

**Status:** Restricted-model mathematics proved below, pending independent review. Full input-access and representation ledgers audited. No unrestricted time lower bound and **P versus NP OPEN**.

## PROPOSE ATTACKS -> SEARCH -> BUILD

**Attacks:** (1) strengthen the k-wise source-probe lower bound against *adaptive*, randomized, promise-pure quotients using the edge boundary of the complete MCSP property; (2) falsify a supposed semantic impossibility of source-adaptive threshold descent by allowing unbounded construction work; (3) look for source-answer circularity, dense-vs-sparse Partial-MCSP encoding drift, and generic one-tape simulation costs.

**Reviewed project:** \`LOSSY_PROMISE_CASCADE6\`, \`PARTIAL_SAMPLE_WEDGE7\`, \`PROMISE_CASCADE_FIXEDPOINT8\`, \`SOURCEQUERY_SYNTHESIS10\`, \`K_ELIMINATION_TRANSFER4\`, root \`main.tex\`, \`THRES_HASHBRIDGE4\`, \`CLOCKFEATURE5\`, \`RESOURCE_KPIPRODUCT6\`, \`MAGRED_KWISE_YESBUDGET7\`, \`MAGRED_DIMFREE6\`.

**Primary literature:** hypercube edge isoperimetry [1,2], randomized one-work-tape exact MCSP [3], circuit-only hardness magnification [4], and Partial-MCSP [5,6]. No citation transfers a lower bound between those models.

## THEOREM 1: EDGE-BOUNDARY-ADAPTIVE-QUOTIENT8

Let A be a nonempty proper subset of the N-bit Hamming cube. Let J be any randomized adaptive **bit-query** transformation with target YES/NO promises Y',N' disjoint. For each f in A require Pr[J(f) in Y'] >= 1-e_Y, and for each f outside A require Pr[J(f) in N'] >=1-e_N, where e_Y+e_N<1. Bad random seeds may land *outside* both promises; these are counted as failures. J may output seed metadata and use arbitrary computation other than accessing the source through charged input-bit queries.

Define D_A(f) to be the number of indices i for which flipping bit i of f leaves A. Let Q(f) be the expected number of **distinct** source-bit addresses actually read by J(f). Then for every f in A,

    Q(f) >= (1-e_Y-e_N) D_A(f).                               (1)

Furthermore,

    E_{f uniform in A} Q(f) >=
      (1-e_Y-e_N) [N-log_2|A|].                              (2)

**Proof of (1):** Fix an index i with f^i outside A. Couple the executions of J(f) and J(f^i) with identical random coins. Until the first source query to i, both transcripts and outputs coincide. If i is never queried, both outputs coincide. Since target YES and NO are disjoint, correctness on *both* coupled runs implies that i was queried. Failure probability is at most e_Y+e_N by union bound. Hence Pr[query i on f]>=1-e_Y-e_N. Sum this inequality over all outgoing neighbors of f. Linearity of expectation on the number of distinct queries proves (1).

**Proof of (2):** Let X be uniform over A. For each i, conditional on X with coordinate i omitted, the coordinate X_i is either fixed or fair over its two possible values. Therefore

    Pr[X^i in A] = H(X_i | X_{-i}).

By the entropy chain rule and monotonicity under conditioning,

    sum_i H(X_i | X_{-i}) <= H(X) = log_2 |A|.

Thus E_{f in A} D_A(f)>=N-log_2|A|. Average (1). This is the classical hypercube edge-isoperimetric inequality with a direct elementary entropy derivation. QED.

**Corollary for exact MCSP:** Let N=2^n, 0<beta<1 fixed, s=floor(N^beta), A={f:CC(f)<=s}. The standard fan-in-two circuit count shows log_2|A|=O(s log(n+s))=O(N^beta log N)=o(N). Therefore any randomized adaptive promise-pure quotient from **exact** MCSP[s] with two-sided error eps<1/2 must satisfy

    E_{source YES f uniform in A} Q(f) >=
       (1-2eps)[N-O(N^beta log N)].

At eps=1/3 it needs at least (1/3-o(1))N source-bit probes on average over the low-complexity YES set, hence also in the worst case. If YES is preserved perfectly, coefficient strengthens to 1-e_NO. This significantly improves the earlier N^{beta-o(1)} k-wise query floor for exact MCSP.

**Limits:** This is source-bit **query** complexity, not an N^{1.99} one-work-tape time lower bound. Full sequential scanning remains possible and costs N. The result does NOT automatically apply to Gap-MCSP or a far-from-small-circuits source promise: one-bit neighbors of YES may occupy the unspecified gap. It rules out adaptive *sublinear-reading* promise-pure quotients of total exact MCSP, not full-scan compression or non-coordinate output processing after that scan.

## THEOREM 2: ADAPTIVE-SEMANTIC-EXISTENCE8

For fixed 0<tau<beta<1, s=floor(N^beta) and t=floor(N^tau), there exists an exact, deterministic, **source-adaptive** quotient from exact MCSP[s] to the **sparse-list encoding** of Partial-MCSP[t], with m=N^{1-beta+tau+o(1)} *distinct, correctly labeled* samples and output length O(m log N)=o(N). This is strictly a statement of **semantic existence**, with *no computationally efficient reduction*.

**NO side:** For every size-t circuit C differing from source f on d positions, correct those positions using d point indicators and XOR. Then CC(f)<=t+O(d log N). Hence if CC(f)>s, every size-t circuit differs on at least d_*=Omega(s/log N) positions. The number of size-t circuits M_t is at most 2^{O(t log(n+t))}. A uniformly random m-point source restriction is inconsistent with *every* such circuit with positive probability when

    m >= (N/d_*) (ln M_t +1)
      = N^{1-beta+tau+o(1)}.

Exhaustively search the finite coordinate subsets to find one valid target NO sample.

**YES side:** Every f has at least N/2 points carrying its majority label. Since m=o(N), select m of these points. Its sampled partial function has a size-zero constant circuit, hence target YES.

**Crucial circular step:** To decide which sampling policy to execute, the semantic map first runs an exhaustive **source MCSP[s] decider**. It thereby preserves every YES and NO label, and the output fibers are truly promise pure. Since its output has o(N) bits, the map is many-to-one. But its runtime is not below the CHMY lower bound: the source decision has merely been hidden inside the compiler. This is a counterexample to *semantic impossibility*, NOT a positive source-efficient construction.

## REPRESENTATION-DRIFT8

The common dense representation of Partial-MCSP/MCSP* is a length-N truth table over {0,1,*}; replacing all but m entries by * still outputs length N, so its contraction exponent is lambda=1. The semantic map above uses a **different** language with input \`(n,t,[(address,label)])\` containing only m addressed records of n+1 bits each. It genuinely has length O(m n), but results stated for a dense partial truth-table encoding cannot automatically be invoked with sparse-list input-length parameters.

The sparse-list consistency language itself is in **jointly uniform NP**. With m records and threshold t, dimension-free interpolation gives a trivial YES for consistent records whenever t>=4m+O(1); otherwise t=O(m) and a circuit of size t is a polynomial-length certificate verifiable in polynomial time, with one exponent independent of stage j. This does not prove any hardness lower bound or same-tape compiler.

## EXACT FINITE CONTROLS (COMPUTATIONAL, NOT ASYMPTOTIC)

A reproducible standard-library Python experiment exhaustively enumerated up-to-s NAND circuits and boundary neighbors for (n,s)=(3,1),(4,1),(4,2),(5,2),(5,3),(6,3), with truth-table lengths N=8,16,32,64 and easy-family sizes 11,16,46,82,347,724. All six family checks satisfied the edge-isoperimetric inequality. In these small configurations, every easy source happened to have all N neighbors outside its easy family; this is a finite observation only.

For n=4,s=2,t=1, all 65,536 truth tables were enumerated in the NAND basis: 46 source YES, 65,490 source NO. A greedy source-adaptive target NO anti-checker needed at most five labeled examples; every YES allows at least eight equal-labeled examples. This finite example does not compress input bits once address serialization is counted.

For an actual shorter **sample payload** on the usual AND/OR/NOT basis, n=6,N=64,source threshold s=3,target t=1: six-variable parity depends on six essential variables and cannot use only three fan-in-two gates. Four sample addresses 0,1,2,3 have parity labels 0,1,1,0. Exhaustive enumeration of all 44 size-at-most-one AND/OR/NOT truth tables finds no consistent circuit. The four labeled examples have a 28-bit address/label payload versus the source's 64 bits, excluding parameter and format overhead. A source-YES function can instead output any four same-label points. The branch deciding which policy to use remains circular.

No finite test proves a superlinear algorithmic bound.

## CHARGED LEDGER AND NEXT TARGET

The query theorem yields r>=1 in any unit-cost source-input-access model for exact MCSP. The c=1.99 CHMY lower bound is established at **a specific exponent beta=mu chosen by that theorem**, not at every beta in (0,1). Only at that CHMY source threshold, and in its randomized **one-work-tape/one-way-input** model, does the admissible local reduction exponent need to lie in the still-open interval [1,1.99). The semantic map establishes output exponent a=1-beta+tau but provides no admissible r. If generic one-tape fusion has a quadratic penalty, theta*r>=2 already erases c=1.99. No target algorithm exponent K is eliminated: a compiler first deciding MCSP has unknown/high cost, and choosing stage j based on its own collapse-dependent exponent is circular. The Partial-MCSP source is not automatically another **total** MCSP instance, so iteration also needs a genuinely typed, uniform next-stage reduction.

**Highest-value next test: STREAMING-SELECTIVE-ANTICHECKER9.** Demand a source-independent algorithm in the exact CHMY tape model that reads all N bits, does not call an MCSP[s] decider, emits sparse labeled samples of total length N^{a+o(1)}, lowers threshold from s=N^beta to t=N^tau, preserves both source promises for every input with controlled error, and has actual composed time exponent r<1.99. Track work-tape buffer, address sorting and replay, sample-indicator computation, off-promise seeds, and same-model fusion. No known construction meets these requirements.

**Status:** Restricted lemmas proved, independent review pending. Full-sweep selective sampler OPEN. General cascade OPEN. **P versus NP OPEN.**

## References

1. Rashtchian and Raynaud, *Edge Isoperimetric Inequalities for Powers of the Hypercube*, Electronic Journal of Combinatorics 2022. https://arxiv.org/abs/1909.10435
2. Ellis, Keller, Lifshitz, *On a Biased Edge Isoperimetric Inequality for the Discrete Cube*, 2017. https://arxiv.org/abs/1702.01675
3. Cheraghchi, Hirahara, Myrisiotis, Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23
4. Oliveira, Pich, Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, Theory of Computing 2021. https://theoryofcomputing.org/articles/v017a011/
5. Hirahara, *NP-Hardness of Learning Programs and Partial MCSP*, FOCS 2022. https://eccc.weizmann.ac.il/report/2022/119/
6. Ilango, *Constant Depth Formula and Partial Function Versions of MCSP Are Hard*, SIAM Journal on Computing 2022. https://doi.org/10.1137/20M1383562

<!-- END_OF_VERIFIED_REPORT::MAGRED-EDGEADAPT8::P_VS_NP_OPEN -->
