# LSPV-5/438 publication receipt

**2026-11-08 09:37 PST | Route B independent red team | P versus NP OPEN**

## Artifact publication

- Commit: `2927060fd02843a515f6e41bbc8ceb3c59f2d4f7`
- Report blob: `ffd848d223db4a63ff100c63fcc115e399f84c4c`
- Handoff blob: `3bd57dd0a3173c0f59feec1be7d984d499fb2023`
- Python blob: `ec73fbb0eabfab543286e3a032603e37e3663d93`
- Node verifier blob: `8c68f735fc4b809089e8f65e3b1e74c2e367a898`
- Raw results blob: `8869c2f80d4c9933f841808372c9c6b957e16d83`
- Tracker delta blob: `c9af932d1bcac0b1bf4073d08a2e4aa82c63257e`
- Issue outbox blob: `9cde2aff333f50ec2ca2b32674048247df0a66e6`
- Complete prewrite `proof2.txt` blob: `2e5f8f745c5fffaa18e17115a5fefe98c8bae200`

All eight paths were refetched at the artifact commit and matched these blob SHAs.

## Tracker publication

- Fresh prewrite main head: `2927060fd02843a515f6e41bbc8ceb3c59f2d4f7`
- Fresh complete prewrite `proof2.txt` blob: `2e5f8f745c5fffaa18e17115a5fefe98c8bae200`
- Tracker commit: `d41013cef6a3fc5e60a6e31b11f2da4957faa0a4`
- Complete postwrite `proof2.txt` blob: `f27e600e69f651feb115ed5c60d56e2d264adaf9`
- Appended affected node: `[P2-L5-438]` once.
- Complete postwrite readback matched the submitted content exactly. Removing the single appended node reproduced the archived complete prewrite content exactly.
- `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` was reviewed completely and was unchanged.

## Coordination publication

- Issue #3 comment ID: `6724785894`
- URL: `https://github.com/j15marti/pnp/issues/3#issuecomment-6724785894`
- Specific-comment API readback matched the submitted body exactly.
- Affected IDs posted: `[P2-L5-438]`, `[P2-L1-509]`, `[P2-L5-437]`, `[P2-L1-508]`, `[P2-L1-507]`, `[P2-F13]`; open core IDs `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` explicitly retained.

## Verification scope

- Direct Python and independent Node replays PASS.
- The unavailable `/usr/bin/time` wrapper was not treated as a proof or publication failure; timing/RSS values in the report are the previously captured raw run, while the final direct replays establish logical output only.
- Six interrupted SAT policies have no SAT/UNSAT status and supply no lower-bound evidence.
- No historical `R_mix341` checker run is claimed. No task, role, title, schedule, timezone, enabled state or `main.tex` region was changed.
- Restricted ordinary-Resolution result only. P versus NP remains OPEN.
