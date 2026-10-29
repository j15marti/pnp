# Boundary plus local-backdoor burden: actual CNF tests

The user's bound is valid under the original static syntactic 2CNF-backdoor assumptions. The report additionally derives k+h <= 3b+1 by contracting the connected incidence graph, where h is the number of boundary-only clauses. Consequently

    n <= 3(b+q) + 9bq,
    b+q >= (2/3) * (sqrt(n+1)-1).

This is a restricted structural bound, not a SAT runtime lower bound. Independent mathematical referee review is pending. P versus NP remains OPEN.

All instances are actual connected proper signed exact-(2,2) 3CNFs from the research corpus. They are constructed examples, not industrial competition benchmarks. `fixtures/` contains canonical DIMACS sources and `BOUNDARY_BURDEN1_table.csv` contains the comparison table.

Small sources exhaust all boundaries and compute exact local hitting minima. For any fixed boundary, private primal components give the optimal finest allowed partition, so the small results are global optima over the declared static architecture. The five small source patterns cover 70,208 boundary sets. W1 is UNSAT; V is a same-scope SAT mutation with 54 models. Both have exact minimum burden five, while the user's rounded floor is two.

Larger cycle and torus cases test explicitly listed boundary candidates. Their local hitting sets are feasible witnesses checked directly. HiGHS optimality statuses are recorded, but the reported larger burdens are achieved upper bounds, not globally optimal boundary decompositions. An ordinary independently coded capped DPLL solver also decides both labels on every measured pair. All selection, branch, propagation and component work is included in its logical counters. These are not native TM timing or space bounds.

Requirements: Python 3.11+; SciPy is needed only for larger hitting-set runs. The three unchanged source implementations in `inputs/` make this folder self-contained.

From the repository root:

```bash
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage small --case W1
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage small --case 6
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage small --case 9
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage small --case 12
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage small --case 15
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage cycle --case 4
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage cycle --case 8
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage cycle --case 16
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage torus --case 6
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage torus --case 12
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage torus --case 24
python3 research/explorations/boundary-burden/BOUNDARY_BURDEN1.py --stage periodic --case scaling
```

Each invocation was under three seconds in the recorded run. Raw JSON records its exact source hashes and timing. Timing differences on replay are expected; mathematical decisions and witnesses must continue to verify.

Build the PDF from this directory with pdfLaTeX, BibTeX, then pdfLaTeX twice. The current root's ownership markers differ from the older required pattern; repository preflight reports this pre-existing issue. This experiment creates new append-only research artifacts and does not edit the living root.
