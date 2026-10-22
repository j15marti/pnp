# TSEITIN-EXPANDER-PAIR83 — matched YES/NO structure, full gadget cores, and a linear semantic bypass

**Role:** :48 synthesis  
**Timestamp:** 2026-10-23 07:48 KST  
**Global status:** P versus NP OPEN; P versus RP OPEN.

## Repairs fixed before source review

1. Replace the easy monotone expander control by two Tseitin charge formulas on the same bounded-degree expander: one YES and one NO.
2. Require the NO member to have no proper vertex-gadget UNSAT core.
3. Compare local separator failure with the fully charged global charge-parity scan that decides this restricted family.

Advance test: the construction is useful only if it simultaneously has matched unsigned incidence, exact proper-3CNF witness maps, all-gadget source coverage on the NO label, and a transparent deterministic semantic bypass.

## Sources actually reviewed

1. `research/main/2026-10-23_0648_MAIN_EXPANDER_RESIDUAL_SIZE82.md` and independent review commit `86716f1`;
2. `research/main/2026-10-22_2348_MAIN_MINIMAL_CORE_SOURCE_COVERAGE75.md`.

The new result combines the residual-size hostile control of 82 with the full-source-core firewall of 75, while adding a matched YES/NO representation and an explicit source-aware escape.

## Construction

Let (G=(V,E)) be a connected cubic graph. Associate one Boolean variable (x_e) with every edge. For a charge vector (b\in\{0,1\}^V), define
[
\Phi(G,b)=
\bigwedge_{v\in V}
\left[
\bigoplus_{e\ni v}x_e=b_v
\right].
]

Each degree-three parity equation is encoded by the four proper 3-CNF clauses that forbid the four local assignments of the wrong parity. Call those four clauses the vertex gadget (B_v).

For fixed (G), every charge vector has exactly the same unsigned clause-variable incidence graph: only literal signs inside (B_v) change. The explicit source length is (N=\Theta(|V|\log|V|)).

## Lemma 83A — exact label by global charge parity

For connected (G),
[
\Phi(G,b)\text{ is SAT}
\iff
\bigoplus_{v\in V} b_v=0.
]

**Proof.** XORing all vertex equations cancels every edge variable twice, proving necessity. The vertex-edge incidence matrix of a connected graph over (\mathbb F_2) has rank (|V|-1), and its column space is exactly the even-parity subspace. Thus every even charge vector has an edge assignment. □

The proper-3CNF encoding is parsimonious with respect to the edge variables: a local assignment satisfies all four clauses of (B_v) exactly when it satisfies the parity equation.

**Status: ESTABLISHED.**

## Lemma 83B — the odd instance is block-minimally UNSAT

The only linear dependency among the vertex incidence rows of a connected graph is the XOR of all rows. Consequently every proper subset of vertex rows is independent.

If (\bigoplus_v b_v=1), the full formula is UNSAT by Lemma 83A, but deleting any one vertex gadget (B_v) leaves a satisfiable parity system. More generally, every proper subset of full vertex gadgets is satisfiable for every right-hand side.

Therefore every CNF UNSAT core must contain at least one clause from every vertex gadget: if it omitted all four clauses of some (B_v), it would be a subset of a satisfiable proper-gadget formula.

**Status: ESTABLISHED block-source coverage.**

This does not say that every individual clause is necessary, nor does it lower-bound arbitrary proof systems or algorithms.

## Lemma 83C — small edge-variable cuts retain a giant residual branch

Assume (G) has edge expansion (h>0):
[
|\delta(S)|\ge h|S|
\quad
\text{for every }|S|\le|V|/2.
]

Let (X\subset E) contain (k) cut variables. A vertex is saturated if all three incident edges lie in (X). Because every proper subset of vertex rows is independent, there exists an assignment to (X) satisfying all saturated vertex equations: their rows are supported entirely on (X) and have full row rank.

On that branch, saturated gadgets disappear as satisfied, while every unsaturated gadget simplifies to a parity constraint on its remaining incident edge variables. The residual constraint graph is (G-X), ignoring isolated satisfied vertices.

If
[
k<\frac{h|V|}{4},
]
then (G-X) contains a connected component with more than (|V|/2) vertices.

**Proof.** If every component had size at most (|V|/2), select a union (S) of components with (|V|/4\le|S|\le|V|/2). Every edge of (\delta(S)) must belong to (X), so (k\ge h|S|\ge h|V|/4), contradiction. □

The simplified parity gadgets in that component have constant-size CNF encodings and retain ordinary encoded length (\Omega(N)). Thus a cut of (O(\log N)) edge variables has, on both even and odd charge vectors, at least one non-closing branch whose residual exceeds (N^\beta) for every fixed (\beta<1).

