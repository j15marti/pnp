# TMR-3/073: exact five-symbol counting on near-complete triple-incidence graphs

Date: 2026-11-17 17:24 PST, America/Los_Angeles. Owner: TMR-3 / PNP Time-Space Tradeoffs.
Status: PROVED/EXACT restricted mathematical construction, external independent mathematics review OPEN. Two finite executions COMPUTATIONAL. P versus NP OPEN.

## Candidate, exact quantifiers, and falsifiers

The named target C3-T5-PARTIAL-TRIPLE-INCIDENCE-SIGNATURE closes a nontrivial /072 extension. For every integer k >= 4 and any set F of *missing* three-element subsets of [k], put U = union of missing triples, s=|U|, and assume s < k. Construct I(k,F) with k hubs, one private sink leaf for each triple not in F, and arcs from exactly its three hubs. There exists one uniform deterministic source-authenticated algorithm that counts EVERY full T5 coloring in O(poly(N) * 2^s) bit time with poly(N) writable bits. The all-source solver correctly falls back to forest enumeration on any valid input not recognized as this family.

Four designated falsifiers: F1 some pair of hubs not covered by a present triple, so two-palette rigidity fails; F2 a monochrome hub assignment counted twice by pair enumeration; F3 a missing monochrome leaf correction mistaken for the missing mixed-leaf correction; F4 incomplete source reading, discovery, big-integer precision, head seeking, output, or physically retained state invalidates the bound. All four are addressed below. A separate sparse three-palette counterexample falsifies extension to arbitrary partial triple hypergraphs.

## Source and template

The fixed template is Z5 with R(a,b) iff (b-a) mod 5 belongs to {1,3}, and Out(a)={a+1,a+3}. The canonical binary input consists of unary n, 0, unary m, 0, followed by exactly m directed arcs with low-bit-first endpoint indices of width max(1,ceil(log2 n)). The parser verifies all bits, delimiters, lengths and endpoints; duplicated arcs are normalized; loops and opposite arcs have exact count zero. On valid inputs output the exact nonnegative integer Z(G)=# {x:V->Z5 respecting all arcs}, then YES iff it is positive. Malformed inputs explicitly reject.

Source-derived family recognition identifies hubs by indegree zero and positive outdegree, sink leaves by outdegree zero and indegree three, checks they exhaust all vertices, checks each leaf has exactly three *distinct hub* parents, and checks that no two leaves have the same parent triple. It enumerates all binom(k,3) triples to find the actually missing set F, then tests s<k and k>=4. Recognition is not an oracle, and failed recognition returns to the all-input correct forest counter.

## Rigidity lemma

For distinct a,b, |Out(a) intersect Out(b)|=1 exactly when b-a is 2 or 3 modulo five; otherwise it is zero. A triple leaf permits two colors if all hubs have one color, one if its hubs use a compatible two-color pair, and zero otherwise. Every pair of hubs is contained in a present triple when s<k: for a pair inside U select a hub outside U, and for a pair meeting the complement choose any third different hub. Any triple containing an outside-U vertex must be present by definition of U. Consequently the colors on every pair of hubs must be equal or adjacent in the undirected compatibility graph (Z5, differences +/-2), which is a triangle-free five-cycle. All hubs therefore use at most two colors, and each distinct pair is uniquely one of the five unordered pairs {a,a+2}.

## Exact theorem and proof

Let r=k-s>=1, m=binom(k,3)-|F|. For each binary mask B subset U, put u=|B| and define

    f_F(B) = number of missing triples fully contained in B or fully contained in U\B.

For each p=0,...,r define

    e_F(B,p)=binom(u+p,3)+binom(k-u-p,3)-f_F(B),

with binom(t,3)=0 for t<3. Then the exact ORIGINAL graph count is

    Z(I(k,F)) = 5 * ( sum_(B subset U) sum_(p=0)^r
                              binom(r,p) * 2^(e_F(B,p))
                        - 2^m ).                                      (1)

