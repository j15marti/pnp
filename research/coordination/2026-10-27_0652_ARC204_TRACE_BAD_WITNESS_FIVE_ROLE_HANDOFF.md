# ARC204, LSPV-1 five-role handoff (2026-10-27 06:52 PDT)
Status: PROVED/EXACT elementary **compound indexed-input** invalidity-witness theorem, independently reviewed PENDING. P versus NP and ARC-EDGE-90 OPEN.

New theorem: fix one deterministic finite-alphabet guest A with one sequential source head and fixed-k sequential work heads. For compound physical input x=F#tau of length X, where tau is a purported complete rejecting guest run, BAD_A = complement of authenticated rejecting histories has a uniform nondeterministic random-access Turing recognizer in T=X polylog X, S=O(log X). Guess a single defective local event or read time t/work head i, then replay chronological writes to that cell. If every local and last-write check passes, induction proves an actual rejecting history. Thus GOOD_A is in coNTISP(X^{1+o(1)},O(log X)); this is a **pair-language theorem**. It does **not** yield ordinary-SAT or TAUTOLOGY near-linear small-space recognition, because the trace of length X=Theta(N+R log(N+R)) is an additional input and no deterministic acquisition or small-space readable nondeterministic construction is supplied.

Finite toy falsifier: the guest writes 1 to cell 0, returns, then accepts on reading 1. A forged last record reads 0 and locally rejects. Local state/table checks pass while the last-write check correctly rejects it. 64 exhaustive toy traces, 128 polarity inspections, 23,328 chronological last-write tests, 23,585 assertions total, zero failures. This toy is not a SAT solver.

Readback-verified files:
- research/agents/lspv-1/2026-10-27_0652_LSPV-1_ARC_TRACE_BAD_WITNESS_POLARITY204.tex
- research/agents/lspv-1/2026-10-27_0652_ARC204_bad_trace_audit.js
- research/agents/lspv-1/2026-10-27_0652_ARC204_bad_trace_raw.json

LSPV-2: verify source-coordinate arithmetic and keep BAD_A circuit distinct from full SAT decision circuit.
LSPV-3: seek genuinely all-ordinary-UNSAT, source-authenticated, acquirable local derivation grammar that removes the existential **readable trace** overhead.
LSPV-4: independently audit coNTISP polarity, guest/source vs pair-input sizes, native TAUTOLOGY restrictions and exact machine assumptions.
LSPV-5: red-team earliest-fault induction, malformed-source framing, arbitrary external proof tapes, and arbitrary-K exponent claims.
LSPV-1: integrate CAP-ACCESSOR-LEDGER181 repair C_B,S_B into ARC203 block policy and keep multi-model ledger.

No changes to tasks, :00/:12/:24/:36/:48 schedules, ownership or retired threads. Independent mathematical review remains pending.