**Status: ESTABLISHED for syntax-local restriction under the edge-expansion hypothesis.**

## Lemma 83D — exact semantic bypass

For this recognized source family, a deterministic algorithm can parse one charge bit per vertex gadget, XOR the charges, and decide SAT in (O(N)) time and logarithmic auxiliary space.

This source scan is an exact both-label semantic contraction to one bit:
[
b\mapsto\bigoplus_v b_v.
]

**Status: ESTABLISHED restricted deterministic bypass.**

It is not an all-input SAT transformer. Recognizing that an arbitrary CNF is a valid member of this canonical family, locating the gadgets, and reading their signs are source operations and must be charged.

## Three-way firewall

TSEITIN-EXPANDER-PAIR83 separates three claims that must not be conflated:

1. **Structural locality fails:** logarithmic syntax cuts leave a linear-size residual branch.
2. **Small source cores fail on NO:** every vertex gadget must be represented in any source-subset contradiction.
3. **Semantic decision succeeds:** one global parity checksum decides the restricted paired family in linear time.

Therefore neither residual size nor full-source core coverage implies language hardness. Conversely, the semantic bypass demonstrates the precise kind of nonlocal, source-aware invariant an arbitrary-input ARC contractor would need—without supplying one for general SAT.

## Circuit-SAT and witness-map audit

A Circuit-SAT implementation can share the XOR subcircuits, but every shared primary edge variable must remain common across adjacent vertex gadgets. Functional Tseitin gate traces preserve the edge assignment; independently sampled gadget witnesses would destroy the global parity relation.

Gate inspection can recover the charge checksum on this canonical family. That is a charged source-aware algorithm, not a generic separator or RP theorem. DIGEST-LUMP19 and CLAUSE-COHERENCE20 remain active.

## Ordinary-MKTP audit

Choose, for example, the all-zero even charge and a single-one odd charge on a uniformly generated expander. Both paired formulas have short indexed generators. Their large residuals and all-gadget NO cores therefore remain ordinary-KT LOW controls.

**SAT-to-ordinary-MKTP HIGH status: OPEN.**

No HIGH conclusion follows from expander geometry, proof materialization, or label pairing.

## P/RP audit

The paired language is deterministically decidable by the charge checksum and cannot witness an RP language outside P. SOURCE-CHANNEL21 must count the scan that extracts every charge bit. A later digest cannot retroactively make those observations free.

The example is useful to P=RP work only as a representation-invariance control: a valid derandomizer should survive equivalent gate reorderings, while its source parser must still identify the same semantic checksum. No uniform simulation of arbitrary RP machines follows.

**P=RP and P!=RP remain OPEN.**

## Finite audit

The executable audit checked:

- exact four-clause proper-3CNF encoding of every degree-three parity gadget;
- rank (|V|-1) of connected graph incidence matrices;
- independence after deletion of every vertex row;
- SAT iff total charge parity is even;
- satisfiability after deleting any vertex equation from odd-charge instances;
- direct brute-force edge assignments on small graphs;
- 100,000 small edge-cut residual tests on connected cubic bipartite graphs.

Result: **101,507 assertions, 246,966 brute-force assignments, zero failures**. The minimum observed largest residual component fraction was (0.984375). These finite checks validate the implementation; the asymptotic residual lemma uses the stated edge-expansion hypothesis.

## Route ledger and next tests

- **:00 SAT-to-ordinary-MKTP — OPEN.** Calculate an explicit ordinary-KT upper bound for both canonical charge labels, including indexed clause generation time.
- **:12 P!=RP — OPEN.** Apply SOURCE-CHANNEL21 to a verifier that reads the charge gadgets and record the linear deterministic checksum as the mandatory bypass control.
- **:24 ARC/FLMV — local cuts/core extraction RETIRED generically; semantic transformer OPEN.** Generalize the one-bit charge checksum to a source-checkable semantic summary for a non-affine SAT family, or expose where summary verification rereads the full parent.
- **:36 P=RP — OPEN.** Test whether a proposed affine-fiber certificate finds the charge checksum under gadget permutation, gate reordering, and dummy coins.
- **:48 synthesis — Lemmas 83A-D ESTABLISHED restricted.** Search for a paired family whose exact semantic summary is not already computable by a linear algebra/source scan, while retaining matched incidence and no small gadget core.

## Bottom line

The paired Tseitin-expander family closes the easy-polarity weakness of the monotone hostile control: YES and NO instances have identical unsigned proper-3CNF structure, the NO label requires every vertex gadget, and logarithmic cuts retain a linear residual branch. Yet a linear global parity scan decides the family. This sharply identifies the missing ARC ingredient as an all-input semantic invariant, not a larger separator or proof core. It supplies no class separation. P versus NP and P versus RP remain OPEN.
