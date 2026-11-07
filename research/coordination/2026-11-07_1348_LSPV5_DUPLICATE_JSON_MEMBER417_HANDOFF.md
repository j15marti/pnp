# LSPV-5/417 five-role handoff: duplicate JSON member provenance

**2026-11-07 13:48 PST | Route B | `[P2-D1]`, `[P2-D3]`, `[P2-L5-417]` | COMPUTATIONAL/PROVED-RESTRICTED | P versus NP OPEN.**

The exact recovered `/341` JavaScript checker uses `JSON.parse`, whose duplicate-name semantics retain the last member. Six proof-critical last-canonical mutations (`id`, derived `id`, `parents`, source `literals`, `kind`, affine `mask`) were accepted with the baseline checker-output hash; the reverse order exposed the forged value and rejected. Two independent strict raw parsers rejected all twelve duplicate packets.

This is stronger than numeric-ID aliasing: arbitrary raw proof-critical bytes can be erased before checking. A sufficient recovered-sublanguage repair must reject duplicate decoded member names before object construction, then enforce canonical string IDs and affine-coordinate ranges. Post-parse canonicalization is too late. Treat this as a proposed repaired parser, not a silent historical grammar revision.

Artifacts: `research/main/2026-11-07_1348_MAIN_DUPLICATE_JSON_MEMBER_REFEREE417.md`; `experiments/review/lspv5_417_duplicate_json_member_audit.py`; `experiments/review/verify_lspv5_417_duplicate_json_member.mjs`; `results/raw/review/2026-11-07_1348_LSPV5_DUPLICATE_JSON_MEMBER417.json`.

Next: authenticate the complete historical parser and repeat strict-ingestion tests on RES, LOCAL-CONVERT, DEF, branching and assumption discharge. `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. No satisfiable source, shorter proof or P-versus-NP result was obtained.
