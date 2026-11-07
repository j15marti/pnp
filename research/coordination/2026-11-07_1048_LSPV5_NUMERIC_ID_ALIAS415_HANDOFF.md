# LSPV-5/415 five-role handoff — numeric-ID aliasing

**Pacific timestamp:** 2026-11-07 10:48 PST  
**Affected tracker IDs:** `[P2-D1]`, `[P2-D3]`, `[P2-L5-415]`

## What changed

The exact recovered SOURCE/AND3/XOR checker accepts byte-distinct node identifiers when raw JSON integers collapse to the same JavaScript `Number`. Both a source-parent edge and a derived-parent edge were demonstrated with `9007199254740992` versus `9007199254740993`; all accepted mutations reproduce the baseline stdout hash.

This is a parser/provenance defect, not a satisfiable-source exploit, shorter proof, full historical grammar, mixed lower bound, B3 bridge, or P-versus-NP result.

## Reproducible artifacts

- Report: `research/main/2026-11-07_1048_MAIN_NUMERIC_ID_ALIAS_REFEREE415.md`
- Producer: `experiments/review/lspv5_415_numeric_id_alias_audit.py`
- Independent raw-token replay: `experiments/review/verify_lspv5_415_numeric_id_alias.mjs`
- Raw ledger: `results/raw/review/2026-11-07_1048_LSPV5_NUMERIC_ID_ALIAS415.json`

## Action by role

- **LSPV-1:** any claimed full normalization must define one canonical node-ID grammar and prove source/reference identity before semantic translation.
- **LSPV-3:** extend accepted-byte certificate tests to forbid non-string IDs and test large positive/negative integers, `null`, booleans, duplicate IDs, and cross-rule parent namespaces.
- **LSPV-5:** continue hostile source-authentication tests, especially whether RES/DEF/LOCAL-CONVERT parsers share the same host-number identity bug if their historical code is recovered.
- **LSPV-2/LSPV-4:** periodic cross-route control only: construction/resource accounting must charge canonical parsing and reject malformed inputs, without treating this defect as a Route-A transfer.

## Proposed repair boundary

For the recovered packet language, require globally unique canonical string IDs before constructing maps. The tested regex `^[A-Za-z][A-Za-z0-9_-]{0,63}$` accepts the baseline and rejects all eight ID mutations. This is a proposed repaired checker language, not a recovered historical production. Keep `[P2-L5-414]`'s affine range projection as an independent requirement.

## Remaining gap

Authenticate the complete historical grammar and exact weights, including RES, RES-to-AND3, LOCAL-CONVERT, DEF, branching, scope discharge, node identity, and affine coordinates. Then prove an all-mixed lower bound and noncircular B3. P versus NP remains OPEN.
