# LSPV-4 ARC-ASSIGNMENT-STATE-FIREWALL259, 2026-10-30 17:36 PDT
**Single integrated direction:** arbitrary correct SAT decider A -> Phi(A), universal adaptive parameterized residual SAT, actual strict FLMV Theorem 5.7. Both P=NP and P!=NP OPEN. Preserve existing five research agents and their schedules/enablement.

## New restricted result
A controller obliged to retain an exact internally mutable t-pin assignment state for n named variables, with later arbitrary \`status(x_i) in {unassigned,0,1}\` queries and without a free copy of update history, must distinguish \`binom(n,t)*2^t\` states. Thus at least \`ceil(log2(binomial(n,t))+t)\` abstract bits; on a fixed finite-tape polynomial-time FLMV machine with one fixed original input, \`Omega(n)\` counted space for \`t=Theta(n)\`, accounting for the at-most \`O(s+log T+log N)\` bits of head-position state. In strict signed exact-(2+,2-) 3CNF with fixed-slot \`N=Theta(n log n)\`, this is \`Omega(N/log N)\`, incompatible with the proposed \`N^0.501131...\` writable-space target. The only forbidden implementation is the *universal stable dense assignment interface*, not unrestricted SAT, implicit recomputation, source-aware semantics, witness streaming, or polynomial algorithms that don't store assignments.

An exact complementary observation: every strict22 original variable has four occurrences and induces at most six overlapping original clause pairs. Thus at most \`6n\` of the \`binom(m,2)\` pair-mode records are nontrivial; full materialization costs quadratic space unnecessarily. On W1 and matched signed-swap SAT, 73 of 190 original clause pairs share a variable, with both original 2+/2- quotas intact. Source S/U targets and all four modes were checked rather than promoted into a SAT oracle.

## Independent and same-source audit
The original source-indexed JS reproducer and full 166,071-byte raw JSON are committed with exact readback. Nine exact SAT/UNSAT controls passed 1,311,384 original clause/complement identity checks, 1,808 pair SS/SU/US/UU modes and 1,240 triple modes. W1 UNSAT 0 models / 151 DPLL nodes / 10,388 declared selected operations; signed-swap W1 SAT 168 models / 19 nodes / 1,408; H1 SAT 4 models / 7 nodes / 197. Eager full S/U diagnostics plus identical DPLL cost respectively 108,096, 99,086 and 31,789 selected charged operations, including conservative upper-bound triple enumeration; no node reduction. The independent checker separately confirmed both W1 labels, endpoint false-clause counts (1,2) on both sources, t-pin state cardinalities 160/59136/96096 with bit minima 8/16/17, and exact infinite-tail FLMV fractions.

**Exact FLMV:** d*(6/5)=23/45 and d*(241/200)=11642479/23232400. For each, k=2 beats k=1,3 and all k>=4 by c^-4<d2. Entry must be strict and same deterministic indexed read-only-input random-access machine, not selected-operation event proxies.

## Published verified artifacts
- [Formal report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-10-30_1736_LSPV-4_ARC_ASSIGNMENT_STATE_FIREWALL259.tex)
- [Primary executable JS](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-10-30_1736_LSPV4_ARC_ASSIGNMENT_STATE_FIREWALL259_repro.js)
- [Complete raw results](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-10-30_1736_LSPV4_ARC_ASSIGNMENT_STATE_FIREWALL259_raw.json)
- [Independent executable checker](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-10-30_1736_LSPV4_ARC_ASSIGNMENT_STATE_FIREWALL259_independent.js)
- [Independent exact summary](https://github.com/j15marti/pnp/blob/main/results/summaries/arc/2026-10-30_1736_LSPV4_ARC_ASSIGNMENT_STATE_FIREWALL259_independent.json)

## Prior work and boundary
Independent theorem review still pending. Standard information counting is not asserted to be new; this is a different declared interface than LSPV-4 RESPONSE-WIDTH258 (ordered child-label decoder), SELECT-INDEX252 (single-level prefix directory), HIGHWATER254 (physical buffer allocation), and LSPV-3 ADDITIVE-MULTIPLICATIVE-GATE257 (two tariffs). AFFINE-SMALLBIAS-DESCENT-GATE2 remains a restricted affine MCSP no-go. CONSTRUCTION-STRENGTHEN17/CP22LIFT1 do not certify an on-demand strict22 native small-space emitter. This run does not use the retired cosine/t+s bound or transfer an information-state-interface lower bound to arbitrary SAT machines.

## Next OPEN arrow
Find an exact both-label hereditary N^{1/2}-bit ordinary child generator with N^{3/5} children, without a permanently retained Omega(N/log N) root state, and charge every replay and policy switch in the native FLMV machine. If such representation is semantic or regenerative, prove acquisition and access bounds rather than assuming a free assignment-state oracle. No universal ARC contraction known.
