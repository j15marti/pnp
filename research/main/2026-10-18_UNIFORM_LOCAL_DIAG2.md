# UNIFORM-LOCAL-DIAG2: Diagonal Remote Points and the 2-Local NL/PSPACE Boundary

**Status:** New exact construction and complexity boundary. This gives an unconditional polynomial-scale lower bound against a uniform local representation class while preserving PSPACE succinct membership. It does not supply the missing P-hard gating reduction.

**Date:** 2026-10-18

## 1. Motivation

DATA-DIRECTSUM1 identified a tension:

- constant-probe/local representations admit strong unconditional lower bounds;
- polynomial-scale representation witnesses become exponentially long after succinctification.

There is one important exception: **Boolean 2-local range membership**. Even when the seed is exponentially long relative to the succinct descriptor, range membership is a 2-CSP and can be handled through succinct graph reachability in PSPACE.

This note combines that observation with the remote-point theorem of Korten-Pitassi-Impagliazzo (KPI) and a finite diagonalization over short decoder descriptions.

The result is a single explicit hard string, not merely a hard list.

---

## 2. Uniform 2-local generators

Fix a universal decoder \(U\).

A decoder description \(d\) and output coordinate \(i\) define a depth-2 decision tree over seed bits:

\[
U(d,i;z)\in\{0,1\},
\qquad
z\in\{0,1\}^{S}.
\]

The decoder may choose the second queried seed address adaptively after observing the first bit. Invalid/nonhalting descriptions are interpreted as a fixed trivial output rule after a declared timeout.

For fixed \(d,S,M\), define

\[
G_{d,S,M}(z)
=
\bigl(
U(d,1;z),\ldots,U(d,M;z)
\bigr).
\]

Every output coordinate depends on at most two seed bits, so \(G_{d,S,M}\) is a time-2 locally computable generator in the sense used by KPI.

The computational work needed to determine the two probe addresses is not counted by the local-generator lower bound itself. For the complexity classifications below we require the universal decoder to be simulable in \(O(\log M)\) writable workspace from \(d,i\).

---

## 3. KPI remote point specialized to locality two

KPI Theorem 4 applies to even locality \(t\). For \(t=2\), word size \(w=1\), and fixed constant \(\varepsilon>0\), its stretch condition has the form

\[
m
\ge
C_\varepsilon\, S\log S
\]

up to the fixed lower-order factors in their theorem.

Under this condition, given any 2-local generator

\[
G:\{0,1\}^{S}\to\{0,1\}^{m},
\]

their deterministic polynomial-time algorithm outputs

\[
h\in\{0,1\}^{m}
\]

satisfying

\[
\operatorname{dist}
\bigl(h,\operatorname{range}(G)\bigr)
\ge
(1/2-\varepsilon)m.
\]

In particular,

\[
h\notin\operatorname{range}(G).
\]

No cryptographic assumption is used.

---

## 4. New theorem: diagonal remote point against every short uniform decoder

Choose a base block length \(m\) and constant \(c>0\). Set

\[
D=\lfloor c\log_2 m\rfloor,
\qquad
K=2^D\le m^c,
\qquad
M=Km.
\]

Enumerate all decoder descriptions

\[
d_1,\ldots,d_K\in\{0,1\}^{D}.
\]

Partition the final output coordinates \([M]\) into \(K\) consecutive blocks

\[
B_1,\ldots,B_K,
\qquad
|B_j|=m.
\]

For each \(j\), let

\[
G_j
=
G_{d_j,S,M}\big|_{B_j}
:
\{0,1\}^{S}\to\{0,1\}^{m}
\]

be the restriction of the full \(M\)-output generator described by \(d_j\) to its own diagonal block.

Assume

\[
m\ge C_\varepsilon S\log S.
\]

Apply the KPI remote-point algorithm to \(G_j\) and obtain

\[
h_j
\in
\{0,1\}^{m}
\]

with

\[
h_j\notin\operatorname{range}(G_j).
\]

Define

\[
H
=
h_1\Vert h_2\Vert\cdots\Vert h_K
\in\{0,1\}^{M}.
\]

### Theorem 4.1: UNIFORM-DIAG1

For every description \(d\in\{0,1\}^{D}\),

\[
\boxed{
H\notin\operatorname{range}(G_{d,S,M}).
}
\]

### Proof

Let \(d=d_j\).

Suppose toward contradiction that for some seed \(z\),

\[
G_{d_j,S,M}(z)=H.
\]

Restrict both sides to block \(B_j\). Then

\[
G_j(z)=h_j.
\]

But \(h_j\) was constructed outside \(\operatorname{range}(G_j)\), contradiction. \(\square\)

### Quantitative form

Since

\[
M=Km\le m^{c+1},
\]

the excluded seed length can be almost

\[
S
=
\widetilde{\Theta}(m)
=
\widetilde{\Theta}
\bigl(
M^{1/(c+1)}
\bigr)
\]

for locality two.

