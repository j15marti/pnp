# TMR-4/036: Directed-zero scalar closure preserves correlated tariff information

**2026-11-14 20:39 PST** | **SCALAR-CLOSURE056** | TMR-4 PNP Cost-Sound Abstraction

**Status:** PROVED/RESTRICTED for the explicitly specified inference-priced transition protocol. 76,698 native CPython check groups and a separately reconstructed 2,166-row V8 matrix are COMPUTATIONAL evidence. Independent TMR-5/TMR-3 mathematical audit OPEN. Full SAT-machine and proof-calculus transfer OPEN. **P versus NP OPEN.**

## 1. Candidate and four falsifiers fixed before source review

**Candidate:** zero-cost SCC collapse plus componentwise-minimum closure, as used safely in TMR-4/035, can lose a substantial tariff even when an exact weighted scalar potential survives all zero-cost moves. Replace it with the greatest zero-edge-isotone scalar minorant of a fixed weighted raw obstruction vector, then independently check every paid edge.

Falsifiers: (F1) an authentic zero edge decreases the scalar; (F2) a paid edge discharges more weighted potential than its price; (F3) a compact fused operation completes several tasks in one paid step; (F4) a genuine zero-cost completion reaches the goal. F1 is excluded by proof; F2 is exhaustively checked in the base model. F3 and F4 are real shortcuts in explicitly enlarged models and are retained, not refined away.

**Preflight and originals:** controlling fusion directive blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6 read first; November 13 TMR replacement; proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 (28,714 characters); proof2 authentic Git blob 930c5eeddafce656717f28055a7a9a755f44737c (Contents API returned an empty string); root main.tex authentic blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (Contents API also returned empty); AGENTS, CODEX, repository skill, five newest TMR handoffs and issue #3 through TMR-3/035. Relevant originals inspected: TMR-4/035 exact SCC/LP and Python; TMR-3/035 COMPACTFAN056; TMR-2/035 AFFQUOT055; TMR-1/035 Q-TM/Q-RES-H; TMR-5/031 independent fusion replay; LEAD-0029 Lipschitz falsifiers and LSPV-3/615 original checker counterexample. /341 remains FAIL on its accepted language; /386 is RESTRICTED. Neither serves here as a logical authority.

**Primary conceptual references, no claim of priority:** Cousot & Cousot, Abstract Interpretation, POPL 1977, pp.238-252, DOI https://doi.org/10.1145/512950.512973 (order-theoretic collecting semantics); Hoffmann et al., Two Decades of Automatic Amortized Resource Analysis, Mathematical Structures in Computer Science 2022 (local operational cost and potential discipline). All claims below follow from elementary direct proofs, not from importing a resource lower bound.

## 2. Exact finite-graph zero-closure theorem

Let G=(V,E0,E+) be a finite directed graph with authenticated zero-cost edges E0 and paid edges E+. Let p:V -> Q_{>=0}^d be a raw vector and lambda >=0 a fixed rational weight vector. Put q(v)=lambda.p(v) and Z(v)={u: v ->0* u}, the entire directed zero-reachability set, **not just the zero SCC**. Define

$$
h_\lambda(v)=\min_{u\in Z(v)}\lambda^\top p(u).
$$

**THEOREM (PROVED/EXACT, finite graph):** h is the pointwise greatest scalar function g satisfying g(v)<=q(v) for all v and g(v)<=g(u) on every authentic zero-cost edge v->u. It is constant on SCCs. If in addition every paid edge obeys h(v)-h(u)<=w(v,u) and every completed goal has h(goal)<=0, then h(initial) is a lower bound on the price of every completed concrete path.

**Proof:** For any zero edge v->u, Z(u) is a subset of Z(v), so min_{Z(v)}q<=min_{Z(u)}q. Since v belongs to Z(v), h(v)<=q(v). For any other g satisfying the two requirements, follow any zero path v->0* u: g(v)<=g(u)<=q(u). Minimize over all u to get g(v)<=h(v). Mutual reachability gives equality on SCCs. The paid inequality and the zero inequality telescope along every concrete execution and the goal value is <=0. QED.

The prior componentwise closure uses

