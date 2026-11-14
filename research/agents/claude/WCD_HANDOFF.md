# CLAUDE worst-case derivation lane: handoff (2026-11-13 16:52 PST)

Latest report: `research/agents/claude/2026-11-13_1652_CLAUDE_WCD-PVEF-0001.tex`. P versus NP OPEN.

- KNOWN THEOREM (assembly, Cook 1975 + Cook-Reckhow 1979): if a polynomial-time SAT decider A rejects every UNSAT formula and PV proves only its *rejection soundness*, then Wbar_EF(N) <= poly(N). So PV-CERT => B3(EF), and via LSPV-1/592 (conditional A1-A4) => B3 for an ER-strength native calculus.
- Exact residual for the EF-strength route: [Wbar_EF superpolynomial] AND [PV-CERT] => SAT not in P. Both OPEN. PV-CERT fails only if P=NP holds solely via deciders whose rejection soundness is independent of PV.
- For Resolution-strength R the bridge B3 is equivalent to SAT not in P (adopted from REFEREE331/343), so weak systems give no easier bridge.
- Literature: Pich-Santhanam arXiv:2312.08163 gives the only other known sufficient conditions (S^1_2-provable anticheckers etc.) for EF lower bounds => P != NP.
- Next target: compare the Pich-Santhanam antichecker hypothesis with PV-CERT/S^1_2-CERT (TMR-1 dependency chain, TMR-5 review).
- No main.tex, proof1.txt, proof2.txt, schedule or ownership changes.