Meanwhile

\[
D
=
\frac{c}{c+1}\log_2 M+O(1).
\]

Thus we obtain an explicit family \(H_M\) with a polynomial representation lower bound against every 2-local generator whose **uniform decoder description has only \(O(\log M)\) bits**.

This is stronger in scale than the Tourlakis-derived \(\operatorname{polylog}M\) hard-description gap, but it applies to a restricted local representation class.

---

## 5. Explicitness

There are only

\[
K\le m^c
\]

decoder descriptions.

For each description, materialize its block-restricted local generator and run the KPI polynomial-time remote-point algorithm.

Because

\[
M=Km
\]

and \(c\) is fixed, the complete string \(H\) is deterministically constructible in time polynomial in \(M\).

This establishes ordinary explicitness.

### Open strengthening: polylog-space explicitness

KPI select the remote point from a polynomial-size Naor-Naor limited-independence list using a constant number of spectral tests. Their proof controls these tests through \(k=O(\log m)\) trace moments.

There is a plausible polylog-space implementation:

1. enumerate candidate-list entries from their short seeds;
2. regenerate the relevant XOR schemes and matrix entries on demand;
3. replace eigenvalue storage by direct enumeration of closed walks contributing to
   \[
   \operatorname{tr}
   \bigl((B^\top B)^{k/2}\bigr);
   \]
4. use \(O(\log^2 m)\)-bit fixed-point arithmetic.

For the normalized matrices in KPI, the closed-walk products have rational denominators after the square-root normalizations cancel around each closed walk.

This strongly suggests an

\[
\log^{O(1)}m
\]

workspace implementation with quasipolynomial time, but the complete threshold/gap arithmetic has not yet been audited. It remains **OPEN** and should not be treated as proved.

---

## 6. The associated minimization language

Define

\[
\mathrm{ULR2}_{c}
=
\left\{
(x,S):
\begin{array}{l}
|x|=M,\ \exists d,\ |d|\le D(M),\\
\exists z\in\{0,1\}^{S},\
G_{d,S,M}(z)=x
\end{array}
\right\},
\]

where

\[
D(M)=\lfloor \alpha\log M\rfloor
\]

for fixed \(\alpha<1\).

The diagonal family from Theorem 4.1 gives explicit NO instances with

\[
S
=
\widetilde{\Omega}
\bigl(
M^{\beta}
\bigr)
\]

for a fixed \(\beta>0\) determined by \(\alpha\).

---

## 7. New theorem: explicit ULR2 is in NL

Fix \(x,S,d\).

Every equality

\[
U(d,i;z)=x_i
\]

is a Boolean relation on at most two seed bits.

Any Boolean relation on two variables is expressible as a conjunction of at most four 2-CNF clauses: for each forbidden assignment, add the clause excluding exactly that assignment.

Therefore

\[
G_{d,S,M}(z)=x
\]

is equivalent to satisfiability of a 2-CNF formula

\[
\Phi_{d,x}
\]

over the \(S\) seed variables.

The clauses of \(\Phi_{d,x}\) are logspace-generable from \(d,i,x_i\).

Because

\[
|d|=O(\log M),
\]

an NL machine can:

1. guess \(d\);
2. run the standard NL/coNL 2-SAT / implication-graph test for \(\Phi_{d,x}\).

Hence

\[
\boxed{
\mathrm{ULR2}_{c}\in NL.
}
\]

This is an exact upper bound for the declared decoder model.

---

## 8. New theorem: the succinct version is in PSPACE

Now let \(x\) be represented by a Boolean circuit

\[
X(i)=x_i.
\]

The explicit seed length \(S\) and output length \(M\) may be exponential in the succinct descriptor length.

For a guessed decoder description \(d\), the range-membership condition is still a 2-CNF over \(S\) variables, but its clauses are represented succinctly.

Its implication graph has \(2S\) vertices. Given two implication-graph vertices, whether the corresponding edge exists can be decided in polynomial space by generating the relevant constraint index and evaluating \(X\) and the decoder.

Reachability in an exponentially large graph given by a circuit is in PSPACE by the standard succinct-reachability / Savitch argument.

Therefore:

\[
\boxed{
\operatorname{succ}(\mathrm{ULR2}_{c})
\in PSPACE.
}
\]

The exponentially long seed does **not** force an NEXP upper bound here because Boolean binary constraints reduce to succinct graph reachability rather than arbitrary succinct SAT.

This is the key exception to the witness-scale obstruction in DATA-DIRECTSUM1.

---

## 9. The locality-two boundary

The preceding construction lands exactly at the classical complexity jump

\[
NL
\longrightarrow
PSPACE
\]

under succinct representation.

This is not accidental.

For locality two over Boolean seed cells, range membership is 2-CSP / 2-SAT-like.

Once arbitrary 3-local Boolean constraints are allowed, fixed-generator range membership has the expressive power of 3-CSP, and one level of succinct representation naturally reaches nondeterministic exponential-time behavior.

