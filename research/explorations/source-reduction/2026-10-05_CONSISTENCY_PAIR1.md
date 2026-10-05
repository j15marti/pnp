# CONSISTENCY-PAIR1 — Exact Covering Characteristics for Equality/Disequality-Correlated Type-1 Chains

**Date:** 2026-10-05  
**Repository:** \`j15marti/pnp\`  
**Global status:** **OPEN. P versus NP remains open.**

This note follows RESIDUAL-HARD1.

The residual NP-hardness construction uses degree-2 mediators that resolve exactly to Boolean equality/disequality constraints between coordinates of two type-1 chains. These relations are substantially stronger than the single binary cross-chain clause analyzed previously.

The purpose here is to compute their exact Liu characteristic values and quantify what a matching of such constraints buys in the DLS accounting.

---

# 1. Setup

A type-1 chain has state space

\[
D=\{0,1\}^3\setminus\{000\},
\qquad |D|=7.
\]

Two independent type-1 chains therefore have 49 joint states and characteristic

\[
\lambda_{\rm ind}
=
\left(\frac37\right)^2
=
\frac9{49}.
\]

Fix one coordinate in each chain.

For equality,

\[
A_{=}
=
\{(u,v)\in D^2:u_1=v_1\}.
\]

For disequality,

\[
A_{\ne}
=
\{(u,v)\in D^2:u_1\ne v_1\}.
\]

Because one coordinate equals 0 in 3 states of \(D\) and equals 1 in 4 states,

\[
|A_=|
=
3^2+4^2
=
25,
\]

and

\[
|A_{\ne}|
=
2\cdot3\cdot4
=
24.
\]

---

# 2. Liu characteristic LP

For \(k=3\), Liu's characteristic value for a solution space \(A\) is the unique feasible \(\lambda\) for which there is a distribution \(\pi\) satisfying

\[
\sum_{a\in A}\pi(a)=1
\]

and

\[
\lambda
=
\sum_{a\in A}
\pi(a)
\left(\frac12\right)^{d(a,a^*)}
\qquad
\forall a^*\in A.
\]

Equivalently, let

\[
M_{a^*,a}
=
2^{-d(a,a^*)}.
\]

Then

\[
M\pi
=
\lambda \mathbf1,
\qquad
\mathbf1^\top\pi=1.
\]

The companion script solves this system exactly over the rationals.

Reproducible script:

\`experiments/source_reduction/consistency_pair_characteristics.py\`

Raw results:

\`results/source_reduction/2026-10-05_consistency_pair_characteristics.json\`

---

# 3. Theorem CONSISTENCY-CHAR1

**Status: PROVED/EXACT by exact rational solution of Liu's finite LP.**

For coordinate equality between two type-1 chains,

\[
\boxed{
\lambda_{=}
=
\frac{81}{391}
\approx0.2071611253.
}
\]

For coordinate disequality,

\[
\boxed{
\lambda_{\ne}
=
\frac{27}{130}
\approx0.2076923077.
}
\]

Both strictly exceed the independent-pair value

\[
\frac9{49}
\approx0.1836734694.
\]

Thus both relations yield a strict DLS improvement.

The exact relative DLS factors are

\[
\boxed{
\frac{(9/49)}{(81/391)}
=
\frac{391}{441}
\approx0.8866213152
}
\]

for equality, and

\[
\boxed{
\frac{(9/49)}{(27/130)}
=
\frac{130}{147}
\approx0.8843537415
}
\]

for disequality.

The equality relation is the slightly worse of the two and is therefore the conservative value for mixed consistency edges.

---

# 4. Comparison with the earlier single-binary-clause correlation

The earlier outside-mediator branch analysis used one activated binary clause and obtained

\[
\lambda_{\rm bin}
=
\frac{81}{416}
\approx0.1947115385.
\]

The equality/disequality constraints are stronger because each relation is represented by two binary clauses.

Numerically,

\[
\lambda_{=}
=
\frac{81}{391}
>
\frac{81}{416}
=
\lambda_{\rm bin}.
\]

Thus after exact mediator elimination, an occurrence-consistency edge should be credited as one **full equality/disequality pair relation**, not as just one ordinary binary-clause correlation.

---

# 5. Conditional all-paired bottleneck

Suppose all type-1 chains can be covered by disjoint equality-correlated pairs.

If \(\nu\) is the number of chains, the DLS factor becomes

\[
\left(\frac43\right)^{n-3\nu}
\lambda_=^{-\nu/2}.
\]

Balancing this against the type-1 branching term

\[
3^\nu
\]

gives the conditional base

\[
\boxed{
c_{=,\rm all}
\approx
1.3087695488.
}
\]

For all disequality pairs,

\[
\boxed{
c_{\ne,\rm all}
\approx
1.3083861020.
}
\]

These are conditional exact-accounting values, not new general 3-SAT upper bounds.

They are noteworthy because they lie much closer to the randomized PPSZ scale than the original deterministic type-1 bottleneck.

---

# 6. Guaranteed matching inside an NP-hard source family

Tovey's bounded-occurrence result, as summarized by Berman-Karpinski-Scott, gives an NP-hard source family in which every source variable occurs exactly four times.

For such a source formula with \(m\) clauses and \(n_s\) source variables,

\[
3m=4n_s.
\]

In the occurrence-splitting construction of RESIDUAL-HARD1, connect the four occurrences of each source variable by a path.

Each source variable contributes 3 consistency edges, hence

\[
E
=
3n_s
=
\frac{9m}{4}.
\]

Construct the multigraph \(G_{\rm con}\) whose vertices are the \(m\) chain clauses and whose edges are occurrence-consistency constraints.

Each source clause contains three occurrences, and each occurrence is incident to at most two edges of its variable path, so

\[
\Delta(G_{\rm con})\le6.
\]

A greedy matching in a multigraph of maximum degree \(\Delta\) has size at least

\[
\frac{|E|}{2\Delta-1}.
\]

Therefore

\[
|M|
\ge
\frac{(9m/4)}{11}
=
\frac{9m}{44}.
\]

The matching covers at least

\[
2|M|
\ge
\frac{9m}{22}
\]

chain vertices.

Hence the guaranteed covered-chain fraction is

\[
\boxed{
f\ge\frac9{22}
\approx0.40909.
}
\]

This is a purely graph-theoretic matching guarantee on this NP-hard control family.

---

# 7. Mixed conditional balance

Credit the matched fraction \(f\) with the conservative equality characteristic

\[
\lambda_*=\frac{81}{391}
\]

and leave the unmatched fraction with the ordinary type-1 characteristic

\[
\lambda_1=\frac37.
\]

Then the mixed DLS factor is

\[
\left(\frac43\right)^{n-3\nu}
\lambda_*^{-f\nu/2}
\lambda_1^{-(1-f)\nu}.
\]

At the guaranteed fraction

\[
f=\frac9{22},
\]

balancing against \(3^\nu\) gives

\[
\boxed{
c_{\rm mixed}
\approx
1.3198092830.
}
\]

Again this is a conditional accounting bound for this structured family, not a general 3-SAT theorem.

---

# 8. DLS-only view after exact mediator elimination

For the RESIDUAL-HARD1 occurrence-splitting construction, after eliminating all degree-2 mediators there are only the \(3m\) occurrence variables, and the \(m\) disjoint base type-1 chains cover all variables.

Thus

\[
n=3m
\]

and the free-variable factor

\[
\left(\frac43\right)^{n-3m}
\]

is 1.

With no pair credit, the DLS-only per-variable base is

\[
\left(\frac73\right)^{1/3}
\approx
\boxed{1.326352403}.
\]

At guaranteed matching coverage

\[
f=\frac9{22},
\]

the conservative DLS-only base becomes

\[
\boxed{
1.315514446.
}
\]

If every chain were equality-paired, it would become

\[
\boxed{
1.300015777.
}
\]

These values are useful as structured-family diagnostics only.

---

# 9. Interpretation

RESIDUAL-HARD1 and CONSISTENCY-PAIR1 together give an important correction.

The current externally mediated clean-core definition contains an NP-hard subclass.

But that subclass is **not invisible** to stronger correlation accounting.

After the degree-2 mediators are resolved:

\[
\boxed{
\text{hidden occurrence consistency}
\to
\text{strong equality/disequality pair relations}.
}
\]

A matching of those relations yields substantially more DLS improvement than the single-binary-clause characteristic.

So the correct conclusion is not:

> the low-degree clean core is hard and therefore the current exact bound is tight.

It is:

> the low-degree clean core can retain NP-complete expressive power, but some of that power may be exposed as strong matchable correlations after local elimination.

---

# 10. New preprocessing/refinement rule

This suggests an exact-algorithm refinement before declaring a mediator core unresolved.

### RESOLVE-MATCH rule

1. Detect degree-2 mediators with one positive and one negative occurrence.
2. Eliminate the mediator by exact resolution.
3. If the resolvent is a binary chain-pair relation, insert it into a **strong pair graph**.
4. Recognize equality/disequality pairs as two-clause relations rather than counting each binary clause separately.
5. Extract a maximum or maximal matching of the strong pair graph.
6. Credit each matched pair with the appropriate exact characteristic.

This strictly strengthens the current direct-correlation hypergraph, which only sees chain-only residual 3-clauses before mediator elimination.

---

# 11. New residual target: resolution-clean core

After applying RESOLVE-MATCH, define a stricter residual family in which no cheap low-degree mediator elimination exposes:

- a binary pair relation;
- a chain-only 3-clause giving a direct pair/triple correlation;
- another already-characterized low-width relation.

Call this tentative family the

\[
\boxed{\text{resolution-clean core}.}
\]

The next question is:

\[
\boxed{
\text{does the resolution-clean core still contain an NP-hard subclass?}
}
\]

If yes, the structural program must go beyond low-width elimination and pair matching.

If no, the new preprocessing may close a substantial portion of the previous low-degree obstruction.

This is now a sharper target than the old generic low-degree mediator case.

---

# 12. Strict status

## PROVED/EXACT
- \(\lambda_=81/391\).
- \(\lambda_{\ne}=27/130\).
- exact relative DLS factors \(391/441\) and \(130/147\).
- matching bound \(f\ge9/22\) for the exactly-four-occurrence source control after occurrence-path splitting.

## EXACT CONDITIONAL ACCOUNTING
- all-paired balance bases \(1.30877\) and \(1.30839\).
- mixed \(f=9/22\) balance base \(1.31981\).
- structured DLS-only diagnostic bases.

## OPEN
- whether the general low-degree clean core always exposes enough resolvable/matchable strong relations;
- complexity of the stricter resolution-clean core;
- whether this yields a new general deterministic 3-SAT upper bound;
- any P-vs-NP lower bound.

---

# References

1. S. Cliff Liu, *Chain, Generalization of Covering Code, and Deterministic Algorithm for k-SAT*, ICALP 2018 / arXiv:1804.07901.
2. C. A. Tovey, *A simplified NP-complete satisfiability problem*, Discrete Applied Mathematics 8(1):85–89, 1984.
3. P. Berman, M. Karpinski, A. D. Scott, *Computational complexity of some restricted instances of 3-SAT*, Discrete Applied Mathematics 155(5):649–653, 2007.

---

## Bottom line

The degree-2 clean-core NP-hardness construction survives the original structural filters, but mediator elimination reveals much stronger pair correlations than were previously credited.

The new most concrete target is therefore:

\[
\boxed{
\text{low-degree clean core}
\to
\text{RESOLVE-MATCH}
\to
\text{resolution-clean core}.
}
\]

That refinement may be more useful for improving the exact algorithm than treating all low-degree external mediation as one unresolved case.
