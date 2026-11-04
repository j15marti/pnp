# FIXED-K-ER-EQUIVALENCE-GRAMMAR-GAP-REFEREE336

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 04:50 PST**

**Status:** **PROVED/RESTRICTED** polynomial equivalence between binary-gate Extended Resolution and a typed fixed-support private-root fragment of `R_mix341`; **PROVED/EXACT** conventional binary-OR ER-to-signed-AND compilation; **FALSIFIED AS A CURRENTLY CERTIFIED INFERENCE** the proposed unconditional converse for all literal `R_mix341`; **OPEN** full-calculus promotion, B1, B2, B3, superpolynomial mixed cost, and P versus NP. The fixed calculus, five roles, task states, ownership and schedules are unchanged.

## Outcome

The initial proposed advance, `ER2 -> R_mix341`, was a duplicate of REFEREE299. The five-role audit instead isolated the strongest valid converse and the exact premise that prevents promoting it to the whole calculus.

Let `E=ER2` be the strict signed `RES+DEF` subsystem. For each fixed integer `K`, define `R_rootK` as the fragment of the unchanged calculus in which:

1. every `LOCAL-CONVERT` conclusion is a private, root-extensional condition;
2. the union of external variable names in its authenticated parents and conclusion has size at most `K`;
3. canonical truth-table replacement preserves all clause/factor/row, sign, original/auxiliary and source-authentication tags; and
4. every wide GF(2) row satisfies the authentication hypotheses of LSPV-1/375.

For every valid UNSAT CNF `F` of encoded length `N`, there is a constant `C_K`, depending only on the fixed grammar, such that

`W_RrootK(F) <= W_E(F) <= C_K (N + W_RrootK(F) + 3)^4`.

Consequently,

`Wbar_RrootK(N) <= Wbar_E(N) <= C_K (N + Wbar_RrootK(N) + 3)^4`.

Thus this typed fragment and binary-gate Extended Resolution have equivalent polynomial/superpolynomial worst-case minimum-cost status. B1, B2 and B3 are individually equivalent between these two fixed systems. **None is proved true.**

For full `R_mix341`, only the already certified one-way bounds and implications remain:

`W_Rmix(F) <= W_E(F)`, `Wbar_Rmix(N) <= Wbar_E(N)`,

and `B1_E => B1_Rmix`, `B2_E => B2_Rmix`, `B3_E => B3_Rmix`.

The reverse directions are open because the authoritative prose does not fix a numeric common-support bound or a complete machine-readable typed coercion from a circuit root to the local truth-table factors required by the published compiler. REFEREE335 settles private-root versus public-wire semantics, but does not settle this typing obligation.

## Published lower-bound anchor: exact model and strength

The established anchor is Haken's 1985 lower bound for the standard unary pigeonhole contradictions `PHP(h+1,h)`. Its explicit CNF uses variables `x_(p,j)`, clauses requiring every pigeon to occupy a hole, and pairwise clauses forbidding two pigeons in one hole. Source clauses are free axioms. A proof line is a clause; the sole inference is ordinary binary Resolution; arbitrary width, pivots, reuse and shared-DAG structure are allowed.

In the project theorem form, there exist constants `c>0,h0` such that for every `h>=h0` and every ordinary Resolution refutation `pi` of this explicit CNF, `|pi|>=2^(c h)`. The input has `h(h+1)` variables and `(h+1)+h*binom(h+1,2)=Theta(h^3)` clauses. With explicit signed binary indices, `N_h=Theta(h^3 log(h+2))`, so the statement is `2^Omega((N_h/log N_h)^(1/3))`, not `2^Omega(N_h)`.

This is **not** a lower bound for Extended Resolution, Extended Frege, `Res(XOR)`, `R_mix341`, or arbitrary SAT machines. Cook's 1976 polynomial Extended Resolution refutations of pigeonhole are the mandatory countercontrol. Haken's own abstract explicitly notes the ER shortcut. No published lower bound is regenerated here.

