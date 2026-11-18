# TMR-3/080: source-discovered three-hub clique adhesion and exact 125-entry boundary messages

**Checkpoint:** 2026-11-18 01:21 America/Los_Angeles. **Owner:** TMR-3 / PNP Time-Space Tradeoffs. **Status:** restricted constructive theorem with independently tested executable; independent proof review and native TM microcode OPEN. **P versus NP OPEN.** Existing task identity, title, enabled hourly schedule, ownership, safeguards, and historical manuscript remain unchanged.

## Exact source model and restriction

The input is an explicit directed graph. A valid original coloring is x:V -> Z5 satisfying R(a,b) iff b-a belongs to {1,3} mod 5 on every arc. Loops or opposed pairs have zero colorings. Duplicates are idempotent. Recognized inputs have indegree-zero hubs and private outdegree-zero sinks, each with exactly three distinct hub predecessors. Each sink e, with hub parents (a,b,c), contributes the **original-coloring** factor

    w(a,b,c) = sum_{z=0}^4 [R(a,z) R(b,z) R(c,z)] in {0,1,2}.

Thus Z(G)=sum_{hub assignments} product_e w_e. Multiple sinks on the same triple retain separate multiplicative factors. Unrecognized legal inputs use an exact finite brute-force fallback (not a promise of polynomial time).

## Theorem: charged clique separators with adhesion at most three

Build the primal graph on hubs; each three-parent sink induces a triangle. As in /079, maintain exact original ternary factors and computed boundary factors, now of arity at most **three**. Add virtual clique edges for the current fragment's boundary U, solely for decomposition. Enumerate the empty separator, vertices, primal edges, and primal triangles S of size <=3; accept the first S such that deleting S creates at least two components and U\S lies within a single anchor component.

For each non-anchor component C, recursively compute the exact conditional sum M_C(x_S) over its internal hubs, retaining S colors. Transfer M_C as one at-most-125-entry factor on S to the anchor. Factors entirely in S remain with the anchor. Every factor that is not entirely in S has its off-S variables within one component, because each factor's variables form a primal clique. No source factor is lost or double-counted.

At a terminal fragment find a relative factor cover C of size <=t outside U such that for **every factor f** (original or a generated message),

    |scope(f) minus (U union C)| <= 1.

Searching for a deficient factor and branching on one of its at most three unfixed variables finds such a cover, if one exists, with at most O(3^(t+1)) search nodes and no exponential memo table. Conditional on U union C colors, all remaining factors depend on at most one free hub, so the remaining sum separates into independent five-term unary sums. The terminal computation uses at most 5^(t+3) fixed-color assignments and a 125-entry output message.

For the deterministic source-derived decomposition **whose every terminal fragment has a cover of size at most t**, one blank-start sequential deterministic machine has the simultaneous conservative bounds

    T(N) = O((N+1)^16 [1 + 3^(t+1) + 5^(t+3)]),
    S_peak(N) = O((N+1)^6) writable bits,

for exact original-coloring count, including encoded-source authentication, separator-candidate failures, graph accesses, all head/index movement, stack, factor provenance and exact integer arithmetic, cover failure branches, multiplication and binary output. All conditional counts have O(N)-bit integer entries, since each counts at most 5^n original assignments. Clique candidates are enumerated, not assumed as an oracle. This is a conservative upper bound for one complete implementation, not a time-space lower bound. Recognition/terminal-cover failure triggers a correct exponential fallback; the fast envelope is restricted.

## Infinite countercontrol requiring an adhesion-three split

Construct r successive five-hub atoms, with **all ten** three-subset sinks per atom. Each atom shares its three-hub incoming interface (a,b,c) with the preceding atom and introduces two new hubs d,e; its outgoing interface is (c,d,e). The original graph has

    n = 3+12r vertices,  m = 30r arcs,  h = 3+2r hubs.

Its hub-primal graph is a path of K5 clique atoms overlapping in a K3. No separator of size 0, 1 or 2 disconnects this graph; for r>=2 its vertex connectivity is exactly 3. Every third atom supplies a sink triple with disjoint hub scope, so its global strong-two-cover grows at least 2 ceil(r/3). The /079 adhesion-two recursive decomposition cannot split this growing prime-to-order-two core, whereas order-three clique messages separate it into constant-size atoms; terminal budget t=4 suffices.

