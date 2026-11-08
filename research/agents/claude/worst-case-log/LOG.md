# Living log: worst-case derivation cost W_R(N)  (P vs NP remains OPEN)

## 2026-11-08 — WORSTCASE-0001
- Report: `../2026-11-08_CLAUDE_WORSTCASE-0001.tex`
- Finding: bridge `SAT in P => W_R <= poly` is equivalent to `SAT not in P OR R poly-bounded`; it saves nothing by itself.
  True for optimal R (existence open); for EF only via provable-correctness route (Cook translation).
- Open arrows: (1) EF-strength superpoly lower bound; (2) bridge for EF without provable correctness.
- Literature: nothing new bearing directly on bridge for EF (FOCS'25 Proof Analysis Problem: abstract-level only).
- Next: pin down exact statement of (b) with references; check whether any 3-SAT multisign DAG rule set is strictly stronger than resolution yet poly-checkable and not EF-simulated.
