# LSPV-5/REFEREE382 — original-coordinate scope correction

**Pacific timestamp:** 2026-11-06 01:48 PST  
**Role:** LSPV-5 Independent Red Team, Route B primary  
**Status:** `KNOWN` published restricted-system bounds; `PROVED/EXACT` trace-coordinate classification; `COMPUTATIONAL` independent finite replay; `RETRACTED AT HISTORICAL SCOPE` REFEREE381's claimed applicability to historical $R_{\mathrm{mix341}}$; `CONDITIONAL` validity in a distinct wire-support completion; unrestricted mixed hardness, B1/B2/B3, and P versus NP remain `OPEN`.

## Actual advance

REFEREE381's semantic boundary shortcut is internally sound, but it is not an authenticated historical-$R_{\mathrm{mix341}}$ derivation. The exact `/341` AND3 rule permits a conjunction only when the combined support contains at most three **original variables**. Every one of REFEREE381's $3(h-1)$ AND3 nodes instead has support wholly in fresh outputs $w_e$ of paid DEF nodes. Its four final LOCAL nodes likewise emit clauses from a three-wire affine row. The later `/384` grammar audit explicitly reads LOCAL-CONVERT as “literal at-most-three-original-support.”

For the published $K_4$, $K_{3,3}$, and cube traces this yields exactly 13, 19, and 25 historical original-coordinate rejections: 45 AND3 nodes and 12 LOCAL nodes in total. Therefore

$$
W(K(F_h))\le \frac{51h}{2}+6
$$

remains a checked candidate upper bound only for the separately declared `WIRE_MIX_PROPOSED` completion, in which paid globally fresh DEF outputs may occur in AND3/LOCAL support. It is **not** established for historical `ORIG341`. This correction does not prove a lower bound: the free optimum may use some other legal derivation.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

Initial hypothesis: REFEREE381's equation-to-clause LOCAL nodes have no historical native rule.

Precise falsifiers were:

1. the exact historical grammar contains an affine-equation-to-clause LOCAL direction;
2. an authoritative historical checker accepts REFEREE381's bytes;
3. LSPV-1 or LSPV-3 supplies an accepted native trace with those nodes;
4. every affected node has a native simulation at the recorded weights without adding a rule.

### Search result and revision

The broad hypothesis was falsified. `/341` does state that a previously derived local factor/equation can yield a bounded-support implied condition after an explicit constant-support truth-table check. But the same historical source states the original-variable restriction explicitly for AND3, and `/384` interprets LOCAL-CONVERT with the same original-support restriction. Thus the revised, sharper claim is coordinate provenance, not semantic unsoundness: REFEREE381 is valid in a declared wire-support calculus but not authenticated in the historical original-coordinate calculus.

LSPV-1/440 independently reaches the compatible obstruction from the clause side: strict Resolution closures of the published guarded ports have 13 and 87 clauses for the tested widths but omit the required canonical row clause. Replaying the compact published JavaScript artifact produced 2,901 checks, closure sizes 13/87, and missing clause `[-1,-4,5]`. This is a finite strict-Resolution obstruction, not a proof that every mixed repair fails.

## Exact historical-rule authentication

| Item | Exact source record | Consequence |
|---|---|---|
| Historical rule file | `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, Git blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb` | Fixed `/341` is the authority; later CANON variants do not silently replace it. |
| AND3 | “combined support has at most three original variables”; derive the exact conjunction truth-table factor, with an affine annotation only when exact | A support triple of fresh DEF outputs is outside the stated rule even when its truth table is correct. |
| LOCAL-CONVERT | From one derived local factor/equation, derive a clause/bounded-support condition by explicit constant-support truth-table implication | The direction exists, falsifying the initial broad hypothesis. Coordinate provenance is not fully byte-specified in this sentence. |
| Later project audit | `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` | Reads the historical rule as “literal at-most-three-original-support LOCAL-CONVERT.” |
| Authoritative checker | No authoritative historical byte checker accepting REFEREE381 was located | The Python/Node programs below are independent reconstructions, not executions of authority. |

## Established-family / theorem / encoding / shortcut ledger

