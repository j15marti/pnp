# LSPV-3/563: An accepted two-owner nested DEF-to-Resolution chain in the original archived /386 checker

**2026-11-10 23:24 PST | PNP Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

## Target, candidate and falsifiers specified before the experiment

**Target:** authenticate a concrete instance of paid-node global freshness, a fresh wire used as the signed input to another paid gate, zero-extra-charge owner-qualified facets, and strict signed RES ancestry, using the **unchanged original archived /386 checker**, not a proposed substitute parser. This advances one subdependency of [P2-D1], but the complete historical five-rule R_mix341 byte language remains OPEN.

**Candidate:** the original source-bound 69-record, 50-paid /386 guarded-K4 proof of LSPV-3/561 admits a source-identical, checker-accepted extension with a second paid gate `z9 = z8 AND (NOT x3)`, three additional owner-qualified free facets, and two intermediate RES nodes. The new chain must have both paid owners in the final contradiction ancestry while charging each owner only once.

Four precise falsifiers were fixed before testing: F1, nested gate input `8` violates the native declaration-order/freshness rule; F2, the signed facets or the RES pivots fail native canonicality, chronological parent typing or resolvent equality; F3, source substitution, underpayment, ancestor loss, or final-sink corruption passes the native checker; F4, the unchanged checker or its bundled self-test rejects the fully valid packet. All four were tested. The accepted packet defeats F1, F2 and F4. Thirteen hostile corruptions were rejected, addressing F3 within the tested mutation set.

## Historical authority and source corpus

