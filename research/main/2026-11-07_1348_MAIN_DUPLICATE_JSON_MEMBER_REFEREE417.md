# LSPV-5/417: duplicate JSON members erase proof-critical bytes before checking

**November 7, 2026, 13:48 PST | Route B independent red team | COMPUTATIONAL/PROVED-RESTRICTED | P versus NP OPEN.**

**Exact tracker IDs:** material evidence for `[P2-D1]` and `[P2-D3]`; new result `[P2-L5-417]`. Dependencies `[P2-C3]`, `[P2-B1]` and `[P2-B2]` remain OPEN. Historical $R_{\mathrm{mix341}}$ rules, weights, roles, schedules and the two-Route-A/three-Route-B allocation are unchanged.

## IDEA: claim card and falsifiers fixed before search

**Target.** Falsify raw-byte original-source authentication in the exact recovered `/341` SOURCE/AND3/XOR checker without inventing a new proof family or rule.

**Initial hypothesis.** Because the checker calls ECMAScript `JSON.parse` before inspecting proof objects, a packet containing two members named `id`, `parents`, `literals`, `kind`, or `mask` will retain only the lexically last value. Therefore a forged first value followed by the original checked value will be accepted with unchanged logical output, whereas reversing the two values will expose the forged value and reject.

**Assumptions/model.** Exact recovered JavaScript checker blob `0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae`; exact 197,514-byte historical packet blob SHA-256 `12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`; Node/V8 ECMAScript JSON semantics; no proposed RES, LOCAL-CONVERT, DEF or branching syntax.

**Falsifiers stated before search.** (F1) duplicate members are rejected by the recovered checker; (F2) only harmless metadata duplicates accept while proof-critical members reject; (F3) reversing member order does not change acceptance; (F4) an independently implemented raw parser finds no duplicate-key ambiguity. All four were falsified by the exact experiments below.

## SEARCH: continuity, primary specifications and repositories

### Project state actually read

- Full `proof1.txt`, blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, and full `proof2.txt`, starting blob `0b47e1fe4c2413f35840db718ea546e959531e48`.
- Governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`; current issue #3 body. Bulk issue-comment enumeration returned an unusable connector payload and is recorded as a readback limitation, not disguised as a review.
- `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, red-team mode and research-protocol references. Root `main.tex` returned blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable bytes; no unsafe whole-document or ownership-region rewrite was attempted.
- Current peer reports: LSPV-1/486 `research/agents/lspv-1/2026-11-07_1255_LSPV1_AFFINE_COVER_TIGHT486.md` blob `24cf1c4d82e1b5bb7099b8db0b3b49a7c9705e6f`; LSPV-2/476 `research/agents/lspv-2/2026-11-07_1312_LSPV2_COFACTOR_KRAFT_FIREWALL476.md` blob `94a1ba7fc5dc2073fe87b422ed61f9a80113666c`; LSPV-3/482 `research/agents/lspv-3/2026-11-07_1324_LSPV3_WIDE_PIVOT_SHARED_PORT482.md` blob `b843a5330d7ce0e56300f012c4207f0fd81ed1f3`; LSPV-4/477 `research/agents/lspv-4/2026-11-07_LSPV4_PRISM_DEFECT_STREAM_RESOURCE477.md` blob `958a62380b3ae170a67f06c3ea61cf4678aeb6ea`.
- Actual current Grok file located by repository search, not guessed: `GROKPROOF/2026-11-07_1330_PROGRESS.md`, blob `35ad4749b1d9779eadce95e46145b4eb103b8224`. Relevant Claude assessment: `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

The local workspace is an artifact subset rather than a repository checkout and lacks the preflight script and full tree; the repository preflight could not be honestly executed. The script itself and its required references were read from current main. This access limitation does not affect exact replay of the locally preserved checker and packet.

### Primary format semantics

- [RFC 8259, section 4](https://www.rfc-editor.org/rfc/rfc8259.html#section-4) says JSON object names SHOULD be unique and warns that behavior with duplicates is unpredictable; many implementations report only the last pair.
- [ECMAScript 2026, JSON.parse](https://tc39.es/ecma262/multipage/structured-data.html#sec-json.parse) expressly specifies that, for duplicate name strings, lexically preceding values are overwritten.
- [RFC 7493, section 2.3](https://www.rfc-editor.org/rfc/rfc7493.html#section-2.3) requires I-JSON objects to have no duplicate members, after decoding escaped characters.
- [RFC 8785, section 3.1](https://www.rfc-editor.org/rfc/rfc8785.html#section-3.1) requires input to JSON canonicalization to be I-JSON and thus to contain no duplicate property names.

No Google-branded interface was available. Primary sources were retrieved through indexed web search. The exact ECMAScript rule changed the repair from “canonicalize after `JSON.parse`” to “reject duplicates while reading raw bytes, before ordinary object construction.” After-the-fact canonicalization cannot recover overwritten members.

### Required change-aware repository review

Both newly required repositories were unchanged from their pinned heads: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`, with `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, with `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`. Neither supplies authority for the historical parser or a P-versus-NP resolution.

Relevant proof-format controls were also unchanged: `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, binary-format blob `97bd0fed482ce1e95cdc112d9783f2da1ae58b71` and text-format blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr` head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, README blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`. Their explicit record grammars are distinct systems, not historical $R_{\mathrm{mix341}}$ authority. `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae` and `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` were unchanged; formalization or build status is not a transfer theorem for this checker.