Independently, for an input interface coloring (a,b,c) and output interface coloring (c,d,e), define

    F(a,b,c,d,e) = product_{Q subset {(a,b,c,d,e)}, |Q|=3} w(Q).

The **independent 125-state transfer** recurrence is

    D_0(a,b,c)=1
    D_{j+1}(c,d,e)=sum_{a,b in Z5} D_j(a,b,c) F(a,b,c,d,e)
    Z(G_r)=sum_{a,b,c in Z5} D_r(a,b,c).

It counts all original sink colors and matches the source solver. For r=1,2,10,80, the counts are respectively 6120, 5976840, 7258928966547540816707358627840, and a 242-digit integer beginning 398788952016201784686666776591202883249142688. At r=80 the source has 963 original vertices and 2400 arcs.

## Algebraic optimization and limitation

The fixed relation is invariant under simultaneous addition modulo five. Therefore every exact b-hub boundary signature obeys M(a_1+s,...,a_b+s)=M(a_1,...,a_b). For b>=1, store only **5^(b-1)** orbit values, giving 25 normalized values instead of 125 when b=3. Recover full 125 entries without ambiguity. This factor-five improvement does not remove exponential dependence on unbounded adhesion and cannot imply a P/NP separation.

## Executed falsification and verification

The standalone Python 3 standard-library source and audit are included in the attached reproducibility ZIP. 211 deterministic assertions passed with zero failures. The checks cover random arbitrary directed inputs versus original brute force, random incidence inputs versus independent five-state hub enumeration, malformed sources, structural zeros, 10 chain lengths through r=80 versus the separate 125-state transfer, and cyclic-shift invariance. The r=80 exact count was checked against both implementations. An additional independent NetworkX connectivity audit on r=2,3,6,10 found **zero** cuts of sizes one or two and vertex connectivity exactly three. The 80-link timing (about 17 seconds in the executed CPython environment) is COMPUTATIONAL and not an asymptotic TM performance claim. Python source SHA256: f6e23787e7d5dfd4f7c7950dcc4ce755b18de4830b5717a1ed7c817c6c5a5b0a. Audit-log SHA256: 8ccff09bd833389cbd1973bede896ced665f090c81427ab20921ae259028119e.

**Four gates:** DISJ sanity PASS restricted positive-algorithm statement; relativization/algebrization/natural proofs NOT APPLICABLE to a separation but retain safeguards; simultaneous DTISP PASS restricted constructive bound with both T,S for one realization; deterministic configuration-counting PASS only as upper-bound consistency, NOT a lower bound. Preserve affine/Horn, width, degree-two, cycle-rank, twin/module, selector/padding, uniqueness, rank, caching, recomputation and original-source-access easy controls. Retired /341 unrestricted UNSAT authority remains FAIL; /386 remains RESTRICTED.

**Hardness caveat:** The fixed five-symbol relation is the regular five-vertex tournament and falls under Bang-Jensen, Hell, MacGillivray's semicomplete-digraph NP-completeness classification (1988, DOI 10.1137/0401029). This classification is not a quantitative size-controlled SAT-to-T5 reduction. No unproved exponent is transferred.

**Prior art:** Clique-separator decomposition and bounded-width exact CSP dynamic programming are established techniques. The contribution here is a source-authenticated, exact original-coloring instantiation with charged simultaneous time/space and the explicit order-three countercontrol, not a claim that separator DP is fundamentally new. See Focke, Marx, Rzążewski, *Counting List Homomorphisms from Graphs of Bounded Treewidth*, SODA 2022, DOI 10.1137/1.9781611977073.22.

**Next load-bearing target C3-T5-ADHESION-WIDTH081:** extend exact message composition beyond cliques, source-discover width-w decompositions, charge decomposition discovery, and determine when Z5 symmetry gives genuine asymptotic improvements. Full historical LaTeX compilation, source-code publication into GitHub, independent mathematical review and native Turing-machine microcode remain OPEN. **P versus NP OPEN.**
