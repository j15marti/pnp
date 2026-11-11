# LSPV-2/545: Ill-formed UTF-8 SOURCE identifiers accepted by the recovered historical fixture checker

**2026-11-10 18:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED ECMAScript/Node decoding lemma + COMPUTATIONAL original-body replay. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE; four falsifiers

**Candidate.** LSPV-2/544's strict valid-UTF-8 byte scanner is not a complete representation of the recovered /341 fixture checker's accepted **raw byte** inputs, because the original checker reads packet files through Node fs.readFileSync(path, 'utf8'), which replaces invalid UTF-8 octets instead of rejecting them. Test a live SOURCE identity rather than irrelevant comments or unused metadata. A proof-path abstraction restricted to strictly valid UTF-8 would then miss an actually accepted proof packet.

**F1:** Native Node decoding might reject invalid 0x80 and 0x81. **FALSIFIED:** native OS Node v22.16.0 Buffer UTF-8 decoding maps both isolated octets to U+FFFD; strict TextDecoder('utf-8', {fatal:true}) rejects. The original checker source explicitly invokes fs.readFileSync(...,'utf8').

**F2:** Changing a live SOURCE ID to the decoded replacement character might break shared parent lookup. **FALSIFIED:** changing all THREE occurrences of live K4 source s0 to the same decoded character preserves all 1,401 original-checker assertions.

**F3:** The checker could accept a corrupted opcode or broken sharing despite the mutation. **FALSIFIED:** replacing only the first source-ID occurrence rejects with missing antecedent, replacing the AND3 opcode rejects with unknown rule, and simultaneously mapping s0 and s1 to the same decoded U+FFFD rejects with duplicate source ID.

**F4:** Strict byte validation could still cover all native-accepted packets by treating raw invalid bytes as errors. **FALSIFIED:** two byte-distinct raw accepted packets contain 0x80 versus 0x81, while their entire decoded JSON strings and parsed objects agree. A fatal strict-UTF-8 prefilter would discard both accepted paths.

**Precedence.** This is not a rediscovery of /540 duplicate JSON keys, /541 Infinity IDs, /543 ASCII spans, /544 Unicode-escape equivalence, LSPV-5/479 negative zero, or LSPV-3/557 SAT-source forgery. Those examples involve valid UTF-8 source bytes. The previously explicit /544 gap was that invalid UTF-8 was rejected by the **reference**, not tested at the original raw-byte decoder boundary. This run closes that specific finite gap.

## Authenticated scope and original source

Historical mathematical declaration: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, Git blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. It declares source-explicit unit-paid RES, AND3, XOR, LOCAL-CONVERT and conservative DEF, with other branch/context/deletion obligations not given complete accepted-byte syntax.

Original producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, blob 4081022e8a3841d79f751a3d3a7a10decbb026da. Original independently written **restricted fixture checker**: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0.

The recovered checker only dispatches AND3 and XOR and hardcodes a proof-length rule for its cubic fixtures. It is not the authoritative complete R_mix341 checker, not an external-source-bound proof system, and has independently documented acceptance defects for some SAT sources. All claims below concern original signed UNSAT K4, not the forged SAT-source packet.

## Theorem 545.1: native accepted-byte language strictly extends the strictly decoded reference domain

Let D be Node's replacement-mode UTF-8 decoder, P the JavaScript JSON parser, and C the recovered original checker body operating on P(D(b)). Consider the original K4 certificate b0: 16 signed 3-CNF sources, six edge variables, zero satisfying assignments among 64, and 15 distinct paid AND3/XOR nodes.

Construct b80 by replacing each of the three raw ASCII token bytes for string value s0 (quoted) with the bytes 22 80 22. Construct b81 similarly using 22 81 22. No other bytes are changed. Both raw strings are **not valid UTF-8**. Yet

$$
b_{80}\ne b_{81},\qquad D(b_{80})=D(b_{81}),
$$

and both decoded values replace source ID s0 and its two descendant references with the same JavaScript string U+FFFD. Consequently all shared-ID map lookups still succeed, and the original checker accepts both with its original source/inference checks:

$$
C(b_{80})=C(b_{81})=\mathrm{ACCEPT}.
$$

Any reference parser that rejects every non-strictly-valid UTF-8 stream has a proper under-approximation of this recovered checker's raw accepted-byte language. This is a proof of an **operational representation gap**, not of mathematical unsoundness or complete-calculus semantics.

**Proof scope:** On the pinned code path, Node reads raw bytes with 'utf8' replacement decoding, then JSON.parse. The two byte mutations occur inside string values. By inspection, all decoded values, including original signed clauses, proof operators, source IDs, paid IDs and parent lists, coincide between b80 and b81. The unmodified original-body checker passes 1,401 assertions for each. Node's tested decoder maps both isolated invalid bytes to the same U+FFFD. Strict fatal-mode decoding rejects both. A reimplementation that insists on fatal UTF-8 therefore cannot project every actual accepted concrete path without first proving an appropriate cost- and source-preserving normalizer.

**Lexical cost qualification:** Each changed token occupies three raw bytes instead of the four-byte ASCII token "s0". The shortest direct, legal UTF-8 spelling of the *same* U+FFFD string value is five bytes including quotation marks. A lexeme-preserving replacement costs an additional two bytes per occurrence, six bytes for all three. This is NOT a no-go theorem for identity-aware renaming or compression, which may choose another shorter collision-free ID.

## Raw results and execution status

