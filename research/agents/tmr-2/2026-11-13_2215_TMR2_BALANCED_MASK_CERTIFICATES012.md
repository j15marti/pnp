# TMR-2/012 | Exact 5-or-6 certificate dichotomy for every SAT eight-mask block

**Date:** November 13, 2026, 22:15 PST. **Role:** TMR-2 Information Necessity. **Status:** NEW TMR2-BC12 CANDIDATE pending independent TMR-5 mathematical review. Finite evidence COMPUTATIONAL. P versus NP OPEN.

## Exact source, claim and relation to previous work

Retain the complete original all-declared-ID-used strict proper 3-CNF grammar of TMR-2/010 and /011: unary header, canonical even-parity core identifiers, three original sign-plus-ID literal fields per clause, and canonical positive spare-variable fillers. Each of r disjoint eight-clause blocks acts on exactly three variables. Each block contains eight arbitrary 3-bit sign masks a=(a_0,...,a_7). It is UNSAT iff those masks are exactly a permutation of 0,...,7. All blocks must be SAT for the product formula to be SAT. Original source length is

$$
w=\lceil\log_2(6r+2)\rceil,\quad N=2^w-1,\quad K=\lceil(N-3r)/3\rceil,\quad M=8r+K,\quad L=N+M+2+3M(w+1)=\Theta(r\log r).
$$

A promise sign-bit certificate consists of original sign-bit positions whose observed values force the answer over the entire two-label template family G_r. TMR-2/011 proved 5r for a particular SAT tuple (1,2,3,4,5,6,7,7) in every block and 24 for every UNSAT formula.

**New theorem candidate TMR2-BC12.** For any SAT block a, its exact sign certificate size is 5 if some coordinate has the same bit value in at least five of the eight row masks; it is exactly 6 otherwise. The otherwise case means each of the three coordinates has exactly four zeros and four ones. For an arbitrary SAT product F of r independently chosen SAT blocks, its minimum sign certificate size is the SUM of the r individual 5-or-6 values. For every UNSAT product, it remains exactly 24.

## Proof

For observed positions Q on one block, let A_i be the subcube of eight possible masks compatible with observations in row i. An UNSAT completion is a perfect matching choosing one different mask from each A_i. By Hall's theorem it exists iff every set R of s rows has at least s distinct available masks in the union of their A_i.

Any four or fewer observations permit such a matching as proved in TMR-2/011. With at most FIVE observations, for s=1 the relevant domain is nonempty; for s=2 some row has at most two observations and therefore at least two masks; for s=3 or 4 some row has at most one observation and therefore at least four masks; and for s>=6 some row is unqueried, so eight masks are available. Only s=5 could violate Hall. It can do so only with exactly five queried rows and exactly one observed bit in each. Each domain is a four-mask half-cube. Two distinct half-cubes have union of size at least six, while five identical half-cubes have union of size four. Therefore a five-bit SAT certificate exists precisely when FIVE different rows agree on the SAME coordinate/value. This is equivalent to a coordinate frequency of at least five. The four-bit universal lower bound gives the exact minimum five in that case.

Every SAT block has two identical complete masks, because it is not a permutation of all eight. Observing all three bits in each such duplicate row is a six-bit certificate. If every coordinate is balanced four/four, no five-row same-coordinate/value certificate exists, proving the exact minimum SIX. For a SAT product, observing fewer than this minimum within ANY one block allows an agreeing UNSAT completion of that block with all other blocks unchanged. Conversely concatenating optimal per-block certificates forces all blocks SAT. This proves additivity. The previous 24-bit UNSAT certificate proof remains unchanged.

## Uniform family and physical-machine consequence

Take the **balanced SAT block**

$$
b=(0,0,3,3,5,5,6,6).
$$

Every bit coordinate is balanced four zeros/four ones, and all four even-parity masks are duplicated. For the strict original source B_r containing r disjoint copies of b,

$$
\boxed{C_{G_r}(B_r)=6r}.
$$

The exact *sign-only* Hamming distance from b to an UNSAT eight-mask permutation is FOUR: changing at most three sign bits leaves at least one original duplicated pair intact, whereas flipping the low bit in one occurrence of each of masks 0,3,5,6 creates the four missing masks 1,2,4,7. This does NOT assert four-bit robustness against identifier or header changes.

Let A be any ONE fixed total correct deterministic multitape 3-SAT decider for all lengths, with h finite original read-only input heads (at most h source observations per transition). Its halting execution on B_r must have observed a promise certificate: otherwise a same-length valid opposite-label input agreeing at every observed position gives exactly the same deterministic complete run. All writable memory, rereads, adaptive access, algebraic representations and recomputation are permitted. No online or one-pass correctness is imposed. Thus

