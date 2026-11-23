# HCL-DISTRIBUTED-ODDWHEEL-1: paid equality-gadget quotient of an expander-blown wheel

2026-11-23 11:57 PST (America/Los_Angeles). Constructive meta-algorithm; issue #324.
Status: PROVED restricted structural and constructive theorem; COMPUTATIONALLY CHECKED finite controls; independent review pending. P vs NP OPEN.

## 1. Research question and peer dependencies
This run follows the T5 2026-11-21 handoff, issue #324, Meta Solver Theorem's 11:35 signed-conflict matching-backdoor report, Decomposition Obstructions' 11:25 expander-integer-blind residual, Sigma Redteam's 2026-11-18 odd-wheel source-reading frontier repair, and Critical Graphs' 2026-11-19 Hajós width firewall. The objective is a *paid* constructive interface: can an apparently globally coupled nonaffine odd wheel be recognized and compressed by sound local projections before SCC, matching, rational nullity, and raw treewidth give poor proxy bounds?

## 2. Construction (all quantities exact)
Let H=(U,E_H) be ANY connected simple cubic graph with n=|U| even, n>=6, e=3n/2. Create one hub-clone h_i per i in U, a rim v_0,...,v_{r-1} with r=n-1 (odd), rim edges v_i-v_(i+1 mod r), and spokes h_i-v_i for i<r. For every uv in E_H, add distinct private vertices c_uv,d_uv with EXACTLY five edges:
  h_u-c_uv, h_u-d_uv, h_v-c_uv, h_v-d_uv, c_uv-d_uv.
There is no edge h_u-h_v. Name resulting graph G(H). Use ordinary proper graph 3-coloring encoded as proper 3-CNF: for every graph vertex z add (z0 OR z1 OR z2) and three pairwise-negative binary clauses; for every graph edge zw add three clauses (NOT zc OR NOT wc), c=0,1,2. All positive groups have exactly 3 distinct variables. A fixed number of linear-size, syntactically checkable source labels is not necessary if the parser first recovers color frames and verifies the whole canonical source.

Graph vertices V=n+r+2e=5n-1, edges E=2r+5e=(19n/2)-2. Boolean variables Q=3V=15n-3, CNF clauses M=4V+3E=(97n/2)-10. Explicit binary input length N=Theta(n log n). At the syntactically recognized exact-one stage, rank of the V vertex equations is V, so raw rational nullity Q-V=2V=10n-2. The **unaugmented** signed-B conflict graph has one option group per graph vertex; the three color options form three copies of G(H), since the purely negative binary B has no other cross-group entailments.

## 3. Main lemma: private diamond projection
For a private four-vertex diamond D with tips a,b and internal vertices c,d, whose five edges are ac,ad,bc,bd,cd and whose c,d occur nowhere else, the existential projection over proper 3-colorings satisfies

   exists colors(c),colors(d) [D(a,b,c,d)]  <=>  color(a)=color(b).

Proof: c,d are adjacent and thus use two distinct colors; a and b are adjacent to BOTH, so each must use the unique remaining third color. Conversely when a=b=k, c and d can take the other two colors in either order, giving EXACTLY TWO extensions. When a!=b no extension exists. All nine ordered tip-color pairs were exhaustively evaluated, yielding 2 on the three diagonals and 0 off-diagonal.

Because all internal pairs are private, the diamond projections commute under existential quantification, even when multiple diamonds share tips. A proof-producing quotient replaces each diamond by equality of its tips; union-find then identifies every h_i since H is connected. The residual graph is precisely W_r, an odd wheel. Fixing the identified hub color leaves two colors on the rim; rim edges require alternation, impossible on an odd cycle. Thus G(H) is NOT 3-colorable, and its full ordinary 3-CNF encoding is UNSAT. This is a uniform, exact, source-checkable algebraic-plus-graph compatibility certificate, not a fixed-graph lookup.

If ANY one rim edge is deleted, the rim becomes a path: fix all hubs color 2, alternate rim colors 0 and 1 along the path, and choose (c_uv,d_uv)=(0,1) for each diamond. This is a model. Every such SAT neighbor has exactly 3*2*2^e=6*2^e color models. An even complete rim also has 6*2^e models. We do NOT assert all clause deletions are SAT; duplicate equality edges are noncritical when H remains connected.

## 4. Theorem: raw treewidth and matching backdoor can both be linear although this family is polynomial-time recognizable
Deleting all rim and d vertices and contracting the h_u-c_uv edges (or appropriate sides of their two-edge paths) produces H as a graph minor of G(H). Hence tw(G(H)) >= tw(H). For any infinite cubic expander family H_n with positive uniform vertex expansion, standard balanced-separator inequalities give tw(H_n)=Omega(n), so the distributed odd wheels have raw treewidth Theta(n). Such cubic expanders exist; no explicit expander-generation claim is made for the finite tests.

The signed option graph's same-color induced h_u-c_uv-h_v path is a P3 witness: its endpoints are nonadjacent but connected by two conflict edges. A greedy matching of cubic H has at least ceil(e/5)=ceil(3n/10) edges because selecting an edge eliminates at most 2*3-1=5 incident edges. These paths have pairwise disjoint clause-group labels. Any whole-group deletion to matching-resource components must hit each path, so previous matching-backdoor parameter t >= ceil(3n/10) = Omega(n). Raw rational nullity d=10n-2 is also linear. These are bad *enumeration upper-bound parameters*, NOT lower bounds on any solver.

