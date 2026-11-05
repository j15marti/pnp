# Modular shifts and the size of an UNSAT proof

November 4, 2026, Pacific time

For a direct one-hot encoding of pairwise modular constraints, let $h$ count the vertices of degree at least four after forced shifts have been contracted and parallel constraints combined. Every unsatisfiable instance has a constructible ordinary Resolution refutation of size $3^h\operatorname{poly}(N)$, where $N$ is the encoded source length. Consequently $h=O(\log N)$ gives polynomial-size refutations in the project's fixed mixed calculus, which includes ordinary Resolution. Early contradictions during contraction have polynomial refutations by themselves.

The coloring ingredients are established. Aboulker et al. analyzed the same high-degree parameter for ordinary coloring. Bernshteyn, Kostochka and Pron proved the correspondence degree-colorability theorem used below. The contribution here is their application to the shifted constraints with a traceable conversion all the way back to the original CNF, along with a tested upper and lower benchmark. No claim of priority for the parameterized coloring algorithm is intended. [1,2]

## Source language

An oriented constraint $(u,v,D)$ permits $x_v-x_u\in D\subseteq\mathbb Z_3$. Input vertices have all three labels available. In the direct CNF, each vertex has one at-least-one clause and three pairwise at-most-one clauses. A singleton shift supplies the three forward and three reverse label implications. Any other mask supplies one binary negative clause for each forbidden endpoint-label pair. The source may have loops or several constraints on the same pair.

$N$ counts the encoded input, including these clauses. The result also gives a decision algorithm within the stated time bound. The conclusions about refutations refer to this explicit source encoding. Applying them to a different SAT source requires a separately justified proof translation.

## 1. Contract forced differences and keep their proofs

In each connected component of singleton shifts choose a root and propagate offsets. Each root-label implication along a spanning-tree path is obtained by resolving parent and child implications. The three root labels suffice for all descendants, and the derivations can be shared.

Translate each source exclusion to a clause on the corresponding root labels by resolving with these path implications. A fixed edge outside the chosen tree is also checked. An incompatible fixed edge supplies a forbidden-pair clause by using its implication and the endpoint's at-most-one clause. A loop that excludes its forced difference immediately rules out every root label.

Intersect parallel masks, keeping one witness clause for each excluded pair. If only one difference remains between two variables, derive a transport implication for each source color by resolving the destination's at-least-one clause against its two forbidden destination colors. Substitute the newly forced shift into incident exclusions by Resolution. Each such step eliminates a representative. At most $n-1$ additional contractions can occur. An empty mask yields an immediate constant-step refutation from its already derived exclusions. With $n$ source vertices and $m$ constraint records, these operations require $O((n+1)(m+1))$ derived lines. They use original variables and explicit binary pivots.

In the absence of an early contradiction, the remaining graph $Q$ is simple. Each edge forbids just one difference $d_{uv}$, equivalently $x_v\ne x_u+d_{uv}$. Full masks contribute no edges. Every normalized solution lifts by the recorded offsets.

## 2. Identify low-degree components that extend every boundary assignment

Let $H=\{v:\deg_Q(v)\ge4\}$, $h=|H|$. Temporarily fix a labeling of $H$ consistent with its internal constraints. For a component $C$ of $Q-H$, each incident edge from $H$ forbids at most one color at its endpoint in $C$. Thus the list of remaining colors at $v$ satisfies

$$
|L(v)|\ge 3-d_H(v)\ge d_C(v).
$$

Each internal edge forbids a matching between the lists of its endpoints, since translation by a fixed residue is a permutation. Two sufficient tests guarantee extension for *every* choice on $H$.

1. If some vertex of $C$ has original quotient degree below three, its list is strictly larger than its internal degree. Root a spanning tree there. Greedily color in reverse tree order. Each nonroot vertex has an uncolored parent, and the root has a spare color.
2. If any biconnected block of $C$ is neither a complete graph nor a cycle, Theorem 9 of Bernshteyn, Kostochka and Pron guarantees a coloring for every such assignment of lists and matchings. For their exact-degree formulation, shrink the lists to the internal degrees first. Bridges are two-vertex cliques. For correspondence coloring, cycles of **both** parities must be retained in this test. [2]

Discard components passing either test, including their edges into $H$. The retained graph has exactly the same extendible labelings on $H$. In fact each full labeling of the retained graph extends, since the discarded components meet the retained part only through $H$. The proof generator can use just the sourced clauses of the retained part.

Every block of the remaining low-degree graph is a clique or cycle. A four-clique uses all three incident edges available at each low vertex, so it is an isolated component of $Q$, including from $H$. Every other retained low component has treewidth at most two. One can glue edge, triangle and triangulated-cycle bags at the common cut vertex. Include all of $H$ in those bags, with a separate bag for $H$, and treat each isolated four-clique independently. The resulting width is at most

