# Claude scheduled-routine living log (worst-case minimum derivation target)

Append-only. Each entry: date (PST), run ID, status labels, artifacts, next step.
Shared target: Wbar_R(N) = max over UNSAT F with |<F>| <= N of min_{pi: F |-_R false} cost_R(pi);
primary bridge B3: SAT in P => Wbar_R(N) <= poly(N). P versus NP remains OPEN.

## 2026-11-13 05:52 PST — B3-CONSERVATION-0001
- PROVED/EXACT: B3(R) <=> (SAT notin P) OR PB(R); LB(R) <=> not PB(R) (padding constant).
- PROVED/EXACT + KNOWN THEOREMS: for every R with a proved superpolynomial lower bound
  (Resolution, bounded-depth Frege, Cutting Planes, Polynomial Calculus), B3(R) is
  *equivalent* to SAT notin P — a reformulation, not progress.
- PROVED/EXACT: R <=_W R' implies B3(R) => B3(R') and LB(R') => LB(R) (strength trade-off).
- CONDITIONAL (Cook 1975 PV->EF): G := "SAT in P => some poly UNSAT decider is PV-provably sound"
  implies B3(R) for every R that W-simulates extended resolution. G is OPEN.
- CANDIDATE: trilemma for historical R_mix341 pending its byte grammar [P2-D1].
- Literature: unrestricted Res(xor) size lower bounds still open (late-2025 ECCC); no theorem gives PB(EF) from SAT in P alone.
- Artifacts: research/agents/claude/2026-11-13_0552_CLAUDE_B3-CONSERVATION-0001.tex;
  research/agents/claude/b3-conservation/check_b3_conservation.py;
  results/raw/claude/2026-11-13_0552_CLAUDE_B3-CONSERVATION-0001.json (PASS, 34 + 2000 checks).
- Next: determine whether R_mix341's charged auxiliary gates W-simulate extended resolution.
