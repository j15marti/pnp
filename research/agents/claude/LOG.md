# Claude research log (living, append-only)

Shared target: worst-case minimum derivation cost `Wbar_R(N)` and bridge B3
(`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`).
P versus NP remains OPEN. Root `main.tex` ownership regions are not edited by these notes.

## 2026-11-11 00:51 PST — CERTDECIDER-0001
- Report: `2026-11-11_0051_CLAUDE_CERTDECIDER-0001.tex`
- PROVED/EXACT (calibration): the certified-decider calculus `R_T[Res]` (resolution plus a
  rule that rejects F using a machine e that comes with a T-proof of `Corr(e,c)`, the clock
  charged in full):
  - LB ⟺ ¬PT_T ("T proves no polynomial-time SAT decider correct");
  - B3 ⟺ H_T ("SAT∈P ⇒ T proves some polynomial-time decider correct");
  - LB ∧ B3 ⟺ P≠NP, so the split is exact;
  - Gödel obstruction: T does not prove LB for `R_T[S]` (T ⊢ LB → Con(T)).
- Duplicate avoided: the relativization barrier for B3 is already REFEREE296.
- Open handoffs: a B3 condition that does not imply H_T; does B3 for R_mix341 imply H_PV?
