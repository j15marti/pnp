# K-ELIMINATION-TRANSFER4: Recovering the Earlier K-Elimination and Porting It to META-LIFT

**Status:** Substantive reconciliation. The earlier project really did contain an exact K-elimination mechanism, but it was conditional on a strict hereditary contraction. That generic contraction does **not** transfer to arbitrary decoder descriptions. However, the current META-LIFT formulation can avoid the apparent \((\log M)^K\)-description problem altogether by using clocked uniform programs rather than expanded circuits. A cofinal clock parameter then absorbs the unknown exponent exactly, provided the source-to-target gating map is independent of that clock parameter.

No \(P\neq NP\) or \(P\neq PSPACE\) separation is claimed.

**Date:** 2026-10-18

---

## 1. What the earlier project actually proved

Repository recovery found three distinct K-elimination statements that had been conflated in later summaries.

### 1.1 Aggregate recursive fixed point

RECOVERY-STRENGTHEN7 proved the exact recurrence closure

\[
C=\max\left\{1,r,\frac{v-h}{1-h}\right\},
\qquad
P=\max\{p,h\},
\]

for a hereditary recursive phase with child-scale exponent

\[
h<1
\]

and fully charged executed child volume \(v\).

The handoff correctly states that the concrete ledger

\[
(r,v,h,p)
=
\left(\frac65,\frac{11}{10},\frac12,\frac12\right)
\]

**eliminates the inherited exponent \(K\)** once one uniform hereditary all-input phase with those bounds exists.

This was an exact fixed-point theorem. The missing theorem was the all-input phase itself.

### 1.2 Max-affine / return-cycle elimination

FINAL-LINK-ARC proved the more general max-affine recurrence

\[
t'
\le
\max\{r,\max_j(w_j+\lambda_j t)\},
\]

with every

\[
\lambda_j<1.
\]

The limiting envelope is

\[
C_*
=
\max\left\{
r,\max_j\frac{w_j}{1-\lambda_j}
\right\}.
\]

Thus a finite number of returns suppresses every finite seed exponent.

The typed-cycle version weakens the hypothesis further: individual edges may have scale one, provided every reachable return cycle has product

\[
\prod_{e\in Z}\theta_e<1.
\]

### 1.3 Cofinal charged hit

The strongest logical weakening was the Cofinal charged hit theorem.

It does **not** require one universal contraction map.

It allows the successful finite route, its parameters, and its depth to depend on the unknown starting exponent \(K\). It only requires an unbounded/cofinal set of candidate exponents and one finite source-checkable route to a forbidden endpoint for every such seed.

This is the previous project result most directly relevant to the current META-LIFT issue.

---

## 2. What the earlier theorem did not prove

KABSORB1 and KPATH1 are the corresponding guards.

If a declared construction makes calls of positive scale \(\beta>0\) to an assumed \(N^K\) algorithm, the implementation retains a term

\[
\alpha+\beta K.
\]

In a finite dependency DAG, a semantic leaf contributes

\[
A_P+\Theta_P\beta_s K
\]

along a root-to-leaf path \(P\).

Therefore a favorable optional contraction does not erase \(K\). Every K-dependent path must be dominated by a mandatory contracting cycle/edge or independently bounded construction.

This distinction remains valid in the META-LIFT setting.

---

## 3. Direct generic port to decoder-description length is impossible

LOCALITY-BOUNDARY3 proposed a generic description contraction

\[
K\mapsto\alpha K+\beta
\]

for descriptions of length

\[
L=(\log M)^K.
\]

That is too strong for arbitrary decoder descriptions.

### Theorem 3.1: GENERIC-DESCRIPTION-CONTRACTION-NOGO1

There is no semantics-preserving transformation that maps **every** \(L\)-bit decoder description to an equivalent description of length \(o(L)\) for a representation model capable of emitting arbitrary embedded constant strings.

### Proof

Consider descriptions that ignore the seed and contain an arbitrary \(L\)-bit payload \(u\). On the first \(L\) output coordinates the decoder emits exactly \(u\).

