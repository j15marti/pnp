# DATA-DIRECTSUM1: Cell Sampling, Explicit Local Hardness, and the Succinctness Barrier

**Status:** Substantive intermediate progress. One exact global-cell lemma and one exact block corollary are proved. Current data-structure lower bounds provide a stronger unconditional hard-object source for constant-probe representations, but they do not yet close META-LIFT because the corresponding succinct minimization problem carries exponentially long witnesses.

**Date:** 2026-10-18

## 1. Objective

PCP-GATE1 isolated the missing property as a resource-bounded global-knowledge/direct-sum theorem:

\[
\text{short representation}
\Longrightarrow
\text{one small fixed set that resolves many queries/functions}.
\]

The static and dynamic data-structure literature is a natural place to search because cell-sampling lower bounds explicitly convert small query time into a small **single global set of memory cells** resolving many queries.

This note determines exactly what that machinery gives and where it stops.

---

## 2. Exact cell-sampling lemma for a fixed representation

Let \(D\) be a fixed table of \(S\) memory cells. Let a deterministic query algorithm answer queries from a finite set \(Q\), probing at most \(t\) cells of \(D\) on every query.

Because \(D\) is fixed, even an adaptive algorithm follows one definite probe path on every query \(q\). Let

\[
P(q)\subseteq[S],
\qquad |P(q)|\le t,
\]

be the set of cells actually probed.

A cell set \(C\subseteq[S]\) **resolves** \(q\) if

\[
P(q)\subseteq C.
\]

### Lemma 2.1: GLOBAL-CELL1

For every integer \(\Delta\ge t\), there exists a set \(C\subseteq[S]\), \(|C|=\Delta\), resolving at least

\[
|Q|\,
\left(
\frac{\Delta-t+1}{S}
\right)^t
\]

queries.

In particular, if \(\Delta\ge 2t\),

\[
\boxed{
|Q(C)|
\ge
|Q|
\left(\frac{\Delta}{2S}\right)^t.
}
\]

### Proof

Choose \(C\) uniformly among all \(\Delta\)-subsets of \([S]\).

For a fixed query with \(r=|P(q)|\le t\),

\[
\Pr[P(q)\subseteq C]
=
\frac{\binom{S-r}{\Delta-r}}{\binom{S}{\Delta}}
=
\prod_{j=0}^{r-1}
\frac{\Delta-j}{S-j}.
\]

Since \(r\le t\),

\[
\Pr[P(q)\subseteq C]
\ge
\left(
\frac{\Delta-t+1}{S}
\right)^t.
\]

Summing indicators over \(q\in Q\) and using linearity of expectation gives the first claim. If \(\Delta\ge2t\), then \(\Delta-t+1\ge\Delta/2\). \(\square\)

### Interpretation

This is exactly the global-set phenomenon we wanted at the **query level**:

\[
\boxed{
\text{few probes}
\Longrightarrow
\text{one fixed cell set resolving many different queries}.
}
\]

It is the basic mechanism behind modern cell-sampling lower bounds.

---

## 3. Exact block version and the complete-function decay

Partition the query set into \(k\) blocks

\[
Q=Q_1\sqcup\cdots\sqcup Q_k,
\]

where each block has at most \(h\) queries.

Say \(C\) **fully resolves block \(i\)** if it resolves every query in \(Q_i\).

For block \(i\), the union of all cells touched by its queries has size at most

\[
th.
\]

### Corollary 3.1: GLOBAL-BLOCK1

For every \(\Delta\ge th\), there exists \(C\subseteq[S]\), \(|C|=\Delta\), fully resolving at least

\[
k
\left(
\frac{\Delta-th+1}{S}
\right)^{th}
\]

blocks.

If \(\Delta\ge2th\),

\[
\boxed{
\#\{\text{fully resolved blocks}\}
\ge
k
\left(\frac{\Delta}{2S}\right)^{th}.
}
\]

### Consequence

Taking \(\Delta=S/2\) gives only roughly

\[
k\,4^{-th}
\]

fully resolved blocks.

Thus generic cell sampling converts a small probe bound into a useful global set only when the number of query points per complete object is also small.

If each \(f_i\) is a Boolean function on \(r\) input bits, then

