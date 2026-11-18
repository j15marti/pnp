# TMR-5/095: #P-hard counting on universally satisfiable bipartite DAG T5 instances

**Date:** November 18, 2026 (Pacific). **Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Status:** Exact symbolic polynomial-time Turing reduction, independently executed finite tests. External proof review pending. **P vs NP remains OPEN.**

## Theorem and strict scope

Let T5=(Z5,R), R(a,b) iff b-a (mod 5) is 1 or 3. Given any **acyclic directed source** G=(V,E) and t>=1, replace each source arc u->v by t internally disjoint directed length-4 paths and t internally disjoint directed length-8 paths, all directed from u to v. Denote the output F_t(G). Its exact size is n+10mt vertices and 12mt arcs.

F_t(G) is a DAG (path substitution in a DAG preserves acyclicity). Its entire underlying undirected graph is **bipartite**, even for a non-bipartite underlying source G: put all original vertices in one partition class and alternate along every even-length private path. Every assignment of the original vertices extends to a full T5 solution, since the endpoint transfer counts are strictly positive. Restricted decision is therefore identically YES, including when every original label is arbitrarily prescribed.

Nevertheless **exact counting restricted to these universally SAT bipartite DAGs is #P-complete under polynomial-time Turing reductions**. It is not a parsimonious reduction and implies NO existential-decision time lower bound.

## Exact arithmetic certificate

For the T5 adjacency matrix A, direct matrix multiplication and independent increment enumeration give
```
(A^4)[0,*] = (4,4,1,6,1)
(A^8)[0,*] = (36,70,36,57,57)
w(d)       = (144,280,36,342,57)
```
The effective weight for one 4/8-path pair is w(d)=(A^4)[0,d]*(A^8)[0,d], where d is the terminal minus initial symbol modulo five. Use prime-valuation rows p=2,3,5,19, plus the total histogram row:
```
 M = [4 3 2 1 0]
     [2 0 2 2 1]
     [0 1 0 0 0]
     [0 0 0 1 1]
     [1 1 1 1 1]
 det(M) = -2
```
For every histogram h=(h0,...,h4) of edge differences with sum h_d=m, set z_h=product_d w(d)^h_d. Unique prime factorization and det(M) !=0 show that all z_h are distinct positive integers. If N_h is the number of source vertex assignments with histogram h, then

Z(F_t(G)) = sum_{sum h_d=m} N_h*z_h^t.

There are H=binom(m+4,4)=O(m^4) histograms. The H values for t=0,...,H-1 form an invertible Vandermonde matrix. Exact rational elimination recovers every N_h and thus the **original** native T5 count Z(G)=sum_{h0=h2=h4=0} N_h. At t=0 the count 5^n is known without querying; for t>=1, all oracle instances are SAT bipartite DAGs. Their sizes are O(n+m^5), their output count bit lengths are polynomial, and rational interpolation has polynomial bit complexity.

To prove counting hardness on acyclic sources independently, start from the primary Dyer–Greenhill (2000) #P-completeness of homomorphism counting to the undirected C5. Replace an arbitrarily oriented undirected source edge {u,v} by **u->a, a->b, b->c, u->c, c->v**. For each valid C5 endpoint pair there is exactly one private extension (a,b,c)=(u+1,u+2,u+3) mod 5, and otherwise none. Direct all-3125-private-assignment audit supports the symbolic proof. Orient the source edges by a total order on the original vertices to ensure the entire lifted T5 graph is a DAG. This is a parsimonious reduction proving #T5 is #P-hard even on DAG inputs, and its composition with the even-path Vandermonde transformation yields the theorem.

## Explicit adversarial witness

An undirected triangle transformed through the five-arc C5 gadget gives an **UNSAT 12-vertex, 15-arc T5 DAG**. Its even-path F_1 lift has **162 vertices, 180 arcs** and is a SAT bipartite DAG. Give every original source vertex 0 and extend each private 4-path using increments (3,3,3,1), and each private 8-path with (3,1,1,1,1,1,1,1). The complete 180-arc witness passed independent verification.

## Independent reproducibility

The executed third-party-free CPython verifier is contained in the conversation evidence ZIP together with exact raw JSON, LaTeX section and SHA256 manifest. Results: both transfer powers checked by independent arithmetic; determinant -2; **3125** five-arc private cases; **48** randomized acyclic source graphs and **646** histogram coefficients reconstructed through independent modular Vandermonde solving; explicit DAG/bipartite checks; independent native homomorphism enumeration yielding **4295** solutions for the 12-vertex one-source-arc F_1 gadget; 12-vertex UNSAT source checked by independent backtracking; explicit 162-vertex SAT witness; **zero assertion failures**. Modular interpolation is only finite verification; the theorem uses exact rational arithmetic.

## Ranked dependency synthesis

| Arrow | Status |
|---|---|
| Exact fixed T5 CSP NP-completeness | PROVED, Bang-Jensen et al. 1988; Hell–Nesetril C5 reduction |
| #C5 hardness -> acyclic #T5 hardness | PROVED, Dyer–Greenhill 2000 + checked parsimonious five-arc gadget |
| Even-length substitution gives SAT bipartite DAGs | PROVED |
| Positive edge weights encode all five histogram coordinates | PROVED, determinant -2 |
| Exact counting on universally SAT bipartite DAGs | PROVED, polynomial-time Turing hardness; review pending |
| Exact counting/representation complexity -> necessary existential decision work | FALSIFIED as a general instancewise inference |
| Representation-independent worst-case T5 lower bound | OPEN |
| Superpolynomial Boolean SAT lower bound and P != NP | OPEN |

**Next:** require TMR-2/TMR-4 invariants to treat exact multiplicity, polynomial transfer-elimination, and existential decision as distinct resources even under bipartite-DAG promises.

## Primary references

[1] Bang-Jensen, Hell, MacGillivray (1988), *The Complexity of Colouring by Semicomplete Digraphs*. https://doi.org/10.1137/0401029

[2] Dyer, Greenhill (2000), *The Complexity of Counting Graph Homomorphisms*. https://doi.org/10.1002/1098-2418%28200010/12%2917%3A3/4%3C260%3A%3AAID-RSA5%3E3.0.CO%3B2-W

[3] Hell, Nesetril (1990), *On the Complexity of H-Coloring*. https://doi.org/10.1016/0095-8956(90)90132-J
