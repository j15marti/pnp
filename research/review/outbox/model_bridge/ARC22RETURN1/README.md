# ARC22RETURN1 publication and root-repair handoff

Status: CANDIDATE with complete symbolic proofs; independent research review pending. P versus NP remains OPEN.

Canonical report:
`research/agents/lspv-4/2026-10-13_0250_LSPV-4_ARC22RETURN1.tex`
Commit: `50628dfb4cecdecff35cbb52185d8d518c4de661`.
Blob: `8bb653632e0ac2a7c51b98b52d248bfa918d3750`.
Header and final sentinel read back; full blob matches exact local source.

Compact verifier:
`experiments/review/arc22_return_verifier.py`
Commit: `7fb29711a4fa01821cd4566c3acd17f8ee7e4548`.
Blob: `db47d7112b7c8b084cedd939b31a6d67dee24c89`, read back and matched locally.

Audit publication:
`results/raw/review/2026-10-13_arc22_return_publication.json`
Commit: `9027c33fca7277cc26162143061ed4a15652bd5a`.
Blob: `07b63d6674a69e59c8db7ad0c8828b3b20c5d3cb`, read back.
The package JSON has equivalent data with different whitespace.
17,025 assertions passed across the full runner and a separate verifier.
A separate implementation by the same author is not independent human review.

## Complete reproducibility fallback

Drive LOG: https://drive.google.com/file/d/1LJ1mJWfKwDNnMGWCebgwooNtO96l8wgT/view
Folder ID `1B7ML198fDIPj3aztsODoVK2JbodGeHeQ` was confirmed as LOG.
ZIP size: 438331 bytes.
SHA-256: `95f77c578d163e76a84adea2c8cf4f9f98f88f54a1c4050c9ad00e5171c1dcbb`.
Downloaded ZIP matched uploaded bytes; all 21 manifest entries matched.
It contains the exact report, PDF, full instrumented phase runner, separate
verifier, pinned unchanged compiler/decoder, all raw rows, and a proposed
LSPV-4-owned insertion with the prior guarded preparer reference.
The full instrumentation runner and complete raw rows are preserved there;
only the compact verifier and aggregate raw fingerprints are claimed published
to GitHub in this run.

## Root reconciliation remains pending

No root main.tex write was made. A fresh read after standalone verification
returned blob `2373f3ced8b19e89dab587593934ebd30f30ec3f`; do not reuse it without
refetching. A preceding tree entry measured the root at 261492 bytes, but the
complete current root was not staged from truncated connector responses.
Local git access failed DNS resolution. Full-checkout preflight and repository-
wide validators were not run. This is a documented incomplete reconciliation,
not canonical whole-run success.

Recovery: obey current AGENTS.md, verify the standalone report, fetch complete
current main.tex bytes and SHA, reconcile only the unique marked LSPV-4 region,
preserve all other bytes, then verify readback, balanced markers and OPEN status.
The packaged insertion is a proposal, not an applied root edit. Preserve schedules
and other ownership regions. Do not reconstruct missing scientific bodies.

Scientific guard: branching then properizing/rebalancing through U expands on
balanced sources. Direct reuse of a decoded source already in C22 contracts and
can uniformly remove nested U padding. Neither query-size expansion nor depadding
is an unrestricted SAT lower bound. The next target is a native residual consumer
with actual successor coverage and charged joint resources, not another return
through the same expanding compiler.
