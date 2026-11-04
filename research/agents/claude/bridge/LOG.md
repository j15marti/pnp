# Worst-case derivation-cost living log (bridge/)
Target: Wbar_R(N)=max_{F UNSAT,|F|<=N} min_{pi:F|-_R bot} cost_R(pi); weakest bridge SAT in P => Wbar_R<=poly.

## 2026-11-04 BRIDGE-0001
- Prop 1: LB(R) & Br(R) <=> LB(R) & P!=NP; for Resolution Br <=> P!=NP. Bridge must be a constructive soundness-translation (B1), not a lemma from truth of P=NP.
- Exact min tree-like Res sizes tabulated (treelike_min.py).
- Literature: no unrestricted Frege/EF lower bound as of 2026-11 (only restricted tree-like semantic Frege, TR26-078).
- Next: test bridge mechanism on a provably-correct algorithm class (bounded treewidth DP) in ER.
- Status: OPEN. P vs NP OPEN.
