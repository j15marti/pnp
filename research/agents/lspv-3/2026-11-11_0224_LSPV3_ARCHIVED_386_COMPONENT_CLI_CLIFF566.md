# LSPV-3/566: archived /386 native SOURCE-component CLI acceptance cliff

**2026-11-11 02:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED original-code theorem + COMPUTATIONAL exact original-body replay | P versus NP OPEN**

## Candidate and four falsifiers registered before testing

**Candidate:** The original archived /386 SOURCE / paid conservative DEF owner / free facet / strict Resolution checker does **not** impose connectedness of its complete original graph. Consequently a valid short K4 refutation can be embedded in any disjoint union of K4 components, retaining an exact complete signed SOURCE ledger and unchanged paid proof DAG. The mathematical checker accepts every embedding. Its **complete original CLI**, however, can reject the two-component packet while accepting three or more components, because its even-charge regression control assumes connectedness when E<=12 and is skipped for E>12. This is an accepted-byte parser/checker distinction for the actual archived /386 implementation, **not authentication of the missing full R_mix341 grammar**.

Precommitted falsifiers: **F1** a source clause, sign, guard, vertex identity or parent changes illegally; **F2** an original core proof or required control rejects a genuinely valid packet for a reason other than the identified connectedness bug; **F3** the full CLI has the same acceptance response on k=2 and k=3, contrary to the precise E<=12 cutoff; **F4** the 28 RES parent DAG, gate-owner cost or terminal contradiction changes when only complete, unused original SOURCE records are added. Source, typing, graph, mutation, tariff and CLI tests below refute F1-F4 for the constructed packets.

## Authenticated original source and scope

Original archived checker: `experiments/arc/lspv2_386_independent_verify.js`, exact Git blob **338305c0ce101704205e57543756b8127074a986**. It was independently written in the historical project and is the **actual pinned archived program** executed here, not a claimed recovered unified mixed-rule program. Seed packet: LSPV-1/568, `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json`, blob **e3eb2a46857776089ab83f4ad50159ef622d2869**, with 17 original SOURCE records, 28 paid RES and one conservative paid-but-unused DEF owner. Its source formula is guarded 4-CNF, **not a proper unguarded width-three source**. The checker itself generates expected signed source clauses from `spec`; it does not verify an externally supplied original DIMACS hash.

By direct source inspection, `checkProof` checks h even, 3h/2 edges, distinct sorted vertex pairs, three incident edges per vertex, exact signed local parity clauses, guard SOURCE, paid definition declarations, chronological RES parent indices, signed pivots and exact resolvents. It does **not** check that the graph is connected. `control=true` enumerates edge assignments **only if E<=12** and tests the even-charge model count against **2^(E-h+1)**, a connected-graph rank formula. Its complete CLI also performs eleven negative packet mutations, one of which requires a paid gate owner to exist.

The distinct /341 original recovered fixture checker `experiments/arc/lspv2_341_independent_verify.js`, blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**, still dispatches only AND3/XOR; it does NOT accept RES/DEF/LOCAL-CONVERT. The original historical five-family declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob **c87acd11d32ccfc3b7acd3667ef11daeb60079cb**, is not an executable full mixed byte parser.

## Theorem 566.1: exact native-core constant-work component embedding

**PROVED/RESTRICTED (readable original code and explicit packet construction; independent review pending).**

Let k>=1. Form the disjoint union G_k of k copies of K4, so h=4k, E=6k, and use charge vector b=(1,0,...,0) on the 4k vertices. Set the unique guard variable g=6k+1, paid but unused conservative gate output z=g+1, and owner definition `[0,z,1,4]`. For each vertex include the original verifier's four exact canonically sorted guarded forbidden-parity clauses; include the guard SOURCE `[g]`. There are **16k+1 distinct SOURCE records**. The first copy's source is an odd-charged K4 and all remaining copies are even-charged K4 components. Since every graph edge touches exactly two vertices, the first component cannot simultaneously satisfy its four vertex parity conditions. Thus each source formula F_k is UNSAT.

Take the original LSPV-1/568 W=29 packet; consistently replace old guard 7 by g and old gate output 8 by z, including their signed appearances and signed RES pivots. Append **16(k-1)** fresh SOURCE records for the additional components immediately **before the final RES record**, not inside the proof's existing ancestry. The original 28 RES nodes and all their ordered parent *indices* remain unchanged; the terminal node simply moves to the end of the extended array. The paid owner stays globally fresh; its single declaration is charged exactly once, although unreferenced. All additional sources have exact vertex provenance, no premises and zero inference cost.

