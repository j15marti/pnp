# TMR-4/088: successor-triangle expansion, high minimum frontier, constant-width exact OBDD

November 18, 2026, America/Los_Angeles. Additive to /087, preserving TMR-4 identity, ownership, manuscript and existing schedule.

## Precise restricted theorem

The source relation remains R(a,b) iff b-a mod 5 belongs to {1,3}; only original unweighted directed edges are permitted. Replace every oriented core edge u->v of a simple undirected graph H of minimum degree >=2 with a fresh z and three source arcs u->v, u->z, z->v. The triangle is an **exact functional gadget**: for each a=x_u, the only extension is x_v=a+1 and x_z=a+3 (mod 5). Source authenticity is checked by degree-2 gadget discovery, unique directed triangles, and full arc-cover verification; no source role metadata is trusted.

Solve all core potential equations p_v-p_u=1 along directed edges by signed BFS. Any inconsistent cycle gives count 0; otherwise each of c connected components has exactly five possible gauge shifts, and each private vertex is uniquely determined. Thus the exact original-variable count is **0 or 5^c**. A source-derived **complete-query five-way OBDD** tests every original variable on every path, retains five component-gauge states plus a rejecting state, resets at component boundaries, and has width <=6, nodes <=6N and transitions <=30N. The accept and reject counts are precisely Z and 5^N-Z. This is NOT a general T5-CSP algorithm; any off-class source must be routed to a correct fallback.

The encoded graph is parsed, verified, fully charged, and sorted in deterministic O(L log L) comparison overhead; subsequent graph and OBDD operations cost O(N+M), plus bit arithmetic and output. No free Fourier transform, tensor contraction, eviction, switch or oracle-provided variable order is used.

## Growing minimum-frontier source counterexample

For each k>=2 set H=K_{k,k}. Orient every core edge left-to-right, then expand every edge by the exact triangle. This SAT source has exactly **five** assignments. For the paired UNSAT source reverse just one core edge and its private triangle. All other edges of K_{k,k} minus that edge remain connected and force right-minus-left =1; the flipped edge forces right-minus-left =-1. Their difference is 2 mod 5, so UNSAT.

For both sources: N=k²+2k, M=3k², q=M-N+1=2k²-2k+1. In every ordering of the complete original-variable source, immediately after k core vertices have been queried, all k remaining core vertices touch the queried prefix. Therefore the **minimum** possible touched-future frontier is at least k=Omega(sqrt N). The underlying source has no K4 (and no five-vertex tournament palette), no directed false twins, and many cheap degree-two gadget separators. Despite minimum frontier growing unboundedly, the SAT source has OBDD width <=6 and the UNSAT source width 1. This explicitly falsifies any attempted inference from *minimum* graph frontier alone to minimum OBDD width or machine time. It does NOT resist affordable affine-gadget reductions.

## Four falsifiers

1. A two-edge directed path without its closing edge is not the same one-extension functional relation. The exact triangle and extension multiplicities must be checked.
2. Growing **minimum** frontier and q=Theta(N) do not imply OBDD or machine complexity lower bounds; a charged source-derived semantic quotient collapses to six states.
3. Reversing the directed edge is not negating R at equal colors. The UNSAT construction is a modular cycle contradiction with a genuine reversed triangle.
4. Source-obvious degree-two gadgets, separators and modular equations remain cheap; treating the high-frontier graph as irreducible would be invalid.

## SAME_REALIZATION ledger

The executable handles canonical original-graph JSON, vertex bounds, duplicate arcs, loops, full in/out adjacency, private-vertex and triangle recognition, complete arc coverage, modular signed BFS, component and order discovery, five outgoing transitions per layer node, complete rejection chains, state sharing, exact big-integer accepted/rejected multiplicities, output and error handling. Python uses expected-case hashes and an explicit alternative deterministic sort overhead; no worst-case unit-cost hash claim. Even rejected paths query all N variables. The 3-bit validity-checked block FBDD is <=6 nodes per five-way node. The direct parsimonious CNF uses 3N+15M clauses, 9N+90M literals. The full 32-mask arc consistency interface is not discarded for other families.

## Four finite verification gates

G1: 18 authenticated K_{k,k} examples (SAT/UNSAT, k=2,3,4,5,8,12,20,40,100), four non-bipartite/disconnected core expansions, six arbitrarily relabeled instances, and eight invalid/nonmember source rejections. Largest N=10,200, M=30,000, q=19,801, minimum frontier >=100.

G2: 787,650 original-assignment versus explicit OBDD decisions (781,250 exhaustive for the k=2 pair); 1,500 relabeled and 2,000 extra-core checks; 782,850 actual literal-CNF evaluations on valid codes and 1,200 invalid code controls; complete exact accept+reject path counts across all 18 paired cases.

G3: Independent JavaScript BigInt source recognizer, gadget discovery, modular BFS and 781,250 brute-force original source assignments, plus twelve paired source counts and five direct exact-gadget fiber checks.

G4: Byte-identical full Python and JavaScript reruns with zero unexpected failures. The k=100 SAT source had 61,194 internal OBDD nodes, width 6 and exact count 5; paired UNSAT had 10,200 internal nodes, width 1 and count 0. Computational tests are marked COMPUTATIONAL. Independent mathematical review, full LaTeX compile and physical TM-microstep verification remain OPEN.

## Handoff

Next D4-T5-HIGH-FRONTIER-AFFINE-IRREDUCIBLE-089: Seek mixed SAT/UNSAT families with growing minimum frontier after charging discovery of source-definable functional gadgets, affine cycle consistency, separator, palette, twin, backdoor, domain, cycle-syndrome and quotient reductions. Compare minimum native five-way FBDDs with unrestricted interleaved bit FBDDs for identical authenticated inputs. Restricted reverse simulations from /084 and /085 must not be generalized without proof. P versus NP remains OPEN.

Reference: Barto, Kozik and Niven (2009), *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Comput. 38(5), 1782-1802, DOI 10.1137/070708093.
