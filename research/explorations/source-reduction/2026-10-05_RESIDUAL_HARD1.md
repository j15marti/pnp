# RESIDUAL-HARD1 — NP-Completeness Inside the Degree-2 Externally Mediated Clean-Core Schema

**Date:** 2026-10-05  
**Repository:** \`j15marti/pnp\`  
**Global status:** **OPEN. P versus NP remains open.**

This note tightens CLEANCORE-POLY1 against the actual project definition of the low-degree externally mediated clean core.

The previous note cautiously separated the ambient mediator language from the strict residual clean-core case. Under the current clean-core definition, that caveat is too strong: the direct 3-SAT dual-encoding gadgets already satisfy the structural residual conditions used in the project.

The result below is a structural NP-completeness theorem. It is **not** a lower bound and does not prove \(P\ne NP\).

---

# 1. Background: Liu 1-chains versus project clean-core structure

Liu's chain framework defines a 1-chain in 3-CNF as a single 3-clause, whose solution space is exactly

\[
D=\{0,1\}^3\setminus\{000\}.
\]

An instance is a collection of variable-disjoint chains.

The project's later clean-core refinement takes a collection of bare type-1 chains and forms a rank-\(2/3\) correlation hypergraph whose vertices are chains. A hyperedge exists only when a **residual clause supported entirely on chain variables** directly couples two or three distinct chains.

After deleting a maximal hypermatching, the externally mediated clean core is a set \(J\) of chains with no such remaining chain-only cross clause. Any remaining coupling between clean chains passes through at least one outside variable.

The high-degree mediator rule separately handles an outside variable \(y\) if branching on \(y\) activates sufficiently many disjoint binary chain-pair correlations.

This clean-core definition is a project refinement, not a theorem stated in Liu's paper.

---

# 2. Definition: EM2-CLEAN

Define the class \(\mathrm{EM2\text{-}CLEAN}\) of 3-CNF formulas admitting the following partition.

There are \(m\) pairwise disjoint chain triples

\[
T_a=\{z_{a1},z_{a2},z_{a3}\},
\qquad
a\in[m],
\]

with one base 1-chain clause

\[
B_a=z_{a1}\vee z_{a2}\vee z_{a3}.
\]

All remaining variables are outside mediators \(y\in Y\).

For each mediator \(y\), there is a binary clause

\[
Q_y=\ell_u\vee \ell_v,
\]

where \(\ell_u,\ell_v\) are literals on variables belonging to two **distinct** chain triples, and the formula contains exactly the two clauses

\[
Q_y\vee y,
\qquad
Q_y\vee\neg y.
\]

No mediator occurs anywhere else.

Thus every mediator:

- has degree exactly 2;
- occurs once positively and once negatively;
- couples exactly two distinct chains;
- has one activated binary pair constraint in either polarity branch.

There are no non-base residual clauses supported entirely on chain variables.

---

# 3. Lemma RESOLVE2

**Status: PROVED/EXACT.**

For every Boolean clause \(Q\),

\[
(Q\vee y)\wedge(Q\vee\neg y)
\equiv Q.
\]

### Proof

If \(Q=1\), both clauses hold for either value of \(y\).

If \(Q=0\), the conjunction becomes

\[
y\wedge\neg y,
\]

which is impossible. \(\square\)

Therefore every EM2 mediator is a syntactic hiding of one binary chain constraint.

---

# 4. Theorem RESIDUAL-HARD1

**Status: PROVED/EXACT.**

SAT restricted to \(\mathrm{EM2\text{-}CLEAN}\) is NP-complete.

Moreover, the reduction is linear size, the direct pair/triple correlation hypergraph is empty, every outside mediator has degree exactly 2, and every chain variable occurs in at most 9 target clauses.

---

## Proof

Take an arbitrary 3-CNF

\[
F=\bigwedge_{a=1}^{m}
(L_{a1}\vee L_{a2}\vee L_{a3})
\]

with three distinct non-tautological literal occurrences per clause.

Create one fresh Boolean variable

\[
z_{aj}
\]

for every literal occurrence \(L_{aj}\).

For each source clause \(a\), add the positive base clause

\[
B_a=z_{a1}\vee z_{a2}\vee z_{a3}.
\]

Thus the \(B_a\)'s are pairwise variable-disjoint type-1 chains.

Interpret \(z_{aj}\) as the truth value of the **literal occurrence** \(L_{aj}\), not directly as the source variable value.

---

## Consistency paths

Fix one original variable \(x\). List its occurrences as

\[
o_1,\ldots,o_t.
\]

Connect consecutive occurrences by a path.

If two consecutive occurrences have the same polarity, their occurrence-truth variables \(u,v\) must satisfy

\[
u=v.
\]

Encode equality by

\[
(\neg u\vee v)
\wedge
(u\vee\neg v).
\]

If the source occurrences have opposite polarity, require

\[
u\ne v,
\]

encoded by

\[
(u\vee v)
\wedge
(\neg u\vee\neg v).
\]

For every binary clause \(Q\) in these equality/disequality constraints, introduce a fresh mediator \(y_Q\) and replace \(Q\) by

\[
(Q\vee y_Q)
\wedge
(Q\vee\neg y_Q).
\]

By RESOLVE2 this is exactly equivalent to \(Q\).

---

## Correctness

Suppose \(F\) is satisfiable.

Assign every occurrence variable \(z_{aj}\) the truth value of the corresponding source literal \(L_{aj}\).

Every base clause \(B_a\) is true because source clause \(a\) is satisfied.

Occurrence values of the same original variable obey equality when the source literals have the same sign and disequality when they have opposite signs. Hence every consistency constraint is satisfied, and every mediator pair is satisfiable.

Thus the target is satisfiable.

Conversely, suppose the target is satisfiable.

By RESOLVE2, every occurrence-consistency binary clause holds.

Along the path of occurrences of each source variable, these equalities/disequalities force one globally consistent Boolean value for the original variable.

Every base chain state belongs to

\[
D=\{0,1\}^3\setminus\{000\},
\]

so at least one literal occurrence in every source clause is true.

Hence the recovered source assignment satisfies \(F\).

Therefore

\[
F\in 3SAT
\iff
R(F)\in \mathrm{EM2\text{-}CLEAN}.
\]

The reduction is polynomial, indeed linear. Membership in NP is immediate. Therefore \(\mathrm{EM2\text{-}CLEAN}\)-SAT is NP-complete. \(\square\)

---

# 5. Linear size and bounded occurrence

Let the source formula have \(m\) clauses and therefore \(3m\) literal occurrences.

If source variable \(x\) occurs \(t_x\) times, its consistency path uses \(t_x-1\) edges.

Hence the total number of consistency edges is

\[
E
=
\sum_x(t_x-1)
=
3m-n_{\rm used}
\le 3m.
\]

Each consistency edge uses two binary clauses.

Each binary clause uses one fresh degree-2 mediator and becomes two target 3-clauses.

Therefore:

\[
\#\text{mediators}=2E\le6m,
\]

\[
\#\text{residual 3-clauses}=4E\le12m,
\]

\[
\#\text{target clauses}=m+4E\le13m,
\]

and

\[
\#\text{target variables}=3m+2E\le9m.
\]

Every occurrence variable is incident to at most two consistency-path edges.

For each incident edge it participates in two binary constraints, each represented by two mediator clauses, hence at most four residual 3-clauses per path edge.

Including its base chain clause,

\[
\boxed{
\deg(z_{aj})\le1+2\cdot4=9.
}
\]

Every mediator has degree exactly 2.

Thus the target NP-hard family is bounded-occurrence.

---

# 6. Exact clean-core audit

The reduction satisfies the current project clean-core invariants.

## Type-1 chains

The base clauses

\[
B_a=z_{a1}\vee z_{a2}\vee z_{a3}
\]

are mutually variable-disjoint 1-chains.

Their chain solution space is exactly the seven-state type-1 domain \(D\).

## Empty direct-correlation hypergraph

Every non-base target clause contains one outside mediator.

Therefore there is **no residual 3-clause supported entirely on chain variables** that couples two or three chain triples.

Hence the project's direct rank-\(2/3\) correlation hypergraph has

\[
\boxed{0}
\]

hyperedges on this construction.

A maximal hypermatching is empty, so the entire chain set survives into the externally mediated core.

## Low mediator degree

Every outside mediator occurs exactly twice.

Therefore all mediators lie in the low-degree regime.

## Current branch rule

For one mediator,

\[
Q\vee y,
\qquad
Q\vee\neg y,
\]

setting either \(y=0\) or \(y=1\) activates exactly one binary pair constraint \(Q\).

Thus

\[
d_0=d_1=1.
\]

Using the project's current exact branch rule

\[
R(d_0,d_1)
=
\frac34
\left[
\left(\frac{416}{441}\right)^{d_0}
+
\left(\frac{416}{441}\right)^{d_1}
\right],
\]

we get

\[
\boxed{
R(1,1)
=
\frac{208}{147}
\approx1.414965986
>1.
}
\]

Therefore these mediators are not certified favorable by the existing high-degree branch criterion.

---

# 7. Finite implementation audit

Reproducible script:

\`experiments/source_reduction/residual_clean_core_hardness.py\`

Raw result:

\`results/source_reduction/2026-10-05_residual_clean_core_hardness.json\`

The test generated 60 random small source 3-CNFs and checked:

- source satisfiability equals dual occurrence-CSP satisfiability;
- every target mediator has degree 2;
- every mediator appears in both polarities;
- every residual mediator clause touches two distinct chain triples;
- the direct pair/triple correlation hypergraph is empty;
- chain-variable occurrence is at most 9.

All 60 checks passed.

This is a finite implementation sanity check only. RESIDUAL-HARD1 is proved analytically above.

---

# 8. Important correction to CLEANCORE-POLY1

CLEANCORE-POLY1 stated a caveat that its simple binary gadgets might be removed by the project's clean-core preprocessing because resolving the mediator exposes a direct pair constraint.

Under the **current structural definition** of the clean core, this is not an exclusion condition.

The direct-correlation hypergraph is constructed from residual clauses that are already supported entirely on chain variables.

The EM2 gadget has no such clause before mediator elimination.

Thus the gadget belongs to the current low-degree externally mediated clean-core schema.

If the project adopts an additional preprocessing rule that exhaustively resolves degree-2 opposite-polarity mediators before defining the clean core, that would define a **new stricter residual class**. RESIDUAL-HARD1 applies to the present definition, not automatically to that strengthened one.

---

# 9. What this means algorithmically

The theorem does **not** imply that the low-degree clean core requires exponential time.

It says something narrower and useful:

\[
\boxed{
\text{the current structural definition of the unresolved branch contains an NP-complete subclass.}
}
\]

Therefore the remaining case cannot be dismissed merely by observing:

- low outside-variable degree;
- absence of direct chain-only pair/triple clauses;
- an empty direct correlation hypergraph;
- failure of the current high-degree mediator branch test.

Some additional global algorithmic structure is required.

---

# 10. But the reduction itself exposes a new algorithmic route

The EM2 gadget is exactly resolvable.

After resolving all mediators, the target becomes:

1. disjoint positive type-1 chain clauses;
2. binary equality/disequality consistency constraints between chain coordinates.

These binary constraints are significantly stronger than the single-clause binary correlations previously analyzed.

This motivates a new exact characteristic calculation and matching analysis, developed in the companion consistency-pair note.

The key lesson is:

\[
\boxed{
\text{NP-hard residual structure can still be substantially easier than the current worst-case base}
}
\]

for an exact exponential algorithm.

Thus RESIDUAL-HARD1 is a classification result, not evidence that \(1.32793^n\) is tight.

---

# 11. Relation to literature

Liu defines a 1-chain's solution space as the satisfying assignments of its chain clauses; for a single positive 3-clause this is exactly the seven nonzero Boolean triples. His deterministic framework combines branching with derandomized local search over a Cartesian product of such chain solution spaces.

For bounded-occurrence context, Tovey showed that 3-SAT remains NP-complete when variables occur in at most four clauses. The present occurrence-splitting reduction does not need that restriction to obtain bounded target occurrence: its path construction already bounds each new occurrence variable by 9 target clauses.

---

# 12. Strict status

## PROVED/EXACT
- RESOLVE2.
- RESIDUAL-HARD1.
- linear reduction.
- target maximum occurrence bounds.
- empty direct pair/triple correlation hypergraph.
- degree-2 mediator property.
- \(d_0=d_1=1\) for every mediator.
- current branch ratio \(R(1,1)=208/147>1\).

## DOES NOT FOLLOW
- \(P\ne NP\);
- an exponential lower bound;
- hardness of a future stronger class obtained after exhaustive mediator resolution;
- tightness of the current deterministic \(1.32793^n\) analysis.

## NEW NEXT TARGET
Resolve the degree-2 mediators, compute exact covering characteristics of equality/disequality-correlated chain pairs, and determine how much matching coverage is forced in bounded-occurrence NP-hard source families.

---

## References

1. S. Cliff Liu, *Chain, Generalization of Covering Code, and Deterministic Algorithm for k-SAT*, ICALP 2018 / arXiv:1804.07901.
2. C. A. Tovey, *A simplified NP-complete satisfiability problem*, Discrete Applied Mathematics 8(1):85–89, 1984.

---

## Bottom line

The current low-degree externally mediated clean-core definition is expressive enough to encode arbitrary 3-SAT even when:

\[
\boxed{
\begin{array}{c}
\text{direct pair/triple hypergraph is empty},\\
\text{every mediator has degree 2},\\
d_0=d_1=1,\\
\text{and every chain variable has bounded occurrence}.
\end{array}
}
\]

The right next move is therefore not to argue that the residual core is structurally easy. It is to exploit the **specific strong correlations revealed after mediator elimination**.
