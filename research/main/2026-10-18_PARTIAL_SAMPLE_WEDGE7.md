# PARTIAL-SAMPLE-WEDGE7: Hamming-Boundary and Interpolation Barriers for Partial-MCSP Quotients

**Status:** PROVED/EXACT combinatorial and circuit-counting lemmas, pending independent review. This rules out a natural source-independent coordinate-sampling implementation of `PARTIAL-MCSP-BRIDGE1` for exact MCSP and sharply constrains it for Gap-MCSP. It does not rule out source-adaptive anti-checkers, nonlinear fingerprints, Hirahara-style random-function reductions, or arbitrary promise-pure quotients. P versus NP remains OPEN.

**Date:** 2026-10-18

---

## 1. Motivation

`LOSSY-PROMISE-CASCADE6` identified partial functions as a natural many-to-one representation:

\[
J_S(f)=f|_S.
\]

YES preservation is immediate: a circuit computing the full truth table is consistent with every sampled partial table.

The unresolved issue is NO preservation. This note proves two exact obstructions for the most direct proposal, in which the sample coordinates are selected independently of the source truth table and the target is ordinary Partial-MCSP.

The two obstructions form a wedge:

1. if too few coordinates are sampled, a near hard function is indistinguishable from a small function;
2. if the target circuit threshold is too large relative to the number of sampled coordinates, every partial function has a trivial interpolating circuit.

For the standard Gap-MCSP parameter \(s=N^\beta\), these two constraints force sample length at least

\[
\widetilde\Omega\!\left(N^{\max\{\beta,1-\beta\}}\right).
\]

Above the square-root threshold \(\beta>1/2\), the interpolation side dominates and the output sample is already essentially as large as the circuit-size parameter. The naive Partial-MCSP quotient therefore does not provide threshold descent.

---

## 2. Model

Let

\[
N=2^n
\]

be the truth-table length. Let \(CC(f)\) denote fan-in-two Boolean circuit size under any fixed standard complete basis.

For a threshold \(s\), define

\[
Y_s=\{f\in\{0,1\}^N:CC(f)\le s\}.
\]

For a promise gap \(s_{\rm yes}<s_{\rm no}\), define

\[
Y=Y_{s_{\rm yes}},
\qquad
N_0=\{f:CC(f)\ge s_{\rm no}\}.
\]

A coordinate-sampling quotient chooses a set

\[
S\subseteq[N],\qquad |S|=m,
\]

independently of the source truth table and outputs

\[
J_S(f)=(S,f|_S).
\]

The uniform-sampling case chooses \(S\) uniformly among the \(m\)-subsets of \([N]\). Including the random seed or a canonical description of \(S\) in the output does not affect the indistinguishability arguments below.

---

## 3. Exact MCSP has a Hamming-boundary YES/NO pair

### Lemma 3.1: HYPERCUBE-BOUNDARY1

Let \(A\subsetneq\{0,1\}^N\) be nonempty. Then there exist

\[
x\in A,
\qquad
y\notin A
\]

with

\[
d_H(x,y)=1.
\]

### Proof

The Hamming cube on \(\{0,1\}^N\) is connected. Take a path from a vertex in \(A\) to a vertex outside \(A\), and select the first edge crossing the boundary. \(\square\)

### Corollary 3.2: MCSP-BOUNDARY1

Whenever \(Y_s\) is nonempty and proper, there are truth tables

\[
f_{\rm yes}\in Y_s,
\qquad
f_{\rm no}\notin Y_s
\]

that differ at exactly one truth-table coordinate.

For every fixed \(0<\beta<1\), the set \(Y_{N^\beta}\) is nonempty and proper for all sufficiently large \(N\).

### Proof of properness

A size-\(s\) circuit can be encoded by

\[
O(s\log(n+s))
\]

bits: for every gate, specify its constant-size type and two predecessors among the inputs and earlier gates. Hence the number of functions computed by size-\(s\) circuits is at most

\[
2^{O(s\log(n+s))}.
\]

