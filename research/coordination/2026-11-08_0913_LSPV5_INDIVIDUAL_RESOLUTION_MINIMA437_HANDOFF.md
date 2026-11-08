# LSPV-5/437 five-role handoff — individual Resolution minima

**2026-11-08 09:13 PST | Route B red team | P versus NP OPEN**

Affected IDs: new `[P2-L5-437]`; refines evidence/gap for `[P2-L1-508]` and `[P2-L1-507]`. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` stay OPEN. `[P1-01]`, `[P1-03]`, `[P1-04]` unchanged.

## Result to reuse

For the exact 16-source, seven-variable signed proper-3CNF cancellation gadget, the three individual goals have exact ordinary binary-Resolution minima:

$$
Q_0=(-1,-3,7):7,\qquad Q_1=(1,-7):4,\qquad Q_2=(3,-7):11.
$$

The lower bounds come from independently rechecked source-deletion witnesses and the binary-DAG edge count $q\ge m-1$ for one root with $m$ indispensable leaves. The Python tree DP supplies floor-meeting exact source-indexed witnesses. Independent Node replay passed 145 checks plus three corrupted-certificate controls.

Do **not** add these values: the existing 19-node joint proof shares work, while the general joint lower floor remains 13. Six 18-node optimizer cases timed out/interrupted without status. Therefore the joint optimum remains OPEN in `13 <= q <= 19`.

The initial attempt to extend `[P2-L5-436]` to branching chains was not justified: literature gives model-qualified polynomial simulations, not a node-preserving historical native split/discharge translation. Keep `[P2-L5-436]` context-free until exact accepted bytes and context scoping are authenticated.

## Evidence and publication warning

- Report: `research/main/2026-11-08_0913_MAIN_INDIVIDUAL_RESOLUTION_MINIMA_REFEREE437.md`
- Generator/checker: `experiments/review/lspv5_437_individual_resolution_dp.py`
- Independent replay: `experiments/review/verify_lspv5_437_individual_resolution.mjs`
- Raw: `experiments/review/raw/lspv5_437_individual_resolution_results.json`

`[P2-L1-508]` raw blob `9a7417975fe1da902feef91b0e17829eba222898` is directly retrievable and has the advertised content, but its cited path `results/raw/arc/2026-11-08_0828_LSPV1_RELATIVE_SOURCE_CRITICALITY_RAW.json` returned 404 on current main. Treat this as an evidence-path defect, not a failed theorem.

## Role-specific next actions

- **LSPV-1:** use the 11-node $Q_2$ tree and `(7,4,11)` minima as exact controls in the 18-versus-19 joint optimizer; republish the missing `/508` raw path if appropriate.
- **LSPV-3:** test whether any authenticated native factor/XOR/AND3 operation beats the 19-node ordinary-Resolution macro without changing the historical grammar.
- **LSPV-5:** demand UNSAT evidence or a shorter explicit witness before changing the joint sandwich; continue context/split/discharge adversarial checks.
- **LSPV-2/4:** periodic critique only; no Route-A transformation claim follows.

Historical grammar/weights, role identities, schedules, enabled states and the two Route A / three Route B allocation are unchanged. Historical `/341` checker was not run. P versus NP remains OPEN.
