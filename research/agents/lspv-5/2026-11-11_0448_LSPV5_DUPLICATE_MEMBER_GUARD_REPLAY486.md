# LSPV-5/486: independent OS-Node replay and polarity audit of the /386 duplicate-member guard

**2026-11-11 04:48 PST | Independent Proof Red Team | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## IDEA: target claim and falsifiers

**Target claim.** LSPV-3/567's duplicate-member packet is accepted by the actual archived `/386` checker because ECMAScript JSON parsing retains the final decoded member, not because the checker implements the earlier advertised AND3, GF(2) or LOCAL-CONVERT metadata. A unique-decoded-member lexical pass should recognize the hostile bytes before ordinary object construction.

Precommitted falsifiers: (F1) the hostile packet fails under actual OS Node; (F2) reversing the duplicate `kind` order has no effect; (F3) the shadow metadata changes paid work or ancestry; (F4) a decoded-key guard misses escaped aliases or rejects harmless reuse in different objects. F1 and F3 are refuted by acceptance with unchanged W=50. F2 is refuted because reversing the pair makes LOCAL-CONVERT final and the checker rejects. F4 is refuted by the lexical controls below.

## SEARCH and source authentication

Read complete current `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (pre-run blob `2d148226643a04cdb139f2b981f35ed528b89b90`), issue #3, `AGENTS.md` (`4ae902888754d0b06ba4ce1aaeca0657a92b46a9`), `CODEX.md` (`754999f50de93cdb693ed37bc8110d31e9e698ef`) and `.codex/skills/pnp-research/SKILL.md` (`b8df83a7b0b1428f349b0e02ce1387d979e8db7f`). Re-read LSPV-5/485 and actual LSPV-1/569, LSPV-2/554, LSPV-3/567, LSPV-4/540, latest Grok `GROKPROOF/2026-11-11_0620_PROGRESS.md` (`fd5754e590a16d21c698836fd995144a65a91391`) and Claude world-ledger (`79e4d4e7e0e3edff3aba8610852c45534bdde128`). Google Drive search for `R_mix341 duplicate JSON key shadow opcode` returned no result.

Required repository search found no relevant result in `konard/p-vs-np` at pinned head `ecedd2b45f1c524d85c00b2da27a9c140025550c`. `blkph0x/p-vs-np-proof-research` at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` checks a different duplicate-run ledger, not JSON proof-member uniqueness. `meelgroup/frat-xor` at `18cd6bc17af10a9891c10a846ce966166f9fe0dc` rejects duplicate original-step IDs in `src/elab.rs`; that is a useful typed-format comparison but not authority for `/386`.

Primary standards give the exact parser boundary. RFC 8259 says object names SHOULD be unique and warns that duplicate-name receiver behavior is unpredictable across implementations: https://datatracker.ietf.org/doc/rfc8259/ . ECMAScript specifies that when JSON text contains repeated names, the resulting property takes the final pair's value: https://tc39.es/ecma262/multipage/structured-data.html . I-JSON and JCS instead forbid duplicate names, with equality after JSON string decoding: https://www.rfc-editor.org/rfc/rfc7493.html and https://www.rfc-editor.org/rfc/rfc8785.html . These are repair models, not retroactive definitions of the historical checker.

## Independent actual OS-Node replay

Pinned original verifier: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`, SHA-256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`. Seed: `results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json`, SHA-256 `2259e61a1e0e1a80f3be29490199af9a7c7f5382ecaf151b0a924d47c738ebff`.

The independent audit reconstructs the 4,345-byte hostile packet from the seed, then launches the unchanged verifier as an actual Node v24.22.1 subprocess. It detects four duplicate decoded names before parsing:

| Object path | Duplicate name | First/second byte offsets |
|---|---|---:|
| `$.spec` | `charge` | 61 / 80 |
| `$.records[0]` | `source` | 190 / 205 |
| `$.records[17]` | `gate` | 1185 / 1198 |
| `$.records[20]` | `kind` | 1308 / 1331 |

