# Living log: worst-case derivation complexity W_R(N)  (P vs NP remains OPEN)

Target: max over UNSAT F, |F|<=N, of min over derivations pi of cost_R(pi); free choice of pi. Bridge: SAT in P => W_R <= poly(N).

## 2026-11-08 DERIV-0001
- Prop (known): lower bound for poly-checkable R => NP != coNP. Lower bound alone is stronger than P != NP.
- Prop (proved): if R has an unconditional super-poly bound (resolution), bridge <=> SAT not in P. No progress.
- Bridge for strong R needs p-optimal-like behavior (open). Dichotomy: weak R has bounds but no bridge; strong R has bridge but bounds are NP != coNP-hard.
- Computation: min DAG resolution refutation of full 3-var 3-CNF = 7 (exact); PHP_2^3, Tseitin K4 exact search timed out.
- Literature: nothing new closes the bridge (EF lower bounds only linear; arXiv 2506.16956 meta-complexity).
- Next: space/time-space cost measures (non-size), connect to ARC/FLMV spine; red-team the dichotomy.
Files: 2026-11-08_CLAUDE_DERIV-0001.tex, min_res_dag.py, min_res_dag_results.json
