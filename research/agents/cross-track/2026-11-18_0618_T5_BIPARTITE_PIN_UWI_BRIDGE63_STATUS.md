# CROSS-TRACK SYNTHESIS 63 | T5 BIPARTITE RELATIVE PINNING
**2026-11-18 06:18 PST. Status:** RESTRICTED EXACT/CONDITIONAL. Independent review OPEN. **P vs NP OPEN.**

## Proposals frozen in the run before retrieval
(1) Fully charged T5 relative-pinning self-reduction preserving the BIPARTITE promise, hostile-checking the #62 triangle gadget. (2) Canonical 25-to-5 one-hot Resolution restriction, without arbitrary-decider transport. (3) Contrast high-girth orientation-blind low-order moments and exact dual-Fourier/frontier contractions against unrestricted source access. (4) Require a genuinely necessary nonrelativizing WRAPPER hinge and correct same-input UWI clock. This report records the proposals; no prior external timestamped pre-search commit is asserted.

## Latest specialist sources read
- **Resource Contraction:** [TMR-3/084 PR 276](https://github.com/j15marti/pnp/pull/276), exact T5 dual-frequency elimination, source-charged upper bounds T=O((N+1)^14 5^(2(w+1))), S=O((N+1)^6 5^(w+1)) bits, BFS vs DFS width 99 vs 1 on a 100-triangle chain. No unrestricted lower bound.
- **Nonrelativizing Simulation:** [LSPV-5 KOOPMON1 commit 7cceaa8](https://github.com/j15marti/pnp/commit/7cceaa86876d6ea3adbb5807d25c6c9abca8e66f), restricted source-authenticated nonlinear monomial closure certificate, and exponential monomial closure with cheap factored evaluator. No necessary nonrelativizing hinge.
- **Universal Obstruction:** [TMR-2/083](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_0507_TMR2_T5_REGULAR_GIRTH_MOMENTS083.md), 5-regular growing-girth YES/random-NO same-skeleton sources, and exact forest subinstance counts 5^(n-k)2^k for k<g. Query scope only, not machine time.
- **Proof Transport:** [TMR-4/087 PR 277](https://github.com/j15marti/pnp/pull/277), source-certified complete-query T5 OBDD upper bound 10^b+1 for a fixed touched-future frontier b; 4-connected high-cycle-rank yet source-cheap counterexample. Canonical Resolution proof restriction from #61 is encoding specific.
- Project history from cross-track #61/#62, Library and Google Drive NONALG-0003 (historical PFCERT space-state gate) was checked; no newer relevant Drive T5 report was located. Primary references: Bang-Jensen/Hell/MacGillivray 1988 DOI 10.1137/0401029, Atserias/Dalmau 2008 DOI 10.1016/j.jcss.2007.06.025.

## New theorem: every mod-5 relative offset has a constant-size *bipartite* T5 pin gadget
Let R(a,b) iff (b-a) mod5 is 1 or 3. Bipartite always means the underlying undirected graph. Fresh auxiliary vertices and genuine original T5 arcs only; no named color constants.

**Same-side terminals u,v:** Introduce a,b on the other side. Add arcs u->a->v and u->b<-v. The first length-2 path permits v-u in {1,2,4}; the second permits {0,2,3}. Their intersection is the singleton {2}. Thus 2 new vertices and 4 arcs enforce offset +2; swapping terminal roles enforces -2=3. Series-composition of at most TWO such blocks enforces every residue:
0=(+2)+(-2), 1=(-2)+(-2), 2=(+2), 3=(-2), 4=(+2)+(+2).
Cost <=5 new vertices and 8 arcs, retaining the bipartition.

**Opposite-side terminals u,v:** Install four internally disjoint 3-edge u-to-v paths with q=0,1,2,3 reverse-oriented edges respectively. A length-3 path with q reversals permits four of five offset residues and excludes exactly q+1 mod5. Intersection over q excludes {1,2,3,4}, enforcing offset 0 with 8 new vertices and 12 arcs, girth 6. For other offset d use a fresh opposite-side terminal z, enforce z-u=0 by the four paths, then v-z=d using the same-side series gadget. Maximum **14 new vertices and 20 arcs**. All gadgets remain undirected-bipartite. They do NOT preserve 5-regularity or high girth >=8.

**Theorem 63.3, conditional:** If total BIPARTITE-T5 decision is polynomial-time, BIPARTITE-T5 witness search is polynomial-time on the *identical original source*. For each original weak component, choose a root, normalize root color 0 by componentwise automorphism and adaptively pin relative offsets for each other vertex. Test d=0,1,2,3, commit the first satisfiable modified query, otherwise commit d=4. Each query remains bipartite; last committed offsets give an original verified witness. On n variables, m arcs, c weak components, calls <= 1+4(n-c), each query has <=n+14(n-c) vertices and <=m+20(n-c) arcs. Charge every parsing, component computation, source reserialization, query, simulator workspace, recursion, full original arc verification and witness output. Uniform polynomial D implies polynomial total time/space. This is a reduction, NOT a claimed fast D.

**Tree-only negative lemma:** A 2-terminal forest gadget cannot enforce a single relative offset between distinct vertices. If the terminals share a tree with path length L>=1, the set of endpoint differences has size min(L+1,5), since each signed step is baseline+{0,2}; off-path leaves independently extend. If disconnected, all five offsets extend. Thus reconvergence/cycles are necessary for such pure 2-terminal pins. This does not rule out complex high-girth nonforest pins.

## Executed hostile audit
Self-contained Python stdlib source and exact JSON results are in the accompanying local research bundle `2026-11-18_0618_T5_BIPARTITE_PIN_UWI_BRIDGE63_BUNDLE.zip`. Seed 202611180618. **16,552 assertions, 0 failures**. Checked all 510 orientation words for paths of lengths 1..8; every length-2/3 path against independent full-color enumeration; all 10 parity x offset gadgets across all 25 endpoint colors (250 cases); 40 independently enumerated original bipartite sources, 200 pin queries (38 original SAT, 2 UNSAT); and the full decision-only extractor on all 40 (311 oracle calls including 38 extra *audit-only* final check calls, peak 61 vertices/88 arcs). Verified all original witnesses. Finite checks do not imply resource lower bounds.

## Proof DAG
| Arrow | Status |
|---|---|
| T5 fixed-template homomorphism NP-complete | ESTABLISHED external |
| Exact same-side +2/-2 and opposite-side zero bipartite pins | PROVED RESTRICTED |
| All five offsets with <=14 fresh vertices, <=20 arcs | PROVED RESTRICTED |
| Bipartite T5 D in P => same-original-input witness W_D in FP | PROVED CONDITIONAL |
| Two-terminal forest gadget pins one exact offset | FALSIFIED |
| High girth 8 and five-regular promise preserved by our compiler | FALSIFIED |
| Low-order forest moments => unrestricted machine lower bound | OPEN/UNSUPPORTED |
| Indispensable nonrelativizing WRAPPER hinge | OPEN |
| Universal same-input/common-clock UWI against W_D | OPEN |
| General arbitrary-decider-to-Resolution proof transport | OPEN |
| Unrestricted T5 superpoly time lower bound; P vs NP | **OPEN** |

## Specialist handoffs
**Resource Contraction:** Fully charge each source scan, gadget generation, oracle call, peak live workspace and dual-width contraction on generated bipartite queries.
**Nonrelativizing Simulation:** Show an indispensable source-dependent WRAPPER operation that cannot be replaced by this relativizing self-reduction or polynomial factored endpoint evaluation.
**Universal Obstruction:** Quantify over one identical final bipartite YES source, common polynomial clock, and include W_D with its auxiliary bipartite queries; keep stronger 5-regular/high-girth promises distinct.
**Proof Transport:** Develop checked one-hot proof-file translations only after explicit gadget compiler; never infer general decider-to-Resolution. Compare TMR-4's cheap source-certified frontier algorithm.

This report changes no other specialist files, agents, schedules, or root proof trackers.
