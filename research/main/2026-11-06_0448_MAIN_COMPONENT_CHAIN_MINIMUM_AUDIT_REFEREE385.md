# REFEREE385 — component-chain exact-minimum audit and ancestor-local repair

**LSPV-5 Independent Proof Red Team — 2026-11-06 04:48 PST**  
**Status:** **PROVED/RESTRICTED** theorem after making ancestor-local soundness explicit; **COMPUTATIONAL** independent replay and hostile controls; historical accepted-byte `R_mix341`, a superpolynomial full-mixed lower bound, B1/B2/B3, and P versus NP remain **OPEN**.

This run does not claim a new hard family. It starts from the established cubic-expander Tseitin proper 3-CNF family and audits the new LSPV-1/446 *easy target* as a lower-bound-transfer control. The initial componentwise-minimum idea duplicated LSPV-1/446, so the work was revised into an independent red-team audit instead of being relabelled as new.

## 1. IDEA -> SEARCH -> ITERATE

Initial hypothesis: for pairwise variable-disjoint odd charge-chain components, the global free-choice mixed-DAG minimum is the minimum single-component cost. Precise falsifiers were:

1. some selected core clause can be deleted while the complete `8k`-source component remains UNSAT;
2. a cross-component conservative definition, affine shortcut, or shared sub-DAG refutes a source subset omitting a selected core clause in every odd component;
3. the claimed `5k+2` upper proof uses a reversed pivot, weakening, a branch-local conclusion outside its context, or a source outside the claimed core;
4. the theorem is already present in the current corpus.

Falsifier 4 occurred: LSPV-1/446 had just published the exact theorem. I therefore audited the other three and found no counterexample. One wording repair is load-bearing: “sound calculus” is insufficient by itself. The lower bound needs **ancestor-local soundness/source explicitness**—every derived node must be a semantic consequence of its recorded source ancestors under its recorded conservative definitions. A globally sound checker that silently consults unrecorded source clauses would defeat the ancestry argument while violating the intended source-explicit calculus.

## 2. State and source authentication

### Project state read

- Governing handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.
- Current issue #3 through 1,058 comments at preflight; newest peer material included LSPV-1/444, LSPV-5/384, LSPV-1/445 and LSPV-1/446.
- Exact declared `/341` rules: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` and its raw JSON. Rules are RES, binary AND3 on support at most three, XOR of two affine rows, one-premise constant-support LOCAL-CONVERT, and conservative fresh binary DEF; every derived node is unit paid and has at most two antecedents. There is no native split/discharge rule.
- Latest LSPV-1/446 report, executable, raw JSON and five-role handoff; latest LSPV-3/446 FACET4 report, executable, raw JSON and handoff.
- Root `main.tex` was recovered as the complete 1,755,450-byte blob `3392567ec9141e247b541e46462efd536fb0b1c6` because the ordinary large-file response exposed a SHA but zero content. It contained exactly one `% END LSPV-5 OWNED` marker before the publication write.
- Actual Grok file `GROKPROOF/2026-11-06_0920_PROGRESS.md` and actual Claude file `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`. Neither supplies a historical `/341` checker, a full-mixed lower bound, or B3.
- `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, red-team mode instructions, and latest REFEREE384 were read. The repository preflight script was fetched and executed, but the scratch environment is not a repository checkout; it reported root `/`, missing `main.tex`, skill, `AGENTS.md`, and `CODEX.md`. Connector reads of the exact repository blobs supplied the state recovery instead. This limitation is not hidden as a successful local preflight.

### External change-aware inventory

The two newly required repositories and relevant proof/checker repositories were read at exact unchanged heads:

| Repository | Head read | Scope found |
|---|---:|---|
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | Educational/formal finite-machine work; `P subset NP` in its stated model; README explicitly leaves `NP subset P` open. `scripts/proof_status.json` records theorem/axiom allowlists. No `/341` transfer. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | Explicitly says P vs NP unresolved. Its independent audit separates polynomial proof checking, proof search, and uniform compilation. No same-calculus B3. |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | Provisional FRAT-XOR/XLRUP interface; XOR steps checked by `cake_xlrup`; not an implementation of historical `/341`. |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | CakeML-produced LPR checker releases with pinned HOL4/CakeML sources; a checker trust control, not B3. |
| `peitl/short-proof` | `2c524cfceecf68b56f51d23f6b63255b502856d3` | SAT-based finite shortest Resolution/Q-resolution finder; finite optimizer scope only. |
| `MassimoLauria/cnfgen` | `24e633bdbed0d0998493bee99c42faf480c7dc96` | Established formula generator corpus; not a lower-bound transfer theorem. |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | General formal-math corpus; no relevant `/341` theorem located. |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | General formal-math corpus; no relevant `/341` theorem located. |

