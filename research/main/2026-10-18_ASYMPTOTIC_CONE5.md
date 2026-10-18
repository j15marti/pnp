# ASYMPTOTIC-CONE5: Cofinal Slope Absorption and Parameter-Descent Targets for MCSP

**Status:** New exact conditional magnification criteria and a parameter-descent theorem. These results do not prove a new MCSP lower bound. They show that the lower-bound exponent itself may shrink to zero, provided it shrinks asymptotically more slowly than the MCSP compression parameter. This converts the project's earlier unknown-\(K\) elimination into an asymptotic hardness-magnification criterion.

**Date:** 2026-10-18

---

## 1. Motivation

The current META-LIFT branch has been treating the unknown polynomial exponent \(K\) as something to eliminate by a clock family or a recursive contraction.

A recent project branch, MCSPMAGCONE1, suggested a different route: let the MCSP circuit-size parameter

\[
s=N^\beta,\qquad N=2^n,
\]

tend to zero in the exponent,

\[
\beta\downarrow0.
\]

Under a collapse hypothesis such as \(P=NP\) or \(NP\subseteq P/poly\), the known upper bounds for MCSP have resource exponents of the form

\[
u_0+K\beta+o(1)
\]

for one fixed but unknown finite \(K\).

Therefore one does **not** need a fixed positive lower-bound margin. It is enough for an unconditional lower-bound margin \(g(\beta)\) to satisfy

\[
\boxed{
\frac{g(\beta)}{\beta}\to\infty.
}
\]

The lower-bound exponent may itself tend to zero.

This is the clean asymptotic analogue of the project's earlier cofinal \(K\)-elimination.

---

## 2. General cofinal slope-absorption theorem

Let \(\{Q_\beta\}_{\beta>0}\) be a parameterized family of problems on \(N\)-bit inputs.

Fix a computational model \(\mathcal M\) and a baseline exponent \(u_0\ge0\).

Suppose a collapse hypothesis \(H\) implies that there exist a finite constant \(K\) and a function

\[
\rho(\beta)>0,\qquad \rho(\beta)\to0,
\]

such that, for every sufficiently small fixed \(\beta>0\),

\[
Q_\beta
\in
\mathcal M
\left[
N^{u_0+K\rho(\beta)+o(1)}
\right].
\]

Suppose there is a sequence

\[
\beta_j\downarrow0
\]

and an unconditional lower-bound margin \(g(\beta_j)>0\) such that

\[
Q_{\beta_j}
\notin
\mathcal M
\left[
N^{u_0+g(\beta_j)-o(1)}
\right].
\]

### Theorem 2.1: COFINAL-SLOPE-ABSORB1

If

\[
\boxed{
\frac{g(\beta_j)}{\rho(\beta_j)}
\longrightarrow\infty,
}
\]

then \(H\) is false.

### Proof

Assume \(H\).

It supplies one fixed finite \(K\).

Choose \(j\) so large that

\[
g(\beta_j)>2K\rho(\beta_j).
\]

For this now-fixed \(j\), the gap

\[
\Delta
=
g(\beta_j)-K\rho(\beta_j)
\]

is a positive constant independent of \(N\).

For sufficiently large \(N\), all \(o(1)\) terms are smaller than \(\Delta/3\). The collapse upper bound then places \(Q_{\beta_j}\) strictly inside the class excluded by the lower bound, contradiction. \(\square\)

### Examples of sufficient shrinking margins when \(\rho(\beta)=\beta\)

Any of the following are enough:

\[
g(\beta)=\sqrt{\beta},
\]

\[
g(\beta)=\beta\log(1/\beta),
\]

or a fixed positive constant.

By contrast,

\[
g(\beta)=C\beta
\]

for one fixed \(C\) is not enough to eliminate an arbitrary unknown \(K\).

---

## 3. Search-MCSP streaming consequence

McKay-Murray-Williams prove that, if \(P=NP\), then for every reasonable size parameter \(s(n)\), search-MCSP has a one-pass streaming algorithm using

\[
\operatorname{poly}(s(n))
\]

space and

\[
\operatorname{poly}(s(n))
\]

update time.

The proof uses one fixed polynomial-time algorithm for Circuit-Min-Merge after the polynomial hierarchy collapses. Therefore one may take one finite constant \(d\), independent of the particular sufficiently small fixed \(\beta\), such that for

