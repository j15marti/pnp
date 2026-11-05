# LSPV-3/414: Affine-hull quotient firewall and a fully native AND3/LOCAL/GF(2) unchanged-replay counterexample

**November 4, 2026, 23:28 PST.** PNP Hypergraph & Proof Certificates. **PROVED/EXACT:** (i) affine row equivalence on source models is equality modulo an explicit affine annihilator; (ii) testing membership in that annihilator is coNP-complete even for satisfiable source CNFs; (iii) a **legal six-node native** `R_mix341` proof prefix shows that replacing LOCAL public-root clauses by source-model-equivalent clauses invalidates downstream exact AND3/GF(2) typing. **COMPUTATIONAL:** two independent exhaustive implementations. **OPEN:** full native proof normalization, a counterexample to existence of *any* polynomial normalization, B1/B2/B3, superpolynomial mixed minimum and P versus NP. The native calculus and five task identities/schedules/states were not changed.

## IDEA, model and falsifiers (registered before SEARCH)

**Hypothesis.** Source-model equivalence of locally asserted clauses is insufficient to preserve the global exact GF(2) annotations of an AND3 factor, even if all old and replacement clauses are genuine paid LOCAL-CONVERT consequences, all original clauses are proper, no DEF/facet/export rule is used and the original source is SAT.

F1: The native input factors, LOCAL implications, AND3 support bound or GF(2) annotations fail a four-row check. F2: A source-model-equivalent *non-tautological* LOCAL root replacement preserves the old affine annotation after all. F3: The quotient obstruction disappears if one uses the affine hull of source models rather than all source models. F4: The construction accidentally presumes private-wire export, arbitrary DEF facet selection, a free semantic oracle or a changed calculus.

Fix the **literal original** `R_mix341` of `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` at blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, especially its lines 13--22: valid DIMACS CNF, free indexed source clauses, unit-cost non-source nodes of indegree at most 2; RES on clauses; AND3 exact truth-table conjunction on <=3 ORIGINAL variables with exact GF(2) annotation only when globally equivalent; XOR of two authenticated GF(2) rows; unary LOCAL-CONVERT only for a verified implication of a derived local factor/equation; a separate paid fresh two-input conservative DEF. No unpublished expansion or changed rule is assumed.

## SEARCH: complete source trail and limitations

Read first the original governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`; issue #3 through the LSPV-2/410 (23:12) update; `AGENTS.md` blob `19656af1`, `CODEX.md` blob `754999f5`, `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7`; original /341; grammar addendum `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` blob `bbcdad9a`; LSPV-1/411 `research/agents/lspv-1/2026-11-04_2300_LSPV-1_PUBLIC_PORT_CLAUSE_COMPILER411.md` blob `178ced24`; LSPV-2/410 `research/agents/lspv-2/2026-11-04_2312_LSPV-2_TWO_STAGE_BEHAVIORAL_FACET_COMPILER410.md` blob `19e272e0`; LSPV-3/413 blob `e3263f02`, LSPV-4/405 from issue #3, and LSPV-5 REFEREE355 `research/main/2026-11-04_2248_MAIN_LOCAL-PORT-SOUNDNESS-B3-TRACE-TYPE-FIREWALL-REFEREE355.md` blob `e5633677`. Earlier /413 already warned that model-conditional DEF aliases differ off-source; the **new point** is a counterexample wholly in the *native and non-tautological LOCAL/AND3/GF(2) fragment*, plus the exact affine annihilator classification and guarded complexity theorem.

Read actual `GROKPROOF/2026-11-05_0515_PROGRESS.md` blob `f348f7bb` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727` and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6`. Grok discusses a separate FLMV all-input transfer; Claude's portfolio/one-tape bounds concern restricted machine models. None resolves native grammar or B3.

Actual general-web queries: `Cook Reckhow 1979 relative efficiency propositional proof systems p-bounded proof systems NP coNP original full text`; `Extended resolution clause definition selectors DRAT LRAT gate extension variable defining clauses proof logs`; `Gocht Nordstrom certifying parity reasoning efficiently PB proofs extended resolution XOR definitions`; `Pich Santhanam 2023 199 self provability extended frege SAT polytime implication`; `Haken 1985 intractability resolution pigeonhole original full paper`; `Raz Tzameret 2008 resolution over linear equations multilinear proofs full paper PDF`. Read author-hosted Cook bibliography <https://www.cs.toronto.edu/~sacook/>, primary ECCC abstract <https://eccc.weizmann.ac.il/report/2023/199/>, primary AA AI bibliographic/abstract <https://ojs.aaai.org/index.php/AAAI/article/view/16494> (full publisher page blocked), and Weizmann publication record <https://weizmann.esploro.exlibrisgroup.com/esploro/outputs/journalArticle/Resolution-over-linear-equations-and-multilinear/993262684803596> (publisher full paper restricted). Direct Google-branded search was **not available**. These sources contextualize proof logging/reflection and supply no project-specific proof compiler.

Authenticated `github.com/openai` file-search queries: `ExecCNFNodeSearchCosts`, `CookLevin`, `LRAT proof checker`, `extended resolution proof checker`. Full sources inspected from `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f4` and `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean` blob `1e23a159`; they formalize execution costs and a Cook--Levin reduction, respectively, but **not** a same-`R_mix341` correctness/reflection compiler. LRAT search found no applicable result. No program/library is treated as a theorem.

## ITERATE I: exact native, proper-clause six-node discriminator

Use the **satisfiable** source, explicit 25-byte ASCII DIMACS:

```text
p cnf 2 3
1 0
-2 0
1 2 0
```

Write `x=x_1`, `y=x_2`, so `F=x ∧ ¬y ∧ (x∨y)`, whose **only** model is `(x,y)=(1,0)`. All source and LOCAL clauses below are proper and non-tautological. Inference DAG:

1. **AND3** from original clauses `(x)` and `(x∨y)`: exact factor `A=x`, with checked GF(2) row `x=1`.
2. **AND3** from original clauses `(x)` and `(¬y)`: exact factor `B=x∧¬y`, **without** an affine annotation.
3. **LOCAL-CONVERT** from `B`: clause `P=(x∨y)`. Check `B⇒P` on all four original valuations.
4. **LOCAL-CONVERT** from `B`: clause `Q=(x∨¬y)`. Check `B⇒Q`.
5. **AND3** from `P,Q`: exact factor `P∧Q=x`, which is annotated by the **globally exact** row `x=1`.
6. **XOR** the two authenticated rows of nodes 1 and 5 to get `0=0`. This node is a harmless, sound GF(2) consequence, not a refutation.

Now perform the proposed **source-model-only port normalization**: keep the source, parent `B`, and `P`, but replace `Q=(x∨¬y)` by `Q'=(¬y)`, another **legal paid LOCAL-CONVERT** of the SAME parent `B`. Both `Q,Q'` evaluate TRUE on every source model, and `B⇒Q'` holds on all four original assignments. Yet the downstream *exact* conjunction becomes

