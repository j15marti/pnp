# LSPV-5/418: JSON escape aliases defeat raw-byte proof identity

**November 7, 2026, 14:48 PST | Route B independent red team | COMPUTATIONAL/PROVED-RESTRICTED | P versus NP OPEN.**

**Exact tracker IDs:** material evidence for `[P2-D1]` and `[P2-D3]`; new result `[P2-L5-418]`. Dependencies `[P2-C3]`, `[P2-B1]` and `[P2-B2]` remain OPEN. Historical $R_{\mathrm{mix341}}$ grammar, weights, roles, schedules and the two-Route-A/three-Route-B allocation are unchanged.

## IDEA: claim card and falsifiers fixed before search

**Target.** Falsify byte-level original-source and proof-node authentication in the exact recovered `/341` SOURCE/AND3/XOR checker after the proposed migration from numeric IDs to strings.

**Initial hypothesis.** The checker calls ECMAScript `JSON.parse` before constructing its source/proof `Map`s. Thus literal JSON string `"s0"` and byte-distinct `"\u0073\u0030"` become the same JavaScript string before definition/reference lookup; the same applies to derived ID `d0` and proof-critical member names. Equal-decoding aliases should accept with baseline output, while aliases decoding to `x0`, `jd` or `qarents`, and malformed escapes, should reject.

**Quantifiers/model.** There exists a byte-distinct valid JSON packet $J'$ for each of four proof-node definition/reference positions and two proof-critical member-name positions such that `JSON.parse(J')` equals the relevant checked value of baseline packet $J$, and the recovered checker accepts $J'$. Exact recovered checker SHA-256 `0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae`; exact 197,514-byte packet SHA-256 `12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`. No RES, LOCAL-CONVERT, DEF, branching or discharge rule is inferred.

**Falsifiers stated before search.** (F1) escaped/literal definition and reference aliases do not both pass; (F2) only object-key spellings pass while source/derived reference aliases fail; (F3) byte-distinct controls decoding to different strings also pass; (F4) an independent raw-token verifier cannot distinguish the spellings. All four were defeated by the experiment.

## SEARCH: continuity, primary specifications and repositories

### Project state actually read

- Complete `proof1.txt`, blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, and complete initial `proof2.txt`, blob `d327680c736d8e68435ff7fbc63ced3354a2dc65`.
- Historical governing handoff at required commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, file blob `033b54b87b7cbe94912af5cf67daa52859143a07`, and current same-path handoff blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; current issue #3 body. Issue-comment enumeration was retried twice and both calls ended with `Transport closed`; this is recorded as an access limitation, not disguised as review.
- `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`, and its complete red-team mode and research-protocol references. Root `main.tex` returned blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable bytes, so no whole-document or ownership-region rewrite was attempted.
- Current peers: LSPV-1/487 `research/agents/lspv-1/2026-11-07_1410_LSPV1_NONAFFINE_AFFINE_TEMPLATE487.md` blob `7cb31cd771808fb2accdc5c1c47ef4df63cfaee0`; LSPV-2/477 `research/agents/lspv-2/2026-11-07_1412_LSPV2_CYCLE_CUTSET477.md` blob `3b4e01f7218f523fd895e4f2178a93175d91989d`; LSPV-3/483 `research/agents/lspv-3/2026-11-07_1424_LSPV3_DEF_CYCLE_RANK483.md` blob `b94dcf1dad2aef841f7b885f7728e0deb4b41f6e`; LSPV-4/479 `research/agents/lspv-4/2026-11-07_1440_LSPV4_EXPANDER_BLOCK_TREE_FRONTIER479.md` blob `8d440937abdfa36c74f39790fbe4be588f0089f4`.
- Actual Grok file located from commit history: `GROKPROOF/2026-11-07_1330_PROGRESS.md`, blob `35ad4749b1d9779eadce95e46145b4eb103b8224`. Relevant Claude assessment: `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

The local workspace is an artifact subset and lacks the repository preflight script; the mandatory preflight command failed with file-not-found. The current skill and both references were nevertheless read completely from GitHub. This limitation does not affect exact local replay of the preserved checker and packet.

### Primary parser semantics

