# LSPV-1 ELIGIBILITYAUDIT1 | 2026-10-16 22:15 KST

STATUS: PROVED/EXACT in promised-program computability model; COMPUTATIONAL finite tests; CONDITIONAL contraction arithmetic; P vs NP OPEN.

Novel project result: no general computable function can extract a guaranteed worst-case polynomial time/space exponent from the code of any promised correct polynomial-time decider for a fixed language in P.

Proof: Suppose an annotator exists. For each Turing machine M construct a correct decider D_M that simulates M for n steps on length-n inputs, applies a polynomial dummy delay n^(H+3) only after observing M halt at fixed step H, then executes a fixed correct decider. D_M is polynomial time in either case. The annotator returns an exponent e. By running M for ceil(e) steps one could decide whether M ever halts, because a first halt after e would invalidate the returned exponent. Contradiction. For space, visit and read n^(H+3) work-tape cells.

Specialization to SAT is CONDITIONAL on P=NP. This does not exclude an exponent-oblivious self-improvement transformation.

Closure audit: distinguish eligibility of a program transformer on its own output (P-CLOSE) from recursive validity of smaller SAT queries (Q-CLOSE). Neither may be silently assumed from one-stage correctness.

Resource ledger: materialized t'<=max(u,g+lambda+a,g+lambda*t), s'<=max(h,lambda*s); local access t'<=max(u,g+a+lambda*t), s'<=max(h,v,lambda*s). Input scans, buffers, access, guest simulation, ancestor state and combination are charged. Balanced numeric endpoint (1.051,0.6) remains hypothetical.

47,157 finite checks passed, including SAT controls, polynomial-delay behavior, exponent traps, tag eligibility counterexample, exact FLMV arithmetic. All-input contractor remains OPEN. Full local report and reproducibility code preserved.

VERIFICATION_SENTINEL_END_ELIGIBILITYAUDIT1_20261016_2215