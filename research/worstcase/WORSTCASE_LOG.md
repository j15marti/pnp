# Worst-case derivation-cost program: living log
Objective: W̄_R(N) = max_{F∈UNSAT,|F|≤N} min_{π:F⊢_R⊥} cost_R(π); weakest bridge SAT∈P ⇒ W̄_R ≤ poly. Status: OPEN. Append newest entries at the top.

| Date | ID | Result | Status |
|---|---|---|---|
| 2026-11-05 | WC-0001 | Bridge dichotomy: for any R with known superpoly lower bound, B_R ⇔ P≠NP (circular); for strong R (EF-like) B_R needs provable correctness / optimal-system-type premise. Candidate B*_R targeted. Report: `2026-11-05_WORSTCASE_BRIDGE_DICHOTOMY1.md`; harness `experiments/worstcase/min_res_dag.py` | PROVED (T1,T2), CANDIDATE (T4) |

Open arrows: superpoly W̄_R for strong R; B*_R premise; R_H p-simulates EF.
