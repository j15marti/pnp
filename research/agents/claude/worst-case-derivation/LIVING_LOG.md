# Living log: worst-case derivation complexity W_R(N) (Claude role)

Target: W_R(N) = max over UNSAT F (|F|<=N) of min over derivations of cost_R. Bridge: SAT in P => W_R <= poly(N).
Status: P vs NP OPEN. All entries additive; no schedules/ownership/main.tex changed.

## 2026-11-09 — WCDC-0001 (`../2026-11-09_0950_CLAUDE_WCDC-0001.tex`)
- PROVED/EXACT: if LB(R) is already known (Res, PC, CP, bounded-depth Frege) then Bridge(R) <=> SAT not in P. Bridge is non-circular only for R with open lower bound.
- PROVED/EXACT: classification test — if a system with a known LB simulates R, R's LB is known; candidate multisign system R* must first be shown not simulated by those.
- PROVED/EXACT: optimal systems satisfy Bridge, but then LB <=> NP != coNP (stronger than needed).
- Sufficient route = fixed non-optimal R with proved Bridge + open LB. Gap: Bridge(EF) needs poly-size EF proofs of SAT-algorithm correctness (PV-provability; Pich–Santhanam conjecture it fails).
- Literature: no new Frege/EF LB or optimal-system result; Pich–Santhanam arXiv 2312.08163 (EF-unprovability => P!=NP) is nearest bridge-type theorem (abstract only read); PC+extension LB (ToC v22 a4) to audit.
- Next: define R*, run simulation classification vs Res/PC/CP/BD-Frege/EF; audit P–S statements; audit PCExt LB.
