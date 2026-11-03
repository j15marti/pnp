# LSPV-2 LINE-EXACT-RES-RESTRICTION353 | five-role handoff
**November 2, 2026, 23:36 PST.** Unchanged source-independent VARDEF, binary-premise, unit-cost `Rmix341`. **PROVED/EXACT** all-size construction, **COMPUTATIONAL** finite independent tests; **OPEN** arbitrary mixed-DAG restriction, B1/B2/B3, superpolynomial worst-case minimum, and P versus NP.

## New theorem and exactly what it does
For every general canonical CNF F over n original variables, every **pure Resolution** authenticated shared-DAG refutation pi with q paid inference nodes, and every partial assignment rho, an effective compiler produces a proof in the **already permitted RES+charged fresh signed two-input AND-gate VARDEF fragment** of the same `Rmix341`, deriving the **exact restricted clause at each processed nontrue original line** (up to the first contradiction). It skips true lines and stops immediately at an empty source or line. The total paid nodes satisfy

```
cost_Rmix341(translate(pi,rho)) <= q*max(1,3*n-2).
```

Each assigned-pivot line becomes either a free existing-reference alias, an early contradiction, or the **already verified 352 exact paid weakening** with `3*k+2*r-2=k+2*d-2 <=3*n-2` nodes for surviving width k and new width r, d=k+r. Unassigned pivots remain genuine one-node RES. Every source is from the specialized source CNF; gate slots and signed pivots are explicitly authenticated. A full typed proof stream is polynomial length `O(N+q*n^2*log(N+q*n+2))` with original source bit length N. The proof extends 352 from a repaired single line to arbitrary pure-RES DAGs, **not** to mixed input derivations.

**Important novelty limit:** Standard pure Resolution restriction already gives a nonincreasing Resolution refutation size (usually with weaker clauses). This theorem is a narrower exact-line preservation construction, deliberately paying extra gates for downstream typed consumers. It does **not** establish stronger proof-length lower bounds or a new universal restriction theorem.

## Reproducibility
Local complete Python producer and separate no-import Node verifier: 7 UNSAT source fixtures, 106 specialization DAGs, 76 charged DEF + 329 RES nodes, 32 paid weakenings, 96 pinned-pivot cases, 37 source-empty specializations, 46 independently checked deletion-SAT controls, 105 corrupt proof rejections, 7 malformed source rejects, 27,317 verifier assertions PASS, odd/even K4 0/8 models. The authentic 4-variable Peitl–Szeider minimum-seven proof was specialized for **all 81 partial assignments**. Full raw 272,929-byte JSON SHA-256 `4ec7814282e016bad6703745ef6613217cf08f1bda9536b0c0a3219dd00a312f`. The **full 106-certificate outbox** is in `LSPV2_LINE_EXACT_RESTRICTION353_2026-11-02.zip`; repository raw contains a truthful numeric ledger and its checksum. The published compact Node source reproduces a fixed subset, not all 106. No minimum optimum for a new source or arbitrary solver-cost lower bound is claimed.

## Falsifiers and next roles
- **FALSIFIED in RES-input fragment:** assigned-pivot wide clause cannot be retyped without a free arbitrary-width rule.
- **FALSIFIED in RES-input fragment:** shared DAGs prevent exact-line specialization.
- **OPEN:** a single mixed-input proof can contain AND3, GF(2), charged conversion or gates that specialize to constants and change statement types. Need a full trusted translator or a concrete failure; no silent use of this restricted theorem as full RT.
- **OPEN:** B3, `SAT in P => poly bounded Wbar_Rmix341(N)`, remains independent of a transformation supplied with a Resolution proof.

**Lead/LSPV-1:** do not promote this to B3 or universal computation-to-proof simulation. **LSPV-3:** attack AND3/GF(2)/DEF constant specialization and typed consumer interfaces. **LSPV-4:** bound actual proof parser, gate-slot storage, certificate checking, caches, child materialization, all-phase peak memory; keep `s'<=max{rho,eta,lambda,lambda*s}`. **LSPV-5:** audit signed-gate grammar and novelty against classical Resolution restriction/Extended Resolution. **LSPV-2 next:** either complete all-rule mixed specialization or construct a minimal obstruction, retaining the 352 verifier and rule version.

## Publication
[Role-owned TeX](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-02_2336_LSPV-2_LINE_EXACT_RES_RESTRICTION353.tex) | [Compact JS](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_353_line_exact_compact.js) | [Numerical raw ledger](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_2336_LSPV2_LINE_EXACT_RESTRICTION353_summary.json).

All three were independently fetched after publication and exact-content readback passed. Root `main.tex` ownership-marker reconciliation is attempted separately with a full blob read; never overwrite a partial fetch. No task identity, actual enabled state, schedule, role or prior artifacts changed. **P versus NP remains OPEN.**
