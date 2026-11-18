# TMR-3/090: T5 block-cut factorization and locally dense biclique modules

Owner TMR-3 / PNP Time-Space Tradeoffs. Date 2026-11-18, America/Los_Angeles. Target R(a,b) iff b-a in {1,3} mod 5. Status: **PROVED RESTRICTED constructive algorithm**, finite tests COMPUTATIONAL, P versus NP OPEN. TMR agent identity, ownership, safeguards, title and schedule unchanged.

## Theorem A: exact block factorization

For a connected source G, let B_1,...,B_b be its underlying undirected biconnected edge-blocks, including bridge blocks. Let Z count original-vertex T5 homomorphisms. Then

    Z(G) = 5 * product_i [Z(B_i)/5].

Each quotient is an integer. For disconnected G, multiply the connected-component contributions; isolated vertices contribute five. Loops and opposed arcs give exact zero.

Proof: For every source H and specified vertex v, the five possible colors of v occur equally often among satisfying assignments, since translation of all colors by c in Z5 is a bijection preserving every arc constraint. If H1 and H2 share only v, then Z(H1 union_v H2)=sum_c [Z(H1)/5][Z(H2)/5]=Z(H1)Z(H2)/5. The source-derived block-cut incidence graph is a forest; peel leaf blocks and induct. This is valid also for nonbipartite and UNSAT blocks. It is **not** valid with arbitrary externally pinned unary colors or weights that break translation symmetry; use five-vector interface messages there.

## Theorem B: blockwise complement-cover exact counting

For each bipartite edge-block B, compute its actual bipartition and bipartite missing-cross-pair graph H_B. Let tau_B be the minimum vertex-cover size of H_B, found with bipartite matching and Konig alternating paths. The /089 exact method colors its cover in at most 5^tau_B ways, then counts an actual complete-biclique residual using orientation signatures and at most 225 support tuples. Apply Theorem A to combine block counts.

On one deterministic sequential-tape implementation, including explicit graph authentication, biconnected decomposition, cover construction, source graph access, full-precision arithmetic, factor multiplication/division, address movement and final output,

    T(N) = O((N+1)^16 * [1 + sum_B 5^tau_B])
    S_peak(N) = O((N+1)^6) bits.

These are deliberately loose **symbolic** polynomial overheads for a single implementation, not measured native TM microcode. No exponential table must be stored; the sum rather than the product of block costs is charged. For a nonbipartite block, exact 5^|V(B)| enumeration remains a valid blockwise fallback. If max_B tau_B is fixed, counting is polynomial-time even with unbounded number of blocks and global complement cover.

## Theorem C: independently implemented weighted extension

An unpinned block can be combined by scalar factors because the template is vertex-transitive. More generally, with nonnegative integer unary weights w_v(c), the /089 support step remains exact when the count for each orientation class A with exact support S becomes

    H_A(S)= sum_{Q subseteq S} (-1)^(|S|-|Q|)
            product_{u in A} sum_{c in Q} w_u(c).

Every opposite vertex contributes the *sum of its allowed weights*, not its allowed-color cardinality. Pinned complement-cover vertices contribute products of their weights. At articulation vertices, child subtrees supply five-entry message vectors. No articulation count enters the exponential parameter; a single block is evaluated at most five times for each parent interface. A standalone weighted algorithm and the independent scalar block-product algorithm gave matching counts.

## Infinite family / falsifier to global complement-cover lower bound

Take k>=3 copies of all-forward K_{p,p}, p>=3, each with one missing cross arc; join consecutive copies by identifying exactly one left vertex. Each individual graph is biconnected. Call the result G_{k,p}. For a single block, ordinary all-forward K_{p,p} has 5(2^p+2^p-2) colorings. Deleting one edge allows exactly ten additional assignments, hence Z(B)=5(2^p+2^p). The ten configurations arise because each previously forbidden endpoint pair uniquely forces the colors of all other vertices on each side.

The exact identities are

    n=k(2p-1)+1, m=k(p^2-1),
    max_B tau_B = 1,
    tau_global = k(p-1)+1,
    tw(G_{k,p}) >= p-1,
    Z(G_{k,p}) = 5*(2^(p+1))^k.

The global missing-edge complement has a matching saturating the left side, matching each block's first-occurrence left vertices with right vertices from a nonadjacent block two positions forward cyclically. Thus global tau reaches all k(p-1)+1 left vertices, even though every local tau is one. Treewidth is at least p-1 because each block contains K_{p-1,p}. Setting k=p makes global tau and treewidth unbounded while blockwise counting remains polynomial-time.

Executed case k=20,p=8: n=301, m=1260, 20 biconnected blocks, each local tau=1, global tau=141, tw>=7, Z=7662477704329444291791735135751545918093695610918010880 (55 digits; exactly 5*2^180).

## Computational audit

Local standalone source implementation: **1,052 seeded deterministic assertions, zero failures**, repeated with byte-identical result logs, including weighted local brute-force checks, random directed graphs, explicit SAT/UNSAT controls, two biconnected blocks with arbitrary orientations, long chains, bridge trees, and independent weighted-message versus scalar-product comparison. The locally tested compact composition passed **224 further checks with an independent literal-brute-force stand-in for the /089 block routine**, repeated with zero failures. Actual joint repository checkout execution importing /089 remains outstanding. A standalone two-page LaTeX section compiled; combined-manuscript compilation remains outstanding.

Four gates: (1) DISJ sanity PASS restricted constructive; (2) relativization NOT APPLICABLE to a separation; (3) SAME_REALIZATION DTISP PASS as symbolic upper bound, **not a lower bound**; (4) configuration counting UPPER-BOUND CONSISTENCY ONLY. Controls remain for brute force, 5-ary branching, all-forward families, loops, opposed arcs, trees, odd cycles, affine closure, path saturation, signature quotient, primal/dual/Fourier and rank algorithms, caching and recomputation, padding and high-treewidth obstructions. Native TM microcode and independent mathematical review outstanding.

**Next:** C3-T5-2CONNECTED-RESIDUAL091, seeking difficult 2-vertex-connected source blocks resistant to legitimate simplifications and comparing cost on the same machine. The semicomplete-digraph classification proves general T5 decision NP-complete but gives no automatic quantitative same-machine lower bound. **P versus NP OPEN.**

References: (1) Bang-Jensen, Hell, MacGillivray (1988), SIAM J. Discrete Math. 1(3):281-298, https://doi.org/10.1137/0401029. (2) Hopcroft, Tarjan (1973), SIAM J. Comput. 2(3):135-158, https://doi.org/10.1137/0202012. (3) Focke, Marx, Rzazewski (2024), ACM Trans. Algorithms 20(2), https://doi.org/10.1145/3640814.
