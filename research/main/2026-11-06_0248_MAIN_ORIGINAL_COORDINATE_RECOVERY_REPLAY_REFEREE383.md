# LSPV-5/REFEREE383 — original-coordinate recovery replay

**Pacific timestamp:** 2026-11-06 02:48 PST  
**Role:** LSPV-5 Independent Red Team, Route B primary  
**Status:** `KNOWN THEOREM/DUPLICATE` for the $12h+2$ construction already stated by LSPV-1/436; `PROVED/EXACT` independent rule-level historical RES/AND3/XOR instantiation; `COMPUTATIONAL` finite certificates and hostile controls; authoritative accepted-byte parser, exact guarded-family optimum, full mixed hardness, B1/B2/B3, and P versus NP remain `OPEN`.

## Actual advance

REFEREE382 correctly rejected REFEREE381's fresh-wire AND3/LOCAL proof as historical-$R_{\mathrm{mix341}}$ evidence. It did **not** eliminate the earlier, stronger original-coordinate shortcut from LSPV-1/436. This run independently instantiates that known construction on the exact REFEREE381 guarded source bytes and checks every node.

For the guarded proper-3-CNF $K(F_h)$ built from a cubic odd-Tseitin source:

1. derive $\neg g$ once from the four padding clauses using three oriented Resolution nodes;
2. for each of the $4h$ original Tseitin clauses, resolve its two private split clauses on $y_i$, then resolve on $g$ against the shared $\neg g$, costing $8h$ Resolution nodes;
3. at each vertex conjoin the four recovered original three-clauses in three AND3 nodes supported on exactly the three original edge coordinates, costing $3h$;
4. XOR the $h$ exact vertex rows in a balanced tree, costing $h-1$ nodes and ending in $0=1$.

Therefore the historical rule-level calculus described in `/341` has the explicit legal shared-DAG upper bound

$$
W_{R_{\mathrm{mix341}}}(K(F_h))\le 3+8h+3h+(h-1)=12h+2.
$$

The already proved source-indispensability bound gives

$$
8h+3\le W_{R_{\mathrm{mix341}}}(K(F_h))\le12h+2.
$$

This is an envelope, not an exact optimum. The construction uses no DEF, LOCAL, split, discharge, weakening, semantic oracle, or fresh-wire affine coordinate. Consequently the guarded Tseitin family remains a linear-work failure as a candidate for full mixed-system superpolynomial hardness. This does not establish a polynomial bound on worst-case $\overline W_R$ and does not prove B3.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

Initial hypothesis: repair REFEREE381 within historical `/341` by deriving $\neg g$, recovering every original Tseitin clause, and replaying the original-coordinate AND3/GF(2) proof.

Precise falsifiers:

1. the four padding clauses do not derive $\neg g$ by oriented Resolution;
2. a split source pair cannot recover its original clause without weakening or assumption discharge;
3. some AND3 node needs more than three original variables or a fresh-wire coordinate;
4. the final XOR chain fails exact edge cancellation or omits an AND premise.

### Search result and revision

The construction was found verbatim in LSPV-1/436, blob `2c72bdf3934f91188e330fa628207ac1a02c5d68`; its $12h+2$ expression is not new. LSPV-1/439 explicitly retained it as the strongest upper control. The revised task therefore became independent source-byte instantiation and adversarial validation after REFEREE382, not rediscovery or novelty.

All four falsifiers fail at the rule level. The exact historical `/341` rule text licenses arbitrary-width oriented RES, AND3 over at most three original variables with exact truth-table annotation, and XOR of typed affine equations including $0=1$. The published finite traces use only those rules. No authoritative historical byte parser was located, so “accepted by the authoritative checker” remains `OPEN` and is not claimed.

## Claim card

| Field | Exact record |
|---|---|
| Claim ID | `LSPV-5/REFEREE383` |
| Quantifiers | For every connected simple bridgeless cubic graph $G_h$ and every odd charge vector $\chi$, the guarded source $K(F_{G_h,\chi})$ has a rule-level `/341` refutation with work $12h+2$ and span at most $5+\lceil\log_2h\rceil$. |
| Model | Fixed historical rule text `/341`: free authenticated source clauses; unit-cost binary RES, AND3, XOR; shared acyclic DAG; no added rule. |
| Resource | Sum of weights of distinct paid nodes. Span is longest weighted dependency path under unbounded parallelism. Implemented time/space are separately charged. |
| Same realization | Exact raw guarded DIMACS sources from REFEREE381, SHA-256 authenticated; proof nodes refer to those source labels. |
| Sufficient predecessor | `/341` exact original Tseitin proof plus the `/436` strict-3 guard recovery. |
| Falsification target | Invalid source identity, pivot orientation, factor truth table, original-coordinate scope, XOR mask, source ancestry, or root. |

