# LSPV-5/REFEREE381 — guarded Tseitin boundary-row bypass

**Pacific timestamp:** 2026-11-06 00:52 PST  
**Role:** LSPV-5 Independent Red Team, Route B primary  
**Status:** `KNOWN` source family and ordinary-Resolution lower bound; `COMPUTATIONAL` finite candidate traces; `CONDITIONAL` historical-$R_{\mathrm{mix341}}$ admissibility; unrestricted mixed-calculus lower bound and B3 remain `OPEN`.

## Actual advance

The latest LSPV-1 construction left a four-variable guarded affine exporter unauthenticated. This run removes that exporter from the candidate upper bound.

For a connected simple cubic graph $G=(V,E)$ with $h=|V|$, put one odd Tseitin charge at $v_*$ and charge zero elsewhere. In the guarded, proper-3-CNF construction below, the candidate shared derivation:

1. derives exact three-variable parity rows only at the $h-1$ charge-zero vertices;
2. XORs them to the three-edge boundary equation at $v_*$;
3. converts that one three-variable equation to its four clauses;
4. combines those clauses with the four guarded charge-one blockers in exactly seven Resolution nodes to derive $g$;
5. derives $\neg g$ from the padding gadget in three Resolution nodes and resolves to the empty clause.

Under the declared semantic grammar (owner-qualified definition facets, exact-factor `AND3`, row `XOR`, implication-preserving `LOCAL`, and oriented `RES`) this costs

$$
\frac{3h}{2}\;\mathrm{DEF}+20(h-1)\;\mathrm{RES}+3(h-1)\;\mathrm{AND3}
+(h-2)\;\mathrm{XOR}+4\;\mathrm{LOCAL}+16\;\mathrm{RES}+7\;\mathrm{RES}
+3\;\mathrm{RES}+1\;\mathrm{RES}
=\frac{51h}{2}+6.
$$

This is an upper-bound control, not a minimum proof and not a lower bound. It defeats any proposed transfer that treats the missing four-variable exporter as the only obstruction. It does **not** authenticate the historical byte grammar: historical access to definition facets and the exact equation-to-clause `LOCAL` are still open.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

Initial hypothesis: the LSPV-1/437 positive-guard Tseitin lower-bound candidate collapses under the known mixed $\mathrm{GF}(2)$ shortcut after transporting the guard through paid definitions.

Precise falsifiers:

1. the guarded source clauses do not authenticate the affine premises;
2. historical `GF2` cannot carry or eliminate the guard;
3. the construction requires an absent split, discharge, or weakening rule;
4. an already accepted historical trace provides the claimed transport with different costs.

### Evidence that changed the idea

- LSPV-1/438 proposed $w_e=(\neg g)\wedge x_e$ but left the local compiler open.
- LSPV-1/439 supplied explicit clausal derivations: 20 `RES` nodes per charge-zero vertex and 16 `RES` nodes at the charge-one vertex, while correctly declining to claim the four-variable exporter.
- LSPV-3/436 and /440 preserve the grammar firewall: semantic implication is not historical provenance, and `GATE-LOCAL` is proposed rather than authenticated.
- Exact-phrase searches found no prior project occurrence of the boundary-only construction or its seven-node bridge.

Revised claim: export only the $h-1$ charge-zero rows, sum them to the exceptional boundary, and finish clause-wise. This avoids the disputed four-variable object and uses no branching, discharge, weakening, or branch-local leakage.

## Family / theorem / encoding / method / transfer ledger

