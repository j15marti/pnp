# LSPV-3: criticality forces an identity obstruction matrix, but not a hard selector

**November 18, 2026, 20:22 PST.** Role: PNP Hypergraph & Proof Certificates (historical role, no schedule changes). **PROVED/RESTRICTED** incidence theorem, **COMPUTATIONAL** independent finite replay, general time lower bound **OPEN**. P versus NP **OPEN**.

## Candidate, exact scope, and pre-search falsifiers

**Candidate:** Edge-minimal UNSAT in a private-disjoint block decomposition forces every original block to have a distinguishing shared assignment on which it alone is refutable. Thus the full-domain row/block obstruction matrix contains a permutation identity and has maximal column rank and maximal set-cover optimum, even when SAT-deletion witnesses and a global obstruction are inexpensive.

Falsifiers checked: (F1) a reconstructed deletion witness violates an intact source arc; (F2) a supposedly unique bad block has an internal extension under the same shared row; (F3) source H9/H33/H_t is satisfiable or a deletion remains UNSAT; (F4) the source-derived path support differs from exhaustive five-color propagation. All four finite controls passed on the sources below. The theorem itself is symbolic; the finite checks do not imply a time lower bound.

## Main theorem: criticality => identity minor

Let (F(z,x_1,ldots,x_B)=igwedge_{j=1}^B F_j(z,x_j)) be UNSAT, with pairwise disjoint private scopes (x_j). Assume **block-minimality**: deleting any nonempty original block makes the remaining conjunction SAT. Define the complete-domain blocker relation
[
M(z,j)=1iff F_j(z,cdot)	ext{ is UNSAT}.
]
Then there are **pairwise distinct** rows (z_1,ldots,z_B) such that
[
oxed{M(z_i,j)=mathbf 1[i=j]}.
]
Consequently the complete matrix has rank (B) over **every field**, Boolean rectangle-cover rank (B), and minimum integral or fractional set-cover weight (B) when columns are original blocks. These statements concern the chosen block language, not intrinsic computation.

**Proof.** Since (Fsetminus F_j) is satisfiable, take a full coloring/assignment to every variable in all other blocks. Restrict it to the shared variables to get (z_j). Every (F_i), (i
e j), has a private witness at (z_j), so (M(z_j,i)=0). If (F_j(z_j,cdot)) were satisfiable too, its disjoint private witness could be pasted with the others, contradicting UNSAT of (F). Hence (M(z_j,j)=1). Different private-point rows cannot coincide. The resulting (B	imes B) submatrix is the identity. The full matrix has exactly (B) columns, giving rank (B) over all fields. The identity lower-bounds any Boolean rectangle factorization by (B), and columnwise rectangles give an upper bound (B). Every fractional cover of all rows must assign column (j) weight at least one because row (z_j) has only that blocker, so its optimum is (B). QED.

**T5 corollary.** Let (H) be connected, edge-minimal UNSAT for (R(a,b)iff(b-a)mod5in{1,3}). Partition every original arc into nonempty blocks whose private internal vertices are disjoint after fixing the common branching vertices. For block (j), choose any original arc (e_j) in it. A coloring of (H-e_j) exists by criticality and witnesses all other blocks. Thus the theorem applies to every partition that meets the stated disjointness. In particular every maximal degree-two thread is essential to a full-branch-row cover. The proof does not assume a small source-visible UNSAT certificate, or efficiently **discover** the (z_j).

**Important scope:** if only (R<B) rows are supplied, the rank argument yields at most (R) essential columns from the selected rows. A list of some rows is not an UNSAT proof unless its coverage is shown complete or a separate sound symbolic argument covers all other rows. Coarsening the block partition changes the matrix and its rank; full-domain rank is a representation-sensitive property, not a lower bound for every correct algorithm.

## Source-authenticated finite verification

Executed an independent standard-library CPython MRV+arc-consistency solver and independent endpoint relation propagation, with source hashes verified against the existing repository originals. For each maximal thread, an actual (H-e) coloring was found using one original arc from that thread. Its branch-row projection was checked against **all** thread supports, with exactly one false thread. Every original-arc deletion was separately solved. Full-graph UNSAT was also independently checked.

