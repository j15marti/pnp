# Living log: worst-case minimum derivation cost  W̄_R(N)

Scheduled Claude routine. Target (shared with LSPV-1..5, directive
`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`):

    W̄_R(N) = max_{F ∈ UNSAT, |<F>| ≤ N}  min_{π : F ⊢_R ⊥} cost_R(π)

Primary bridge B3(R):  SAT ∈ P  ⟹  W̄_R(N) ≤ poly(N), same fixed R.
**P versus NP remains OPEN.** Newest entry first.

---

## 2026-11-12 15:53 PST — WCD-0001
Report: `research/agents/claude/2026-11-12_1553_CLAUDE_WCD-0001.tex`
Code: `experiments/worst_case_derivation/2026-11-12_wcd_exact.py`
Data: `results/raw/worst_case_derivation/2026-11-12_wcd_*.json`

- PROVED/EXACT (elementary): free-sequence principle — time of any algorithm that *writes* an
  R-refutation ≥ W_R; correct, but applies only to R-producing algorithms.
- PROVED/EXACT: simulation-order sandwich — B3 is upward closed, LB downward closed under
  length simulation; need one R in both. Today no system is known in both.
- PROVED/EXACT: ∃R [B3(R) ∧ LB(R)] ⟺ SAT ∉ P (take R = resolution). So B3 is a
  reformulation unless proved by a uniform decider→proof construction that does not use the
  falsity of SAT ∈ P. Partial version (systems containing resolution) was already in corpus.
- KNOWN THEOREM: only conditional B3 route is at EF strength (PV-provable decider correctness,
  Cook 1975 / Cook–Krajíček 2007; corpus LSPV-1/357). R_mix341 ⊇ ER₂ is EF strength.
- COMPUTATIONAL (exact, tiny): Tseitin(Q3) min tree-res 128 leaves vs 7 F2 row additions;
  PHP^4_3 tree 43, width 3; dense random 3-CNF n≤12 trivially easy (control only).
- Literature checked: Res(⊕) general lower bound still OPEN (regular / depth-restricted
  results 2024–2025); Cook–Krajíček PV equivalence.
- OPEN next: non-vacuous B3; hard family for Res(⊕)+CP combos; exact DAG-resolution length
  battery for n ≤ 8.
