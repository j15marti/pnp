# PRIME-MULTISIGN-DAG1 n=5 results

Status: COMPUTATIONAL finite experiment. P versus NP remains OPEN.

Model:
- n=5.
- Exact signed width-3 clause universe has 80 clauses.
- Fixed clause order.
- At each layer a state may skip or include the next clause.
- Each included clause has its own unique prime, so the product is an injective square-free identifier of the selected-clause history/set in this fixed order.
- Semantic state is the exact 32-bit satisfying-assignment mask of the conjunction.
- For future conjunction by arbitrary clauses, equality of semantic masks is an exact context-sufficient quotient. This is a diagnostic model, not an unrestricted hypergraph-DAG minimum.

Observed layers:
depth | prime states | semantic/context classes | log2 classes
1 2 2 1.000000
2 4 4 2.000000
3 8 8 3.000000
4 16 16 4.000000
5 32 32 5.000000
6 64 64 6.000000
7 128 128 7.000000
8 256 256 8.000000
9 512 448 8.807355
10 1024 640 9.321928
11 2048 1120 10.129283
12 4096 1600 10.643856
13 8192 2800 11.451211
14 16384 4000 11.965784
15 32768 7000 12.773139
16 65536 10000 13.287712

Findings:
1. Prime labels retain all selected-clause information exactly.
2. The first semantic collisions in this ordering occur at depth 9.
3. By depth 16, 65536 prime-labelled states quotient to 10000 semantic masks, a 6.5536-to-1 average syntactic/semantic ratio.
4. Therefore raw prime-history count is not a lower-bound resource. Legal semantic quotienting discards substantial prime information.
5. The contextual class count itself continues to grow in this finite prefix, but this is not an asymptotic theorem and not an unrestricted DAG lower bound.
6. Parity is a hostile control: its residual contextual state can collapse to two parity classes despite depending on all variables. Small contextual quotient is compatible with easy global algebraic structure.
7. Next target should compare exact contextual-class growth under multiple clause orders and controls, and test whether any lower envelope survives Horn, 2-SAT, affine/Tseitin, independent products, bounded treewidth, renaming, and source-legal recomputation.

Guard:
This experiment does not establish that a machine must materialize either the prime product or the semantic mask. INTERP/RECOMP and compact evaluators remain valid attacks. SAME_REALIZATION acquisition and ordinary-CNF SAT return remain OPEN.
