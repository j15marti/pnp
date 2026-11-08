# Worst-case derivation program: living log
Target: W_R(N) = max over UNSAT |F|<=N of min over refutations pi of cost_R(pi). Bridge B_R: SAT in P => W_R <= poly(N). P vs NP remains OPEN.

## 2026-11-08 WORSTCASE-0001 (research/agents/claude/2026-11-08_CLAUDE_WORSTCASE-0001.tex)
- Proved: if W_R is superpoly (res, PC, CP, bd-Frege) then B_R <=> SAT not in P (circular). Optimal R satisfies B_R but then lower bound <=> NP != coNP. EF: bridge follows from PV-provable correctness (known), not from SAT in P alone.
- Net: non-circular route needs Frege-strength R with a bridge by in-system simulation AND a superpoly lower bound; no weaker bridge found.
- Computation: exact min DAG-resolution lengths, Tseitin C3=5, C4=7, C5>=9 (worstcase/minres.py).
- Literature: nothing new settles optimal proof systems (arXiv 2408.07408; 2506.16956).
- Next: give the multisign DAG hypergraph an explicit verifier V_R; embed ARC/FLMV objects in a Frege-strength R.
