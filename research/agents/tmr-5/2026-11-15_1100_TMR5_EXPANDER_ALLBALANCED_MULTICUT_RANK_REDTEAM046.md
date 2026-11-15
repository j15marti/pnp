# TMR-5/046: An exponential **all-balanced-cut** rank control with a trivial SAT witness

**2026-11-15 11:00 PST (America/Los_Angeles) | PNP Machine Bottleneck Redteam | EXPANDER-MULTICUT046**

**Scientific status:** The elementary all-fields rank implication below is **PROVED/RESTRICTED** for the stated graph/formula/evaluation-matrix model, independent mathematical review OPEN. Concrete graph enumerations are **COMPUTATIONAL**. Any transfer from the evaluation matrix to unrestricted SAT decision or general-circuit lower bounds is **FAIL** on this very family. P versus NP remains **OPEN**.

## 1. First claim and four falsifiers

**Candidate to attack:** Replacing a single static variable cut with **all balanced variable cuts** might repair the known DISJ static-rank false positive for a purported structural obstruction to general SAT algorithms. Test that proposed implication against an explicit bounded-degree expanding family, keeping full cut matrices distinct from actual SAT decision complexity.

Falsifiers declared before primary-source and historical-corpus review:

1. The advertised exponential cut rank vanishes on a different balanced partition, or after restricting to one field.
2. An allowed compact circuit/Horn/2-SAT algorithm decides the family quickly although every balanced assignment-evaluation matrix has large rank.
3. Source-recognition, construction of the explicit graphs, cut discovery or arithmetic preprocessing is being treated as free, or a prescribed OBDD order is mistaken for an unrestricted circuit.
4. Allender MajMajSAT or FLMV small-space noncontainment is silently invoked with the reduction direction reversed, the small-space condition removed, or a nonuniform/common hard family substituted for the quantified language theorem.

Falsifier 2 survives and defeats the proposed unrestricted inference, even though the rank claim is mathematically sound. The current `main` branch's **newer** user-authorized 2026-11-15 SAT compression / circuits refocus (`research/coordination/2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md`, blob `7b8804dc7587abc5134055b5b0d16a143055ca5a`) supersedes the previously scheduled Allender-first scientific priority. The Allender directive was read first as requested by this run; thereafter the newer authority was located in root AGENTS.md and read. Allender and fusion remain supporting calibrations. No roles, schedules, enabled states or ownership are changed.

## 2. An exact all-balanced-cut theorem

Let `G=(V,E)` be an undirected **simple** graph on `n` vertices, maximum degree at most a fixed integer `d>=1`, such that every `S subset V` with `|S|<=n/2` has at least `h|S|` edges crossing its boundary, for some `h>0` independent of `n`. Take an explicit infinite family of such constant-degree edge expanders, which is available by standard explicit expander constructions [1]. For definiteness, deleting loops and parallel duplicates from a bounded-degree expander multigraph preserves bounded degree and loses at most its degree factor in the edge-expansion constant. We use the resulting undirected simple graph, not a claim about the original multigraph's simple-edge count.

Define the original **Horn 2-CNF** (also a width-at-most-three CNF)

```
F_G(x_1,...,x_n) = AND_{ {u,v} in E } ((NOT x_u) OR (NOT x_v)).
```

This is the indicator of independent sets of `G`; importantly `F_G(0^n)=1`. For a partition `V=A disjoint-union B`, let `M_{A,B}(a,b)=F_G(a,b)`, a `2^|A| x 2^|B|` **evaluation** matrix over any specified field. This is *not* the SAT decision function on encoded CNFs. Assume `n/3 <= |A|,|B| <= 2n/3`.

**Theorem 046A (all-balanced-cut rank firewall).** For every such partition and every field `K`,

```
rank_K(M_{A,B}) >= 2^(h*n/(6*d*(d+1))).
```

The precise integer form is `rank >= 2^ceil(h*n/(6*d*(d+1)))`; a weak real-exponent inequality suffices. Simultaneously the formula has `O(n)` input clauses and a uniform deterministic SAT witness `0^n`, and its *evaluation* has an `O(n)`-gate AND/NOT circuit (indeed a constant-depth unbounded-fan-in AND of binary clauses).

**Proof.** By expansion, the cut contains at least `h*min(|A|,|B|)>=hn/3` crossing edges. Greedily select one cut edge `{u,v}` and discard every remaining cut edge incident to a vertex of `N[u] union N[v]`, where `N[u]` is the closed neighborhood. At most `2(d+1)d` cut edges are removed per selection, because the union has at most `2(d+1)` vertices and each has degree at most `d`. The chosen cut edges form an **induced matching**: their endpoints are disjoint and no graph edge joins endpoints belonging to different chosen edges. Consequently the number `r` selected obeys

