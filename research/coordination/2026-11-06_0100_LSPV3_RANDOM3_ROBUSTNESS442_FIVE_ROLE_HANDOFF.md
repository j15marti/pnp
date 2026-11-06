# LSPV-3/442 Five-role handoff | 2026-11-06 01:00 PST

**Existing allocation unchanged: two Route A (LSPV-2/4), three Route B (LSPV-1/3/5).** No changes to active tasks, times, weights or role ownership. P versus NP OPEN.

**Established direct strict-3 family:** for n variables, m=8n independently uniform random proper width-three signed clauses. Chvátal–Szemerédi (JACM 1988) establish exponential *unrestricted shared-DAG ordinary Resolution* size a.a.s. at c=8,k=3. Pang (arXiv:2610.00837v2, 2026-10-24) **reports** exp(Omega(n)) unrestricted DAG Res(PC_1/F_2)=Res(XOR) size on the same distribution; this recent result is an *unrefereed preprint* and has not been independently fully verified here. No 3-CNF reduction or gadget preservation needed. Neither theorem covers R_mix341.

**NEW PROVED/EXACT:** For d(F)=min over assignments of the number of falsified *indexed original source clauses*, deleting at most k clauses preserves UNSAT when d(F)>k. In the above random model,

$$
\Pr[d(F)\le n/10]\le \exp[-(8D_{\mathrm{KL}}(1/80\Vert1/8)-\ln2)n]
=\exp(-0.03211993244018\ldots n).
$$

Thus all sufficiently large such random hard inputs have no individually essential clauses with high probability, and are robust to deletion of ANY <=floor(n/10) indexed source clauses. The source-indispensability `m-1` lower-bound arguments in /341 and /440 cannot be applied to these inputs without a new premise. Their earlier theorems are not refuted.

**COMPUTATIONAL:** n=12 seed=36, m=96, all 4096 assignments falsify >=5 clauses, certifying 3,469,497 arbitrary deletions of <=4 source indices preserve UNSAT. Five total original-source fixtures including a planted SAT control; independent Python replay 91,136 assignments with source SHA-256 comparison, four malformed source rejections and polarity-hash rejection. No finite proof-size hardness certified.

**LSPV-1:** distinguish two restricted theorem statuses and their input-bit lengths (B=O(n log n)); no B3 inference. **LSPV-3:** search accepted native AND3/GF(2)/DEF/LOCAL shortcuts with branch scope, reconvergence and shared nodes; do not rely on all m sources being indispensable. **LSPV-5:** audit Chernoff bound, duplicate source indices, strongest algorithms and proofwise transfer; challenge Pang's unreviewed model match. **LSPV-2/4:** stay on all-input same-machine FLMV Route A and use the family only as negative control where relevant.

**Artifacts:** report `research/agents/lspv-3/2026-11-06_0100_LSPV3_RANDOM3_CLAUSE_ROBUSTNESS442.md`; standalone `experiments/arc/lspv3_442_random3sat_robustness.js`; summary `results/raw/arc/2026-11-06_0100_LSPV3_RANDOM3_ROBUSTNESS442.json`; complete independent checks in local reproduction archive.

Root main.tex blob had zero readable bytes; no unsafe update performed. Native R_mix341 facets, full mixed-DAG normalization, superpolynomial Wbar_R and B3 remain OPEN.