$$
\widetilde p_j(v)=\min_{u\in Z(v)}p_j(u),\qquad
\lambda^\top\widetilde p(v)\le h_\lambda(v).
$$

The inequality can be strict because **different coordinates attain their minima in incompatible zero-reachable normal forms**. The componentwise closure is sound but may be unnecessarily weak. This is a new, explicitly tested application relative to the prior project implementation, not a claim that the general order-theoretic construction is novel.

**Optimization caveat:** h depends piecewise linearly on lambda, so a single ordinary linear tariff LP with predetermined delta rows is not automatically equivalent to optimizing these scalar-closed potentials. Enumerate finite active-minimizer chambers or use a correct disjunctive formulation, and always verify every actual edge exactly. For this particular protocol the entire feasible cone can be proved symbolically.

## 3. Qualified concrete system and exact seven-column tariff

For each integer n>=1 the state is (z,t), where z is an n-character string over {U,L,R,D} and t in {0,1} is a redundant tag. Each position is one separately required AND obligation; U means unchosen normal form, L/R are two alternative free representations, and D means *paid discharged*. A completed goal has z=D^n, either tag. This is an explicitly bounded inference-priced event protocol, NOT a physical Turing machine or a 3-SAT verifier.

Exact native rule inventory:

| Rule | Applicability | Effect | Price |
| --- | --- | --- | ---: |
| free_alias_toggle | all states | change tag | 0 |
| free_choose_L / free_choose_R | position is U | change it to L or R | 0 |
| paid_discharge | position is L/R | change it to D | 1 |
| paid_malformed_nop | nonterminal | stay unchanged | 1 |

The complete abstract graph contains the exact same states and transitions at the exact same charges (identity simulation). Every concrete edge maps to a one-edge abstract path of equal cost, preserving goal identity and all remaining obligations. Tag toggles form SCCs of size two; there are 4^n SCCs. Directed free choices have no reverse edge, so they are NOT collapsed as SCC equivalences.

Use the seven requested coordinates (CNF, XOR, separator, fusion, Gamma, interface, machine), with only Gamma and interface nonzero:

$$
p_\Gamma(z)=2|\{i:z_i\in\{U,R\}\}|,\qquad
p_{\mathrm{int}}(z)=2|\{i:z_i\in\{U,L\}\}|.
$$

Take lambda=(0,0,0,0,1/2,1/2,0). One U task has raw pair (2,2). Its zero-reachable L and R forms have (0,2) and (2,0). Therefore the componentwise minimum is (0,0), although none of those states has completed the task. The scalar zero closure instead has value exactly one on U/L/R and zero on D.

For n independent AND tasks:

$$
\boxed{h_\lambda(z)=|\{i:z_i\ne D\}|,\quad
h_\lambda(U^n)=n,\quad
\lambda^\top\widetilde p(U^n)=0.}
$$

Every free step preserves h, every paid_discharge reduces h by exactly one, and every malformed paid no-op reduces h by zero. Goals have h=0. Each task requires one and only one paid discharge in this exact rule inventory, hence the shortest paid path costs exactly n, matching the bound.

**Entire exact rational tariff cone for all n in the base protocol:**

$$
\boxed{0\le\lambda_\Gamma\le 1/2,\qquad 0\le\lambda_{\mathrm{int}}\le 1/2.}
$$

Necessity: one isolated R completion discharges 2 lambda_Gamma, and one isolated L completion discharges 2 lambda_interface, each for price one. Sufficiency: zero edges are scalar monotone and the only useful paid steps discharge one selected task. All other columns are zero and their nonnegative weights are unconstrained in this qualified model.

The separately published machine-readable CSV contains every one of the 2,166 authentic edges in all three n=3 variants, with seven raw deltas, scalar closed delta, exact charge and slack. The standalone Python reproduces the full edge matrices for all n=1..5.

## 4. Two real hostile model extensions

**Paid FUSE_ALL:** add an authentic one-step price-one transition from any nonterminal state to the completed goal. For n>1 the base potential fails: explicit n=3 transition (UUU,0)->(DDD,0) discharges **3** for a charge of **1**. The new minimum is one. The new exact cone is

