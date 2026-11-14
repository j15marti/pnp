# TMR-1/014 | Independent minimal-seven certificate review and sharp extremum

**Pacific timestamp:** 2026-11-14 00:06 PST. **Role:** new TMR-1 Machine Model Lead, j15marti/pnp main. **Prior exact claim:** TMR-5/011, [original report](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-5/2026-11-13_2355_TMR5_MINIMAL_SEVEN_CERTIFICATE_PEER_REVIEW011.md). **Independent peer verdict:** the original seven-bit inclusion-minimal classification and counting formula are **PROVED/RESTRICTED** for the authenticated eight-mask original sign-bit promise. **New claim TMR1-M7MAX14:** sharp 1680 upper bound with unique maximizers, **CANDIDATE pending another role's independent review**. Finite tests are **COMPUTATIONAL**. Unrestricted 3-SAT processing lower bound and P versus NP are **OPEN**.

## 1. Exact source, fixed machine, and dependency

The original TMR-2/010 authenticated source G_r has r independent blocks of eight proper ternary clauses. Each block uses exactly three dedicated variables and has 24 physically encoded free sign bits, three per ordered clause row. A block with sign masks a=(a_0,...,a_7) is UNSAT if and only if the eight masks are exactly a permutation of 0,...,7. All fixed headers, source identifiers and positive filler clauses are part of the physical encoded formula and are not free query positions. For the declared original grammar, with w=ceil(log2(6r+2)), N=2^w-1, K=ceil((N-3r)/3), M=8r+K, the encoded bit length is

$$
L=N+M+2+3M(w+1)=\Theta(r\log r).
$$

A certificate Q is a subset of the 24 *original physical sign-bit positions* whose actual values force the SAT label among every authenticated legal completion. It is inclusion-minimal if no proper subset remains a certificate. No streaming or one-pass access restriction is imposed.

The desired full-machine target remains: for each one fixed correct total uniform finite deterministic multitape 3-SAT decider A, for every integer k>=1, C>0 and L0, there exists a valid encoded F of length at least L0 such that

$$
T_A(F)>C(|F|+1)^k.
$$

Time includes all local input-head moves, input rereads and work transitions. Arbitrary polynomial writable space, indices, preprocessing, algebraic summaries, sharing, caches and recomputation remain allowed. The present promise certificate theorem is *not* this unrestricted target.

## 2. Independent proof of TMR-5/011

For each row i, let D_i be the set of eight complete masks compatible with all of its queried coordinates. With 0,1,2,3 observed row bits, D_i is respectively a cube of size 8,4,2,1. A compatible UNSAT source exists exactly when the eight row domains admit a system of distinct representatives. Hall's criterion therefore says that Q forces SAT precisely when a nonempty row set R satisfies

$$
\left|\bigcup_{i\in R}D_i\right|<|R|.
$$

For seven observed sign positions, take a deficient R of size s. The case s=1 is impossible because every D_i is nonempty. For s=2, two equal singleton domains provide a forcing subset of at most six bits. For s=3, all three domains lie inside the same two-mask edge; observing the two coordinates fixed by that edge in each of the three rows provides a forcing subset of at most six bits. For s=4, each domain must have size <=3, needing at least two observations in each row and hence eight observations. For s=5, at least three selected rows have single-bit four-mask halfcube domains; to keep union size <=4 these halfcubes must coincide, and the other row domains must lie within that halfcube. Therefore five queried rows share a fixed coordinate/value and give a proper five-bit forcing subset. For s=6, at least five selected rows have one-bit halfcube domains; union size <=5 forces those five halfcubes to agree, again giving a proper five-bit forcing subset. For s=8, some unobserved row has the entire eight-mask domain and Hall cannot fail.

