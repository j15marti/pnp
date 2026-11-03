# REFLECTION-FAMILY-EQUIVALENCE-REFEREE318

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 10:48 PST**

**Status:** KNOWN published Resolution lower bound first; PROVED an abstract reflection-family equivalence and independently rederived the earlier LSPV-1 353 localization; PROVED/RESTRICTED its exact strict-Resolution specialization; FALSIFIED the claim that semantic correctness or an UNSAT reflection encoding itself supplies the missing short proofs; COMPUTATIONAL both-label, malformed and XOR controls. `Rmix341` restriction stability, short `Rmix341` reflection proofs, B1, B2, B3, a superpolynomial `Wbar_Rmix341`, and P versus NP remain OPEN. No task, schedule, enabled state, ownership, calculus, encoding, rule or weight was changed.

## Established lower bound and its exact restrictions

Start with the classical Urquhart / Ben-Sasson--Wigderson consequence for Tseitin contradictions. There are constants `alpha,c>0` and an infinite family of bounded-degree (take cubic) `alpha`-edge expanders `G_h` such that, for every sufficiently large admissible `h`, the odd-charge Tseitin contradiction encoded as an ordinary width-three CNF requires at least `2^(c h)` lines in every unrestricted DAG Resolution refutation.

The encoding has one variable per edge, hence `3h/2` variables, and four proper width-three clauses per cubic vertex, hence `4h` clauses. With explicit binary variable identifiers its encoded length is `N_h=Theta(h log h)`. The theorem is therefore

`W_Res(Ts(G_h,chi_h)) >= 2^(Omega(h)) = 2^(Omega(N_h/log N_h))`.

Its model is ordinary syntactic Resolution: original CNF clauses plus binary resolution, DAG sharing allowed, lines counted once. It is not an arbitrary SAT machine lower bound, not Extended Resolution hardness, and not an all-rule `Rmix341` lower bound.

The mandatory countercontrol is decisive. The same source exposes a linear GF(2) contradiction. In the fixed mixed calculus, the previously verified extraction-and-XOR DAG has cost `4h-1` for bridgeless cubic odd Tseitin. The current LSPV-3 fiber lift likewise retains exponential Resolution hardness while having exact mixed cost linear in the source clauses. Therefore this established hard family cannot itself witness superpolynomial `Wbar_Rmix341`; it is useful here only to test the missing transfer.

## Exact reflection-family equivalence

Fix a proof calculus `R` and nonnegative inference-node cost. For each `N`, suppose a CNF `H_N` satisfies:

1. `H_N` is UNSAT and `|H_N| <= q(N)` for one polynomial `q`;
2. for every valid UNSAT CNF `F` of encoded length at most `N`, there is a syntactic partial assignment `rho_F` such that simplification leaves **exactly** `F`, with no remaining auxiliary contradiction: `H_N|rho_F = F`;
3. every `R` refutation of `H_N` restricts and normalizes to an `R` refutation of `F` without increasing inference cost. A fixed polynomial cost blow-up gives the corresponding polynomial version.

Then

`Wbar_R(N) <= W_R(H_N)`.

Proof: take a minimum `R` refutation of `H_N`, restrict it by `rho_F`, and use condition 3. This gives `W_R(F)<=W_R(H_N)` for every relevant `F`; maximize over `F`.

Conversely, if `Wbar_R(M)<=p(M)` for every `M`, then

`W_R(H_N) <= Wbar_R(|H_N|) <= p(q(N))`.

Thus, for a polynomial-size, witness-transparent, restriction-stable reflection family, polynomial `R` proofs of the single family `{H_N}` are equivalent up to polynomial encoding rescaling to polynomial `Wbar_R`. Under `SAT in P`, this is an exact localization of B3. It does **not** prove B3: the statement that `{H_N}` has short `R` proofs is essentially the missing conclusion repackaged as one family.

This theorem is not claimed novel. It independently reconstructs the conditional one-family localization already stated in `research/agents/lspv-1/2026-11-02_2100_LSPV-1_UNIVERSAL_REFLECTION_SINGLE_FAMILY353.tex` at blob `946ff874ac8eeeb4af3e5dbe50ad7726d2a87498`. The current increment is the red-team separation of its two nonautomatic premises, an exact finite restricted-proof control, and reconciliation with the newer clock-coverage objection.

## Why decider correctness does not close the equivalence

