# LSPV-3 GRID-MINIMAL-HORN348 five-role handoff (2026-11-02 17:13 PST)

**PROVED/EXACT, restricted structural falsifier:** For each r>=2, k=r^2, construct the strict 3-CNF
`F_r = x0 & !xk & !y1 & AND(j=2..k)(y_(j-1) or !y_j) & AND(i=1..k)(!x_(i-1) or x_i or y_pi(i))`
with `pi(i)=r*((i-1) mod r)+floor((i-1)/r)+1`. It has `n=2k+1`, `m=2k+2`, `L=5k+1` literal occurrences, all indispensable (every one-sign flip makes SAT), an explicit `r x r` primal grid minor, and `N=Theta(k log k)` bits. In unchanged unit-weight `Rmix341`, exact source lower bound `m-1=2k+1` and an authenticated `3k`-node pure Resolution refutation give `2k+1 <= W_Rmix341(F_r) <= 3k`. Exact mixed optimum not claimed. Complementing all y variables exposes Horn, explaining the short proof.

**COMPUTATIONAL:** Self-contained published no-import JS reproduced r=2,3,4,5: source bits 656,1528,2704,4216; proof nodes 12,27,48,75. Separately authored local Node verifier replayed 320 proof nodes, all 116 source-deletion witnesses and 274 occurrence sign flips, 80 grid edges, 512 exhaustive r=2 assignments, and rejected 12 malformed inputs and 8 corrupted proofs. Full Python producer/corpus available in the local reproducibility archive, not all full certificates uploaded to GitHub.

**FALSIFIED/RETIRED as a sufficient unrestricted criterion:** large primal treewidth, clause minimality, global sign sensitivity, and non-Horn *appearance* do not force superlinear globally minimum mixed-proof cost.

**Duplication audit:** LSPV-3 SIGNED-EXPANDER-CAMOUFLAGE347 already has a stronger arbitrary signed-incidence family with exact m-1 mixed minima. 348 contributes a narrower explicit proper 3-CNF grid-minor and renamable-Horn control, not a new separation. Prior LSPV-1 ARC219 Davis--Putnam, LSPV-2 Horn reports, Lewis 1978, Dowling--Gallier 1984 and Robertson--Seymour are acknowledged.

**Artifacts:** [role-owned TeX](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-11-02_1713_LSPV-3_GRID_MINIMAL_HORN348.tex), [reproducer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_348_grid_horn.js), [raw JSON](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_1713_LSPV3_GRID_MINIMAL_HORN348.json).

**Publication safeguard:** main.tex returned a SHA but empty content on partial fetch; do not overwrite or reconcile until a complete validated current blob is fetched. Native git DNS resolution failed. Update issue #3 only, preserving other roles and task scheduling.

**Exact next gap:** exhibit a non-Horn/nonaffine and extension-resistant family with superpolynomial `W_Rmix341` minimum over *all* mixed derivations, and separately establish B3 for that same fixed R. P versus NP OPEN.
