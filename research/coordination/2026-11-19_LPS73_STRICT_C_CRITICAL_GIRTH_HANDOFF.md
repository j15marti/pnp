# 2026-11-19 Critical-graphs handoff: LPS p73 strict C
**Status:** PROVED using published theorem; finite girth COMPUTATIONALLY VERIFIED; efficient critical extraction OPEN. P versus NP OPEN.

New sources (not yet critical): p73,q89 Cayley PSL graph v=352440,e=13040280, graph girth5, strict-C incidence10; p73,q257 v=8487168,e=314025216, girth6, incidence12. Eigenvalue lower bound >=-2sqrt73 gives Hoffman chi>=5.3305, hence >=6. Canonical private-head C encoding is UNSAT. Source tests use local Cayley word enumeration, not materialization or 5-color exhaustive proof. Exact group cycle certificates and predicates in the ZIP.

PROVED criticalization: deterministic edge deletion while exact non-5-colorability remains, recording every kept edge's deletion coloring, yields critical subgraph without reducing girth; doing this for large LPS graphs is exponential and not completed. This is the next blocker. Source-specific spectral UNSAT certificate may be lost by trimming.

FALSIFIED K6-lift attack: Brooks makes every nontrivial connected K6 graph cover 5-colorable; checked all 1024 2-lift switching classes, all 1023 connected ones SAT for direct strict C, 30690 clauses verified. K6 direct strict-C critical control: 15/15 deletion witnesses verified.

Row selector in private-head encoding: first monochromatic original edge gives constant-size refutable block for EVERY z in O(E) comparisons. This easy full-domain cover does not meet B<=N^.65 or establish arbitrary-C lower bounds.

Recommended independent audits: rederive p73/q89/q257 LPS spectral applicability and Cayley girths; independently replay exact short-cycle vertices; review criticalization monotonicity and input/output space charging; attempt smaller core plus complete deletion ledger; test graph-coloring shortcuts first. Previous LSPV-3 girth firewall remains applicable.