There are

\[
2^L
\]

pairwise distinct represented strings/functions.

Descriptions of length at most \(L^\alpha\), for any fixed \(\alpha<1\), number at most

\[
2^{L^\alpha+1}.
\]

For sufficiently large \(L\),

\[
2^{L^\alpha+1}<2^L.
\]

Therefore not every \(L\)-bit decoder can have an equivalent \(L^\alpha\)-bit decoder. \(\square\)

### Consequence

The old max-affine K-elimination algebra cannot simply be relabeled as a decoder-compression theorem.

A contraction would have to exploit special structure of the **particular uniform descriptions produced under the collapse assumption**.

---

## 4. The apparent \((\log M)^K\) description blowup is avoidable

The previous formulation expanded a hypothetical polynomial-time output-bit algorithm into a Boolean circuit.

If the succinct input/address length is \(m\), a time-\(m^K\) algorithm yields a circuit of size roughly

\[
m^{O(K)},
\]

which became the troublesome decoder-description bound

\[
(\log M)^K.
\]

This expansion is unnecessary.

Under a uniform-program representation, keep:

1. the fixed code of the output-bit algorithm \(A\);
2. the source succinct descriptor \(D\);
3. fixed formatting/length metadata.

The decoder description is then

\[
d_{A,D}
=
\langle A,D,\mathrm{meta}\rangle.
\]

After choosing the represented target length so that

\[
\log M\ge C|D|
\]

for a fixed padding constant \(C\),

\[
\boxed{
|d_{A,D}|=O(\log M)
}
\]

independently of the runtime exponent \(K\).

The decoder computes the requested output bit by running \(A(D,i)\). It need not store an expanded \(m^K\)-size circuit.

Thus the unknown exponent moves from **description length** to the decoder's **clock/workspace allowance**.

This is a much better location for it.

---

## 5. Clocked uniform 2-local representations

Fix an integer \(c\ge1\).

Define a decoder class \(\mathcal D_c\) as follows.

A description \(d\) has length

\[
|d|\le \alpha\log M
\]

for a fixed \(\alpha<1\).

On output coordinate \(i\), the universal machine may perform at most

\[
(\log M)^c
\]

steps and use at most

\[
(\log M)^c
\]

writable cells before returning a depth-two adaptive decision tree over the representation seed.

The output still depends on at most two seed bits.

Let

\[
ULR2[c]
\]

be the corresponding range-membership/minimization language.

### Lemma 5.1: SUCCINCT-ULR2-CLOCK1

For every fixed \(c\),

\[
\boxed{
\operatorname{succ}(ULR2[c])\in PSPACE.
}
\]

### Proof sketch

A succinct target circuit has descriptor length \(m\), and

\[
\log M=\operatorname{poly}(m).
\]

The decoder description has polynomial length in \(m\). Its declared clock and workspace are

\[
(\log M)^c=\operatorname{poly}(m)
\]

for fixed \(c\).

After the decoder is simulated, every output constraint is still a Boolean relation on at most two seed variables. Range membership is therefore satisfiability of a succinctly represented 2-CNF.

Implication-graph reachability is decidable in polynomial space. \(\square\)

---

## 6. KPI diagonal hardness survives the clock

For fixed \(c\), there are still only

\[
2^{\alpha\log M}=M^\alpha
\]

candidate decoder descriptions.

For every description \(d\), simulate its clocked computation on a block coordinate and recover the two-probe local decision tree.

Then apply the KPI locality-two remote-point construction to the block restriction.

The diagonal block construction from UNIFORM-LOCAL-DIAG2 therefore extends verbatim.

### Theorem 6.1: CLOCKED-DIAG1

For every fixed \(c\) and suitable parameters, there is an explicit string

\[
H_{M,c}
\]

outside the range of every decoder in \(\mathcal D_c\) with seed length below the KPI threshold.

The number of decoder descriptions remains polynomial in \(M\).

Using the trace-moment streaming refinement from LOCALITY-BOUNDARY3, the construction uses

