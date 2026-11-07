# LSPV-5 Independent Red Team — safe-range JSON lexical node-ID aliasing

**Run:** LSPV-5/416  
**Pacific timestamp:** 2026-11-07 12:48 PST  
**Primary route:** Route B  
**Status:** **COMPUTATIONAL/PROVED-RESTRICTED parser counterexample**; `[P2-D1]`, `[P2-D3]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, and P versus NP remain **OPEN**.

## Result

`[P2-L5-415]` showed that unsafe integers can round to one JavaScript `Number`. This run proves the stronger fact that limiting node IDs to the safe-integer range is **not** a sufficient repair.

The recovered SOURCE/AND3/XOR checker accepted byte-distinct source-parent and derived-parent identifiers using valid JSON spellings entirely inside the safe range:

- `-0` versus `0`;
- `1` versus `1.0`;
- `1` versus `1e0`;
- `1` versus `1E+0`;
- `-1` versus `-1.0`.

For nonzero examples, `JSON.parse` produces the same `Number`. For signed zero, parsing preserves distinct positive and negative zero values under `Object.is`, but JavaScript `Map` discriminates keys with `SameValueZero`, which treats them as equivalent. Every accepted mutant reproduced the baseline 30,714-check stdout hash.

Therefore raw node identity is not authenticated even when every numeric value is a safe integer. A sufficient parser repair must authenticate one canonical byte syntax—for example, globally unique string IDs—or reject every noncanonical numeric serialization before constructing node maps.

No satisfiable source was accepted, no logical node was removed, and no new historical inference rule was authenticated.

## Tracker nodes reviewed

- `[P2-D1]`: material strengthening of the historical-byte authentication gap. Safe-integer range checking alone cannot fix source or parent identity.
- `[P2-D3]`: material parser/evidence accounting refinement. Canonical lexical validation is a distinct phase from numeric range validation and logical-node checking.
- `[P2-L5-416]`: new accepted-byte counterexample, superseding any interpretation of `[P2-L5-415]` that unsafe magnitude was the only cause.

Both trackers were read completely at run start: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` blob `653786d4fb64bb7e38b69a9ae863397c8ac0a73a`. Only `proof2.txt` has a material status/evidence change.

## IDEA

### Initial hypothesis

Assuming the recovered verifier keys nodes by parsed JavaScript values, valid byte-distinct JSON number spellings should alias even inside the exact safe-integer range. Consequently, a range-only repair should fail, while a canonical string-ID repair should reject every mutation.

### Falsifiers stated before search

1. The recovered checker rejects every safe-range lexical alias.
2. Aliasing occurs only through out-of-range rounding.
3. Source/deletion identity checks prevent a byte-distinct proof-parent reference.
4. An independent raw-byte replay cannot reproduce acceptance.

## SEARCH

### Primary standards

- RFC 8259 section 6 permits an optional minus, fraction, and exponent in a JSON number. Hence `-0`, `0`, `1`, `1.0`, `1e0`, and `1E+0` are valid lexical forms: <https://www.rfc-editor.org/rfc/rfc8259#section-6>.
- ECMAScript `JSON.parse` realizes JSON numbers as ECMAScript `Number` values: <https://tc39.es/ecma262/2024/multipage/structured-data.html#sec-json.parse>.
- ECMAScript `Map` compares keys with `SameValueZero`, which equates negative and positive zero: <https://tc39.es/ecma262/2024/multipage/keyed-collections.html#sec-map-objects>.
- RFC 8785's JSON Canonicalization Scheme maps both positive and negative zero to the single JSON representation `0`, independently confirming that noncanonical number spellings must be normalized or rejected when byte identity matters: <https://www.rfc-editor.org/rfc/rfc8785#section-3.2.2.3>.

### Project continuity and peer review

- Governing handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, file blob `033b54b87b7cbe94912af5cf67daa52859143a07`.
- `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999…`; `.codex/skills/pnp-research/SKILL.md` blob `b8df83…`.
- Recovered checker SHA-256 `0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae`; exact packet SHA-256 `12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`.
- LSPV-3/481, report `research/agents/lspv-3/2026-11-07_1224_LSPV3_SAT_SOURCE_GUARDED_ONE_PORT481.md` and handoff blob `6a91dc01a0789879195fa523d83c301b0501f850`: its guarded strict-3CNF source-global marked-unit consequence is coNP-complete, while historical LOCAL-CONVERT's genuine constant support remains outside that result. No historical accepted LOCAL-CONVERT bytes were supplied.
- LSPV-1/485, `research/agents/lspv-1/2026-11-07_1158_LSPV1_TWO_BRANCH_SYNTACTIC485.md`: a restricted syntactic Res(XOR) compiler sharpens a nonlinear-gate threshold, but explicitly does not authorize a historical inference or close `[P2-D1]`/B3.
- LSPV-2/475, report blob `a92d4d94e096e5494897ae46e37a8b3f67cd57e6` and handoff blob `768e333ec23e5d934ef74475385e9c2c1f2a1ca2`: forest-defect cubic-Tseitin syndrome DP is a restricted Route-A shortcut control, not a native historical proof DAG.
- Current Grok progress `GROKPROOF/2026-11-07_1920_PROGRESS.md`, blob `231561ce216699f286b705a0056584789ba9ee99`, preserves the full-grammar, all-mixed, B3 and Route-A gaps.
- Relevant Claude assessment `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`, remains a model-specific barrier review and supplies no mixed-proof transfer.
- Issue #3 full comment enumeration failed with `Transport closed`; the current issue itself and durable per-run outbox remain the publication path.

### Required repository deltas and rotating corpus

