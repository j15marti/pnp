# LSPV-5/438 handoff: terminal overlap and minimum-tree sharing

**2026-11-08 09:31 PST | Route B independent red team | P versus NP OPEN**

## Material result

- Independently replayed and reimplemented `[P2-L1-509]`: for the exact 16-source cancellation gadget, the indispensable-source overlap graph for the three goals is connected. Any pruned context-free source-authenticated binary shared DAG deriving all three goals has at least 15 derived nodes. Together with `[P2-L1-507]`, the current ordinary-Resolution joint range is `15..19`.
- Exact tree-closure enumeration proves a stricter but deliberately restricted statement: individually minimum Resolution trees for the three goals can share at most one derived node in total, so their union has at least `7+4+11-1=21` derived nodes. The known 19-node joint proof escapes because its Q2 cone is not individually minimum and reuses Q1 work.
- This supersedes only the `13..19` joint-range sentence in `[P2-L5-437]`; its exact individual minima `(7,4,11)` remain valid.

## Verification

- `experiments/review/lspv5_438_terminal_overlap_redteam.py`: 128 assignments, 35 exact candidate macro clauses and 266,799 aggregate tree-closure states; recorded 3.51 s and 21,672 KiB maximum RSS.
- `experiments/review/verify_lspv5_438_terminal_overlap.mjs`: independent Node implementation; 12 aggregate assertions and three hostile controls PASS in 9.97 s.
- Exact `/509` JavaScript blob `8092730781f1d0787d509800c8ff7e663bdcb425` replayed with 485 checks PASS.
- Six 15-node SAT cases (3,675 variables, 49,449 clauses each) were interrupted without status and are failed search policies, not lower-bound evidence.

## Next work

1. Decide the 15--18-node ordinary-Resolution cases with a complete proof-line-symmetry treatment and independently checkable SAT/UNSAT evidence.
2. Adversarially test nonminimum cones and source fan-out, since the minimum-tree obstruction does not cover them.
3. Authenticate the exact historical native RES/LOCAL/DEF/split/discharge grammar and accepted trace bytes before any mixed-calculus transfer claim.
4. Keep `[P2-B1]`, `[P2-B2]`, `[P2-C3]`, and `[P2-D1]` OPEN. Restricted Resolution evidence does not resolve P versus NP.
