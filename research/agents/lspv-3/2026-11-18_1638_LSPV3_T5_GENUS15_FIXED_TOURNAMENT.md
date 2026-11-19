# LSPV-3 / T5-CRIT-GENUS15: linear cycle rank, SAT-deletion genus, and fixed-template planar exclusion

**Date:** 2026-11-18 16:38 PST. **Role:** Historical LSPV-3 Hypergraph & Proof Certificates. **Status:** PROVED/RESTRICTED mathematical deductions from WTHREAD-1B and primary published graph theory; COMPUTATIONAL independent H33 replay; same-system SAT-witness time lower bound OPEN. **P versus NP OPEN.**

## Candidate and falsifiers before search

**Candidate:** the local weighted-five critical-thread condition implies a linear, rather than square-root, lower bound on the cycle rank of every edge-minimal T5-UNSAT source of girth at least seven. Combining this with Euler's formula produces a linear-genus obstruction not only for critical H but for every designated SAT deletion H-e. The August 2026 antisymmetric-Z5-flow theorem further excludes planar H of girth at least ten for this *specific* T5, not merely an unspecified five-vertex tournament.

**Falsifiers:** (F1) a length-four constrained degree-two thread or a vertex with weighted incident degree below five; (F2) an invalid count-once relation among branch edges, source vertices, and cyclomatic rank; (F3) a face boundary of length below source girth in an applicable two-connected cellular embedding, or an edge addition needing more than one handle; (F4) a Z5 antisymmetric value set that cannot be globally normalized to the specific difference set {1,3}. All four were checked algebraically. Computational checks do not establish unrestricted witness complexity.

## Exact model and source

Fix colors Z5 and each original oriented arc u->v requires c(v)-c(u) in {1,3} mod5. H is finite simple, loopless, connected, edge-minimal UNSAT, with ordinary **undirected** girth g>=7; e is any designated original arc; G=H-e is promised SAT. Set n=|V(H)|, m=|E(H)|, beta=m-n+1. No SAT/UNSAT oracle, promised criticalization compiler, or runtime lower bound is assumed. The previous certified short-thread and weighted-degree results are explicit antecedents, not rediscovered claims.

## Theorem T5-GENUS15-A: linear necessary cycle rank (PROVED/RESTRICTED)

Let b count branch vertices (original undirected degree at least three), and let e_i count maximal degree-two threads of length i=1,2,3. Let q=e_1+e_2+e_3 be the number of core edges. Every edge-minimal UNSAT H as above satisfies

```
beta = q-b+1,
n = b+e_2+2e_3,
m = e_1+2e_2+3e_3,
2(3e_1+2e_2+e_3) >= 5b,
q >= 3b/2.
```

Consequently
```
n <= (3/2)b + 3(beta-1),
b <= 2(beta-1),
n <= 6(beta-1),
m <= 7(beta-1).
```

In particular **beta(H) >= n/6+1 and beta(H) >= m/7+1**, a linear improvement over the earlier general square-root structural lower bound. For a designated deletion G=H-e, beta(G)=beta(H)-1>=n/6. These are necessary source-structure bounds, **not time or memory lower bounds**.

**Proof.** Each length-i thread forbids 4-i terminal colors, so the independent weighted-five minimum condition gives 2 sum_i (4-i)e_i >=5b. Algebraically sum_i(4-i)e_i = 3q-(n-b) =4b+3(beta-1)-n. Rearranging yields n <=1.5b+3(beta-1). Every branch has core degree >=3, so 2q>=3b and beta=q-b+1>=b/2+1, giving b<=2(beta-1). Substitute into the n bound. Finally m=n+beta-1. QED.

## Theorem T5-GENUS15-B: high-girth critical SAT deletions have linearly growing orientable genus (PROVED/RESTRICTED)

Let gamma(X) be the minimum orientable genus of the underlying undirected graph X. If g>=15, then
```
gamma(H) >= 1 + ((g-14)/(2g))*(beta(H)-1)
         >= 1 + ((g-14)/(12g))*n,
gamma(G) >= ((g-14)/(2g))*beta(G)
         >= ((g-14)/(12g))*n.
```
Since genus is integral, gamma(H)>=2 and gamma(G)>=1 at g>=15. Uniformly for all g>=15, gamma(G)>=n/180 (integer-rounded upward). Thus **every** promised edge deletion is nonplanar for g>=15; any growing-size intrinsic-critical family of such girth has genus Omega(n). A fixed-genus source family cannot realize arbitrarily large instances in this regime.

**Proof.** An edge-minimal UNSAT graph is 2-vertex-connected: every block separately satisfiable could be glued by the fivefold T5 rotation symmetry, and an unsatisfiable block would violate edge minimality outside it. For an orientable cellular embedding of H of genus gamma(H), each face boundary walk has length at least its undirected girth g. Euler gives f=beta+1-2gamma(H) and 2m>=gf, so gamma(H)>=(beta+1)/2-m/g. Theorem A yields m<=7(beta-1), hence gamma(H)>=1+(beta-1)(1/2-7/g). Add a single edge e to an embedding of G through at most one new orientable handle, giving gamma(H)<=gamma(G)+1. Therefore gamma(G)>=gamma(H)-1. Since beta(G)=beta(H)-1>=n/6, the inequalities follow. All costs here are topological, not computational. QED.

