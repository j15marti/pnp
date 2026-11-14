# TMR-4/005: exact horizon-capped program-dependent MAY abstraction

**Date:** 2026-11-13 16:38 PST (America/Los_Angeles). **Owner:** TMR-4, new cost-sound abstraction specialist. **New theorem:** TMR4-HC5, **CANDIDATE pending TMR-5 independent review**. **Independent peer audit:** TMR5-FT3, **PROVED/RESTRICTED** at its finite-battery scope after symbolic reconstruction. Finite source-level transition-table checks: **COMPUTATIONAL**. **P versus NP: OPEN**.

## 1. Target, scope and exact machine

Let $A$ be any **one fixed**, finite, total, deterministic, correct multitape 3-CNF-SAT decider serving all binary input lengths. Its read-only source tape is physical and two-way with endmarkers; it has a finite alphabet and control, finitely many writable tapes, and a fixed finite program. A full concrete configuration records the program, control, source contents $x$, the input head, each work-tape head and all nonblank work-tape cells. Every physical step has time cost one; visited writable cells, input rereads, indexes, conversion, cached encodings and recomputation count in the true resource ledger. Malformed strings are decided correctly. Distinguish $L=|x|$ encoded bits from clause and variable counts.

The unrestricted target still has quantifier prefix
$$
\forall A\,\forall k\ge1\,\forall C>0\,\forall L_0\,
\exists x\in\mathrm{VALID3CNF}:\quad
|x|\ge L_0\ \wedge\ T_A(x)>C(|x|+1)^k.
$$
**Nothing below proves this.** Instead, HC5 gives an explicit *program-dependent*, source-bound, all-step cost-sound construction, and an exact diagnosis of what its potential does and does not certify. This differs from the program-blind common-start ceiling of TMR-4/004.

## 2. New theorem TMR4-HC5: constructive capped exact-trace abstraction

For each specific finite program $A$, explicit input $x$, and integer horizon $B\ge0$, a uniform effective procedure $\mathrm{Cap}(A,x,B)$ constructs a finite weighted MAY graph $G_{A,x,B}$ with initial state $s$, SAT and UNSAT goals, relation $\mathcal R$ from the **actual instrumented machine execution**, and an explicitly computable nonnegative potential $\Phi$ such that:

1. Initial full configuration is related to $s$, preserving its source/program binding.
2. For **every related concrete state and every concrete legal transition**, there is a finite abstract path to a related concrete successor of cost at most the physical step cost one.
3. Every concrete SAT or UNSAT halt is related to the correspondingly labeled abstract terminal. The graph retains both terminal labels, even when the abstract suffix is unknown.
4. On **every** abstract edge $u\xrightarrow{w}v$, including zero-cost edges and cycles, $\Phi(u)\le w+\Phi(v)$ and $\Phi(g_{SAT}),\Phi(g_{UNSAT})\le0$.
5. If $h$ is the number of concrete steps actually executed by the constructor, $h\le B$, then
   $$
   \boxed{\Phi(s)=d_G(s,\{g_{SAT},g_{UNSAT}\})=h
   =\min\{B,T_A(x)\}\le T_A(x).}
   $$
   The equality with $\min\{B,T_A(x)\}$ is **an analytical characterization of the constructed finite graph**, not a definition of an unknown potential or a computational shortcut for discovering $T_A(x)$.

**Effective construction, with no SAT oracle.** Run the supplied transition table on the actual source $x$ for at most $B$ steps, stopping early if the machine halts. Preserve the exact successive complete configurations $c_0,\ldots,c_h$, plus an *analyst-only* transition-number ghost tag. If the run halts at $h\le B$, make vertices $p_0,\ldots,p_{h-1}$ and an edge of cost 1 along the actually observed next transition, ending in the goal labeled by the actual terminal control. No knowledge of the SAT answer independent of running $A$ was required. If the run has not halted after $h=B$ steps, keep the $B$ exact prefix vertices $p_0,\ldots,p_{B-1}$, connect $p_{B-1}$ to a MAY state $\star$ at cost 1, and add $\star\to\star$, $\star\to g_{SAT}$, and $\star\to g_{UNSAT}$ at cost 0. For $B=0$ and a noninitially halted machine, start directly at $\star$. Include both labeled goals even in the halted case, with no invented edge to the opposite goal.

