# LOCALITY-LEDGER33 (2026-10-22)
Status: established restricted lemmas; P vs NP OPEN. No all-input SAT-to-ordinary-MKTP reduction.

**Source-index KT transfer.** If F_t has an O(log N)-bit, polylog-time source-indexer and G(F,i) uses polylog-time, polylog-many source bit probes per output index, then the full target has an ordinary source-free polylog-time indexed program containing t. Thus KT(G(F_t,*))=polylog N=o(M^(1/k)), any fixed k. An indexed 8-clause minimally UNSAT 3CNF padded by t duplicates supplies explicit easy UNSAT instances. Local hashes cannot produce guaranteed HIGH KT here.

**Critical clause placement.** For a q-probe, source-independent address sampler and m=t+8 clauses, place the one-bit critical sign change among m slots. An opposite-label SAT/UNSAT 3CNF pair exists whose generated targets differ in at most floor(qM/m) positions. Hamming closeness is NOT a KT classification proof.

**Hostile audit:** 1,765 assertions, zero failures; all 258 n<=5 late-selector INDEX cases SAT iff x_j, deletion-minimal UNSAT cores, length-matched padded 3CNF pairs and synthetic source-index reconstruction. With BLAKE2s over three indexed source bits, t=7,31,127,511 gave respective changed-target-bit counts 2/1024, 6/4096, 9/32768, 10/262144.

**Exact k=241 accounting:** M=N^(6/5+o(1)), p=M^(1/241+o(1)); per-bit budget minus p exponent is exactly 1/48200. MMW Theorem 4.2 after replacing Sigma3 queries with an ordinary length-q solver of exponent C has conservative bound M p^(C+1). At k=241 and C=1 its exponent 1.2099585 exceeds 1.205. Sufficient arithmetic for this approach is k>240(C+1). The unknown PH exponent remains charged.

First missing arrow: fully charged, all-input, genuinely opposite **ordinary KT** classifications, including padded easy UNSAT. No proof of high KT from hashes or apparent randomness.

Sources: McKay-Murray-Williams STOC 2019, Theorem 4.2; Ilango, SIAM J. Computing 2026 (random-oracle result, not ordinary unrelativized KT).