Induction through the unchanged original 28 RES records validates every same-signed pivot, strict resolvent and parent. Independent SOURCE regeneration validates all 16k+1 original clauses; source counts, summary and terminal sink are exact. The unchanged original `checkProof(dat,{control:false})` therefore accepts for every finite k>=1 with

$$
m_k=16k+1,\quad R_k=28,\quad G_k=1,\quad W_k=R_k+G_k=29,\quad
\#\mathrm{records}=16k+29.
$$

This **does not** establish that every SOURCE record is essential: only the first K4 component participates in the contradiction. It furnishes an explicit native-core counterexample to a source-*count*-only positive paid-work lower bound for unrestricted disconnected inputs in this archived checker, not a bound for certified connected expander families.

## Theorem 566.2: complete-CLI acceptance is nonmonotone under source-component padding

**PROVED/RESTRICTED for the given program, conditional on the published source and packet; independently reviewable code proof.**

For k=1, the even-charge regression `[0,...charge.slice(1)]` is the all-zero charge, with **2^(6-4+1)=8** valid edge assignments, so the original control accepts. For k=2, there are **two** connected components; the all-zero even-charge linear incidence system has rank h-2 and hence **2^(12-8+2)=64** models, while the checker expects **2^(12-8+1)=32**. The mathematical core accepts but `control=true` and full CLI reject with `even mismatch`. For every k>=3, E=6k>12, so the checker **skips the model-count check completely**. All eleven bundled hostile mutations still fail for this specific k-family, as each changes a checked source, unique paid owner, parent, pivot, total charge, graph or terminal clause. Thus the original complete CLI accepts every k>=3 packet in the family while rejecting k=2.

This is a **checker regression-control topology bug** and a size-dependent acceptance cliff, not a SAT-soundness attack and not an in-calculus free graph-padding operation. Source F_k changes with k; original-source bytes and graph size are **not** preserved across different k.

## Exact hosted-V8 original-body measurements

The original checker source and all its eleven complete-CLI negative tests ran in hosted V8 with only virtual file input, output-only SHA display and `structuredClone` adapters. The mathematical `checkProof` source and negative-test bodies were **unchanged**. **No operating-system Node subprocess was executed in this hosted run.** The separate complete stand-alone Node reproducer invokes the exact archived checker in a real OS subprocess when run in a checkout; that route is published but not claimed as executed here.

| Copies k | Signed sources | Native core | Native `control=true` | Complete original CLI | Paid W | Compact JSON bytes |
|---:|---:|---|---|---|---:|---:|
| 1 | 17 | ACCEPT | ACCEPT, even=8 | ACCEPT; 3,542 assertions | 29 | 2,866 |
| 2 | 33 | ACCEPT | **REJECT**, even=64 vs expected 32 | **REJECT**, `even mismatch` | 29 | 3,933 |
| 3 | 49 | ACCEPT | ACCEPT, enumeration bypassed | ACCEPT; 5,900 assertions | 29 | 4,992 |
| 4 | 65 | ACCEPT | ACCEPT, enumeration bypassed | ACCEPT; 7,080 assertions | 29 | 6,064 |
| 5 | 81 | ACCEPT | ACCEPT, enumeration bypassed | ACCEPT; 8,260 assertions | 29 | 7,137 |

Independent JS construction verified **every** original signed SOURCE clause against an independently reconstructed incidence/parity multiset and that the graph has exactly k four-vertex components. Nine hostile native-core mutations were all **REJECTED**: deletion, forged signed source, duplicate source, wrong charge, underpayment, false pivot, malformed owner, duplicate graph edge and forged SOURCE parent.

**Positive legal shortcut, retained rather than refined away:** removing the *unused* paid owner declaration from the k=3 packet and correcting paid summary to W=28 gives another genuine native mathematical-core **ACCEPT**, while the original full CLI **REJECTS** because its `gate_defs.shift()` corruption becomes a no-op. This reuses LSPV-1/568's no-owner control in the new disconnected family. It is not a corrupted certificate. Any CEGAR cost invariant assigning an unavoidable 29 paid nodes to the original core source would be falsified by this legal W=28 witness.