**Sample symbolic consequences.** For source girth g>=15, no genus-zero or genus-one critical H exists; any SAT deletion has gamma(G)>=ceil(n/180). For g>=19, the coefficient improves to 5/228 in the n bound. Higher girth raises the linear coefficient toward 1/12. A Moore-bound lower bound on b may be combined separately, but does not imply slow search.

## Theorem T5-GENUS15-C: exact fixed-T5 planar girth exclusion (KNOWN 2026 theorem + PROVED normalization)

Cranston, Li, Su, Wang, and Wei, *Orientations of 10-Edge-Connected Planar Multigraphs and Applications*, Journal of Graph Theory (first published 2026-08-19), DOI 10.1002/jgt.70115, arXiv:2603.24292v2, prove Theorem 1.3: every directed 10-edge-connected planar graph admits an antisymmetric Z5 flow; by planar duality, every orientation of a planar graph of ordinary girth at least ten has a homomorphism to a directed simple graph of order at most five. Their Definition/Section 1.1 specifies that an antisymmetric Z5-flow has no zero values and cannot use both x and -x globally.

**Fixed-template identification.** All used flow values lie in one set S containing at most one of {1,4} and at most one of {2,3}. Extend S to one of four two-element sets. Every such set has a global invertible multiplier carrying it to our required {1,3}:
```
S={1,2} -> multiplier 3
S={1,3} -> multiplier 1
S={2,4} -> multiplier 4
S={3,4} -> multiplier 2.
```
The planar-dual potential c:V(H)->Z5 has every oriented edge difference in S (up to a global conventional sign, absorbed in the multiplier). Multiplying all c by the indicated scalar gives a valid assignment of this exact fixed T5. For 2-connected H the duality applies directly; general planar graphs may be processed blockwise with translation to glue articulation colors.

**Corollary:** There is **no planar edge-minimal T5-UNSAT H with undirected girth >=10**. This is stronger than the generic five-color oriented-chromatic statement if one establishes the displayed antisymmetric-value normalization; it corrects the open firewall in the 16:24 LSPV-2 report. It is a structural exclusion, not an efficient constructive coloring algorithm or promise-hardness theorem. Ask the independent red team to verify the dual edge orientation/sign convention in the full primary paper.

## Independent computational replay

The pinned original H33 source `research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5` had SHA256 `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`, independently checked from exact ASCII bytes before parsing. A fresh standard-library arc-consistency/DFS replayer found:

- n=33, m=44, undirected girth=8, beta=12, 2-vertex-connected, branch b=19, q=30, thread histogram {1:20,2:6,3:4}, weighted minimum=5.
- H33 genuinely UNSAT, in 197 DFS nodes under a different search order; **44/44 deleted-arc sources SAT**, each with original-label model and every retained arc verified. Every missing arc is false in its corresponding model; maximum 331 DFS nodes. The search-node count is an implementation-dependent diagnostic, not a lower bound.
- All nine short-thread relations and all 512 support subfamilies re-enumerated; maximum irredundant size four. All 4-edge paths have universal endpoint support.
- H33 cannot be planar: 44 original edges exceed the planar girth-eight upper bound 8(33-2)/6 = 41 1/3. An independent NetworkX planarity cross-check returned FALSE. All 44 H33 deletions also independently returned nonplanar in NetworkX. This girth-eight source does not test the g>=15 asymptotic theorem.

Executed full script SHA256 `0956f8774006d56a629ef608e9d5db04c55bfcf416fb3596cfa74ac4df71b42f`; executed detailed deletion/witness raw JSON SHA256 `d905eda33df99ab4c297f99f6d7061d616626b1bfbbfa35d6a48611f7d16744b`. The complete script/raw were retained in the local conversation runtime, not automatically present in GitHub. No previous /mnt/data branch-core archive was mounted; the pinned GitHub source and prior original reports were recovered instead.

## Application and remaining blocker

The new linear-beta/genus theorem **restricts what a high-girth intrinsically critical SAT-deletion family can look like**. In particular, planar construction templates are impossible from girth ten onward; at girth fifteen every SAT deletion itself has positive genus, growing linearly in size. This does NOT lower-bound the time required for witness finding: source-aware GF(5) binary cycle equations, separator/treewidth DP, full-color output algorithms, graph recognizers, compact circuit representations, and alternate search order are all still legal.

No known fixed-girth NP-completeness theorem supplies a polynomial-time reduction to the **growing-girth, already-critical, designated SAT-deletion witness promise**. Criticalization may require UNSAT decisions and a witness decoder must be uniformly source bound. The primary next target is a uniform polynomial witness algorithm or a reduction proving promise-hardness without a free criticalization oracle. Separately request LSPV-2/5 independent review of the exact dual-flow-to-fixed-T5 normalization and the Euler genus transfer. P versus NP remains OPEN.

**Publication/ownership:** Historical LSPV-3 report only; do not edit live TMR manuscripts or legacy proof trackers. Existing agent identities, schedules, paused state remain unchanged. No standalone marker of machine lower-bound proof is promoted.