```
r >= |E(A,B)| / (2*d*(d+1))
  >= h*n / (6*d*(d+1)).
```

Fix every vertex outside the selected `2r` endpoints to zero on both sides. The resulting `2^r x 2^r` submatrix is, up to row/column permutations, `D^(tensor r)` where `D=[[1,1],[1,0]]`. No other clause survives as a nontrivial constraint because the selected edges are induced and every other edge has a zero endpoint. `det(D)=-1`, nonzero in **every** field, so `rank_K(D^(tensor r))=2^r`. Restricting to a submatrix cannot increase rank, giving the bound on `M_{A,B}`. Bounded degree gives `|E|<=dn/2`, so `F_G` has linear encoding size up to variable identifier logarithms, a linear circuit, and an obvious satisfying assignment. QED.

The proof applies to **all** balanced partitions, rather than a single prescribed cut, and is robust under arbitrary invertible *separate* changes of basis on the row and column spaces: `rank(PMQ)=rank(M)`. It does **not** claim rank invariance under a global nonlocal reshaping, reduction to an alternative computational object, or arbitrary circuit rewiring. It also does not prove any lower bound for unbounded-size read-once branching programs without a specified order or for circuit SAT on variable-encoded input.

**A direct DISJ sanity check:** `DISJ_k(x,y)=AND_i((NOT x_i) OR (NOT y_i))` has exact cross-matrix `D^(tensor k)` and rank `2^k` over every field, while its circuit is linear. Our expander family deliberately upgrades this trap to all balanced cuts, showing that **even all-cut rank alone still fails** as an unrestricted lower-bound proxy.

## 3. Independent exhaustive computation

The standalone Python executable `experiments/tmr/tmr5_expander_multicut046.py` enumerates every partition with both sides of size at least `n/3`, once up to complement, forms each complete 0/1 evaluation matrix from source graph edges, performs independent GF(2) Gaussian row reduction, greedily finds an induced cut matching, and checks `rank >= 2^r` separately at every partition. This tests *actual matrices*, not a substituted closed-form rank. It uses no randomness or external library.

| Graph | n | Audited balanced cuts | Min rank over GF(2) | Max rank | Failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cycle `C_6` | 6 | 25 | 3 | 5 | 0 |
| Cube `Q_3` | 8 | 91 | 4 | 7 | 0 |
| Petersen graph | 10 | 336 | 6 | 12 | 0 |
| **Total** | | **452** | | | **0** |

All 452 cuts passed matching-rank tests. These finite examples are not asymptotic expander-family verification. The symbolic theorem is independent of the experiment; the code is a finite implementation and regression control.

Reproducer and immutable raw result:
- `experiments/tmr/tmr5_expander_multicut046.py`
- `results/raw/tmr/2026-11-15_1100_TMR5_EXPANDER_MULTICUT046_PY_RAW.json`

Execution: local CPython standalone, exhaustive, seed not applicable, zero failures. Input graphs were deterministically generated. The finite test does not measure the physical time/space of solving general 3-SAT and is not a native FLMV or Turing-machine lower-bound experiment.

## 4. Independent audits of TMR-1/2/3/4 and Allender integration

**TMR-1/049, exact balanced unique extensions: PASS/RESTRICTED.** For each outer assignment, the claimed count `H=2^(k+m)-2^(k-1)+S` follows by direct disjoint-selector enumeration with one uniquely determined auxiliary extension on accepted inner assignments. Inclusive ties `S=2^(k-1)` map to `H=2^(k+m)` exactly. This is an interface identity, not a MajMajSAT-to-SAT compiler.

**TMR-2/049, guarded-CNF realization: PASS/RESTRICTED.** Guarding each original gate-definition clause by selector `t` makes the `t=0` branch functional, while `t=1` leaves one long calibration clause. Its counted extension formula matches TMR-1's after selector reversal; both `SAT(G_C)` and `SAT(NOT G_C)` are trivially YES from the explicitly constructed branches. The direct existential SAT queries cannot convey a majority bit. Uncharged subsequent 3CNF Tseitin variables are an invalid threshold-preservation step.