\[
s=N^\beta
\]

both resources are bounded by

\[
N^{d\beta+o(1)}.
\]

### Corollary 3.1: STREAM-SLOPE-MAGNIFY1

Suppose there exist

\[
\beta_j\downarrow0
\]

and \(g(\beta_j)>0\) such that every one-pass search-MCSP streaming algorithm at

\[
s=N^{\beta_j}
\]

has either space or update time exceeding

\[
N^{g(\beta_j)-o(1)},
\]

and

\[
\boxed{
\frac{g(\beta_j)}{\beta_j}\to\infty.
}
\]

Then

\[
\boxed{P\ne NP.}
\]

### Interpretation

MCSPMAGCONE1 required a fixed \(\delta>0\) margin

\[
N^\delta.
\]

That is sufficient but stronger than necessary.

The correct asymptotic target is merely

\[
N^{\omega(\beta)}.
\]

Equivalently, since \(s=N^\beta\), the required streaming lower bound is

\[
s^{\omega(1)}
\]

along the selected parameter sequence.

So the target is a **superpolynomial-in-\(s\)** streaming lower bound, not necessarily any fixed power of \(N\).

---

## 4. One-tape MCSP version

Cheraghchi-Hirahara-Myrisiotis-Yoshida restate the McKay-Murray-Williams streaming construction as a one-tape oracle upper bound:

\[
MCSP[s(n)]
\in
DTIME_1^O[N\cdot\operatorname{poly}(s(n))]
\]

for an oracle \(O\in\Sigma_3^P\), with query lengths \(\operatorname{poly}(s(n))\).

Under \(P=NP\),

\[
\Sigma_3^P=P.
\]

Replacing the fixed oracle procedure by its fixed polynomial-time algorithm and charging the one-tape simulation yields, for some finite constant \(d\),

\[
MCSP[N^\beta]
\in
DTIME_1
\left[
N^{1+d\beta+o(1)}
\right]
\]

for every sufficiently small fixed \(\beta\).

### Corollary 4.1: ONETAPE-SLOPE-MAGNIFY1

If there are \(\beta_j\downarrow0\) and margins \(g(\beta_j)>0\) such that

\[
MCSP[N^{\beta_j}]
\notin
DTIME_1
\left[
N^{1+g(\beta_j)-o(1)}
\right]
\]

and

\[
\frac{g(\beta_j)}{\beta_j}\to\infty,
\]

then

\[
P\ne NP.
\]

Again the excess exponent may tend to zero.

---

## 5. Gap-MCSP circuit version

Oliveira-Pich-Santhanam prove the following magnification theorem: for a universal constant \(c\), a fixed \(N^{1+\varepsilon}\) lower bound for sufficiently small Gap-MCSP parameters implies

\[
NP\not\subseteq P/poly.
\]

Their proof actually gives a more quantitative statement.

Assume

\[
NP\subseteq P/poly.
\]

Their Anti-Checker Lemma supplies a fixed constant \(k\) such that, for every sufficiently small \(\beta\), the anti-checker circuit has size

\[
N^{1+k\beta}.
\]

The generated anti-checker list has

\[
t=N^{10\beta}
\]

entries, so wiring the selected truth-table bits costs

\[
N^{1+10\beta}.
\]

Their Succinct-MCSP instance has length

\[
m=N^{10\beta+o(1)}.
\]

Under \(NP\subseteq P/poly\), Succinct-MCSP has circuits of size \(m^\ell\) for one fixed \(\ell\). Thus this final component has size

\[
N^{10\ell\beta+o(1)}.
\]

For all sufficiently small \(\beta\), the last term is below the linear-scale terms. Consequently there is one finite constant

\[
C
\]

such that, for every sufficiently small \(\beta\),

\[
GapMCSP_\beta
\in
Circuit
\left[
N^{1+C\beta+o(1)}
\right],
\]

where \(GapMCSP_\beta\) denotes their promise

\[
Gap\text{-}MCSP
\left[
\frac{2^{\beta n}}{10n},
2^{\beta n}
\right].
\]

### Corollary 5.1: GAPMCSP-SLOPE-MAGNIFY1

Suppose there are \(\beta_j\downarrow0\) and \(g(\beta_j)>0\) such that

