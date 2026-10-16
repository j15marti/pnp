# LSPV-3 SEEDREPLAY14 handoff to LSPV-4 and LSPV-5
Status: scoped exact theorem; P versus NP open.

A fixed public generator G mapping a seed s of at most c log2(N+2) bits to a fully encoded satisfiable formula F of N bits and a valid witness, in polynomial N time, admits one fixed polynomial-time witness finder. That finder enumerates at most 4(N+2)^c seeds, recreates each entire candidate formula, compares exact bytes with the unchanged input F and verifies its paired witness. The finder has constant description length and becomes eligible in the UWI logarithmic program budget for sufficiently long inputs.

LSPV-4: audit source-planted shield constructions for low seed length plus cheap witness replay before claiming any general forced work.

LSPV-5: after proper-3CNF or exact-(2,2) compilation, check the paired generator's seed length and time against final output length. No source decoding is needed for exact replay.

Tests: 136 proper 3CNFs; 136 satisfiable clause-order permutations outside the generator image; 3288 assertions, zero discrepancies. Full local source, raw results and LaTeX preserved. The unconditional UWI common-input theorem is OPEN.
