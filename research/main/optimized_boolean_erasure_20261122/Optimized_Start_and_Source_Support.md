# Optimized Boolean starting assignments and persistent source obstructions

Research date: 22 November 2026.

## 1. Setting and the near-satisfying hypothesis

Let F be an UNSAT strict 3-CNF: every source clause has three literals on three distinct variables. Let its n variable names form V. Suppose a full assignment alpha violates exactly one source clause C*. Choose x in vars(C*).

For any release set R containing x, let rho_R agree with alpha outside R and leave all variables in R unknown. Each pair (F,rho_R) is a fresh input. Nothing in the results transfers a machine state from one release set to another. Write mu(R) for the smallest number of source clauses whose restrictions under rho_R are already UNSAT.

At a pinned level the decision concerns completions compatible with the supplied values. If the global source status is unknown, rejecting this one restriction does not establish global UNSAT. Global incompatibility requires all relevant value slices to be incompatible, as in the previously proved shared-union recursion. Choosing globally UNSAT examples for this analysis does not grant an all-UNSAT promise to a solver.

The hypothesis that alpha violates exactly one clause is substantive. It is equivalent to the existence of a clause C* such that F without C* is satisfiable. A minimally UNSAT source always has such assignments, but an arbitrary UNSAT source need not. For example, the conjunction of two variable-disjoint UNSAT sources forces every full assignment to violate at least two clauses. A minimum core can have a deletion witness even when that witness violates additional rows of the full source.

There is no intrinsic UNSAT variable. Every x in the uniquely violated clause has the one-unknown property below. Choosing a variable outside C* instead leaves C* as an empty residual clause and gives a one-row obstruction. The intended study therefore explicitly requires x in C*.

## 2. A distinguished row belongs to every obstruction

For every release set R, the assignment alpha restricted to R satisfies every residual source row except C*. Consequently every UNSAT source subset contains C*. This remains true after arbitrarily many other values are released.

Once x in C* is unknown, C* cannot become an empty clause. No other row can become empty either, because alpha supplies a satisfying extension for that row. Thus every level with x unknown has no empty residual clause and

\[
\mu(R)\ge 2.
\]

These are semantic statements about source subsets. A decision algorithm need not explicitly identify C* or verify that it is the only violated row if it can establish a contradiction another way.

## 3. One unknown: the exact obstruction

With only x unknown, C* becomes a unit literal ell that alpha makes false. Every other surviving clause is a unit that alpha makes true, so its literal is not-ell. Since the residual formula is UNSAT, at least one such opposite unit must occur. Hence

\[
\boxed{\mu(\{x\})=2.}
\]

The source partner is characterized exactly. Let D_x(alpha) be the set of clauses D other than C* whose unique alpha-satisfied literal is the literal on x, with polarity opposite the x literal in C*. Then D_x(alpha) is nonempty, and the minimum source cores at this level are precisely the pairs {C*,D} with D in D_x(alpha).

One can also see existence directly: flip alpha(x). This repairs C*. Because F is UNSAT, the new assignment violates some D. For D to be true before the flip and false afterward, its only alpha-satisfied literal must have been its literal on x.

The source evidence is therefore two particular rows and the supplied values that make their other literals false. After those two residual units are established, their incompatibility has a constant-size verification. Finding the rows, acquiring their source positions, obtaining the supplied values, and any representation construction remain separate charged work.

## 4. Two unknowns: complete case classification

Release a second value y distinct from x. Flip variable names and signs conceptually so that alpha(x)=alpha(y)=0 and the C* literals on these variables, when present, are positive. This is a mathematical normalization; an implementation must pay for any explicit conversion it performs.

| Location of y | Residual C* | Possible exact mu | Condition |
|---|---|---|---|
| y outside C* | x | 2 or 3 | mu=2 exactly when some D in D_x(alpha) does not contain y |
| y inside C* | x or y | 3 or 4 | mu=3 exactly when a residual unit not-x or not-y occurs; otherwise mu=4 |

In the second row, “x or y” denotes the binary clause, not a choice between two unit clauses.

### Second value outside C*

C* remains the unit x. A two-clause contradiction must consist of opposite units, so mu=2 exactly when some x-critical source partner still restricts to not-x. This happens exactly when y is absent from that partner.

If no partner survives as a unit, mu cannot be two. Set x=1 as required by C*. The remaining residual problem has only y unknown and is UNSAT. An empty clause after this substitution would have arisen from an opposite unit not-x before substitution, which is excluded. Therefore two remaining source rows provide opposite units on y. Together with C*, they give a three-row obstruction, so mu=3.