For \(s=N^\beta\), this is

\[
2^{o(N)},
\]

strictly smaller than the \(2^N\) Boolean functions for large \(N\). Constant functions show nonemptiness. \(\square\)

---

## 4. Coordinate-sampling indistinguishability

Let \(f_0,f_1\) differ on a set

\[
D=\{i:f_0(i)\ne f_1(i)\},
\qquad |D|=d.
\]

Let

\[
E=\{S\cap D\ne\varnothing\}
\]

be the event that the sample notices at least one disagreement.

If \(E\) does not occur, then

\[
J_S(f_0)=J_S(f_1)
\]

exactly, including the seed/sample-set component.

### Theorem 4.1: SAMPLE-PAIR-ERROR1

Let a possibly randomized target decision procedure receive only \(J_S(f)\). Suppose it must output opposite labels on \(f_0\) and \(f_1\), and succeeds with probability at least \(1-\varepsilon\) on each source.

Then

\[
\boxed{
\Pr[E]\ge1-2\varepsilon.
}
\]

If the reduction/target has perfect completeness on \(f_0\), then soundness \(1-\varepsilon\) on \(f_1\) requires

\[
\boxed{
\Pr[E]\ge1-\varepsilon.
}
\]

### Proof

Conditioned on \(\neg E\), the target input distributions are identical. For opposite correct labels, the sum of the two conditional success probabilities is therefore at most one. Conditioned on \(E\), their sum is at most two. Hence

\[
\Pr[\mathrm{success}|f_0]
+
\Pr[\mathrm{success}|f_1]
\le
1+\Pr[E].
\]

If both terms on the left are at least \(1-\varepsilon\), the first inequality follows.

For perfect completeness, every target input arising from \(f_0\) is accepted. On \(\neg E\), the identical target input arising from \(f_1\) is also accepted. Thus rejection of \(f_1\) can occur only on \(E\). \(\square\)

### Corollary 4.2: UNIFORM-SAMPLE-BOUND1

For uniform sampling without replacement,

\[
\Pr[E]
=
1-
\frac{\binom{N-d}{m}}{\binom Nm}
\le
\frac{md}{N}.
\]

Therefore two-sided error \(\varepsilon\) requires

\[
\boxed{
m\ge(1-2\varepsilon)\frac Nd,
}
\]

and perfect completeness requires

\[
\boxed{
m\ge(1-\varepsilon)\frac Nd.
}
\]

For exact MCSP, Corollary 3.2 gives \(d=1\). Thus error \(1/3\) requires

\[
m\ge N/3
\]

for general two-sided reductions and

\[
m\ge2N/3
\]

for perfect-completeness Partial-MCSP sampling.

### Consequence

A source-independent sublinear coordinate sample cannot be a constant-error promise-pure reduction from exact MCSP to Partial-MCSP. This is a per-source randomized obstruction, not a fixed-seed/global-goodness argument.

---

## 5. Sparse high-complexity truth tables exist near zero

The exact-MCSP boundary theorem is stronger than needed for the no-gap problem. For Gap-MCSP we need a quantitative upper bound on the Hamming distance between a YES function and at least one NO function.

### Lemma 5.1: SPARSE-HARD-TABLE1

Fix \(0<\beta<1\) and put

\[
s=N^\beta.
\]

For all sufficiently large \(N=2^n\), there is a Boolean function \(h_N\) such that

\[
CC(h_N)>s
\]

and

\[
|h_N^{-1}(1)|
\le
C_\beta s
\]

for a constant \(C_\beta\) depending only on the circuit basis and \(\beta\).

Equivalently, a circuit-hard truth table occurs within Hamming distance

\[
O_\beta(N^\beta)
\]

of the all-zero function.

### Proof

The number of functions computed by size-\(s\) circuits is at most

\[
2^{C s\log_2(n+s)}
\]

for a basis-dependent constant \(C\).

Choose

\[
d=\lceil C_\beta s\rceil
\]

with \(C_\beta\) large enough. Since \(s=N^\beta\),

