# TMR-4/012: exact cost-sound parallel-head spatial MAY distance

**Date:** 2026-11-13 21:40 PST (America/Los_Angeles). **Role:** TMR-4, Cost-Sound Abstraction. **Repository:** j15marti/pnp, main.

**Scientific status:** New theorem TMR4-PH12 is **CANDIDATE pending TMR-5/TMR-1 independent review**. Exhaustive finite graph checks are **COMPUTATIONAL**. Independent mathematical review finds TMR-1/011's one-head result internally correct at **PROVED/RESTRICTED** scope. The all-exponent 3-SAT lower bound and P versus NP remain **OPEN**.

## 1. Exact target and relationship to prior work

TMR-4/009 and independent TMR-5/008 established the input-head plus observed-source-set MAY abstraction and its left-aligned $O(L)$ ceiling. TMR-1/011 generalized the exact abstract shortest-path formula to **one** local input head starting at an arbitrary input position. TMR-1/011 explicitly warned that a one-head formula is wrong for multiple dispersed heads. This run independently checks its proof, derives an exact **arbitrary finite number of parallel local input heads** formula, and audits its all-edge potential by native Python execution.

A fixed correct total deterministic multitape decider $A$ runs uniformly over all binary input lengths. Its read-only source has $L$ encoded bits, not $L$ variables or clauses. The input interface has a fixed $h\ge1$ read-only heads in data positions $H=(p_1,\ldots,p_h)$, each reading its **pre-move** cell and moving at most one position per charged transition. Finite program/control, fixed alphabet, all writable work tapes, heads, intermediate representations, cached input, indices, recomputation, precomputation, and arbitrary source rereads are part of the actual concrete machine and charged. An outside-endmarker visit can be represented by a non-observing local step; the mathematical formula is for the declared data-cell start positions. The model does not include free indexed source jumps.

For a fixed valid source $x\in\{0,1\}^L$, choose *independently certified* opposite-label, valid, same-length sources $y_i$ and difference sets $D_i=\{p:x_p\ne(y_i)_p\}\ne\varnothing$. These are external mathematical witnesses, not instructions or an oracle for $A$. The abstract state $(H,V)$ retains the head positions and a ghost set $V$ of source bits previously observed by the concrete execution. It deliberately forgets all writable configurations. A paid MAY edge of cost 1 can move each head locally and observe any subset of the pre-move data positions. Zero-cost stutters are permitted. Each of the SAT and UNSAT goal edges has abstract cost 0 and is guarded by $V\cap D_i\ne\varnothing$ for **all** $i$.

## 2. New exact multihead theorem TMR4-PH12

Define the unhit supports at state $(H,V)$ as $\mathcal U(V)=\{D_i:D_i\cap V=\varnothing\}$. If this collection is empty, set $\Psi(H,V)=0$. Otherwise, for head $j$, choose an interval $I_j=[a_j,b_j]$ satisfying $0\le a_j\le p_j\le b_j<L$, and define

$$
c_j(I_j,p_j)=(b_j-a_j)+\min(p_j-a_j,b_j-p_j).
$$

Then the **exact** minimum-cost MAY decision path from $(H,V)$ is

$$
\boxed{
\Psi(H,V)=1+
\min_{\substack{I_j=[a_j,b_j]\ni p_j\\
\forall D\in\mathcal U(V):\
D\cap\bigcup_{j=1}^h I_j\ne\varnothing}}
\max_{1\le j\le h}c_j(I_j,p_j).
}
$$

**Lower bound.** Consider any abstract accepting or rejecting path of $t$ paid steps. For each head, form $I_j$ from its starting position and every data position that head actually read during the path. Every unhit support must have a read coordinate in one $I_j$, so the intervals cover every support. A locally moving head beginning at $p_j$ must travel at least $c_j$ moves to reach the two extremes, and the last extreme must be read during a paid pre-move step. Therefore $t\ge 1+\max_jc_j$. Taking the minimum over all admissible interval choices proves the lower inequality. Zero-cost stutters and subset observations cannot weaken the argument.

**Upper bound.** Choose intervals attaining the finite minimum. Head $j$ first travels to its nearer endpoint and then traverses to the other endpoint, observing every interval coordinate, including a final pre-move read. Its required transitions are precisely $c_j+1$. The other heads move simultaneously and may wait at positions without penalty beyond the shared transition. At most $1+\max_jc_j$ charged steps suffice for **all** heads to cover all selected intervals. Every support has been observed, enabling the appropriate zero-cost abstract goal edge. This is an abstract MAY path, not a claim of a physically realizable SAT-solving computation.

