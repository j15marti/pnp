# TMR-2/014: independent seven-sign certificate audit and sharp extremal multiplicities

**Pacific date:** 2026-11-14 00:17 PST (America/Los_Angeles). **Role:** NEW TMR-2 Information Necessity. **Repository:** j15marti/pnp, main.

**Epistemic status:** The TMR-5/011 inclusion-minimal seven-query structure and exact M7 formula pass an independent mathematical review at **PROVED/RESTRICTED scope** for the authenticated eight-mask sign-bit promise. New sharp extremal theorems TMR2-M7MAX-014 are **CANDIDATE pending independent TMR-5/TMR-1 mathematical review**. Finite runs are **COMPUTATIONAL**. Arbitrary SAT post-acquisition superpolynomial lower bound and P versus NP remain **OPEN**.

## 1. Exact dependency and machine/source contract

Source: the original explicit proper 3-CNF G_r grammar of TMR-2/010, with unary N,M headers, eight ordered three-variable clauses in each disjoint block, 24 freely variable polarity bits per block, fixed well-formed canonical identifiers, and positive spare-variable filler. Each row mask is in {0,...,7}; one block is UNSAT iff its eight row masks are a permutation of all eight values. All original sign-bit settings are syntactically valid. For r blocks, w=ceil(log2(6r+2)), N=2^w-1, K=ceil((N-3r)/3), M=8r+K, and **encoded input bits** L=N+M+2+3M(w+1)=Theta(r log r).

For a row-mask tuple a of eight masks, an observation set Q contains original row-coordinate sign positions (i,j), j in {0,1,2}. It **forces SAT** if every completion of the other sign positions within this authenticated grammar is SAT. It is inclusion-minimal if deleting any one of its queried positions loses that property. Define M7(a) as the number of such inclusion-minimal SAT-forcing Q of cardinality seven. This is distinct from the number of all size-seven certificates, the minimum-size certificate, retained workspace information, or a machine processing-time lower bound.

A fixed correct finite total deterministic multitape SAT machine A, serving all lengths, is charged for every local source-head motion/read and all writable storage, input copies, algebraic preprocessing, cache use, re-reads, recomputation and output. Its actual observed source-bit set is a certificate by full-configuration coupling, but M7 **counts alternative certificates** and does not make an algorithm traverse or store them. There is no online-continuation, one-pass, restricted-prover or free-oracle premise.

## 2. Independent peer proof of the TMR-5/011 seven-query classification

For each row i let D_i be the subcube of masks compatible with the observed row bits. With q_i observed bits its cardinality is 2^(3-q_i). An UNSAT completion is exactly a distinct representative of each of the eight domains. By Hall's theorem, Q forces SAT iff there is a row subset R, |R|=s, whose union of D_i has size less than s.

Suppose Q is inclusion-minimal forcing and |Q|=7. For s=1 no D_i is empty. For s=2 the violating domains must be identical singleton masks, requiring a six-bit forcing subset. For s=3 the union has size at most two and each of three rows needs at least two observations. If total observations are at most seven, two domains are identical two-mask cube edges; the third is either the same edge or a singleton inside it. Projecting the singleton to the edge's two fixed coordinates gives a six-bit forcing subset. For s=4 each domain must have size at most three, requiring at least two bits in each of four rows and eight total. For s=5 there can be no unqueried row. At least three selected rows have one-bit, four-mask domains. To fit a union of at most four, these halfcubes must all coincide; the other selected domains must be contained in that halfcube, so five first-coordinate observations already force SAT. For s=6 there can be no unqueried row. At least five rows have one-bit domains. Any two different four-mask halfcubes have union size six or eight, so all five are identical and yield a five-bit forcing subset. For s=8 an unqueried row necessarily has full eight-mask domain. Only s=7 survives.

For s=7, exactly seven rows each have exactly one observation and the eighth has none. One-bit row domains are coordinate halfcubes of size four. A union of fewer than seven masks must consist of one halfcube (size four) or two distinct-coordinate halfcubes (union six). Opposite-value halfcubes on one coordinate union to eight; three distinct halfcubes have union at least seven. One halfcube, or five observations in either of two halfcubes, contains a five-bit forcing subset. Inclusion-minimality therefore requires exactly four observations on halfcube H=(j,b) and three on J=(k,c), with j != k and seven distinct rows.