\[
\log_2\binom Nd
\ge
 d\log_2(N/d)
=
(C_\beta(1-\beta)+o(1))s\log_2 N.
\]

Meanwhile

\[
C s\log_2(n+s)
=
(C\beta+o(1))s\log_2N.
\]

Taking \(C_\beta>C\beta/(1-\beta)\) makes the number of weight-\(d\) truth tables exceed the number of size-\(s\) circuit functions. At least one such table therefore has circuit complexity greater than \(s\). \(\square\)

### Corollary 5.2: GAP-SAMPLE-FLOOR1

For the promise

\[
CC(f)\le s_{\rm yes}
\quad\text{versus}\quad
CC(f)>N^\beta,
\]

where the all-zero function is a YES instance, any uniform coordinate-sampling quotient with error at most \(1/3\) needs

\[
\boxed{
m=\Omega_\beta(N^{1-\beta}).
}
\]

With perfect completeness the same exponent holds with a stronger constant.

### Proof

Use the all-zero YES truth table and the hard sparse table from Lemma 5.1. Their Hamming distance is \(O_\beta(N^\beta)\). Apply Corollary 4.2. \(\square\)

This lower bound applies even though the sample coordinates and the random seed are explicitly included in the target instance.

---

## 6. Interpolation makes overly short partial samples trivial

A partial function consists of distinct labeled examples

\[
P=\{(x_j,b_j):j\in[m]\},
\qquad x_j\in\{0,1\}^n.
\]

### Lemma 6.1: PARTIAL-INTERPOLATION1

Every such partial function is consistent with a Boolean circuit of size

\[
O(mn).
\]

### Proof

For each positively labeled point \(x_j\), build the equality indicator

\[
EQ_{x_j}(x)
=
\bigwedge_{k=1}^n
\begin{cases}
x_k,&(x_j)_k=1,\\
\neg x_k,&(x_j)_k=0.
\end{cases}
\]

using \(O(n)\) gates. OR all positive indicators. Distinct negative examples are not equal to any positive example, so the circuit outputs zero on them. If there are no positive labels, use the constant-zero circuit. \(\square\)

### Corollary 6.2: PARTIAL-THRESHOLD-FLOOR1

The Partial-MCSP instance \((P,t)\) is automatically YES whenever

\[
t\ge Cmn
\]

for the basis-dependent interpolation constant \(C\).

Hence a coordinate-sampling reduction whose target threshold is \(t\) cannot have any NO outputs unless

\[
\boxed{
m=\Omega(t/n).}
\]

---

## 7. The square-root wedge

Combine the sampling and interpolation floors.

### Theorem 7.1: PARTIAL-SAMPLE-WEDGE1

Consider a uniform coordinate-sampling quotient from a Gap-MCSP promise on \(N=2^n\) bits into Partial-MCSP with target threshold

\[
t=N^{\beta+o(1)},
\qquad 0<\beta<1,
\]

perfect completeness, and constant soundness error.

If the NO promise includes all functions of circuit complexity greater than \(N^\beta\), then the number of sampled points must satisfy

\[
\boxed{
 m
 =
 \widetilde\Omega
 \left(
 N^{\max\{\beta,1-\beta\}}
 \right).
}
\]

### Proof

Corollary 5.2 gives

\[
m=\Omega_\beta(N^{1-\beta}).
\]

Corollary 6.2 gives

\[
m=\Omega(t/n)
=
N^{\beta-o(1)}.
\]

Take the maximum. \(\square\)

### Corollary 7.2: ABOVE-SQRT-NO-DESCENT1

For every fixed \(\beta>1/2\), such a quotient requires

\[
\boxed{
m=N^{\beta-o(1)}.}
\]

Thus the natural same-threshold Partial-MCSP sample does not move a high-parameter MCSP instance into a lower threshold exponent. If the target length is \(M=m\), then retaining threshold \(t=N^\beta\) gives

\[
t=M^{1-o(1)},
\]

