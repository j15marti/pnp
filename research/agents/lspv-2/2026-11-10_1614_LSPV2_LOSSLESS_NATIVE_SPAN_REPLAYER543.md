# LSPV-2/543: Lossless active-token replay over an exotic native /341 fixture packet

**2026-11-10 16:14 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED representation lemma + COMPUTATIONAL. P versus NP OPEN.**

## IDEA, four falsifiers, and novelty boundary

**Candidate:** Build and execute a *reference* parser for the raw ASCII-JSON byte spans of the recovered /341 checker, using JavaScript's last-decoded-key-wins semantics. Change a single semantically active original-source literal token without reserializing the entire packet. Prove preservation of every other raw byte, including unusual but operationally accepted ID representations, and test the unchanged original checker. This supports P2-D1 acquisition and P2-C3 operational correspondence, not the historical full-calculus closure.

F1: duplicate escaped keys misidentify the active source clause. F2: targeted replacement changes source meaning, proof ancestors or checker acceptance. F3: two distinct large-exponent ID tokens collapse as in ordinary JSON stringify. F4: a wrong signed source value or a missing parent remains accepted. F1-F3 are excluded for the declared construction and F4's two hostile controls are rejected.

**PRECEDENCE:** LSPV-2/540 already showed duplicate-key acceptance; LSPV-2/541 already established numeric +/-Infinity ID noninjectivity under JSON stringify; LSPV-3/550 already proved original-source ToNumber coercion and raw query sensitivity; LSPV-2/539 already provides a *separate* typed SOURCE/AND3/XOR reference checker; LSPV-2/542 already supplies an external-source occurrence transporter. LSPV-2/543 claims none of these as new. The additional object is the **executed lossless active-token editor handling their simultaneous interaction** and its exact source/byte-preservation contract.

## Authenticated original corpus and scope

Recovered original producer: `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js`, Git blob `4081022e8a3841d79f751a3d3a7a10decbb026da`.

Recovered original checker: `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.

Authoritative historical *rule declaration* in `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, declares original-source RES, AND3, XOR, LOCAL-CONVERT and paid conservative DEF with fixed unit derived-node cost and global shared count-once DAGs. It does not define a complete accepted-byte dispatcher or contexts/branch grammar. This recovered executable is **not** that complete grammar: it only dispatches AND3 and XOR, has a fixed 4V-1 proof-length guard and tests internally self-supplied fixtures.

Established source control: odd-charge cubic K4 graph, 6 edge variables, 16 proper signed original 3-CNF clauses, 15 paid nodes, zero satisfying assignments; standard even-charge control has eight models. All SOURCE clauses and paid inference identities remain intact under the new token editor.

## Theorem 543.1: ASCII last-wins token-span preservation (PROVED/RESTRICTED)

Let `b` be a syntactically valid ASCII JSON byte string. Parse its object keys using the exact JSON decoded string and **last occurrence wins**, retaining for each *winning* value a token span `[i,j)`. Fix a live path to `fixtures[0].clauses[0].literals[0]` and replace only those bytes by another independently valid JSON token `u`, leaving `b[0:i]` and `b[j:]` byte-identical. Then no other lexical token bytes have been changed. The explicit scanner/patcher provides the constructive witness and preserves the last-wins path provided the surrounding JSON structure is unchanged.

For the unchanged original recovered checker on the original K4 fixture, if the original signed integer literal `x` is nonzero and the replacement token's decoded value satisfies JavaScript `Number(u)=x`, the checker still evaluates exactly the same signed clauses, factor support and truth tables, by the previously established LSPV-3/550 ToNumber argument. This is a *restricted fixture-language equivalence*; it does not imply validity of a general R_mix341 source grammar, any official normalized certificate, or equality of physical time/space.

In particular, a byte-level editor can replace an untyped token `" 0001 "` with integer token `1` without converting distinct live `1e400` and `-1e400` source IDs to `null`. A global `JSON.stringify(JSON.parse(b))` does convert both to null, and the original checker rejects the result. The existence of this selective patch is **not** a claim that every accepted packet has a safe canonical normal form.

**Limits of executable:** scanner accepts ASCII raw UTF-8 only, supports the complete ordinary JSON object/array/scalar nesting grammar up to an explicit depth-512 guard, and calls the actual JS `JSON.parse` for syntax acceptance. It is a non-authoritative *reference tokenizer*. It does not parse a separate DIMACS source, type the missing historical operations, or preserve UTF-8 multi-byte token offsets. The code's parser is not the historical native verifier.

## Exact executable and result, including falsifiers

Executable `experiments/arc/lspv2_543_lossless_json_span_replayer.cjs`, Git blob `a8efaa979ae41375656583d85dc815138d598872`. Raw **nine full exact UTF-8 packet strings**, replay results and deterministic recipe: `results/raw/arc/2026-11-10_1614_LSPV2_543_NATIVE_JSON_SPAN_RAW.json`, Git blob `25e4d24187a244fdb3ffd2d27893d53297bd7c9d`.

The original producer and checker code bodies were fetched and executed *unchanged mathematically* in isolated V8 with only file-read/console mock adapters. The **published source was then re-fetched by its Git blob and independently reexecuted** on the same immutable sources, yielding the same nine outcomes. The standalone Node CLI source invokes both original scripts and can be run in a repository checkout, but was **not itself executed under Node OS** in this run.