## Exact family / theorem / encoding / method / transfer ledger

| Family or control | Exact encoding and parameter | Published theorem/model | Known method and present status | Remaining transfer |
|---|---|---|---|---|
| Cubic odd Tseitin | Connected cubic $G_h$; one variable $x_e$ per edge; for each vertex include the four proper signed 3-clauses falsified by the wrong-parity local assignments. Exactly $3h/2$ variables, $4h$ clauses, and $\Theta(h\log(h+2))$ indexed bits. | Urquhart 1987, DOI `10.1145/7531.8928`: $2^{\Omega(h)}$ ordinary unrestricted shared-DAG Resolution length on suitable expanders. Ben-Sasson–Wigderson supplies the width/size route. | Historical `/341` has exact optimum $4h-1$: three AND3 nodes per vertex plus $h-1$ XOR nodes. `PROVED/EXACT` in `/341`. | Resolution hardness does not transfer to the stronger mixed calculus. |
| Guarded strict-3 Tseitin $K(F_h)$ | Replace each $C_i=(a_i\vee b_i\vee c_i)$ by $(g\vee a_i\vee y_i)$ and $(\neg y_i\vee b_i\vee c_i)$. Add $(\neg g\vee p^s\vee q^t)$ for $s,t\in\{0,1\}$. Exactly $8h+4$ proper 3-clauses and $11h/2+3$ variables. | LSPV-1/435–436 proves ordinary-Resolution hardness preservation by an explicit proof transformation, not equisatisfiability alone. Thus suitable expanders remain $2^{\Omega(h)}$ hard in ordinary Resolution. | This run reproduces the known `/436` mixed shortcut $12h+2$ using only original-coordinate RES/AND3/XOR. Lower source floor $8h+3$. | Exact mixed optimum and authoritative accepted-byte syntax remain open; the family cannot witness superpolynomial full mixed work. |
| Unary PHP control | $p_{i,j}$, one wide pigeon clause per pigeon, binary collision clauses. Not native 3-CNF for unbounded holes. | Haken 1985, DOI `10.1016/0304-3975(85)90144-6`: exponential ordinary shared-DAG Resolution size. | Cook 1976 gives polynomial Extended-Resolution proofs; this shortcut must not be excluded. | Any strict-3 transfer needs a lower-bound-preserving simulation direction and encoded-size bound. |
| Bit-PHP `Res(\oplus)` control | $n=2^\ell$ holes, $n+1$ pigeons, width-$2\ell$ signed collision clauses. | Braun arXiv:2609.23015 reports $2^{\Omega(n/\ell^2)}$ unrestricted DAG-like `Res(\oplus)` size for $\ell\ge32$; current preprint/formalization was not independently kernel-replayed here. | Cook/ER-style definitions are outside the lower-bound model. LSPV-3/444 blocks one proposed high-support GATE-LOCAL translation but not every historical repair. | No transfer to extension-enabled `/341`, strict 3-CNF, or arbitrary algorithms. |
| Random proper 3-CNF control | Signed proper 3-clauses at constant density. | Chvátal–Szemerédi 1988: exponential ordinary-Resolution hardness with high probability in the stated regime. A current Pang preprint reports stronger algebraic-system results, but remains unrefereed. | No established mixed all-rule invariant; LSPV-3/443 obtains only a linear bounded-premise core floor. | Full mixed transfer remains `OPEN`. |

Certified UNSAT, proof-size hardness in a named system, and finite execution are separate claims. No restricted lower bound above is an all-algorithm SAT lower bound.

## Rule-by-rule proof

Let $m=4h$ and write the four pad clauses as

$$
P_{st}=\neg g\vee p^s\vee q^t,\qquad s,t\in\{0,1\},
$$

where exponent notation selects the signed literal. Resolve $P_{00}$ with $P_{01}$ on $q$, and $P_{10}$ with $P_{11}$ on $q$, obtaining $\neg g\vee p$ and $\neg g\vee\neg p$. Resolve on $p$ to obtain $\neg g$. These are three paid nodes, and every pad source is an AND obligation.

For each base clause $C_i=(a_i\vee b_i\vee c_i)$, resolve

$$
(g\vee a_i\vee y_i),\quad(\neg y_i\vee b_i\vee c_i)
$$

on $y_i$ to get $g\vee C_i$, then resolve with the single shared $\neg g$ node to get $C_i$. This is exactly two nodes per clause, hence $8h$. There is no weakening: both conclusions are exact resolvents.

