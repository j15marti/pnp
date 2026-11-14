# TMR-2/013: exact five- and six-observation certificate counts for every eight-mask source

**Date:** November 13, 2026, 23:12 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity. **Repository:** j15marti/pnp, main. **New claim:** TMR2-ALL6-013, CANDIDATE pending independent TMR-5/TMR-1 mathematical review. **Peer claim independently checked:** TMR5-SIX10, PROVED/RESTRICTED at its exact balanced-mask promise scope. **Computational evidence:** independent native CPython complete-permutation source audit. **Unrestricted P versus NP:** OPEN.

## 1. Scope and exact source binding

Retain the actual strict-proper ordered three-CNF binary template G_r of TMR-2/010, not an arbitrary representation or all three-CNF. Its unary N,M header, canonical three distinct occurring core IDs per eight-clause block, positive filler clauses covering every spare declared ID and original fixed-width sign-plus-ID fields are authenticated. The only free coordinates in G_r are the 24 original clause-polarity bits in each block. Each clause of one block forbids one of the eight assignments to its three core variables, and the block is UNSAT iff its eight row masks form a permutation of 0,...,7. All blocks are SAT iff the product is SAT.

For r blocks the exact encoded length is

$$
w=\lceil\log_2(6r+2)\rceil,\quad N=2^w-1,\quad K=\lceil(N-3r)/3\rceil,
\quad M=8r+K,\quad L=N+M+2+3M(w+1)=\Theta(r\log r).
$$

For a single arbitrary source tuple a=(a_0,...,a_7), write f_m for the count of the full mask m. For a pair of bit coordinates J of size two and two-bit value v, write f_{J,v} for the number of rows with that projection. For coordinate j and bit b, write n_{j,b} for the number of rows whose j-th polarity bit equals b. The 24 source observation coordinates are ordered row-coordinate pairs (i,j).

A size-k SAT-forcing sign certificate is a set Q of k such original bit positions such that **every** completion within the full authenticated mask template consistent with the observed bit values remains SAT. Count all certificates of exactly size k, including supersets of smaller ones. This is a promise-query notion, not compulsory stored bits, a refutation calculus or a physical lower bound after input acquisition.

## 2. New exact theorem for ALL eight-mask tuples

**TMR2-ALL6-013 (CANDIDATE, rigorous scoped proof below):** For every eight-row tuple a in {0,...,7}^8, without any balance assumption, the numbers of exactly five- and six-position SAT-forcing certificates are

$$
N_5(a)=\sum_{j=0}^2\sum_{b=0}^1\binom{n_{j,b}}{5}
$$

and

$$
\boxed{
N_6(a)=
\sum_{m=0}^{7}\binom{f_m}{2}
+\sum_{\substack{J\subseteq\{0,1,2\}\\|J|=2}}\sum_{v\in\{0,1\}^2}
\binom{f_{J,v}}{3}
+\sum_{j=0}^{2}\sum_{b=0}^{1}
\left[
\binom{n_{j,b}}{6}
+(24-n_{j,b})\binom{n_{j,b}}{5}
\right].
}
$$

Use the conventional definition binom(n,k)=0 for n<k. The three terms enumerate respectively (A) two identical fully observed masks, (B) three equal two-coordinate projections, and (C) six-bit supersets of a five-bit halfcube certificate. All three classes are disjoint. The formula also evaluates to zero on every UNSAT permutation.

**Peer corollary, independently reviewed:** If a is balanced, every n_{j,b}=4, so the third term vanishes and the expression reduces exactly to TMR-5/010's two-form TMR5-SIX10 theorem. Our analysis checks its previously OPEN independent-review obligation without assuming the peer's count formula.

## 3. Proof from an exhaustive classification of possible Hall violations

For each row i with q_i queried coordinates, let D_i be its nonempty subcube of matching 3-bit masks. The number of allowed masks is |D_i|=2^(3-q_i), namely 8,4,2,1 for q_i=0,1,2,3. A completion to an UNSAT permutation is a perfect matching between the eight rows and the eight masks. By Hall's distinct-representatives theorem, Q forces SAT exactly when some row set R of cardinality s has |union_{i in R} D_i|<s. We use exactly six total observed positions and analyze every s.

