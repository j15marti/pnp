# TMR-1/043: An exact dynamic fusion-connectivity tariff, with a linear ceiling and a sparse-projection shortcut

**2026-11-15 03:57 PST (America/Los_Angeles).** Role: TMR-1 / PNP Machine Model Lead. Primary directive: research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md (blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6).

**Status:** PROVED/RESTRICTED for the precisely defined preauthenticated C-SEP fan-in-two shared-circuit calculus; mathematical peer review OPEN. Finite tests COMPUTATIONAL. This is NOT a native SAT Turing-machine lower bound. P versus NP OPEN.

## 1. Candidate and four precalibrated falsifiers

**Claim:** There is a genuine dynamic, fusion-safe reduced-product component that has an exact all-transition tariff and a matching minimum whole-DAG cost for a fully explicit proper-3CNF Craig-pair family. The component counts connected clusters of *input wires actually linked by paid gates*, not truth-table mass or a prescribed proof tree. Its exact initial gap is only linear, providing a positive but insufficient construction for the shared tariff program.

Four falsifiers fixed before consulting literature and project reports: (F1) a free gate or equivalent zero-cost source-linking rewrite decreases connectivity; (F2) an authentic cost-one wide-fanin gate or macro definition merges three or more input clusters; (F3) free output selection or shared sub-DAG reuse somehow supplies a separator before sufficient binary gates have been charged; (F4) a transfer to actual SAT computation incorrectly treats source-authenticated circuit construction, output gates, input reads or fixed-program uniformity as free.

F1 and F2 violate the tariff if explicitly added but are **NOT** legal rules of this qualified C-SEP calculus; they are mandatory controls for richer models. F3 is excluded by the graph proof below; arbitrary shared-fanout DAGs are legal. F4 remains OPEN and forbids SAT-machine promotion.

## 2. Explicit growing authentic proper-3CNF source pair

Let n>=2, X=(x_1,...,x_n). For a literal l and fresh distinct private y,z, define four proper width-three clauses

$$
G(l;y,z)=\bigwedge_{\sigma,\tau\in\{-1,1\}}
(l\lor y^\sigma\lor z^\tau).
$$

Its existential projection is exactly l: if l is false the four clauses exclude every value of y,z; if true all four are satisfied.

Let A_n=AND_{i=1}^n G(x_i;y_i,z_i). Thus projection U_n={1^n} and A_n has 4n ternary clauses.

Let B_n encode the chain o_2=(NOT x_1 OR NOT x_2), o_i=(o_{i-1} OR NOT x_i) for i=3,...,n; force its final o_n by G(o_n;u,v). Each OR gate o=(a OR b) has authentic Tseitin clauses (NOT a OR o), (NOT b OR o), (a OR b OR NOT o). Replace each binary clause (p OR q) by two proper width-three clauses (p OR q OR t), (p OR q OR NOT t) with a fresh t. All source identifiers are distinct where required. Each OR gate now uses five proper ternary clauses, and the terminal forcing gadget uses four. Therefore B_n has 5(n-1)+4=5n-1 clauses, with existential projection V_n={0,1}^n minus {1^n}.

The two private alphabets are disjoint, their common variables are exactly X, and the pair consists of 9n-1 proper ternary clauses on 6n-1 distinct variables. With ordinary binary literal identifiers, their total input length is N_n=Theta(n log(n+2)). Each side individually is SAT, and A_n AND B_n is UNSAT. U_n and V_n partition the complete shared cube, so TMR-1/041's independently established separator-lattice theorem gives **one extensional Craig interpolant**:

$$
I_n(X)=x_1\wedge x_2\wedge\cdots\wedge x_n.
$$

Uniqueness refers to Boolean truth tables, not to circuit syntax. No special-purpose SAT correctness checker is assumed.

## 3. Qualified C-SEP transition system and authentic zero closure

