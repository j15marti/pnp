# Living log: worst-case minimum derivation cost (Claude scheduled routine)

Target: Wbar_R(N) = max over UNSAT F with |<F>| <= N of the minimum cost_R(pi) over refutations pi.
Primary bridge: B3(R): SAT in P implies Wbar_R(N) <= poly(N), for the same preselected R.
The best derivation sequence is granted for free; search cost is not charged.
Status vocabulary follows AGENTS.md. **P versus NP remains OPEN.**

## 2026-11-15 10:52 PST — B3-FRONTIER-0001
Report: `research/agents/claude/2026-11-15_1052_CLAUDE_B3-FRONTIER-0001.tex`
- PROVED/EXACT: LB is downward-closed and B3 upward-closed under p-simulation.
- PROVED/EXACT: if LB(R) is a proved theorem, then B3(R) is equivalent to P != NP. For resolution, CP, PC, bounded-depth Frege and anything they simulate, the "weakest bridge" is the whole problem. This covers a multisign-hypergraph calculus whose moves are local signed merges or unit propagation.
- PROVED/EXACT: B3 is vacuously true outside Algorithmica, so its content lives only in the P=NP world.
- KNOWN THEOREM (Cook 1975; Cook–Krajíček 2007): a poly-time SAT decider with PV-provable correctness makes EF polynomially bounded.
- Exact split: B3(EF) follows from that theorem together with the reflection hypothesis RH_PV (or the residual gap RG). Both are OPEN, and LB(EF) is OPEN.
- Recommendation: extend the hypergraph calculus with extension nodes (EF level) if it is to carry a contentful bridge. Hard families must then be EF-candidates (random 3-CNF, proof-complexity generators), not PHP or Tseitin, which have short EF proofs.
- Next targets: (a) is RH_PV refutable relative to an oracle or under a cryptographic assumption? (b) does EF + extension-free hypergraph merging reach a known intermediate system (Res(lin), AC0[p]-Frege) where LB is partially known?
