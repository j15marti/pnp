# LSPV-3/592: SAT/UNSAT-inconsistent Cartesian product of two original checkers

**2026-11-12 09:24 PST | Hypergraph & Proof Certificates | Historical Route B | PROVED/RESTRICTED source-inspection theorem + COMPUTATIONAL original-body replay. P versus NP OPEN.**

**Affected IDs:** P2-D1, P2-C3 restricted boundary; P2-B1 OPEN; P2-B2 and P2-B3 separately OPEN. This is NOT an original complete R_mix341 checker.

## Candidate and advance falsifiers

Candidate D1-592: the unchanged archived /341 and /386 verifier programs each accept one common JSON file, although the /341 source has a satisfying assignment and the /386 original signed source is UNSAT. They do not inspect one another's provenance or cross-rule parent typing.

F1: either unchanged checker rejects the common JSON. F2: /341 source not SAT or /386 guarded source has a satisfying assignment. F3: corrupting a source or parent on one side causes the other checker to reject, defeating the asserted independence. F4: either executable validates a common source or a mixed RES/AND3/GF(2) inference link. Exact source inspection and original-code differential replay exclude all four falsifiers for these archived implementations.

## Precise sources, duplication audit and preflight

Original /341 SOURCE/AND3/XOR verifier: experiments/arc/lspv2_341_independent_verify.js, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**.

Original /386 SOURCE/DEF/RES verifier: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**.

Original /341 SAT-source previously native-accepted input: results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json, blob **6cf9b0fe1e5a9419e8967d836c707c385418b810**.

Original /386 W29 accepted guarded-K4 input: results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json, blob **4177ec15a0c7253378d5652a6b13b7152601d300**.

**Prior art:** LSPV-2/549 already exhibited a two-original-checker polyglot on distinct original UNSAT sources. LSPV-1/553 and /594 and LSPV-2/537 established that these verifiers have restricted dispatch and /341 rejects locally legal redundant paid-node padding. LSPV-3/582 already established the SAT-source /341 acceptance due to charge type and affine-annotation defects. **Incremental new result:** a quantified Cartesian-product acceptance theorem plus an accepted pair of mutually inconsistent SAT-versus-UNSAT source truth labels. It is not a new independent /341 soundness failure.

Read both root trackers in full: proof1.txt blob **06f7ebc8c2283304a0f5200b518c6e48fa41e343**, proof2.txt blob **ba4d1c0faf9acbce836ffc5e16740b197e4c7bbe**; issue #3 and latest comments; AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; LSPV-3/539-549 and /582, /587, /591; LSPV-2/537, /549 and /577; LSPV-1/553 and /594; LSPV-4/564 and LSPV-5/506 issue material; Grok 2026-11-12_0821_PROGRESS; and Claude ONETAPE-0001. Original scripts and actual certificate files were opened and inspected. Full repository preflight/CI could not be executed with the available hosted repository connection.

## Theorem 592.1: precise archive-specific Cartesian-product closure

Let A be any JSON accepted by the original /341 checker, and B any JSON accepted by the original /386 checker where the /386 summary is an ordinary object and has no meaningful length field. Form a JSON object J with fields:

    fixtures = A.fixtures
    spec = B.spec
    gate_defs = B.gate_defs
    records = B.records
    summary = object_copy(B.summary) plus length = A.fixtures.length

Then **C341(J) = ACCEPT and C386(J) = ACCEPT**, independently of whether the two original sources are the same or have equal SAT labels.

**Proof:** The unchanged /341 executable evaluates its original fixture graph, charge array, signed clauses, paid AND3/XOR nodes, deletion witnesses and summary.length. It never reads the top-level spec, gate_defs, records or /386 summary counters. The unchanged /386 executable evaluates its own spec, gate_defs, records and numeric summary counters. It never reads fixtures or summary.length. Therefore J preserves every field inspected by each validator, so each returns the same acceptance as its original input. Neither contains a cross-component original-source identity assertion or a shared mixed-rule parent lookup. QED. This proves *separate-program product closure only*, NOT a combined historical R_mix341 proof language.

## Exact accepted-byte witness, source truth and differential replay

Published dual-accepted native JSON: **results/raw/arc/2026-11-12_0924_LSPV3_592_DUAL_SAT_UNSAT_ACCEPTED_PACKET.json**, Git blob **d104f7cfc8a10709919d65289bb0a31c0cc1c4ff**, exactly **11,487 characters**.

