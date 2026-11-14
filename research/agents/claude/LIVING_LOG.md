# Claude living research log (PNP)

Append-only log of Claude scheduled runs. Newest entry first. Status labels follow AGENTS.md. **P versus NP remains OPEN.**

## 2026-11-14 09:52 PST — BRIDGE-STRENGTH-0001
- **Target:** the shared worst-case minimum-derivation objective `Wbar_R(N)` and the "weakest sufficient bridge" B3: `SAT in P => Wbar_R(N) <= poly(N)`.
- **Result (PROVED/EXACT, elementary, not yet independently reviewed):**
  1. If SAT is in P, then B1, B2 and B3 are all equivalent to "R is polynomially bounded". B3 is weaker only because it is vacuous when SAT is not in P.
  2. B2 turns any lower bound on `Wbar_R` into a lower bound on the worst-case time of every SAT algorithm, up to a polynomial.
  3. For Resolution (using the known Tseitin-on-expanders bound), B2 implies that every CNF-SAT algorithm needs worst-case time `2^{Omega(N/log N)}` in bit length N. That is a length-measured ETH-type bound, much stronger than P != NP.
  4. Monotonicity: systems with a proved bridge form an up-set under p-simulation, and systems with a proved lower bound form a down-set. For every system with a known lower bound, B3 is equivalent to P != NP.
  5. Not charging for finding the best derivation sequence is sound for lower bounds (the user's clarification holds). The gap is that a general decider need not output a derivation.
- **Computational:** Tseitin DIMACS bit length is `Theta(n log n)`, checked against a closed form and against explicit K4 and prism builds (UNSAT, PASS).
- **Open:** B1, B2 and B3 for EF and for R_mix341; a superpolynomial EF-strength lower bound; P vs NP.
- **Sanity test for future bridge proposals:** a valid B3 argument must use rules that Resolution lacks. Otherwise, applied to Resolution, it would prove P != NP.
- **Files:** `research/agents/claude/2026-11-14_0952_CLAUDE_BRIDGE-STRENGTH-0001.tex`, `experiments/claude_bridge/`, `results/raw/claude_bridge/2026-11-14_tseitin_length.json`.
- **Not done:** root `main.tex` was not edited (Claude has no ownership region). No LaTeX compiler was available in the container; only a structural brace and environment check was run.

## Earlier Claude reports
- 2026-10-28: WORLD-LEDGER-0001, DIRECTPRODUCT-0001, TPORT-0001/0002, ONETAPE-0001 (see this folder).
