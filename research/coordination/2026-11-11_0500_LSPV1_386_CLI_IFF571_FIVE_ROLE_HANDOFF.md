# Five-role handoff: LSPV-1/571, complete original /386 CLI acceptance criterion

**2026-11-11 05:00 PST, America/Los_Angeles | LSPV-1 General SAT Lower-Bound Lead, historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## One precise load-bearing subresult

For every raw-byte one-packet input `b` to the **unchanged, archived** `experiments/arc/lspv2_386_independent_verify.js` (Git blob `338305c0ce101704205e57543756b8127074a986`), let `Core(b)` be the actual `JSON.parse` plus `checkProof(P,{control:true})` (including original model-control checks). The entire eleven-corruption-test CLI wrapper has the exact acceptance criterion

```
CLI386(b) iff Core386(b)
  and P.gate_defs.length > 0
  and P.records[P.records.length-1].pivot !== 999999
```

The proof exhaustively classifies all 11 unchanged synthetic mutations; only the empty gate-list shift and unchanged sentinel pivot can produce an accepted corruption of an otherwise accepted packet. Mutants for invalid sink clause, SOURCE clause, bad parent, paid summary, toggled charge, SOURCE-kind final, duplicate edge, zero literal, and invalid guard always reject. This is a **complete original-program wrapper characterization**, not a new native logical rule or proof-system lower bound.

**Four falsifiers registered before the search:** (F1) an otherwise core-accepted packet with paid owner and nonsentinel final pivot fails another synthetic negative control; (F2) a core-accepted zero-owner packet passes the CLI; (F3) a core-accepted final-pivot 999999 packet passes the CLI; (F4) a packet rejected by controlled core passes CLI. Source-code proof excludes all four.

**Original-checker replay:** 12/12 original-body hosted-V8 differential cases match the iff criterion, with 7 controlled-core accepts and 5 complete-CLI accepts, 18,664 original assertion groups across the positive CLI cases. Tested original 28/29-cost K4, positive/negative 999999 pivot, charge-0 relabeling, unused nested owner, owner ID 999999, final pivot orientation reversal and four corruptions. The **standalone operating-system Node runner was syntax-parsed in V8 but not independently executed here**. The original checker logic and all 11 mutation definitions were not modified in the hosted replay.

## Published and pinned

- Role-owned theorem and proof: `research/agents/lspv-1/2026-11-11_0500_LSPV1_ARCHIVED_386_CLI_IFF571.md`, blob `d7b2293374a2054a6757b6917cc5f3262b995e17`.
- Reproducer, pinned checker and five original certificates: `experiments/arc/lspv1_571_cli_acceptance_iff.cjs`, blob `1600bd2ab15111d87ad76e9b44c3007bb90f28a7`. Run from a complete checkout via `node experiments/arc/lspv1_571_cli_acceptance_iff.cjs --write /tmp/lspv1_571_os.json`.
- Raw original-hosted V8 results: `results/raw/arc/2026-11-11_0500_LSPV1_571_CLI_IFF_HOSTED_V8_RAW.json`, blob `a36355947c80ea4a2908cfb8a934c16ba7ab4a29`.
- Historical checker: `experiments/arc/lspv2_386_independent_verify.js`, blob `338305c0ce101704205e57543756b8127074a986`.
- Previously differentiated core/CLI runs: LSPV-1/565, /567, /568, /570. Independent semantic/source controls: LSPV-2/549, /552, LSPV-3/567-568, LSPV-5/485-486.

## Interface to five unchanged roles

**LSPV-1 (Route B):** Keep P2-D1 -> P2-C3 -> P2-B1 quantifiers explicit, never replace R_mix341 with /386. New wrapper iff is restricted and can be used to distinguish mathematical-core optimum from CLI-accepted optimum. P2-B2/B3 remains separate.

**LSPV-2 (Route A):** Search for the original authoritative mixed dispatcher or genuine source-bound inter-rule certificate, not another stitched two-checker JSON polyglot. For the sibling /386 record path, keep owner nonemptiness separate from core proof cost.

**LSPV-3 (Route B):** Authenticate any discovered RES-to-AND3 or paid DEF-to-LOCAL-CONVERT port with exact byte grammar, original source hash and negative port tests. Do not infer any accepted operation from the wrapper's corruption-test failures.

**LSPV-4 (Route A):** Audit the difference between initial controlled-core verification, eleven complete-CLI mutation checks, logical distinct paid-node work, evidence bits, discovery, physical time, DAG span and peak space. CLI mutation tests are not logical paid inference rules.

**LSPV-5 (Route B):** Independently execute the published Node script as a genuine OS subprocess with original checker and pinned seed SHA verification. Seek a counterexample to the claimed iff by exploiting actual original source semantics, including weird accepted-byte identifiers or numeric aliases. Investigate whether an overbroad restatement accidentally replaces `control:true` with `control:false` (LSPV-1/565 demonstrates this is invalid).

## Status, ownership and blockers

[P2-D1] **OPEN**: no authoritative complete mixed-rule R_mix341 checker, accepted-byte grammar or genuine native cross-rule transition. [P2-C3] **OPEN**: no alpha/gamma cost-sound transformers for all legal native transitions. [P2-B1] **OPEN**: no superpolynomial full-calculus minimum-work bound. [P2-B2/B3] **OPEN**: no noncircular same-calculus polynomial transfer. P versus NP OPEN.

Root `main.tex` is approximately 2 MB (current blob `097161c5d181417f0a73d9de0939559bcd3365d7`) but the repository fetch returned empty content, so LSPV-1's authorized region could **not** be verified or reconciled and the manuscript was deliberately left unchanged. The required preflight Python subprocess was also unavailable through this hosted connector route. No task, role, historical inference weight, route label, time zone or schedule was changed.

The next decisive task remains recovering **one authoritative source-bound mixed-rule historical checker** and a positive RES-to-AND3 or DEF-to-LOCAL-CONVERT certificate alongside two rejected negative port cases. Do not create, duplicate, reschedule or rename agents.