$$
w=\max\{3,h+2\}.
$$

The implementation finds an order directly. On the low graph excluding isolated four-cliques the treewidth is at most two, so a vertex of degree at most two exists in each nonempty subgraph of the elimination process. Eliminating such a vertex with fill preserves the bound by deletion or edge contraction. Remove any remaining isolated four-cliques, then $H$. At a low-vertex elimination there are at most $h$ higher-degree neighbors, and an isolated four-clique has none. The returned order is checked against $w$.

## 3. Produce a refutation from the original clauses

For an eliminated vertex $v$ with $w_v$ remaining neighbors, enumerate the $3^{w_v}$ assignments on its boundary. Cache an existing source or derived negative clause for each forbidden assignment, allowing a clause stronger than the full assignment exclusion. If none of the three colors of $v$ extends a boundary assignment through its incident factors, obtain three witness clauses. A witness already omitting $v$ can be reused. Otherwise resolve the witnesses against the at-least-one clause of $v$ in at most three binary steps. This yields a clause ruling out the boundary assignment. If any color extends the row, keep the row feasible. These tables represent the exact projection at each step. On UNSAT the last exclusion is the empty clause. Related CSP-to-Resolution connections are developed by Jeavons and Petke. [3]

Counting all paid derivations gives

$$
S_{\rm Res}(F)\le O((n+1)(m+1))+3\sum_v 3^{w_v}
\le O((n+1)(m+1))+3n\,3^{\max(3,h+2)}.
$$

Clause width is at most $\max(3,w+2)$ including intermediate resolvents. Parent indices and pivots have ordinary binary encodings. With directly indexed ternary tables or balanced lookup trees, table lookups, boundary descriptions, certificate output and replay collectively take $3^h\operatorname{poly}(N)$ bit operations in this construction. This is a worst-case upper bound. The elementary frontier solver supplied separately may use more states with a poor vertex ordering.

For this encoding, any family whose minimum mixed refutation cost divided by every polynomial tends to infinity would require $h/\log N\to\infty$. Failure of polynomial boundedness on a subsequence requires the ratio to be unbounded there. A large $h$ is only a necessary condition. This result leaves B3, unrestricted SAT time, and a superpolynomial minimum for the full mixed calculus open.

## 4. Exact classification at maximum quotient degree three

For a connected simple quotient with maximum degree at most three, a noncolorable component must be cubic by the spare-color argument. All blocks must then be cliques or cycles. Inspect a leaf block of its block-cut tree. A non-cut vertex has degree three within that block, forcing the block to be a four-clique. Every vertex of that clique is saturated, so the whole component is $K_4$.

On a $K_4$, UNSAT occurs exactly when all the forbidden offsets are differences of vertex potentials. In that case translating each vertex by its potential gives ordinary three-coloring of four mutually adjacent vertices. Otherwise an oriented triangle has nonzero offset sum, since triangles span the cycle space of $K_4$. Select two vertices of that triangle and choose their colors so they forbid the same color at the third. The nonzero triangle sum is exactly what makes this choice legal on the edge between them. Color the fourth vertex first, avoiding at most two colors, then color the third vertex, which also faces at most two distinct forbidden colors. This gives a satisfying labeling. Out of $3^6=729$ labeled offset choices, exactly $3^{4-1}=27$ are potential differences. All 729 were checked. Ordinary degree-four 3-coloring is already NP-complete, so the unrestricted quotient problem contains an NP-complete subclass at maximum degree four. [4]

## 5. A family on which minimum logical work provably grows

Use the ordinary zero-forbidden-offset wheel on an odd rim of length $r\ge3$. The hub uses one color, forcing the rim to alternate between the other two. Odd parity prevents closure. For $r\ge5$ only the hub belongs to $H$, and a rim elimination order has width at most three.

Every one of the $6r$ edge/color exclusion clauses is indispensable. Removing a rim edge permits the odd rim to alternate along the remaining path with equal endpoints. Removing a spoke permits that rim vertex to take the hub's color, and the remaining rim is a path. In each case permute the three colors to violate exactly the selected clause. All $r+1$ vertex at-least-one clauses are also indispensable. Leave the selected vertex uncolored and color the vertex-deleted graph. At-most-one clauses are dispensable, since from any surviving nonempty label sets satisfying the edge exclusions one may choose one label at each vertex.

Thus the proof DAG must use at least $7r+1$ distinct source clauses. A connected ancestor DAG with $s$ source nodes and $t$ binary inference nodes has at least $s+t-1$ edges and at most $2t$. Hence $t\ge s-1$. Width-three elimination supplies at most $81(r+1)$ binary resolutions using the direct source exclusions. In particular

$$
7r\ \le\ S_{\rm Res}(W_r)\ \le\ 81(r+1).
$$

