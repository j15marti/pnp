# TMR-1/098: Planar, bounded-degree, balanced bipartite T5-CSP is NP-complete

**Owner:** TMR-1 / PNP Machine Model Lead. **Date:** 2026-11-18 13:56 PST (scheduled research). **Status:** arbitrary-size theorem with explicit construction, primary-source verification, and finite computational audits. Independent proof review / formal kernel / complete LaTeX build remain OPEN. P versus NP OPEN.

## Primary-source input, verified independently
Johnson, Martin, Oostveen, Pandey, Paulusma, Smith and van Leeuwen, *Complexity Framework for Forbidden Subgraphs I: The Framework*, Algorithmica 87 (2025), 429–464, published 2025-01-05, DOI https://doi.org/10.1007/s00453-024-01289-2, Appendix B, **Theorem 22**: **undirected C5-Colouring is NP-complete even for planar simple subcubic graphs**. This exact restriction, not generic 3-colourability, is the hardness source. The proof in the paper uses a flower gadget to reduce vertex degrees. See https://link.springer.com/article/10.1007/s00453-024-01289-2 .

## Theorem C1-T5-PLANAR-DEG6-098
Let T5 be the five-element circulant tournament with R(x,y)=1 iff y-x mod 5 is in {1,3}. Deciding whether an input digraph admits a homomorphism to T5 is NP-complete **even when every instance is a loopless planar oriented bipartite digraph**, every vertex has equal indegree and outdegree, **indegree and outdegree each at most three** (total undirected degree at most six), and every arc is in exactly one member of a partition of the arcs into directed 4-cycles. Every auxiliary vertex has indegree=outdegree=1. No maximum-directed-path-length bound is asserted for this construction.

### Explicit gadget / counting audit
Take a simple undirected planar subcubic source graph H=(V,F), n=|V|, m=|F|. Order each edge {u,v} as u<v. For that edge create exactly two fresh vertices a_e,b_e and four directed arcs

u -> a_e -> v -> b_e -> u.

All four arcs comprise one directed 4-cycle. The resulting D(H) has **N=n+2m vertices, M=4m arcs**.

Let P(x,y)=sum_{z in Z5}R(x,z)R(z,y), the number of forward two-step extensions. In difference order d=y-x mod 5,

P(d)=(0,1,1,0,2).

The independent backward path from y to x contributes P(-d). Therefore

Q(d)=P(d)P(-d)=(0,2,0,0,2).

Thus every original undirected edge is satisfied iff the endpoint colors differ by +1 or -1 mod 5, exactly the edges of undirected C5; **each allowed endpoint pair has exactly two choices for (a_e,b_e)**. This is both an existence equivalence and a precise count transfer:

**#Hom(D(H),T5) = 2^m #Hom(H,C5).**

Every satisfying target witness restricts to a valid source coloring. Every source coloring extends in 2^m target ways. This is not parsimonious, but it is decision-, witness-, and exact count-factor-preserving. The constant factor is explicitly computable and does not show #P-hardness on the planar subcubic class without an independently justified source counting theorem.

### Restricted-output promises
- **Planar:** in a fixed planar embedding of H, replace a narrow neighborhood of each original edge by two internally vertex-disjoint paths between its endpoints. A planar 4-cycle fits in the same neighborhood, and disjoint edge neighborhoods do not cross.
- **Bipartite:** put all original vertices in one part and all introduced a_e,b_e in the other. Each arc crosses this bipartition.
- **Balanced and bounded degree:** each source vertex v gains one incoming and one outgoing arc per incident undirected source edge, so indeg(v)=outdeg(v)=deg_H(v) <=3. Each auxiliary vertex has indeg=outdeg=1. Thus total degree <=6.
- **Oriented, with arc-disjoint C4 partition:** each edge gadget is a directed simple 4-cycle, the only arcs added. No opposed arc pairs or self-loops arise.
- **Connected case:** if H is connected and has >=1 edge, D(H) is strongly connected, although the unconditional NP-completeness statement does not depend on this extra promise.
- **Malformed canonical inputs:** a deterministic source parser maps any invalid graph word to D(K3), the fixed planar, subcubic, balanced, bipartite NO instance. K3 has no homomorphism to the triangle-free undirected C5. Thus the reduction is total and its outputs always obey the restrictions. Empty H is mapped to empty D(H), with one solution.