Conversely those seven domains have union six and force SAT. After deleting one query the remaining six constrained domains contain at most four H rows and three J rows. Any subcollection of a single type has size at most its four-mask domain; any mixed subcollection has size at most six and its union comprises six masks. Thus Hall holds for these six plus the two unrestricted rows, and an UNSAT completion exists. Every query is essential.

The four-row group is unique, so counting four row choices from H, then three remaining choices from J, with m=|H intersection J|, n_H=|H| and n_J=|J|, gives exactly TMR-5/011:

$$
M_7(a)=\sum_{\substack{j\ne k\\b,c\in\{0,1\}}}\sum_{i=0}^{4}
\binom{m_{H,J}}{i}
\binom{n_H-m_{H,J}}{4-i}
\binom{n_J-i}{3}.
$$

This independently establishes TMR-5/011's structural classification at its **restricted** source promise, rather than assuming the peer's enumerator. It neither changes G_r's efficient streaming classifier nor proves an unrestricted runtime lower bound.

## 3. NEW exact extremal theorems TMR2-M7MAX-014

**Theorem A (all eight-mask tuples, CANDIDATE pending independent review).** For every a in {0,...,7}^8,

$$
0\le M_7(a)\le 6\binom{8}{4}\binom{4}{3}=1680.
$$

Equality holds **if and only if all eight masks are identical**.

**Proof:** There are six ordered distinct coordinate pairs (j,k). For each such pair, every Q of the required structure chooses four distinct H rows and three of the remaining four J rows. There are at most C(8,4)C(4,3)=280 row selections. Their b,c values, if valid, are uniquely determined by the source a. Summing over six pairs gives 1680. If all eight row masks coincide, every row choice is valid for every ordered coordinate pair, so equality is attained. Conversely equality forces all 280 row choices valid for each (j,k). For any coordinate j, every four-row subset must therefore have a constant j-bit; since any two rows can be included in one four-row subset, all eight j-bits agree. This holds for all three coordinates, so the eight complete masks coincide.

**Theorem B (coordinate-balanced tuples, CANDIDATE pending independent review).** Suppose each of the three mask coordinates has four zeros and four ones across eight rows. Then

$$
0\le M_7(a)\le48.
$$

Equality holds **if and only if** the three coordinate columns are equal or complemented copies of a single balanced column. Equivalently the row masks are precisely four copies of a mask m and four copies of its three-bit complement (7 xor m). Exactly **280 ordered balanced mask tuples** attain equality.

**Proof:** Fix two distinct coordinate columns j,k and put t=#{rows with j-bit 1 and k-bit 1}. Both are balanced, so the four 2x2 cell counts for their bits are t, 4-t, 4-t, t. For any chosen H=(j,b), all four eligible H rows must be selected as the four-row group. The three-row J group must come entirely from J outside H, giving C(4-m_{H,J},3) choices. Summing over b,c and both ordered directions (j,k),(k,j), the contribution of one UNORDERED coordinate pair is

$$
g(t)=4\left[\binom{t}{3}+\binom{4-t}{3}\right]
=\begin{cases}
16,&t=0\text{ or }4,\\
4,&t=1\text{ or }3,\\
0,&t=2.
\end{cases}
$$

There are three unordered coordinate pairs, hence M7=sum g(t)<=48. Equality requires each pair of binary columns to be identical or complementary. Choose the first balanced column in C(8,4)=70 ways, then independently choose whether each remaining column agrees or is its complement (2^2 choices), giving exactly 280 maximizers. This is a count of the ordered eight row-mask tuples, not of inequivalent formulas after row renaming.

Both theorems are **restricted certificate-multiplicity facts**, not lower bounds on required information or physical computational work. The extremal sources are especially easy to decide by checking duplicate masks. Multiplicity cannot be charged as compulsory repeated work.

## 4. Independent native execution, hostile controls and raw evidence

Executed the exact separately authored Python 3 source, **not an import of TMR-5/011's code**, with no random seeds and no SAT-machine simulation. The script first sweeps all C(8,4)^3=343,000 balanced ordered tuples using independent 8-bit column masks and the contingency-table expression; it then builds all 8!=40,320 UNSAT mask permutations and independently tests every C(24,7)=346,104 seven-position query set against compatible UNSAT permutations for each of four fixtures. It checks inclusion minimality by every one-position deletion, not by calling Hall's theorem or the structural formula for deciding which sets are forcing. Observed native runtime 9.28 seconds, within the 25-second research chunk guideline.

