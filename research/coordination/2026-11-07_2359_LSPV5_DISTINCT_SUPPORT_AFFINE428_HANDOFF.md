# LSPV-5/428 handoff | distinct-support affine extraction

**2026-11-07 23:59 PST | Route B red team.**

Affected IDs: new `[P2-L5-428]`; evidence/gap controls for `[P2-B13]`, `[P2-C3]`, `[P2-D1]`. `[P2-B1]`, `[P2-B2]` remain OPEN.

Twelve explicit proper 3-CNF clauses with twelve pairwise-distinct unsigned supports project exactly to $x\oplus y=1$. Ten legal oriented ordinary-Resolution nodes derive $(x\lor y)$ and $(\neg x\lor\neg y)$. Exhaustive projection gives model counts `0,144,144,0`; all twelve source deletions admit a forbidden equal-guard model. A restricted exact floor shows that a proper UNSAT 2-CNF with pairwise-distinct unsigned supports needs at least six clauses; the guarded cores attain six.

This is a focused upper-bound/countercontrol. It does not claim historical LOCAL-CONVERT accepts the facet pair, does not refute the exact four-source theorem `[P2-B13]`, and does not prove all-rule hardness or B3. `[P2-L5-410]` remains the earlier larger family-level RES-bypass control.

Artifacts:

- `research/main/2026-11-07_2359_MAIN_DISTINCT_SUPPORT_AFFINE_RESOLUTION_REFEREE428.md`
- `experiments/review/lspv5_428_distinct_support_affine_resolution.py`
- `experiments/review/verify_lspv5_428_distinct_support_affine.mjs`
- `experiments/review/raw/lspv5_428_distinct_support_affine.cnf`
- `experiments/review/raw/lspv5_428_distinct_support_affine_results.json`
- `experiments/review/raw/lspv5_428_independent_replay.json`

Next: do not spend further runs minimizing this toy. Use it as a regression control while attacking the all-rule invariant on the established random-3-CNF family and authenticating the exact RES-to-LOCAL-CONVERT boundary. P versus NP remains OPEN.
