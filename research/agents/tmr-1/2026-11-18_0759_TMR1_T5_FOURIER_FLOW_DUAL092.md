# TMR-1/092: exact Fourier-flow duality, FPT cycle-rank counting, and polynomial-space realization

**Owner:** TMR-1 / PNP Machine Model Lead. **Date:** 2026-11-18 07:59 America/Los_Angeles. **Status:** exact symbolic derivation, finite computational verification. Independent review, LaTeX compilation and kernel proof OPEN. P versus NP OPEN.

## Model and theorem

Let \(\Sigma=\mathbb Z_5\), and let \(R(a,b)=1\) precisely when \(b-a\bmod 5\in\{1,3\}\). The authenticated input is a directed graph \(G=(V,E)\) with \(n\) declared vertices and \(m\) distinct ordered arcs, possibly including self-loops and opposed arcs. Let \(c\) be its number of weakly connected components, including isolates, and \(\rho=m-n+c\). Choose a primitive fifth root of unity \(\zeta\). Define \(\lambda_k=\zeta^k+\zeta^{3k}\) for \(k\in\mathbb F_5\), and let \(\partial:\mathbb F_5^E\to\mathbb F_5^V\) be the directed incidence map (outflow minus inflow; loop columns are zero).

**Theorem C1-T5-FOURIER-FLOW-DUAL092.** For *every* such graph, with no promise on orientation, loops, connectedness or satisfiability,

\[
\boxed{\#\mathrm{Hom}(G,T_5)
=5^{n-m}\sum_{f\in\ker_{\mathbb F_5}\partial}
       \prod_{e\in E}(\zeta^{f_e}+\zeta^{3f_e}).}
\]

The flow kernel has dimension \(\rho\), even with loops. The expression is a nonnegative integer although its summands lie in \(\mathbb Z[\zeta]\) and \(5^{n-m}\) may be rational. In the basis \(1,\zeta,\zeta^2,\zeta^3\), all three nonconstant coefficients cancel exactly and the constant coefficient is divisible by \(5^{m-n}\) when \(m>n\).

**Proof.** Finite Fourier inversion gives, for any \(d\in\mathbb F_5\),
\(R(d)=5^{-1}\sum_{k=0}^4(\zeta^k+\zeta^{3k})\zeta^{-kd}\).
Expand the product over all arcs and interchange finite sums. Summing each vertex color \(x_v\in\mathbb F_5\) gives \(5\) if the signed exponent of that color is zero mod 5, and zero otherwise. The simultaneous conditions are exactly \(\partial f=0\). Hence the sum over colors contributes \(5^n\) precisely on circulations, proving the identity. The usual incidence-matrix rank argument (one linear dependency per weak component and a spanning forest minor of rank \(n-c\)) gives nullity \(m-(n-c)=\rho\). Loops contribute zero columns, so they are fully covered. The coefficient cancellation and divisibility follow from equality with the integer homomorphism count and uniqueness of the cyclotomic basis representation. No numerical approximation is involved. QED.

## Two complementary exact algorithms

1. **Cotree-flow enumeration:** Construct a spanning forest of the underlying undirected multigraph (forget arc direction but retain the distinct arc identities). Let \(F\) denote its \(n-c\) edges and \(Q=E\setminus F\) its \(\rho\) chords, including loops. Assign each chord one of five flow values. Eliminate tree leaves bottom-up, enforcing signed conservation; each chord assignment has exactly one resulting tree-flow completion. Multiply the \(\lambda_{f_e}\) in \(\mathbb Z[\zeta]\) using the integer relation \(\zeta^4=-1-\zeta-\zeta^2-\zeta^3\). Accumulate exactly and apply \(5^{n-m}\). Time \(5^\rho\operatorname{poly}(L)\), peak writable space \(\operatorname{poly}(L)\) on a sequential binary machine.

