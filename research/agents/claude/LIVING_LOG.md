# Claude agent living log — worst-case derivation directive

Shared target: Wbar_R(N) = max over UNSAT F with |<F>| <= N of min over R-refutations of cost_R(pi);
bridge B_R: SAT in P => Wbar_R(N) <= poly(N). P versus NP remains OPEN in every entry below.

## 2026-11-10 15:51 PST — WR-BRIDGE-SQUEEZE-0001
Report: `research/agents/claude/2026-11-10_1551_CLAUDE_WR-BRIDGE-SQUEEZE-0001.tex`
- PROVED/EXACT (squeeze): if a superpolynomial lower bound on Wbar_R is already known (Resolution, AC0-Frege,
  Cutting Planes, Polynomial Calculus), then B_R is *equivalent* to P != NP. For those R the bridge only restates P != NP.
  Simulation monotonicity: R <=_p R' gives B_R => B_R'.
- KNOWN THEOREM (Cook 1975; Krajicek-Pudlak 1990): B_{R_T} holds whenever SAT in P is witnessed by a decider whose
  soundness T proves (T = PV gives Extended Frege). Residual of [P2-B2] = a provability gap.
- PROVED/EXACT (extensionality barrier): every sound polynomial-time decider A has an extensionally identical
  polynomial-time A' (padded with a search for short proofs of T's inconsistency) with T not proving Sound_{A'}.
  Reflecting on the given code therefore cannot prove the bridge; a proof must construct a new, provably sound decider.
- CONDITIONAL: if the /341 rules are locally sound and checkable in polynomial time, then B_mix341 => B_EF.
- No compile check: no LaTeX toolchain in the container; braces and environments checked by script.
- Next targets: (a) a uniform transformation from an arbitrary decider to a provably sound one (or an oracle/independence
  obstruction to one); (b) whether the Krajicek-Pudlak p-optimal construction under E=NE can be made a fixed system chosen in advance.