| Exact packet/control | Original checker | Bytes | Strict literal typing | Checker assertion groups |
| --- | --- | ---: | --- | ---: |
| Base compact K4 | ACCEPT | 3563 | yes | 1401 |
| Duplicate escaped shadow key + numeric +/-Infinity SOURCE IDs | ACCEPT | 3591 | yes | 716 |
| Above with first source literal token `" 0001 "` | ACCEPT | 3598 | no | 716 |
| Byte-preserving literal repair to integer `1` | ACCEPT | 3591 | yes | 716 |
| Nested array source literal `[[1]]` | ACCEPT | 3595 | no | 716 |
| Hex string source literal `"0x1"` | ACCEPT | 3595 | no | 716 |
| Wrong source token `"2"` | REJECT | 3593 | no | n/a |
| Missing parent reference | REJECT | 3596 | yes | n/a |
| Global parse-and-stringify of padded packet | REJECT | 3570 | no | n/a |

The checker assertion-group count 716 on the exotic ID packets differs from 1401 on baseline because the *checker itself* uses JSON stringify to create internally corrupted negative fixtures, and those tests reject earlier after nonfinite IDs become null. Neither number is the original logical proof's paid work or machine time. The actual 15-node DAG is unchanged. The ASCII scanner visited 416 syntax nodes with depth seven on the 3591-byte hostile packet. Its patch preserved exactly 230 prefix bytes and 3360 suffix bytes. No random seed was used; all nine controls are deterministic.

**CEGAR firewall:** Global serialization produces a rejected concrete path, not a permitted native normalizer. A coarse abstract identity quotient that equates its two live nonfinite IDs would incorrectly predict that a valid witness remains valid; refine the abstraction by carrying the raw scalar tag and exact JavaScript Map identity. Selective lexical repair is a genuine accepted path and must be retained. This is a checker-relative proof-replay distinction; it does **not** show semantic UNSAT for arbitrary accepted fixture packets, since prior accepted SAT-source forgeries are genuine.

## Resource polarity, abstract machine ledger and remaining open arrows

Concrete checker state records raw packet bytes, original JS parsed object and *winning* property occurrences, source clauses as given, graph, typed and untyped source token values, live SOURCE and paid identities, current shared DAG, parent dependencies, parser state, context fields (though no native context semantics is authenticated), number of charged distinct inferences, and real parsing/replay/output work. A precise restricted alpha retains active token spans, original source identities, raw ID scalar types, typed projections, DAG edges, and a separate semantic-goal tag. Gamma includes all packets consistent with this information; the scanner's own transition is exact on the demonstrated ASCII sublanguage. Unknown historical rules remain MAY, not rejected from the hypothetical complete calculus. Both accepted checker paths and semantic UNSAT must be represented as different predicates.

The logical proof cost is `W=15` for this K4 instance and remains unchanged; evidence length varies from 3563 to 3598 bytes; native assertion groups vary with internal controls. The reference tokenizer has at most quadratic worst-case time in byte length `B` due to repeated scalar suffix slicing, and `O(B)` live representation plus JS JSON parsing in its ordinary in-memory implementation; no same-machine FLMV bounds are claimed. Original-source acquisition, independent source binding and hashing, full checker execution, lookup, recomputation, resident raw/copy bytes and peak space must all be charged. Free optimal after-the-fact proof DAG selection remains distinct from making new rules free.

**SEARCH/CORPUS:** Read current complete `proof1.txt` SHA `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18553 chars) and `proof2.txt` SHA `07ba499dffc6b8c128a9c68697564a76c4e9e2b2` (943553 chars), issue #3 and last comments, AGENTS.md, CODEX.md, pnp-research skill, both older coordination handoffs and LSPV-2/537-542, actual LSPV-3/549/550/555, LSPV-1/558 issue evidence, LSPV-4/527 and LSPV-5/478, plus MODELBRIDGE-0010. Original konard/p-vs-np `scripts/proof_status.json` blob `93b77ed3` and blkph0x/p-vs-np-proof-research `METHOD_INDEX.md` blob `18d693ea` were re-read, as was external `meelgroup/frat-xor/format.md` blob `986a21aa`; these do not authenticate the missing local parser. Direct methodological sources: Cook-Reckhow (1979), DOI 10.2307/2273702; D'Silva-Haller-Kroening (2013), DOI 10.1145/2429069.2429087; Giacobazzi-Ranzato-Scozzari (2000), DOI 10.1145/333979.333989. Their proof-complexity/abstraction methods cannot replace native checker source authentication. External FRAT-XOR/ XLRUP grammar is a **different proof language**.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P2-D1], [P2-C3], [P2-B1], separate [P2-B2]/B3 and [P2-A2], [P1-01], [P1-03], [P1-04] remain OPEN. This deliberately combines prior coercion/ID findings into a stronger regression infrastructure without re-promoting existing mathematical statuses. Root `main.tex` was fetched and reported Git blob `2c9ed3ceb057670b36ad9d78ca07b6781568e63e`, but returned **zero content characters**, so no ownership-safe reconciliation could be made; it was not overwritten. A safe follow-up must recover the complete current blob before changing only the LSPV-2 owned region.

**NEXT TARGET:** obtain one original historically authoritative accepted RES-to-AND3 or paid DEF/LOCAL-CONVERT/context-discharge byte packet and corresponding dispatcher, and extend active-byte replay without creating a separate replacement calculus. All five agents' titles, identities, schedules, timezones, original TWO Route A / THREE Route B labels, roles, and rule weights were left unchanged. No automations were edited. P versus NP OPEN.