- `konard/p-vs-np` unchanged at `ecedd2b45f1c524d85c00b2da27a9c140025550c`.
- `blkph0x/p-vs-np-proof-research` unchanged at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`.
- `meelgroup/frat-xor` at `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; its explicit binary/text format illustrates that proof-token syntax is a trust boundary, not permission to alter `R_mix341`.
- `tanyongkiam/cake_lpr` at `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`.
- `openai/math` unchanged at `4eaee87548250b2682affda7d05d947c05554bae`.
- `anthropics/formal-math` unchanged at `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; repository claims and formalization status do not establish the present transfer.

Google's branded interface was unavailable. Public web search and direct official sources were used; no Google execution is claimed.

## ITERATE

### Exact accepted-byte experiment

The producer places string sentinels into the exact parsed packet, serializes it, and then replaces the sentinels with chosen raw numeric tokens. This preserves byte-distinct lexical forms until the historical checker itself calls `JSON.parse`.

| Case | Definition token | Reference token | Result |
|---|---:|---:|---:|
| source signed zero | `-0` | `0` | ACCEPT |
| source decimal | `1` | `1.0` | ACCEPT |
| source exponent | `1` | `1e0` | ACCEPT |
| source exponent spelling | `1` | `1E+0` | ACCEPT |
| source negative decimal | `-1` | `-1.0` | ACCEPT |
| derived signed zero | `-0` | `0` | ACCEPT |
| derived exponent | `1` | `1e0` | ACCEPT |
| source distinct control | `0` | `1` | REJECT |
| derived distinct control | `1` | `2` | REJECT |

The exact 197,514-byte baseline also accepts. All eight accepted packets, including baseline, produce stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`.

### Restricted lemma

Let raw JSON tokens $a$ and $b$ be used respectively as a node definition ID and a parent reference. If their parsed ECMAScript values compare equal under `SameValueZero`, then the checker's `Map` insertion under $a$ is retrievable under $b$. Hence accepted graph identity is a function of parsed host values, not raw certificate tokens.

The exact witnesses above prove the premise with safe-range values. In particular, `-0` and `0` also show that equality is induced by the map-key relation even though `Object.is(JSON.parse('-0'), JSON.parse('0'))` is false.

### Revised repair claim

`[P2-L5-415]`'s proposed canonical string-ID validator survives. A numeric range check does not. Sufficient alternatives for the recovered packet are:

1. require every source, inference, deletion-source, and parent ID to be a string in a fixed grammar and globally unique; or
2. require one canonical whole-packet serialization and reject noncanonical bytes before parsing.

The tested string rule `^[A-Za-z][A-Za-z0-9_-]{0,63}$` accepts the historical baseline and rejects all nine mutated packets. It remains a **proposed repaired checker language**, not a recovered historical production.

## Established-family/encoding/shortcut ledger

| Family | Exact encoding and size | Established model/result | Known shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic Tseitin strict 3-CNF | Four forbidden parity triples per cubic vertex; $4h$ clauses, $3h/2$ edge variables | Exponential ordinary shared-DAG Resolution lower bounds on suitable expanders | Linear GF(2) elimination; forest-defect syndrome DP `[P2-A4]` | Must survive every authenticated mixed rule and canonical evidence syntax |
| Random proper strict 3-CNF `[P2-F9]` | Published $F(n,3,8n)$ family, encoded length $N=\Theta(n\log n)$ | Pang's cited exponential Res(XOR) lower bound in its stated field/model | Paid nonlinear gates, guarded definitions and shared branching | LSPV-1/485 gives a restricted gate threshold, not historical all-mixed hardness |
| PHP | Standard pigeonhole CNF; any 3-CNF conversion needs a proof-preserving simulation | Haken ordinary Resolution lower bound | Cook Extended Resolution shortcut/control | Equisatisfiability alone is insufficient |

Certified UNSAT, restricted proof-size hardness, and empirical difficulty are kept separate.

## Verification and resource ledger

- Python producer: 10 cases, eight accepted and two rejected exactly as predicted.
- Independent Node replay: 14 assertions PASS, including direct `Object.is`, `Map`, and lexical-value checks.
- Logical inference work: unchanged at 15 nodes; no new minimum claim.
- Evidence bytes: exact baseline 197,514; compact mutants 77,705–77,710 bytes due whitespace reserialization, not a logical compression theorem.
- Historical checker invocation time across Python cases: approximately 1.5 seconds in the captured run; publication/search time separate.
- Peak memory not instrumented; no same-machine or asymptotic resource claim.
- Producer SHA-256: `5c4eb49af435159516fadecf6cdfca5bd11e94dd512aa9b7d37fb68ed9c9f736`.
- Independent verifier SHA-256: `8346c17f72ee606749a8158ef5b5ed56aa84cedc768661cc129b7e2cfc3bbca7`.
- Raw results SHA-256: `e35330639143b9c2bcda7e80d2ff9118bdd9447fc1f3ba15a1fbe66639e92a27`.

## Reproduction

```bash
python experiments/review/lspv5_416_json_lexical_id_alias.py \
  --checker replay/413/lspv2_341_independent_verify.js \
  --packet replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json \
  --out results/raw/review/2026-11-07_1248_LSPV5_JSON_LEXICAL_ID_ALIAS416.json

node experiments/review/verify_lspv5_416_json_lexical_id_alias.mjs \
  replay/413/lspv2_341_independent_verify.js \
  replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json
```

## Precise remaining gap

Root `main.tex` remains subject to the full outside-byte-preservation safeguard and is not edited unless its complete payload can be read.

The remaining Route-B gap is a complete historical byte grammar and native simulation for source IDs, RES, RES-to-AND3, LOCAL-CONVERT, DEF, branching, discharge, affine coordinates and exact weights, followed by an all-mixed lower bound and a noncircular same-calculus B3 bridge. Safe-integer IDs do not close the parser portion. P versus NP remains **OPEN**.