\[
GapMCSP_{\beta_j}
\notin
Circuit
\left[
N^{1+g(\beta_j)-o(1)}
\right]
\]

and

\[
\boxed{
\frac{g(\beta_j)}{\beta_j}\to\infty.
}
\]

Then

\[
\boxed{
NP\not\subseteq P/poly,
}
\]

and in particular

\[
P\ne NP.
\]

This strictly weakens the fixed-\(\varepsilon\) premise in the published theorem.

---

## 6. Asymptotic exponent shrinkage as a lower-bound transport theorem

The user's proposed “asymptotic shrinkage of the exponent” can be stated exactly.

Suppose a lower-bound transport operation takes a certified point

\[
(\beta,g)
\]

to another certified point

\[
(\beta',g')
\]

in the same target problem/model/promise family.

Assume fixed constants

\[
0<\lambda<1,
\qquad
\rho>0
\]

such that

\[
\beta'\le\lambda\beta
\]

and

\[
g'\ge\rho g.
\]

### Theorem 6.1: SLOPE-AMPLIFICATION1

If

\[
\boxed{\rho>\lambda,}
\]

then repeated transport yields

\[
\beta_t\le\lambda^t\beta_0,
\]

\[
g_t\ge\rho^t g_0,
\]

and hence

\[
\boxed{
\frac{g_t}{\beta_t}
\ge
\left(\frac{\rho}{\lambda}\right)^t
\frac{g_0}{\beta_0}
\to\infty.
}
\]

Therefore any one valid seed lower bound with \(g_0>0\), together with a repeatable same-model transport satisfying \(\rho>\lambda\), activates the cofinal slope-magnification criteria above.

### Important point

The lower-bound margin itself may shrink:

\[
\rho<1
\]

is allowed.

For example,

\[
\lambda=\frac12,
\qquad
\rho=\frac34
\]

gives

\[
\beta_t=2^{-t}\beta_0,
\qquad
g_t\ge(3/4)^t g_0.
\]

Both exponents go to zero, but

\[
\frac{g_t}{\beta_t}
\ge
\left(\frac32\right)^t
\frac{g_0}{\beta_0}
\to\infty.
\]

This is the exact asymptotic-shrinkage phenomenon we want.

---

## 7. Variable-factor version

A fixed contraction is unnecessary.

Suppose

\[
\beta_{t+1}\le\lambda_t\beta_t,
\]

\[
g_{t+1}\ge\rho_t g_t.
\]

Then

\[
\frac{g_t}{\beta_t}
\ge
\frac{g_0}{\beta_0}
\prod_{i<t}
\frac{\rho_i}{\lambda_i}.
\]

Thus it suffices that

\[
\prod_i\lambda_i=0
\]

in the limiting sense

\[
\sum_i-\log\lambda_i=\infty,
\]

and

\[
\boxed{
\sum_i
\log\left(\frac{\rho_i}{\lambda_i}\right)
=\infty.
}
\]

This permits contraction factors tending to one.

The right invariant is therefore not a fixed shrinkage constant. It is the cumulative growth of the **lower-bound slope**

\[
\boxed{
\Gamma(\beta)=\frac{g(\beta)}{\beta}.
}
\]

---

## 8. Recent lower bounds: which ones help?

### 8.1 Cheraghchi-Hirahara-Myrisiotis-Yoshida: useful seed, wrong parameter region

Their strongest oracle one-tape theorem says that for every

\[
\frac12<\mu<1
\]

and every

\[
\frac12<\mu_0<\mu,
\]

\[
MCSP[N^\mu]
\notin
BPTIME_1^O
\left[
N^{2(\mu_0-o(1))}
\right]
\]

even with arbitrary oracle \(O\) when all oracle queries have length \(N^{o(1)}\).

Thus the lower exponent can approach

\[
2\mu
\]

from below.

This is a strong exponent lower bound.

But it only exists in the regime

\[
\mu>\frac12.
\]

The same paper explicitly identifies this as the parameter wall: current magnification upper bounds live at \(s=2^{o(n)}=N^{o(1)}\), while their lower bound lives above the square-root threshold.

So this theorem is **not** itself a P-vs-NP conclusion.

It is, however, an excellent seed for SLOPE-AMPLIFICATION1.