\[
h=2^r.
\]

For polynomially many blocks \(k=N^{O(1)}\) and constant \(t\), the bound can guarantee even one fully resolved \(f_i\) only while approximately

\[
2^r=O(\log N),
\qquad
r=O(\log\log N).
\]

This is far below the domain sizes used by the random-function/direct-sum mechanisms in Partial-MCSP hardness.

### Conclusion

\[
\boxed{
\text{cell sampling gives the desired global set for query points,}
}
\]

but a generic conversion to a global set of **entire functions** incurs an exponential \(th\) loss.

That is the precise form of the obstacle identified qualitatively in PCP-GATE1.

---

## 4. This limitation is not just an artifact of our proof

The direct-product literature for data structures is problem-specific.

Generic strong direct-product theorems are known in communication complexity under suitable measures, but there is no comparable black-box theorem that turns an arbitrary cell-probe lower bound into a strong direct product for many correlated queries.

Existing data-structure direct-sum/direct-product theorems exploit special structure, such as partial match, nearest neighbor, orthogonal range counting, or related communication problems.

Therefore RESOURCE-DIRECTSUM1 cannot currently be discharged by citing a generic cell-probe theorem.

---

## 5. Stronger 2025 static lower bounds materially improve the hard-object side

Korten, Pitassi, and Impagliazzo (ECCC TR25-030, revised May 2025) prove state-of-the-art unconditional static cell-probe lower bounds.

For explicit problems \(F:[N]\times[M]\to\{0,1\}\) supporting suitable limited-independence distributions, they obtain, for even constant probe complexity \(t\),

\[
S
\ge
\widetilde{\Omega}\!\left(
N^{2/t}
(\log M)^{1-2/t}
2^{-O(w)}
\right).
\]

For nonadaptive bit-probe schemes and odd constant \(t>1\), they construct explicit problems with

\[
M\le\operatorname{poly}(N)
\]

and

\[
\boxed{
S\ge N^{2/t+\varepsilon_t}
}
\]

for a constant \(\varepsilon_t>0\).

This is qualitatively stronger for our purposes than the Tourlakis truth-table gap:

- target strings may have polynomial length;
- the representation lower bound is itself polynomial in that length;
- a source witness of polynomial size can now fit below the hardness threshold after polynomial parameter padding.

So the earlier **polylog-gap versus polynomial-witness** obstruction is not inherent to all resource-bounded representation measures.

---

## 6. Range avoidance gives an explicit hard-string mechanism

A particularly useful observation in Korten-Pitassi-Impagliazzo is the equivalence between nonadaptive bit-probe data structures and local generators.

If

\[
G:\{0,1\}^{S}\to\{0,1\}^{N}
\]

has every output computable from at most \(t\) seed bits, then \(G\) is an \(NC^0_t\)-type local generator.

A data-structure lower bound is equivalent to saying that an explicit list of columns contains a string outside the range of every such generator.

More strongly, their Theorem 4 gives a deterministic algorithm for **remote-point range avoidance**. For even \(t\), word size \(w\), and suitable stretch, given any time-\(t\) locally computable generator

\[
G:[2^w]^S\to\{0,1\}^m,
\]

the algorithm outputs a string \(h\in\{0,1\}^m\) satisfying

\[
\boxed{
\operatorname{dist}(h,\operatorname{range}(G))
\ge
(1/2-\varepsilon)m.
}
\]

The running time is

\[
m^{O(t^2w)}
\]

for the stated parameter regime.

### Potential project use

Fix a universal bounded-probe decoder \(U\). Its seed contains the candidate description. For each output coordinate, \(U\) performs at most \(t\) probes into that description.

Then \(U\) is itself a locally computable generator:

\[
U:\{0,1\}^S\to\{0,1\}^m.
\]

Applying the remote-point theorem gives a deterministic string

\[
h_{S,m}
\]

that is not merely outside every \(S\)-bit \(t\)-probe representation, but at constant relative Hamming distance from all of them.

Thus the data-structure literature supplies a much stronger candidate hard object than the polynomial-advice SAT truth table:

\[
\boxed{
\text{explicit, polynomial-scale, approximate local-representation hardness.}
}
\]

