# ADVICE-HIERARCHY1: Length-Dependent Programs, Fixed-Resource Meta-Complexity, and the Gating Barrier

**Status:** Substantive intermediate progress. Two exact transfer lemmas and one new self-succinct target are established. The final P-vs-PSPACE / P-vs-NP separation remains open.

**Date:** 2026-10-18

## 1. Goal

The META-LIFT program asks whether unconditional lower bounds from the resource-contraction / time-space work can replace the random hard truth table used in MCSP/MOCSP hardness constructions.

The most useful formulation is not unrestricted circuit complexity. It is a **length-dependent program** model:

- one program/advice string \(d_n\) may be chosen separately for each input length \(n\);
- the same \(d_n\) must work for every \(n\)-bit input;
- running time and workspace are explicitly bounded.

This is exactly the setting of advice complexity and nonuniform time-space lower bounds.

The central question is:

\[
\text{Can we obtain a self-succinct minimization target whose NO side is protected by an unconditional advice-robust lower bound?}
\]

The answer is partially yes. The hardness resource can be obtained unconditionally. The remaining obstacle is a **gating / reduction problem**, not the absence of a lower bound.

---

## 2. Existing advice lower bounds are stronger than the naive diagonalization

Three known results are directly relevant.

### 2.1 Tourlakis: SAT time-space-advice lower bounds

Tourlakis proved nontrivial lower bounds for SAT on random-access deterministic machines with nonuniform advice.

A useful form is:

If SAT is solved in time \(n^a\), space \(n^b\), and advice

\[
o\!\left(n^{(a+b)/2-\varepsilon}\right)
\]

for some \(\varepsilon>0\), then necessarily

\[
a\ge \rho(b)
:=
\frac{\sqrt{b^2+8}-b}{2}.
\]

In particular:

- with \(n^{o(1)}\) space, exponents \(a<\sqrt2\) are excluded even with substantial sublinear advice;
- near-linear time and sublinear space remain impossible with comparably sublinear advice.

Thus the project's “program may depend on input length” escape is already covered by an unconditional SAT lower-bound theorem in a significant parameter region.

### 2.2 Fortnow-Santhanam: hierarchies against sublinear advice

