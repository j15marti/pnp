# LSPV-5 REFEREE368: branch extension freshness is a soundness boundary

**November 5, 2026, 11:48 PST. Route B primary.** **PROVED/EXPLICIT for a declared comparison grammar:** branch-local extension-variable freshness is unsound; a seven-inference, two-branch certificate accepted by that flawed checker refutes the empty CNF on two declared variables, which actually has four models. **PROVED/RESTRICTED repair:** if every definition output is globally fresh from the original source universe, all active assumptions and every earlier definition, and every native mixed rule already has a polynomial local Extended-Frege simulation, then context-typed branching adds at most polynomial proof power. Each guarded node is translated once, so shared DAGs are not unfolded. **OPEN:** whether the exact historical `R_mix341` bytes enforce all required conditions, whether arbitrary auxiliary-variable splits are native, any superpolynomial lower bound for the complete mixed calculus, B1/B2/B3, and P versus NP. No historical rule or weight is changed.

## IDEA fixed before SEARCH

**Initial hypothesis.** A source-authenticated context-typed branching wrapper around the proposed globally fresh CANON2R grammar should be polynomially equivalent to unbranched CANON2R/Extended Frege if every branch-local mixed object is guarded by its assumptions.

**Falsifiers fixed in advance.** (F1) a branch-local `DEF`, `LOCAL-CONVERT`, `AND3`, or `GF2` object survives discharge without its guard; (F2) preserving shared reconvergent subproofs forces exponential duplication; (F3) explicit contexts/export IDs require superpolynomial evidence relative to source plus nodes; (F4) a split on an auxiliary variable requires a semantic oracle or an unavailable native owner. Prediction: a nodewise guarded translation works under global freshness, but fails if a context variable may also become a definition output.

## SEARCH: the initial claim required a repair

The governing five-role handoff, current issue #3, REFEREE365--367, LSPV-1/423, LSPV-3/427--428, current Grok and Claude artifacts, and the unchanged historical `/341` evidence were reviewed. LSPV-1/423's balanced odd-Tseitin mixed trace has exact work $4h-1$ and ideal span $\lceil\log_2(4h)\rceil$ in the declared semantic fragment, but the historical selector serialization remains open. LSPV-3/428 shows that a branch-only proof of maximum context size $d$ and local clause width $w$ yields a Resolution proof of width at most $d+w$; this still does not cover extension or affine rules. `GROKPROOF/2026-11-05_1913_PROGRESS.md` supplies no historical Rmix compiler or B3. `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` correctly warns that an open lemma already implying a separation is not a bridge.

Actual literature queries included `extended Frege deduction theorem polynomial proof case split proof complexity`, `Frege systems polynomial deduction theorem assumptions`, `Krajicek proof complexity extended Frege deduction theorem branching`, and `Cook Reckhow extended Frege p-equivalent case analysis`. Direct Google-branded access was unavailable; indexed web search and authenticated GitHub search were used, and Google is not claimed.

The decisive primary source is Olaf Beyersdorff, *The Deduction Theorem for Strong Propositional Proof Systems* (FSTTCS 2007; Theory of Computing Systems 2010; earlier ECCC TR06-142). It records four facts needed here:

1. Classical deduction is known for Frege, but unrestricted EF and SF do not satisfy it because extension/substitution rules are not sound under arbitrary extra premises.
2. The extension axiom $q\leftrightarrow\varphi$ is not itself a tautology. The output $q$ must be new and absent from the final theorem.
3. Minimal counterexample: from the extra premise $p$, unrestricted `EF ∪ {p}` may introduce $p\leftrightarrow q$ using the premise variable $p$ as the extension output, then derive $q$; yet $p\to q$ is not a tautology.
4. The restricted system $EF^{-}$ forbids extension variables occurring in the extra premises. Beyersdorff's Theorem 3 proves the classical deduction property for $(EF+\Psi)^{-}$, with polynomial overhead. Its proof explicitly depends on the extension output not occurring in the extra premises.

Bonet--Buss, *The Deduction Rule and Linear and Near-Linear Proof Simulations*, JSL 58(2), 1993, proves polynomial, often near-linear, simulations of several deduction-Frege systems by Frege. This supports the branch-only side, not unrestricted EF under premises. Beyersdorff further shows that broad weak/efficient deduction properties for strong proof systems have consequences as strong as optimality or polynomial boundedness; they cannot be assumed as a routine B3 lemma.

