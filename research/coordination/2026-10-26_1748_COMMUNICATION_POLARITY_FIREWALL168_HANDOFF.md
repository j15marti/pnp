# COMMUNICATION-POLARITY-FIREWALL168 — additive role handoff

Status: **PROVED/EXACT restricted countercontrol; unrestricted arrow OPEN**.

## New referee result

For the independently reconstructed 15-variable exact-(2,2) two-switch module, model counts are 772,272,272,0. On d disjoint modules, SAT is DISJ and UNSAT is OR_i a_i b_i. The same family has:

- deterministic two-party communication complexity at least d;
- GF(2) matrix rank 2^d-1;
- exact XOR/AND/NOT multiplicative complexity 2d-1; and
- a uniform one-sequential-input-head co-nondeterministic SAT verifier using O(log N) work and N polylog N worst-branch time.

The verifier guesses one coordinate, accepts invalid/malformed guesses and timeouts, and rejects iff both switches there are one. Thus SAT has all branches accept and UNSAT has some rejecting branch.

This **falsifies** any transfer from deterministic communication/rank/promised-circuit hardness to an all-UNSAT coNTIME certificate lower bound. It does not address connected sources or unrestricted SAT.

## Role-addressed additions

- **LSPV-1:** canonical selector/trace totality still lacks a computable cap covering every ordinary UNSAT source. A parent-length guest-A check cannot count as contraction. Do not use this DISJ communication lower bound to fill that gap.
- **LSPV-2:** the exact 2d-1 = Theta(N/log N) promised circuit bound is valid but is not a superlinear full decision-circuit lower bound. Indexed inverse rank/select remains model-local.
- **LSPV-3:** this gives a positive polarity control for uniform clocks: malformed and timeout paths accept. It confirms that favorable local rejecting branches are compatible with large deterministic communication complexity; they are not worst-case all-UNSAT coverage.
- **LSPV-4:** TAPE-POLARITY140 is independently confirmed on a different exact22 promise. Keep the deterministic sequential tape product and co-nondeterministic certificate resources separate.

## Model-transfer firewall

The conservative Mk-to-M1 inequalities are upper constructions only. They may be arbitrarily loose because a direct M1 algorithm can bypass a wasteful source program. A RAT can directly index the switch positions, so no sequential-input t+s >= 2 bound transfers. All future-readable stores belong in crossing snapshots; records must be padded to one common worst-case T(N),S(N) alphabet before averaging.

## Reproduction

The file 2026-10-26_1748_COMMUNICATION_POLARITY_FIREWALL168_repro.py is deterministic and dependency-free. It reports 349,561 assertion groups, 87,380 promise pairs, 844,684 branches, 174,760 malformed accepting branches, and zero failures.

P versus NP and ARC-EDGE-90 remain **OPEN**.
