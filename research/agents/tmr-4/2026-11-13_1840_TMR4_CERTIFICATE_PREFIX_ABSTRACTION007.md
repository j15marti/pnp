# TMR-4/007: exact-prefix plus arbitrary opposite-label difference certificates

**Report time:** 2026-11-13 18:40 PST (America/Los_Angeles). **Role:** NEW TMR-4 Cost-Sound Abstraction, j15marti/pnp main. **Scientific status:** CANDIDATE theorem until independent TMR-5 review; finite verification COMPUTATIONAL. The unrestricted all-exponent deterministic 3-SAT lower bound and P versus NP remain OPEN.

## 1. Exact increment over existing work and falsification contract

TMR-4/001 already supplied the arbitrary-overlap *difference-set hitting-set* abstraction for original input reads. TMR-4/006 independently supplied a *concrete paid execution-prefix plus residual individually sensitive source-bit* product and falsified naive double charging. **This report combines the exact paid prefix with arbitrary overlapping certified opposite-label difference sets**, rather than merely one-bit neighbors. The new suffix potential can be strictly positive when *no original literal-field bit* is individually SAT/UNSAT-sensitive. The hitting-set and certificate-complexity ideas are classical [1,2]; the purpose here is a fully specified all-transition machine-cost simulation and a precise stronger scoped example, not a claim of novel separation.

Predeclared falsifiers: (F1) an actual source read, recomputation, copy, index move, working-head movement or halt has no affordable abstract path; (F2) a real SAT/UNSAT terminal lacks its correctly labeled abstract goal; (F3) some MAY edge, including a zero-cost stutter, violates the potential inequality; (F4) the potential double-counts source bits observed in the concrete prefix; (F5) a graph-observation argument charges unobserved information *after* it has already been acquired; (F6) the proposed candidate is misconstrued as superpolynomial despite a linear source-bit ceiling. Each is addressed below.

## 2. Machine model and finite certified adversary family

Fix **any one** finite, total, correct, deterministic multitape 3-SAT decider $A$ for all binary input lengths. Its actual concrete configurations include fixed program/control, the full read-only encoded source and endmarkers, all input-head locations, complete work-tape contents and heads, all temporary representations, indices, counters, stacks, buffers, cached encodings and repeated or recomputed values. Every physical transition costs 1; the finite input interface observes at most a fixed $q\ge1$ original source-bit positions per physical transition. All addresses and indirect read operations must be implemented and charged under the declared finite machine model. Let $x$ be any valid encoded proper 3-CNF of bit length $L$, and let $f(x)\in\{\mathrm{SAT},\mathrm{UNSAT}\}$ be its mathematically true label. Malformed-input behavior remains the total decider's responsibility.

Choose **any finite certified collection** of valid encoded $y_1,\ldots,y_r$, each of length $L$ and with independently justified $f(y_i)\ne f(x)$. These can be SAT witnesses versus an independently established UNSAT source, or vice versa. Define the nonempty difference sets

$$
D_i=\{j\in\{0,\dots,L-1\}:x_j\ne (y_i)_j\},
\qquad \mathcal D=\{D_1,\dots,D_r\}.
$$

This collection is an *analysis parameter*, not a table or oracle available to $A$. It may be empty. We never assume efficient enumeration of all opposite inputs, discovery of hard formulas, or a solver correctness proof in a chosen formal calculus. Every source and neighbor is explicitly bound to the same fixed bit grammar and same length.

Attach to physical configurations an external ghost trace monitor $V$, the original source-bit positions ever observed by physical input heads. This is not solver-accessible storage. Initially $V=\varnothing$; one concrete step updates $V$ to $V'=V\cup R$ with $|R|\le q$. Repeated reads, endmarkers, purely computational work and zero new source observations leave $V$ unchanged. Ghost augmentation never changes $A$'s physical execution or charged cost.

A deterministic unread-source coupling proves that at **any correct physical terminal**, $V$ hits every $D_i$. Otherwise some $y_i$ agrees with $x$ at every source coordinate examined, has the same length/endmarkers, and induces the identical sequence of finite-control, read-only-head, work-tape, and terminal states, contradicting their opposite labels. No online restriction is needed: this uses the actual complete adaptive transcript, including arbitrary rereads.

For any $V\subseteq[L]$, put

$$
\tau_{\mathcal D}(V)=
\min\bigl\{|W|:W\subseteq[L]\setminus V,\;
(V\cup W)\cap D_i\ne\varnothing\ \text{for every }i\bigr\}.
$$

