# Worst-case derivation-cost program: living log

Objective (user directive, shared by all five roles):
W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi); target bridge  SAT in P  =>  W_R(N) <= poly(N).
Status: **P versus NP remains OPEN.** Nothing below proves a lower bound. Strict labels per AGENTS.md.

## Entry 2026-11-07 (run CLAUDE-WC-0001) -- full text: research/agents/claude/2026-11-07_CLAUDE_WC-0001.tex

Results (all PROVED/EXACT unless marked):
1. **Free-search = nondeterminism.** If every move of R is poly-time checkable and cost is poly-bounded in the derivation's bit length, then W_R is the shortest-proof function of a Cook-Reckhow system. Granting the optimal sequence for free is therefore exactly the NP/coNP gap, not a harmless relaxation: W_R <= poly iff R is p-bounded.
2. **Bridge/lower-bound dichotomy.** Let B(R) be "SAT in P => W_R poly". If W_R is unconditionally superpolynomial (e.g. R = resolution, Haken; cutting planes; bounded-depth Frege), then B(R) is *equivalent* to P != NP. So the bridge can be proved for no system with a known lower bound without proving P != NP. Usable R must lie beyond the lower-bound frontier (Frege/EF-like), where W_R's growth is unknown.
3. **Sufficient bridge (PROVED, conditional form).** If some poly-time SAT algorithm A has poly-size R-proofs of the soundness instances "A(F)=0 -> not F", and R closes under cut/modus ponens, then W_R poly (trace of A is poly size). Hence: *a superpolynomial W_R lower bound implies P != NP or every poly-time SAT algorithm is R-unprovably correct.* Closing the "or" is the whole remaining bridge; it needs R-provability of correctness for some algorithm (Levin search gives verified witnesses, not verified rejections: its reject-correctness assumes the unknown time bound).
4. **Cost-model rule.** Any "minimal reduced state + minimal work" model with locally poly-checkable multisign-hypergraph moves is a Cook-Reckhow system; a lower bound for it is a proof-complexity lower bound for that system, and cannot outrun Pich-Santhanam-type barriers for strong systems.

Next targets: (a) formalize multisign DAG hypergraph moves as R_MS and place it in the p-simulation order (Res <= R_MS <= EF?); (b) decide whether B(R_MS) is provable via a soundness-reflection lemma or equivalent to P != NP (dichotomy of item 2); (c) hard UNSAT families for R_MS surviving resolution/algebraic/circuit-compression tests.

Literature clue checked: Pich-Santhanam, "Why are proof complexity lower bounds hard?" (FOCS 2019) -- barriers for strong systems like EF; arXiv 2312.08163 ("Towards P != NP from Extended Frege lower bounds") -- Cook-Reckhow program framing. Exact statements to be verified against primary text next run.