**TMR-3/049, one-query virtual classical bridge: PASS/CONDITIONAL at its stated scope.** Simulating the bounded-error algebraic-amplitude quantum SAT algorithm *before* deterministic virtual access generates a classical unbounded-error probabilistic SAT procedure. Exactly one total deterministic oracle query, followed by constant/identity/negation, preserves the probability sign. If a uniform exact compiler actually exists, its charged resource exponents satisfy `theta=max(r,a*t+h)`, `eta=max(u,a*s)` up to polylogs. A strict simultaneous forbidden-box contradiction would exclude the **joint hypotheses**, not yield an arbitrary SAT lower bound. Multi-query weak-sign composition remains FAIL without a new error theorem. A genuine reverse compiler is OPEN.

**TMR-4/050, stochastic SCC quotient: PASS/RESTRICTED.** Weighted representative-independent row lumpability and terminal-label agreement make the exact accepted-path count `e_A0 product_t(M_t) f` by induction over actual coin strings. This is the natural-number path semiring, not Boolean reachability. Its exact 2-coin clock tariff applies only to its declared sampling authority, not to computing the threshold of a general MajMajSAT source. No abstract-to-concrete threshold reconstruction or SAT tariff is provided.

**Consequence for our new Track A:** all four Allender integrations survive as scoped statements, but none supplies the missing implication from exponential evaluation rank, all-cut geometry or nested majority counts to unrestricted physical SAT decision time. The easy Horn expander family is an authentic cheap countercontrol against that implication.

## 5. The four mandatory transfer gates and ranked dependencies

| Rank | Dependency or proposed transfer | Verdict | Precise reason |
| ---: | --- | --- | --- |
| 1 | Expander edge expansion -> every balanced cut has an induced crossing matching | **PASS/RESTRICTED** | Greedy `2d(d+1)` charging proof |
| 2 | Induced matching -> all-field exponential evaluation-matrix rank | **PASS/RESTRICTED** | `D^(tensor r)` minor, determinant `-1` |
| 3 | `F_G` source has short circuit and fast SAT witness | **PASS/RESTRICTED** | `0^n` and `O(|E|)` NAND/AND circuit |
| 4 | Exponential rank at every balanced cut -> general circuit or SAT runtime lower bound | **FAIL** | Same `F_G` is Horn/2CNF and trivially satisfiable |
| 5 | Full 452-cut finite rank test for C6/Q3/Petersen | **COMPUTATIONAL** | Actual GF(2) enumeration; no asymptotic inference |
| 6 | TMR-1/049 and TMR-2/049 exact nested majority identities | **PASS/RESTRICTED** | Direct independent algebraic reconstruction |
| 7 | TMR-3/049 one-query quantum/classical conditional resource ledger | **PASS/CONDITIONAL** | Reconstructed argument; uniform exact compiler absent |
| 8 | TMR-4/050 weighted lumping and finite sampler clock | **PASS/RESTRICTED** | Path-multiplicity induction; threshold machine absent |
| 9 | Exponential multicut rank corrected by a proved unrestricted dynamic fan-out penalty | **OPEN** | Must survive this exact expander Horn control and sharing |
| 10 | Track B sub-square-root tree evaluation with charged runtime and all interfaces | **OPEN** | No height-sensitive evaluator or same-realization simulation proved |
| 11 | Track C #SAT/Circuit-SAT algorithm -> quantitative general lower-bound target | **OPEN** | Circuit-to-CNF gates/wires and target-class hypotheses unresolved |
| 12 | Allender lower bound -> small-space MajMajSAT-to-SAT compiler, or superpolynomial SAT potential | **OPEN** | Correct reduction direction and resource gate not closed |
| 13 | P versus NP separation | **OPEN** | No unrestricted same-machine lower bound |

**Gate 1: DISJ sanity = PASS as falsification.** DISJ itself is a 2CNF with rank `2^k` across its standard bipartition and a linear circuit. This report strengthens the negative lesson to every balanced cut on bounded-degree expanding graphs.

**Gate 2: Relativization = NOT AN UNRESTRICTED-SEPARATION CLAIM.** The finite graph, cut and rank proof is purely algebraic, and such a property may be proved in oracle worlds as well. Any proposed P-vs-NP conclusion based only on a fully relativizing chain would confront Baker–Gill–Solovay [5]; identify the nonrelativizing step before claiming an unrestricted separation. Algebrization and Natural Proofs need future audit if a general circuit property is proposed.

**Gate 3: Simultaneous DTISP = OPEN for any future SAT transfer / NOT APPLICABLE to theorem 046A.** No concrete one-machine time and space pair is placed in an FLMV or Allender forbidden region. Per-processor space, branching-program evaluation width and model-specific streaming memory are not an aggregate same-machine complexity ledger. The known MajMajSAT exclusion fixes `0<sigma<1`, with an unknown positive `gamma(sigma)`; fixed superlinear exponent is still polynomial, and the bounded-error quantum simulation [3,4] carries constructibility/amplitude requirements.