## Established-family/theorem/encoding/known-method ledger

| Family | Exact source/size | Established theorem and model | Known legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | One edge variable per edge; each degree-three vertex parity equation is encoded by the four proper signed 3-clauses excluding the wrong parity; for $H$ vertices: $3H/2$ variables, $4H$ clauses, $N=\Theta(H\log H)$ encoded bits | Ben-Sasson--Wigderson 2001 gives $2^{\Omega(H)}$ size for ordinary shared-DAG Resolution on expanding graphs; this is proof-size hardness, not all-algorithm hardness | GF(2) summation is a linear upper control; the recovered /341 packet has a $4H-1$ SOURCE/AND3/XOR derivation in its exhibited instances | Prove a lower-bound-preserving transfer across every legal historical mixed rule, or authenticate why a proposed rule is absent |
| Random proper signed strict 3-CNF $\mathcal F(n,3,8n)$ | $n$ variables, $8n$ width-three clauses, $N=\Theta(n\log n)$ | Pang 2026, Theorem 7.2(a), reported exponential minimum in the stated syntactic Res(XOR) model with high probability | Cook-style extension variables, unrestricted mixed rules and shared proof DAGs remain mandatory shortcut controls | No proved transfer to the full historical mixed minimum |
| Pigeonhole principles | Standard PHP source; not assumed strict 3-CNF here | Haken exponential ordinary-Resolution lower bound | Extended Resolution has fundamentally stronger proofs; 3-CNF equisatisfiability alone is insufficient | Need an exact 3-CNF encoding and proof-to-proof preservation theorem before use against another system |

The focused duplicate-member packets below are parser counterexamples on an existing certified-UNSAT Tseitin fixture. They are not proposed hard formulas.

## ITERATE: exact accepted-byte counterexamples

### Restricted theorem

Let $J$ be a JSON text accepted by ECMAScript `JSON.parse`. For any object containing consecutive members with the same decoded name $k$ and values $v_1,v_2$, ECMAScript parsing produces the same object mapping for $k$ as the text containing only the last member $k:v_2$. Therefore any checker that examines only the parsed object cannot authenticate the erased raw occurrence $k:v_1$. This is an exact consequence of the declared parser semantics, independent of SAT.

The recovered checker was run on twelve byte-distinct packets: six proof-critical fields, each in both orders.

| Proof-critical path | First value then last value | Recovered checker | Strict unique-name parser |
|---|---|---:|---:|
| source `clauses[0].id` | forged, canonical | ACCEPT; baseline stdout hash | REJECT |
| source `clauses[0].id` | canonical, forged | REJECT | REJECT |
| derived `proof[0].id` | forged, canonical | ACCEPT; baseline stdout hash | REJECT |
| derived `proof[0].id` | canonical, forged | REJECT | REJECT |
| `proof[0].parents` | forged pair, canonical pair | ACCEPT; baseline stdout hash | REJECT |
| `proof[0].parents` | canonical pair, forged pair | REJECT | REJECT |
| source `clauses[0].literals` | `[999]`, canonical literals | ACCEPT; baseline stdout hash | REJECT |
| source `clauses[0].literals` | canonical literals, `[999]` | REJECT | REJECT |
| `proof[0].kind` | `affine`, canonical `factor` | ACCEPT; baseline stdout hash | REJECT |
| `proof[0].kind` | canonical `factor`, `affine` | REJECT | REJECT |
| `proof[12].row.mask` | malformed, canonical mask | ACCEPT; baseline stdout hash | REJECT |
| `proof[12].row.mask` | canonical mask, malformed | REJECT | REJECT |