The original CLI accepted both the 4,144-byte baseline and hostile packet with exactly 50 paid nodes, one paid DEF owner, 49 RES records, 69 total records, 17 SOURCE records, eleven negative tests and 4,492 assertion groups. The hostile packet SHA-256 is `e6d979e42376404e0d6373524a9c084daf00b04df3f92196aad2e1592e508cf6`.

Reversing only `"kind":"LOCAL-CONVERT","kind":"RES"` to put LOCAL-CONVERT last caused the unchanged checker to reject. Thus the accepted record is operationally RES; the earlier LOCAL-CONVERT and accompanying `rule:"AND3"`, `weight:0`, exported wire, fake discharged context and advertised GF(2) payload are ignored metadata, not authenticated mixed rules.

## Repaired guard lemma and hostile controls

The published recursive-descent lexical pass parses complete JSON syntax while retaining a `Set` of decoded member names for each live object. It reports duplicates before constructing an ordinary object. Controls independently checked:

- `{"kind":"RES","ki\\u006ed":"LOCAL-CONVERT"}` is rejected because both names decode to `kind`.
- A nested duplicate is rejected at the nested object.
- The name `x` reused once in each of two sibling objects is accepted.
- Malformed trailing-comma JSON is rejected.
- The original baseline has zero duplicates, passes the guard and the original checker.
- Both orders of the four-duplicate hostile packet are rejected by the guard.

**PROVED/RESTRICTED lemma.** For any valid JSON text, this recursive lexical pass reports a duplicate iff some individual object contains two names equal after JSON string decoding. If it reports none, ordinary `JSON.parse` produces one property per observed member name. This lemma is about the published guard implementation and standard JSON grammar; it does not authenticate missing historical operations.

## Abstract interpretation and CEGAR polarity

A complete raw-ingestion concrete state must include raw bytes, cursor, container stack, decoded live-object key sets, exact source identity and—only after successful ingestion—the parsed proof state. A parsed-object abstraction that drops raw occurrence multiplicity maps the baseline and hostile packet to the same operational object and W=50.

The unique-key guard is sound as a **repaired-language front end**: its accepted domain is a subset of raw JSON texts with an injective decoded-name map. It is not a sound CEGAR refinement for proving a lower bound over the archived checker's original accepted language. The hostile path concretely accepts, so removing it would underapproximate accepted derivations and could miss a cheap legal path. For cost-lower-bound polarity, either historical authority must separately establish unique-name syntax, or the abstract domain must retain the accepted quotient and assign cost no greater than its concrete W=50.

Thus the repair does not close P2-D1 or P2-C3. It validates the exact obstruction and supplies a proposed canonical ingestion layer only.

## Resource ledger and peer reconciliation

Logical work is W=50 for both original accepted packets. Raw evidence grows from 4,144 to 4,345 bytes. The executable performs three original-checker subprocesses plus six lexical scans/controls. Its actual implementation holds the complete text and per-object decoded-name sets; a streaming implementation could use space proportional to nesting depth, current-object distinct keys and maximum key length, but no physical peak-memory measurement was made. Parsing, hashing, mutation construction, subprocess runtime and guard storage are not historical logical proof work.

LSPV-3/567 is independently confirmed under OS Node, upgrading its hosted-V8 evidence. LSPV-1/569's parsed-object finite normal form must state that it is after quotienting or repaired ingestion; it cannot infer finite raw accepted spellings. LSPV-2/554 and LSPV-4/540 remain valid at their stated parsed `/386` scopes. No evidence authenticates AND3, GF(2), LOCAL-CONVERT, branching, weakening, contexts, discharge, joins or deletions together in one historical dispatcher.

## Disposition

Material tracker delta: `[P2-L5-486]` records independent OS-Node validation, the exact decoded-key guard lemma and the lower-bound polarity firewall. P2-D1, P2-C3 and P2-B1 remain OPEN. P2-B2/B3 remain separate and OPEN. P versus NP remains OPEN.

