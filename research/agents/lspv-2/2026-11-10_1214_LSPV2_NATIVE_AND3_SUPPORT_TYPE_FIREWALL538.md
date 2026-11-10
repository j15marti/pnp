# LSPV-2/538: Native /341 accepted AND3 support-string semantic counterexample

**November 10, 2026, 12:14 PST | LSPV-2 SAT-Circuit Reduction Builder, historical Route A | PROVED/RESTRICTED checker-specific + COMPUTATIONAL | P versus NP OPEN**

## IDEA, exact candidate, four falsifiers

Candidate: The *original recovered* /341 SOURCE/AND3/XOR verifier accepts a semantically invalid original-variable AND3 transition on genuine signed 3-CNF, because it permits a string rather than a vector of integer support coordinates. Falsifiers: (F1) original checker enforces integer-array type; (F2) JavaScript substring membership excludes the missing variable; (F3) affine-row equality tests recover the missing variable; (F4) changed truth table still represents the parent conjunction. All four falsified by original code inspection, unchanged-code V8 replay and explicit countermodel.

## Original source, immutable code, exact bytes

Original producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, Git blob 4081022e8a3841d79f751a3d3a7a10decbb026da. Original checker: experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. This original checker handles a special *fixture grammar*, not the complete historical R_mix341 rule system.

Use its original odd-charge Petersen cubic-graph 3-CNF, containing 15 original edge variables, 40 proper signed original clauses, 39 paid AND3/XOR nodes and 10 vertices. The source is genuinely UNSAT. The original node d2 has parents d1 and s3, integer support [0,2,12], AND3 truth table 150 and affine annotation mask 0x1005, rhs 1. Preserve *all* graph data, signed source clauses, charges, source IDs, other proof nodes, parents, row and sink. Change only d2.support to the JSON string "012" and d2.table to integer 90. The complete accepted JSON packet occupies 8,785 UTF-8 bytes and is included in the raw results.

Original verifier condition is sup.every(x => p.support.includes(x)); when p.support is string "012", .includes(12) succeeds because 12 is a substring. For truth-table evaluation, p.support[j] instead enumerates the three characters 0,1,2, so variable12 stays zero. The attached affine row also passes because the checker tests only these misenumerated assignments, and downstream XOR trusts unchanged affine metadata.

The actual signed source parent conjunction is

$$
x_0\oplus x_2\oplus x_{12}=1,
$$

whereas the falsely accepted derived factor computes

$$
x_0\oplus x_2=1.
$$

For $(x_0,x_1,x_2,x_{12})=(0,0,0,1)$ both parents are true while claimed derived output is false. Of the 16 original-variable assignments to those four coordinates, eight disagree.

**Theorem 538.1 (PROVED/RESTRICTED).** The recovered exact /341 test-fixture verifier accepts a proof packet containing an original-variable semantically invalid AND3 transition. This follows from the actual immutable checker code's two uses of the wrongly typed support field and the explicit accepted-byte V8 replay plus the original-variable countermodel. This is *not* a proof that a satisfiable source is refuted, *not* an attack on a correctly typed separate reference checker, and *not* authentication of the missing full historical R_mix341 grammar.

## Verification and hostile controls

Original unchanged JavaScript checker executed directly inside V8, with only Node CLI file-read/console wrappers replaced. Baseline Petersen packet: **ACCEPT, 4,347 historical verifier checks**. Forged string-support Petersen packet: **ACCEPT, 4,347 checks**, unchanged source and 39 paid identities. Full seven-fixture historical packet regression: **ACCEPT, 30,714 checks**.

Nine precisely specified probes: two accepted and seven rejected as expected. Rejection controls: unchanged table with string support, forged table with integer support, incorrect substring, wrong affine mask, dangling parent, source polarity corruption, and corrupted sink. An independent Python original-variable semantic evaluator reproduced 16 assignments, eight discrepancies, including the displayed concrete countermodel. A separately labelled strict typed reference filter rejects non-array support. The published Node harness pins original Git blob hashes but was not executed as a Node CLI in this run; the unchanged-source audit function *was* executed in V8. No complete R_mix341 checker or native FLMV machine was executed.

Executable and raw artifacts: experiments/arc/lspv2_538_support_string_native.cjs; experiments/arc/lspv2_538_support_semantic_independent.py; results/raw/arc/2026-11-10_1214_LSPV2_538_NATIVE_AND3_SUPPORT_RAW.json. Raw JSON contains the *entire* 8,785-byte accepted forged packet.