Proof: Fix one of the five unordered compatible palettes, and call one palette symbol the first color. For a hub coloring with B first-colored inside U and p first-colored outside U, choose the outside indices in binom(r,p) ways. Each present monochromatic triple leaf has two permitted colors; each present mixed two-color triple leaf has one. Of all binom(k,3) possible triples, precisely binom(u+p,3)+binom(k-u-p,3) are monochromatic and precisely f_F(B) of those are absent. Independence of private sinks yields 2^(e_F(B,p)) complete original sink assignments. Every nonmonochrome hub labeling uses a unique compatible unordered pair and appears exactly once in the five-pair sum. Each of the five monochrome hub labelings belongs to two compatible unordered pairs, so each appears twice. It has 2^m sink completions; subtract 5*2^m to remove the surplus. This proves (1), with no lost multiplicities or assumed preloaded leaf colors.

When F is empty, s=0, formula (1) is algebraically identical to /072's complete-incidence formula. When d=|F|, s<=3d. Therefore this entire nearcomplete family has O(poly(N) 8^d) exact time, with polynomial writable space, hence polynomial time when d is bounded. This does NOT mean every 3-uniform incidence CSP is easy.

## All-input same-machine time, peak-space and query ledger

Use one fixed blank-start finite-alphabet, locally headed deterministic multitape machine. Original bit input length N satisfies n,m,k,d,s<=N.

Phase A (read/parse/normalize): charge all source bits, unary numbers, endpoint widths, malformed detection, duplicate normalization, loop/opposite-edge detection, adjacency construction, head travels, and working indices. Conservative time O((N+1)^6), aggregate live space O((N+1)^3) bits.

Phase B (source-derived recognition): construct indegrees/outdegrees and each private sink's actual parent set, reject nonfamily sources, enumerate at most binom(k,3)<=N^3 candidate identities, calculate F and U, and check all promises. All discovery/failed discovery and physical table seeks are charged. Conservative time O((N+1)^8), peak retained space O((N+1)^3) bits. No family oracle, source graph oracle or free stored triples.

Phase C (streaming specialized count): exactly Q=2^s(r+1) (B,p) terms, and at most d*2^s actual missing-triple scans. Every term charges bitmask formation, f_F(B), actual address and source-table access, binomial arithmetic, exponent construction, large integer shifts, exact multiply/sum, correction and output. A generous O((N+1)^7) bit-steps per term covers conventional machine-head movement and polynomial-size integer arithmetic. At all times intermediate integer length is O(k+m+1)=O(N): the uncorrected five-palette sum counts each legal coloring at most twice, and Z(G)<=5^n. Store the input-derived triple list, one mask, loop counters, binomial working values, accumulator and output buffer, NOT an exponential memo table. Complete recognized bound T=O((N+1)^10(1+2^s)), S_peak=O((N+1)^3) bits.

Phase D (nonfamily valid graph fallback): select a weak spanning forest, fix each component root color zero, enumerate the two legal edge differences for each of n-c tree edges, verify all original arcs, then multiply by 5^c independent component translations. Complete fallback bound T=O((N+1)^10(1+2^(n-c))), S_peak=O((N+1)^3) bits. Every valid input follows either Phase C or D after paid common preprocessing. Malformed inputs reject. Correct YES/NO is exact count nonzero. These budgets are for one sequential machine and charge output and simultaneous live workspace, not a parallel span or a preloaded answer/checkpoint.

## Counterexample to unrestricted two-palette inference

Five hubs with only two private leaves, indexed by {0,1,2} and {2,3,4}, permit the hub coloring (0,2,2,4,4). The first leaf has the unique common successor of {0,2}, and the second has that of {2,4}; hence the coloring extends despite using THREE hub colors globally. The missing support includes every hub, so s=k and this source is correctly routed to fallback. The near-complete restriction is load-bearing.

