# TMR-3/094: Critical-deletion SAT witnesses and time-space transfer barrier

2026-11-18 America/Los_Angeles. Owner: TMR-3 / PNP Time-Space Tradeoffs.
**STATUS: PROVED/EXACT restricted algorithms and promise-reduction implication; COMPUTATIONAL finite checks; OPEN unrestricted witness lower bound. Independent peer review pending. P vs NP OPEN.**

## Input and scope
Fixed T5 on Z5: arc (u,v) requires x_v-x_u mod 5 in {1,3}. Explicit binary input is a pair (H,e), where e is a designated arc of an edge-minimal UNSAT oriented H. Required output is a full coloring of H-e. Promise recognition is NOT assumed free; the constructive solvers work without checking UNSAT, reporting failure off promise. Isolates must be removed from H's edge-bearing core and colored separately. Every lower-bound claim must quantify over ALL uniform algorithms and promised SAT instances.

## A. Exact source-derived branch-core witness algorithm, PROVED/EXACT
For connected min-undirected-degree-2 H with b degree-at-least-3 branching vertices, suppress each maximal degree-two path P; preserve its actual orientation word and endpoint relation. A length-L path with f forward traversals has difference set
D(L,f) = {2L-f+2j (mod 5) : j=0,...,L}, of cardinality min(5,L+1).
All nine relations with 1<=L<=3 and 0<=f<=L are distinct. Every edge-minimal UNSAT H has no degree-two thread of >=4 edges: an internal four-edge path admits all five endpoint differences, and cannot be essential.

If e is an arc in a thread, omit the ENTIRE thread endpoint constraint: cutting that edge leaves two independently extensible free-ended path segments. Retain exact constraints from the other threads. Enumerate the b branch colors with one anchor at zero by fivefold translation, at most 5^(b-1) tuples. For a compatible tuple, recover every original internal vertex with five-state path DP (or one-ended propagation on the severed thread), then verify the complete x against all original arcs except e. Source authentication, adjacency traversal, failed candidates, reconstructing all thread interiors, output and verifier are all part of the same realization.

Conservative simultaneous deterministic random-access bounds for explicit input length N:
T(N)=O((N+1)^4(1+5^(b-1))), S_peak(N)=O((N+1)^2) bits.
Direct deterministic sequential-tape implementation:
T(N)=O((N+1)^8(1+5^(b-1))), S_peak(N)=O((N+1)^3) bits.
Both are upper bounds only, not exact measured costs or lower bounds. Graphs with b=0 take an ordinary cycle/path solver. Legal alternate algorithms include binary spanning-tree enumeration O*(2^(n-c)) and five-state primal/branch-core treewidth DP O*(5^(tw+1)). No one ordering is imposed on an unrestricted solver.

## B. Improved high-girth structural constant, PROVED/EXACT
For an edge-minimal UNSAT H after discarding isolated vertices, assume undirected girth >=7. The suppressed core B has min degree >=3. It is simple: any loop thread makes a cycle of <=3 arcs, and two parallel threads make a cycle of <=6 arcs. Thus m(B)<=binom(b,2). Each thread has at most two interior vertices. Therefore n<=b+2m(B)<=b^2. With cyclomatic number beta=m(B)-b+1, min degree 3 gives beta>=b/2+1>=sqrt(n)/2+1. This tightens the constants supplied in the current branch-core handoff, but is ONLY a graph-parameter bound; it in no way forces 5^b actual time or space. The externally named branch-core ZIP and THEOREM.md were not mounted in this environment; this short-thread/simple-core claim was rederived directly and the nine relations independently enumerated. The separate handoff Moore/girth arithmetic was not fully independently audited.

## C. Exact relative-pin search-to-decision compiler, PROVED/EXACT
For one fresh w, the arcs u->v,u->w,w->v are feasible iff x_v=x_u+1 mod 5; then x_w=x_u+3 uniquely. Chains of at most five such triangles force any relative difference d in Z5, with unique internal extension. Given arbitrary SAT G, fix a reference vertex color zero by rotation, and recover each other original color via at most five *ordinary unrestricted T5 SAT decision* queries with the already fixed pins. No more than 1+5(n-1) decision calls, polynomial total query generation, and final full witness verification are needed. The queried graphs can be UNSAT or off the critical-deletion promise. Consequently this does NOT give a critical-promise SAT witness algorithm and cannot transfer ordinary decision lower bounds to that promise without an additional bridge.

## D. All-outcome total-promise reduction barrier, PROVED implication
Suppose a polynomial-time many-one map f takes EVERY Boolean formula, both satisfiable and unsatisfiable, to a valid edge-minimal-UNSAT T5 pair (H_phi,e_phi), and a polynomial-time decoder outputs SAT(phi) from phi and EVERY valid witness of H_phi-e_phi. Then NP=coNP. Proof: for an UNSAT formula, the promised output has a polynomial-length T5 witness. Guess and verify it, then check the decoder outputs NO. This puts UNSAT in NP. The theorem rules out assuming a standard two-outcome/all-witness reduction for free; it is NOT a ban on other reductions or a proof NP!=coNP.

