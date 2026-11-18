# TMR-4/090 | universal five-channel gap and uniform-compiler barrier

2026-11-18 PST. Exact target: canonical original-label T5-CSP, Sigma=Z5, R(a,b) iff (b-a mod 5) is 1 or 3. TMR-4 remains PNP Cost-Sound Abstraction; this is additive to /089 and preserves all prior work. **Status: PROVED/EXACT for the restricted model, finite tests COMPUTATIONAL, P versus NP OPEN.**

## Candidate D4-T5-UNIFORM-WIDTH-GAP-090

**Theorem 1.** For any authenticated T5 input G with at least one arc, if G is UNSAT then its minimum complete-query five-way OBDD and deterministic adaptive FBDD width is exactly 1; if G is SAT then both minimum widths are at least **5**, irrespective of the variable order or adaptive branching. Complete-query means every root-to-terminal path queries every original vertex exactly once, including all rejected paths; width counts internal states per query depth.

**Proof.** An UNSAT source has the one-state-per-layer rejecting-completion chain with n nodes and 5^n rejecting original paths. For SAT G, fix a computation prefix just before the first query u of any vertex in a nontrivial weak component. All previous queries concern isolates. Fix their answers. Every a in Z5 has a nonempty satisfying residual f_a, by translating a complete satisfying coloring in the component of u. Translation covariance gives f_a(y)=f_0(y-a) on the remaining labels in that component. If f_a=f_b for distinct a,b, f_0 is invariant under shift b-a. Since 5 is prime, the shift generates Z5, so all five residuals would coincide. But the queried u is essential: starting from any satisfying coloring, change only u to the color of one neighbor v, making their original arc violate irreflexivity R(t,t)=0. Therefore f_a are five distinct nonzero residual predicates. Deterministic states after querying u cannot merge any two branches; width >=5. Adaptivity does not change this conclusion. Edgeless SAT graphs are an essential exception.

**Theorem 2.** For each fixed k=1,2,3,4, recognizing whether the minimum complete-query five-way deterministic OBDD or FBDD width is <=k on T5 sources having at least one arc is **coNP-complete**. There is no polynomial-time all-input algorithm emitting a correct diagram with width <5 times optimum, unless P=NP.

**Proof.** By Theorem 1, the threshold language is exactly T5-UNSAT restricted to nonempty-arc inputs. T5-Hom is NP-complete by the Barto-Kozik-Niven published smooth-digraph dichotomy: the regular five-vertex tournament is its own core and not a directed cycle. Add a disjoint satisfiable single arc to any input to enforce the nonempty-arc condition without changing SAT status. Immediate local contradictions (loops or antiparallel arcs) may be replaced by a fixed unsatisfiable oriented four-vertex transitive tournament in strict oriented-source grammar. Thus threshold recognition is coNP-complete. A factor-alpha diagram compiler with alpha<5 would return width<=4 on UNSAT inputs and must return width>=5 on SAT inputs; testing its output width would decide T5-SAT in polynomial time. This is a representation *optimization* barrier, not a lower bound on source-SAT runtime.

**Theorem 3 (one-way implication).** A uniform polynomial-time exact all-input FBDD compiler of polynomial output size would give a polynomial-time T5-SAT decider by accepting-terminal reachability. The reverse is not justified: existing TMR-2/071 LPS/Razgon examples have cheap pure-source/sink YES deciders but exponential syntactic original-label pointwise read-once representations; /072 adds source-recognizable mixed answers. This does not refute a hypothetical all-input P=NP world, and unrestricted lower-bound transfer stays OPEN.

## Four falsifiers

F1: Five-valued branches might share the same nonzero suffix. Refuted by prime-order cyclic translation plus essential incident arc; the edgeless exception is explicit.
F2: Adaptive reading might avoid five distinct states. It cannot on the specified complete deterministic read-once model; no claim for non-complete or unrestricted machine models.
F3: Tiny existence of a rejection diagram might imply cheap construction. It does not: minimum-width threshold is coNP-complete; source decision and compiler discovery are separately charged.
F4: Boolean/CNF recoding and all-zero merging might preserve incorrect multiplicities. All original five-label rejecting branches continue to depth n, and invalid 3-bit codes are rejected separately.

## Reproducible evidence and four computational checks

Python and an independently authored Node.js program enumerated all 729 four-vertex labeled simple oriented graphs (three choices per unordered pair), all 24 orders each (17,496 complete cofactor OBDD checks), all 455,625 original assignments and their corresponding *literal-evaluated* three-bit CNF formulas, 10,413 invalid-code controls, and 2,048 oriented 32-mask domain propagation cases. Original Python additionally verified 10,935,000 complete OBDD assignment paths by integer path-weight propagation and rejected five malformed encoded sources. Histograms match independently: 88 UNSAT with OPT=1; one edgeless SAT with OPT=1; and 640 nonempty SAT split into 12 at OPT=5, 536 at OPT=6, 92 at OPT=11. Two runs per implementation were byte-identical. Zero unexpected failures.

Same complete four-vertex skeleton: the orientation induced by the first four colors of T5 has Z=5, fixed-order width 6, 18 internal nodes; transitive K4 has Z=0, width 1, four internal nodes. This is finite evidence, not extrapolation.

The standalone JavaScript file under experiments/tmr/ is an independent compact audit of all 729 graphs, 17,496 orders, literal valid-code CNF checks and 2,048 mask cases. The full Python, second independent JavaScript, invalid-code controls, checksums and raw logs are in the companion downloadable evidence ZIP, not misidentified as repository files.

## SAME_REALIZATION and model guards

The source parser charges every ASCII byte, every vertex declaration, sorted arc, range check, loop and duplicate. The reference general compiler pays for all 5^n original evaluations and cofactor bitsets, source discovery, variable ordering, five-way transitions, state merges, complete rejecting paths, caching/eviction/recomputation, exact O(n)-bit counts and full output. Its general worst-case time and space may be exponential, conservatively O(5^n(L+1)^6) bit operations and O(5^n(L+1)^5) writable bits for source length L. The existential UNSAT rejection chain is never treated as a free *uniformly discoverable* object. No free Fourier/Z5 tensor operation or source-switch oracle exists.

The standard 3-bit code uses exactly 3n+15m auxiliary-free CNF clauses and 9n+90m literals. Valid-code inputs number 5^n; invalid-code inputs number 8^n-5^n. The 32 unary masks are all subsets of the five valid codes, and hence are not an intrinsic asymptotic advantage over three-bit propagation. The previous restricted block simulation has <=6 binary decoder nodes per native node; unrestricted interleaved Boolean FBDD minimum width is not covered by this theorem.

**Four proof gates:** (1) DISJ/model gap PASS restricted, unrestricted source-runtime inference FAIL; (2) relativization and nonrelativizing P-vs-NP implications OPEN; (3) simultaneous DTISP is a charged *upper* ledger only; (4) deterministic configuration counting is upper-consistency only. Full external mathematics review, LaTeX compilation and physical TM tape-head microsteps remain OPEN. Finite evidence is COMPUTATIONAL.

**Next D4-T5-UNIFORM-LOWER-TRANSFER-091:** separate the cost of discovering a pointwise diagram from the small semantic optimum; attempt a genuinely mixed source family resistant to legal quotient/gadget/source recognizers and prove a model-matched reverse implication, rather than invoking OPT_width as a free oracle. P versus NP OPEN.

References: Barto, Kozik and Niven, SIAM J. Comput. 38(5), 2009, doi:10.1137/070708093; Razgon arXiv:1411.0264; Lubotzky-Phillips-Sarnak Combinatorica 1988, doi:10.1007/BF02126799.
