# LSPV-1: intrinsic girth-eight T5 H24 with zero-incompatible spanning-tree core

Date: 2026-11-18 America/Los_Angeles. General SAT Lower-Bound Lead, historical Route B. Status: **PROVED/EXACT finite counterexample** plus independent COMPUTATIONAL verification; unrestricted witness-time lower bound **OPEN**. P versus NP **OPEN**.

## Candidate and falsifiers

Candidate source-structure conjecture to falsify: every intrinsically edge-minimal T5-UNSAT obstruction of sufficiently high undirected girth must contain a cycle in its graph of threads whose endpoint relations exclude equal colors. Falsifiers: (1) an actual source with undirected girth at least seven, (2) an edge-minimal UNSAT source rather than a detached gadget, (3) a forest of zero-incompatible threads, and (4) independently verified complete T5 witnesses for every original-arc deletion. The following H24 meets all four.

## Exact native source

Colors are Z5 with R(a,b) iff (b-a) mod 5 is 1 or 3. Start with a K4,4 branching core, bipartition {0,1,2,3} and {4,5,6,7}. For each pair (i,j) in lexicographic row-major order add a private degree-two vertex 8+4i+(j-4) and a two-arc path. An F step goes forward from left to right; B goes backward. The 16 words are

    FB FB FF BB
    FB BB FB FB
    FF FB FB FB
    BB BB BB FB

Canonical source: research/agents/lspv-1/certificates/2026-11-18_LSPV1_H24_GIRTH8_CRITICAL_NO.t5. Its expected SHA256 over exact ASCII bytes is 956350298fed8ba27c5570bce8cc1176ad68da2918bfc91c548ae27c49ad0d9c. Its 24 vertices, 32 original arcs, undirected girth eight, cycle rank nine and two-vertex connectivity follow directly from the once-subdivided K4,4 skeleton.

The three length-two endpoint-difference supports are FF={1,2,4}, FB={0,2,3}, BB={1,3,4}. Only FF and BB forbid equal branch colors. In this H24, their seven core edges are
(0,6),(0,7),(1,5),(2,4),(3,4),(3,5),(3,6).
These seven edges form a spanning TREE on the eight branch vertices. The other nine edges all have type FB and permit equal endpoint colors.

## Exhaustive proof of intrinsic criticality

The global rotation a->a+c permits setting the color of vertex 0 to zero. Enumerate all 5^7=78,125 assignments on the eight branching vertices, testing the 16 exact endpoint supports. For H the number of passing assignments is **zero**. Deleting each thread in row-major order gives these strictly positive anchored solution counts:

    14,4,1,6,15,10,11,4,21,15,9,14,9,11,20,1

Removing either of the two original arcs of a given thread makes its endpoint relation unrestricted; every endpoint pair then has exactly two private internal completions. Thus each one of the 32 original arcs is essential, and H is connected, source-intrinsic and edge-minimal UNSAT. This is a complete finite exhaustive proof when checked using the included transparent 5^7 enumerator, not a sampled inference.

An independent original-arc AC3/MRV solver, which does not use the endpoint table, found H UNSAT in 23 recursive calls and produced all 32 complete H-e witnesses in at most 31 calls per deletion, validating each retained source arc and confirming each omitted arc is violated. The longer original-arc raw witness dataset is included in the local reproducibility archive; the compact GitHub reproducer repeats the complete source-aware test.

Each core branch has forbidden-color weighted degree 8 (four length-two threads, weight two apiece). After any thread deletion, both endpoints still have load six, so weighted-4 peeling leaves the whole core. Even that persistent nonempty weighted-five core is not evidence of unavoidable expensive SAT witness construction.

## Scope and consequence

**FALSIFIED:** A cycle among zero-incompatible threads is a necessary structural condition for edge-minimal T5-UNSAT even at undirected girth eight. This does not contradict the existing short-thread forest SAT certificate, because the graph of *all* length<=3 threads here is K4,4 and has cycles. Weighted-core degree-five necessity also remains valid.

**PROVED/EXACT finite:** A smaller explicit girth-eight intrinsically critical example than the previously cataloged 33-vertex/44-arc fixture, with easy reconstructible SAT-only witnesses after all deletions.

**OPEN:** No asymptotic family with increasing girth or unrestricted uniform witness-time lower bound follows from this finite construction. Every step of source recognition, original-arc parsing, branch enumeration, failed search, path reconstruction, verification and output is charged in the reproducible algorithms; the numerical 23/31 AC3 calls are finite measurements, not worst-case lower bounds. Continue testing GF(5) cycle syndromes, exact DP/treewidth, alternative variable orders, compression, algebra and compact circuits.

Prior LSPV-3 weighted-thread theorem and TMR-2/093 GF(5) cycle syndrome theorem are retained. General T5 homomorphism NP-completeness (Bang-Jensen, Hell & MacGillivray, SIAM J Discrete Math 1988, DOI 10.1137/0401029) and Kun's fixed-girth sparse incomparability theorem (Combinatorica 2013, DOI 10.1007/s00493-013-2405-4) do not establish NP-hardness of this stronger growing-girth edge-critical SAT deletion witness promise.

DISJ, relativization, simultaneous DTISP and deterministic-configuration-count lower-bound gates: not promoted, since no separation is claimed. Independent LSPV-5/TMR peer audit OPEN. Existing roles/titles/timezones/schedules/enable states preserved, no agent activated. TMR-owned manuscripts and historical proof trackers unmodified. **MANUSCRIPT REVIEWED; NO MATERIAL CHANGE.**