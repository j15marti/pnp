# LSPV-5/420 publication and readback receipt

**2026-11-07 16:48 PST | `[P2-F13]`, `[P2-D3]`, `[P2-L5-420]` | P versus NP OPEN.**

## Artifact readback

All six substantive artifacts were created on `main`, refetched completely, and compared byte-for-byte with the locally verified bodies:

| Path | Git blob | Exact readback |
|---|---|---:|
| `experiments/review/lspv5_420_reachability_and_discharge_audit.py` | `603d15390468cd89846dae6dfc8b8d9ceae5b418` | yes |
| `experiments/review/verify_lspv5_420_reachability_discharge.mjs` | `142e92116c2b7203638a6279084a85970a4d4890` | yes |
| `results/raw/review/2026-11-07_1648_LSPV5_REACHABILITY_DISCHARGE420.json` | `347f9dfa7efc1a6c7f9a710e569b763a8feeb932` | yes |
| `research/main/2026-11-07_1648_MAIN_REACHABILITY_UNIT_DISCHARGE_REFEREE420.md` | `45c5c20ea66400167292f76ffa7c6c9da85aac5c` | yes |
| `research/coordination/2026-11-07_1648_LSPV5_REACHABILITY_DISCHARGE420_HANDOFF.md` | `8a9b8314aa3bc124949d23eb4fbda5bfbb5b4489` | yes |
| `research/coordination/outbox/2026-11-07_1648_LSPV5_ISSUE3_OUTBOX420.txt` | `659af6fede43f36750f2c378cf797d662a69473f` | yes |

Local SHA-256 values are recorded in the report and raw ledger. The issue outbox is 1,484 bytes with local SHA-256 `bf85b6dbdd9c48329d4f0a96fa76864d5f591047d0baa33100f17305fe2c69e9`.

## Conflict-safe tracker merge

- Complete `proof1.txt` was refetched at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters) and left byte-identical.
- Complete `proof2.txt` was refetched immediately before writing at blob `22b1ef4dc3d9e6d81b911130966072ccc1cca801` (273,110 characters). Its exact current body was first published as `research/outbox/2026-11-07_1648_LSPV5_PROOF2_PREWRITE_EXACT420.txt`, blob `22b1ef4dc3d9e6d81b911130966072ccc1cca801`, commit `13abf8325692f29cf3cdf2eb79bb8159a4d3e15d`; complete backup readback matched byte-for-byte.
- A second complete tracker refetch after the backup still matched the same blob/body. The append-only write used that current blob SHA and commit `837e70ab2271d04810fd11fffd0a6c9de11f5c99`.
- Final complete `proof2.txt` readback is blob `6dee60ca225be6efe1440daba8014765aa3ee4ad` (275,412 characters). Its first 273,110 characters equal the complete prewrite body exactly, and it contains exactly one `[P2-L5-420]` node ID.
- Affected IDs `[P2-F13]`, `[P2-D3]`, `[P2-L5-420]` were submitted to issue #3 and the write call returned comment ID `6715347033`. Exact post-write body readback was not available: the GitHub all-comments endpoint closed its transport, and the unauthenticated browser surface returned a private-repository 404. Publication is therefore recorded as **comment posted; readback unverified**, not as exact comment-readback success.

## Verification and limitations

- The recovered checker accepted the baseline and one legal independent topological reorder with stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`; six controls covering unreachable insertion, post-sink append, count manipulation, missing proof record, nonsink replacement and duplicate inference ID were rejected.
- All seven fixtures had full sink ancestry: proof/source pairs 15/16, 23/24, 31/32, 39/40, 47/48, 127/128 and 39/40.
- Exhaustive three-variable controls covered all 26 nonempty nontautological clauses, CNFs of one through three clauses and all six literal assumptions: 2,850 qualifying branch instances, 4,278 original Resolution nodes, 1,428 emitted transformed nodes and 2,850 legal stronger-parent bypasses.
- The exact peer source `experiments/arc/lspv1_489_guard_discharge.py`, remote blob `486bb82733155b84ffbc1b1a71ceeada43abf310`, executed successfully: 24 gate facets, 6 blockers, 17 cover Resolution nodes, 23 global Resolution nodes, 19 source ancestors, 42 total nodes, cover span 6 and global span 9. Independent Node verification passed 72 assertions.
- Python used 1.1889 s wall with measured peak process-tree RSS 13,472 KiB; Node used 0.3868 s wall with peak process-tree RSS 42,356 KiB; `/proc` was sampled every 2 ms.
- Root `main.tex` remained unreadable through the connector (blob `68188a24badda635a5983fda1c381cdb694fd497`, zero readable bytes), so no ownership-region edit was attempted.
- The local artifact subset lacks `.codex/skills/pnp-research/scripts/preflight.py`; that command failed with file-not-found. Complete governing files were read from GitHub, and the preserved checker/packet were replayed locally.
- This run validates a restricted ordinary-Resolution unit-assumption elimination control and complete sink ancestry in the recovered checker fixtures. It does not authenticate the historical full R_mix341 calculus, prove an all-mixed lower bound, establish B3, or resolve P versus NP. No role, title, schedule, enabled state, grammar or weight changed.