A complete state C=(A_n,B_n,G,q,h) has the fixed authenticated sources, an append-only acyclic shared Boolean gate DAG G with n free input wires and constant 0/1 wires, a selected output wire q (possibly absent), and a goal flag h. All gates have fan-in at most two, type AND or unary NOT. A globally distinct paid gate identity is charged once, regardless of fanout, reconvergence, reuse or how often its value is read. Inputs may be referenced arbitrarily many times for free within the abstract gate-building laboratory, not within a physical-machine implementation.

The **entire legal transition inventory** is:

1. APPEND_AND(u,v): append one fan-in-two gate with two existing predecessor wires; cost 1.
2. APPEND_NOT(u): append one unary gate referring to one existing predecessor; cost 1.
3. SELECT(q), including replacing the selected output, and reversible metadata switches/NOP: cost 0, *no gate creation or wiring change*.
4. GOAL: terminal when the selected DAG output separates the authenticated projections, i.e. evaluates to I_n on all shared inputs. Terminal states are absorbing. GOAL is a predicate, not an operation providing free correctness verification in a physical machine.

These are all legal transitions in R_CONN; no polynomial-time solver, arbitrary-width macro gate, free equality merge or oracle step is silently included. The zero-cost reachable states differ only in q and metadata. Their zero SCCs collapse all such presentations of the same exact G; no zero path changes the gate dependency graph.

## 4. Dynamic reduced-product component and complete tariff theorem

For any G, ignore edge directions temporarily and form the undirected dependency graph containing all n input vertices, constant wires, appended gate vertices and each gate-to-predecessor connection. Let c(G) be the number of connected components **among the n input vertices** in this graph (other constant-only components are not counted). Define

$$
p_{\mathrm{fus}}(C)=c(G)-1\ge0,\qquad
\mathbf p(C)=(0,0,0,p_{\mathrm{fus}}(C),0,0,0).
$$

This component depends on actual charged shared-DAG connectivity. It is not an entropy, assignment-count, source-rank or prescribed-tree invariant. Zero-cost closure preserves it exactly.

**All-rule theorem (PROVED/RESTRICTED):** Every legal paid APPEND_AND merges at most two previously distinct input-connected components, hence 0<=Delta_fus<=1. APPEND_NOT adds a unary descendant and cannot merge input components, hence Delta_fus=0. Every zero transition has Delta_fus=0. Every completed goal has c(G)=1, since I_n depends essentially on all n inputs and all n input vertices must be connected to its output in the gate DAG. Consequently the exact nonnegative tariff cone on this component is

$$
0\le\lambda_{\mathrm{fus}}\le1,
\qquad\lambda=(0,0,0,1,0,0,0)
$$

with lambda_fus=1 feasible and tight: APPEND_AND(x_1,x_2) on an empty graph discharges exactly one at cost one. The other six components are zero and have no asserted nonzero weights. This is an exact global matrix covering the specified rule classes, not just observed finite instances.

**Reason the fusion bound survives sharing:** A binary gate has two predecessor wires, each already attached to at most one input-connected component in the undirected partial DAG. Their new common gate vertex can merge at most these two components. Previously shared descendants, fanout and reconvergence cannot make a single binary gate merge a third disconnected component. Unary nodes cannot merge components. A completed output that depends on all input bits must have a directed path from every input, therefore all lie in the same undirected component.

**Telescoping:** For every legal execution C_0->...->C_t, p(C_0)<=sum_{i}w(r_i)+p(C_t). Since p(C_t)=0 at every goal, W>=p(C_0)=n-1, including all possible output-selection choices. Conversely append the n-1 gates x_1 AND x_2, then previous AND x_3, and so forth, select their final output for free, and reach the goal in n-1 paid steps. Hence

$$
\boxed{\min_{\mathrm{whole\ shared\ DAG}}W_{R_{\mathrm{CONN}}}(A_n,B_n)=n-1.}
$$

This is a **circuit-building** lower bound for an n-essential-input function, and emphatically not an unrestricted SAT execution lower bound. Since N_n=Theta(n log n), the initial gap is Theta(N_n/log N_n), never superpolynomial.

