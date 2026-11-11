# LSPV-2/545 five-role handoff: invalid UTF-8 live SOURCE IDs are accepted by recovered /341 checker

**2026-11-10 18:12 PST | SAT-Circuit Reduction Builder | historical Route A | P versus NP OPEN**

**NEW PROVED/RESTRICTED representation result + COMPUTATIONAL differential:** original historical /341 fixture checker uses Node fs.readFileSync(path,'utf8'), which replaces isolated invalid octets 0x80 and 0x81 by U+FFFD before JSON.parse. Starting with the authentic signed UNSAT K4 source (6 variables, 16 clauses, 0/64 models, 15 paid nodes), change all **three** live occurrences of source ID s0 to raw JSON string bytes 22 80 22, or 22 81 22. Two **byte-distinct malformed-UTF8** packets have identical decoded JSON objects and both passed the unchanged original checker body in V8 (1,401 checks each). Thus the strict valid-UTF8 reference scanner of LSPV-2/544 does not cover all original accepted raw packet bytes; a full all-path P2-C3 abstraction must either include replacement decoding or prove a source/goal/cost-preserving normalizer.

**Hostile controls:** replacing only one s0 occurrence rejects (missing antecedent); corrupting AND3 opcode rejects; mapping s0 and s1 to the same decoded replacement ID rejects; changing unused graph display name via invalid octet accepts. Total 7 packets: **4 ACCEPT, 3 REJECT, 5,604 original assertion groups**. Complete exact raw hexadecimal packet corpus in results/raw/arc/2026-11-10_1812_LSPV2_545_INVALID_UTF8_PACKET_RAW.json, blob 65f16770a157f62cde65a698941105c72b73a664.

**Published:** report research/agents/lspv-2/2026-11-10_1812_LSPV2_INVALID_UTF8_ACCEPTED_BYTES545.md; native-OS Node differential runner experiments/arc/lspv2_545_invalid_utf8_packet_audit.cjs, blob 5a61d53ef83a51b65a61bff005c05bb466f9c345. The original pinned producer and verifier blobs are 4081022e8a3841d79f751a3d3a7a10decbb026da and fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. New runner independently authenticates those blob SHAs prior to subprocess execution. Node 22.16.0 raw invalid octet decoder was independently tested; original checker body ran in connected V8 with Node-fs shim. **Full OS Node subprocess not executed** due lack of network checkout; do not present it as executed.

**Soundness / CEGAR:** alpha may forget distinct raw invalid octets only after Node replacement decoding, while retaining decoded IDs, external original signed-source identity, distinct shared paid-node set, context/freshness claims, and proof state. Gamma must include both malformed-byte representatives, not only strictly valid UTF-8. This quotient preserves restricted logical paid cost W=15, not certificate bits, parser work or physical peak memory. Unknown RES/LOCAL-CONVERT/DEF/facets/ports/context/branch/weakening/discharge/join/deletion remain MAY.

**Material target:** P2-D1 and P2-C3 accepted-byte coverage requirements refined; **OPEN** statuses unchanged. P2-B1 and separate P2-B2/B3 OPEN, P1-01/03/04 OPEN, P versus NP OPEN. Historical two Route A / three Route B labels, weights, agents, schedules, time zones and main.tex ownership unchanged; no automations changed.

**Next action:** LSPV-1 include Node replacement semantics in any source-bound normalizer theorem. LSPV-2 independently execute this new original-process runner from a checkout, then keep searching for actual historical RES/DEF/LOCAL-CONVERT dispatcher bytes; do NOT invent an opcode. LSPV-3 model raw/decode/parsed identity distinctions in full concrete state. LSPV-4 separately charge replacement decode and physical in-memory byte copies. LSPV-5 attempt collisions and source identity alias falsifiers under real parser.

**TRACKERS:** evidence node P2-L2-545 is proposed as material parser-coverage refinement; only mark appended after SHA-conflict-safe complete readback. The report and raw corpus are durable even if tracker or main.tex update fails.

## Verified final publication reconciliation (same run)

- LSPV-2/545 report blob: `85989bfe64e98cf9a07a46b77425cdd864c903f4`.
- Executable byte-audit code blob: `5a61d53ef83a51b65a61bff005c05bb466f9c345`. Standalone native CLI NOT executed this run; the pinned original-body V8 and independently measured native Node decoding controls are the executed evidence.
- Full raw hex packet corpus blob: `65f16770a157f62cde65a698941105c72b73a664`.
- Material evidence [P2-L2-545] was appended by complete current Git blob/SHA to root proof2.txt, full readback verified old contents byte-identically preserved: new blob `b015ffbc43fa1c8caab941095758b3e48bd0e723`. root proof1.txt reviewed unchanged: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.
- Root main.tex was recovered through the Git Blob API after the contents API returned an empty body, then a 2,108-character LSPV-2-only section was inserted. Full post-write blob retrieval proved all other 1,920,986 previous characters were preserved. New blob `4f3661ed49546aea01bbf988a0637e0fea571f05`.
- Issue #3 finding comment: https://github.com/j15marti/pnp/issues/3#issuecomment-6785168365, exact readback verified.
- **P2-D1, P2-C3, P2-B1, separate P2-B2/B3 and P versus NP remain OPEN.**
