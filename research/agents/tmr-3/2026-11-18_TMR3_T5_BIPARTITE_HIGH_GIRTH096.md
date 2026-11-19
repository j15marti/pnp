# TMR-3/096: bipartite high-girth physical-critical T5 CSP

**Date:** 2026-11-18 Pacific. **Owner:** TMR-3 / PNP Time-Space Tradeoffs.
**Status:** PROVED (existence/extremal); COMPUTATIONAL (finite audits); OPEN (general intrinsic-critical witness lower bounds and FLMV transfer). P vs NP OPEN.

## Theorem 1 (PROVED)
For every integer g>=7 there exists a **connected, physical-arc-minimal T5-UNSAT directed simple graph H** whose underlying graph is bipartite, whose undirected girth is >g, and whose vertex count is 2^{O(g)}. Every physical arc deletion H-e is SAT. No polynomial-time construction or witness-search lower bound is asserted.

**Proof.** Existence and order bounds for five-regular graphs with prescribed girth imply a five-regular graph X with girth>g and |X|=2^{O(g)} [1,2]. Take one connected component B of its bipartite double cover. Then B has n vertices and m=5n/2 edges, is bipartite, and retains girth>g. Orient the edges independently and uniformly. Because T5 is a loopless tournament, a proper five-coloring x satisfies exactly one of the two orientations of each underlying edge, with probability 2^{-m}; a nonproper coloring never satisfies. Therefore the exact expectation is

    E[Z_T5(orientation B)] = P_B(5)/2^m <= (5/sqrt(32))^n < 1.

An UNSAT orientation exists, and a random orientation is UNSAT with probability at least 1-(5/sqrt(32))^n. Keep an inclusion-minimal UNSAT set of its **physical arcs**, and discard isolates. This is connected (otherwise one component makes the others redundant), still bipartite, still girth>g, and arc-minimal UNSAT. Finding this minimal arc set may involve NP-hard SAT/UNSAT tests; the existence proof does not supply an efficient uniform generator.

## Theorem 2 (PROVED)
Let f_bip(g) be the minimum nonisolated vertex count among such physical-critical bipartite oriented graphs of girth>g. Then

    3*2^floor((g-3)/6)-2 <= f_bip(g) <= 2^{O(g)}.
    Consequently f_bip(g)=2^{Theta(g)}.

**Proof.** An arbitrary directed degree-two thread of L edges has endpoint support equal to an affine translate of {0,2,...,2L} in Z5. Length>=4 has all five endpoint differences, and thus cannot occur in a physical-edge-minimal UNSAT graph. A connected degree<=2 graph is a path or cycle, both T5-SAT, so there are branch vertices. Suppress all degree-two threads: the core has minimum degree three, each core edge represents at most three original edges, and with girth>g>=7 the core has no parallel edges. Any core cycle of length l lifts to an original cycle of length <=3l. Put r=floor((g-3)/6). No core cycle has length <=2r+1, so a radius-r breadth-first ball in the min-degree-three core has at least 1+3(2^r-1) distinct branching vertices. The original graph contains these vertices. Theorem 1 supplies the matching exponential-in-g order upper bound. This is a **size/girth** theorem, not a lower bound on witness computation as a function of input n.

## Finite intrinsic-critical witness control (COMPUTATIONAL)
The source is the 80-vertex, 160-edge degree-four, girth-eight incidence graph of the symplectic generalized quadrangle W(3,3), with 40 points and 40 totally isotropic projective lines over GF(3). An acyclic seeded orientation is UNSAT. After 160 **charged** exact SAT minimization calls, its critical directed subgraph has **31 vertices, 42 arcs, girth 8, bipartite underlying graph, acyclic orientation, biconnectivity, 19 branch vertices, and cycle rank 12**. Its 30 degree-two threads have lengths 1:20, 2:8, 3:2.

The complete five-bit-domain reference tested H as UNSAT, constructed and individually verified every one of **42 SAT witnesses for H-e**, and confirmed each such witness violates the deleted physical arc. Root-fixed solver search nodes range **8..36** per deletion (707 combined). The deterministic program passed 652 counted assertions and two executions had identical logical audit records. Short-path support enumeration checked all 512 subfamilies of nine relations (largest irredundant intersection four); 512 K(3,3) orientation controls were also solved.

An **independently implemented 0-1 ILP reduction**, solved by SciPy/HiGHS, confirmed H infeasible and all 42 H-e feasible. This is independent computational verification, not mathematical peer review. The complete local reproducibility package retains the full 42-coloring ledger and original 80-vertex generator; the repository smoke executable authenticates the compact 31-vertex graph and all physical edge deletions.

## Time-space and quantifier gate
For any explicitly encoded connected promised H-e, the previous binary spanning-tree enumeration yields at most 2^(n-1) candidates, with complete graph input access, verification, reconstruction and output charged. A conservative simultaneously accounted sequential-tape upper bound is T(N)=O((N+1)^8 (1+2^(n-1))), S_peak(N)=O((N+1)^3) bits. It is an **upper bound**, not a native TM benchmark. The finite node counts likewise do not establish a general lower bound. FLMV applies to SAT recognition in its model [3], not automatically to this SAT-only promise witness search. No valid all-witness promise reduction is known.

**Four gates retained:** source-faithful; no claimed P/NP separation; simultaneous time-space accounting; no representational/structural-to-all-algorithm lower-bound inference. All easy-family and algebraic controls remain live.

**Next blocker C3-T5-BIPARTITE-PROMISE-TRANSFER097:** construct and authenticate a uniform physical-critical high-girth family efficiently, or prove a promise-correct SAT-witness hardness transfer without free UNSAT tests, while red-teaming propagation, GF(5), treewidth, flow, branching and compact circuits.

[1] Sachs 1963, https://doi.org/10.1112/jlms/s1-38.1.423
[2] Lazebnik, Ustimenko, Woldar 1997, https://doi.org/10.37236/1328
[3] Fortnow, Lipton, van Melkebeek, Viglas 2005, https://doi.org/10.1145/1101821.1101822