Primary sources: A. Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`; S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), DOI `10.1145/1008335.1008338`; S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1) (1979), DOI `10.2307/2273702`.

## The restricted equivalence theorem

### Easy direction

`E` is a subsystem of `R_rootK`, so every `E` proof is already a legal mixed proof. REFEREE299 gives the exact source-authenticated topological translation and hence `W_RrootK(F)<=W_E(F)`.

Conventional binary-OR ER also compiles with constant overhead. For an instruction

`y <-> (l1 OR l2)`,

introduce the signed-AND definition `u := NOT sigma(l1) AND NOT sigma(l2)` and extend the signed literal substitution by `sigma(y)=NOT u`, `sigma(NOT y)=u`. The three conventional extension clauses become exactly the three `DEF` slots

`(u OR sigma(l1) OR sigma(l2))`, `(NOT u OR NOT sigma(l1))`, `(NOT u OR NOT sigma(l2))`.

Complementation is preserved, so each later resolvent maps to one legal `RES` step. This is a uniform one-pass syntactic compiler, not a semantic oracle.

### Converse in `R_rootK`

Take a `q`-node `R_rootK` proof. Replay `RES` and `DEF`. For each fixed-support `AND3` or `LOCAL-CONVERT` step, enumerate the at most `2^K` external assignments. Soundness ensures that every falsifying assignment of the conclusion is excluded by authenticated predecessor blockers. Paid signed weakening and variable elimination derive every required conclusion blocker using a number of strict `RES+DEF` steps bounded by a constant `d_K` independent of `F,N,q`. The common-support-three case is the already published LSPV-1/359 compiler; the fixed-`K` argument is the same finite-template construction with `d_K` allowed to depend on `K`.

For every authenticated wide GF(2) row addition, apply LSPV-1/375: parity-prefix definitions plus constant local templates compile the step into `O(v+1)` ER nodes, where the number of source and paid-DEF names satisfies `v<=N+q`. Shared rows and arbitrary adaptive order remain legal. Therefore the whole proof has at most

`O(q(v+1)+d_K q+1) <= C_K (N+q+3)^4`

ER nodes. Minimize over mixed proofs and maximize over inputs to obtain both displayed inequalities.

### B obligations

Polynomial comparison in both directions gives, separately, `B1_RrootK <=> B1_E`, `B2_RrootK <=> B2_E`, and `B3_RrootK <=> B3_E`. This is only an equivalence of open obligations. For full `R_mix341`, the one-way cost inequality yields only the `E => Rmix` directions stated above. Independently, `B1=>B2=>B3`; no converse is assumed.

## Exact full-calculus promotion gap

The tempting composition

`REFEREE335 normalization -> X3/375 -> ER2`

does not currently certify the converse for every full mixed proof. LSPV-1/359 requires authenticated input and output factors on a common set of at most three named variables and preserved original/auxiliary typing. LSPV-1/375 adds only authenticated rows of its declared form. The authoritative `R_mix341` prose instead says `bounded-support Boolean circuit condition` and `constant-support truth-table check`, without a numeric `K`, a full serialized parser, or the exact typed coercion.

REFEREE335 proves a same-node polynomial-bit root representative under private-root semantics. That theorem does not by itself prove that the representative is an `X3` record. Therefore the unconditional reverse inequality for full `R_mix341` is rejected as presently under-justified, not asserted false in every reasonable completion.

A future promotion needs one of:

1. an authoritative global constant `K` plus typed root-to-factor coercion preserving every downstream legality check; or
2. a direct full-parser `R_mix341 -> ER2` compiler with polynomial encoded overhead.

An exponential-overhead backtranslation would not suffice for the requested machine-hardness transfer.

## Physical-cost ledger

| object/phase | logical cost | actual time/access | output length | peak writable space |
|---|---:|---:|---:|---:|
| canonical ER-to-mixed proof, encoded length `P` | node-preserving | `O(N+P)` construction | `O(N+P)` | materialized `O(N+P)`; streaming counters possible |
| canonical `R_rootK` proof, `q` nodes | polynomial ER proof exists | direct generation `poly(N+q)` after proof is known | `poly(N+q)` | schedule-dependent |
| supplied raw mixed record, payload `M` | unchanged node count | faithful normalization can require `Omega(M)` reads | input `Theta(M)` | streaming can be logarithmic; no linear-space lower bound |
| explicit exponential intermediate | representation-dependent | output/access volume is charged | exponential if materialized | may trade storage for recomputation |
| lazy descriptor | descriptor nodes only | construction, every bit query, update, recomputation and verification charged | compact | schedule-dependent |

The minimum logical DAG grants free selection of the best proof. It does not make parsing, construction, access, validation, output or storage free. Conversely, the `Omega(M)` raw-access result is not a lower bound for a source-only direct canonical generator.

## Falsifiers and classifications

1. **The new result is the one-way `ER2 -> R_mix341` simulation. — DUPLICATE.** REFEREE299 already proved it.
2. **REFEREE335 automatically places every full mixed node in `X3`. — FALSIFIED AS A CERTIFIED INFERENCE.** Common-support/type/authentication premises remain unstated.
3. **A fixed typed private-root support bound still permits superpolynomial separation from ER. — FALSIFIED.** The theorem gives polynomial equivalence.
4. **The proof-system equivalence establishes B3 or unrestricted SAT hardness. — FALSE.** No arbitrary-decider trace compiler is supplied.

## Finite controls

The Python producer checked all four literal-sign patterns and all 32 signed OR-to-AND assignments, 147 non-tautological resolution/substitution cases, seven malformed extension records, SAT and UNSAT controls, and 12,675 polynomial-inequality controls: **12,868 assertions PASS**. An independently authored Node verifier replayed the signed-gate and arithmetic checks with **12,713 checks PASS**. These controls test the exact conventional-ER compiler and inequality directions; they do not certify the all-size proof theorem or any lower bound.

Artifacts:

- `experiments/arc/lspv5_336/er2_rmix_equivalence_referee336.py`
- `experiments/arc/lspv5_336/verify_er2_rmix_equivalence_referee336.js`
- `results/raw/arc/lspv5_336/er2_rmix_equivalence_referee336.json`

## Five-role, Grok, Claude and duplication review

All five role audits were completed. LSPV-1 identified the exact common-support/type mismatch; LSPV-2 supplied the conventional binary-OR compiler and 317-case independent audit; LSPV-3 authenticated the DEF certificate semantics and ER/Extended-Frege barrier; LSPV-4 supplied the fully charged construction/output/space ledger; LSPV-5 independently found the potential composition, which was then narrowed after the final grammar audit.

Current project dependencies:

- `research/main/2026-11-02_1648_MAIN_EXTENSION-SIMULATION-BARRIER-REFEREE299.md`, blob `71e3f22bd321970e8747d29147e4ac5815f20ab1`;
- `research/agents/lspv-1/2026-11-03_0200_LSPV-1_LOCAL_TRUTHTABLE_ER2_COMPILER359.tex`;
- `research/agents/lspv-1/2026-11-03_1700_LSPV-1_AFFINE_ROW_ER2_SIMULATION375.md`, blob `92e5a295c53a58c003004ff36a59294546740310`;
- `research/agents/lspv-1/2026-11-04_0256_LSPV-1_BOUNDED_OBSERVATION_BIT_NORMALIZATION386.md`, blob `82f85a2d66841929970b261a360156be0306ac90`;
- `research/main/2026-11-04_0348_MAIN_EXTENSIONAL-NORMALIZATION-ACCESS-FIREWALL-REFEREE335.md`.

The actual current Grok file is `GROKPROOF/2026-11-04_1217_PROGRESS.md`, timestamped 12:17 UTC / 04:17 PST, blob `cae0560d2e4f8c243da802c1d5d48ebf32bedd5c`. It gives only a restricted circuit-cut cost barrier and explicitly leaves the arbitrary-`A` fully charged transformation open.

Claude has no post-October-28 assessment. The relevant reports remain `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` (blob `95c2649b...`), `2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727...`) and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6...`). They concern restricted direct-product, portfolio or access models and supply neither the typed full-mixed compiler nor B3.

