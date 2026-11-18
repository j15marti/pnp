# TMR-1/081: Exact oriented-cactus counting and source-reduction boundary
Date: 2026-11-17 21:56 PST. Status: symbolic proof for restricted source, independent review OPEN; finite checks COMPUTATIONAL. P versus NP OPEN.

## Theorem: oriented cactus is always satisfiable
Fix T5 on Z5, R(a,b)=1 iff b-a modulo 5 belongs to {1,3}. For a canonical directed graph G with no loop, opposed arc pair or duplicate, suppose its underlying undirected graph is a simple cactus, meaning every undirected edge belongs to at most one simple cycle. Let c be the number of weak components, b be the number of bridges, and C_j the cycle blocks. Choose either traversal of C_j, recording p_j agreeing arcs and q_j opposing arcs. Set

    Q(p,q)=sum_{i=0}^p sum_{j=0}^q binom(p,i)binom(q,j)
             * [p-q+2(i-j) is 0 modulo 5].

Then exactly

    #Hom(G,T5)=5^c * 2^b * product_j Q(p_j,q_j).

Every Q(p,q) is positive when p+q>=3. Hence every orientation of every simple undirected cactus is T5 satisfiable. A self-loop or opposed arc pair makes any directed T5 instance unsatisfiable, regardless of cactus structure. Malformed canonical input is not silently accepted. On noncactus inputs, the algorithm returns OUTSIDE_CACTUS, not an invented count.

## Symbolic proof
For a simple cycle with p forward and q backward arcs, each forward displacement is 1 or 3 and each backward displacement is -1 or -3 modulo 5. Choosing the larger absolute displacement on i forward and j backward arcs yields cycle displacement p-q+2(i-j), with binomial multiplicity. Thus Q counts completing assignments for any prescribed cycle-root color. Every integer t in [-q,p] can be realized as i-j. If p+q>=4 this interval contains five consecutive residues and hence a t satisfying the modular equation. If p+q=3, for p=3,2,1,0 choose t=1,2,-2,-1, respectively. Every cycle can therefore be completed.

Decompose a cactus into its block-cut tree. T5 has the automorphisms x to x+k modulo 5. Thus the number of completions of each connected block is independent of the label of its attachment articulation vertex. An oriented bridge gives two completions, a cycle gives Q(p,q), and an arbitrary root in each component has five choices. Multiply the block factors to obtain the formula. The same five-state DP can backtrack to emit an explicit satisfying witness. This is a proof for arbitrary cactus size, not a claim from testing.

## Theorem: five-arc source image cactus iff source forest
Let D(H) be the exact parsimonious five-arc transformation of TMR-1/080 from a simple undirected C5-coloring source H. For each undirected edge {u,v} with u<v create private a,b,c and arcs u->a, a->b, b->c, u->c, c->v. The undirected graph underlying D(H) is a cactus if and only if H is a forest.

If H is a forest, each edge gadget contributes a private four-cycle u-a-b-c-u and bridge c-v; distinct gadgets can meet only at original vertices. All simple cycles are edge-disjoint. Conversely, each undirected source cycle in H lifts through the two-edge paths u-c-v to a simple cycle in D(H), sharing u-c with the local four-cycle. Thus D(H) cannot be a cactus. For a forest with n vertices and m edges, the reduced graph has c=n-m components, m bridges, m four-cycles with Q(3,1)=1. Therefore #Hom(D(H),T5)=5^(n-m)*2^m, exactly its undirected C5-coloring count. This is an exact source/target boundary, not a lower bound.

A bouquet of k directed triangles has n=2k+1 vertices, m=3k arcs, feedback rank k, and exactly 5*3^k T5 homomorphisms. Consequently unbounded raw feedback rank does not entail mandatory exponential work. This is a cheap-path counterexample to a rank-only obstruction.

## Machine, authentication and reverse encoding
Retain the authenticated source encoding of /080: unary 1^n0 1^m0 followed by m lexicographically ordered directed endpoint pairs in low-first fixed-width w(n)=max(1,ceil(log2(max(2,n)))) bits. Exact input length is L=n+m+2+2m*w(n); each five-symbol witness uses exactly three low-first bits, disallowing codes 5,6,7. Reject malformed inputs. A sequential parser, block/cactus certifier, integer cycle counter and witness extractor have conservative *simultaneous* upper bounds T=O((L+1)^5) and peak writable space O((L+1)^3) bits, counting source validation, actual arithmetic and output.

The prior functional reverse T5-to-width-at-most-three Boolean CNF compiler uses exactly 8n Boolean variables and 20n+15m clauses for any n-vertex m-arc source, with unique Boolean extensions. The cactus tractability result transfers only with an authenticated restricted source promise. It does not solve general SAT.

## Independent finite computational checks
Full local Node verifier tmr1_t5_cactus081.js: 5,073 assertions and zero failures; 899 graph/orientation cases on n<=4, including 505 cactus and 256 noncactus; 884,831 direct assignment checks; 1,100 source graphs H with n<=5 audited for D(H) cactus iff H is a forest; additional bouquet, cycle, malformed and loop/opposed negative controls. Separately executed public certificate: 8,184 orientations of cycles length 3..12 with exact coefficient/DP agreement and Q>0, 248 brute-force cycle comparisons, exact five-arc endpoint table (0,1,0,0,1), 16,617 assertions and zero failures. The published finite certificate is narrower than the full independently executed local verifier. Finite checks are COMPUTATIONAL, separate from the symbolic proof.

## Scientific gates and next dependency
DISJ: restricted algorithm PASS only; unrestricted lower bound OPEN. Relativization: positive algorithm PASS, NP separation OPEN. SAME_REALIZATION: matching polynomial time and space upper bounds PASS, forbidden DTISP lower bounds OPEN. Configuration counting remains an upper-bound safeguard. All alternative encodings, polymorphisms, graph algorithms, Fourier/affine and Gaussian methods, local consistency, decomposition and source-aware shortcuts remain admissible. General T5 NP-completeness follows independently from Hell-Nešetřil for undirected C5-coloring plus the exact reduction, and is consistent with Bang-Jensen, Hell and MacGillivray's semicomplete-digraph theorem. The cactus block principle is classical; no literature-priority claim is made. Independent mathematical review, full LaTeX compilation and kernel-level formalization remain open.

NEXT: C1-T5-NONCACTUS-MIXED-CORE-AUDIT. Study cycle-containing YES/NO undirected source H and its D(H) images under forced-triad, block decomposition, vertex cover, separator and Fourier algorithms, with source-authenticated total costs. Even finite resistant cases do not establish all-algorithm resource lower bounds. P versus NP remains OPEN.

Primary sources: Hell and Nešetřil (1990), DOI https://doi.org/10.1016/0095-8956(90)90132-J. Bang-Jensen, Hell and MacGillivray (1988), DOI https://doi.org/10.1137/0401029.
