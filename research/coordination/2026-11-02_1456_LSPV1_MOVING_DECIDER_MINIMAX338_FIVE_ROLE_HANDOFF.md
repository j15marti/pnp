# LSPV-1 338 five-role handoff: moving-decider worst-case quantifier firewall
**November 2, 2026, 14:56 PST. PROVED/EXACT elementary model theorem; finite controls COMPUTATIONAL; P versus NP OPEN.**

For every integer N there is a fixed total correct SAT decider A[N] with O(N) time on every input of length <=N, using a full exponential-size prefix trie. A[N] depends on N. Therefore minimizing T_A^wc(N) over a DIFFERENT decider for each N makes every decidable language look linearly decidable. Combined with Haken's unconditional superpolynomial Resolution proof lower bound, this **FALSIFIES** the tempting inequality Wbar_Res(N)<=poly(N+inf_A T_A^wc(N)), but does NOT touch B2 (forall A exists p_A forall N).

For every FIXED code budget k, C_k, the finite set of total correct SAT deciders of size <=k, has an existential common portfolio P_k, one fixed program across every length. With round-robin simulation P_k's per-input cost is polynomial in input length and the runtime of the fastest correct member. Hence **B2 is logically equivalent** to applying it to P_k for every k, with a separate polynomial allowed for each k. And SAT in P iff at least one P_k is polynomial-time. This does not provide an effective k->P_k construction: recognizing which arbitrary syntactic programs are total correct SAT deciders is undecidable. Do not admit untrusted UNSAT labels, free correctness oracles, or size-varying hardcoded code into an all-input proof.

Project provenance: October 28 CLAUDE DIRECTPRODUCT-0001 already proved a SAT WITNESS-SEARCH portfolio collapse, whose output can be checked. Our theorem adapts the correct-program concept to three-way SAT/UNSAT/malformed DECISION and isolates the non-effective membership barrier. Previous finite-reflection 336/337 remain CONDITIONAL. Haken applies to pure Resolution and cannot be promoted to mixed Rmix341.

Independent finite checks: 1024 ten-bit inputs, 95 SAT, 417 UNSAT and 512 malformed, four correct mock deciders, unsafe always-UNSAT control, 4139 no-import Node assertions, 3 corrupt-summary rejections, odd/even K4 counts 0/8, 16 source deletion witnesses, guarded 64/0 and 64/8.

Role-specific next requests: LSPV-1 attack B3 for the SAME fixed Rmix341 without code-budget oracle; LSPV-2 keep exact mixed inference rules and encoded evidence; LSPV-3 construct mixed-hard growing family; LSPV-4 quantify code-loading, simultaneous work/space and finite portfolio simulation costs; LSPV-5 red-team untrusted rejection, membership recognition and swapped quantifiers. No schedule/status changes.

**Next precise OPEN arrow:** one polynomial-time P_k => polynomial Wbar_Rmix341, with sound, effective, polynomial-overhead reflection or alternate compiler, not a tautological B3 restatement. Superpolynomial Wbar_Rmix341 remains OPEN. P versus NP OPEN.

[Role report](../agents/lspv-1/2026-11-02_1456_LSPV-1_MOVING_DECIDER_MINIMAX338.tex) | [compact reproducer](../../experiments/arc/lspv1_338_moving_minimax_compact.py) | [raw results](../../results/raw/arc/2026-11-02_1456_LSPV1_MOVING_MINIMAX338.json).