- s=1 cannot fail because every D_i is nonempty.
- s=2: to have a union of size one, both domains must be the same singleton. This requires all three observations in each of two rows. They must have identical complete masks, exactly class A.
- s=3: a union of size at most two forces at least two observations per row. The total six-bit budget then forces exactly two observed bits in each of three rows, and all three domains must be the same two-element subcube. In {0,1}^3 such an edge is identified by its two fixed coordinates and their values. This is exactly class B.
- s=4: a union of size at most three would require at least two observations in each of four rows, costing at least eight, impossible.
- s=5: the union must have size at most four, so each of the five rows must be observed at least once, consuming at least five bits. With at most six bits, either all five have one queried bit or one has two and four have one. Each one-bit row permits a four-mask halfcube. To keep the entire union at size at most four, all these halfcubes must coincide, and the possible two-bit row must lie inside the same halfcube. Thus Q includes at least five queried original positions in the same coordinate/value halfcube H_{j,b}.
- s=6: every row must be queried at least once, so exactly six rows have a single observed bit each. Any two distinct three-bit halfcubes have union size at least six, which does not violate Hall for six rows. A failing union of at most five therefore requires all six observed halfcubes identical. In particular, Q contains a five-bit halfcube certificate, again class C.
- s=7 or s=8: at most six rows have any queried bit, so a selected unqueried row supplies all eight masks to the union and prevents a failure.

Conversely, each class indeed violates Hall: two singleton rows with identical required masks; three rows each restricted to the same edge; or five rows restricted to a four-mask halfcube. Hence classes A, B and C are necessary and sufficient.

For class A, each duplicated full mask contributes binom(f_m,2). For class B, each equal two-bit projection contributes binom(f_{J,v},3). For class C, define H_{j,b} as its n_{j,b} original query positions. An exactly-six-element Q contains five or more positions in H_{j,b} in precisely binom(n_{j,b},6)+(24-n_{j,b})binom(n_{j,b},5) ways. Distinct H_{j,b} are disjoint sets of physical query positions, so a six-element Q cannot contain five positions in two distinct H sets. Classes A and B use respectively only two or three rows, so neither can contain a five-row halfcube certificate. Classes A and B have different row supports and do not overlap. Summing is therefore exact, not a union-bound overcount. For k=5, only the five-row halfcube Hall failure remains, giving the N_5 formula.

This proof does NOT require correctness on arbitrary continuations of a one-pass stream. It requires correctness of a fixed total solver on all legal complete G_r sources, and uses only comparisons of full sources that agree on actually observed physical bits.

## 4. Hostile controls and exact native execution

I wrote an independent CPython verifier from scratch using a technique different from the TMR-5 matching solver. It explicitly enumerates all 8!=40,320 UNSAT permutations, packs their compatibility with each possible observed polarity position into large integer bitsets, and intersects those bitsets for **every** one of the binom(24,5)=42,504 five-position subsets and binom(24,6)=134,596 six-position subsets. A query is classified SAT-forcing precisely when no UNSAT permutation is compatible with all its observations. Structural predicted counts are computed separately and asserted equal to these directly enumerated completion results. No Hall matching, no peer code wrapper and no SAT oracle were used in the classification.

**Exact published native execution:** Python script experiments/tmr/tmr2_all_masks_c6_013.py, Git blob 8b78e6a7ba4f91547d165d09e7d4de19496bc61e; elapsed 8.154 seconds. Eight tuples, 1,416,800 actual k=5/k=6 query subsets, full completion compatibility against the 40,320 permutations, zero failed assertions. The identical full native JSON output is in results/raw/tmr/2026-11-13_2312_TMR2_ALL_MASK_C6_013_RAW.json, Git blob fa08876bf8ce1fd0e235ff8d7c22613e4a61b2e1. Execution was a native CPython run, not hosted V8.

| Tuple | N5 | A: full pairs | B: projection triples | C: five-bit extensions | N6 |
|---|---:|---:|---:|---:|---:|
| (0,0,3,3,5,5,6,6) | 0 | 4 | 0 | 0 | 4 |
| (0,0,1,1,6,6,7,7) | 0 | 4 | 8 | 0 | 12 |
| (0,0,0,0,7,7,7,7) | 0 | 12 | 24 | 0 | 36 |
| (1,2,3,4,5,6,7,7) | 3 | 1 | 3 | 57 | 61 |
| (7,7,7,7,7,0,0,0) | 3 | 13 | 33 | 57 | 103 |
| (7,7,7,7,7,7,0,0) | 18 | 16 | 60 | 327 | 403 |
| (7,7,7,7,7,7,7,7) | 168 | 28 | 168 | 2772 | 2968 |
| (0,1,2,3,4,5,6,7) | 0 | 0 | 0 | 0 | 0 |

