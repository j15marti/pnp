# Exact compatibility beyond independent coordinates

**Status:** exact research implementation, with polynomial time for each fixed affine rank. A universal polynomial SAT bound remains OPEN.

The complete proof note is compatibility_continuation.pdf. The ZIP includes its LaTeX and BibTeX sources, both solver strategies, integration bridges, examples, independent verification programs, and recorded results.

## What changed

The previous affine-table prototype's 2-SAT terminal required independent coordinate forms. The new bridge computes all coordinate dependencies and solves the resulting 2-CNF plus affine system exactly. Every one of the previous 996 small interface cases is now resolved, including all 14 previously unresolved cases.

The implementation also supports arbitrary-width Horn CNF with parity equations. These fixed-codimension tractability results have established prior art, including Arvind–Guruswami, Brakensiek–Gopi–Guruswami, and Mastrolilli; this package makes the construction, witnesses, costs, and limitations executable.

## Requirements

Python 3.10 or later. No third-party packages are required for the programs or tests.

## Run examples

From the extracted directory:

~~~bash
python composition_solver.py 2cnf examples/rank_two_unsat.json --uncapped
python composition_solver.py horn examples/graph33.json --term-cap 100000
python composition_solver.py factors examples/factors_dependent.json --uncapped
python composition_solver.py cnf examples/small_sat.cnf --term-cap 100000
python composition_solver.py horn examples/horn_facts.json --strategy seeds --seed-cap 1000
~~~

The default strategy stores a polynomial in exact Horn-closure keys. The seeds strategy streams small generating sets and uses polynomial workspace without a global cache. Both are exact if run uncapped, but either can take exponential time when affine rank grows.

The default CLI caps each temporary polynomial at 100000 terms, or the streaming search at 100000 attempted seeds. A cap produces UNRESOLVED. It never produces an UNSAT conclusion. These are backend resource caps, not limits on preprocessing or scans of already explicit tables.

## Input formats

For 2cnf and horn modes, use JSON with:

~~~json
{
  "n": 3,
  "clauses": [[-1, 2], [-2, -3]],
  "equations": [[7, 1]]
}
~~~

Clauses use signed one-based variable identifiers. An equation is [mask, right_hand_side], where bit i-1 of mask is the coefficient of variable i. For example [7,1] means x1 XOR x2 XOR x3 = 1. JSON inputs declare an explicit dense variable universe.

For factors mode, use n plus a list of factors, each containing equations, forms, and an explicit Boolean table. A form is another integer coefficient mask. The table's index is the bit vector of form values, with the first form in the least significant bit. All factors share the same ambient variables.

For cnf mode, supply a DIMACS file. Its occurring variable identifiers are relabeled densely before any mask allocation, so sparse large identifiers are supported. The result includes original_assignment mapping original identifiers to truth values. The integer witness field is in the dense occurring-variable order. The CNF frontend uses the exact selector reduction and does not claim a general speed advantage.

## Public APIs

- closure_parity.solve_2cnf_affine(n, clauses, equations, term_cap=None)
- closure_parity.solve_horn_affine(n, clauses, equations, term_cap=None)
- seed_parity.solve_2cnf_affine_seeds(n, clauses, equations, seed_cap=None)
- seed_parity.solve_horn_affine_seeds(n, clauses, equations, seed_cap=None)
- composition_solver.solve_affine_tables(factors, term_cap=None, strategy="polynomial", seed_cap=None)
- composition_solver.solve_cnf_via_selectors(n, clauses, term_cap=None, strategy="polynomial", seed_cap=None)

Results contain status, witness, reason, and counters; integration calls add bridge diagnostics. Witness is an integer mask or null. Unsupported non-bijunctive tables return UNRESOLVED in factors mode. Larger explicit tables are accepted when their exact unary/binary-clause encoding is verified.

## Reproduce verification

Each invocation below is a separate short stage.

~~~bash
python agent_sources/validate_closure_solver.py
python agent_sources/validate_seed_solver.py
python validate_integration.py baseline --out results/integration_baseline.json
python validate_integration.py tables --out results/integration_tables.json
python validate_integration.py cnf --out results/integration_cnf.json
python agent_redteam/verify_obstructions.py
python agent_redteam/verify_singleton_fixedpoint.py
~~~

Both backends independently passed all 15376 Horn/2-CNF and affine relation pairs on up to three variables, plus 1400 larger random/capped cases each. Exhaustive corpus construction and random seeds are specified in the verification scripts. Complete integration inputs and results are retained, including the compressed previous interface corpus.

The 33-variable mixed example is UNSAT but all 66 singleton branches remain consistent under the specified complete affine-hull/binary-summary exchange. Exact symbolic solving refutes it with 1416 candidate products and a peak of 120 polynomial terms. These are selected execution counters, not physical instruction counts or a scalable benchmark result.

The connected anchor family produces exactly 3^m flat polynomial terms despite having treewidth at most three and an explicit easy satisfying assignment. This is a limitation of eager flat expansion, not a lower bound on SAT decision.

## Compile the report

With a working LaTeX installation:

~~~bash
pdflatex compatibility_continuation.tex
bibtex compatibility_continuation
pdflatex compatibility_continuation.tex
pdflatex compatibility_continuation.tex
~~~

## Remaining obligation

Neither the number of generating seeds nor the number of expanded canonical terms has a universal polynomial bound. A controller must choose exact representations and factorized operations with a proved bound on all acquisition, intermediate construction, search, and fallback work.