**TMR-1/011 review and special case.** For $h=1$ this formula reduces *exactly* to TMR-1/011's interval expression. With $h\ge2$ and dispersed starts it can be strictly smaller. In particular $L=11$, $D_1=\{0\}$, $D_2=\{10\}$ gives cost 16 from a **single** head at 5, cost 11 for two heads both at 0, and cost **1** for two heads respectively at 0 and 10. Therefore importing the one-head expression into a multihead machine is unsound.

## 3. Concrete simulation, both terminal labels and every-edge potential

**Initial binding:** Map the complete actual starting configuration (program, tapes, finite control, heads, fixed source) to $(H_0,\varnothing)$, before the first read. The source $x$ and witness sources $y_i$ are fixed mathematically, not chosen by the abstract run.

**Every physical step:** Any concrete step, including a step spending all its work on compact algebra, source copying, encoding, work-space writes or rereads, has a one-step MAY image of abstract cost 1, with the same pre-move source positions observed and the same (possibly clipped) local source-head movements. Any unobserved work-tape behavior is conservatively included. Thus **every related concrete state and every successor** has a related abstract successor at cost no greater than the concrete increment. No solver template is required.

**Both terminals:** If a correct concrete run on $x$ halted without observing any member of some $D_i$, the deterministic run on opposite-label $y_i$ would have identical scanned symbols, control, all work-tape contents, all head movements and the same terminal answer, a contradiction. Thus the actual run hits every certified support, enabling its **correct** abstract SAT or UNSAT goal. It follows that

$$
d_{\rm MAY}((H_0,\varnothing),\mathrm{goal})\le T_A(x).
$$

**Every abstract edge:** Since $\Psi$ is an explicit finite interval minimum independent of the unknown runtime of $A$, it equals the shortest remaining MAY goal distance. Prefixing any cost-1 abstract step to an optimal continuation proves $\Psi(u)\le1+\Psi(v)$ on **every** paid edge, including parallel moves, selective observations and no observations. Zero-cost stutters preserve $\Psi$; guarded zero-cost goal edges originate where $\Psi=0$, and $\Psi(g_{\rm SAT})=\Psi(g_{\rm UNSAT})=0$. Therefore the all-edge inequality $\Psi(u)\le c(u,v)+\Psi(v)$ holds everywhere and telescopes to $\Psi(H_0,\varnothing)\le T_A(x)$. This potential is an explicit finite combinatorial formula, **not** $T_A(x)$ in disguise.

**Sharp limitation:** A single head can always sweep the entire $L$-bit input, regardless of supports; therefore even this exact parallel-head MAY lower bound satisfies

$$
\Psi(H_0,\varnothing)\le L+\min_j\min(p_j,L-1-p_j)
\le L+\lfloor(L-1)/2\rfloor<3L/2
\quad (L\ge2).
$$

This is an **expressivity ceiling for the lower bound**, not an upper bound on actual SAT runtime. Adding all opposite-label sources, exponentially many difference supports, or additional unrestricted writable memory cannot increase the MAY minimum beyond this sweep. Source-observation certificates alone cannot prove an $\omega(L)$ processing lower bound, much less an all-exponent SAT lower bound.

A fictitious free one-step jump from source position 0 to 10 with a read at 10 would violate the locally moving potential: $11\not\le1+0$. That transition is forbidden by the declared physical model. Conversely, the genuine paid sequential scan is a permitted cheap abstract path and **must not be deleted** by a putative CEGAR refinement without a replay proof of spuriousness against the specific fixed program.

## 4. Executed tests and hostile controls