A parameter-descent transformation that starts at any \(\mu_0>1/2\) and repeatedly satisfies

\[
\mu_{t+1}\le\lambda\mu_t,
\qquad
g_{t+1}\ge\rho g_t,
\qquad
\rho>\lambda,
\]

would carry this known unconditional seed into the asymptotic magnification cone.

### 8.2 Near-quadratic \(N^{1.99}\) one-tape lower bound: same diagnosis

The same paper proves

\[
MCSP[N^{\mu_2}]
\notin
BPTIME_1[N^{1.99}]
\]

for a constant \(\mu_2\) close to one.

This gives a large starting margin

\[
g_0=0.99.
\]

The exponent is already more than strong enough.

The missing resource is **parameter descent**, exactly as the authors themselves emphasize.

### 8.3 Comparator-circuit MCSP lower bound: bounded slope

Known shrinkage arguments give, for comparator circuits,

\[
MCSP[N^\alpha]
\notin
Comparator
\left[
N^{1+\alpha/2-\varepsilon}
\right]
\]

for the stated parameter range.

The excess margin is only

\[
g(\alpha)\approx\frac{\alpha}{2}.
\]

Hence

\[
\frac{g(\alpha)}{\alpha}
\approx\frac12.
\]

This does not eliminate an unknown polynomial coefficient by itself.

It is a useful control demonstrating why the **ratio** \(g(\beta)/\beta\), not the absolute lower-bound exponent, is the correct quantity.

### 8.4 Formula/branching-program/local-PRG lower bounds

There are much stronger MCSP lower bounds against De Morgan formulas, general formulas, branching programs, and local-generator/data-structure models.

These may supply seeds or gadgets, but their model does not match the direct \(P\ne NP\) streaming/one-tape/circuit magnification endpoints above.

They remain supporting technology rather than a terminal lower bound.

### 8.5 NAE high-girth/moment work

The recent NAEGAUGEHIGHGIRTH1 construction gives logarithmic-order pseudorandom UNSAT distributions and exact gauge independence.

It does not yet provide a lower bound against the unrestricted circuit/streaming models required here.

Its useful role would be in constructing a parameter-descent gadget or a local indistinguishability layer, not as the final exponent seed.

---

## 9. Why ordinary padding does not amplify slope

The project has repeatedly tested polynomial padding as a \(K\)-elimination device.

For one-tape lower bounds, let a source problem on length \(N\) have a lower-bound exponent

\[
1+g.
\]

Pad to

\[
N'=N^q,
\qquad q>1.
\]

The same raw work lower bound, when merely re-expressed in the new length, becomes