\[
(\log M)^{O(c+1)}
\]

workspace and quasipolynomial-or-larger time depending on the chosen direct simulator.

The precise time is not load-bearing here. The important point is that for every **fixed** \(c\), the hard family remains effective and its succinct membership language remains in PSPACE.

---

## 7. Exact cofinal absorption of the unknown exponent

This is the point where the earlier Cofinal charged hit idea transfers cleanly.

Suppose a single bit map

\[
B(D,i)
\]

is fixed independently of \(c\).

Under the counterfactual

\[
P=PSPACE,
\]

assume \(B\in PSPACE\). Then one deterministic polynomial-time machine \(A_B\) decides \(B\):

\[
T_{A_B}(n)\le n^K
\]

for some fixed but unknown finite \(K\).

Choose any fixed

\[
c>K.
\]

The short decoder

\[
d_D=\langle A_B,D\rangle
\]

has length \(O(\log M)\), and on coordinate \(i\) runs inside the \((\log M)^c\) clock after a fixed padding of the represented length.

Therefore the entire output string

\[
x_D[i]=B(D,i)
\]

has a zero-probe decoder in \(\mathcal D_c\).

### Theorem 7.1: COFINAL-CLOCK-ABSORB1

For a **c-independent** PSPACE bit map \(B\), the unknown polynomial exponent in the collapse

\[
P=PSPACE
\]

does not require a \((\log M)^K\)-bit decoder description.

A cofinal family of fixed clock classes

\[
\mathcal D_1,\mathcal D_2,\ldots
\]

absorbs the exponent: after the hypothetical polynomial algorithm \(A_B\) is selected, choose one finite \(c>K\).

No growing clock parameter is used inside one target instance, and no input-dependent advice is introduced.

### Relation to the old theorem

This is exactly the same logical move as Cofinal charged hit:

- the hypothetical algorithm is selected first;
- its finite exponent exists but need not be known by the algorithm;
- the meta-proof then selects one fixed member of a cofinal family;
- that member remains a single uniform complexity problem.

---

## 8. Important circularity: do not choose \(B=B_c\)

There is a subtle failure mode.

Suppose the bit language itself depends on the selected clock parameter:

\[
B_c(D,i).
\]

Under \(P=PSPACE\), each \(B_c\) has some polynomial-time exponent

\[
K(c).
\]

Cofinality alone does **not** imply that there is a \(c\) with

\[
c>K(c).
\]

For example, the exponents could satisfy

\[
K(c)=c+1.
\]

Therefore one cannot take the bit language to be “compute the c-clocked diagonal hard family \(H_{M,c}\)” and then argue that a sufficiently large \(c\) makes its own decoder fit.

That would be circular.

### Exact rule

The cofinal clock trick is valid only when the semantic/source bit map whose P algorithm supplies the decoder is fixed independently of the clock parameter.

---

## 9. Consequence: POLYLOG-DESCRIPTION-DIAG1 is no longer the main obstacle

LOCALITY-BOUNDARY3 identified

\[
(\log M)^K
\]

description length as the next obstacle.

The recovered K-elimination work changes that diagnosis.

For the collapse-generated **uniform** decoder, expanded circuit descriptions are optional. A short clocked program suffices.

Therefore:

