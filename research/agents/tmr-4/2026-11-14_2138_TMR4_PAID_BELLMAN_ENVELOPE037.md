# TMR-4/037: Paid Bellman closure of a nonlinear minimax obstruction

**2026-11-14 21:38 PST | PAID-ENVELOPE060 | PNP Cost-Sound Abstraction**

**Scientific status:** PROVED/RESTRICTED for the exact finite hidden-source query transition systems and the all-q symbolic family. Native Python enumeration is COMPUTATIONAL, not an asymptotic SAT result. This is an independent new **paid-path closure characterization** applied to TMR-2/036; TMR-2 previously established the distinct minimax-versus-certificate fact and the exact linear tariff cone. Neither SAT/UNSAT general machine lower bounds nor a superpolynomial gap follow. Independent peer review OPEN. **P versus NP OPEN.**

## 1. Candidate and fixed falsifiers

**Candidate:** Authentic directed zero-cost closure by itself cannot repair the nonlinear worst-case decision-depth obstruction W from TMR-2/036. Saturating *all paid as well as zero-cost paths*, in the precise Bellman sense, gives the greatest sound scalar lower-bound potential that never exceeds seed W. The paid closure may collapse to the easiest compatible certificate distance B, even though worst-case query complexity is q squared.

Preselected falsifiers: (F1) an actual paid read makes a previously large W vanish and invalidates the unscaled W tariff; (F2) a zero-cost alias or repeat observation changes the candidate potential; (F3) a one-price shared or compact gate supplies a shorter authentic path and invalidates a stronger inferred obstruction; (F4) the graph silently chooses read answers incompatible with a single fixed source or is transferred uncharged to a syntax-aware SAT machine.

## 2. Sources, priority, and duplication control

Read the controlling fusion directive first, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6, then TMR replacement, full root proof1, root proof2 recovered through authentic Git blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 chars), canonical main.tex through Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 chars), AGENTS, CODEX, the repository research skill, all five current TMR handoffs, and issue #3 through TMR-3/036.

Original claim/evidence inspected: TMR-2/036 research/agents/tmr-2/2026-11-14_2113_TMR2_NONLINEAR_MINIMAX_TARIFF_COLLAPSE036.md plus experiments/tmr/tmr2_minimax_tariff059.py; TMR-4/036 research/agents/tmr-4/2026-11-14_2039_TMR4_SCALAR_DIRECTED_ZERO_CLOSURE036.md plus experiments/tmr/tmr4_scalar_closure056.py; TMR-5/032 asymmetric fusion; TMR-1/036 actual SAT-machine versus native Resolution transfer obstruction; TMR-3/036 affine SAT cost control; LEAD-0029 original Lipschitz audit. Earlier LSPV-3/076 already established the worst-case q squared versus cheapest certificate q for AND-of-ORs, and is credited. No duplication claim is made for those facts.

Primary methodological background: P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977, pp. 238-252, DOI https://doi.org/10.1145/512950.512973. The new finite-graph characterization below is proved directly and does not import any assertion about abstract cost from the paper. The source-aware restriction is essential.

## 3. Qualified exact concrete/abstract system

For each q>=1 there is a **fixed hidden binary source** x in {0,1}^{q*q}. Its Boolean answer is an AND of q rows, each the OR of q source coordinates. Complete concrete state C=(q,x,sigma,tag,halt), with transcript sigma in {?,0,1}^{q*q} consistent with x on every known coordinate and redundant tag in {0,1}. Both SAT-like TRUE and FALSE outputs count as completed goals only when forced by transcript:

- FALSE if any row contains q observed zeros.
- TRUE if every row has at least one observed one.
- Otherwise undecided.

Legal native query-protocol operations are: paid READ(j), price exactly 1, when sigma_j is unknown, reveals the actual x_j; free TAG toggle, price zero, only changes redundant tag; cached repeated lookup, price zero (or physical reread price one), leaves transcript unchanged; paid NOP of price one. These classes are complete **for this selected query laboratory**. A source-independent free oracle, compact parity hint, uncharged source expansion, SAT syntax inspection, or arbitrary multi-read instruction is NOT part of this qualified system. In the unrestricted SAT system any such genuine operation remains MAY and would require a new calibration.

The exact abstraction alpha(C)=sigma forgets fixed x and tag. Its READ transition relation safely contains both 0 and 1 answers whenever sigma_j is unknown; each concrete transition maps to **one abstract edge of exactly the same price**. Authentic zero-cost SCCs are the two tag variants at each transcript, and the directed zero closure on the quotient is identity. Zero alias/repeat operations therefore never decrease W or B. Every concrete terminal maps to a terminal abstract state and has potential zero. This proves all-step cost-underestimating simulation *inside the qualified query protocol*, not from a general physical Turing machine.

## 4. New general paid-envelope theorem

Let G=(V,E,w) be any finite directed graph with w(e)>=0 and let f:V->R_{\ge0}. Define the authentic **paid-path envelope**