2. **Primal tree-increment enumeration:** Assign each spanning-forest arc one of its two permitted increments \(1\) or \(3\), for exactly \(2^{n-c}\) choices. Fix the root color of each weak component to zero, propagate the unique colors along the forest, and accept the choice if all \(\rho\) chords satisfy their oriented beat constraints. A componentwise additive translation supplies exactly \(5^c\) homomorphisms per accepted choice. Therefore
\[
\#\mathrm{Hom}(G,T_5)=5^c\left|\{b\in\{0,1\}^{n-c}:
\text{all cotree arcs validate after propagation}\}\right|.
\]
Time \(2^{n-c}\operatorname{poly}(L)\), peak writable space \(\operatorname{poly}(L)\).

Choose the method with the smaller exponential factor to obtain **exact decision, counting and witness construction** in
\[
\boxed{\operatorname{poly}(L)\min\{5^{\,m-n+c},\,2^{\,n-c}\}}
\]
time and polynomial peak writable space. A positive exact count can be followed by branch/self-reduction to construct a witness with polynomially many counter invocations; alternatively the primal enumeration produces one directly. The displayed time bound is a uniform upper bound, NOT a lower bound.

The full proof tolerates forests, loops, opposed arcs, disconnected instances, isolates and every orientation. With \(m=0\), the formula gives \(5^n\). A loop is UNSAT, and its Fourier factor sums to \(\sum_k\lambda_k=0\); a tree has exactly \(5^c2^m\) assignments. This independently recovers and checks prior boundary cases.

## Primary-source complexity context

Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3) (1988), pp. 281–298, DOI https://doi.org/10.1137/0401029, prove the relevant homomorphism dichotomy. The specified \(T_5\) is a tournament containing more than one directed cycle (e.g. \(0\to1\to2\to0\) and \(0\to3\to4\to0\)), so general \(\mathrm{Hom}(-,T_5)\) is NP-complete. Prior role-owned constructive reductions and parsimonious strict-3-CNF compilation remain available. The Fourier result is a **parameterized exact algorithm**, not a polynomial-time decision algorithm on unrestricted instances. It does not establish a superpolynomial lower bound for any model.

## Executed computational controls and machine accounting

Full independent local Node.js script, exact 4-coordinate cyclotomic BigInt arithmetic (no floating-point roots), checked **1,237** graphs including every loop-permitted digraph on at most three vertices, seeded 4- and 5-vertex graphs, self-loops, opposed arcs, a directed 5-cycle, transitive \(K_4\), and small transitive complete orientations. It checked **1,381,317** original assignments, **455,737** flow enumerations, **6,621** spanning-tree increment choices, **523,558 assertions, zero failures**. Every tested Fourier count equalled both the direct five-color count and the independent tree-increment count. Local source SHA-256: 554edbbad5cac63f1c00497e999164ed9ddf4e237f553070250eeb4fcf481893. Raw result SHA-256: 07811e96e5cd5851dbc5a8e73519f61b62266a042e5260e0782e7dd6202afa4f. The separately published compact public Node verifier was also executed, checking **731** graphs with **444,854** assertions, **421,547** flow assignments and zero failures; Git blob SHA b472d30cb8662fb9b356ceca377e41acfcf23c3c.

All costs include graph reading, spanning-forest construction, integer coefficient arithmetic, exact divisibility, output and peak live storage. Enumeration is sequential. Under unit-cost algebraic assumptions the same formula holds, but no unit-cost claim is needed for these binary bit-machine upper bounds. These checks are COMPUTATIONAL and do not constitute independent mathematical review or a formal proof-kernel replay.

## Handoff and safeguards

Preserve the existing TMR-1 identity/title, enabled hourly schedule, manuscript \`main1_PNP_MACHINE_MODEL_LEAD.tex\`, draft PR #197 and issue #3. Preserve a byte-exact archive of the previous compact handoff before updating it. No agent creation, duplication, disabling, rescheduling, merging or immediate reruns. Next research target: hard-source instances with \(\rho=\Omega(n)\) that survive exact cotree enumeration heuristics, modular shortcut contraction, binary-domain Gaussian controls, Fourier-flow dualization, bounded-treewidth dynamic programming and all alternative encodings. Do not infer resource lower bounds merely from high \(\rho\); the high-treewidth voltage gadgets /085 were cheaply soluble. **P versus NP remains OPEN.**
