# SIGMA REDTEAM35 | Selector dependence, QBF and hidden oracle firewall

**UTC:** 2026-11-19 03:53; **PST:** 2026-11-18 19:53.
**STATUS:** Restricted exact quantifier and resource lemmas PROVED; finite audits COMPUTATIONAL; arbitrary-CNF specialist OPEN; P versus NP OPEN.
**Sentinel:** SIGMA35_SELECTOR_QBF_ORACLE_20261119_0353Z_PROVED_SCOPED_OPEN_GENERAL

## PROPOSE / SEARCH / BUILD
Proposed adversarial controls: existential-row for universal-row replacement; selector accessing an otherwise private witness; nondeterministic gate traces; hidden UNSAT oracle; free correct-path polarity; delayed guest solvers, encoded input and oversized memory addresses.
Read current `j15marti/pnp` main tree SHA `7f90301e71984373a41b74c0b974565b13f9a373`, research protocol, `research/agents/sigma-primary/2026-11-18_T5_ADVICE_FIREWALL35.md`, `research/agents/lspv-2/2026-11-18_1920_LSPV2_BLOCK_BATCH_CORRECT_PATH_AUDIT.md`, `research/agents/lspv-4/2026-11-18_1840_LSPV4_BLOCK_POLARITY_RESOURCE_FIREWALL.md`, and SIGMA34 dynamic-sign audit. The selector coNP-completeness result and T5 H9 construction are PRIOR PROJECT WORK.

## Quantifier theorem and concrete falsifiers
Let `F(z,Y)=AND_j B_j(z,Y_j)` with identical shared z and genuinely pairwise disjoint private `Y_j`. Then `UNSAT(F) <=> FORALL z EXISTS j FORALL Y_j NOT B_j(z,Y_j)`. The existential j may vary with z, but it cannot vary with the private y when used to claim that some whole block is UNSAT.

On identical matrix `M(z,j,Y)=NOT B_j(z,Y_j)`, strict `Sigma1 = EXISTS z,j,Y M`; strict `Sigma2 = EXISTS z,j FORALL Y M`; strict `Sigma3 = EXISTS z FORALL Y EXISTS j M`. Under disjoint product semantics Sigma2=Sigma3 for this PARTICULAR M, but neither is the true global NO prefix starting `FORALL z`. Moving z to EXISTS makes a false UNSAT verdict possible.

If blocks share private witnesses, `FORALL Y EXISTS j NOT B_j(Y)` need NOT imply `EXISTS j FORALL Y NOT B_j(Y)`. Tiny falsifier: B0(y)=y, B1(y)=NOT y. Non-affine falsifier: B0(a,b)=a OR b, B1(a,b)=NOT(a OR b). Both source blocks individually SAT; their conjunction UNSAT. This rules out silently treating a first-violated-clause selector as a refutable-block selector in arbitrary CNFs.

UNSAT of a gate circuit with trace T(inputs,t) requires `NOT EXISTS inputs,t [T AND output=1]` or `FORALL inputs,t [T=>output=0]`. The shortcut `FORALL inputs EXISTS t [T AND output=0]` can be a **false NO** if traces permit both output values. Its substitution is certified only under total functional trace semantics and legally post-input quantifier placement. A source-unverified trace oracle is not allowed.

For an arbitrary CNF G(z), a fixed selector returning the single block `B0(z,y)=G(z) AND y` is universally sound iff G is UNSAT. Thus selector correctness checking is coNP-complete, as already established in the project's earlier ADVICE-FIREWALL35. Giving a free correct selector program or free child BAD predicate grants hidden answer-oracle power. A black-box all-z query lower bound applies to a **source-opaque interface only**.

## Exact finite experiments with independent referee
Complete stdlib-Python primary auditor: **149,578 assertions, zero failures**. Separate set-theoretic/transfer-matrix referee: **1,286 assertions, zero failures**. Combined 150,864 assertions, NOT disjoint mathematical problems. Deterministic reruns produced byte-identical result JSON; ZIP CRC and SHA256 manifest pass.
* 256 exhaustive disjoint two-factor tables: 207 SAT, 49 UNSAT; **126 SAT inputs had some bad z row** (invalid outer-exists NO); **18** UNSAT inputs required z-dependent blocker. Strict Sigma1/Sigma2/Sigma3 for same local matrix: **255/175/175** true.
* 256 exhaustive pairs with overlapping private witness bits: **81** UNSAT conjunctions, **50** with no individually UNSAT factor, exact dependency-swapping counterexamples.
* 16 trace relations: **3** false-NO naive existential trace cases; all **4** total functional trace cases correct.
* 3,000 structured/random disjoint 3-factor cases, including 1,500 forced empty-fiber cases: **1,502 UNSAT, 1,498 SAT; 2,897** all-factor-non-affine; 144,000 double-NOT equivalence checks.
* Exact tournament T5 H9: relation R(a,b) iff (b-a) mod 5 is in {1,3}. Four internally disjoint paths from vertex 0 to 1 with signs ++, +++, ++-, ---; 9 vertices/11 arcs. There are zero full colorings among 5^8=390,625 root-fixed assignments, but each of 11 edge deletions is SAT. Root-fixed deletion counts: **[36,36,12,12,12,12,12,12,8,8,8]**; times 5 for all color rotations. Independent transfer-matrix code matches. Endpoint b=0,1,2,3,4 yields an unavailable PATH selector [0,1,2,0,3]. A first-violated EDGE selected by looking at an entire coloring is NOT a whole UNSAT source edge.

