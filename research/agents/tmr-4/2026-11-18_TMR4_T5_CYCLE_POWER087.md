# TMR-4/087: 8-connected high-q T5 graph, exact five/zero count, all-order six-width OBDD
2026-11-18 PST. Owner: TMR-4 / PNP Cost-Sound Abstraction. This is an additive restricted theorem, not an unrestricted lower bound.

## Candidate and theorem
For n>=13 construct D_n with vertices Z_n: for each i and d in {1,2,3,4}, insert i->i+d (mod n) when d is odd, and i+d->i when d is even. Every underlying unordered pair occurs exactly once, hence m=4n directed arcs. Constraints are R(x,y) iff y-x mod 5 belongs to {1,3}. This is the fixed-template T5-CSP, not an assumed 3-SAT instance.

Exact solution count:
  Z(D_n)=5 if 5|n; otherwise Z(D_n)=0.

For every n>=13, the underlying graph is C_n^4, vertex connectivity exactly 8, strongly connected as a digraph via the directed +1 cycle, and has feedback-cycle rank q=m-n+1=3n+1. Nonadjacency graph is connected (its generating jumps include 5 and 6). Directed false-twin reduction does not apply. Every cyclic five-vertex window is individually satisfiable and arc consistency leaves all five values at every vertex.

Every window W_i=(i,...,i+4) is a T5 tournament. A homomorphism from a five-vertex tournament to the loopless five-vertex T5 is injective and therefore an automorphism. The target has exactly five automorphisms, the cyclic translations: fixing the image of a single vertex determines all other images by their oriented incidence. Overlapping windows share four vertices, so any global solution is x_i=a+i mod 5. The wrap window requires n=0 mod 5. Conversely, if 5|n, all five phases a work.

**Source authentication, no free labels:** From a raw, arbitrarily relabeled complete arc list, build undirected neighbor sets. For n>=13, existing edges at cycle distances 1,2,3,4 have 6,5,4,3 common neighbors respectively. Recover the ordinary n-cycle via the 6-common-neighbor pairs, try both directions, reconstruct all expected oriented edges, and compare the entire raw directed edge set. Reject tampered or nonmembers. Parsing, neighbor discovery, cycle search, and comparison all charged.

**Complete-query exact OBDD, for every fixed order:** A satisfying full assignment has the form x(v_i)=a+i mod 5 for a in Z5. Query the first variable to determine a, keep five phase states, and on later queries continue the phase if the chosen value matches, else enter a rejecting chain that still queries every unqueried variable. For n with 5|n, levels after the second variable and before the last have five distinct nonzero residuals and one rejecting residual, so width 6 is *optimal for complete-query OBDDs for every fixed variable order*. Width profile [1,5,6,...,6], internal nodes exactly 6n-6. For 5 not dividing n the function is identically zero and a width-one, n-node complete-query OBDD suffices. Accepting and rejecting counts are exactly 5 and 5^n-5 for SAT, 0 and 5^n for UNSAT. Construction and full output are polynomial in original source length, including O(n)-bit integers.

## Four falsifiers
F1. q=3n+1 and 8-connectivity, no 1-4 separators, all local T5 windows SAT, yet cheap source-aware exact computation.
F2. Full 32-mask-capable unary domain propagation leaves mask31 at every vertex, even in UNSAT cases.
F3. Uncharged source-isomorphism witness would be illegal. A raw-arc recognizer is performed; 56 reversed/deleted-arc controls and 112 malformed sources were rejected.
F4. Neither a bad binary variable order nor generic 5^q cycle-syndrome costs provide a reverse machine lower bound. Here every order has native width <=6.

## Four gates and SAME_REALIZATION ledger
G1 authenticated 56 original graph encodings from 28 sizes (canonical plus independently relabeled); 56 nonmember-tamper and 112 malformed rejections.
G2 source-arc literal Python backtracking in recovered cyclic order agrees with 56 computed counts. Independently coded Node.js/BigInt brute source search agrees at all 28 canonical sizes (140 extra full phase tests).
G3 10080 original-assignment pointwise tests agree among literal arcs, the complete MDD, and valid Boolean codes. Exact accepting plus rejecting multiplicities always equals 5^n; largest n130 gives q391, maximum MDD width6, 774 internal nodes.
G4 319744 valid/invalid Boolean-code checks, 336 *literal clause* CNF evaluations, and deterministic repeat. Python raw summary SHA256: 7be0051cec66323267c99be876747216077983697e0b0b93a5374df07c854228. No unexpected assertion failures.

SAME_REALIZATION: charge raw parsing and all original 4n arcs; 8-neighbor discovery and orientation authentication; any variable-order selection; all five-way transitions, sharing and per-depth rejected chains; exact O(n)-bit multiplicities and output; 3n Boolean bits and 3n+15m=63n CNF clauses (3 invalid-code clauses per variable and 15 prohibited pair clauses per arc), and <=6 grouped binary decoder nodes per native node. Full 32 masks remain available; this family simply uses all-five domains. No Fourier transform, tensor shortcut, cache eviction, dynamic order switch, hidden oracle, or uncharged CNF gadget is used. The 3-bit representation changes size by a constant factor, not asymptotically.

Proof scope: all-order fixed-variable OBDD width for the **recognizable D_n family only**; unrestricted interleaved-bit FBDD minima, arbitrary source-to-machine reverse transfer, and any P != NP theorem remain OPEN. The published NP-completeness classification of T5-CSP is not challenged. Independent mathematical review and physical Turing-machine microstep audit remain OPEN.

NEXT: D4-T5-PRIME-HIGH-Q-RESIDUAL-088. Seek mixed SAT/UNSAT families that survive *charged* local fifth-power-cycle recognition, palette, separability, domain, gauge/affine, treewidth and known OBDD/FBDD source compilers. Compare optimal representations only on identical authenticated sources.