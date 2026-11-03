# LSPV-3 369 to five-role team: quantitative Res(⊕)-to-mixed transfer firewall
**November 3, 2026, 9:24 PST. Same fixed Rmix341; no task, state, schedule, ownership or weight changes.**

## Result and prior-work check
Start with Braun's September 2026 arXiv 2609.23015 *preprint claim*: for `ell>=32`, `n=2^ell`, every unrestricted DAG Res(⊕) proof of original bitPHP `F_ell` uses `S>exp(n/(32768 ell^2))` nodes including original clauses. This statement is Lean-formalized according to the paper, but was **not independently kernel-replayed** this run.

**Important duplication avoided:** LSPV-3's existing full-Cook signed-gate generator `research/agents/lspv-3/2026-11-02_1624_LSPV-3_BPHP_FULL_COOK_CERTIFICATE346.tex` (blob `e4931b197b759708fc53983c028894dc35c1eaab`) already proves `m-1<=q_ell<=C n^4` for legal source-preserving Rmix RES/DEF refutations of this *same* BPHP formula, with full finite DAG replays. No new BPHP proof generator was needed.

**NEW quantitative corollary, CONDITIONAL on Braun's theorem:** For the prior uniformly short mixed refutations `pi_ell` with charged node count `q_ell`, *every* same-source Res(⊕) refutation `rho_ell` satisfies

```
S(rho_ell) > exp( [9/(32768*C^(1/4))] *
                  q_ell^(1/4)/(log2(q_ell+1)+1)^2 ).
```

This follows from `q_ell<=C n^4` and source indispensability `q_ell+1>=m=n^2(n+1)/2>=n^3/2`. It forbids polynomial-output reverse translation even if nonuniform, oracle-assisted or after-the-fact: the required *output* does not exist. Original explicit ASCII source length is `N=Theta(n^3 ell^2)` **bits**. The theorem is about proof output size, **not** generalized SAT runtime.

Existing Haken/ER nonprojection and Braun/BPHP mixed escape were already recorded in BPHP343, BPHP346, LSPV-2 364 and LSPV-5 REFEREE316. The rate as a function of input mixed logical cost is the present scoped incremental result. No globally superpolynomial `Wbar_R` follows; B1/B2/B3 remain OPEN.

## Falsifiers and controls
F1 polynomial same-source mixed-to-Res(⊕) backtranslation on BPHP: **FALSIFIED conditional on Braun**. F2 direct import of Braun restricted hardness into Rmix minimum: **FALSIFIED unconditionally by prior Cook Rmix proof**. F3 restricted proof length implies all-SAT-machine lower bound: **UNSUPPORTED**. F4 Grok's interpretation of an upper running-time envelope as a per-query lower bound: **FALSIFIED**.

Independent isolated-JS finite signed controls checked ell=1,2,3: 6/40/288 BPHP clauses; 78 deletion SAT witnesses, 364 literal-sign-repair witnesses, matched SAT injective counterparts; exhaustive ell=1,2 UNSAT checks; K4 odd/even Tseitin 0/8 models. These finite tests neither validate the large Braun theorem nor certify any mixed minima. Source/derived-node count, evidence bits, verification, discovery and all-phase peak RAM remain separate.

## Repository audit
Read first user-approved refocus, current issue #3, AGENTS.md, CODEX.md, pnp-research skill, prior BPHP346, current LSPV-3 367/368, peers LSPV-2 365, LSPV-1 366, LSPV-5 316. The actual directories `GROKPROOF/`, `research/agents/grok/`, and `research/agents/claude/` were listed. Read Grok progress 2026-11-03 1217/1518 UTC and Claude TPORT-0001/0266. Neither supplies B3; Grok's 1217 reasoning reverses upper and lower query cost. Web reviewed Braun arXiv 2609.23015, Cook 1976, Haken 1985, Buss 1987. GitHub code search of openai for resolution-proof verifier returned zero relevant files. Duplicate BPHP compiler found, acknowledged, not reimplemented.

## Exact artifacts and write limitations
* Formal report: `research/agents/lspv-3/2026-11-03_0924_LSPV-3_BRAUN_BACKTRANSLATION_BLOWUP369.tex`
* Control script: `experiments/arc/lspv3_369_braun_backtranslation_controls.js`
* Raw ledger: `results/raw/arc/2026-11-03_0924_LSPV3_BRAUN_BACKTRANSLATION369_public.json`
* This handoff: `research/coordination/2026-11-03_0924_LSPV3_BRAUN_BACKTRANSLATION_BLOWUP369_FIVE_ROLE_HANDOFF.md`

Container Python/Bash/preflight and native Node replay failed with `redis.exceptions.ResponseError`; exact finite checks executed in isolated JavaScript tool. Root `main.tex` returned SHA `19ddee0fe84c07eee85de006362a4cb4073e292f` but **zero bytes** via GitHub `fetch_file`, so no partial overwrite was attempted. GitHub create-file writes use new role-owned filenames; all are subject to independent readback. P versus NP remains OPEN.

**Next gap:** An actual full-Rmix resistant lower-bound theorem, not a Haken/Braun lower bound for a strictly weaker calculus, and a separate noncircular proof of B3 for the unchanged Rmix341.
