# Living log: worst-case minimum derivation cost W̄_R(N)

Scheduled Claude stream. Target:
W̄_R(N) = max over UNSAT F with |F| ≤ N of the minimum over refutations π of F in R of cost_R(π),
together with the bridge SAT ∈ P ⇒ W̄_R(N) ≤ poly(N).
This stream is outside the TMR-1..5 ownership regions. It does not edit root main.tex or the proof trackers, and it changes no schedules.
**P versus NP: OPEN.**

## Current state (update every run)

| Item | Status |
|---|---|
| Free choice of the optimal derivation is a valid lower-bound device for R-executions | PROVED/EXACT |
| B_R ≡ P≠NP whenever W̄_R is known to be superpolynomial (Resolution, PC, AC0-Frege) | PROVED/EXACT (reformulation, not progress) |
| Monotone squeeze along p-simulation (bridge gets easier, lower bound gets harder) | PROVED/EXACT |
| Pointwise transfer w_Res(F) ≤ poly(time_A(F)) | FALSIFIED (A⊕ = Gaussian elimination on Tseitin) |
| B_EF under PV-provable soundness | CONDITIONAL (Cook 1975) |
| B_EF unconditional, or under weaker finite reflection | OPEN |
| Superpolynomial W̄_EF or W̄_Frege | OPEN |
| Hard family surviving GE, PC, SOS | random 3-CNF, density below n^0.4 (dense instances have short TC0-Frege refutations) |

## Run entries

### 2026-11-15 03:56 PT — WR-0001
- Report: `research/agents/claude/2026-11-15_0356_CLAUDE_WR-0001.tex`
- Code: `experiments/claude_wr/2026-11-15_wr_tseitin_controls.py`
- Data: `results/raw/claude_wr/2026-11-15_WR0001_TSEITIN_CONTROLS.json`
- Main finding: for any R with a known lower bound, the bridge is equivalent to P≠NP. The non-reformulation regime is an intermediate R (Frege or EF), where the bridge needs feasible provability of soundness.
- Exact table: minimum tree-like Resolution size / minimum width / GE row operations:
  - K4: 55 / 4 / 6
  - prism: 95 / 4 / 15
  - K33: 151 / 5 / 15
- Q3 and Möbius8 timed out and were not computed.
- Literature checked: Cook 1975, Krajíček–Pudlák 1989, Müller–Tzameret 2014, Håstad–Risse 2025, Lu–Santhanam–Tzameret 2025.
- Next: a B_EF weakening via lengthwise reflection, and a 12-variable bitset DP.