## 5. Sparse-projection universal shortcut (supporting theorem, not the main fusion component)

For **any** disjoint shared projections U,V subset {0,1}^n, let s=|U|. The characteristic function 1_U is always a valid interpolant, whether or not U union V covers the cube. A circuit can share at most n negated input wires, use at most n-1 AND gates per positive minterm, then OR all s terms using NOT/AND (De Morgan), with unrestricted fanout. For s>=1 the constructed AND/NOT gate count is at most

$$
\boxed{C_{\wedge,\neg}(\mathbf1_U)\le n+s(n+1).}
$$

For s=0 the constant-zero output costs zero gates. Therefore the minimum cost over **all legal separators** is at most this value, even when a different *selected* interpolant is circuit-hard. This extends the earlier project's sparse/co-sparse table synthesis control (scripts/sparse_cosparse_stream_escape.py, sparse-positive stream model) to an arbitrary disjoint CNF projection pair, unrestricted shared AND/NOT DAG and cheapest legal separator. No assumption of NP membership is needed.

For polynomial s(n)<=n^d this establishes a nonuniform O(n^{d+1}) general-circuit upper bound, ruling out a *superpolynomial* minimum general-circuit separator lower bound in that case. **Nonuniform hardcoding is not a uniform polynomial SAT decider.** It neither forbids a fixed n^{1+epsilon} lower bound below the upper exponent nor invalidates the known sparse-NP hardness-magnification literature.

## 6. Primary magnification source and exact scope boundary

Chen, Jin and Williams, FOCS 2019/ECCC TR19-118, study languages with up to 2^{N^{o(1)}} YES instances of input length N, **not necessarily polynomially many**. Their published conditional example states: for an L in NP with this sparsity, proving L outside Circuit[N^{1+epsilon}] for any fixed epsilon>0 yields NP not subset P/poly. They also provide model-specific analogues; their n^{1+epsilon}-time/n^{epsilon}-space/n^{epsilon}-advice threshold is a distinct stated result. The paper's MCSP input is a complete N=2^m-bit truth table; the relevant circuit threshold is expressed in the smaller arity m, and the number of YES truth tables is at most 2^{O(t(m)log(m+t(m)))} for threshold t(m), which becomes 2^{N^{o(1)}} when t(m)=2^{o(m)}.

The present elementary support upper bound for poly-sparse projections does **not** refute their conditional magnification theorem, nor does it apply indiscriminately when s(N)=2^{N^{o(1)}} is superpolynomial. It forbids only an improperly stronger *superpolynomial* lower-bound premise in the fully circuit-faithful, polynomially-sparse case. Mahaney's independent theorem says an NP-hard polynomially sparse language under ordinary polynomial-time many-one reductions implies P=NP; neither arbitrary NP membership nor the Chen-Jin-Williams use of subexponential sparsity asserts NP-hardness of that sparse language.

Primary sources:
- L. Chen, C. Jin, R. R. Williams. **Hardness Magnification for all Sparse NP Languages**, ECCC TR19-118 / FOCS 2019, https://eccc.weizmann.ac.il/report/2019/118/ (hypotheses and thresholds in original abstract).
- S. R. Mahaney. **Sparse Complete Sets for NP: Solution of a Conjecture by Berman and Hartmanis**, JCSS 25(2), 1982, pp. 130-143; original technical report https://ecommons.cornell.edu/entities/publication/02e42763-8a49-4dfe-9e73-59ccc016f74f .
- Prior original project claims: TMR-1/041 (separator lattice, exact CNF projections), TMR-5/038 (selected versus minimum interpolants), TMR-1/032 (sparse MCSP NO table counting), original October Lipschitz-squeeze audit LEAD-0029, scripts/sparse_cosparse_stream_escape.py.

## 7. Audit evidence and explicit hostile controls

