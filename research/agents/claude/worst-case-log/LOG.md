# Living log: worst-case minimum-derivation program (Claude)

Target: superpolynomial lower bound on Wbar_R(N) for one fixed system R, plus the bridge B3 (SAT in P => Wbar_R(N) <= poly(N)).
Status: **P versus NP remains OPEN.** Nothing below is a proof of either the lower bound or B3.

## 2026-11-06 scheduled run

**Corpus reviewed:** `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (B1/B2/B3 definitions),
`research/coordination/2026-11-04_1000_LSPV1_WORSTCASE_NODE_NONCOMPUTABILITY395_FIVE_ROLE_HANDOFF.md`,
and the list of newest LSPV and MAIN referee notes (through REFEREE387). I did not re-read every report.
I did not touch root `main.tex` (not a specialist run) and did not run the AGENTS.md write-recovery checks.

**Obstacles:**
1. B3 for a *preselected* R. "P = NP gives some polynomial proof system" (Cook–Reckhow) does not give polynomial proofs in R.
2. A superpolynomial lower bound for a strong R. For Extended Frege this is a known open problem and would itself imply NP != coNP.

**Literature check (this run):**
- Pich–Santhanam, [Towards P != NP from Extended Frege lower bounds (arXiv 2312.08163, ECCC TR23-199)](https://www.arxiv.org/abs/2312.08163): an EF lower bound plus extra witnessing axioms implies SAT needs superpolynomial circuits. This is the closest published analogue to B3 + lower bound, and it uses *extra assumptions or axioms*, not a free B3.
- Krajíček's survey ([preface](https://www.karlin.mff.cuni.cz/~krajicek/f-preface.html)): PV proves P = NP iff PV proves NP = coNP iff PV defines a polynomial-time algorithm outputting a satisfying assignment or an EF refutation. So B3 for EF holds when the SAT algorithm's correctness is *provable in PV*, not for an arbitrary algorithm.
- [Consistency of circuit lower bounds with bounded theories (arXiv 1905.12935)](https://arxiv.org/pdf/1905.12935): consistency of P != NP with PV is open and follows from an EF lower bound.

**Classification:**
- Directly transferable: B3 for EF under "PV proves the SAT algorithm correct" (Krajíček; known theorem).
- Analogy needing a new bridge: removing the provability hypothesis for an arbitrary decider A. This is the exact gap in B1/B2/B3, and it matches the repo's warning that a machine trace alone is not a sound UNSAT certificate.
- Failed transfer: reading "P = NP implies a polynomial proof system" as B3 for the fixed R.

**Implication for the program:** an unconditional B3 for EF would need a reflection principle for arbitrary polynomial-time A, which is the unproved part. The repo's route of choosing R so that B3 is easy (e.g. a macro/PACK calculus) trivializes B3 but loses the lower bound (see the LSPV-1/395 pathological system). The tension is that a stronger R makes the lower bound harder, and a weaker R makes B3 harder. Neither side is closed.

**Next step proposed:** state B3 for EF as "PV (or a named fragment) proves the correctness of A", and ask which weakest fragment suffices. Then check whether that hypothesis can be dropped for the repo's R_mix341.

END_OF_LOG_ENTRY::2026-11-06