The empty witness family has $\tau_{\varnothing}(V)=0$. The complete source coordinates always hit every nonempty $D_i$, so $0\le \tau_{\mathcal D}(V)\le L-|V|$. For a collection of singleton difference sets $\mathcal D=\{\{p\}:p\in P\}$ this specializes to $\tau_{\mathcal D}(V)=|P\setminus V|$ and recovers TMR-4/006 exactly.

## 3. CANDIDATE theorem TMR4-CP7: exact prefix and residual certificate potential

For any integer $B\ge0$, physically simulate $A(x)$ for at most $B$ transitions, preserving the *actual full configurations*, read addresses and ghost sets. If it halts at $T\le B$, keep the complete exact cost-one chain of length $T$, with its actual SAT or UNSAT terminal label. The potential on stage $j$ is $T-j$, and on both goal labels is 0.

Otherwise $T>B$. Retain a cost-one exact chain $p_0\to\cdots\to p_B$ with complete concrete configurations and actual source observations $V_B$; identify the last node with an abstract suffix node $\star_{V_B}$. Introduce suffix nodes $\star_V$ for **every** $V_B\subseteq V\subseteq[L]$. Give each $\star_V$ a zero-cost stutter; for every nonempty $R\subseteq[L]\setminus V$ with $|R|\le q$, give a cost-one edge $\star_V\to\star_{V\cup R}$. When $V$ hits every certified $D_i$, give zero-cost edges from $\star_V$ to **both** distinct abstract goals $g_{\rm SAT},g_{\rm UNSAT}$. They are MAY outcomes, not assertions that both physical labels are possible. This ensures no hidden label oracle or solver template gates the suffix graph.

The complete MAY graph is finite, although it may have exponentially many mask states. Every actual physical successor after the horizon relates to the ghost-observation node $\star_V$; every prefix configuration relates to its exact chain node. The concrete state relation includes the full source and program *on the concrete side* and therefore does not conflate physical configurations as equal; the abstraction deliberately forgets them after the prefix. The relation is defined for instrumented concrete histories, since the same underlying work configuration may occur with different observation histories.

Define

$$
\Phi(\star_V)=\left\lceil\frac{\tau_{\mathcal D}(V)}q\right\rceil,\qquad
\Phi(g_{\rm SAT})=\Phi(g_{\rm UNSAT})=0,
$$

and, when $T>B$, define $\Phi(p_j)=B-j+\Phi(\star_{V_B})$. On each exact prefix edge the potential inequality holds with equality. On any suffix edge revealing $R$, extend a minimum residual hitting set for $V\cup R$ by $R$ to obtain

$$
\tau_{\mathcal D}(V)\le |R|+\tau_{\mathcal D}(V\cup R)
\le q+\tau_{\mathcal D}(V\cup R).
$$

Consequently $\Phi(\star_V)\le 1+\Phi(\star_{V\cup R})$. Every zero-cost stutter preserves $V$ and $\Phi$. Every terminal edge starts at $\tau_{\mathcal D}(V)=0$ and therefore satisfies $\Phi(\star_V)\le0+\Phi(g)$. Thus $\Phi(a)\le c(a,b)+\Phi(b)$ holds on **EVERY abstract edge**, not only executed paths, with both goals having potential zero.

Every legal physical transition from **every related ghost-concrete/abstract pair** maps to a finite abstract path of total cost at most its concrete increment 1: the exact paid prefix edge, a cost-one new-read edge, or a zero-cost stutter, respectively. If the physical successor halts, append its appropriate goal edge at zero cost. The unread-source coupling guarantees the terminal guard, so both actual SAT and actual UNSAT terminations preserve their true labels. All actual executions, including copies, algebraic operations, temporary encodings, head movements, arbitrary memory, rereads, recomputation and delayed final original reads, remain represented. Zero-cost abstract stutters do **not** mean those real operations are free; the MAY graph deliberately undercharges them, which is the safe direction for a lower-bound abstraction.

A minimum hitting set of size $\tau_{\mathcal D}(V_B)$ can be revealed in batches of at most $q$, so an abstract path *attains* the suffix potential. Conversely any suffix goal path must hit every $D_i$, which costs at least $\lceil\tau_{\mathcal D}(V_B)/q\rceil$ paid reveal edges. Therefore the **exact abstract shortest decision-path cost** equals

$$
\boxed{
d_{\rm MAY}(s,\mathrm{goal})=\Phi(s)=
\begin{cases}
T_A(x),&T_A(x)\le B,\\
B+\left\lceil\tau_{\mathcal D}(V_B)/q\right\rceil,&T_A(x)>B.
\end{cases}
\quad\le T_A(x).
}
$$

This is a program-dependent, source-dependent **all-machine simulation theorem candidate**, not a proof of a superpolynomial initial potential. The precise bound is also valid as a direct observation-coupling inequality. No actual cheap source computation is excluded by its graph.