\[
(N')^{(1+g)/q}.
\]

The excess over the linear baseline is

\[
\frac{1+g}{q}-1
=
\frac{g-(q-1)}{q},
\]

which is no larger than \(g/q\) and is usually zero or negative.

Meanwhile a circuit threshold

\[
s=N^\beta
\]

becomes

\[
s=(N')^{\beta/q}.
\]

Thus padding never produces the desired inequality

\[
\rho>\lambda.
\]

For zero-baseline resources, pure homogeneous rescaling can at best scale both the resource exponent and \(\beta\) by the same factor, preserving the slope rather than amplifying it.

This formalizes the negative result seen in PADLIFT-STRATEGY7.

---

## 10. New primary target: THRESHOLD-DESCENT1

The known one-tape lower bounds give us a genuine unconditional seed.

The missing theorem can now be stated without reference to an arbitrary SAT solver.

### THRESHOLD-DESCENT1

Construct a repeatable, model-matched lower-bound transport for MCSP satisfying

\[
(\beta,g)
\longmapsto
(\beta',g')
\]

with

\[
\beta'\le\lambda\beta,
\]

\[
g'\ge\rho g,
\]

and

\[
\boxed{\rho>\lambda.}
\]

The transport must preserve:

1. the MCSP or Gap-MCSP promise;
2. the declared computational model;
3. uniformity/randomization/error requirements;
4. input encoding and output-length accounting;
5. all simulation and preprocessing overhead.

If it exists, then the Cheraghchi-Hirahara-Myrisiotis-Yoshida lower bound supplies the starting seed and finite/asymptotic iteration supplies the P-vs-NP contradiction.

### Equivalent formulation

We do not need to preserve the lower-bound exponent.

We only need to make the **compression parameter shrink faster than the lower-bound margin**.

That is a substantially weaker target.

---

## 11. Candidate mechanisms and immediate falsifiers

### A. Simple dummy-variable padding

Rejected by Section 9.

### B. Ordinary restrictions

A restriction that shrinks both the active truth-table dimension and the hardness exponent proportionally has

\[
\rho=\lambda.
\]

It cannot improve the slope.

This matches earlier project audits of restriction-based exponent transport.

### C. Direct products / direct sums

Potentially useful only if one proves a genuine resource direct-sum theorem.

The desired effect is that the threshold parameter contracts while the machine lower-bound margin is retained by more than the same fraction.

Generic circuit sharing is an immediate adversary.

This connects directly to DATA-DIRECTSUM1 and PCP-GATE1.

### D. Local PRG / range-avoidance replacement

Potentially useful because the high-parameter one-tape lower bound is itself proved using local PRGs.

A successful construction would need to reduce the effective MCSP threshold without increasing the local-generator complexity at the same rate.

This is the most literature-aligned candidate, but no such descent theorem is currently known.

### E. Succinct/implicit threshold encoding

This can change the parameter without materializing a larger truth table.

However, the target must remain the same magnification problem/model or carry a separately proved magnification theorem.

Implicit-MCSP hardness results currently require additional assumptions in the strongest known forms.

---

## 12. Relation to CLOCK-INDEPENDENT-GATE1

There are now two parallel routes.

### Route A: META-LIFT / local representation

Use:

- KPI remote-point hardness;
- succinct PSPACE membership;
- cofinal clock absorption;
- CLOCK-INDEPENDENT-GATE1.

### Route B: asymptotic MCSP cone

Use:

- existing MCSP hardness magnification;
- a known high-parameter one-tape lower-bound seed;
- THRESHOLD-DESCENT1 / SLOPE-AMPLIFICATION1.

Route B has one major advantage:

\[
\boxed{
\text{it does not require constructing a new semantic gating problem.}
}
\]

MCSP already supplies the meta-complexity gate.

Its sole new burden is parameter descent.

For that reason, THRESHOLD-DESCENT1 should now be treated as at least as high-value as CLOCK-INDEPENDENT-GATE1.

---

## 13. Current conclusion

The exponent lower bounds from the recent parallel work are useful, but not because their exponents need to be increased.

They are already strong enough.

The missing property is a transport in the **parameter direction**.

The strongest new quantitative criterion is:

\[
\boxed{
\frac{g(\beta)}{\beta}\to\infty.
}
\]

This gives a form of asymptotic exponent shrinkage where both the MCSP parameter exponent and the lower-bound margin may tend to zero.

The lower-bound margin only has to shrink more slowly.

This is the correct analogue of the project's earlier unknown-\(K\) contraction.

The most concrete next problem is therefore:

\[
\boxed{
\textbf{THRESHOLD-DESCENT1 / SLOPE-AMPLIFICATION1}.
}
\]

Start from the unconditional one-tape MCSP lower bound above the \(1/2\) threshold and seek a repeatable transformation that decreases the circuit-size exponent faster than it decreases the lower-bound margin.

---

## References

1. Dylan M. McKay, Cody D. Murray, R. Ryan Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019.
2. Mahdi Cheraghchi, Shuichi Hirahara, Dimitrios Myrisiotis, Yuichi Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, ECCC TR20-103 / Algorithmica.
3. Igor C. Oliveira, Ján Pich, Rahul Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, CCC 2019 / ECCC TR18-158.
4. Igor C. Oliveira, Rahul Santhanam, *Hardness Magnification for Natural Problems*, FOCS 2018.
5. Karthik C. S., Satyanarayana V. Lokam, Nitin Saurabh, *Algorithms and Lower Bounds for Comparator Circuits from Shrinkage*, Algorithmica 2023.
6. Oliver Korten, Toniann Pitassi, Russell Impagliazzo, *Stronger Cell Probe Lower Bounds via Local PRGs*, FOCS 2025 / ECCC TR25-030.
7. PORTFOLIO-SHIELD-SAT project: MCSPMAGCONE1, PADLIFT-STRATEGY7, DATA-DIRECTSUM1, K-ELIMINATION-TRANSFER4, NAEGAUGEHIGHGIRTH1.
