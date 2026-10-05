# CLAUSECHAR-HYPERMATCH1 — Exact Rank-2/3/4 Characteristics and Greedy RESOLVE-HYPERMATCH

**Date:** 2026-10-05  
**Repository:** \`j15marti/pnp\`  
**Global status:** **OPEN. P versus NP remains open.**

This note extends RESOLVE-MATCH1.

The pair-only rule loses degree-2 mediator resolvents spanning three or four clean chains. Here we derive an exact characteristic formula for every single non-tautological mediator resolvent and use it in a polynomial greedy rank-\(2/3/4\) hypermatching.

The result closes the synthetic SPREAD4/TRIPLE escape, but exposes a stronger obstruction:

\[
\boxed{
\text{low mediator degree does not prevent all useful relations from concentrating on one chain.}
}
\]

Thus a general deterministic-base improvement still needs a density/incidence lemma or a separate high-chain-incidence branch.

---

# 1. Local type-1 kernel

Let

\[
D=\{0,1\}^3\setminus\{000\}.
\]

For \(u,v\in D\), define the Liu \(k=3\) local kernel

\[
K_{u,v}=2^{-d(u,v)}.
\]

Let

\[
N=K^{-1},
\qquad
z=N\mathbf 1,
\qquad
t=\mathbf 1^\top z.
\]

Exact rational calculation gives

\[
\boxed{
t=\frac73
}
\]

and hence the one-chain characteristic

\[
\lambda_1=t^{-1}=\frac37.
\]

---

# 2. Local falsifying blocks

For a consistent set \(L\) of literals drawn from one type-1 chain, let

\[
B(L)\subseteq D
\]

be the states on which every literal in \(L\) is false.

Define

\[
a(B)
=
z_B^\top
\left(N[B,B]\right)^{-1}
z_B.
\]

For all possible non-tautological local literal patterns on one 3-bit chain, the exact values are:

### One local literal

\[
\boxed{
a(B)\in
\left\{
\frac59,\frac23
\right\}.
}
\]

Multiplicity over coordinate/sign choices:

| \(a(B)\) | count |
|---:|---:|
| \(5/9\) | 3 |
| \(2/3\) | 3 |

### Two local literals

\[
\boxed{
a(B)\in
\left\{
\frac19,\frac{2}{15},\frac29
\right\}.
}
\]

| \(a(B)\) | count |
|---:|---:|
| \(1/9\) | 3 |
| \(2/15\) | 3 |
| \(2/9\) | 6 |

### Three local literals

\[
\boxed{
a(B)\in
\left\{
0,\frac1{45},\frac1{21},\frac19
\right\}.
}
\]

| \(a(B)\) | count |
|---:|---:|
| \(0\) | 1 |
| \(1/45\) | 3 |
| \(1/21\) | 1 |
| \(1/9\) | 3 |

The zero case is the positive local base clause itself: its falsifying state would be \(000\), which is not in \(D\).

---

# 3. Theorem CLAUSECHAR1

**Status: PROVED/EXACT, with finite local feasibility certificate.**

Let \(C\) be one non-tautological clause whose literals lie on \(r\) distinct type-1 chains.

For each participating chain \(i\), let \(B_i\subseteq D\) be the states falsifying all literals of \(C\) belonging to chain \(i\).

Then the satisfying state space of \(C\) is

\[
A
=
D^r
\setminus
(B_1\times\cdots\times B_r).
\]

Its characteristic value is

\[
\boxed{
\lambda(C)
=
\left[
\left(\frac73\right)^r
-
\prod_{i=1}^{r} a(B_i)
\right]^{-1}.
}
\]

---

## Proof

The full \(r\)-chain kernel is

\[
M=K^{\otimes r},
\]

with

\[
M^{-1}=N^{\otimes r}.
\]

Partition the full state space as

\[
D^r=A\sqcup B,
\qquad
B=B_1\times\cdots\times B_r.
\]

Write the inverse kernel in blocks:

\[
M^{-1}
=
\begin{pmatrix}
N_{AA}&N_{AB}\\
N_{BA}&N_{BB}
\end{pmatrix}.
\]

By the block-inverse / Schur-complement identity,

\[
M_A^{-1}
=
N_{AA}
-
N_{AB}N_{BB}^{-1}N_{BA}.
\]

Let

\[
z_{\rm full}=M^{-1}\mathbf1
=
z^{\otimes r}.
\]

Then

\[
\mathbf1_A^\top M_A^{-1}\mathbf1_A
=
\mathbf1^\top M^{-1}\mathbf1
-
z_B^\top N_{BB}^{-1}z_B.
\]

The first term factorizes as

\[
\mathbf1^\top M^{-1}\mathbf1
=
t^r
=
\left(\frac73\right)^r.
\]

Since \(B\) is a Cartesian product,

\[
N_{BB}
=
\bigotimes_i N[B_i,B_i],
\]

and

\[
z_B
=
\bigotimes_i z_{B_i}.
\]

Therefore

\[
z_B^\top N_{BB}^{-1}z_B
=
\prod_i
z_{B_i}^\top
N[B_i,B_i]^{-1}
z_{B_i}
=
\prod_i a(B_i).
\]

Thus

\[
\mathbf1_A^\top M_A^{-1}\mathbf1_A
=
\left(\frac73\right)^r
-
\prod_i a(B_i),
\]

and the characteristic value is its reciprocal.

For the finite local literal patterns relevant to degree-2 mediator resolvents, the companion exact calculation also checks the nonnegativity of the resulting characteristic distribution. \(\square\)

---

# 4. Exhaustive degree-2 mediator catalog

A degree-2 outside mediator has one positive and one negative pair-term clause.

Eliminating it produces one clause containing at most four chain literals and supported on \(2,3,\) or \(4\) distinct chains.

Up to canonical relabeling, exhaustive enumeration gives:

| rank | relation schemas |
|---:|---:|
| 2 | 324 |
| 3 | 1512 |
| 4 | 1296 |
| **total** | **3132** |

CLAUSECHAR1 evaluates every schema exactly.

For all 324 rank-2 schemas, the formula was independently cross-checked against a direct rational solve of the full characteristic system.

All 324 checks agree.

Reproducible verifier:

\`experiments/source_reduction/clause_characteristics.py\`

Raw result:

\`results/source_reduction/2026-10-05_clause_characteristics.json\`

---

# 5. Exact worst single-resolvent constants

For each rank, compare against \(r\) independent type-1 chains:

\[
\lambda_{\rm ind}(r)
=
\left(\frac37\right)^r.
\]

## Rank 2

\[
\boxed{
\lambda_{\min,2}
=
\frac{81}{440}.
}
\]

Independent value:

\[
\left(\frac37\right)^2
=
\frac9{49}.
\]

Weakest relative DLS factor:

\[
\boxed{
g_2
=
\frac{440}{441}
\approx0.997732.
}
\]

---

## Rank 3

\[
\boxed{
\lambda_{\min,3}
=
\frac{729}{9236}.
}
\]

Independent value:

\[
\left(\frac37\right)^3
=
\frac{27}{343}
=
\frac{729}{9261}.
\]

Weakest relative DLS factor:

\[
\boxed{
g_3
=
\frac{9236}{9261}
\approx0.997301.
}
\]

For comparison, the familiar all-positive three-chain single clause gives

\[
\frac{729}{9136},
\]

which is stronger than the worst rank-3 width-4 relation.

---

## Rank 4

\[
\boxed{
\lambda_{\min,4}
=
\frac{6561}{193856}.
}
\]

Independent value:

\[
\left(\frac37\right)^4
=
\frac{81}{2401}
=
\frac{6561}{194481}.
\]

Weakest relative DLS factor:

\[
\boxed{
g_4
=
\frac{193856}{194481}
\approx0.996786.
}
\]

Thus every non-tautological degree-2 mediator resolvent gives a strict DLS gain over treating its participating clean chains as independent, regardless of whether it spans 2, 3, or 4 chains.

The gain can be very small, but it is exact and positive.

---

# 6. Conditional full-coverage balance

If every type-1 chain were covered by disjoint worst-case rank-\(r\) blocks, the type-1 branching/DLS balance would become:

| rank \(r\) | weakest full-coverage balance base |
|---:|---:|
| 2 | 1.3275403912 |
| 3 | 1.3276193206 |
| 4 | 1.3276518216 |

All improve on the baseline

\[
1.3279235672.
\]

For rank 4, if only a fraction \(f\) of chains is covered:

| \(f\) | conditional balance base |
|---:|---:|
| 0 | 1.3279235672 |
| 1/4 | 1.3278555888 |
| 1/2 | 1.3277876384 |
| 3/4 | 1.3277197160 |
| 1 | 1.3276518216 |

These are exact-accounting consequences of a stated coverage fraction, not general 3-SAT bounds.

---

# 7. Polynomial greedy RESOLVE-HYPERMATCH

Maximum weighted rank-\(3/4\) set packing is not used.

Instead use a polynomial greedy rule:

1. eliminate each degree-2 mediator;
2. compute its exact clause characteristic by CLAUSECHAR1;
3. assign edge weight
   \[
   w(C)
   =
   \log
   \frac{\lambda(C)}
   {(3/7)^{r(C)}};
   \]
4. order exposed relations by decreasing weight;
5. greedily retain a relation when its chain support is disjoint from all previously retained supports.

The selected relations form a maximal rank-\(2/3/4\) hypermatching.

Every selected block is credited once in the DLS product.

Reproducible implementation:

\`experiments/source_reduction/resolve_hypermatch.py\`

Raw output:

\`results/source_reduction/2026-10-05_resolve_hypermatch.json\`

---

# 8. Synthetic adversarial battery

Parameters:

\[
k=12
\]

clean chains,

\[
24
\]

degree-2 mediators,

30 deterministic seeds per pattern.

## Pair-rich

Mean chain coverage:

\[
\boxed{0.728}.
\]

Mean selected blocks:

\[
4.37.
\]

Mean DLS multiplier relative to independent treatment:

\[
0.9116.
\]

---

## SPREAD4

Every degree-2 mediator has its two pair terms on four distinct chains.

The pair-only RESOLVE-MATCH graph was empty.

RESOLVE-HYPERMATCH now recovers the relations.

Mean coverage:

\[
\boxed{0.667}.
\]

Mean selected blocks:

\[
2.0.
\]

Mean relative DLS factor:

\[
0.98848.
\]

Thus the previous pair-only SPREAD4 escape is closed in this finite battery.

---

## TRIPLE

The two pair terms span exactly three chains.

Mean coverage:

\[
\boxed{0.692}.
\]

Mean selected blocks:

\[
2.77.
\]

Mean relative DLS factor:

\[
0.95967.
\]

Again the pair-only loss is largely recovered.

---

## Random

Mean coverage:

\[
\boxed{0.633}.
\]

Mean relative DLS factor:

\[
0.97521.
\]

---

## STAR

All exposed relations share one hub chain.

Mean selected blocks:

\[
\boxed{1}.
\]

Mean chain coverage:

\[
\boxed{\frac16}.
\]

For growing \(k\), the same construction can force coverage

\[
O(1/k).
\]

This is the surviving adversarial obstruction.

---

# 9. Theorem HYPERMATCH-DENSITY1

**Status: PROVED/EXACT.**

Let \(H\) be a hypergraph of non-tautological resolved mediator relations on \(\nu\) clean chains.

Suppose:

- every hyperedge has rank at most 4;
- \(H\) has \(M\) hyperedges;
- every chain belongs to at most \(\Delta\) hyperedges.

Then every maximal hypermatching contains at least

\[
\boxed{
\frac{M}{4\Delta}
}
\]

hyperedges.

### Proof

A selected hyperedge contains at most four vertices.

Each of those vertices is incident to at most \(\Delta\) hyperedges.

Therefore selecting one edge can delete/intersect at most \(4\Delta\) unresolved hyperedges.

A maximal greedy process must delete all \(M\) original edges.

Hence at least \(M/(4\Delta)\) selections are required. \(\square\)

Since every selected relation touches at least two chains, the matched chain count is at least

\[
\boxed{
\frac{M}{2\Delta}.
}
\]

Thus if

\[
M\ge \alpha\nu
\]

and

\[
\Delta\le D
\]

for constants \(\alpha,D>0\), then a constant chain fraction

\[
\boxed{
f\ge\frac{\alpha}{2D}
}
\]

is guaranteed.

This would immediately imply a strict improvement of the type-1 bottleneck using the weakest rank-\(2/3/4\) constants above.

---

# 10. Theorem HYPERMATCH-NOFORCE1

**Status: PROVED/EXACT.**

Low outside-mediator degree alone does not imply constant hypermatching coverage.

### Proof

Fix one clean chain \(T_0\).

Construct arbitrarily many degree-2 mediators whose resolvents all include \(T_0\) together with one to three other clean chains.

Every resulting rank-\(2/3/4\) relation intersects every other through \(T_0\).

Therefore every hypermatching has size at most 1.

As the number of clean chains tends to infinity, the covered chain fraction tends to zero. \(\square\)

Hence the mediator-degree condition controls the degree of the **outside variable**, not the incidence degree \(\Delta\) of clean chains in the resolved-relation hypergraph.

These are distinct resources.

---

# 11. Connection to sparsification

The sparsification lemma is potentially relevant to the exact-algorithm branch because bounded-occurrence sparse subinstances can control incidence degree.

But this comes with a critical accounting guard.

Sparsification expresses a \(k\)-CNF as a disjunction of up to

\[
2^{\varepsilon n}
\]

sparse subinstances.

Therefore:

- for an exact exponential algorithm, one may potentially trade the \(2^{\varepsilon n}\) overhead against a sufficiently larger base improvement;
- for the P-vs-NP/SRAS extraction program, sparsification is **not** a polynomial contraction and cannot be used for free.

No general improvement is claimed here from sparsification.

---

# 12. New exact-algorithm hinge

RESOLVE-HYPERMATCH reduces the unresolved structural question to a sharper dichotomy.

Let \(H_{\rm res}\) be the rank-\(2/3/4\) hypergraph of cheap resolved mediator relations.

Either:

### A. Bounded chain incidence

\[
\Delta(H_{\rm res})=O(1)
\]

and there are linearly many exposed relations.

Then HYPERMATCH-DENSITY1 forces constant hypermatching coverage and the Liu balance improves.

### B. High chain incidence

Some clean chain participates in many resolved relations.

Then the current analysis needs a new branch/reduction rule exploiting **high chain incidence**.

This is distinct from the existing rule that branches on a high-degree outside mediator.

Thus the next natural algorithmic target is:

\[
\boxed{
\textbf{high-chain-incidence branching}
}
\]

or another exact reduction that turns concentration around one clean chain into a provable recurrence gain.

This is more precise than the previous generic “low-degree clean core” obstruction.

---

# 13. SRAS interpretation

The same dichotomy has a source-accounting interpretation.

Cheap local mediator elimination transforms hidden constraints into a rank-\(\le4\) relation system.

If the relation system spreads out, disjoint blocks give independent reusable reduction credit.

If it concentrates, a small source region controls many continuation obligations.

Thus concentration should be treated as a candidate LOCALIZE/high-influence event rather than as missing information.

A successful universal source-to-reduction theorem would need to formalize exactly this kind of alternative.

No such unrestricted theorem is proved here.

---

# 14. Strict status

## PROVED/EXACT
- CLAUSECHAR1.
- finite local \(a(B)\) table.
- exhaustive 3132 mediator-resolvent schema enumeration.
- all 324 direct rank-2 cross-checks.
- worst rank-\(2/3/4\) characteristic constants.
- HYPERMATCH-DENSITY1.
- HYPERMATCH-NOFORCE1.

## COMPUTATIONAL
- 30-seed rank-\(2/3/4\) greedy hypermatching battery.

## EXACT CONDITIONAL ACCOUNTING
- balance improvements under stated coverage fractions.

## OPEN
- a general lower bound on relation density \(M/\nu\);
- a general upper bound on clean-chain incidence \(\Delta\);
- a favorable high-chain-incidence recurrence;
- a resulting improved deterministic 3-SAT base;
- any P-vs-NP lower bound.

---

## Bottom line

The low-degree clean-core obstruction has narrowed again.

Every degree-2 mediator supplies a small relation with a strictly favorable Liu characteristic, and rank-\(2/3/4\) hypermatching captures the SPREAD4/TRIPLE cases that pair matching misses.

The only simple adversarial escape left in this layer is **concentration**:

\[
\boxed{
\text{many cheap relations sharing the same few clean chains}.
}
\]

That makes high-chain-incidence branching the next concrete exact-algorithm target.
