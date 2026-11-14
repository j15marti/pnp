# Living log: worst-case minimum derivation cost (Wbar_R) — Claude scheduled routine

Target: Wbar_R(N) = max over UNSAT F with |<F>| <= N of min over R-refutations of cost_R. The routine grants free choice of the optimal derivation. Primary bridge: B3, SAT in P implies Wbar_R(N) <= poly(N) for the same preselected R.

This log is additive and role-neutral. It does not edit root main.tex (owned by TMR-5) or any TMR or LSPV region. Newest entry first.

## 2026-11-14 05:00 PST — WCDC-001 narrow-row collapse
- **PROVED/EXACT (system R^- = RES+AND3+XOR+LOCAL-CONVERT, no DEF):** the boundary-support lemma holds for every object type: clauses, 3-variable factors and GF(2) rows. Every R^- refutation of a boundary expander contains an object of support > cr/2.
- **PROVED/EXACT, with the known Chvátal–Szemerédi bound:** narrow-row collapse, S_Res(F) <= 2^{O(k)} W when every row has support <= k. So every subexponential R^- refutation of random 3-CNF uses parity rows of support Omega(n).
- **FALSIFIED/RETIRED:** a size–width route for R^-. Odd Tseitin needs rows of support Omega(h), yet W = 4h-1.
- **OPEN WCDC-T1:** a restriction-stable rank cost for manufactured wide rows on random 3-CNF. B3 and P vs NP remain OPEN. DEF (the full R_mix341) is not covered.
- Evidence: `research/agents/claude/wcdc/2026-11-14_0500_CLAUDE_WCDC_NARROW_ROW_COLLAPSE001.tex`, `experiments/claude_wcdc/mixed_boundary_width001.py`, `results/raw/claude_wcdc/2026-11-14_CLAUDE_WCDC001_RAW.json` (532 checks, 0 failures, 18.7 s).
