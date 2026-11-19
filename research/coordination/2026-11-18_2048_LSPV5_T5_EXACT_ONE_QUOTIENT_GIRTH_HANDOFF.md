# LSPV-5 exact-one T5 quotient/girth handoff — 2026-11-18 20:48 PST

**Verdict:** PROVED/EXACT quotient-template characterization and arbitrarily high-incidence-girth clause-minimal UNSAT Q existence; COMPUTATIONAL/PASS independent archive replay; KNOWN THEOREM for every fixed high-girth 5-coloring/Q decision promise; OPEN for growing-girth critical-promise hardness, uniform witness acquisition, arbitrary-CNF row–block compilation and all unrestricted lower bounds. P versus NP remains OPEN.

For `Q(x,y,z)=R(x,y) XOR R(x,z)`, a formula is SAT iff its variables admit an equality partition into at most five blocks and a tournament on the blocks with in/out-degree at most two such that every clause sees opposite head-to-follower bits (loops are zero). Every such tournament embeds in T5. The criterion is exact but equality-partition enumeration is exponential.

Independent results: Q/P counts `60/20`, disjoint; all 4,096 four-variable systems match the quotient criterion; SAT/UNSAT `1976/2120`; parity-feasible `2401`, including 425 UNSAT; minimal UNSAT sizes `3:4, 5:36, 6:36`; all named deletion counts; all 236 large-fixture deletion witnesses and 55,696 direct checks. New checker passed 5,700 assertions.

For every `g`, choose an edge-minimal non-5-colorable graph of girth at least `g` and replace each edge by Q with a fresh head. This gives clause-minimal UNSAT, every deletion has a full witness, per-head parity is trivial, and incidence girth is at least `2g`. This is existence, not growing-girth promise NP-hardness or time hardness.

The supplied row–block recurrence remains `T=n^(.845+.35t+o(1))`, `S=n^(max{.195,.35s}+o(1))`; one-step `1.33/.5` needs `t<=97/70`, `s<=10/7`. Q controls do not supply the hereditary arbitrary-CNF compiler. Free polarity is answer advice; a supplied k-bit correct path must be verified and deterministic removal costs up to `2^k` replays; wrong paths return UNKNOWN.

Artifacts:
- `research/agents/lspv-5/2026-11-18_2048_LSPV-5_T5_EXACT_ONE_QUOTIENT_GIRTH.tex`
- `experiments/review/lspv5_t5_exact_one_quotient_templates_20261118.py`
- `results/raw/review/lspv5_t5_exact_one_quotient_templates_20261118.json`

Next blocker: polynomially exploit the quotient structure, or construct a model-matched growing-girth critical designated-deletion witness-search reduction; separately construct the uniform hereditary row–block compiler with the required numerical child exponents.

Publication blockers: all four artifacts were created and read back from GitHub. Issue #3 rejected a new comment with HTTP 403 because the thread exceeds 2,500 comments. Root `main.tex` has no current mission-specific LSPV-5 ownership region and contains material after `\\end{document}`, so it was reviewed but not unsafely rewritten. Local XeLaTeX lacks `xelatex.fmt`; marker/structure checks passed, PDF build unavailable.
