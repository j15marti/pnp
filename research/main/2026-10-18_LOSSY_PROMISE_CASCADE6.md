# LOSSY-PROMISE-CASCADE6: Promise-Pure Quotients as the Missing Many-to-One Abstraction

**Status:** New synthesis theorem and research target. The quotient trichotomy and cascade accounting are exact. No construction satisfying the load-bearing quotient hypotheses is yet proved. P versus NP remains OPEN.

**Date:** 2026-10-18

## 1. Motivation

The current threshold-descent branch has progressively ruled out:

- injective or source-recoverable descent;
- short deterministic fixed-seed affine sketches;
- ordinary padding/inflation;
- generic one-tape fusion;
- treating a randomized hash image as if it were ordinary MCSP.

These failures all point to the same missing abstraction already present in earlier project work:

\[
\boxed{
\text{a genuinely lossy many-to-one semantic quotient, defined only up to a promise.}
}
\]

The correct object is not necessarily a smaller ordinary MCSP instance.

It is a short quotient \(J(x)\) together with a label problem defined on the image of \(J\).

---

## 2. Promise-pure quotient trichotomy

Let a source promise problem be

\[
\Pi=(Y,N),
\qquad
Y,N\subseteq\{0,1\}^*,
\qquad
Y\cap N=\varnothing.
\]

Let

\[
J:Y\cup N\to Z
\]

be any map.

There are three qualitatively different cases.

### Case A: lossless / reconstructible

The relevant fibers of \(J\) are singleton or carry enough side information to reconstruct the source.

Then no genuine semantic compression has occurred. Any resource gain must pay for the reconstruction record or source replay.

### Case B: lossy and mixed

\[
J(Y)\cap J(N)\ne\varnothing.
\]

Then no deterministic label on \(J(x)\) can solve the source promise on all promised inputs.

This is not a valid exact quotient.

### Case C: lossy and promise-pure

\[
\boxed{
J(Y)\cap J(N)=\varnothing.
}
\]

Then define the induced image promise

\[
\Pi_J
=
\bigl(
J(Y),
J(N)
\bigr)
\]

and its image label

\[
\operatorname{LABEL}_J(z)
=
\begin{cases}
1,&z\in J(Y),\\
0,&z\in J(N).
\end{cases}
\]

The map may merge exponentially many YES instances and exponentially many NO instances.

Only cross-label collisions are forbidden.

### Lemma 2.1: PURE-QUOTIENT-FACTOR1

There exists a well-defined Boolean label on \(J(Y\cup N)\) satisfying

\[
\Pi(x)=\operatorname{LABEL}_J(J(x))
\]

for every promised \(x\) if and only if

\[
J(Y)\cap J(N)=\varnothing.
\]

This is immediate, but it isolates exactly what the current descent construction needs.

---

## 3. Why promises matter

For a total problem, every source string is semantically constrained.

For a promise problem, collisions with the unpromised middle region are harmless.

Thus the correct target for Gap-MCSP-style work is not necessarily an exact quotient of all truth tables. It is a quotient pure only between:

\[
Y=\{f:CC(f)\le s_{\rm yes}\}
\]

and

\[
N=\{f:CC(f)\ge s_{\rm no}\},
\]

with no requirement on

\[
s_{\rm yes}<CC(f)<s_{\rm no}.
\]

This is exactly the freedom that ordinary exact MCSP quotients do not have.

For randomized reductions, purity can be relaxed further: for each promised source \(x\), over the seed \(r\), the output need only land in the correct target promise with high probability.

The seed need not be globally good for all source strings simultaneously.

---

## 4. Randomized seed-indexed quotient

Let

\[
J_r(x)
\]

be a randomized quotient.

Define target sets

\[
Y'=\{(r,z): z\text{ has a valid YES explanation}\},
\]

\[
N'=\{(r,z): z\text{ satisfies the declared NO promise}\}.
\]

A valid randomized promise reduction requires:

