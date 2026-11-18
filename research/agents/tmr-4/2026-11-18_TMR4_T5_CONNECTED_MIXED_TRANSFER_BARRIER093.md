# TMR-4/093: Connected mixed SAT/UNSAT sources expose an exact-OBDD transfer barrier

2026-11-18 America/Los_Angeles. Restricted mathematical construction, independently checked finite COMPUTATIONAL evidence. P versus NP OPEN. Preserve all prior /083–/092 work and TMR-4 identity, ownership, manuscript, hourly schedule and SAME_REALIZATION controls.

## Model and new theorem

Let T5 be Z5 with R(a,b) iff b-a mod 5 lies in {1,3}. Let H=(U,W,F) be a connected simple undirected bipartite graph, maximum degree Delta, with all original arcs oriented U->W. Choose w in W of positive degree and introduce one vertex s. Define G+(H)=D(H) plus the arc w->s, and G-(H)=G+(H) plus the reverse arc s->w. Both original source graphs are connected, are non-forward-bipartite as directed graphs in general, and differ by exactly one original arc.

**Theorem 093A (complete original-assignment multiplicities).** Z(G+)=2 Z(D(H))>0 and Z(G-)=0. D(H) is SAT with U=0,W=1; every permitted w color admits precisely two s colors. The two-cycle in G- cannot map homomorphically into the loopless T5 tournament. There are no auxiliary variables, uncharged projections or multiplicity factors.

**Theorem 093B (all fixed original-variable orders).** If b(H) is the minimum number of edges crossing a balanced vertex cut, every deterministic native 5-way fixed-order OBDD that computes the complete satisfaction predicate of G+ has width at least

    2^floor(b(H)/(4 Delta^2)).

In contrast the predicate for G- is identically zero, hence its reduced exact OBDD has zero internal nodes and a complete-query exact OBDD has width one and n+1 internal nodes.

Proof: Given ANY variable order including the new s, remove s and cut the induced core order after half the core variables. The matching argument of /092 extracts a crossing induced matching of size >=b(H)/(2 Delta^2), of which at least half have the same prefix-to-suffix direction. For U-prefix edges, vary selected prefix U in {0,2}, fix other U=0 and all W=3, then distinguish each selected coordinate by changing its suffix W from 3 to 1. For W-prefix edges, vary selected prefix W in {1,3}, fix other W=1 and all U=0, then change one matched suffix U from 0 to 3. All 2^k prefixes extend to SAT, with pairwise distinct suffix predicates. In BOTH palettes all W values belong to {1,3}, and R(1,4)=R(3,4)=true. Setting s=4 preserves every selected completion and probe irrespective of where s occurs in the full variable order. Thus the /092 signatures remain valid with the attached vertex. The UNSAT predicate is constant zero by 093A.

For even checkerboard r x r grids, b(H)>=r/2 and Delta<=4, giving SAT-side all-order exact OBDD width >=2^floor(r/128). Bounded-degree connected bipartite expanders with b(H)=Omega(n) give SAT-side width 2^Omega(n). The source decision task on BOTH sides remains O(n+m): read and validate arcs, identify the unique pendant marker on this restricted class, verify a connected pure-U-to-pure-W core, check whether the pendant is bidirectional, then output a verified witness or the two-cycle obstruction. NONMEMBER cases are not promised easy.

**Theorem 093C (unavoidable per-instance nullity).** For ANY unsatisfiable finite-domain CSP source G, its exact complete-assignment satisfaction function is constant zero. Consequently every UNSAT instance has a one-state full-query OBDD regardless of any conjectural difficulty of determining that it is UNSAT from its encoded graph. Adding mixed SAT/UNSAT data cannot overcome this semantic-to-source transfer obstruction. In particular, minimum exact-predicate OBDD width is not a sound per-instance lower-bound measure for source SAT decision.

## Restricted genuine model equivalence

A deterministic *assignment stream verifier*, already given its authenticated source and a specified fixed read-once order, with <=W fully specified reachable configurations at each layer, unrolls to <=nW exact 5-way complete OBDD nodes and <=5nW arcs, with full transition computation charged. Conversely, an explicitly materialized n-layer S-node exact OBDD runs as a deterministic input-stream table program using O(log S) addressing bits and O(5S log(S+n)) transition-table bits. Exact accepted and rejected assignment multiplicities are recovered by dynamic programming with O(n)-bit integers. Neither direction implies a cheap compiler or SAT existence solver from the original source: discovering the configurations, constructing the table and existentially finding an accepted path must be charged.

