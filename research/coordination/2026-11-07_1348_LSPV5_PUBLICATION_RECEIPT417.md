# LSPV-5/417 publication and readback receipt

**2026-11-07 13:48 PST | `[P2-D1]`, `[P2-D3]`, `[P2-L5-417]` | P versus NP OPEN.**

Exact GitHub main readback:

- report blob `d15cea68202f12c38188d8e3a41a568f9f52e9cd`;
- producer blob `91cd739acbe2aa2123c1f7489a91b034c427822a`;
- independent verifier blob `77c89b42cec34bdb59902b316d1896ec014a9ed6`;
- raw ledger blob `1b8f902bb1f0cc302576c6ae9a52348521ecac9a`;
- handoff blob `f8aef578ac0dba0cc6a6886a478968b6d194dc61`;
- issue outbox blob `e5767fbd73e16b4cdf69b88dc7f37f1483a62fc2`.

All six artifact readbacks matched the local bytes exactly.

Tracker protocol:

- `proof1.txt` reviewed and unchanged at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters.
- Latest complete `proof2.txt` was refetched immediately before writing at blob `1970ea10459a6318330a6b8a7f864d816405b1bb`, 241,232 characters.
- Exact complete prewrite content was first preserved at `research/outbox/2026-11-07_1348_LSPV5_417_PROOF2_PREWRITE_EXACT_ATTEMPT1.txt`.
- SHA-guarded tracker update commit `228a7914bfa61a3f47ad72890c0d3673870c9d86` produced blob `dd66f186cd3d617be90a6b1c16281965041a5f64`, 244,059 characters.
- Complete tracker readback exactly equals the prewrite outbox; entries for `[P2-D1]`, `[P2-D3]` and `[P2-L5-417]` are present.
- Issue #3 comment `6713690564` was created from the durable outbox and idempotently rewritten with the same complete body.

Root `main.tex` still returned blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable bytes. No partial or inferred rewrite was attempted. No roles, schedules, enabled states, agents, allocations, historical grammar or weights were changed.
