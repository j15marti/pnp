# TMR-5/081: Five arcs are optimal for bipartite-underlying DAG C5-to-T5 edge gadgets

**Research date:** 2026-11-17 22:42 PST. **Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Status:** PROVED/EXACT within an explicitly restricted private, unpinned, directed-edge pp-gadget model. Mathematical external review OPEN; independently executed finite enumeration COMPUTATIONAL. **P versus NP OPEN.**

## Model and target relation

The fixed target is the tournament T5=(Z5,R) with R(x,y) iff (y-x) mod 5 is in {1,3}. A source gadget is a finite loopless simple oriented graph with distinct terminal vertices u,v, unpinned existential auxiliary vertices, and no other predicates. All source arcs are R constraints. The induced binary relation is

S_G = {(x,y) in Z5^2 : there exists a satisfying assignment to the auxiliary vertices with u=x,v=y}.

The target relation is S_C5 = {(x,y): (y-x) mod 5 in {1,4}}, undirected five-cycle adjacency. The resource counted is the number of distinct directed arcs in the private edge gadget, not the runtime or size of a global reduction.

## Main theorem and proof

**Theorem.** If the source gadget is a directed acyclic graph (DAG) and its underlying undirected graph is bipartite, then a gadget with at most four arcs cannot define S_C5. The five-arc gadget

    u -> a, a -> b, b -> c, u -> c, c -> v

is a bipartite-underlying DAG, defines S_C5, and has exactly one private extension for every permitted pair. Hence the minimum number of arcs is **five** under these constraints.

**Lower-bound proof.** Components disconnected from both terminals either make the induced relation empty or contribute only a satisfiable existential factor. If u and v are in different components, vertex-transitivity of T5 and no pinned constants imply that either the relation is empty or all 25 terminal pairs are feasible. Suppose they share a connected component. With at most four distinct underlying edges and bipartiteness, this component is either a tree or a 4-cycle (any larger bipartite cycle requires at least six edges).

In a tree, branches off the unique terminal-to-terminal path never constrain the endpoints because every T5 vertex has incoming and outgoing neighbors. A directed path of k edges has endpoint support given by a sum of k two-element subsets {1,3} and/or {2,4} of Z5. Cauchy-Davenport implies support size at least min(5,k+1). For k>=2 this is at least three; for k=1 it is {1,3} or {2,4}, neither the required {1,4}.

For an underlying 4-cycle, if the terminals are adjacent, their direct oriented arc forces difference in {1,3} or {2,4}, excluding at least one required difference. If opposite, the two internally disjoint length-two paths have support from the following three sets:

- S_+={1,2,4}, directed path u -> a -> v.
- S_-={1,3,4}, reverse directed path v -> a -> u.
- S_0={0,2,3}, a fork or collider.

The endpoint relation is the intersection of two path supports. The **only** pair of those supports whose intersection is {1,4} is S_+ intersect S_-. This forces a directed four-cycle, violating acyclicity. Thus at most four arcs cannot suffice. Isolated, disconnected, and duplicate constraints do not change the conclusion. Antiparallel arcs make the instance unsatisfiable because the template is an asymmetric loopless tournament.

**Five-arc upper-bound proof.** For u->a->b->c, the total three-step difference is one of {0,2,3,4}. The additional direct arc u->c permits only {1,3}; therefore c=u+3, achieved uniquely through increments (1,1,1), forcing a=u+1 and b=u+2. The final c->v constraint is true exactly when v-u belongs to {4,1}. Hence there is exactly one extension per permitted terminal pair. The underlying source is a 4-cycle with a leaf, hence bipartite, and u,a,b,c,v is a topological order. QED.

## Exact comparison with prior gadgets

| Construction | Arcs | DAG | Underlying bipartite | Extensions per permitted pair |
|---|---:|---|---|---:|
| Directed four-cycle u->a->v->b->u, prior /072 | 4 | NO | YES | 2 |
| Four-arc triangle-containing u->a,u->b,b->a,b->v, prior /073 | 4 | YES | NO | 1 |
| Five-arc TMR-1/080 gadget, this run | 5 | YES | YES | 1 |

