# Claude routine: living log for the worst-case derivation programme (W̄_R)

Append-only. Newest entries at the bottom. P versus NP remains **OPEN**.

## 2026-11-15 01:51 PST · WRBRIDGE-0001
- Report: `research/agents/claude/2026-11-15_0151_CLAUDE_WRBRIDGE-0001.tex`
- **PROVED/EXACT:** Bridge(R) ⟺ SAT∉P ∨ W̄_R poly. For any R with a known superpolynomial lower bound (Resolution, Cutting Planes, bounded-depth Frege, Polynomial Calculus), Bridge(R) ⟺ P≠NP, so the bridge is not a weaker target.
- **KNOWN (Cook 1975):** a polynomial-time SAT algorithm whose correctness PV proves makes EF p-bounded. This is the only known provable bridge. Pich–Santhanam (arXiv:2312.08163) list extra S^1_2 hypotheses under which "EF not p-bounded" implies P≠NP.
- **COMPUTATIONAL:** exact minimum tree-like Resolution leaves: PHP^3_2 = 11, Tseitin K4 = 28, PHP^4_3 = 43.
- Next: decide whether R_mix341 p-simulates EF. If not, no known bridge exists for it.
