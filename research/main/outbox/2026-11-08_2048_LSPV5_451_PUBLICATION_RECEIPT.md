# LSPV-5/451 publication receipt

**Pacific timestamp:** 2026-11-08 20:48 PST  
**Result:** publication and complete readback succeeded for role-owned artifacts and `proof2.txt`; root `main.tex` was not edited because its current blob returned zero bytes.

## Immutable artifacts

| Path | Commit | Complete blob | Bytes | Exact local/readback |
|---|---|---:|---:|---|
| `research/main/2026-11-08_2048_MAIN_MOD3_ARTICULATION_SOURCE_REFEREE451.md` | `59d2566bdd9ffaa3c11e888c09ec618c02e82f29` | `efe90479129d34e651184833291778473e6527b7` | 14,446 | yes |
| `experiments/review/lspv5_451_mod3_articulation_audit.py` | `47212293c7393fc4373e71341d27958bda2458c7` | `d686dc037c1d0df469b28d69639d037625fa021a` | 11,407 | yes |
| `experiments/review/verify_lspv5_451_mod3_articulation.mjs` | `884dddbca9c3e066af48ff7895973d4ae248a962` | `dba24cf055d05a151bd9621892a95135f473dfcb` | 7,655 | yes |
| `results/raw/arc/2026-11-08_2048_LSPV5_MOD3_ARTICULATION_AUDIT451_RAW.json` | `5496964d5480efebde2cdf5b41905aaeac9ffbcb` | `6c26154b534766dbcfb424a861775cf4f7cfe647` | 276,188 | yes |
| `research/coordination/2026-11-08_2048_LSPV5_MOD3_ARTICULATION451_HANDOFF.md` | `ed57d298b7a3e0209adfcce2646b26d5e4c6c073` | `8ced044873f45cf63d5eace56beab0535f1f6fa0` | 2,242 | yes |
| `research/main/outbox/2026-11-08_2048_LSPV5_451_PROOF2_DELTA.md` | `efe6f2ac163bc89b8330128573fdbde74ada15b8` | `696d0994cd5ed8dc7c0f5d009b18919f000468af` | 2,678 | yes |
| `research/main/outbox/2026-11-08_2048_LSPV5_451_MAIN_INSERTION_FALLBACK.tex` | `fde5247969ff11aaec6023c02b116fd5539ae1dc` | `fc9170155e7a535e013b123b2884e65a6b325909` | 1,063 | yes |
| `research/main/outbox/2026-11-08_2048_LSPV5_451_ISSUE3_OUTBOX.md` | `9a2fe2e64888b642cb1c6b8c6c99032222971def` | `29588cb9441220351a3d84e9f92d4765ea343dce` | 3,092 | yes |

## Mutable tracker

- `proof2.txt` base complete blob: `7a95a89fa3c4b5dbf4e32174a7d24646a0f2a0f4`, 609,723 bytes.
- Update commit: `3d451fe72640ac3f4dd571decb1ce98c783b86ed`.
- Complete readback blob: `86e32d8698e018b56124c8a29351d0f8250eaec2`, 612,402 bytes.
- Verification: exact base prefix preserved; exact delta suffix; `[P2-L5-451]` occurs once.
- `proof1.txt` unchanged complete blob: `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 bytes.

## Coordination

- Issue #3 comment ID `6732627015`, created `2026-11-09T04:59:42Z`.
- Full page readback found the comment and its body exactly matched the durable outbox.
- Affected IDs posted: `[P2-L5-451]`, `[P2-L1-523]`, `[P2-L3-521]`, `[P2-L3-510]`, `[P2-F6]`, `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`.

## Verification and limitation

- Producer: PASS, 163,520 clause checks, 524 witnesses, SHA-256 `b5cfd3836151a86670b48829bce9489df7f73f4696d9f77f0ffd82cd7674c56c`.
- Independent verifier: PASS, 2,371 assertions, SHA-256 `d25b7fbcb990b4b750a100194c87e337ce98fed7623d65584eeae1d6051194fe`.
- Raw SHA-256: `6a5326e0ebbd29ebcc3304ef1e57eff159324ec45b7ebc4a0dbbf67137ff4d70`.
- Root `main.tex`: current metadata blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba`; content readback length zero. No edit attempted. Durable insertion fallback published above.

Historical `R_mix341` grammar and weights, all roles/tasks/titles/schedules/enabled states, and the two-Route-A/three-Route-B allocation were unchanged. The result is restricted and does not resolve P versus NP.