\[
x\in Y
\Longrightarrow
\Pr_r[(r,J_r(x))\in Y']\ge1-\varepsilon,
\]

\[
x\in N
\Longrightarrow
\Pr_r[(r,J_r(x))\in N']\ge1-\varepsilon.
\]

Bad seeds may land outside the target promise.

This is fundamentally different from demanding that every fixed seed induce a globally answer-pure quotient.

That distinction explains why fixed-seed affine-hash no-go theorems do not automatically kill randomized promise quotients.

---

## 5. The current fingerprint construction is an example

For MCSP, let

\[
Y_s
=
\{TT(C):|C|\le s\}.
\]

For a fingerprint \(H_r\), define the image language

\[
\operatorname{HASHIMAGE}_s
=
\{
(r,z):
\exists C,\ |C|\le s,\ H_r(TT(C))=z
\}.
\]

Then

\[
f\in Y_s
\Longrightarrow
(r,H_r(f))
\in \operatorname{HASHIMAGE}_s
\]

for every seed.

For a hard \(f\), a sufficiently strong fingerprint may satisfy

\[
\Pr_r[
(r,H_r(f))
\notin \operatorname{HASHIMAGE}_s
]
\ge 1-\varepsilon.
\]

This is a genuinely lossy many-to-one semantic quotient.

Its current failures are quantitative/model-theoretic:

1. dense fingerprints are too expensive in the one-tape source model;
2. the target is HASHIMAGE, not ordinary MCSP;
3. the obvious verifier is not polynomial with one exponent uniform as the MCSP parameter tends to zero.

Those are bridge problems, not failures of the lossy-promise abstraction.

---

## 6. General lower-bound transfer through a promise-pure quotient

Let \(\Pi_0\) be a promise problem on length \(N\) with a lower bound

\[
T_{\Pi_0}(N)
>
N^{c-o(1)}
\]

in a declared randomized machine model.

Suppose a randomized quotient \(J\) reduces \(\Pi_0\) to another promise problem \(\Pi_1\), with:

- output length
  \[
  M=N^{\lambda+o(1)};
  \]
- reduction time
  \[
  N^{r+o(1)};
  \]
- reduction error at most \(\varepsilon<1/3\);
- model-matched composition overhead fully charged.

If \(\Pi_1\) has an algorithm running in

\[
M^{K+o(1)},
\]

then the source runs in

\[
N^{\max\{r,\lambda K\}+o(1)}
\]

under ideal same-model composition.

Therefore any source lower bound with

\[
r<c
\]

forces

\[
\lambda K\ge c
\]

unless some model/promise hypothesis fails.

This is the lossy many-to-one analogue of the project's earlier max-affine exponent ledger.

---

## 7. New theorem: lossy promise cascade eliminates unknown K

The quotient language need not remain the same after each step.

Let

\[
\Pi_0,\Pi_1,\Pi_2,\ldots
\]

be a jointly uniform family of promise problems.

Assume:

1. \(\Pi_0\) has an unconditional same-model lower bound
   \[
   N^{c-o(1)}
   \]
   for some \(c>1\).

2. For every stage \(j\), there is a randomized promise reduction
   \[
   J_j:\Pi_j\to\Pi_{j+1}
   \]
   with length contraction
   \[
   N_{j+1}\le N_j^{\lambda+o(1)},
   \qquad
   0<\lambda<1,
   \]
   and local reduction time
   \[
   N_j^{r+o(1)}
   \]
   for one fixed \(r<c\).

3. Errors across every fixed finite composition can be amplified/allocated while preserving the source lower-bound error regime.

4. There is one joint language/promise specification
   \[
   \Pi^\star(1^j,x)
   \]
   whose YES/NO sides are in a class that collapses to P under the contradiction hypothesis, with one resulting polynomial exponent \(K\) independent of \(j\).

5. Sequential composition is model matched, including input/output tapes, replay, serialization, workspace and random bits.

### Theorem 7.1: LOSSY-PROMISE-CASCADE1

Under those hypotheses, the contradiction hypothesis is impossible.

### Proof

Under the collapse, the joint target family has one polynomial algorithm of exponent \(K<\infty\).

After \(d\) quotient stages, the final call has cost

\[
N^{\lambda^d K+o(1)}.
\]

The reduction work across all stages is bounded by

\[
N^{r+o(1)}
+
N^{\lambda r+o(1)}
+
\cdots
\]

and therefore has exponent \(r+o(1)\).

Choose one finite constant \(d\) after the hypothetical \(K\) is fixed so that

\[
\lambda^d K<c.
\]

Then the entire composed source algorithm has exponent

\[
\max\{r,\lambda^dK\}<c,
\]

contradicting the source lower bound. \(\square\)

### Significance

This is the earlier unknown-\(K\) elimination mechanism, but now the contraction is allowed to pass through a sequence of **different lossy promise languages**.

We do not need an MCSP-to-MCSP self-reduction.

---

## 8. Why this may be easier than THRESHOLD-DESCENT1

THRESHOLD-DESCENT1 required a map

\[
MCSP_{\beta}
\to
MCSP_{\beta'}
\]

in the same problem family while preserving a delicate lower-bound slope.

LOSSY-PROMISE-CASCADE1 permits

\[
MCSP
\to
Q_1
\to
Q_2
\to\cdots
\]

where each \(Q_j\) is tailored to the particular lossy representation.

The essential requirements are only:

- source answer survives as an image label;
- each quotient is genuinely shorter;
- the family of image-label problems remains jointly low under the collapse hypothesis;
- the source-model reduction cost remains below the known lower-bound exponent.

This is strictly more flexible.

---

## 9. Partial functions are a natural quotient representation

A second canonical lossy map is coordinate restriction.

For a set \(S\subseteq\{0,1\}^n\), define

\[
J_S(f)=f|_S.
\]

The target is a partial function.

The natural label is Partial-MCSP:

\[
\exists\text{ size-}s\text{ circuit consistent with all labels in }f|_S.
\]

This map is automatically many-to-one.

YES preservation is exact:

\[
CC(f)\le s
\Longrightarrow
J_S(f)\in PartialMCSP_s.
\]

NO preservation requires a promise that \(f\) is sufficiently far from every size-\(s\) circuit, or a stronger anti-checker/hitting-set property.

Thus partial functions expose precisely the missing promise condition rather than forcing an invalid exact quotient.

The Partial-MCSP literature is therefore directly relevant to the present branch, not merely adjacent meta-complexity background.

---

## 10. Relation to Hirahara's promise-problem viewpoint

Hirahara's work on non-disjoint promise problems explicitly treats meta-computational promise problems as the natural objects induced by PRG/HSG constructions.

His later Partial-MCSP result proves that partial-function circuit minimization is NP-hard under randomized polynomial-time many-one reductions.

These results do not supply LOSSY-PROMISE-CASCADE1 automatically.

They do support the architectural move:

\[
\boxed{
\text{stop forcing the quotient target to be ordinary total MCSP.}
}
\]

The promise/image-label problem itself may be the correct intermediate computational object.

---

## 11. New research targets

### A. PROMISE-PURE-QUOTIENT1

Construct one near-linear same-model randomized quotient from the published high-parameter MCSP lower-bound source into a shorter promise problem with exact one-sided or two-sided image semantics.

### B. PARTIAL-MCSP-BRIDGE1

Test whether a streamed partial-function quotient can preserve a sufficiently strong MCSP NO promise while having output exponent below one.

Audit anti-checkers, Hamming-distance-to-small-circuit bounds, and random coordinate samples.

### C. ITERABLE-IMAGE1

Find a family of image-label problems closed under repeated lossy quotienting, with one jointly NP/PSPACE-uniform verifier whose exponent/space bound does not deteriorate with the stage.

### D. ONE-TAPE-PROMISE-FUSION1

Give a source-model fusion theorem for the quotient cascade with no generic quadratic one-tape penalty.

---

## 12. Conclusion

The current no-go results are not telling us that compression is impossible.

They are telling us the compression cannot be:

- injective;
- source-reconstructible;
- a fixed short affine sketch;
- ordinary padding;
- or silently relabeled as ordinary MCSP.

The surviving shape is exactly:

\[
\boxed{
\text{lossy}
+
\text{many-to-one}
+
\text{promise-pure}
+
\text{jointly uniform image label}.
}
\]

This matches the strongest earlier project quotient architecture and gives a direct new way to reuse the old \(K\)-elimination theorem.

The highest-value target should therefore move from a same-problem threshold descent to:

\[
\boxed{\textbf{PROMISE-PURE-QUOTIENT1 / LOSSY-PROMISE-CASCADE1}.}
\]

## References

1. Shuichi Hirahara, *Non-Disjoint Promise Problems from Meta-Computational View of Pseudorandom Generator Constructions*, CCC 2020 / Theory of Computing 19(4), 2023.
2. Shuichi Hirahara, *NP-Hardness of Learning Programs and Partial MCSP*, FOCS 2022 / ECCC TR22-119.
3. Dylan McKay, Cody Murray, R. Ryan Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019.
4. Mahdi Cheraghchi, Shuichi Hirahara, Dimitrios Myrisiotis, Yuichi Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021.
5. PORTFOLIO-SHIELD-SAT project: prior lossy quotient / image-label audits, ASYMPTOTIC-CONE5, THRES-ENTROPY1, THRES-LOSSYPROBE2, THRES-HASHBRIDGE4, CLOCKSAT1.
