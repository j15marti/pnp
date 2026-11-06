# WCD living log (worst-case derivation programme)

P versus NP remains OPEN. Append newest entries last.

## 2026-11-06 — WCD-0001 (Claude)
- Created directive `research/governance/2026-11-06_WORSTCASE_DERIVATION_DIRECTIVE1.md` and report `research/agents/claude/2026-11-06_CLAUDE_WCD-0001.tex`.
- Result (PROVED/standard): free search of the optimal sequence is harmless; W̄_R poly ⇔ R poly-bounded. Bridge Br(R) is equivalent to SAT∉P whenever LB(R) is already a theorem (e.g. Resolution), so useful R must have open LB (≥ EF strength), making LB(R) imply NP≠coNP.
- Br(EF) follows from poly-size EF proofs of correctness of some poly-time SAT decider (PV-provability); not implied by SAT∈P. This is the weakest known sufficient bridge.
- Next: Red Team to test whether provable-correctness hypothesis can be weakened (e.g. to single-instance reflection with advice); Lower-Bound Lead to check whether MINCOST348 orbit quotient extends to the EF-strength Rmix.
- Literature: no new EF lower bound or p-optimality result found (2026 search).
