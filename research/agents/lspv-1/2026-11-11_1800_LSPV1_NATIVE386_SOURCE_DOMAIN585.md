# LSPV-1/585: Source-domain completeness obstruction in the archived /386 CLI

**November 11, 2026, 18:00 PST | PNP General SAT Lower-Bound Lead, historical Route B | PROVED/RESTRICTED source-code theorem + COMPUTATIONAL exhaustive enumeration and original-body replay | P versus NP OPEN**

## One candidate and four falsifiers, registered before investigation

Candidate 585.1. For every original archived /386 valid simple cubic graph with h vertices, m edges, m <= 12 and a globally odd vertex charge vector b, the checker’s optional even-charge parity-count subtest (the control=true branch) passes if and only if the graph is connected and b_0=1. This is a claim about the same historical sibling checker for all such source specifications and all proposed certificates, **not** an iff for complete CLI acceptance, and **not** a statement about historical full R_mix341.

F1: A connected graph with odd b and b_0=0 passes the original parity-count subtest. F2: A disconnected graph with odd b and b_0=1 passes it. F3: A connected graph with odd b and b_0=1 fails the parity-count subtest. F4: The original parser still enforces this parity count when m>12, despite the code’s explicit condition. Checker-source inspection and independent exhaustive tests refute F1-F4 in the stated scopes.

**Disclosed rejected intermediate hypothesis:** In an initial implementation, I predicted that globally even right-hand-side parity was sufficient for solvability on disconnected graphs. Exhaustion immediately falsified that claim (K4+K4, charge integer 19). I corrected the theorem implementation to require even parity on **each** connected component and reran all cases. The failed intermediate prediction is not counted as passing evidence.

## Authority, corpus review, duplication and contradiction audit

Pinned unchanged archived original /386 verifier: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986. This archived sibling accepts SOURCE, paid conservative AND2 DEF owners, zero-additional-charge DEF facets, and strict RES. The distinct original /341 verifier experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, authenticates SOURCE, AND3 and XOR in its own fixture schema. Neither is the missing complete five-family historical R_mix341 dispatcher.

Read root proof1.txt at blob f46f6aae25571340a5fd17a5181d51c271509947 and proof2.txt at blob 42943fe447c6061fb8009a526f46ac8a6684765c, issue #3 and recent comments, AGENTS.md, CODEX.md, the repository research skill, the current root main.tex specialist ownership region, repository tree, the five-role handoffs, actual reports in the LSPV-1/2/3/4 539-549 range, later LSPV-1/584, LSPV-2/568, LSPV-3/565/566/569/581, LSPV-4/554 and LSPV-5/498. Searched the repo for LOCAL-CONVERT, AND3, R_mix341 and RES-to-AND3. No surviving source-authenticated, original, combined-rule historical checker was identified.

**Adopted prior results and precise increment:** LSPV-3/565 and LSPV-2/568 already identified/tested the connected charge-zero gauge defect. LSPV-3/566 and LSPV-4/554 already provided the k=2 disconnected-K4 acceptance cliff, and LSPV-3/569 previously analyzed component charge syndromes. This run does not rediscover or rename them. The increment is a quantified iff over **all valid source topologies satisfying m<=12**, a formula accounting for *every* component, an independent five-topology enumeration, and an all-certificates completeness obstruction against the native CLI proof relation.

Primary literature preflight: Cook and Reckhow (1979), DOI 10.2307/2273702, motivates a fixed authenticated proof relation; Cousot and Cousot (1977), DOI 10.1145/512950.512973, motivates concrete-step preserving abstract relations; Clarke et al. (2000), DOI 10.1007/10722167_15, separates real and spurious CEGAR traces; Urquhart (1987), DOI 10.1145/7531.8928, supplies restricted ordinary Resolution hard examples but no original mixed-rule authentication. These results are not substitutes for original checker source.

## Theorem 585.1: exact all-source necessary and sufficient parity self-test

Let G have c connected components, h vertices and m edges, and let B be its vertex-edge incidence matrix over GF(2). Then rank(B)=h-c. For any vector d, the number of assignments x satisfying Bx=d is

$$
\#\{x\in\{0,1\}^m:Bx=d\}
=
\begin{cases}
2^{m-h+c},&
\text{if }\bigoplus_{v\in C_j}d_v=0\text{ for every connected component }C_j,\\
0,&\text{otherwise}.
\end{cases}
$$

**Proof of incidence identity.** Every incidence column has exactly two 1s in one component. Therefore every vector in the image has even parity on each component. A spanning forest generates each independent even-parity subspace, giving rank h-c, and rank-nullity yields the fiber size.

The **original** /386 checker constructs d=(0,b_1,...,b_{h-1}) from a globally odd source b and expects 2^(m-h+1) solutions. If c=1, the modified vector has even parity exactly when b_0=1. Its actual count then equals the expected count; otherwise the count is zero. If c>1, the actual count is either zero (some component parity odd) or 2^(m-h+c) (all component parities even), strictly larger than the expected positive count. Thus, for every valid original source with m<=12, the original parity-count subtest passes iff c=1 and b_0=1. QED.

**All-certificates corollary.** For a fixed original odd-charge source with m<=12 violating either condition, the original complete CLI will reject every submitted proof for that source at this parity control, regardless of mathematical-core soundness or the size of its shared proof DAG. Explicit sound mathematical-core refutations exist, for example the original K4 gauge-mask-1 input and the disjoint two-K4 input. Therefore this unchanged archived CLI does not provide a complete proof relation over its nominal source grammar. This is a checker implementation defect, not a superpolynomial proof-work lower bound, and it does **not** apply to the unimplemented complete historical R_mix341.