Required repository review was change-aware. Heads were unchanged: `konard/p-vs-np` at `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `blkph0x/p-vs-np-proof-research` at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `meelgroup/frat-xor` at `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `openai/math` at `4eaee87548250b2682affda7d05d947c05554bae`; and `peitl/short-proof` at `2c524cfceecf68b56f51d23f6b63255b502856d3`. Targeted code searches for `deduction theorem extension variable`, `fresh variable extension`, and `assumption branch` found no Rmix branch-discharge theorem in either new required repository, FRAT-XOR, short-proof, or OpenAI Math. The one `konard` hit was an archived external P-vs-NP attempt, not an EF deduction theorem. FRAT-XOR's typed CNF/XOR provenance remains a format precedent only. OpenAI Math's unrelated uses of “deduction” do not formalize this proof-complexity claim.

## Established family/theorem/encoding/method ledger

No new hard family was invented. The run retains the established exact 3-CNF cubic-expander odd-Tseitin family from REFEREE367. For connected cubic $G=(V,E)$ and odd total charge $\chi$, use one variable $x_e$ per edge and, at every vertex, the four width-three clauses excluding assignments of the wrong parity. Thus $h=|V|$ gives $3h/2$ variables, exactly $4h$ clauses, and explicit binary DIMACS length $N=\Theta(h\log h)$.

| Family / theorem | Exact model and bound | Known legal method | Remaining transfer |
|---|---|---|---|
| Urquhart / Ben-Sasson--Wigderson cubic-expander odd Tseitin | Every ordinary shared-DAG Resolution refutation has $2^{\Omega(h)}$ lines for a suitable expander family. Source, Resolution and inessential weakening only; no extension or GF(2). | Typed branching collapses to Resolution exactly (REFEREE367). Width obeys $d+w\ge w_{Res}(F)$ (LSPV-3/428). | Does not survive full mixed rules: AND3/GF(2) gives exact $4h-1$ work. |
| Haken unary PHP | Exponential ordinary shared-DAG Resolution size in the stated PHP CNF encoding. Standard PHP is not exact 3-CNF. | Cook gives polynomial Extended-Resolution PHP proofs. | An equisatisfiable 3-CNF conversion alone does not transfer Haken's lower bound; the direction and overhead must be proved. |
| Tseitin in linear-equation systems | Polynomial proofs in stronger algebraic systems; lower bounds in `Res(\oplus)` literature are only for the expressly stated restricted variants. | Gaussian elimination / affine row addition; shared rows and balanced reductions. | A restricted algebraic lower bound is not arbitrary-machine or full-Rmix hardness. |

The strongest shortcut is part of the true minimum. It cannot be excluded to preserve a hardness claim. The new result instead identifies a soundness condition any branching-plus-extension shortcut must satisfy.

## Declared unsafe wrapper and seven-node false refutation

This comparison grammar uses judgements $\Gamma\vdash C$, free source references, and unit-paid `ASSUME`, selected semantic `DEF` facet, exact oriented `RES`, and exact complementary two-premise `MERGE`. `MERGE` is an AND obligation; both $\Gamma,p\vdash C$ and $\Gamma,\neg p\vdash C$ are required. The flawed freshness rule says only that an output is fresh *within the current branch context*. It neither reserves the source variable universe nor prevents incompatible branches from giving one identifier different definitions.

Take the strict source bytes

```text
p cnf 2 0
```

This formula has four models. The accepted dependency DAG is:

| Node | Context | Rule / conclusion |
|---:|---|---|
| 0 | $p$ | `ASSUME` $p$ |
| 1 | $p$ | branch-local `DEF` reuses output $p$ and defines $p\leftrightarrow0$, emitting facet $\neg p$ |
| 2 | $p$ | resolve nodes 0,1 to $\bot$ |
| 3 | $\neg p$ | `ASSUME` $\neg p$ |
| 4 | $\neg p$ | branch-local `DEF` reuses output $p$ and defines $p\leftrightarrow1$, emitting facet $p$ |
| 5 | $\neg p$ | resolve nodes 4,3 to $\bot$ |
| 6 | empty | `MERGE` both complementary contradictions to $\bot$ |

Every local facet is semantically valid *for its newly imposed relation*, both branch contradictions are present, contexts are exact, and the dependency graph is acyclic. The failure is conservativity: the alleged definition output is the split/source variable. Each branch changes the problem rather than abbreviating a formula. This is the two-branch refutation form of Beyersdorff's one-premise $EF\cup\{p\}$ counterexample.

