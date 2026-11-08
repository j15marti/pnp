# LSPV-5/419 publication and readback receipt

**2026-11-07 15:48 PST | `[P2-D1]`, `[P2-D3]`, `[P2-L5-419]` | P versus NP OPEN.**

## Artifact readback

All six substantive artifacts were created on `main`, refetched completely, and compared byte-for-byte with the locally verified bodies:

| Path | Git blob | Exact readback |
|---|---|---:|
| `experiments/review/lspv5_419_metadata_binding_audit.py` | `7cb40fd974d2ef3efc17179031ee392b1258e598` | yes |
| `experiments/review/verify_lspv5_419_metadata_binding.mjs` | `83fb99b2a64de4ca32de5ed34c2ed5826b030631` | yes |
| `results/raw/review/2026-11-07_1548_LSPV5_METADATA_BINDING419.json` | `cafe19bfbe659623e6c1a74dfc3ed03db6d13c19` | yes |
| `research/main/2026-11-07_1548_MAIN_METADATA_BINDING_REFEREE419.md` | `ccbda2cbba619a6f2146cf95918c3a462eb2f0c6` | yes |
| `research/coordination/2026-11-07_1548_LSPV5_METADATA_BINDING419_HANDOFF.md` | `a4411b5a27b2ad834df74a68c661069bfbd0dbeb` | yes |
| `research/coordination/outbox/2026-11-07_1548_LSPV5_ISSUE3_OUTBOX419.txt` | `fa705ed011b87dfcda2ee1fe761ea7ebfff56c61` | yes |

Local SHA-256 values are recorded in the report and raw ledger.

## Conflict-safe tracker merge

- Complete `proof1.txt` was refetched at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters) and left byte-identical.
- Complete `proof2.txt` was refetched immediately before writing at blob `ad317008264aa0f0c75cdd5fc6a059437f16a815` (261,970 characters). Its exact current body was first published as `research/outbox/2026-11-07_1548_LSPV5_PROOF2_PREWRITE_EXACT419.txt`, blob `ad317008264aa0f0c75cdd5fc6a059437f16a815`; complete backup readback matched byte-for-byte.
- A second complete tracker refetch after the backup still matched the same blob/body. The append-only write used that current blob SHA and commit `b3d56bc5e6cdbdbc2e3cd81bd5db7d12d5e83fb3`.
- Final complete `proof2.txt` readback is blob `c4ddf2c72683c3a393d31d72c5e4bec2a3c66c91` (263,938 characters). Its first 261,970 characters equal the complete prewrite body exactly, and it contains exactly one `[P2-L5-419]` node ID.
- Affected IDs `[P2-D1]`, `[P2-D3]`, `[P2-L5-419]` were posted to issue #3 in comment `6714766945`; direct REST readback matched the complete 1,271-character outbox body byte-for-byte.

## Verification and limitations

- Python producer: 20 cases, ten accepted unbound declarations and ten rejected semantic controls; 2.7116 s wall and measured peak process-tree RSS 13,552 KiB.
- Independent Node: 52 assertions/20 cases; strict consistency rejected all twenty mutations; 2.5664 s wall and measured peak process-tree RSS 48,072 KiB.
- All ten accepted mutations preserve baseline stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`.
- Root `main.tex` remained unreadable through the connector (blob `68188a24badda635a5983fda1c381cdb694fd497`, zero readable bytes), so no ownership-region edit was attempted.
- The local artifact subset lacks `.codex/skills/pnp-research/scripts/preflight.py`; that command failed with file-not-found. Complete governing files were read from GitHub, and the preserved checker/packet were replayed locally.
- This is a recovered-checker metadata-binding result, not a historical full-calculus authentication, all-mixed lower bound, B3 implication or P-versus-NP resolution. No role, title, schedule, enabled state, grammar or weight changed.
