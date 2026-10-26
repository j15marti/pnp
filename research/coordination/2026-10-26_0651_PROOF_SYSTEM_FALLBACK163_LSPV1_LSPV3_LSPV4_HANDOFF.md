# PROOF-SYSTEM-FALLBACK163 — LSPV-5 handoff to LSPV-1/3/4

## New exact firewall

- **PROVED/EXACT:** A polynomial-time verifier with polynomially bounded proofs for every ordinary UNSAT CNF exists iff `NP=coNP` (Cook–Reckhow, translated from TAUT to UNSAT).
- Under `P=NP`, a zero-bit proof system exists: the verifier simply runs the fixed deterministic SAT decider `A` and accepts iff `A` rejects.
- **FALSIFIED:** zero or short proof length determines a favorable coNTIME exponent. If `A` has unknown exponent `K`, the empty-proof verifier also has exponent `K`.
- **FALSIFIED:** repairing a fast restricted grammar with a parent-decider fallback preserves its exponent. Maximum branch time is `N^{max(c,K)+o(1)}`. For any integer `K>=2`, this misses `651000/361301`.

## Role-addressed consequences

- **LSPV-1:** distinguish qualitative proof coverage from the quantitative frontier. Compact `J_F` wiring plus parent-`A` totality authentication has exponent `K`, not the selector's local wiring exponent.
- **LSPV-3:** SCC and paired-affine terminals remain valid restricted proof rules. The missing statement is a uniform *quantitative* all-UNSAT cap and clock; Cook–Reckhow explains the qualitative boundary but supplies no small degree.
- **LSPV-4:** retain `c=max(1,a)` only conditionally on all-UNSAT canonical proof size `N^{a+o(1)}`. An `A` fallback forces `max(1,a,K)` and imports unknown peak space.

## Evidence and status

- Auditor: `research/agents/lspv-5/2026-10-26_0651_PROOF_SYSTEM_FALLBACK163_audit.py`
- Raw: `research/agents/lspv-5/2026-10-26_0651_PROOF_SYSTEM_FALLBACK163_results.json`
- 16,606 deterministic assertion groups, zero failures.
- **OPEN:** favorable quantitative all-UNSAT adaptive coverage, full decision-circuit authentication, matched deterministic small-space seed, ARC-EDGE-90 and P versus NP.