The theorem is **restricted** to unpinned, private, two-terminal simple directed-edge gadgets. It does not establish optimality for shared auxiliaries among multiple source edges, pinned symbols, extra predicates, weighted pp-definitions, reductions employing larger global structures, or a lower bound on algorithmic work.

## Reproduction and execution

The independent CPython standard-library program exhaustively enumerated all simple oriented source graphs with 2 to 5 labelled vertices, at most four arcs, fixed ordered terminals 0 and 1, with DAG and bipartite filters. The five-vertex cutoff is complete: a connected component with at most four edges has at most five vertices; irrelevant components cannot create C5 adjacency.

The executable checked **3,556** eligible source graphs, **17,780** endpoint-difference supports and found **zero** counterexamples. Among 4-arc bipartite source graphs, it independently found exactly **8** labelled occurrences implementing C5 adjacency when directed cycles are allowed, and **none** was a DAG. It checked all 25 ordered terminal pairs for each of the three benchmark gadgets, including all private assignment extensions, confirming extension counts 2,1,1 respectively and zero assertion failures.

Two separate CPython executions produced byte-identical JSON: SHA256 ef643a8f50968cfdf2c12f5aefdd07cf701559eaae60649360e2f8cd297e3861. Executed source SHA256 9101b1cbcfd109285de934c4b3f93e4e76896308f2e861ac19ea9abc50603d02, Git blob 823d6fc40ab79bb582a4f5e8b2eff42d2b03f6ed. Source compiled successfully. The Python code and complete raw JSON are in:

- experiments/tmr/tmr5_t5_dag_bip_opt081.py
- results/raw/tmr/2026-11-17_2242_TMR5_T5_DAG_BIP_OPT081_RAW.json

The independently executed finite verification corroborates the all-size symbolic result. Native machine microsteps, repository-wide preflight, full LaTeX compilation, external referee verification and Lean/nanoda were not executed.

## Ranked dependency and safeguard audit

**T5 complexity:** KNOWN PRIMARY THEOREM, NP-complete (Bang-Jensen, Hell and MacGillivray 1988, applies because T5 is a semicomplete digraph with multiple cycles); C5 graph homomorphism NP-complete by Hell and Nešetřil 1990. **TMR-1/080 reduction gadget:** independently rechecked, PROVED/EXACT within model. **Minimal five-arc DAG+bipartite edge pp-gadget:** this run PROVED/EXACT RESTRICTED. **Treewidth, fixed-order OBDD, rank or gadget size as a universal unavoidable runtime measure:** FALSIFIED as generic instancewise claims or OPEN under stronger quantifiers, per earlier redteam controls. **Representation-independent all-algorithm resource necessity:** OPEN. **Superpolynomial Boolean SAT lower bound:** OPEN.

DISJ sanity **PASS** only for local gadget and prior countercontrol; relativization **NOT APPLICABLE** to a separation; simultaneous DTISP **NOT APPLICABLE** to lower bounds; deterministic configurations **upper-bound safeguard only**. The theorem is about minimal representation of one binary relation and gives no NP separation.

**One highest-priority next dependency:** attempt a genuinely algorithm-independent cost bound on mixed YES/NO authentic T5 instances that survives authenticated private gadget elimination, C5 extraction, adaptive branching and tensor/algebraic algorithms. **P versus NP remains OPEN.**

## Primary references

Bang-Jensen, J., Hell, P., MacGillivray, G. (1988). *The Complexity of Colouring by Semicomplete Digraphs*. SIAM J. Discrete Math. 1(3), 281–298. https://doi.org/10.1137/0401029.

Hell, P. and Nešetřil, J. (1990). *On the Complexity of H-Coloring*. Journal of Combinatorial Theory B 48, 92–110. https://doi.org/10.1016/0095-8956(90)90132-J.