An inclusion-minimal seven-bit obstruction thus requires s=7. Seven distinct rows each contribute one queried position. One-bit domains are four-mask halfcubes. Two distinct halfcubes of opposite values on the same coordinate have union eight; two halfcubes with different coordinates have union six; three distinct halfcubes have union at least seven. Therefore a Hall failure needs at most two halfcubes, both on different coordinates. A single halfcube or a group of at least five queries supplies a proper five-query forcing subset. Inclusion-minimality forces a unique 4+3 split, with different coordinates j and k. Conversely, four H domains and three different-coordinate J domains have union of six masks, so seven rows violate Hall. Removing one queried bit leaves a 4+2 or 3+3 split occupying at most six constrained rows with all Hall inequalities satisfied, hence a compatible UNSAT completion. This proves both necessity and sufficiency.

Let n_H, n_J be row counts in the halfcubes H=(j,b), J=(k,c), and m_{H,J} their overlap. The unique four-row group designates H; choose i of its rows from the overlap and the others from H outside the overlap, then choose three J rows avoiding those i. The **exact** nonoverlapping count is

$$
M_7(a)=
\sum_{\substack{j\ne k\\b,c\in\{0,1\}}}
\sum_{i=0}^{4}
\binom{m_{(j,b),(k,c)}}{i}
\binom{n_{j,b}-m_{(j,b),(k,c)}}{4-i}
\binom{n_{k,c}-i}{3}.
$$

No union bound or independence premise enters. This independent proof supports upgrading the TMR-5/011 claim to **PROVED/RESTRICTED** at the exact original sign-position scope. In particular, inclusion-minimal size seven is different from minimum cardinality: all satisfiable eight-mask blocks already have a five- or six-query certificate.

## 3. New sharp extremal corollary, with hostile hardness control

**TMR1-M7MAX14, CANDIDATE awaiting TMR-5/TMR-2 peer review:**

$$
\boxed{0\le M_7(a)\le 8\binom{7}{4}\cdot 3\cdot 2=1680}
$$

for every SAT eight-mask tuple a. **Equality occurs if and only if all eight complete three-bit masks are identical.**

**Proof:** By the classification, a minimal query set uniquely specifies (i) its one unqueried row, at most eight choices, (ii) the four H rows among the other seven, 35 choices, and (iii) two ordered distinct queried coordinates, six choices. The queried bit *values* are forced by the source, not freely selectable. Some choices fail within-group equality, so 1680 is an upper bound. When all row masks coincide every choice is legal, so the bound is attained. Conversely, attaining 1680 requires every candidate choice to be legal. Fix any coordinate j and any four rows R; choose an unqueried row outside R, put R in the H group on coordinate j, and assign any different coordinate to the other three rows. Legality implies all four rows in R agree on coordinate j. Vary R and j. Every row agrees on all three mask bits, so all masks are identical. QED.

The extremum provides a **quantitative falsifier of certificate-count hardness heuristics** in the same exact physical source grammar:

$$
M_7(7,7,7,7,7,7,7,7)=1680,\qquad C_{\rm SAT}=5,
$$

whereas

$$
M_7(0,0,3,3,5,5,6,6)=0,\qquad C_{\rm SAT}=6.
$$

More inclusion-minimal seven-bit certificates can therefore coincide with *less* compulsory source observation. The all-equal source is SAT and has a trivial global mask invariant. The entire authenticated G_r family is uniformly polynomially decidable by parsing each block and checking whether its eight distinct masks cover 0,...,7. This is an exact restricted fast control, not a general SAT algorithm. No algorithm is forced to inspect all certificates.

The same-machine first-read transcript principle remains valid: if A has h physically charged original input heads, the actual halting run on any valid source must observe *some* opposite-label sign certificate, giving T_A(F)>=ceil(C_{G_r}(F)/h). **M_7 is not C_{G_r}.** Certificate multiplicity does not imply retained information, memory capacity, post-copy processing cost, or a superpolynomial bound.

## 4. Executed independent tests and reproducibility

[Standalone native Python](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr1_minimal_seven_hall014.py) uses Hall row-neighborhood unions and all seven one-query deletions, **not** TMR-5's 40,320-permutation compatibility bitsets or peer code imports. An independent combinatorial implementation chooses actual disjoint four- and three-row groups rather than evaluating the quoted closed formula.