## Four falsifiers

F1: On all UNSAT instances the *minimum* exact-assignment OBDD is trivial, regardless of source-solving complexity. Even mixed connected inputs do not fix this.
F2: Extra variables can destroy old residual signatures. The new common s=4 color explicitly survives all selected W in {1,3}, and finite pointwise probes verify this.
F3: SAT-side OBDD width (even for every fixed order) does not imply hard source SAT; the original connected pendant pattern is recognized and decided in linear time on this family.
F4: Grouped 3-bit Boolean codes simulate a 5-way node with <=6 binary nodes, full unary propagation still has 32 masks, and direct no-auxiliary validity CNF has 3n+15m clauses and 9n+90m literal occurrences. Unrestricted bit-interleaved Boolean FBDD and adaptive FBDD reverse transfer remain OPEN.

## SAME_REALIZATION ledger

Canonical sorted original arcs with n, SHA-256, malformed-source checks, source graph discovery, degree/pendant recognition, connectedness and structure verification, ordering, every one of five assignment edges, 32 unary-domain masks, all original accepting AND rejected assignment continuations, fan-out/sharing, n-mask vector copying and hashing, cache and eviction, exact BigInt arithmetic, output, grouped Boolean conversion and actual signed-literal CNF evaluation are all charged. Native five-way propagation is NOT unit-cost: the tested programs copy or encode n-domain state at each transition. Full OBDD serialization takes Omega(5S log S) bits when requested. No free source advice, SAT oracle, Z5 Fourier transform, tensor contraction or adaptive switch. The O(n+m) source recognizer is only asserted for the authenticated restricted class; general-case fallback may be exponential.

## Four verification gates, finite COMPUTATIONAL

G1: 12 authenticated connected SAT/UNSAT graphs from grids r=2..7, six Python/JavaScript canonical source SHA matches on independently generated saved sources, five malformed-source rejections, correct pendant structural recognition.
G2: 31,250 Python and 26,250 independent JavaScript pointwise original-assignment vs native-OBDD checks; 190 Python and 290 JavaScript complete prefix-multiplicity layer audits; 124 induced-matching residual probes; exact original assignment counts and (when built in both languages) observed width/node counts agree.
G3: 5,548 Python and 2,400 JavaScript ACTUAL signed-literal 3-bit validity-CNF evaluations, including 2,670 and 1,200 invalid-code cases respectively; all 2,048 oriented domain-mask pairs checked in each implementation.
G4: byte-identical repeated Python and independent JavaScript logs and JSON, zero unexpected failures; r=7 independently constructed in JS, Python algebraic count independently agrees. The independent r=7 JS propagator contained 61,014 SAT internal layer-state nodes, peak width 2,401, and 54 UNSAT internal nodes with width 5, contrasted with the source-aware width-one UNSAT OBDD. The live map holds every surviving state (no eviction); native mask-cache storage is O(nW) mask entries plus key, exact-count and language-runtime overhead. Each transition hashes an O(n)-length mask key, so OBDD transition count cannot be treated as physical microstep time. Formal mathematical referee audit, LaTeX compile and physical Turing-machine microsteps remain outstanding.

| r | vertices | exact SAT count | exact UNSAT count | Python SAT propagator width | Python UNSAT propagator width |
|---:|---:|---:|---:|---:|---:|
|2|5|60|0|16|5|
|3|10|820|0|56|5|
|4|17|26040|0|161|5|
|5|26|1936620|0|461|5|
|6|37|338656320|0|1181|5|
|7|50|139566652360|0|not constructed in Python|not constructed in Python|

The measured width 5 of the UNSAT *unoptimized propagation* program is NOT its minimum; source-aware detection provides a width-one complete rejecting OBDD. Do not confuse observed compilation sizes with proved asymptotic minima.

## Next dependency

D4-T5-DECISION-SPECIFIC-SOURCE-MACHINE-TRANSFER-094: require a quantified lower bound for uniform machines deciding nonemptiness from original encoded G, including source-visible shortcuts and preprocessing. Stop using minimum full-assignment OBDD width as a proxy for SAT existence. Preserve previous /092 results; P versus NP remains OPEN.

References: Barto, Kozik and Niven, SIAM J. Computing 38(5) (2009), DOI 10.1137/070708093; Bryant, IEEE Trans. Computers (1986), DOI 10.1109/TC.1986.1676819; Razgon, arXiv:1709.08890 (2017), matching width methods (different formal setting).
