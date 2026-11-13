# TMR-2 / 004: affine clique Tseitin compression falsifier

**2026-11-13 15:12 PST (America/Los_Angeles).** New TMR-2 Information Necessity, j15marti/pnp main. Symbolic assertions are **CANDIDATE** pending TMR-5 independent review; executed finite evidence **COMPUTATIONAL**. P versus NP **OPEN**.

## Exact claim, source, and model

We construct connected strict proper 3-CNF formulas of arbitrarily large primal treewidth, having exponentially many satisfying assignments in YES instances, yet a single fixed correct total deterministic multitape SAT decider has a polynomial fast path on every family member. Thus no representation-independent runtime or memory necessity follows from either semantic multiplicity or treewidth alone. This is a scoped falsifier, not an all-input polynomial SAT algorithm.

The explicit source encoding is unary header $1^N0\,1^M0$ followed by $M$ ordered clauses of three signed literals, each literal using one sign and $w=\max(1,\lceil\log_2N\rceil)$ identifier bits. The bit length is $L=N+M+2+3M(1+w)$. The machine is one finite all-length program with fixed finite tape alphabet, one physically sequential two-way read-only input head and finitely many writable work tapes. All parsing, copying, counters, conversions, lookups, rereads and Gaussian operations are charged. Invalid sources are rejected by a total parser. The unrestricted target still quantifies over every such correct decider, all polynomial exponents and constants, and some algorithm-dependent hard valid input; nothing here closes it.

## Construction TMR2-AC4

For even $m\ge6$ take $K_m$ with vertices $v=0,\dots,m-1$. Introduce a Boolean variable $x_{vw}$ for each unordered edge. At vertex $v$, list its $d=m-1$ incident edge variables as $e_{v,1},\ldots,e_{v,d}$ and introduce $d-3=m-4$ private variables $y_{v,1},\ldots,y_{v,d-3}$. Given charge bits $b_v$, impose:

$$
e_{v,1}\oplus e_{v,2}\oplus y_{v,1}=0,
$$

$$
y_{v,j-1}\oplus e_{v,j+1}\oplus y_{v,j}=0\qquad(2\le j\le d-3),
$$

$$
y_{v,d-3}\oplus e_{v,d-1}\oplus e_{v,d}=b_v.
$$

Every row uses three distinct variables. For a row $a\oplus c\oplus d=r$, introduce exactly four proper width-three clauses forbidding each of the four violating truth assignments. A literal is positive if the forbidden bit is zero and negative if it is one. Use fixed canonical edge IDs, private-variable IDs and clause order. The resulting formula $F_{m,b}$ has

$$
E=\frac{m(m-1)}2,\quad N=E+m(m-4)=\frac{3m(m-3)}2,\quad M=4m(m-3).
$$

### Claim A: exact labels and witness count, CANDIDATE pending independent review

$$
F_{m,b}\in SAT\quad\Longleftrightarrow\quad\bigoplus_{v=0}^{m-1}b_v=0.
$$

For an even-charge instance, there are exactly

$$
2^{E-m+1}=2^{(m-1)(m-2)/2}
$$

complete satisfying assignments, including assignments to the auxiliaries.

**Proof.** Each block of four clauses is truth-table equivalent to the corresponding 3-variable parity equation. Eliminating the local auxiliary chain yields $\bigoplus_{u\ne v}x_{uv}=b_v$ at every graph vertex. XORing all vertex equations cancels each edge twice, proving necessity of even total charge. Conversely choose any spanning tree and arbitrary values for all $E-m+1$ non-tree edges. Solve the tree-edge values by successively eliminating leaves. The final root equation holds precisely when total charge is even. Every edge assignment uniquely determines all private auxiliary values by the local chain. The dimension and exact count follow. Neither a SAT oracle nor compulsory witness enumeration is used.

### Claim B: actual source primal treewidth, CANDIDATE pending review

$$
\operatorname{tw}(F_{m,b})\ge m-1.
$$

**Proof.** For each vertex $v$ define a disjoint primal-graph branch set consisting of all private variables $y_{v,j}$ and all edge variables $x_{vw}$ with $v<w$. The private variables are connected by their consecutive parity triples; every assigned edge variable occurs in a triple adjacent to a private variable. Every branch set is nonempty for $m\ge6$. For each $v<w$, variable $x_{vw}$ belongs to branch set $v$ and occurs in a parity triple at $w$ adjacent to an auxiliary in branch set $w$. Thus contracting branch sets produces a $K_m$ minor. Treewidth is minor-monotone and $\operatorname{tw}(K_m)=m-1$. This concerns the CNF primal graph, not a graph only promised by metadata.

### Claim C: one uniform fully charged polynomial fast path, CANDIDATE pending review

An exact affine recognizer parses a general strict 3-CNF, groups signed clauses by unordered identifier triples, and checks that each group contains exactly four different clauses forming one complete XOR3 parity block. For accepted sources the formula is literally a GF(2) linear system; ordinary bitwise Gaussian elimination decides its SAT label in polynomial time with all work, row storage, indices, source reads and output charged. Any other valid source goes to a fixed exhaustive SAT decider. Therefore ONE fixed finite total correct all-input decider runs in polynomial time on every such recognized affine source, including arbitrary variable renaming, sign flipping, reordered clauses/literals, disjoint products and unused variable padding. This is not a general polynomial SAT guarantee.

For canonical $F_{m,b}$ there is an even smaller fast path: check the public canonical graph/gadget template as the input arrives, extract each authenticated final-gate charge $b_v$ and accumulate a one-bit XOR. Binary counters and expected-identifier generation use $O(\log(L+2))$ writable cells and polynomial transitions, conservatively $O(L^3)$. All deviations take the complete fallback. No nonuniform answer table, oracle or unchecked input promise is used. The machine need not retain exponentially many candidate assignments or all boundary valuations.

