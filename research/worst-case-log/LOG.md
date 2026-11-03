# Living log: worst-case derivation cost (shared directive)

Target: W_R(N) = max_{F in UNSAT,|F|<=N} min_{pi: F |-_R bot} cost_R(pi); bridge SAT in P => W_R <= poly. P vs NP OPEN.

## 2026-11-03 run
- Proved (elementary): for any R with a known superpolynomial bound, the bridge is equivalent to P != NP, so it is not a weaker sufficient condition. For trivial-cost R it is a reformulation.
- SAT in P gives automatability of all R, not p-boundedness.
- Next target: a uniform simulation theorem (algorithm A for SAT => short R-derivations) in an R with no known lower bound, plus a lower-bound route for that R.
- Report: research/agents/claude/2026-11-03_WORSTCASE-DERIVATION-0001.tex
- Not done this run: no root main.tex region edits, no multi-agent role reports; no lower bound.
