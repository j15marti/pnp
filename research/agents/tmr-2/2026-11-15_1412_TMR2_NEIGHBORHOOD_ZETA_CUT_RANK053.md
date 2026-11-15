# TMR-2/053: Exact neighborhood-zeta rank and a three-variable strict-CNF firewall

**2026-11-15 14:12 PST | PNP Information Necessity | Track A | revision `tmr2_neighborhood_zeta053.v1`.**
**Status:** PROVED/EXACT for the scoped algebraic lemmas and exact CNF gadget (independent mathematical peer review OPEN); finite experiments COMPUTATIONAL. General circuit/SAT lower-bound transfer OPEN. **P versus NP OPEN.**

## 1. Candidate, objects, and precommitted falsifiers

**Candidate:** Replace crude induced-matching rank estimates on a cross-only cut by the exact rank determined by distinct neighborhood unions; then ask whether its two high-rank selector-conditioned slices remain a compulsory dynamic resource.

For a finite simple graph G=(A disjoint-union B,E) with **all edges crossing the declared partition**, define the fixed-formula satisfying-assignment matrix

```
D_G(S,T) = 1[for every (a,b) in E, NOT(a in S AND b in T)]
```

Rows are S subset A and columns are T subset B. This is NOT the SAT decision function on encoded formulas and NOT an arbitrary machine computation. The complement J-D is the selector-z=1 partial projection of a functional CNF, not a standalone SAT verdict.

Falsifiers fixed before literature and corpus comparison: (F1) distinct OR-neighborhood unions might become linearly dependent in GF(2) or odd characteristic; (F2) a simple graph with many edges but small neighborhood-union closure might have small rank; (F3) selector contraction, unique extensions, a compact circuit, or an all-zero certificate might bypass large rank; (F4) applying the cross-only formula to an original graph with internal A- or B-edges might silently overclaim an all-cut theorem. F2, F3 are real shortcuts; F1 is disproved; F4 is prohibited by the scope.

## 2. Exact neighborhood-zeta theorem, every field

For each S subset A define the forbidden B-neighborhood union

```
U(S) = union_{a in S} (N_G(a) intersect B).
F_G = {U(S) : S subset A},        r_G = |F_G|.
```

**THEOREM 053-A (PROVED/EXACT, restricted).** For every field K, with no hypothesis on characteristic,

```
rank_K(D_G)       = r_G,
rank_K(J - D_G)   = r_G - 1,
rank_K(D_G + J-D_G) = rank_K(J) = 1.
```

The exact deterministic one-way communication complexity for *evaluating this fixed relation* when Alice holds S and Bob holds T is ceil(log2 r_G) bits (the final output bit and protocol convention excluded).

**Proof.** Let v_U(T)=1[T subset B\U]. Every row of D_G equals v_{U(S)}. The complete square matrix Z with rows indexed by all U subset B, columns by all T subset B, and Z[U,T]=v_U(T) is the Boolean-lattice subset-zeta matrix after complementing the row index. Under inclusion order Z is triangular with diagonal 1, so det(Z)=+/-1. Thus its 2^|B| rows are linearly independent over **every** field. Distinct members of F_G give distinct independent rows, proving the first identity. Since U(empty set)=empty set, v_empty=the all-ones row. The rows of J-D are 0 for U=empty and v_empty-v_U for every U in F_G minus {empty}. Those r_G-1 vectors are independent, as any dependence would contradict the independence of {v_U}. The last identity is literal entrywise addition and rank(J)=1. For one-way communication, two S with different U give different Boolean rows and cannot share a deterministic message; sending the U-class index suffices. QED.

**Sharp examples:** a k-edge matching has r=2^k and complement rank 2^k-1. K_{k,k} has k^2 edges but r=2 and complement rank 1. A star has r=2 regardless of its degree. Thus counting edges, expansion across ONE cut, or the number of accepted assignments cannot substitute for exact neighborhood closure.

**Expansion corollary (one cut at a time).** If the cross-edge graph is obtained by deleting within-side edges of a degree-at-most-d graph G with balanced edge boundary at least h n/2, greedy selection of crossing edges gives an induced matching of size t >= |E_cross|/(2d^2) >= h n/(4d^2). The 2^t subsets of the selected A endpoints have pairwise distinct neighborhood unions on the selected B endpoints. Hence r_G >= 2^{h n/(4d^2)}. This applies to the separately constructed *cross-edge graph for each cut*. It is NOT a claim that a single cross-only formula works simultaneously at every partition; the earlier TMR-2/052 fixed-full-graph all-cut result is a separate theorem.