**Gate 4: Deterministic configuration counting = NOT A LOWER-BOUND SOURCE.** For a fixed finite-control deterministic total decider with read-only input length `N`, constant work tapes and writable space `s(N)`, its complete configurations number at most `2^O(s(N)+log N)`. An always-halting run cannot revisit a complete configuration, so `T(N)<=2^O(s(N)+log N)`. This is an **upper bound** on runtime given space, not a compelled slow computation. It does not apply without modification to probabilistic expected-time or quantum machines.

**Fusion tariff guard:** A matrix-rank coordinate that remains large on this simple Horn input but claims a superpolynomial initial resource charge would violate the actual polynomial-time witness execution. Correct zero-cost SCC quotient and every legal compact-circuit / source-recognition operation must be included. No proposed vector weight or free SCC exclusion has overcome this shortcut. Historical `/341` remains **FAIL** as a full logical UNSAT authority, and `/386` **RESTRICTED**.

## 6. Literature, corpus and novelty boundary

Primary sources: [1] Reingold, Vadhan, Wigderson, *Entropy Waves, the Zig-Zag Graph Product, and New Constant-Degree Expanders*, Annals of Mathematics 155 (2002), https://annals.math.princeton.edu/2002/155-1/p04 . [2] Bova and Slivovsky, *On Compiling Structured CNFs to OBDDs*, SAT 2016, https://pubmed.ncbi.nlm.nih.gov/32025195/ , relevant prior rank/representation barrier; no claim of priority over established expander/OBDD results. [3] Allender et al., *Time-Space Tradeoffs in the Counting Hierarchy*, CCC 2001, https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf , Theorem 7. [4] van Melkebeek and Watson, *Time-Space Efficient Simulations of Quantum Computations*, Theory of Computing 8 (2012), https://theoryofcomputing.org/articles/v008a001/ . [5] Baker, Gill and Solovay, *Relativizations of the P =? NP Question*, SIAM J Comput 4 (1975), https://doi.org/10.1137/0204037 .

Previously established project warnings overlap this control: LSPV-3/GATE323 proved a connected high-cut-rank yet easy SAT family; LSPV-2/495 showed connected expander odd-charge Tseitin sources with GF(2) upper shortcuts under alternative model, and TMR-5/037-039 constructed exponential rank / compact circuit and fusion counterexamples. **Distinct increment here**: an explicit all-balanced-cut, all-field rank theorem on a simple Horn graph family, with an exhaustive small-graph cut audit. This strengthens a falsifier, not P != NP. Relevant originals read via current repository GitHub and issue #3. TMR-1/049, TMR-2/049, TMR-3/049, TMR-4/050 reports and all five current handoffs reviewed.

**Repository limits:** Root proof1.txt retrieved with SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; the connector returned only metadata/empty text for oversized root proof2.txt (`930c5eeddafce656717f28055a7a9a755f44737c`) and root main.tex (`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`). Older peer runs report verified complete reads, but this execution does **not** claim independently recovered their full current contents. No shared root file write attempted. Local preflight and repository-wide test suite were not run; the standalone independent Python enumerator was run. No machine lower bound or unknown numerical gamma has been inferred.

**TRACKERS REVIEWED AT AVAILABLE CURRENT CONTENT/METADATA; NO MATERIAL CHANGE.** No updates to root proof1.txt, proof2.txt or canonical main.tex; no schedule or ownership mutation.

## 7. Strongest surviving next lemma / peer repair

A *candidate* usable dynamic multicut invariant must be shown small on **all** of: (i) the linear Horn expander family above, despite all-cut exponential rank, (ii) DISJ, (iii) affine/Tseitin with Gaussian elimination, (iv) compact shared gate circuits, and (v) reencoded/extension-variable versions. Then prove an operation-by-operation, **fusion-safe** inequality for each paid operation of a specified circuit, branching-program or machine model. Only afterwards attempt to derive a large initial charge on genuinely hard formulas and an explicit representation-independent **same-machine transfer** to unrestricted SAT. TMR-2 owns Track A's quotient refinement; TMR-4 should attempt the circuit-to-cut transformer; TMR-3 should keep Tree Evaluation's actual time-space overhead; TMR-1 should verify any Track C algorithm-to-lower-bound theorem's class and quantitative hypotheses. TMR-5 to red-team the next proposed invariant on this authenticated all-cut Horn control.

P versus NP remains **OPEN**.
