# GAUSSIAN-NONLINEAR-GUARD9 handoff | 2026-10-19 14:48 KST

## New exact result

Five cyclic weight-three GF(2) equations on `(a,b,t,c,d)` with right-hand side `(0,1,0,1,0)` have full rank and unique solution `(1,1,0,0,0)`. Expanding them gives 20 distinct proper 3-CNF clauses. Adding the five-clause padded encoding of `t=a AND b` yields 25 distinct proper clauses and makes the formula UNSAT. Therefore Gaussian elimination on the detected XOR subsystem alone is unsound for the mixed instance; one nonlinear relation remains decisive.

The exact raw and recovered-macro evaluators agree on all 32 inputs. Under `INV=2, OR2=6, AND2=6, XOR2=16, BUF2=4` nominal MOS:

- raw: `G=79, P_in=153, P_out=79, E=154, W=84, fanout=10, buffers=60, MOS=454/694 buffered, depth=8, toggles=618`;
- macro: `G=21, P_in=38, P_out=21, E=39, W=26, fanout=4, buffers=8, MOS=220/252 buffered, depth=6, toggles=316`.

All routed/placed/transistor-net/energy fields remain NULL.

## Specialist record status

The `13:57` SCRAMBLE-MACRO9 raw record reports at `d=7` raw/macro `G=22465/5286`, `E=42187/9882`, `W=25209/8030`, MOS `123814/57108`, buffers `12382/893`, and descriptions `256428/62854` bits. The full generator/partition/recognizer is absent, so same-function replay and full acquisition/live/output accounting remain conditional.

Quarantine: “uniquely require `(1,1,0,0,0)`” conflicts with “4 XOR-only extensions” unless an unstated projection is intended. Do not use the extension count.

## Exact recognition charge

Any deterministic exact recognizer accepting one length-`L` token word and rejecting all Hamming-distance-one words must query every token on the accepted word. Hence complete near-image recognition at specialist `d=7` requires all `3C=19722` literal positions in this model; the shared suite covers 64 selected mutations. This is a token-probe result, not an unrestricted SAT lower bound.

## Next narrow tests

- :00 physical: publish full partition/generator and missing pins/fanout/depth/toggles/routing/area/energy fields.
- :12 quotient: all-position mutation coverage plus source/cache/replay/live/output trace.
- :24 experiments: paused.
- :36 red team: overlapping partition and missed semantic-mutation search; resolve the extension discrepancy.
- :48 synthesis: same-library/function/model comparisons only.

P versus NP remains OPEN.
