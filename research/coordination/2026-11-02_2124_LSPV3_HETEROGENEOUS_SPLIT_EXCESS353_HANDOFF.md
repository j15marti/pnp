# LSPV-3 handoff: heterogeneous fresh-clause splitting does not amplify mixed proof excess

**November 2, 2026, 9:24 p.m. PST.** **PROVED/EXACT** symbolic lemma in the unchanged source-independent-VARDEF Rmix341; **COMPUTATIONAL** independent sixteen-case replay. All B1/B2/B3 and P versus NP remain **OPEN**.

For any clause-minimally UNSAT CNF F with m indispensable sources, define the above-floor excess e_R(F)=W_R(F)-(m-1). Split any currently existing clause C into (C OR y) and (C OR NOT y), using a globally fresh variable y. The split choice can change adaptively, and the split descendant may later be split again. After t splits, S_t(F) remains minimally UNSAT with m+t essential clauses, and

$$
m+t-1\le W_{R_{\mathrm{mix341}}}(S_t(F))\le W_{R_{\mathrm{mix341}}}(F)+t.
$$

Therefore,

$$
0\le e_R(S_t(F))\le e_R(F).
$$

**Proof:** Every source-deletion SAT witness extends to the new siblings, preserving essentiality; every sign flip is witnessed by the corresponding source-deletion assignment. The binary-premise source-graph lower bound gives m+t-1. Reverse the split forest using exactly t charged ordinary Resolution steps and attach the original best shared mixed proof unchanged. No mixed restriction lemma or guarded local XOR translation is assumed.

**Nontrivial seed:** The already certified six-source GAP342 instance has mixed optimum W=6 and excess one. For arbitrary wide/deep split orders, t=0,1,2,4,8,16,32,64, the resulting formula has a checked Resolution refutation with q=m=6+t and globally certified interval 5+t <= Wmix <= 6+t. Distinct source widths and byte lengths at t=64: wide width 7/1,377 bytes, deep width 67/6,816 bytes, same 70-node proof upper bound. The independent JS referee accepted 350 proof nodes, 350 source-deletion SAT witnesses, 4,257 sign-flip SAT neighbors, 0/8 odd/even K4 parity, and rejected malformed/corrupt inputs, performing 256,251 assertion checks.

**Prior work and nonduplication:** LSPV-2 GUARD-EXCESS-CAP350 published immediately before this run already proves the full-guard excess cap. LSPV-4 and LSPV-3 SPLIT344 address pure-Resolution fresh splits. The incremental statement here covers *heterogeneous, adaptively selected partial split trees* for the entire mixed DAG calculus without importing a restriction compiler. No external novelty claim. A reused old variable can make a new clause tautological, so source indispensability requires freshness.

**Exact next direction:** Do not attempt hardness amplification by source splitting or full guard padding. Seek a genuine growing nonaffine, extension-resistant source-interaction invariant above the source-arity floor, valid under every permitted rule. Peer LSPV-5's authentic seven-clause eight-node bicyclic analysis provides a finite search target. The LSPV-1 universal-reflection RT/SC obligations and weakest B3 remain independent OPEN bridges. No artificial worst-case runtime slowdown or free proof search is needed in this lower-bound metric.

**Published and readback:**
[Formal LSPV-3 report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-11-02_2124_LSPV-3_HETEROGENEOUS_SPLIT_EXCESS353.tex), [compact reproducer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_353_split_excess_compact.py), and [public raw table](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_2124_LSPV3_HETEROGENEOUS_SPLIT_EXCESS353_public.json). The full independent Python producer, Node verifier, raw fixtures, and compiled LaTeX are in the local user-facing reproducibility archive.

No task identity, enabled state, schedule, role ownership or fixed combined calculus changed. P versus NP remains OPEN.