\[
\boxed{
\text{unknown }K\text{ need not appear in description length.}
\]

The remaining issue is not generic description compression.

It is the construction of a **clock-independent semantic gating map**.

---

## 10. Revised load-bearing target

### CLOCK-INDEPENDENT-GATE1

Construct one deterministic source-to-target bit map

\[
B(D,i)
\]

with the following properties.

1. **Clock independence.**
   \(B\) is fixed before the clock exponent \(c\) is selected.

2. **Source semantics.**
   The represented target instance distinguishes the relevant source YES/NO cases without evaluating the source decision inside the reduction.

3. **PSPACE bit access.**
   \(B\in PSPACE\), with a fixed uniform machine independent of \(c\).

4. **Meta-complexity gap.**
   For every sufficiently large fixed \(c\), the source cases map to opposite sides of \(ULR2[c]\), or of another clocked self-succinct minimization problem.

5. **Weak construction.**
   The ordinary/succinct reduction obeys the output-size and workspace conditions needed by META-LIFT.

If CLOCK-INDEPENDENT-GATE1 is obtained, COFINAL-CLOCK-ABSORB1 removes the unknown P-time exponent automatically.

---

## 11. Why the aggregate recursive theorem is still useful

The clock trick handles a fixed c-independent bit map.

If a future gating construction contains genuinely recursive calls whose costs still carry a positive-scale unknown exponent, the old fixed-point machinery remains applicable.

For a recurrence

\[
K_{j+1}
\le
\max\{r,a+\lambda K_j\},
\qquad
\lambda<1,
\]

finite iteration gives

\[
K_j
\le
K_*+\lambda^j(K_0-K_*)_+,
\qquad
K_*=\max\left\{r,\frac{a}{1-\lambda}\right\}.
\]

But a strict hereditary contraction still has to be proved.

The present clock absorption should therefore be used **before** trying to invent a description contraction.

---

## 12. Literature cross-check

Two Ryan Williams results help calibrate the transfer boundary.

### Self-improvement for Circuit-SAT

Williams's STOC 2024 theorem genuinely contracts an exponent for Circuit-SAT circuit families. In the simplified theorem, one self-composition step changes

\[
2^{ak}
\]

to roughly

\[
2^{ak/2}
\]

while retaining near-linear dependence on circuit size.

This is a real self-improvement theorem, but it is specific to Circuit-SAT/#Circuit-SAT/quantified circuit analysis. It does not imply generic compression of arbitrary decoder descriptions.

### Time to square-root space

Williams's STOC 2025 theorem gives

\[
TIME[t]
\subseteq
SPACE[O(\sqrt{t\log t})].
\]

Applied once to a \((\log M)^K\)-time decoder, this reduces a space exponent roughly from \(K\) to \(K/2\).

It does not by itself give an iterative polynomial-time K-erasure: the resulting simulator is a space algorithm, not a new polynomial-time algorithm with the same quantitative exponent.

Thus neither external theorem replaces COFINAL-CLOCK-ABSORB1 or the missing gating theorem.

---

## 13. Current conclusion

The user's recollection was correct: the project had a genuine mechanism that eliminated an unknown \(K\).

The exact transfer is:

\[
\boxed{
\text{use cofinality for the uniform clock parameter;}
}
\]

do **not** try to compress arbitrary \((\log M)^K\)-bit decoder descriptions.

The old recursive fixed-point theorem remains valid but requires a strict hereditary shrinker, and a generic description shrinker is information-theoretically impossible.

The current META-LIFT spine should therefore be updated as follows:

\[
\boxed{
\text{retire POLYLOG-DESCRIPTION-DIAG1 as the primary target}
}
\]

and replace it with

\[
\boxed{
\textbf{CLOCK-INDEPENDENT-GATE1}.
}
\]

If the gating map is independent of the clock exponent, the unknown polynomial exponent supplied by \(P=PSPACE\) is no longer the central obstruction.

---

## References

1. PORTFOLIO-SHIELD-SAT, RECOVERY-STRENGTHEN7, 2026-10-08.
2. PORTFOLIO-SHIELD-SAT, FINAL-LINK-ARC, 2026-10-08.
3. PORTFOLIO-SHIELD-SAT, KABSORB1 and KPATH1, 2026-10-05.
4. R. Ryan Williams, *Self-Improvement for Circuit-Analysis Problems*, STOC 2024.
5. R. Ryan Williams, *Simulating Time With Square-Root Space*, STOC 2025.
6. Oliver Korten, Toniann Pitassi, Russell Impagliazzo, *Stronger Cell Probe Lower Bounds via Local PRGs*, FOCS 2025 / ECCC TR25-030.
7. PORTFOLIO-SHIELD-SAT, UNIFORM-LOCAL-DIAG2 and LOCALITY-BOUNDARY3, 2026-10-18.
