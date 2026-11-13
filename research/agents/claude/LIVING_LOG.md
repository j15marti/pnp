# CLAUDE living log — worst-case minimum derivation program

Scheduled-routine log for the shared target
`Wbar_R(N) = max_{F in UNSAT, |<F>| <= N} min_{pi: F |-_R bot} cost_R(pi)`
and the bridge `B3: SAT in P => Wbar_R(N) <= poly(N)`
(directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`).
Additive only: this log changes no schedules, roles, TMR/LSPV regions or root `main.tex`.
P versus NP remains OPEN.

## 2026-11-13 14:50 PST — B3-ORACLE-0001

Report: [`2026-11-13_1450_CLAUDE_B3-ORACLE-0001.tex`](2026-11-13_1450_CLAUDE_B3-ORACLE-0001.tex)

- **PROVED/EXACT (oracle collapse).** Relative to TQBF (or, for the plain version, to SAT itself),
  B3 is *equivalent* to `X(R)`: "Wbar_R is polynomially bounded". So a relativizing proof of B3
  proves X(R) outright. For size-compatible R that gives NP = coNP; if LB(R) holds, B3 is false
  relative to TQBF.
- **PROVED/EXACT (black-box indistinguishability).** Any B3 argument that uses the polynomial-time
  decider only through its input–output behaviour plus an oracle-machine time bound proves X(R)
  unconditionally. B3 must use the **code** of the algorithm. PQ ledger item 5 (black-box resource
  extraction) is a FAILED TRANSFER for B3.
- **PROVED/EXACT (collapse after the lower bound).** Once LB(R) is proved, B3(R) is equivalent to
  SAT ∉ P. For Resolution, Cutting Planes, AC0-Frege, PC and regular Res(⊕), LB is already a known
  theorem, so B3 there is exactly P ≠ NP.
- **PROVED/EXACT (price of a strong R).** If R p-simulates ER (paid DEF gates), LB(R) is a
  superpolynomial EF lower bound, which has been open since 1979.
- **KNOWN THEOREM + CONDITIONAL.** The one known code-using route is Cook–Krajíček 2007:
  `SAT in P => PV proves P=NP` would give B3 for EF-strength R. That premise is OPEN. The corpus
  already had this route (LSPV-5/317, LSPV-1/361); it is credited there.
- Literature check: superpolynomial lower bounds for general DAG-like Res(⊕) are still open
  (regular, depth-restricted and tree-like cases are solved: EGI 2024, Bhattacharya–Chattopadhyay
  arXiv:2507.23008, ECCC TR25-116/118).
- **Next missing implication:** a non-black-box (code-using) proof of `X(R)` from SAT ∈ P for the
  selected R, and, separately, LB(R). Both are OPEN.
