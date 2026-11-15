# TMR-4/054: Syntactically live, fault-observable gates do not force cut rank or circuit-SAT work

**2026-11-15 15:11 PST | TMR-4 / PNP Cost-Sound Abstraction | Tracks A/C.**

**Status:** PROVED/EXACT for the scoped symbolic construction and functional Tseitin accounting, independent mathematical review OPEN; COMPUTATIONAL for the finite Node/V8 audit; arbitrary circuit-to-BP or SAT-machine lower-bound transfer OPEN. **P versus NP OPEN.**

## Candidate, exact model, falsifiers declared before source review

**Candidate OLG054.** Test whether syntactic gate liveness strengthened by a *counterfactual single-gate output fault* excludes the easy structural shortcuts that defeat static rank and prescribed circuit-to-cut tariffs. Model: explicit shared fan-in-at-most-two acyclic Boolean circuit on $n$ named inputs, with NOT/AND/OR gates and one output; each distinct gate counted once. A gate is *live* if it lies on a directed path to the output. It is *fault-observable* if an original input exists for which flipping only that gate's emitted value, then faithfully recomputing all downstream gates, changes the circuit output. Fault override is a counterfactual diagnostic, NOT a legal SAT-algorithm step.

Precommitted falsifiers: F1 a generated gate is dead or never fault-observable; F2 a claimed unique Tseitin extension fails or auxiliary-variable count is hidden; F3 DISJ with full static cut rank cannot be evaluated by a small shared branching program; F4 the symbolic recognition and exact counting shortcut secretly takes exponential time. An unrestricted gate-size hardness promotion would also fail if a different cheap circuit exists.

## Symbolic construction, proved in the stated model

For any $n\ge2$, signal $a_0=x_1$ and $k\ge n-1$, let $z_j=x_{2+((j-1)\bmod(n-1))}$ and introduce four distinct gates per layer:

$$
u_j=\neg z_j,\quad
v_j=a_{j-1}\wedge z_j,\quad
w_j=a_{j-1}\wedge u_j,\quad
a_j=v_j\vee w_j.
$$

By distributivity and complementarity, $a_j=a_{j-1}$ for every assignment, so $f_{n,k}(x)=a_k=x_1$. Nevertheless, **all $4k$ gates are live and fault-observable**. Every variable occurs in the source and its functional CNF when $k\ge n-1$. For $u_j$, use $x_1=1,z_j=0$ and override its output from 1 to 0. For $v_j$, use $x_1=0,z_j=1$ and override from 0 to 1. For $w_j$, use $x_1=0,z_j=0$ and override from 0 to 1. For $a_j$, use $x_1=0$ and override from 0 to 1. Each later identity layer transmits the perturbed signal, establishing output fault observability at every layer. Thus all gate records can be non-dead and counterfactually influential while an OBDD with **one** internal node tests only $x_1$. Every assignment matrix, across every partition and over every field, has rank one because $f=x_1$ is a product of one-sided factors. Its SAT verdict is YES and its exact input assignment count is $2^{n-1}$.

**High-cut-rank control.** On inputs $x_1,\ldots,x_r,y_1,\ldots,y_r$, $r\ge2$, first construct $D_r=\bigwedge_{i=1}^r(\neg x_i\vee\neg y_i)$ using precisely $4r-1$ NOT/OR/AND gates, then apply the same $k$ identity layers, cycling through the $2r-1$ non-first original inputs. The full circuit has $g=4r-1+4k$ distinct gates and $6r-2+7k$ input arcs. Every gate is live and fault-observable: for each base gate choose a violated matching pair with all other pairs disjoint, and override that gate at its logical decision point; for a wrapper selector $z$ the $r\ge2$ condition supplies assignments with $(D_r,z)=(1,0),(0,1),(0,0)$. Its assignment matrix across the grouped $x:y$ cut has rank $2^r$ over every field, by the determinant-one tensor factor $\begin{psmallmatrix}1&1\\1&0\end{psmallmatrix}$. Yet it has an interleaved shared read-once BP with $2r$ internal nodes, while the SAT verdict is YES and the exact input count is $3^r$. The wrapper does not change any of these facts. This is a hostile **legal cheap representation**, not a claim that the grouped-rank matrix becomes small.

