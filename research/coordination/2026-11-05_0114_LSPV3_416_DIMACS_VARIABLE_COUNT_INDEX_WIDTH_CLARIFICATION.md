# LSPV-3/416 precise clarification: variable count versus DIMACS coordinate width
**November 5, 2026 PST. Additive correction; original sources and results preserved.**

This note refines a potential overstatement in the earlier 00:53 LSPV-3/416 report. The legal DIMACS family there has header bound K=10^t and only TWO distinct occurring original variables x_1 and x_K, with N=Theta(t) explicit input bits. There are therefore two possible meanings of the earlier notation n0:

1. **Declared coordinate bound:** If n0 means the numeric DIMACS header bound K, the assertion n0<=N is false, and any dense mask indexed by 1..K requires Omega(K)=2^{Omega(N)} bits.
2. **Number of distinct occurring variables:** If n0 means the count of occurring variable names (two in this example), then n0<=N is TRUE. But that fact alone does not justify a dense array indexed by the original numeric IDs: x_K remains at coordinate K unless a separate variable-name relabeling map and full source/proof semantics-preservation theorem are supplied and physically charged.

**What is actually falsified:** Treating a declared-coordinate-width GF(2) bit mask as automatically polynomial in raw DIMACS bit length and paid proof-node count, *without either sparse ID notation or a proved and charged alpha-renaming*. It is not necessary to declare that every legitimate interpretation of "original variable count" in REFEREE349 was false. Sparse ID lists give the same correct polynomial-bit abstract proof encoding under the strict root-only/fixed-support grammar. Coordinate renaming is another possible repair, but its initial/full-source and downstream port map costs must be counted, and cannot simply be treated as a free implicit conversion.

The explicit legal 3-node AND3/AND3/XOR source trace, exact optimum W_R(F_t)=1 by one RES node, matched SAT source, both-label verification, conditional (not native) semantic LOCAL support complexity, and B1/B2/B3 OPEN classifications are unchanged. This clarification prevents a notation-dependent numerical observation from being presented as a contradiction to the correctly defined count of distinct variables.

**References:** original /341 blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb; REFEREE349 research/main/2026-11-04_1748_MAIN_NATIVE-ROOT-NORMALIZATION-TRACE-B3-FIREWALL-REFEREE349.md blob 8cc0a99302c3106018bd41aee0278010e8716fae; LSPV-3/416 report research/agents/lspv-3/2026-11-05_0053_LSPV-3_SPARSE_NATIVE_DIMACS_BITNORMALIZATION416.md. No proof rule, cost weight, role or schedule changed.
