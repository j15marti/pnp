# Worst-case minimum-derivation program: living log (CLAUDE routine)

Shared objective: W̄_R(N) = max over UNSAT F with |F| ≤ N of min over derivations π of cost_R(π).
Target bridge: SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). **P versus NP remains OPEN.**

## Current verified state

| Item | Status |
|---|---|
| Bridge(R) holds vacuously if P ≠ NP; Bridge ∧ LB ⇔ P≠NP ∧ LB | PROVED/EXACT (WCD-0001 Thm 1) |
| Bridge(R) ⇔ P ≠ NP for Res, CP, AC0-Frege, PC, SOS, regular/low-depth Res(⊕) | PROVED/EXACT (WCD-0001 Cor 2), so it is a reformulation |
| Bridge for EF, restricted to PV-provably sound deciders | KNOWN THEOREM (Cook 1975; Krajíček–Pudlák 1989) |
| Matched-theory bridges for AC0 / AC0[2]-Frege are trivially true (SAT ∉ AC0[2]) | PROVED from known theorems |
| Pointwise bridge fails for resolution (Tseitin family) | KNOWN THEOREM |
| Exact min tree-like Res sizes, Tseitin C6/K4/K33/Q3, PHP 3→2 and 4→3 | COMPUTATIONAL |
| Unrestricted Bridge(R) together with LB(R) for one fixed R | OPEN |

## Highest-value next target
WCD-T1: unrestricted Res(⊕). Does a matched theory exist whose provably sound deciders reach beyond AC0[2]?

## Run history
- 2026-11-13 00:51 PST, WCD-0001: report `research/agents/claude/2026-11-13_0051_CLAUDE_WCD-0001.tex`; code `experiments/claude_wcd/`; raw `results/raw/claude_wcd/`.