## 3. Exact strict proper 3-CNF with unique extension

Let the original n variables be x_1,...,x_n, introduce three fresh variables p,q,r, and add **seven** distinct 3-clauses, one falsified by each of the seven nonzero assignments to (p,q,r). This forces the unique pin assignment (0,0,0). For every cross edge (u,v), add the proper ternary clause

```
(not x_u OR not x_v OR p).
```

Every satisfying original x of the cross-edge independence condition has **exactly one** extension to the pins, and every violating x has none. For m crossing edges the complete, duplicate-free, width-exactly-three source has

```
V = n+3 declared variables, C = m+7 clauses, 3(m+7) literal occurrences,
encoded length N = O((n+m) log(n+m)) bits.
```

All-zero is an immediately verifiable satisfying assignment. A *fixed total correct* SAT decider may try that assignment first, then perform an ordinary fully charged exhaustive fallback on other CNFs; on every instance in this constructed family it succeeds after one syntactic scan, O(N) work and O(log N) temporary indexing under the standard sequential read-only input model. This does NOT make arbitrary SAT easy.

For a counted uniquely determined selector z=OR_{edges}(x_u AND x_v), the **existing** TMR-2/052 functional strict-3CNF lift uses V=n+2m+2 variables, C=6m+4 clauses and 18m+12 occurrences for m>=2. Applying Theorem 053-A to its cross-only instance strengthens its generic bound to the exact ranks (r_G,r_G-1), yet contracting the real selector collapses to rank one. No uncharged auxiliary multiplicity is used.

## 4. Reproducible exact benchmarks

Executable: `experiments/tmr/tmr2_neighborhood_zeta053.js`.
Raw per-cut data: `results/raw/tmr/2026-11-15_1412_TMR2_NEIGHBOR_ZETA053_V8_RAW.json`.
Revision `tmr2_neighborhood_zeta053.v1`, deterministic LCG seed 20261115 only for the 12 Q4 partition samples, finite field prime 65521. No packages. Executed in hosted V8; native Node replay, repo-wide preflight, LaTeX build and a physical Turing-machine emulator were not run.

**362 exact cuts, 2,938 assertions, 12,032 full pin-assignment evaluations, zero failures.** GF(2) elimination checked all cases; F_65521 elimination checked every case with n<=10. Exhaustive balanced cuts: cycle C6 (20), cube Q3 (70), Petersen (252); plus one-cut matching k=1..6, K4,4, star and 12 seeded Q4 cuts.

| Cross-edge family | Exact neighborhood-rank range | Number of tested partitions |
|---|---:|---:|
| Matchings k=1..6 | 2,4,8,16,32,64 | 6 |
| Complete bipartite K4,4 | 2 | 1 |
| Star K1,6 | 2 | 1 |
| C6 cross-edge subgraphs | 4..6 | 20 |
| Q3 cross-edge subgraphs | 4..16 | 70 |
| Petersen cross-edge subgraphs | 14..32 | 252 |
| Q4 cross-edge subgraphs | 36..72 | 12 seeded |

For every tested case, rank_GF2(J-D)=r-1, and the odd-prime runs agree. The strict-CNF unit tests enumerate all 8 assignments to pins for all original x on six small graph families, verifying the unique-extension count exactly.

These are **finite COMPUTATIONAL checks**, not a verified asymptotic circuit or machine lower bound.

## 5. Same-realization resource ledger and cheap controls

| Operation/object | Time/work | Workspace/representation | Status |
|---|---|---|---|
| Build graph-to-strict-CNF source | O((n+m)log(n+m)) bit output work | O(log(n+m)) working bits with streamed edge enumeration, plus input graph storage if materialized | Constructive restricted |
| Evaluate all-zero assignment on source | O(N) sequential bit work | O(log N) bits for grammar/registers | Genuine SAT shortcut |
| Enumerate distinct neighborhood unions | O(2^{|A|}(|A|+|B|)) bit operations via bitmask ORs, conservative | up to O(r_G|B|) bits retained | Rank *acquisition* not free |
| Dense field-rank check | naive polynomial in 2^{|A|}+2^{|B|} field operations | exponential matrix possible; bit length of F65521 entries <=16 | COMPUTATIONAL only |
| Selector contraction | exact symbolic identity D+(J-D)=J | compact O(m) gates, no need materialize D | Legal cheap representation |
| Total correct decider on off-family inputs | exhaustive fallback, may be exponential | O(N) bits of assignment/workspace | Correctness retained |