For a fixed total correct P-time decider `A`, the decider-induced Cook--Reckhow system `D_A` from REFEREE317 has linear certificates. B3 asks whether the same preselected `Rmix341` length-simulates that system. A reflection CNF can combine all length-`N` rejection-soundness instances, but:

- external correctness of `A` proves only that `H_{A,N}` is semantically UNSAT;
- a rejecting trace proves only what `A` computed, not that the answer is correct;
- neither fact bounds `W_R(H_{A,N})`;
- assuming polynomial `W_R(H_{A,N})` plus exact restriction transport is, by the theorem above, already equivalent to the desired worst-case polynomial minimum.

The exact generic shortcut is false. REFEREE317's fixed truth-table proof system is sound, complete and effectively checkable yet requires one paid record for every assignment. Universal reflection formulas with linearly many witness/selector variables therefore still have exponentially long proofs in that grammar. More abstractly, a proof system can be padded without losing soundness, completeness or effective verification. These are transfer countercontrols, not claims about `Rmix341`.

## LSPV-1 reflection theorem and LSPV-4 clock objection

Current LSPV-1 `RESTRICTION-STABLE-REFLECTION367` constructs a declared witness-transparent selector/tableau CNF and uses the standard fact that strict Resolution restrictions do not increase length. When the selected formula is actually rejected within the honest clock and all deterministic trace bits are fixed, its residual is claimed to be the original source. Under those explicit conditions, the Resolution inheritance theorem is correct and gives hard reflection formulas from established Resolution-hard sources.

Current LSPV-4 `CLOCK-COVERAGE-REFLECTION366` supplies the material objection that must not be dropped: a naive `reject-by-b` clock filter can leave an auxiliary contradiction rather than an authenticated source proof. At clock 5 in its finite control, an UNSAT formula rejected only at step 6 produces a spurious empty residual; at the honest clock, exact source recovery succeeds. Therefore “clocked reflection” does not imply condition 2 above. The clock must cover every relevant all-input run, and the specialization must be checked after fixing all selector and deterministic tableau wires.

There is no conflict: LSPV-1 proves a restricted theorem for a declared transparent construction; LSPV-4 proves that transparency and honest coverage are substantive premises, not consequences of semantic correctness.

## Rule-by-rule status for the same fixed `Rmix341`

| Rule family | Restriction status | Obstruction |
|---|---|---|
| Strict RES | **PROVED** | Delete satisfied clauses/literals and suppress redundant nodes; length does not increase. |
| GF2 | **PLAUSIBLE/UNPROVED for exact grammar** | Substitution preserves an affine equation, but constants, zero rows, duplicate rows and charged normalization must be legal. |
| AND3 extraction | **OPEN** | A restricted four-clause source block can shrink or disappear; the extracted parity record may no longer have the required authenticated source shape. |
| Signed VARDEF / ER2 | **OPEN globally** | A fixed input can turn a two-input definition into a unit, constant or alias; exact retyping and costs are not yet specified for every case. |
| LOCAL-CONVERT | **OPEN** | The payload language and validation semantics remain insufficiently fixed to prove grammar-preserving restriction. |
| Shared DAG scheduling | **Logically separate** | Logical restriction may lower node count; materialization, lookup, normalization and recomputation remain charged machine work. |

Consequently, strict Resolution reflection hardness does not transfer to `Rmix341`, and full mixed restriction closure cannot be assumed from the Resolution proposition.

## Four falsifiers

1. **A polynomial-time correct decider makes its reflection family easy for the preselected calculus.** **FALSIFIED as a generic lemma:** correctness makes the formula UNSAT but supplies no proof-length bound; padded/truth-table systems are exact countercontrols.
2. **One universal reflection family is a strictly weaker problem than B3.** **FALSIFIED under the stated transparency and restriction hypotheses:** polynomial proofs for that family are equivalent to polynomial `Wbar_R` up to encoding rescaling.
3. **Any clocked rejecting tableau specializes to the selected source.** **FALSIFIED by LSPV-4's clock-5 control:** an auxiliary clock contradiction can survive and counterfeit source refutation.
4. **Strict Resolution restriction closure proves mixed restriction closure.** **FALSIFIED as an inference:** AND3, VARDEF, GF2 normalization and especially LOCAL-CONVERT require separate typed proofs.

## Independent exact controls

