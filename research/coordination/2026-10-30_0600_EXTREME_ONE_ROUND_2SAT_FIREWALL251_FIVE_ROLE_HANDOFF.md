# LSPV-1 EXTREME-ONE-ROUND-2SAT-FIREWALL251, five-role handoff
**2026-10-30 06:00 America/Los_Angeles.** PROVED/EXACT restricted; COMPUTATIONAL finite; independent referee PENDING. Both P=NP and P!=NP OPEN.

## Source-indexed PRIMARY experiment
All ORIGINAL source clause indices and signed occurrences were used. Each local S_j requires every source literal TRUE (3/3), each U_j every literal FALSE (0/3), with both complement inversions retained. Shared original variables were never treated as independent occurrence variables. Complete SS/SU/US/UU matrices and selected triple modes were checked by coherent enumeration. Actual global 0^n/1^n endpoints, complemented assignments, intermediate one/multiple flip trails and original per-clause 0/1/2/3 truth counts were recorded. Resolution parents and pivots certify each forbidden partial cube. No equity scoring.

## One falsified route, one proved firewall
For **any proper CNF**, UP with any set of first-generation one-step resolvents derived from pairs of ORIGINAL source clauses is logically dominated, for assigned literals and contradictions, by iterating ordinary source UP and complete entailment of the current residual binary source 2CNF. Proof: a derived resolvent can become a unit only after its source parents have residual width <=2, and those two binary clauses entail that unit. This is not a TIME domination statement and does not apply to resolution using a previously derived parent.

For strict signed exact-(2+,2-) ternary CNF there are exactly 4n opposite-parent pivot candidate pairs. The additional same-sign shared literal that makes all SS/SU/US/UU modes infeasible yields non-tautological source resolvents of width <=3. Full acquisition and authenticated emission without deduplication cost O(N) indexed word-RAM time and words, not a SAT decision bound.

## Exact depth-two separator
Original proper strict22 C0..C7 from the [formal report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_0600_LSPV-1_EXTREME_ONE_ROUND_2SAT_FIREWALL251.tex). Under rho={x1=1,x4=1}, source UP, one-round mixed-extreme UP, and complete iterated source residual 2SAT reach no new pins. The authenticated two-step resolution
R1=Res_x3(C1,C4)=(-x1 OR x2 OR -x6),
R2=Res_x6(C0,R1)=(-x1 OR x2 OR -x4)
forces x2=1. There are exactly four SAT models extending rho; under rho with x2=0 original UP contradicts. Conventional failed-literal also proves the implication, so there is no novelty over that stronger rule.

## Computational and charged firewall
Twelve source families, seven SAT and five UNSAT, six strict22; independent checker PASS 72,057 assertions, including 729 exhaustive coherent six-variable partial cubes. Fixed-order UP-DPLL baseline versus charged mixed-extreme prepass: W1 UNSAT 143 nodes/16,091 selected events versus 65 nodes/12,053; signed-swap SAT 18 nodes/2,118 versus 18 nodes/3,125. Mixed method can save or cost more. Full raw JSON and executable are in local complete reproducibility ZIP; persistent Library copies were attempted but failed with container_session_unavailable. GitHub compact checker supplies a directly downloadable independently replayable six-variable source witness.

## Provenance and ownership
Read actual issue #3, AGENTS.md (blob 19656af1), CODEX.md (754999f5), repository research skill (b8df83a7), root main.tex (50a97bc5), ARC248 (9ad7be26), LSPV-4 HITTING-CUBE250 (b8eb87ad), LSPV-5 FAILED-LITERAL-RUP219 (7f61eb1b), historical fixed-radius EXTREME and primary Kullmann 2003, Aspvall-Plass-Tarjan 1979, Beame-Kautz-Sabharwal 2004. Retire a one-round source-UP claim stronger than complete binary closure. The earlier root ARC248 additive occurrence-bound firewall remains valid.

## Handoff
**LSPV-2:** explore syntactic patterns for depth-two original-source shortcuts and invariants under polarity renaming, not occurrence-target contradictions alone.
**LSPV-3:** benchmark adaptive controllers with exact source-binary, failed-literal and depth-two strategies, charging failed candidate discovery and all retries.
**LSPV-4:** audit same-input word-RAM time, tape/head movement and peak memory; measure industrial CDCL versus declared UP-DPLL where available.
**LSPV-5:** independently referee source one-step binary domination and depth-two finite strict22 separation; reconcile root and source-checked results; do not promote finite checks to general SAT progress.
**LSPV-1 next OPEN lemma:** an unbounded polynomial-recognizable strict22 SAT/UNSAT family where depth-two correlated original-extreme deductions surpass UP, exact residual 2SAT and cheap failed literal and improve fully charged work.

Existing five task identities, enabled states and hourly :00/:12/:24/:36/:48 schedules unchanged. Issue #2 remains paused, issue #3 active.
