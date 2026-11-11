# Claude routine living log: worst-case derivation directive

Append-only log for the scheduled Claude routine that works on the shared worst-case target
`Wbar_R(N) = max_{F UNSAT, |<F>| <= N} min_{pi: F |-_R bot} cost_R(pi)` and the bridge
`B3(R): SAT in P => Wbar_R(N) <= poly(N)`. This routine is not one of LSPV-1..5. It does not edit root `main.tex` ownership regions.
**P versus NP remains OPEN.**

## 2026-11-11 14:52 PST, B3-COLLAPSE-0001
- Report: `research/agents/claude/2026-11-11_1452_CLAUDE_B3-COLLAPSE-0001.tex`
- Ledger rows L41 to L46 added in `world-ledger/`. All pass the consistency check.
- Result: B3 is monotone in R, so it is weakest for the strongest R. Under SAT in P, Wbar_R is polynomial iff R is p-optimal (PROVED/EXACT, elementary). Without auxiliary variables, the multisign-hypergraph system is Resolution: its lower bound is a known theorem (Tseitin, about 2^{N/log N}), so B3 for it is *equivalent* to P != NP. With extension variables it is EF-equivalent. B3(EF) then holds for every PV-provably-correct algorithm (Cook 1975), and full B3(EF) and EF lower bounds are both OPEN.
- Literature consulted: Cook 1975, Cook and Reckhow 1979, Krajíček and Pudlák 1989 (E=NE implies a p-optimal system exists), Köbler, Messner and Torán 2003, Pudlák 2020.
- Next target: the residual gap "SAT in P => some poly-time SAT decider A has poly-size EF proofs of ||RS_A||_n". Test whether any known relativized or Gödelian construction separates it from SAT in P.
