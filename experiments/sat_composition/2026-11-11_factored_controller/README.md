# Factored exact compatibility controller

This package continues AFFINE-TABLE-COMPOSITION2 with automatic separator discovery, exact small-boundary messages, complete witness reconstruction, and independent verification. P versus NP remains open.

The complete report is `factored_compatibility.pdf`. Its LaTeX and BibTeX sources are included. The recovered ARC235 and ARC236 reports are included for provenance: the underlying two-variable composition and ternary-cover ideas already existed in this project. This release implements and audits their integration with the general local-rank engines.

## Requirements

Python 3.10 or later. All solver and verification code uses only the standard library. No API credentials or network access are needed.

## Run the examples

From the extracted `AFFINE_TABLE_COMPOSITION3` directory:

```bash
python controller.py horn examples/one_anchor_20.json --term-cap 20
python controller.py 2cnf examples/two_anchors_20.json --term-cap 20
python controller.py 2cnf examples/graph33.json --term-cap 100000
python controller.py 2cnf examples/affine_only.json --term-cap 0 --seed-cap 0
python controller.py horn examples/one_anchor_20.json --strategy seeds --seed-cap 20
python controller.py cnf examples/small_sat.cnf --term-cap 100000
python controller.py 2cnf examples/three_anchors_balanced_8.json --term-cap 20
```

The first two examples return SAT through small pieces. The graph example returns UNSAT. The original affine input resolves SAT through Gaussian elimination even with zero expansion/search budgets. The last example returns UNRESOLVED at the stated term cap. With `--uncapped`, supported local solving finishes exactly but can require exponential work.

`--full-audit` retains every bag, boundary assignment, local result, selected child state, and cached witness in the CLI output. The default CLI displays a compact record. API results always retain the full audit.

## What the controller does

1. Preserve a polynomial Gaussian terminal for inputs containing only units, tautologies, and affine equations.
2. Compile low-arity affine rows into clauses where the selected clause language permits it.
3. Build the factor-scope graph and discover separating sets of at most two vertices, or at most one for general Horn input.
4. Use graph-only clique fill to preserve the complete attachment boundary.
5. Validate the decomposition, source coverage, and running intersection.
6. Compute exact child feasibility tables and encode them as clauses.
7. Invoke the exact local engine at most four times per bag, or two in Horn mode.
8. Join compatible local witnesses and check every original source constraint.

An unsupported universal claim is not assumed: the graph search may leave one large bag. Discovery caps cause this exact fallback. Per-query term or seed caps produce unresolved states. A parent forbids only child states proved UNSAT; a local SAT candidate selecting an unresolved child is downgraded to UNRESOLVED.

## Inputs and public APIs

Mixed JSON has this complete structure:

```json
{
  "n": 3,
  "clauses": [[-1, 2], [-2, -3]],
  "equations": [[7, 1]]
}
```

Clauses use signed one-based variable identifiers. An equation is `[mask, rhs]`, where coefficient bit `i-1` names variable `i`. Thus `[7,1]` is `x1 XOR x2 XOR x3 = 1`. Mixed JSON declares an explicit variable universe. For sparse external labels, the DIMACS CNF frontend densely relabels occurring variables before mask allocation and reports `original_assignment`.

Public APIs are:

- `controller.solve_auto(n, clauses, equations, mode="2cnf", strategy="polynomial", max_separator=None, candidate_cap=100000, max_splits=None, term_cap=None, seed_cap=None)`
- `controller.solve_cnf(n, clauses, **options)`
- `separator_decomp.discover_decomposition(n, clauses, equations, max_separator=2, candidate_cap=100000, max_splits=None)`
- `factored_solver.solve_decomposed(n, clauses, equations, decomposition, mode="2cnf", strategy="polynomial", term_cap=None, seed_cap=None)`

The explicit decomposition schema is:

```json
{
  "bags": [[0, 1], [0, 1, 2], [0, 1, 3]],
  "edges": [[0, 1], [0, 2]],
  "discovery_counters": {}
}
```

Bag variables are zero-based global identifiers. The graph of bags must be a forest. Every complete factor scope must fit in a bag, and all bags containing a variable must be connected. These conditions are checked, not trusted. Invalid input raises `ValueError`.

## Resource semantics

The default CLI permits 100000 terms in any one temporary local polynomial, or 100000 attempted seeds in any one local seed search. These caps reset per local query. The Gaussian terminal is a separate polynomial procedure and does not consume expansion or seed budget.

Discovery uses at most 100000 separator candidates by default and at most the number of occurring variables in split operations. `--candidate-cap` and `--split-cap` change those limits. `--unlimited-discovery` removes only the candidate cap; the default polynomial split cap remains. Failed candidate scans, graph copies, fill operations, source ownership, message work and reconstruction have explicit counters. Counters record selected operations, not all physical instructions or Python memory.

For a supplied decomposition, `d_b` is the rank of the original affine rows assigned to bag `b`. For the automatic wrapper it is the rank after low-arity row normalization. The exact guarantee is polynomial for fixed maximum local rank, with separately recognized arbitrary-rank affine queries. Global rank may grow. The seed strategy has polynomial workspace even when local ranks grow, while its time can still be exponential.

`original_witness_checks` in the CNF frontend refers to the pre-lowering mixed selector instance. `original_cnf_clause_checks` separately records the subsequent checks against the user's actual CNF.

## Reproduce the recorded verification

Each command is a separate stage:

```bash
python agent_redteam/audit_discovery.py
python agent_redteam/audit_factored.py
python verify_affine_terminal.py
python verify_controller.py all --out results/controller_validation.json
python verify_controller.py cli --out results/controller_cli_validation.json
python agent_sources/verify_three_anchor_obstruction.py
python agent_sources/verify_balanced_three_anchor_obstruction.py
```

The current-source audits include all 1100 labeled graphs on up to five vertices, 2200 decomposition checks, 580 small/capped solver cases, 4060 exact subtree-message comparisons, 696 automatic-controller cases, nine CLI cases, and eight rank-1024 Gaussian controls. Exact corpus definitions and random seeds are in the verifiers. Structured 200-triple tests have global rank 200 and maximum local rank one. The current summary and manifest identify the exact source hashes; an earlier development smoke record is deliberately excluded.

The balanced three-anchor controls demonstrate the scope limit. Every source-preserving decomposition with at most two shared variables has a full bag owning all ternary parity rows. The specified polynomial and cardinality-ordered seed routines have exponential costs on a family with an explicit easy SAT witness. The larger `m=20` numbers in the report are derived from proved formulas, not executed benchmarks.

## Report compilation

With a working LaTeX installation:

```bash
pdflatex factored_compatibility.tex
bibtex factored_compatibility
pdflatex factored_compatibility.tex
pdflatex factored_compatibility.tex
```

## Remaining research target

A useful next extension is to recognize larger interfaces whose actual messages stay tractable and to charge any branching needed for the remaining messages. ARC236 already supplies one conditional ternary hitting-cover theorem. Universal favorable coverage, discovery and total polynomial cost remain open. Arbitrary three-variable messages with rank-one leaves can encode general 3-SAT.