Choosing y outside the union of C* and a known partner preserves that pair immediately. Choosing y inside one partner's scope need not destroy every two-row obstruction: another partner might omit y. The exact test quantifies over all partners.

### Second value inside C*

C* becomes x or y and blocks only 00. Every other residual row is true at 00. Its only possible nontrivial normalized forms are

\[
\neg x,\quad \neg y,\quad \neg x\lor y,\quad
x\lor\neg y,\quad \neg x\lor\neg y.
\]

A second clause cannot exclude all three remaining assignments, so mu is at least three. If not-x occurs, it excludes 10 and 11, and global UNSAT guarantees another row excluding 01. Those two rows with C* form a three-row core. The not-y case is symmetric.

If neither negative unit occurs, the three remaining assignments each require their corresponding binary clause. All four binary clauses then form the minimum core, so mu=4. This also shows that one release can increase the smallest obstruction from two directly to four.

## 5. Exact persistence criterion for arbitrary release sets

Define the critical boundary for a partner D by

\[
B_D=(\operatorname{vars}(C^*)\cup\operatorname{vars}(D))\setminus\{x\}.
\]

For every release set R containing x,

\[
\boxed{
\mu(R)=2
\quad\Longleftrightarrow\quad
\exists D\in D_x(\alpha):\ R\cap B_D=\varnothing.
}
\tag{1}
\]

The forward implication uses the distinguished-row result. A two-row UNSAT core must contain C*. Two nonempty, non-tautological clauses are jointly UNSAT only when they are opposite units. Thus C* must retain only x, and the other row must retain only the opposite x literal. Its remaining source literals are fixed false, so that row belongs to D_x(alpha), and no other variable of either source row lies in R. The reverse implication follows by restricting the two clauses: they are the same opposite units as at the first level.

Let

\[
h(\alpha,x)=\min_{D\in D_x(\alpha)}|B_D|.
\]

Because both source rows have exactly three distinct variable names and share x,

\[
2\le h(\alpha,x)\le4.
\]

Equation (1) gives the exact best endpoint:

\[
\boxed{
\max\{|R|:x\in R,\ \mu(R)=2\}=n-h(\alpha,x).
}
\tag{2}
\]

Choose a partner attaining h, retain its boundary variables, and release every other variable first. Every fresh level from r=1 through r=n-h has mu_r=2. Conversely, any release set with mu=2 has a surviving partner by (1), and therefore contains at most n-h variables. Switching partners along a chain cannot exceed this endpoint.

Thus every admissible starting assignment and designated x has a two-row plateau through at least r=n-4. If the two source rows share all three variable names, only two values need remain supplied and the plateau reaches r=n-2. These statements concern minimum source support. They do not claim that selecting the best alpha, selecting a partner, or locating its rows is free or computationally optimal.

### Sharpness even after choosing alpha and x

A CNF is linear when distinct clauses share at most one variable. UNSAT linear strict 3-CNF formulas exist; Scheder proves existence for every exact clause width k [1,2]. Taking an inclusion-minimal UNSAT subset preserves linearity and exact width. It also supplies a near-satisfying assignment for each selected C*.

In any such linear source, every opposite-unit partner for a designated x shares exactly x with C*. Its two other variables are disjoint from C*'s two other variables. Therefore h=4 for every admissible alpha, C*, and x. Optimizing the starting assignment and designated variable cannot improve the endpoint n-4 on these sources.

Arbitrarily large examples can also be obtained by adjoining satisfiable clauses on fresh disjoint triples of variables. The old UNSAT component still forces the unique violated row of any admissible near-assignment to lie in that component, and no new row can be an x-critical partner. Linearity and h=4 persist.

This establishes sharpness of the four-pin structural guarantee. It does not assert computational hardness of a particular linear formula or of finding its critical pair.

## 6. Bounds controlled by the released part of C*

Let r=|R| and d=|R intersect vars(C*)|, with d at least one. Then

\[
\boxed{
d+1\le\mu(R)\le1+2^r-2^{r-d}.
}
\tag{3}
\]

The upper bound can also be capped by the number of available source rows or distinct residual types.

For the lower bound, consider the d completions obtained from alpha by flipping just one released variable belonging to C*. Each satisfies C* and therefore must violate another row of any UNSAT core. A row true at alpha cannot be false at two distinct such one-bit flips: becoming false after the first flip means its unique alpha-satisfied literal was on that flipped variable. Hence d distinct additional rows are required.

For the upper bound, choose a minimal core. It contains C*. Each other row has a private assignment satisfying all the core's other rows, including C*. These private assignments are pairwise distinct. The d-literal residual C* is false on exactly 2^(r-d) completions, leaving 2^r minus 2^(r-d) possible private assignments for the other rows. There can be at most that many other rows. The reference assignment itself supplies a private assignment for C*.

