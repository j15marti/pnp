# Living log: shared worst-case derivation directive (Claude lane)

Objective: `W̄_R(N) = max_{F∈UNSAT,|F|≤N} min_{π:F⊢_R⊥} cost_R(π)`. The weakest bridge is
**B3: SAT∈P ⇒ W̄_R(N) ≤ poly(N)**. Status labels follow AGENTS.md. P versus NP remains **OPEN**.

Each scheduled run appends one entry, newest last. The Claude lane owns no region of root `main.tex`.

---

## 2026-11-12 03:00 PST, B3-RELATIVIZATION-0001
- **Report:** `research/agents/claude/2026-11-12_0300_CLAUDE_B3-RELATIVIZATION-0001.tex`
- **Code/data:** `research/agents/claude/b3-relativization/`
- **Literature checked:**
  - Baker–Gill–Solovay
  - Cook–Reckhow
  - Krajíček–Pudlák (E=NE ⇒ p-optimal system exists; P=NP ⇒ E=NE)
  - Pich–Santhanam arXiv:2312.08163
  - Aaronson–Wigderson
- **PROVED/EXACT:** Fix any system R and keep R unrelativized.
  - If B3 is proved in a way that relativizes in the decider, then W̄_R is polynomial unconditionally, by taking the TQBF oracle.
  - With byte domination, this gives NP=coNP.
  - So "relativizing B3 + superpolynomial W̄_R" is inconsistent.
  - Pointwise simulation theorems that also cover oracle algorithms are blocked the same way.
  - This upgrades LSPV-1/360 from CONDITIONAL to unconditional.
- **PROVED/EXACT:** If a lower bound for R is already known (Res, AC0-Frege, CP, PC), then B3_R ⇔ P≠NP. That makes B3_R a reformulation.
- **COMPUTATIONAL:**
  - Exact minimum Resolution size, all 161 UNSAT 2-variable CNFs: distribution {1:112, 2:48, 3:1}.
  - 40 sampled 3-variable 3-CNFs: maximum 4.
  - Complete 3-variable formula: 7.
  - The oracle decider uses 1 query on every instance.
- **Open target handed to roles:** T-B3, i.e. SAT∈P ⇒ some P-time SAT decider is S^1_2/PV-provably correct. Any B3 proof must use a non-oracle property of the decider.
- **Still OPEN:** superpolynomial W̄_{R_mix341}, B3, T-B3, P vs NP.
