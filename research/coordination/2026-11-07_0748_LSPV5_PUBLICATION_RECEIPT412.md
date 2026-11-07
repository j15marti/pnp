# LSPV-5/412 publication and readback receipt

**2026-11-07 08:00 PST | P versus NP OPEN.**

Published and completely read back:

| Artifact | Git blob | Characters |
|---|---|---:|
| `research/main/2026-11-07_0748_MAIN_AND3_PARENT_GRAMMAR_REFEREE412.md` | `b99084b9e1534654207042d00d6645361dfc5863` | 14,687 |
| `research/coordination/2026-11-07_0748_LSPV5_AND3_PARENT_GRAMMAR412_HANDOFF.md` | `ad46143d945f72128dadc8a6a31da343492739c9` | 2,086 |
| `experiments/review/lspv5_412_and3_parent_underdetermination.py` | `fd1bbec5af6334873931b4a5a4dfbae06fa9a900` | 18,133 |
| `experiments/review/verify_lspv5_412_and3_parent_underdetermination.mjs` | `f81991a790003d16fc52840c6da4b7c6d2f33f0d` | 8,383 |
| `results/raw/review/2026-11-07_0748_LSPV5_AND3_PARENT_UNDERDETERMINATION412.json` | `fc9344d367f5706d1b14d97f44a8565be4112047` | 2,520 |

Conflict-safe tracker merge:

- complete starting `proof2.txt`: blob `af757c6238edcc9140eb4c183c5c7964302cdf3b`, 160,665 characters;
- complete final `proof2.txt`: blob `7b3808f351a8c303a030d181e0f07eb46a91ba76`, 163,840 characters;
- exact full-content comparison: PASS;
- `[P2-D1 evidence, LSPV-5/412]` count: 1;
- `[P2-L5-412]` count: 1;
- `proof1.txt` unchanged: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters.

Coordination issue #3 accepted comment ID `6709520998`. An idempotent full-body update by that ID succeeded. Bulk full-thread retrieval returned no comment payload, so body readback could not be independently completed; the exact body was saved first at `research/coordination/outbox/2026-11-07_0748_LSPV5_ISSUE3_412.md` and published before the comment. The exact tracker delta was similarly saved first at `research/coordination/outbox/2026-11-07_0748_LSPV5_PROOF2_412_DELTA.md`.

Root `main.tex` was not edited: the connector returned a nonempty blob SHA with zero readable content bytes, so outside-byte preservation could not be guaranteed.

No role, title, task, schedule, enabled state, two/three Route allocation, historical grammar or weight changed.
