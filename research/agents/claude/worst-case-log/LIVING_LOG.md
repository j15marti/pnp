# Living log: worst-case minimum-derivation programme (W_R(N))

Target: Wbar_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi); weakest bridge SAT in P => Wbar_R(N) <= poly(N).
Status of P vs NP: OPEN. No lower bound or transfer theorem is established by anything below.

## 2026-11-08 run (Claude, scheduled)
- Repo had no prior "shared worst-case directive" file; this log creates it. Report: `2026-11-08_CLAUDE_WORSTCASE-0001.md`.
- Result (PROVED/EXACT, elementary): bridge dichotomy -- see report. Summary:
  1. Bridge is vacuously true if P != NP, so it can only be *proved* usefully by a route that does not assume P != NP.
  2. For any R with an unconditional superpoly lower bound (resolution, cutting planes, bounded-depth Frege), "bridge for R" IMPLIES SAT not in P. So it is at least as hard as P != NP: dead route for weak R.
  3. For strong R (Frege/EF), a bridge is equivalent to R having poly proofs of soundness of every true poly-time SAT algorithm -- an optimality-type statement (Krajicek-Pudlak), open; Cook-Reckhow: Wbar_R superpoly for ALL R <=> NP != coNP, a statement STRONGER than P != NP.
  4. "Free optimal sequence" is harmless for lower bounds (min over pi is non-uniform), but then Wbar_R poly <=> R p-bounded, which already implies NP = coNP, so the bridge is NOT a consequence of SAT in P alone for non-optimal R.
- Next targets: (a) define time-space cost (length + clause space, pebbling-style) and test whether the bridge is easier for the cost measure "total work of a RAM tracing a decider" (then it is trivial but lower bound = P != NP restated); (b) enumerate exact small-N values of Wbar for resolution to calibrate hard families.