In the project's earlier notation, d is t_r and the surviving region outside C* has size Q_r=2^r-2^(r-t_r). The proven conclusion is mu(R)-1 at most Q_r. Thus Q_r is an upper bound on the number of additional rows in a minimal source obstruction. It is not a lower bound requiring Q_r local exclusions, probes, inferences, or machine steps. A single source row or shared calculation can exclude many of those assignments together.

For r at most three, both bounds and every intermediate integer are realizable:

| Unknown count r | Released C* variables d | Possible minimum-core sizes |
|---:|---:|---|
| 1 | 1 | 2 |
| 2 | 1 | 2, 3 |
| 2 | 2 | 3, 4 |
| 3 | 1 | 2, 3, 4, 5 |
| 3 | 2 | 3, 4, 5, 6, 7 |
| 3 | 3 | 4, 5, 6, 7, 8 |

To see realizability first in width-at-most-three CNF, set alpha=0 and C*=(x_1 or ... or x_d). Partition its complement by the position of the first true variable among x_1,...,x_d. The clauses

\[
D_j=x_1\lor\cdots\lor x_{j-1}\lor\neg x_j,
\qquad 1\le j\le d,
\]

forbid those d disjoint regions. Together with C* they partition the r-cube, giving a minimal core of size d+1 and a unique violated row at alpha.

Replace any D that omits some variable u by the two clauses D or u and D or not-u. Their forbidden regions partition D's former region. The core remains minimal, C* remains the unique violated row at alpha, and its size rises by exactly one. Continue until every point outside C*'s forbidden region has its own clause. All clause widths are at most r, so for r at most three this proves every size in the table. The next section embeds these constructions in literal strict 3-CNF sources.

For r greater than three, the private-assignment upper bound remains valid, but this construction would require wider clauses. No sharp exponential core-size claim for fixed-width 3-CNF follows from it.

## 7. Strict 3-CNF realizations

Any width-at-most-three residual construction G above can be realized as a restriction of a globally UNSAT strict 3-CNF source while preserving its near-satisfying reference assignment.

Take fresh names a,b,p,q. Pad a unit literal ell to (ell or a or b). Pad a binary clause D to (D or a). Leave ternary clauses unchanged. Add, for each v in {a,b}, the four strict clauses

\[
Z(v;p,q)=
(\neg v\lor p\lor q)\land
(\neg v\lor p\lor\neg q)\land
(\neg v\lor\neg p\lor q)\land
(\neg v\lor\neg p\lor\neg q).
\]

This gadget forces v=0: if v=1, exactly one of its four clauses fails for every pair p,q; if v=0, all four are true. The resulting source is satisfiable exactly when G is satisfiable. Every clause has three literals on distinct variable names.

Supply a=b=p=q=0 and release only the intended residual variables. All eight forcing rows become true, and the padded rows reduce exactly to G. With the all-zero reference, all forcing rows are satisfied and exactly the padded C* is violated.

In particular, the two-unknown cases have residual witnesses

\[
\begin{array}{c|c|c}
\text{location of y}&\mu& G\\\hline
y\notin C^*&2&\{x,\neg x\}\\
y\notin C^*&3&\{x,\neg x\lor y,\neg y\}\\
y\in C^*&3&\{x\lor y,\neg x,\neg y\}\\
y\in C^*&4&\{x\lor y,\neg x\lor y,x\lor\neg y,\neg x\lor\neg y\}.
\end{array}
\]

If every declared variable must occur in the source, the otherwise-unused y in the first example can occur in the additional satisfied row (not-a or y or p). It introduces no residual constraint when a=0.

## 8. The endpoint source-cardinality floor

If only one variable value remains supplied, every nontrivial residual clause of a strict 3-CNF has width at least two. Each such clause forbids at most one quarter of the completion cube. Covering the cube therefore requires at least four clauses. When no values remain supplied, every source clause has width three and forbids exactly one eighth, so an UNSAT source needs at least eight clauses.

Together with the no-empty-row argument, any admissible near-assignment release path satisfies the pointwise floor

\[
\mu_r\ge
\begin{cases}
2,&1\le r\le n-2,\\
4,&r=n-1,\\
8,&r=n.
\end{cases}
\]

The full eight-clause cube on three variables attains this floor. Additional variables can occur in rows satisfied by the reference assignment and be released first; the original cube core remains. Thus the floor path 2,...,2,4,8 is realizable for arbitrary larger declared source sizes.