The trace is 513 canonical bytes / 4,104 evidence bits, SHA-256 `49eeb8f9a083b7a86393fd76d419cc34e95a5f10ac9c266633d91f48b4896580`. It has seven paid nodes and unit-weight critical path three under an ideal parallel model. The declared unsafe checker accepts it; exhaustive evaluation independently finds four source models. Therefore any proposed branch/CANON/Rmix checker with only branch-local output freshness is unsound.

**Scope warning.** This is not claimed to be legal under authenticated historical `R_mix341`. It is an explicit legal counterexample to the precisely stated *branch-local-freshness wrapper*. Historical legality remains unresolved until the old byte grammar proves freshness against the external source universe, assumptions and all definition owners.

## Restricted repair and polynomial guarded translation

Define the repaired comparison wrapper `B-CANON2R^-` by adding assumptions/merge to CANON2R subject to all of the following:

1. every definition output is globally fresh: it occurs in no original source identifier, active or discharged context, input port, earlier line, or earlier definition owner;
2. branch split variables are original variables, or are owned by an unconditional earlier definition whose complete defining facets remain available in both branches;
3. incompatible branches may not reuse an output identifier; every exported/private wire has one global owner and explicit scope;
4. every non-branch native rule has an already proved polynomial local EF translation using only its explicit authenticated premises;
5. `MERGE` consumes both exact complementary contexts, and no branch-local conclusion is cited in a weaker/incomparable context.

**Theorem (PROVED/RESTRICTED).** Under conditions 1--5, a shared `B-CANON2R^-` proof DAG of $q$ nodes and $L$ explicit evidence bits translates in polynomial time and size to an unbranched EF proof. Each judgement $\Gamma\vdash\theta$ is represented by the guarded formula $(\bigwedge\Gamma)\to\theta$.

**Proof.** Process the acyclic dependency graph once. Source and local mixed nodes use their fixed local EF simulations. For a definition $z\leftrightarrow\varphi$, global freshness ensures $z$ is absent from the extra assumptions, precisely the $EF^{-}$ hypothesis; introduce the same extension axiom once and derive its guarded form by Frege reasoning. Resolution/multi-premise nodes combine guarded parent formulas under the consumer context. `MERGE` applies propositional case analysis to the two guarded children. Each record is compiled once and parent references preserve fan-out; no branch tree is expanded. Formula/context construction and local checking are polynomial in $q+L$. This is also a direct nodewise version of Beyersdorff's Theorem 3. Conversely unbranched CANON2R embeds with empty contexts, so this repaired wrapper is p-equivalent to CANON2R/EF under the prior CANON2R local-simulation hypotheses. $\square$

The theorem deliberately does not authenticate historical `/341`; does not prove that arbitrary auxiliary splits can be moved before the branch; and does not cover a semantic `LOCAL-CONVERT` or affine step lacking an explicit polynomial EF derivation. Those are conditions, not conclusions.

## Independent replay and hostile controls

The producer and an independent Node implementation share only the serialized traces. Both report:

- unsafe trace accepted under branch-local freshness; source has four models;
- unsafe trace rejected under global freshness;
- safe UNSAT trace accepted with two distinct fresh branch-local outputs 3 and 4;
- identical trace hashes; independent replay made 685 assertions;
- rejection of source/context output reuse, cross-branch global owner reuse, a corrupt definition facet, omitted negative AND branch, branch-context leakage, and malformed DIMACS clause count.

The safe trace has 11 records: three free sources, eight paid records, of which two fresh `DEF` records are explicit grammar controls and are not ancestors of the contradiction. Its logical proof core has six paid nodes and span four. It is 754 bytes / 6,032 evidence bits, SHA-256 `5dca0bb28f19fa94fb1f8f83a40fbc38e371a167072afa11826f308eaf799682`. The final recorded Python run took 1,582,365 ns and 10,496 KiB `ru_maxrss`; these host measurements include interpreter/runtime overhead and prove no machine lower bound.

Artifacts:

- `experiments/arc/lspv5_368/branch_def_freshness_referee368.py`
- `experiments/arc/lspv5_368/verify_branch_def_freshness_referee368.mjs`
- `experiments/arc/lspv5_368/unsafe_branch_def_referee368.json`
- `experiments/arc/lspv5_368/safe_branch_def_referee368.json`
- `results/raw/arc/2026-11-05_1148_LSPV5_REFEREE368_raw.json`
- `results/raw/arc/2026-11-05_1148_LSPV5_REFEREE368_independent.json`

