# LSPV-5/484 — mathematically nonzero Resolution parents underflow to record zero

**Role:** LSPV-5 Independent Proof Red Team, historical Route B  
**Pacific timestamp:** 2026-11-11 02:51 PST  
**Status:** COMPUTATIONAL accepted-byte counterexample plus PROVED/RESTRICTED parameterized underflow lemma  
**Affected chain:** material evidence for `[P2-D1]`; it blocks an unqualified parsed-Number identity abstraction for `[P2-C3]`. `[P2-B1]` and separate `[P2-B2]/B3` remain OPEN. P versus NP remains OPEN.

## Outcome

The unchanged archived `/386` verifier accepts a Resolution parent written as the mathematically nonzero JSON decimal `1e-324` as positional parent zero. It likewise accepts `-1e-324` as negative zero. The baseline and hostile certificates have the identical verified outcome: 50 paid nodes, one charged DEF owner, 49 RES nodes, 69 records, 17 SOURCE records, 4,492 assertions, and identical model counts.

This is not merely another spelling of the mathematical integer zero. Before binary64 conversion, `1e-324` denotes the exact positive rational $10^{-324}$. ECMAScript JSON parsing first realizes the JSON number as an ECMAScript Number. Because

$$
10^{324} > 2^{1075},
$$

we have

$$
0 < 10^{-324} < 2^{-1075},
$$

where $2^{-1075}$ is half the least positive binary64 subnormal. Round-to-nearest, ties-to-even therefore maps $10^{-324}$ to $+0$ and $-10^{-324}$ to $-0$. The verifier then accepts the parsed value with `Number.isInteger(j) && j >= 0 && j < i` and dereferences `known[j]`. Both signed zeros select array property `"0"`.

Consequently, raw accepted bytes, exact JSON-decimal meaning, parsed Number identity, and positional proof-parent identity are four distinct layers. A sound byte-authenticated concrete semantics cannot silently identify them.

## IDEA — target and falsifiers stated before search

**Target claim.** After JSON parsing and the `/386` integer/bounds checks, every accepted Resolution-parent token denotes the same mathematical integer that it spells.

Precise falsifiers:

1. A positive token `1e-324` underflows to $+0$ and is accepted as parent zero.
2. A negative token `-1e-324` underflows to $-0$ and is accepted as parent zero.
3. A nearby nonzero subnormal such as `5e-324` incorrectly passes integer typing.
4. An overflow token such as `1e400` incorrectly reaches parent lookup.

Falsifiers 1 and 2 occurred. Controls 3 and 4 did not: both are rejected.

## SEARCH — authenticated inputs and literature

### Project inputs

- Archived `/386` verifier: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`.
- Exact shared baseline packet: `results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json`, Git blob `b9c1d306c300a3f1917ee01ecab16358ac77d4de`, SHA-256 `6272ffa2223cc426c2401d16d48919dcb5421a7e15490d97cc5cbc5f653b1527`.
- Mutation site: record 22, second parent, raw baseline `0` in `"parents":[16,0]`.
- Tracker readbacks: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; initial `proof2.txt` blob `20fd65cf8842d32a851a14a1496c7ea6156cb160`. The latter was refetched before the conflict-safe tracker write.
- Governance: `AGENTS.md` blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.

Current peer evidence read before the experiment included LSPV-1/568, LSPV-2/553, LSPV-3/566, LSPV-4/539, Grok's 2026-11-11 02:18 progress file, and Claude's world ledger. The relevant exact result is LSPV-1/568's 28-paid mathematical-core and 29-paid full-CLI upper bounds for guarded K4; this run independently executed its published Node reproducer and recovered the advertised core packet SHA-256 `fe36e3cba279fc6e20fcd6185e0e964034ef9259aae1caf8fb531e76007856f6` and CLI packet SHA-256 `c628ee7e8c77de308201c6717ccf5ed3d4ba0f5a9fabffebf5d765fba09df839`.

### Primary specifications

- ECMA-262 specifies `JSON.parse` and the ECMAScript Number type; Number values use IEEE-754 binary64 semantics: <https://tc39.es/ecma262/multipage/structured-data.html#sec-json.parse> and <https://tc39.es/ecma262/multipage/ecmascript-data-types-and-values.html#sec-ecmascript-language-types-number-type>.
- `Number.isInteger` delegates to `IsIntegralNumber`: <https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-number.isinteger>.
- RFC 8259's JSON number grammar permits exponent notation and warns that interoperability assumptions around binary64 limit exact agreement: <https://www.rfc-editor.org/rfc/rfc8259>.
- I-JSON gives the corresponding interoperability warning: <https://www.rfc-editor.org/rfc/rfc7493>.

Targeted project/repository searches found no R_mix341 grammar in `konard/p-vs-np` at `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `blkph0x/p-vs-np-proof-research` at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, or `meelgroup/frat-xor` at `18cd6bc17af10a9891c10a846ce966166f9fe0dc`. OpenAI GitHub search found a SAT-sparsification formalization in `openai/math`, not this native parser. Google Drive searches for `R_mix341 native calculus accepted byte` and `P2-D1 P2-C3 proof2` returned no files. These negative searches are not novelty evidence.

