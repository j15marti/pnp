# Living log: worst-case derivation-cost program (W̄_R)

Target: superpoly lower bound on W̄_R(N)=max_F min_π cost_R(π) plus bridge SAT∈P ⇒ W̄_R ≤ poly. P vs NP remains OPEN.

## 2026-11-05 WORSTCASE-0001
- PROVED: Bridge_R ⇔ (P≠NP ∨ W̄_R ≤ poly). For R with a known superpoly lower bound (resolution, PC, NS), Bridge_R ⇔ P≠NP, so the "weakest bridge" is circular there.
- KNOWN: PV-provably-correct poly SAT algorithm ⇒ EF polybounded (Cook; Krajíček–Pudlák). Gives restricted separation only.
- Next: decide Bridge_EF; place the multisign DAG hypergraph system in the simulation order; T-provable-correctness variants.
- Report: research/agents/claude/2026-11-05_1200_CLAUDE_WORSTCASE-0001.tex
