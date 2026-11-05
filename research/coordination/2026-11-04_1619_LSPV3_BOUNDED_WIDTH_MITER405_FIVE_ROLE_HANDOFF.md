# LSPV-3/405 five-role handoff: exact semantic support from bounded-width reconvergent circuits

**November 4, 2026, America/Los_Angeles.** PROVED/EXACT restricted, peer review pending; COMPUTATIONAL finite tests. Full Rmix341 hardness, B1/B2/B3 and P versus NP remain OPEN.

## IDEA -> SEARCH -> ITERATE

Initial prediction: unlike decomposable-only LSPV-3/404, arbitrary reconvergent circuit semantic support is tractable given a **checked tree decomposition of the complete gate-constraint primal graph** of width w. Falsifiers: XOR cancellation, absorption, miter width blowup, false decomposition scope claims, and a hidden semantic oracle.

Reviewed user-approved Nov.2 refocus, issue #3, AGENTS.md, CODEX.md, research skill; reports LSPV-3/403-404, LSPV-2/402, LSPV-4/397, REFEREE347. Actual Grok file `GROKPROOF/2026-11-04_2315_PROGRESS.md`, Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` and `..._1521_CLAUDE_ONETAPE-0001.tex` reviewed. None provides B3. General web queries: Boolean circuit essential variable bounded treewidth SAT miter, knowledge compilation bounded circuit width, Haken Resolution PHP, Cook Extended Resolution PHP. Primary Amarilli et al. arXiv:1811.02944v2 Sections 2/4 read. Direct Google-branded search unavailable. Authenticated GitHub scoped to OpenAI and actual full file read: `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean` (blob e60f4d98); irrelevant to B3.

### Proved restricted theorem

Copy each wire and gate relation twice. Constrain input pairs equal except opposite at i, and force the two copies of output v opposite. Satisfiability is exactly essentiality of i at v. Lift original tree-decomposition bags B to `B^0 union B^1 union {v^0,v^1}`, obtaining width <=2w+3, by full gate-scope coverage and connectedness. Therefore the exact support of designated v is computable in `n poly(s,|T|,w) 2^(2w+4)` using standard Boolean CSP SAT DP given the checked decomposition. This permits nonlinear reconvergence and cancellation. w=O(log s) gives a polynomial checker. Acquisition of decomposition, gate/source authentication and all DP/evidence costs must be charged separately.

### Verified finite controls

Deterministic Python producer in the local reproducibility archive: 202 circuits, 702 individual miter SAT versus independently exhaustive sensitivity queries, seed 202611041624; six malformed circuit rejections; odd/even K4 Tseitin 0/8 models; observed min-fill bucket width at most 5. GitHub independent JavaScript script passed 1,464 assertions (360 pseudorandom circuits, six hostile fixtures, six malformed rejections). Finite tests are not proofs of the asymptotic bound.

- Report: `research/agents/lspv-3/2026-11-04_1619_LSPV-3_BOUNDED_WIDTH_MITER_SUPPORT405.tex`.
- Code: `experiments/arc/lspv3_405_independent_miter.js`.
- Raw: `results/raw/arc/2026-11-04_1619_LSPV3_BOUNDED_WIDTH_MITER405_raw.json`.

### Roles and next target

LSPV-1: audit B3 conditional p-boundedness; do not infer it from bounded-width support checking. LSPV-2: test AND3/LOCAL-CONVERT typed port representations for known bounded-width decompositions after paid extensions. LSPV-3: test proof-carrying width certificates on unrestricted mixed DAG traces, looking for compact high-width falsifiers. LSPV-4: charge discovery of decomposition, two-copy construction, materialized DP tables, checking, output, and all-phase peak space. LSPV-5: independently red-team whether equivalent circuits can have very different width and whether any claimed transfer wrongly equates structural width with intrinsic runtime.

No inference rules, weights, task identities, schedules or enabled states changed. Root main.tex is not safe to update unless its complete current content and the LSPV-3 ownership marker are available. P versus NP OPEN.
