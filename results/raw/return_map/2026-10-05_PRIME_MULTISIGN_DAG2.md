# PRIME-MULTISIGN-DAG2 lower-envelope hostile controls

Status: COMPUTATIONAL finite evidence only. P versus NP remains OPEN.

Model: n=5. A DAG state is the exact satisfying-assignment mask of the conjunction selected so far. Unique prime labels identify syntactic selected-constraint histories; semantic masks quotient histories that are indistinguishable under all future conjunctions. Eighty deterministic random orders per family. Seed family begins 20261005/271828. Depth 16 where available.

Depth-16 semantic-context classes:

| family | min | median | mean | max |
|---|---:|---:|---:|---:|
| generic signed 3-clause universe | 6878 | 14566 | 15242.52 | 30912 |
| planted-TRUE 3-clauses | 6883 | 13611 | 13976.58 | 22176 |
| Horn exact-3 clauses | 3274 | 6046 | 6362.85 | 13128 |
| bounded-treewidth-like windowed exact-3 | 12648 | 21244 | 20837.65 | 30728 |
| native 2-SAT constraints | 1966 | 3929.5 | 3945.70 | 5354 |
| native XOR pair/triple constraints | 451 | 623 | 629.24 | 754 |
| native independent-product 2-CNF blocks | 2476 | 2476 | 2476 | 2476 |

Findings:
1. Generic 3-CNF has a larger sampled lower envelope than Horn, 2-SAT and XOR in this finite test.
2. This is NOT a hardness separator: the bounded-treewidth-like easy control has an even larger quotient than generic 3-CNF.
3. Therefore raw contextual-class count I=log2(classes), even after sampled clause-order minimization, is FALSIFIED as a standalone hardness measure.
4. Prime labels remain useful instrumentation: they distinguish syntactic/history states before exact semantic quotienting.
5. Any surviving invariant must minimize over representation/decomposition as well as order, or charge a source-matched obstruction to compact recombination. Treewidth/affine algorithms show that large semantic-mask diversity can coexist with easy SAT.
6. No asymptotic conclusion follows from n=5 or from sampled rather than exhaustive order minimization.

Next candidate:
PRIMEDAG3 should compare quotient size with the size of the smallest known compact combiner representation for each family, e.g. affine rank for XOR and separator/table width for bounded-treewidth instances. Candidate quantity is not raw class count but excess contextual diversity beyond a compact source-matched representation. This must still survive INTERP/RECOMP and arbitrary-algorithm transfer.
