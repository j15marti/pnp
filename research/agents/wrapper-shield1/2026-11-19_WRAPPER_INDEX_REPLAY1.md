# WRAPPER-SHIELD1 / INDEXREPLAY1: charged sparse checkpoint replay and polarity audit
Date: 2026-11-19. Status: **PROVED/EXACT (restricted source model; independent review pending)**; **COMPUTATIONAL (eight bounded controls)**; **CONDITIONAL (local exponent transport)**; **OPEN (unrestricted SAT, P vs NP)**.

## Exact integration target
For authenticated explicit source records representing (F=\bigvee_{z\in Z}\bigwedge_{j<B}G_{z,j}(y_j)), where (R=|Z|\le N^{.195}), (B\le N^{.65}), (M\le N^{.35}), (BM=O(N)), and private variables are disjoint after fixing z:
SAT iff (\exists z\ \forall j\ \exists y_j\ G_{z,j}); UNSAT iff (\forall z\ \exists j\ \forall y_j\ \neg G_{z,j}).
This is an **explicit-format assumption** and has NOT been established for arbitrary CNFs.

YES specialist: verified satisfying assignments for *every* block of one row, assembled using disjoint private coordinates, or UNKNOWN. NO specialist: verified local UNSAT certificate for a selected block in *every* row, or UNKNOWN. Source authentication and exact local checker are compulsory. A bad selector/wrong path is not an answer. A complete uniform deterministic one-sided specialist decides SAT by complement and is not available from this result. Free polarity advice leaks the source answer.

## SPARSE-CHECKPOINT-REPLAY1
**PROVED/EXACT, restricted sequential-record random-access input model.** For B variable-length source records of length at most M, total O(N), and Q authenticated requested record indices, after an O(N) full-source scan store only every q-th record's offset. On a random-access indexed read-only input, access to record j replays at most q sequential records from checkpoint floor(j/q)*q. All address/index tapes, scanning, parsing, replay, records, checker, failed branches, and live ancestors are charged. Symbolic ledger:
```
T_index+replay = O(N + Q*q*M + Q*polylog N)
S_index       = O(ceil(B/q)*log N)
S_peak        = O(S_index + M + S_local + k_live + log N).
```
At (q=\lceil B\log N/N^{1/2}\rceil=N^{.15}\operatorname{polylog}N) and Q=R, the index is O(N^.5) bits and replay scan at most (N^{.695}\operatorname{polylog}N) bits/steps beyond the O(N) build, provided the source encoding and local checker satisfy assumptions. Full offsets cost (\Theta(B\log N)) bits and violate the sqrt target at saturation. The index does **not discover** correct indices or local refutations. Without any index, rescanning full source per row costs (RN=N^{1.195}), already under the claimed (N^{1.33}) time threshold, so indexing is not the load-bearing barrier.

For a complete deterministic local checker of T_loc(M)=M^{a+o(1)}, S_loc(M)=M^{b+o(1)}, a row-major exhaustive all-block realization costs:
```
T = N^(max(1.195, 0.845+0.35*a)+o(1))
S = N^(max(0.35, 0.35*b, 0.195)+o(1)).
```
The proposed T<=N^1.33 and S<=N^.5 polylog therefore require a<=97/70 and b<=10/7. A hypothetical polynomial SAT seed has **no** guaranteed such exponents. An extensionally identical padded seed A_D incurs its explicit N^D delay per reached call.

Correct-path UNSAT selector advice takes k=R ceil(log2 B) bits **plus local refutations**, and enumerating it costs up to 2^k=B^R=N^{Theta(N^.195)} verifier calls. A YES row index alone is short but private SAT witness bits may be Theta(N). Adaptive/alternating policies need their entire strategy or fully charged universal branches: a favorable path is not a free decision algorithm. If all YES and NO have polynomial-size, polynomial-time-checkable source certificates then NP=coNP, not established.

## Executed T5 controls
Independent graph-generation and source verification used H9 with four internally vertex-disjoint T5 paths ++, +++, ++-, --- and path-cofactor count vectors
(0,1,1,0,2), (3,0,3,1,1), (1,3,0,3,1), (3,1,1,3,0). Their pointwise product is zero at each Z5 endpoint difference (NO certificate). All eleven single-edge deletions have separately found SAT witnesses. Synthetic row-conditioned block copies were used to test YES, NO and deliberately incorrect NO choices; **this is not a generic CNF reduction**.