- [RFC 8259 sections 7 and 8.3](https://www.rfc-editor.org/rfc/rfc8259.html#section-8.3) permit any character to use a Unicode escape and specify comparison after transforming textual representations to Unicode code units. Its example explains why comparing unconverted escaped text is wrong.
- [ECMAScript `JSON.parse`](https://tc39.es/ecma262/multipage/structured-data.html#sec-json.parse) realizes JSON strings as ECMAScript strings. After parsing, `"s0"` and `"\u0073\u0030"` have identical code units.
- [RFC 8785 section 3.2.2.2](https://www.rfc-editor.org/rfc/rfc8785.html#section-3.2.2.2) gives one canonical serialization: printable non-control ASCII such as `s0`, `id` and `parents` is serialized as-is, not by optional Unicode escapes.

The search changed the repair statement: decoded string equality is correct semantic JSON behavior, so rejecting these packets is justified only when byte-canonical certificate identity is an explicit language requirement. The sufficient repair is a canonical raw packet grammar (or canonical reserialization equality check after a strict duplicate-preserving parse), not a claim that ordinary JSON equality should distinguish the values. Google-branded search was unavailable; indexed web search of authoritative specifications was used and logged.

### Required change-aware repository review

Both newly required repositories were unchanged: `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, with actual `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, with actual `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`. Both explicitly scope their proved items; neither authenticates historical $R_{\mathrm{mix341}}$.

Proof-format controls were read at pinned current heads: `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, text format blob `986a21aa92b62f844ef1fce852193142c41b2b1f` and tentative binary format blob `97bd0fed482ce1e95cdc112d9783f2da1ae58b71`; `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, README blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`. These are distinct explicit checker languages, not authority for `/341`. `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae` README blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, `eth/Challenge.lean` blob `6297ab1398884550253bdd1475704729d02ce89b` explicitly contains `sorry` placeholders. Repository titles, builds and manifests are not P-versus-NP proofs.

## Established-family/theorem/encoding/known-method ledger

| Family | Exact 3-CNF/source size | Established theorem/model | Known legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | One edge variable per edge; each degree-three parity equation is its four proper signed 3-clauses excluding the wrong parity. For $H$ vertices: $3H/2$ variables, $4H$ clauses, $N=\Theta(H\log H)$ bits | Ben-Sasson--Wigderson 2001 gives $2^{\Omega(H)}$ ordinary shared-DAG Resolution size on expanders. This is proof-size hardness in Resolution | GF(2) summation is a linear upper control; the recovered fixtures use SOURCE/AND3/XOR derivations | Authenticate and lower-bound every historical legal mixed shortcut, or prove a source-retracting simulation |
| Random proper strict 3-CNF $\mathcal F(n,3,8n)$ | $n$ variables, $8n$ width-three clauses, $N=\Theta(n\log n)$ | Pang 2026 Theorem 7.2(a), reported exponential minimum in the stated syntactic Res(XOR) model with high probability | Paid extension variables, mixed rules and shared DAGs are mandatory controls | No full historical mixed-calculus transfer |
| Pigeonhole principles | Standard PHP source; no strict-3CNF encoding is assumed here | Haken exponential ordinary-Resolution lower bound | Extended Resolution is stronger; equisatisfiability alone preserves no lower bound | Need exact 3-CNF encoding and proof-to-proof preservation theorem |

The focused packets below mutate the existing certified-UNSAT K4 Tseitin fixture. They are parser/provenance controls, not new candidate hard formulas.

## ITERATE: exact accepted-byte aliases

### Restricted theorem and experiment

For any valid JSON string token $t$, `JSON.parse(t)` yields its decoded Unicode string. Therefore a checker that authenticates IDs and member names only after ordinary parsing cannot distinguish two byte strings with the same decoded string. This statement is exact under the declared parser model; whether the certificate language intends raw-byte canonical identity is a separate historical grammar question.

Thirteen packets were generated by changing exactly one raw token in the compact baseline:

| Mutation position | Raw token | Decoded value | Checker |
|---|---|---|---:|
| source `clauses[0].id` definition | `"\u0073\u0030"` | `s0` | ACCEPT |
| source `proof[0].parents[0]` reference | `"\u0073\u0030"` | `s0` | ACCEPT |
| derived `proof[0].id` definition | `"\u0064\u0030"` | `d0` | ACCEPT |
| derived `proof[1].parents[0]` reference | `"\u0064\u0030"` | `d0` | ACCEPT |
| member name for source ID | `"\u0069\u0064"` | `id` | ACCEPT |
| member name for parents | escaped `parents` | `parents` | ACCEPT |
| same four ID locations | escaped `x0` | `x0` | all REJECT |
| source member name | escaped `jd` | `jd` | REJECT |
| parents member name | escaped `qarents` | `qarents` | REJECT |
| source ID | `"\uZZZZ"` | invalid JSON | REJECT |

All six equal-decoding packets reproduced the baseline checker-output SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`. The Python audit obtained 6 accepts and 7 rejects exactly as predicted. The separately authored Node implementation rebuilt all mutations, independently tokenized every JSON string, required each raw token to equal `JSON.stringify(JSON.parse(token))`, made 34 assertions, and rejected all 13 mutated packets as noncanonical or malformed. This defeats F1--F4.

### Revised claim and weakest repair

The initial phrase “string IDs repair identity” was too strong. **Revised claim:** canonical globally unique string IDs repair the numeric alias defects `[P2-L5-415/416]` only if the certificate language also fixes a canonical raw serialization. Plain JSON strings repair numerical rounding but still admit byte aliases.

A sufficient proposed ingestion stack for the recovered sublanguage is:

1. parse raw bytes while rejecting duplicate decoded member names (`[P2-L5-417]`);
2. reject any packet whose every raw JSON string token is not its prescribed canonical serialization (`[P2-L5-418]`), or canonicalize before signing/comparing bytes while binding the canonical bytes;
3. require globally unique canonical string IDs with exact decoded reference matching (`[P2-L5-415/416]`);
4. validate affine coordinate domains (`[P2-L5-414]`);
5. authenticate every historical rule and original-source production, still OPEN.

This is a proposed repaired checker language, not a silent revision of historical $R_{\mathrm{mix341}}$. If historical semantics intentionally identify all JSON-equivalent spellings and authenticate only decoded objects, the accepted equal-decoding cases are not a soundness bug; they instead prove that raw-byte provenance/signature claims require an extra canonicalization rule.

## Work, evidence, span and machine-resource ledger

- **Logical work:** all accepted variants retain the same 15 distinct inference nodes and output hash. No $W_R(F)$ decrease was shown.
- **Explicit evidence:** compact baseline 77,713 bytes; equal/different ID and `id`-key variants 77,723 bytes; `parents`-key variants 77,748 bytes; malformed control 77,717 bytes. Preserved historical packet: 197,514 bytes.
- **Construction/search:** Python deep-copies the parsed packet, inserts one raw token, materializes a temporary file and launches the exact checker per case. Discovery/search is excluded from ideal $W_R$ but charged in this actual experiment.
- **Verification and output:** Python producer: 13 checker cases, 2.1019 s wall, measured peak process-tree RSS 12,952 KiB. Independent Node replay: 34 assertions/13 cases, 1.8821 s wall, measured peak process-tree RSS 51,480 KiB. Sampling used `/proc` at 2 ms and can undercount short-lived peaks; values are host measurements, not FLMV bounds.
- **Parsing/source/index/head reads:** each checker launch reads and parses the complete compact packet, builds source/proof maps, and captures output; the strict verifier scans all raw string tokens. Temporary files are deleted after each case.
- **Storage/retrieval/recomputation:** producer 7,446 bytes, independent verifier 4,182 bytes, raw ledger 10,398 bytes, plus packet/checker copies and child-process state. Cases are recomputed sequentially; no cache-based asymptotic claim is made.
- **Work/span/schedule:** cases are independent and could run in parallel, but published scripts run sequentially. No weighted critical-path theorem, parallel-reference pricing, or same-machine realizable schedule is claimed.

## Status, artifacts and remaining gap

**Actual advance:** exact equal-decoding definition/reference/key accepted-byte witnesses and a canonical raw-token repair for the recovered SOURCE/AND3/XOR parser. Status `COMPUTATIONAL/PROVED-RESTRICTED`: exact parser lemma plus finite recovered-checker execution.

**Independent challenge:** decoded string equality is standard JSON semantics. The result establishes a gap only for raw-byte certificate identity/provenance, not logical object identity. No satisfiable source was accepted, no proof shortened, and no established hard-family lower bound moved across a mixed rule.

Artifacts:

- `experiments/review/lspv5_418_json_string_escape_alias.py`, SHA-256 `5f591d9cdc97f267795d707bc7d563639d9864c4e8d9dfdd9766681fc20bcf65`.
- `experiments/review/verify_lspv5_418_json_string_escape_alias.mjs`, SHA-256 `00398a58058ccd9a970e1e0b151337d7db2d5b8d7621373ac548a464aca845d3`.
- `results/raw/review/2026-11-07_1448_LSPV5_JSON_STRING_ESCAPE_ALIAS418.json`, SHA-256 `62fae98d16c940a72a5c7834151d5e47391df3dd426598102043aeaf9260facb`.

**Precise remaining gap:** recover a historically authorized complete parser and decide whether certificate identity is raw-canonical or decoded-object identity; then test RES, LOCAL-CONVERT, DEF, branching and assumption-discharge records before attempting `[P2-C3]`. Independently, full mixed lower bound `[P2-B1]` and noncircular B3 `[P2-B2]` remain OPEN. **P versus NP remains OPEN.**
