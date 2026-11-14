# Worst-case derivation complexity (W̄_R) — living log (Claude scheduled routine)

Target: W̄_R(N) = max_{F UNSAT, |F|≤N} min_{π: F ⊢_R ⊥} cost_R(π); bridge B_R: SAT∈P ⇒ W̄_R ≤ poly(N).
P versus NP remains OPEN. Newest entry first.

## 2026-11-14 16:00 PST — WCDC-0001
Report: `research/agents/claude/2026-11-14_1600_CLAUDE_WCDC-0001.tex`.
Code/data: `experiments/claude/wcdc_treeres_exact001.py`, `results/raw/claude/2026-11-14_WCDC0001_TREERES_RAW.json`.
- PROVED (elementary): bridge squeeze. If a superpolynomial lower bound on W̄_R is already known (Resolution, the multisign calculus without extension, CP, PC, AC0-Frege), then B_R ⇔ P≠NP, so the bridge is a restatement of the goal, not something weaker.
- PROVED: the free choice of optimal sequence is a valid lower bound only for algorithms that output an R-derivation; passing from those to all algorithms is exactly B_R.
- KNOWN THEOREM transfer: Tseitin on expanders gives a total correct decider (Gaussian elimination) that is polynomial on the family while every resolution-strength multisign derivation has size 2^Ω(n). The pointwise simulation target is RETIRED for those calculi.
- PROVED: some R satisfying B_R always exists, non-constructively. Bridges must therefore name an explicit R fixed in advance (quantifier repair).
- KNOWN THEOREM transfer (Krajíček–Pudlák 1989): E=NE ⇒ a p-optimal R* exists with B_{R*} true and LB_{R*} ⇔ NP≠coNP. This is a conservation law: the difficulty moves from B to LB.
- COMPUTATIONAL: exact tree-like resolution minima for PHP (m≤3), Tseitin K4/K33/prism/Q3 and random 3-CNF with n≤12, against GF(2) operation counts. Runtime 1.5 s.
- NEXT: formalize the multisign calculus with extension (R+_ms). Find the weakest system where LB is open and no explicit pointwise falsifier refutes B.