### Uniformity caveat

The cited theorem gives a polynomial-time algorithm. The paper does not state the polylogarithmic-workspace bound required by META-LIFT.

The construction uses:

- a polynomial-size almost-\(k\)-wise candidate list,
- transformations of local decision trees into XOR/CSP and matrix objects,
- spectral tests to select a passing candidate.

Several of these subroutines have highly parallel linear-algebraic implementations, so a polylog-space implementation is plausible for fixed \(t,w,\varepsilon\), but this has **not** been proved here.

This is a concrete LOCAL-META subproblem.

---

## 7. New 2026 dynamic result confirms the global-information phenomenon

Young Kun Ko (ECCC TR26-047, revised October 7, 2026) proves

\[
\Omega\!\left(
\left(\frac{\log n}{\log\log n}\right)^2
\right)
\]

cell-probe lower bounds for the Boolean Multiphase Problem instantiated with inner product over \(\mathbb F_2\).

This closes the previous \(\widetilde{\Omega}(\log^{1.5}n)\) barrier for Boolean dynamic problems.

The result is relevant because the Multiphase Problem explicitly separates:

1. a preprocessing/global-information phase,
2. a small update or semantic change,
3. a later indexed query.

That architecture resembles the project's source-state / selector / continuation models.

However, the lower bound remains polylogarithmic in query probes. It does not by itself provide the polynomial-scale representation/direct-sum gap needed for META-LIFT.

Its current role is therefore **diagnostic and adversarial**, especially against proposals that claim a tiny dynamic update can expose globally preprocessed information at negligible cost.

---

## 8. A stronger obstruction appears: hard scale versus succinct witness scale

The Korten-Pitassi-Impagliazzo hard object solves one side of the Gating Triangle, but creates a new issue.

Consider a representation target

\[
MINREP_t(y,S)
=
\left[
\exists d\in\{0,1\}^{S}:
U_t(d)=y
\right]
\]

for an explicit \(m\)-bit string \(y\).

If the useful lower-bound regime has

\[
S=m^\alpha
\]

for constant \(\alpha>0\), then on a succinctly represented string of length

\[
m=2^r,
\]

the candidate description has length

\[
S=2^{\alpha r}.
\]

The straightforward witness is therefore exponentially long in the succinct descriptor size.

This destroys the small-certificate proof that gave

\[
\operatorname{succ}(LOW_{a,b,\delta})\in\Sigma_2^P.
\]

### Proposition 8.1: SUCCINCT-WITNESS-SCALE1

Polynomial-scale description hardness for explicit \(m\)-bit strings becomes exponential witness length after one level of succinct encoding.

Therefore a local-representation minimization problem does **not** inherit the low-succinct-complexity property merely because its explicit representation verifier is local.

This is not a proof that the succinct target lies outside PSPACE. It is an exact obstruction to the standard \(\exists\)-small-description / \(\forall\)-query PH upper bound.

---

## 9. For expressive local range membership, the succinct version reaches NEXP scale

The preceding scale problem is real rather than cosmetic.

Succinct 3SAT is NEXP-complete. An exponentially long satisfying assignment is exactly an exponentially long seed for a local constraint verifier.

A local generator can encode clause satisfaction using a constant number of word probes per clause: seed cells encode assignment bits/words and each output checks one local constraint.

Thus sufficiently expressive **succinct local-range membership** naturally contains succinct CSP/SAT behavior.

The ordinary target can be NP-like, while one level of succinct encoding rises to NEXP.

This is the wrong direction for META-LIFT, whose key requirement is:

\[
\operatorname{succ}(M)\in PSPACE
\]

or preferably \(PH\).

So the static data-structure route creates a new version of the same Gating Triangle:

| Property | Constant-probe local representation |
|---|---|
| polynomial-output explicit hard object | **yes** |
| polynomial-scale unconditional lower bound | **yes** |
| deterministic remote point | **yes, polynomial time** |
| low succinct version via small witness | **no** |
| source semantic gating | **still open** |

---

## 10. Why simply concatenating a list of hard candidates does not solve selection

Cell-probe lower bounds and range-avoidance algorithms often produce a polynomial-size list in which at least one string is hard.

One might try to concatenate all candidates.