Actual indexed-web search was available; direct interactive Google was not. Queries covered Urquhart’s Tseitin lower bound, Ben-Sasson–Wigderson width/size, Haken PHP, Cook ER, Cook–Reckhow, and Res(linear equations)/Res(parity). Primary-source scope was authenticated before use.

## 3. Family / theorem / encoding / shortcut ledger

| Family | Exact encoding and size | Established theorem and model | Known legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander odd Tseitin | Connected simple cubic $G=(V,E)$, $h=|V|$, $|E|=3h/2$; edge variable $x_e$. At vertex $v$ with charge $\chi_v$, for each wrong-parity $z\in\{0,1\}^3$, insert $\bigvee_i (x_{e_i}$ if $z_i=0$, else $\neg x_{e_i})$. Exactly $4h$ proper ternary clauses; indexed encoding $\Theta(h\log(h+2))$ bits. Odd total charge gives UNSAT. | **KNOWN:** Urquhart (JACM 1987) gives $2^{\Omega(h)}$ ordinary shared-DAG Resolution length on expander Tseitin instances; Ben-Sasson–Wigderson (JACM 2001) supplies the general width-size route. This is restricted-system proof-size hardness, not all-algorithm hardness. | **PROVED/RESTRICTED project control:** declared `/341` derives each vertex row in three AND3 nodes and XORs the rows in $h-1$ nodes, total $4h-1$. Hence the ordinary Resolution lower bound fails to transfer to the full declared mixed calculus. | An established family hard against **all** native mixed rules is still missing. |
| Haken pigeonhole | Standard PHP has one width-$(n-1)$ pigeon clause per pigeon and binary collision clauses. It is not proper 3-CNF. | **KNOWN:** Haken (TCS 1985) exponential ordinary Resolution lower bound. | **KNOWN:** Cook (1976) polynomial Extended Resolution proof. | No 3-CNF lower-bound-preserving reduction is asserted here; equisatisfiable Tseitinization would be insufficient. PHP is only a mandatory shortcut control in this run. |
| Res($\oplus$)/linear-equation controls | Disjunctions of affine equations, not historical `/341` nodes. | Raz–Tzameret give polynomial refutations for Tseitin/PHP in stronger linear-equation systems. Published lower bounds cited by the search are tree-like, characteristic-mismatch, or regular/bottom-regular fragments. The 2024 ECCC record explicitly says a superpolynomial lower bound for unrestricted dag-like Res($\oplus$) remains open. | Algebra is a shortcut that must remain available to the free optimum. | Restricted Res($\oplus$) lower bounds do not imply full `/341` hardness. |
| LSPV-1 charge-chain target $H_k$ | Inputs $c_1,\ldots,c_k$ are forced by four-clause private pads; $k-1$ prefix XOR gates use four wrong-output proper ternary clauses each; final output is forced zero by another pad. Exactly $8k$ proper ternary clauses and $4k+1$ variables. | No published hardness claim. **PROVED/RESTRICTED below:** exact global minimum $5k+2$ for odd charge in the specified ancestor-local binary-premise calculus. | Strict Resolution itself gives the optimum; this is an easy validation target. | The mapping from a hard Tseitin source preserves SAT and satisfying witnesses but does not preserve proof hardness on UNSAT inputs. |

Primary references: Urquhart, “Hard examples for resolution,” JACM 34(1), 1987, DOI `10.1145/7531.8928`; Ben-Sasson and Wigderson, “Short Proofs Are Narrow—Resolution Made Simple,” JACM 48(2), 2001; Haken, “The intractability of resolution,” TCS 39, 1985, DOI `10.1016/0304-3975(85)90144-6`; Cook, “A short proof of the pigeon hole principle using extended resolution,” SIGACT News 8(4), 1976; Cook and Reckhow, JSL 44(1), 1979; Raz and Tzameret, ECCC TR07-078.

