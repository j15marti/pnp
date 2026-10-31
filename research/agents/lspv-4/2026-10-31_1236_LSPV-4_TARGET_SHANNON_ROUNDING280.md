# LSPV-4 TARGET-SHANNON-ROUNDING280
31 October 2026, 12:36 PDT. **PROVED/EXACT for a restricted compiler architecture; COMPUTATIONAL independent finite controls; CONDITIONAL FLMV transfer; P versus NP OPEN.** Independent external mathematical review pending.

## Exact obstruction
The target is **all valid** duplicate-free proper Monotone 3-SAT-(2,2) formulas of Döcker (arXiv:1912.08032), not an easy all-positive subfamily. Every clause has three distinct same-sign literals; every variable has two occurrences of each sign. Invalid strings are rejected in any total target-language solver. The broader signed strict-2P2N language remains a comparison superset.

**Quota lemma.** Every nonempty valid target formula has n>=6 divisible by 3, exactly m=4n/3 clauses, and exactly m/2 clauses of each sign. Proof: 3m=4n, 3m_+=3m_-=2n; n=3 would require two duplicate positive triples, so is impossible.

**Three-pivot rounding theorem (restricted).** Suppose a target-valid re-encoding of a residual under r assigned variables retains a separate active target variable for every one of its n-r unassigned original variables, possibly adding auxiliary variables or changing every clause. Then
  n_child >= max(6, 3*ceil((n-r)/3)),
  m_child >= 4*max(2,ceil((n-r)/3)).
In particular, for r=1 or r=2, both child variable count and clause count are at least those of the parent. This does not restrict re-encoders that eliminate or merge source variable identities with a separately proven semantics.

**Full Shannon portfolio no-go (restricted).** If an algorithm enumerates every one of 2^r assignments to r pivots as distinct target-valid children, without branch pruning, merging or early proof, and retains all n-r remaining source variables distinctly, it cannot simultaneously guarantee q<=N^(gamma+o(1)) and maximum physical child length <=N^(lambda+o(1)) for any finite gamma and fixed lambda<1. Indeed q=2^r forces r=O(log N). Every child then has n-O(log N) or more variables, and under explicit canonical DIMACS its bit length is (1-o(1))N, contradicting the power-short requirement. This covers the proposed ARC (gamma,lambda)=(3/5,1/2) only in the stated **full-Shannon, identity-preserving architecture**. A certified interface DP, source-dependent compression or branch merging is not ruled out.

Same-source both-label correctness remains the standard exact Shannon identity SAT(F)=OR_a SAT(F|a), UNSAT(F)=AND_a UNSAT(F|a). Raw cofactors are generally outside the target grammar and require fully charged re-encoding. A solution to the present restricted theorem is NOT the missing arbitrary-A -> Phi(A) compiler.

**Canonical encoding:** ASCII "p cnf n m\n" header plus exactly 3 signed decimal integers and "0\n" per clause with one space between tokens, no comments or extra spaces. The byte length depends only on n:
  B(n) = len("p cnf n (4n/3)\n") + 4*(4n/3) + 2n + 4*sum_{i=1}^n digits10(i).
Thus B(6)=78 and B(198)=3410, in this new encoding. ARC279's different DIMACS serializer produced different physical bits and is not substituted.

## Four falsifiers and matched original-source controls
F1 raw cofactor stays target-valid: FALSE. F2 one/two-pivot identity-preserving target reentry must physically shrink: FALSE. F3 complete 2^r Shannon splitting supports both small child number and sqrt-length: FALSE within declared class. F4 original S/U conflict aggregate distinguishes opposite SAT labels: FALSE, demonstrated by U198 UNSAT and V198 SAT with identical pair counts.