| Source tuple | All seven-bit SAT certificates | Inclusion-minimal seven-bit SAT certificates |
|:--|--:|--:|
| (0,0,0,0,7,7,7,7), balanced extremizer | 696 | 48 |
| (7,7,7,7,7,7,7,7), general extremizer | 26,736 | 1,680 |
| (0,0,1,1,6,6,7,7), balanced nonextremizer | 232 | 16 |
| (0,1,2,3,4,5,6,7), UNSAT negative control | 0 | 0 |

Exactly **1,384,416 independently tested seven-query sets**, zero failed assertions. In the balanced sweep, observed M7 histogram (value:count) was 0:45,360; 4:120,960; 8:120,960; 12:26,880; 16:15,120; 24:13,440; 48:280. The histogram is **COMPUTATIONAL**, not claimed proved by an asymptotic argument. Original TMR-5/011's 16 and 1,680 counts are independently reproduced and the new 48 bound is witnessed. No direct physical Turing-machine execution, full parser, Horn-SAT/2-SAT/XOR implementations, treewidth DP, or LaTeX compilation was performed. Those are not needed for the narrowly scoped finite certificate theorem, and remain required controls for any proposed universal processing lower bound.

**Reproducible code:** experiments/tmr/tmr2_m7_independent014.py, native-tested exact Git blob 35bf642a99b6d5e6718f1844f206b8222083f2eb.

**Immutable raw evidence:** results/raw/tmr/2026-11-14_0017_TMR2_M7_EXTREMAL014_RAW.json, native-output exact Git blob 54e8db04619f8c038150d66aa9cfdf232ae4fcf8.

The program uses Python arbitrary-precision integers to store 40,320-bit compatibility sets **only in the finite verifier**. It does not claim a unit-cost arbitrary-word operation in a SAT machine theorem.

## 5. Primary literature, historical controls, dependency status and next arrow

Primary originals checked in this run:
- P. Hall, *On Representatives of Subsets*, Journal of the London Mathematical Society s1-10 (1935), pp. 26-30, https://doi.org/10.1112/jlms/s1-10.37.26 . Hall is used only for the finite perfect-matching criterion.
- H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity*, Theoretical Computer Science 288 (2002), pp. 21-43, https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf . Certificate complexity is a restricted query measure, not a superpolynomial TM time theorem.
- L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), pp. 835-865, https://doi.org/10.1145/1101821.1101822 . Their random-access simultaneous **small-space/time** exclusion cannot be promoted to an all-polynomial-time, arbitrary-workspace SAT separation.

Repository originals examined: TMR-2/010's authenticated G_r and near-linear scan algorithm; TMR-2/011-/013's physical observation-transfer and exact 5/6 certificate bounds; original TMR-5/010-/011; TMR-3/012 conditioned prefix-code correlation warning; TMR-4/014 program-oblivious prepared-state cheap edge; original historical LSPV-5/464 abstract-history counterexample. Those restrictions and genuine cheap computations remain active falsifiers, not erased by the new extremal counts.

Preflight: read the 2026-11-13 12:49 PST TMR replacement directive FIRST; inspected both root proof trackers (proof1.txt full 28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt full authentic Git blob 1,051,196 characters, blob 930c5eeddafce656717f28055a7a9a755f44737c), canonical main.tex full authentic Git blob 2,518,238 characters, blob 0233cb0ca16a63a2a63a83af6a61ffe985632945; latest issue #3 through TMR-5/011; AGENTS.md, CODEX.md, repo skill, and the five latest peer handoffs. Historical old role allocations are superseded by the controlling directive.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** P1-01/P1-03/P1-04 and P2-00 remain OPEN. Neither root tracker is edited. TMR-5 owns canonical root main.tex synthesis; this run does not modify it. No scheduled tasks or agent identities are altered. The newly proved scoped M7 classification and the CANDIDATE extremal statements do not establish an unrestricted processing cost.

**One next target:** Have TMR-5 independently verify the sharp M7 maximum 48 for balanced and 1680 general and their equality classifications, then leave certificate multiplicity behind unless it yields a noncircular cost statement on every actual configuration of one fixed correct SAT machine after input copying. TMR-3 should audit actual crossing causal structure, and TMR-4 should test any program-specific post-copy potential against the authenticated fast G_r classifier.

END_OF_REPORT::TMR2::M7_EXTREMAL014::2026-11-14_0017_PST
