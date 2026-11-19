# Strict-C critical graph run: Paley17 witness core and LPS spectral resilience

2026-11-19 PT. **PROVED** spectral monochromatic-edge lower bound and Hajós witness transport; **COMPUTATIONALLY VERIFIED** 17-vertex physically critical source and 919 original-C deletion witnesses; **CONDITIONAL** LPS q=89,257 figures on published Ramanujan source theorem and prior local-girth verification. P versus NP remains OPEN.

## Spectral theorem and obstruction-cover consequence

Let G be n-vertex d-regular with adjacency spectrum on 1-perpendicular bounded below by -lambda. For **every** assignment z:V(G)->[k], the number of monochromatic edges satisfies

```
M(z) >= n*(d-(k-1)*lambda)/(2*k).
```

**Proof:** For each color-class vector x_i, split x_i=(n_i/n)*1+y_i, y_i orthogonal to 1. Then x_i^T A x_i >= (d+lambda)n_i^2/n-lambda*n_i. Sum and use sum n_i^2>=n^2/k; 2M=sum x_i^T A x_i. This charges no path or polarity advice. Every monochromatic edge e forces a refutable source-original clause C(h_e,u_e,v_e) for **all five** private-head values. An edge partition into blocks of <=s private heads therefore contains at least ceil(M_min/s) refutable blocks for every z. A source-verified spectral inequality can certify a *global symbolic* cover, but is not a free, unrestricted SAT decision procedure.

For the nonbipartite p=73, d=74 LPS Ramanujan graphs [1], lambda=2sqrt(73). Their exact universal lower bound for k=5 is ceil(n*(74-8sqrt(73))/10):

| q | graph vertices | C clauses | C variables | min violated C clauses for EVERY z | edges deletable while UNSAT is guaranteed | incidence girth from prior agent |
|---|---:|---:|---:|---:|---:|---:|
| 89 | 352440 | 13040280 | 13392720 | 199058 | 199057 | 10 |
| 257 | 8487168 | 314025216 | 322512384 | 4793528 | 4793527 | 12 |

In particular **no original LPS C clause is individually indispensable**, and any edge-minimal non-5-colorable subgraph must remove at least M_min-1 original edges (because deleting one more retained edge leaves a 5-colorable graph). The LPS graphs are large *noncritical* UNSAT controls. Previous local cycle checks, not this run, established their girths. Full materialization/verification is still charged. For block size floor(N^.35), every z must refute >=639 of 41796 q89 blocks or >=5046 of 330553 q257 blocks. All original graph vertices remain shared, so an explicit N^.195-row enumeration is impossible.

## NEW small fully certified physical-C critical control

Construct the Paley graph P(29) on F29: a,b adjacent iff b-a is a nonzero square modulo29. P29 has 29 vertices, 203 edges, degree14, graph girth3. Exhaustively reject all binomial(29,5)=118755 independent 5-subsets and exhibit an independent 4-set: alpha(P29)=4. Thus every five-coloring incurs at least 29-5*4=9 monochromatic edges by a one-endpoint-per-monochromatic-edge vertex deletion argument. The Paley eigenvalues give a weaker >=4 spectral guarantee [2].

Lexically test deletion of every edge using a complete DSATUR five-color decision; delete edges that leave UNSAT and retain an actual five-color deletion witness for all others. The resulting **17-vertex, 62-edge, K5-free, 6-edge-critical** graph has 63 triangles and degree >=5. Its graph6 string (vertices 12..28 remapped to 0..16) is:

```
PumPAdyTpveCITHTafhH_JGs
```

An independent exact DP over independent-set color classes proved non-5-colorability in 11764 memo states. Every one of the 62 physical original strict C clauses, using a fresh head and distinct names per clause, has a complete 79-variable deletion assignment with the deleted clause FALSE and all 61 retained clauses TRUE. The independent replay made 3782 true and 62 false original-C checks. Extraction charged **267 complete five-color calls and 10933 DSATUR search nodes** including the initial source, 203 failed/successful edge deletion candidates, final UNSAT call and all 62 independent repeat SAT checks. No oracle or supplied correct path.

## Smaller infinite source-critical family

Balanced Hajós joins of t copies of the 17-vertex graph preserve 6-chromaticity, edge-criticality, complete deletion witnesses, and K5-freeness. A join identifies one selected-edge endpoint from each child, deletes both selected edges, and adds the bridge between their other endpoints. Induction constructs all new deletion colorings from the child colorings; recoloring a child by any color permutation aligns identified roots. Private heads are assigned completing values for all unequal endpoints.

For t copies graph vertices=16t+1, edges=61t+1; physical C variables=77t+2, clauses=61t+1. The bridge is not in a triangle; existing triangles survive, hence graph girth3/C incidence girth6, **not growing**.

| t | C variables | C clauses | verified original-C deletion witnesses | replayed C checks |
|---:|---:|---:|---:|---:|
| 1 | 79 | 62 | 62 | 3844 |
| 2 | 156 | 123 | 123 | 15129 |
| 4 | 310 | 245 | 245 | 60025 |
| 8 | 618 | 489 | 489 | 239121 |
| **Total** | | | **919** | **318119** |

Independent replay uses the GF(5) quadratic identity (a-b)^2+(b-c)^2+(c-a)^2==1 mod5, independently confirmed for all 125 tuples against the canonical R/C predicate. Original source, head-candidate enumeration, C check, complete output and both solver polarities must be accounted. Family generation is bounded-width/source recognizable and gives NO general hardness result. Explicit full witness output for t=1,2,4,8 comprises 402238 C-variable color values; archive carries compact graph-color witnesses with deterministic private-head expansion.

## Source evidence and unresolved questions

Reproduction package in the conversation: `T5C_Paley17_LPS_Spectral_Critical_20261119.zip`. Commands: `python3 verify.py --out results.json`; `python3 extract_critical.py`; `python3 independent_replay.py`; `python3 hajos_paley.py`; `python3 replay_family.py`. Clean-room unzip and independent replay passed. Deterministic candidate-shake seed 2026111905 found 13 equal edges on P29, without claiming optimality. Key source SHA256: 17-graph6 `d1dbbc95553d9fe49e1edd1afdcc40daf4bd21c473a42244a36aee7d362276f0`; critical C ledger `d51a02e7bd602483bfc209795271dad3a5d0b99b73063079304fb14b0d7bf57e`; Hajós family `f62ed1f1d315876b672a0afcac34e643b04eac4bcf684eaab4bfeda2b1496361`.

**OPEN:** growing-incidence-girth edge-critical C family with physically verified deletion ledger. LPS is high girth but quantitatively noncritical; Paley-Hajós is critical but constant girth. Nothing here proves an unrestricted superpolynomial lower bound, the N^.195 explicit-row layout, a RAM N^1.33/sqrt N algorithm, or P != NP. Independent discovery and verification remain charged.

References: [1] Lubotzky, Phillips, Sarnak, Ramanujan Graphs, Combinatorica 1988, https://doi.org/10.1007/BF02126799. [2] Paley graph parameters, https://aeb.win.tue.nl/graphs/Paley.html. [3] Exoo-Goedgebeur girth/chromatic bounds, DMTCS 2019, https://doi.org/10.23638/DMTCS-21-3-9. Prior repository reports `2026-11-19_LPS73_GIRTH_SOURCE_K6_LIFT_FALSIFIER.md` and `2026-11-19_HAJOS_CRITICAL_WITNESS_WIDTH_FIREWALL.md` were fetched/read. User library `t5_strict_research.pdf` pages 1-8 was read; ZIP was not recovered. No agent schedule/manuscript ownership changes.
