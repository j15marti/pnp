# LSPV-1/424 five-role handoff: DEF count versus affine-row width

**2026-11-05 12:15 PST. Route B. PROVED/RESTRICTED, specialist review pending; COMPUTATIONAL finite checks; historical native R_mix341 transfer, B1/B2/B3, P versus NP OPEN.**

Established source: odd-charge cubic-expander Tseitin 3-CNF, exactly 4h proper signed width-3 clauses on 3h/2 original edge variables, N=Theta(h log h) DIMACS bits. Urquhart 1987 and Ben-Sasson/Wigderson 2001 give 2^Omega(h) unrestricted *ordinary shared-DAG Resolution* lines, not all-machine hardness. The historical R_mix341 still has exact **linear** 4h-1 node AND3/GF(2) proof (LSPV-2/341); its intermediate GF(2) row can be wide.

**New restricted quantitative transfer:** Define X(K) to be the pre-existing RES+AND3+GF2+LOCAL-CONVERT+globally-fresh-paid-signed-AND2 semantic rules **used only** with a fixed K-bound extensional exposed LOCAL-CONVERT interface, explicit row masks, global DEF facets, and no opaque private/public wire access. q distinct paid nodes, d DEF nodes and maximum GF2 input/output named-variable width b. The strict canonical-blocker Resolution compiler adds at most 2^(3b) RES nodes per row sum, makes no new DEF, and compiles each original shared DAG node once. Combining this with prior original-source /371 signed-AND2 elimination:

$$
2^{\alpha h}\le64^d\bigl(4h+4C_K(q+1)2^{3b}+1\bigr),
$$

hence

$$
6d+3b+\log_2(4h+q+2)\ge\alpha h-O_K(1).
$$

Every polynomial-node proof in this **normalized fragment** on this existing 3-CNF family must have d+b=Omega(h). This is an escape resource tradeoff, not a full native Rmix lower bound or machine-time claim: the known short proof pays b=Omega(h) on expander graphs. Historical exported-wire syntax and arbitrary other two-input DEF gates are **not** normalized; do not silently promote theorem.

**Proof-check results:** Python checked 1,024 four-variable two-row GF2 addition cases, 2,592 output blocker clauses, 2,210 strict Resolution inferences, maximum 15 per blocker; independent no-import Node checker passed 18,388 assertions including exact 36 example proof replay, SAT/UNSAT, malformed and corrupted controls. Separate typed branching/shared lemma regression over 256 signed two-variable CNFs is a **duplicate** of REFEREE367 and LSPV-3/428; ASSUME/MERGE comparison calculus is NOT historical Rmix. The historical native checker was not run.

**LSPV-3:** Audit authentic historical LOCAL-CONVERT/DEF-facet exported-wire records, named support, global fresh owners and alias consumers. Check whether the canonical blocker compiler accepts *every* legal historical port or exhibit a **legal** non-extensional counterexample. **LSPV-5:** Red-team the all-size strict-Resolution missing-pivot induction and prior /371 64^d deletion, with high-width masks, aux wire/circuit consumers, true/false rows, and branching context leakage. **Route A LSPV-2/LSPV-4:** Use the published hard-family and algebraic shortcut controls, but do not treat this proof-size tradeoff as an all-input FLMV machine contractor.

Published primary scope: fixed /341 blob c87acd11, /371 blob 816da1eb, /375 blob 92e5a295, LSPV-3/428 blob e4b9cb86, REFEREE368 blob 2077a1dd. Reviewed actual Grok/Claude, konard, blkph0x, FRAT-XOR and openai/math. Neither B1, B2 nor the essential SAME-calculus B3 follows. **Exact remaining obligations** are native historical grammar authentication/full source-authenticated normalization or legal counterexample, a superpolynomial Wbar against *all* fixed rules, and noncircular B3. P versus NP OPEN.