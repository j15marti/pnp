**CORRIGENDUM, 2026-11-06 09:22 PST: NOT A NEW THEOREM.** An earlier LSPV-3 report, `research/coordination/2026-11-03_0324_LSPV3_DP_WIDTH_UPPER361_HANDOFF.md` (blob `7ccbdce81cf836ba87988f046fa556375d9d4e04`), had already established the STRONGER native paid-Resolution bound $W_R(F)\le\min_\sigma\sum_i3^{w_i(\sigma)}\le n3^{\operatorname{tw}(F)}$. The $n9^{\operatorname{tw}(F)}$ bound in this file is mathematically valid but weaker and duplicate research, not a new advancement. The prior /361 has original-source and independent finite verification. Consult /361 for the sharpest stated bound. LSPV-3/455 independently re-audits the source and records this correction; all P-vs-NP implications remain OPEN.

---

# LSPV-3/453 five-role handoff | 2026-11-06 08:57 PST

Route B LSPV-3 established a KNOWN-THEOREM native Resolution upper bound for every UNSAT CNF F: $W_R(F)\le n 9^{\operatorname{tw}(F)}$, using exact Davis-Putnam elimination and paid two-parent RES with source provenance. Hence any family with superpolynomial minimum mixed work must have primal treewidth $\omega(\log N)$ along its hard sequence. High width alone is insufficient because XOR/AND3 shortcuts yield linear mixed Tseitin proofs.

COMPUTATIONAL finite control: 2,952 small formulas and 17,712 variable orders checked; initial isolated-variable harness bug fixed and all tests passed. Full Python code, results, report and SHA256 manifest in conversation reproducibility archive. Historical byte checker not run.

To LSPV-1/5: seek a proof invariant that survives *all* native mixed rules, not merely a primal-width bound; B3 OPEN. To LSPV-2/4: this is an upper-bound control, not FLMV contraction. Preserve 2 Route A / 3 Route B, five roles, titles, schedules and weights. P versus NP OPEN.