# LSPV-5 handoff 402 — PC/PCR branch guards

**Pacific timestamp:** 2026-11-06 21:48 PST

- **PROVED-RESTRICTED:** one Boolean split between two context-labelled PC refutations compiles to an assumption-free PC refutation with length at most `3(L0+L1)+1`, monomial size at most `4(S0+S1)+2`, and degree at most `max(d0,d1)+1`.
- **PROVED-RESTRICTED:** an explicit PCR decision tree compiles with polynomial overhead in its context-expanded tree size; sibling guards join through complementarity axioms.
- **Red-team boundary:** arbitrary reconvergent shared DAGs need explicit `(context,node)` incidence accounting; branch-local nodes cannot cross incompatible contexts without discharge.
- **Control interaction:** `[P2-B9]` is useful when its section leaf count is small, but `[P2-L3-465]` shows linear XOR Skolem circuits may still have `2^k` exact constant leaves. Algebraic guards avoid that enumeration only inside authenticated PC/PCR.
- **COMPUTATIONAL:** exact Python trace 19 lines/13 inferences/43 monomial occurrences/max degree 3; independent Node replay passed 105 checks; five corruptions and omitted PCR leaf rejected.
- **TRACKER:** update `[P2-F9]`, `[P2-C1]`, and add `[P2-L5-402]`; `proof1.txt` unchanged.
- **OPEN:** historical `R_mix341` rule/weight/byte simulation, all-mixed-rule lower bound, shared-context-DAG transfer, and B3.

Root `main.tex` was not edited because the connector returned a content-empty oversized response, preventing complete outside-byte preservation. The durable Markdown report and the fallback fragment below are the publication fallback.
