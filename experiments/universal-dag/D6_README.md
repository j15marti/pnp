# D(6,8), with D(5,8) and D(4,8) controls

Simple genuine 3-CNF: eight distinct clauses, three distinct variables per clause.
The n variables are the available universe; unused variables are allowed. Clause
IDs enumerate variable triples in lexicographic order, then falsifying patterns
0..7. This is a coordinate permutation of the earlier n=4 encoding.

## Verified results

| n | Possible clauses | All formulas | UNSAT | UNSAT using all n variables | Best tested query DAG | Shared circuit gates |
|---|---:|---:|---:|---:|---:|---:|
| 4 | 32 | 10,518,300 | 272 | 268 | 508, prior run | 64, prior run |
| 5 | 80 | 28,987,537,150 | 4,380 | 3,030 | 13,147 | 256 |
| 6 | 160 | 8,917,061,687,820 | 30,020 | 7,800 | 50,460 | 720 |

The new n=5 and n=6 query DAG bounds are heuristic upper bounds, not minima.
The n=6 support certificate gives 159 query nodes as a lower bound. With binary
AND/OR and unary NOT gates, the circuit bounds are 158 through 720. The n=5
corresponding lower bounds are 79 query nodes and 78 binary gates.

Every UNSAT n=6 row is sign-balanced, I=0. None has degree variance zero, so
every 2P2N instance of D(6,8) is SAT. This is a finite-size result, not a statement
about larger 2P2N families. The UNSAT variance range is V=24 through 96.

## Why exhaustive UNSAT enumeration is small

Each clause falsifies exactly one eighth of all assignments. Eight clauses are
UNSAT if and only if their falsifying subcubes are pairwise disjoint and cover
the whole assignment cube. The enumerator selects an uncovered assignment and
tries each nonoverlapping clause covering it. Every partition appears exactly
once. This enumerates all UNSAT formulas without iterating over all formulas.

Verification uses an independent Python literal evaluator and memoized partition
count. It checks every exported UNSAT row, absence of duplicates, and equality
of enumerated and independently counted totals. The exported ordered DAG must
accept every UNSAT row and have exactly the same number of accepting weight-eight
inputs, computed by binomial-weighted dynamic programming. These two checks
exclude both false negatives and false positives over the complete promise.
This is symbolic exhaustive verification, not 8.9 trillion individual evaluations.

The circuit checker reconstructs every pure-OR vertex support and the final
AND/NOT structure. This establishes equivalence to assignment coverage for all
inputs. Shared identical OR subexpressions reduce the unshared n=6 bound from
1,280 gates to 720. The resulting circuit has depth 12.

## Run on Mac

Use the compiler setup in FRONTIER_README.md. In this directory:

```bash
mkdir -p d6_output
clang++ -O3 -std=c++17 partition8.cpp -o partition8
clang++ -O3 -std=c++17 partition8_dag.cpp -o partition8_dag
./partition8 6 0 d6_output/n6_first
./partition8 6 1 d6_output/n6_mrv
./partition8_dag 6 d6_output/n6_first.bin d6_output/n6 1
python3 verify_partition8.py 6 d6_output/n6_first.bin d6_output/n6.dag d6_output/n6 d6_output/n6_mrv.bin
python3 coverage_shared.py 6 d6_output/n6
```

Python requires version 3.10 or newer. No external packages are needed. The last
argument of partition8_dag is the maximum number of adjacent-swap passes. The
recorded search used one pass, following six initial orders; it did not exhaust
all orders or adaptive policies. It stops early if a full pass cannot improve
the incumbent. There is no checkpoint-resume implementation.

Replace 6 by 5 in the commands and filenames for the intermediate row. The two
partition pivots are first-uncovered and fewest-available-clauses. Both n=6
enumerations produced exactly the same 30,020 clause sets.

## Data format and storage

Each `.bin` file is a concatenation of 8-byte records. Every byte is a clause ID;
the eight IDs in a record are sorted and distinct. Records are in deterministic
enumeration order, not lexicographic order. Pair-witness CSV row indices are
zero-based indices in this binary file. Replace the indicated clause a with b;
the listed assignment satisfies the resulting formula.

Large `.bin` and `.dag` files are preserved as deterministic `.gz` files. To
verify an archived result, decompress copies first:

```bash
gzip -dk n6_first.bin.gz
gzip -dk n6.dag.gz
```

`n6_verification.json` records the baseline unshared circuit bound of 1,280;
`n6_circuit.json` records the subsequently verified shared bound of 720. The same
distinction is 320 versus 256 for n=5. Both are valid upper bounds.

The new I,V histograms cover every UNSAT formula only. The full SAT population
histogram, semantic-function count, and isomorphism quotient were not computed.
All labeled UNSAT formulas are retained, including those using fewer variables.
Code and artifact hashes are recorded in manifest.json.
