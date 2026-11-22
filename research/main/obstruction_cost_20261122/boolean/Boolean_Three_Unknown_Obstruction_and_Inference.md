# Three unknown Boolean variables: shortest obstruction and combination cost

## Scope and result

This note treats a residual CNF with three unknown Boolean variables as a fresh, independent input. It assumes no earlier exposure to a less erased assignment. Clauses have at most three literals; satisfied clauses, duplicate literals, tautological clauses, and duplicate clauses can be normalized with their actual acquisition and normalization costs charged separately.

Two quantities must be retained:

\[
\mu(F)=\min\{|K|:K\subseteq F,\ K\text{ is UNSAT}\},
\]

and

\[
g_{\mathrm{res}}(F)=\min\{\text{number of binary-resolution inferences in a refutation of }F\}.
\]

The latter counts inferences only. It does not silently include or omit actual runtime: source acquisition, proof search, representation construction, storage, transport, and output must be charged in a machine-cost account.

The identity \(g_{\mathrm{res}}=\mu-1\), valid for residual formulas with at most two Boolean variables, fails at three variables. The following explicit formula has

\[
\boxed{\mu(F)=5,\qquad g_{\mathrm{res}}(F)=5>4=\mu(F)-1.}
\]

This separates the size of a shortest source obstruction from the cost of combining that obstruction in a specified proof language. It is not an unrestricted computation lower bound.

## An exact five-clause example

Let

\[
\begin{aligned}
A&=\neg x\lor\neg y, &B&=y\lor\neg z, &C&=x\lor z,\\
D&=\neg x\lor y\lor z, &E&=x\lor\neg y\lor\neg z.
\end{aligned}
\]

The blocked assignments are disjoint and exhaust the Boolean cube:

| Clause | Assignments it alone forbids | Assignments satisfying all other clauses |
|---|---|---|
| A | 110, 111 | 110, 111 |
| B | 001, 101 | 001, 101 |
| C | 000, 010 | 000, 010 |
| D | 100 | 100 |
| E | 011 | 011 |

The coordinate order is \(x,y,z\). Every assignment violates exactly one clause. Consequently the formula is UNSAT, and removing any one of its five clauses makes it SAT. Thus every source clause is necessary and \(\mu(F)=5\).

There is also a compact semantic description. The first three clauses allow exactly the assignments \(011\) and \(100\). Clause D excludes the second assignment, and clause E excludes the first. This description is another valid way to combine the evidence, provided the work required to establish the description is charged.

### A refutation with five inferences

\[
\begin{aligned}
P&=\operatorname{res}_{z}(D,B)=\neg x\lor y,\\
N&=\operatorname{res}_{y}(P,A)=\neg x,\\
Q&=\operatorname{res}_{y}(E,B)=x\lor\neg z,\\
X&=\operatorname{res}_{z}(Q,C)=x,\\
\bot&=\operatorname{res}_{x}(X,N).
\end{aligned}
\]

The original clause B is reused. Its reuse is allowed. A proof DAG shares the source node, while a tree-like presentation has two occurrences of B. Both presentations use five inference vertices. No extra charge for a repeated logical leaf should be mistaken for a mandatory new acquisition of the original clause.

### Why four inferences cannot suffice

Here resolution uses non-tautological clauses and no auxiliary variables, with one charge per ordinary binary-resolution inference. The empty clause can be obtained only by resolving opposite unit clauses.

First, the inputs contain no unit clause. Second, no pair of input clauses resolves to a unit. The three binary clauses have different pairs of variables, so any non-tautological resolvent of two of them still has two literals. Resolving a ternary input clause against another input leaves at least two literals whenever the resolvent is non-tautological. Resolvents of D and E are tautological.

Suppose a refutation used at most four inferences. Its last step requires two opposite units \(\ell\) and \(\neg\ell\). There are only three preceding derived clauses. Because an input pair cannot derive a unit, the first derived clause Q must be a nonunit, the second step must derive one of the units using Q and an input, and the third step must derive its opposite.

The third step cannot use only inputs. It cannot obtain \(\neg\ell\) by resolving the unit \(\ell\) against another non-tautological clause: that resolution deletes the complementary literal, and cannot return it. It therefore must use Q and an input. Since both parents are nonunits, deriving the unit \(\ell\) forces Q to contain \(\ell\), and deriving \(\neg\ell\) forces Q to contain \(\neg\ell\). That would make Q tautological, contrary to the rule language. The assumed four-inference refutation is impossible.

