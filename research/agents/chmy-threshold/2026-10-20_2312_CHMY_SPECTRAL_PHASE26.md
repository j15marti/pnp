# CHMY-SPECTRAL-PHASE26 | 2026-10-20 23:12 Asia/Seoul
**Status:** new restricted label-mixed-fiber theorem and phase-query frontier proved, finite checks completed; both P-vs-NP proof routes remain OPEN.

## Ideas proposed before literature
(1) Full nonlinear Walsh-magnitude/autocorrelation quotient rather than local copies; (2) repair lost spectral phase with adaptive signed Walsh queries; (3) dual-local-PRG hybrid against actual CHMY machine; (4) test compatibility with OPS Gap-MCSP.

## Theorem 26A (proved, exact restricted semantic falsifier)
Fix 0<beta<1/2, N=2^(2d). Let f_h(x,y)=x.y XOR h(y), where x,y in F2^d. Direct Walsh expansion proves W_f(a,b)=2^d*(-1)^(h(a)+a.b) for every a,b. Consequently every f_h has the same COMPLETE indexed Walsh magnitudes 2^d and the same FULL autocorrelation (N at zero, zero elsewhere). If h(0)=0 then all also have the same Hamming weight and same histogram of signed Walsh values. If XOR_y h(y)=1, their complete ANF degrees all equal d (d>=3).
There are 2^(2^d-2) such h. h_easy(y)=AND(y_1,...,y_d) has a circuit of O(d) gates, hence CC(f_h_easy)<N^beta. Circuit counting gives at most 2^O(s log(s+d)) d-input functions computable by s gates; for s=N^beta, this is 2^o(2^d). Therefore some h_hard of the same constraints has CC(h_hard)>N^beta, hence CC(f_h_hard)>N^beta by restricting x=0. These opposite-MCSP-label sources have IDENTICAL indexed magnitude spectra, signed-value histograms, full autocorrelations, weights, and degrees. Every deterministic lossy quotient based only on these globally nonlinear features has a mixed-label fiber. In particular Q_N(f)[a,b]:=1{|W_f(a,b)|=2^d} maps both to the SAME N-bit string 1^N.
This is a semantic counterexample, NOT a lower bound on arbitrary MCSP computations.

## Theorem 26B (proved, restricted adaptive feature query model)
A deterministic postprocessor may know ALL features above for free and adaptively query at most q signed indexed Walsh coefficients, but may not independently query arbitrary truth-table bits. The Walsh answer at (a,b) reveals exactly h(a) because a.b is public. Follow queries on h_easy: at most q distinct h positions are disclosed. The same answers are consistent with at least 2^(2^d-q-2) h satisfying h(0)=0 and odd truth-table parity. For q<=(1-epsilon)2^d this family has 2^Omega(2^d) elements; the number of N^beta-size d-input circuits is only 2^o(2^d). Hence a hard h shares the ENTIRE adaptive transcript with the easy h. An all-input label-pure quotient in this restricted feature model therefore needs (1-o(1))*sqrt(N) distinct phase locations in the worst case. This is NOT a one-tape lower bound.

## Literature/model check
Original CHMY Theorem 16/Corollary 23: randomized two-sided error, one-way read-only input PLUS exactly one two-way work tape, actual local PRG, optional query strings of length N^o(1), specified RTM state-count/time/error bound (doi:10.4230/LIPIcs.STACS.2021.23). MMW (doi:10.1145/3313276.3316396) assumes the compression target exists; OPS (doi:10.4086/toc.2021.v017a011) is a nonuniform Gap-MCSP/Gap-MKtP model, not a replacement.
This experiment DOES NOT substitute a fake generator for CHMY's real G: its falsifier applies to all ordinary source truth tables and defeats the needed all-input semantic arrow before pseudorandomness is relevant. A proposed two-PRG hybrid would require proving both R(U_N) looks uniform on the larger domain AND legal one-tape simulation of D∘R; neither follows from locality.
A complete FWHT requires O(N log N) elementary word operations and O(N log N) bits if fully materialized, and this proposed quotient fails the intended one-work-tape streaming budget independently of semantics.

## Reproducibility
Executable chmy_spectral_phase26_audit.py and full report were generated in this run; 78,281 exact assertions, 0 failures. Exhaustive constraints: d=2 four functions, d=3 64 functions; d=4 sample 256 functions; 69,696 independently checked indexed Walsh coefficients; verified ANF degree, weight, signed histogram, autocorrelation and adaptive phase-query transcript pairing. Finite checks do not measure exact circuit complexity; asymptotic hard h exists by counting.

## Next best construction
Seek a source-checkable lossy *label-monochromatic* fiber invariant that retains indispensable information not lost by absolute Walsh spectrum, degree, weight or o(sqrt(N)) phase probes. Falsify by adaptive matched-transcript YES/NO pair first, THEN test CHMY actual local G, two-sided error, one-way tape fusion and full child/source access ledger. Maintain exactly two routes and five agent offsets. P versus NP OPEN.
<!-- END_VERIFIED_CHMY_SPECTRAL_PHASE26 -->