$$
P\land Q'=(x\lor y)\land\neg y=x\land\neg y,
$$

with truth table `(00,01,10,11)↦(0,0,1,0)`, compared with old `x` table `(0,0,1,1)`. No single GF(2) equation on `(x,y)` has exactly one satisfying valuation, whereas `x∧¬y` does. The old `x=1` annotation is **illegal** after replacement; in fact this new factor cannot be annotated by *any* exact affine row. The unchanged XOR consumer is therefore not a legal native replay. **No DEF or private-circuit-wire premise appears anywhere.**

**Counterexample classification:** a legal old native proof prefix and a legal replacement LOCAL inference whose **old downstream annotations cannot be copied unchanged**. This defeats the claim that source-model equality of public LOCAL assertions suffices for all-consumer proof-DAG normalization. It does **not** prove no different polynomial source-authenticated compiler exists; e.g., retaining the old `Q` and original row is a constant-cost repair here. It is neither a hard-family result nor a refutation of B1/B2/B3.

## ITERATE II: the exact intrinsic affine-hull obstruction

Let `M(F)={a∈GF(2)^n:F(a)=1}` and define the homogeneous source-affine annihilator

$$
H_F=\{(u,c)\in GF(2)^{n+1}:\;u\cdot a\oplus c=0\text{ for every }a\in M(F)\}.
$$

For any two **affine** functions `f(a)=u·a⊕c` and `g(a)=v·a⊕d`,

$$
f|_{M(F)}=g|_{M(F)}\quad\Longleftrightarrow\quad
(u\oplus v,c\oplus d)\in H_F.
$$

This is immediate by subtraction over GF(2). Thus source-model semantics determines an affine signature only as a **coset modulo `H_F`**, rather than as an absolute GF(2) row. If `M(F)` is nonempty and its affine hull has dimension `d`, then `dim H_F=n-d`: fix a model `a_0`, require `u` orthogonal to all differences `a⊕a_0`, and set `c=u·a_0`. For UNSAT `M(F)=∅`, all rows qualify vacuously and `dim H_F=n+1`. Hence a quotient by source models **cannot generally transport globally exact affine normal forms**. The boolean quotient itself remains a congruence for Boolean operations; the failure is specifically the *extra global-exact row annotation*, not ordinary conjunction.

**Further proved complexity barrier (SAT-promise):** For a valid CNF `F` promised satisfiable and an affine row `(u,c)`, deciding `(u,c)∈H_F` is **coNP-complete**. Membership is in coNP because a model falsifying the row is an NP witness. To reduce arbitrary CNF UNSAT for `G(x)`, introduce fresh `s` and

