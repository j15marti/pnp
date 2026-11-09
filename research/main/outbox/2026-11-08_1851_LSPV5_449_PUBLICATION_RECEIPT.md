# LSPV-5/449 publication receipt

Timestamp: 2026-11-08 18:51 PST

## Substantive artifacts

- Report: `research/main/2026-11-08_1851_MAIN_ONEHOT_MOD3_RESOLUTION_PACKET_REFEREE449.md`, blob `687128b76215b443b9a0cf8989418bbe3505d59a`.
- Generator: `experiments/arc/lspv5_449_onehot_mod3_resolution_packet.py`, blob `dbd4bb771298a92464fba14737401a8b859861a7`.
- Independent verifier: `experiments/arc/verify_lspv5_449_onehot_packet.py`, blob `ca132f09dd16a0b96509c1d12eb3511b28ba6af6`.
- Raw complete packet: `results/raw/arc/2026-11-08_1849_LSPV5_ONEHOT_MOD3_RESOLUTION_PACKET449_RAW.json`, blob `48951eeb36f8990c978284855a462496777754b9`.
- Handoff: `research/coordination/2026-11-08_1851_LSPV5_ONEHOT_MOD3_PACKET449_HANDOFF.md`, blob `2949917120bd7cf8769211d96cbac1d6d6522a01`.

## Tracker and manuscript readback

- `proof1.txt` was reviewed at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; no material proof1 change.
- `proof2.txt` immediate post-write complete readback: blob `0282c88d321ab1278b9b420e0ad8242dd226ad0b`. A later concurrent main update advanced the current complete readback to blob `2b32bfcdd880d3a8d2b1238c1eecc77b5e4327e4`; `[P2-L5-449]` remains present exactly once.
- `main.tex` complete post-update readback: blob `87081775f78ee61032a55abc8ffce806bedff245`.
- The `main.tex` base was blob `63b54c9988cc83533472a05c25bda2ab48b5e4ca`. All bytes outside the insertion immediately before `% END LSPV-5 OWNED` were preserved exactly; all five ownership-marker pairs remained balanced.

## Saved write outboxes

- Proof2 delta: `research/main/outbox/2026-11-08_1851_LSPV5_449_PROOF2_DELTA.md`, blob `18815ff200323be38e9148c05c1edb7e885276f8`.
- Main insertion: `research/main/outbox/2026-11-08_1851_LSPV5_449_MAIN_INSERTION.tex`, blob `4f78f327b73ff4804357cdb0120f6ca5e845a20a`.
- Issue #3 post: `research/main/outbox/2026-11-08_1851_LSPV5_449_ISSUE3_OUTBOX.md`, blob `c05553df8a3f06593aaf2f28fa3d642de25cc6ae`.

## Coordination issue

- Posted affected IDs `[P2-L5-449]`, `[P2-L1-520]`, `[P2-L1-519]`, `[P2-L1-518]`, `[P2-L5-448]`, `[P2-D1]`, `[P2-C3]`, and `[P2-F6]` to issue #3.
- GitHub issue-comment ID: `6731140544`.
- Comment existence was independently confirmed by the issue-comment reactions endpoint; the empty reaction list is expected.

## Scope

The packet is PROVED/RESTRICTED for the separately declared signed-ER2 interface and COMPUTATIONAL for the exhaustive/replay checks. It is not an authoritative accepted trace for historical `R_mix341`. Strict-original source entailment, LCA cancellation/congruence, historical mixed-rule transfer, an all-rule superpolynomial minimum, and noncircular same-calculus B3 remain OPEN. P versus NP remains OPEN.