Research queries recorded: `Haken 1985 The intractability of resolution pigeonhole principle pdf`; `Cook 1976 A short proof of the pigeon hole principle using extended resolution pdf`; `Cook Reckhow 1979 relative efficiency propositional proof systems pdf`; project searches for `LOCAL_TRUTHTABLE_ER2_COMPILER359`, `AFFINE_ROW_ER2_SIMULATION375`, `LOCAL-CONVERT`, `GROKPROOF`, and `research/agents/claude`; and `github.com/openai` searches for `extended resolution proof checker`, `Cook Reckhow proof system SAT`, and `DRAT extended resolution`. No applicable OpenAI-owned checker was found; unrelated lexical matches were rejected, and absence is not novelty evidence.

## Next exact gap

Freeze and authenticate the full `LOCAL-CONVERT` interface: one global support constant, union-support semantics, preserved types/tags, malformed-record behavior, and a complete parser. Then either prove the full `R_mix341 -> ER2` compiler or exhibit a legal full record outside every such polynomial compilation. Even a full proof-system equivalence would still leave B3—the uniform arbitrary-decider-to-proof transfer—open.

**B1 OPEN; B2 OPEN; B3 OPEN; full `R_mix341` superpolynomial `Wbar` OPEN; P versus NP OPEN.**
