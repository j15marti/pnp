# Living log — worst-case minimum-derivation programme (Claude scheduled runs)

Target: `Wbar_R(N) = max_{F UNSAT, |<F>|<=N} min_{pi: F |-_R false} cost_R(pi)`, with free choice of the best derivation, plus bridge
B3: `SAT in P => Wbar_R(N) <= poly(N)` for one fixed system R. **P versus NP remains OPEN.**

Append one entry per run, newest at the bottom.

---

## 2026-11-12 — run B3-CONSERVATION-0001
Report: `research/agents/claude/2026-11-12_CLAUDE_B3-CONSERVATION-0001.tex`

- **PROVED/EXACT (elementary):** for every R, `B3_R <=> (SAT not in P) or (Wbar_R poly-bounded)`. So for any R with an already-known superpolynomial lower bound (Resolution, Cutting Planes, bounded-depth Frege, Polynomial Calculus, and any hypergraph calculus they p-simulate), B3_R is **equivalent to P != NP**. For those systems B3 is the whole problem, not a weaker first step.
- **PROVED/EXACT:** if R is optimal, B3_R holds unconditionally, and a lower bound for R is equivalent to NP != coNP.
- **KNOWN THEOREM pattern (Cook 1975; Krajicek–Pudlak 1989):** if R p-simulates EF and a polynomial SAT algorithm has correctness with short R-proofs (for EF: provable in PV), then Wbar_R is polynomial. The gap that remains open: P = NP could hold with no correct algorithm whose correctness PV can prove.
- **Literature this run:** de Rezende–Engström–Ghannane–Risse 2026 (ECCC TR26-078, arXiv:2604.28172) proves superpolynomial lower bounds for *tree-like* semantic Frege with bounded line size. It does not cover DAG-like proofs, which are exactly the shared-DAG regime of the hypergraph calculus. No general Frege lower bound has been found as of this run.
- **Next:** first check each proposed R against the conservation corollary; pursue B3 for EF in the PV-provability form; look for DAG-like lower bounds for the hypergraph calculus.
- root `main.tex` not edited (not an LSPV ownership role).
