# Fixed-(n,m) frontier audit and search

This is an executable upper-bound search and independently checked certificate
package. It is **not** an exact minimum-DAG synthesizer. No global minimum is
claimed. Search considers fixed orders plus several adaptive policies. All
published DAGs are then checked on every promised input by a separate C++ program.

Input bits use `q = 8*omitted_variable + falsifying_pattern`. Variables are 0..3;
the three remaining variables are in increasing order; bit j of the pattern is
the value at which literal j is false. All 32 clauses are distinct. Exactly m
input bits are set. Unused variables are permitted: n denotes the available
variable universe, consistently with the earlier binomial counts.

DAG terminals: 0 = SAT, 1 = UNSAT. Decision nodes are counted without terminals.
Circuit output: 1 = SAT. Circuit basis: two-input AND/OR and unary NOT, with free
fan-out and uncharged input wires. These are different resource measures.

## Run on a Mac

Download this experiment directory from the research branch, or clone that branch.
Open Terminal in this directory. Check the compiler:

```bash
xcrun --find clang++
```

If the compiler is absent, install Apple's Command Line Tools, then rerun the
compiler check after installation finishes:

```bash
xcode-select --install
```

Compile and run the complete search and verification:

```bash
mkdir -p output
clang++ -O3 -std=c++17 frontier.cpp -o frontier
clang++ -O3 -std=c++17 verify_frontier.cpp -o verify_frontier
./frontier output 40
./verify_frontier output
python3 check_controls.py output
```

The final Python controls require Python 3.10 or newer. The C++ search and verifier
have no third-party dependencies. Do not use `-DNDEBUG` to disable checks: the
important verifier checks are explicit runtime checks and always remain enabled.

`40` is a maximum number of adjacent-swap passes; search stops that phase early
if a complete pass produces no improvement. Three insertion-sifting sweeps and
23 adaptive policies follow (three deterministic policies plus random seeds
1..20). Search is heuristic and can finish without having found a global optimum.
The m=8 optimized order is applied to m=9..11 without independently optimizing
those rows. Improvements are printed to stderr; the full search trajectory is CSV.

## Files

- `search.csv`: every evaluated order/policy, node count and memo-state count.
- `best.dag`: smallest m=8 construction from the sparse-positive search.
- `best_order.txt`: best associated order, clause IDs 0..31.
- `D4_8.dag` through `D4_11.dag`: best of two tested orders per row, independently
  rebuilt using a coverage-state dynamic program.
- `ordered_panel.csv`: baseline versus optimized-order construction sizes.
- `verification.csv`: exhaustive counts and error totals.
- `coverage.circuit`: explicit 64-gate SAT circuit, valid at every clause count.
- `pair_witnesses.csv`: 496 base pairs proving no correct classifier can omit two
  clause-input bits entirely.
- `extended_pair_witnesses.csv`: 1,984 checked pair witnesses for m=8..11.
- `imbalance_variance.csv`: full population histogram for I and 4V, with UNSAT
  counts in each bin. Here I=sum |d+ - d-| and 4V=4 sum d_i^2-9m^2. Individual
  formulas and isomorphism classes are not stored in this new artifact.
- `controls.json`: constant-output D3 controls, tree/DAG distinction, histogram
  reconciliation, circuit size and depth.

The search writes its best graph on improvement and flushes the CSV log. It does
not yet support resuming a partially completed search. Re-running overwrites the
named output files; use a fresh output directory for a separate experiment.

## Certificates and limitations

Every pair of distinct input positions has two weight-m inputs that differ only
in those positions and have opposite SAT status. If a DAG never queries both of
these positions, it cannot distinguish that pair. Consequently any correct DAG
must query at least 31 distinct positions and hence needs at least 31 query nodes.
This holds even for DAGs that reread input bits. A fan-in-two circuit with one
output and at least 31 essential input wires needs at least 30 binary gates.

These support lower bounds are weak and do not establish the true minima. The
64-gate upper bound follows by OR-ing the four incident edges at each of 16 cube
vertices (48 gates), AND-ing their coverage bits (15), then negating (1).

Simple child-cost addition certifies a decision-tree recurrence, not minimum
shared DAG size. Hash-consing improves a construction but does not fix that
optimization gap. Similarly, canonical reduced OBDDs certify a fixed total
Boolean function; promise-compatible completions require an additional global
optimization. Exact global synthesis with independently checkable infeasibility
certificates remains the next target.