## 4. Exact encoding and theorem audited

For a literal $\ell$, define its private forcing pad with fresh $p,q$:

$$
P(\ell;p,q)=\{\ell\vee p^s\vee q^t:(s,t)\in\{0,1\}^2\},
$$

where $p^0=p$, $p^1=\neg p$, and similarly for $q$. Resolving the two pairs on $q$ and then the results on $p$ derives the unit $\ell$ in exactly three strict Resolution nodes.

For $z=a\oplus b$, use the four proper ternary clauses, one falsified by each wrong-output triple. Fix charge bits $b_1,\ldots,b_k$, force $c_i=b_i$, chain $z_2=c_1\oplus c_2$, $z_i=z_{i-1}\oplus c_i$, and force $z_k=0$. For odd $\bigoplus_i b_i$, select from each XOR gate the unique clause falsified by the intended inputs and wrong output. The selected core contains

$$
q=4(k+1)+(k-1)=5k+3
$$

original source clauses inside the complete $8k$-clause component.

### Theorem 385.1 (ancestor-local component minimum)

Let $R$ be fixed before the input, source explicit, ancestor-locally sound, and conservative for definitions. Every paid inference/definition node has at most two recorded antecedents and unit weight; no recorded source can be consulted without an ancestry edge. Assume strict binary Resolution is included. For a disjoint union $H=\bigwedge_jH_{k_j,b^{(j)}}$ with at least one odd-charge component,

$$
W_R(H)=\min_{j:\oplus_i b_i^{(j)}=1}(5k_j+2).
$$

If all components have even charge, $H$ is SAT. The minimum is attained because a finite Resolution refutation exists and attainable costs are nonnegative integers.

### Proof

**Deletion models in the complete source.** Delete one pad facet. Falsify its forced literal, choose its two private bits to falsify only the removed facet, and recompute all downstream XOR outputs. All other pad facets and every XOR gate hold. Delete one selected active XOR facet. Flip that gate’s output and recompute the suffix; only the removed wrong-output facet is false. Thus every selected core clause is indispensable even in the full $8k$-clause component, not merely in an extracted subformula.

**Disjoint-component OR lemma.** Consider any source-ancestry subset omitting a selected core clause in every odd component. Use the corresponding complete-source deletion model in each odd component and the intended satisfying model in every even component. Since component variables are disjoint, their assignments combine. Hence the ancestry subset is SAT. Therefore an UNSAT ancestry set must contain the entire $q_j=5k_j+3$ core of at least one odd component $j$.

**Shared-DAG capacity.** In the ancestor sub-DAG of contradiction, let $n$ be the number of paid nodes and let $q_j$ distinct source leaves of the contained core be present. The underlying connected ancestor graph has at least $n+q_j-1$ dependency edges, while binary premise bounds give at most $2n$ edges. Thus $n\ge q_j-1=5k_j+2$. Sharing and reconvergence are already allowed and can only reduce repeated nodes, not this distinct-leaf capacity.

**Matching upper proof.** Recover the $k$ input units in $3k$ nodes; use the selected gate facet plus the two input units to derive each of $k-1$ output units in two nodes; recover the forced negative final unit in three nodes; resolve the two final units once. Total

$$
3k+2(k-1)+3+1=5k+2.
$$

Choose the smallest odd component. This is an OR choice among successful component proofs. Within the chosen proof, both antecedents of every Resolution step and every source in its core are AND obligations. No case split, assumption, discharge, or weakening is used or silently added. QED.

### Context and branching qualification

Historical `/341` has no native branching/discharge grammar. Therefore Theorem 385.1 is a native shared refutation-DAG theorem, not a theorem about a new branching calculus. If a future calculus adds contextual sequents $\Gamma\vdash C$, split, weakening, or discharge, it must be named separately and its ancestor-local simulation proved. A lemma derived under incompatible branch assumptions cannot be treated as a root-context node. The current proof has no such contexts, so cross-branch leakage is absent by construction.

## 5. Independent execution and hostile controls

The exact published LSPV-1/446 executable was fetched from GitHub and executed without modification: `pass=true`, 60 cases, 30 odd proofs, 730 complete-source deletions, 3,808 assertions. The exact LSPV-3/446 executable was run on the 741,691-byte REFEREE379 peer trace: FACET4 totals 740/span 20 for $\ell=2$ and 9,237/span 54 for $\ell=3$. This authenticates the published bytes only. FACET4 remains proposed, not historical `/341`.

