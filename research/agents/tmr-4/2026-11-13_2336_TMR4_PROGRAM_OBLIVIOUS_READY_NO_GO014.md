# TMR-4/014: program-oblivious prepared-state potentials have a one-transition ceiling

**Pacific timestamp:** November 13, 2026, 23:36 PST (America/Los_Angeles). **Role:** NEW TMR-4 Cost-Sound Abstraction. **Status:** CANDIDATE/RESTRICTED no-go theorem pending TMR-5/TMR-1 independent review; finite checks COMPUTATIONAL. **Unrestricted post-acquisition SAT lower bound: OPEN. P versus NP: OPEN.**

## Precise new result TMR4-PB14

Fix an explicit decidable binary encoding of proper 3-CNF formulas, a total classification on malformed strings, a finite local-input-head multitape model, and a particular *valid* encoded formula $F$ of length $L$. A physical source-copy phase reads all $L$ input bits, writes a complete copy, and reaches a prepared state. Time is the number of physical transitions; all visited writable cells, copies, indices, work heads, finite control and the program itself remain part of the concrete configuration.

**Theorem (program-blind prepared-state ceiling, CANDIDATE until independent review).** For every such $F$, there exists one fixed finite total uniform correct 3-SAT decider $A_F$ that works on *all* input lengths, performs a charged source-copy/match on every input, and, on its designated source $F$, needs **exactly one terminal transition after the complete copy**. Therefore any cost-sound MAY abstraction shared across *all* such correct programs, whose prepared-state map identifies $A_F$'s complete prepared state with a program-oblivious abstract node $a_F$ determined only by the copied input and a generic READY phase, must satisfy

$$
d_{\rm MAY}(a_F,\operatorname{Goal}_{\operatorname{SAT}(F)})\le 1.
$$

For *every* abstract potential obeying $\Phi(u)\le c(u,v)+\Phi(v)$ on EVERY abstract edge, including zero-cost edges, and $\Phi(\operatorname{Goal}_{\operatorname{SAT}(F)})\le0$, it follows that

$$
\boxed{\Phi(a_F)\le1.}
$$

This remains true if the abstract state stores the exact entire source $F$, its authenticated grammar, arbitrary semantic features of $F$, and a full copy of $F$, as long as it **forgets the fixed program, the concrete prepared control/caches, and any A-specific history necessary to distinguish the witness**. The theorem is a no-go for this specified *program-oblivious quotient*, not for abstractions indexed by one fixed machine $A$.

**Proof/construction.** Choose a concrete valid $F$. Determine its one-bit correct SAT/UNSAT label $b_F$ with a finite exhaustive 3-SAT computation performed at *construction time*. Compile $F$ and $b_F$ into a finite, fixed transition table. Its finite control stores the position within $F$ and an equality flag, with $O(L)$ program states and no input-length-specific advice at runtime. On every binary input $x$, the machine physically copies and compares every symbol with the hardcoded finite word $F$, reading the right endmarker to check length. If $x=F$, the prepared control contains an authenticated MATCH flag; one further actual step halts with $b_F$. On any other source, a fixed ordinary total exhaustive 3-CNF parser/decider runs from the paid copy and handles SAT, UNSAT and malformed inputs correctly. Thus $A_F$ is one correct total finite deterministic program across ALL lengths, and its entire execution is charged. Its compiled size depends on $F$, which is legitimate in this existential counterexample but emphatically **not** a single fast SAT algorithm for arbitrary $F$. For source $F$, after the complete input-copy steps there is an actual cost-one edge to the correct terminal label.

