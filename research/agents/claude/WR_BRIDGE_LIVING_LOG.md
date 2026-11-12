# Living log — shared worst-case derivation directive (W̄_R)

Target: `W̄_R(N) = max_{F∈UNSAT,|F|≤N} min_{π:F⊢_R⊥} cost_R(π)`, with the weakest sufficient bridge
`B3(R): SAT∈P ⇒ W̄_R(N) ≤ poly(N)`. **P versus NP remains OPEN.** Append one entry per run.

## 2026-11-11 19:52 PST — WR-BRIDGE-0001
Report: `research/agents/claude/2026-11-11_1952_CLAUDE_WR-BRIDGE-0001.tex`
- PROVED/EXACT (folklore): **search neutrality** — under SAT∈P every Cook–Reckhow R is automatable, so charging or not charging strategy discovery leaves B3(R) unchanged.
- PROVED/EXACT: **frontier collapse** — if a lower bound LB(R) is already a theorem (Res, CP, PC, AC0-Frege, restricted Res(⊕)), then B3(R) ⇔ P≠NP; the bridge is only weaker than the goal for R beyond the proved lower-bound frontier (AC0[p]-Frege, Frege, EF, …).
- KNOWN: EF instantiation reduces to the PV-provability gap (Cook 1975; Krajíček–Pudlák); matches LSPV-1/357, /361.
- PROVED/EXACT: **explicit-family obstruction** — TR(R) forces every polynomial-time-generated UNSAT family to be easy for R; hard witnesses for the TR route must be non-explicit. B3 is unaffected. Dense random 3-CNF (m ≥ Cn^1.4) is excluded by Feige–Kim–Ofek witnesses.
- Open next: place R_mix341 relative to AC0[2]-Frege; non-explicit hard candidates (constant-density random 3-CNF, τ-formulas).
