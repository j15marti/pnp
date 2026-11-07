# Five-role handoff | LSPV-1/470 | November 7, 2026 PST

**Material restricted finding for [P2-D2] only.** The signed source-authenticated general-CNF family F(U,S) encodes SET COVER in the minimum cost over a *layered subset* of legal binary Resolution refutation DAGs. Every set activation s_j costs one globally shared paid node; each element goal g_i costs one; every goal is required to close the final negative clause with k paid Resolution steps. The precise restricted optimum is

$$
W_{\mathrm{layer}}(F)=2k+\tau(U,\mathcal S).
$$

Therefore deciding whether the minimum within this fixed layered grammar is <=2k+b is NP-complete by Karp's SET COVER. A legal shortest proof has <=2k+r nodes and all covered formulas have a trivial polynomial-time UNSAT recognizer, so NP-hard *optimal proof search* is not a lower bound on proof work or SAT decision.

**Proof system qualification:** Every emitted proof is a sound source-authenticated ordinary Resolution DAG, but only the layered subgrammar is optimized. No claim about unrestricted Resolution, historical R_mix341, R_mix341 accepted bytes, original strict 3-CNF, or all-machine SAT hardness. Do not import restrictions into fixed Rmix341 to obtain a lower bound. This is an exact countercontrol for branch-by-branch minimization and discovery-cost mischarging.

**Published evidence:** Report \`research/agents/lspv-1/2026-11-07_LSPV1_SET_COVER_SHARED_RES_OPT470.md\`; executable \`experiments/arc/lspv1_470_layered_setcover_resolution.cjs\`; raw \`results/raw/arc/2026-11-07_LSPV1_470_SET_COVER_SHARED_RES_RAW.json\`. Standalone code blob \`dca97dc50099c89b0d5250e1de329239d0df3871\` read back and V8-executed exactly: 57,164 finite set systems, 105,218 assertions, 1,502 full Resolution proofs, 235 source truth-table SAT/UNSAT controls and nine rejected corruptions. No native Rmix341 checker or FLMV machine was executed.

**LSPV-3:** Test whether any source-authenticated *full* mixed native grammar permits a cheaper bypass; maintain strict assumption and original-source scopes. **LSPV-5:** Confirm NP-hardness quantifiers and disallow promoting restricted-grammar optimizer hardness to W_R or P != NP. **LSPV-2/LSPV-4:** Preserve ideal work vs actual optimizer time/space distinction, full same-machine resource charging. **LSPV-1:** Refocus immediately on historical grammar and noncircular B3, not more toy optimizer families.

proof1.txt and proof2.txt reviewed. [P2-D1], [P2-B1], [P2-B2], [P2-C3], [P2-A2], P versus NP remain OPEN. Five tasks, identities, allocation (2A/3B), times, historical weights/calculus and main.tex unchanged.
