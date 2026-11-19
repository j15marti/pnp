# TMR-5/090: native 2-connected T5 ladders falsify a partition-rank-to-work inference

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Date:** 2026-11-18 (Pacific). **Status:** symbolic proof and independent reproducible computation, scoped. External mathematical review/formal kernel OPEN. P versus NP OPEN.

## Primary-theorem checkpoint

The exact fixed template is the loopless tournament on Z5 with R(a,b) iff b-a mod 5 belongs to {1,3}. T5 is a core: adjacent vertices of a loopless complete tournament cannot be identified by an endomorphism. Each vertex has indegree and outdegree two, and T5 is not a directed cycle. The Barto-Kozik-Niven no-sources/no-sinks dichotomy (SIAM J. Computing, 2009, doi:10.1137/070708093) directly implies NP-completeness. The Bang-Jensen-Hell-MacGillivray semicomplete-digraph theorem (SIAM J. Discrete Mathematics, 1988, doi:10.1137/0401029) also applies. Neither establishes an unconditional superpolynomial deterministic time lower bound.

## Native-input theorem: bad-order rank is exponential, optimal-order computation is easy

For each h>=1 let m=3h+1. Take vertices t_i,b_i (0<=i<m) and exactly the directed T5 constraints t_i->b_i (rungs), t_i->t_(i+1) (top rail), and b_i->b_(i+1) (bottom rail). There are n=6h+2 vertices and e=9h+1 arcs. The directed graph is acyclic. Its undirected graph is bipartite, has maximum degree three, treewidth two, is 2-vertex-connected (the outer cycle visits every vertex), and has cycle rank 3h. There are NO gadget or pinning constraints.

**Exact counting.** There are ten rung states (a,b) satisfying R(a,b). From each one, precisely three next-column rung states (a',b') obey R(a,a'), R(b,b'), and R(a',b'). Proof: letting d=b-a in {1,3}, the choices delta_a=a'-a, delta_b=b'-b in {1,3} have exactly three of four combinations with d+delta_b-delta_a in {1,3}. Thus

    Z(L_m)=#Hom(L_m,T5)=10*3^(m-1)=10*3^(3h).

A ten-state transfer computes this exactly using O(m) fixed-size arithmetic operations, with O(m)-bit intermediate integers. A five-valued ordered decision diagram (MDD) in order t_0,b_0,t_1,b_1,... has width at most **51**: retain the previous valid rung pair (10 possibilities) and, between assigning the next top and bottom symbols, that pair plus the new top symbol (at most 50), plus a rejection sink. For a literal **Boolean OBDD**, encode each symbol in three consecutive bits with unused codes 5,6,7 rejected. There are at most 10 previous-rung states, 8 top-bit prefixes, 8 bottom-bit prefixes, and a rejecting sink, giving Boolean OBDD width at most **641**, independent of h. This grouping also provides a bounded-boundary tensor contraction and an adaptive FBDD; direct counting is polynomial in bit time.

**Top-row-first cut-rank theorem.** Now use variable order t_0,...,t_(m-1),b_0,...,b_(m-1). Restrict its top/bottom assignment-indicator matrix to 2^h top strings indexed by alpha in {0,1}^h and 2^h bottom strings indexed by beta in {0,1}^h. For each k=0,...,h-1 set

    t_(3k)=0, t_(3k+1)=1 if alpha_k=0 else 3, t_(3k+2)=4, t_(3k+3)=0,
    b_(3k)=1, b_(3k+1)=2 if beta_k=0 else 4, b_(3k+2)=0, b_(3k+3)=1.

All horizontal edges and all anchor rungs are satisfied. The only variable test, at column 3k+1, is

    Q = [ R(1,2) R(1,4) ] = [ 1 1 ]
        [ R(3,2) R(3,4) ]   [ 0 1 ].

Consequently the restricted 2^h-by-2^h matrix equals the h-fold Kronecker product Q^(tensor h). Since det(Q)=1, its rank is exactly 2^h over every field, including GF(2) and GF(5). The full assignment-indicator top/bottom cut matrix has rank at least 2^h. Since distinct residual functions must occupy distinct states of any deterministic OBDD with top-row-first variable order, **that order requires width at least 2^h**. This is a native-T5 indicator rank lower bound, not a projected C5 or gadget statistic.

**Authentic input recognition.** The orientation has a unique indegree-zero source t_0. Try its two outgoing neighbors as b_0, follow the row-forward arcs, and check the entire recovered arc set. At most two walks, O(n+e). Thus after arbitrary vertex relabeling, a uniform direct algorithm recognizes and counts this family in polynomial time without advice about its names.

## Independent execution and safeguards

The separately executed compact verifier [Python](../../experiments/tmr/tmr5_090_ladder_obdd_compact.py) confirms six exhaustive-backtracking vs ten-state transfer comparisons for m=2..7, the exact counts 30,90,270,810,2430,7290, and all 87,380 entries in the Kronecker-minor test for h=1..8, with full rank 2^h over GF(2), GF(3), and GF(5), zero assertion failures. A larger standalone verifier additionally passed 180 randomized vertex relabelings and complete reconstructed-arc checks, and verified extensions of every selected top prefix. The original full source, raw JSON, stdout, and complete mathematical report are in the conversation evidence ZIP. The compact repository verifier was executed locally before publishing. This finite evidence checks the symbolic proof but is not a substitute for external review.

## Ranked dependency update

| Chain step | Status |
|---|---|
| Specific T5 fixed-template CSP NP-completeness | **PROVED** by primary theorem; does not resolve P versus NP |
| TMR-1 five-arc C5-to-T5 gadget | **PROVED, restricted** in prior audits, not used here |
| Native ladder rank >=2^h at one cut | **PROVED, restricted** over all fields |
| Top-row-first fixed OBDD width >=2^h | **PROVED, restricted** |
| Interleaved five-way MDD width <=51; encoded binary OBDD <=641; exact counting in polynomial bit time | **PROVED, restricted** |
| A large rank across a fixed cut forces algorithm-independent work | **FALSIFIED** for this native family |
| Global cycle rank requires exponential work | **FALSIFIED** as an instancewise claim |
| Arbitrary-order/adaptive/tensor/general CSP worst-case lower bound | **OPEN** |
| Transfer to a Boolean-SAT superpolynomial lower bound | **OPEN** |
| P versus NP | **OPEN** |

**Next gate:** TMR-2/TMR-4 must take the minimum over legal variable orders, adaptive decompositions and source-aware global algorithms. A hard single partition, even with rank over every field, is not necessary machine work.

References: [1] Bang-Jensen J, Hell P, MacGillivray G, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1988;1(3):281-298, https://doi.org/10.1137/0401029. [2] Barto L, Kozik M, Niven T, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Comput. 2009;38(5):1782-1802, https://doi.org/10.1137/070708093.

No peer manuscripts, agent identities, schedules, ownership, safeguards or PR merge state were changed.
