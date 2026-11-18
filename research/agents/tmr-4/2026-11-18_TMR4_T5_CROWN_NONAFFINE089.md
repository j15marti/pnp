# TMR-4/089: nonaffine crown quotient destroys a minimum-frontier lower-bound proxy

2026-11-18, America/Los_Angeles. Additive to /088; TMR-4 identity, schedule, living manuscript, old results and proof firewalls are preserved. Status **PROVED restricted symbolic theorem; COMPUTATIONAL finite evidence**. No unrestricted machine lower bound. P versus NP OPEN.

## Precise result
For k>=4, authenticate the original digraph with U={u_i}, V={v_j}, and arcs u_i->v_j exactly when i!=j. The alphabet is Z5, R(a,b) iff b-a in {1,3} mod5. The source is the directed crown graph K_(k,k) minus its matching, with n=2k, m=k(k-1), q=k²-3k+1. No source partition or vertex ordering is assumed in the input: the recognizer recovers the two sides from in/out degrees and checks each unique missing partner and every arc.

**Theorem:** Z(k)=10*2^k+10*k-10 exact colorings. A complete-query, original-variable five-way OBDD has width <=10k+12 and <=2k(10k+12) internal nodes, including layer-specific rejecting states. Every original assignment follows one length-2k path. Rejecting multiplicity is exactly 5^(2k)-Z(k).

**Proof:** Let O(a)={a+1,a+3}. For any distinct colors a,b, O(a) and O(b) intersect in either zero or one element; five unordered pairs intersect, forming a 5-cycle. k>=4 U colors using three distinct values yield an empty V_j support after removing a suitable U_j; two incompatible colors likewise fail. Five monochrome U strings contribute 5*2^k extensions. For each of five compatible pairs, there are 2^k-2-2k two-color U strings with both colors repeated twice, each with a unique V extension, and 2k strings with a singleton at an index j, each having two V extensions. Summation is the stated formula.

**FBDD construction:** Query all U, then all V. Track up to two compatible colors, multiplicities saturated at two, and the index if one color is still a singleton. A third color, incompatible pair, or bad V color enters a rejecting state, which nevertheless queries every later original variable. At V_j, allowed colors are O(a), O(b) or O(a) intersect O(b), depending on whether j is the unique singleton. At a fixed layer there are at most five monochrome states, five repeated-pair states, 10k singleton-index states and one rejection state (plus initial state), proving <=10k+12. Prefix multiplicities are added on merges, not discarded. General nonmembers use the complete five-way decision-tree fallback, exponential as required.

**Unavoidable graph frontier:** Every vertex of the underlying crown has degree k-1, there are no false twins, triangles, directed successor-triangle gadgets, degree-two private gadgets, articulation vertices, or tournament palettes. Vertex connectivity is k-1. After any ordering's first k vertices, at least k-1 of the k unqueried vertices are adjacent to the prefix: if a queried vertices lie in U, this follows directly for a=0,..,k; only a=1 or a=k-1 can lose one. Hence minimum frontier >=k-1 while actual recognized OBDD size is O(k²)=O(m), with q=Theta(k²). This is a **nonaffine** (global compatible-pair) semantic quotient, beyond the affine-triangle family of /088.

**Mixed companion:** Reverse exactly four arcs u_i->v_(i+1 mod4), for i=0..3. The induced eight-vertex directed four-crown is UNSAT: all 5^8 colorings and all 125 cyclically normalized U choices exhibit an empty V domain. The source recognizer discovers a missing-matching crown and the four-cycle of reversed arcs even after vertex relabeling. This yields an exact complete-query width-one rejection chain, n nodes, 5^n rejected assignments, on all k>=4. Its constant-size UNSAT certificate is an explicit weakness, **not** an irreducibility claim.

## Four falsifiers
F1: large *minimum* frontier, q and connectivity do not imply large minimum OBDD width.
F2: lack of affine triangles, palette and twins does not eliminate a source-aware nonaffine quotient.
F3: a SAT witness or UNSAT certificate alone does not provide an assignment-preserving exact counter: complete rejected paths and all incoming multiplicities are necessary.
F4: one poor Boolean bit order, implicit validity rejection, or uncharged graph recognition cannot support unrestricted FBDD-to-source transfer.

## SAME_REALIZATION
Charged input parsing and bounds, duplicate arcs/loops, full graph discovery, missing-matching/orientation test, source ordering, five-way transitions and shared state lookup, layer-specific rejection chains, exact big-integer path counts, output and Boolean/CNF conversion. Actual Python has expected-case hashes; sort-based deterministic source preprocessing is O(L log L) comparisons, O(k²) graph and OBDD transitions plus conservative O(k³ polylog k) bit arithmetic; O(k² log k) bits of explicit stored graph/states. No free Fourier/tensor transforms, machine switching or cache evictions; exact fallback for unrecognized input is exponential. Grouped three-bit Boolean FBDD costs <=6 binary decoder nodes per five-way node. Direct auxiliary-free CNF uses 3n+15m clauses and 9n+90m literals, including 3 invalid-code clauses per symbol, 15 forbidden-pair clauses per arc. Full 32 unary masks still correspond to 32 subsets of valid 3-bit codes; the present compression is source-family-specific.

## Four verification gates
G1: 17 canonical sources, 12 SAT recognitions, two relabeled UNSAT certificates, 4,678 exhaustive half-cut subsets for k4..7, 8 malformed input rejections, 9 specialization nonmembers, 3 generic-fallback tests.
G2: 390,625 exhaustive source-vs-five-way-OBDD-vs-literal-CNF assignments (k4), 5,500 sampled original assignments at larger sizes, 300 invalid-code controls and 390,625 UNSAT companion assignments.
G3: independent Node.js program checks 97,500 U choices (k4..7), separately evaluates 781,250 full original SAT/UNSAT k4 assignments against actual literal CNF, with 300 invalid controls.
G4: two byte-identical Python and Node.js executions, zero unexpected failures. k100: n=200,m=9,900,q=9,701,count=12,676,506,002,282,294,014,967,032,054,750, OBDD width 1,011, 151,654 internal nodes, 758,270 transitions. UNSAT companion width1, n=200.

**End-to-end proof safeguards:** DISJ/static cut arguments cannot transfer; nonrelativizing extraction OPEN; simultaneous time/space is an explicit upper-bound same realization only; configuration counting gives no negative result. Independent mathematical review, full LaTeX compilation and physical TM microstep check are OPEN. Barto-Kozik-Niven (SIAM J Comput 38(5), 2009, doi:10.1137/070708093) establishes NP-completeness of unrestricted T5 via the published smooth-core dichotomy; this restricted class remains polynomial.

Next: D4-T5-HIGH-FRONTIER-NONAFFINE-QUOTIENT-RESISTANT-090. Seek mixed sources resisting compatible-pair, constant obstruction, affine, twin, separator, backdoor, Fourier and gauge reductions; compare unrestricted interleaved Boolean and native five-symbol minimum FBDDs on identical authentic graphs. P versus NP OPEN.

Complete Python, independent JS, exact raw audit and hashes are in companion TMR4_089_T5_crown_nonaffine_quotient.zip.