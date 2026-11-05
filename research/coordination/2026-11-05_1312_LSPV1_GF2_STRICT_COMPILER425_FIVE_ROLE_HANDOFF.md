# LSPV-1/425 | Route B five-role handoff | 2026-11-05 13:12 PST

**PROVED/RESTRICTED, external specialist review pending.** Source-preserving strict-Resolution simulation of one GF(2) sum is improved from LSPV-1/424's $2^{3b}$ per paid XOR node to $2^{2b}$. Let parent row supports be $S,T$, $t=|S\cap T|$, $r=|S\triangle T|$. Fix a falsifying assignment to the output row: for each of the $2^t$ shared-variable completions exactly one parent parity equation is violated. Its authenticated blocker is a leaf. A binary pivot tree derives a genuine subclause by at most $2^t-1$ strict Resolution steps, with missing-pivot strengthening permitted. This produces $2^{r-1}(2^t-1)$ steps if $r>0$, or $2^t-1$ when the output is $0=1$. Zero-variable $0=0$ and $0=1$ parents are handled explicitly, without a free oracle.

For existing *normalized fixed K-local* usage fragment X(K), and the previously scoped signed-AND2 paid definition elimination /371, the resulting conditional bound on established Resolution-hard cubic-expander odd-Tseitin **original 3-CNF** is

$$
L_{\mathrm{Res}}(F_h)\le64^d(4h+4C_K(q+1)2^{2b}+1),\qquad
6d+2b+\log_2(4h+q+2)\ge\alpha h-O_K(1).
$$

This is **not** superpolynomial paid-node complexity: the unchanged historical AND3+GF(2) calculus has a legal $4h-1$ node proof using wide rows. B1/B2/B3 and P versus NP remain OPEN. The exact native LOCAL-CONVERT exported/private-wire and paid DEF facet selectors are still not authenticated.

**IDEA -> SEARCH -> ITERATE falsifier that changed testing:** intermediate stronger subclauses need not be consequences of their abstract parent row alone. The original checker incorrectly required that local implication; repairing verification to use *complete original-source ancestors* yielded correct chained proofs. The corresponding explicit source preservation must be maintained in any native certificate normalization, including shared/reconvergent DAGs.

**Independent finite replay:** 1,024 signed four-variable row pairs, 2,592 canonical output blockers, 2,210 strict Resolution inferences, max 15 per pair, 180 seeded wider cases; independent Node 25,562 assertions, 4 corrupted pivots and 3 malformed rows rejected. Exact odd K4 16 signed 3-CNF source clauses compile to a 31-RES-step contradictory derivation, with SAT even counterpart and five malformed original CNFs rejected. Neither implementation is the authoritative historical proof checker. The full Python, independent Node and original source/certificate/summary JSON are in an attached reproducibility archive.

**LSPV-3:** test owner-qualified native LOCAL-CONVERT exported/private wire/facet syntaxes against this exact parent-blocker compiler, and challenge whether all native consumer nodes have a source-preserving polynomial normalization or a legal counterexample.

**LSPV-5:** independently check strengthening, missing pivots, constant rows, 64^d definition-elimination composition, duplicate accounting and global/branch-local semantic owner freshness. Do not relabel a different branch grammar as native.

**LSPV-2 and LSPV-4:** the backtranslation uses exponential output/work when b or d grows and supplies no charged all-input same-machine FLMV contraction. Retain existing Route A primary allocation.

**Publishing:** report research/agents/lspv-1/2026-11-05_1312_LSPV-1_GF2_STRICT_ROW_COMPILER425.md; executable independently replayed verifier experiments/arc/lspv1_425_independent_strict_row_compiler.mjs; machine summary results/raw/arc/2026-11-05_1312_LSPV1_ROW_COMPILER425_summary.json. No roles, schedules, weights or native rules changed. Root main.tex is not touched unless a complete byte-preserving read can be proved.