The mathematical declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, Git blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, fixes unit-paid RES, AND3, GF(2) XOR, LOCAL-CONVERT and conservative DEF **semantics**, but does not supply one all-rule byte parser. The recovered /341 fixture checker `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, accepts SOURCE/AND3/XOR only. The separate, genuine archived /386 original `experiments/arc/lspv2_386_independent_verify.js`, blob `338305c0ce101704205e57543756b8127074a986`, accepts signed SOURCE, paid two-input AND gate owners, free defining DEF facet records and strict signed Resolution. **It is the only authoritative checker used in this experiment.**

The exact original checker-accepted seed is blob `d0fa96a155672f8f6a6a3428eacafa15e79b9e88` from LSPV-3/561, containing 17 original signed guarded K4 SOURCE records, 3 facet records, 49 paid RES nodes and one paid gate owner. LSPV-2/549 independently establishes that dual acceptance by the /341 and /386 checkers never authenticates one cross-language mixed proof; LSPV-3/562 establishes guarded-source restriction, **not** a native /341 converter. LSPV-4/535 documents the /386 CLI/core hostile-test distinction, under which a packet with a nonempty gate bank is necessary for CLI success. LSPV-1/565 documents a charge-label-dependent failure of its bundled even-charge control. LSPV-3/541 and /544 provide prior typed owner/facet and abstract-cost semantics, not accepted full-Rmix bytes. LSPV-5/482 provides a separate live-identifier namespace falsifier.

Required preflight: `proof1.txt` SHA `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` preflight SHA `b148b8e9270f5911c4f9daa5df1d8e182ea22a2a`; issue #3 and latest peer comments; `AGENTS.md` `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`; `CODEX.md` `754999f50de93cdb693ed37bc8110d31e9e698ef`; `.codex/skills/pnp-research/SKILL.md` `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`; current handoff LSPV-3/562; peer/source 539-549 and 550-562; actual /341 and /386 historical implementations; Grok `GROKPROOF/2026-11-11_0620_PROGRESS.md` and Claude world-ledger README. Search of required repository code and history did not reveal an authenticated one-checker five-rule Rmix341 dispatcher.

## Theorem 563.1: an exact accepted-byte nested-owner /386 witness

**PROVED/RESTRICTED for the archived /386 accepted language; COMPUTATIONAL checker replay.** Let `P_561` be the authentic 69-record guarded-K4 certificate, with the first paid gate `[0,8,1,2]`, i.e. `z8=x1 AND x2`. Construct `P_563` by preserving all 17 original signed SOURCE records exactly, adding a globally fresh paid gate declaration

```json
[1,9,8,-3]
```

and inserting three `DEF` facet views:

```json
{"kind":"DEF","c":[8,-9],"parents":[],"gate":1}
{"kind":"DEF","c":[-3,-9],"parents":[],"gate":1}
{"kind":"DEF","c":[3,-8,9],"parents":[],"gate":1}
```

All three clauses are the exact signed defining facets of `z9=z8 AND NOT(x3)`; no facet is charged as an independent paid inference. After the original paid RES node producing `D1=[-2,3,-7,-8]` (new index 23), insert the two paid strict RES steps

```json
{"kind":"RES","c":[-2,3,-7,-9],"parents":[20,23],"pivot":8}
{"kind":"RES","c":[-2,3,-7,-8],"parents":[22,24],"pivot":9}
```

The latter reproduces exactly D1, but as a newly paid inference record (new index 25). The original following RES record at new index 26 is redirected from its original D1 parent to the newly produced D3 (parents `[19,25]`, pivot 8). Every subsequent parent index is shifted by five as needed. All old derived clauses and the terminal empty clause are unchanged. The second gate's *output* is an intermediate variable used as an authentic strict RES pivot, not merely unused metadata. Both gate owners and four defining facet views are in the terminal proof ancestry. The old and new proof graphs share their previously derived nodes and original sources, rather than duplicating the full derivation.

The resulting **exact compact UTF-8/ASCII JSON certificate is 4,421 bytes**, Git blob **`08aa169b5db49b2ddd1cb5a9b6890fcc3b790916`**, and its original checker bookkeeping is

| property | seed /561 | nested /563 |
|---|---:|---:|
| Original signed SOURCE records | 17 | 17 |
| Distinct paid gate owners | 1 | 2 |
| Free owner-qualified facet views | 3 | 6 |
| Paid strict Resolution nodes | 49 | 51 |
| **Total paid logical work** | **50** | **53** |
| Chronological records | 69 | 74 |
| Compact JSON evidence bytes | 4,143 | 4,421 |
| Full original checker assertions | 4,492 | 4,663 |

The source is independently UNSAT: all (2^7=128) edge-and-guard assignments were evaluated and none satisfies its 17 source clauses. The full contradiction ancestry includes 72 of the 74 chronological records, all 17 original SOURCE, facet records 17, 19, 20 and 22, both paid owners 0 and 1 by transitive closure, and every inserted detour record. The parent-defined longest-path span is 11, not the physical wall time. No minimum-optimality result is claimed: the added gate/RES detour is intentionally redundant and illustrates exact legality and count-once ownership, **not a harder SAT instance or a lower bound**.

### Proof

The original /386 gate owner loop iterates definitions in order, checks globally distinct safe-integer owner/output identifiers and permits a new signed input literal when its absolute coordinate is an original edge variable or an output in the **previously entered definition bank**. Hence input `+8` for output `9` passes the original implementation's `gate used before declared` guard; the negative control reversing the two declarations fails. The three new facet clauses are precisely the normalized outputs of the original `views(9,8,-3)` function. The first new RES pivot 8 eliminates `8` from facet `[8,-9]` against `-8` in D1; the second eliminates 9 from `[3,-8,9]` against `-9` in the first resolvent, yielding D1 again. Both obey chronological parent indices and exact sign-canonical `key` ordering. Redirecting the next RES node from D1 to its newly reconstructed identical clause leaves all remaining strict RES verifications unchanged. There are precisely two new RES records and one additional paid gate owner, so the original summary guard forces total charge 53; three extra zero-extra-charge facets do not increment the charge. Reusing the resulting D3 and all other shared prior nodes adds no additional work. The original terminal empty clause and source list remain unchanged. This is a full, finite, exact original-checker accepted trace, not an abstract replacement grammar.

## Original-checker execution, controls and a parser distinction

Hosted V8 executed the **entire originally archived /386 verifier body**, including all eleven internal hostile mutation checks, without modifying mathematical check logic; only filesystem input, console output and output-only SHA digest were adapted. The accepted base packet passed 4,492 checker assertions. The 4,421-byte nested packet passed **4,663**. An otherwise equivalent packet consistently renaming output wire 9 to 10, re-sorting each signed clause in the native absolute-literal canonical order, and changing pivot 9 to pivot 10 was also accepted with **4,663** assertions. A trial which renamed only the clause literals but left the RES pivot 9 (and failed to restore canonical order) was rejected. Thus accepted-byte syntax includes the signed pivot field and canonical clause order, not merely semantic gate equivalence.

Thirteen deliberately corrupted packets all **REJECTED**: reversed owner order, wrong signed operand, duplicate gate output, duplicate owner ID, removed owner, bad facet, wrong intermediate resolvent, wrong pivot, forward parent reference, undercounted paid owners, undercounted total paid work, changed signed SOURCE, and forged nonempty sink. The raw result ledger preserves original-checker diagnostics. This is a deterministic finite test over a single historical source, not a proof that every possible corruption is rejected.

**Execution disclosure:** The unchanged original program was executed inside V8 with I/O adapters. A complete stand-alone native Node subprocess runner was written and syntax checked, but **not executed as an operating-system subprocess during this run**. The runner pins both original Git blobs and will require a full checkout for direct subprocess reproduction. The separate ancestor/source analysis is an **independent reimplementation of selected checks** and is not being labeled the authoritative checker.

## Restricted concrete configurations and cost-safe projection

For this archived /386 fragment, an authenticated concrete configuration may be represented as

[
 C=(B,H,F,Delta,G,V,D,A,P,I,sigma)
]

where (B) is the complete original UTF-8 JSON input, (H) its parser and decoded-ID state, (F) the authenticated ordered original signed guarded SOURCE rows, (Delta) the paid global gate bank with owner IDs and predecessor-input dependencies, (G) the global fresh output-wire set, (V) the ordered available signed clause views (including zero-extra-charge owner facets), (D) the complete chronological parent DAG, (A) active/discharged assumption contexts, (P) the distinct paid-identity set, (I) visible/private/exported interface metadata, and (sigma) the verifier phase. **For this /386 checker only**, contexts (A) are trivial and (I) has no native branch/export/private grammar. They are placeholders to prevent an unjustified full-mixed transfer.

For a typed /386 sublanguage, let (alpha) retain the source commitment, gate declarations and transitive owner closure, signed clauses and oriented pivots, all live DAG edges, and the distinct paid RES+DEF identities. Let (gamma) include every full chronological /386 configuration consistent with these records. Since the abstraction copies every checker-accepted SOURCE/DEF/RES transition, the typed inclusion property holds for the archived fragment; every source-preserving complete refutation remains represented; and

[
 W^{#}(alpha(P))=N_{mathrm{RES}}+|mathrm{paidOwners}|=W_{/386}(P)
]

when no pruning is performed. Optional cost-safe *backward slice of proof ancestry* can reduce or leave this value unchanged for the **mathematical core only**. It must retain definition ancestors transitively, including gate wire 8 consumed by gate 9. The /386 **standalone CLI** has a self-test requirement for a nonempty gate bank (LSPV-4/535); an all-owner-pruned normalized packet may therefore fail CLI even when its mathematical core accepts. The current /563 packet retains both active owners, so original core and wrapper agree.

This exact /386 fragment relation is **not** a rule-by-rule (alpha/gamma) for full R_mix341; no legal RES-to-AND3, LOCAL-CONVERT, GF(2), assumption branching, discharge, weakening, deletion or join has been authenticated by this one checker. For unknown historical full-grammar transitions, conservative MAY edges remain required, perhaps with zero abstract cost floor; do not infer a positive all-rule lower bound.

## CEGAR, literature, and barrier audits

A "cheap abstract refutation" using the *new second gate* cannot be discarded as spurious simply because the detour is redundant. It is accepted by the genuine /386 checker, so /386 abstraction must preserve the paid gate, its facets and signed pivot references. Exact source/DAG/owner reconstruction and original-checker replay reject the listed hostile packets; any future refinement that blocks a packet requires the proved concrete-step inclusion property, not only negative tests. Conversely the /386 checker is an incomplete sibling and cannot decide whether a formally similar transition is admissible in the missing full historical R_mix341 grammar.

Primary literature: Cook and Reckhow (1979), "The Relative Efficiency of Propositional Proof Systems," *Journal of Symbolic Logic* 44, 36–50, https://doi.org/10.2307/2273702, distinguishes fixed proof systems and polynomial proof verification from arbitrary algorithmic lower bounds. Cousot and Cousot (1977), "Abstract Interpretation," POPL, https://doi.org/10.1145/512950.512973, provides the general sound overapproximation discipline, not the exact historical byte grammar. FRAT-XOR/XLRUP (`https://github.com/meelgroup/frat-xor/blob/main/format.md`) and the archived Cake-LPR checker (`https://github.com/tanyongkiam/cake_lpr`) are distinct parser/checker systems and **cannot** be imported as Rmix341 syntax. Other required project-repository searches and Grok/Claude status reviews revealed no complete five-rule source parser. Same-machine resource and SAT-hardness transfers remain separate from the byte-authentication result.

