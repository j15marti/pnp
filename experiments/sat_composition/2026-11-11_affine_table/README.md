# Exact SAT composition prototype

**Status: exact parameterized construction, independently checked. P versus NP remains open.**

The proof note gives the mathematical statements, full proofs, costs, counterexamples, source review, and remaining universal obligation. This package contains complete dependency-free Python programs, LaTeX and BibTeX sources, and raw machine-readable verification results.

## What is implemented

`affine_table.py` represents an exact relation as an affine GF(2) core and an explicit table on linear coordinates. It implements conjunction, existential projection, affine-hull extraction, and exact Walsh normalization. Its DIMACS front end performs factor elimination and returns SAT, UNSAT, or UNRESOLVED if a supplied table budget is exceeded. A resource limit never returns UNSAT.

`independent_2sat.py` implements a separate polynomial terminal: when all factors have at most two table coordinates and their distinct reduced linear forms are globally independent, it translates them into ordinary 2-CNF, solves by strongly connected components, and lifts a satisfying assignment to the original variables. Otherwise it returns unresolved. This terminal is supplied as a separate module; the default factor-elimination CLI does not automatically invoke it.

The source programs require Python 3.10 or later and use only the standard library.

## Run the solver

```bash
python affine_table.py example.cnf --cap 20
```

The complete DIMACS input may use arbitrary valid signed variable identifiers; occurring variables are relabeled densely before matrix allocation. The maximum table dimension is an algorithm parameter, not a theorem that every formula stays below that limit.

## Reproduce the finite checks

Run these commands from this directory. They were deliberately split into stages below 30 seconds in the development environment.

```bash
python verify_affine_table.py algebra --out results/algebra.json
python verify_affine_table.py sat --out results/sat.json
python verify_affine_table.py controls --out results/controls.json
python verify_affine_table.py selector --out results/selector.json
python validate_affine_compiler.py
python validate_affine_dimension.py
python independent_2sat.py small --out independent_2sat_small.json
python independent_2sat.py wide --out independent_2sat_wide.json
python context_pruning_validation.py
```

The independent all-pairs verifier checks all 256 Boolean functions on three variables, 2,048 projections, and 65,536 conjunctions against truth-table semantics. The randomized stages use seed 20261111. The stored JSON includes input formulas/factors and source SHA256 hashes. Counters describe selected operations, not complete native instruction counts. Finite validation supports the proofs and does not establish a general polynomial bound.

## Compile the note

With a working LaTeX installation:

```bash
pdflatex sat_composition_proof.tex
bibtex sat_composition_proof
pdflatex sat_composition_proof.tex
pdflatex sat_composition_proof.tex
```

## What remains open

The proved cost is polynomial in the input and number of operations, multiplied by an exponential in the largest temporary table dimension. No theorem bounds that dimension logarithmically on all SAT inputs or supplies a universally applicable polynomial alternative. Long OR interfaces prove that the chosen single-table format can be exponentially larger than an easy symbolic expression. The explicit Horn-2CNF plus disjoint-XOR selector construction in the note is the next focused compatibility test.
