# ARC-LINEAR22-SATURATION1 reproducibility package

This package contains a new **restricted-model construction** for the P versus NP ARC/FLMV research program. P versus NP and the all-input ARC transformation remain OPEN. The theorem is about a specific signed exact-(2,2) source family and specified compression algorithms, not all SAT machines.

## Run standard-library checks

All Python files must be in the same directory. Python 3.9+ recommended.

```bash
python arc_linear22_mini.py
python arc_linear22_projection_firewall.py
python arc_linear22_dp_reentry.py
python arc_two_pivot_lookahead.py
python arc_linear22_signed_relabel_audit.py
python arc_linear22_canonical_contractor.py
python arc_mixed_projection_test.py
```

The independent colored graph-isomorphism check requires NetworkX:

```bash
python -m pip install networkx
python arc_signed22_gi_control.py
```

This finite checker uses NetworkX VF2. Its empirical running times are **not** the polynomial-time theorem; the theorem invokes Luks's bounded-degree GI result.

## File contents

- `ARC_LINEAR22_PROJECTION_FIREWALL_2026-10-30.tex` and `.pdf`: complete formal report, source evidence, scoped statements, limits and bibliography.
- `arc_linear22_mini.py`: independent standard-library exact local certificate.
- `arc_linear22_projection_firewall.py`: exact signed 3-partite formula, per-pivot normalized DAG counts, sampling.
- `arc_linear22_dp_reentry.py`: four exact width-four resolvents and proper-3CNF reentry with complete local truth checks and two bit-length contracts.
- `arc_two_pivot_lookahead.py`: all two-variable cofactor alternatives at k=7,9,11 and independent semantics samples.
- `arc_linear22_signed_relabel_audit.py`: six arbitrary signed renaming, clause-order, literal-order controls.
- `arc_signed22_gi_control.py`: the colored trivalent signed-port graph and satisfying-witness transport.
- `arc_linear22_canonical_contractor.py`: explicitly authenticated one-child terminal for the canonical all-SAT grammar, with negative controls.
- `arc_mixed_projection_test.py`: broader exploratory baseline, including balanced strict22 and ordinary random CNFs.
- `*_results.json`: raw finite outputs for each script.

Do **not** interpret code-level gate-call counts as physical FLMV machine steps or total simultaneous live memory. The original input remains read-only, output bit length is charged, and the model language is explicitly declared. The first-pivot theorem survives signed renaming, but no unconditional runtime lower bound follows.