The finite catalog has one 3-variable UNSAT formula `U8`, the conjunction of all eight full clauses, and eight SAT neighbors `S_i` obtained by deleting one clause. Exact enumeration gives zero models for `U8` and exactly one model for every `S_i`.

A reflection CNF chooses exactly one catalog formula. A SAT label forbids its selector; an UNSAT label gates the selected original clauses. With the correct labels the 53-clause reflection CNF has zero models. Changing only the `S0` label to UNSAT produces a 59-clause CNF with exactly one model, selecting `S0` and its unique source assignment. Thus one false rejection makes the reflection formula SAT; a trace does not certify correctness.

For the correct CNF, fixing the selector to `U8` leaves exactly the eight original clauses. A 16-inference explicit Resolution refutation of the reflection CNF contains a seven-node gated refutation of `U8`; restriction yields exactly those seven nodes and the empty clause. This verifies the cost direction `W_Res(U8)<=W_Res(H)` on a complete encoded example without claiming either global minimum.

The producer rejected 11 missing/false/malformed transfer schemas and four malformed label arrays. The independent no-import Node verifier rebuilt the formulas, both labels, proof nodes and all classifications with 46 assertions. Mandatory XOR controls returned zero odd-charge K4 models and eight even-charge models.

Raw SHA-256: `035a54d0be7f5813ee4bebb75b9c85749ca64ce11d2af24f92847f4910ce36be`.

## B1/B2/B3 classification

| Obligation | Status | Exact reason |
|---|---|---|
| Strict-Resolution reflection inheritance | **PROVED/RESTRICTED** | Standard nonincreasing restriction plus exact source specialization. |
| One-family equivalence | **PROVED/CONDITIONAL** | Requires polynomial-size UNSAT `H_N`, universal exact coverage and cost-stable restriction. |
| `Rmix341` restriction stability | **OPEN** | Several charged rules lack a complete typed normalization proof. |
| Short `Rmix341` proofs of reflection family | **OPEN and equivalent to target under the premises** | Correctness proves UNSAT, not shortness. |
| B1 pointwise | **OPEN** | No arbitrary-decider computation-to-proof producer. |
| B2 worst-case | **OPEN** | No arbitrary-decider worst-case domination. |
| B3 weakest bridge | **OPEN** | Neither reflection shortness nor a different length simulation into the same fixed calculus is proved. |
| Superpolynomial `Wbar_Rmix341` | **OPEN** | Tseitin has a linear XOR escape. |

No simulation inequality is reversed. A family-specific fast recognizer plus exhaustive fallback is not an all-input polynomial SAT decider and cannot establish B3.

## Grok, Claude and peer assessment

The repository directories were located rather than guessed: `GROKPROOF/`, `research/agents/grok/`, and `research/agents/claude/`. Exact current files reviewed were:

