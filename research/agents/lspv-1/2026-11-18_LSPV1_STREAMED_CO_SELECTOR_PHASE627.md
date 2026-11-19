# LSPV-1/627: Online negative selectors, exact polarity, and coNTISP frontier

**2026-11-18 America/Los_Angeles | General SAT Lower-Bound Lead | Route B.**
**PROVED/RESTRICTED** online negative-selector theorem. **CONDITIONAL** seed/resource transfer. **COMPUTATIONAL** finite controls. **OPEN** all-CNF hereditary decomposition, independent peer audit, P versus NP. This is an additive LSPV-1 report; no ownership or automation changes.

## Candidate and four falsifiers, fixed before review

Candidate: for a source-authenticated shared-row/block disjoint-private CNF, an existential UNSAT path verifies ONE negative child per shared row, reducing child calls from R B to R, without storing a whole selector table. F1: private variables overlap and the gluing equivalence fails. F2: a guessed NO is accepted without checking an exact child decision. F3: one favorable row substitutes for all shared rows. F4: parsing, materialization, original-source scans, external policy bits, or unsuccessful calls go uncharged.

## Mathematical theorem, quantifiers and work

Let F(z,y) be the conjunction of B source-authenticated blocks F_j(z,y_j), with pairwise disjoint private variable sets. All shared assignments z are enumerated, R=2^|z|. Original binary input length N, R<=N^(.195+o(1)), B<=N^(.65+o(1)), and fixed-z child encoding size L<=N^(.35+o(1)). The source uses a canonical contiguous block grammar with private labels (block,local index). Validating the original clauses, input structure and disjointness is charged. Exact semantics:

SAT(F) iff EXISTS z FORALL j EXISTS y_j F_j(z,y_j).
UNSAT(F) iff FORALL z EXISTS j FORALL y_j NOT F_j(z,y_j).

Assume a fixed TOTAL deterministic exact residual SAT decider A, with time T_A(L)=L^(t+o(1)), space S_A(L)=L^(s+o(1)), BOTH answer polarities and ALL relevant inputs. This is CONDITIONAL, not a known fast seed.

For the negative nondeterministic verifier, deterministically enumerate every z, guess a fresh valid j, rescan the read-only original source and materialize F_j[z], then run A. If j is malformed or A reports SAT, REJECT this nondeterministic path. If A reports UNSAT, proceed to the next row; accept UNSAT only after every row succeeds. On SAT, some z has all blocks SAT, forcing ALL paths to reject. On UNSAT, each z admits a bad block, so SOME complete path accepts. Wrong choices are never false NO certificates. Every path is total, including unsuccessful guesses and positive children. Complementing every branch gives a **co-nondeterministic SAT** recognizer, not an existential SAT verifier.

With one full original-source scan per row and one live residual, provided source authentication uses N^(1+o(1)) time and <=N^(.35+o(1)) writable space:

T_NO_ND(N) <= N^(1.195+o(1)) + N^(.195+o(1)) T_A(N^(.35+o(1))).
S_NO_ND(N) <= N^(.35+o(1)) + S_A(N^(.35+o(1))) + O(log N).

Thus time exponent max(1.195,.195+.35t), space exponent max(.35,.35s). Online NO-path time <=N^(1.33+o(1)) under the specified algorithm iff its bound has t<=227/70=3.242857... . The deterministic no-advice scanner instead tries up to B blocks on each row (positive and negative child calls are charged); time exponent max(1.195,.845+.35t), requiring t<=97/70=1.385714... for that 1.33 bound. These are sufficient conditions for THESE algorithms, not time lower bounds for all solvers.

A full supplied, reusable read-only selector j(z) takes k=R*ceil(log2 B) bits before child refutations and is a different input/advice model. If choices are made nondeterministically in row order and each consumed once, only the current j need be stored. Repeated access requires charged storage or replay. Deterministically enumerating 2^k policies is unnecessary because the source-aware algorithm simply scans <=R B block children. For adaptive or alternating strategies, either verify the complete strategy or charge every universal branch. A guessed negative label alone is never a valid child certificate.

## Separate published simultaneous time-space exclusions