$$
T_A(B_r)\ge\lceil6r/h\rceil=\Omega(L/\log L)
$$

for fixed h. This is source *acquisition*, not retained workspace, proof enumeration, or post-acquisition processing. The complete structured two-label class remains decidable by the TMR-2/010 uniform authenticated mask-table fast path in proposed O(L(1+log L)^2) time with logarithmic work space, plus charged exhaustive fallback for nonmembers. Thus no superpolynomial 3-SAT lower bound follows. TMR-4/012 and TMR-5/009 additionally cap source-only MAY potentials at O(L).

## Executed checks, source provenance and hostile controls

Exact published standalone Python 3.13.5 was executed natively (2.52 seconds internally, about 3.40 seconds in a second complete process run). For old tuple (1,2,3,4,5,6,7,7), it enumerated every 55,455 position subset of sizes 0..5, finding zero certificates below 5 and 3 certificates of size 5, reproducing TMR-2/011. For new balanced b, it enumerated every 190,051 subset of sizes 0..6, finding zero at sizes 0..5 and exactly four 6-bit certificates. Exhaustive sign mutations found zero UNSAT neighbors at distances 1..3 and 144 at distance 4. Product source-mask controls r=1,2,3,8,64 tested both labels and the derived 6r/24 counts (not a full original binary parser simulation). Zero failed assertions.

Separately written native Python bit-parallel verification, LOCAL ONLY, enumerated all 8!=40,320 UNSAT permutations and intersected their bit-agreement sets for every 55,455 query subset of sizes <=5 on b; it independently found zero SAT certificates (0.53 seconds). This is a different algorithm from the published augmenting-path matcher, not a wrapper.

The exact native executed source and raw output were published and read back at Git blob hashes b1ec9df7174b8f72c1f04c854dff4decb0488978 and 9b04d3d3e0e4557ac7d32dce5ef8d2031dd481bb:
- experiments/tmr/tmr2_balanced_mask012.py
- results/raw/tmr/2026-11-13_2215_TMR2_BALANCED_MASK012_RAW.json

Controls: previous unbalanced SAT tuple, balanced SAT tuple, UNSAT-permutation neighbors, products, compact table classifier. Not performed: native physical multitape machine simulation, exhaustive new full binary 3-CNF parser tests, Horn/2SAT/GF(2) regression, LaTeX compilation, repository-wide preflight. These limits prevent stronger claims. Future proposed processing bounds must survive Horn/2SAT, GF(2)/Gaussian elimination, bounded treewidth, disjoint products, padding, renaming, auxiliary variables, caching, sharing and recomputation.

## Sources, full-corpus status and handoff

Original sources independently checked: P. Hall, On Representatives of Subsets, Journal of the London Mathematical Society 10 (1935), 26-30, https://doi.org/10.1112/jlms/s1-10.37.26 ; H. Buhrman and R. de Wolf, Complexity Measures and Decision Tree Complexity: A Survey, Theoretical Computer Science 288 (2002), 21-43, https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf . The present exact 5-or-6 formula is a project-specific deduction, not attributed to either paper.

Read the superseding November 13 12:49 PST replacement directive FIRST, proof1.txt complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2.txt complete original 1,051,196-character Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c despite blank normal file fetch, main.tex complete 2,511,782-character Git blob SHA c04a02a97492f88938791f363ff91d99b67cd78b, AGENTS.md, CODEX.md, pnp-research SKILL.md, current five TMR handoffs, latest issue #3 through TMR-1/012, original TMR-2/010 and /011 reports/source, TMR-5/007, TMR-1/010 and TMR-4/008 handoff. One guessed file name for TMR-4/008 returned 404 and its correct path was recovered from the handoff. Historical checker failures are not reinterpreted as new obligations.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex was not edited; TMR-5 owns synthesis. No tasks or schedules were changed. P1-01, P1-03, P1-04, P2-00 and the unrestricted all-exponent processing bottleneck remain OPEN.

**TMR-5 review target:** independent proof audit of the five-query Hall characterization for *every* SAT tuple, product additivity, and sign-only radius four. **Next substantive target:** falsify or prove an all-transition POST-ACQUISITION processing charge surviving the same fixed-machine compact mask classifier and arbitrary polynomial workspace.

END_OF_REPORT::TMR2-BC12::2026-11-13_2215_PST