Membership in NP follows by a 3-bit-per-vertex T5 witness and checking each arc. Combined with the published planar subcubic C5-colouring theorem, this proves NP-completeness of the restricted T5 decision problem.

## Exact bit-length and SAME_REALIZATION audit
Use the existing canonical graph encoding, including unary n,m headers and two fixed-width addressed endpoints per edge, where w(k)=max(1,ceil(log2(max(2,k)))). The exact valid-source and target bit lengths are

L_H=n+m+2+2m*w(n),
L_D=n+6m+2+8m*w(n+2m).

By subcubicity 2m<=3n, hence N=n+2m<=4n and w(N)<=w(n)+2 for n>=1. Consequently

L_D <= n+22m+2+8m*w(n)

and

7L_H - L_D >= 6n + (6w(n)-15)m + 12 >= 0.

The last expression is nonnegative when w>=3 directly; if w=2 it is >=(3/2)n+12 by m<=3n/2; for w=1 (n<=2), m<=1. The n=0 case is immediate. Therefore **L_D <= 7L_H** for all valid planar subcubic source encodings. For malformed words of bit length L, output the fixed finite D(K3), giving an affine bound L_out <= 7(L+1)+O(1), with fixed constants if necessary.

A single deterministic sequential binary machine can parse the source, check degree and unique undirected edges, emit the target canonically (renumber and sort its 4m arcs), and recover/reconstruct witnesses in conservative simultaneous polynomial time O((L+1)^4) and peak writable space O((L+1)^2). Both are upper bounds, with all output, addresses, copying, parsing, sorting, and work tape charged in the same machine model. The expansion theorem says nothing about a deterministic superpolynomial time lower bound.

## Executed COMPUTATIONAL verification
The dependency-free Node.js certificate exhaustively checks all 25 endpoint pairs for the four-cycle Q(d) identity; all simple undirected subcubic graphs through six vertices (12,912 structural cases) for bipartiteness, exact degrees, balance, counts of vertices/arcs and the 7-fold canonical bit-length bound; all 844 subcubic source graphs through five vertices for direct source assignment counts and gadget product counts (2,441,056 source assignments); and direct complete target enumeration for 90 small instances. **386,508 assertions, zero failures.**

An independent Python 3.12 / NetworkX 3.6.1 planarity audit tested the same 12,912 subcubic graphs: **12,902 were planar and their corresponding targets were planar; zero source-planar/target-nonplanar violations**. The largest measured expansion ratio among these planar test graphs was **6.5**, on K4. The proof for arbitrary size is the narrow-edge-neighborhood embedding, not finite tests.

Certificate: experiments/tmr/tmr1_t5_planar_degree098_certificate.js
Raw: results/raw/tmr/2026-11-18_TMR1_T5_PLANAR_DEGREE098_RAW.json
Living manuscript: main1_PNP_MACHINE_MODEL_LEAD.tex

## Scope and research relevance
This strengthens the /089 four-cycle construction by transferring **planarity and bounded-degree NP-hardness**, verified against an exact 2025 primary-source theorem. Balanced, bipartite, planar, locally low-degree, four-cycle decomposable graph structure alone cannot be a universal efficient-solvability criterion. Conversely, every such output exposes local 4-cycle gadgets that may be contracted, so these restrictions **do not supply a general lower-bound mechanism** and cannot forbid cheap source-aware preprocessing, local consistency, Fourier, Gaussian/algebraic special cases, bounded-treewidth DP, polymorphism methods or alternate encodings.

Next: explore hard image instances under gadget-blind algorithmic compression and consider stricter maximum indegree/outdegree <=2 or width bounded by O(sqrt n) for planar graphs; respect planar separators and all known efficient algorithms. Independent mathematical review, full LaTeX compilation, formal kernel reconstruction outstanding. **P versus NP OPEN.**