## 4. New proper 3-CNF falsifier of singleton-only sensitivity

Construct $x$ with $N=6$ declared variables and **all 20 distinct, all-positive proper three-variable clauses** indexed by the 20 subsets of $\{1,\ldots,6\}$ of size three. Every clause uses three distinct identifiers, all six variables occur, and the assignment setting every variable true satisfies $x$. Encode with the project's unary $1^N0\,1^M0$ header, sign-plus-$w$-bit identifiers, $M=20,w=3$. The full encoded length is

$$
L=(6+1)+(20+1)+20\cdot3\cdot(1+3)=268.
$$

Produce $y_1$ by replacing the **first eight** clauses by all eight different sign patterns on variable triple $(1,2,3)$; produce $y_2$ by replacing the **last eight** clauses by all eight sign patterns on $(4,5,6)$. Leave all other clause slots byte-identical. Each $y_i$ has 20 proper clauses, uses all six variables, has exact length 268, and is UNSAT because its eight-clause core forbids all assignments to the corresponding triple. The source $x$ is SAT. Their encoded difference sets $D_1,D_2$ are nonempty and **disjoint** because they occupy disjoint clause slots. Hence

$$
\tau_{\{D_1,D_2\}}(\varnothing)=2
\quad\text{and}\quad
\Phi(\star_\varnothing)=2\quad(q=1),
$$

even though no individual flip of a literal-sign bit, or a valid single identifier-field bit, makes $x$ UNSAT: the all-true assignment still satisfies every clause after any such one-bit change. The earlier *literal-field singleton* certificate set is empty, whereas the multi-bit adversary graph has positive potential. This is a concrete strict proper 3-CNF improvement, not only a toy Boolean threshold demonstration. It is still **constant** information acquisition, not a superlinear result.

Independent native Python exhaustive evaluations confirmed SAT($x$), UNSAT($y_1$), UNSAT($y_2$), length 268, difference-set cardinalities 33/35 and disjointness. Independently authored hosted-V8 code exhaustively evaluated all $2^6=64$ assignments for each source, and checked all 60 one-bit sign mutations, 84 valid one-bit identifier mutations and 96 invalid identifier mutations: no valid single literal-field mutation inverted the SAT label. A fixed program can trivially brute-force these small formulas; the construction makes no large-time claim.

A second, explicitly **toy Boolean-function** hostile control is majority on odd $n$ bits at $x=1^n$. Individual one-bit sensitivity is zero, but its exact all-opposite-input certificate complexity is $(n+1)/2$. For $n=9$, there are 256 opposite-label source strings and its certificate size is five. This is a finite decision-tree distinction, not a SAT lower bound. It shows strict growth beyond singleton sensitivity. The prior TMR-4/006 double-count counterexample remains valid; the new theorem's $V_B$ residualization avoids it for overlapping difference sets as well.

## 5. Executed verification and reproducible artifacts

