# TMR-1/097: Sharp DAG-height decision threshold and one-query height-one counting hardness

**Owner:** TMR-1 / PNP Machine Model Lead. **Date:** 2026-11-18 12:56 PST.
**Status:** Two elementary, arbitrary-size theorems. Finite computational certificate executed independently. Peer review, whole-manuscript compilation and formal-kernel reconstruction remain OPEN. **P vs NP OPEN.**

## Exact model
Use the fixed tournament \(T_5=(\mathbb Z_5,R)\), \(R(x,y)=1\) iff \(y-x\bmod5\in\{1,3\}\). An input is an arbitrary finite directed constraint graph. Its *directed height* is the maximum arc count along any directed path in a DAG, not undirected treewidth.

## Theorem C1-T5-HEIGHT-097 (sharp decision threshold)
Every directed acyclic input of height at most two has a satisfying assignment computable in linear word-RAM time. In contrast, T5-CSP remains NP-complete on inputs of height at most three, indeed height exactly three on the nontrivial flattening images.

**Proof:** Topologically process a DAG, defining \(h(v)\) as the longest directed path ending at \(v\), with sources at level 0. For an arc \(u\to v\), \(h(u)<h(v)\). If maximum height is two, only level pairs \((0,1),(0,2),(1,2)\) can occur. Color levels 0,1,2 respectively **0,3,1**: \(R(0,3)=R(0,1)=R(3,1)=1\). This labels every arc correctly. Parsing a canonical source and computing the levels has polynomial bit-machine time and space; no reduction is silently free.

For hardness at height three, the already established parsimonious /096 equality-gadget reduction takes general T5-CSP to a four-layer DAG with \(N=n+3k\) vertices, \(M=m+5k\) arcs and encoded length at most \(28L\). It has exactly the original number of satisfying assignments. When the original graph has an arc \(u\to v\), the image has a length-three path \(p_u\to q_v\to a_v\to b_v\), so its height is **exactly three**. General T5-CSP is NP-complete by Bang-Jensen, Hell and MacGillivray [1]. Membership in NP is immediate from 3-bit per vertex witnesses.

**Sharp small obstruction:** The transitive tournament \(TT_4\) on four vertices with all arcs \(i\to j\), \(i<j\), is a height-three DAG with no homomorphism to T5, because T5 has no transitive induced subtournament on four vertices. Every four-subset of T5 contains a directed triangle; by rotational symmetry check the complement of vertex 0, where \(2\to3\to4\to2\). By contrast \(TT_3\) has exactly five homomorphisms, including \((0,3,1)\).

## Theorem C1-T5-HEIGHT1-COUNT-097 (one-query metric #P hardness)
Although **every** height-one DAG is satisfiable, exact counting of T5 homomorphisms on the restricted family is #P-complete **under polynomial-time metric counting reductions**. The reduction makes one counting-oracle query. No parsimonious or constant-factor encoded-length reduction is claimed.

The primary Dyer-Greenhill theorem [2,3] establishes #P-completeness of counting homomorphisms from simple undirected graphs into undirected \(C_5\).

Given an undirected simple graph \(H\) with \(n\) vertices and \(m\) edges, set \(k=\max(1,3n)\). Keep one source-layer vertex for each vertex of H. For each edge \(e=\{u,v\}\), create \(k\) separate sink vertices \(s_{e,j}\) and edges \(u\to s_{e,j}, v\to s_{e,j}\). The resulting loopless bipartite input \(D_k(H)\) has
\[
N=n+km,\qquad M=2km,
\]
with no paths longer than one edge and every sink indegree exactly two. A witness always exists: all sources color 0, all sinks color 1.

For fixed source colors \(x,y\), the number of valid shared outneighbors is
\[
S(x,y)=\sum_z R(x,z)R(y,z)
=\begin{cases}
2&x=y,\\
1&y-x\pmod5\in\{2,3\},\\
0&\text{otherwise}.
\end{cases}
\]
The first row is [2,0,1,1,0]. Let \(P_H(z)=\sum_{j=0}^m a_jz^j\), where \(a_j\) counts original vertex colorings in which every edge is either monochromatic or has difference \(+2/-2\), and precisely \(j\) edges are monochromatic. Each coefficient satisfies \(0\le a_j\le5^n\). By independently summing the \(k\) sink variables per source edge,
\[
\#\mathrm{Hom}(D_k(H),T_5)=P_H(2^k).
\]
The coefficient \(a_0\) equals \(\#\mathrm{Hom}(H,C_5)\), because edges of difference \(\pm2\) form an undirected five-cycle, isomorphic to the usual \(\pm1\) cycle. Since \(2^k>5^n\) (including \(n=0\)), no higher base-\(2^k\) digit contributes to the least significant digit:
\[
\boxed{\#\mathrm{Hom}(H,C_5)=\#\mathrm{Hom}(D_k(H),T_5)\bmod2^k.}
\]
This is a **single-query exact metric reduction** with polynomial-time postprocessing. Its output length is polynomial but not constant-factor relative to H. In the canonical directed bit encoding, with \(w(t)=\max(1,\lceil\log_2\max(2,t)\rceil)\),
\[
L_D=N+M+2+2Mw(N)=n+3km+2+4kmw(n+km).
\]
For \(n\ge1\), \(N=n+3nm\), \(M=6nm\), so \(L_D=O((n+m+1)^2\log(n+m+2))\). The count oracle output is below \(5^N\), thus has \(O(N)\) bits; taking the remainder is polynomial-time on the SAME_REALIZATION sequential bit model. Malformed source graph encodings are rejected without an oracle query. Counting membership in #P is by a standard polynomial witness verifier, and hardness is **only** asserted under the stated metric reduction. Decision is trivial while counting is #P-hard.

## Verification, falsification and limits
The independently executed local Node.js verifier checked 33,868 topologically ordered DAGs through six vertices (12,356 height-two-or-less), all 1,100 simple undirected graphs through five vertices, 5,149 small-base polynomial evaluations, 1,100 one-query modular recoveries, 24 directly enumerated T5 target counts, all 25 common-outneighbor entries, and \(TT_3/TT_4\). **34,315 assertions, zero failures.** The separately executed short public replay checked **14,582 assertions, zero failures**. These finite experiments are **COMPUTATIONAL** and do not replace the symbolic proofs.

This strengthens a tractability boundary and supplies a counting/decision separation, **not** a superpolynomial lower bound. General polynomial-time algebraic, Gaussian-on-restricted-inputs, Fourier, polymorphism, propagation, bounded-treewidth, and alternate-representation paths remain admissible. No agent identities, schedules, ownership, or states changed. P versus NP remains OPEN.

## References
[1] J. Bang-Jensen, P. Hell, G. MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J Discrete Math 1 (1988), 281-298. https://doi.org/10.1137/0401029

[2] M. Dyer, C. Greenhill, *The Complexity of Counting Graph Homomorphisms*, Random Struct Algorithms 17 (2000), 260-289. https://doi.org/10.1002/1098-2418(200010/12)17:3/4%3C260::AID-RSA5%3E3.0.CO;2-W

[3] M. Dyer, C. Greenhill, *Corrigendum*, Random Struct Algorithms 25 (2004), 346-352. https://doi.org/10.1002/rsa.20036