This volume argument establishes a mathematical lower bound on the number of source rows in an obstruction. It does not require an algorithm to count assignments, and it is not a runtime lower bound.

## 9. Independently checked guarded arbitrary-3SAT bridge

The coordinator's construction preserves the optimal early source-cardinality floor while placing an arbitrary strict 3-CNF H at the final release.

For every clause C=(ell_1 or ell_2 or ell_3) of H, take a private fresh variable s_C. Add four fresh guard variables p,x,a,b. Define F(H) by the guard rows

\[
(p\lor x\lor a),\quad(p\lor x\lor\neg a),\quad
(p\lor\neg x\lor b),\quad(p\lor\neg x\lor\neg b)
\]

and the two rows

\[
(\neg p\lor\ell_1\lor s_C),\qquad
(\neg s_C\lor\ell_2\lor\ell_3)
\]

for each C. The source is strict 3-CNF, and its all-zero assignment violates exactly the first guard row for every H, regardless of H's satisfiability.

If p=0, all four guards are jointly inconsistent. If p=1, all guards disappear and each private pair is equivalent, after choosing s_C, to its original clause C. Thus F(H) is SAT exactly when H is SAT.

More strongly, any UNSAT source subset must contain all four guards: if a guard is missing, set p=0, choose x,a,b satisfying the remaining guards, and set every s_C=0. Then every H-derived row is satisfied. With all guards present, p is forced to one. Only complete private pairs constrain H; a single remaining half can always be satisfied by its own s_C. Minimal cores therefore correspond exactly to a minimal core of H, both halves of each selected clause, and all four guards. For UNSAT H,

\[
\mu(F(H))=4+2\mu(H).
\]

Choose a as the first released value. Retain only p=x=0 while releasing every other value, including b, all H variables and all private s_C. The first two guards remain the opposite units a and not-a. Hence mu_r=2 through r=n_F-2. Release x next while retaining p=0; the four guards form a minimal four-row obstruction, and all H-derived rows are jointly satisfiable with the private variables zero. Thus mu_(n_F-1)=4. Release p last; the full F(H) problem is exposed.

This path has the smallest source-obstruction cardinality possible at every earlier level, while the final problem is equivalent to arbitrary H. For H equal to the complete eight-clause cube on three variables, n_F=15, F(H) has 20 rows, and its exact profile is mu_1 through mu_13 equal to 2, mu_14=4, and mu_15=20.

The x-first alternative has a three-pin plateau: retain p=a=b=0, release x and all H and private variables, then release b, then a, then p. Its final source-cardinality stages are 2,3,4,4+2mu(H). Choosing a first gives the longer two-row plateau.

These are fresh-instance statements. The all-zero reference is explicit and independent of any solution of H. A solver must be correct on both final SAT and final UNSAT inputs; the construction does not grant an UNSAT promise. Cheap earlier restrictions cannot settle the last unrestricted source.

## 10. Computational interpretation

The exact optimum in (2) optimizes source support persistence, not actual computation. For a supplied release set that preserves a known opposite-unit pair, a correct uniform procedure can verify that pair and reject. If the pair is not already located, a scan can search for the two polarities of the designated variable, while falling back to a general solver if no such certificate is found. This remains correct on both labels.

Under a declared indexed read-only value-array model, checking each source literal against its supplied or unknown status gives a near-linear scan with logarithmic or polylogarithmic auxiliary storage. Under a different access model, the lookup and transport costs must be charged explicitly. The statement does not supply a new worst-case bound for all r-unknown instances. It supplies an available correct route on the instances whose surviving pair is verified.

Choosing alpha, identifying its uniquely violated row, discovering a good partner, and constructing or obtaining the partial assignment are not free if they are part of the computational task. Conversely, if the fresh problem supplies the partial assignment as input, its explicit information belongs to that input and must not be treated as a hidden computation performed by the solver.

All sound combinations remain allowed. Source-core cardinality, contextual information, proof length, discovery time, and full time/space/cumulative-storage cost are different quantities. No additional local inference is compulsory after earlier charged work has established a sound verdict.

## References

[1] Dominik Scheder. *Unsatisfiable Linear k-CNFs Exist, for every k*. arXiv:0708.2336, 2007. https://arxiv.org/abs/0708.2336 . The exact-width definition and existence result justify the sharpness example in section 5.

[2] Dominik Scheder. *Unsatisfiable Linear CNF Formulas Are Large and Complex*. STACS 2010, LIPIcs volume 5, pages 621-632. https://doi.org/10.4230/LIPIcs.STACS.2010.2490 . The published result also establishes existence of UNSAT linear exact-width formulas. No proof-complexity lower bound from that paper is transferred to unrestricted computation here.
