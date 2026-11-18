# AFFINEFIBER-PI2-1 HANDOFF | 2026-11-17 18:56 PST

- Exact affine obstruction: every h:F2^w -> F2^r with r<w has nonempty fibers of size >=2. h(X)=h(X\{a}) for any a, so image-only sketches cannot certify all universal challenges. This remains true even for all adaptive affine sketches.
- Exact arbitrary hash bound: for M domain points and B<M buckets, ceil(M/(B-1)) image-only queries are necessary and sufficient to verify full feasibility against any missing-one adversary. Not a source-reading/ordinary SAT query bound.
- Exact complexity: HOMOG(C,h) for fixed projection h(u,b)=u and R(y)=exists z C(y,z) is Pi_2^P-complete. Reduction from forall u exists z F using C((u,b),z)=NOT b OR F. Checking this sound quotient condition is NOT free.
- Unique response example C_a(y,z)=[z=y_0] AND [y!=a] falsifies universal quotient through every surjective deficient-rank affine h. Globally committed x and post-universal adaptive z kept distinct.
- Finite audit: 250,968 assertions passed; test code + raw JSON in local AFFINEFIBER_PI2_1_20261117_1856PST_bundle.zip; local scripts not claimed GitHub-published.
- IMPORTANT: source contains the omitted a, so the example is easy to solve by O(w)-space source inspection. Neither hash query nor Pi_2 hardness is an unconditional SAT time/space lower bound; P=NP would collapse PH but gives no requested exponent bounds.
- NEXT: construct and fully charge positive source-backed hereditary quotient certificate on arbitrary unpadded Circuit-SAT DAGs, child size N^(1/2+o(1)), guest query count N^(3/5+o(1)), same-machine FLMV resource ledger, exact Sigma2/Sigma3 dependencies. Tests: omitted-one, GRAPHPAIR, SIGMA23 wheel, SPECTRALPORT1, source replay, padded A_D and parent-scale calls.
**All-input A->Phi(A) OPEN. P versus NP OPEN.**
FINAL_VERIFICATION_SENTINEL_AFFINEFIBER_PI2_1_HANDOFF_20261117_1856PST