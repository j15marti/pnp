# SOURCEQUERY-SYNTHESIS10 | 2026-10-18 17:57 KST
**Status:** Scoped theorem; P versus NP OPEN.

Read newest available Threshold Descent, Clock Gate, Resource Direct Sum, Magnification Red Team and main LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, K_ELIMINATION_TRANSFER4. Reviewed the primary STACS 2021 Cheraghchi-Hirahara-Myrisiotis-Yoshida Lemma 15, Corollary 23, Theorem 16.

## ROBUST-SOURCE-PROBE-FLOOR10
For N=2^n, source YES circuit complexity at most s=N^mu, source NO Hamming distance >delta*N from every function of complexity at most N^nu (0<mu<=nu<1, 0<delta<1/2), any randomized, adaptively bit-querying, standalone semantic quotient into disjoint YES/NO output sets with uniform per-input error below 1/2 requires q=Omega(s/n^2) source-bit queries. The target can be any nonlinear image language; it cannot continue reading the source.

Proof: degree <q uniform polynomials over GF(2^n), composed with binary trace, have O(q n^2) circuit size and their q evaluations on adaptively chosen distinct coordinates are indistinguishable from q samples of a uniformly random truth table. Uniform tables are delta-far from all size-N^nu circuits except with probability 2^{-Omega(N)}, by circuit counting and the Hamming-ball bound. If q<=s/(A n^2), the quotient would distinguish these two input distributions despite their identical transcripts, contradicting error <1/2.

Combine MAGRED-DIMFREE6: every m-record consistent partial table has a circuit of size at most 4(m-1)+O(1), so nontrivial NO at threshold t requires m=Omega(t). For m=N^a, t=N^tau, tau<=a. When a<mu, the selective generator must read q/m >= N^{mu-a-o(1)} times as many source bits as it emits records. This is necessary, not sufficient; a full one-way N-bit sweep remains possible.

Exact GF(8) audit: q=2,3,4,5, polynomial families 64,512,4096,32768; all adaptive transcript and two-record postselection distributions exactly matched those of all 256 uniform truth tables. Zero discrepancies.

PROOF DAG: ESTABLISHED scoped source-probe and interpolation lower bounds, classical polynomial independence, CHMY one-tape exact-MCSP lower bound. DERIVED model-matched robust-distance extension, independent review appropriate. CONDITIONAL cofinal K absorption and lossy-cascade accounting. OPEN selective full-sweep YES budget reduction plus NO soundness, same-one-tape fusion, jointly NP/PH-low image language, rho>lambda slope map. RETIRED naive sampling, fixed-threshold Partial-MCSP cascade, fixed-seed short hash-as-MCSP, uncharged KPI model transfer.

**Research allocation:** SOURCE-SWEEP-SELECTIVE-ANTICHECKER2 remains top. No P vs NP contradiction.

Primary: Cheraghchi et al., STACS 2021, DOI 10.4230/LIPIcs.STACS.2021.23; Alon et al., Random Structures & Algorithms 1992, DOI 10.1002/rsa.3240030308.