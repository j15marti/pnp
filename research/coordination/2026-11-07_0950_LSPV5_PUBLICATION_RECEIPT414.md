# LSPV-5 publication receipt 414

Timestamp: 2026-11-07 09:50 PST

## Published artifacts and complete readback

- `research/main/2026-11-07_0950_MAIN_AFFINE_GHOST_PORT_REFEREE414.md`: blob `43c54b4adc1ddf48f4c0bd5ac6d0824db30486c9`, exact content readback.
- `experiments/review/lspv5_414_affine_ghost_port_audit.py`: blob `b984ea2f9f86a3f709a928ad5f315ab20fe8fb84`, exact content readback.
- `experiments/review/verify_lspv5_414_affine_ghost_port.mjs`: blob `392ca52b8c90ecd3b9274f1b493c56e27285feae`, exact content readback.
- `results/raw/review/2026-11-07_0950_LSPV5_AFFINE_GHOST_PORT414.json`: blob `058d0bf564be049f362d92d1b3f24a7332a560cb`, exact content readback.
- `research/coordination/2026-11-07_0950_LSPV5_AFFINE_GHOST_PORT414_HANDOFF.md`: blob `808df661b4a55d59cc2ea542c2d10b7332ccffdd`, exact content readback.
- `research/coordination/outbox/2026-11-07_0950_LSPV5_ISSUE3_OUTBOX414.txt`: blob `aef73b1c5e43b14274c928df2920f8e309741e46`, exact content readback.

## Trackers

- `proof1.txt`: reviewed, unchanged, complete blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.
- `proof2.txt`: conflict-safe complete replacement from current blob `067f29c734736c09d14cc25401a3f24046311d37`; complete readback at blob `7e4dac762491ccfa07f951852ded43b33e6996e9` with one evidence entry under `[P2-D1]`, one under `[P2-D3]`, and one defining `[P2-L5-414]` (the identifier also appears in a cross-reference).

## Coordination issue

- Issue #3 comment ID `6711381148` created from the durable outbox and then replaced idempotently by ID with the exact same body.
- Affected IDs posted: `[P2-D1]`, `[P2-D3]`, `[P2-L5-414]`.

## Execution

- Exact historical producer/checker packet replay: PASS.
- Python adversarial audit: PASS.
- Independent Node verifier: 37 assertions, PASS.
- Mutant packet SHA-256: `2192cca5e56762995fd55fd17c7cb44fc8c92ced7a5c240c84713f420e25d051`.

## Safeguard blocker

Root `main.tex` was not edited. Its fetched blob `68188a24b3cffc8104b34e9a0f165a81d4e4a767` exposed an empty payload, so complete outside-marker byte preservation could not be certified.

P versus NP remains OPEN.
