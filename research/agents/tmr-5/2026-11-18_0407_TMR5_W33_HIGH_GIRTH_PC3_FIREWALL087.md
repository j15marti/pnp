# TMR-5/087: exact PC3 closure at girth >= 7; direct 80-vertex UNSAT T5 counterexample

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Date:** 2026-11-18 America/Los_Angeles. **Status:** independent symbolic theorem, finite complete DFS and independently checked MILP. Formal kernel/external review OPEN. **P versus NP OPEN.** Existing title, branch, living manuscript, hourly schedule and safeguards preserved.

## Theorem (exact unanchored PC3 fixed point on high-girth orientations)

Let `T5` be `Z5` with `R(a,b)` iff `(b-a)%5 in {1,3}`. Let `G` be **any simple oriented graph** whose underlying undirected girth is at least 7. Initialize ordinary binary, unanchored path consistency with equality on diagonal variable pairs, the T5 edge relation on directed arcs and its transpose on reversed pairs, and the universal relation elsewhere.

For distinct vertices `u,v` of underlying distance `d<=3`, let `P[u,v]` be the composition of directed-edge relations along their unique undirected shortest path. For `d>=4` or disconnected pairs, take the full relation. Set `P[u,u]` to equality.

**Then the greatest path-consistent subnetwork is exactly P. In particular, every relation is nonempty, so unanchored PC3 accepts every such input, even if it is UNSAT.**

Proof: Forward increments are `{1,3}=1+{0,2}` and backward increments are `{-1,-3}={2,4}=2+{0,2}`. A path of length `d` permits the endpoint differences `c+{0,2,...,2d} (mod 5)`, with cardinality `min(5,d+1)`. Thus four or more arcs in series impose no endpoint restriction. Girth >=7 means every path of length <=3 between distinct endpoints has a unique reduced simple path, otherwise two short paths make a cycle of length <=6. For a triple `u,w,v`, if the sum of the two relevant short distances is >=4, then `P[u,w]∘P[w,v]` is the full relation (including cases with a full, surjective factor). Otherwise, the concatenation is a walk of length <=3; any backtracks only relax its relation, so `P[u,v]⊆P[u,w]∘P[w,v]`. The diagonal case is handled by equality, with each edge/path relation surjective. Hence P is a nonempty path-consistent subnetwork of the initial constraints. Conversely PC3 composes every input path of length <=3, so any fixed point is contained in P. Therefore the fixed point equals P. QED.

This theorem assumes *one directed orientation per undirected edge*, no 2-cycles. It concerns **unanchored** PC3, not singleton-rooted PC3.

## Explicit direct NO instance and YES companion

Use the symplectic incidence graph W(3,3) on F3^4. There are 40 projective points and 40 totally isotropic projective lines for alternating form

`B(p,q)=p0*q2-p2*q0+p1*q3-p3*q1 (mod 3)`.

The 160 incidence edges give a connected, bipartite, 4-regular underlying graph with girth **8**, diameter 4, N=80 and M=160. Generate projective point coordinates in lexicographic order after normalizing first nonzero coordinate to 1; enumerate all orthogonal two-dimensional spans, order the 40 lines by their sorted point sets, and sort the 160 incidence edges `(point_id,line_id)`. Direct canonical edge i point-to-line when bit i of the following mask is set; otherwise reverse it:

`0xfa11b749a37a90ad5e8e6028df085ec0a06e4a3d`.

**This orientation is UNSAT**, as verified by a complete branch-and-AC3 search fixing variable 0 to symbol 0 (valid by global translation symmetry). It required only **9 DFS nodes, 5 closed leaves and 3,776 arc revisions**. Explicit case split:
* `x40=1`: `x1=0` and `x1=3` both close.
* `x40=3`: `x1=2` closes; `x1=0` leads to `x2=1` and `x2=4`, both closing.

An independent SciPy/HiGHS binary ILP encoded all 80 one-hot variables, with 400 Boolean columns, 2,480 rows and 5,200 nonzeros. HiGHS returned **infeasible, status 2**. Exact search and MILP were independent.

Yet the original unanchored T5-PC3 algorithm accepted in **two scans**, and its relation matrix agreed on all 6,400 ordered pairs with the short-path formula. A separate C++ bitset implementation also accepted in two scans and rejected **all 80 singleton-anchored PC3 attempts**. An independent Python relation implementation rejected sample anchors 0, 40 and 79. This finite counterexample does NOT establish the still-missing explicit NO instance that survives every singleton-rooted PC3 test.

For every vertex of W(3,3), the distance counts are `(1,4,12,36,27)`; the PC3 relation cardinalities for distances 0 through 4 are respectively `(5,10,15,20,25)`. The Python verifier checked **259,200** unordered-pair/third-variable PC3 compatibility conditions, with zero failures. There are no auxiliary reduction gadgets.

A YES orientation on the **identical underlying graph** directs every incidence edge point-to-line, with witness all points=0 and all lines=1. Appending arbitrarily long pendant paths to the NO instance produces connected, max-degree-at-most-5, girth-eight UNSAT instances of arbitrarily large size that still defeat unanchored PC3. Recognition of this constructed family is easy, so this is a falsification of local consistency, not a resource lower bound.

## Dependency verdict

| Proof arrow or algorithm claim | Status |
|---|---|
| This exact T5 fixed-template homomorphism CSP is NP-complete | **PROVED**, primary semicomplete-digraph theorem [1] |
| Direct unanchored PC3 is complete for T5 | **FALSIFIED**, 80-vertex high-girth UNSAT input |
| Exact PC3 closure theorem on oriented graphs of girth >=7 | **PROVED**, mathematical argument and finite checks |
| Universal singleton-rooted PC3 completeness | **FALSIFIED NONCONSTRUCTIVELY** in prior bounded-width/Datalog argument; explicit finite counterexample **OPEN** |
| TMR-1 five-arc C5-to-T5 encoding | **PROVED/SCOPED** in earlier independent work, unused here |
| Fixed-order OBDD, tensor rank, treewidth or representation size forces arbitrary-machine work | **FALSIFIED** as general instancewise inference |
| Unrestricted superpolynomial lower bound for T5 | **OPEN** |
| Transfer of lower bound to unrestricted Boolean SAT / P versus NP | **OPEN** |

Four safeguards: DISJ-style false positive PASS; relativization barrier not crossed; no simultaneous DTISP theorem; configuration counting remains an upper-bound control. Repository preflight, complete LaTeX compilation, formal proof-kernel checking and external mathematical review not performed. Draft PR #209 remains unmerged; no peer ownership or schedules modified.

### References

[1] Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 281-298 (1988), https://doi.org/10.1137/0401029 .
[2] Barto, Kozik, *Constraint Satisfaction Problems Solvable by Local Consistency Methods*, J. ACM 61(1), article 3 (2014), https://doi.org/10.1145/2556646 .
[3] Kozik, *Solving CSPs Using Weak Local Consistency*, SIAM J. Comput. (2020), https://doi.org/10.1137/18M117577X .
