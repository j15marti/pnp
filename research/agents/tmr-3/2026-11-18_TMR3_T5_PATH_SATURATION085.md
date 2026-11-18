# TMR-3/085: Four-step saturation and high-width padding falsifier

**Owner:** TMR-3 / PNP Time-Space Tradeoffs. **Date:** 2026-11-18 PT.
**Status:** exact restricted decision algorithm, source-derived infinite-family counterexample, not an unrestricted resource lower bound. **P versus NP OPEN.**

## Theorem 085A: exact T5 walk kernel

With symbols Z5 and arc relation y-x in {1,3}, let M be the target adjacency matrix. Its powers count fixed-endpoint extensions along directed paths with private internal vertices. The first rows of M, M^2, M^3 and M^4 are

    (0,1,0,1,0)
    (0,1,1,0,2)
    (3,0,3,1,1)
    (4,4,1,6,1).

Every entry of M^4 is positive, while none of the preceding powers is all-positive. Thus T5 has primitive exponent exactly 4. Let w=(4,4,1,6,1). If a directed four-edge path u->p->q->r->v has three private internal vertices with no other incident arcs, then deleting the path preserves *satisfiability*, because every assignment of its two endpoints extends. For *counting*, deleting the path without adding a binary factor is invalid: the exact factor is w(x_v-x_u). Consequently for the complete four-subdivision S4(H) of any directed base graph H,

    Z(S4(H))=sum_{x in Z5^{V(H)}} prod_{(u,v) in E(H)} w(x_v-x_u).

This identity counts colorings of every original source vertex, including subdividing vertices.

## Theorem 085B: high-width easy family, verified from original source

Take the directed k-by-k toroidal grid H_k (k>=3), with right/down arcs modulo k. It has k^2 vertices, 2k^2 arcs, and total incident degree four at each vertex. Replace each arc with a length-four directed path having three private vertices. The resulting source G_k has

    n=7k^2, m=8k^2, cycle rank=m-n+1=k^2+1.

By contracting path interiors and deleting torus wraparound edges, the underlying graph has the ordinary k-by-k grid as a minor. Hence tw(G_k)>=k. Nevertheless G_k is always T5-SAT: assign color 0 to all core vertices, and colors (1,4,2) to the three private vertices on every directed path. Every path is then (0,1,4,2,0), with allowed increments (1,3,3,3).

These source graphs are *recognizable without an external certificate*: core vertices have total degree four, private vertices indegree=outdegree=1. Trace every outgoing arc from every core for four steps, check three distinct private internal vertices, a core endpoint, and exact coverage of all source arcs/vertices. On accepted inputs, adjacency-list recognition and exact witness construction take O(n+m) RAM operations. One deterministic sequential-tape realization, with the original encoded source length N, has conservative **simultaneous** upper bounds T=O((N+1)^4), S_peak=O((N+1)^2) bits including source access, validation, tape seeks, addresses, output and witness verification. Its exact fallback for arbitrary inputs is T=O((N+1)^4 5^n), S_peak=O((N+1)^2) bits, using backtracking. These are charged symbolic *upper bounds*, not native microcode results.

## Theorem 085C: connected difficulty-preserving padding

For any connected original T5 input F with marked vertex v, attach G_k through one additional directed four-edge path from v to any torus core vertex. The padded input P_k(F) is satisfiable iff F is satisfiable: restriction proves one direction; for the other, extend each coloring of F by making all torus core vertices have the color of v and using relative offsets (1,4,2) on every length-four path. Thus arbitrary original SAT and UNSAT instances can be padded to arbitrarily large primal treewidth and cycle rank *without changing their answer*. This is not an algorithm for solving the unpadded hard core; it rules out source-width/representation-size alone as an algorithm-independent lower-bound certificate.

## Executed checks and numerical controls

The complete local reference implementation passed **283 audit groups in each of two byte-identical runs, zero failures**. These included each ordered endpoint color pair for path lengths 1..5; direct exact original-coloring counts on four small subdivided graphs; recognized K4 subdivision controls; connected SAT and UNSAT padding controls; 144 seeded arbitrary-graph brute-force comparisons (n<=6), and explicit torus witnesses.

For k=3..8, the observed tuples (k,n,m,cycle_rank,base min-fill width,BFS-dual min-fill width,DFS-dual min-fill width) were:

    (3,63,72,10,6,8,9)
    (4,112,128,17,9,15,16)
    (5,175,200,26,14,24,25)
    (6,252,288,37,17,34,36)
    (7,343,392,50,20,47,49)
    (8,448,512,65,25,61,64).

The min-fill numbers are **observed achieved widths**, not proven minima across all elimination orders or spanning trees. The only claimed unbounded lower bound is tw(G_k)>=k from the grid minor. A 70,000-vertex/80,000-arc original source (k=100) had a verified explicit T5 witness.

Complete local reference Python SHA256: e6ddda1cd65162dae728907061a6fe456c6051c586ee4a72e9ecd8ded1fbd7f6.
Complete local audit SHA256: 3ad5a21f9f9b7511d5cd80aef802dbd714507019d2743e35e8ab4cdf280911bc.

## Verification gates and next dependency

DISJ: restricted PASS against width-only hardness claims. Relativization: NOT APPLICABLE to any separation. Simultaneous DTISP: restricted PASS as one charged constructive upper bound. Configuration-counting: PASS as upper-bound consistency only, never an algorithm-independent space lower bound. Prior easy-family and original-source validation safeguards remain mandatory.

**Next:** C3-T5-IRREDUCIBLE-CORE086. Delete every independently recognized private four-path, carry the positive factor only for counting, and search for a certified hard candidate with no such vacuous padding and with large primal and optimally tested dual representations. Do not infer a P-vs-NP theorem from finite computation.

**References:** Bang-Jensen, Hell and MacGillivray (1988), https://doi.org/10.1137/0401029; Brualdi and Liu (1990), https://doi.org/10.1002/jgt.3190140413; Demaine and Hajiaghayi (2008), https://doi.org/10.1007/s00493-008-2140-4.
