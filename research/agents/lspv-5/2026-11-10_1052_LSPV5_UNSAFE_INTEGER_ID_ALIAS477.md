# LSPV-5/477 — unequal accepted bytes alias one proof identifier

**Pacific timestamp:** 2026-11-10 10:52 PST  
**Role:** LSPV-5 Independent Proof Red Team (historical Route B label retained)  
**Status:** **COMPUTATIONAL ACCEPTED-BYTE COUNTEREXAMPLE** plus **PROVED/EXACT parser-alias lemma**  
**Tracker impact:** material `[P2-L5-477]` under `[P2-D1]`; `[P2-C3]` and `[P2-B1]` remain open; `[P2-B2]`/B3 remain separate.  
**Global status:** P versus NP remains **OPEN**.

## 1. IDEA: target and falsifiers stated before search

Target claim: the pinned LSPV-2/341 JSON verifier authenticates native proof identifiers and parent provenance at the accepted-byte level strongly enough to serve as a concrete component of P2-D1.

Precise falsifiers:

1. two unequal raw numeric identifier lexemes are parsed as the same identifier and accepted;
2. a mismatched source hash, parent type, or branch context is accepted;
3. a repeated-input or tautological defining facet creates an uncharged accepted shortcut;
4. the available verifier is not the authoritative full historical `R_mix341` checker or omits accepted native transitions.

Falsifiers 1 and 4 occurred. The available pinned verifier accepts the first hostile file below, while its grammar covers only its encoded SOURCE/Tseitin, AND3, and XOR checks rather than the complete historical rule inventory.

## 2. Governing state and exact corpus read

This run read the current `proof1.txt`, `proof2.txt`, issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, the current five-role handoffs, and actual role artifacts. In particular it reviewed LSPV-1/552, LSPV-2/536, LSPV-3/539, 543, 544, 546, 547, 548 and 549, LSPV-4/522, the previous LSPV-5/476, the current Grok progress artifact, and the Claude one-tape artifact. Google Drive search for `PNP R_mix341 proof2` found no matching artifact; GitHub was therefore the canonical source.

The pinned code and baseline were read from:

- `experiments/review/2026-11-07_2219_native_core_audit/historical/lspv2_341_mixed_tseitin_min_dag_native_verifier.mjs` (Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`);
- `experiments/review/2026-11-07_2219_native_core_audit/baseline/341_mixed_tseitin_min_dag.json` (Git blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`).

The local replay copies had SHA-256 values `b7d01c7390cad6ac7da7ce5ff5af68b31a0ba70375ace06e677a8ec9ac913834` and `0f4f92b84f0c8c74b0df1ef41d190493ec71465692e65ce504d193665fc520c2`, respectively.

## 3. SEARCH: sources and scope controls

The search included the primary Abstract Interpretation starting point (Cousot and Cousot), Abstract Conflict-Driven Learning and Abstract Satisfaction, RFC 8259's JSON number interoperability condition, FRAT/FRAT-XOR formats, CakeLPR, and current required repositories `konard/p-vs-np` and `blkph0x/p-vs-np-proof-research`. FRAT-XOR uses explicit positive-integer identifiers and typed instruction namespaces; CakeLPR supplies a formally verified checker for its own specified format. Neither establishes the historical `R_mix341` accepted-byte grammar.

RFC 8259 states exact interoperable agreement for integer numbers only in the range $[-(2^{53})+1,(2^{53})-1]$. This is directly relevant because the pinned verifier uses JavaScript `JSON.parse` and then JavaScript `Map` keys without a safe-integer or canonical-lexeme check.

Repository review did not locate an authoritative full checker that simultaneously authenticates SOURCE, oriented Resolution, AND3, GF(2), LOCAL-CONVERT, paid DEF facets, freshness, exported/private wires, branching, weakening, contexts/discharge/joins, and deletions under the fixed historical weights. Therefore this report does not promote the pinned subset verifier into that missing authority.

## 4. ITERATE: accepted hostile certificate

The audit makes only two textual substitutions in the accepted baseline:

1. the first definition identifier, originally JSON string `"d0"`, becomes the raw JSON number token `9007199254740993`;
2. its unique later parent reference becomes the *different* raw token `9007199254740992`.

The tokens have different bytes. Nevertheless Node's `JSON.parse` maps both to the same binary64 number `9007199254740992`. The verifier indexes the definition in a `Map` by that parsed number and later resolves the unequal parent token to the same key.

| Replay | Definition token | Parent token | Outcome |
|---|---:|---:|---|
| Baseline | `"d0"` | `"d0"` | accepted, 30,714 checks |
| Hostile alias | `9007199254740993` | `9007199254740992` | **accepted, 30,714 checks** |
| Safe-number mismatch control | `9007199254740991` | `9007199254740990` | rejected |
| String mismatch control | `"9007199254740993"` | `"9007199254740992"` | rejected |

