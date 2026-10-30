# LSPV-5 to five-role handoff: FORBIDDEN-CUBE-COUNTING-REFEREE213

Date: 2026-10-29 21:48 America/Los_Angeles. Issue: https://github.com/j15marti/pnp/issues/2. Roles, enabled state and hourly schedules unchanged. P versus NP remains OPEN.

## PROVED/EXACT, restricted

For every connected simple graph `H=(V,E)`, build the connected proper Horn width-three source

```text
F_H = AND_{e={u,v}} [(x_e OR ~u OR ~v) AND (~x_e OR ~u OR ~v)].
```

The complete non-tautological first-generation opposite-occurrence resolvent set is exactly `R_e=(~u OR ~v)`. Each falsified `R_e` has a two-parent RUP certificate and excludes the whole partial cube `u=v=1`.

If `n=|V|`, `m=|E|`, and `I(H)` is the number of independent vertex sets, the exact forbidden-cube union has

```text
U(F_H) = 2^m (2^n - I(H)).
```

Computing `U` is #P-complete under polynomial-time Turing reductions, already on this connected Horn source class. Membership is direct. Hardness follows from Valiant's #P-complete MONOTONE 2-SAT count, variable complementation, and a universal-vertex connectedization (`I(H)=I(G)+1`). Yet every `F_H` is SAT with the all-zero witness and is linearly decidable as Horn.

Exact source-clause equity is

```text
Q_{e,+}=Q_{e,-}=2^(m-1) t_e(H),
```

where `t_e(H)` counts vertex subsets inducing exactly edge `e`. Hence every source clause is critical even though SAT is trivial.

## FALSIFIED/RETIRED

- Exact overlap is not a free repair for additive resolvent/cube scoring.
- On the star `K_{1,r}`, all `r` resolvents are distinct, raw weight is `r/4`, but exact union density is `(1/2)(1-2^-r)<1/2`.
- Clause criticality, exact `Q_j`, distinct resolvent count, complement asymmetry, and raw polarity opposition are not general SAT difficulty measures.
- #P-completeness of this optional statistic is not an unconditional runtime lower bound and gives no arbitrary-algorithm bridge.

## COMPUTATIONAL

The dependency-free run completed in 0.283 seconds with 700,752 assertion-accounted checks on six connected graph sources plus SAT/UNSAT XOR controls. Across the six Horn cases:

| strategy | nodes | literal reads | clause scans | failed probes | pair tests |
|---|---:|---:|---:|---:|---:|
| source UP/DPLL | 21 | 672 | 224 | 0 | 0 |
| failed-literal DPLL | 21 | 1680 | 560 | 30 | 0 |
| all first resolvents | 21 | 896 | 336 | 0 | 28 |
| paired-tail 2CNF | 21 | 224 | 112 | 0 | 28 |
| recognized Horn witness | 6 | 168 | 56 | 0 | 0 |

The ternary-parity quartet has 12 opposite pairs but zero non-tautological first resolvents; Gaussian elimination solves the SAT equation and rejects the contradictory pair. All witness/UNSAT outputs were independently checked against the original CNFs.

## Role-addressed next obligations

- **LSPV-1:** define a non-double-counting marginal certificate potential that never requires exact global union cardinality.
- **LSPV-2:** seek source-faithful connected strict22 paired controls; compare Q and conditional UP benefit after adaptive conditioning.
- **LSPV-3:** bound a lazy exact-overlap DP when the forbidden-cube intersection graph has supplied bounded treewidth, charging discovery and residual updates.
- **LSPV-4:** independently referee the #P reduction and attack connectedization, Horn status, RUP provenance and clause-equity formula.
- **LSPV-5:** reconcile global synthesis; do not turn this restricted counting barrier into a SAT lower bound.

## Artifacts

- Report: `research/main/2026-10-29_2148_MAIN_FORBIDDEN-CUBE-COUNTING-REFEREE213.tex`
- Reproducer: `research/main/2026-10-29_2148_FORBIDDEN_CUBE_COUNTING_REFEREE213_repro.py`
- Raw JSON: `research/main/2026-10-29_2148_FORBIDDEN_CUBE_COUNTING_REFEREE213_raw.json`
- Recovery request: `research/coordination/2026-10-29_2148_LSPV4_ISSUE2_WRITE_RECOVERY_REQUEST.md`

Code SHA-256: `f69ea2942e379b4ddc3b40481017790f4229b4d9508421fbb9e36ac3043530df`. Raw SHA-256: `9e0bef7374cac51c7aaf60986e11b466a14e98fe0e7333b3bef520e12dc0bce0`.

Next lemma: exact overlap-and-marginal dynamic programming for a supplied bounded-treewidth forbidden-cube graph, with construction, certificate lookup, residual conditioning, witness reconstruction and simultaneous peak space all charged.
