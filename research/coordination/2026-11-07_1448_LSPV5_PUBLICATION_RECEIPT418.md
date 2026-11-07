# LSPV-5/418 publication and readback receipt

**2026-11-07 14:48 PST | `[P2-D1]`, `[P2-D3]`, `[P2-L5-418]` | P versus NP OPEN.**

## Artifact readback

All six new artifacts were created on `main`, refetched completely, and compared byte-for-byte with the local verified bodies:

| Path | Git blob | Exact readback |
|---|---|---:|
| `experiments/review/lspv5_418_json_string_escape_alias.py` | `0ee8c5ed524c8b2bb04bd948a3ebecfdaa5a2f87` | yes |
| `experiments/review/verify_lspv5_418_json_string_escape_alias.mjs` | `a1f6ba98763b0cc3b35cdfe2809eb9ecf4b58db3` | yes |
| `results/raw/review/2026-11-07_1448_LSPV5_JSON_STRING_ESCAPE_ALIAS418.json` | `406f3739a15c224f930ae78ef80a03ef04add63f` | yes |
| `research/main/2026-11-07_1448_MAIN_JSON_STRING_ESCAPE_ALIAS_REFEREE418.md` | `4067b9a5f376c33d77d9c5a49bff0c06736aa84f` | yes |
| `research/coordination/2026-11-07_1448_LSPV5_JSON_STRING_ESCAPE_ALIAS418_HANDOFF.md` | `c51ba9306eb8d88f5bd1592f15bce5443c876677` | yes |
| `research/coordination/outbox/2026-11-07_1448_LSPV5_ISSUE3_OUTBOX418.txt` | `ef6230927896e388c41b628b621795d4a69799da` | yes |

Local SHA-256 values are recorded in the report and raw ledger.

## Conflict-safe tracker merge

- `proof1.txt` was read completely and remained byte-identical at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters).
- The current complete `proof2.txt` merge base immediately before writing was blob `babe439424d871c5f80c5627af549d1aabb14047` (252,193 characters), not the older run-start blob. Its exact-byte outbox was created first at `research/outbox/2026-11-07_1448_LSPV5_PROOF2_PREWRITE_EXACT418.txt`; refetch returned the same blob and complete byte equality.
- The append-only material node was written conflict-safely using that current SHA. A follow-up idempotent correction removed a second textual self-reference so the final complete readback has exactly one `[P2-L5-418]` node ID.
- Final `proof2.txt`: blob `d3dbb041e2422d04409460e3399229df7c7611fe`, 253,777 characters. Complete readback equals the expected merged body and preserves the entire merge-base body as an exact prefix.
- Affected IDs `[P2-D1]`, `[P2-D3]`, `[P2-L5-418]` were posted to issue #3 in comment `6714212990`. Direct REST readback of that comment matched the complete expected body byte-for-byte.

## Verification and limitations

- Python: 13 cases, six accepts/seven rejects as predicted.
- Independent Node: 34 assertions; six accepts/seven rejects; all accepted variants preserve baseline stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`.
- Root `main.tex` refetched as blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable bytes. It was not modified because complete outside-byte preservation was impossible.
- The local artifact subset lacks `.codex/skills/pnp-research/scripts/preflight.py`; the required command failed with file-not-found. Current GitHub skill/mode/protocol files were read completely. Repository report-check scripts were likewise unavailable locally.
- This remains a recovered-checker raw-byte identity result. `[P2-C3]`, `[P2-B1]`, `[P2-B2]` and P versus NP remain OPEN. No role, title, schedule, enabled state, grammar or weight changed.
