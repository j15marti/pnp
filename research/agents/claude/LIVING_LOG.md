# Claude living log: worst-case minimum derivation programme

This log is append-only. Each scheduled Claude run adds one entry. **P versus NP remains OPEN.**

Target: $\overline W_R(N)=\max_{F\in UNSAT,|F|\le N}\min_{\pi:F\vdash_R\bot}\mathrm{cost}_R(\pi)$ for the fixed system R_mix341. Primary bridge: B3, `SAT∈P ⇒ Wbar_R ≤ poly(N)`. See `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.

## 2026-11-10 16:00 UTC: WBAR-CALIBRATION-0001
Report: `research/agents/claude/2026-11-10_1600_CLAUDE_WBAR-CALIBRATION-0001.tex`
- **PROVED/EXACT:** On the SAT side, the minimum work to reach the minimal reduced state is O(N): the free best sequence guesses a satisfying assignment and checks it. Only UNSAT can be hard, so the worst-case minimal work equals Wbar_R.
- **PROVED/EXACT (from known theorems):**
  - If NP≠coNP, then Wbar_R is superpolynomial (Cook–Reckhow).
  - If R simulates Extended Resolution (ER), a superpolynomial Wbar_R bound implies that Extended Frege (EF) is not polynomially bounded. For R_mix341 this is CONDITIONAL on the exact-source ER translation.
  - If R is polynomially equivalent to EF, B3(R) is the same as "P=NP ⇒ EF polynomially bounded". That is the Pich–Santhanam programme.
- **Literature delta:** ECCC TR26-018 (Itsykson–Podolskii–Shekhovtsov, CCC 2026) proves superpolynomial Res(⊕) size bounds only for depth o(n²/log⁴n); unrestricted Res(⊕) superpolynomial bounds are still open. These results transfer down to the DEF-free fragment of R_mix341, but not to the full system.
- **Next subgoal (CANDIDATE, OPEN):** a lower bound for the DEF-free fragment, using the fact that clause lines and XOR-row lines stay separate.
- No bridge is claimed, and root main.tex was not edited.
