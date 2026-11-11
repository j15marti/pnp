# Living log: worst-case minimum-derivation directive

Append-only log for the scheduled CLAUDE routine on

    Wbar_R(N) = max_{F in UNSAT, |<F>| <= N} min_{pi : F |-_R bot} cost_R(pi)
    Bridge(R): SAT in P  =>  Wbar_R(N) <= poly(N)

**P versus NP remains OPEN.** Status labels follow AGENTS.md.

## 2026-11-11 14:00 PST — WORSTCASE-DERIVATION-0001
Report: `research/agents/claude/2026-11-11_1400_CLAUDE_WORSTCASE-DERIVATION-0001.tex`

- **PROVED/EXACT (sandwich).** For every fixed Cook–Reckhow R: NP≠coNP ⇒ [Bridge(R) ∧ LB(R)] ⇒ P≠NP. If LB(R) is already known (Resolution, CP, PC, bounded-depth Frege), then Bridge(R) ⇔ P≠NP, so proving it is a restatement, not progress. Under p-simulation, a stronger system makes the bridge easier and the lower bound harder.
- **PROVED/EXACT (EF floor).** w_{R_mix341}(F) ≤ 2·|ER refutation of F|. So LB(R_mix341) implies a superpolynomial Extended Frege lower bound. No Frege lower bound is known (2026 literature check).
- **Bridge side for R_mix341.** It follows from FS-PV (LSPV-1/357): SAT∈P implies some polynomial-time decider whose rejection soundness is provable in PV. Status: OPEN.
- **Hard families.** PHP and odd Tseitin are retired as R_mix341-hard. Random 3-CNF at density n ≪ m ≪ n^{3/2} is the sole CANDIDATE, and its hardness is an EF-strength conjecture.
- **COMPUTATIONAL.** Exact minimum Resolution width on toy instances (`min_width.py`, `min_width_results.json`). Two instances are undetermined (timeout).
- **Next targets.**
  1. Does SAT∈P imply FS-PV for some decider? Compare with the Krajíček–Pudlák E=NE ⇒ p-optimal theorem.
  2. Does R_mix341 p-simulate the p-optimal system that exists under E=NE?
  3. Look for an EF-hardness candidate in the random 3-CNF window.