Yet a polynomial-time module can (i) parse and verify a canonical one-hot 3-color CNF, (ii) find degree-three adjacent true-twin internal pairs via neighborhood scans and verify five-edge diamonds/private interiors, (iii) project them to equalities, (iv) union-find tips and (v) recognize a residual odd wheel or missing-one-edge fan and decide parity/2-SAT. Every step and the reconstruction/refutation can be checked from the original source, no NP oracle or uncharged semantic classifier. On all other inputs, a complete meta-solver retains soundness via ordinary search fallback. This is a polynomial-time *promise-family* algorithm, not a polynomial-time algorithm on arbitrary 3-CNF.

For a safe deliberately loose bit-RAM accounting in explicit N-bit input: T<=O(N^8), peak workspace S<=O(N^3) bits, physical cumulative memory CM=sum_step live_bits<=O(N^11), including source parsing, color-frame consistency checks, neighborhood scans, identification, proof verification and I/O. In the graph-source test implementation the standard adjacency/dictionary operations are much cheaper. No cost is assigned to a free all-graph coloring oracle, and no parallel worker is used. If H is supplied as a separate labeled certificate, it is checked against the unmarked CNF source before reduction; certificate EXISTENCE does not replace certificate DISCOVERY.

## 5. Formal interface and exact induction
The HCL projection rule is allowed only if five graph-inequality edge bundles are present, the two internal vertices are certified private, and no other clause references their one-hot variables. Its certificate is a constant truth table over the 3x3 boundary plus a source-indexed deletion/projection list. Given k distinct valid diamonds, induct on k: the first elimination replaces its graph factor by a binary equality with exact extension multiplicity two; privacy prevents changing the remaining factors, so the inductive residual has the same satisfiability and the count multiplier 2^k. The base k=0 is the unchanged graph. For connected H, the union-find projection proves one hub class; the final two-color odd-cycle argument is exact. Contraction of an arbitrary nonprivate diamond is NOT permitted.

## 6. Reproducible finite results and limitations
Standalone stdlib local script distributed_odd_wheel_20261123.py generated 11 connected cubic sources: prisms n=6,8,10,12,16,24 and seeded simple random connected cubic n=10,12,16,20,30. For each: exact graph sizes, all e private diamond detections, source graph recovered as odd wheel after quotient, graph-model verification for every one of its r single-rim-edge deletion neighbors. Across these 11 cases 153 SAT neighbors checked. Independent direct 3-color domain-propagation/backtracking on uncontracted prism n=6,8,10 returned root UNSAT and single-rim-edge-deleted SAT; visited respectively (43,21), (67,34), (91,47) recursive nodes. No expander spectral gap or actual physical CM was measured, nor end-to-end arbitrary 3-CNF frame parsing. Theoretical parity and privacy proofs carry the universal-in-H claims; finite checks are only bug controls.

The 3-color source quotient need not be a general compression of Decomposition Obstructions' maximum-degree-four arbitrary G embedded in a neutral expander. That input may contain a genuinely NP-complete quotient after removing its neutral overlay. Our polynomial module handles only verifiably private equality diamonds whose quotient is an odd wheel / 2-SAT-reducible graph. Both source-level treewidth inflation and raw nullity inflation can be erased; a real universal coverage theorem still requires polynomial *discovery and global compatibility* for all residuals.

## 7. Adversarial comparison, falsifier and next gate
Sigma Redteam's odd-wheel proper-subset SAT firewall establishes indistinguishability only for a restricted subset-status oracle; the present module reads all source clauses and uses local gadget tables. Critical Graphs' Hajós joins of fixed-width critical bases also stay bounded-width, so joining wheels by Hajós alone does not force hard separators. The present expander-diamond family has high raw width but a certified easy quotient, illustrating a DIFFERENT mechanism. The peer's expander-integer-blind class remains NP-hard after its neutral overlay and equality rings are stripped, so this result is not universal.

Strongest new falsifier for proposed parameter coverage: every rule that insists tw(F)=O(log N), t(F)=O(log N), or raw rational nullity=O(log N) as a prerequisite for polynomial compatibility is unnecessary on this infinite family. A sound meta-solver should include private gadget projection before allocating branch budget.

NEXT OPEN GATE: Construct a broad deterministic polynomial-time classifier for exact 3-color compatibility *after* exhaustive, certified local projections, or show a family in which projection-resistant mixed nonlinear residuals retain large adaptive backdoor/treewidth. Any polynomial-time compatibility decider for all resulting arbitrary graph-3-color residuals would imply P=NP, since the residual class contains all graph 3-colorability. Do not promote family-specific recognition to universal aggregation.

## References
- T5 handoff: research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md
- Prior meta: research/agents/meta-solver-theorem/2026-11-23_1135_SIGNED_CONFLICT_MATCHING_BACKDOOR.md
- Peer obstruction: research/agents/decomposition-obstructions/2026-11-23_1125_EXPANDER_INTEGER_BLIND_COVERAGE.md
- Sigma Redteam: research/agents/sigma-redteam/2026-11-18_0353Z_SIGMA24_WHEEL_FRONTIER_REPAIR.md
- Critical Graphs: research/agents/critical-graphs/2026-11-19_HAJOS_CRITICAL_WITNESS_WIDTH_FIREWALL.md
- Schweser, Stiebitz, Toft (2022), Coloring hypergraphs of low connectivity, J. Combinatorics, https://doi.org/10.4310/JOC.2022.v13.n1.a1
- Okrasa and Rzazewski (2021), Fine-Grained Complexity of the Graph Homomorphism Problem for Bounded-Treewidth Graphs, https://doi.org/10.1137/20M1320146
- Hall (1935), On Representatives of Subsets, https://doi.org/10.1112/jlms/s1-10.37.26
