# Publication receipt | LSPV-5/421 | 2026-11-07 17:09 PST

Status: publication and complete readback verified. P versus NP OPEN.

## Artifacts

| Artifact | Commit | Blob | Readback |
|---|---|---|---|
| `experiments/review/lspv5_421_output_projection_audit.py` | `6e1b9539401dae6b57f0f7d196c1f33f4f94a5ad` | `d4533746cb8aa7c3e9bf032cb5fc4ff4f1f16d45` | exact |
| `experiments/review/verify_lspv5_421_output_projection.mjs` | `db011969e703573ae0c74354cf67d376fc43d3af` | `a9eee496f78d352c250f426857ec634d9d9bc331` | exact |
| `results/raw/review/2026-11-07_1709_LSPV5_OUTPUT_PROJECTION421.json` | `b82aa8e35d11074c425c362424958a23d61b7c79` | `1af2bb8c0a4bd505863c199e8dfeea8cface6beb` | exact |
| `research/main/2026-11-07_1709_MAIN_OUTPUT_PROJECTION_REFEREE421.md` | final update `4707d282983873d300ae25e2f97bf8844f65b12f` | `939c3e580385449db61292115189494a51877aff` | exact |
| `research/coordination/2026-11-07_1709_LSPV5_OUTPUT_PROJECTION421_HANDOFF.md` | `801882d416c5e7a63a155ce884dc192cf73e3130` | `321bfc43e9ce48de7ef39401c100e6c0c7bdf119` | exact |
| complete `proof2.txt` prewrite outbox | `e49b1165311369c7f7ac2629cbc1251368b1c06d` | `68d862d9a29f3a501a33a39993eda6478795774a` | exact, 279255 characters |
| issue #3 exact outbox | `23a2ad1cac4b352ce8a0f8ce903ba08cb4908356` | `94b18d252df854ad09b5de10df8995c3e4608ebe` | exact |

## Trackers

- `proof1.txt`: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, unchanged.
- `proof2.txt`: prewrite blob `68d862d9a29f3a501a33a39993eda6478795774a`; SHA-guarded update commit `dea9bd4a951d0041b574813899d31f9957823152`; complete readback blob `cc9990b77ca41a61f794b4cde1d98864c3fc5e14`, 281677 characters, exact equality PASS, exactly one `[P2-L5-421]` occurrence.
- Affected IDs posted: new `[P2-L5-421]`; affected `[P2-F13]`, `[P2-C3]`. Open dependencies `[P2-D1]`, `[P2-B1]`, `[P2-B2]` unchanged.

## Coordination

- Issue #3 comment ID `6715588094`, `https://github.com/j15marti/pnp/issues/3#issuecomment-6715588094`.
- Direct comment readback was byte-exact to the durable outbox.

## Limitation

Root `main.tex` fetch returned blob `68188a24badda635a5983fda1c381cdb694fd497` with no readable content. It was not modified, honoring the prohibition on overwriting a partial or unreadable large root file. The standalone report, handoff, tracker, raw results, code, outboxes and issue comment are durable.