The baseline and hostile verifier stdout were byte-identical, SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`. The hostile certificate SHA-256 is `bc3dd21b05efff0d236a9b519981a4b1d2a7dd2ba8b4b53f572aadcbbf4bc10e`.

### Exact lemma

Let a verifier parse JSON into JavaScript values, accept arbitrary JSON numbers as proof identifiers, and use the parsed value as a `Map` key. Then raw-byte identifier authentication fails: there exist distinct legal JSON number lexemes $a\ne b$ such that `JSON.parse(a) === JSON.parse(b)`, so a definition keyed by $a$ can be referenced by $b$. The displayed pair is an explicit witness.

This is a parser/provenance equality failure, not merely a cosmetic serialization discrepancy: the verifier accepts a parent reference whose raw identifier bytes were never defined.

## 5. Abstract-interpretation consequence

A concrete accepted-byte configuration must retain at least

$$
C=(B,\,i,\,\Gamma,\,D,\,G,\,w,\,\mu),
$$

where $B$ is the authenticated source/certificate byte string, $i$ is the parser position, $\Gamma$ is the assumption context, $D$ is the exact identifier-to-node environment, $G$ is the typed shared proof DAG, $w$ is accumulated distinct-node cost, and $\mu$ is live verifier state. The abstraction used for provenance cannot erase the relation between an identifier's raw lexeme/span and its semantic key.

The map

$$
\alpha_{\mathrm{num}}(\ell)=\operatorname{Number}(\ell)
$$

is many-to-one on accepted JSON numeric lexemes and is therefore not provenance-reflecting. If abstract nodes or count-once costs are keyed only by `Number`, distinct concrete byte coordinates can be merged. That invalidates any P2-D1 claim requiring exact source authentication and can also corrupt P2-C3 cost accounting by collapsing supposed distinct identities.

CEGAR cannot discard the discovered path as spurious: it replays successfully in the pinned checker. Rejecting it requires a parser/grammar repair, not merely abstract refinement.

### Conditional repair lemma

If identifiers are restricted to canonical strings compared byte-for-byte, or to canonical decimal lexemes parsed as `BigInt` with an injective serialization check, and every parent lookup retains the authenticated source span, this particular alias is rejected. LSPV-3/549's test-only grammar uses canonical string identifiers, which independently demonstrates the repair pattern. It does **not** prove that the historical calculus had that rule. Adopting it without historical authority would define a repaired calculus rather than authenticate `R_mix341`.

## 6. Independent peer replays

All available peer programs were rerun from their published source, without treating their reimplementations as the historical authority:

- LSPV-1/552: 57,337 enumerated cases and 11 controls; regenerated JSON exactly matched published blob `93059a...`.
- LSPV-2/536: 1,530 cases and six malformed controls passed; aggregate published values were consistent.
- LSPV-3/549: K4 127 records/63 paid CASE nodes, shared instance 18/8, ten corruption and four malformed controls; regenerated JSON exactly matched published blob `b3d488...`.
- LSPV-4/522: 80 canonical clauses, 3,160 pairs and 80 duplicate controls plus the published graph model counts; aggregate values were consistent.

These reproduce the reported finite/test-only claims at their stated scope. None supplies the missing complete historical grammar.

## 7. Classification and node impact

- **Family failure:** not tested; hard-family testing is premature until all native shortcuts are admitted.
- **P2-D1:** **material failure for the pinned LSPV-2/341 verifier's byte-authentication use**. The complete historical grammar remains open.
- **P2-C3:** remains **OPEN**. No cost-sound abstraction may inherit numeric-key identity without repairing/authenticating it.
- **P2-B1:** remains **OPEN**, dependent on D1 and C3 closure.
- **P2-B2/B3:** unchanged and separate.
- **P versus NP:** **OPEN**.

Any earlier phrase suggesting “native accepted-byte authentication” from this 341 verifier must be qualified: it is acceptance by a pinned independent semantic verifier on parsed JSON values, not authentication of raw proof identifier bytes and not validation of the full historical rule inventory.

## 8. Resource ledger

The hostile run used Node v24.22.1, Python 3.12.14 and Linux. The accepted mutant is 197,538 bytes; the published audit source is 4,488 bytes; the raw summary is 1,744 bytes. The verifier performed 30,714 checks on both baseline and mutant. Parsing, mutation construction, verifier subprocess output, hashing and the two negative controls were charged in the executable audit. This is a finite accepted-byte parser counterexample; it is not a proof-DAG work lower bound or a machine-space theorem.

The local repository was not available as a git checkout, so `.codex/skills/pnp-research/scripts/preflight.sh` could not be executed. The run instead used current GitHub blobs, exact SHA-pinned reads, conflict-safe Contents API updates, and post-write full readback. This limitation is not disguised as a successful local preflight.

## 9. Advance and remaining gap

**Actual advance:** an independently executable, accepted hostile certificate proves that the pinned LSPV-2/341 verifier conflates two unequal proof-ID byte strings. This defeats using that parser, unchanged, as P2-D1's raw source/provenance authentication layer.

**Precise remaining gap:** locate and authenticate the actual historical full `R_mix341` byte grammar and checker for every accepted operation, or establish by historical evidence that a canonical injective identifier grammar was fixed. Only then can a full concrete-step inclusion proof and cost-nonincreasing shared-DAG abstraction be attempted for P2-C3 and transferred toward P2-B1.

TRACKERS REVIEWED; MATERIAL CHANGE `[P2-L5-477]`.
