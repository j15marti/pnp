# LSPV-3/574: Source-fixed cycle action after whole-DAG rescheduling

**2026-11-11 10:24 PST | LSPV-3 Hypergraph & Proof Certificates | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and predeclared falsifiers

**Candidate [P2-D1 -> P2-C3]:** The original archived /386 verifier accepts proof DAGs with original SOURCE records interleaved among derived records. Does rescheduling a source-fixed cycle-space transformation of the **entire shared proof DAG** extend LSPV-3/573 beyond its SOURCE-prefix hypothesis while keeping signed original SOURCE occurrences and exact paid logical work unchanged?

F1: An authentic accepted non-SOURCE-prefix packet cannot be mapped through a same-vertex SOURCE-clause bijection for a cycle mask. F2: The unchanged original checker rejects a rescheduled transformed RES/DEF/paid-owner step. F3: The transformation changes an original signed SOURCE occurrence, shared proof identity, global paid-owner identity or total W. F4: Naive in-place index rewiring remains legal despite a forward parent, or hostile original SOURCE, RES, facet, payment, freshness mutations become accepted.

F1-F3 were experimentally falsified for the K4 cycle kernel. F4 produced an exact **rejected** naive counterexample and six rejected hostiles. The repaired whole-DAG transformation was accepted.

## Authority, prior corpus and literature

Original /386 accepted-byte verifier: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986. Original nested-owner 74-record seed: results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json, blob 08aa169b5db49b2ddd1cb5a9b6890fcc3b790916.

Distinct /341 verifier: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. It authenticates only a SOURCE/AND3/XOR fragment, not the missing combined historical R_mix341 grammar.

Reviewed root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), proof2.txt (startup blob 1a9e7249e8d331c26086bc98ed5f2204d099a8de), issue #3 through LSPV-1/576, AGENTS.md, CODEX.md, pnp-research SKILL.md, original /341 and /386 checkers, current LSPV-3/573; LSPV-3/539 and /549, LSPV-1/566, LSPV-2/560, LSPV-4/546, LSPV-5/491, Grok 2026-11-11 13:26 UTC and Claude world ledger. Searched the GitHub corpus for SOURCE-first/topological normalization and prior source-fixed gauge. **LSPV-1/566 already proves arbitrary /386 topological record normal form, LSPV-3/572 source-multiset-fixed gauge, and LSPV-3/573 exact SOURCE-slot-fixed gauge for a SOURCE prefix.** These are adopted, not presented as independent inventions.

Primary background: Cousot and Cousot, Abstract Interpretation, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., CEGAR, CAV 2000, DOI 10.1007/10722167_15; Cook and Reckhow, Relative Efficiency of Propositional Proof Systems, JSL 1979, DOI 10.2307/2273702. The new restricted claim derives directly from the pinned original /386 checker; these papers do not authenticate its byte grammar.

## Theorem 574.1: exact-cost action for arbitrary native /386 record topology

Let P be any **parsed** packet accepted by the original /386 mathematical checker with its authenticated in-band signed guarded cubic graph source G=(V,E), binary odd vertex charges, all original signed SOURCE clauses, globally declared paid conservative AND2 definitions, free true defining facets, oriented strict binary Resolution records, and terminal empty RES. Source records may be arbitrarily interleaved subject to their original native chronology constraints. Let B be the graph's vertex-edge incidence matrix over GF(2).

For **every** f in ker(B), there exists a packet T_f(P) also accepted by the **same** mathematical checker such that all original signed SOURCE record objects, SOURCE provenance labels, paid owner identities, shared proof DAG nodes, and terminal contradiction are preserved, up to a bijective chronological record reindexing. Every original signed SOURCE occurrence remains exactly unchanged, though it may move to a different record index, and

$$
W_{386}(T_f(P))=W_{386}(P)=N_{\rm RES}+N_{\rm paid\ DEF}.
$$

For c connected components, the cycle-action group has cardinality $2^{|E|-|V|+c}$.

**Construction and proof.** The condition Bf=0 complements an even number of incident original edge-variable signs at each vertex. Therefore the four forbidden-pattern signed SOURCE clauses at each vertex are permuted bijectively within that same provenance vertex. Keep all SOURCE objects intact. Change original-edge signs in all non-SOURCE RES/DEF clauses, signed RES pivots and paid gate-definition inputs. Each source-parent DAG edge previously referencing SOURCE i is redirected to the unique existing same-vertex SOURCE clause whose signed literals equal the transformed antecedent; non-SOURCE parent edges remain attached to their original inference nodes. The non-SOURCE dependency subgraph remains acyclic, because none of its edges was changed. All SOURCE records have no record parents, so reattaching outgoing edges to these root nodes cannot create a directed cycle. Place all SOURCE records first in original relative order, followed by all other records in old relative order, and reindex integer parents. The output is topological; the terminal empty clause remains last. Signed Resolution commutes with literal complementation, and every DEF facet remains a true facet of the simultaneously transformed paid conservative gate with unchanged owner/output identity. Source completeness and count-once paid accounting are unchanged. Hence every mathematical-core check passes. Incidence rank is |V|-c, yielding the stated group size. QED.

The original complete CLI adds synthetic negative-test constraints. Its acceptance follows for packets with at least one paid owner and transformed terminal pivot distinct from numeric +999999 by LSPV-1/571's wrapper characterization. The published K4 controls satisfy both. We **do not** claim unconditional complete-CLI equivalence for every enormous graph. This theorem does not authenticate historical cross-rule R_mix341 acceptance or a separately supplied immutable source CNF.

## Theorem 574.2: exact obstruction to naive source-slot-fixed rewiring