$$
\mathcal E_f(s)=\min_{s\overset{\pi}{\longrightarrow}t}
\left(w(\pi)+f(t)\right),
$$

where the empty path is admitted, all actual zero/paid edges are admitted, and costs sum along the path. Then:

1. 0<=E_f(s)<=f(s).
2. For every edge r:s->t, E_f(s)<=w(r)+E_f(t).
3. If h is *any* nonnegative scalar potential with h<=f and h(s)<=w(r)+h(t) on every edge, then h(s)<=E_f(s) for every state.
4. If every completed goal g satisfies f(g)=0, then E_f(g)=0.
5. Adding genuine legal edges can only weakly DECREASE E_f. It cannot justify a larger lower bound.

**Proof:** (1) follows from nonnegative costs and the empty path. For (2), prefix edge r to an optimal path from t. For (3), telescope h along any finite path, use h(t)<=f(t), and take the minimum. For (4), apply (1). For (5), minimization over a superset of paths cannot increase a minimum. The empty-path bound makes the result well-defined even with zero SCCs. QED.

This is the **greatest cost-consistent minorant** of f, not merely the greatest zero-monotone minorant h0(s)=min_{t in Reach0(s)} f(t) established in TMR-4/036. On a finite graph it can be computed by adding a terminal sink with edge t->sink of cost f(t), then taking exact nonnegative shortest paths. But if f is a computational hardness measure and the graph contains every authentic machine state, computing E_f may be as difficult as solving the original task. This is a soundness calibration, not a complexity breakthrough.

## 5. Exact application to the nonlinear AND/OR protocol

For undecided transcript sigma, let A be the set of active rows with no observed one, a=|A|, and u_i be the number of unread source bits in active row i. Define

$$
W(\sigma)=\sum_{i\in A}u_i,\qquad
B(\sigma)=\min\left(a,\min_{i\in A}u_i\right).
$$

At either completed label both W and B equal zero.

W is the standard worst-case adaptive decision-tree depth in this restricted protocol, a previously established result. B is the cost of the shortest **compatible** completion: set one unknown bit to one in each active row to force TRUE (a reads), or set all remaining unknowns to zero in one active row to force FALSE (min u_i reads). Both are genuine query traces for *some source input consistent with the current partial transcript*. The two different source-completion choices do not constitute a single machine's ability to control an oracle answer.

**NEW EXACT TRANSFER:** for the complete MAY abstract graph of compatible query answers,

$$
\boxed{\mathcal E_W(\sigma)=B(\sigma)\quad\text{for every q and every transcript}.}
$$

**Proof:** B(s)<=W(s) follows from the displayed definitions. For any query successor s' reachable at price one, B(s)<=1+B(s') because an optimal compatible certificate for s' can be preceded by that actual read; zero aliases leave B unchanged. Hence B(s)<=cost(path)+B(t)<=cost(path)+W(t) for every path, so B<=E_W. Conversely the explicitly described compatible certificate-completion path reaches a terminal goal after B(s) reads; W(goal)=0. Thus E_W<=B. QED.

In particular, initially

$$
W(?^{q^2})=q^2,\qquad
\boxed{\mathcal E_W(?^{q^2})=B(?^{q^2})=q.}
$$

The ratio q is unbounded. The zero-cost closure alone leaves W=q squared unchanged but the authentic paid-path consistency constraints reduce its maximum sound minorant to q.

## 6. Exact rational matrix and LP frontier

For any legal READ, Delta B<=1 and Delta W<=D_q=q^2-q+1. At the authentic frontier with q-1 observed zeros in one row, all other bits unread, reading its last zero completes FALSE and yields Delta(B,W)=(1,D_q) at price one. Consequently the **entire** two-component nonnegative linear-tariff cone is

$$
\boxed{\lambda_B\ge0,\quad\lambda_W\ge0,\quad
       \lambda_B+D_q\lambda_W\le1.}
$$

The necessity comes from the frontier; sufficiency from the two per-read upper bounds. Every zero-cost alias, repeated read and paid NOP satisfies the inequality. Completed goals have zero in both components. Exact witnesses include lambda=(1,0), (0,1/D_q), and (1/2,1/(2D_q)) when ordered (B,W). The initial linear-potential maximum is

$$
\max(q,q^2/D_q)=q.
$$

This cone and its q optimum were already obtained by TMR-2/036; here they serve as an **independent all-edge check** of the new general paid-envelope theorem, and establish that nonlinear E_W repairs the same overdischarge without inventing cost. Machine-readable symbolic rule matrix is published separately.

**Genuine violation:** q=3, transcript ???????00, READ coordinate 6 with answer zero, price one, drops W by 7 and B by 1. Raw lambda_W=1 overcharges by 6. No zero-cost SCC quotient can remove this authentic paid transition. The shortest paid-envelope repair yields B and respects this edge.

## 7. Executed code, native provenance, controls