Logical paid work is 53, evidence bytes 4421, abstract parent-DAG span 11, original V8 verifier assertion groups 4663. Host construction, search, failed proposed renaming, all source reads, checker invocation and output serialization cost physical operations; peak live writable memory and machine time were not measured. The nested owner bank alone is not an indication of a SAT decision lower bound. No uncharged discovery cost was added to the ideal minimum and no paid shared node is counted twice.

## Corpus reconciliation and proof-chain status

**CORPUS REVIEWED:** root proof1/proof2; issue #3; AGENTS.md; CODEX.md; pnp-research skill; historical /341 declaration; both exact archived checkers and /561 certified seed; LSPV-1/565; LSPV-2/539–550 with /549; LSPV-3/539–562 including /541,/544,/559,/561,/562; LSPV-4/535; LSPV-5/482; relevant Grok progress, Claude world ledger, primary Cook–Reckhow/Cousot work and FRAT-XOR/Cake-LPR repository examples. (Not every file in the full repository history was reread; discovery/search targeted materially relevant originals.)

**DUPLICATION / CONTRADICTION AUDIT:** LSPV-3/561 already authenticated one paid gate owner with facet-to-RES and /562 source restriction. LSPV-4/535 already proved that unused owners and repeated facets can be accepted. The additional new scope here is a **second live paid owner whose input is an earlier paid gate output**, with a signed intermediate RES-pivot chain used in the actual contradiction ancestry, together with 13 hostile negative packet tests and canonical renaming. Nothing here refutes /549 noncomposition, /535 CLI/core discrepancy, /541 signed facet distinction, or /562 guard theorem.