| Item | Exact record | Status / remaining transfer |
|---|---|---|
| Base family | Connected simple cubic $G_h$; edge variable $x_e$; charge vector $\chi$ with $\bigoplus_v\chi(v)=1$. At each vertex with incident edges $(e_0,e_1,e_2)$, include the four clauses $C_b=\bigvee_i(x_{e_i}\text{ if }b_i=0\text{ else }\neg x_{e_i})$ for $b\in\{0,1\}^3$ with $b_0\oplus b_1\oplus b_2\ne\chi(v)$. | Exact proper 3-CNF: $3h/2$ variables and $4h$ clauses. UNSAT follows because XORing all vertex equations cancels every edge twice but leaves odd total charge. `KNOWN`. |
| Published lower bound | Urquhart, *Hard examples for resolution*, JACM 34(1), 1987, DOI 10.1145/7531.8928; width route also covered by Ben-Sasson–Wigderson, *Short Proofs Are Narrow*, JACM 48(2), 2001. For a constant-expansion bounded-degree family, ordinary Resolution refutation size is $\exp(\Omega(h))$. | Model is ordinary shared-DAG Resolution with clauses and the Resolution rule. This is **not** hardness for Extended Resolution, $\mathrm{Res}(\oplus)$, $R_{\mathrm{mix341}}$, branching programs, or algorithms. `PROVED-RESTRICTED`. |
| Guarded proper-3-CNF | For every base clause $C=(a\vee b\vee c)$ introduce a fresh $y_C$ and replace it by $(g\vee a\vee y_C)\wedge(\neg y_C\vee b\vee c)$. Add four clauses $(\neg g\vee p^s\vee q^t)$, $s,t\in\{0,1\}$, where exponent notation selects the positive/negative literal. | $8h+4$ proper 3-clauses. If $g=0$, the base Tseitin formula is recovered after existentially eliminating each $y_C$; if $g=1$, the padding gadget is contradictory. Thus the source is UNSAT. Ordinary-Resolution hardness preservation is a separate project result; equisatisfiability alone is not used as a mixed-system lower bound. |
| Paid guarded edge | One globally fresh $w_e$ per edge with $w_e=(\neg g)\wedge x_e$ and facets $(\neg w_e\vee\neg g)$, $(\neg w_e\vee x_e)$, $(w_e\vee g\vee\neg x_e)$. | Shared once across both endpoint derivations. Historical availability and cost of facet references remain unauthenticated. `CONDITIONAL`. |
| Charge-zero compiler | Four wrong-assignment blockers over $(w_{e_0},w_{e_1},w_{e_2})$, each in five `RES` nodes; three `AND3` nodes combine them into the exact parity-zero factor. | $20\,\mathrm{RES}+3\,\mathrm{AND3}$ per vertex. Independently replayed semantically. Historical `AND3` exact-factor syntax remains to authenticate. |
| Boundary aggregation | XOR the $h-1$ charge-zero rows. Every internal edge occurs twice and cancels; only the three edges incident to $v_*$ remain, with RHS zero. | $h-2$ shared `XOR` nodes. A balanced aggregation has span $\lceil\log_2(h-1)\rceil$ without changing work. Historical row encoding and reference costs remain to authenticate. |
| Exceptional bridge | Four `LOCAL` nodes emit the odd-assignment blockers of the boundary parity-zero row. Six binary eliminations and one final elimination combine them with the four guarded even blockers of the charge-one vertex to derive $g$. | Exact seven-`RES` bridge below. No four-variable exporter. Historical `LOCAL` remains the key grammar gap. |
| Mandatory shortcuts | Ordinary Resolution is hard on the expander family, while extension variables and algebraic parity reasoning can collapse that restricted hardness. Cook–Reckhow’s Extended Frege discussion and the project’s native unguarded Tseitin shortcut are controls, not exclusions. | Therefore ordinary-Resolution hardness does not transfer automatically into the full mixed minimum. `KNOWN` methodological control; full transfer `OPEN`. |

## Exact seven-node bridge

Let $(w_0,w_1,w_2)$ be the boundary variables. Write $B_b=g\vee C_b$ for the four guarded blockers with even $b$, and $C_b$ for the four unguarded blockers with odd $b$. Oriented Resolution gives:

1. $\operatorname{Res}_{w_2}(B_{000},C_{001})=g\vee w_0\vee w_1$;
2. $\operatorname{Res}_{w_2}(C_{010},B_{011})=g\vee w_0\vee\neg w_1$;
3. resolve the preceding two on $w_1$ to obtain $g\vee w_0$;
4. $\operatorname{Res}_{w_2}(C_{100},B_{101})=g\vee\neg w_0\vee w_1$;
5. $\operatorname{Res}_{w_2}(B_{110},C_{111})=g\vee\neg w_0\vee\neg w_1$;
6. resolve the preceding two on $w_1$ to obtain $g\vee\neg w_0$;
7. resolve on $w_0$ to obtain $g$.

Every inference has both premises as an AND obligation. There is no branch choice, assumption discharge, or weakening. The derivation DAG is acyclic; shared definition nodes and accumulated affine rows are charged once.

## Work, span, storage, and sharing

- **Distinct-node work:** exactly $51h/2+6$ under unit weights for the declared node types. This does not revise historical weights; it is conditional on those node types matching the historical calculus.
- **Producer trace span:** the serialized left-fold XOR gives unit-weight span at most $h+10$ from zero-cost sources.
- **Balanced candidate span:** balancing the $h-1$ row aggregation gives span at most $12+\lceil\log_2(h-1)\rceil$; work is unchanged.
- **Retention schedule:** keeping every inference realizes the shared-DAG work with $O(h)$ logical nodes and $O(h\log h)$ identifier/evidence bits for bounded-degree indexed graphs. Recomputing rows can lower live storage but increases executed work; no such recomputation is hidden in the reported node total.
- **Branching model:** this trace is a legal candidate only if its native rules authenticate. It is not a case-split proof. Consequently it neither adds a split rule nor tests branch-local context discharge; it is nevertheless a mandatory upper-bound control for the global minimum.

## Independent finite replay

Artifacts:

- producer: `experiments/review/lspv5_381_guarded_tseitin_boundary_bypass.py`;
- independent verifier: `experiments/review/lspv5_381_independent_verify.mjs` (does not import producer code);
- raw traces: `results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json`.

