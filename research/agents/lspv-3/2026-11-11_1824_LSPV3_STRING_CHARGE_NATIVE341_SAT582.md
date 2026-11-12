# LSPV-3/582: JSON charge-type coercion in the original archived /341 source parser

**November 11, 2026, 18:24 PST (America/Los_Angeles) | Hypergraph & Proof Certificates, historical Route B | PROVED/RESTRICTED checker-code theorem + COMPUTATIONAL original-body V8 replay | P versus NP OPEN.**

## Candidate and four precise falsifiers

**Candidate P2-D1 / P2-C3:** On the **unchanged** archived `/341` SOURCE/AND3/XOR fixture verifier, a previously published accepted SAT-source packet can replace its noncanonical *numeric* first charge `4294967297` with the short JSON string `"1"`, Boolean `true`, or array `[1]`, without changing a single original signed source clause, paid derivation, parent reference or SAT witness. The accepted-byte grammar therefore cannot be described by a well-typed bit charge field, even if an independent parity-checking abstraction coalesces these values to bit 1.

Four falsifiers, fixed before the executed type differential: **F1**, the original checker rejects the string/Boolean/array case; **F2**, replacing with proper numeric 1 is accepted just as often; **F3**, the explicit assignment fails to satisfy the in-band original signed CNF; **F4**, negative controls for incorrect source, unsupported opcode, invalid parent/affine row or invalid sink are also accepted. All four fail in the hosted original checker and direct signed-clause evaluation.

This extends, and depends upon, LSPV-3/568's *previously published* SAT-source input. It does **not** claim a new independently sound SAT refutation or that charge type coercion is the only defect in that packet: the /568 source also relies on the pre-existing malformed affine-support annotation bypass.

## Pinned original sources and precedents

- Original archived `/341` checker, `experiments/arc/lspv2_341_independent_verify.js`, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**.
- Original archived `/341` producer, `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js`, Git blob **4081022e8a3841d79f751a3d3a7a10decbb026da**.
- Prior accepted SAT-source certificate from LSPV-3/568, `results/raw/arc/2026-11-11_0424_LSPV3_568_NUMERIC_WRAP32_SAT_ACCEPTED_PACKET.json`, Git blob **adb4864906029ecf7b1cd1cf7a4bf513218a13a8**.
- The different /386 checker, `experiments/arc/lspv2_386_independent_verify.js`, Git blob **338305c0ce101704205e57543756b8127074a986**, does **not** authenticate the same signed original source or share a dispatcher.
- Consulted recent peer controls: LSPV-4/539 (native free-facet quotient), LSPV-3/543 (separate declared-semantic facets), LSPV-2/549 (dual-checker polyglot), LSPV-1/553 (/341 incomplete native rule coverage), LSPV-3/568, /578 and /581, and issue #3 through LSPV-1/585.

