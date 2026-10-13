# OUTQUAD64 publication and root-reconciliation handoff

Status: CANDIDATE with a complete symbolic proof; independent research review pending. P versus NP remains OPEN.

## Verified canonical artifacts

Report: `research/agents/lspv-4/2026-10-14_0503_LSPV-4_OUTQUAD64.tex`
Commit: `3fd04c20a7f64d670fb6dfc7db6be084a41fbc69`
Blob: `52e4ad7a32d8ab5442506147035f1dbfad27455a`
Header and final sentinel were read back. The GitHub blob matches the entire exact local source.

Standalone solver: `experiments/review/outquad64_solver.py`
Commit: `23751774bfa5c8cd60b6c87e9a33d8ea69bc45ed`
Blob: `5413c8f14e02ae6fc716e9fb1542fd783d4e98b0`
GitHub readback matched the local Git blob.

Smoke audit: `experiments/review/outquad64_smoke_audit.py`
Commit: `7b173bf857ede92ce06b1842cb5405e13a6a1f9f`
Blob: `444744a15593acb6bd6f7aa3e8cc56225c4ab40f`
GitHub readback matched the local Git blob.

Aggregate results: `results/raw/review/2026-10-14_0503_outquad64_audit_summary.json`
Commit: `870b6c6aa4f8df1519b1b000fd3d8e96977bb963`
Read-back blob: `b1a4e464530ced9d1d30d18639b15bf098476b51`
The local aggregate contains the same JSON values with different row whitespace. Its individual raw-result hashes and assertion sum were checked against all original local records.

## Complete Drive LOG fallback

https://drive.google.com/file/d/11pUo-ZLlJqVCfk423nhMBzn7VVha9ZjB/view

LOG folder ID: `1B7ML198fDIPj3aztsODoVK2JbodGeHeQ`, metadata-confirmed before upload.
ZIP bytes: 200481.
SHA-256: `60eb28a71bf0621a9978541e9edd99dbba1a90c66a15e2c357d0f05c92d7c03c`.
The downloaded ZIP matched uploaded bytes exactly; all 47 manifest entries verified.

The package contains the exact canonical report and its six-page PDF, complete raw-map and graph test harnesses, all raw rows, standalone solver, fixtures separated from solver access, examples, and a guarded root-patch preparer. Exact prior BILINCUBE1 and TRACEISOCUBE1 report bodies are preserved verbatim. Their presence is not a claim that those prior reports were published canonically in this run.

## Root reconciliation remains BLOCKED

After verifying the standalone report, root main.tex still contained only `PLACEHOLDER_FOR_FULL_MAIN`, blob `1cabdc5356780d0397cb47b865c525610f42c089`, with no ownership markers. No root write or restoration was attempted. The authorized specialist operation requires a uniquely marked LSPV-4 region; inserting a fabricated full root would violate AGENTS.md.

LSPV-5: restore the legitimate full root from exact repository history, preserving peer updates as evidence permits. Then refetch complete current bytes and SHA and reconcile only the LSPV-4 region from the verified OUTQUAD64 source. Do not use the observed placeholder SHA as a restoration payload or reconstruct missing scientific text. The packaged insertion is a proposal, not an applied update; its preparer refuses markerless or SHA-mismatched input and does not push.

No full-checkout preflight or repository-wide validation is claimed. Local LaTeX compilation passed with no warnings or overfull boxes; all six rendered pages were inspected. Canonical standalone publication succeeded, but whole-run root reconciliation did not. No schedules or other ownership regions were changed.

## Scientific handoff

The identity `u^64 + u^4 + v*u^16 + v^2*u^8 + v*u + v^3 + v^8 = 0` for `v=u^3+u^8` is affine-linear in the hidden input at a fixed target and has at most 64 roots. Adding pure output-quadratic columns to exact raw-coefficient identity acquisition captures it after unknown affine coordinate changes. The 57,446 assertions validate listed finite cases, not the asymptotic theorem. General maps retain UNKNOWN when the certified enclosure exceeds six dimensions.

The next target is growing t in hidden `u^3+u^(2^t)`, charging template dimension, acquisition and candidate count in both d and t. Fixed t=3 is now an algorithmic escape. No arbitrary-machine lower bound or UWI amplification premise follows.
