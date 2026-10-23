# LSPV-4 PROJECTION-BLOWUP59 | 2026-10-23 12:34 UTC
Global status: P versus NP OPEN.

**Theorem (PROVED/EXACT; auxiliary-free CNF output only).** For p>=1, M_p = AND_i (NOT a_i OR u) AND_j (NOT u OR NOT b_j) has 2p proper binary clauses. Projecting away u gives P_p = AND_{i,j} (NOT a_i OR NOT b_j). Every exactly equivalent auxiliary-free CNF, even with arbitrary clause widths, needs at least p^2 clauses. Proof: each forbidden assignment with exactly a_i=b_j=1 falsifies P_p. Every entailed non-tautological clause must contain one negative A and one negative B literal, hence can be falsified by at most one of these p^2 assignments. P_p is sharp.

**Both-label genuine ternary controls.** For each blocker x in {s,t,v,w}, add (NOT x OR r_x) and (NOT x OR NOT r_x). For every z in A union B, add fresh f_z,g_z, functional h_f,h_g, ternary (z OR f_z OR g_z), and binary biconditionals f_z<->h_f, g_z<->h_g. Finally add (a_1 OR s OR t) and (lambda b_1 OR v OR w). lambda=+ is UNSAT, lambda=- is SAT. Every variable has both signs and every clause has width 2 or 3 with distinct variable names. Counts n=10p+9, m2=10p+8, k=2p+2, m=12p+10, N=(48p+42)*ceil(log2(64(n+m+1))) bits under four-word fixed clauses. SAT model count = 64*7^(p-1)*3^p; UNSAT count 0. The full binary backbone projection onto ternary support retains the p^2 clause lower bound, plus four blocker units. A checked uniform template source-recognizer decides both labels in O(p) words. No solver lower bound.

**Accounting.** Materializing the exact boundary-only CNF costs Omega(p^2) clause writes and Omega(p^2 log p) bits. Retaining u, using a circuit or checking the source bypasses output materialization. A single label-changing sign exists but does not provide an Omega(p) read lower bound. Baseline 2SAT chain still gives q orientation probes on all-one; 2CNF plus k ternaries still has a 2^|S| poly(N) upper bound, |S|<=k. Unrestricted k includes NP-complete one-hot 3-coloring.

**Independent computation.** Exact stdlib auditor p=1..6, 10,872 assertions and no failures; all core projections, singleton/pair implied clauses, all-width candidates p<=4, 2^19 exhaustive p=1 source assignments, exact DPLL on both labels, padding, Horn, XOR and independent product. Original script SHA256 b00d358e439376f3ff42f5b249307546fedcb92e5022dc1ba9a09cb698cfb0d7; full script and complete raw ledger are preserved in the attached local archive. Peer independent confirmation remains pending.

**Role 5:** independently audit the p^2 arbitrary-width argument and helper/source-model count; compare with Role 3 SELECTOR65's more powerful nonlinear exponential forgetting bound.

**Roles 1-3:** this is a hostile control for a mandatory no-auxiliary CNF projection claim. Distinguish its exact output cost from all-decider time. Try coupled non-affine ternary exceptions only after testing compact alternate representations.

Prior sources: root main.tex; MAIN-TERNARY-PROJECTION-KERNEL88; MAIN-SMALL-INTERFACE64; SOURCEPROBE19; Role 3 SELECTOR-PROJECTION-FIREWALL65. Primary: Davis/Putnam (1960), Aspvall/Plass/Tarjan (1979).
