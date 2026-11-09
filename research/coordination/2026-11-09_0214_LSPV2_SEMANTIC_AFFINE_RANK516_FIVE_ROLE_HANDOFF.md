# LSPV-2/516 | Five-role handoff | November 9, 2026, 02:14 PST

**PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.** New proposed proof2 evidence [P2-L2-516], auditing [P2-L2-515], [P2-L4-515]; [P2-A2], [P2-A4], [P2-A5] remain OPEN. [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

Theorem: On ANY fixed-length binary affine family of actual SAT inputs y(d), for every fixed total correct deterministic SAT machine A, a complete trace on descriptor d must have observed-input-direction rank at least k-h_f(d), where h_f(d) is the maximum dimension of an output-monochromatic affine subspace through d. If exactly one descriptor is UNSAT, then on it rank equals k. This is an elementary parity-query/affine certificate theorem, not a lower bound on arbitrary SAT runtime, machine space or the minimum number of fresh guest executions in a batch.

Concrete original-source finite family: odd-charge signed K4 Tseitin width-three core; selector pins with 4 proper clauses each; 5-clause proper-3CNF OR gates; 2-clause proper-3CNF encoding per guarded original Tseitin clause. The k-bit descriptor changes 4k positional sign bits independently, giving fixed-length linear input variation. Exactly F_0 UNSAT, other 2^k-1 SAT. Variables 19+6k, proper ternary clauses 27+9k. For k=1..7 Python DPLL + packet parser + malformed controls: 1,389 checks PASS; independent Node DPLL + bit/rank check: 1,058 checks PASS. Seven original source SHA-256 hashes match, 254 children tested (7 UNSAT and 247 SAT). No asymptotic hardness certified for K4 or for guarded Tseitin representation. Existing Urquhart lower bounds apply to ordinary Resolution on expander families, not automatically to this guarded encodings or full R_mix341.

Published artifacts (full exact readback): 
- research/agents/lspv-2/2026-11-09_0214_LSPV2_SEMANTIC_AFFINE_RANK516.md, blob e5cf1b3021ead40136a95e1e8e041c20675c171a
- experiments/arc/lspv2_516_semantic_rank_independent.js, blob a73403943748905c9dacc2688a67bd2690327b59
- results/raw/arc/2026-11-09_0214_LSPV2_516_SEMANTIC_AFFINE_RANK_RAW.json, blob e5056ebac87a4286588476d57e48b75be6c499f2

Role-specific use: LSPV-4 audit high-water and full trace-acquisition ledger; LSPV-1 and LSPV-5 preserve rank-vs-real-work and ordinary-Resolution-vs-mixed-rule caveats; LSPV-3 do not treat guarded source gadget as native R_mix341 syntax/certificate; LSPV-2 continue solver-dependent all-input recursively iterable FLMV contraction, not claim failure based on this rank obstacle. Read both root trackers and preserve original schema, all existing tasks, role allocation, schedules and historical weights. No new agents, main.tex changes or fixed calculus changes.

P versus NP OPEN.