**WHAT CHANGED RELATIVE TO ROOT MAIN:** an additional original-archived-/386 accepted-byte reference for dependent gate owner order, two-owner global payment, owner/facet references and exact signed RES chronology. The existing root-main OPEN status and full /341 missing parser diagnosis do not change.

**ADOPTED / REJECTED / RETIRED PRIOR COMPONENTS:** adopt /561 original accepted packet and /535 cost/CLI firewall. Reject treating a native /386 trace as a full /341 mixed proof and reject imposing charges on the six free DEF facet views. No historical component retired.

**STALE OR OVERSTATED CLAIMS:** any statement that original /386 gate definitions must consume only original variables is false: signed input +8 from earlier paid output wire passes. No independently verified current tracker entry makes that restriction.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P2-D1], [P2-C3], [P2-B1], separate [P2-B2]/[P2-B3] and P1-01/P1-03/P1-04 remain **OPEN**; P versus NP is **OPEN**. The historical five-agent identities, Route A/B distribution (2 Route A, 3 Route B), schedules, source/pricing contracts and ownership boundaries are unchanged. The next decisive target remains one ORIGINAL full-Rmix341 checker admitting the same source-bound RES/AND3/LOCAL-CONVERT port in a single program.

## Exact published artifacts

- code: `experiments/arc/lspv3_563_nested_386_owner_chain.cjs`, blob `998be49893879c542754dbb0710ef7592e99340b`.
- checker-accepted certificate: `results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json`, blob `08aa169b5db49b2ddd1cb5a9b6890fcc3b790916`.
- raw original-body hosted V8 run: `results/raw/arc/2026-11-10_2324_LSPV3_563_NESTED_386_V8_RAW.json`, blob `7f6b0f429ef1dafe415a6c865529beeb43e60bf5`.
- five-role handoff: `research/coordination/2026-11-10_2324_LSPV3_NESTED_NATIVE_386_OWNER_CHAIN563_FIVE_ROLE_HANDOFF.md`.
