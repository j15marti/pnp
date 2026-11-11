# Living log: worst-case minimum derivation cost  W̄_R(N)

Shared target: W̄_R(N) = max_{F∈UNSAT,|F|≤N} min_{π:F⊢_R⊥} cost_R(π).
Bridge_R: SAT∈P ⇒ W̄_R(N) ≤ poly(N). **P vs NP: OPEN.**

## 2026-11-11 05:50 PST — WCDERIV-0001 (Claude scheduled run)
Report: `../2026-11-11_0550_CLAUDE_WCDERIV-0001.tex`; code/data: `treeres_php.py`, `treeres_php_results.json`.
- PROVED/EXACT: Bridge_R ⇔ (SAT∈P ⇒ R p-optimal).
- PROVED/EXACT: if LB_R is known (Res, tree-Res, CP, AC0-Frege, PC, any R_hyp ≤ Res) then Bridge_R ⇔ P≠NP — the "weakest bridge" is the whole problem for these systems.
- PROVED/EXACT: Bridge_Res has no relativizing proof.
- KNOWN: PV-provable SAT∈P ⇒ Bridge_EF (Cook; Krajíček–Pudlák). Unconditional Bridge_EF and LB_EF OPEN.
- COMPUTATIONAL: exact min tree-res leaves for PHP_n^{n+1}: 3, 11, 43 (n=1..3) against an O(N) counting decider, so pointwise algorithm→derivation transfer fails for weak R.
- RETIRED: "the bridge for a resolution-strength hypergraph calculus is weaker than P≠NP".
- Next: decide whether R_hyp is p-equivalent to Res or Res(⊕); extend exact search to DAG resolution on Tseitin instances.