| R | B | N source bytes | Full directory bytes | Sparse bytes | sqrt(N) byte cap | Sparse build+replay bytes SAT / UNSAT |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 32 | 4,068 | 48 | 48 | 63 | 4,459 / 4,578 |
| 6 | 80 | 10,158 | 140 | 70 | 100 | 11,200 / 11,329 |
| 8 | 128 | 16,313 / 16,314 | 224 | 112 | 127 | 17,587 / 17,854 |
| 10 | 1024 | 131,098 / 131,099 | 2,304 | 331 | 362 | 135,699 / 136,220 |

Eight test cases passed source checks, 4/6/8/10 incorrect NO selectors were rejected, correct NO source-refutations verified, and correct YES witnesses for respectively 32/80/128/1024 private blocks were verified. Truncated SHA256 key-only caching produced SAT/UNSAT collisions (2-bit:6; 4-bit:2; 6-bit:1; 8-bit:0), illustrating that a finite zero-collision result cannot justify semantic cache reuse. Exact authenticated source equality required.

The test used Python stdlib and seed 20261119. Full report and executable/raw JSON are in the conversation artifact WRAPPER_SHIELD1_INDEX_REPLAY_20261119_bundle.zip. Hashes: code SHA256 d7af435267d3111ff1b912fa8a1ae5a36d699d7abe4dd93dc216b4ed83bf9ecc; raw JSON SHA256 a1134eb16b0b59e9d1b71b97d01ee124c54accd2c973dda2b5d79214636861f4; report SHA256 858dbcc81155ab0420018c24fe8ce194ab08364dd48818280a6bb8432123d47f. Python fixture itself retains source for generation, so physical Python heap is **not** claimed to implement the asymptotic space bound. The mathematical directory construction is streaming.

## Model / barriers / controls
Known theorem: Fortnow et al., JACM 2005 [https://lance.fortnow.com/papers/files/tst.pdf], random-access read-only input multitape Turing machines, **charged index/work tapes**, write-only output. At time exponent c=1.33, Theorem 5.7's k=3 bound excludes DTISP[n^1.33,o(n^0.27910)] SAT (via quasilinear completeness); Theorem 6.4's k=3 bound excludes the relevant co-nondeterministic class with o(n^0.08930) space. Neither rules out sqrt(N) workspace. Fortnow JCSS 2000 [https://lance.fortnow.com/papers/files/npvsnl.pdf] gives SAT not in NTISP[n^(1+o(1)),n^(1-epsilon)]. The strongest deterministic SAT subpolynomial-space time benchmark cited here is c<2cos(pi/7)~1.80194, not at S=N^.5. These are random-access TM results, not zero-overhead word-RAM transfers. Haken/Urquhart resolution lower bounds do not exclude unrestricted SAT algorithms. Read-only external certificate tape is not free ordinary NTISP writable memory.

A constant-degree expander 2CNF primal graph defeats automatically splitting arbitrary original CNF into sublinear blocks by fixing only O(log N) variables and syntactic deletion; it does NOT defeat semantic solver shortcuts or prove any SAT time lower bound.

DISJ PASS **only in source-authenticated format**; relativization PASS for restricted indexing but no separation consequence; simultaneous DTISP NOT MET for an unconditional arbitrary-CNF solver; deterministic configurations OPEN for unrestricted extraction. All output and certificate access must be accounted for. Independent review pending, P versus NP OPEN.

**Single next lemma:** SOURCE-BOUND-UNSAT-SELECTOR1: provide an all-input source-authenticated CNF-to-row/block compiler (or a carefully defined NP-hard domain) and uniform sound deterministic charged discovery of one locally refutable block for *each* row on every NO input, with correct YES routing and **both** child polarities; test expander/Tseitin and growing-girth T5 H33. Until that is done, sparse replay closes only the index/lookup accounting subproblem.

Project background: research/agents/lspv-1/2026-10-16_LSPV-1_WRAPPERCHARGE1_HANDOFF.tex; research/coordination/2026-11-18_1822_LSPV3_OBSTRUCTION_COVER_CORRECT_PATH_HANDOFF.md; research/agents/sigma-primary/2026-11-18_T5_STATICSELECTOR34.md. Existing five TMR manuscripts, schedules, issue #3 and retired proof trackers left unchanged.
