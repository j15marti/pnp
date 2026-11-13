# Living log: worst-case minimum derivation cost programme (Claude scheduled routine)

Target: `Wbar_R(N) = max_{F UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)`, together with the bridge `B3_R: SAT in P => Wbar_R(N) <= poly(N)`.
Each run appends one entry. Status labels follow AGENTS.md. **P versus NP remains OPEN.**

## 2026-11-13 10:00 PST — BRIDGE-CLASS-0001
- Report: `research/agents/claude/2026-11-13_1000_CLAUDE_BRIDGE-CLASS-0001.tex`; check: `research/agents/claude/bridge-class/def_er_check.py` (68/68 PASS).
- PROVED/EXACT: `W_{R_mix341}(F) <= L_ER(F)`. Each Extended Resolution extension is one DEF node, so the full R_mix341 p-simulates Extended Resolution with constant 1.
- PROVED/EXACT corollary: a superpolynomial `Wbar_{R_mix341}` would be a new superpolynomial Extended Frege lower bound on CNFs. The Pich–Santhanam (FOCS 2019) barrier therefore applies directly.
- PROVED/EXACT: if `LB_R` is a known theorem (Resolution, Cutting Planes, Polynomial Calculus, bounded-depth Frege, every restricted subsystem the corpus has lower-bounded), then `B3_R` is equivalent to `SAT not in P`, so it is a reformulation. If P != NP, `B3_R` holds vacuously for every R.
- Reformulation: for R at least as strong as ER, `B3_R` is equivalent to "SAT in P implies some polynomial-time decider A has short R-proofs of its soundness tautologies". PV-provable soundness of A is sufficient. This is the LSPV-1/337 premise, now stated for the unmodified R_mix341. Status: OPEN.
- Literature: Cook–Reckhow 1979; Krajíček–Pudlák 1989 together with Book's theorem (SAT in P gives *some* p-optimal system, which is a failed transfer to a fixed R); Pich–Santhanam FOCS 2019; Arteche–Khaniki–Pich–Santhanam ECCC TR23-199.
- Next: either (a) pick a fixed R built to satisfy B3 (EF plus soundness axioms, as in TR23-199) and attack its lower bound, or (b) accept a weaker R and treat B3 as equivalent to P != NP, i.e. abandon the split.