$$
F_G(s,x)=\bigwedge_{C\in G}(s\lor C).
$$

`F_G` is always SAT by setting `s=1`, but `F_G\models(s=1)` iff `G` is UNSAT. Therefore the row `s\oplus1=0` is in `H_{F_G}` exactly for UNSAT `G`. The reduction preserves polynomial explicit DIMACS bit length and needs no SAT-label axiom. This is classical-style entailment hardness proved here for the specific candidate invariant, **not** an unconditional runtime lower bound or evidence that P≠NP.

## ITERATE III: independent hostile verification

`verify_native.py`: **67,423 actual Python assertions PASS**, independently enumerating both native witnesses and 16/256 arbitrary 2-/3-input source-model sets, 1,024/65,536 ordered affine-function pairs, affine-hull dimension/homogeneous-kernel agreement, 256 guarded-CNF reductions, 25-byte strict source model, opposite-label and malformed controls. `verify_independent.mjs`: **67,414 independently coded JavaScript assertions PASS**; its affine span is computed by XOR-closure rather than the Python elimination algorithm. Source table ordering differs between languages but labelled valuations agree. Corrupted or retyped old GF(2) rows are rejected, as is the absence of a legal affine label for the changed conjunction. Both checks use exact finite evaluation and claim no asymptotic hardness by extrapolation.

Sha256 (local sandbox reproducibility files): Python source `4bc570497de2ffe0757766bc00dfa37f6808f9960636a7fe81c887da05a5750d`; JavaScript source `17bf10714c744d6127ecfcda4a33473ed45c85bca6ae3c76bf710f3360c15334`; Python raw `d91b0b10f2be23810b6b2956e1b7f831f15992e8a6f6cdc90468f696fc09cf4b`; JavaScript raw `609a10a31868caa6f173a739fa34c3149725690f05467b130fc305bb872bd458`.

**Charged accounting:** original trace `q=6` unit-cost nodes, three original free clauses, all supports <=2, no DEF, one GF(2) sum. This is a **constructed upper trace**, not a certified minimum. With 25 ASCII input bytes and six constant-width records, flat explicit proof evidence is O(1) for this fixed witness. General stored gate/table/parent IDs require bit-level encoding, read access, updates, output, proof replay and all-phase peak memory; `q` does not equate to time or space. Exhaustive model sets are **offline diagnostics**, not a free legal rule or proof-search certificate. No FLMV resource claim is made.

## B3 audit and next obligation

For any uniform total polytime SAT decider `A`, `A(F∧¬r)` could decide `r∈H_F` in polynomial time under `SAT∈P`. That **does not** produce a native authenticated row or a proof that the decider correctly answers every source formula. Merely computing semantic information does not close

$$
\mathrm{SAT}\in P\;\Longrightarrow\;\overline W_{R_{\rm mix341}}(N)\in N^{O(1)}.
$$

**Next:** preserve globally exact GF(2) signatures through all LOCAL/AND3 replacements, or attach explicit source-derived row-change certificates whose legitimacy is proved under the **unchanged** original /341 grammar; independently settle DEF facet and exported-wire selectors. Separately pursue a noncircular same-fixed-R B3 reflection/translation argument. Haken's `2^{Ω(h)}` lower bound on ordinary DAG Resolution pigeonhole CNFs (standard explicit signed-index size `Θ(h^3 log h)` bits), Cook's polynomial Extended Resolution PHP proof, and short XOR Tseitin refutations are countercontrols, not unrestricted computation lower bounds.

**STATUS:** native source-model-only unchanged-replay mechanism **FALSIFIED** by a legal typed trace; affine-hull characterization and SAT-promised coNP-completeness **PROVED/EXACT**; full native normalization, noncircular B3, full mixed superpolynomial minimum and P versus NP **OPEN**. No main.tex or task state is claimed changed here.

## References

[1] Cook SA, Reckhow RA (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1):36--50. Author bibliography <https://www.cs.toronto.edu/~sacook/>.

[2] Haken A (1985), *The Intractability of Resolution*, TCS 39:297--308. Ordinary Resolution only.

[3] Cook SA (1976), *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4):28--32.

[4] Raz R, Tzameret I (2008), *Resolution over Linear Equations and Multilinear Proofs*, APAL 155:194--224. <https://doi.org/10.1016/j.apal.2008.04.001>.

[5] Gocht S, Nordström J (2021), *Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs*, AAAI 35(5):3768--3777. <https://doi.org/10.1609/aaai.v35i5.16494>.

[6] Pich J, Santhanam R (2023), *Towards P != NP from Extended Frege Lower Bounds*, ECCC TR23-199 <https://eccc.weizmann.ac.il/report/2023/199/>. Self-provability is a separate assumption, not a free B3 argument.
