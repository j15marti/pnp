# LEAD-0024 — Concrete wrapper-as-SAT prime-lineage example

Timestamp: 2026-10-06 14:56 PT
Agent: LEAD
Global status: **P versus NP remains OPEN.**

## 1. Purpose

Build the smallest explicit CNF example combining:

- an ordinary SAT instance;
- SAT-answer-directed wrapper branching;
- multisign lineage \(T,F,\neg T,\neg F\);
- distinct prime labels;
- a rolling hash;
- nominal DAG reconvergence;
- a lineage-dependent detour/recursive return;
- a later SAT restriction selected by the retained lineage;
- and existential projection back to the original SAT semantics.

The purpose is to test whether making the wrapper itself a SAT formula converts an external provenance distinction into a genuine formula-internal nonmergeability condition.

## 2. Base formula

Use

\[
F(x_1,x_2,x_3)=x_1\wedge x_2,
\]

with \(x_3\) free.

Thus \(F\) has exactly the assignments with \(x_1=x_2=1\).

## 3. Stage 1

A seed \(s\in\{0,1\}\) selects the actual restriction test

\[
x_1=s.
\]

For this \(F\),

\[
\beta_1
=
\operatorname{SAT}(F\upharpoonright x_1=s)
=
s.
\]

The self-reduction preserves the satisfiable branch, so the semantic selected value is always

\[
a_1=1.
\]

But the lineage differs.

If \(s=1\), the tested branch was accepted directly:

\[
L_1=T,
\qquad
p_1=2.
\]

If \(s=0\), the tested false branch was rejected and the wrapper flips to true:

\[
L_1=\neg F,
\qquad
p_1=7.
\]

Both histories therefore have identical Boolean SAT state

\[
x_1=1
\]

but distinct intensional states.

## 4. Reconvergence and recursive return

Both paths reach the same nominal merge node \(M_1\).

The \(T\) path proceeds directly to the next query node.

The \(\neg F\) path sets a detour bit, visits an extra control node, then returns to the same query node.

Thus the control graph has nominal reconvergence but different realized histories.

## 5. Stage 2 is selected by lineage

The retained lineage controls the next actual SAT restriction:

\[
T\Rightarrow x_2=1,
\]

\[
\neg F\Rightarrow x_2=0.
\]

Since the current semantic state already has \(x_1=1\),

\[
\operatorname{SAT}(F\upharpoonright x_1=1,x_2=1)=1,
\]

while

\[
\operatorname{SAT}(F\upharpoonright x_1=1,x_2=0)=0.
\]

So the two nominally reconverged histories genuinely generate different later SAT answers.

Again self-reduction chooses \(x_2=1\) in both cases, yielding:

- direct route: \(L_2=T,p_2=11\);
- flipped route: \(L_2=\neg F,p_2=19\).

Hence both paths end with

\[
x_1=x_2=1
\]

and the same wrapper output

\[
\operatorname{out}=1,
\]

but retain different exact prime-lineage values.

## 6. Prime product and hash

The exact prime product is functionally constrained.

For seed 0:

\[
P=7\cdot19=133.
\]

For seed 1:

\[
P=2\cdot11=22.
\]

The toy rolling hash is

\[
h_1=p_1\bmod16,
\qquad
h_2=(3h_1+p_2)\bmod16.
\]

Therefore:

\[
s=0:
(P,h_1,h_2)=(133,7,8),
\]

\[
s=1:
(P,h_1,h_2)=(22,2,1).
\]

The primes and hashes are auxiliary coordinates. No computational factoring hardness is assumed.

## 7. Single-route existential wrapper CNF

The CNF with free seed contains:

- 46 variables;
- 309 clauses.

It is satisfiable.

More importantly, forcing either post-merge lineage remains satisfiable:

\[
G_{\exists}\wedge(L_1=T)
\]

is SAT, and

\[
G_{\exists}\wedge(L_1=\neg F)
\]

is also SAT.

This is an exact finite demonstration of EXISTENTIAL-PATH-ESCAPE1:

