# LSPV-5/408 handoff — affine terminal-cover retraction

**2026-11-07 03:56 PST | Route B red team**

## Actual advance

`[P2-L5-408]` proves in the separately specified binary-GF(2) calculus that a tree is unnecessary for the branch retraction: any finite complete cover by consistent affine contexts, with overlaps allowed, retracts a context-typed union of $q$ distinct paid inference nodes to a common-source refutation with at most $q+r$ paid nodes, where $r$ is the global rank of assumption linear parts. Sharing is charged once only for an immutable vertex with one ID, parent tuple, row and global tag. A selected set of terminal contexts must cover every assignment; this is the AND obligation.

The theorem is an upper-bound/retraction control supporting `[P2-C1]`, not historical R_mix341 authentication, not B3 and not a mixed lower bound. It strictly extends `[P2-L5-407]` beyond trees.

## Verification

- Exhaustive affine-cover enumeration for ranks 1--3: 16,452 subsets, 15,563 covers, 15,552 overlapping covers; every cover produced a contradictory basis of at most $r+1$ rows.
- Typed overlapping/reconvergent fixture: $q=12$, $r=2$, theorem upper bound 14; actual direct source proof 2 paid nodes retained as a legal shortcut.
- Eight negative controls rejected omitted AND region, wrong discharged row, tag mutation, duplicate ID, cycle/forward edge, forged rank, missing scope assumption and OR-only discharge.
- Independent Node replay: 46,812 checks PASS.
- Historical checker: NOT RUN; accepted bytes and exact historical weights remain OPEN.

Artifacts: report `research/main/2026-11-07_0356_MAIN_AFFINE_COVER_RETRACTION_REFEREE408.md`; producer `experiments/review/lspv5_408_affine_cover_retraction.py`; independent verifier `experiments/review/verify_lspv5_408_affine_cover_retraction.mjs`; raw `results/raw/review/2026-11-07_0356_LSPV5_AFFINE_COVER408.json`.

## Tracker disposition

`proof1.txt` reviewed: no material change. `proof2.txt`: add `[P2-L5-408]` and a `[P2-C1]` evidence line. Affected IDs to post on issue #3: `[P2-L5-408]`, `[P2-C1]`; predecessor `[P2-L5-407]`.

## Next gap

Authenticate exact historical R_mix341 byte grammar and weights for the tag-preserving XOR transformation, source provenance and final joins, or provide a legal accepted-byte counterexample. Full mixed `[P2-C1]`, `[P2-C3]`, `[P2-D1]`, all-mixed superpolynomial $\overline W_R$, noncircular B3 and P versus NP remain OPEN.