## Actual executions and pinned evidence

The exact, readable, role-owned JS reference source at experiments/tmr/tmr3_t5_nearcomplete073.js (Git blob a5375b344c4ea15ce6e2f7be17ffecd39e4304f4) was ACTUALLY executed twice in V8 on its final source. Two byte-identical outputs, 85 independent specified comparisons, zero failures. It tests small 5^k hub enumerations, source decoding/recognition, full-graph forest fallback, the sparse three-color control and k=14 with one missing triple. Immutable raw at results/raw/tmr/2026-11-17_1724_TMR3_T5_NEARCOMPLETE073_V8_RAW.json.

Separately, a genuinely independent readable Python 3 implementation ran twice locally, seed 202611171724, with byte-identical raw JSON. The complete local Python script SHA256 is f57db192dce415e1cd0ee2713a9e5bc723806166647d7be1c1bb74162952a112; local raw JSON SHA256 is 7f330c16ffcb049a805d706d2d76dd978234384e1bffdd2d59d36a85815a69fa. It completed 266 checks, including 59 recognized-family and 70 generic-fallback instances, zero failures. The Python file is local evidence, not claimed GitHub-published. Both independent implementations count I(10,{(0,1,2)}) as 3323069990719572559518672062266736640 (129 original vertices, 357 arcs). The complete H_10 has 130 vertices and 360 arcs. Finite tests are COMPUTATIONAL and do not measure a native local-head TM trace.

A local repository checkout was unavailable, so no repository preflight or full LaTeX compilation was executed. External mathematical review and native TM microcode execution remain OPEN. Complete repository readback and exact blob verification are separate publication checks.

## Four verification gates and scientific guards

DISJ sanity: PASS restricted. No static rank to compulsory computation lower bound. Relativization: NOT APPLICABLE WITH REASON to a separation, because this is a positive exact algorithm; BGS, algebrization and Natural Proofs remain OPEN for any future unrestricted proof. Simultaneous DTISP: PASS restricted for the same-machine complete parsing, discovery, evaluation, arithmetic and output ledger; no SAT resource lower bound is claimed. Deterministic configuration counting: PASS as upper-bound consistency only, never a deterministic time lower bound or randomized/quantum assertion.

Horn/2-SAT, affine/Gaussian, bounded treewidth, equalities, autarkies, products, padding, selectors, unique solutions, field changes, auxiliary multiplicity, modules, caching and every other legal exact solver remain admissible. The older /341 is FAIL as full UNSAT authority; /386 is RESTRICTED. T5 decision is NP-complete by Bang-Jensen, Hell and MacGillivray (1988), but that classification does not independently give a quantified SAT-to-T5 exponent transfer. TMR-5/074 separately reports a source-checked linear-vertex SAT-to-T5 construction, subject to its own review; no forbidden resource pair is inferred here. P versus NP OPEN.

**ONE next lemma (OPEN): C3-T5-HOLES-WITHOUT-UNIVERSAL-HUB-QUOTIENT.** Seek a source-authenticated, efficiently constructible exact weighted color-signature when the support of missing triples covers every hub, or give a concrete dense-source obstruction to the proposed quotient. Include original sink multiplicities, head operations, and same-execution space.

## Primary source and predecessor

Bang-Jensen, J.; Hell, P.; MacGillivray, G. (1988). The Complexity of Colouring by Semicomplete Digraphs. SIAM J. Discrete Math. 1(3):281-298. DOI https://doi.org/10.1137/0401029 . Journal abstract explicitly establishes NP-completeness when the semicomplete template has more than one directed cycle. Predecessor TMR-3/072 original report: research/agents/tmr-3/2026-11-17_1624_TMR3_T5_PRIME_TRIPLE_INCIDENCE072.md, Git blob 2cd90e491730625f03f474a360a51de2a7ca9251. Its complete-incidence formula and all previous source-authenticated upper algorithms remain intact.
