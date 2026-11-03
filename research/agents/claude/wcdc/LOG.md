# WCDC living log: worst-case derivation complexity  W_R(N) = max_F min_pi cost_R(pi)

Directive (user): fixed sufficiently powerful inference system R; free choice of optimal derivation (no charge for search);
priority = weakest sufficient bridge  SAT in P  =>  W_R(N) <= poly(N). P vs NP remains OPEN.

Append one dated entry per run. Never delete earlier entries; mark superseded ones.

## 2026-11-03 23:50 UTC  (WCDC-0001)  report: ../2026-11-03_2350_CLAUDE_WCDC-0001.tex
- PROVED/EXACT: min over free strategy = Cook-Reckhow proof size; W_R poly for some R iff NP = coNP.
- PROVED/EXACT (dichotomy): for any R with a known superpoly lower bound (Res, CP, PC, AC0-Frege) the bridge is
  *equivalent* to P != NP, so it is not a weaker target. For Frege/EF the bridge is not known and the lower bound is open.
- PROVED/EXACT (conditional bridge): SAT in P via M + short Frege proofs of Sound_{M,N} => W_Frege poly.
  The bridge costs exactly the certified soundness of the decider; not free from SAT in P alone.
- Union/strategy-switching systems inherit the strongest component (no middle ground).
- Literature: Pich-Santhanam STOC'21 (+ follow-ups) = analogy only; Atserias-Mueller = strategy search NP-hard (consistent);
  Razborov 2015 / Krajicek generators = only route beyond Res-like, tied to crypto assumptions (inadmissible).
  Several cited facts (Tseitin/Frege, PHP/EF, Li-Oliveira attribution) from memory: RE-VERIFY next run.
- Open next: (1) unconditional P=NP => EF p-bounded? (2) minimal fragment verifying the trace-evaluation step,
  (3) space-bounded bridge.
- Not edited: root main.tex (no ownership region for this author).
