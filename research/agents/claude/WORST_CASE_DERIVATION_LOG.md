# Living log: worst-case minimum derivation cost W̄_R(N)

Target: W̄_R(N) = max over UNSAT F with |F| ≤ N of the minimum cost over refutations π : F ⊢_R ⊥.
Bridge: SAT∈P ⇒ W̄_R(N) ≤ poly(N). **P vs NP: OPEN.**

| Date | Run | Result | Status |
|---|---|---|---|
| 2026-11-11 | WCDERIV-0001 | For any R that already has an unconditional lower bound (resolution, cutting planes, AC0-Frege), the bridge is equivalent to P≠NP. It is a reformulation. | PROVED/EXACT |
| 2026-11-11 | WCDERIV-0001 | The relativized bridge is false (PSPACE oracle). Any proof of the bridge must be non-relativizing. | PROVED/EXACT |
| 2026-11-11 | WCDERIV-0001 | The best known bridge is Cook 1975: a SAT∈P algorithm that PV proves correct gives polynomial-size EF refutations. The gap is certifying soundness of the algorithm's trace inside R, not strategy search. | KNOWN THEOREM |
| 2026-11-11 | WCDERIV-0001 | Exact minimum tree-like resolution size: PHP 5, 21, 85 (n=1..3); Tseitin(K4) 55. | COMPUTATIONAL |

Next highest-value target: decide whether the multisign hypergraph calculus with extension is p-equivalent to EF.
Report: `2026-11-11_CLAUDE_WCDERIV-0001.tex`; code and data: `worst-case-derivation/`.
