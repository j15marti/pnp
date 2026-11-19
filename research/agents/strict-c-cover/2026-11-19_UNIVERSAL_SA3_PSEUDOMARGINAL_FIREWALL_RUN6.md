# Independent T5-C obstruction-cover run 6: universal three-variable marginal firewall

**Status (2026-11-19): PROVED algebraic lemma, independently FINITELY VERIFIED; P versus NP remains OPEN.**

## Exact theorem and quantifiers

For EVERY unpinned strict-C source F with finite variable names, and each original 3-name clause interpreted using R(a,b) iff (b-a) mod 5 in {1,3}, there exists a rational family of probability measures mu_U on Z5^U for EVERY subset U of at most THREE variable names. The measures are normalized, nonnegative, marginally consistent on every inclusion V subset U, and the distribution for each original clause has support only on the 30 accepted original-C tuples. Arbitrary clause overlaps and duplicate physical scopes are allowed.

Hence the full 3-variable local-marginal (standard level-3 SA local-distribution) relaxation is feasible even on UNSAT strict-C sources, not merely the pairwise physical-clause-overlap relaxation proved in run 5. This is a lower bound FOR THAT RELAXATION ONLY, not for arbitrary algorithms.

## Constructive proof

Call a pair linked if it occurs together in any physical clause. Give each singleton the uniform distribution. Give every linked pair marginal q(a,b)=0 if a=b, 2/30 for cyclic distance 1, and 1/30 for cyclic distance 2; give each unlinked pair independent uniform probability 1/25. For any triple of names, count its linked pairs:

* 0: independent uniform;
* 1: q on the linked pair times independent uniform third variable;
* 3: uniform over the 30 allowed C tuples (even when this triple is not itself a source clause);
* 2: two linked pairs meet at a center. Give the center uniform color b; conditioned on b, sample the two leaf differences u,v in {1,2,3,4} according to R0/30, with R0 rows `[3,1,0,6],[1,0,4,0],[0,4,0,1],[6,0,1,3]`.

The R0 row and column sums are [10,5,5,10]. For each d in Z5, the sum of R0 entries with v-u=d mod5 equals 6. Therefore the two center-leaf pair marginals equal q while the unlinked leaf-leaf marginal is independent uniform 1/25. All four cases have the same prescribed pair and singleton marginals, and every physical clause has three linked pairs, so it is supported exactly on C. This completes the proof. All probabilities can be represented with denominator 750.

## Sharp F3 example

F3=C(a,b,c) AND C(a,b,d) AND C(a,c,d) is UNSAT, physically clause-critical, with four distinct names. Fixing a, the graph of pairs (x,y) satisfying C(a,x,y) on the other four colors is the path 2-1-4-3. The three C clauses require b,c,d to form a triangle in that path, impossible. All 625 complete assignments were exhaustively evaluated. SAT deletion witnesses for clauses [0,1,2] respectively: [0,1,1,2], [0,1,2,1], [0,1,2,2]. Three-variable local marginals are still feasible, but a distribution on all four names supported on all three clauses cannot exist, so level four refutes THIS SOURCE; no all-source SA4 result is claimed.

## Two independent exact finite audits

Original R-triangle predicate matched the independent consecutive-three-color set predicate on all 125 triples, 30 accepted. The primary checker examined all 2,300 triple scopes on a native 25-variable / 25-clause girth-8 critical source (287,500 assignment weights), all F3/K6/dense-overlap triples, and 1,676 triple scopes on the native 150-variable / 176-clause girth-10 control including all 176 original clause scopes (209,500 weights, seed 2026111906). Every triple sum equaled 750 and every pair/unary marginal exactly matched its prescribed integer values. A separately written checker replayed all 2,300 native25 scopes, the dense sources and F3. The native25 fixture SHA256 is `5d0b9630a3fe29a1aab5b3b4100e39d125ca43494401e25e81d23b6fa2279402`. No new independent UNSAT classification of native150 is claimed.

## Sound one-sided source-indexed specialist

A deterministic UNSAT-or-UNKNOWN algorithm scans triples of original physical records; any three different C scopes on exactly four names form an F3 isomorph. It emits the three original clause indices and source SHA256, re-verifies the input, and checks all 625 assignments to the core. F3, complete K6 and a seeded nine-variable overlap source returned verified UNSAT; native25 and native150 returned UNKNOWN. An adversarial one-record F3 SAT mutation returned UNKNOWN; forged hashes and duplicated indices were rejected. Actual Python input parsing stores O(n+m) records in memory; a random-access read-only input model can implement this triple-record scan with O(log(n+m)) writable words and O(m^3) time. This is not the proposed N^1.33-time endpoint.

For explicit full three-variable marginal output, an adjacency matrix implementation costs O(m+n^2+125n^3) operations and O(n^2) writable words plus Theta(125n^3) streamed entries. A read-only record scan trades time O(mn^3) for logarithmic writable words. Neither yields a universal efficient all-z refutable-block procedure or solves arbitrary CNF.

## Obstruction-cover implication and next falsifiable experiment

**FALSIFIED**: Any method based solely on globally consistent distributions on ALL subsets of at most three variable names can acquire an UNSAT cover of every strict-C source. **OPEN**: source-uniform exact SA4 primal/dual feasibility on native25 girth-8 critical source; arbitrary C all-z certificate acquisition under row <=N^.195, block <=N^.65, private <=N^.35, full verification and peak-space charge. No proof-system-to-unrestricted-machine transfer.

Full independently executable package, including original fixtures, scripts, data, two audit outputs and SHA256SUMS: `T5C_Universal_SA3_Firewall_Run6_20261119.zip`, archive SHA256 `9db3f1fe12eee570b294f6df7382c00e1d109039f2af624fc417f1ae66d1ff8e`.

Reference: [1] *The Sherali-Adams and Weisfeiler-Leman Hierarchies in (Promise Valued) Constraint Satisfaction Problems* (2026), https://doi.org/10.1145/3756323 ; [2] Dechter (1999), *Bucket Elimination*, Artificial Intelligence 113:41-85; [3] Ciardo and Živný (2024), https://arxiv.org/abs/2406.19685.