At a vertex $v$, all four recovered clauses have support equal to its three original incident edge variables. Combine them as two pairwise AND3 factors and one final AND3 factor. Exhaustive evaluation of eight assignments verifies exact equivalence with

$$
\bigoplus_{e\ni v}x_e=\chi(v).
$$

This costs $3h$ and satisfies the literal original-coordinate bound. XOR the rows. Every edge appears at its two endpoints and cancels, while $\bigoplus_v\chi(v)=1$. The final paid node is the permitted contradiction row $0=1$. A balanced XOR tree uses $h-1$ nodes.

Thus work is $12h+2$. Pad elimination has depth two; clause recovery depth three; the local factor tree reaches depth five; balanced XOR gives span $5+\lceil\log_2h\rceil$. The ideal minimum is allowed to choose something even shorter.

## Lower envelope, sharing, and branch semantics

LSPV-1/436 proves that if $F_h$ is clause-minimally UNSAT, then $K(F_h)$ is clause-minimally UNSAT. Cubic bridgeless odd-Tseitin sources have this property. Hence every one of the $8h+4$ guarded source clauses must occur in the ancestry of any sound source-explicit refutation. With at most two premises per paid unit node, the connected-ancestry bound gives $W\ge(8h+4)-1=8h+3$.

The present proof is one acyclic shared DAG. The $\neg g$ node is retained once and referenced in all $4h$ recoveries; it is never recomputed or charged $4h$ times. Every RES/AND3/XOR node is a directed hyperedge with all parents required. There is no OR case choice, branch assumption, branch-local lemma, reconvergence under incompatible contexts, discharge, or weakening. The result therefore tests shared reasoning without adding a split rule to `/341`.

The lower and upper bounds leave a $4h-1$ gap. Nothing here proves attainment of either endpoint as the guarded-family minimum.

## Independent finite instantiation

Artifacts:

- producer: `experiments/review/lspv5_383_original_coordinate_recovery.py`;
- independent verifier: `experiments/review/lspv5_383_independent_verify.mjs`;
- raw: `results/raw/review/2026-11-06_0248_LSPV5_ORIGINAL_COORDINATE_RECOVERY383.json`;
- authenticated input: REFEREE381 raw SHA-256 `f3200e609df200d892ff630103c3490961094d705585880daf4df3befa7254a3`.

| Graph | $h$ | source clauses | lower floor | proof work | balanced span | deletion witnesses |
|---|---:|---:|---:|---:|---:|---:|
| $K_4$ | 4 | 36 | 35 | 50 | 7 | 36 |
| $K_{3,3}$ | 6 | 52 | 51 | 74 | 8 | 52 |
| cube | 8 | 68 | 67 | 98 | 8 | 68 |

The independent Node verifier performed 10,719 assertions. It re-parses the exact DIMACS, checks source SHA-256 and source-record identity, every oriented pivot and exact resolvent, every eight-row AND3 factor and affine annotation, original-coordinate support, every XOR mask/RHS, balanced depth, backward liveness, all 156 deletion witnesses, the even-charge SAT witnesses, and eight malformed inputs.

Eight hostile mutations were rejected: wrong RES pivot, corrupt source clause, fresh-wire AND3 support, wrong factor truth table, wrong affine RHS, wrong XOR row, omitted deletion witness, and false root.

Direct peer controls were also executed from current published GitHub bytes:

- LSPV-1/442 compact strict-Resolution join: closure 87, 5 models before the opposite row, 0 after, canonical join 7 versus strengthened join 6; 18 compact assertions.
- LSPV-3/444 compact prefix-scope analyzer: 2,720 truth rows, 180 assertions, eight mutants rejected. It tests inlined-original support only and is not a historical checker.

None of these programs is described as execution of an authoritative historical `/341` checker.

## Resource ledger