which is the near-maximal/trivial interpolation regime.

This directly blocks the simplest attempt to descend from the published one-tape MCSP lower bounds above the square-root threshold by uniform coordinate sampling.

---

## 8. What survives

The theorem does **not** refute the broader `LOSSY-PROMISE-CASCADE1` architecture.

The following remain possible and require separate analysis:

1. **Source-adaptive anti-checkers.** The chosen coordinates may depend nontrivially on the source truth table and may be designed to hit every small circuit rather than sampled uniformly.
2. **Far-from-small-circuit promises.** If every NO instance is guaranteed to be Hamming-far from every size-\(s\) circuit, then sublinear random sampling can be sound.
3. **Non-coordinate nonlinear fingerprints.** A quotient may combine all source bits rather than expose a coordinate restriction.
4. **Random-function / conditional-Kolmogorov constructions.** Hirahara's Partial-MCSP hardness reduction uses random functions, pseudorandom-generator ideas and conditional Kolmogorov complexity; it is not the naive coordinate sampler ruled out here.
5. **Different target thresholds or image languages.** These require a complete promise and cascade ledger.

The result says that partial functions do not provide a free descent merely by taking a short random sample of the source truth table.

---

## 9. Revised highest-value targets

### A. SOURCE-ADAPTIVE-ANTICHECKER1

Construct, in the source one-tape model and below the published lower-bound exponent, a short list of coordinates \(S(f)\) such that:

- every source YES circuit has a short target explanation;
- every promised NO truth table disagrees with every target-size circuit on at least one selected coordinate;
- selection and serialization costs are fully charged;
- the target family is jointly low under the collapse assumption.

### B. DISTANCE-PROMISE-CASCADE1

Define an iterable promise family in which each NO instance is quantitatively Hamming-far from the relevant representation class, and show that this distance promise is preserved by each quotient stage.

### C. NONLINEAR-PROMISE-QUOTIENT1

Construct a non-coordinate, many-to-one quotient with promise-pure image fibers and near-linear one-tape evaluation.

---

## 10. Relation to the literature

Hirahara proves randomized NP-hardness of Partial-MCSP using algorithmic-information-theoretic machinery, random functions and conditional Kolmogorov complexity. The construction is substantially more structured than uniform coordinate sampling.

The meta-complexity literature also contains barriers showing that the complexity of MCSP can depend strongly on the size threshold and that robust reductions are delicate. The present theorem is elementary and model-specific: it isolates the exact Hamming-information and interpolation costs of one natural quotient proposal.

---

## 11. Conclusion

The partial-function route survives only in a stronger form than random coordinate sampling.

For exact MCSP, a one-bit Hamming boundary forces linear sampling.

For Gap-MCSP at threshold \(N^\beta\), sparse hard truth tables force

\[
\Omega(N^{1-\beta})
\]

samples, while generic interpolation forces

\[
\widetilde\Omega(N^\beta)
\]

samples if the target threshold remains \(N^\beta\).

Therefore the direct Partial-MCSP bridge has the exact lower envelope

\[
\boxed{
\widetilde\Omega
\left(
N^{\max\{\beta,1-\beta\}}
\right),
}
\]

with its minimum at the square-root parameter.

The next construction must use a **source-adaptive anti-checker, a preserved distance promise, or a genuinely nonlinear promise-pure quotient**.

---

## References

1. Shuichi Hirahara, *NP-Hardness of Learning Programs and Partial MCSP*, FOCS 2022 / ECCC TR22-119.
2. Igor C. Oliveira, Ján Pich, Rahul Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, CCC 2019 / ECCC TR18-158.
3. Hanlin Ren, Rahul Santhanam, *A Relativization Perspective on Meta-Complexity*, ECCC TR21-089.
4. PORTFOLIO-SHIELD-SAT project: `LOSSY-PROMISE-CASCADE6`, `THRES-ENTROPY1`, `THRES-LOSSYPROBE2`, `THRES-HASHBRIDGE4`, and `CLOCKFEATURE5`.