## P2-C3: cost-sound abstraction, alpha/gamma and CEGAR

A concrete state of the recovered accepted-byte checker includes original source bytes and binding, graph, signed original factors, parsed field *types*, typed or untyped actual variable semantics, complete shared DAG with source and paid IDs, and full acceptance/checking history. Define alpha into a MAY domain recording exact signed source provenance, paid IDs, dependencies and checked annotations, but mapping an untyped semantic factor to TOP. Gamma contains every raw packet/transition consistent with that record, including this checker-accepted invalid typed transition. This preserves the needed Post(gamma(a)) subset gamma(Post#(a)) over the recovered checker behavior, and mapping its paid event at unchanged non-increased charge preserves negative-proof resource polarity. A strict typed AND3-only abstraction that discards this accepted path is *unsound relative to the recovered accepted-byte language*.

The forged packet is **genuine accepted behavior** of this checker, not a spurious path for checker-relative CEGAR. It is spurious relative to intended typed Boolean AND3 semantics; defining that intended full historical relation and proving a new checker faithfully implements it is still OPEN. Unknown RES, LOCAL-CONVERT, paid DEF, defining facets, exported/private wires, contexts, branching, weakening, discharge, joins and deletions must be authenticated or conservatively overapproximated. Never turn absence in this fixture checker into absence from the full declared calculus.

The 39 paid nodes are a logical work count, while certificate bytes (8,785), input parsing, checker assertion groups (4,347), critical path, machine time and peak space are separate resources. Do not infer operational work or memory from proof size. Branch AND obligations, proper assumption discharge, all legal shared DAG reuse and globally fresh paid IDs remain required in the eventual full abstraction.

## CORPUS REVIEWED and duplication/contradiction audit

Read the two entire root trackers, issue #3/recent comments, AGENTS.md, CODEX.md, project pnp-research skill, new native-focus instruction and relevant 2026-11-09 handoffs. Read original /341 producer and checker, LSPV-2/537; LSPV-1/553; LSPV-3/549 and /550, LSPV-3/502; LSPV-5/414; LSPV-4/523; Grok 2026-11-10 progress; original MODELBRIDGE-0010. Change-aware external source checks: konard/p-vs-np scripts/proof_status.json blob 93b77ed3, blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea, meelgroup/frat-xor format.md blob 986a21aa, tanyongkiam/cake_lpr README.md blob e94f45e9, openai/math README.md blob cc5b0a03. They do not authenticate full historical R_mix341 bytes.

This newly discovered **derived AND3 support** type flaw is distinct from LSPV-3/550's *source literal* coercion, LSPV-5/414 and LSPV-3/502's phantom affine masks, LSPV-1/553's rejected legal paid padding, and LSPV-2/537's earlier metadata and opcode corpus. No historic inference weight changed. Primary intellectual controls: Cook-Reckhow (1979, DOI 10.2307/2273702), Cousot-Cousot (1977, POPL, DOI 10.1145/512950.512973), D'Silva-Haller-Kroening ACDCL (POPL 2013), and external FRAT-XOR's *different* authenticated byte grammar. No foreign format transfers into /341 automatically.

## WHAT CHANGED RELATIVE TO ROOT MAIN; adopted/rejected/retired

Adopted immutable original-source PETERSEN provenance, exact original checker execution, genuine GF(2) shortcut controls and count-once shared nodes. Rejected the inference that an accepted untyped *checker* AND3 certificate is automatically a sound typed Boolean AND3 transition. Rejected any replacement of the original absent all-rule grammar by CANON1/2/2R or by the stricter reference filter. No historical theorem or rule retired. Root main.tex should incorporate this restricted counterexample only inside LSPV-2's own region.

**Material evidence [P2-L2-538] supports OPEN [P2-D1] and OPEN [P2-C3]. [P2-B1], [P2-B2]/B3 remain OPEN. [P1-01], [P1-03], [P1-04] remain OPEN.** Next target: an authentic externally source-bound accepted RES-to-AND3, LOCAL-CONVERT, paid DEF facets and discharged branch packet, plus a full typed cost-sound replayer. Existing five roles, titles, schedules, enabled states and 2A/3B assignment unchanged. P versus NP OPEN.
