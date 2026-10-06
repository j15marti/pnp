# HIGHINC-CLOSE1 — Finite High-Incidence Pattern Audit for Resolved Type-1-Chain Relations

**Date:** 2026-10-05  
**Repository:** j15marti/pnp  
**Global status:** **OPEN. P versus NP remains open.**

This note closes the finite local-pattern audit left open by LINK-DICHOTOMY1.

The result is an exact statement about the Liu/DLS potential in the current
resolved rank-<=4 type-1-chain interaction model. It is not an unrestricted
SAT lower bound and does not by itself yield a new published 3-SAT
running-time bound.

---

## 1. Setup

Let

\[
D=\{0,1\}^3\setminus\{000\}
\]

be the positive type-1 chain domain, with characteristic

\[
\lambda_1=\frac37.
\]

Fix one chain

\[
T=(x_1,x_2,x_3).
\]

In the current resolved rank-<=4 mediator schema, a single resolved clause
contains at most two literals from T. Thus the nonempty local part on T has one
of 18 literal patterns:

- 3 positive one-literal patterns;
- 3 negative one-literal patterns;
- 3 ++ two-literal patterns;
- 6 mixed +- two-literal patterns;
- 3 -- two-literal patterns.

Up to coordinate permutation, these are only five sign types.

Suppose m incident resolved clauses share the same local pattern Q(T),

\[
Q(T)\vee P_1,\ldots,Q(T)\vee P_m,
\]

and the outside chain supports of the petals \(P_i\) are pairwise disjoint.

Branch exactly on the local condition Q:

\[
F
\equiv
(F\wedge Q)\vee(F\wedge\neg Q).
\]

In the Q=0 branch, every selected incident clause exposes the petal \(P_i\).

---

## 2. Conservative petal credit

A one-literal center can leave a nonempty petal supported on at most three
chains.

A two-literal center can leave a nonempty petal supported on at most two
chains.

From CLAUSECHAR1, the weakest currently catalogued nontrivial single-resolvent
gain among all such petals is conservatively

\[
\boxed{
g=\frac{440}{441}.
}
\]

Rank-1 and rank-3 petals are strictly better, so using g for every petal is
safe for the local DLS-potential calculation.

If a selected petal is empty after Q=0, that branch is immediately
unsatisfiable and is better than the bound below.

---

# 3. Theorem LOCALPATTERN-BRANCH1

**Status: PROVED/EXACT in the declared DLS-potential model.**

For each of the five local sign types, let \(a_Q\) be the relative local DLS
factor of the Q=1 child and \(b_Q\) the relative factor of the Q=0 child before
petal credit.

Then

\[
\boxed{
R_Q(m)
=
a_Q+b_Q g^m
}
\]

upper-bounds the sum of the two child local-potential contributions relative
to the parent type-1-chain contribution.

The exact coefficients and smallest strict thresholds are:

| center type | \(a_Q\) | \(b_Q\) | least \(m\) with \(R_Q(m)<1\) |
|---|---:|---:|---:|
| \(1+\) | \(16/21\) | \(5/7\) | \(484\) |
| \(1-\) | \(5/7\) | \(16/21\) | \(433\) |
| \(2++\) | \(20/21\) | \(3/7\) | \(968\) |
| \(2+-\) | \(19/21\) | \(4/7\) | \(790\) |
| \(2--\) | \(33/35\) | \(4/7\) | \(1015\) |

Hence the uniform threshold is

\[
\boxed{
q_* = 1015.
}
\]

---

## 4. Derivation of the one-literal rows

### Positive literal

For \(Q=x_1\):

- Q=1: the base 3-clause is satisfied and the other two chain variables
  become uncovered variables in the Liu cover. Relative factor:

\[
\frac{(4/3)^2}{7/3}
=
\boxed{\frac{16}{21}}.
\]

- Q=0: the base clause becomes a positive 2-clause with characteristic
  \(3/5\). Relative factor:

\[
\frac{(3/5)^{-1}}{(3/7)^{-1}}
=
\boxed{\frac57}.
\]

Therefore

\[
R_{1+}(m)
=
\frac{16}{21}
+
\frac57
\left(\frac{440}{441}\right)^m,
\]