The /341 component contains **48 signed clauses on 18 original variables** and **47 charged AND3/GF(2) proof nodes**. Assignment **101001000000100000** satisfies all **48 of 48** signed source clauses by direct literal evaluation. The previously reported affine alias/charge-type defects remain in this packet.

The /386 component contains **17 original guarded SOURCE records**, with **six edge variables and guard 7**. All **64** edge assignments with guard fixed to 1 fail the original CNF; its source is UNSAT. It has 46 proof records, **28 paid Resolution inferences**, one once-paid conservative definition owner, and **W=29**.

The full common JSON file was accepted by both **unchanged original checker bodies executed in hosted V8 with I/O adapters**, obtaining **3,273** original /341 assertion groups and **3,125** original /386 assertion groups, including the respective bundled five and eleven hostile controls.

| Case | Original /341 | Original /386 |
|---|---|---|
| Unmodified SAT/UNSAT dual packet | ACCEPT | ACCEPT |
| Forge /341 SOURCE literal | REJECT | ACCEPT |
| Forge /386 SOURCE record | ACCEPT | REJECT |
| Break /341 parent identity | REJECT | ACCEPT |
| Break /386 chronological parent | ACCEPT | REJECT |
| Forge /341 terminal GF(2) sink | REJECT | ACCEPT |
| Forge /386 RES pivot | ACCEPT | REJECT |

Across the seven independent paired cases, **8 of 14 original-checker executions accepted**, six rejected, and **25,592 positive original assertion groups** passed. Every case roundtripped through JSON serialization. The unchanged executable inference functions were invoked with only Node file/argument/stdout and /386 report-hash adapters, not reimplemented. **The separate published OS Node replayer was written and read back but was NOT executed as an OS subprocess in this run.** The /386 printed SHA-256 field was deliberately marked uncomputed in the hosted replay. This does not affect any checker assertion.

Raw hosted ledger: results/raw/arc/2026-11-12_0924_LSPV3_592_DUAL_CHECKER_HOSTED_RAW.json, Git blob **719de5ea222b864ba010ae24bf6bfc7999c86445**. Complete Node original-checker OS reproducer: experiments/arc/lspv3_592_dual_checker_cartesian_product.cjs, blob **abeb6e4113a1cc8e1132afa6de425eb7c25b589a**. Full GitHub content readback was exact.

## P2-D1 -> P2-C3 consequence and proof limits

A joint ACCEPT/ACCEPT verdict from the two archived checkers **does not establish original-source-bound mixed legality**. The exhibit has incompatible source SAT labels and completely separate proof languages. A legitimate full-native R_mix341 checker must enforce one externally authentic original CNF, actual typed cross-rule parent references, global proof-DAG ancestry and once-paid identities, fresh wires, owner-qualified facets, private/exported capabilities and assumption scope/discharge, using its authentic historical fixed charges.

An acceptance-sound MAY abstraction of *the two archived programs' intersection* must retain the above polyglot, because it is genuinely accepted by both. A source-sound abstraction of the intended **full historical calculus** would instead need an authenticated single-source semantics; imposing that semantic condition is not a sound reconstruction of the unknown archived parser. Spurious CEGAR paths may be pruned only after explicit source-bound proof obligations, and the existing SAT-source /341 checker bug must remain visible.

**Do not add 47+29 to claim W76 for one proof.** They are two independently paid ledgers without shared source, owner or parent identifiers. Evidence bits, hosted assertion counts, actual machine time, span and peak space are distinct measurements. No general SAT or proof-system lower bound follows.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root tracker node is newly closed or downgraded beyond earlier /549 and /582 warnings. All five agent identities, titles, schedules, timezone, historical weights, ownership boundaries and the existing two Route A / three Route B allocation are preserved; no automation was created or modified.

**OPEN:** P2-D1, P2-C3, P2-B1, separate P2-B2/P2-B3 and P versus NP.

**Next load-bearing falsifier:** find a single externally source-bound historical R_mix341 verifier and original accepted packet with a true RES-to-AND3 or DEF-facet-to-LOCAL-CONVERT parent edge; verify exact accepted bytes, source hash, fixed weight, fresh/private/exported wires and hostile cross-source/parent/context variants. If original behavior cannot be located, preserve all unknown rules as MAY, not as forbidden rules.

## Sources

Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702: https://doi.org/10.2307/2273702 .

Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973: https://doi.org/10.1145/512950.512973 .

Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV (2000), DOI 10.1007/10722167_15: https://doi.org/10.1007/10722167_15 .

External example, not historical R_mix341: FRAT-XOR/XLRUP accepted proof format, https://github.com/meelgroup/frat-xor/blob/main/format.md .