No authoritative historical checker was executed. The traces are accepted only by the two explicitly declared REFEREE368 implementations.

## Separate work, span, evidence, time and space ledgers

| Ledger | Unsafe falsifier | Safe control / theorem |
|---|---:|---:|
| Distinct logical nodes | 7 paid, all ancestors | 8 paid serialized; 6 in ancestor proof core |
| Ideal unit-inference span | 3 | 4 for proof core |
| Explicit certificate | 513 bytes / 4,104 bits | 754 bytes / 6,032 bits |
| Verification | 6 parent reads, 4 context tests, 10 literal scans | 8 parent reads, 6 context tests, 20 literal scans, 3 source reads |
| Construction/search | fixture construction and seven corruptions are charged in the host run; absent from the ideal minimum by design | guarded compiler is polynomial but no historical implementation is claimed |
| Storage/schedule | materialized all records; no minimum-space claim | sharing is retained by references; a physical schedule must still charge retention/recomputation, parsing and output |

Logical node weights do not imply machine time. Source reads, identifier parsing, facet truth-table scans, context subset checks, reference retrieval, serialization and peak memory remain separately charged. Nothing here changes the historical weight table.

## Consequences for mixed lower bounds and B3

1. **A branch wrapper can be unsound before it is strong.** Exact two-case discharge is not enough. Extension outputs must be fresh from assumptions and the external source universe, not merely fresh per branch.
2. **The safe repair does not create a lower bound.** It shows that a disciplined branching wrapper is no stronger than EF up to polynomial simulation. Existing hard Resolution families may still have short EF/GF(2) proofs.
3. **No global mixed normalizer follows.** A rule-by-rule polynomial source retraction still needs authenticated historical LOCAL-CONVERT payloads, exported/private wire ownership, AND3/GF(2) equations, paid facets and exact Resolution orientation.
4. **B3 remains noncircularly open.** `SAT in P` gives a polynomial decider, not automatically polynomial EF/CANON2R/Rmix refutations. Adding “the decider is correct” as a trusted premise is reflection; assuming polynomial certificates is the desired conclusion. Beyersdorff's results reinforce that broad deduction properties for strong systems are substantive proof-complexity assumptions, not free syntax.
5. **Family status is classified correctly.** Odd Tseitin is certified UNSAT and exponentially hard for ordinary Resolution/Bctx, but easy in the authenticated mixed affine fragment. Haken PHP is Resolution-hard but ER-short. Neither is full-mixed or all-machine hardness.

## Revised claim and next exact gap

The initial p-equivalence idea survives only after replacing ordinary EF-under-premises by the explicit $EF^{-}$ freshness discipline. The new substantive advance is the exact seven-node false refutation showing why that condition cannot be omitted, plus a nodewise shared-DAG repair that does not exponentially unfold branches.

Next: inspect the historical `/341` bytes, not CANON2R prose, to decide whether source variables, context variables, repeated inputs and incompatible branches can ever become definition outputs; then replay the minimal fixture against the authoritative checker if one exists. If global freshness is authenticated, extend the guarded proof rule-by-rule to actual LOCAL-CONVERT/export/AND3/GF(2) nodes. Separately, B3 still requires a noncircular implication from a polynomial SAT decider to polynomial proofs in this same fixed calculus. P versus NP remains **OPEN**.

## References

- O. Beyersdorff, *On the Deduction Theorem and Complete Disjoint NP-Pairs*, ECCC TR06-142, 2006.
- O. Beyersdorff, *The Deduction Theorem for Strong Propositional Proof Systems*, FSTTCS 2007; Theory of Computing Systems 44, 2009/2010, DOI `10.1007/s00224-008-9146-6`.
- M. L. Bonet, S. R. Buss, *The Deduction Rule and Linear and Near-Linear Proof Simulations*, JSL 58(2), 1993, 688--709, DOI `10.2307/2275228`.
- E. Ben-Sasson, A. Wigderson, *Short Proofs Are Narrow--Resolution Made Simple*, ECCC TR99-022; JACM 48(2), 2001.
- A. Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987.
- S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976.
- A. Haken, *The Intractability of Resolution*, TCS 39, 1985.

**Publication guard.** No task identity, title, timezone, schedule, enabled state, historical rule or weight was modified. No other role's manuscript region was edited.

