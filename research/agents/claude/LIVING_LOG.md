# Claude scheduled-routine living log

Append-only. Statuses use the AGENTS.md vocabulary. P versus NP remains OPEN.

## 2026-11-13: B3-DISJUNCTION-0001
- Report: `research/agents/claude/2026-11-13_CLAUDE_B3-DISJUNCTION-0001.tex`
- PROVED/EXACT (elementary): B3_R ⟺ (SAT ∉ P) ∨ PB_R for every fixed R. The bridge is a reflection/disjunction statement, not an independent weaker lemma.
- Corollary: for any R p-simulated by a system with a known lower bound (Res, Res(k), AC0-Frege, PC, CP, regular Res(⊕)), proving B3_R is the same as proving SAT ∉ P.
- New red-team check (Resolution control test): every B3 arrow must use a property of R that Resolution lacks (for R_mix341, extension/DEF). Otherwise the arrow is a disguised P≠NP claim.
- Literature: no general dag-Res(⊕), AC0[p]-Frege or EF superpolynomial lower bound as of the search. Recent depth-restricted Res(⊕) bounds are arXiv 2507.23008 and 2511.20023.
- Next: apply the control test to each B3-supporting arrow in root main.tex.
