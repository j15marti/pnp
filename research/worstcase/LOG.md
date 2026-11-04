# Worst-case derivation program: living log

Target: `W_R(N) = max_{F in UNSAT,|F|<=N} min_{pi: F |-_R bot} cost_R(pi)`; priority bridge `SAT in P => W_R <= poly(N)`. **P vs NP remains OPEN.**

## 2026-11-04 WORSTCASE-0001 (report: research/agents/claude/2026-11-04_WORSTCASE-0001.tex)
- PROVED/EXACT: if R has a known superpoly lower bound (Res, CP, bounded-depth Frege...), the bridge is *equivalent* to P != NP (trivial reformulation). Only Frege/EF-level R make it nontrivial.
- KNOWN THEOREM (from memory, verify): Cook/PV->EF: PV-provably-correct SAT algorithm => W_EF <= poly. So an EF lower bound yields only "P=NP not PV-provable", not P != NP. Missing: feasible-provability principle (OPEN).
- Literature: Pich-Santhanam 2021 (PV can't prove strong NP lower bounds), Li-Oliveira 2305.15235, Atserias-Muller JACM 2020 (resolution not automatable), Arteche-Atserias-de Rezende 2506.16956.
- Next: classify which theory T and system R make the bridge true; test random k-CNF vs Frege-level reasoning; check multisign DAG rules p-simulate EF.
