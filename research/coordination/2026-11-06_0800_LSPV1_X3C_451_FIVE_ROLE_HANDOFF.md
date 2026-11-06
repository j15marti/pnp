# LSPV-1/451: 3-local promise-UNSAT XOR optimum, five-role handoff

**2026-11-06 08:00 PST | LSPV-1 | Route B lead.** Follow latest 2 Route A (LSPV-2/LSPV-4), 3 Route B (LSPV-1/LSPV-3/LSPV-5) allocation. All schedules, weights, task ownership and historical R_mix341 remain unchanged. P versus NP remains **OPEN**.

## What actually advanced

**PROVED/RESTRICTED:** X3C reduces to minimum binary-XOR-refutation work of a system of **at-most-three-variable source GF(2) equations** that is promised UNSAT. For X3C universe size $r=3q$, triples $S$, and $L=q+1$, the source system has a global XOR chain forcing $\bigoplus_i y_i=1$, a zero-parity row per triple, and $r$ private zero-chain fallbacks enforcing $y_i=0$. Its exact contradiction support size is

$$
\kappa(E_S)=r+2+\min_{J\subseteq S}
\bigl(|J|+(q+2)\operatorname{wt}(\mathbf1_r\oplus\bigoplus_{j\in J}\mathbf1_{S_j})\bigr).
$$

The globally best shared-DAG logical work equals $\kappa-1$ and ideal two-input span equals $\lceil\log_2\kappa\rceil$. The threshold $W_{\mathrm{XOR}}(E_S)\le r+1+q$ is equivalent to X3C exact cover: any fallback exceeds the budget; a <=q collection of triples covering an odd number of times at each of 3q coordinates must be exactly q disjoint triples. Thus computing the optimum is NP-complete on **promised UNSAT**, arity-three affine sources. Gaussian elimination still supplies a polynomial-size nonminimum refutation. This is **optimizer hardness, not proof-work hardness**.

**Original signed width-at-most-three CNF:** translate each source affine equation of arity $d\le3$ to $2^{d-1}$ wrong-parity-blocking clauses, using $2r+1+r(q+1)$ variables and $r(2(q+1)+5)+4m+2$ clauses, with $m$ source triples. Translation is equisatisfiable. It is **not** a demonstrated proof-cost-preserving reduction into historical R_mix341, whose original signed clauses must be authenticated and any row extraction must be paid. No legal mixed lower bound follows.

**COMPUTATIONAL:** Standard-library Python produced 355 deterministic control systems and passed 18,280 assertions, including exact X3C threshold, Gaussian UNSAT, syntactic CNF encoding, full paid XOR certificates, malformed/corrupt controls, K4 odd/even signed-3CNF, and q1 exhaustive source minimum. Separate Node verifier on 12 full raw examples passed 742 assertions. A further standalone JavaScript original-source verifier executed 204 controls and 11,832 assertions. Full local raw JSON SHA256: `d8768340157e2c7906178c56f8db6f0805bd668d266c232a3e43c06fb1c3b79d`. The full producer, independent checker, certificates, signed DIMACS and raw data remain in a reproducibility ZIP; GitHub hosts the report, standalone verifier and metadata summary.

## Family / known-model / shortcut ledger

| Source family | Encoding and size | Published lower bound | Legal shortcut | Transfer remaining |
| --- | --- | --- | --- | --- |
| Cubic-expander odd Tseitin | 1 var/edge, 4 signed width-3 clauses/vertex, $h$ vertices, $N=\Theta(h\log h)$ bits | Urquhart (1987), Ben-Sasson–Wigderson (2001): $2^{\Omega(h)}$ ordinary shared-DAG Resolution | Declared AND3/GF(2) $4h-1$-node mixed proof on bridgeless cubic graph | No full mixed superpolynomial minimum follows. Authenticate historical accepted-byte grammar. |
| Unary PHP | $h(h+1)$ vars, $\Theta(h^3)$ clauses, $N=\Theta(h^3\log h)$ bits | Haken (1985): $2^{\Omega(h)}$ ordinary Resolution | Cook/Buss polynomial Extended Resolution/Frege proofs | Do not transfer ordinary Resolution hardness to extended calculus. |
| X3C gadget (focused counterexample) | $\le3$-local affine rows; polynomial signed width-$\le3$ CNF above | NP-complete **exact optimal XOR proof** under an always-UNSAT promise | Gaussian elimination polynomial nonminimum proof | No lower bound for decision, unrestricted mixed refutation, or full source-authenticated 3-CNF proof cost. |

## Cross-role handoff, no schedule changes

**LSPV-3 (Route B certificates):** test whether original signed 3CNF wrong-parity clause blocks can be paid-converted to native local GF(2) rows in strict historical /341, with correct two-parent AND3 usage and source bit provenance. Include any legal alternatives that shorten refutation, and distinguish the new signed-CNF proof system from the XOR-source toy.

**LSPV-5 (Route B red team):** independently attack the private-chain uniqueness argument, the $q+2$ fallback barrier, purported NP-completeness on promised-UNSAT affine sources, and any inference of full mixed hardness. Check current theoretical literature and stronger native shortcuts. In prior project work LSPV-1/450 proved the dense-row syndrome reduction, so do not call this a new NP-hardness classification without qualifying the 3-local strengthening.

**LSPV-2 and LSPV-4 (Route A):** use the gadget and existing expander Tseitin only as *adversarial controls* for the all-input recursively iterable, same-machine FLMV contraction. Neither mathematical minimum-work optimization nor polynomial Gaussian elimination demonstrates an all-input resource-improving transformer. Charge all phases, child materialization, time and space.

**LSPV-1 next:** seek a noncircular, rule-specific B3 bridge to historical R_mix341; in parallel look for an established proof-hard family resistant to *all* permitted mixed rules, instead of treating optimizer NP-hardness as that lower bound.

## Corpus and status

Governing five-role handoff blob c3889a3, R_mix341 historical semantic grammar LSPV-2/341 blob c87acd11, LSPV-3/451, Grok 2026-11-06_1220_PROGRESS, Claude TPORT-0002, current issue #3, AGENTS.md, CODEX.md, pnp research skill, required konard proof status (93b77ed3), blkph0x method index (18d693e), FRAT-XOR format (986a21), CakeML LPR, Peitl short-proof, ABC and openai/math ExecCNF examined. Google-branded search unavailable, indexed general web search/GitHub search performed. No authoritative historical /341 checker run and no root main.tex edit: retrieval yielded a file SHA but no safe complete file content.

## Artifacts

- [Detailed LSPV-1 report](../agents/lspv-1/2026-11-06_0800_LSPV1_PROMISE_UNSAT_3LOCAL_X3C_OPTIMUM451.md)
- [Standalone exact source-row verifier](../../experiments/arc/lspv1_451_x3c_3local_xor_selfcheck.mjs)
- [Raw experiment summary](../../results/raw/arc/2026-11-06_0800_LSPV1_X3C_451_summary.json)

**OPEN:** the complete native accepted-byte grammar and source transfer, full all-rule superpolynomial $\overline W_{R\mathrm{mix341}}$, B1/B2/B3 and P versus NP.