**Published-exact native CPython 3 verification** used the source at \`experiments/tmr/tmr4_multihead_interval012.py\`, seed \`202611132136\`. The generator enumerates interval-cover combinations independently of breadth-first shortest paths through the paid physical-head MAY graph. It compares optimal costs on 212 seeded and explicit instances with one, two or three independent local heads and 2 to 11 source positions. It additionally checks the exact potential inequality across all 39,008 enumerated allowed selective-observation paid edges on selected small instances, including visited-set combinations and zero-potential terminal guards.

Raw results: **212** formula/BFS comparisons, **139** multihead cases, **73** one-head cases, **2,080** BFS states, **5,795** BFS edges, **39,008** paid-edge potential inequalities, **7** explicit hostile/boundary controls, **0 failures**. Test controls distinguish one versus two heads with dispersed starts; initial versus completed source observations; leftmost transport; and illegal free indexed jumps. The executable prints JSON and takes an optional output filename. Its published Git blob hash was checked against the natively executed source, \`135a5e45848b0f517da315a4499511d9b8abbf9a\`. No instruction-level SAT multitape simulator, general SAT fallback, or full repository preflight was executed. Finite tests are **COMPUTATIONAL**.

Source: \`experiments/tmr/tmr4_multihead_interval012.py\`. Immutable raw: \`results/raw/tmr/2026-11-13_2139_TMR4_MULTIHEAD_INTERVAL012_RAW.json\`.

## 5. Scope, literature, original failures and next target

This extension is a mathematical identity in the source/head MAY graph, with an unrestricted **work-tape** all-transition simulation for machines having the declared local input interface. It does **not** transfer to constant-cost random-access input, a growing number of program-dependent input heads, post-move free observations or a chosen solver calculus. Both SAT/UNSAT labels are represented, but terminal MAY permission does not compute either label in concrete time. The polynomial authenticated two-label block-mask classifier of TMR-2/010 remains a direct hostile countermodel to claims that high certificate complexity implies expensive global consistency processing. Horn-SAT, 2-SAT, XOR/Tseitin Gaussian elimination, bounded-treewidth DP, products, sharing, padding, auxiliary-variable constructions, caching and recomputation remain allowed.

The original historical LSPV-5/479 **negative-zero ID alias**, /511 **accepted string support path** and /514 **typed/edge-suffix normalizer** were reviewed as concrete checker/normalizer counterexamples or restricted prior results. A native checker accepting a concrete path must not be repaired by simply excising it. Those legacy checker phenomena are not an unrestricted machine-computation bridge.

Primary literature verified for scope:
1. Cousot and Cousot (1977), *Abstract Interpretation: A Unified Lattice Model*, POPL, https://doi.org/10.1145/512950.512973, gives the general overapproximation motivation, **not** the new interval identity.
2. Buhrman and de Wolf (2002), *Complexity Measures and Decision Tree Complexity*, TCS 288, 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X, treats decision-tree and certificate complexity rather than physical SAT processing.
3. Fortnow, Lipton, van Melkebeek and Viglas (2005), *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865, https://doi.org/10.1145/1101821.1101822, establishes simultaneous restricted time-space exclusions, not an unrestricted all-polynomial-workspace separation.

**Corpus preflight:** replacement directive was read FIRST and rechecked, SHA \`47459817e66dccf1f3079e6c724c0fd2643e7bc4\`. Full proof1.txt (28,714 characters, SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`) and **full authoritative proof2 Git blob** (1,051,196 characters, SHA \`930c5eeddafce656717f28055a7a9a755f44737c\`) were recovered. The ordinary proof2 contents response was misleadingly blank. Full root main.tex Git blob (2,507,300 characters, SHA \`c0d657568af18ed0a2d17843b8ef0e6c11ac6327\`) was similarly recovered despite its blank contents response. Read issue #3 through TMR-3/010, AGENTS.md, CODEX.md, pnp-research skill, all newest TMR handoffs, TMR-1/011, TMR-5/008, TMR-4/009, TMR-2/011, TMR-3/010, and relevant original failed checker/normalizer artifacts. Older LSPV allocation language is superseded by the 12:49 PST TMR directive; historical mathematics and counterexamples remain valid data.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No tracker update is warranted by an $O(L)$ source-transport result. Root main.tex is unchanged; TMR-5 owns final whole-document synthesis. No scheduled tasks were created, modified or revived.

**One next target:** Construct a full-machine program-aware potential that cannot terminate merely by observing all input positions, and rigorously replay any cheap abstract counterpath against the particular fixed decider before refining. Its all-transition correctness and superpolynomial initial value for every correct decider are **OPEN**. The strict team quantifier target remains, for every fixed correct total $A$, every integer $k\ge1$, $C>0$, $L_0$, some valid $x$ with $|x|\ge L_0$ and $T_A(x)>C(|x|+1)^k$.

END_OF_REPORT::TMR4::PARALLEL_HEAD_INTERVAL012::2026-11-13_2140_PST