The **exact published source** experiments/tmr/tmr4_paid_bellman_envelope060.py was natively executed in CPython before upload and independently hash-matched to the GitHub blob 241d6789317527738b4169ac06145154fe3e9424 (local git hash-object identical). Raw stdout results/raw/tmr/2026-11-14_2138_TMR4_PAID_ENVELOPE060_NATIVE_RAW.json matched local Git blob 13b1dde0c240866f20caff7290ad06a2d9b3bd43. This is native Python computation over a semantic query graph, **not a compiled finite-state Turing machine**.

Totals: 512,222 assertion groups and zero failures for q=1,2,3, examining respectively 3, 81, 19,683 canonical transcripts; 2, 152, 77,022 distinct READ edges **per redundant-tag choice**. Every state E_W=B, zero alias invariance, every paid edge E(s)<=1+E(t), all terminal states E=0, three exact rational dual weights, and frontier violations were checked. For q=3, 77,022 paid READ transitions per tag, with both real tags having the same abstract transcript.

Hostile controls: (a) zero-cost alias/tag SCC leaves E invariant; (b) cached rereads and paid no-ops do not increase the potential; (c) adding a **new** one-price source-result shortcut from the initial state, explicitly changing the model, reduces initial optimal cost to one; (d) adding a **new** zero-price oracle from the initial state reduces it to zero. (e) Shared OR-row resolution already encoded by B; duplicating unresolved rows as independent proof obligations would overcharge. (f) affine/Gaussian, Horn, Krom, bounded-treewidth, autarky, equality, compact circuits, extension variables and arbitrary syntax-aware preprocessing remain legitimate **MAY operations for the unrestricted SAT machine**; they are not silently excluded by transfer. An authenticated such operation requires recalibration, never CEGAR deletion of a real cheap path.

The finite enumeration validates code and scoped claims, not any asymptotic complexity lower bound. The all-q statements above rest on the self-contained proof.

## 8. Dependency map, weakest gap, next peer audit

- **PASS/RESTRICTED:** finite zero SCC quotient, identity all-step query-model simulation, two-label goal preservation, exact paid-envelope maximality, E_W=B, rational LP matrix.
- **FAIL:** zero-only closure makes worst-case minimax W a valid one-unit tariff; it fails on an authentic last-zero paid READ.
- **RESTRICTED:** hidden indexed-source query access is **not** syntax-aware arbitrary SAT execution, nor a physical single-tape/multitape model. Read-answer choice in the existential envelope ranges over compatible different fixed sources, rather than being controlled by a decider on one source.
- **OPEN:** uniform same-system transfer covering every fixed total correct SAT machine; all authentic legal operations and compact algebraic shortcuts; an initial potential exceeding every fixed input-length polynomial; fusion-safe multiscale composition.
- **Historical authority:** /341 remains FAIL as a full logical UNSAT checker; /386 remains RESTRICTED to its guarded tested fragment. Neither is used or repaired.

**Genuinely new relative to prior work:** the greatest **paid** cost-consistent minorant theorem is applied to the peer nonlinear minimax source graph, with a proved E_W=B identity, direct exact-rational executable verification, explicit distinction between compatibility across different hidden sources and one fixed input, and a general counterexample to treating zero-only scalar closure as sufficient to certify paid Lipschitz cost.

**Next target for TMR-4:** construct a source-authenticated, *same fixed input* state abstraction retaining the actual machine control and paid access/recompute ledger, and prove whether its maximal cost-consistent minorant contains any nontrivial residual nonlinear component after Gaussian elimination, learned clauses and shared reuse. TMR-2 should audit the B/W all-q proof and hidden-source quantifiers; TMR-3 should audit physical input-read pricing and graph-to-machine overhead; TMR-5 should hostile-test adding cheap algebraic operations and the authentic source restriction. No promotion beyond RESTRICTED before those checks.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1, proof2, root main.tex remain unchanged; no additional agents or schedule mutation.


## 9. Independent V8 all-edge matrix replay

A separate V8 implementation, not a wrapper around the CPython functions, exhaustively generated the **complete q=2 concrete transition inventory including both tag values** into results/raw/tmr/2026-11-14_2138_TMR4_PAID_ENVELOPE060_Q2_ALL_EDGES.csv. There are 704 legal edges: 162 zero TAG, 160 zero CACHE_REPEAT, 78 price-one NOP, and 304 price-one READ edges. It independently recovered maximum Delta W=3 and Delta B=1 and identified 88 concrete READ rows that violate a raw unit-weight W tariff. The seven-component columns and all-q exact symbolic tariff constraints are recorded in results/raw/tmr/2026-11-14_2138_TMR4_PAID_ENVELOPE060_SYMBOLIC_MATRIX.json. This second execution verifies the finite q=2 matrix independently; the unbounded-q claim rests on the proof in Sections 4-6.

END_OF_REPORT::TMR4::037::2026-11-14_2138_PST
