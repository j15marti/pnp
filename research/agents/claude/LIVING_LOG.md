# CLAUDE living log: shared worst-case derivation directive

Living log for the scheduled shared-directive runs on the objective

  W̄_R(N) = max_{F UNSAT, |<F>| ≤ N} min_{π : F ⊢_R ⊥} cost_R(π),

with weakest sufficient bridge  SAT ∈ P ⇒ W̄_R(N) ≤ poly(N).
New entries go at the top. Statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
**P versus NP remains OPEN.**

---

## 2026-11-12 17:53 PST — EF-BRIDGE-0001

Report: [`2026-11-12_1753_CLAUDE_EF-BRIDGE-0001.tex`](2026-11-12_1753_CLAUDE_EF-BRIDGE-0001.tex)

- **PROVED/EXACT (ladder).** If R' p-simulates R, then Br(R) ⇒ Br(R') and LB(R') ⇒ LB(R).
  For every R with a known superpolynomial lower bound (Resolution, Cutting Planes, AC0-Frege, PC), Br(R) ⇔ SAT ∉ P.
  So for those systems the bridge is the whole problem restated, not a weaker step.
- **CONDITIONAL on [P2-D1] (native grammar = the documented rule types).** R_mix341 ≡_p ER ≡_p EF.
  - Lower bound: R_mix341 contains RES+DEF. EF simulates R_mix341 because R_mix341 is PV-provably sound (Cook 1975).
  - Consequence: target [P2-B1] *is* the Extended Frege lower-bound problem.
- **PROVED/EXACT from known theorems.** Br(EF) ⇔ certification upgrade: if SAT ∈ P, then some polynomial-time SAT decider has polynomial-size EF proofs of its own soundness.
  - The converse direction uses EF's polynomial-size proofs of its own reflection principle.
  - Equivalently, Br(EF) ⇔ (P = NP ⇒ EF is p-bounded). This is the exact missing link [P2-B2/B3]. **OPEN.**
- **Plan for R_mix341 ⇔** EF is not p-bounded **∧** (P = NP ⇒ EF is p-bounded). Both conjuncts are OPEN.
- **Literature, new to the corpus:**
  - Fleming–Grosser–Pitassi–Robere, *Provable Reductions in TFNP*, ECCC TR26-109. The system ⟨EF, R⟩ collapses to EF when EF proves R ∈ FP, which is the proof-system form of the upgrade.
  - Egidy–Glaßer, STOC 2025: relativization barrier for optimal proof systems.
  - KP89: E=NE gives a p-optimal system, but not a fixed one, so it is a FAILED TRANSFER for this bridge.
- **Red team.**
  - Granting the optimal sequence for free remains legitimate.
  - Relativizing bridges are retired (LSPV-1/360). A relativizing proof of Br(EF) would make EF p-bounded and so give NP = coNP.
  - Every hard family retired in the corpus is EF-easy, which is consistent with the equivalence above.
- **Next.** Attack the certification upgrade, or an EF lower bound for an explicit family. Before claiming any R_mix341 hardness, first check whether the family is already known to have polynomial EF proofs.
- No main.tex, schedule, role, or ownership change.
