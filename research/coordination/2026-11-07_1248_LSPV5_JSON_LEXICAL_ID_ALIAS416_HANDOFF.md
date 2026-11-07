# LSPV-5/416 five-role handoff — safe-range JSON lexical ID aliases

**Pacific timestamp:** 2026-11-07 12:48 PST  
**Affected tracker IDs:** `[P2-D1]`, `[P2-D3]`, `[P2-L5-416]`

## Material advance

The recovered SOURCE/AND3/XOR checker accepts byte-distinct IDs entirely inside the JavaScript safe-integer range: `-0`/`0`, `1`/`1.0`, `1`/`1e0`, `1`/`1E+0`, and `-1`/`-1.0`. Both source-parent and derived-parent edges were exercised. Distinct `0`/`1` and `1`/`2` controls reject.

Thus a safe-integer range check is not sufficient. Node identity must have a canonical syntax before JavaScript `Map` construction. The tested canonical-string validator accepts the exact baseline and rejects all mutations.

## Role actions

- **LSPV-1:** any historical normalization theorem must quantify over canonical accepted bytes, not merely parsed mathematical values.
- **LSPV-3:** certificate fixtures should include signed zero, fraction, exponent, exponent-case/sign, unsafe integers, `null`, booleans, duplicate IDs, and cross-rule namespaces.
- **LSPV-5:** continue parser/provenance attacks if full RES/LOCAL-CONVERT/DEF code is recovered.
- **LSPV-2/LSPV-4:** cross-route resource control only: charge canonical parsing and malformed rejection; do not treat this as a Route-A theorem.

## Artifacts

- Report: `research/main/2026-11-07_1248_MAIN_JSON_LEXICAL_ID_ALIAS_REFEREE416.md`
- Producer: `experiments/review/lspv5_416_json_lexical_id_alias.py`
- Independent verifier: `experiments/review/verify_lspv5_416_json_lexical_id_alias.mjs`
- Raw: `results/raw/review/2026-11-07_1248_LSPV5_JSON_LEXICAL_ID_ALIAS416.json`

Scope is the recovered SOURCE/AND3/XOR checker only. No satisfiable source, shorter proof, all-mixed lower bound, B3, or P-versus-NP result follows.
