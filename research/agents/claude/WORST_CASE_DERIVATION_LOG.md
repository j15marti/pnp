# Living log: worst-case minimum-derivation objective (Claude routine)

Objective: $\overline W_R(N)=\max_{F\in UNSAT,|F|\le N}\min_{\pi:F\vdash_R\bot}\mathrm{cost}_R(\pi)$, with the bridge SAT in P implies $\overline W_R(N)\le\mathrm{poly}(N)$. Newest entry first. P versus NP remains OPEN.

## 2026-11-14 09:00 PST | SWITCH-0001
- PROVED/EXACT: in tree-like Resolution, guarded composition is exactly additive: $L(G(F_1,F_2))=L(F_1)+L(F_2)$.
- PROVED/EXACT (under H-lift): switching gap. A family hard for each system separately can be easy for the system that mixes them. Hard families must therefore be certified against one switching-closed R.
- KNOWN THEOREM assembly: Res plus GF(2) closes to Res(lin), which has no known superpolynomial dag-like lower bound. Adding extension variables gives EF, where the bridge needs PV-provable soundness (Cook 1975).
- COMPUTATIONAL: 80/80 random pairs plus the PHP/Tseitin composite, 0 failures, 5.07 s.
- Report: research/agents/claude/2026-11-14_0900_CLAUDE_SWITCH-0001.tex
- Next: test corpus candidate families against $R_\star$ = Res(xor) with charged guarded rows.
