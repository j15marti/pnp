# RP DIGEST-PORTFOLIO8: restricted witness-density theorem, 2026-10-21 17:12 KST

For each n divisible by 3, construct 2^n connected proper 3CNF formulas F_a with the unique satisfying assignment a. Divide variables into triples, insert the seven clauses satisfied only by the designated triple value, and connect adjacent triples with redundant satisfied bridge clauses. Each formula has 8n/3-1 clauses, at most 8 occurrences per variable, and equal fixed-width encoded size.

A randomized verifier that accesses a formula only through a q-bit preprocessing summary and at most h adaptive yes/no checks of complete proposed assignments, accepting only a valid witness, has acceptance probabilities p_a satisfying sum_a p_a <= 2^q h. Thus some F_a has p_a <= h*2^(q-n). To achieve the RP 1/2 acceptance threshold for every F_a, necessarily h*2^q >= 2^(n-1). A cyclic uniform-suffix witness sampler attains equality on the forced family.

This proves a restricted information-interface lower bound, NOT P!=RP or P=RP. The formula family itself is easy in P; arbitrary algorithms may read clauses or exploit other mechanisms.

Reference audit: 38179 assertions, zero failures, exhaustive unique-witness testing for n=3,6, connected degree-8 tests up to n=9, UNSAT controls and 100 seeded arbitrary-summary controls.

Next: determine whether real completion-time WRAPPER candidates rely exclusively on q digest bits and h whole-witness checks, or whether original source reads, partial clause feedback, timing, or state provide an extra channel. Only apply the inequality once this interface is verified.

Prior related reports directly reviewed: REPLAY-STATE6, TRACE-FOURIER4, ANF7. P vs RP and P vs NP remain OPEN.