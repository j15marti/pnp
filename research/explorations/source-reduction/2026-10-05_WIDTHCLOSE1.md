# WIDTHCLOSE1 — Bounded-Width Closure and the Guarded-Correlation No-Go

**Date:** 2026-10-05  
**Repository:** \`j15marti/pnp\`  
**Global status:** **OPEN. P versus NP remains open.**

This note follows RESOLUTION-CLEAN-GADGET1.

The one-step resolution-clean gadget hides a binary chain relation behind width-4 resolvents. The next question is whether hiding a useful correlation behind several layers of local inference can itself produce a hard SRAS acquisition resource.

For constant resolution width, the answer is no.

---

# 1. Exact width-4 derivation for RC-GADGET1

Recall

\[
Q=x_1\vee z_1,
\]

and the four gadget clauses

\[
C_1=Q\vee\neg z_3\vee\neg w_1,
\]

\[
C_2=Q\vee w_2\vee\neg w_3,
\]

\[
C_3=Q\vee w_1\vee\neg w_2,
\]

\[
C_4=Q\vee\neg z_2\vee\neg w_1.
\]

The auxiliary type-1 chain clauses are

\[
B_Z=z_1\vee z_2\vee z_3,
\]

\[
B_W=w_1\vee w_2\vee w_3.
\]

Because \(z_1\) already occurs in \(Q\), ordinary resolution gives:

1. resolve \(B_Z\) with \(C_1\) on \(z_3\):
   \[
   Q\vee z_2\vee\neg w_1;
   \]

2. resolve this with \(C_4\) on \(z_2\):
   \[
   Q\vee\neg w_1;
   \]

3. resolve with \(C_3\) on \(w_1\):
   \[
   Q\vee\neg w_2;
   \]

4. resolve with \(C_2\) on \(w_2\):
   \[
   Q\vee\neg w_3.
   \]

Now combine these three guarded negative units with \(B_W\):

5. resolve \(B_W\) with \(Q\vee\neg w_1\):
   \[
   Q\vee w_2\vee w_3;
   \]

6. resolve with \(Q\vee\neg w_2\):
   \[
   Q\vee w_3;
   \]

7. resolve with \(Q\vee\neg w_3\):
   \[
   \boxed{Q}.
   \]

The maximum clause width in this derivation is 4.

Thus RC-GADGET1 defeats one-step mediator cleaning but **not** exhaustive width-4 resolution closure.

---

# 2. Theorem WIDTHCLOSE1

**Status: PROVED/EXACT.**

For a CNF on \(n\) Boolean variables, the number of distinct non-tautological clauses of width at most \(w\) is at most

\[
\boxed{
N_w(n)
=
\sum_{i=0}^{w}
2^i\binom{n}{i}.
}
\]

Therefore exhaustive resolution closure restricted to width at most \(w\) can be computed in time polynomial in \(N_w(n)\) by saturation.

In particular, for fixed constant \(w\),

\[
\boxed{
N_w(n)=n^{O(w)}=\operatorname{poly}(n).
}
\]

Hence every consequence with a constant-width resolution derivation can be discovered in polynomial time by a sufficiently brute-force bounded-width preprocessing pass.

---

## Proof

A non-tautological clause of width \(i\) is specified by:

1. choosing \(i\) distinct variables:
   \[
   \binom ni;
   \]
2. choosing one of two signs for each selected variable:
   \[
   2^i.
   \]

Summing over \(0\le i\le w\) gives \(N_w(n)\).

A saturation algorithm stores all currently known width-\(\le w\) clauses and repeatedly adds every non-tautological resolvent of width at most \(w\) until no new clause appears.

There are at most \(N_w(n)\) insertions. A naive implementation may examine polynomially many pairs in \(N_w(n)\), so its running time is polynomial in \(N_w(n)\).

For constant \(w\), this is polynomial in \(n\). \(\square\)

---

# 3. Corollary WIDTH-GUARD1

**Status: PROVED/EXACT.**

A proposed SRAS acquisition lower bound cannot rest solely on the claim

> a useful chain correlation is hidden behind a constant-width resolution derivation.

Such a relation is polynomially discoverable by exhaustive bounded-width closure.

Therefore constant-width inference depth—even very large depth—does not by itself supply a superpolynomial acquisition barrier.

The relevant parameter is not merely derivation depth but some resource that cannot be saturated with only polynomially many states, such as growing width, growing representation complexity, or a different model-matched obstruction.

---

# 4. Width growth calibration

The crude closure bound is

\[
N_w(n)
\le
\sum_{i=0}^{w}(2n)^i
\le
(w+1)(2n)^w.
\]

Therefore:

- \(w=O(1)\): polynomial closure;
- \(w=O(\log n)\): at most quasipolynomial-size brute-force closure;
- \(w=\omega(1)\): the naive enumeration becomes superpolynomial;
- \(w=\Omega(n)\): the state space can become exponential.

This is only an upper bound on a brute-force inference method. It is **not** a lower bound on SAT computation.

A global algorithm can still bypass large resolution width, as XOR/Tseitin plus Gaussian elimination repeatedly demonstrates.

---

# 5. Guarded contradiction construction

There is a general way to hide a relation \(Q\) behind an auxiliary contradiction.

Let

\[
H(W)=\bigwedge_{i=1}^{m} C_i(W)
\]

be an unsatisfiable CNF on auxiliary variables \(W\), and let \(Q(X)\) be any clause on disjoint variables.

Define

\[
G_Q(H)
=
\bigwedge_{i=1}^{m}
\left(Q\vee C_i\right).
\]

Then:

## Lemma GUARDED-UNSAT1

**Status: PROVED/EXACT.**

If \(H\) is unsatisfiable, then

\[
\boxed{
G_Q(H)\equiv Q.
}
\]

### Proof

If \(Q=1\), every guarded clause is true.

If \(Q=0\), the guarded formula reduces exactly to \(H\), which is unsatisfiable. \(\square\)

RC-GADGET1 is a small finite-domain variant of this principle: the auxiliary type-1 chain domain supplies the contradiction when \(Q=0\).

---

# 6. Acquisition interpretation

GUARDED-UNSAT1 explains why “hide the correlation more deeply” risks circularity.

To expose \(Q\), one may need to establish that the auxiliary system \(H\) is inconsistent.

If \(H\) belongs to an easy family, the hidden correlation is cheap:

- 2-SAT \(H\): SCC/implication analysis;
- affine \(H\): Gaussian elimination;
- bounded-treewidth \(H\): dynamic programming;
- constant-width resolution \(H\): WIDTHCLOSE1.

If we choose \(H\) to be an arbitrary hard SAT/UNSAT family, then the cost of discovering \(Q\) has simply inherited the original SAT difficulty.

Thus:

\[
\boxed{
\text{hard hidden-correlation acquisition}
\not\text{ obtained for free from deeper guarding}.
}
\]

One must prove an independent theorem that every relevant SAT computation needs the guarded correlation while no compact global evaluator bypasses the auxiliary contradiction.

That is essentially the original SRAS extraction/barrier obligation.

---

# 7. Connection to proof complexity

Resolution width is still useful in a **restricted proof model**.

Ben-Sasson–Wigderson size-width tradeoffs show that sufficiently large width requirements can imply exponential resolution proof size.

But this remains a resolution lower bound.

A P-vs-NP argument would still need an arbitrary-algorithm extraction theorem mapping every hypothetical polynomial SAT decider into the charged proof/inference object.

Therefore WIDTHCLOSE1 is best used as a filter:

- constant-width hidden relation: too cheap;
- high-width relation: potentially interesting in resolution;
- unrestricted runtime implication: still missing.

---

# 8. Revised clean-core preprocessing ladder

The structural program should credit increasingly strong polynomial inference before declaring a residual object hard.

### Level 0 — direct clauses
Direct pair/triple correlation hypergraph.

### Level 1 — local mediator elimination
Resolve degree-2 mediators and promote low-width resolvents.

### Level 2 — constant-width closure
Saturate all resolution consequences up to a fixed width \(w\).

By WIDTHCLOSE1, this remains polynomial for constant \(w\).

### Level 3 — compact global evaluators
Run specialized polynomial inference where applicable:

- SCC / 2-SAT;
- Gaussian elimination / affine structure;
- bounded-treewidth DP;
- polymorphism/CSP algorithms;
- other recognized compact summaries.

### Level 4 — residual acquisition problem
Only after all such cheap channels are credited is there a candidate SRAS acquisition debt.

This prevents syntactic hiding from being mistaken for complexity.

---

# 9. New theorem target

The clean-core/P-vs-NP route would need something much stronger than hidden constant-width correlations:

\[
\boxed{
\text{every polynomial-size ordinary SAT computation must acquire a relation}
}
\]

whose discovery/use cannot be achieved by:

- constant-width saturation;
- known global algebraic algorithms;
- compact separator/DP summaries;
- replay/reread;
- DAG sharing;
- arbitrary polynomial transcript processing.

Equivalently, we need an acquisition resource outside all currently P-closed inference channels.

This restates the source-to-reduction problem in a sharper structural form.

---

# 10. Strict status

## PROVED/EXACT
- explicit width-4 derivation of \(Q\) from RC-GADGET1;
- WIDTHCLOSE1;
- WIDTH-GUARD1;
- GUARDED-UNSAT1.

## KNOWN EXTERNAL CONTEXT
- resolution size-width lower bounds can turn large width into large resolution proofs.

## FALSIFIED/RETIRED AS GENERIC HINGES
- constant-width hidden correlation;
- long constant-width inference depth;
- guarded easy contradictions.

## OPEN
- growing-width/source-matched acquisition theorem for arbitrary SAT algorithms;
- representation-independent hidden-correlation lower bound;
- nonrelativizing/nonalgebrizing bridge;
- \(P\ne NP\).

---

## Bottom line

The one-step resolution-clean gadget is structurally real but computationally cheap once width-4 closure is credited.

This gives a useful rule for SRAS:

\[
\boxed{
\textbf{Do not charge hidden information that lies in a polynomially saturable inference class.}
}
\]

A viable acquisition barrier must survive not just provenance and replay attacks, but also exhaustive constant-width inference and compact global evaluators.
