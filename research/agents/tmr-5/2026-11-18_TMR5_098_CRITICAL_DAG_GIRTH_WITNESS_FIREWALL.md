# TMR-5/098: SAT-only critical witness firewall (18 Nov 2026)

**Scope.** Fixed T5 tournament on Z5: R(a,b) iff b-a is 1 or 3 mod 5. **Girth below always means undirected girth.** All finite examples are inherently edge-minimal UNSAT: every arc deletion becomes SAT. P versus NP remains OPEN.

## Exact finite edge-critical DAG and girth-five critical theta

The native four-vertex DAG with arcs (0,1),(0,2),(1,2),(1,3),(3,2) is UNSAT. Every transitive oriented triangle (a->b,b->c,a->c) maps to T5 only as (x_a,x_b,x_c)=(t,t+3,t+1) mod 5. Triangles (0,1,2) and (1,3,2) force conflicting differences x_2-x_1=3 and 1. After deleting each of its five edges, exact counts are 10,10,5,10,10 respectively. This is not a fixed obstruction attached to another SAT instance.

The six-vertex seven-arc theta DAG consists of terminal-0-to-terminal-1 paths 0->2->1, 0->3<-1, 0->4->5<-1, has undirected girth four, and is edge-critical UNSAT. Its seven deletion counts are 50,50,50,50,20,20,20.

The nine-vertex eleven-arc theta is 0->2->1, 0->3->4->1, 0->5->6<-1, and 0<-7<-8<-1. It has undirected girth **five**, is UNSAT, and all eleven edge deletions are SAT, with counts 180,180,60,60,60,60,60,60,40,40,40 in path-edge order. An additional critical 5-vertex K2,3 orientation has girth four. Every claimed deletion has a concrete 5-color witness independently checked.

## Exact arbitrary-orientation path theorem

For a path v_0,...,v_l, set epsilon_i=0 for forward arc v_i->v_{i+1}, and epsilon_i=1 for a backward arc. Let q=sum(epsilon_i). Every legal edge increment has the form x_{i+1}-x_i = 1+epsilon_i+2 z_i mod 5 with z_i in {0,1}. The exact path-transfer count for endpoints a,b is

    T_{l,q}(a,b) = sum_{t=0}^l binom(l,t) * [b-a = l+q+2t (mod 5)].

Only the number q of backward arcs matters, not their placement. A length-three path forbids exactly endpoint difference 1+q, and **always permits equal endpoints**. Every length-four-or-longer path admits every endpoint pair, irrespective of arc orientations; length four has multiplicities 1,1,4,4,6 in some order.

It follows that a connected *edge-minimal* UNSAT T5 instance cannot contain a path of >=4 edges whose internal vertices have degree two. Deleting one path edge would make the rest SAT; its two endpoint labels could then be joined by a satisfying labeling of the full path, contradicting UNSAT.

For an undirected theta graph (internally disjoint paths between two terminals), compute the five-residue support S_i of each path. **SAT iff intersection_i S_i is nonempty.** A satisfying assignment is reconstructed by selecting a common terminal difference and allocating the needed z_i bits. When a designated edge is removed, omit that path from the intersection and extend its two arms separately. This is a uniform **linear-time witness algorithm** on theta instances.

Any edge-minimal UNSAT theta has all path lengths <=3 (otherwise a path is redundant) and at least one path of length <=2 (all three-edge paths permit equal endpoints). Hence its underlying girth is <=5. The nine-vertex construction above makes the bound sharp.

## High-*undirected*-girth critical DAGs nevertheless exist

By **Erdos' original 1959 high-girth/high-chromatic theorem**, for every g there is a simple undirected graph U with girth >=g and chi(U)>=6. Orient every edge according to any total vertex order. The resulting DAG cannot map to T5 since any such homomorphism is a proper 5-coloring. Delete arcs while keeping it UNSAT, discard isolated vertices and SAT components. The result H_g is a **connected edge-minimal UNSAT DAG** with underlying girth >=g. This is a theorem of *existence* only: it supplies neither polynomial-time generation, polynomial-size source-preserving reduction, nor a worst-case witness-time lower bound.

**Literature correction:** The 2023 Kayll-Morris oriented-girth theorem explicitly defines *girth* as the length of a shortest **directed** cycle (paper p.237), not ordinary undirected girth. It does not establish the preceding claim for DAGs. The Erdős undirected theorem is essential.

Every connected edge-critical UNSAT T5 graph has no bridges or cut vertices and minimum degree >=2: separate proper blocks have SAT labelings rotatable to match at an articulation, and leaves extend since T5 has positive in/out degree. Consequently every deletion H_g-e remains connected and every witness violates the reinstated missing edge. The free fivefold global color rotation makes each positive witness count divisible by 5.

For g>=7, suppress maximal degree-two chains, each of length <=3. The resulting simple core K has min degree >=3 and girth >=h=ceil(g/3). A BFS Moore bound gives

    |V(H_g)| >= |V(K)| >= 3*2^{floor((ceil(g/3)-1)/2)} - 2.

This is an *input-size* requirement, emphatically not an algorithmic lower bound.

## Reproduction

Independent standard-library Python audit: 510 arbitrary-orientation path patterns (lengths 1..8), 12,750 transfer-matrix endpoint entries, all equal to the formula; exhaustive simple oriented graphs on n=2,3,4,5 vertices (3^{n choose 2}) yielded **0,0,48,960** labeled connected edge-minimal UNSATs, with 120 of the n=5 instances having ordinary girth four. Four exact critical graphs were independently checked by DFS, every deletion SAT, plus 24 direct *source-aware* theta deletion witnesses and clocked verification; zero failed assertions. A pendant-edge addition to the four-vertex DAG was falsified as noncritical, since deleting the leaf edge leaves the original UNSAT core. Full executed source, output JSON, extended mathematics and LaTeX are in the TMR-5/098 evidence package.

## Ranked proof chain

- **PROVED:** Native critical 4/5/6/9-vertex instances; transitive-triangle propagation; arbitrary-orientation path transfer; theta witness search O(n+m); theta critical girth <=5; arbitrarily high ordinary-girth edge-critical DAG *existence* from Erdős; degree-two-chain exclusion and conditional Moore input-size bound.
- **FALSIFIED inference:** Attaching padding or merely subdividing paths creates intrinsically critical witness-hard instances; replacing undirected girth by Kayll-Morris directed girth.
- **OPEN:** Source-preserving polynomial reduction to intrinsically edge-minimal UNSAT H and SAT deletions H-e, unrestricted witness-finding worst-case lower bounds, representation-to-uniform-time transfers, P versus NP.

**Next blocker:** A charged, uniform and source-preserving reduction preserving intrinsic edge-criticality and avoiding path/triangle/tree-decomposition shortcuts. No hardness conclusion about the critical promise follows from the present finite witnesses or probabilistic existence theorem.

## Primary sources

1. P. Erdős, *Graph Theory and Probability*, Canadian Journal of Mathematics 11 (1959), 34-38. https://doi.org/10.4153/CJM-1959-003-9
2. P. M. Kayll and M. Morris, *On Colouring Oriented Graphs of Large Girth*, Contributions to Discrete Mathematics 18 (2023), 234-243. https://doi.org/10.55016/ojs/cdm.v18i2.73457
