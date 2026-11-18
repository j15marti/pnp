# TMR-4/083: Smooth-core dichotomy and palette-backdoor exact compiler

**Object:** CSP homomorphism to directed T5 with Sigma=Z5 and R(a,b) iff (b-a) mod 5 is 1 or 3. Original input is a canonical complete directed graph encoding. This is not itself a 3-SAT instance.

## Established target classification

The 2009 theorem of Barto, Kozik and Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J Comput 38(5), 1782-1802, DOI 10.1137/070708093, proves that CSP(H) for smooth H is NP-complete unless every component of the core is a directed cycle. See also Larose, *Algebra and the Complexity of Digraph CSPs: a Survey*, 2017, Theorem 15, DOI 10.4230/DFU.Vol7.15301.267.

T5 is smooth: every vertex has in/outdegree two. It is its own core: as a loopless tournament, any endomorphism must be injective, hence bijective. It is not a directed cycle since every vertex has outdegree two rather than one. Consequently **decision CSP(T5) is NP-complete**, by a previously published theorem, not as a new finding from a finite experiment. The exact template's 5^5=3,125 self-maps were independently enumerated in Python and JavaScript; precisely five preserve all ten arcs, namely the cyclic translations.

NP-completeness remains true for **oriented, loopless input digraphs**: any general source with a self-loop or opposite arc pair is trivially UNSAT for loopless T5, and can be replaced in polynomial time by a fixed oriented K6, likewise UNSAT by injectivity. Otherwise retain it. This preserves YES/NO under ordinary many-one reductions. No claimed hardness restriction on 4-connected or palette-dominated sources follows.

## D4-T5-PALETTE-BACKDOOR083

A source-induced five-vertex T5 copy is a palette. Its five possible images are the five translations. A vertex adjacent to four palette vertices has only one possible image, the missing palette color, or fails orientation checks. Five palette neighbors force UNSAT. With q exceptional vertices having at most three palette adjacencies, all original constraints reduce to checking at most 5^q normalized assignments. The exact original count is 5 times that normalized count. Enumerating five-element source palettes costs at most n^5 poly(L), and exact counting costs 5^q poly(L), with actual source scans and integer growth included. For q=O(log L) both are polynomial.

Query original palette colors, q exceptional colors, then forced colors. A complete original five-symbol OBDD, including rejecting continuations, has width <= 5^(q+1)+1 and <= n(5^(q+1)+1) internal nodes. Every original assignment is represented; accept+reject path multiplicities equal exactly 5^n. For q=0 width<=6.

Concrete sources add t=20,25,30,35 pinned vertices to one T5 palette, connect them by a directed t-cycle and quadratically many other compatible arcs. The SAT family has five solutions. An additional arc between two same-color pinned vertices makes the corresponding UNSAT family have zero solutions. Both are >=4-vertex-connected, strongly connected, and have quadratic feedback rank, linear cover, no directed false twins and connected nonadjacency graphs in all eight tested inputs. This is a **cheap-source counterexample**, not an NP-hard residual.

Four falsifiers: (1) published NP-completeness does not prove a deterministic superpolynomial lower bound; (2) high connectivity/density/structural signatures coexist with width<=6; (3) all five unary colors survive elementary AC-3 even for these UNSAT controls, so unary propagation is insufficient; (4) three-bit parsimonious CNF uses 3n Boolean variables and 3n+15m clauses, with <=7 binary OBDD query nodes per five-way node, so the direct encoding is only constant-factor overhead. Rejected bit strings with invalid codes are distinguished from original-symbol rejected assignments.

## SAME_REALIZATION and verification gates

Full execution includes canonical byte preflight and SHA-256, graph discovery, palette search, literal verification of every arc, explicit order, all 5-way OBDD transitions, state sharing and rejection continuation, exact big integers, literal Boolean clause construction and output. No hidden Fourier transforms, approximation, eviction or free variable-order switching.

Gate 1: 12 canonical sources, 8 malformed rejections and 2 valid nonmember controls.
Gate 2: 2,424,125 native assignment/OBDD checks, 7,050 actual CNF checks, 180 invalid-code checks, with accept+reject=5^n in all 12 diagrams.
Gate 3: all 3,125 T5 self-maps and 120 permutations checked; partial small-input counts brute-force compared against normalized compiler counts.
Gate 4: independently executed JavaScript verifier recomputed core maps, partial-source counts and dense pin checks; its eight common dense source counts and arc totals agree with Python. Repeat Python and JavaScript executions were byte-identical; unexpected failures 0.

Complete executable programs and source JSONs reside in the downloadable TMR4_083_T5_smooth_core_palette.zip evidence package from this run. The GitHub manuscript contains the theorem, bounds and explicit firewall; these are not claims of unrestricted machine lower bounds.

**Next:** D4-T5-PUBLISHED-REDUCTION-INSTANTIATION. Extract concrete source gadgets/reduction for this exact template from the 2009 theorem, then check real source-aware simplifications before lower-bound proposals. P versus NP OPEN, physical TM microstep proof and external peer review OPEN.
