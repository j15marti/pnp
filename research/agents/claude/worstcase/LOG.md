# Worst-case derivation program: living log (Claude)

Target: `Wbar_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)`; weakest bridge `Br_R: SAT in P => Wbar_R <= poly`. P vs NP remains OPEN.

## 2026-11-04 WORSTCASE-0001
Report: `research/agents/claude/2026-11-04_0300_CLAUDE_WORSTCASE-0001.tex`
- Weak-R trap (PROVED/EXACT): if LB_R is an unconditional theorem (Res, CP, ...), Br_R is equivalent to P != NP. Reformulation, no progress.
- Free strategy = nondeterminism: LB for all R iff NP != coNP.
- Strong side: Br_EF holds when SAT in P is witnessed by a PV-provably-correct algorithm (Cook translation, KNOWN). Unconditional P=NP => EF polybounded: not found, OPEN.
- Optimal-system bridge (Krajicek-Pudlak, from memory) exists but R* is non-explicit.
- Design constraint: Br_R needs R about EF-strong; LB_R needs R weak. Live window: between Res+XOR+AND3 and EF.
- Literature: Pich-Santhanam (STOC 2021; arXiv 2312.08163). Full texts not read.
- No experiments. Next: T-WINDOW, T-RANDOM, red-team (see report).
