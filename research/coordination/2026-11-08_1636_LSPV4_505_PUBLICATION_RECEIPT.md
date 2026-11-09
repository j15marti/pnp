# LSPV-4/505 publication and exact-readback receipt

**2026-11-08 16:36 PST | Route A | P versus NP OPEN**

IDEA -> SEARCH -> ITERATE evidence: source/instance/machine/model and proof/falsifier ledger in `research/agents/lspv-4/2026-11-08_1636_LSPV4_CLIPPED_INPUT_HEAD_MONITOR505.md`.

Published `main`, each file independently fetched and read back:
- `research/agents/lspv-4/2026-11-08_1636_LSPV4_CLIPPED_INPUT_HEAD_MONITOR505.md`, Git blob `0ef38656bec8deab54ea439fac8e7eb8aa6a65f3`, 13322 UTF-8 characters.
- `experiments/arc/lspv4_505_clipped_input_monitor.cjs`, Git blob `de33c398b3f460ba6510027d22597dd8bc213b44`, 4645 chars. Reexecuted fetched actual JS in V8: PASS, 64 traces, 81000 modeled guest steps. Standalone Node CLI emits result JSON.
- `results/raw/arc/2026-11-08_1636_LSPV4_505_INPUT_HEAD_RAW.json`, Git blob `38580e19ef990a427c61c96b022b332635cc0933`, 1386 chars, valid JSON with both independently run Python and JS counts.
- `research/coordination/2026-11-08_1636_LSPV4_CLIPPED_INPUT_HEAD_FIVE_ROLE_HANDOFF505.md`, Git blob `97c29bb152701f272886903d9fa437531a27108c`, 2622 chars.

Root trackers read entirely. `proof1.txt` unchanged Git blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, length 18553. `proof2.txt` current prewrite `2ed8a7da8dcc146d5d865bd4bc77921b6f2a138b`, length 546436; SHA-guarded appended [P2-L4-505] with all prior characters byte-for-byte preserved; commit `ab95ac964f6dbabb553fef7fc22eef796f5bb771`; exact full-content readback Git blob `fd4f5cddcc9ea1d4dc7fd24a3df0c2834eb486ab`, length 549093. Peer writes may advance the head later.

Coordination issue #3, comment 6729613572: https://github.com/j15marti/pnp/issues/3#issuecomment-6729613572; fetched individually and exact-body comparison PASS.

Independent Python hosted verifier and its complete 64-case raw ledger persisted in chat archive `LSPV4_505_CLIPPED_INPUT_HEAD_INDEPENDENT_REPRO.zip`, SHA-256 `9127739150d15caaa2c461595378c1acd229a722c6be0b4c0c581c82b73ffb5c`. This run did not execute a complete native FLMV interpreter. No main.tex, unrelated roles, agent schedules, enabled states, allocation, R_mix341 rules or weights changed. Remaining [P2-A2], [P2-A4], [P2-A5] OPEN and P versus NP OPEN.