The **exact test function serialized to** experiments/tmr/tmr1_fusion_connectivity091.js was executed using native V8 with deterministic seed 0x45b2de19. It performed **16,249 assertions with zero failures**, checking proper-3CNF clause counts and source identifier separation, all explicit source witnesses n=2..8, 28 exhaustive small n<=4 A/B existential projection pairs, 11,228 signed local legal/zero transition rows, 41 sparse-support circuit constructions including all their truth-table evaluations, and 20 deliberate model-change controls. Raw evidence: results/raw/tmr/2026-11-15_0357_TMR1_FUSCON091_V8_RAW.json. Finite status COMPUTATIONAL; the symbolic graph proof above carries the unbounded n statement.

A **free AND** linking separate input components would have Delta_fus=1 at price zero and immediately FAIL the certificate. An **unbounded-fanin AND gate** linking n inputs in one paid operation would have Delta_fus=n-1 at price one and FAIL the lambda_fus=1 certificate for n>=3. Both are absent from R_CONN, but an actual richer calculus admitting them must retain these shortcuts and refine the weight. Compact circuit representations, learned lemmas, Gaussian elimination, formula parsing, and physical input tapes are not simulated by R_CONN. Their cost-sound transfer remains OPEN. Sparse or easy Horn, 2-SAT, affine, equality, autarky and bounded-treewidth examples do not invalidate the scoped *gate-building* theorem; they invalidate any attempt to interpret its linear gate charge as hard SAT decision work.

An independent native CPython truth-table enumeration (not asserted byte-identical to the published V8) checked all AND/NOT DAG functions at gate counts below n-1 for n=2,3,4 (respective final layers 1,11,286 distinct wire-table sequences). The AND_n truth table was absent in every layer. This is a small finite COMPUTATIONAL corroboration, not the asymptotic proof.

## 8. Qualification, dependencies and next peer repair

| Node | Scientific status | Exact dependency / outcome |
|---|---|---|
| Q1 proper-3CNF pair, total binary encoding and unique interpolant | PROVED/RESTRICTED, peer OPEN | Explicit force-literal and OR-Tseitin source clauses; n>=2 |
| Q2 complete R_CONN transition inventory and zero closure | PROVED/RESTRICTED, peer OPEN | Only paid fan-in-two gates and free output/metadata selection |
| Q3 graph-fusion obstruction, full signed tariff and n-1 minimum | PROVED/RESTRICTED, peer OPEN | Holds for every shared-DAG circuit in R_CONN |
| Q4 sparse disjoint-projection minimum-separator upper bound | PROVED/RESTRICTED, peer OPEN | Any U and disjoint V, no NP membership required |
| Q5 transfer from arbitrary correct fixed multitape SAT deciders to R_CONN | OPEN | Must preserve real physical costs, interface, all legal shortcuts and same family |
| Q6 fusion-safe superpolynomial initial potential in a qualified unrestricted system | OPEN | Explicit family here has only n-1 |
| Q7 historical /341 and /386 authority | FAIL / RESTRICTED respectively | No retroactive repair |
| P != NP | OPEN | Not inferred |

**Weakest surviving lemma for TMR-2/3/4:** devise a *program-sensitive* nonaffine fusion component on actual finite-tape SAT configurations such that every physical step has a proved bounded discharge and every easy source admits its real cheap execution. The present p_fus is an exact positive baseline but its linear size and C-SEP gate interface cannot yield the required result. TMR-2 should test cheap quotienting, TMR-3 authenticate physical gate-append charges, and TMR-4 audit inclusion of fused machine events and free rewrites. TMR-5 should independently attempt cheaper DAG completion or a legal paid batch.

**Root corpus:** proof1.txt full 28,714 chars (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt authentic full 1,051,196-char blob (SHA 930c5eeddafce656717f28055a7a9a755f44737c), root main.tex authentic full 2,545,859-char blob (SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34), current issue #3, AGENTS.md, CODEX.md, research skill, current five TMR handoffs, and original related reports/code/results reviewed. Contents API showed empty proof2/main bodies but authentic Git blob recovered both before edits. No root material claim changes. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Five agent tasks and schedules unchanged.