This gives a direct proof of the lower bound, independently of the exhaustive computation. Ordinary resolution can omit tautological intermediate clauses without increasing the minimum useful refutation length: resolving a tautology either leaves a tautology or yields a weakening of the other premise. A stronger replacement may be propagated through descendants. The finite audit explicitly uses the non-tautological convention.

For comparison, the five-clause formula

\[
G=\{x\lor y,\ x\lor\neg y,\ \neg x\lor y\lor z,\ \neg x\lor y\lor\neg z,\ \neg x\lor\neg y\}
\]

also has \(\mu(G)=5\): its five blocking subcubes are disjoint and cover all eight assignments. Its first two clauses resolve to x, its third and fourth resolve to \(\neg x\lor y\), the latter resolves with the fifth to \(\neg x\), and one final resolution gives the empty clause. Therefore \(g_{\mathrm{res}}(G)=4\). The pair F,G has the same shortest source-obstruction size but different exact inference costs in the same proof language.

## Exact finite classification

Over three Boolean variables there are \(3^3=27\) normalized non-tautological clauses, including the empty clause. A coordinate is absent, positive, or negative. Each nonempty clause blocks a nonempty subcube of the eight assignments.

The audit enumerates all inclusion-minimal covers of these eight assignments by the 26 nonempty-clause blocking subcubes. It finds 869 such cores. Including the singleton empty clause gives 870 minimal cores.

| Core size | Number of labeled minimal cores | Minimum resolution inference count |
|---:|---:|---|
| 1 | 1 | 0 |
| 2 | 3 | 1 |
| 3 | 24 | 2 |
| 4 | 245 | 3 |
| 5 | 266 | 4 for 258 cores; 5 for 8 cores |
| 6 | 286 | 5 |
| 7 | 44 | 6 |
| 8 | 1 | 7 |

The 869 nonempty cores form 43 orbits under variable permutations and independent sign flips. Exactly one orbit, comprising the eight exceptional size-five cores, has no read-once resolution refutation. The formula displayed above represents that orbit.

### Why the enumeration is complete

The enumeration processes the eight assignments in a fixed order. At each stage it maintains all inclusion-minimal clause sets covering the assignments processed so far. To process the next assignment, it retains each current set that already covers it, and otherwise extends that set by each clause that blocks it. It then removes nonminimal sets.

For completeness, let K be a minimal cover after the next assignment is added. It contains some minimal cover H of the earlier assignments. If H already covers the new assignment, minimality implies K=H. Otherwise K contains a clause C blocking the new assignment, and H together with C is a cover contained in K; minimality implies K=H union {C}. Thus every new minimal cover occurs among the candidates. Induction proves completeness.

The numbers of surviving covers after one through eight assignments are 7, 19, 53, 89, 239, 395, 647, and 869. Every final result is checked both for full coverage and for a private assignment for each of its clauses.

Read-once resolution is checked by a second dynamic program. For each subset S of a core's clauses, the program records all clauses derivable by a binary resolution tree that uses each source clause in S exactly once. It considers every partition of S into two nonempty parts and every possible resolvent of their recorded clauses. The empty clause occurs for the full source set if and only if such a read-once refutation exists.

### Why this determines exact inference lengths

For any binary-resolution refutation, discard nodes not leading to the final contradiction. If its resulting DAG has b distinct source clauses and g inference vertices, it has b+g vertices and 2g premise edges. Its underlying undirected graph is connected, so

\[
2g\ge b+g-1,
\qquad g\ge b-1\ge\mu(F)-1.
\]

Equality \(g=\mu(F)-1\) forces \(b=\mu(F)\) and an underlying tree, so there is a read-once refutation using a minimum core. The dynamic program supplies equality for all 42 nonexceptional orbits. The exceptional orbit has the direct five-inference proof and matching lower bound above.

The singleton empty clause has g=0. The unique eight-clause core consists of all full ternary clauses, each blocking one assignment, and has a seven-inference balanced resolution refutation.

For an arbitrary, possibly nonminimal, three-variable UNSAT CNF, this yields an exact description after its minimum cores are known:

\[
g_{\mathrm{res}}(F)=
\begin{cases}
5,&\mu(F)=5\text{ and every minimum core belongs to the exceptional orbit},\\
\mu(F)-1,&\text{otherwise}.
\end{cases}
\]

Indeed, choosing any minimum core gives the upper bound. A refutation with \(\mu-1\) inferences must use a minimum core read once, by the connected-DAG argument. This classification is an exact finite statement about three variables, not a formula-size asymptotic result.

## Allowing every sound combination method

