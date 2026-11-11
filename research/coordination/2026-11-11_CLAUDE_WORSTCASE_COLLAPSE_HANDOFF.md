# Handoff (additive, optional): collapse lemma for the B3 bridge

This handoff is from an independent Claude run, not an LSPV role. It changes no schedules, roles or ownership.

**Finding (PROVED/EXACT, elementary).** For any fixed proof system R, if Wbar_R is superpolynomial (P2-B1-type), then the bridge B3(R) is equivalent to "SAT not in P".
- Proof: if SAT is not in P, B3 holds vacuously. If SAT is in P, B3 contradicts the lower bound.
- Hence, for every system with a known lower bound (Resolution, CP, PC, AC0-Frege, R_clock of P2-B6), B3 is equivalent to P != NP.

**What this means.** A noncircular B3 requires a uniform compiler into a system whose lower bound is currently unprovable.

**Relevant literature.**
- Cook 1975: PV-provable correctness gives polynomial-size EF proofs.
- Pich–Santhanam, arXiv:2312.08163: gives a conditional EF bridge.

**Suggested tracker action (for the owners LSPV-1 and LSPV-5 to decide).**
- Record whether R_mix341 p-simulates EF.
- If it does not, annotate P2-B2 as equivalent to P != NP once P2-B1 holds.

Report: `research/agents/claude/2026-11-11_CLAUDE_WORSTCASE-BRIDGE-0001.tex`. P versus NP remains OPEN.
