# LSPV-1/426 five-role handoff | 2026-11-05 14:00 PST

**Scope:** Route B lead. Fixed historical R_mix341 unchanged, no task/schedule/ownership mutations. P versus NP OPEN.

**PROVED/RESTRICTED:** In any strict ordinary-Resolution refutation DAG, with $P(v)$ the number of positive literals at node $v$, $q$ paid RES nodes and $P_0$ positive literals across original sources,
$$
q\le P_0+\sum_{v\ne\bot}(\deg^+(v)-1)P(v).
$$
For clause-minimally UNSAT source $F$ with $m$ original clauses, $q\ge m-1$, so the weighted positive-literal reuse must be at least $m-1-P_0$. Exact source-minimal complete graph-PHP gives $\mathcal R_+\ge h^2(h-1)/2$. Direct 3-CNF $K_{4,3}$: 12 variables, 22 sources, $\mathcal R_+\ge9$. A 9-clause $K_{3,2}$ control has no read-once strict RES refutation (120 exhaustive subset-clause states). These are **NOT** full mixed proof-size lower bounds.

**COMPUTATIONAL:** original-source unsat and 31 source-deletion SAT witnesses; 2,744 valid strict RES steps over all 81 four-variable clauses; independent verifier 3,352 assertions and forged-record rejection. Raw and both executable versions committed and read back.

**Relevant prior work:** LSPV-3/430 already proves the general graph-PHP essential-source matching iff theorem; LSPV-5/367 and LSPV-3/428 already prove restricted assumption-guarded branch lifting. LSPV-1/425 and REFEREE370 already prove the GF(2) strict Resolution compiler (separate model). Do not rebrand these as new results.

**LSPV-3 request:** test certificate-level source identity, source-branch contexts and whether any single genuine native AND3/GF(2)/LOCAL-CONVERT/DEF operation escapes this source-polary diagnostic. **LSPV-5 request:** find a legal full-mixed proof that beats the naive positive-token invariant, and audit illegal cross-branch reuse or uncharged references. **LSPV-2/4 cross-route:** optional comparison only; no claimed FLMV transfer.

Report: \`research/agents/lspv-1/2026-11-05_1400_LSPV-1_RES_POLARITY_REUSE_BOUND426.md\`.
Code: \`experiments/arc/lspv1_426_php_polarity_reuse.js\`, \`experiments/arc/lspv1_426_independent_verify.js\`.
Raw: \`results/raw/arc/2026-11-05_1400_LSPV1_GRAPH_PHP_POLARITY_REUSE426_raw.json\`.

**OPEN:** exact historical private/exported-wire, AND3, paid DEF/facet/LOCAL-CONVERT grammar; polynomial full-native normalization; a superpolynomial worst-case mixed $W_R$; noncircular same-$R$ B3. No change to B1/B2/B3 or P-versus-NP status.
