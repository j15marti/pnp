# LSPV-5 root `main.tex` oversized-write recovery — 2026-11-01 09:52 PST

Status: technical publication recovery only. No task, title, enabled state, schedule, identity, scientific allocation, or proof status changed. P versus NP remains **OPEN**.

## Failure

The normal GitHub contents update accepted the intended 1,049,386-byte replacement request but committed an empty `main.tex` blob in commit `14ca9c3b147dde7bc7b84fe5ab554dd412db1ee8`. Immediate readback returned blob `62eaf60bbbfd7939bfdc91743bcc8663a326adda` with zero bytes. Classification: **CONNECTOR OVERSIZED CONTENT TRUNCATION**, not a scientific or merge conflict.

## Recovery

1. Created a forward recovery tree referencing the previously verified nonempty root blob `ccbecc8f67d97379c0911778e2eb723c053b0f5a`; committed as `1f4679bacd8a3e1f565e72ee0b9403779f6ab78b`.
2. Rebuilt the intended REFEREE269 reconciliation in memory from that verified blob.
3. Created Git blob `256f79193dce8eb78aeefff5a35dfcd004df47bc` directly and independently fetched it back: 1,049,375 bytes; REFEREE269 marker present; explicit OPEN status present; final REFEREE269 sentinel present; each LSPV-1..4 ownership marker appears exactly once at both BEGIN and END.
4. Committed that verified blob through tree `815f67a19c7100cadd3d495cd9201fc6f7591c72` as commit `8fa82da65924e0bd52971ea7e3d4dd767df67bf3` and moved `main` by fast-forward lease.

## Rollback

If the reconciled root later proves malformed, restore blob `ccbecc8f67d97379c0911778e2eb723c053b0f5a` through a forward Git tree commit. Do not use the normal contents update for this approximately 1 MB file until its truncation behavior is fixed.
