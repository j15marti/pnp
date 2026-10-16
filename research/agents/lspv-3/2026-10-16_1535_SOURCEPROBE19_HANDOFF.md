# SOURCEPROBE19 handoff to LSPV-1/2/4/5
2026-10-16 15:35 KST. Status: scoped exact; P versus NP OPEN.

Theorem: For a secret point oracle O_z(x)=[x=z], a deterministic black-box witness program making <=q queries and one final guess succeeds for at most q+1 of the 2^n secrets. The success set is contained in its all-zero-oracle query addresses plus its final candidate. Thus K programs simultaneously fail on a single final O_z if 2^n>K(q+1). This preserves the exists-z-forall-p quantifiers and complete fixed-clock charges.

Fatal lift issue: the explicit Boolean circuit for O_z, AND of n literals, reveals every secret bit. Its canonical proper 3-CNF has 3n variables, 4n clauses, and one fixed polynomial-time witness parser. Thus no source-aware UWI hardness or P!=NP proof follows. The uniform diagonal constructor also uses a larger polynomial clock, not an impossibility of P.

Tests: 73,556 assertions, zero discrepancies; six adaptive portfolios n=7..12; 69,888 exhaustive gadget assignments; query-bound sharpness example. Full local files: SOURCEPROBE19_RAW.json, sourceprobe19_test.py, and 2026-10-16_1535_LSPV-3_SOURCEPROBE19.tex.

Highest-value next lemma: obtain an aggregate success-set bound when all solvers can read the same complete finite circuit source and perform unrestricted polynomial preprocessing. Test source-replay, OR-selector and reject-fiber adversaries before any claimed transfer. Do not silently convert oracle query costs to ordinary computation costs.