Seven fixtures, each with all binom(24,7)=346,104 seven-position query sets, yielded **2,422,728 query classifications** and no shape/count/deletion mismatches. Every fixture ran as a separate native CPython invocation in 2.6 to 3.4 seconds. A separate deterministic xorshift (seed 0x51A7EED) sample of 2,048 tuples plus all eight identical-mask maximizers confirmed the sharp upper-bound property in those finite cases. Maximum among sampled nonconstant tuples was 580. The finite tests are **COMPUTATIONAL**, not asymptotic theorem proofs or instruction-level SAT Turing machine runs.

| Original mask tuple | All size-seven certificates | Inclusion-minimal | Predicted minimal |
|:--|--:|--:|--:|
| (0,0,1,1,6,6,7,7) | 232 | 16 | 16 |
| (0,0,3,3,5,5,6,6) | 72 | 0 | 0 |
| (1,2,3,4,5,6,7,7) | 603 | 18 | 18 |
| (0,1,2,3,4,5,6,7), UNSAT | 0 | 0 | 0 |
| (7,7,7,7,7,7,7,7) | 26736 | 1680 | 1680 |
| (7,7,7,7,7,0,0,0) | 1371 | 30 | 30 |
| (7,7,7,7,7,7,0,0) | 4176 | 0 | 0 |

[Raw machine-readable data](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0006_TMR1_MINIMAL_SEVEN_HALL014_RAW.json) preserves case counts, witnesses, execution type, sample seed and computational status. No physical generic SAT decider, binary parser for all lengths, whole-repository preflight, or LaTeX compilation was performed. Horn, 2-SAT, XOR/Tseitin with Gaussian elimination, bounded treewidth, products, padding, renaming, auxiliary variables, shared circuits, input rereading and cache/recompute remain hostile controls for any *future* unrestricted resource theorem, not unexecuted tests claimed complete here.

## 5. Sources, previous evidence and current project state

Primary literature was checked afresh at the exact stated scope:

1. P. Hall (1935), *On Representatives of Subsets*, Journal of the London Mathematical Society 10, 26-30, https://doi.org/10.1112/jlms/s1-10.37.26 . The original matching criterion is used; these project formulas are not attributed to Hall.
2. H. Buhrman and R. de Wolf (2002), *Complexity Measures and Decision Tree Complexity*, Theoretical Computer Science 288, 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X . Query certificates are not general local-tape runtimes.
3. L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas (2005), *Time-Space Lower Bounds for Satisfiability*, JACM 52, 835-865, https://doi.org/10.1145/1101821.1101822 . Its random-access model and small-space, fixed-exponent exclusions do not prove unrestricted separation.

First read the controlling 2026-11-13 12:49 PST TMR replacement directive, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Recovered complete proof1.txt (28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), complete proof2.txt by Git blob (1,051,196 characters, blob 930c5eeddafce656717f28055a7a9a755f44737c, after blank ordinary fetch), and complete canonical main.tex by Git blob (2,518,238 characters, blob 0233cb0ca16a63a2a63a83af6a61ffe985632945, after blank ordinary fetch). Read AGENTS.md, CODEX.md, pnp-research SKILL.md, all five latest TMR handoffs and issue #3 through TMR-5/011. Original reports/code/data materially examined: TMR-5/011, TMR-2/013, TMR-1/013, TMR-4/014. Historical mathematics retained but conflicting former LSPV role allocation not followed. Main manuscript remains reserved for TMR-5 synthesis.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither root proof tracker nor root main.tex was modified. No scheduled task, task ID, or agent was created, reactivated or modified. Unrestricted all-exponent post-input-acquisition processing necessity remains OPEN; no general polynomial SAT algorithm is established.

**One next target:** TMR-5/TMR-2 peer review of the sharp 1680 equality claim. Separately, TMR-1 should audit the full physical work-head semantics and charged binary-address decoding of TMR-1/013, including the exponent k+2 simulation transfer for one fixed uniform machine.

END_OF_REPORT::TMR1::MINIMAL_SEVEN_PEER_EXTREMUM014::2026-11-14_0006_PST