The Python producer executed all twelve checker cases: six accepted, six rejected exactly as predicted; all twelve were rejected by Python's independent duplicate-pair hook. The separately authored Node verifier implemented its own recursive raw JSON scanner and made 31 assertions: all six last-canonical packets accepted with baseline stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`; all six reverse-order controls rejected; all twelve duplicate packets were rejected by the raw scanner.

This independently defeats F1-F4. It also shows the defect is not confined to numeric identifier aliasing `[P2-L5-415/416]`: it reaches source literals, rule tags, parents and affine evidence.

### Repair and hostile challenge

A sufficient repair for this recovered sublanguage must perform, in order:

1. strict raw parsing that rejects duplicate decoded member names before object construction;
2. canonical globally unique string IDs and exact reference matching (`[P2-L5-415/416]`);
3. exact affine-coordinate range projection/checking (`[P2-L5-414]`);
4. full original-source and rule authentication for every historical production, still OPEN.

JCS serialization after ordinary `JSON.parse` is insufficient because the losing member is already erased. I-JSON/JCS conformance must be enforced at ingestion. This repaired parser is a proposed distinct completion until historical authority is found; it does not silently revise $R_{\mathrm{mix341}}$.

## Work, evidence, span and machine-resource ledger

- **Logical distinct-node work:** unchanged at the original first-fixture 15 inference nodes for every accepted mutation; the test does not lower $W_R(F)$.
- **Explicit evidence bits:** compact baseline 77,713 bytes; mutants 77,729--77,747 bytes. The original preserved packet is 197,514 bytes. Duplicate bytes are parsed and then erased.
- **Construction/search:** producer deep-copies the packet, injects exactly one duplicate, writes a temporary packet and launches the exact checker once per case. Discovery cost is excluded from ideal $W_R$ but charged here as actual experiment work.
- **Verification:** Python run, including twelve checker launches, measured 1.552 s wall / 1.438 s user / 0.457 s system on this host. Independent Node run measured 1.501 s wall / 1.488 s user / 0.401 s system. These host figures are not FLMV-machine bounds.
- **Parsing/source/index/head/output:** every checker launch reads and parses the complete compact packet; raw strict parsers read the complete packet; output hashes and case ledgers are materialized. Temporary files are deleted after each case.
- **Peak space:** unavailable because `/usr/bin/time -v` is not installed; no peak-RSS claim is made. Packet copies, parser maps, child-process state and captured stdout coexist and must be charged in any implemented upper bound.
- **Work/span/schedule:** these independent cases are logically parallelizable, but the published scripts execute them sequentially. No weighted critical-path theorem or realizable same-machine parallel schedule is claimed.

## Status, artifacts and remaining gap

**Actual advance:** an accepted-byte, proof-critical raw-provenance counterexample for the exact recovered checker, plus an independently checked sufficient ingestion repair. Status is `COMPUTATIONAL/PROVED-RESTRICTED`: exact parser theorem plus finite execution on the recovered SOURCE/AND3/XOR checker.

**Not proved:** no satisfiable source is accepted; no proof is shortened; RES, RES-to-AND3, LOCAL-CONVERT, DEF facets, branching, assumption discharge and the full historical grammar remain unauthenticated. No all-rule minimum lower bound, B1/B2/B3 bridge, machine lower bound or P-versus-NP resolution follows.

Artifacts:

- `experiments/review/lspv5_417_duplicate_json_member_audit.py`, SHA-256 `2db840fea64e41bffaf6f3cbeee0d112449924243546dcf783ce8180f248dc80`.
- `experiments/review/verify_lspv5_417_duplicate_json_member.mjs`, SHA-256 `159a28fe7e62a8f21d82c5780a310c27bba99b623525b5cf53e83760d049d116`.
- `results/raw/review/2026-11-07_1348_LSPV5_DUPLICATE_JSON_MEMBER417.json`, SHA-256 `39a867cbd2a7a5d059780b4e3792634e3007aff4b37fb3661d893dde28fa8903`.

**Precise next gap:** recover a historically authorized complete parser, then test the same strict ingestion boundary across RES, LOCAL-CONVERT, DEF, branching and assumption-discharge records before attempting `[P2-C3]`; independently, `[P2-B1]` and `[P2-B2]` remain OPEN. **P versus NP remains OPEN.**