| Phase | Actual charged record |
|---|---|
| Logical evidence | $12h+2$ distinct paid nodes in the exhibited proof; sources are free under fixed `/341` weights. Reference/application costs are exactly those expressed by the nodes; no revised weight is introduced. |
| Producer | 0.113 s elapsed, 0.105 s user, 0.008 s sys; 13,148 KiB child maximum-RSS upper bound; 458 stdout bytes. |
| Independent verifier | 0.093 s elapsed, 0.087 s user, 0.019 s sys; 50,280 KiB child maximum-RSS upper bound; 600 stdout bytes. |
| Explicit artifacts | Producer 13,833 bytes, SHA-256 `8adc8e2d200b451b623a35b226e403ca60678166bfe064c2af64e8dfc5d21017`; verifier 7,942 bytes, SHA-256 `a3f6591e56a4b0ea2bdbabea93d8f482dae2f147ee74423bf0fedb151560ceda`; raw 254,223 bytes, SHA-256 `524f65bf4f033000ccaa675e14c870654eb758621d26cdb282f95b604b93df7b`. |
| Parsing/source/index/head reads | Exact source bytes, repository head, issue #3, governance, peer reports, historical `/341`, external repository heads, and primary-source records were read. Connector-side transfer bytes/cache memory were not exposed. |
| Construction/search | Exhaustive edge enumeration generated deletion witnesses only for $h=4,6,8$; this finite search is not part of the ideal proof work. The symbolic all-size proof uses the known incidence/minimality argument. |
| Conversion/update/output | Source recovery is two RES nodes per base clause. Serialization writes explicit clauses, factors, masks, witnesses, and provenance. Two producer runs yielded the identical raw SHA-256. |
| Retention/recomputation | The logical schedule retains shared $\neg g$ once. The verifier rebuilds semantics during each hostile replay. A streaming implementation may discard recovered clauses after forming vertex rows; explicit output still incurs its full evidence bits. |
| Compact versus materialized affine rows | Explicit variable masks across the XOR tree can occupy $O(h^2\log h)$ bits; a compact graph/incidence schedule can describe the same construction in $O(h\log h)$ source-scale bits but must pay expansion/checking work. No exponential encoding was materialized or forbidden by fiat. |
| Failed policies | Local preflight failed because this execution directory is a partial artifact workspace without root `main.tex`, `AGENTS.md`, `CODEX.md`, or the skill file. Their authenticated current GitHub bytes were read instead; the failure is recorded rather than disguised. |
| All-phase simultaneous peak | At least 50,280 KiB among instrumented local phases. Connector and publication memory were unavailable, so no stronger simultaneous-peak claim is made. |

## Search, provenance, duplication, and continuity record

- Current project head at search start: `90718f598d08520acf5dcd71ad260c6dbaec5f89`. Read current issue #3, governance, project research instructions, exact `/341`, `/384`, REFEREE381–382, LSPV-1/442, LSPV-3/444, and their executable controls.
- Read actual Grok `GROKPROOF/2026-11-06_0920_PROGRESS.md` and Claude ONETAPE README/source. Neither supplies a different historical grammar or B3 bridge.
- Duplicate found and adopted: LSPV-1/436 already states this exact $12h+2$ shortcut; LSPV-1/439 retains it. This report claims independent reproduction and post-REFEREE382 scope reconciliation only.
- Required change-aware external review found unchanged heads: `konard/p-vs-np@ecedd2b45f1c524d85c00b2da27a9c140025550c`, `blkph0x/p-vs-np-proof-research@7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `meelgroup/frat-xor@18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `tanyongkiam/cake_lpr@033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `peitl/short-proof@2c524cfceecf68b56f51d23f6b63255b502856d3`, `MassimoLauria/cnfgen@24e633bdbed0d0998493bee99c42faf480c7dc96`, `openai/math@4eaee87548250b2682affda7d05d947c05554bae`, and `anthropics/formal-math@16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. No reviewed repository authenticates historical `/341` bytes or proves B3.
- Primary literature checked: Urquhart 1987; Haken 1985; Cook 1976; Cook–Reckhow 1979; Ben-Sasson–Wigderson 2001; current Braun and Pang preprint records. Direct Google-branded search was unavailable; indexed web search was used.
- Cross-field audit: circuit sharing supplies only an analogy for retaining $\neg g$ once; the exact result follows from proof-DAG identity, so no foreign theorem is imported. VLSI/communication locality cannot yield unrestricted machine hardness here. Status: `FAILED TRANSFER` for any such lower-bound inference.

## Classification and precise remaining gap

- `KNOWN THEOREM/DUPLICATE`: the all-size $12h+2$ construction is LSPV-1/436, not a new theorem.
- `PROVED/EXACT`: under the exact rule-level `/341` RES/AND3/XOR definitions and weights, the construction is legal, source-authenticated, original-coordinate, and has the displayed work/span bounds.
- `COMPUTATIONAL`: exact $K_4$, $K_{3,3}$, and cube traces; 10,719 independent checks; 156 deletion witnesses; eight malformed sources; eight corruptions rejected; peer compact replays executed.
- `OPEN`: authoritative accepted-byte syntax/parser; exact guarded-family minimum inside the envelope; a family with superpolynomial minimum against every historical mixed rule; and a noncircular theorem that `SAT in P` implies polynomial $\overline W_R$ for this same fixed $R$.

**Publication status:** the dated report, code, raw evidence, handoff, root insert, commit, issue update, and readback are recorded by the publication step of this run.

**P versus NP remains OPEN.**
