# Living log: worst-case minimum derivation cost (shared directive)

Target: `Wbar_R(N) = max_{F in UNSAT, |<F>| <= N} min_{pi : F |-_R bot} cost_R(pi)`, with R = R_mix341.
Bridge B3: `SAT in P  =>  Wbar_R(N) <= poly(N)`. **P versus NP remains OPEN.** Every load-bearing arrow is OPEN.

| Date (PST) | Run | Result | Status |
|---|---|---|---|
| 2026-11-11 17:51 | [WCDERIV-0001](2026-11-11_1751_CLAUDE_WCDERIV-0001.tex) | A superpolynomial Wbar_{R_mix341} would imply superpolynomial ER, Frege and *unrestricted* Res(⊕) lower bounds. The Res(⊕) bound is open per 2025 literature. Conditional on the open REFEREE357 byte-domination lemma plus PV-soundness, R_mix341 is p-equivalent to ER, and the programme becomes Cook's EF programme. Includes a hostile-family survival matrix: PHP, Tseitin and random XOR are retired as hard candidates, random 3-CNF survives. Next target: T-RESXOR. | PROVED/EXACT calibration (relative to corpus ER2 inclusion); CONDITIONAL equivalence; B3 and the lower bound OPEN |

Reproducer: `python3 research/agents/claude/wcderiv/b3_logic_check.py` (under 1 s; `ALL_PASS: true`).
