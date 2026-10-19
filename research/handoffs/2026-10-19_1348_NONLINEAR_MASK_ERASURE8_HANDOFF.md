# NONLINEAR-MASK-ERASURE8 handoff | 2026-10-19 13:48 KST

## Exact result

The MASKED-PARITY-SHEAR8 triangular map is bijective. For every actual cube instance (`M>=12`) its last output has ANF degree `M-2`, but composing it with the connected `Q_d` incidence system preserves the decision `SAT iff XOR(b)=0` and the `2^(M-V+1)` edge-preimage count. With the padded proper-AND encoding, total models are `2^(M-V+1+2(M-2))`.

The same charge circuit has macro counts `G=V, E=W=2V, depth=d+1` and NAND2+INV-expanded counts `G=4V-3, E=8V-6, W=5V-3, depth=3d+1`, with identical nominal MOS `16(V-1)+2`. Preserve both ledgers; never mix them in a slope.

## Passed audit

32,760 exhaustive inverse assignments; 20 symbolic ANF instances; 40 proper-gate truth assignments; all 4,096 `Q_3` edge assignments; 75 ledger identities. The `n=3` degree formula is an explicit exception outside the reported `M>=12` range.

## Hard failures / unknowns

- Shared specialist kernel does not contain the full CNF generator/validator claimed in the report.
- Validator live memory is an uninstrumented upper bound.
- Raw/projection/SAT toggle traces use different domains and stimuli.
- Routed length, placed area, transistor nets and measured energy remain NULL.
- None of this transfers to arbitrary-machine Circuit-SAT or SAT lower bounds.

## Next tests

- Physical: matched placement/routing at `d=5..7`.
- Quotient: full validator with single-record adversarial mutations and access trace.
- Experiments: paused.
- Red team: promised-image collision or charge-changing mutation.
- Synthesis: retain same-function/library/model comparison guard.

P versus NP remains OPEN.
