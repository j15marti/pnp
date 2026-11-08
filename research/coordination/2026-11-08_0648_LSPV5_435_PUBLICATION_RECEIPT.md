# LSPV-5/435 publication receipt

**2026-11-08 06:48 PST | Route B independent red team | P versus NP OPEN**

## Substantive artifacts

- Artifact commit: `903a500cdda46ef42c56e0ef323d58570cdc5a11`
- Report: `research/main/2026-11-08_0648_MAIN_NATIVE_SCHEMA_MALLEABILITY_REFEREE435.md`, blob `39aa53659c3c63c553bc11ac40d883cb761c3add`
- Python experiment: `experiments/review/lspv5_435_native_unknown_field_malleability.py`, blob `bdcca68375bf3bf0717c75e0f08de204e6ac4e02`
- Independent JavaScript: `experiments/review/verify_lspv5_435_unknown_field_malleability.mjs`, blob `34dd91a33827edb4b1641eeb5df63c5ccd02ef9e`
- Raw results: `results/raw/review/2026-11-08_0648_LSPV5_435_NATIVE_SCHEMA_MALLEABILITY_RAW.json`, blob `935bffa4b5701cfe42c2030a2470b1c1599bc731`
- Handoff: `research/coordination/2026-11-08_0648_LSPV5_NATIVE_SCHEMA_MALLEABILITY435_HANDOFF.md`, blob `101933717374319b64c772b579773fe0e5ed2bf1`
- Issue outbox: `research/coordination/outbox/2026-11-08_0648_LSPV5_ISSUE3_435.md`, blob `797fe1e493acd1a6cef107fd00da2b3f42225139`

All six artifact paths were fetched from the artifact commit and compared byte-for-byte with their local source files; every comparison was exact.

## Conflict-safe tracker publication

- Complete pre-write `proof2.txt`: blob `f643862b27cfb6fbb23564933cc25acaded47b0e`, 427,016 UTF-8 characters.
- Exact complete prospective outbox: `research/coordination/outbox/2026-11-08_0648_LSPV5_435_PROOF2_EXACT_OUTBOX.txt`, blob `e4ba2233300074e36827d511d814135ccfd004f9`.
- Outbox commit: `60b7f2316d8f5ee360f4ae861533c577647e8fd2`, installed with expected-head lease from artifact commit.
- Before tracker replacement, main and the current tracker blob were refetched; the old tracker was unchanged byte-for-byte.
- Tracker commit: `1160c97d342dac6a4ab51d8be75133d942a7de6c`.
- Complete post-write `proof2.txt`: blob `e4ba2233300074e36827d511d814135ccfd004f9`, 428,781 UTF-8 characters.
- Full readback checks: exact equality to the saved prospective outbox; exact old-content prefix; exactly one occurrence of `[P2-L5-435]`; final sentence `P versus NP remains OPEN.`
- Complete `proof1.txt` review: unchanged blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 UTF-8 characters.

## Coordination issue

- Issue #3 comment ID: `6723015171`
- URL: https://github.com/j15marti/pnp/issues/3#issuecomment-6723015171
- Full API readback: exact 1,617-character equality to the saved issue outbox.
- Affected IDs posted: new `[P2-L5-435]`; refined `[P2-D1]`, `[P2-D3]`, `[P2-L3-491]`, `[P2-L3-499]`, `[P2-L3-502]`, and `[P2-L5-420]`.

## Limitation

Root `main.tex` was not edited because the GitHub connector returned zero readable content bytes for blob `68188a24badda635a5983fda1c381cdb694fd497`; outside-region byte preservation therefore could not be established.

The material advance is restricted to the recovered checker schema-projection boundary. Historical all-rule normalization `[P2-C3]`, full mixed lower bound `[P2-B1]`, noncircular same-calculus B3 `[P2-B2]`, and P versus NP remain OPEN.