The example also shows why the allowed operations must remain explicit. Assign each Boolean assignment one bit, in the order 000,001,010,011,100,101,110,111. The five blocking masks are

\[
M_A=192,\quad M_B=34,\quad M_C=5,\quad M_D=16,\quad M_E=8.
\]

Their bitwise OR is 255. Four binary OR operations combine the five masks, followed by a comparison with the all-ones mask. For three variables each mask occupies eight bits. Mask construction, obtaining the clauses, locating the rows, and any representation conversion remain charged. This does not establish that the bitmask implementation is faster than the resolution implementation under a common full machine model. It establishes that the fifth resolution inference is not a logically universal extra combination operation.

A single macro-operation could recognize this whole five-clause pattern, or an implication-graph computation could recognize the two residual models of A, B, C. Such methods are sound. They must be charged by their actual realization, rather than declared free or disallowed because they do not match a chosen local inference language.

For a pure binary aggregation model whose final object explicitly depends on all five source objects, four aggregation vertices are necessary by the same connected-graph count. That graph count concerns fan-in and dependency, not a requirement to count assignments or a lower bound on all algorithms. The aggregation representation may already expose the contradiction before a proposed final local test. If earlier charged work has established the decision bit, no further nontrivial local inference is forced.

## Implications for the erased-variable program

For r=3 the shortest source obstruction has at most eight clauses. More generally, for a fixed r-variable residual CNF, every minimal UNSAT core has at most \(2^r\) clauses because each clause of a minimal core has a private assignment, and these private assignments are distinct. For r=3 the bound is attained by the eight full ternary clauses. For increasing r with fixed clause width k, this does not assert that the \(2^r\) bound is attainable by k-CNF.

At fixed r, normalization reduces the semantic types to finitely many cases. The cost of acquiring and simplifying the original formula can still depend on its encoded length. The constant-size residual case cannot by itself force a growing local decision cost after a sufficient summary has already been constructed.

The useful strengthening is therefore to retain three separate objects at each independent erasure level: the smallest source obstruction, the cheapest verified way of establishing its incompatibility in each candidate representation, and the fully charged way to obtain and construct that representation. Taking the cheapest sound route must be allowed. A lower bound on one representation's inference length is evidence about that route, not evidence that no other route can avoid it.

## Reproduction and provenance

All results here are new calculations for this project and are not claimed as a previously unknown classification. Two small complete scripts produce the recorded raw output:

* `boolean_three_probe.py`: complete minimal-cover enumeration and read-once resolution test.
* `boolean_three_probe_results.json`: 869 cores represented by 43 symmetry orbits, histogram, private witnesses, and script hash.
* `boolean_three_witness_audit.py`: independent truth-table verification, five-step proof verification, and breadth-first search of all useful non-tautological resolution additions.
* `boolean_three_witness_audit_results.json`: full witness and the exact breadth-first search result.

Run commands, each bounded to 30 seconds:

```sh
timeout 30s python boolean_three_probe.py > boolean_three_probe_results.json
timeout 30s python boolean_three_witness_audit.py > boolean_three_witness_audit_results.json
```

The concrete witness search has 1, 9, 42, 144, 405, and 957 states at depths 0 through 5. It first derives the empty clause at depth 5. The run took approximately 0.0045 seconds, excluding process startup.

Recorded script SHA-256 hashes:

```text
boolean_three_probe.py
85fb22d33256c461fe9029181bd43f9df7760613c5c5d1a7e17df8af88c983e4

boolean_three_witness_audit.py
4b496a555e0e6cc76f5ad4f1588821485585c4013b401160a6536ed3f28227b0
```

## Primary literature for context

1. Konstantin Sidorov, Koos van der Linden, Goncalo Homem de Almeida Correia, Mathijs de Weerdt, and Emir Demirovic. *How To Discover Short, Shorter, and the Shortest Proofs of Unsatisfiability: A Branch-and-Bound Approach for Resolution Proof Length Minimization*. arXiv:2411.07955, 2024. https://arxiv.org/abs/2411.07955 . This work studies the distinct optimization problem of finding shortest resolution proofs. The finite calculations above use a simpler exhaustive method appropriate for only three variables.
2. Albert Atserias and Moritz Muller. *Automating Resolution is NP-Hard*. Author manuscript dated September 3, 2019. https://www.cs.upc.edu/~atserias/papers/automating-resolution-np-hard/automating-resolution-np-hard.pdf . Their definition of automatizability separates shortest proof length from the time needed to find a proof. Their hardness theorem is conditional in its algorithmic consequence and does not provide an unrestricted P versus NP separation.
