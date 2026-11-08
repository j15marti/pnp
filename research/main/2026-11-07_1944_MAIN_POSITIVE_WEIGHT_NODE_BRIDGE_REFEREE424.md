# LSPV-5/424 independent referee: positive-weight node bridge and mixed-calculus firewall

**Pacific timestamp:** 2026-11-07 19:44 PST  
**Role:** LSPV-5 independent red team, Route B primary  
**Tracker nodes:** `[P2-B3]`, `[P2-L5-423]`, new evidence node `[P2-L5-424]`  
**Status:** **PROVED/EXACT** elementary metric bridge; **PROVED-RESTRICTED / CONDITIONAL** consequence for a distinct fixed calculus; historical $R_{\mathrm{mix341}}$, B2, B3 and P versus NP remain **OPEN**.

## IDEA: falsifiable target before search

Initial hypothesis: the restricted B1 argument in LSPV-1/492 and `[P2-L5-423]` still lacked an exact bridge from Pang's proof-DAG node count to the project's weighted distinct-node minimum. Under a fixed finite grammar with a uniform positive lower bound on derived-node weights, an exponential all-DAG node lower bound should survive free source axioms and shared-DAG accounting.

Precise falsifiers stated before search:

1. historical $R_{\mathrm{mix341}}$ permits a zero-weight derived inference;
2. the relevant proof-size theorem counts an object not bounded by distinct paid nodes, even after subtracting source axioms;
3. a native unit-cost rule batches an unbounded number of Pang nodes without a proved simulation; or
4. the latest project theorem already states and proves the exact weighted bridge with its node-count convention.

Search falsified neither the restricted bridge nor its need. The historical `/341` semantic report explicitly assigns unit cost to every derived node and says no derived node has zero weight. It also exposed the decisive limitation: positive weights solve only the accounting step; Pang's restricted lower bound still says nothing about extra mixed rules. The revised target was therefore an exact restricted metric theorem plus adversarial countermodels preventing a silent calculus transfer.

## SEARCH: sources, versions and scope

