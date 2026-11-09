# LSPV-4/506 publication and readback receipt

**2026-11-08 17:36 PST | Route A | P versus NP OPEN**

Authoritative main artifacts, all refetched after create-only commits with exact nonempty UTF-8 content:
- Report `research/agents/lspv-4/2026-11-08_1736_LSPV4_CRITICAL_SIGN_CACHE_STAR506.md`, blob `0a3f8d4e9d01239706407eb1c43e9d8242640e35`, 15,771 characters, commit `a327fe46e20105627b2e142b7b1dda9d163c57aa`.
- Standalone independent V8 `experiments/arc/lspv4_506_critical_cache_star_independent.cjs`, blob `1e78903bcbae27fb9ce3ecb4fbbc0baf136dc036`, 1,621 characters, commit `e7d2a93c0e5ff140a2788107fdd458217128f09c`. Exact published bytes were reexecuted in V8 and PASS: 72 K3,3 SAT mutants, 128 permutations, exact sum 2,628.
- Raw `results/raw/arc/2026-11-08_1736_LSPV4_506_CRITICAL_CACHE_STAR_RAW.json`, blob `167147da1ede0d2a80115d544e9cf9256487168d`, 2,166 characters, commit `6e65a25138a27ba8366f75d20862ca88b7f3a6e1`.
- Handoff `research/coordination/2026-11-08_1736_LSPV4_CRITICAL_CACHE_STAR_FIVE_ROLE_HANDOFF506.md`, blob `e4198ee0797b1f2ddf5a61dada52811c9689e36d`, 3,103 characters, commit `3a9dafe8cb6ba922db80decd4c50c236ae901ce8`.

Root trackers were both completely fetched and inspected. `proof1.txt` unchanged: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters. On `proof2.txt`, old complete blob `b20f53cccf5c7347b2a9f2da782a457e46172812`, 570,059 characters, was used as expected SHA. A conflict-guarded append added exact node **[P2-L4-506]** without modifying the old prefix, resulting in blob `d40b17bd67d560eac034ef1dfe5a405368478f22`, 573,232 characters, commit `a86389a4fdbfc1dbf7dbb7b0c5ee5b5ed51c647d`. Exact complete-content comparison and blob-SHA comparison PASSED after write, then both root trackers were independently rechecked once more.

Issue #3 post: https://github.com/j15marti/pnp/issues/3#issuecomment-6730403869 . Full comment-body equality and ID readback PASSED.

Independent Python code SHA-256 `359a32ccf7ee565cac5a9f0e3843226b390adb150ff377b3e840d849a246e151`; raw Python output SHA-256 `593e4c52f064fc1e7d3875e3ddba1cdd5b6b50212dff25803d7fab48310da201`; deterministic second Python execution exactly matched original output. A local zipped standalone reproducibility archive `LSPV4_506_CRITICAL_CACHE_INDEPENDENT_REPRO.zip` passed ZIP integrity tests, SHA-256 `a852c2f8df972e8b9b60d9f434839d7431ff54428f7f0b2aae0b60b2c5dad60d`.

**Explicit blocker:** Root `main.tex` GitHub fetch identified blob `42fd637c90bb8eec6b7a8e181990c6650b725fd2` but returned **zero bytes**. Its full contents and LSPV-4 ownership markers could not be authenticated, so no root manuscript modification was attempted. Reports, code, tracker and issue update succeeded without this unsafe write. Hosted tests are not a native FLMV checker or historical R_mix341 checker.

Five existing agent IDs, titles, schedules, enabled states, Route A/B allocation (two A and three B), old work/space conventions and historical R_mix341 grammar and weights remain unchanged. Status: scoped [P2-L4-506] PROVED/RESTRICTED and COMPUTATIONAL, [P2-A2]/[P2-A4]/[P2-A5], Route B transfers and P versus NP OPEN.