| Source | n / m | branch vertices | maximal threads | UNSAT search calls | full deletions SAT | distinct identity rows | domain coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| H9 (four parallel paths) | 9 / 11 | 2 | 4 | 1 | 11/11 | 4 | all 25 rows |
| H33 (undirected girth 8) | 33 / 44 | 19 | **30** | 73 | **44/44** | **30** | 1,024 sampled rows, plus the 30 distinguishing rows |
| critical cycle H_2 | 9 / 11 | 3 | 5 | 1 | 11/11 | 5 | all 125 rows |
| critical cycle H_7 | 24 / 31 | 8 | 15 | 1 | 31/31 | 15 | 1,024 sampled rows, plus the 15 distinguishing rows |

The H33 incidence matrix therefore has an explicit (30	imes30) identity minor and rank **exactly 30**, despite being a 33-vertex high-girth finite critical instance. H33 has (5^{19}=19,073,486,328,125) possible branch rows, not 30. The 1,024 random rows were **not** an exhaustive certificate. The independent full-source UNSAT check is a separate finite computation. Maximum search calls on a deletion were 123. These calls are DFS nodes, **not** calibrated RAM instruction counts.

H33 bytes SHA-256: `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`, exact Git blob `c84890d9f32aee6d40e619f03e79d6b61b4e2d6f`, canonical repository source `research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5`. H9 bytes SHA-256: `15625c3bec0f5281a6a943f42b611995d9607cceec71c52e544bcd48f099d1d2`, Git blob `548acde751bee5de97e002897c47c4581bc55017`.

The prior LSPV-3 H_t construction already exhibited essential distinct blockers on one specific family. The theorem here extends the identity-minor conclusion to **every** block-minimal private-disjoint instance, and independently exercises it on the unrelated girth-eight H33 source. The prior LSPV-1 tight-five batch-lifting and Red Team thread-polynomial results remain accepted; this does not claim new original-vertex lift complexity.

## Arbitrary-CNF universality and optimization firewall

The older source-authenticated `SOURCE_COVER_OPTGAP146` already gave a reduction from SET COVER using fresh-private 3CNF point-exclusion chains. We independently replicated its projection mechanic, **not** as a new NP-hardness theorem: for any shared (k)-bit row (a), a signed clause (C_a=igvee_i(z_i
e a_i)) excludes exactly (a); standard existential Tseitin 3CNF chains keep private scopes disjoint. Grouping exclusion chains by arbitrary sets (S_j) makes (F_j(z,cdot)) UNSAT exactly when (zin S_j). Thus even easy local membership can implement an arbitrary overlapping cover hypergraph, and selecting a **minimum** original-block cover is SET COVER. But a nonminimal cover can simply select all blocks, so NP-hard **optimization** is not a lower bound for finding one bad block per row or for SAT decision.

Independent finite control: 24 random 16-row/6-block set systems (`seed=20261119`), 2,304 exact source/row membership assertions and 24/24 equality checks of the optimum; separately 5,440 single-forbidden-row existential-Tseitin tests for (k=3,4,5,6). No failures. This reproduces an old mechanism and calibrates the newer critical-matrix observation.

## Correct-path, two polarities, and source-bound certification

For private-disjoint blocks:
[
mathrm{SAT}(F)iffexists z orall j exists x_j:F_j(z,x_j),qquad
mathrm{UNSAT}(F)ifforall z exists j orall x_j:
eg F_j(z,x_j).
]

* **SAT path:** proposed shared (z) plus compatible witnesses for **every** private block, with a full original-source validator, is sound; an invalid candidate returns UNKNOWN. The complete witness and verifier/output are charged.
* **UNSAT path:** for **every** shared row in an authenticated complete domain, a block index (j(z)) plus a sound source-bound negative derivation for (F_j(z,cdot)) is a sound certificate. If the source-native system lacks negative derivations, an index alone is **not** a verifiable UNSAT certificate. An incomplete row list certifies only its listed rows. Wrong guesses return UNKNOWN.
* **Free label/polarity routing** is an extra advice channel, not uniform all-input decision. A supplied (k)-bit path to a sound deterministic verifier is not its acquisition. Exhaustive deterministic enumeration of (2^k) paths charges every failed verification and needs at least a path counter or an explicitly accounted alternative storage mechanism. If a path is an alternating strategy, universal subtrees or a fully specified, verified policy must be charged; an existential leaf is not the strategy.
* The existence of polynomial-size polynomially verifiable native negative certificates for arbitrary UNSAT CNFs would place coNP in NP, hence imply NP=coNP [2]. No such conclusion is assumed.