The actual benchmark does NOT implement a polytime general #SAT counter. A selector sum identity is not a physical one-step machine transition. All source parsing, alternative representations, sharing, recomputation, failed attempts and output are chargeable. All unknown machine operations remain MAY.

**Hostile controls:** DISJ matching has rank 2^k while its 2CNF and strict lift have a linear-size gate/edge description and all-zero witness. K_{k,k} shows raw edge count is a false rank proxy. The core is Horn and Krom; forced-pin strict 3CNF is a transparent 2SAT/unique-extension quotient, not a hard general 3SAT instance. Gaussian elimination, affine/XOR controls, equality/union-find, bounded-treewidth DP, certified autarkies, independent products, zero-padding, learned clauses, caching and recomputation cannot be discarded from an arbitrary algorithm. Matching has bounded treewidth; K_{k,k} has growing width but tiny rank. Invertible local bases preserve rank; no Walsh-Hadamard-over-GF(2) claim. A uniquely satisfying full assignment has a rank-one indicator across all cuts; isolation by Valiant-Vazirani is randomized and promise-sensitive. Boolean assignment tensors and SAT decisions on *input strings* remain distinct.

## 6. Mandatory four-gate table

| Gate | Verdict and reason |
|---|---|
| 1. DISJ sanity | **PASS** as hostile falsification: matching has 2^k rank and O(k) 2CNF/circuit plus all-zero witness. Any unrestricted rank-to-work claim is **FAIL**. |
| 2. Relativization | **PASS restricted** for a purely finite algebraic theorem. A necessary nonrelativizing step for P-vs-NP is **OPEN**; no algebrization/Natural Proofs avoidance theorem is asserted. |
| 3. Simultaneous DTISP | **NOT APPLICABLE WITH REASON** to matrix rank. The same all-zero verification execution has explicit O(N) time and O(log N) workspace; no SAT forbidden-box machine or reduction is offered. Unrestricted transfer **OPEN**. |
| 4. Configuration counting | **PASS** as an upper-bound guard only: for total deterministic read-only-input machines T<=2^{O(s+log N)}, or 2^{O(s)} if s>=log N. This was not used as a lower bound. |

## 7. Corpus reconciliation, primary sources and next lemma

Read FIRST the 2026-11-15 SAT-compression directive (blob 7b8804dc...), then proof1.txt fully (28,714 characters, SHA 06f7ebc8...), proof2.txt and main.tex exact SHAs (930c5eed..., 6ac34c5d...) whose oversized connector bodies returned EMPTY, AGENTS.md, CODEX.md, repository research skill, all five current TMR handoffs, issue #3 through the latest 2026-11-15 entries, original TMR-2/052 and TMR-4/053 reports/code/raw, and TMR-5/049 count-compression counterexample. Local GitHub clone DNS failed; preflight scripts and full root-content reconciliation could not be run. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.**

Previous TMR-2/052 showed rank-collapse for a fixed graph over all cuts. This run adds the **exact** neighborhood-union rank and exact complement rank for bipartite cross-only instances, plus a smaller n+3 strict-3CNF unique-pin lift. It does **not** replace /052 or its fixed-graph all-cuts theorem. TMR-4/053's adaptive switch-transcript rectangle bound stays valid and is a separate restricted representation theorem; no contradiction. The TMR-5/049 scalar-count collision remains a hostile warning about compression definitions. Historical /341 is FAIL as full logical UNSAT authority; /386 is RESTRICTED. No agent identities or schedules changed.

Primary literature used for scope: Mehlhorn and Schmidt, *Las Vegas is Better Than Determinism in VLSI and Distributed Computing*, STOC 1982, https://people.mpi-inf.mpg.de/~mehlhorn/ftp/LasVegasDeterminismVLSI.pdf (communication-matrix rank lower bound in split-input model); Kushilevitz and Nisan, *Communication Complexity*, Cambridge University Press, https://doi.org/10.1017/CBO9780511574948 (row classes/communication model). The Boolean-lattice zeta identity is reproved completely above, not claimed as a novel general algebraic technique.

**ONE NEXT LEMMA for TMR-4/TMR-5 peer review:** characterize whether an adaptive shared-branching-program's number of *distinct dynamically realized* neighborhood-union types yields a lower bound after charging every owner switch and allowing input-dependent order. Test on K_{k,k}, DISJ_k, the /052 selector and an all-zero accepting SAT path. A positive static charge cannot be used without a same-machine, every-transition transfer. **P versus NP OPEN.**