The governing historical five-role handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8` (blob `033b54b8...`), current issue #3, `AGENTS.md` (`19656af1...`), `CODEX.md` (`754999f5...`), project instructions (`b8df83a7...`), and both current trackers were read. `proof1.txt` was blob `96aefb3d...`; exact final tracker blobs and head are recorded in the publication receipt after the conflict-safe write.

Actual project artifacts inspected:

- LSPV-1/492 (`73018cc7...`) and LSPV-1/493 (`14391fc9...`), including the restricted B1 and affine-cover claims;
- LSPV-3/488 (`49ce3c6f...`) and current issue comments for LSPV-1/493, LSPV-3/488 and LSPV-4/484;
- the historical semantic rule report `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11...`), which states: original clauses are free; every derived node has unit logical cost; no derived node has zero weight; and every derived node has at most two antecedent IDs;
- actual current Grok file `GROKPROOF/2026-11-08_0320_PROGRESS.md` (blob `72edb314...`) and Claude file `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6...`). Both retain unrestricted transfers as open.

Primary/repository evidence:

- Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837. Its proof size is nodes in a proof DAG; for fixed $p,r,w$ and suitable density, linear polynomial-calculus degree yields $\exp(\Omega(n))$ size in $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$. This is a recent preprint and a restricted proof-system theorem.
- Required deltas: `konard/p-vs-np` remains at `ecedd2b45...` with `scripts/proof_status.json` blob `93b77ed...`; `blkph0x/p-vs-np-proof-research` remains at `7dedc73f...` with `METHOD_INDEX.md` blob `18d693e6...`. Neither supplies an all-$R_{\mathrm{mix341}}$ lower bound or noncircular B3.
- Rotating proof-format corpus: `meelgroup/frat-xor/format.md` blob `986a21...` and `peitl/short-proof/README.md` blob `93d209...`. They concern certificate syntax/checking or finite proof search, not this asymptotic mixed-rule transfer.
- Targeted `openai` GitHub searches for a proof-complexity transfer returned no applicable result. A separate Google-branded interface was unavailable; indexed primary-research search and direct repository files were used.

No source title, badge, successful build, or repository claim was treated as proof. I did not execute Lean, Pang's proof, or an authoritative historical $R_{\mathrm{mix341}}$ byte checker.

## Established-family ledger

| Field | Exact record |
|---|---|
| Family | Pang $F(n,3,8n)$: $m=8n$ independently sampled proper width-3 clauses; use the duplicate-free hard subsequence proved in `[P2-L5-423]`. |
| Exact 3-CNF | Each clause chooses three distinct variables and one polarity per variable from $8\binom n3$ possibilities. The duplicate-free instance is a set of $8n$ strict 3-clauses. |
| Size | $n$ variables, $m=8n$ clauses; inspected formal bit encoding satisfies $L\le192n^2+129n+2$. |
| Theorem/source | Pang Theorem 7.2(a), arXiv:2610.00837: a.a.s. $\exp(\Omega_{p,r}(n))$ size for fixed `Res(PC_r/F_p)` parameters. |
| Model/rules | Syntactic shared proof DAG in restricted $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$; not arbitrary algorithms and not historical $R_{\mathrm{mix341}}$. |
| Permitted methods | All legal DAG sharing and reconvergence in that calculus; extension, affine/Tseitin, local-conversion and other mixed shortcuts are controls unless separately simulated. |
| Known shortcut/control | Cook-style extension and GF(2)/Tseitin reasoning can collapse Resolution-hard structure in stronger systems. They cannot be excluded to protect a claim. |
| Remaining transfer | Prove hardness across every native mixed rule, or a polynomial retraction/simulation preserving source authentication and exact costs. Equisatisfiability is insufficient. |

Pang's result is restricted proof-size hardness on UNSAT formulas, not merely certified UNSAT, empirical solver difficulty, or all-algorithm hardness.

## ITERATE: exact metric theorem

### Lemma 424.1 (positive-weight distinct-node bridge)

Fix a proof calculus. Let $D$ be a valid acyclic proof dependency DAG, let $S(D)$ count all distinct nodes, let at most $m$ nodes be free authenticated source axioms, and suppose every derived node $v$ has fixed weight $w(v)\ge\alpha>0$. If $q(D)$ is the number of distinct derived nodes, then

$$q(D)\ge\max(0,S(D)-m)$$

and therefore

$$W(D)=\sum_{v\text{ derived}}w(v)\ge\alpha q(D)\ge\alpha\max(0,S(D)-m).$$

If the source theorem's size convention counts derived nodes only, then simply $W(D)\ge\alpha S(D)$. Taking minima preserves the inequality because it holds for every valid DAG. If every DAG refuting $F_n$ has $S(D)\ge\exp(\kappa n)$ and $m=O(n)$, then

$$W_R(F_n)\ge\alpha(\exp(\kappa n)-O(n))=\exp(\Omega(n)).$$

This argument already counts a shared subproof once. It requires no discovery charge and no tree unfolding.

### Corollary 424.2 (exact restricted metric repair)

Define the distinct source-authenticated `Res(PC_r/F_p)` calculus with each derived DAG node charged one. For Pang's duplicate-free $F(n,3,8n)$ subsequence, $m=8n$. Thus Pang's node lower bound implies the same exponential lower bound for this exact unit-weight minimum, up to subtracting $8n$ if source nodes are included in $S$. The vague “paid cost polynomially related to Pang DAG size” premise in `[P2-L5-423]` is unnecessary at this explicitly fixed restricted scope.

Combined with the conditional exact-counter upper bound already audited in `[P2-L5-423]`, this sharpens the conditional restricted B1 contradiction. It does not prove B2 or B3.

### Why this is not a mixed-calculus transfer

The historical semantic `/341` report also uses unit derived-node weights, so positive-weight accounting is not the blocker. But its rule set contains RES, AND3, XOR, LOCAL-CONVERT and DEF. Pang's theorem lower-bounds only its own legal DAGs. Enlarging the derivation set can decrease the minimum:

$$\min_{D\in\mathcal D_{\mathrm{mix341}}}W(D)\le
\min_{D\in\mathcal D_{\mathrm{Res(PC)}}}W(D)$$

whenever the right-hand derivations embed. The desired lower-bound direction needs an all-rule lower bound or a polynomial retraction from every mixed proof. No such theorem was found or proved.

Two adversarial controls isolate the assumptions:

1. **Zero weight:** 1,000 distinct derived nodes of weight zero have $S=1000$ and $W=0$.
2. **Unbounded batch:** one new unit-cost macro can designate one million virtual Pang steps. This changes the calculus; a Pang node lower bound cannot be imported without a simulation theorem.

### Branching/shared semantics control

Two common derived lemmas `g1,g2` feed branch-local nodes `l` under context $\{x\}$ and `r` under $\{\neg x\}$. The AND obligation uses the union `{g1,g2,l,r}` and costs 4, not $3+3=6$. An OR choice between complete alternatives costs 3. Neither branch-local node is reusable in the incompatible context. No split, discharge or weakening rule was added to historical $R_{\mathrm{mix341}}$.

## Executed checks and resource ledger

- Python producer: 583,474 assertions over all $0\le m\le32$, all source counts, $0\le q\le64$, and $1\le\alpha\le8$, plus shared-DAG, context, countermodel, asymptotic, SAT/UNSAT and malformed controls.
- Independent Node/BigInt verifier: 583,470 assertions with a separate implementation.
- Preserved `/341` semantic replay: 30,714 checks passed on K4, K3,3, cube, Petersen, prism-6, prism-16 and a bridge control; seven malformed and five corruption controls were rejected. This is the preserved independent verifier, not the authoritative historical checker.
- One initial command used the nonexistent prefix `experiments/replay/413`; it failed before execution and was corrected to `replay/413`. A separate attempt to feed the `_independent.json` summary rather than the fixture produced a TypeError and is not counted.
- Logical work: no rule or weight changed. Evidence bits are two small programs and raw JSON. Search, repository reads, parsing, construction, output and verification were charged as ordinary host work; the ideal proof minimum intentionally excludes discovery.
- Work/span/space: distinct-node work and AND/OR costs are reported separately from any span. Scripts used ordinary host time and memory; no FLMV same-machine or peak-space result is claimed. Retention shares `g1,g2`; recomputation would create and charge new nodes under the fixed ID/derivation rules.

## Tracker decision, advance and precise gap

Material evidence changes `[P2-B3]` and refines `[P2-L5-423]`: the Pang-node-to-weight bridge is now exact for the explicitly defined distinct unit-weight restricted calculus. Add `[P2-L5-424]`. `[P2-B1]`, `[P2-B2]`, `[P2-D1]`, `[P2-C3]` and historical-$R_{\mathrm{mix341}}$ B3 remain **OPEN**. `proof1.txt` has no material change.

**Actual advance:** exact positive-weight theorem and explicit zero-weight/batch firewalls; shared-DAG and context accounting tested.  
**Verification:** 1,166,944 new assertions plus 30,714 preserved semantic replay checks.  
**Publication status:** report, programs, raw result and handoff prepared for a leased current-head commit; receipt records final SHAs and readback.  
**Precise remaining gap:** an all-native-rule lower bound or polynomial source-authenticated retraction for the fixed historical mixed calculus, plus a noncircular same-calculus B3.  
**P versus NP remains OPEN.**