which is strictly below 1 for the first time at

\[
\boxed{m=484}.
\]

### Negative literal

For \(Q=\neg x_1\), the two branches exchange the preceding local roles:

\[
R_{1-}(m)
=
\frac57
+
\frac{16}{21}
\left(\frac{440}{441}\right)^m.
\]

The first strict threshold is

\[
\boxed{m=433}.
\]

---

# 5. Derivation of the two-literal rows

For a two-literal center Q, the Q=1 child keeps a local relation on the same
three chain variables.

Exact characteristic solves give:

\[
\lambda_{2++}=\frac9{20},
\qquad
\lambda_{2+-}=\frac9{19},
\qquad
\lambda_{2--}=\frac5{11}.
\]

Relative to the parent \(\lambda_1=3/7\), this yields:

\[
a_{2++}
=
\frac{(3/7)}{(9/20)}
=
\boxed{\frac{20}{21}},
\]

\[
a_{2+-}
=
\frac{(3/7)}{(9/19)}
=
\boxed{\frac{19}{21}},
\]

\[
a_{2--}
=
\frac{(3/7)}{(5/11)}
=
\boxed{\frac{33}{35}}.
\]

For the Q=0 branch:

- ++: two zeros force the third chain variable to 1, so the local cost is
  one state and

\[
b_{2++}
=
\frac1{7/3}
=
\boxed{\frac37}.
\]

- mixed +-: the positive base clause is already satisfied and one chain
  coordinate remains free, giving

\[
b_{2+-}
=
\frac{4/3}{7/3}
=
\boxed{\frac47}.
\]

- --: again the positive base clause is satisfied and one chain coordinate
  remains free:

\[
b_{2--}
=
\boxed{\frac47}.
\]

Thus:

\[
R_{2++}(m)
=
\frac{20}{21}
+
\frac37g^m,
\]

\[
R_{2+-}(m)
=
\frac{19}{21}
+
\frac47g^m,
\]

\[
R_{2--}(m)
=
\frac{33}{35}
+
\frac47g^m.
\]

The first strict thresholds are respectively

\[
\boxed{968,\ 790,\ 1015}.
\]

---

# 6. Combining with LINK-DICHOTOMY1

Recall LINK-DICHOTOMY1.

For desired petal matching size q, define

\[
B_4(q)=1,
\]

\[
B_s(q)
=
1+18(4-s)(q-1)B_{s+1}(q)
\qquad
(s=3,2,1).
\]

If a chain has incidence

\[
d>18B_1(q),
\]

then q incident resolved clauses share one local pattern on the chain and have
pairwise chain-disjoint outside petals.

Set

\[
q=q_*=1015.
\]

Then:

\[
B_4=1,
\]

\[
B_3=18253,
\]

\[
B_2=666307513,
\]

\[
B_1=36484334181829.
\]

Therefore define

\[
\boxed{
D_* =
18B_1
=
656718015272922.
}
\]

Any chain with incidence strictly larger than \(D_*\) admits a
LOCALPATTERN-BRANCH1 branch whose conservative local DLS ratio is strictly
below 1.

The constant is enormous and is not proposed as practical. Its significance
is only that it is independent of n.

---

# 7. Bounded-incidence side

ACTIVE-DENSITY1 gives, after deleting truly inactive chains,

\[
M\ge\frac{\nu_{\rm act}}4.
\]

HYPERMATCH-DENSITY1 gives a maximal hypermatching covering at least

\[
\frac{M}{2\Delta}
\]

active chains.

Hence if

\[
\Delta\le D_*,
\]

then

\[
\boxed{
f_{\rm covered,act}
\ge
\frac1{8D_*}
=
\frac1{5253744122183376}.
}
\]

This is microscopically small but is a fixed positive constant.

Because every selected rank-2/3/4 resolved relation has characteristic
strictly better than independent type-1 chains, any such fixed coverage gives
a strict DLS improvement on the active resolved-chain subsystem.

---

# 8. Theorem RESOLVED-INCIDENCE-DICHOTOMY1

**Status: PROVED/EXACT for the declared resolved rank-<=4 type-1-chain
interaction model, subject to the existing LINK-DICHOTOMY1 and CLAUSECHAR1
hypotheses.**