## Correct-path / polarity model (PROVED conditional theorem)
For untrusted k-bit advice, a sound verifier must output verified YES only on an authentic satisfying assignment, verified NO only on a COMPLETE independently sound UNSAT certificate, and UNKNOWN otherwise. Every wrong path must avoid false labels. A free answer/polarity bit or a promised winning path without wrong-path soundness is answer advice, not an algorithm. If both labels have successful k-bit advice and a deterministic verifier with cost (T_V,S_V), serial enumeration yields at most O(2^k(T_V+poly(N+k))) time and O(S_V+k+log N) writable space. A one-polarity NO-verifier does not automatically decide YES. A succinct response program j(z) is an entire strategy, not a single path; all universal z branches, program bits, replay, verification, source access and proof acquisition must be charged. Read-only advice can save writable storage but not length/access or production costs.

A sound source-reading specialist may enumerate original blocks for each z, restrict/materialize or decode each child, run a TOTAL deterministic SAT seed, stop on an authenticated UNSAT child, and for overall NO check every permitted z. All attempts and both child-answer polarities count. YES witness printing must recover and check all required private assignments, potentially additional SAT calls.

## Physical cost and simultaneous time-space theorem firewall
For R<=n^.195 already-enumerated shared rows, B<=n^.65 blocks PER row, L<=n^.35 physical guest length, total worst case RB<=n^.845 guests. For a hypothetical total correct deterministic SAT seed of time L^p and writable space L^s, a literal sequential buffered caller has time
`O(T_parse+T_index + n^.845[n^.35 polylog n+n^(.35p)] + T_verify + T_output)`,
and peak space
`O(S_index+n^.35 polylog n+n^(.35s)+S_replay+|z|+log n)`.
Therefore the n^1.33 target via THIS implementation needs p <= (1.33-.845)/.35 = **97/70 = 1.385714**, plus other costs. Arbitrary polynomial p=2,3 gives guest call exponents 1.545,1.895. Peak n^.5 requires s<=10/7 PLUS offsets; n^.65 stored offsets exceed budget. Distinct explicit full children have total n^1.195 encoded bits. If n means full source length, simultaneously claiming this independent physical child sum is inconsistent; virtual access must be charged. If B is total rather than per-row, replace .845 by .65.

For ordinary all-input SAT at actual encoded length N and FLMV's random-access TM model, c=1.33 gives deterministic simultaneous exclusion at space o(N^.279104) and co-nondeterministic SAT (= nondeterministic UNSAT) at o(N^.089300) on the explicit finite-k sufficient curves; neither forbids (1.33,.5). If actual source N=n^1.195, a hypothetical all-input SAT decider at n^1.33 time,n^.5 space becomes (N^1.112971,N^.418410), which enters FLMV deterministic exclusion. The structured specialist IS NOT an all-input solver. Nondeterministic SAT has an easy accepting witness; Fortnow 2000 only excludes near-linear N^{1+o(1)} time with N^{1-epsilon} writable space, not general (1.33,.5). Resolution lower bounds concern a restricted proof system, not arbitrary NO-verifiers. Williams 2cos(pi/7) ~1.80194 is a subpolynomial-space endpoint; Buss-Williams proves an alternation-trading proof-system limit, not an all-method ceiling. McKay-Williams ITCS 2019 T*S=Omega(N²/polylog N) addresses PRINTING 3SAT witnesses in its oracle-branching-program/RAM model, not general decision SAT or promise T5.

R<=T distinct memory addresses is tautological, not the FLMV maximum-work-tape-position space measure. One read of address 2^100 uses one distinct address but must represent 101 address bits and may place the work-tape head very far away. Delay, interpretation, parent-sized guest calls, padding N=m^2, recursive expansion and live concurrent guest buffers destroy any uncharged literal exponent contraction. No nonrelativizing step has been identified by merely source-naming a semantic BAD oracle.

## Classification / handoff
**PROVED:** disjoint-product equivalence, wrong-outer-quantifier and overlapping-witness counterexamples, gate-trace functional firewall, source-opaque row-query limitation, bounded verified-advice enumeration, conditional resource algebra.
**COMPUTATIONAL:** 150,864 assertions and T5 H9 independent transfer audit.
**FALSIFIED:** single bad row establishes NO; selector depending on private assignments establishes a whole refutable block; arbitrary gate traces prove NO; generic polynomial SAT seed yields n^1.33; used-location count establishes FLMV space.
**OPEN:** source-authentic uniform general-CNF one-block discovery, all-z strategy certification without coNP oracle, source-size/guest same-model accounting, hereditary recursion, T5-to-arbitrary-CNF transfer, P vs NP.
**Next:** T5 H33 or a 33-vertex critical instance with explicit shared cutset, physically serialized children and dependency-checked trace; regress missing-one sibling, oracle/INTERP/DELAY, source rewrite, all universal branches.

Full stand-alone markdown report, scripts, raw results, hashes and independent rerun available as `SIGMA_REDTEAM35_PACKAGE.zip` conversation artifact, SHA256 `021dca0e0f8dd45142a71df5592324ac43bd39d8811e2d8d9e542d252d4d2c25`.

References: FLMV JACM 2005 https://doi.org/10.1145/1101821.1101822 ; Fortnow JCSS 2000 https://doi.org/10.1006/jcss.1999.1671 ; Williams Computational Complexity 2006 https://doi.org/10.1007/s00037-007-0221-1 ; Buss-Williams Computational Complexity 2015 https://doi.org/10.1007/s00037-015-0104-9 ; McKay-Williams ITCS 2019 https://doi.org/10.4230/LIPIcs.ITCS.2019.56 ; Ben-Sasson/Wigderson JACM 2001 https://doi.org/10.1145/375827.375835 .
