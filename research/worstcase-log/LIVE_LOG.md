# Living log: worst-case minimum-derivation-cost programme

Target: W̄_R(N) = max over UNSAT F (|<F>|<=N) of min over refutations pi of cost_R(pi); optimal sequence granted for free (search is not charged, which is legitimate for a lower bound on executing it).
Weakest bridge B3: SAT in P  =>  W̄_R(N) <= poly(N).
Status of P vs NP: OPEN. No superpolynomial W̄_R lower bound and no B3 transfer is established anywhere in this log.

## Entry 2026-11-03 (scheduled run, single agent)

CORPUS REVIEWED: repo tree; AGENTS.md; LSPV-1 335 (core reduction + explicit-generator barrier), LSPV-1 365 (budget-free ER2 acquisition); handoff index through 2026-11-03_1036. Not re-read byte-for-byte; main.tex and ownership regions NOT edited (not an LSPV role this run).

DUPLICATION / CONTRADICTION AUDIT: the task's formulation is the same as LSPV-1 335/364/365 (R fixed, free optimum, B3 primary). No contradiction found. Nothing below is claimed as new theorem content.

STATUS-CLASSIFIED OBSERVATIONS (KNOWN / reformulation level):
1. KNOWN (Cook–Reckhow 1979): a p-bounded proof system exists iff NP = coNP. So "SAT in P => some proof system has W̄ <= poly" is trivial (verifier runs the decider, proof empty). The content of B3 is entirely that R is FIXED independently of the decider A. B3 for natural R (Frege/EF) is a strong statement: it is equivalent to "P=NP => R is p-bounded" and, combined with an unconditional superpolynomial lower bound, would give P != NP. Both halves are individually open for EF.
2. Reformulation, not progress: superpoly W̄_R lower bound + B3 together are equivalent in strength to P != NP when R is sound; B3 alone cannot be proved by a relativizing argument if the lower bound for R also relativizes, since oracles exist with P^O = NP^O and others with P^O != NP^O. (Classification: barrier remark, ANALOGY level; the exact oracle-relativized statement of R was not audited.)
3. LSPV-1 335 Thm 2 stands: any explicit poly-time generated UNSAT family with superpoly W_R refutes the arbitrary-decider domination TR(R) for the SAME R. So hard instances for the transfer-compatible route must be non-explicit or algorithm-dependent.

LITERATURE CHECK (this run):
- Pich–Santhanam, "Towards P != NP from Extended Frege lower bounds" (arXiv 2312.08163 / ECCC TR23-199): conditional on EF non-p-boundedness plus a self-provability / witnessing-formula hypothesis (e.g. S^1_2 proving a poly-time function witnesses errors of small circuits for SAT), one obtains SAT needs superpoly circuits. This is the nearest published form of a "proof lower bound => P != NP" bridge; its hypothesis is exactly a B3-type provability assumption, not a proved theorem. Classification: ANALOGY/CANDIDATE needing a new bridge; hypothesis not discharged. Suggested follow-up: check whether the self-provability hypothesis can be stated for the repo's R_mix341 as a falsifiable lemma.
- Web search for 2026 proof-system-lower-bound => P != NP results: none accepted/peer-reviewed. Only unrefereed preprints (e.g. arXiv 2512.11820) and STOC 2026 IPS finite-field lower bounds, which bear on P vs NP only indirectly. Not adopted.

WHAT CHANGED RELATIVE TO ROOT MAIN: nothing; this entry only adds a log and a literature pointer.
STALE OR OVERSTATED CLAIMS FOUND: none.

NEXT TARGETS (priority order):
(a) State B3 for R_mix341 as a Pich–Santhanam-style self-provability lemma and test it against LSPV-4's syntax-U LOCAL-CONVERT counterexample.
(b) Hard-instance work must avoid poly-time-generated families (335 Thm 2).
(c) Independent red-team of any claimed superpoly lower bound against resolution, algebraic (IPS/PC), circuit/ER, shared-DAG and adaptive-switching bypasses.

P versus NP OPEN.
% END_OF_LIVE_LOG_ENTRY 2026-11-03
