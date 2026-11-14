# Worst-case minimum derivation cost — living log (Claude scheduled routine)

**P versus NP remains OPEN.** Newest entry first. Statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## Shared directive (copied from the scheduled prompt; no other copy was found in the repo on 2026-11-14)

Target: `W̄_R(N) = max_{F∈UNSAT, |⟨F⟩|≤N} min_{π:F⊢_R⊥} cost_R(π)` for one fixed, strong inference system R (multisign DAG hypergraph reductions as one instance). The optimal derivation is chosen for free. Priorities: (1) superpolynomial lower bound on W̄_R; (2) free choice of the derivation, with no charge for search; (3) the weakest sufficient bridge `SAT∈P ⟹ W̄_R(N) ≤ poly(N)`; (4) hard instances that survive resolution, algebraic reasoning, circuit compression, shared DAGs, and strategy switching.
Roles: General SAT Lower-Bound Lead · SAT-Circuit Reduction Builder · Hypergraph & Proof Certificates · Time-Space Resource Auditor · Independent Proof Red Team.

## 2026-11-14 09:48 UTC — WCDERIV-0001 (first run)

Report: `2026-11-14_0948_CLAUDE_WCDERIV-0001.tex`. Code and data: `treeres_vs_gauss.py`, `treeres_vs_gauss_results.json`.

- **KNOWN THEOREM:** a free optimal sequence is a nondeterministic certificate. W̄_R ≤ poly holds for *some* system R exactly when NP = coNP (Cook–Reckhow). A lower bound for every R is therefore NP ≠ coNP, which is stronger than P ≠ NP.
- **PROVED/EXACT (bridge collapse):** if W̄_R is already known to be superpolynomial, then Bridge_R holds exactly when SAT ∉ P. So the bridge is as hard as the target for Res, CP, PC, bounded-depth Frege and regular Res(⊕). The split helps only for R ⊇ DAG Res(⊕), AC0[p]-Frege, Frege or EF, and for those systems the lower bound is itself a major open problem.
- **PROVED/EXACT:** a bridge cannot rely only on the hard family being easy to decide. Counterexamples: PHP (Haken) and Tseitin on expanders, which Gaussian elimination decides in polynomial time but which need exponential-size resolution refutations. A valid bridge must use correctness on *all* CNFs. The corpus's Q_A clock system and reflection bridge (codex 2026-11-11 report, LSPV-1/336 and /361) already capture this. For EF, the bridge comes down to short EF proofs that Q_A is sound: **OPEN**. The literature check found no theorem that P = NP implies EF is polynomially bounded.
- **Survival matrix (KNOWN THEOREMS, recheck before load-bearing use):** PHP fails against CP and Frege. Tseitin fails against PC(F2), CP and Res(⊕). Random 3-CNF at constant density survives every system that has a known lower-bound technique. Random 3-CNF with m ≥ c·n^1.4 fails against TC0-Frege (Müller–Tzameret). **CANDIDATE** hard family: random 3-CNF at constant density. The open columns are DAG Res(⊕), AC0-Frege and Frege.
- **COMPUTATIONAL:** exact minimum tree-like resolution size compared with GF(2) elimination steps. Tseitin: C6 23/5, C10 39/9, K4 55/5, prism 95/9, K33 151/11, cube 255/20. PHP: PHP^3_2 21, PHP^4_3 85. The Petersen graph and PHP^5_4 hit the 25-second stage budget.
- **Next questions by role.** Lead: state Bridge_R for R = Frege/EF as a reflection statement, and decide whether a weaker R (e.g. Res(⊕)+extension) avoids both halves being P≠NP-hard. Builder: specify the multisign-DAG system R and its exact p-simulation relations with Res(⊕) and Frege. Hypergraph: random 3-CNF lower bounds for regular/bounded-depth Res(⊕). Auditor: length–space tradeoffs (Ben-Sasson–Nordström) for the chosen R. Red Team: check every survival-matrix entry against primary sources.
- Root `main.tex` was not edited, because it has no Claude ownership region. P vs NP: **OPEN**.
