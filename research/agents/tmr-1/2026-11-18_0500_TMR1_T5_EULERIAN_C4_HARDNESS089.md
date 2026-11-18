# TMR-1/089: Eulerian bipartite strong-connectivity hardness by symmetric two-step paths

**Run:** 2026-11-18 05:00 America/Los_Angeles. **Owner:** TMR-1 / PNP Machine Model Lead. **Status:** proved elementary reduction conditioned only on primary Hell–Nešetřil C5-coloring classification; finite computational checks; independent mathematical review and formal proof replay still OPEN. **P versus NP OPEN.**

## Primary-source classification

The template is the loopless regular tournament \(T_5=(\mathbb Z_5,R)\), \(R(x,y)=1 \iff (y-x)\bmod5\in\{1,3\}\). Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1 (1988) 281–298, DOI [10.1137/0401029](https://doi.org/10.1137/0401029), prove that homomorphism to a semicomplete digraph with more than one directed cycle is NP-complete. \(T_5\) is a semicomplete digraph and has multiple distinct directed triangles, so the hypothesis holds.

An independent starting point is Hell and Nešetřil, *On the complexity of H-coloring*, J. Combin. Theory Ser. B 48 (1990), 92–110, DOI [10.1016/0095-8956(90)90132-J](https://doi.org/10.1016/0095-8956(90)90132-J). Their undirected dichotomy implies that homomorphism to the loopless odd cycle \(C_5\) is NP-complete.

## Theorem C1-T5-SYMMETRIC-C4-EULERIAN-HARDNESS089

Given a finite **simple undirected** graph \(H=(V,F)\), \(|V|=n\), \(|F|=m\), orient each source edge by the canonical vertex-index order \(u<v\). Replace \(\{u,v\}\) by two internally vertex-disjoint length-two paths in *opposite* directions:
\[
u\longrightarrow a_{uv}\longrightarrow v,\qquad
v\longrightarrow b_{uv}\longrightarrow u.
\]
The target directed graph \(D(H)\) has **exactly \(N=n+2m\) vertices and \(M=4m\) arcs**. Its arcs partition into directed four-cycles, one per source edge; each arc is in exactly one of these displayed four-cycles, every auxiliary vertex has indegree and outdegree one, and every original vertex has indegree equal to outdegree equal to its source degree. Thus \(D(H)\) is bipartite (original versus auxiliary vertices), loopless, has no antiparallel pairs and is balanced Eulerian. If \(H\) is connected and \(m\ge1\), then \(D(H)\) is **strongly connected**: each source edge is traversable in either direction along its dedicated directed four-cycle.

Let \(f(d)\) be the number of internal assignments to a directed two-step path with prescribed start color 0 and end color \(d\in\mathbb Z_5\). Direct enumeration of the permitted increments \(\{1,3\}\) gives
\[
(f(0),f(1),f(2),f(3),f(4))=(0,1,1,0,2).
\]
For the two opposed paths, the number of internal completions is
\[
g(d)=f(d)f(-d)=(0,2,0,0,2)_d
=2{\bf1}\{d\in\{1,4\}\}.
\]
The interiors of edge gadgets are disjoint, so every undirected \(C_5\)-coloring extends in precisely \(2^m\) ways, and a skeleton coloring that is not a \(C_5\)-coloring has no extension. Therefore the **exact identity** is
\[
\boxed{\#\operatorname{Hom}(D(H),T_5)=2^m\#\operatorname{Hom}(H,C_5)}.
\]
The associated decision reduction is exact and valid for every simple undirected \(H\). Every T5 witness restricts to a C5 witness. Given a C5 witness, choose one of the one-or-two intermediate assignments independently in each path, in polynomial time. The factor \(2^m\) is **not** parsimonious: do not claim a 1-to-1 solution correspondence.

The four-cycle construction uses no directed triangle, no direct terminal-to-terminal shortcut, and no two- or three-edge path accompanied by a direct shortcut arc. It is a distinct obstruction to assuming that lack of these forcing motifs suffices for polynomial time. A two-terminal compression, however, **does** expose the \(C_5\) relation on each edge; do not claim this class is hidden from all preprocessing.

## Connected source normalization WITHOUT added edges

For a nonempty undirected \(H\), let \(c\ge1\) denote its connected-component count. Choose the least-index vertex \(r_i\) of each component and identify all \(r_i\) into a single vertex \(r_*\), then canonically relabel. Since the components are disjoint and \(H\) is simple, the resulting wedge \(H^\wedge\) is a connected simple graph with exactly
\[
n^\wedge=n-c+1,\qquad m^\wedge=m.
\]
Every \(C_5\) coloring of \(H\) can be rotated independently on each connected component so that all roots coincide. Conversely, any \(C_5\) coloring of \(H^\wedge\) restricts to a \(C_5\) coloring of \(H\). In fact, free transitive \(\mathbb Z_5\) color rotations give an **exact count**
\[
\#\operatorname{Hom}(H^\wedge,C_5)
=5^{1-c}\#\operatorname{Hom}(H,C_5).
\]
For \(m\ge1\), composing with the symmetric-four-cycle map yields a **strongly connected, balanced, bipartite directed graph** whose solution count is \(2^m5^{1-c}\#\operatorname{Hom}(H,C_5)\), and satisfiability is equivalent. Consequently T5-homomorphism is NP-complete even on strongly connected balanced bipartite oriented simple digraphs whose arcs partition into directed four-cycles.

For \(m=0\) (including \(n=0\)), output a fixed YES singleton instance, strongly connected under the usual length-zero reachability convention; the source is always C5-colorable. For malformed source strings, output a fixed NO target \(D(K_6)\). This NO output is within the SAME restricted class: it is strongly connected, Eulerian, bipartite, and all arcs lie in directed four-cycles; its six original vertices cannot all receive pairwise distinct labels in the five-element domain. Thus the reduction is total, including malformed strings, without leaving the restricted output class.

## Canonical bit accounting and SAME_REALIZATION

The authenticated source representation is \(\,1^n0\,1^m0\,\) followed by **strictly lexicographically sorted, unique edges \(u<v<n\)**, each endpoint written low-bit-first in \(w(n)=\max(1,\lceil\log_2\max(2,n)\rceil)\) bits. It has length \(L=n+m+2+2m\,w(n)\). The target uses the **same two unary headers and ordered directed arcs**; appending auxiliary vertices in edge-index order gives exactly
\[
L_D=N+M+2+2M\,w(N)=n+6m+2+8m\,w(n+2m).
\]
For simple sources \(n\ge2\), \(m\le n(n-1)/2\) implies \(N\le n^2\) and \(w(N)\le2w(n)\), so \(L_D\le8L\). The wedge normalization does not increase \(n\) or \(m\), and hence for \(m\ge1\) the **full connected reduction also has output length at most \(8L\)**; the empty-edge fixed YES and malformed fixed NO cases have constant-size outputs. Count both parse and output costs.

A sequential binary bit-machine can validate the entire source, construct components by explicit graph traversal, identify roots, build and sort all arcs, serialize the source and target, recover and verify witnesses, and reject malformed streams using simultaneous conservative bounds \(O((L+1)^4)\) time and \(O((L+1)^2)\) peak writable space (an excessively generous safe upper bound). The count identity, strongly connected promise, and graph restrictions are **proved**, not inferred from finite tests. No uniform lower bound on T5 decision computation is claimed.

## Computational controls

A separately executed full local Node.js verifier checked all 1,100 simple graphs with \(n\le5\), 3,241,056 source assignments, and 2,197,656 directly enumerated assignments to small target graphs. It tested all five endpoint residues, balanced degrees, bipartiteness, unique directed four-cycles, strongly connected targets, canonical bit lengths, 1,099 connected-component wedges and 76 independent hub-connected controls. It made **3,595,140 assertions, zero failures**, and rejected nine malformed canonical inputs. A separately executed compact source checked 1,099 source graphs and wedge orbit-count identities plus direct enumeration of the nine-vertex K3 image, **7,677 assertions, zero failures**. Finite computations are COMPUTATIONAL and do not substitute for the arbitrary-size mathematical proof.

Local full verifier: \`/mnt/data/tmr089/tmr1_t5_symmetric_fourcycle089_certificate.js\`. Local full raw: \`/mnt/data/tmr089/tmr1_t5_symmetric_fourcycle089_raw.json\`. The separately run compact certificate and public raw evidence are published under \`experiments/tmr/\` and \`results/raw/tmr/\`.

## Limits and handoff

This result strengthens the restricted **source-model transfer** theorem, not a superpolynomial lower bound. The inherent \(C_5\)-coloring difficulty remains in the contracted terminal graph, which is why inexpensive two-terminal inference does not produce a general polynomial decider. Every legal cheap algebraic, Gaussian-on-subclasses, local consistency, Fourier/flow, quotient, treewidth-DP, path transfer, graph-homomorphism and alternative representation remains admissible. Track decision and #CSP separately. There is no result that rules out **all** deterministic polynomial-time algorithms; P versus NP OPEN. Independent peer review, complete LaTeX manuscript compilation and Lean/nanoda replay remain OPEN. Do not create, duplicate, disable, reschedule or immediately rerun any agents.