# CERT-GENERATOR-COMPRESSIBILITY77 (hourly-check note)

**Global status: P versus NP OPEN; P versus RP OPEN. Root main.tex not modified.**

Follow-up to TWO-LABEL-CERTIFICATE-ENVELOPE76 (its :00 row: compute KT-proxy for explicit certificates; reject materialized-length arguments if a short generator exists).

## Experiment (COMPUTATIONAL, tiny scale)
`experiments/review/2026-10-22_certificate_generator_compressibility77.py` -> `results/2026-10-22_certificate_generator_compressibility77.json`.
Explicit DPLL refutation-tree traces (unit propagation, fixed variable order) for PHP_n^{n+1} (n=3..7) and random 3-CNF at ratio 5.0 (20..50 vars, 3 seeds); lzma/zlib size as crude upper bound on description length. One invocation, ~seconds (node budget 60,000; PHP_7 hit budget, so it is a truncated trace).

## Result
- PHP lzma/raw ratio: 2.55, 0.64, 0.19, 0.064, 0.024 for n=3..7. Raw length grows ~8-9x per n; compressed grows ~2-3x.
- Random 3-CNF trace ratio also falls with size (1.5 -> ~0.2 at 50 vars).
- Compressibility does **not** separate the structured family from random instances at these sizes; both traces are self-similar tree preorders.

## Interpretation (strict)
- Supports ENVELOPE76's point: explicit certificate length is not evidence of HIGH ordinary KT. Reinforces RETIRED status of "materialized length as the HIGH-side argument".
- Also shows generic compressors are a poor discriminator; a meaningful KT test needs the indexed generator plus random-access time, as ENVELOPE76 specifies. Not done here.
- No claim about asymptotics, no bearing on any load-bearing OPEN arrow (all-input hereditary semantic compression). Status: COMPUTATIONAL only.