The separately published raw corpus contains all seven exact certificate **octet sequences in full hexadecimal**, not only textual recipes. The unmodified original producer and checker bodies were fetched at their pinned Git blobs and invoked in the connected V8 engine with only the fs and console wrappers replaced. Each wrapper returned the precise JavaScript string that Node's replacement decoder produces from the corresponding octets. Independent local **OS Node v22.16.0** tested 0x80 and 0x81 replacement behavior; the new published standalone script makes the complete, genuine-Node subprocess execution reproducible from a repository checkout.

| Packet | Raw bytes | Original-body V8 verdict | Check groups |
| --- | ---: | --- | ---: |
| Unchanged K4 | 3518 | ACCEPT | 1401 |
| All three source s0 tokens: invalid 0x80 | 3515 | ACCEPT | 1401 |
| All three source s0 tokens: invalid 0x81 | 3515 | ACCEPT | 1401 |
| Only first source s0 token: invalid 0x80 | 3517 | REJECT | n/a |
| First AND3 opcode: invalid 0x80 | 3515 | REJECT | n/a |
| Distinct s0/s1 raw invalid bytes decode to same ID | 3512 | REJECT | n/a |
| Graph display label: invalid 0x80 | 3517 | ACCEPT | 1401 |

**4 accepted, 3 rejected, 5,604 successful original-checker assertion groups.** A full standalone OS Node subprocess of the pinned original checker **has not been run in this session**, since the container cannot resolve github.com for checkout; the generated script was syntax-tested and published/read back, but its end-to-end subprocess results should be independently executed on a checkout. This caveat does not weaken the direct original-body V8 differential result or the independently verified Node decoder behavior.

Published native-CLI executable: experiments/arc/lspv2_545_invalid_utf8_packet_audit.cjs, blob 5a61d53ef83a51b65a61bff005c05bb466f9c345. The executable SHA-authenticates the Git blob of BOTH original scripts before invoking either, constructs seven raw packets, invokes the original checker in Node subprocesses, compares expected verdicts, enumerates all 64 signed K4 assignments, and emits the raw audit summary. The complete raw packet ledger is results/raw/arc/2026-11-10_1812_LSPV2_545_INVALID_UTF8_PACKET_RAW.json, blob 65f16770a157f62cde65a698941105c72b73a664. The ledger explicitly labels its V8 execution boundary rather than claiming OS subprocess completion.

## Cost-sound transition projection and CEGAR

A concrete state must retain raw octets b, decoder mode D, parser state, decoded JSON object, original signed source commitment, SOURCE occurrence identities, actual JavaScript Map key equality, parent references, paid creation IDs, shared-DAG dependencies, claimed contexts, wires/ports/definitions, output and cumulative physical work and live peak. For known fixture transitions, define alpha to retain P(D(b)), source identities and signed clause occurrences, verified AND3/XOR states, and the global paid-creation set, but optionally forget **which ill-formed octet** decoded to U+FFFD. Define gamma by all byte strings with the same decoded object and correct source/transition information. The checker-specific logical unit cost and complete goal project exactly for the authenticated fixture derivations; no byte-length or native time/space bound follows from forgetting raw octets.

An abstract low-cost path that changes only a single shared SOURCE occurrence is **spurious**, because the unchanged checker rejects it and a refinement may record ID equality. The complete three-occurrence invalid-byte replacement is **real**, because the checker accepts, and MUST remain in a cost-sound MAY overapproximation. The collision of two distinct source IDs is a genuine native rejection, not evidence against source sharing generally.

For **unknown full-calculus** RES/LOCAL-CONVERT/DEF/facets/contexts/wires/branch/discharge/joins/weakening/deletion operations, the abstract transition relation must still include MAY behavior with a justified optimistic cost. No missing full-rule operation has been shown illegal by these tests. Inference-node count 15 is not certificate length, construction time, parsing work, proof DAG acquisition, span, transient allocations, or physical peak memory.

## Scientific and publication reconciliation

Primary sources: Cook–Reckhow (1979), DOI 10.2307/2273702, fixes proof-system verifier importance; D'Silva, Haller and Kroening, *Abstract Satisfaction*, POPL 2014, DOI 10.1145/2535838.2535868, motivates sound abstract transitions; ECMA-262 and Node's Buffer/UTF-8 decoding contract justify parsed-identity versus byte-identity distinction. The exact signed Tseitin controls predate this run and are not claimed novel.

Read BOTH root proof trackers, issue #3 (1594 comments), AGENTS.md, CODEX.md, research skill, Nov 9/10 five-role handoffs, historical /341 original source, LSPV-2/537-544, LSPV-3/556-557, LSPV-5/479-480 and LSPV-1/560 issue receipt, LSPV-4/530 issue receipt. Change-aware external repository checks: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 and blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5. No checked external source supplies historical complete R_mix341 syntax.

**Proof statuses:** [P2-D1], [P2-C3], [P2-B1], separate [P2-B2]/B3 and [P1-01], [P1-03], [P1-04] all OPEN. The present **restricted** counterexample materially refines a parser coverage dependency but cannot close full calculus authentication, a global cost-sound abstraction, a superpolynomial lower bound, or the bridge to unrestricted SAT decision time. Every accepted history must remain represented; a strict decoder alone is unsound for full native accepted-byte coverage.

All five existing titles, identities, schedules, timezone, two Route A/three Route B labels, historical weights, and ownership boundaries remain preserved. No automations changed. P versus NP OPEN.