External comparison specifications are distinct systems: [FRAT-XOR formal format](https://github.com/meelgroup/frat-xor/blob/main/format.md), [Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, 1979](https://doi.org/10.2307/2273702) and [Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000](https://doi.org/10.1007/10722167_15). None licenses inventing historical R_mix341 transitions.

## Theorem 582.1: strict-type versus bitwise-coercion acceptance

In the original checker the charge schema is tested only by `f.charges.length===V` and

```js
f.charges.reduce((x,y)=>x^y,0)===1
```

At each SOURCE clause, the separately evaluated local forbidden-pattern check is

```js
parity!==f.charges[v]
```

where `parity` is a primitive integer bit in {0,1}. In ECMAScript, bitwise XOR first applies numeric 32-bit coercion, whereas `!==` does not coerce types. Thus

```js
(0 ^ "1") === 1;  (0 ^ true) === 1;  (0 ^ [1]) === 1;
1 !== "1";        1 !== true;        1 !== [1];
```

The string, Boolean and array have the required XOR residue 1 yet make the intended local equality check nonrestrictive. For the *same exact signed clauses*, numeric `1` makes the invalid local forbidden-pattern parity visible and the original checker rejects. Replacing **all twelve** charge entries with strings (`"1"`, `"0"`) also retains original checker acceptance. A correct typed source parser would instead require `charge[v]===0 || charge[v]===1` *before* interpreting source parity; that would be a **reference repair**, not an authenticated historical checker.

The original signed source in the accepted fixture consists of **48 clauses on 18 edge variables**. Assignment

```
101001000000100000
```

satisfies **48/48** clauses by independent literal evaluation. All original proof records, supported tables, row masks, parent edges, original clause IDs and chronology remain byte-value identical across the charge substitutions. This establishes a literal SAT-source acceptance defect in the recovered fixture checker, **not** a genuine mathematical derivation of contradiction.

## Exact original-checker differential

The original archived checker body was executed in **hosted V8** through `new Function`, adapting only `require('fs')`, `process.argv` and `console.log` to supply the serialized exact JSON input. The source of the checker was fetched directly from GitHub; no independent replacement checker determined acceptance. All positive cases passed the original verifier's five built-in corruption controls and seven malformed-CNF controls.

| Exact first charge representation | UTF-8 JSON bytes (compact plus newline) | Original verdict | Checker assertions |
| --- | ---: | --- | ---: |
| Prior numeric `4294967297` | 8,581 | ACCEPT | 3,273 |
| JSON string `"1"` | **8,574** | **ACCEPT** | **3,273** |
| Boolean `true` | 8,575 | ACCEPT | 3,273 |
| Array `[1]` | 8,574 | ACCEPT | 3,273 |
| Every charge a string | 8,596 | ACCEPT | 3,273 |
| JSON string `"01"` | 8,575 | ACCEPT | 3,273 |
| JSON string `"0x1"` | 8,576 | ACCEPT | 3,273 |
| Proper numeric `1` | 8,572 | **REJECT** | source forbidden pattern parity |

Total differential: **7 accepted and 11 rejected** over 18 byte-distinct candidate classes. Other rejected controls: string zero, Boolean false, empty array, null, nonnumeric string, unsupported `LOCAL-CONVERT`, nonexistent parent, forged signed SOURCE literal, invalid affine mask, and corrupted sink. The last five isolate surrounding grammar checks; they do not imply an all-rule mixed language.

All sizes above include one trailing LF, matching the published **8,574-byte** exact string-charge certificate.

## CEGAR and exact logical-work implications

A cost-sound overapproximation of *actual checker acceptance* cannot silently reject `"1"` while admitting numeric 1 as an interchangeable source-parity bit: that would exclude a concrete accepted-byte path and violate concrete-step inclusion. Conversely, an abstraction representing *mathematically sound source refutations* **must not** regard the accepted SAT-source path as a legitimate refutation. These are distinct relations. For a historical acceptance interpreter, retain a field's **raw JSON type**, its ToInt32 XOR residue, the numeric signed-literal source occurrence, strict-equality comparison and untrusted source-binding status separately.

The no-new-derivations transformation preserves all **47** existing paid AND3/XOR records and their original ordered shared DAG. This does not establish minimum work, and the checker's fixture-length convention is not a complete fixed historical weighting contract. Treat unimplemented RES, LOCAL-CONVERT, DEF, exported/private wires, branching, weakening, discharge, reconvergence, deletion or joins as **unknown/MAY** for the full historical calculus, not silently rejected or made free.

### Publication and reproducibility

- Exact original-checker accepted packet: `results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json`, Git blob **6cf9b0fe1e5a9419e8967d836c707c385418b810**.
- Raw 18-case hosted-original differential: `results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_HOSTED_ORIGINAL341_RAW.json`, Git blob **1b3fb2a385a3f66a0932625a447d2911eb9fb638**.
- Standalone unchanged-original **OS subprocess** reproducer: `experiments/arc/lspv3_582_string_charge_original341_os_replay.cjs`, Git blob **37021476f4c17b3b6d5bdf399cc21b2099c3822**. Script syntax was parsed in hosted V8, but OS process execution was **not performed** in this run. The script checks original Git blobs, byte identity, original positive/negative verdicts, and independent SAT witness; it must be executed separately for OS claims.
- Dated five-role handoff in `research/coordination/`.

## Proof tracker status and next falsifiers

**P2-D1 OPEN:** this is an additional exact JSON-schema acceptance distinction in an incomplete archived /341 checker. No historical single-dispatcher original-source-bound complete R_mix341 certificate was found.

**P2-C3 OPEN:** typed abstraction must distinguish raw field tags from coerced bits and acceptance from sound mathematical derivation, while preserving shared-DAG and paid-node identity.

**P2-B1 OPEN; P2-B2 and P2-B3 separately OPEN:** no superpolynomial all-rule minimum, no B3 fixed-system simulation theorem, no SAT decision-time transfer. P1-01/03/04 unchanged. **P versus NP remains open.**

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both complete root proof trackers were read with their GitHub contents and SHA. Existing exactly five role identities, Pacific hourly schedules, two Route A / three Route B assignments, ownership boundaries and all historical fixed weights remain unchanged. No automations were created or modified.

## Publication receipt and owned manuscript reconciliation

The dated five-role handoff is published at `research/coordination/2026-11-11_1824_LSPV3_STRING_CHARGE_FIREWALL582_FIVE_ROLE_HANDOFF.md`, original Git blob `8a9771511a4cb65a85ee42744e82eb32e321cdb5`. Issue #3 coordination comment was posted as [issue comment 6812708838](https://github.com/j15marti/pnp/issues/3#issuecomment-6812708838).

`main.tex` was recovered through its complete Git blob, because the standard GitHub contents fetch returned empty text for this large file. Prewrite blob `d58bcdbacff8c17dd7a090dd463cad1a0a89bf29`, 2,143,390 characters; authorized `LSPV-3/582` insertion 2,069 characters, entirely within the unique LSPV-3 owned sentinels; commit `5284b78411b29b973bc1a77d6ed7195924bf0201`; postwrite blob `63cad737142a47bd0ae756528afdc8a62ae74f9f`, 2,145,459 characters. Full Git blob readback confirmed byte-for-byte equality to the composed manuscript, and removing the insertion exactly reconstructs every character of the previous manuscript. No unrelated owner's region was altered.
