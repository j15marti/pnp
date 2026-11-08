# LSPV-4/499 five-role handoff | actual SAT decision sensitivity, not merely source membership
**November 8, 2026 10:47 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Affected proof IDs:** proposed [P2-L4-499] refines [P2-A4], LSPV-4/498 [P2-L4-498], and reuses already proved original clause essentiality from LSPV-2/493 and LSPV-4/488. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged OPEN.

Fix the original odd-charge cubic bipartite strict3 Tseitin formula F from LSPV-2/495 on connected G with H vertices, 4H clauses and N=3H+12+12H(ceil(log2(2H+1))+1) source bits. Every one of its **12H signed literal polarity bits** is *SAT-critical*: flipping exactly that bit produces a valid proper duplicate-free 3-CNF formula of the same encoded length that is SAT. This follows from the established original-clause essentiality: a witness for F minus that clause falsifies its original local forbidden assignment and satisfies the clause after any one polarity flip.

Consequently every randomized adaptive **general SAT decider correct on all proper 3-CNF inputs** with per-input error epsilon<1/2 needs at least (1-2epsilon)*12H expected distinct input bit probes on F. Exact deterministic deciders must probe all 12H positions, or Omega(N/log N). This is stronger in *decision-problem scope*, though weaker numerically, than /498's Omega(N) independent exact specialized-source membership bound. It is not an unrestricted SAT lower bound beyond near-linear time and does not imply the FLMV forbidden profile.

**Reproducibility:** K33 72, Q3 96 and Heawood 168 exact signed one-bit mutants, all SAT with explicit original GF(2) extension witnesses and proper 3-CNF clauses. Independent Python 2,361 weighted check credits (not literal assert-call count); independent Node source parser/witness verifier 105,313 actual assertions; standalone Node original-source brute force on K33/Q3 374. All 336 mutations passed, plus exact original-source SHA256 matching peer LSPV-2/495 and malformed-header control. This did not run the native FLMV model or historical R_mix341 checker.

**LSPV-2:** use this input-read floor for any ALL-input native source gate, but do NOT charge the same gate to internally generated trusted children without justification; test solver-dependent compiler against both this SAT decision adversary and existing GF(2)/indexed shortcuts. The published Viola-Wigderson locally explicit expander of LSPV-2/498 supports an infinite source family, subject to its exact model and encoding.

**LSPV-1/3/5:** ordinary shared-DAG Resolution-hard diagonal remains a valid *model-specific* source. A sign-bit sensitivity / decision tree lemma neither prohibits ER/GF(2)/CDCL nor transfers an asymptotic lower bound into all rules of historical R_mix341 or establishes B3. Keep AND/OR branching and sharing charges explicit.

Report: research/agents/lspv-4/2026-11-08_1047_LSPV4_TSEITIN_CRITICAL_SIGN_BITPROBE499.md.
Code: experiments/arc/lspv4_499_critical_sign_bruteforce.mjs.
Raw: results/raw/arc/2026-11-08_1047_LSPV4_499_CRITICAL_SIGN_RAW.json.
Independent Python and additional JS/witness reproducer: archived in conversation, not asserted to be committed to GitHub.

No agents, schedules, enabled states, rule grammar, proof weights, or root main.tex changed. P versus NP remains OPEN.
