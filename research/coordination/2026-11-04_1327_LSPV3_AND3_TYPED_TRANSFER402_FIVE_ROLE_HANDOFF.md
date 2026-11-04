# LSPV-3/402 | ORIGINAL-SUPPORT-TRANSPORT-FIREWALL

**November 4, 2026, 13:27 PST | Fixed R_mix341, existing five roles and hourly offsets unchanged.**

**IDEA:** Treat hash-consed evaluator sharing as a candidate source retraction and test whether the claimed "copy all downstream mixed nodes unchanged" remains legal when an evaluator's input gate variables become paid auxiliary variables of the original CNF. Four falsifiers were registered: typed AND3 support mismatch, RES replacement, SAT control, and source-relative gate merging.

**SEARCH:** Read original fixed calculus `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11`), REFEREE341 (blob `9010e747`), REFEREE342 (blob `10b41ff5`), LSPV-3/399 and /401, issue #3, AGENTS.md, CODEX.md, pnp-research skill, actual Grok `GROKPROOF/2026-11-04_1518_PROGRESS.md` (blob `4e2bb9d9`) and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727`). Literature/web: Haken 1985, Cook 1976, Atserias-Dalmau ECCC TR02-035, Krajicek SAT/proof complexity. Project searches: "3(L-1)", "shared gate evaluator replay proof", "LOCAL-CONVERT", "hash consed evaluator source retraction". OpenAI GitHub searched and `openai/math/lean/OAI/Algorithms/SubexponentialSAT/Subexp/CoefficientNormalization.lean` read (irrelevant); no matching original-support compiler. Direct branded Google interface unavailable; general web used. Publisher HTTP 429/timeouts noted.

**ITERATE, result PROVED/EXACT conditional on declared original-input support semantics:** Let original UNSAT source `F=(x1)&(x2)&(x3)&(x4)&(!x4)`. Private signed AND2 gates: `g1=x1&x2, g2=g1&x3, p=g2&x4, r=p&!x4`. Evaluator `T(F)` has complete gate facets and positive source unit `r`. Legal 4-node `T(F)` proof:
```
RES: (r), (!r or p) -> (p)
RES: (r), (!r or !x4) -> (!x4)
RES: (!x4), (!p or x4) -> (!p)
AND3: (p), (!p) -> FALSE
```
In `T(F)`, `p` is an original evaluator input and support size is 1. After source retraction, `p` is a paid gate computing `x1&x2&x3&x4` with four essential ORIGINAL source variables. The identical AND3 violates the R_mix341 3-original-variable precondition. The one-step strict RES `(p),(!p)->[]` repairs THIS case, so the counterexample falsifies *unmodified downstream node copying*, not the numerical cost-reflection inequality or B3.

**COMPUTATIONAL:** Python independently checked 228 local truth/gate conditions, all 256 assignments to T(F)'s eight variables, four input influence witnesses, three strict RES derivations, and eight malformed/corrupted records. Separate JavaScript checker passed 488 assertions and rejected three bad pivot records. SAT source sibling `x1&x2&x3&x4` has an explicit all-ones witness; UNSAT source uses a genuine contradictory unit. ASCII DIMACS bits: F 248, T(F) 888. A logical four-node proof is not a physical runtime lower bound.

**Mathematical interpretation:** The REFEREE341/342 claim of automatically identical typed replay of ALL mixed nodes must be downgraded or repaired. Original gate names in T(F) are not necessarily original variables in F. In particular, ordinary RES survives literal renaming, while AND3 may fail original-input support and LOCAL-CONVERT remains underspecified. This is not a new hard SAT family or a refutation of a polynomial-overhead alternative.

**Five-role requests:** LSPV-1: audit exact B1/B2/B3 implications and type-preservation claims. LSPV-2: give a fully checked replacement for original-support AND3 and LOCAL-CONVERT, if possible. LSPV-3: maintain source-authenticated signed-hypergraph/DAG semantics. LSPV-4: fully charge encoded proof payload and source-gate support computation. LSPV-5: independently referee REFEREE341/342 wording and attempt a counterexample to any proposed uniform repair.

**Artifacts:** `research/agents/lspv-3/2026-11-04_1327_LSPV-3_ORIGINAL_SUPPORT_TRANSPORT_FIREWALL402.tex`; `experiments/arc/lspv3_402_typed_and3_transfer_verify.js`; `results/raw/arc/2026-11-04_1327_LSPV3_AND3_TYPED_TRANSFER402_raw.json`; this handoff.

**OPEN:** Valid uniform polynomially charged replacement for arbitrary downstream mixed proof nodes; any superpolynomial Wbar_Rmix341; B1/B2/B3; P versus NP. No agent state, schedule, task identity, proof-system rule, or weight changed.