## ITERATE — proof and exact replay

### Parameterized lemma

**Lemma (restricted to ECMAScript JSON Number conversion).** For every integer $k\ge 324$, the exact JSON decimals $10^{-k}$ and $-10^{-k}$ convert respectively to ECMAScript Numbers $+0$ and $-0$.

**Proof.** Direct exact-integer comparison establishes $10^{324}>2^{1075}$. Therefore $10^{-324}<2^{-1075}$. For $k\ge324$, $0<10^{-k}\le10^{-324}<2^{-1075}$. The two adjacent nonnegative binary64 values at zero are $0$ and $2^{-1074}$, whose midpoint is $2^{-1075}$. Round-to-nearest, ties-to-even selects zero strictly below the midpoint. Sign preservation yields $-0$ for the negative values. QED.

This proof does not rely on finite testing. The script independently checks the load-bearing integer inequality using `BigInt`.

### Accepted family and controls

| Raw parent token | Parsed value | Verifier result | Same verified outcome |
|---|---:|---:|---:|
| `1e-324` | $+0$ | ACCEPT | yes |
| `1e-325` | $+0$ | ACCEPT | yes |
| `1e-400` | $+0$ | ACCEPT | yes |
| `1e-1000` | $+0$ | ACCEPT | yes |
| `1e-1000000` | $+0$ | ACCEPT | yes |
| `-1e-324` | $-0$ | ACCEPT | yes |
| `-1e-325` | $-0$ | ACCEPT | yes |
| `-1e-400` | $-0$ | ACCEPT | yes |
| `-1e-1000` | $-0$ | ACCEPT | yes |
| `-1e-1000000` | $-0$ | ACCEPT | yes |
| `5e-324` | least positive subnormal | REJECT | n/a |
| `1e-323` | positive subnormal | REJECT | n/a |
| `1e400` | $+\infty$ | REJECT | n/a |
| `"1e-324"` | string | REJECT | n/a |

The first positive hostile packet is 7,538 bytes with SHA-256 `ba64ceccfd859c756ea19ff76c94d26706b602897940f85e5331772e394f584d`. The first negative hostile packet is 7,539 bytes with SHA-256 `3b0837a4193e01cd2f8e4d6b94ec2f977eabe5f1954273839e665418f95e2077`. Canonical JSON reserialization maps the hostile parent to raw `0`, remains accepted, and produces 7,532 bytes with SHA-256 `88b3cd002eca90bd2bffe0dd1529c189fabddc28f523f507f1570a73df707826`.

### Why this is not spurious CEGAR behavior

The cheap path is concretely replayed by the unchanged archived verifier, not only by an independent model. CEGAR therefore may not remove it as spurious relative to that accepted language. A refinement may distinguish exact tokens, but a transformer that rejects them needs a proved coherent normalization theorem for every identifier occurrence, source hash, context, deletion reference, and cost identity in the intended full calculus.

### Concrete and abstract states

For the tested fragment, take a complete concrete state

$$
c=(B,P,i,K,G,C,Q),
$$

where $B$ is the exact input byte string; $P$ is the lossless token/parse trace; $i$ is the current record index; $K$ is the chronological record array; $G$ is the parent dependency DAG; $C$ is the cost ledger; and $Q$ contains verifier-control state and result counters. A Resolution step is admissible only after exact parsing, parent typing/range checks, parent retrieval, strict syntactic resolution, chronological insertion, ancestry/cost update, and all wrapper controls.

The tested parser abstraction

$$
\alpha_{\mathrm{num}}(B,P,i,K,G,C,Q)
=
(\operatorname{JSON.parse}(B),i,K,G,C,Q)
$$

forgets exact decimal meaning and raw token bytes. Its concretization $\gamma_{\mathrm{num}}(+0)$ includes raw `0`, `-0` after index coercion, and every positive `1e-k` with $k\ge324$; $\gamma_{\mathrm{num}}(-0)$ includes the negative family. If the abstract identity layer uses array-property lookup or SameValueZero, both signed-zero classes then select parent zero.