This does not automatically preserve the lower bound.

A data-structure representation for one column receives the database identity only through its stored representation. A program computing a concatenation receives the block index as part of its query address for free.

Thus a program can use the block index to select different behavior, while the original data-structure lower bound does not give that identity freely to the query algorithm.

Therefore:

\[
\boxed{
\text{hard-list}
\not\Rightarrow
\text{hard concatenation}
}
\]

without an additional index-hiding or direct-sum theorem.

This is another exact place where RESOURCE-DIRECTSUM1 remains load-bearing.

---

## 11. New highest-value intermediate theorem

The most useful theorem to pursue is no longer a completely generic direct product.

It is the following hybrid.

### INDEX-HIDDEN-DIRECTSUM1

Construct an explicit family

\[
\{h_j\}_{j\in[k]}
\]

and an encoding

\[
H
\]

with polynomial total length such that:

1. every query to \(H\) can be generated in polylogarithmic workspace;
2. a short representation of \(H\) cannot exploit a freely supplied block identity to simulate unrelated representations of each \(h_j\);
3. from any short representation of \(H\), cell sampling extracts one small fixed cell set resolving enough complete blocks to violate a known static data-structure/range-avoidance lower bound;
4. the corresponding minimization target retains a succinct version in PSPACE.

The key new ingredient is **index hiding**. Ordinary concatenation fails property 2.

Possible mechanisms to test include:

- expander mixing of block coordinates,
- locally decodable / locally testable encodings of block identity,
- secret-sharing of the block selector,
- cross-block parity checks,
- tensor/direct-product codes whose local views overlap.

Every candidate must be audited against an adaptive program that computes a different address set for each query.

---

## 12. Current conclusion

The data-structure/direct-product search produced real progress.

### What is now proved

\[
\boxed{
\text{few probes}
\Rightarrow
\text{one fixed small cell set resolving many queries}
}
\]

with an exact quantitative bound.

### What current literature adds

The 2025 Korten-Pitassi-Impagliazzo results provide explicit polynomial-scale local-representation lower bounds and deterministic remote-point constructions, much stronger in scale than the Tourlakis-based hard table.

The 2026 Ko result strengthens the dynamic Boolean lower-bound side and is especially relevant to adaptive selector models.

### What remains

Generic cell sampling loses exponentially when "knowing one object" means answering an entire large block of queries.

And once the hard representation threshold is polynomial in explicit string length, its succinct version naturally carries an exponentially long existential representation.

So the problem has shifted from:

\[
\text{“Can data structures give a global-set theorem?”}
\]

to the sharper pair:

\[
\boxed{
\text{Can we hide the block/index strongly enough to obtain a complete-object direct sum?}
}
\]

and

\[
\boxed{
\text{Can we do so while retaining a PSPACE/PH succinct target?}
}
\]

These are now the two load-bearing questions.

---

## References

1. Anna Gál and Peter Bro Miltersen, *The Cell Probe Complexity of Succinct Data Structures*, TCS 2007.
2. Kasper Green Larsen, *Higher Cell Probe Lower Bounds for Evaluating Polynomials*, FOCS 2012.
3. Mihai Pătraşcu and Mikkel Thorup, *Unifying the Landscape of Cell-Probe Lower Bounds*, SICOMP 2011.
4. Yitong Yin, *Simple Average-Case Lower Bounds for Approximate Near-Neighbor from Isoperimetric Inequalities*, ICALP 2016.
5. Oliver Korten, Toniann Pitassi, Russell Impagliazzo, *Stronger Cell Probe Lower Bounds via Local PRGs*, ECCC TR25-030, revised 2025.
6. Young Kun Ko, *An \(\Omega((\log n/\log\log n)^2)\) Cell-Probe Lower Bound for Dynamic Boolean Data Structures*, ECCC TR26-047, revised October 7, 2026.
7. Christos H. Papadimitriou and Mihalis Yannakakis, *A Note on Succinct Representations of Graphs*, Information and Control 71(3), 1986.
8. PORTFOLIO-SHIELD-SAT project: PCP-GATE1, ADVICE-HIERARCHY1, INDEXCUT43, ADDRESSSEM44, CLOCKCOMPRESS32.
