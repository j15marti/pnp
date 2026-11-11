# LSPV-1/566: archived /386 topological proof-record normal form

**2026-11-11 00:00 PST | LSPV-1 General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and four falsifiers (specified before the experiment)

**Candidate:** Under the unchanged archived /386 checker, every legal reordering of a completed source-bound proof that preserves all parent-before-child edges and keeps the terminal contradiction last is accepted at identical logical cost, including orderings with paid RES inferences before some original SOURCE records and free DEF facets before all SOURCE records.

F1: a SOURCE or DEF view requires earlier record parents. F2: owner freshness or clause validation depends on proof-record order rather than the global gate_defs list or source spec. F3: first-payment or source completeness is sensitive to reordering. F4: the original checker rejects a correctly reindexed topological witness or accepts a malformed forward-parent/owner/facet/source/payment control.

These four falsifiers are resolved for the original archived checker function, NOT the unavailable historical five-rule R_mix341 dispatcher.

## Source/corpus recovery

Read both complete current root trackers, proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt SHA 8927e4ba0c54ba701ceac55e918203fcdf675e1a; issue #3 through LSPV-4/536; AGENTS.md, CODEX.md, and the repository pnp-research SKILL.md. Inspected the authentic checker experiments/arc/lspv2_386_independent_verify.js at blob 338305c0ce101704205e57543756b8127074a986, the 4,421-byte signed nested-owner packet results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json at blob 08aa169b5db49b2ddd1cb5a9b6890fcc3b790916, reports LSPV-1/565, LSPV-2/550, LSPV-3/563, LSPV-4/536, LSPV-5/482 and their recent five-role handoffs, and relevant earlier LSPV-1/539, /543 and /539-549 dependency entries. Root main.tex was recovered from Git blob fab2c0240916f14d4784463d49764ddd958fdff8 after the contents API returned an empty body.

Original LSPV-2/341 declaration supplies semantic rules but NOT a complete authoritative five-rule accepted-byte checker. The archived /341 checker blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0 dispatches SOURCE/AND3/XOR only; the separately archived /386 checker handles SOURCE/paid DEF-owner/free facet/strict RES. Dual acceptance of these checkers does not authenticate cross-rule transitions.

Primary literature: Cook and Reckhow, *Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36-50, DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973; Clarke et al., *Counterexample-Guided Abstraction Refinement*, JACM (2003), DOI 10.1145/876638.876643. These sources guide proof-system and abstraction discipline; the exact theorem below follows from the pinned original checker, not the literature.

## Theorem 566.1: arbitrary topological reordering (PROVED/RESTRICTED)

Let P be a packet accepted by the original /386 function checkProof(P,{control:true}). Its records are r_0,...,r_(L-1), with the final record the empty contradiction. Let sigma be a bijection on the L indices that leaves the original terminal record last, and makes every parent of a record precede that record. Apply sigma to the record order, replace all parent indices with their images, and keep all record contents, source names, paid owner names, signed pivots, graph/spec, ordered gate_defs and summary unchanged. Call the result P^sigma.

Then

$$
\operatorname{Accept}_{386}(P)\Longrightarrow
\operatorname{Accept}_{386}(P^\sigma),
\qquad
W(P^\sigma)=W(P)=N_{\rm RES}+N_{\rm gate\_defs}.
$$

The complete shared proof DAG and terminal ancestry are carried bijectively by sigma, and every owner is counted once. This holds for every /386-accepted packet, including legal nested gate definitions. It is NOT a theorem about full R_mix341.

**Proof:** The original checker preprocesses all gate_defs and their facet clauses into maps before processing any record. SOURCE and DEF records must have empty parent lists and are independently validated against the immutable original graph/spec or globally predeclared owner; their duplicate/completeness bookkeeping is set-based. A RES record uses only its two earlier parents, exact signed pivot and canonical resolvent. Under any dependency-respecting permutation, both parents still precede the child, the parent clauses stay identical, and induction proves that every corresponding derived clause is unchanged. The terminal record remains the empty clause at the end; summary counts and fixed cost N_RES+number of unique gate_defs are invariant. The E<=12 graph model-count control depends only on the unchanged graph/charges. Therefore every check remains true. QED.

**Normal form:** N(P) is the stable partition SOURCE, DEF, RES, with parent indices renamed by the bijection. Since SOURCE/DEF have no record parents and the RES relative order is preserved, N(P) is legal whenever P is accepted, W is identical, and N(N(P))=N(P). This gives a completed-trace exact quotient for this /386 checker but **not** an online or all-native-rule alpha/gamma, physical time/space bound, or byte-length equivalence.

## Independent original-body replay

Tested the unchanged original /386 checkProof with graph control enabled against the previously published source-bound nested signed guarded K4 packet. Its 74 records contain 17 original SOURCE clauses, six zero-additional-price DEF facets, two distinct paid gate owners [0,8,1,2] and [1,9,8,-3], and 51 paid strict RES nodes. The checker returns paid=53, def=2, res=51, sources=17, records=74, oddModels=0, evenModels=8 and guardFalseModels=64.

All **128/128** seeded random parent-respecting topological permutations were accepted by the original checkProof at W=53; 128 changed order, 125 placed a RES before the last SOURCE, and 35 began with a DEF facet. Both SOURCE-first and DEF-first normal-form controls were accepted. Six hostile mutations REJECTED: forward parent, bad facet, missing paid owner, underpayment, forged source, inconsistent charge. **103,895** original-checker assertion groups passed across the accepted checks and rejection controls. Evidence was executed in hosted V8 with only input module/CLI iteration adapted. The standalone Node reproducer passed V8 syntax parsing; operating-system Node execution and the original CLI's separate eleven synthetic mutation tests were not performed in this run.

Code: experiments/arc/lspv1_566_record_topology_replay.cjs.
Raw: results/raw/arc/2026-11-11_0000_LSPV1_566_TOPOLOGICAL_RECORD_NORMAL_FORM_V8_RAW.json.

## Cost-sound abstraction interface and open dependency ledger

For completed accepted /386 traces only, alpha(P)=N(P), with gamma(Q) all accepted topological record permutations with identical original source identity, facets, owner payments and shared inference DAG. P belongs to gamma(alpha(P)), terminal contradiction is preserved, and W is exact. This is **not** the required P2-C3 concrete-step inclusion over all historical native operations. In particular one may not silently preload future SOURCE knowledge into an online parser, assume unknown branching/discharge rules commute, or replace the historical calculus with this sibling.

P2-D1 OPEN: one fixed sibling's record-order property is authenticated; single-checker mixed RES/AND3/GF(2)/LOCAL-CONVERT, private/exported wires and branching/discharge still unavailable.
P2-C3 OPEN: no full alpha/gamma, per-operation cost-soundness or complete CEGAR witness.
P2-B1 OPEN: no superpolynomial lower bound over optimal shared mixed proof DAGs.
P2-B2/B3 OPEN: no noncircular uniform SAT-decider-to-same-calculus polynomial-proof transfer.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This scoped sibling result does not close a load-bearing chain node. No root proof tracker updates justified. Distinct paid logical work, certificate evidence bits, discovery cost, physical time, span and peak writable space remain different resources.

**Next target:** obtain an authoritative historical single-checker accepted-byte RES-to-AND3 or DEF-to-LOCAL-CONVERT certificate and let LSPV-5 independently replay it. LSPV-2/4 audit per-operation cost and memory; LSPV-3 owns exact native grammar. All five current role identities/titles/schedules/Pacific timezones, historical tariffs, ownership boundaries and TWO Route A / THREE Route B labels preserved; no automations changed. P versus NP remains OPEN.
