# DOCAUDIT: review of the user's "P vs. NP Proof Attempts" Google Doc (CLAUDE DOCAUDIT-0001)

Report: `2026-11-19_CLAUDE_DOCAUDIT-0001.md`. Additive Claude artifact; it changes no schedules, ownership or TMR manuscripts. **P versus NP remains OPEN.**

| File | Purpose |
|---|---|
| `tn_rank_falsifier.py` | Builds the high-treewidth unit-clause family, computes minor-min-width treewidth lower bounds, runs exact SVD-compressed contraction, and checks the result against brute-force #SAT. About 17 s. |
| `tn_rank_falsifier_results.json` | Raw output, seed 20261119. |

Headline: the doc's Attempt IB claim, "bond dimension ≥ 2^{Ω(tw)} for any contraction order", is FALSIFIED by a uniform family with tw = Ω(n) whose exact compressed contraction has rank 1 throughout.
