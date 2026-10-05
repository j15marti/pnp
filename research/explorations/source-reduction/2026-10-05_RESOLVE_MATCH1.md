# RESOLVE-MATCH1 — Weighted Pair Extraction from Low-Degree Mediators

**Date:** 2026-10-05  
**Repository:** \`j15marti/pnp\`  
**Global status:** **OPEN. P versus NP remains open.**

This note implements the RESOLVE-MATCH refinement proposed after RESIDUAL-HARD1 and CONSISTENCY-PAIR1.

The rule is:

1. eliminate every cheap degree-2 outside mediator;
2. if its resolvent is supported on exactly two clean chains, add the resulting relation to that chain pair;
3. combine all exposed constraints on the same pair;
4. compute the exact Liu characteristic of the resulting \(7\times7\) pair relation;
5. select a maximum-weight matching, where edge weight is the logarithmic DLS gain relative to two independent type-1 chains.

The main conclusion is two-sided:

\[
\boxed{
\text{RESOLVE-MATCH can substantially improve structured subclasses}
}
\]

but

\[
\boxed{
\text{low mediator degree alone does not force any positive pair-matching coverage.}
}
\]

Thus it is an exact-algorithm refinement, not yet a general improvement of the worst-case \(3\)-SAT base.

---

# 1. Baseline

A type-1 chain has characteristic

\[
\lambda_1=\frac37.
\]

Two independent type-1 chains therefore have

\[
\lambda_{\rm ind}
=
\lambda_1^2
=
\frac9{49}.
\]

For a correlated pair relation \(R\subseteq D^2\) with characteristic \(\lambda_R\), pairing the chains replaces the independent DLS factor

\[
\lambda_1^{-2}
\]

by

\[
\lambda_R^{-1}.
\]

The multiplicative gain is therefore

\[
g(R)
=
\frac{\lambda_{\rm ind}}{\lambda_R}.
\]

A useful correlation has

\[
\lambda_R>\lambda_{\rm ind},
\]

so \(g(R)<1\).

For weighted matching it is convenient to use

\[
w(R)
=
\log\frac{\lambda_R}{\lambda_{\rm ind}}.
\]

Maximizing total matching weight minimizes the DLS product.

---

# 2. Exact catalog of one-resolvent pair relations

Suppose a degree-2 mediator \(y\) has one positive and one negative clause,

\[
A\vee y,
\qquad
B\vee\neg y,
\]

and both pair terms \(A,B\) involve the same two type-1 chains.

There are

\[
3\cdot3\cdot2\cdot2
=
36
\]

possible pair terms on an ordered chain pair.

Exhaustively combining the two mediator sides and removing tautologies yields exactly

\[
\boxed{324}
\]

distinct non-tautological pair-relation schemas.

For each schema, the Liu characteristic system was solved exactly over the rationals.

All 324 were feasible.

There are only 14 distinct characteristic values:

| \(\lambda\) | number of relation schemas |
|---:|---:|
| \(81/440\) | 9 |
| \(135/733\) | 18 |
| \(75/407\) | 9 |
| \(81/439\) | 36 |
| \(135/731\) | 36 |
| \(81/437\) | 36 |
| \(81/436\) | 18 |
| \(27/145\) | 36 |
| \(45/241\) | 18 |
| \(81/431\) | 36 |
| \(27/143\) | 36 |
| \(81/416\) | 9 |
| \(27/137\) | 18 |
| \(1/5\) | 9 |

Hence every non-tautological same-pair single-mediator resolvent gives at least

\[
\boxed{
\lambda_{\min}
=
\frac{81}{440}
>
\frac9{49}.
}
\]

The weakest guaranteed relative DLS gain is therefore

\[
\boxed{
\frac{(9/49)}{(81/440)}
=
\frac{440}{441}
\approx0.997732.
}
\]

This gain is small but strictly positive.

The strongest one-resolvent relation in the catalog has

\[
\lambda=\frac15.
\]

---

# 3. Conditional balance from guaranteed matched fraction

Suppose a fraction \(f\) of type-1 chains can be covered by matched pair relations, and conservatively credit every matched pair only with

\[
\lambda_{\min}=\frac{81}{440}.
\]

The mixed DLS factor is

\[
\left(\frac43\right)^{n-3\nu}
\lambda_{\min}^{-f\nu/2}
\lambda_1^{-(1-f)\nu}.
\]

Balancing against the type-1 branching term \(3^\nu\) gives:

| matched chain fraction \(f\) | conditional balance base |
|---:|---:|
| 0 | 1.3279235672 |
| 1/4 | 1.3278276897 |
| 1/2 | 1.3277318679 |
| 3/4 | 1.3276361018 |
| 1 | 1.3275403912 |

Thus even the weakest catalog relation would improve the deterministic bottleneck if a positive matched fraction could be forced.

Stronger relations such as equality/disequality yield much larger improvements, as shown in CONSISTENCY-PAIR1.

---

# 4. RESOLVE-MATCH algorithm

For every degree-2 mediator:

1. form its exact resolvent;
2. discard tautologies;
3. inspect the number of distinct clean chains in the resolvent;
4. if exactly two chains occur, append the resolvent to that chain-pair bucket.

For each pair bucket:

1. intersect all pair relations induced by its resolvents;
2. obtain the exact allowed subset \(R\subseteq D^2\);
3. solve Liu's finite characteristic system;
4. if \(\lambda_R>\lambda_1^2\), add an edge with weight
   \[
   w_R=\log(\lambda_R/\lambda_1^2).
   \]

Then compute a maximum-weight matching.

Each matched edge is charged once and receives its full exact relation characteristic.

This automatically credits multiple degree-2 mediators between the same chains jointly rather than as unrelated clauses.

Reproducible implementation:

\`experiments/source_reduction/resolve_match.py\`

Raw output:

\`results/source_reduction/2026-10-05_resolve_match.json\`

---

# 5. Adversarial structural battery

Synthetic clean-core patterns were generated with:

\[
k=12
\]

chains and

\[
24
\]

degree-2 mediators, over 30 deterministic seeds per pattern.

The patterns were deliberately chosen to separate mediator degree from pair-matchability.

## PAIR-RICH

Both mediator sides use the same chain pair.

Results:

\[
\text{mean pair edges}=13.53,
\]

\[
\text{mean matched chain fraction}=0.739,
\]

with coverage ranging from

\[
0.50
\quad\text{to}\quad
0.833.
\]

Mean DLS multiplier relative to treating matched chains as independent:

\[
\boxed{0.9132}.
\]

This is the intended favorable regime.

---

## STAR

All pair-exposing mediators concentrate through one hub chain.

Many useful pair edges exist, but a matching can use only one of them.

Mean pair edges:

\[
6.1.
\]

Matched chain fraction:

\[
\boxed{\frac16}.
\]

Mean DLS multiplier:

\[
0.9466.
\]

Thus pair-edge count alone is not sufficient; overlap matters.

---

## SPREAD4

Each mediator side uses a disjoint chain pair, so its resolvent spans four chains.

Then:

\[
\boxed{
\text{pair graph is empty}.
}
\]

Matching coverage:

\[
\boxed{0}.
\]

DLS improvement:

\[
\boxed{1}.
\]

All mediators still have degree exactly 2.

---

## TRIPLE

The positive and negative pair terms share one chain and span three chains total.

Again:

\[
\boxed{
\text{pair graph is empty}.
}
\]

Matching coverage:

\[
0.
\]

---

## RANDOM

The two pair terms are independently random.

At this tested scale, pair-exposing coincidences are rare:

\[
\text{mean pair edges}=0.167,
\]

\[
\text{mean matched chain fraction}\approx0.0222.
\]

The mean DLS improvement is correspondingly negligible.

---

# 6. Theorem RESOLVE-MATCH-NOFORCE1

**Status: PROVED/EXACT as a structural counterexample.**

Low outside-mediator degree alone does not imply a positive RESOLVE-MATCH pair-coverage fraction.

### Proof

For every \(k\ge4\), construct degree-2 mediators whose positive pair term uses chains \(a,b\) and whose negative pair term uses two distinct chains \(c,d\), with

\[
\{a,b\}\cap\{c,d\}=\emptyset.
\]

Eliminating the mediator yields one width-4 resolvent supported on four clean chains.

No pair bucket receives this constraint.

Repeating the construction arbitrarily many times leaves the RESOLVE-MATCH pair graph empty.

Therefore no positive matching fraction follows from mediator degree 2 alone. \(\square\)

A three-chain version gives the same no-pair conclusion when the two mediator sides overlap in exactly one chain.

---

# 7. Consequence for the general deterministic bound

RESOLVE-MATCH does not currently improve the unconditional worst-case type-1 bottleneck.

The reason is structural, not numerical.

To turn the catalog gain

\[
\lambda_R>\frac9{49}
\]

into a global bound, one needs a theorem forcing enough **pair-exposing** low-degree mediators with sufficiently nonconcentrated incidence.

Possible hypotheses that would suffice include a lower bound on pair-exposing edge density together with an upper bound on pair-graph degree.

For example, if the exposed pair graph has \(E\) edges and maximum degree \(\Delta\), greedy matching gives

\[
|M|
\ge
\frac{E}{2\Delta-1}.
\]

But neither \(E=\Omega(\nu)\) nor bounded \(\Delta\) follows from the present low-mediator-degree condition.

Therefore the load-bearing missing statement is now:

\[
\boxed{
\text{low-degree clean core}
\Longrightarrow
\text{pair/hyperrelation density or another exploitable global structure}.
}
\]

---

# 8. Why this is still useful

The rule significantly strengthens the exact algorithm on structured formulas.

In particular, the NP-hard occurrence-consistency subclass from RESIDUAL-HARD1 is pair-rich after mediator elimination.

There the relations are equality/disequality, with exact characteristics

\[
\lambda_=
=
\frac{81}{391},
\qquad
\lambda_{\ne}
=
\frac{27}{130},
\]

far above the catalog minimum \(81/440\).

CONSISTENCY-PAIR1 already showed that bounded-occurrence controls force a constant matching fraction and hence substantial improvement.

Thus:

\[
\boxed{
\text{NP-hardness of the clean-core schema}
\not\Rightarrow
\text{worst-case exact-algorithm behavior}.
}
\]

The worst-case obstruction can move into the SPREAD4/TRIPLE-style regime where local mediator elimination exposes higher-arity relations rather than pair relations.

---

# 9. Natural extension: RESOLVE-HYPERMATCH

The adversarial battery identifies the next exact-algorithm refinement.

Every degree-2 mediator resolvent is supported on at most four chains.

Therefore, instead of discarding three- and four-chain resolvents, construct a rank-\(2/3/4\) hypergraph in which each hyperedge is labeled by the exact relation induced on its participating chain states.

Then:

1. compute exact characteristic values for these small relation blocks;
2. extract a weighted hypermatching;
3. credit each disjoint block once in DLS.

This subsumes RESOLVE-MATCH.

The key question becomes whether low-degree externally mediated cores force a positive weighted rank-\(\le4\) hypermatching after cheap mediator elimination.

Unlike the pair-only statement, every non-tautological degree-2 mediator contributes some rank-\(\le4\) relation.

The remaining obstruction would be heavy overlap/concentration, which may interact with high-degree branching or sparsification.

This is the most promising continuation of the exact-algorithm branch.

---

# 10. SRAS interpretation

RESOLVE-MATCH is also a useful accounting correction.

The computation should not charge a hidden pair relation if a polynomial local elimination pass exposes it.

Instead that relation belongs to the already-credited UNIVERSAL-EVALUATOR / cheap-inference layer.

The adversarial SPREAD4 construction shows where the unresolved information moves:

\[
\boxed{
\text{pair summary}
\longrightarrow
\text{higher-arity local relation}.
}
\]

The next SRAS question is whether repeated cheap elimination necessarily accumulates into a polynomial-size global relation system or eventually forces a genuinely hard acquisition step.

No such theorem is proved here.

---

# 11. Strict status

## PROVED/EXACT
- complete 324-relation same-pair catalog;
- 14 exact characteristic values;
- minimum \(\lambda=81/440\);
- weakest relative gain \(440/441\);
- RESOLVE-MATCH-NOFORCE1.

## COMPUTATIONAL
- 30-seed synthetic pattern battery;
- maximum-weight-matching measurements.

## EXACT CONDITIONAL ACCOUNTING
- balance-base improvements as a function of matched-chain fraction.

## NOT PROVED
- positive pair coverage in every low-degree clean core;
- improved general 3-SAT deterministic base;
- lower bound for SAT;
- \(P\ne NP\).

---

## Bottom line

RESOLVE-MATCH works exactly as intended when low-degree mediators expose pair relations, and every such single-mediator pair relation is at least slightly better than independence.

But the worst-case clean core can route every degree-2 mediator through three or four chains and make the pair graph empty.

So the next exact target is not another pair lemma. It is:

\[
\boxed{
\textbf{RESOLVE-HYPERMATCH on rank }2/3/4\textbf{ relations}.
}
\]

That is the smallest refinement that closes the SPREAD4/TRIPLE escape found by this experiment.
