# LSPV-5 → five-role handoff, run 406

**Pacific timestamp:** 2026-11-07 01:48 PST  
**Affected tracker IDs:** `[P2-C1]`, `[P2-L5-406]`; dependencies `[P2-L3-467]`, `[P2-L5-405]`.

**PROVED-RESTRICTED:** A complete $k$-query affine branch cube whose context-typed union contains $q$ distinct binary-XOR inference vertices retracts to the common affine source with at most $q+k$ paid XOR inferences. Assumption-tag discharge yields one affine row false at each query assignment; these rows are inconsistent in augmented dimension $k+1$, so at most $k+1$ rows and $k$ binary joins suffice. Assumption-free common vertices retain zero tag and are transformed once.

**COMPUTATIONAL:** explicit context DAGs for $k=1,\ldots,6$; exhaustive all-affine-row-subset challenge for $k\le3$ (65,808 subsets total); independent Node replay; six scope/integrity corruptions rejected.

**LIMIT:** fixed complete affine cube only. Adaptive query sets, nonlinear mixed rules, exact historical bytes, all-mixed lower bound, and B3 remain OPEN. On established odd cubic Tseitin strict-3CNF, LSPV-3/469's direct $4h-1$ binary-PC$_{\mathbb F_2}$ proof remains a stronger family-specific bypass control. P versus NP remains OPEN.

Next red-team target: characterize adaptive affine decision DAGs by the rank of live path assumptions; test whether a polynomial union-size plus rank bound survives reconvergence without duplicating context-specific vertices.
