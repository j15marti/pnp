# MAGRED-HASHSTREAM4 | 2026-10-18 14:33 KST

STATUS: PROVED/EXACT in the restricted one-way input model, pending independent review; COMPUTATIONAL finite controls. P versus NP OPEN.

## PROPOSE ATTACKS
Test output-length versus workspace in polynomial fingerprints; test premature-output escape; test beta-uniformity of the hash-image witness verifier; test error multiplication through repeated randomized reductions.

## SEARCH AND RECONCILIATION
Reviewed THRES-HASHBRIDGE4, THRES-LOSSYPROBE2, CONE-SYNTHESIS2, CLOCKSAT1, DATA-DIRECTSUM1, MAGRED-TAPEFUSION3, ASYMPTOTIC-CONE5, and primary CHMY 2021 (one-work-tape plus one-way input), MMW 2019 (streaming MCSP), and OPS 2021 (Gap-MCSP circuits). AFFINE-KERNEL4 already treats fixed-hash collisions and is not claimed as new.

## BUILD: HASH-STREAM-RANK4
Let K=GF(2^b), let alpha have algebraic degree b, and let N>=2b. Compute H_alpha(f)=sum_{i=0}^{N-1} f_i alpha^i from a one-way stream of N bits, emitting the standard b-bit hash value exactly. No payload bit can be emitted before reading the first N-b source positions, because every nonzero coordinate functional is sensitive to some one of the last b coefficients, which are a field basis. The first b coefficients are also a basis. Consequently, 2^b prefixes at the N-b cut yield different partial hashes, and with a common zero suffix they require 2^b distinguishable machine states. Hence exact deterministic memory is at least b bits, and standard bounded-alphabet one-work-tape space is Omega(b). This is a one-pass storage theorem, not a general time lower bound.

If a randomized transducer emits no payload before that cut and recovers the entire fingerprint with error epsilon<1/2, Fano's inequality applied to the uniform b-bit prefix message yields memory at least b-h2(epsilon)-epsilon*log2(2^b-1). The early-output restriction is essential for the stated randomized proof. Rereading source or random-access per-coordinate evaluation escapes.

## BUILD: BETA-QUANTIFIER-GUARD4
The indexed hash-image witness verifier in THRES-HASHBRIDGE4 explicitly scans all N circuit input positions. With s=N^beta and target description length L=N^(beta+o(1)), this verifier takes at least L^(1/beta-o(1)) time. Along beta_j->0, the displayed verifier exponents diverge. Separate per-beta NP verifiers do not supply one common uniform exponent K under P=NP. A different, jointly polynomial verifier could repair this; this is no intrinsic complexity lower bound.

## ERROR AND MODEL
A 7/8-correct reduction plus a 2/3-correct target solver guarantees only 7/12 success. Amplifying the solver to error 1/12 gives 77/96 success, with all calls charged. Four independent 7/8-success stages have conservative all-success guarantee (7/8)^4<2/3. Successful iteration requires an explicit error budget. Hash output is an indexed image problem, not ordinary MCSP/Gap-MCSP, and the one-work-tape fusion proof remains OPEN.

## TESTS AND NEXT
Exhaustively checked all 504 field seeds for b=3..8; 936 basis and 3342 suffix-dependency assertions passed, plus full 2^b prefix image for one full-degree seed per field. Full-degree counts: 6,12,30,54,126,240. Source: experiments/meta/2026-10-18_magred_hashstream4.py. Raw: results/raw/meta/2026-10-18_MAGRED_HASHSTREAM4.json.

NEXT: HASH-IMAGE-BRIDGE1 needs a joint-beta uniform verifier and one-work-tape, promise-preserving, error-controlled compiler charging b-bit space, source sweep and target access. No lambda/rho improvement is established.