A crucial new hostile control is the old unbalanced tuple: the balanced-only TMR5-SIX10 formula would return 1+3=4, while the true number is 61. The new class C precisely accounts for the missing 57, so the balance hypothesis is essential to the earlier abbreviated expression but **not** to the generalized theorem.

Additional unexecuted controls: no native physical multitape SAT decider, all-length binary grammar parser, Horn/2-SAT/XOR Gaussian elimination, arbitrary auxiliary-variable encoding, entire main.tex compile or repository-wide preflight was run. The G_r template has a compact constant-eight-bit mask recognizer and the prior candidate TMR-2/010 charged source-level O(L(log L)^2) decision algorithm. Thus a large count of certificates does not mandate expensive processing, retention or superpolynomial time.

## 5. Correct machine transfer and limitations

For a fixed finite total deterministic correct 3-SAT machine A with h simultaneously observing input heads, its halting run on a legal G_r source must observe a set of original polarity bits that is a valid promise sign-certificate. If there were an opposite-label legal completion agreeing on every observed position, deterministic trace replay would preserve all control and writable states even with arbitrary input rereading, caching and algebraic representations, contradicting correctness. Therefore T_A(F) >= ceil(C_{G_r}(F)/h) under the declared per-transition observation convention, where C_{G_r} is the *minimum certificate size*, not N_5 or N_6. The balanced products have C=6r and yield only Omega(L/log L).

Certificate multiplicity N_6(F) is distinct from minimum observation cost C(F), minimum decision-tree depth, proof length, peak writable information and actual time. Even exponentially many legal completions are described by only the L source bits. A can scan, compress, retain, reread or recompute arbitrarily. No processing lower bound after a complete input copy follows from the present formulas. All every-exponent uniform P!=NP obligations remain OPEN, as do P1-01/P1-03/P1-04 for the constructive direction.

## 6. Primary sources and repository provenance

Primary combinatorial source: P. Hall, *On Representatives of Subsets*, Journal of the London Mathematical Society 10 (1935), 26-30, DOI https://doi.org/10.1112/jlms/s1-10.37.26 . Used solely for the perfect-matching characterization, not as a claim that Hall established these project-specific formulas.

Decision-tree/certificate model context: H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288 (2002), 21-43, DOI https://doi.org/10.1016/S0304-3975(01)00144-X . Standard query complexity does not charge physical tape-head movement or general post-acquisition processing.

Before this write I read the 2026-11-13 12:49 PST authoritative replacement directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1.txt full 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered full 1,051,196-character authentic Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c despite empty normal connector body; root main.tex recovered full authentic 2,515,087-character Git blob SHA c9944b36cc043c7a0c1808b8ffbbacc19ea4350b despite empty normal connector body; issue #3 latest through TMR-1/013; AGENTS.md, CODEX.md, repo pnp-research skill; all five current TMR handoffs; original TMR-2/010,/011,/012 and TMR-5/010 peer report/code/raw. Older LSPV work is preserved as historical evidence, not old priorities.

**Tracker decision:** TRACKERS REVIEWED; NO MATERIAL CHANGE. The formulas are new restricted sign-certificate enumerations and change neither the uniform P=NP nor P!=NP load-bearing status. Neither proof1.txt nor proof2.txt nor root main.tex is edited by TMR-2. No scheduled task or agent was created, revived or changed. The native repository preflight and LaTeX compiler were unavailable without a local repository checkout. The report and standalone code/raw were published to GitHub main and require explicit readback verification. Finite evidence remains COMPUTATIONAL; new theorem CANDIDATE until independent peer mathematical review.

**One next target:** TMR-5 independently check the unbalanced Hall s=5/s=6 classification and the no-double-count claim. Then seek/falsify an unrestricted processing charge that remains nonzero after all source bits have been copied into writable memory and survives polynomial-space algebraic and cached alternatives.

END_OF_REPORT::TMR2-ALL6-013::2026-11-13_2312_PST
