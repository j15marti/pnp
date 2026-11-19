# LSPV-4 | Critical T5 SAT-witness resource audit: minimum-product spanning tree
Date: 2026-11-18, America/Los_Angeles. Historical Route A. No agent/schedule/ownership changes. P versus NP OPEN.

**Statuses:** PROVED: an exact uniform SAT-only witness algorithm, polynomial writable space, conditional same-machine work upper bound, weighted-core structural obstruction, girth-based sparsity. COMPUTATIONAL: 55 independently verified original-edge-deletion witnesses. LITERATURE-DERIVED: planar girth >=10 impossible for T5-UNSAT. OPEN: superpolynomial worst-case witness cost on growing-girth intrinsic-critical inputs; promise-preserving hardness.

## Mechanism and falsifiers
Input is the **full** encoded connected edge-minimal T5-UNSAT source H and the designated original edge e; G=H-e is SAT by promise. T5 colors are Z5, R(a,b) iff (b-a) mod 5 in {1,3}. No witness advice, SAT/UNSAT oracle, alternative grammar, free preprocessing, precomputed root label, nonuniform table or UNSAT certificate is used.

Candidate: suppress degree-two threads of H, delete the designated thread's endpoint constraint, build an intact-core spanning tree minimizing the product of its endpoint-choice counts, pin one core root to 0 under fivefold rotation, and perform exact source-aware tree backtracking while checking all non-tree threads. Reconstruct every original degree-two vertex, output all n labels and check every original arc except e.

Falsifiers: (F1) deleted-thread endpoint relation is not universally free or remaining core disconnected; (F2) wrong terminal choice counts for mixed arc orientations; (F3) a cheaper different tree, or actual search exceeds the stated bound; (F4) uncharged parsing, temporary memory, path reconstruction, output or verification. All four have exact proof obligations and independent finite controls.

## Theorem 1: uniform witness construction, proved
Every maximal degree-two thread P has 1<=L_P<=3; a path of four original arcs is unconstrained at its endpoints and contradicts edge minimality. For a fixed endpoint color, any length-L thread has **exactly L+1 permissible colors** at its other endpoint, independently of arc directions. Deletion of any original arc of P splits it into two rooted fragments and removes its *entire* core endpoint constraint. The intact branch multigraph K_e remains connected because H is 2-vertex-connected and H-e is connected.

Let B be the set of branch vertices (b=|B|), Q the set of threads (q=|Q|), and P_e the thread containing e. For any spanning tree T of K_e define
```
M_e(T) = product_{P in T} (L_P+1)
M_e = min_{T spanning K_e} M_e(T).
```
Root T at one branch color 0. At each parent-before-child assignment, explore only L_P+1 allowed child colors and check every already-closed non-tree thread. Thus at most M_e complete branch assignments and at most 2M_e-1 search states are explored: all branching factors are >=2. Every valid full coloring survives these checks, and any accepting core labeling extends independently to original thread interiors, including the two fragments of the removed edge. This is an exact SAT-witness finder, not merely a decision procedure. Kruskal with weights log(L_P+1), equivalently sorted by L_P=1,2,3, yields M_e and is *optimal only among spanning-tree product bounds*, NOT optimal among all algorithms or even all practical search orders.

M_e <= 4^(b-1). Independently, searching the original connected graph on a rooted spanning tree gives <=2^(n-1) complete candidate labelings. The best of these uniform upper controls may be selected on the full source, charging the comparison and construction.

**Full-machine accounting:** Let N be source-plus-edge-ID bit length. Parsing every byte, validating vertex IDs/edge directions/duplicates/connectivity, adjacency and thread discovery, computing 25-entry endpoint supports, Kruskal sorting, parent order, failure/backtrack checks, all live tables, reconstructing all n labels, emitting exactly 3n fixed-width color bits, and checking m-1 retained arcs are all charged. RAM operation count O(poly(N)+q M_e+n+m), with O(N log N) stored bits for source, tables, stacks and output. A deliberately conservative deterministic one-tape bit-machine implementation takes O(N^3(M_e+1)) bit steps and O(N^2) writable bits using sequential scans, bounded indices and no large integer counts. Interpreter wall time is *not* that bit-machine measure. The promise merely ensures a positive leaf exists; the exhaustive search is uniform for all encoded instances in the structural class. No superpolynomial lower bound follows.

