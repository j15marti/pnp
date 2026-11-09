# LSPV-5/450 publication receipt

**Run:** 2026-11-08 19:50 PST  
**Role:** LSPV-5 independent red team, Route B  
**Status:** artifacts, material `proof2.txt` node and issue #3 notification published and read back; root `main.tex` blocked by zero-byte content response. P versus NP OPEN.

## Immutable artifacts on `main`

| Path | Commit that created file | Readback blob |
|---|---|---|
| `research/main/2026-11-08_1950_MAIN_DEF_FACET_OWNER_BOUNDARY_REFEREE450.md` | `af62e0ffd2939724eccdbcde89528bf2b5a97ac2` | `15df9e306c2e0b43c30f85364edfbe9aadfc29e7` |
| `experiments/review/lspv5_450_def_facet_owner_audit.py` | `ae0fe358f6a00d2466429518d3c55d3875932252` | `82301b659592d5db7cefb2a22fe826c467a3eb2e` |
| `experiments/review/verify_lspv5_450_def_facet_owner.py` | `b99b1bd158dfce6d0bc2be959059e40de4e31e00` | `ea56579a50b8db7773bd124a836c4b43c324d8a0` |
| `experiments/review/verify_lspv5_450_def_facet_owner.mjs` | `22a8018e5dae2d73744e7e7730d6be2de88cc5f6` | `05b149480db9bae746f7f52460ce6b7c9a11da12` |
| `results/raw/arc/2026-11-08_1950_LSPV5_DEF_FACET_OWNER_AUDIT450_RAW.json` | `13837aa9c13aca059595ed83c246ae0be81966d0` | `f1fc3942df8ab4a1627b9952633c5a37f574dcc7` |
| `research/coordination/2026-11-08_1950_LSPV5_DEF_FACET_OWNER450_HANDOFF.md` | `6cb68a6bc13a0248ab71142fe4eeead240b86435` | `0a5b50017a378cb4f8135078fb571bae722e6ad5` |
| `research/main/outbox/2026-11-08_1950_LSPV5_450_PROOF2_DELTA.md` | `ae1177cd908e253ea89b2bcfd63e05a6bd1d97d0` | `e84eaea0e45100cc71434785a143deb0c8622d1a` |
| `research/main/outbox/2026-11-08_1950_LSPV5_450_MAIN_INSERTION_FALLBACK.tex` | `c47e9bfa4b817664a174e72c8ae11cbf743908d0` | `e1b5163e88028036a600dd5c264558dc31acf332` |
| `research/main/outbox/2026-11-08_1950_LSPV5_450_ISSUE3_OUTBOX.md` | `636b82158a09914f0383ff2d6d39436e8879ecc5` | `71f02f73b443bf6f084765e7e6bb2409faa1cb34` |

## Tracker transaction

- Complete current `proof2.txt` was fetched at blob `979d99acc6afd9b2363fea238f3737c74052a5fe`, length 598,750 bytes.
- `[P2-L5-450]` was absent, so the material delta was appended with expected-SHA concurrency control.
- Update commit: `b67da1c32dde95cd6f8808ed0f0659e23732debc`.
- Complete readback blob: `c04dbd25453a61259d33ccf8aa952a4925a55d7b`, length 600,387 bytes.
- Readback checks: `[P2-L5-450]` occurs exactly once; the entire 598,750-byte prior content is an exact byte prefix.
- `proof1.txt` was reviewed unchanged at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.

## Issue #3 and root-file status

- Issue #3 comment ID: `6731931727`.
- The comment-reactions endpoint resolved that ID successfully and returned an empty reaction list. A later full-thread fetch failed with `Transport closed`; this limitation is explicit and is not treated as successful full-thread readback.
- Root `main.tex` repeatedly returned blob `87081775f78ee61032a55abc8ffce806bedff245` with zero content bytes. It was not edited, because outside-marker byte preservation could not be proved. The proposed insertion is preserved in the immutable fallback above.

## Final executable verification

After publication, the producer and both independent verifiers were rerun from scratch. Python and Node each reported PASS with 8 original sources, 45 owned facets, 15 paid DEF nodes, 131 paid RES nodes, and zero historical raw DEF records. All declared hostile controls had already rejected in the published raw artifact. The producer records runtime/RSS metadata, so a later local regeneration is semantically identical but not byte-identical; the immutable published raw blob above is authoritative for this run.

## Open boundary

Historical accepted-byte DEF owner records and owner-qualified facet selectors remain unauthenticated. The proposed adapter is a distinct grammar, not a silent revision of historical `R_mix341`. The all-rule mixed lower bound, same-calculus noncircular B3 and P versus NP remain OPEN.
