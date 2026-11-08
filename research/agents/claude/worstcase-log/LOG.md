# Living log: worst-case derivation-cost program (W̄_R)

Target: W̄_R(N) = max_{F UNSAT,|F|<=N} min_{π:F⊢_R⊥} cost_R(π); bridge B3: SAT∈P ⇒ W̄_R(N) ≤ poly(N). P vs NP OPEN.

## 2026-11-08 (WORSTCASE-BRIDGE-0001)
- Prop 1: if R has an unconditional superpoly lower bound, B3(R) ⇔ P≠NP (vacuous bridge). Bridge only meaningful for R ⊇ EF-strength.
- Prop 2: B3 + lower bound is exactly P≠NP; ¬B3(EF) is consistent with current knowledge.
- Known: Cook–Krajíček: PV ⊢ P=NP ⇔ poly-time alg giving assignment or EF proof; yields B3(EF) conditional on feasible provability.
- Literature: no EF lower bound as of 2026 (CCC 2026 Khaniki–Pich–Sokolov barrier; Alekseev ToC 2026).
- Next: (a) classify which hard families survive EF; (b) check whether R_mix341 p-simulates EF (then B3 reduces to provability form); (c) cost audit of overhead in full-certificate-length charging.
- Report: research/agents/claude/2026-11-08_CLAUDE_WORSTCASE-BRIDGE-0001.tex