FLMV (2005) and Williams (2006/2020) provide decision-SAT forbidden regions on specified random-access/space models, not a theorem for this SAT-only promised search relation. An ordinary T5 NP-hardness reduction may output NO T5 graphs and so does not preserve the promise. If a reduction produces M=O(n^a) bits in time n^r and space n^s, a simulated solver taking M^t time and M^d space, plus n^q per generated source access, yields symbolic composite exponents max(r,at+q) and max(s,ad), provided no more materialized storage is used. Storing the whole n^a-bit reduction normally destroys subpolynomial-space hypotheses. No FLMV exponent is transported without a reduction plus same-machine generator, query and memory proof.

## E. Unbounded-girth intrinsic critical existence, PROVED/EXACT, nonconstructive
Erdos's high-girth/high-chromatic theorem provides an undirected U of chromatic number >=6 and girth >g for each fixed g. Orient U arbitrarily. T5 coloring requires a proper five-coloring, hence the oriented U is UNSAT. Delete edges until UNSAT is edge minimal, discard isolates, and retain its unique edge-bearing component. A cut vertex would enable gluing colorings of proper edge subgraphs by Z5 translations, contradicting criticality. Thus connected 2-vertex-connected edge-minimal UNSAT H of arbitrarily large girth exist. This says nothing about uniform construction or SAT deletion witness hardness.

## Independent COMPUTATIONAL evidence (all zero assertion failures)
- 512 short-thread-relation subfamilies checked: nine distinct relations; maximum irredundant size four; irredundant-size distribution 1:9, 2:26, 3:24, 4:4.
- All 512 orientations of complete K(3,3): 336 UNSAT and zero edge-minimal UNSAT. All 3^9=19,683 absent/forward/backward K(3,3) patterns: 288 edge-minimal UNSAT *labeled subgraphs* (72 six-edge; 216 seven-edge). Some have isolated labels and must be compacted.
- Five-vertex critical H={(0,2),(0,3),(4,0),(1,2),(3,1),(1,4)}. All six deletions have witnesses; rooted solution counts [8,2,2,8,2,2] and all missing-edge differences in {0,2,4}.
- 250 seeded random binary spanning-forest checks versus exhaustive original-coloring search; 60 unique-extension relative-pin exact-count tests; 50 randomized actual decision-to-witness recoveries (321 unrestricted T5 decision calls); 234 independently verified branch-core critical-deletion full witness tests.
- Small repository smoke implementation reproduces critical deletion counts, nine relations, irredundancy and the increment gadget. Full executed local references: verify094.py SHA256 6e98903801af4f19f5a93619be427ef954ad13da856c54a02a53d8d9d03714db; core_solver094.py SHA256 dfb860af3347f021e902bb783680406c1fe4001a5f8043b4b56084e3ec7ced4a; audit094.json SHA256 d6421a00ac752669a34d10e38f19356a928f54e6be84fa9b595ef80d51f4eeaa. Native TM execution, combined LaTeX build and independent peer review outstanding. Finite tests do NOT certify asymptotic runtime.

## Four gates, controls and next blocker
DISJ: restricted constructive sanity PASS, lower bound NOT CLAIMED. Relativization: NOT APPLICABLE to separation; any nonrelativizing bridge remains OPEN. Simultaneous DTISP: PASS conservative same-execution upper bounds, lower-bound transfer OPEN. Deterministic configuration counting: compatible upper bounds, no necessity claim. Keep treewidth, signed GF5 cycles, Fourier, Gaussian/affine, sparse/biclique and block-cut shortcuts, legal caching, compact circuits, variable orderings, full output, padded easy cases, unique-solution and wrapper controls. Do not promote rank, proof or graph complexity to machine runtime.

**NEXT C3-T5-INTRINSIC-PROMISE-LOWER-BOUND095:** obtain a fully specified uniform both-outcome promise reduction or a genuinely execution-sensitive worst-case invariant surviving every legal solver. Both remain OPEN; P versus NP OPEN.

## Sources
[1] Fortnow, Lipton, van Melkebeek, Viglas (2005), JACM 52, https://doi.org/10.1145/1101821.1101822 .
[2] R. Williams (2006), *Inductive Time-Space Lower Bounds for SAT and Related Problems*, https://doi.org/10.1007/s00037-007-0221-1 .
[3] Mudigonda and Williams (2020), arXiv:2012.00330, states 2cos(pi/7) SAT/small-space bound, https://arxiv.org/abs/2012.00330 .
[4] P. Erdos (1959), *Graph Theory and Probability*, Canadian J. Math. 11.
[5] Bang-Jensen, Hell, MacGillivray (1988), *The Complexity of Colouring by Semicomplete Digraphs*, https://doi.org/10.1137/0401029 .
