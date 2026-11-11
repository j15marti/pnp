# Worst-case minimum-derivation living log (Claude scheduled runs)

Target: Wbar_R(N) = max_{F UNSAT, |<F>|<=N} min_{pi: F |-_R bot} cost_R(pi), with free choice of
the optimal derivation. Weakest bridge B3: SAT in P => Wbar_R(N) <= poly(N) for the SAME R.
Canonical trackers: /main.tex, /proof2.txt. **P versus NP remains OPEN.**

| Date (PST) | Run | Result | Status |
|---|---|---|---|
| 2026-11-11 01:52 | WORSTCASE-MU-0001 | Wbar_R is attained on minimally unsatisfiable sources (premise monotonicity). Hard families need unbounded maximum deficiency (Szeider 2003 certificate theorem). Literature: general DAG Res(⊕) lower bounds still open, so a B1 argument for a calculus containing Res(⊕) would settle that problem. | Lemma PROVED/EXACT under PM; corollary CONDITIONAL; finite check COMPUTATIONAL; B1/B3 OPEN |

Report: `research/agents/claude/2026-11-11_0152_CLAUDE_WORSTCASE-MU-0001.tex`;
code/data: `research/agents/claude/worstcase/`.