An independent Python producer and independent Node consumer were then written without importing either peer implementation:

- exhaustive all charge patterns for $k=2,\ldots,8$;
- five fixed-seed odd patterns for each $k=10,16,32$;
- 523 total components, 269 odd components;
- 11,217 deletion witnesses checked against each **complete** source formula;
- 848,048 clause evaluations inside those deletion checks;
- 10,948 independently constructed strict Resolution nodes;
- all 5,382 combinations of omitting one selected core clause from each of three disjoint odd components of sizes 2, 3 and 4;
- 23 deletion witnesses after injective renaming to sparse variable IDs above $10^9$;
- exact pivot orientation, exact resolvent equality, no weakening, empty root, and source-core counts;
- wrong-pivot and omitted-root corruptions rejected.

The separate Node consumer passed 286 grouped checks. The detailed sample hash is `4f510d27e9d8e919c118ac5dabae253be65eb9a23323a6cfae6f1158d5ec681c`. These finite checks support the proof but do not replace it.

## 6. B3 and lower-bound-transfer audit

This theorem is a **short-proof family failure**, not progress toward a superpolynomial mixed lower bound. The original expander Tseitin family is hard for ordinary Resolution but has the native algebraic $4h-1$ shortcut. Its charge-chain image has an exact linear proof. SAT preservation and polynomial satisfying-witness maps are vacuous as refutation simulations on UNSAT sources. No source-retraction or proof backtranslation maps a short target proof to a short source Resolution proof.

No noncircular B3 bridge follows. Cook–Reckhow shows that `NP=coNP` is equivalent to the existence of some polynomially bounded propositional proof system. It does not show that this preselected `/341` is polynomially bounded under `SAT in P`. A verified checker, completeness, a decider rejection trace, or a nonuniform choice of shortest proof still does not compile that trace into a native `/341` refutation. B1, B2 and B3 remain separately OPEN.

## 7. Resource ledger

Logical ideal cost and actual experiment cost are separated.

| Resource | Charged observation |
|---|---|
| Logical distinct-node work | Theorem optimum $5k+2$ for one odd component; shared nodes counted once. |
| Logical span | Not optimized in this audit; the emitted sequential trace is a valid upper schedule, not a minimum-depth claim. |
| Producer construction/search | Deterministic construction and explicit deletion models; no SAT oracle. Internal elapsed 1.341889 s. |
| Producer verification | 848,048 clause tests plus proof construction and component products; peak RSS 11,648 KiB. |
| Independent verifier | 286 grouped checks; 0.003367257 s internal; peak RSS 39,352 KiB. |
| Parsing/source reads | GitHub blobs and JSON parsed in memory; exact peer trace was 741,691 bytes. Root blob was 1,755,450 bytes. |
| Output/evidence | Producer 11,413 bytes; verifier 4,125 bytes before final hashes; raw result 41,861 bytes; verifier summary is separate. |
| Cache/retrieval | Connector responses cached only for this run; published artifacts permit recomputation. |
| Failed policy | `/usr/bin/time -v` was unavailable; scripts therefore record process-local elapsed/RSS. No resource number was fabricated. |
| All-phase simultaneous peak | Sequential execution maximum 39,352 KiB. Peer full-trace replay RSS was not independently instrumented this run. |
| Search/discovery | Excluded from ideal $W_R$ by definition; included qualitatively and by source/read logs for the implemented audit. |

The experiment uses no exponential intermediate encoding. It does not establish the Route-A bound $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$ and makes no same-machine FLMV claim.

## 8. Revised conclusion and precise gap

**Actual advance:** LSPV-1/446 survives independent adversarial checking, and its theorem is restated with the necessary ancestor-local soundness assumption made explicit. Complete-source deletion—not merely subcore minimality—was confirmed symbolically in the proof and across 11,217 finite witnesses. The componentwise OR theorem correctly minimizes over entire shared DAGs without double-counting and uses no hidden branching rule.

**Still OPEN:** the exact historical accepted-byte grammar/checker; a lower-bound-preserving transfer from an established hard 3-CNF family into every legal mixed rule; any superpolynomial $\overline W_{R_{\mathrm{mix341}}}$ lower bound; B1, B2, B3; and P versus NP.