$$
\boxed{0\le\lambda_\Gamma,\lambda_{\mathrm{int}}\le 1/(2n).}
$$

Proof: selected all-R or all-L states require 2n times the corresponding coordinate weight <=1; conversely every state has scalar h<=2n max(lambda_Gamma,lambda_interface)<=1 and the other paid steps respect their tariffs. Taking both weights 1/(2n) certifies the correct initial cost one. Across unbounded n, no positive length-independent weights survive the legal FUSE_ALL.

**Zero-cost FREE_ORACLE:** add a zero edge from every nonterminal to the completed goal. Then every zero-reachability set contains a goal of raw weight zero, so h is identically zero for all nonnegative weights, matching the authentic zero-work execution. The counterexample must not be erased by CEGAR.

These are genuinely *changed model inventories*. They do not imply a free SAT oracle exists. They demonstrate that the chosen tariff must be recalibrated when authentic fusion, compact operations or zero completion enter the concrete system.

## 5. Executions, source, and limitations

**Native CPython run:** fractions.Fraction, Tarjan zero SCC, complete directed BFS zero closure, reverse Dijkstra exact minimum paid work, exhaustive edge inequality checks and 324 exact rational-grid weight comparisons. For n=1..5 and each of base, paid FUSE_ALL, free oracle: **76,698 assertion/check groups, zero failures**. At n=5 the base system has 2,048 states, 14,334 edges, scalar potential 5, componentwise potential 0, and exact minimum 5; the paid FUSE_ALL system has 2,016 real violations under old weights and true minimum 1. Finite tests are COMPUTATIONAL; the symbolic proofs establish all-n statements.

**Independent V8 check:** reconstructed all n=3 transitions and raw seven-delta rows from separate code, matching the native outcomes: base 638 edges/0 violations; paid fusion 764 edges/108 violations; free oracle 764 edges/0 violations. This independently regenerated the published complete 2,166-row CSV, not a compiled physical TM.

Published paths:
- experiments/tmr/tmr4_scalar_closure056.py (standalone reproducible exact implementation, lightly reformatted from the natively executed prototype, not asserted byte identical).
- results/raw/tmr/2026-11-14_2039_TMR4_SCALAR056_NATIVE_RESULTS.json (faithful compact transcription of native output, not the original stdout bytes).
- results/raw/tmr/2026-11-14_2039_TMR4_SCALAR056_TARIFF_ALL_EDGES.csv (independent exact 7-column, all-edge matrix).

**Hostile-scope firewall:** No free physical work on a Turing machine is asserted. The source is an AND-obligation laboratory rather than SAT; Horn, 2-SAT, affine, autarky, separator dynamic programming, learning, compact circuits, arbitrary rereading and extension-variable steps are not part of the qualified base protocol. They are conservative MAY when transferring to arbitrary SAT machines. No superpolynomial initial gap exists here: the base potential is n and true cost n, while fusion reduces true cost to one. /341 FAIL and /386 RESTRICTED historical guards remain unchanged.

## 6. Dependency status and peer request

| Obligation | Status |
| --- | --- |
| Exact finite zero SCC and directed zero closure | PROVED/RESTRICTED |
| Maximal scalar zero-edge minorant | PROVED/EXACT, finite graph |
| All-edge base certificate and goal preservation | PROVED/RESTRICTED |
| Paid fusion and free-oracle shortcuts | PROVED/RESTRICTED |
| Generic scalar-closure optimizer over arbitrary lambda | OPEN |
| SAT-specific fusion-safe superpolynomial initial gap | OPEN |
| Same-system simulation of every correct SAT machine | OPEN |
| P versus NP | OPEN |

**Next target:** combine TMR-2/035's public-affine quotient with an actual specified proof DAG having two nonconfluent free normal forms. TMR-3 must enumerate cheap multi-discharge mechanisms. TMR-5 must independently verify the all-edge cone and the FUSE_ALL path before any status promotion. A dynamic scalar reduced-product obstruction for unrestricted SAT remains unconstructed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither proof tracker nor root main.tex was changed; the five existing TMR schedules were not changed.

END_OF_REPORT::TMR4::036::2026-11-14_2039_PST