This is a sound MAY abstraction only for operational behavior of this particular verifier. It is not sound for the stronger property “same raw token” or “same exact mathematical JSON number.” Any P2-C3 abstraction claiming those properties must retain $B$ and a lossless decimal token domain or prove a normalizer. Conversely, rejecting the accepted family without a normalizer violates concrete-step inclusion.

### Resource polarity

- **Logical cost:** unchanged at 50 paid nodes. The counterexample does not lower $W_R(F)$.
- **Evidence bits:** token length grows with the exponent text; this is charged in packet bytes.
- **Verification time:** at least the input-token parsing work is charged; no unit-cost jump over the long exponent string is assumed.
- **Live peak space:** the script and verifier materialize complete strings/objects; measured process peak RAM was not collected, so no numerical space bound is claimed.
- **Lower-bound polarity:** configuration cardinality is not memory; proof-DAG work is not memory. This experiment supplies neither implication.
- **Abstraction cost:** a lower-bound-safe abstract proof cost must satisfy $\operatorname{cost}(P^\#)\le\operatorname{cost}_R(P)$ for every covered concrete proof. Charging the hostile spelling as an additional inference would reverse the required polarity.

### Repair lemma

For a positional parent field, a sufficient local repair is:

1. parse the raw JSON-number token with exact decimal arithmetic;
2. require exact mathematical integrality and $0\le j<i$ before any binary64 conversion;
3. serialize $j$ in one unsigned decimal notation; and
4. when raw provenance matters, reject rather than silently rewrite any noncanonical packet.

This local lemma does not establish a full-calculus normalizer. Complete repair still requires coherent treatment of identifiers, SOURCE hashes, parent references, deletion, contexts, branching/discharge, joins, freshness, LOCAL-CONVERT ports, paid owners/facets, and all accepted native rules.

## Reproducibility and resource ledger

- Executable: `experiments/review/lspv5_484_res_parent_binary64_underflow_audit.js`, 6,201 bytes, SHA-256 `d1c881aa8b237ee0b7d4e452b300482b942046c46b1a872427259b0403eb9302`.
- Raw result: `results/raw/arc/2026-11-11_0251_LSPV5_484_RES_PARENT_BINARY64_UNDERFLOW_RAW.json`, 5,470 bytes, SHA-256 `5cfb48559eae80ae74c99b87b8c059009aaf1f47fa0a265d5969d26513c0916a`.
- Construction/search: 15 hostile/control packet constructions; all complete packet bytes were materialized and parsed.
- Parsing: charged as actual Node JSON parsing; exact token checks use `BigInt` only for the symbolic inequality.
- Source/index/head reads: project governance, two trackers, issue #3, peer reports, current handoffs, Grok/Claude, required repository heads, and Google Drive searches were performed.
- Verification: each accepted/rejected case ran the unchanged `/386` verifier; outputs were compared structurally to baseline. This is an execution of the archived verifier, not a claim that it is the unidentified full historical R_mix341 checker.
- Output: report, executable, raw evidence, tracker delta, handoff, manuscript block, and issue comment are separately charged artifacts.
- Cache/retrieval/recomputation: baseline packet and checker were read from pinned blobs; hostile packets were regenerated rather than stored individually because the raw result records exact token, size, digest, parse sign, and acceptance.
- Failed policies: no failed search path was charged into the ideal proof minimum; negative Drive/repository results are only source-discovery evidence.
- Simultaneous peak space: not physically measured. The implementation holds the baseline text, one mutated text, parsed packet, verifier module state, and output object concurrently, so any later upper bound must include all of them.

The local checkout lacked root governance files during preflight; authenticated GitHub copies were read instead. This does not affect the executable result but prevents claiming a clean local whole-repository preflight.

## Classification and remaining gap

- **PROVED/RESTRICTED:** the exact underflow lemma for all $k\ge324$ under ECMAScript Number conversion.
- **COMPUTATIONAL:** unchanged archived `/386` verifier accepts all ten sampled hostile tokens and rejects all four controls.
- **OPEN:** authoritative complete historical R_mix341 accepted-byte grammar; full source-authenticated shared-DAG semantics; all-rule cost-sound abstraction; generalized lower bound P2-B1; separate noncircular P2-B2/B3.

This counterexample is material because `[P2-L5-483]` covered a token spelling the mathematical integer zero, whereas `[P2-L5-484]` covers an infinite family of exact, mathematically nonzero JSON decimals. It strengthens the repair requirement from “canonicalize signed zero” to “validate exact mathematical integrality before binary64 conversion.” It proves no semantic UNSAT error and no P-versus-NP result.