## Theorem 2: weighted branch obstruction, proved
For each branch vertex v let w(v)=sum_{P incident v}(4-L_P), counting parallel threads separately. In every edge-minimal UNSAT H, **w(v)>=5**. Remove v and interiors of its incident threads, color that proper subgraph using edge minimality, then extend the precolored other endpoints. Each length-L thread excludes exactly 4-L of the five possible colors at v. If w(v)<=4, the excluded sets cannot cover all five colors, so a completion colors H, contradiction. Consequently 3q_1+2q_2+q_3 >= 5b/2. This is structural necessity, not a search-time lower bound.

## Theorem 3: improved girth/core sparsity, proved
If girth(H)>=10, the simple suppressed core is triangle-free because every core triangle expands to <=9 original arcs. Mantel gives q<=floor(b^2/4); since n=b+sum_P(L_P-1), **n<=b+2 floor(b^2/4)**, hence b>=sqrt(2n)-O(1). If girth(H)>=13, core squares are also impossible. Counting length-two nonbacktracking walks gives sum_v d_v(d_v-1)<=b(b-1). By Cauchy, **q <= b(1+sqrt(4b-3))/4**, hence **n<=(3b+b sqrt(4b-3))/2** and b=Omega(n^(2/3)). Neither is an unrestricted complexity lower bound.

## Primary literature: nonplanarity at girth >=10
Cranston, Li, Su, Wang, Wei, *Orientations of 10-Edge-Connected Planar Multigraphs and Applications*, Journal of Graph Theory, first published August 19, 2026, DOI [10.1002/jgt.70115](https://doi.org/10.1002/jgt.70115), full [arXiv paper](https://arxiv.org/html/2603.24292): every orientation of a planar girth>=10 graph maps to a five-vertex tournament via antisymmetric Z5-flow duality. This matches this **fixed** cyclic T5: the flow uses no zero and no pair of inverses in Z5; its at-most-two-value support can be multiplied by a common nonzero scalar to land in {1,3}, preserving dual vertex potentials. Therefore every girth>=10 T5-UNSAT H is **nonplanar**, as is its branching core. Its core has b>=6: a nonplanar simple graph with b<=5 would require K5, whose triangle could expand to length at most nine. This is an exclusion of a family, not a witness-time result or a proof of NP-hardness under the critical promise.

## Executed independent audit
A new standard-library Python solver reconstructs exact original bytes, enumerates endpoint supports independently of the prior AD formula, computes a fresh minimum-product tree **for every designated original arc**, backtracks, emits all original labels, and checks all retained arcs and all five color rotations. No earlier model counts or stored witnesses are used as input.

| Source | n,m,girth | b,q | M_e range | Maximum attempted branch candidates | Total attempted candidates | Original-witness tests |
|---|---|---|---|---|---|---|
| Four-thread theta | 9,11,5 | 2,4 | 3 to 4 | 3 | 20 | 11/11 |
| Original TMR-2/079 | 33,44,8 | 19,30 | 262144 to 524288 | 16855 | 137844 | 44/44 |

The 33-vertex canonical source is SHA256 `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac` and 493 ASCII bytes. It has q1/q2/q3=20/6/4 and minimum weighted branch degree 5; 40/44 deletions admit a Kruskal tree consisting entirely of 18 length-one threads. The maximum-weight spanning-tree *product bound* can be 47,775,744, versus a minimum of 262,144 (182.25x), without implying a speed ratio for actual solvers. Observed Python batch search: 0.001 seconds (9 vertices) and 0.149 seconds (33 vertices), platform/interpreter-specific.

Independent NetworkX planarity checks: nine-vertex source planar with girth 5; 33-vertex source nonplanar with girth 8, with the returned nonplanar subgraph checked independently. The original source's critical UNSAT status is inherited from the prior all-deletions exact counting auditor and is NOT independently proved by current SAT-only witness verification. No exhaustive 5^33 search, low-level physical memory trace or actual increasing-girth critical family was performed.

**Reproducibility files generated in conversation working directory:** `T5_RESOURCE_MST_REPORT_20261118.md`, `t5_resource_mst_audit_20261118.py`, `T5_RESOURCE_MST_RAW_20261118.json`, `t5_resource_mst_planarity_audit_20261118.py`, `T5_RESOURCE_MST_PLANARITY_RAW_20261118.json`, and `T5_RESOURCE_MST_HANDOFF_20261118.md`. These executable/raw files are not yet GitHub-committed.

**Next blocker:** an increasing-girth, source-authenticated, intrinsically critical UNSAT family and a promise-preserving complexity reduction, plus GF(5)/flow/DP/circuit attempts to falsify any supposed witness-work lower bound. Even a superpolynomial M_e is only an upper bound for this chosen algorithm. Preserve all five current roles' titles, schedules, ownership and activation states; no root manuscript or proof trackers modified. **P versus NP OPEN.**
