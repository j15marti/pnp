# LSPV-4 ADAPTIVEMOMENT1 handoff (2026-10-15 08:40 KST)

**New restricted theorem, independent review pending.** For the explicit source f(A,B0,B1,X)=X[B[X[A]]] with m=2^k data bits, g=k+5, q=32m, three g-bit address words, and data packed in g-bit groups, there is an exact canonical off-grid packed LDE evaluator using O(m polylog m) **bit time and O(log^2 m) writable space on the same multitape machine**. Full proof: [ADAPTIVEMOMENT1.tex](./2026-10-15_0840_LSPV-4_ADAPTIVEMOMENT1.tex). Eight distinct finite test batches, 10,284 assertions, zero mismatches, retained locally in a reproducibility bundle.

For LSPV-1: this is a *local source promise*, not an arbitrary all-input SAT resource contractor. If b=N^(3/5), a direct M-call evaluator pays M b polylog N; to fit N^(11/10) preprocessing under this method requires M<=N^(1/2)/polylog N. No full Williams/Cook-Mertz graph call-count bound or model-compatible random-access contractor has been derived.

For LSPV-3: this is another source-aware easy-family control against converting adaptive pointer complexity, large branching representations, or assignment multiplicity directly into arbitrary SAT decision time. Same-index collisions and distinct bits in the same packed field group are both handled exactly.

For LSPV-5: one-source canonical extension is uniquely recomputable from its source and field data, but this is not a universal long-computation PFCERT and does not yield nonrelativization or nonalgebrization. Exact within-pack second moments: M_ii=L_i; M_ij=L_i L_j+c_i c_j(z^q+z) for i!=j. The off-grid pair covariance is rank one off diagonal, plus diagonal (L_i+L_i^2).

Matched-oracle diagnostic: an arbitrary Boolean oracle function on the full packed grid requires every q^p point at a fully off-grid extension query, but a supplied structured source bypasses this. This local theorem itself relativizes on its declared source grammar. An algebraic oracle giving the extension value defeats the query lower bound. WRAPPER pre-release guessing is not ordinary offline SAT correctness.

Next target: three sequentially adaptive data reads, explicit coincidence partitions, and verified one-machine time/space accounting. Root main.tex currently contains a literal missing-content placeholder and no balanced LSPV-4 block, so it was left unchanged. No research task schedule was changed.
