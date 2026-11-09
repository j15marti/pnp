# Five-role handoff: LSPV-1/528 pair-defect compatibility spectrum

**2026-11-09 00:10 PST | Route B LSPV-1 | PROVED/RESTRICTED spectral lemma, COMPUTATIONAL independent controls; P versus NP OPEN.**

**Material evidence node:** [P2-L1-528], spectral decomposition of the pair-defect clause-compatibility graph on any simple 3-vertex-connected cubic modulo-three Tseitin source. This is distinct from **pre-existing** exact minimum original UNSAT-source-core theorem [P2-L3-522] and supports its independent checking rather than claiming a new exact minimum. References [P2-L3-521], [P2-L1-523], [P2-L5-452]. Load-bearing [P2-D1], [P2-C3], [P2-B1], [P2-B2] all OPEN. proof1 remains OPEN and unchanged.

For G on h vertices, H_G has 9h original R-clauses as vertices. Two R-clauses at different graph vertices are joined if one F3 edge-flow realizes those two as the only defect clauses. G 3-connected implies nonadjacent blocks J9 and adjacent blocks three K3,3. Its spectrum is:

$$
\{9h-27\}\uplus\{-9-6\lambda_i(A_G):2\le i\le h\}
\uplus\{3\}^{3h}\uplus\{-3\}^{3h}\uplus\{0\}^{2h}.
$$

**Proof:** orthogonal decomposition of real functions on each nine-tuple affine F3 plane into constants, three two-dimensional incident-edge coordinate spaces, and a two-dimensional residual, followed by block diagonalization. No new proof inference rule or oracle.

**K4 audit:** H_K4 has 36 vertices, 162 edges, regular degree nine and exact spectrum {-3 x15, 0 x8, 3 x12, 9 x1}. Hoffman gives alpha<=9 and one original vertex's complete nine R clauses attain it. Hence 27 original R clauses must be used, 42 ALO/E clauses individually mandatory, yielding known minimum 69 sources and (under bounded-binary source-explicit unit-cost inference DAG assumptions) at least 68 paid inferences. This **duplicates the number in LSPV-3/522**, not its proof method. No strengthening of [P2-B1] or [P2-B2].

**Controls:** independently executed Python exact enumeration/MILP of K4 and separate Node reconstruction including 262,144 Boolean assignments and all 69 single-clause-deletion witnesses. Exact matrix polynomial A(A-9I)(A-3I)(A+3I)=0 passed. Independent numeric general-family formula checks: K4, K3,3, cube and Petersen (h=4,6,8,10). Full historical accepted-byte R_mix341 checker not run. Parent variable-definition facet ownership still unresolved.

**Artifacts:** research/agents/lspv-1/2026-11-09_0010_LSPV1_PAIR_DEFECT_SPECTRAL_SOURCE_COVER528.md; experiments/arc/lspv1_528_k4_spectral_exact.js; results/raw/arc/2026-11-09_0010_LSPV1_528_PAIR_DEFECT_SPECTRAL_RAW.json. Independent Python scripts and full logs remain downloadable as separate run artifacts. Root main.tex returned empty content despite sha fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba; intentionally unchanged.

**To LSPV-3:** compare spectrum lemma with original proof [P2-L3-522]; investigate whether equivalent subspace decompositions can certify clause-compatibility under weaker connectivity or other published-hard families, but do not repeat the 69-source result as new.

**To LSPV-5:** independently check the nonadjacent pair extension condition and adjacency block decomposition, especially the distinction between source cover and any accepted-byte R_mix341 proof cost; inspect for hidden use of full source semantics.

**To LSPV-2/4:** this is a static proof-complexity source-cover diagnostic only. It does not imply universal FLMV residualization or time-space contraction.

**Lead's next load-bearing target:** authenticate full R_mix341 DEF owner-facet accepted bytes, then test complete original-source global ER2 cancellation and the same-calculus B3 implication. Preserve schedules, task identities, roles, two Route A / three Route B allocation and original inference weights. P versus NP OPEN.
