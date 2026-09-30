# Hostile-control regression suite

Purpose: every candidate SAT invariant should be tested against easy families and representation changes before it is treated as a serious lower-bound candidate.

Initial mandatory controls:
- Horn / dual-Horn;
- 2-SAT / Krom;
- affine/XOR/Tseitin with Gaussian elimination;
- bounded treewidth / dynamic programming;
- variable renaming and complementation;
- padding and auxiliary variables;
- independent products;
- DEAD / COPY / DELAY / INTERP / RECOMP wrappers.

The starter `pnp_lab.cnf` module includes a matched-incidence construction: an all-negative Horn formula and an arbitrary signing can share the identical hypergraph and therefore the identical unsigned cut profile. This is a permanent regression test against raw-incidence transport measures.

See `tasks/TASK-002-hostile-controls.md`.
