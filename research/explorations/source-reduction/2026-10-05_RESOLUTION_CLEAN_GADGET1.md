# RESOLUTION-CLEAN-GADGET1 — Binary Clauses Survive One-Step Width-4 Mediator Cleaning

**Date:** 2026-10-05  
**Repository:** \`j15marti/pnp\`  
**Global status:** **OPEN. P versus NP remains open.**

This note follows RESIDUAL-HARD1 and CONSISTENCY-PAIR1.

A natural strengthening of the low-degree clean-core preprocessing is:

> eliminate every degree-2 mediator \(y\) with one positive and one negative occurrence; if the resolvent has width at most 3 on chain variables, promote it immediately to the direct pair/triple correlation ledger.

This would remove the simple EM2 gadgets

\[
(Q\vee y)\wedge(Q\vee\neg y),
\]

because they resolve directly to the binary clause \(Q\).

The present note tests whether NP-hard expressive power survives after this **one-step low-width resolution cleaning**.

It does.

---

# 1. One-step resolution-clean template

Call a degree-2 mediator one-step resolution-clean when it appears in

\[
A\vee y,
\qquad
B\vee\neg y,
\]

where:

- \(A\) is a 2-clause on literals from two distinct clean chains;
- \(B\) is a 2-clause on literals from two distinct clean chains;
- the resolvent
  \[
  A\vee B
  \]
  has exactly four distinct non-tautological chain literals.

Thus eliminating that mediator exposes a width-4 chain constraint, but no binary or ternary direct correlation in the first resolution step.

---

# 2. The binary target

Let \(X,Z\in D\), where

\[
D=\{0,1\}^3\setminus\{000\}.
\]

We want to implement the binary relation

\[
Q(X,Z)=x_1\vee z_1.
\]

Introduce one auxiliary type-1 chain

\[
W=(w_1,w_2,w_3)\in D.
\]

Consider the four width-4 clauses

\[
C_1=
x_1\vee z_1\vee\neg z_3\vee\neg w_1,
\]

\[
C_2=
x_1\vee z_1\vee w_2\vee\neg w_3,
\]

\[
C_3=
x_1\vee z_1\vee w_1\vee\neg w_2,
\]

\[
C_4=
x_1\vee z_1\vee\neg z_2\vee\neg w_1.
\]

---

# 3. Theorem RC-GADGET1

**Status: PROVED/EXACT.**

Over the seven-state chain domain,

\[
\boxed{
x_1\vee z_1
\iff
\exists W\in D:
C_1\wedge C_2\wedge C_3\wedge C_4.
}
\]

---

## Proof

If

\[
x_1\vee z_1=1,
\]

then every \(C_i\) is already satisfied, so any \(W\in D\) works.

Now suppose

\[
x_1=z_1=0.
\]

Since \(Z\in D\), at least one of \(z_2,z_3\) equals 1.

- If \(z_3=1\), clause \(C_1\) forces \(w_1=0\).
- If \(z_2=1\), clause \(C_4\) forces \(w_1=0\).

Thus in all cases

\[
w_1=0.
\]

Then \(C_3\) becomes

\[
\neg w_2,
\]

so

\[
w_2=0.
\]

Then \(C_2\) becomes

\[
\neg w_3,
\]

so

\[
w_3=0.
\]

Therefore

\[
W=000,
\]

contradicting \(W\in D\).

Hence no auxiliary state exists when \(Q=0\). \(\square\)

---

# 4. Every width-4 clause comes from one legal degree-2 mediator

Each \(C_i\) can be split into two legal pair terms, each pair using two distinct chains.

For \(C_1\):

\[
(x_1\vee z_1)
\vee
(\neg z_3\vee\neg w_1).
\]

For \(C_2\):

\[
(x_1\vee w_2)
\vee
(z_1\vee\neg w_3).
\]

For \(C_3\):

\[
(x_1\vee w_1)
\vee
(z_1\vee\neg w_2).
\]

For \(C_4\):

\[
(x_1\vee z_1)
\vee
(\neg z_2\vee\neg w_1).
\]

Therefore introduce four fresh mediators \(y_1,\ldots,y_4\), and replace each \(C_i=A_i\vee B_i\) by

\[
A_i\vee y_i,
\qquad
B_i\vee\neg y_i.
\]

Every original clause is a 3-clause consisting of:

- one outside mediator;
- two chain literals from distinct chains.

Every mediator:

- has degree exactly 2;
- appears once positively and once negatively;
- has \(d_0=d_1=1\) under the current branch accounting.

Eliminating any one mediator produces exactly one width-4 resolvent.

No first mediator-elimination step exposes a width-2 or width-3 chain-only clause.

---

# 5. Consequence: one-step resolution-clean hardness

Every one of the 36 cross-chain binary clauses used in DUAL3SAT1 can be obtained from the displayed gadget by coordinate permutation and literal negation.

Equality and disequality between occurrence bits are conjunctions of two such binary clauses.

Therefore replace every consistency binary clause in RESIDUAL-HARD1 by one copy of RC-GADGET1.

This yields a linear-size reduction from 3-SAT to a family with:

- disjoint positive type-1 chain clauses;
- degree-2 outside mediators only;
- no original chain-only direct pair/triple residual clause;
- every single mediator resolvent of width exactly 4;
- no direct binary/ternary relation exposed by **one round** of mediator elimination.

Hence:

\[
\boxed{
\text{one-step resolution-clean externally mediated SAT remains NP-hard}.
}
\]

The reduction remains polynomial and uses only constant-size gadgets per source consistency clause.

---

# 6. Computational gadget search

Before the analytic proof above was extracted, the gadget was found by exact finite synthesis.

The search space consisted of all 1,296 arity-3 width-4 relations obtainable as a legal degree-2 mediator resolvent over three 7-state chains.

A mixed-integer formulation searched for a smallest conjunction whose existential projection onto two distinguished chains equals

\[
x_1\vee z_1.
\]

The optimum in this one-auxiliary-chain template was 4 width-4 relations.

Reproducible verifier:

\`experiments/source_reduction/resolution_clean_binary_gadget.py\`

Raw result:

\`results/source_reduction/2026-10-05_resolution_clean_binary_gadget.json\`

The verifier exhaustively checks all

\[
7^2=49
\]

distinguished chain-state pairs.

All 49 projection checks pass.

The analytic theorem above is the proof; the finite synthesis is only a discovery/verification record.

---

# 7. Important limitation: bounded-width resolution can still uncover the gadget

RC-GADGET1 defeats only a **one-step** rule that promotes individual width-\(\le3\) mediator resolvents.

It does not establish hardness against exhaustive bounded-width reasoning.

Indeed, the gadget was deliberately constructed from only four width-4 clauses plus the positive chain clauses for \(Z\) and \(W\). A short sequence of ordinary resolution steps can propagate the contradiction in the \(Q=0\) branch and eventually expose the implied binary clause \(Q\).

Therefore the correct conclusion is:

\[
\boxed{
\text{one-step low-width mediator elimination is insufficient}
}
\]

not

\[
\text{bounded-width resolution cannot expose the hidden pair relation}.
\]

---

# 8. Refined preprocessing ladder

The low-degree clean-core analysis can now be organized as a hierarchy.

### Level 0 — original direct correlation
Look only for chain-only residual clauses already present.

RESIDUAL-HARD1 survives this level.

### Level 1 — single-mediator resolution
Eliminate degree-2 mediators and promote width-\(\le3\) resolvents.

RC-GADGET1 survives this level while still encoding binary consistency.

### Level 2 — bounded-width closure
Compute a controlled resolution closure up to width 4 or another fixed bound and promote newly exposed strong pair/triple relations.

RC-GADGET1 probably does **not** survive this level.

### Level 3 — global structural inference
Use SCC/2-SAT, Gaussian, CSP polymorphisms, separator DP, or other compact global reasoning rather than local resolution.

A genuine residual obstruction must survive all polynomially cheap reasoning admitted at this level.

This ladder is a useful SRAS accounting object: every promoted relation is credited rather than hidden behind syntax.

---

# 9. Relation to P versus NP

The new NP-hardness statement still does not yield a lower bound.

Under \(P=NP\), a polynomial algorithm can solve the gadgetized family.

What the gadget establishes is structural:

\[
\boxed{
\text{absence of immediately visible or one-step-resolvable pair/triple constraints}
}
\]

does not imply loss of NP-complete expressive power.

Thus a future extraction/barrier argument cannot identify “hidden correlation depth 1” with hardness. It must charge the cost of discovering and using correlations across representations.

---

# 10. Next target

The useful next question is now:

\[
\boxed{
\text{How much polynomially bounded inference must be credited before the residual language changes complexity?}
}
\]

Concretely:

1. compute width-4 resolution closure on the gadget family;
2. determine the shortest derivation exposing the hidden binary \(Q\);
3. generalize to gadgets whose hidden relation requires resolution depth/space growing with gadget size;
4. hostile-test whether global 2-SAT/SCC or other compact algorithms collapse those gadgets anyway;
5. only then ask whether the surviving discovery cost can enter SRAS as a non-shareable acquisition resource.

This connects the clean-core structural branch directly to proof-complexity/reconstruction accounting.

---

# 11. Strict status

## PROVED/EXACT
- RC-GADGET1.
- legal degree-2 mediator realization of all four width-4 clauses.
- one-step resolution-clean NP-hardness by substitution into RESIDUAL-HARD1.

## COMPUTATIONAL
- four-clause optimality within the searched one-auxiliary-chain template.
- 49/49 exhaustive projection checks.

## NOT PROVED
- hardness after exhaustive width-4 resolution closure;
- superpolynomial correlation-discovery cost;
- any unrestricted SAT runtime lower bound;
- \(P\ne NP\).

---

## Bottom line

The first strengthened clean-core rule is not enough.

Even when **every individual low-degree mediator resolves only to a width-4 constraint**, four such constraints and one auxiliary type-1 chain can hide an arbitrary binary consistency clause.

So the structural frontier moves again:

\[
\boxed{
\text{direct clean core}
\;\to\;
\text{one-step resolution-clean core}
\;\to\;
\text{bounded-inference clean core}.
}
\]

The next useful experiment is to quantify the inference depth/space needed to expose these hidden correlations and determine whether that quantity can be made to grow without collapsing under a compact global evaluator.