| Path | Blob SHA | Independent assessment |
|---|---|---|
| `GROKPROOF/2026-11-03_1217_PROGRESS.md` | `acf9fbee7079af567db4847ce628c49da45c25b1` | Its query lemma lower-bounds each solver call using only an upper time bound `T_A(M)<=M^K`; that direction is invalid without a matching lower bound. No B3 simulation results. |
| `GROKPROOF/2026-11-03_1518_PROGRESS.md` | `234fc189b01fa163eb10e128556e9d22e085b755` | Explicitly leaves the all-input charged transformation OPEN. |
| `GROKPROOF/2026-11-02_2045_ATTEMPT_ARC_CONSTRUCTION.md` | `130939f5d75a6b31a54f45455e7c271051fcbdc4` | Correctly records failure of naive self-reduction, block enumeration and affine elimination to give the required general contraction. |
| `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex` | `d06a2d56befc775660c34a59067b61f0a8c142a8` | Circuit rewriting experiments and finite optima; it explicitly says no lower bound moved. |
| `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` | `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9` | Restricted alternation-trading portfolio calculus, not reflection shortness or B3. |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` | `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a` | Sequential-access lower bound; explicitly does not transfer to random-access ARC/FLMV or `Rmix341`. |
| `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` | `79e4d4e7e0e3edff3aba8610852c45534bdde128` | Correctly classifies the decisive general lower-bound arrows as open/conditional. |
| `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` | `694c1c8169d9a193397b94e6ee572c476e639a94` | Useful arithmetic/citation audit, but its claim that algebraic immunity one characterizes affine functions is false: `xy` has the linear annihilator `1+x`. No B3 bridge. |

Current peer versions checked: LSPV-1 `RESTRICTION_STABLE_REFLECTION367` at blob `64f4e87aa7c6050d088bb599ec4919aa119ba10e`; LSPV-2 `INLINE_CONE_TRANSFER367` at `ff7fa6df98d45ce62ba2a3f852cdbfcbe8ae59c7`; LSPV-3 `CYCLIC_CHARGE_FIBER_LIFT370` at `400eea022ce1c87353f2a93aa8bb7b80f2428421`; and LSPV-4 `CLOCK_COVERAGE_REFLECTION366` at `c26462292854f13d5d17e41653d70e28ae0a9736`. The first and fourth directly inform the transparency audit; the middle two preserve scoped compilers or demonstrate XOR escape, not B3.

## Literature and GitHub searches

Queries covered Tseitin Resolution lower bounds, restrictions of Resolution proofs, reflection principles, optimal proof systems, Pich--Santhanam witnessing formulas, project reflection/B3 files and `github.com/openai` implementations.

- A. Urquhart, [Hard Examples for Resolution](https://doi.org/10.1145/7531.8928), JACM 34 (1987), supplies expander/Tseitin Resolution hardness.
- E. Ben-Sasson and A. Wigderson, [Short Proofs Are Narrow--Resolution Made Simple](https://doi.org/10.1145/375827.375835), JACM 48 (2001), supplies the width-size route to exponential Resolution bounds.
- P. Pudlak, [Reflection Principles, Propositional Proof Systems, and Theories](https://arxiv.org/abs/2007.14835), surveys precisely the distinction between semantic reflection and short proofs.
- J. Krajicek and P. Pudlak, [Propositional Proof Systems, the Consistency of First Order Theories and the Complexity of Computations](https://doi.org/10.2307/2274765), distinguishes length simulation from effective p-simulation and connects reflection/consistency families to optimal systems.
- J. Pich and R. Santhanam, [Towards P != NP from Extended Frege Lower Bounds](https://eccc.weizmann.ac.il/report/2023/199/), requires explicit witnessing/self-provability conditions; it does not give the present B3 transfer for free.

Project search found the earlier LSPV-1 353 one-family equivalence and the four current peers above. Scoped `github.com/openai` searches found no applicable reflection-to-`Rmix341` theorem or implementation. Search absence is not novelty evidence.

## Work and all-phase space ledger

| Phase | Measured record |
|---|---:|
| Python producer wall time | 0.041167267 s |
| Python producer peak host RSS | 10,368 KiB |
| Node verifier wall time | 0.012788653 s |
| Node verifier peak host RSS | 45,236 KiB |
| Full assignments checked | 8,392 |
| Resolution nodes checked across original/restricted proofs | 14 |
| Malformed controls rejected | 15 |
| Producer source bytes | 12,744 |
| Verifier source bytes | 4,855 |
| Raw JSON bytes | 3,674 |

These host measurements are not FLMV writable-space bounds. Formula generation, parsing, selector constraints, both-label enumeration, clause specialization, proof checking, malformed rejection, XOR enumeration, serialization and independent replay were charged. The logical proof minimum still grants free after-the-fact choice. The all-phase memory envelope remains `s'<=max{rho,eta,lambda,lambda*s}`; a materialized reflection tableau may itself force parent-scale `rho`. XOR state differences are offline diagnostics and were not used as a free oracle.

## Artifacts and next exact gap

- Producer: `experiments/arc/lspv5_318/reflection_equivalence_referee318.py`
- Independent verifier: `experiments/arc/lspv5_318/verify_reflection_equivalence_referee318.js`
- Raw ledger: `results/raw/arc/lspv5_318/reflection_equivalence_referee318.json`
- Five-role handoff: `research/coordination/2026-11-03_1048_LSPV5_TO_FIVE_ROLE_REFLECTION-FAMILY-EQUIVALENCE-REFEREE318.md`

The next weakest noncircular transfer is now exact: either prove polynomial `Rmix341` length domination of the decider-induced Cook--Reckhow system by some route other than assuming short reflection proofs, or first prove a complete typed restriction theorem for every fixed mixed rule and then prove short proofs for a witness-transparent reflection family. The second formulation is a localization of B3, not progress unless its shortness premise is independently derived from `SAT in P`.

**P versus NP remains OPEN.**
