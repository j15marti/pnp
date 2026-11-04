# Worst-case derivation program — living log (Claude role)

Objective: `Wbar_R(N)=max_{F in UNSAT,|F|<=N} min_{pi} cost_R(pi)`; priority bridge `SAT in P => Wbar_R poly`. Strategy discovery is never charged to the minimum. All statuses follow AGENTS.md; P versus NP is OPEN.

| Date | Entry | Status |
|---|---|---|
| 2026-11-04 | `2026-11-04_CLAUDE_BRIDGE-SEARCH-COLLAPSE-0001.md`: under `SAT in P`, poly length bound, poly-time proof finder, and p-optimality of fixed `R` are equivalent. B3 and B1 collapse in the bridge's premise world. | PROVED (hand proof); bridge itself OPEN |

## State carried in from the corpus (as of 2026-11-03 19:47 PST)
* Ordinary Resolution lower bounds (Haken PHP, Tseitin) do not transfer to the fixed mixed calculus: ER and GF(2) rules defeat them (REFEREE305/318).
* Axiom monotonicity: `F subseteq G => W_R(G) <= W_R(F)`; direct-sum amplification is false (REFEREE305).
* Per-source minimization collapses; cutoff minimax with description charge equals P/poly; source-rooted carrying returns to native `W_Rmix341` (REFEREE326).
* Open: superpolynomial `Wbar_Rmix341`, B1/B2/B3, NP not in P/poly, P vs NP.

## Literature check this run
No 2025-26 result found linking `P=NP` to boundedness of a *fixed* Frege/EF system. Relevant: Cook–Reckhow (poly-bounded system iff NP=coNP); Krajíček ECCC 2021/053 (proof-search information vs. proof length).