Fortnow and Santhanam prove nondeterministic time hierarchies that survive polynomially sublinear advice. For suitable constants \(d'>d\ge1\),

\[
NTIME(n^d)
\not\subseteq
NTIME(t(n))/n^{1/d'}
\]

for \(t(n)=o(n^d)\).

This is stronger than ordinary uniform hierarchy diagonalization because the lower-side machine receives a length-dependent advice string.

### 2.3 Buhrman-Fortnow-Santhanam: exponential-time classes versus advice

For every fixed constant \(c\),

\[
NEXP\not\subseteq NP/n^c.
\]

So unconditional hierarchy methods can defeat even polynomial-length nonuniform advice, at the cost of moving the hard language to exponential time.

These theorems show that the ADVICE-HIERARCHY1 lower-bound ingredient is not speculative. It is established literature.

---

## 3. Fixed-resource truth-table complexity

For a bit string \(x\) of length \(2^n\), define

\[
K^{a,b}_{\rm adv}(x)
=
\min_d |d|,
\]

where the minimum is over descriptions \(d\) such that for every index
\(i\in\{0,1\}^n\),

\[
U(d,i)=x_i
\]

within time \(n^a\) and writable space \(n^b\).

The description \(d\) may depend on \(n\), but not on the individual index \(i\).

For a fixed \(\delta>0\), define

\[
LOW_{a,b,\delta}
=
\left\{
x\in\{0,1\}^{2^n}:
K^{a,b}_{\rm adv}(x)\le n^\delta
\right\}.
\]

This is a resource-bounded meta-complexity problem, but unlike MCSP it measures a **fixed uniform time-space model plus length-dependent advice**.

---

## 4. New lemma: the succinct version is low

### Lemma 4.1: SUCCINCT-LOW

For fixed constants \(a,b,\delta\),

\[
\boxed{
\operatorname{succ}(LOW_{a,b,\delta})\in\Sigma_2^P.
}
\]

### Encoding

A succinct input is a Boolean circuit \(D\) with \(n\) input bits. It represents the exponentially long string

\[
x_D[i]=D(i).
\]

Since a circuit with \(n\) inputs has descriptor length at least \(n\), the quantities

\[
n^a,\qquad n^b,\qquad n^\delta
\]

are polynomial in the succinct descriptor length.

### Verification

Guess a description

\[
|d|\le n^\delta.
\]

Universally quantify \(i\in\{0,1\}^n\).

Simulate \(U(d,i)\) for at most \(n^a\) steps, rejecting any computation exceeding \(n^b\) writable cells, and check

\[
U(d,i)=D(i).
\]

For fixed \(a,b,\delta\), the inner predicate is polynomial-time in the succinct descriptor size.

Therefore the whole predicate has the form

\[
\exists d\ \forall i\ R(D,d,i),
\]

with polynomial-time \(R\), proving membership in \(\Sigma_2^P\).

### Consequence

This target has exactly the “low succinct complexity” property needed by META-LIFT:

\[
P=PSPACE
\quad\Longrightarrow\quad
\operatorname{succ}(LOW_{a,b,\delta})\in P.
\]

Unlike the earlier weighted \( |p|+\log t+\lambda s \) proposal, no exponentially long candidate simulation is needed.

---

## 5. SAT truth tables are unconditionally hard in this measure in a nontrivial region

Let

\[
TT_n(SAT)
\]

denote the truth table of SAT restricted to \(n\)-bit encodings.

Suppose constants \(a,b,\delta\) satisfy

\[
a<\rho(b)
\]

and choose \(\varepsilon>0\) so that

\[
\delta<
\frac{a+b}{2}-\varepsilon.
\]

If

\[
K^{a,b}_{\rm adv}(TT_n(SAT))
\le n^\delta
\]

for all sufficiently large \(n\), then the minimizing descriptions \(d_n\) would constitute an advice family of length \(O(n^\delta)\) giving a deterministic SAT algorithm with time \(n^a\) and space \(n^b\).

Since

\[
n^\delta
=
o\!\left(n^{(a+b)/2-\varepsilon}\right),
\]

this contradicts Tourlakis.

Therefore:

\[
\boxed{
K^{a,b}_{\rm adv}(TT_n(SAT))>n^\delta
\quad\text{for infinitely many }n.
}
\]

This is an unconditional lower bound on a length-dependent description measure for the SAT truth-table family.

### Important limitation

Tourlakis' theorem, in this form, does not identify a polynomially dense or computable set of hard lengths. It rules out a globally small advice bound and therefore guarantees infinitely many hard lengths.

A uniform reduction cannot silently choose “the next hard length.”

That hard-length selection issue must be charged.

---

## 6. New slice-transfer lemma

The SAT truth-table lower bound can be made conditional on an arbitrary SAT instance without assuming that a solver emits a proof representation.

Let \(\varphi(z)\) be a CNF on \(m\) assignment bits, and define the Boolean function

\[
F_{\varphi,n}(y,z)
=
SAT_n(y)\wedge \varphi(z),
\]

where \(y\in\{0,1\}^n\).

### Lemma 6.1: SLICE-TRANSFER

If \(\varphi\) is unsatisfiable, then

\[
F_{\varphi,n}\equiv0,
\]

so its truth table has constant-description complexity.

If \(\varphi\) is satisfiable and \(z^\star\) is a satisfying assignment, then any description \(d\) computing \(F_{\varphi,n}\) in time \(T\) and space \(S\) yields a description for \(SAT_n\) by hardwiring \(z^\star\):

\[
d'(y)=d(y,z^\star).
\]

Hence

\[
|d'|
\le
|d|+m+O(\log m),
\]

while time and workspace change by at most lower-order encoding overhead.

Therefore every Tourlakis lower bound for \(SAT_n\) gives:

\[
\boxed{
K^{a,b}_{\rm adv}(TT(F_{\varphi,n}))
\ge
K^{a,b}_{\rm adv}(TT_n(SAT))
-
m-O(\log m)
}
\]

whenever \(\varphi\) is satisfiable.

So, at a hard length \(n\) satisfying

\[
n^\delta\gg m,
\]

the two cases separate:

\[
\varphi\in UNSAT
\Longrightarrow
K^{a,b}_{\rm adv}(TT(F_{\varphi,n}))=O(1),
\]

while

\[
\varphi\in SAT
\Longrightarrow
K^{a,b}_{\rm adv}(TT(F_{\varphi,n}))>n^\delta-m-O(\log m).
\]

This is a genuine unconditional **meta-complexity gap**.

It uses no hash assumption and no proof-system extraction.

---

## 7. Why this does not yet close META-LIFT

The gap is real, but the naive many-one reduction is not low-space/poly-output.

To output the explicit truth table of

\[
F_{\varphi,n}(y,z)
=
SAT_n(y)\wedge\varphi(z),
\]

the reduction must know \(SAT_n(y)\) for target positions.

That is precisely the hard function whose resource lower bound we are exploiting.

Thus the reduction cannot simply materialize the target in deterministic polylogarithmic workspace.

This is a **gating barrier**:

\[
\boxed{
\text{we now have the hard side and the easy side, but not a cheap way to wire the source bit into the hard side.}
}
\]

This is structurally analogous to the coherent-randomness problem in GapMOCSP.

---

## 8. Why the advice lower bound nevertheless improves the project

The earlier MOCSP direction needed a table of provably large unrestricted circuit complexity.

A deterministic low-space generator for such a table would collapse under the assumption \(P=PSPACE\), because the generated bit function would then be in P and would have polynomial-size circuits.

The fixed-resource measure avoids that exact collapse.

A table may simultaneously be:

- computable in polynomial time under \(P=PSPACE\), but
- impossible to compute in a *smaller fixed time exponent* with short advice.

Thus the hard object no longer needs superpolynomial unrestricted circuit complexity.

The relevant lower bound is a **quantitative resource gap**, not an absolute P/poly lower bound.

This is the main conceptual gain from ADVICE-HIERARCHY1.

---

## 9. Interaction with INDEXCUT43 and ADDRESSSEM44

The recent project lower bounds fit naturally here.

### INDEXCUT43

If a computation-dependent address remains unresolved and is represented by standalone SAT children, the children must collectively preserve nearly linear information:

\[
\Omega(N/\log N)
\]

on large subfamilies.

That result can be used to attack any proposal that tries to represent the missing hard-table/gating choice by branching over all possible addresses or descriptions.

### ADDRESSSEM44

If a SAT-dependent address can be extracted inside approximately

\[
T=N^{6/5+o(1)},
\qquad
S=N^{1/2+o(1)},
\]

the extraction enters the FLMV forbidden region.

Thus the gating layer now has a useful dichotomy:

1. leave the semantic selector unresolved, and INDEXCUT43 forces large represented information;
2. resolve it quickly in a low-space regime, and ADDRESSSEM44/FLMV can become applicable.

The remaining escape is to resolve the selector using **large time but small space**. That escape is still legal for basic META-LIFT.

---

## 10. Interaction with CLOCKCOMPRESS32

CLOCKCOMPRESS32 showed that unconditional hierarchy arguments can obstruct a universal compiler from turning all higher-time computations into uniformly fast short descriptions, but that redundant encodings can still be easy.

The present target charges exactly the quantities CLOCKCOMPRESS32 indicates are necessary:

\[
\text{description length}
+
\text{fixed execution time}
+
\text{fixed workspace}.
\]

The new \(LOW_{a,b,\delta}\) target therefore avoids the weakest “short encoding only” failure mode.

---

## 11. Stronger literature route: advice hierarchies instead of SAT

Tourlakis gives a fixed natural hard language, SAT, but only an infinitely-often hard-length conclusion for the induced advice minimum.

Fortnow-Santhanam and Buhrman-Fortnow-Santhanam provide stronger advice-robust hierarchy languages.

This suggests a second target family:

\[
LOW^{L}_{c,\delta}
\]

built from the truth tables of a language \(L\) chosen from an advice hierarchy.

Advantages:

- advice robustness is built into the hierarchy theorem;
- the time exponent can be chosen explicitly.

Disadvantage:

- the bit predicate for \(L\) may require substantially more computation than SAT at the target scale;
- a low-space/poly-output source reduction still needs a way to gate \(L\)'s hard table using the source instance.

So the same gating barrier reappears.

---

## 12. Precise next theorem

The most valuable target is now:

### GATED-HARDTABLE1

Construct a deterministic polynomial-output polylog-space transformation

\[
\varphi
\longmapsto
X_\varphi
\]

such that for fixed \(a,b,\delta\):

\[
\varphi\in UNSAT
\Longrightarrow
X_\varphi\in LOW_{a,b,\delta},
\]

and

\[
\varphi\in SAT
\Longrightarrow
X_\varphi\notin LOW_{a,b,\delta},
\]

while every output bit of \(X_\varphi\) is generated without solving SAT and without importing nonuniform hard-table advice.

If such a transformation exists, then \(LOW_{a,b,\delta}\) is SAT/coSAT-hard under precisely the kind of weak reduction required by META-LIFT, while its succinct version remains in \(\Sigma_2^P\).

That would yield a hierarchy contradiction under the appropriate collapse assumption.

This is now a more concrete target than unrestricted MOCSP derandomization.

---

## 13. Current conclusion

ADVICE-HIERARCHY1 succeeds at the lower-bound level:

\[
\boxed{
\text{unconditional length-dependent description lower bounds exist,}
}
\]

and we can package them into a fixed-resource meta-complexity problem whose succinct version is low:

\[
\boxed{
\operatorname{succ}(LOW_{a,b,\delta})\in\Sigma_2^P.
}
\]

The remaining missing link is no longer “prove a hard table exists.”

It is:

\[
\boxed{
\text{gate an NP/PSPACE source instance into that hard table with a deterministic polylog-space, polynomial-output reduction.}
}
\]

This sharply localizes the research problem.

---

## References

1. Iannis Tourlakis, *Time-Space Tradeoffs for SAT on Nonuniform Machines*, Journal of Computer and System Sciences 63(2), 2001.
2. Lance Fortnow and Rahul Santhanam, *Hierarchies Against Sublinear Advice*, ECCC TR14-171 / Theory of Computing Systems.
3. Harry Buhrman, Lance Fortnow, and Rahul Santhanam, *Unconditional Lower Bounds Against Advice*, ECCC TR09-064.
4. Eric Allender, Harry Buhrman, Michal Koucký, Dieter van Melkebeek, and Detlef Ronneburger, *Power from Random Strings*, SIAM Journal on Computing 35(6), 2006.
5. Eric Allender, Dhiraj Holden, and Valentine Kabanets, *The Minimum Oracle Circuit Size Problem*, STACS 2015 / Computational Complexity.
6. PORTFOLIO-SHIELD-SAT project results: INDEXCUT43, ADDRESSSEM44, CLOCKCOMPRESS32, META-LIFT1/2.