Set $\Phi(p_i)=h-i$ for $0\le i<h$ and $\Phi(\star)=\Phi(g_{SAT})=\Phi(g_{UNSAT})=0$. Every exact-prefix edge is tight: $h-i=1+(h-i-1)$, and all $\star$ edges satisfy $0\le0+0$. Terminal potentials are zero. The sole path from $s$ to any goal traverses $h$ unit edges and then, only in the truncated case, zero-cost $\star$ edges; hence the minimum abstract decision-path cost is exactly $h$. This derives a nontrivial positive finite potential **from a concrete bounded computation**, and never defines it from an unobserved runtime.

**Full-step relation.** Formally instrument the deterministic execution with a ghost transition index $t$ without adding any machine work. For each $t<h$, relate $(c_t,t)$ only to its exact prefix vertex $p_t$, including the entire source, program, input/work heads and tape contents; the next concrete transition maps to the next cost-1 prefix edge or $\star$/actual terminal. If $A$ continues past $B$, relate **every** later nonterminal $(c_t,t)$ to $\star$; each later step maps to its zero-cost self-edge except the final transition, which may map to $\star\to g_{\ell(x)}$ at cost zero. Relate the actual terminal to its correct label-specific goal. Thus every real transition is represented even after forgetting all later work. Repeated concrete configurations, rewinds, temporary encodings, sharing, arbitrary work tapes and recomputation pose no additional hypothesis. $\star$ is an intentional overapproximation, not an uncharged concrete SAT oracle.

**No false all-input claim.** This is a uniform *abstractor* for every finite transition table $A$, not a polynomial SAT decider. The analysis itself spends $h$ real simulated steps and records up to $h$ exact full configurations. For superpolynomial $B$, constructing this particular graph can be superpolynomial. One must separately establish that a prescribed $B$ is exhausted without a halt on the right input; selecting $B$ superpolynomially and asserting $\Phi(s)=B$ is circular unless that no-halt premise is proved. HC5 certifies concrete bounded-trace nonhalting, not an all-exponent lower bound.

## 3. Hostile abstract-path replay and refinement

For $B<T_A(x)$, the cheap abstract path $p_0\to\cdots\to\star\to g_{\ell(x)}$ has cost $B$, while no **actual** machine halt occurs in its first $B$ concrete steps. The path is deliberately *spurious as a bounded-time terminal witness*: it is not a physical $B$-step computation, although the machine ultimately produces the indicated true label. The other zero-cost edge $\star\to g_{\neg\ell(x)}$ may even predict the wrong label. **Both MAY paths are necessary in an abstractor that has genuinely forgotten the suffix without proving its outcome.**

A permitted refinement is to simulate additional actual concrete transitions, replace $\star$ by the newly exposed exact segment, and reintroduce a later $\star$ only after the new horizon. This increases the certified potential by precisely the additional verified nonhalting steps. Simply removing $\star\to g_{\ell(x)}$ because it is a cheap path breaks the terminal-preservation requirement unless a replacement route exists. Deleting an actual accepted trace from the MAY model is unsound. This is consistent with the archived native /341 accepted-byte counterexamples of LSPV-5/510 and /511, whose real paths cannot be declared spurious to rescue a preferred grammar.

The exact simulation theorem alone therefore has **no superpolynomial-content implication**: even an arbitrary-program construction may be cost-sound and have exactly zero potential when $B=0$. Any stronger abstract potential must establish additional *algorithm-independent* constraints that force high cost for each targeted fixed $A$ and input, beyond the ability to expose a long trace by direct simulation.

## 4. Independent peer review: TMR5-FT3 finite battery trie

Independently reviewed the ORIGINAL TMR-5/003 mathematical report, executable and raw data. For any finite $H\subseteq\{0,1\}^*$ with $R=\sum_{x\in H}|x|$, construct a root plus one state per distinct nonempty prefix. Thus $Q\le1+R$ trie states. A fixed finite controller reads one source bit per transition; a **right-endmarker check** distinguishes a complete member from a proper prefix, so an input which extends a member cannot acquire the member's answer. At missing edges/nonterminal endmarkers it rewinds the original input and invokes a paid total correct exhaustive fallback, with blank work tapes. For each $x\in H$, the SAME finite program uses at most $|x|+1$ transitions; its constant-outdegree transition description uses $O((R+1)\log(R+2))$ bits. The empty string, shared prefixes and both terminal labels do not break the construction.

**Verdict: PROVED/RESTRICTED** as a finite-suite nonuniformity theorem, independently of the existing published finite regression. The trie varies with $H$; there is no single program of uniformly bounded description size for an unbounded sequence of chosen batteries. Consequently the result is neither P=NP nor a program-dependent abstraction no-go. It does independently reaffirm TMR-4/004's machine-blind common-start ceiling, already peer reviewed by TMR-5.

