# CONSTRUCTION-STRENGTHEN13 | 2026-10-29 16:48 PDT

Implemented charged adaptive pair merging over the original CONSTRUCTION12 source-module compiler. Every candidate full compilation, failed scope scan and losing candidate is charged. Neutral moves use a decreasing module count, with no resets and at most m rounds. Polynomial acquisition under w=O(log N) does not imply a polynomial final solve.

Exact first-move obstruction: distinct-clause strict22 gives four separate clause occurrences per variable, so a two-clause module has no private variables. Pair support sizes are 6, 12/13, 24/25, or 49 according to union scope size 3/4/5/6; none is affine, and at least two tuples are forbidden. Therefore strict defect-improving pair merging cannot start on ANY such source. Modules with at most three clauses cannot be affine or hide original variables. Independent mathematical referee pending.

Repair: allow equal-defect merges. This crosses the isolated four-clause XOR plateau. Among 48 connected strict22 cases (all SAT), 47 have distinct clauses and all 47 stall under strict policy; neutral policy improves one such source from d=8 to d=6. One duplicate-containing source improves from 8 to 7 under both. Aggregates strict/neutral: final defects 479/477 from 480; candidate compilations 1719/2562; assignment trials 162792/233904. More discovery cost prevents claiming a total speedup. Nine chunks each below 25 seconds; all checks pass. Opposite XOR ordinary-CNF UNSAT control passes; no tested strict22 UNSAT coverage is asserted.

Precedence: CONSTRUCTION12 supplies compiler and terminal; EARLY-AFFINE19 already uses affine inclusion-exclusion. ARC234 and RANK-SWITCH168 supply complementary decomposition/accounting context. No root main.tex edits. main4/main5 receive additive entries.

Proof status: restricted derivations and computational evidence; all-input small defect, favorable ARC and P versus NP OPEN. Conditional K elimination preserved.

Next: charge bounded four-module lookahead or occurrence-closure scoring; judge discovery plus solve, not defect alone. Do not restore strict pairwise local descent as a universal rule.