## Information-necessity consequence and hostile controls

A correct machine must distinguish opposite-label valid sources, but the computational *representation* of that distinction can be a parity flag or a polynomial-size row matrix. Even when the original source has primal width $\Omega(m)$ and $2^{\Theta(m^2)}$ satisfying assignments, there is no obligation to construct those assignments, proof objects or boundary-state tables. A source with an odd number of charges set is UNSAT; changing one charge toggles the valid source label. The four-clause XOR3 syntax is not an assumed free semantic tag: a polynomial recognizer authenticates every literal and every parity block.

The published audit tests both labels, missing blocks, variable renaming, source ordering, sign flips and a complete $K_m$-minor branch-set construction. The affine recognizer also handles disjoint products. Horn, 2-SAT, bounded treewidth, general noncanonical auxiliary encodings, compact circuits, copying/caching, and unrestricted rereading remain hostile controls for a putative universal bottleneck. If a transformation destroys this particular recognized grammar, the fallback still ensures all-input correctness, without a family-wide fast-path claim. A one-pass continuation-equivalence assumption is neither imposed nor available for an unrestricted read-only input machine.

**FALSIFIED/RESTRICTED inference:** many witnesses + many possible boundary values + high primal treewidth necessarily imply superpolynomial transitions or retained information for all correct uniform deterministic SAT deciders. The general all-algorithm hard-input lower bound remains **OPEN**.

## Executed evidence

The exact GitHub-hosted JavaScript was executed in a fresh V8 tool isolate through its exported audit. Tests passed on 30 encoded formulas at $m=6,8,10,12,20,50$, with 15 SAT and 15 UNSAT, 30 source encoding/decoding roundtrips, 30 GF(2) label checks, eight explicit graph-minor certificates, 163,840 complete edge-bit assignment evaluations at $m=6$, five exact solution-count checks, 15 renaming/reordering controls, 15 sign flips, 15 missing-clause rejections, and zero failures. The largest source has $N=3525$, $M=9400$, $L=379527$ bits. The source and raw results were both published on main and verified by exact GitHub readback:

- experiments/tmr/tmr2_clique_affine_audit004.cjs, blob 2bab7fa2261df323a4352fce73d3b54d8e68801e
- results/raw/tmr/2026-11-13_1512_TMR2_CLIQUE_AFFINE004_RAW.json, blob c7a1df10710305e45fdad94fb37f5fbf77576cfd

An independent local Python implementation also completed 30 cases and 163,965 edge-mask/representative checks in 2.368 seconds, with zero failures, but was not uploaded to GitHub. Physical TM simulation, OS Node CLI, project-wide preflight, report-validator and LaTeX compilation were not executed. Finite evidence is **COMPUTATIONAL**, not an asymptotic proof.

## Literature and prior work

Graph parity contradictions originate with Tseitin [1]. A previous project report LSPV-1/452 already compiled three-variable parity into four strict proper 3-CNF source clauses (original blob 8eb3dfb9cd0faf149c3032a7ecec2bdc669f1d5e); it concerned a restricted paid proof system, not the current direct SAT-machine fast path. de Colnet and Mengel [2] study regular-resolution and knowledge-representation restrictions, not arbitrary deterministic TM time. TMR-1/003 already proved a recognizable-family fast-path obstruction; the incremental counterexample here has an explicit $K_m$ minor, a large exact solution space, and a one-flag canonical classification. No claim is made that Gaussian elimination or Tseitin parity is newly discovered.

[1] G. S. Tseitin. "On the Complexity of Derivation in Propositional Calculus." Structures in Constructive Mathematics and Mathematical Logic, pp. 115-125, 1968. https://cir.nii.ac.jp/crid/1570854175771062784

[2] A. de Colnet and S. Mengel. "Characterizing Tseitin-Formulas with Short Regular Resolution Refutations." Journal of Artificial Intelligence Research 76 (2023), 265-286. https://arxiv.org/abs/2103.09609 ; https://doi.org/10.1613/jair.1.13521

[3] Original historical report: research/agents/lspv-1/2026-11-06_0911_LSPV1_PROPER3_PARITY_NATIVE_COMPILER452.md. Related current: research/agents/tmr-1/2026-11-13_1500_TMR1_POLY_SHORTCUT_CORE003.md.

## State reconciliation, peer audit and next target

Read first the authoritative 2026-11-13 12:49 PST five-TMR directive; read both root trackers, latest issue #3, entire root main.tex via Git blob, AGENTS.md, CODEX.md, the research skill, all five TMR handoffs, and original relevant parity/compiler and peer reports. Root proof1.txt was 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343. Root proof2.txt initially yielded a blank contents response but its authentic Git blob 930c5eeddafce656717f28055a7a9a755f44737c contained 1,051,196 characters and was fully recovered. Root main.tex authentic blob 7938c144d3538b08e23531b1fa22d2400f3491bb had 2,487,713 characters. The historical role allocations are overridden, not preserved. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root tracker edit or main.tex edit, and no agents or schedules modified.

TMR-5 should independently audit auxiliary elimination, the explicit primal-graph minor and Gaussian fast-path soundness; TMR-3 should audit same-machine charges; TMR-4 must preserve actual cheap affine execution paths in every all-transition abstraction; TMR-1 must preserve universal fixed-program quantifiers.

**Single next objective:** propose an unavoidable *non-affine* global-consistency computation charge, including all processing before, during and after observation, and falsify it against polynomial-time recognizable shortcut classes. Its transfer to every correct uniform deterministic multitape program is **OPEN**.

END_OF_REPORT::TMR-2::CLIQUE-AFFINE004::2026-11-13_1512_PST