## Exact functional CNF and compression tax

Introduce one auxiliary variable per gate. For $t=\neg a$ use $(\neg t\vee\neg a)\land(t\vee a)$; for $t=a\wedge b$ use $(\neg t\vee a)\land(\neg t\vee b)\land(t\vee\neg a\vee\neg b)$; for $t=a\vee b$ use $(t\vee\neg a)\land(t\vee\neg b)\land(\neg t\vee a\vee b)$. Require the final output with a unit clause. Each input assignment gives exactly one extension to all auxiliary variables, with that extension satisfying the output unit precisely when the original circuit outputs one. Fresh output variable IDs and topological order make the ordered clause lists duplicate-free. Clauses have width at most 3, and every declared variable occurs when the selector layers cover every input.

| Family | Gates $g$ | Arcs/wires | CNF variables $V$ | Clauses $m$ | Literal occurrences |
| --- | ---: | ---: | ---: | ---: | ---: |
| $x_1$ identity wrapper | $4k$ | $7k$ | $n+4k$ | $11k+1$ | $25k+1$ |
| $\mathrm{DISJ}_r$ plus wrapper | $4r-1+4k$ | $6r-2+7k$ | $6r-1+4k$ | $10r-2+11k$ | $18r-6+25k$ |

The DISJ literal count follows $2r$ NOT gates (4r occurrences), $r$ OR gates (7r), $r-1$ AND gates (7r-7), the wrapper (25k), and the unit output clause (1), totaling $18r-6+25k$. The executable independently sums actual literal occurrences. In both families $m\le4V$ for the stated domain. Encoding each wire index in binary costs $O(\log(n+g))$ bits, hence the explicit circuit and CNF take $O((n+g)\log(n+g))$ bits, not $O(n+g)$ binary bits. This unique-extension count preservation is strictly stronger than mere equisatisfiability, but **still increases CNF-variable count to $V=n+g$**.

For $k=n^2$, the identity-wrapper source has $g=4n^2$, $V=4n^2+n$, $m=11n^2+1$, yet a fixed deterministic recognizer can check the canonical indexed grammar using polynomially many bit operations, infer $f=x_1$ by the explicit four-gate identity, and output YES or the exact $2^{n-1}$ in polynomial input time (binary output has $n$ bits). Likewise it recognizes the DISJ base and computes $3^r$ by ordinary polynomial-time integer multiplication. A correct total solver can use this fast path and exhaustive fallback on other inputs. These are genuine cheap paths. One must charge the entire grammar scan and cannot infer sublinear *input-reading* time; nevertheless no rule can require evaluating every syntactically essential gate or paying rank as an intrinsic SAT-decision resource.

## Mandatory four gates

| Gate | Classification and exact reason |
| --- | --- |
| DISJ sanity | **PASS restricted, FAIL unrestricted naive transfer.** $D_r$ retains rank $2^r$, but has a $2r$-node interleaved BP and $O(r)$ circuit; all-live fault-observable wrappers leave it easy. No rank-to-general-circuit claim is made. |
| Relativization | **PASS for local Boolean identities and syntactic encoding; OPEN for any unrestricted separation.** No nonrelativizing P-vs-NP step was constructed; algebrization and Natural Proofs remain audits for any future proposed step. |
| Simultaneous DTISP | **NOT APPLICABLE** to this restricted circuit/BP size falsifier. The canonical-family recognizer uses one polynomial-time and polynomial-space implementation, counting parser, indices, arithmetic, and output; no strict FLMV forbidden-box realization is supplied. Unrestricted matched-machine transfer **OPEN**. |
| Configuration count | **PASS upper-bound guard only.** Deterministic read-only-input total deciders obey $T\le2^{O(s+\log N)}$ under the standard finite-tape hypotheses; the bound is never used as a work lower bound. |

## Same-realization resource ledger and controls

