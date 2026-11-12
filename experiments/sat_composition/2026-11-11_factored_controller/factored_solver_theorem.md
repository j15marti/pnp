# Exact factored dynamic programming with bounded adhesions

Status: PROVED for an explicitly supplied, validated forest decomposition and the declared local solver contracts. This integrates standard decomposition dynamic programming with the existing exact Horn/2-CNF-plus-affine backends. No novelty claim or all-input polynomial SAT theorem is asserted.

## Input contract and representation

The source is a conjunction of original clauses and affine equations over F_2. In 2-CNF mode every clause has width at most two. In Horn mode every nontautological normalized clause has at most one positive literal, with unrestricted width.

The decomposition is an explicit forest of variable bags. Every original factor must have its complete support in at least one bag. The algorithm assigns it exactly once, to the first containing bag. Every variable's containing bags must form a connected subtree. This running-intersection condition is checked for all bag variables, including unused names. Each tree-edge intersection has at most two variables in 2-CNF mode, or at most one variable in Horn mode. Empty bags, zero-scope factors, and a forest with no bags are handled explicitly.

All original input and decomposition records are validated before a conclusion is returned. A malformed decomposition raises an error. A solver cap yields UNRESOLVED and never masquerades as a logical contradiction.

## Exact messages

Root each forest component at its first bag. For a bag b with parent p, write S_b=B_b intersect B_p; root separators are empty. The semantic message is the set of assignments to S_b that extend to a model of all factors assigned within b's subtree.

For each of its at most four boundary assignments, the algorithm:

1. Includes the original factors assigned to b.
2. Includes one clause excluding every child boundary assignment proved UNSAT.
3. Pins the current separator assignment by unit clauses.
4. Calls the selected exact local backend once.

A forbidden assignment on at most two variables is one binary or unit clause, with an empty clause for a forbidden zero-variable assignment. Thus 2-CNF is preserved. For Horn mode, at most one variable is permitted in a message, so every added clause is unary or empty and remains Horn. In both modes the child messages and separator pins introduce clauses only. They introduce no new affine rows.

There are at most 2^|S_b| calls per bag, and exactly one call for a root state. The implementation does not try a second restricted solve after a possible local witness selects an unresolved child state.

Before expansion or seed search, each local query receives a charged polynomial recognition pass. An empty clause proves UNSAT immediately. If every remaining normalized nontautological clause is a unit, the algorithm converts those units to affine equations, performs Gaussian elimination, constructs a model when consistent, and checks it against the complete local query. This unit-affine terminal is polynomial for arbitrary affine rank. Expansion and seed caps do not apply to it, so it may legitimately resolve a query even when both caps are zero. Failed recognition scans are counted as well. The total local decision count is partitioned into affine_terminal_calls and frozen_backend_calls.

## Three-valued correctness with resource caps

Each message state has one of three meanings:

* SAT: a concrete compatible subtree witness is cached.
* UNSAT: no such subtree witness exists.
* UNRESOLVED: no conclusion about that boundary assignment.

The local formula allows all child states except those proved UNSAT. Its solution set therefore contains the projection of every real subtree model. If the backend declares this possible-state relaxation UNSAT, the current boundary state is genuinely UNSAT.

If the backend gives a local model, the algorithm reads the child boundary assignments selected by that same model. If each selected child state is SAT, their cached witnesses can be combined with the local assignment. Running intersection ensures that variables shared with another subtree occur in the intervening separators, where their values already agree. Hence the current state is SAT. If any selected child state is unresolved, the current state remains UNRESOLVED.

This proves soundness of every SAT and UNSAT state by induction. Without caps the backends resolve every local call, so induction also gives exact two-valued messages. With caps a different local witness might have selected certified children even when the returned witness did not; this conservative one-call implementation is allowed to leave such a state unresolved.

For a forest, the answer is UNSAT if any component is UNSAT, SAT if all components are SAT, and otherwise UNRESOLVED. A SAT answer is reconstructed through the cached states. All original clauses and equations are checked again against the complete global assignment.

## Charged parameterized bound

Let N be the explicit dense source size, D the decomposition description size, n_b the number of variables in bag b, L_b the complete local input size including child clauses and pins, and d_b the coefficient rank of original affine rows assigned to b. Then uncapped evaluation has the bound

$$
T\le\operatorname{poly}(N+D)
+\sum_b 2^{|S_b|}\operatorname{poly}(L_b+n_b)
\sum_{i=0}^{d_b}\binom{n_b}{i}.
$$

The polynomial overhead includes forest and running-intersection validation, all containment tests including failed tests, exact factor assignment, local renaming, row-rank computation, message construction, state bookkeeping, witness reconstruction, and final source verification. The local backends charge their own parsing, algebra, closure and candidate work. Their displayed counters are selected operation counts, not complete physical bit-instruction measurements; the asymptotic bound includes the remaining polynomial operations.

The message arity is at most two or one, so the factor 2^|S_b| is at most four or two. If max_b d_b is bounded by a fixed constant, the full runtime is polynomial in N+D even if the total number or rank of affine equations across the forest is unbounded. More generally the displayed sum itself, not merely the maximum rank, is the relevant total bound.

For each query recognized by the unit-affine terminal, replace its binomial-factor cost in this upper bound by the polynomial Gaussian cost. More precisely, take one fixed polynomial P that dominates recognition, Gaussian work, and the polynomial factor of either backend, and let g_q=1 when the terminal recognizes query q and g_q=infinity otherwise. Its charged bound is

$$
P(L_q+n_b)\min\left\{g_q,\sum_{i=0}^{d_b}\binom{n_b}{i}\right\}.
$$

No small-rank assumption is needed for these pure affine or unit-affine cases. This terminal is selected before calling the expansion or seed backend; no expensive expansion is performed merely to discover that Gaussian elimination was applicable.

With the streaming seed backend, the entire evaluation has polynomial workspace even for growing d_b: each local solve uses polynomial workspace; there are only constantly many cached states and local witnesses per bag; and calls execute sequentially. With the polynomial-expansion backend, its potentially larger local working polynomial must be included in peak workspace.

The supplied discovery_counters object is retained as provenance data. It does not certify the cost of an arbitrary external search for a decomposition. A full controller must separately charge actual discovery, rejected decompositions, and any fallback. This theorem does not prove that every input has a suitable efficiently discoverable decomposition.

## Limits of the message language

The separator restrictions are essential to this particular interface. An arbitrary function of two Boolean variables can be written as a 2-CNF by excluding false assignments. A two-variable message need not be Horn, so general Horn mode restricts to one variable. At three variables even a simple positive OR relation is not necessarily representable by a boundary-only 2-CNF-plus-affine conjunction. More expressive messages need their own exact closure and cost theorem.

The implementation and controls are in factored_solver.py and its machine-readable validation outputs. Frozen ATC2 backends are imported without modifying their semantics. P versus NP remains open.