| Instance | $h$ | Source clauses | Paid nodes | Source label control |
|---|---:|---:|---:|---|
| $K_4$ | 4 | 36 | 108 | odd source has 0 underlying Tseitin models; independently generated even-charge counterpart has a checked witness |
| $K_{3,3}$ | 6 | 52 | 159 | same |
| cube | 8 | 68 | 210 | same |

The verifier performed 5,575 structural/semantic checks and rejected eight hostile mutations: wrong Resolution pivot, corrupted original source, nonfresh definition, wrong `AND3` row, wrong `XOR` row, unsound `LOCAL`, omitted source, and false final root. It checks exact source bytes and SHA-256, proper-3-CNF syntax, odd UNSAT at the underlying Tseitin level, even-charge witnesses, global freshness, oriented Resolution, exact factors, affine annotations, XOR cancellation, local implication, all-node liveness, unit $g$, and the empty root.

This is an independent reimplementation, **not** execution of an authoritative historical checker. The authoritative checker was not located in the reviewed historical material.

## Resource ledger

| Phase | Time / peak / evidence |
|---|---|
| Construction + serialization | 0.052 s real, 0.040 s user, 0.012 s sys; 12,928 KiB process maximum RSS |
| Independent parse + verification + hostile replays | 0.105 s real, 0.131 s user, 0.016 s sys; 52,128 KiB process maximum RSS |
| Raw evidence | 221,850 bytes; SHA-256 `f3200e609df200d892ff630103c3490961094d705585880daf4df3befa7254a3` |
| Producer | 13,642 bytes; SHA-256 `397e07b88fcc39a46a0c188e6b41938db04ba3eee09fd3b0b4cd69acf6024e5f` |
| Verifier | 9,917 bytes; SHA-256 `b7598df09d5a6df5ee683ecbecee0d777c9c5fb435683e878c5cf599bfa84789` |
| Determinism | two consecutive producer runs yielded the same raw SHA-256 |
| Reads/search/conversion/output | Project head, issue #3, governance, peer reports, Grok/Claude files, primary literature, and pinned repository heads were read. Tool-side network byte counts, cache occupancy, and retrieval peak were not exposed and are not fabricated. No exponential intermediate encoding was materialized. |
| Failed policies | First verifier replay rejected the trace because object comparison was JSON-key-order sensitive; canonical structural comparison repaired the verifier, after which all proof checks and hostile tests passed. `/usr/bin/time` was unavailable; language runtime resource counters and shell timing supplied the reported measurements. |
| All-phase simultaneous peak | At least 52,128 KiB among instrumented local phases; external retrieval/cache memory was not observable, so no stronger simultaneous-peak claim is made. |

## Source and repository authentication log

- Governing project materials were read at the then-current `j15marti/pnp` head, including `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, the five-role handoff, issue #3, LSPV-1/438-/439, LSPV-3/436-/440, the historical /341 report, `GROKPROOF/2026-11-06_0515_PROGRESS.md`, and the current Claude assessment. An initially guessed Grok path failed; the directory was enumerated and the actual path was then read.
- Required change-aware reviews found unchanged heads: `konard/p-vs-np@ecedd2b45f1c524d85c00b2da27a9c140025550c`, `blkph0x/p-vs-np-proof-research@7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `meelgroup/frat-xor@18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `tanyongkiam/cake_lpr@033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `peitl/short-proof@2c524cf`, `MassimoLauria/cnfgen@24e633b`, `openai/math@4eaee875`, and `anthropics/formal-math@16a5ce`. None supplies the missing historical-$R_{\mathrm{mix341}}$ authentication or a B3 bridge.
- CNFgen’s `cnfgen/families/tseitin.py` was inspected as an implementation reference, not as a lower-bound proof.
- Primary sources: Urquhart DOI 10.1145/7531.8928; Ben-Sasson–Wigderson PDF `https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf`; Cook–Reckhow PDF `https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf`.
- Google-branded search was not available. The indexed web-search service was used and the limitation is explicit.

## Classification and precise remaining gap

- `KNOWN`: the exact odd cubic Tseitin 3-CNF is UNSAT; expander instances have exponential ordinary shared-DAG Resolution lower bounds.
- `PROVED-RESTRICTED`: those lower bounds apply to ordinary Resolution, not to the full mixed calculus.
- `COMPUTATIONAL`: the three finite semantic candidate DAGs and both-label/corruption controls replay independently.
- `CONDITIONAL`: if the historical grammar permits the exact referenced definition facets, `AND3` annotations, row `XOR`, and equation-to-clause `LOCAL` at the recorded weights, then the family has the exhibited linear-work refutations $W_R(K(F_h))\le 51h/2+6$.
- `OPEN`: authenticate those historical bytes/rules and costs, or give a legal counterexample; prove a lower bound surviving every mixed shortcut; and prove a noncircular same-$R$ B3 bridge. Completeness, trace checking, or `SAT in P` alone does not provide such a bridge.

**P versus NP remains OPEN.**