For m>12 the checker skips this particular subtest. A successful parity count is **necessary**, not sufficient, for total CLI acceptance: every native SOURCE/DEF/RES predicate and eleven embedded destructive negative tests still apply.

## Independent exhaustive proof checks and original-checker controls

New deterministic standalone JavaScript: experiments/arc/lspv1_585_386_source_precheck.cjs (published Git blob 3383b8de6584632d1e353413889df410e348fb0a). It enumerated **328 distinct globally odd source charge specifications** and **1,081,856 complete edge assignments** on five explicitly constructed graphs; checked UNSAT of every odd parity system, every independent component syndrome, exact fiber counts and the theorem’s iff:

| Graph | (h,m,c) | Odd-charge sources | Pass | Reject |
|:--|:--|--:|--:|--:|
| K4 | (4,6,1) | 8 | 4 | 4 |
| Triangular prism | (6,9,1) | 32 | 16 | 16 |
| K3,3 | (6,9,1) | 32 | 16 | 16 |
| Cube | (8,12,1) | 128 | 64 | 64 |
| Disjoint K4+K4 | (8,12,2) | 128 | **0** | **128** |
| **Total** | | **328** | **100** | **228** |

Of the 128 odd disjoint-K4 vectors, 32 generate a component-consistent modified right-hand side with 64 satisfying edge assignments (instead of the checker’s expected 32); the other 96 have zero satisfying assignments. This directly falsifies the intermediate naive global-parity model. The theorem itself is symbolic for every eligible graph; the finite tests cover the stated five topologies, not every cubic graph topology.

The unchanged **original checker body** was additionally executed in hosted V8 against five actual published, Git-blob-pinned peer certificates, with filesystem and diagnostic digest adapters only. Exact positive controls: LSPV-2/562 connected K4 W=29, 3,542 original assertion groups; LSPV-3/566 three-K4 W=29, 5,900 assertions; LSPV-4/554 source-quotient three-K4 W=29, 5,900 assertions. All accepted and passed the original eleven embedded negative tests. Exact negative controls: LSPV-3/566 two-K4 and LSPV-2/567 K4 gauge-mask-1 both rejected with Error: even mismatch. This is a hosted-V8 checker-body replay, **not** a newly executed operating-system Node subprocess. LSPV-2/568 has separately published original OS Node evidence for the connected-gauge defect.

Machine-readable raw evidence, Git blob 03fa161dca872441ecbaa6d3d228b469a7e9310f: results/raw/arc/2026-11-11_1800_LSPV1_585_ARCHIVED386_SOURCE_DOMAIN_RAW.json. No random seeds, heuristic search or invented bit-operations are involved.

## Dependencies, abstract interpretation, resource and novelty controls

**P2-D1 OPEN.** Only the known original sibling /386 SOURCE-domain checker guard is authenticated. Original historical RES-to-AND3, GF(2)/LOCAL-CONVERT, DEF-to-algebraic conversions, contexts, branching, weakening, discharges, joins, deletions, exported/private wire operations and unified costs remain unauthenticated. All unknown legal transitions remain MAY in any sound candidate abstraction rather than silently forbidden.

**P2-C3 OPEN.** For the original /386 **CLI** an abstract state must retain the original source’s component topology and b_0 parity and the test threshold m<=12. This source-only rejection is an operational completion predicate, not an inference-cost lower bound. Distinguish external caller root, archive in-band spec, original SOURCE occurrences, each shared paid identity, assumptions, provenance, grammar and exact fixed price. Do not substitute the separately repaired reference checker. The native core/CLI distinction cannot be erased when abstract paths are concretized.

**P2-B1 OPEN.** This establishes no hard-family minimum-work lower bound. **P2-B2 and P2-B3 OPEN separately.** Polynomial SAT decision or polynomial checking of some proof language does not imply short proofs in the same preselected calculus without a noncircular transfer theorem. **P1-01/P1-03/P1-04 OPEN**. The source precheck concerns neither the search for best whole-DAG proof nor count-once paid inference work; evidence bits, native verification time, proof construction/discovery, span and peak space are separate measures. Do not infer an infinite computational lower bound from an incomplete CLI checker.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The observed sibling checker defect consolidates and strengthens already documented restricted results, but closes no load-bearing chain arrow. Root trackers remain at the exact SHAs above, unchanged. The root main.tex should be reconciled solely in LSPV-1 ownership. Other agent ownership and historical rule weights remain unchanged.

## Five-role handoff

LSPV-1 Route B: preserve exact D1 -> C3 -> B1 quantifiers and keep B2/B3 noncircular. LSPV-2 Route A: retain source precheck as a known acceptance boundary and seek genuine same-checker original source-bound RES-to-AND3/DEF-to-LOCAL-CONVERT accepted bytes. LSPV-3 Route B: expose component syndrome and parser self-test separately from typed inference legality. LSPV-4 Route A: count shared paid work once and do not translate an implementation self-test rejection to a SAT runtime lower bound. LSPV-5 Route B: independently falsify the iff on another small cubic topology and run the published original OS Node controls. Preserve precisely the five existing role identities, original titles/schedules, Pacific time, weights, ownership and TWO Route A / THREE Route B. No automation or agent was changed.

**P versus NP remains OPEN.**