## 5. Executed reproducible finite checks

Reproducible source: `experiments/tmr/tmr4_horizon_exact_config_audit005.cjs`. Immutable raw: `results/raw/tmr/2026-11-13_1638_TMR4_HORIZON_EXACT_CONFIG005_RAW.json`.

Actually executed the exact JavaScript `audit()` in hosted V8, not via native OS Node, on **1,022** complete runs of two explicit, fixed deterministic finite transition-table machines on ALL binary words of lengths 0 through 8. Both decide the same toy parity language, the second with a physical input rewind, a second source pass and two writable-head movements per run. The toy machines are not 3-SAT deciders; their role is to independently exercise the machine-level all-step, both-label, head and work-tape mechanics of HC5. The symbolic theorem quantifies separately over any fixed total correct 3-SAT machine.

Recorded **17,410 concrete transitions**, **138,435** concrete-step-to-abstract-path checks over sampled horizons, **583,387** total assertions including all-edge potential inequalities and terminal binding, **5,978** explicitly truncated nonhalting-horizon abstract paths, **3,586** second-pass source reads and **1,022** writable-head moves, with **zero failures**. Maximum observed run length 29 steps. Horizons included $0,1,2,3,\lfloor T/2\rfloor,T-1,T,T+1$ (deduplicated). Physical transition-table steps were executed in the V8 emulator; native Node CLI execution was unavailable because raw GitHub download DNS failed. Neither an unrestricted 3-SAT TM, LaTeX compilation nor the repository preflight script was executed. The finite checks are **COMPUTATIONAL**, not an asymptotic theorem or a physical hardware measurement.

The audit retains fixed program/source tags, input/work head positions, visited work contents, exact prefix chronology, SAT/UNSAT goal labels and both unknown continuation goals. The two program fixtures make materially different time/space choices while computing exactly the same output. Additional Horn, 2-SAT, XOR/Tseitin, bounded treewidth, products, renaming, padding and sharing algorithms are admitted in the general abstract proof but not separately timed in this finite toy audit. Their known polynomial shortcuts remain genuine and cannot be charged away.

## 6. Corpus, historical scope, sources, dependencies and handoff

Read FIRST the authoritative replacement directive at blob `47459817e66dccf1f3079e6c724c0fd2643e7bc4`. Recovered full `proof1.txt` (28,714 characters, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), full `proof2.txt` by authentic blob `930c5eeddafce656717f28055a7a9a755f44737c` (1,051,196 characters), and full canonical root `main.tex` by authentic blob `b261f0c8131c2512c1d018dfed9b257fd856ccc5` (2,492,830 characters). A blank contents response was **not** treated as an empty tracker. Also consulted current issue #3 (1,953 comments), `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, all five current TMR handoffs, original TMR-4/001 and /004, original TMR-5/003 and its code/raw, TMR-3/005, and original LSPV-5/510 and /511 restricted parser counterexamples. The historical LSPV identity/schedule language in older root protocols is superseded, not the scientific evidence.

Primary literature checked for methodological background, **not** as a claimed precedent for HC5: [1] P. Cousot and R. Cousot, *Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints*, POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973 . [2] E. Clarke, O. Grumberg, S. Jha, Y. Lu and H. Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000, LNCS 1855, pp. 154-169, https://doi.org/10.1007/10722167_15 . These establish relevant abstraction/refinement background, not universal SAT lower bounds.

**Dependencies:** HC5 assumes only a specified finite deterministic transition table and exact source binding for its construction; terminal correctness additionally assumes $A$ is a correct total 3-SAT decider. Its resource potential certifies only already simulated nonhalting steps. TMR-4/001 source-observation hitting sets are independent and retain their sharp $\le L$ ceiling; TMR-4/004 machine-blind potential ceiling remains PROVED/RESTRICTED after TMR-5; TMR5-FT3 now has a second symbolic audit. The unrestricted processing lower bound and P versus NP remain **OPEN**.

**Shared-file status:** TRACKERS REVIEWED; NO MATERIAL CHANGE to `proof1.txt` or `proof2.txt`. Root `main.tex` not edited: HC5 awaits independent review and TMR-5 retains whole-document synthesis. No tasks, roles or schedules modified. Existing native accepted historical checker paths remain intact.

**One next target:** TMR-5 independently audit HC5's time-tagged full-state relation and all-step cost direction, then seek a noncircular program-aware potential stronger than the capped execution-prefix certificate, ideally derived from a proved invariant of globally necessary computation rather than an already simulated runtime.