**Actually executed hosted V8 and readback-verified** source-event tests in \`experiments/tmr/tmr4_certificate_prefix007.cjs\`, with immutable raw \`results/raw/tmr/2026-11-13_1840_TMR4_CERTIFICATE_PREFIX007_RAW.json\`:
- 280 finite majority/parity/OR source/function cases, 12,600 abstract subset states;
- 117,298 paid edges, 25,200 zero-cost stutters and 20,160 valid-goal edge checks;
- 142,498 potential-edge checks, 7,394 paid toy physical-event transitions, 4,480 prefix horizons and 560 independently computed BFS shortest paths;
- 114 source cases where full difference certificates beat singleton sensitivity; 1,683 cases with a strict prefix-composition gain;
- 15,120 invalid zero-cost early goal controls rejected, **zero failures**.

**Actually executed independent hosted V8** proper 3-CNF control in \`experiments/tmr/tmr4_sat_disjoint_cert007.cjs\`, immutable raw \`results/raw/tmr/2026-11-13_1840_TMR4_SAT_DISJOINT_CERT007_RAW.json\`: 268-bit SAT formula, two disjoint opposite-label UNSAT changes of 33 and 35 bits, all six variables present, and the 60/84/96 literal-bit flip controls listed above; zero failed assertions. The two main executables were generated from the exact JavaScript audit functions actually executed, not reconstructed from screenshots or merely proposed tests.

**Limitations:** These are full finite source-level evaluations and toy observation-event traces, **not** native physical multitape Turing-machine traces, not a general SAT solver test, and not a real proof that an efficient analyzer can enumerate $\mathcal D$ or compute its hitting sets. No OS Node/LaTeX compiler or repository preflight execution is claimed. The unrestricted all-exponent separation remains OPEN.

## 6. Machine transfer, algebraic controls and ceiling

The coupling argument depends only on one fixed deterministic correct machine, fully paid input access, and opposite-label *valid same-length* source witnesses. It imposes no Horn, 2-SAT, XOR/Gaussian, bounded-treewidth, clause-order, auxiliary-variable, disjoint-product, source reread, compact-circuit, sharing, or workspace restriction. Its cost bound may be small on any of these families; no semantic multiplicity is charged as compulsory processing. Those specific solver implementations were not newly executed in /007. The existing TMR-1/005, TMR-2/007-008, TMR-3/006-007 and TMR-5/005 polynomial structured-family escapes remain hostile to stronger claims.

**Critical exact ceiling:** $\tau_{\mathcal D}(V)\le L-|V|$, so even the most complete and expensive-to-enumerate opposite-neighbor collection gives only $\Phi(\star_V)\le \lceil L/q\rceil$. Choosing large $B$ gives an apparently large prefix term only after executing or independently establishing that the concrete machine has not halted within $B$. An arbitrary correct finite program may preprocess, copy source bits, use compact GF(2) elimination, reread the source, or choose an alternative circuit representation. The observation abstraction forgets this work and cannot prove an unavoidable superpolynomial *processing* cost. No free SAT oracle, advice, shortcut terminal, unbounded-word primitive or ETH/SETH hypothesis is introduced.

## 7. Sources, review request, trackers and publication state

[1] P. Cousot and R. Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints," POPL 1977, pp. 238-252, DOI: https://doi.org/10.1145/512950.512973 . Original author's bibliographic page: https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml .

[2] H. Buhrman and R. de Wolf, "Complexity Measures and Decision Tree Complexity: A Survey," Theoretical Computer Science 288(1), 2002, pp. 21-43, DOI: https://doi.org/10.1016/S0304-3975(01)00144-X . Certificates, sensitivity, block sensitivity and decision-tree bounds are established prior art.

[3] Original TMR-4/001: \`research/agents/tmr-4/2026-11-13_1336_TMR4_OBSERVATION_HITSET001.md\`. Original TMR-4/006: \`research/agents/tmr-4/2026-11-13_1737_TMR4_PREFIX_SENSITIVITY_PRODUCT006.md\`, exact executable and immutable raw. TMR-2/008: \`research/agents/tmr-2/2026-11-13_1823_TMR2_DENSE_SOURCE_BIT_SENSITIVITY008.md\`. TMR-3/007: \`research/agents/tmr-3/2026-11-13_1828_TMR3_CLAUSE_ORDER_LOCALITY_ESCAPE007.md\`. Historical counterexample guard: \`research/agents/lspv-1/2026-11-11_1857_LSPV1_CHECKER_ACCEPTANCE_CEGAR_NOGO586.md\` and native checker normalizer \`research/agents/lspv-5/2026-11-12_1848_LSPV5_NATIVE341_OUTER_ENVELOPE_NORMALIZER515.tex\`, treated as restricted original artifacts, not as an unrestricted SAT bridge.

Read FIRST the 12:49 PST five-TMR replacement directive (SHA \`47459817e66dccf1f3079e6c724c0fd2643e7bc4\`); read complete root \`proof1.txt\` (28,714 characters; SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`) and authentic full Git blob \`proof2.txt\` (1,051,196 characters; SHA \`930c5eeddafce656717f28055a7a9a755f44737c\`; contents API returned blank), full authentic main.tex blob (2,497,977 chars; SHA \`4e0dc7a81c3757289e87661b6df29e458cd03daa\`), latest issue #3 comments through TMR-3/007, AGENTS.md, CODEX.md, the pnp-research skill, all five newest TMR handoffs and the original relevant peer reports/code/raw. Primary source bibliographies checked this run.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt and proof2.txt were not rewritten. TMR-4 left canonical root main.tex untouched for TMR-5 synthesis, despite an authorized TMR-4 region, to avoid unreviewed manuscript promotion. No scheduled tasks, tasks or other agent identities were created, modified or revived.

**TMR-5 independent peer review request:** (i) verify the all-related-pair every-transition ghost-coupling and both-label terminal proof, (ii) independently evaluate the 268-bit SAT and two disjoint UNSAT encoded witnesses, (iii) verify every cost-zero edge and the exact hitting-set shortest path, (iv) try speculative early completion and compact XOR shortcuts as hostile controls. **ONE next target:** a machine-execution potential charging provably unavoidable computational processing beyond acquiring an at-most-$L$ source certificate, without imposing a selected proof calculus or solver representation.

END_OF_REPORT::TMR4::CERTIFICATE_PREFIX_ABSTRACTION007::2026-11-13_1840_PST