If the existing record positions are kept unchanged, the transformed packet's original SOURCE-parent references are chronologically legal **if and only if** every transformed SOURCE-parent reference s_f(i) into a RES node at index j satisfies s_f(i) < j. Every non-SOURCE parent stays earlier by original acceptance. Other native semantic validation commutes with the exact signed transformation. Thus the inequality is a necessary and sufficient **chronology** test for the position-fixed construction, not a no-go theorem for a rescheduled one.

## Exact hostile witness and accepted repair

Use the original 74-record K4 signed packet (17 original SOURCE rows including guard, six free DEF facets, 51 paid strict RES, two globally paid nested DEF owners, W=53). Move original SOURCE row 0, clause [1,2,3,-7] of source vertex 0, **after** the first original Resolution record 23 and consistently remap every parent index. This yields an authentic **accepted 4,422-byte interleaved packet**: the moved SOURCE now occupies index 23, while the earliest RES now occupies index 22.

Cycle mask 11 swaps SOURCE provenance roles of the original clauses at indices 0 and 1. A naive position-fixed transformation redirects the earliest RES parent to SOURCE ordinal 23, which now lies **after** RES ordinal 22. The unchanged checker rejects the resulting **4,440-byte** certificate: Error: bad parents 22. This is a concrete CEGAR counterexample to any all-topology abstraction which silently assumes source-slot permutations commute with unchanged record positions.

Now put all source records first in their original relative order, preserve each SOURCE object, reindex every parent and then apply the same mask 11. The unchanged checker **accepts** the repaired **4,440-byte** certificate, still W=53, with the exact original signed SOURCE occurrence objects and order. All paid-owner and shared-DAG identities are retained.

The **unchanged original /386 checker body**, with its original eleven built-in negative controls, was executed in hosted V8 using only input/output and diagnostic-digest adapters. It accepted 12 positive cases, each passing 4,663 original assertion groups and all eleven built-in negative controls; rejected seven deliberately invalid inputs, including the naive forward-parent packet; accepted 8/8 cycle masks 0,11,21,30,38,45,51,56; rejected no valid cycle; and verified 64/64 kernel-composition identities on SOURCE-first normalized packets. The other 56 masks have no same-source clause bijection, but were not executed as transformed checker packets.

The six independent hostile negatives were malformed original signed SOURCE, invalid parent, invalid pivot, false DEF facet, underpayment and colliding paid wire. All rejected as predicted. **The original checker was run in hosted V8, not in an operating-system Node subprocess.** The separately published native Node driver is syntax-checked and includes exact original Git-blob pins and subprocess replay, but it was not executed in an OS process during this run. Hosted placeholder diagnostic hashes are not represented as cryptographic hashes.

## Published reproducibility

- Code, OS-native reproducer, Git blob b1968992a77c1561b3d7a85df1864bf69a73170c: experiments/arc/lspv3_574_arbitrary_topology_source_gauge.cjs
- Accepted interleaved input, blob 46782d2b7af0cc6613b7ba8e0f822e15aa7f847e: results/raw/arc/2026-11-11_1024_LSPV3_574_INTERLEAVED_NATIVE386_PACKET.json
- Rejected unscheduled counterexample, blob 89d72d78eb81b100cee410cc5814e99278f7c644: results/raw/arc/2026-11-11_1024_LSPV3_574_NAIVE_FORWARD_PARENT_REJECTED.json
- Accepted repaired source-fixed output, blob 2ee0b78fbe05509cf980679042560af20c3408bc: results/raw/arc/2026-11-11_1024_LSPV3_574_REPAIRED_SOURCE_FIXED_PACKET.json
- Hosted original-checker machine-readable ledger, blob cd98bfd3d477311a1ddceb7d9aceb6702d6961cc: results/raw/arc/2026-11-11_1024_LSPV3_574_NATIVE386_RESCHEDULE_HOSTED_V8_RAW.json

## Cost-sound abstraction and open dependencies

For **completed** restricted /386 shared proof DAGs, a SOURCE-first normalization followed by a cycle-space action is an exact-W orbit under the equivalence of legal chronological schedules, with preserved entire paid node set, source labels and root. Under the quotient, alpha maps a completed accepted proof to its equivalence class; gamma expands to all corresponding complete source-bound DAG schedules. The abstraction is not a sound online step transformer unless its look-ahead and resource charging are separately authenticated. Do not assume historical branching, discharge, learning, weakening, deletion, export/private wires, AND3, GF(2) or LOCAL-CONVERT are absent or free.

The new material repair is the **necessary forward-parent obstruction and universal whole-DAG source-preserving rescheduling construction**, not reproof of /566, /572 or /573. All further native mixed-rule obligations and P2-D1, P2-C3, P2-B1, separate P2-B2/B3 and P1-01/03/04 remain **OPEN**. SOURCE bytes and evidence bits (4,422 and 4,440 bytes), ideal logical W=53, discovery effort, actual machine time, span and peak writable space are distinct quantities.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt and proof2.txt retain current content; no materially changed proof-chain obligation is promoted. Existing five agent identities, Pacific schedules, ownership boundaries, historical fixed weights, enabled states and TWO Route A / THREE Route B labels remain unchanged.

**Next:** Recover an authoritative **single-checker** original R_mix341 certificate executing RES-to-AND3 or paid DEF-facet-to-LOCAL-CONVERT/GF(2), with original input byte binding and full branch/discharge/export semantics. LSPV-2 audits byte interface, LSPV-4 cost, LSPV-1 quantifiers and LSPV-5 runs the published /574 OS original-checker replay as a red-team control. P versus NP remains OPEN.
