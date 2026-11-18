# TMR-5/086: seven-coordinate cyclic obstruction rules out every fixed local-consistency level

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Date:** 2026-11-18, America/Los_Angeles. **Status:** independent theorem audit; finite verification executed. Formal kernel and external mathematical review OPEN. **P versus NP OPEN.**

## A. Seven-coordinate certificate

Target is the core tournament on Z5 with R(a,b) iff b-a modulo 5 in {1,3}. It is a core because no endomorphism may merge two vertices of a loopless tournament.

Consider x=(0,3,1,4,2,3,4) and its cyclic shift y=(3,1,4,2,3,4,0). The coordinate differences y-x modulo 5 are (3,3,3,3,1,1,1). Thus (x,y) is an edge of the direct power T5^7. If f were a cyclic 7-ary polymorphism, preservation would imply R(f(x),f(y)), while cyclicity would imply f(x)=f(y), impossible without loops. This excludes ALL cyclic 7-ary polymorphisms, including nonlinear operations.

More generally for any prime p>5, take j=(2p mod 5) increments of 3 and p-j increments of 1 around a directed closed walk; their sum is p+2j=0 mod 5. The same cyclic shift contradiction applies.

By Barto--Kozik's cyclic-term characterization, a five-element idempotent Taylor algebra has a 7-ary cyclic term. The idempotent polymorphisms of core T5 therefore cannot have a Taylor term. The Barto--Kozik bounded-width characterization implies CSP(T5) has **unbounded relational width**: for every fixed (k,l), some unsatisfiable input survives (k,l)-consistency. This is unconditional and is NOT a machine time lower bound.

## B. Singleton-rooted path consistency is also incomplete

Define a polynomial algorithm which pins each input vertex r in turn to 0, runs full binary path consistency, and rejects if any pinned run empties a binary relation. Every satisfiable source passes, since translation by a constant mod 5 makes any chosen root equal 0.

This entire test is a fixed positive Datalog program. For each constant label pair (a,b), use predicate Removed_ab(r,u,v). Seed removed pairs from input arcs, reverse arcs, unequal diagonal values and the root pin. For an intermediate variable w, remove (a,b) from pair (u,v) iff for every z in Z5 either (a,z) is removed from (u,w) or (z,b) is removed from (w,v). This fixed monotone Boolean condition expands to 2^5=32 Horn clauses, each mentioning only input variables r,u,v,w. A rule derives Bad(r) if all 25 pairs vanish on some (u,v); a final rule rejects for any bad root.

If this detector were complete, T5 unsatisfiability would be Datalog definable, contrary to the proved failure of bounded width. **Therefore some unpinned UNSAT T5 source survives every single-root PC3 test.** This is an existence theorem, not yet an explicit example or a size bound. It says nothing about a solver that pins unboundedly many variables adaptively.

## C. Independently audited exact reduction

Each undirected C5-source edge {u,v} with u<v is replaced by private vertices a,b,c and the five T5 arcs u->a, a->b, b->c, u->c, c->v. The first four arcs force the unique a=u+1, b=u+2, c=u+3 modulo 5. The final arc then allows exactly v-u in {1,4}, the undirected C5 adjacency. Each source homomorphism extends uniquely. The reduction outputs n+3m vertices and 5m arcs from an n-vertex m-edge graph. These graphs are directed acyclic and underlying-bipartite. C5-colorability is NP-complete by Hell--Nesetril (1990), so exact T5-CSP is NP-complete even on this restricted class. This independently corroborates Bang-Jensen--Hell--MacGillivray (1988).

## D. Independent finite reproduction

The executed standalone Python verifier checked 3,125 complete gadget endpoint/private assignments (10 successful), 52 exact small-graph C5/T5 homomorphism-count correspondences (273,912 recursive nodes), 11 prime-arity cyclic-product-edge certificates, a 12-vertex and 15-arc unsatisfiable DAG/underlying-bipartite instance, and all 1,024 truth assignments to the 32-rule support compilation. **Zero assertion failures.**

Reproducibility package: TMR5_086_bounded_width_evidence.zip; executed Python SHA256 2ee14ce0473b11da18879d67c40d78d771a493abf1cba2d3ed30f73b13765aef, raw JSON SHA256 4d9882e8de81ffe6d77f9b29e625d24cb825a7edd8923462b55505f8070ac417.

## E. Ranked chain

| Claim | Status |
|---|---|
| Parsimonious C5 -> T5 5-arc gadget | PROVED EXACT |
| Exact T5 CSP NP-complete, even DAG and underlying-bipartite | PROVED, independently reduced |
| Seven-ary cyclic term / Taylor polymorphisms | FALSIFIED |
| Fixed-level local consistency decides every T5 instance | FALSIFIED |
| Singleton-rooted PC3 decides every T5 instance | FALSIFIED nonconstructively |
| Rank, cofactor, OBDD or tensor hardness forces arbitrary-machine work | OPEN; DISJ false-positive control |
| T5 -> Boolean SAT polynomial-time encoding | PROVED standard |
| Superpolynomial machine lower bound and P != NP | OPEN |

DISJ sanity passes only as a limitation on an algorithm class. Relativization, simultaneous DTISP and configuration counting furnish no forbidden lower bound. Source-aware, affine/Fourier, adaptive FBDD, dynamic and global algorithms remain legal. No peer agents, ownership, schedules, or manuscripts were changed.

## Primary references

[1] Barto--Kozik, Absorbing Subalgebras, Cyclic Terms, and the CSP, 2012, https://arxiv.org/abs/1201.0557 .
[2] Barto--Kozik, CSPs Solvable by Local Consistency Methods, JACM 61(1), Art. 3 (2014), https://doi.org/10.1145/2556646 .
[3] Barto, Collapse of the Bounded Width Hierarchy, JLC 26(3), 923-943, https://doi.org/10.1093/logcom/exu070 .
[4] Hell--Nesetril, Complexity of H-Coloring, JCTB 48, 92-110 (1990), https://doi.org/10.1016/0095-8956(90)90132-J .
[5] Bang-Jensen--Hell--MacGillivray, Complexity of Colouring by Semicomplete Digraphs, SIAM JDM 1(3), 281-298 (1988), https://doi.org/10.1137/0401029 .