After removing inactive chains, one of the following holds:

### Bounded-incidence branch

\[
\Delta\le D_*.
\]

Then a maximal resolved-relation hypermatching covers a fixed positive fraction

\[
\ge\frac1{8D_*}
\]

of active chains and receives strict characteristic credit.

### High-incidence branch

\[
\Delta>D_*.
\]

Then LINK-DICHOTOMY1 supplies 1015 pairwise-disjoint petals sharing one local
center pattern, and LOCALPATTERN-BRANCH1 supplies an exact branch with strict
local DLS-potential ratio below 1.

Thus the previous qualitative escape

\[
\text{resolved relations concentrate on one chain}
\]

is no longer an unstructured case in this model.

---

# 9. What this closes and what it does not

## Closed here

- the finite one-/two-literal center-pattern audit;
- the existence of a uniform finite petal threshold;
- the local high-chain-incidence DLS branch;
- the bounded-incidence versus high-incidence structural dichotomy for the
  resolved rank-<=4 type-1-chain model.

## Still open

1. Full integration into the entire deterministic 3-SAT algorithm and a clean
   global running-time constant.

2. Extension from the exact resolved-clause schema to every residual clause
   form that can occur in the broader preprocessing pipeline.

3. Any unrestricted SAT lower bound.

4. Any implication for arbitrary polynomial SAT algorithms.

5. P versus NP.

The present result is an exact-algorithm structural theorem, not the missing
CSE/source-acquisition theorem.

---

# 10. Google Drive audit relevant to the broader proof

The Drive review conducted alongside this calculation found three important
existing results that should remain separate from HIGHINC-CLOSE1.

## A. Manuscript 21A / CLAUDE-0314

Drive independently verifies component localization, expansion-based majority
component lineage, and linear q-Horn component-backdoor depth for the stated
proper exact-2P2N expander family.

These are genuine structural localization results, but the same Drive report
explicitly retains the affine/Tseitin bypass and the missing arbitrary-decider
SAME_REALIZATION bridge.

Therefore they are useful hard-family controls, not CSE.

## B. MAIN LSPV-5-58501 / CLAUDE-0312

The Seed-Fixed Surjectivity Lemma and Orbit-Spectral Recurrence Lemma are
independently verified.

However MAIN 58501 itself identifies the dominant transfer gap:

\[
\text{small q-ary orbit recurrence}
\not\Rightarrow
\text{small Boolean separator}
\]

through the actual odd-prime binaryization.

Thus this route currently does not close the Boolean CSE/evaluator barrier.

## C. Absolute Source-Complexity Separator (ASCS)

The Drive source manual contains an exact ordinary-source separator

\[
D_{\rm ASCS}(y)
=
1
\iff
y\notin
\mathrm{Low}_U(c;m,B,\tau).
\]

Its density and miss lemmas are exact, and the report gives a genuine oracle
replacement under which the ordinary-source containment premise fails.

This is stronger than merely saying source dependence is nonblackbox:
it identifies a concrete nonrelativizing proof line.

But the remaining Fast Source Certificate condition is still open. The
ordinary bounded verifier must fit inside the required size-m
co-nondeterministic distinguisher, and direct replay charges the full source
production time.

So ASCS currently supplies a plausible location for nonrelativization, not the
required cost theorem.

---

# 11. Reproducibility

Script:

experiments/source_reduction/high_incidence_pattern_table.py

Raw exact table:

results/source_reduction/2026-10-05_high_incidence_pattern_table.json

---

## Bottom line

The Drive audit did not reveal a hidden P-vs-NP closure.

It did reveal that two tasks should be separated sharply:

\[
\boxed{
\text{exact clean-core concentration}
}
\]

is now substantially closer to closure, while

\[
\boxed{
\text{arbitrary-algorithm source acquisition / FSC / CSE}
}
\]

remains the real complexity-theoretic bottleneck.

Within the resolved rank-<=4 type-1-chain model, the high-incidence obstruction
is now finite and explicitly bounded by

\[
\boxed{
q_*=1015,
\qquad
D_*=656718015272922.
}
\]