Original-source checks Y6 SAT (20 models by exhaustive enumeration), U198 UNSAT (independently replayed six 32-variable local contradiction modules, a complete 64-assignment six-variable core, and a separately checked 89-node/329-unit/45-leaf local refutation), V198 SAT (complete original-clause checked 198-bit witness). Valid inputs have (n,m)=(6,8),(198,264),(198,264). U/V each have 351 pair vectors 1001, 786 vectors 0110, 33,579 vectors 1111, none 0000. Y has 12/14/2. Every source's coherent 0^n and 1^n assignments has N_0=N_3=m/2, N_1=N_2=0. Local signed occurrences, S/U inversions, all 34,716 clause-pair modes for each large source, partial flips and both raw cofactors are included in the local complete reproducibility archive. The standalone new independent raw verifier checked 89,096 conditions without failure. Independent U/V proof replay also succeeded.

Matched 1200-node ordinary UP-DPLL controls: Y parent 4 nodes, two one-pivot children 4 and 3 nodes; both U/V parents and all four children UNRESOLVED at budget 1200 (not UNSAT or SAT claims). These are logical-operation counts, not matched native FLMV TM timings. Source recognition, child selection, failed trials, output access, guest index-tape operations, replay and peak live space remain chargeable.

## Exact FLMV audit and missing transfer
For c>1 set f_0=1, f_k=c f_(k-1)/(1+f_(k-1)), d_k(c)=min((1/f_k-c)/k,c^(-k)). Exact fractions give d*(6/5)=23/45 and d*(241/200)=11642479/23232400. At both, unique optimum k=2; k=1 and k=3 are smaller and all k>=4 are excluded by the strict upper bound d_k<=c^(-4)<d_2. FLMV 2005 excludes same-machine DTISP(N^c,o(N^d)) simulation of NTIME(N); quantitative transfer to Döcker's target requires a compatible, fully charged source-to-target reduction or a directly applicable theorem. NP-completeness alone does not transfer the numbers. The proposed ARC fixed point (6/5,1/2) is CONDITIONAL, not achieved.

## Searches, reconciliation, and publication limitation
Web/Google queries: "Döcker monotone 3-SAT-(2,2) NP complete duplicate free cofactor closure"; "FLMV Theorem 5.7 SAT time space forbidden envelope"; "fine-grained SAT monotone (2,2) reductions". Primary papers Döcker 2019 arXiv:1912.08032 and FLMV JACM 52(6) 2005 https://lance.fortnow.com/papers/files/tst.pdf (PDF Theorem 5.7 page visually inspected). Separate GitHub connector searches: j15marti/pnp "cofactor variable quota rounding" (no exact match), "Shannon target child" (existing ARC-TRACE-SHANNON111), "CP22LIFT1" (prior size costs); openai/math "SAT" (unrelated formal SAT and thresholds, not this reduction). Do not infer novelty from absence of matches. Read REDIRECT1, CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted MCSP only), CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, root AGENTS/CODEX/pnp-research, issue #3, LSPV-4 ARC279, and earlier original source/certificate.

Full local archive: sandbox:/mnt/data/arc_lspv4_280/ARC_TARGET_SHANNON_ROUNDING280_COMPLETE.zip (formal 5-page PDF/TeX, complete producer and independent verifier, 2.88 MB original-indexed raw JSON, baseline measurements, exact arithmetic, source fixture, proof certificate, SHA-256 manifest). The persistent Library upload returned container_session_unavailable and full GitHub raw/code mirroring is therefore **pending** if not published separately. Root main.tex must be reconciled only inside LSPV-4 ownership markers, otherwise explicitly pending. Nothing changes the five task identities, offsets, enabled/paused states.

**OPEN NEXT ARROW:** devise a total all-valid-target, reject-malformed, source-authenticated hereditary re-encoder that provably eliminates most unassigned identities or certifies merges/pruned branches, plus fully charged indexed guest bit access and peak workspace. Then verify a quantitative FLMV SAT-to-target transfer. No lower bound on arbitrary SAT deciders follows from this report. P versus NP OPEN.

References: Döcker (2019), https://arxiv.org/abs/1912.08032; Fortnow, Lipton, van Melkebeek, Viglas (2005), https://doi.org/10.1145/1101821.1101822; project ARC279 and ARC-LINEAR22-SATURATION1.