## Publication artifacts and exact Git provenance

- Report (this document): `research/agents/lspv-3/2026-11-11_0224_LSPV3_ARCHIVED_386_COMPONENT_CLI_CLIFF566.md`.
- Standalone Node full-checker reproduction: `experiments/arc/lspv3_566_disconnected_386_native_replay.cjs`, Git blob **4638a5a305fa12c577799e3270d9cb0aad191311**. Run `node experiments/arc/lspv3_566_disconnected_386_native_replay.cjs`; `--write` writes a separate OS-native raw ledger and does not overwrite hosted V8 evidence.
- Original-body raw V8 results: `results/raw/arc/2026-11-11_0224_LSPV3_566_COMPONENT_CLI_CLIFF_RAW.json`, blob **4c22e1a1ecf2d19edf79c56acbf3e705c6326292**.
- Exact k=2 core-accepted / CLI-rejected packet: `results/raw/arc/2026-11-11_0224_LSPV3_566_K4x2_CORE_ONLY_PACKET.json`, blob **a193e874ccb2b87642738da00ca5a95c5a6501ae**.
- Exact k=3 complete-CLI-accepted packet: `results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json`, blob **4656b801feba72b84133bacad5ae18692a83fe03**.
- Five-role handoff: `research/coordination/2026-11-11_0224_LSPV3_COMPONENT_CLI_CLIFF566_FIVE_ROLE_HANDOFF.md`.

## Literature and corpus audit

Required project context reviewed: complete root `proof1.txt` blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b**, root `proof2.txt` blob **20fd65cf8842d32a851a14a1496c7ea6156cb160**; issue #3 and latest comments, `AGENTS.md`, `CODEX.md`, research skill, last LSPV-3/565 handoff; actual archived /341 and /386 source files and seed packets. Peer related results checked: LSPV-3/539-549 lineage (particularly /542 and /555), /559-/565, LSPV-2/547-/552, LSPV-1/566-/568 (especially /568's 28/29 W baseline), LSPV-4/532 and /535-/538, LSPV-5 source-identity/byte audit, current GROKPROOF November 11 note and earlier Claude TPORT source. No complete original historical unified mixed-rule checker surfaced. No separate `/341` operation is inferred from `/386` acceptance.

Primary references: [1] Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, DOI 10.2307/2273702, on fixed checked proof languages and shared proof cost; [2] Cousot and Cousot, *Abstract interpretation: a unified lattice model*, POPL 1977, DOI 10.1145/512950.512973, on sound abstraction; [3] FRAT-XOR repository `meelgroup/frat-xor/format.md`, a distinct declared mixed CNF/XOR format elaborated into checked XLRUP. None defines the archived `/386` checker or the missing unified R_mix341 grammar.

## Dependency and resource firewall

**P2-D1 remains OPEN:** /386 source-completeness does not imply source *essentiality* or connectedness, and archived source binding is checker-generated `spec` rather than an external DIMACS hash. This run does not authenticate historical R_mix341 RES-to-AND3, LOCAL-CONVERT, actual DEF/facets with XOR, branch/discharge, exports/private ports, weakening, joins or deletion.

**P2-C3 remains OPEN:** abstractions must distinguish (a) actual mathematical-core acceptance from the additional CLI self-test predicate, (b) an unreferenced paid owner whose removal is a legal W=28 shortcut, and (c) the topology/connected-component count that the CLI silently assumes for E<=12. Any abstract lower bound must count distinct paid proof nodes, not total source records, and must grant free selection of the best *legal* DAG with shared ancestry. Unknown mixed-rule steps must remain conservative MAY at nonnegative cost lower bound 0.

**P2-B1 and separate P2-B2/B3 remain OPEN.** This very easy, disconnected family provides **no** general lower bound, no SAT-algorithm lower bound and no hard-family certification. Logical W=29 or W=28 is separate from original source bytes, serialized evidence bits, derivation span, peak live memory, checker time, and physical solver discovery work. A growing supplied packet costs growing bytes to verify despite constant logical W.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt or proof2.txt; no new load-bearing proof claim is closed. No modifications to historical fixed R_mix341 weights, current five agent identities/titles/schedules/timezones, their ownership boundaries, or existing TWO Route A / THREE Route B allocation. **P versus NP OPEN.**
