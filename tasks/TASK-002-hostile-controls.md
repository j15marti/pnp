# TASK-002 — Hostile-control regression suite

## Objective

Build a reusable automated falsification suite for every candidate invariant, decomposition measure, battery, or source-cost proposal.

## Required controls

At minimum:
- Horn and dual-Horn;
- 2-SAT;
- affine/XOR/Tseitin solved by Gaussian elimination;
- bounded-treewidth CNFs;
- renamable Horn;
- variable permutations and complementations;
- padding / duplicate clauses / auxiliary-variable encodings;
- independent products;
- DEAD, COPY, DELAY, INTERP, RECOMP wrapper-equivalent implementations.

## First exact regression

For a fixed 3-uniform hypergraph H construct:
- the all-negative Horn formula on H;
- multiple generic signings on the same H.

Verify automatically that every unsigned incidence cut profile is identical while tractability can differ drastically.

Any invariant depending only on unsigned incidence geometry must therefore be rejected as a universal SAT-time resource.

## API target

Expose a small interface such as:

```python
result = evaluate_invariant(formula, trace=None, representation=None)
run_hostile_suite(result_or_callable)
```

The suite should return the smallest discovered counterexample and the transformation that broke the proposed invariant.

## Deliverables

- generators under `src/pnp_lab/controls/`;
- tests;
- reproducible seeds;
- counterexample minimizer where practical;
- JSON result schema;
- short LaTeX report template.

Do not infer asymptotics from random testing.
