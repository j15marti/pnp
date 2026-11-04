# Worst-case derivation complexity — living log

Target: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi); weakest bridge B(R): SAT in P => W_R(N) <= poly(N).
Status: P vs NP OPEN. No lower bound and no bridge for a nontrivial R is established.

## 2026-11-04 run CLAUDE-WC-0001
- Report: research/agents/claude/2026-11-04_CLAUDE_WORSTCASE-0001.tex
- Result: B(R) is circular (equiv. to SAT not in P) for every R with a known superpoly bound (Resolution, Res(k), bounded-depth Frege, CP). Only systems with no known bound (EF, Frege) can carry a non-circular bridge.
- Result: "exists R with B(R)" is classically trivial (case split on P=NP); content = an explicit R plus a proof of B(R).
- Known route to B(EF): SAT in P via A with PV-provable correctness => EF p-bounded (Cook; Krajicek-Pudlak; verify refs). Gap: "no" answers of A carry no certificate.
- New target T-REFL (OPEN): weakest reflection hypothesis on A yielding B(R) for explicit R.
- Literature: Krajicek-Pudlak (optimal proof system <=> fast consistency prover; implied by NP=coNP, converse open); Joosten arXiv:2004.05431.