\[
\boxed{
\text{plain existential SAT can choose either route and need not support both}.
}
\]

## 8. Projection test

Existentially project all wrapper variables and retain only

\[
(x_1,x_2,x_3).
\]

Exact enumeration over all eight assignments gives an extension iff

\[
x_1=x_2=1.
\]

Therefore

\[
\boxed{
\exists z\;G_{\exists}(x,z)
\equiv
x_1\wedge x_2
=
F(x).
}
\]

The wrapper is an exact existential extension of the base formula in this toy example.

For fixed seed and fixed satisfying \(x\), the auxiliary extension is unique in the tested construction.

## 9. Paired all-route formula

To test true formula-internal merge forcing, instantiate both fixed routes simultaneously:

\[
G_{\rm pair}(x,z_0,z_1)
=
G(x,s=0,z_0)
\wedge
G(x,s=1,z_1).
\]

This formula has:

- 89 variables;
- 620 clauses.

It remains satisfiable, and projection again gives exactly

\[
x_1\wedge x_2.
\]

Thus requiring both fixed wrapper executions does not change the base SAT semantics in this example.

## 10. FALSE-MERGE1 — exact toy theorem

Now impose an incorrect merge by identifying the complete stage-1 multisign lineage of the two routes:

\[
L_1^{(0)}=L_1^{(1)}.
\]

But the two functional traces require

\[
L_1^{(0)}=\neg F
\]

and

\[
L_1^{(1)}=T.
\]

Therefore the paired formula with the false merge is UNSAT.

The resulting CNF has 89 variables and 628 clauses.

Exact enumeration shows that after projecting the wrapper variables, no original assignment has an extension.

Hence:

\[
\boxed{
G_{\rm pair}
\text{ is equisatisfiable with }F,
\quad
G_{\rm pair}+\text{false merge is UNSAT}.
}
\]

This is a genuine formula-internal nonmergeability statement for the paired toy construction.

## 11. What has been established

### PROVED/EXACT for the toy construction

1. Same semantic SAT state can coexist with distinct multisign/prime/hash histories.
2. Those histories can nominally reconverge.
3. Lineage can direct a later actual SAT restriction whose answer differs by history.
4. Both histories still end at the same SAT endpoint.
5. The single existential wrapper projects exactly to \(F\).
6. Either route alone can satisfy the existential wrapper.
7. A paired both-route wrapper also projects exactly to \(F\).
8. Falsely merging the paired lineage states creates an actual CNF contradiction.
9. For fixed satisfying \(x\) and fixed seed, the tested auxiliary extension is unique.

### NOT established

1. The paired both-route construction is not shown to be forced by ordinary SAT semantics for an arbitrary input.
2. Formula-internal nonmergeability does not imply that an arbitrary SAT decider explicitly stores the lineage variables.
3. Prime magnitude, unique factorization, hash diversity, or recursive path length does not yield a time lower bound.
4. No unrestricted SAT lower bound or P-vs-NP separation follows.

## 12. Interpretation

The test isolates a useful distinction.

For the ordinary existential wrapper,

\[
\exists s,z\;G(F,s,z),
\]

history distinctions are optional because SAT may choose one seed.

For the paired formula,

\[
G(F,0,z_0)\wedge G(F,1,z_1),
\]

both histories are simultaneously part of the formula semantics, and an illegal merge can be detected as unsatisfiability.

Thus making the wrapper itself SAT **can** convert a provenance distinction into a formula-internal correctness constraint, provided the formula actually contains the relevant executions.

The remaining load-bearing question is whether ordinary SAT correctness can force an analogous multi-history capability without manually duplicating every route.

That is the sharper form of SAT-MERGE-FORCING1.

## 13. Next target

Try to replace explicit paired-route duplication by a polynomial-size shared construction whose SAT semantics forces consistency across a large family of recursive histories.

The immediate hostile question is whether this necessarily introduces an \(\exists\forall\) obligation or whether a functional extension / self-composition gadget can keep the construction inside ordinary existential SAT while preserving the simultaneous nonmergeability condition.

P versus NP remains OPEN.