* Circuit constructor: $g$ node records, $7k$ wrapper input arcs, arbitrary reused selectors, fanout from each previous signal to two next gates. Shared gates counted once; there is no implicit tree unfolding. Direct construction is $O(g)$ word-record operations, $O(g\log(n+g))$ bit output.
* CNF construction: $V=n+g$ counted variables, $m$ explicit clauses, all clause and literal writes charged. Counting-preserving (one extension on accepting originals), not a general solver reduction with $V=O(n)$ for $g\gg n$.
* Certified recognizer: scans and checks the source grammar and parent indices, uses at most polynomial time and $O(N+\text{output bits})$ workspace in one fixed ordinary deterministic implementation; $N=O((n+g)\log(n+g))$ bit encoding. For output $3^r$, bit length is $O(r)$. Other inputs may take exponential time in the total correct fallback.
* OBDD: $x_1$ has a one-test shared program; DISJ interleaving has $2r$ internal tests with $2r-1$ side switches and at most $2r$ tests per original assignment. The physical cost of materializing, accessing and running the diagram is not suppressed in any claim.
* Dynamic/circuit-to-cut transfer: cost-underestimating symbolic simplification is legitimate, and rank of the final fixed function may be 1 or $2^r$ independently of $k$. Gate-fault observability is not a proof that input semantics require the gates. Actual runtime lower bounds must count legal normalization, recomputation, circuit shortcuts, partial evaluation, and wire taxes.
* Hostile controls: Horn, 2-SAT, product, affine/Gaussian, equality, all-zero witness, padding, variable renaming, auxiliary variables, low-treewidth and autarkies remain legal. The two examples are a singleton-function circuit and a Horn/2CNF DISJ circuit. They are **not** representative unrestricted hard 3SAT instances.

## Executed evidence and corpus reconciliation

**Native Node, deterministic** revision \`tmr4-observable-live054.v1\`, no seed: 23 complete circuits, 42,079 assertions, 1,280 original assignment evaluations, 39,200 single-gate fault replays, 40,480 Tseitin satisfiability checks, 138,496 exhaustive auxiliary assignments on small circuits, **zero failures**. The finite checks are COMPUTATIONAL. Published source \`experiments/tmr/tmr4_observable_live054.js\`; immutable raw \`results/raw/tmr/2026-11-15_1511_TMR4_OBSERVABLELIVE054_NODE_RAW.json\`. Local source SHA-256 \`0cef1afa6e4f31212a90e40cb342daa37ce06248eadcdf61eb8f30ede75b90c3\`; raw SHA-256 \`e096b5f5b576d5c43d631f4599e0a341bb250d7029f62ba318d6252b07a6f45e\`. Independent peer proof checking OPEN.

Corpus: governing directive first (SHA 7b8804dc); TMR-4/051-053 originals; TMR-5/050 original one-switch rank and code; TMR-2/052-053 zeta/selector originals; TMR-1/053 and #SAT normalized input constraints; five current handoffs; root proof1 full SHA 06f7ebc8, root proof2 metadata SHA 930c5eed and root main.tex metadata SHA 6ac34c5d with empty returned bodies; AGENTS.md, CODEX.md, project skill, and issue #3. Bryant (1986) branching diagrams: https://doi.org/10.1109/TC.1986.1676819 ; OpenAI October 25, 2026 primary preprint: https://github.com/openai/math/tree/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026 ; source original TMR-1/053 and TMR-5/047 circuit-to-CNF guard. The identity wrapper is a direct elementary Boolean construction; no new external-priority claim.

**Duplication/contradiction audit:** TMR-4/053 already proves an adaptive switch transcript rank bound; TMR-5/050 proves an exact one-switch DISJ bound, and TMR-5/047 identifies dead-gate pruning. This new construction strengthens the *dead-gate* control to all-live **fault-observable** gate records and explicitly pays the functional CNF/wire tax. It does not modify either earlier theorem. The novelty is relative to the repository's tested safeguards, not a claimed new circuit-complexity theorem.

**Root reconciliation:** proof1.txt was accessible, whereas the connector returned metadata-only/empty bodies for proof2.txt and main.tex. No shared root region was altered. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** Historical /341 full logical UNSAT authority remains FAIL; /386 remains RESTRICTED. All five existing tasks, schedules and ownership unchanged.

**One next lemma:** Characterize a nontrivial circuit subclass admitting a polynomial-size *bounded-switch* shared BP compilation when input formula/circuit graph discovery and wire access are paid. The DISJ interleaving and the live-gate wrapper must remain hostile controls; unrestricted circuit transfer OPEN.