**Acquisition for the identity rows:** One may uniformly call a correct deterministic full T5/CNF solver on (H-e_j) once for each distinct block, then verify its coloring and project to (z_j). This costs (sum_j T_A(H-e_j)) plus parsing, validation, candidates, and output, not zero. The finite Python audit did precisely these searches. Criticality guarantees the existence of rows, **not** a polynomial acquisition bound.

## Supplied layout and exact resource barrier

With at most (R=N^{.195+o(1)}) explicit rows, (B=N^{.65+o(1)}) private-disjoint blocks and local source length (m=N^{.35+o(1)}), straightforward complete deterministic local child solving takes, under source-indexed streaming assumptions,
[
T(N)le N^{1.195+o(1)}+N^{.845+o(1)}T_A(N^{.35+o(1)}).
]
For (T_A(s)=s^{a+o(1)}), the (N^{1.33+o(1)}) endpoint requires (ale97/70approx1.385714). With one live child, writable space (N^{.5+o(1)}) requires local space exponent (sle10/7), plus a charged compiler and persistent buffers. The hypothesis SAT in P supplies no specific (a) or (s). The all-row branch assignment domain of H33 is vastly larger than (N^{.195}); do not identify the 30 critical rows with exhaustive coverage.

The Fortnow–van Melkebeek 2000 random-access deterministic SAT exclusion at time (N^{1.33}) applies only to space exponent (d<((a+2)/a^2-a)/2=0.2762629317655) at (a=1.33), not (d=.5) [3]. FLMV 2005 gives a positive but model-specific deterministic space threshold for any time exponent below the golden ratio, and a separate co-nondeterministic SAT result for time exponents below (sqrt2) [4]. The (2cos(pi/7)) alternation-trading n^{o(1)}-space barrier concerns deterministic complete SAT, not the .5-space claim [5]. None of these proves a promised-SAT T5 witness lower bound, an UNSAT-block-finding lower bound, or a proof-system-specific refutation lower bound. A nondeterministic SAT witness verifier is different from a nondeterministic UNSAT certificate, and nondeterministic/co-nondeterministic bounds cannot silently change polarity.

## Gates and next dependency

DISJ: PASS for authenticated thread partitions and independent CNF chain variables, OPEN for arbitrary supplied decompositions until verified. Relativization: the identity theorem is elementary and relativizing; no nonrelativizing separation. Simultaneous DTISP: no worst-case time/space separation. Deterministic configuration counting: no lower bound from row-count/rank. Algebraic/compact shortcuts: the low-girth H_t family has a short GF(5) cycle explanation; H33's finite easy solver search is not an asymptotic upper bound. Natural Proofs/algebrization: not relevant to the restricted exact identity statement; no unrestricted circuit property derived.

**Next target:** A useful cross-row obstruction mechanism must move from pointwise rank to a **source-verifiable symbolic negative derivation** with deterministic acquisition. Test a source-bound projected blocker (C_j(z)), verify (F_jRightarrow C_j) with actual native proofs, and verify that the resulting projected constraints exclude the COMPLETE shared domain. Account for all proof discovery/replay and reject a row list lacking a completeness certificate. For intrinsically critical high-girth T5, test whether limited-width GF(5) cycle constraints produce such a compact reusable derivation despite the full-rank pointwise matrix.

**Publication:** report, raw summary, reproduction code, and handoff are intended for the existing LSPV-3 archive; historical role schedule/enable state and TMR ownership unchanged. Root retired proof trackers and main.tex were not edited.

### Primary references

[1] Karp RM. Reducibility Among Combinatorial Problems. 1972. DOI: 10.1007/978-1-46884-2001-2_9 (original chapter DOI has 1-4684-2001-2_9).
[2] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. JSL 44, 1979. DOI: 10.2307/2273702.
[3] Fortnow L, van Melkebeek D. Time-Space Tradeoffs for Nondeterministic Computation. DIMACS TR 2000-06. https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html
[4] Fortnow L, Lipton R, van Melkebeek D, Viglas A. Time-Space Lower Bounds for Satisfiability. JACM 52(6), 2005. https://doi.org/10.1145/1101821.1101822
[5] Buss S, Williams R. Limits on Alternation-Trading Proofs for Time-Space Lower Bounds. Computational Complexity 24, 2015. DOI: 10.1007/s00037-015-0104-9.
