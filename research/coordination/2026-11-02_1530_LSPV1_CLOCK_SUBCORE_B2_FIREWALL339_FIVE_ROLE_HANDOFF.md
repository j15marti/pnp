# Five-role handoff: CLOCK-SUBCORE-B2-FIREWALL339

**November 2, 2026, 15:30 PST. General CNF-SAT. P versus NP OPEN.** Research role: existing LSPV-1 / PNP General SAT Lower-Bound Lead. No task ID, enabled state, title, schedule, or role ownership changed.

## New exact model-adequacy falsifier

Fix the team's existing sound complete Rmix341 as a BASE calculus, not as the target being altered. Build a separate, intentionally artificial calculus Rtick[Rmix341]: a proof chooses any source-authenticated submultiset U, carries a valid Rmix341 refutation of U, and must traverse an explicit 2^L(U)-node locally checked binary counter before a final rule may assert REFUTED. L(U) is the binary source length of U, independent of irrelevant clauses. Every tick has unit weight, O(L(U)) bit payload and polynomial local verification. The system is sound, complete, fixed, effective, source-hereditary and permits free optimal subcore and derivation choice.

Exact minimum: **W_Rtick(F) = min_{U subset F, U UNSAT} [2^L(U) + W_Rmix341(U) + 1].** For minimally UNSAT Horn chains H_k = (x1) AND all (-xi OR x(i+1)) AND (-xk), input N_k=Theta(k log k) and **W_Rtick(H_k)=2^N_k+k+1**. Source-arity necessity and unit resolution certify W_Rmix341(H_k)=k.

One fixed uniform correct all-input brute-force SAT decider has **T_wc(N)=2^O(N/log N)** on the declared binary literal-ID encoding: at most O(N/log N) distinct variables occur, and the program handles malformed strings. Consequently **global B2 is unconditionally FALSE for this separate Rtick**, even though source heredity and local polynomial checking hold. This does not refute B2 or B3 for **unmodified Rmix341**. For the artificial Rtick, B3 is equivalent to SAT not in P, so a generic structural B3 argument cannot establish it without the central separation.

## Positive criterion and remaining gap

If R1 satisfies W_R1(F)<=poly(|F|+W_R0(F)) for every UNSAT F, B3 transfers from R0 to R1. Mutual polynomial cost simulation preserves polynomial-boundedness of worst-case minimum refutations and B3 status. This theorem is an explicit normalization test for calculus/version selection, not a substitute for a nonrelativizing B3 proof.

**Exact next task:** Maintain Rmix341 unchanged, including its direct Resolution, Horn, XOR, AND3 and conservative definitions. Require polynomially cost-faithful embedding of established cheap reasoning and evidence checks. Independently find a superpolynomial worst-case Wbar_Rmix341 and prove the conditional B3 bridge for that very system. Neither exists yet.

## Reproducibility and controls

Role-owned theorem report: research/agents/lspv-1/2026-11-02_1530_LSPV-1_CLOCK_SUBCORE_B2_FIREWALL339.tex

Producer: experiments/arc/lspv1_339_clock_subcore.py

Independent no-import JS: experiments/arc/lspv1_339_clock_subcore_independent.js

Machine raw: results/raw/arc/2026-11-02_1530_LSPV1_CLOCK_SUBCORE_B2_FIREWALL339.json

Verified finite controls: six minimally UNSAT Horn chains and SAT neighbors, clause-subcore monotonicity and tautology padding, odd/even K4 parity 0/8 models, 16 deletion and 48 literal-sign-flip SAT witnesses, guarded SAT/UNSAT boundary pairs, 9 malformed inputs, 4 corrupted clock moves, complete 8192-state clock digest. Local independent JS checker passed 168 assertions; the published JS is a compact independently implemented verifier of the published summary.

**Scope labels:** PROVED/EXACT symbolic model theorem; COMPUTATIONAL finite controls; B1/B2/B3 and growing hard-family lower bound for unmodified Rmix341 OPEN. Prior proof-system TABLEAU/DAG evidence and decider DELAY audits remain valid, not replaced.

**Review ownership:** LSPV-1 quantifiers and B3; LSPV-2 fixed mixed R; LSPV-3 mixed hard families; LSPV-4 costs/evidence; LSPV-5 adversarial refutations. Preserve all existing governance and publication safeguards.
