# Living log: worst-case minimum-derivation program (Claude scheduled routine)

Target: Wbar_R(N) = max over UNSAT F with |<F>| <= N of the min over refutations pi of cost_R(pi). Primary bridge B3: SAT in P implies Wbar_R(N) <= poly(N), for the same preselected R.
**P versus NP remains OPEN.**

## 2026-11-13 08:00 PST — B3-DICHOTOMY-0001
- Report: `research/agents/claude/2026-11-13_0800_CLAUDE_B3-DICHOTOMY-0001.tex`
- PROVED/EXACT (elementary): for every fixed R, P != NP implies B3_R holds vacuously. If a superpolynomial lower bound L_R is already known (resolution, cutting planes, AC0-Frege, PC), then B3_R is *equivalent* to P != NP, so it is a reformulation and not a weaker bridge.
- For R with auxiliary definitions (multisign hypergraph + VARDEF, R_mix341): it p-simulates ER, so L_R is the EF lower-bound problem (OPEN since 1975). The only known B3 route is Cook's PV -> EF translation, which needs a PV proof of rejection soundness (LSPV-1/357, CONDITIONAL).
- Free optimal-sequence selection is legitimate, but it is not where the difficulty lies. Both obstacles concern proof length, not search. Arteche et al. (FOCS 2025) concerns search: a failed transfer.
- Duplicates (adopted): LSPV-5/409 Q_A-simulation equivalence, LSPV-1/357 reflection criterion.
- Next: an explicit-polynomial version of the 357 conditional for R_mix341.