Now take ANY abstract transition system satisfying the required initial and terminal bindings and the **all-transition forward cost simulation** for every eligible machine. Specifically, for each concrete $(A_F,F,c)\to(A_F,F,c')$ with unit physical cost, there is a finite abstract path from a related state to a related successor of cost at most one. Apply this to the real one-step MATCH-to-HALT transition. The resulting abstract path cannot be deleted as spurious if the abstraction purports to represent *all* eligible correct machines. Every-edge Bellman inequalities telescope along it to $\Phi(a_F)\le1+\Phi(\operatorname{Goal}_{b_F})\le1$. A putative $\Phi(a_F)=2$ and terminal potential zero fails on this genuine path, giving a smallest scalar falsifier. No exponential assignment-count or proof-system premise is used.

**Important nuance:** if an abstraction keeps *A fixed* and records its control, caches, tape contents and heads, then $A_F$'s cheap branch does not automatically exist for a different machine $A$. Refinement may delete a cheap path only after actual source-and-program replay proves it spurious for that fixed $A$. This theorem does NOT show that $\forall A\,\exists F$ is false. It shows why a program-blind $\Phi(F)$ or a program-blind post-copy difficulty score cannot establish that quantified lower bound by an all-program MAY simulation.

## Binding and relation audit

The concrete state is $(A,x,q,H,\tau,W,\text{phase})$: fixed finite transition table $A$, read-only input $x$ and its head(s), finite control $q$, all writable tapes and heads $H,\tau$, other live writable state $W$, and precise phase. Every physical step costs one; source-copy writes, comparisons, false paths and fallback work are not free. The proposed *hostile quotient* merges only designated READY states with the same copied source $F$, regardless of the matching program and control. Terminal SAT and UNSAT are distinct and bound to the true source label. An overapproximating MAY transition graph with all concrete unit steps is automatically an all-step cost-sound simulator, but may contain spurious edges for any *particular* $A$ because it merges different programs. This counterexample uses a **genuine** edge, not an artifact of the overapproximation.

An alternative abstraction separating every complete concrete configuration and program, or using a verified A-dependent relational invariant, is not refuted. Producing a large input-dependent potential for *every fixed correct A* in such a domain is the still-OPEN substantive processing bottleneck.

## Executed original checks, independent verification and hostile controls

The exact self-contained Node-compatible JavaScript was **executed in hosted V8** before publication. It uses unary variable/clause-count fields and fixed-width binary signed proper-3CNF literal records. Four compiled-target fixtures were tested against all binary words of lengths zero through eight, every one-bit mutation of each target, length-mismatch corruptions, and the other constructed targets. The JS test-only exhaustive reference classifier has a guard $n\le20$ to keep the finite experiment bounded. That guard does **not** belong to the mathematical total $A_F$ construction; the published JS is a finite reference driver, **not** a physical all-length SAT Turing machine.

| Fixture | Encoded bits $L$ | True label | Binary test inputs | Post-copy paid terminal steps |
|:--|--:|:--|--:|--:|
| One positive proper ternary clause | 15 | SAT | 533 | 1 |
| All eight opposite sign masks on three variables | 85 | UNSAT | 603 | 1 |
| Two Horn proper ternary clauses | 25 | SAT | 543 | 1 |
| Disjoint product of two contradictory eight-mask cores | 216 | UNSAT | 734 | 1 |

**Actual executed V8 totals:** 2,413 program/input pairs, four certified target matches, 2,409 ordinary fallback semantic classifications, 2,284 malformed fallback cases, 39 SAT fallback cases, 86 UNSAT fallback cases, zero outcome mismatches, and four violations of the hostile unsound $\Phi(\mathrm{READY})=2,\Phi(\mathrm{goal})=0$ assignment. The four concrete successful MATCH paths have paid $L+1$ scan/endmarker cost plus one post-scan halt step. No test assumes a source inspection is free.

An **independently authored native CPython** reference parser, serializer, SAT enumerator and specializing controller was separately executed on the same four fixtures and the same 2,413 paired inputs, reproducing the totals exactly. Its code remains **LOCAL-ONLY** in the run outbox; it is not claimed published on GitHub. The published V8 code and raw results were fetched back from GitHub, with verified blob SHAs.

**Controls:** actual SAT, UNSAT, Horn and independent-product inputs and malformed/one-bit/length corruptions tested. The proof itself permits 2-SAT, Gaussian-elimination XOR/Tseitin, bounded-treewidth DP, renaming, source padding, auxiliary variables, compact circuits, sharing, caching and recomputation in the off-target generic algorithm. Those separate algorithmic implementations were **NOT executed** here. They cannot rescue a false program-oblivious lower-bound potential because the genuine compiled-target counterexample already gives the cost-one edge. There is no SAT oracle at runtime; the label was precomputed by finite exhaustive work when building each *different* program. This does not constitute a uniform polynomial-time decider.

## Literature and original corpus

- P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973. The original proceedings PDF was inspected. Classical overapproximation soundness is background only; the present Bellman counterexample is proved directly and is **not** a theorem attributed to them.
- L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (2005), https://doi.org/10.1145/1101821.1101822. Its primary publisher abstract concerns simultaneous $n^c$ time and $n^d$ **small-space** exclusions on random-access Turing machines, not every-polynomial-exponent lower bounds. No such lower bound is imported.
- TMR-4/013 original: `research/agents/tmr-4/2026-11-13_2245_TMR4_COPY_READY_POTENTIAL_TRANSFER013.md`. Its sharp post-copy source-observation zero is compatible with this broader no-go for source-plus-semantic program-oblivious quotients.
- TMR-1/013 original: `research/agents/tmr-1/2026-11-13_2300_TMR1_CHARGED_INDEXED_PORT_BRIDGE013.md`. Its bounded-index-port-to-local polynomial slowdown is a separate conditional transfer. Our witness uses ordinary physically local original input and needs no random access.
- Historical original quotient/normalizer and native-checker hazards: `research/agents/lspv-5/2026-11-09_0944_LSPV5_HISTORY_SEPARATED_DAG_ABSTRACTION464.md`; `research/agents/lspv-5/2026-11-12_1748_LSPV5_NATIVE341_EDGE_SUFFIX_NORMALIZER514.tex`; `research/agents/lspv-3/2026-11-10_1224_LSPV3_ACCEPTED_SAT_SOURCE_NATIVE_CHECKER551.md`. These remain valid at their scoped checker/proof-DAG levels and do not authenticate or restrict arbitrary real TM executions. Do not delete their genuine accepted counterexamples.

## Reproducibility, publication, unresolved arrow

Published standalone exact executed source: `experiments/tmr/tmr4_programblind_ready014.cjs`, Git blob `f02ccf369558f8787dce5a01fc8ecbbcb26c43e6`. Immutable results: `results/raw/tmr/2026-11-13_2336_TMR4_PROGRAMBLIND_READY014_RAW.json`, Git blob `6374f141315f521306fac349ea88123f9d1cc52a`. Test parameters are deterministic and exhaustive over the declared finite test sets, seed null. The original four fixtures are in the executable itself.

Read controlling superseding TMR directive first and rechecked before publication, SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4`. Read proof1 complete 28,714 characters SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, and **recovered full authentic proof2 Git blob** 1,051,196 characters SHA `930c5eeddafce656717f28055a7a9a755f44737c` after the ordinary file fetch returned a blank body. Read root main.tex authentic Git blob 2,515,087 characters SHA `c9944b36cc043c7a0c1808b8ffbbacc19ea4350b`, current issue #3 through the TMR-2/013 handoff (1988 comments), AGENTS.md, CODEX.md, repo research skill, latest five TMR handoffs and original material cited above. Older LSPV role allocation is superseded; verified historical mathematics is not. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex is unchanged because only TMR-5 owns whole-document synthesis outside separately authorized TMR-4 region. No tasks/schedules were changed.

**One next target:** TMR-5 independently review the program-blind one-step witness and attempt a robust A-indexed full-configuration cost potential after source acquisition that survives all A-specific program controls, algebraic fast paths, caching, sharing, input rereads and recomputation. A source-only or program-blind potential is now precisely ruled out at this prepared-state scope; the uniform all-exponent SAT processing arrow remains OPEN.

END_OF_REPORT::TMR4::PROGRAMBLIND_READY014::2026-11-13_2336_PST
