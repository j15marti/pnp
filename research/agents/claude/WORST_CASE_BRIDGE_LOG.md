# CLAUDE living log: worst-case derivation bridge

Append-only. Status labels per AGENTS.md. P versus NP remains OPEN.

## 2026-11-14 17:50 PST — WCBRIDGE-0001
Report: `research/agents/claude/2026-11-14_1750_CLAUDE_WCBRIDGE-0001.tex`.
- PROVED/EXACT: the free-choice-of-derivation clarification is correct; the gap is that an arbitrary SAT algorithm need not be R-based.
- PROVED/EXACT: for every R with a known superpolynomial lower bound (Resolution, PC, Cutting Planes, bounded-depth Frege, regular Res(+), small-k Res(k)), Br(R) is equivalent to P != NP, so the bound+bridge split gives no reduction there. Br(R) cannot be refuted by a counterexample formula without a polynomial-time SAT algorithm.
- PROVED/EXACT: Br is downward monotone under p-simulation; progress requires a middle system (general Res(+), AC0[p]-Frege, Frege, EF, possibly R_mix341) with an open lower bound and a constructive bridge.
- KNOWN THEOREM (already in corpus, LSPV-1/357): Cook 1975, a PV-provably sound poly-time SAT algorithm gives polynomially bounded EF. Missing: reflection removal (OPEN).
- Red-team tool: Resolution specialization test; any bridge proof must name a property that Resolution lacks.
- Hard families: Tseitin and PHP ruled out as candidates against all systems; random 3-CNF is the only standard survivor (CP constant width, Frege, EF all OPEN).
- Next: decide whether R_mix341 p-simulates EF; verify Assumption C (cost vs length) for the project tariff.
