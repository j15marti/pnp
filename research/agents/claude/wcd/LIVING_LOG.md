# Living log: worst-case minimum derivation cost (Claude scheduled routine)

Target (2026-11-02 directive): `Wbar_R(N) = max_{F UNSAT, |<F>|<=N} min_{pi: F |-_R bot} cost_R(pi)`.
Goals: a superpolynomial lower bound for one fixed R, plus the weakest bridge B3: `SAT in P => Wbar_R(N) <= poly(N)`.
Free optimal-sequence selection is allowed; proof search is not charged.
This log is append-only. Newest entry first. **P versus NP remains OPEN.**

## 2026-11-14 03:50 PST, run WCD-RELBARRIER-0001
- Report: `research/agents/claude/2026-11-14_0350_CLAUDE_WCD-RELBARRIER-0001.tex`
- PROVED/EXACT, relativization barrier: `Wbar_R` is oracle-free. Under the TQBF oracle, NP^O = P^O. So if B3 or B2 holds relative to every oracle, `Wbar_R` is polynomial. Any true lower bound LB(R) therefore forces a non-relativizing proof of the bridge.
- PROVED/EXACT: for any R with a known lower bound (Res, CP, AC0-Frege), B3(R) is equivalent to P != NP. Choosing a weak R does not make the bridge weaker.
- PROVED/EXACT, difficulty exchange: B3(R) and LB(R) together are equivalent to P != NP and LB(R). Strengthening R moves difficulty from the bridge to the lower bound, and weakening R does the reverse.
- PROVED/EXACT, given LSPV-1/357 (RES+VARDEF = ER2): a superpolynomial `Wbar_{R_mix341}` implies superpolynomial ER/EF lower bounds, which is a long-open problem.
- CANDIDATE: an algebrization analogue.
- Red-team falsifier: any oracle-uniform trace-to-proof compiler cannot prove B2 or B3 for a system with a true lower bound.
- The PQ ledger item 5 (black-box extraction) is a FAILED TRANSFER for B3.
- Literature: Pich–Santhanam arXiv:1905.12935; Pudlák arXiv:2007.14835; Aaronson–Wigderson ECCC TR08-005; BGS 1975; Cook–Reckhow 1979; Krajíček–Pudlák 1989.
- Root main.tex not edited: this routine is not an LSPV owner. Recommended to LSPV-5: add the barrier to the P2-B2 ledger.
- NEXT: formalize algebrization (IKK); check whether natural proofs block LB(R) for R containing ER; look for a B3 route through universal search plus a PV-provable UNSAT verifier.