Thus the local-generator route exhibits a sharp version of the Gating Triangle:

\[
\boxed{
\begin{array}{c}
t=2:\\
\text{strong explicit local lower bounds}\\
+\text{ succinct PSPACE upper bound}\\
+\text{ explicit problem only NL-like}
\end{array}
}
\]

versus

\[
\boxed{
\begin{array}{c}
t\ge3:\\
\text{much richer explicit gating}\\
+\text{ succinct witness complexity rises sharply.}
\end{array}
}
\]

No claim is made here that every \(t\ge3\) minimization variant is NEXP-complete; the point is that the fixed-generator range-membership core already contains the usual succinct-CSP obstacle.

---

## 10. Consequence for META-LIFT

UNIFORM-DIAG1 now supplies two corners of the desired triangle for a single natural minimization measure:

### Hard side

There are deterministic explicit strings requiring polynomial seed length against all \(O(\log M)\)-description uniform 2-local generators.

### Succinct side

The associated succinct minimization problem lies in PSPACE.

### Missing side

The explicit language lies in NL.

Therefore proving it P-hard under logspace reductions would imply

\[
P=NL,
\]

and proving the stronger polylog-space P-hardness needed by the generalized META-LIFT theorem would itself be separation-strength progress.

So the remaining problem is no longer the absence of a hard object or the exponential witness problem.

It is precisely:

\[
\boxed{
\text{raise the explicit gating power from NL-like to P-hard}
}
\]

without raising the succinct problem beyond PSPACE.

That is a substantially sharper target.

---

## 11. Why the earlier hard-list issue needs a refinement

KPI's list-solution correspondence should be interpreted carefully.

A polynomial candidate list

\[
h_1,\ldots,h_K
\]

guarantees that for each **single** local generator \(G\), at least one candidate is outside \(\operatorname{range}(G)\).

Naively concatenating the list does not yield a hard string against an arbitrary larger-output generator, because each block restriction can be a different generator.

UNIFORM-DIAG1 repairs exactly this problem by assigning the \(j\)-th block to the \(j\)-th candidate **decoder** and making that block remote from that decoder's own restriction.

The diagonalization works because there are only polynomially many \(O(\log M)\)-bit decoder descriptions.

---

## 12. New highest-value targets

### TARGET A: POLYLOG-REMOTE1

Close the workspace audit of the KPI remote-point algorithm.

Desired theorem:

\[
\text{KPI remote point for fixed }t,w
\text{ is computable in }
\log^{O(1)}m
\text{ workspace.}
\]

The trace-moment implementation is the leading route.

### TARGET B: NL-TO-P-GATE1

Find a representation mechanism that preserves the succinct-PSPACE recursion of 2-local range membership but whose explicit minimization problem is P-hard rather than NL-like.

This is difficult for a principled reason: standard succinct-representation theory sends P-complete problems toward EXP, while NL-complete reachability lands in PSPACE.

Any successful construction would have to exploit the meta-complexity/minimization structure in a non-generic way, as MCSP/MKTP do in the Allender-Holden-Kabanets framework.

### TARGET C: RECURSIVE-MIN1

Search for minimization measures with:

1. polynomial-scale unconditional representation lower bounds;
2. an optimality predicate admitting a Savitch-style recursive characterization, so exponentially large witnesses need not be materialized;
3. explicit P-hardness under weak reductions.

Decision-tree complexity is a useful control: its circuit-input version is PSPACE-complete, but truth-table minimization is too easy. OBDD and related branching-program measures should be audited under the same three criteria.

---

## 13. Current conclusion

The local-data-structure direction is not dead.

It now yields an exact new intermediate object:

\[
\boxed{
\text{explicit polynomial-scale hard family}
+
\text{succinct PSPACE membership}.
}
\]

The price is that the explicit minimization language sits in NL.

This identifies a very narrow complexity boundary to attack:

\[
\boxed{
NL\text{-like explicit range membership}
\quad\longrightarrow\quad
P\text{-hard explicit gating}
}
\]

while preserving the same succinct PSPACE recursion.

That is the cleanest formulation of the remaining META-LIFT problem found so far.

---

## References

1. Oliver Korten, Toniann Pitassi, Russell Impagliazzo, *Stronger Cell Probe Lower Bounds via Local PRGs*, FOCS 2025 / ECCC TR25-030.
2. Joseph Naor and Moni Naor, *Small-Bias Probability Spaces: Efficient Constructions and Applications*, STOC 1990 / SIAM J. Comput.
3. Christos Papadimitriou and Mihalis Yannakakis, *A Note on Succinct Representations of Graphs*, Information and Control 71(3), 1986.
4. Bruno Loff and Alexey Milovanov, *The Hardness of Decision Tree Complexity*, STACS 2025.
5. PORTFOLIO-SHIELD-SAT project: META-LIFT, ADVICE-HIERARCHY1, PCP-GATE1, DATA-DIRECTSUM1.
