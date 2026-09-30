# TASK-001 — Exact SU/vMS Boolean product span

## Objective

Determine, for one exact successful SAME_REALIZATION final construction,

`rho(E_H) = dim_F2 span{1, g_i, g_i g_j}`.

This is currently the highest-value falsifiable structural arrow in the project.

## Non-negotiable source rule

Do **not** implement a schematic Reed–Muller / orbit-window surrogate and call it SU/vMS.

Before coding the exact mode, identify and record:
1. the exact generator theorem/definition;
2. the field/vector-space identification;
3. the exact binary encoder;
4. every Boolean projection;
5. the local extractor/query algorithm;
6. all adaptive query dependencies;
7. the final output-coordinate definition.

If any item is missing from the repository/source package, open a task note identifying the exact missing definition and stop that branch.

## Deliverables

- exact source transcription with theorem/page identifiers;
- implementation in `src/pnp_lab/su_vms/`;
- hand-checkable unit tests on the smallest legal parameters;
- exact Boolean coordinate truth tables for the smallest feasible cases;
- ANF degree of every final coordinate;
- exact `rho(E_H)`;
- one explicit independent minor or one explicit sparse quadratic relation when present;
- raw JSON outputs under `results/raw/product_span/`;
- LaTeX interpretation under `research/agents/` or `research/explorations/`.

## Falsification-first questions

- Does adaptivity raise Boolean degree enough to make product span quadratic?
- Is apparent low rank destroyed by a legal encoder/message relabeling?
- Can an `Omega(m^2)` independent minor be found at small legal parameters?
- Are observed low ranks merely finite-parameter accidents?

## Status discipline

Finite ranks are `COMPUTATIONAL`.
A general `O(m)` statement is not PROVED without a symbolic all-parameter argument.