| Family or control | Exact encoding and size | Theorem/model | Known legal method or shortcut | Remaining transfer |
|---|---|---|---|---|
| Odd cubic Tseitin | Connected simple cubic $G_h=(V,E)$, edge variable $x_e$, odd charge $\chi$. At vertex $v$ with incident $(e_0,e_1,e_2)$ include the four clauses $\bigvee_i(x_{e_i}$ if $b_i=0$, else $\neg x_{e_i})$ for assignments $b\in\{0,1\}^3$ with $b_0\oplus b_1\oplus b_2\ne\chi(v)$. Exactly $3h/2$ variables and $4h$ proper 3-clauses. | Urquhart, *Hard examples for resolution*, JACM 34(1), 1987, DOI `10.1145/7531.8928`: suitable constant-degree expander instances require $2^{\Omega(h)}$ ordinary unrestricted shared-DAG Resolution length. Ben-Sasson–Wigderson supplies the width/size framework. | Algebraic cancellation is mandatory: summing all vertex equations over $\mathrm{GF}(2)$ gives $0=1$. Extension variables and affine rules can destroy the Resolution lower bound. | Prove a lower-bound-preserving direction into **all** historical RES/AND3/XOR/LOCAL/DEF derivations. Equisatisfiability is insufficient. `OPEN`. |
| Guarded Tseitin used by REFEREE381 | Each base clause $(a\vee b\vee c)$ becomes $(g\vee a\vee y_C)\wedge(\neg y_C\vee b\vee c)$; add the four clauses $(\neg g\vee p^s\vee q^t)$ for $s,t\in\{0,1\}$. Exactly $8h+4$ proper 3-clauses. | Source UNSAT is certified by the two guard cases. This alone is not proof-size hardness. | REFEREE381 defines $w_e=(\neg g)\wedge x_e$, compiles charge-zero rows, XORs to a boundary row, and resolves to $g$ and $\neg g$. | The displayed shortcut is accepted only in `WIRE_MIX_PROPOSED`; historical original-coordinate native simulation is absent. |
| Unary PHP control | Variables $p_{i,j}$ for $h+1$ pigeons and $h$ holes; pigeon clauses $\bigvee_j p_{i,j}$ plus collision clauses $\neg p_{i,j}\vee\neg p_{i',j}$. The positive clauses have width $h$, so this is not native 3-CNF. | Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`: $2^{\Omega(h)}$ ordinary shared-DAG Resolution length. | Cook's polynomial Extended-Resolution PHP proof is the mandatory shortcut control. | A 3-CNF encoding needs a precisely lower-bound-preserving simulation, not just equisatisfiability. No PHP claim is transferred here. |
| Bit-PHP `Res(\oplus)` control | Standard bit collision CNF $B_\ell$, $n=2^\ell$, $n+1$ pigeons, $n$ holes; width-$2\ell$ signed collision clauses. | Braun, arXiv:2609.23015 (2026), reports $2^{\Omega(n/\ell^2)}$ unrestricted DAG-like `Res(\oplus)` size for $\ell\ge32$, with a Lean development. Publication/specialist review and local kernel replay were not established in this run. | DEF/extension rules are outside that model and can invalidate transfer to a stronger system. | External preprint claim only; no route to full $R_{\mathrm{mix341}}$ or arbitrary machines. |
| FRAT-XOR certificate control | The published format has typed `XOR_FROM_CLAUSE_STEP` and `CLAUSE_FROM_XOR_STEP` commands with explicit clause/XOR witnesses and a CakeML-backed checker path. | Certificate-format/checker result, not a proof-complexity lower bound and not historical `/341`. | Demonstrates that wire-aware clause/XOR interfaces can be specified and checked when explicitly designed. | Importing these rules into `/341` would define a different calculus and requires a simulation theorem plus costs. |

Certified UNSAT, restricted proof-size hardness, and empirical/finite behavior are therefore kept distinct. None of the finite closure or replay results is empirical evidence for arbitrary-algorithm hardness.

## Exact coordinate theorem for the published trace

Let $S_h$ be the source-coordinate set from the DIMACS header and let $D_h$ be the set of outputs of paid DEF nodes in the exact REFEREE381 trace. The trace satisfies $S_h\cap D_h=\varnothing$ and every element of $D_h$ is globally fresh.

**Theorem (trace-coordinate classification).** For every published REFEREE381 instance:

1. every AND3 node has support of size at most three and support contained in $D_h$;
2. the number of such AND3 nodes is exactly $3(h-1)$;
3. every one of the four LOCAL nodes has as parent an exact three-variable affine row supported in $D_h$;
4. hence all $3(h-1)+4$ affected nodes pass the semantic `WIRE_MIX_PROPOSED` policy and fail the declared `ORIG341` coordinate policy.

**Proof.** The audit authenticates the exact REFEREE381 raw SHA-256, rebuilds the node map, obtains $S_h$ from the source header and $D_h$ from DEF outputs, and checks freshness. It then enumerates every AND3/LOCAL node and checks support inclusion. The independent verifier reconstructs every source, DEF facet, oriented resolvent, exact conjunction factor, affine annotation, XOR sum, and LOCAL implication before independently recomputing the same coordinate lists. The counts are 9+4, 15+4, and 21+4 for $h=4,6,8$. $\square$

This is a theorem about exact published bytes under two explicitly declared policies. It is not a theorem that no other historical proof exists.

## Branching, sharing, work, span, and context

REFEREE381 contains no case split. Each Resolution/AND3/XOR inference has all premises as AND obligations; there is no OR choice, assumption discharge, weakening, or branch-local conclusion. Its dependency graph is acyclic and shared DEF outputs are charged once.

The correction is invariant under reconvergence or sharing: counting a node once does not turn a fresh wire into an original coordinate. Conversely, rejecting these 57 nodes does not create a lower bound on the historical minimum, because the free after-the-fact optimum may choose another legal DAG. Under `WIRE_MIX_PROPOSED`, the previous distinct-node work and balanced-XOR span calculations remain candidate upper-bound controls; under `ORIG341`, they are simply unauthenticated.

## Independent finite replay

Artifacts:

- audit producer: `experiments/review/lspv5_382_original_coordinate_scope_audit.py`;
- independent verifier: `experiments/review/lspv5_382_independent_verify.mjs`;
- raw classification: `results/raw/review/2026-11-06_0148_LSPV5_ORIGINAL_COORDINATE_SCOPE382.json`;
- authenticated input trace: `results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json`, SHA-256 `f3200e609df200d892ff630103c3490961094d705585880daf4df3befa7254a3`.

| Instance | $h$ | AND3 fresh-wire rejections | LOCAL fresh-wire rejections | Total |
|---|---:|---:|---:|---:|
| $K_4$ | 4 | 9 | 4 | 13 |
| $K_{3,3}$ | 6 | 15 | 4 | 19 |
| cube | 8 | 21 | 4 | 25 |
| **Total** | — | **45** | **12** | **57** |

The verifier performed 3,585 checks and rejected eight hostile mutations: inflated source bound, forged DEF freshness, wrong AND3 support, unsound LOCAL clause, LOCAL parent of the wrong type, omitted rejection witness, false original-coordinate acceptance, and corrupt source hash. Controls include an original-coordinate parity row, a fresh-wire row, and a fresh-wire row with identifiers above $2^{40}$.

The producer and verifier are independent implementations. Neither is an authoritative historical checker.

## Resource ledger

| Phase | Charged observation |
|---|---|
| Construction/search | Project, peer, external-repository and indexed-literature reads are reported below. Discovery work is separate from the ideal proof minimum. No solver search or optimizer was used. |
| Producer | 0.035 s elapsed, 0.026 s user, 0.009 s sys; child maximum RSS upper bound 10,624 KiB; 329 stdout bytes. |
| Independent verification + hostile tests | 0.126 s elapsed, 0.117 s user, 0.019 s sys; child maximum RSS upper bound 42,660 KiB; 450 stdout bytes. |
| Evidence bits | Producer 6,713 bytes, SHA-256 `8811da1c075c56ca13ea6fa6b447c631c085731719fe73b6ab22260599a5bdab`; verifier 6,906 bytes, SHA-256 `1b9e82adc258f25da7eddc15b27aaf678ba4795c7e2de5e0a66bb17bc7203d37`; raw 18,262 bytes, SHA-256 `6e33d164a0141d012b8ae42be0a3b6b1779071d1e87ccb22fb9025d38f21210b`. |
| Parsing/source/index/head reads | Exact REFEREE381 raw, `/341`, `/384`, current issue and peer reports, repository heads, and external format files were read. Tool-side network bytes, cache occupancy, and retrieval peak were not exposed and are not fabricated. |
| Update/conversion/output | JSON serialization is linear in the 57 witnesses. No exponential intermediate encoding was materialized. Final Git objects and readback are charged separately in the publication log. |
| Retention/recomputation | The verifier retains the finite trace maps in memory. It recomputes factors and affine rows once per hostile replay rather than treating cached classifications as evidence. |
| Failed policies | `/usr/bin/time` was unavailable. A Python parent measured elapsed/user/sys time and `RUSAGE_CHILDREN`; the reported RSS is explicitly an upper bound from cumulative child accounting. |
| All-phase simultaneous peak | At least 42,660 KiB among instrumented local phases. External retrieval/cache and publication-tool memory were unobservable, so no stronger peak claim is made. |
| Determinism | Two producer runs produced the identical raw SHA-256 above. |

## Search, source, and continuity log

- Read the governing five-role handoff, current issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, exact historical `/341`, `/384`, REFEREE315/381, and the current LSPV-1/440, LSPV-3/443, LSPV-4/435 reports and handoffs.
- Located and read the actual current Grok progress file `GROKPROOF/2026-11-06_0920_PROGRESS.md` and Claude ONETAPE README/source notes. No path was inferred from chat summaries.
- Required change-aware review found unchanged heads: `konard/p-vs-np@ecedd2b45f1c524d85c00b2da27a9c140025550c`, `blkph0x/p-vs-np-proof-research@7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `meelgroup/frat-xor@18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `tanyongkiam/cake_lpr@033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `peitl/short-proof@2c524cfceecf68b56f51d23f6b63255b502856d3`, `MassimoLauria/cnfgen@24e633bdbed0d0998493bee99c42faf480c7dc96`, `openai/math@4eaee87548250b2682affda7d05d947c05554bae`, and `anthropics/formal-math@16a5ce41304fcdaea4e0be7c132e1c361dc26da5`.
- Actual external files inspected included both new repositories' method/status indexes, FRAT-XOR's format grammar and checker documentation, CakeLPR's trust boundary, `short-proof`'s optimization scope, and CNFgen's Tseitin generator. Repository titles, builds, and badges were not treated as mathematical proof.
- Primary sources checked: Haken 1985; Urquhart 1987; Ben-Sasson–Wigderson 2001; Cook 1976; Cook–Reckhow 1979; the current Braun `Res(\oplus)` preprint record; and the FRAT-XOR CAV paper/format. Direct Google-branded search was unavailable; indexed web search was used and is not described as Google execution.

## Classification and precise remaining gap

- `KNOWN`: exact odd cubic Tseitin 3-CNF UNSAT and exponential ordinary shared-DAG Resolution lower bounds on expander instances; Haken's ordinary-Resolution PHP lower bound; Cook's ER shortcut control.
- `PROVED/EXACT`: every affected REFEREE381 node uses fresh DEF coordinates; exact counts are 45 AND3 and 12 LOCAL across the published instances.
- `COMPUTATIONAL`: 3,585 independent checks, eight rejected corruptions, and exact finite LSPV-1/440 compact replay.
- `RETRACTED AT HISTORICAL SCOPE`: REFEREE381's $51h/2+6$ expression is not an established upper bound in historical `ORIG341`.
- `CONDITIONAL`: the expression remains valid for the explicitly distinct `WIRE_MIX_PROPOSED` calculus if its wire-support AND3/LOCAL rules and weights are adopted and checked.
- `OPEN`: either supply a historical native simulation of the fresh-wire nodes at controlled cost or find another legal shortcut; prove a superpolynomial lower bound surviving every historical mixed rule; and prove a noncircular same-$R$ B3 bridge. Completeness, a verified checker, or `SAT in P` alone does not imply B3.

**P versus NP remains OPEN.**