This pins the minimum to $\Theta(r)$ for ordinary Resolution. The mixed calculus inherits the upper bound, since ordinary Resolution is an allowed rule. The lower bound stated here is for ordinary Resolution. The measured proofs are upper bounds on the minimum.

| Odd rim | Indispensable axioms | Minimum steps at least | Steps in replayed proof | Maximum clause width |
|---:|---:|---:|---:|---:|
| 5 | 36 | 35 | 84 | 4 |
| 15 | 106 | 105 | 264 | 4 |
| 63 | 442 | 441 | 1,128 | 4 |
| 255 | 1,786 | 1,785 | 4,584 | 4 |

## 6. Experiments and reproducibility

| Test | Result |
|---|---|
| One of seven pair options on every pair of four labeled vertices | All 117,649 decisions matched brute force, including 53,802 UNSAT |
| Seeded multigraphs with loops and parallel constraints | All 500 decisions matched brute force |
| Projection to $H$ after component removal | Identical sets of extendible boundary assignments on 4,096 four-vertex cases, 4,096 five-vertex cases and 300 seven-vertex cases |
| End-to-end contracted and pruned source proof | 11 original vertices, one initial and one newly forced shift. The balanced core had an 81-step original-source refutation. A one-offset change produced a verified satisfying assignment |
| Odd-wheel witnesses | One assignment violating precisely the selected source axiom for every indispensable axiom at the eight recorded sizes. Both clause replayers checked each proof |
| Equal input with a different processing order | A single 25-vertex tree had 2 peak frontier states in one order and 4,096 in another |
| Two 4,000-vertex triangle-chain instances | SAT and UNSAT controls both peaked at 2 retained frontier states and used 11,992 trial extensions |
| Independent proof replay | A separate bitmask checker reconstructs all original clauses. Corrupt pivots, parent indices, source differences and truncated traces were rejected in eight negative controls |

The finite checks validate specific implementations. The asymptotic claims follow from the proofs above. All scripts use the Python standard library. Run the following commands from this directory with Python 3.10 or later.

~~~
python shift_solver.py test --output solver_results.json
python degree_reduction.py
python shift_proofs.py
python verify_traces.py proof_results.json --extra trace_checks.json
python wheel_checks.py
~~~

The first program's solver also accepts arbitrary input from a JSON file or stdin. Its module header gives the schema. The proof compiler's automatic degree reduction is selected by the degree_prune option of refute. Its SAT return certifies feasibility mathematically, while the separate frontier solver can recover a full assignment. The illustrated source certificates can be replayed directly from proof_results.json.

## Prior project work and remaining target

The October work already covered fixed-shift consistency, exceptional edges, feedback vertex sets, width examples, ordinary subcubic coloring and a pair of shifted $K_4$ controls. The present analysis adds a uniform upper bound for the normalized shifted system with an original-CNF proof compiler, exact $K_4$ offset classification and an explicit lower and upper benchmark for the minimum binary Resolution work on odd wheels. [5]

A next falsifiable test is to take zero-offset degree-four graphs with many high-degree vertices and no small contradiction, then compare the smallest identified obstruction with source-preserving transformations using native parity or paid definitions. Any resulting minimum-cost claim must cover all legal mixed proofs on that family.

## References

1. Aboulker P, Brettell N, Havet F, Marx D, Trotignon N. *Coloring Graphs with Constraints on Connectivity*. Journal of Graph Theory, 2017, section 6. [Paper](https://arxiv.org/abs/1505.01616)
2. Bernshteyn A, Kostochka A, Pron S. *On DP-Coloring of Graphs and Multigraphs*. Siberian Mathematical Journal, 2017, Theorem 9. [Paper](https://arxiv.org/abs/1609.00763)
3. Jeavons P, Petke J. *Local Consistency and SAT-Solvers*. Journal of Artificial Intelligence Research, 2012. [Paper](https://arxiv.org/abs/1401.4613)
4. Garey MR, Johnson DS, Stockmeyer L. *Some Simplified NP-Complete Graph Problems*. Theoretical Computer Science, 1976. [Paper](https://doi.org/10.1016/0304-3975%2876%2990059-1)
5. PNP project. [RELATION-ALGEBRA-BOUNDARY93](https://github.com/j15marti/pnp/blob/main/research/coordination/2026-10-23_1548_RELATION_ALGEBRA_BOUNDARY93_HANDOFF.md), [EXCEPTION-KERNEL94](https://github.com/j15marti/pnp/blob/main/research/coordination/2026-10-23_1648_EXCEPTION_KERNEL94_HANDOFF.md), [STAR-CHOICE53](https://github.com/j15marti/pnp/blob/main/research/coordination/2026-10-23_1641_STAR_CHOICE53_HANDOFF.md), [DEGREE-BOUNDARY96](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-23_1848_MAIN_DEGREE_BOUNDARY96.tex), [WIDTH-CERT52 reproducer](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-23_1612_WIDTH_CERT52_repro_min.py).