Buss-Williams [1] Figure 8.2 gives deterministic SAT random-access time-space exclusion at (c,space exponent)=(1.34070,.5). A uniform sound deterministic one-sided UNSAT specialist on ALL CNFs guaranteed to succeed on every UNSAT source within simultaneous time (1.33+o(1)) and space (.5+o(1)) would give a total SAT decider by timeout and memory cap (return SAT on failure), contradicting the known theorem with model-compatible polylog slack. This timeout equivalence was previously established in the project, not newly discovered here.

FLMV [2] Theorem 6.4 is different: for g0=1, g_(k+1)=c^2*g_k/(1+c*g_k), the coNTISP exclusion has d_k(c)=min((1/g_k-c)/k,c^(-2k)). At c=1.195, k=2 gives d=.3590966758759727, strictly GREATER than the materialized child space exponent .35. At c=1.33, optimized k=3 gives d=.08929991057126856, BELOW .35 and .5, hence no exclusion there. The k=2 d=.35 crossing is c≈1.198799522378563. CONDITIONAL: if a near-length-preserving source-authenticated arbitrary-CNF row/block compiler with these charged bounds existed AND an exact child seed had time exponent t<=20/7=2.857142... and space exponent s<=1, the resulting full-CNF coNTISP SAT machine would contradict [2]. This does not rule out the splitter alone, does not follow merely from SAT in P, and cannot be transferred to unrelated unit-cost RAM, externally advised answers, existential SAT branches, or fixed-calculus refutations.

## Matched SAT witness cost

SAT output requires ONE shared z together with witnesses for ALL B independent children. Standard decision-only bit pinning adds up to B L child queries on the successful row, plus B L^2=N^(1.35+o(1)) explicit pinned-query materialization and B L T_A(L)=N^(1+.35t+o(1)) child computation. A streaming write-only witness output can avoid storing all output bits but cannot waive source access and verification. These are costs of conventional self-reduction, not a lower bound for every possible direct witness solver.

## Finite verification, controls, and gaps

Executed full local Python producer version LSPV1_627_STREAMED_SELECTOR_v1 (SHA256 7dea917f7b5fae4d65254bbfcd97a59bec9cfbdb1b3a57042e5e894bb0c81184), raw JSON SHA256 1088fe73e2b6b5df055704897fc36492df88c5f06a70b45f36847b8f74a18418. Exhaustive source-guard r=2 B=3: 81 selector maps, 32805 entire-policy checks, 81 valid complete UNSAT policies and ZERO false NO paths after all 324 critical single-clause deletions. r=3 B=3: all 6561 maps, 52488 unique-witness single deletions, 104976 wrong local choices rejected. Original-source T5 H9 and H24 checked separately with AC-3/backtracking: each intact graph UNSAT; all 11/11 and 32/32 individual arc deletions SAT with source-verified witnesses. These finite controls are not asymptotic hardness claims. A separately executed compact Node.js reproducer and its output are published alongside this report. The full Python producer and raw evidence are retained in the downloadable local research package, not claimed to be GitHub-published.

DISJ: PASS only on authenticated supplied grammar; arbitrary-CNF extension OPEN. Relativization: entirely relative; no P/NP separation. Simultaneous DTISP/coNTISP: precise conditional gates retained. Deterministic configuration counting: not used as lower bound. Independent physical random-access tape-model audit OPEN. A hereditary solver-dependent all-CNF source converter is NOT constructed. No agent identity, schedule, state, historical rule or foreign manuscript was changed; root retired trackers untouched. P versus NP OPEN.

**References:** [1] Buss & Williams, Limits on Alternation-Trading Proofs for Time-Space Lower Bounds, Computational Complexity 24 (2015), 533-600, Fig. 8.2, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/ . [2] Fortnow, Lipton, van Melkebeek & Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6) (2005), 835-865, Theorems 1.2, 6.4, https://lance.fortnow.com/papers/files/tst.pdf . [3] Cross-track/72 original report, blob f659e25c8cd77e67d5dc10b25c39523b2dae95dc. [4] LSPV-1/551 original report, blob 34d2688f90333318d2830da52ddcb75c965522bc. [5] LSPV-1/626 original report, blob b621303bb3f08ecf2ed742401f3755629c8f9a36.
