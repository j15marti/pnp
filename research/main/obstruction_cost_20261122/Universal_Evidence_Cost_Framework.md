# Shortest obstructions and the cost of establishing incompatibility

Research date: 22 November 2026.

Status: exact elementary statements and a model-explicit framework. Every variable-removal level is a fresh static input. No compulsory resolution derivation, explicit branching, counting of completions, or post-preprocessing inference is imposed. The framework does not establish a superpolynomial lower bound.

The useful progress is an exact recursion for the whole family of source obstructions, an exact identification with positive certificates on a realizable Boolean input cube, and a resource ledger that allows arbitrary sound fusion and shared representations. These statements identify what the proposed lower bound still needs to prove.

## 1. The static object and its shortest obstruction

Let the source have labeled rows

\[
F=\bigwedge_{j\in[m]}C_j,
\]

and let \(\rho\) be the values supplied for some of its variables. These supplied values are part of the input. The other variables range over a fixed finite nonempty domain \(D\). For \(J\subseteq[m]\), write

\[
F_J=\bigwedge_{j\in J}C_j.
\]

Define the upward family of source obstructions and its inclusion-minimal members by

\[
\mathcal U_\rho
=\{J\subseteq[m]:F_J|_\rho\text{ is UNSAT}\},
\qquad
\mathcal M_\rho=\operatorname{Min}_{\subseteq}\mathcal U_\rho.
\]

The minimum source-core size is

\[
\mu(F,\rho)=\min\{|J|:J\in\mathcal U_\rho\},
\]

with value \(+\infty\) when the residual is satisfiable. The cardinality counts original row labels. It does not include the supplied-value fields, row addresses, or the computation needed to establish the contradiction. An inclusion-minimal core can be larger than a minimum-cardinality core.

The machine must be correct on both SAT and UNSAT residuals. Selecting a globally UNSAT source for the analyst's study does not give the machine a promise that every permitted source is UNSAT.

## 2. Exact release recursion, with every shared source row counted once

Suppose \(x\) is unknown under \(\rho\). For each \(v\in D\), let

\[
\rho_v=\rho\cup\{x=v\}.
\]

These are separate static restrictions. The following statements are semantic identities, not instructions for a solver to execute the branches.

### Theorem 1: obstruction-family recursion

\[
\boxed{\mathcal U_\rho=\bigcap_{v\in D}\mathcal U_{\rho_v}.}
\tag{1}
\]

If the parent residual is UNSAT, then

\[
\boxed{
\mathcal M_\rho
=\operatorname{Min}_{\subseteq}
\left\{\bigcup_{v\in D}K_v:
K_v\in\mathcal M_{\rho_v}\text{ for every }v\in D\right\}.
}
\tag{2}
\]

In particular,

\[
\boxed{
\mu(F,\rho)
=\min_{K_v\in\mathcal M_{\rho_v}}
\left|\bigcup_{v\in D}K_v\right|.
}
\tag{3}
\]

**Proof.** A row subset has no extension under \(\rho\) if and only if it has no extension for every possible value of \(x\), proving (1). Every union in (2) is therefore a parent obstruction.

For a parent-minimal obstruction \(K\), each finite family of rows \(K\) contains a slice-minimal obstruction \(K_v\subseteq K\). Their union is a parent obstruction contained in \(K\). Inclusion-minimality forces that union to equal \(K\). Conversely, if an inclusion-minimal union in (2) contained a proper parent obstruction \(L\), choosing slice-minimal cores inside \(L\) would produce a strictly smaller union in the same family. This is impossible. Equation (3) follows. QED.

Thus the exact recurrence for source support is a minimum over unions. A sum would overcount every row shared between slices. The immediate bounds are

\[
\max_{v\in D}\mu(F,\rho_v)
\le\mu(F,\rho)
\le\min\left\{m,\sum_{v\in D}\mu(F,\rho_v)\right\}.
\tag{4}
\]

Equation (2) retains all choices of slice-minimal core. Keeping only one shortest core from each slice can lose the best parent union: somewhat larger slice cores may overlap more strongly and yield a smaller union.

This failure occurs even in the following elementary 2-CNF control:

\[
F=(x\lor y)\land(x\lor\neg y)
\land(\neg x\lor z)\land(\neg x\lor\neg z)
\land u\land v\land(\neg u\lor\neg v).
\tag{4a}
\]

When \(x=0\), the unique minimum core is the first pair, which becomes \(y,\neg y\). When \(x=1\), the unique minimum core is the second pair, which becomes \(z,\neg z\). Both slice minima have size 2, and their union has size 4. However,

\[
H=\{u,v,\neg u\lor\neg v\}
\]

is an inclusion-minimal core in both slices and in the parent. The parent has no two-row core: the \(x,y,z\) component needs all four of its clauses, the separate \(u,v\) component needs all three of its clauses, and clauses from different components do not create a contradiction together. Consequently \(\mu(F)=3\). Even retaining every minimum-cardinality slice core would miss the optimal union here. This is a structural illustration in an easy formula class, not a computational hardness claim.

When there is one unknown, every fully specified slice is refuted by a single violated row. Equation (3) becomes the minimum number of rows whose forbidden values cover \(D\). With two unknowns it becomes a minimum union of one-unknown obstructions. This is an exact characterization of the shortest source obstruction; it does not require an implementation to enumerate the cover or execute these decompositions.

### Corollary: source-core size is monotone along nested releases

For a fixed source and nested restrictions \(\rho_{r+1}\subseteq\rho_r\),

\[
\boxed{\mu(F,\rho_r)\le\mu(F,\rho_{r+1}).}
\tag{5}
\]

Any row subset that is UNSAT with fewer values supplied is also UNSAT with more values supplied. Therefore \(\mathcal U_{\rho_{r+1}}\subseteq\mathcal U_{\rho_r}\), proving the result. This works with the extended value \(+\infty\); for a globally UNSAT source all the values are finite.

The families of inclusion-minimal cores themselves need not be nested. Equation (5) concerns source support, not running time, memory, proof-search cost, or the cost of an optimal implementation. No additive computational increment follows from (3), (4), or (5).

## 3. A realizable Boolean input cube for strict symmetric C5

This section specializes to the project's fixed strict symmetric C5 relation. Its domain is \(D=\{0,1,2,3,4\}\), and its satisfying triples are the permutations of

\[
012,\quad123,\quad234,\quad340,\quad401.
\]

All source clauses use three distinct variable names. This is the symmetric relation used in the one- and two-unknown analysis, not the ordered tournament relation in the compact-input construction.

After supplying all but \(r\) variable values, every nontrivial atomic residual has one of these forms:

| Residual type | Number |
|---|---:|
| An everywhere-false row | \(1\) |
| A unary support on a designated unknown | \(10r\) |
| \(C(x_i,x_j,a)\), for \(i<j\) and \(a\in D\) | \(5\binom r2\) |
| \(C(x_i,x_j,x_k)\), for \(i<j<k\) | \(\binom r3\) |

The ten unary supports are five singletons and five doubletons. A true residual row is omitted. Repeated occurrences of the same residual type do not change semantics. Thus there are

\[
M(r)=1+10r+5\binom r2+\binom r3
\tag{6}
\]

nontrivial atomic types. Regard each type \(R_j\) as a subset of \(D^r\), with unused coordinates unconstrained. Define

\[
\boxed{
U_r(z)=1
\iff
\bigcap_{j:z_j=1}R_j=\varnothing,
\qquad z\in\{0,1\}^{M(r)}.
}
\tag{7}
\]

This is a monotone Boolean function: adding constraints preserves UNSAT. It does not follow that a fastest circuit or machine computing it uses only monotone operations.

### Lemma 2: every mask has a genuine fixed-slot source realization

For each \(r\), there is a fixed source layout \(E_r(z)\) such that every \(z\in\{0,1\}^{M(r)}\) is realized, all rows have three distinct names, and

\[
E_r(z)|_\rho\text{ is UNSAT}\iff U_r(z)=1.
\tag{8}
\]

**Construction.** Use unknown names \(x_1,\ldots,x_r\), anchors \(a_0,\ldots,a_4\) supplied with values \(0,\ldots,4\), and a further distinct name \(b_0\) supplied with value \(0\). Include one record for each of the \(M(r)\) types. An active record contains the source clause for that type. An inactive record contains the fixed true clause \(C(a_0,a_1,a_2)\).

The false type is represented by \(C(a_0,b_0,a_1)\). The names are distinct although two supplied values coincide. Binary and ternary types have the displayed forms. The ten choices of distinct fixed values realize exactly the ten unary types:

| Fixed pair | Allowed unknown values |
|---|---|
| \(0,1\) | \(\{2,4\}\) |
| \(0,2\) | \(\{1\}\) |
| \(0,3\) | \(\{4\}\) |
| \(0,4\) | \(\{1,3\}\) |
| \(1,2\) | \(\{0,3\}\) |
| \(1,3\) | \(\{2\}\) |
| \(1,4\) | \(\{0\}\) |
| \(2,3\) | \(\{1,4\}\) |
| \(2,4\) | \(\{3\}\) |
| \(3,4\) | \(\{0,2\}\) |

Inactive rows impose no condition, while active rows impose precisely the selected atoms. This proves (8). QED.

In an ordinary fixed-record encoding the complete source length is

\[
N_{\rm can}(r)=\Theta(M(r)\log(r+2)).
\tag{9}
\]

Headers and the supplied-value array are fixed for a given \(r\). Once the record is identified, a requested source bit is a fixed constant or a function of one mask bit. A fixed lexicographic ranking of unary, pair, and triple indices permits record generation by arithmetic on \(O(\log(r+2))\)-bit indices. This describes an actual restriction family for an arbitrary source solver. It does not mandate that the source solver first construct the mask.

Conversely, a raw residual can be converted to its presence mask in polynomial time under the usual explicit encoding. This is a polynomial equivalence of decision representations. It is not automatically a quasilinear or small-workspace transfer: a sparse source with \(O(r)\) rows may have length \(O(r\log r)\), whereas the dense canonical layout has length \(\Theta(r^3\log r)\). Any sharper resource transfer must account for this expansion, indexing, supplied-value lookup, and mask storage separately.

## 4. Minimum distinguishable positive information is exactly the shortest core

Let \(C_1(U_r,z)\), for \(U_r(z)=1\), be the smallest number of coordinates of \(z\) whose observed values force output 1 on every completion of the remaining coordinates. The certificate may initially contain both zero tests and one tests.

### Theorem 3: exact certificate/core identity

\[
\boxed{C_1(U_r,z)=\mu(z),}
\tag{10}
\]

where \(\mu(z)\) is the minimum number of selected atomic constraints with empty intersection. The minimal positive implicants of \(U_r\) are exactly its inclusion-minimal source cores.

**Proof.** A selected core \(K\) certifies output 1 by giving the observations \(z_j=1\) for \(j\in K\). Every completion retaining those constraints is UNSAT. Hence \(C_1\le\mu\).

Conversely, take any 1-certificate, let \(P\) be its coordinates observed as 1, and let \(Z\) be its coordinates observed as 0. The vector \(1_P\), with precisely the coordinates in \(P\) equal to 1, satisfies all these observations. Consequently \(U_r(1_P)=1\). Monotonicity then says that the positive observations on \(P\) alone force output 1. Thus every 1-certificate contains a source core among its positive coordinates. Its total number of observations is at least \(\mu\). The same argument with inclusion-minimality gives the prime-implicant statement. QED.

All-mask realizability in Lemma 2 is important: arbitrary Boolean completions used in this proof are genuine permitted source inputs, not fictitious combinations that a source grammar forbids.

For a general raw residual, selecting one original occurrence of every type in an atomic core gives an equal-size raw source core. A minimum raw core never needs two copies of one type or a true row. Therefore deduplication preserves \(\mu\). It does not preserve the physical cost of locating or authenticating those occurrences and the associated supplied values.

Equation (10) is an exact answer to one version of the user's minimum-information question. It is a semantic certificate bound, and this distinction has a definite limit. A decision tree can acquire all \(M(r)\) input bits in \(M(r)\) probes. Its remaining leaf label is supplied for free in the query model. Thus a pure bit-query or distinguishability lower bound for this cube cannot exceed \(M(r)\). Computing the appropriate label uniformly can still be difficult; that is a computation question which the query model has excluded from its cost.

In particular, exponentially many different cores, covers, or possible completions do not by themselves force exponentially many operations. At fixed \(r\), the entire Boolean function is finite and can be implemented by a fixed table. For growing \(r\), generation, storage, addressing, or replacement of such tables must be charged in one uniform implementation.

## 5. The shortest obstruction need not give the cheapest decision

One should track a collection of alternatives rather than first impose minimum cardinality and then minimize its proof cost.

Here is an explicit control example on a standard sequential input tape. A Boolean CNF starts with

\[
x,\qquad y,\qquad \neg x\lor\neg y,
\]

has a long stretch of tautological rows, and ends with

\[
z,\qquad\neg z.
\]

Its unique minimum-cardinality core has size 2 and lies at the far end. The prefix has a size-3 core. A single fixed correct SAT decider can recognize the contradictory prefix and reject without accessing the tail, while using a general correct procedure on all other prefixes. The prefix-recognition cost does not grow with the filler length, apart from any encoding header it must read.

By contrast, a procedure required to output a minimum-cardinality core must distinguish this input from the same source with the final \(\neg z\) replaced by \(z\). The second source still has the contradictory prefix but has no size-2 core. The two well-formed encodings differ only near the far end, so any such sequential-tape procedure needs linear head movement on this pair. This is a distinction between decision and the extra minimum-core output requirement, not a lower bound against random access.

The appropriate record for an evidence alternative includes at least its source-support size, acquisition and validation costs, the cost of establishing incompatibility, and the shared resources it uses. A larger, nearby, or already derived obstruction may be the cheapest alternative. A general decision algorithm is not required to output any explicit obstruction.

## 6. Charge physical events once, including sharing and preprocessing

Fix one correct deterministic implementation \(A\) before choosing its input. For its execution on a complete encoded input \(I\), record

\[
T_A(I),\qquad
S_A(I)=\max_t s_t,\qquad
C_A(I)=\sum_{t=0}^{T_A(I)}\max\{1,s_t\}.
\tag{11}
\]

Here \(s_t\) uses the project's stated auxiliary-storage convention. Input storage is added if the physical convention counts it. Registers, addresses, cache entries, relocation metadata, and generated representations are included when live. Arbitrary algebra and sound transformations are allowed, with their actual machine operations charged. A supplied circuit is not a free relation-evaluation oracle.

For time, the physical events are instruction steps. For cumulative memory, they can be taken as live storage-bit/time pairs, with one baseline event at any time having zero counted live bits. If several logical obligations use the same event, it contributes once to the total.

### Lemma 4: a valid additive charge requires capacity control

Let \(w_e\ge0\) be physical event weights. If logical obligation \(i\) charges fractions \(\alpha_{i,e}\ge0\) satisfying

\[
\sum_i\alpha_{i,e}\le1\quad\text{for every }e,
\]

then

\[
\sum_i\sum_e\alpha_{i,e}w_e\le\sum_e w_e.
\tag{12}
\]

Equivalently, if sets of supporting events overlap at most \(d\) times, their summed weights are at most \(d\) times the total physical cost. The proof is to interchange the two finite sums.

Thus a proposed lower bound that adds a cost for every slice, forbidden region, or source core must establish both a compulsory charge for each obligation and disjointness or bounded congestion. The existence of many semantic obligations supplies neither condition. A shared algebraic summary or one operation may settle several of them simultaneously.

There is also no universal reason for another nonconstant local computation after arbitrary preprocessing. Any correct algorithm can designate its entire decision computation as preprocessing, store the answer bit, and return that bit in constant additional work. The preprocessing remains fully charged. An argument about a specific boundary can require more work only after proving that the state actually present at that boundary is still insufficient under the declared machine model. No mandatory phase boundary may be inferred solely from the semantic source decomposition.

The identity in (3) handles sharing of source row labels exactly. It is not yet an event-sharing theorem, since an arbitrary implementation need not separately construct slice proofs at all.

## 7. A constructive normal form that keeps the solver unrestricted

There is a useful polynomial-overhead relationship between deciding UNSAT and finding an irredundant source obstruction. This does not impose any proof calculus on the decider.

### Theorem 5: arbitrary decision yields inclusion-minimal core extraction

Fix a correct deterministic decider \(A\) for the masks of length \(M=M(r)\), and let \(T_A(M)\) and \(S_A(M)\) bound it on all masks at that level. There is an extractor which, on UNSAT \(z\), returns an inclusion-minimal core after at most \(M+1\) invocations of \(A\).

**Construction and proof.** First run \(A(z)\). If it is UNSAT, copy the mask to a writable current mask. Consider each selected coordinate in turn, temporarily clear it, and run \(A\) on the modified mask. Keep the deletion if the result is still UNSAT; otherwise restore the bit. The current mask remains UNSAT. If removing a retained bit once gave a satisfiable formula, later deletions only remove constraints, so removing that bit at the end is still satisfiable. Every retained bit is therefore essential. QED.

With straightforward full-mask bookkeeping and a compatible read-only-input simulation, this gives

\[
T_{\rm extract}\le(M+1)T_A(M)+O(M^2),
\qquad
S_{\rm extract}\le S_A(M)+O(M).
\tag{13}
\]

Machine simulation can add ordinary polynomial overhead on a different model. This is a polynomial normal-form statement, not a claim that a tight time exponent or small-space bound is preserved.

In particular, cumulative memory must include the writable mask retained through all calls. For call costs \(C_{A,i}\), call lengths \(T_{A,i}\), and the same memory convention, a faithful ledger has the form

\[
C_{\rm extract}
\le
\sum_i C_{A,i}
+O(M)\sum_i T_{A,i}
+C_{\rm bookkeeping},
\tag{14}
\]

up to simulation overhead. The persistent-mask term must not disappear by summing only the callee costs.

The theorem supports studying irredundant obstructions alongside an arbitrary polynomial decision algorithm. It does not make minimum-cardinality extraction a required step, and it does not give an efficient incompatibility proof independent of the calls to \(A\).

## 8. Every sound algorithm fits a verifier, without free semantic inference

Source-core cardinality and proof length are different objects. A source core can contain only \(O(M)\) atoms while establishing its incompatibility remains computationally difficult. A rule saying simply “this conjunction is UNSAT” would hide that difficulty if its application were charged as a free primitive.

There is a general verifier construction that permits all inference methods without imposing this free rule. Fix any total correct deterministic decision algorithm \(A\) on the language under study. Define

\[
V_A(I,1^t)=1
\iff
A(I)\text{ reports UNSAT within }t\text{ steps}.
\tag{15}
\]

The unary time allowance has length \(t\), so a bounded simulation is polynomial in its complete input size under a standard machine model. The verifier is sound because \(A\) is correct and complete on UNSAT because \(A\) halts. Its accepted proof can have length \(T_A(I)\). Verification pays for the simulation. No exponentially expanded computation tableau or chosen inference calculus is required.

The quantifier is over fixed correct algorithms. There is no claim that an effective master procedure can recognize all and only sound programs, or that a single polynomially optimal proof system has been constructed.

Conversely, suppose a fixed sound verifier \(V\), a fixed deterministic search procedure \(G\), and a polynomial \(p\) satisfy: for every UNSAT input of length \(N\), \(G\) finds a \(V\)-accepted proof and verifies it within \(p(N)\) total charged time. Then run that search for \(p(N)\) steps. A verified proof means UNSAT; otherwise the input is SAT. Soundness prevents false UNSAT answers, and the guaranteed cap prevents missed UNSAT answers. This yields a polynomial-time decider. Proof discovery and verification, including every preprocessing step, are the operational quantities.

Short proofs merely existing is a weaker property. Cook and Reckhow's general framework identifies polynomially bounded propositional proof systems with \(\mathrm{NP}=\mathrm{coNP}\). This does not by itself supply deterministic polynomial proof search. A superpolynomial proof-size lower bound for every such system would show \(\mathrm{NP}\ne\mathrm{coNP}\), a stronger separation than the immediate target \(\mathrm P\ne\mathrm{NP}\). A deterministic lower bound can instead come from the difficulty of finding proofs even when short proofs exist. [1]

The source's Corollary 4.7 contains a known typo relevant to this distinction: Cook's author page corrects its premise from \(\mathrm P\ne\mathrm{NP}\) to \(\mathrm{coNP}\ne\mathrm{NP}\). The claim used here is the original paper's Propositions 1.1 and 1.4, not the uncorrected corollary. [2]

## 9. Quantifiers and the precise remaining lower-bound task

For any individual known UNSAT input \(I_0\), a correct decider can hardcode \(I_0\), compare its input against that string, return UNSAT on equality, and use exhaustive decision otherwise. It takes \(O(|I_0|)\) time on \(I_0\) on an ordinary sequential comparison model. Even charging the description of the hardcoded input gives only linear description size.

Consequently pointwise minimization over a new correct algorithm for every input cannot give a superpolynomial lower bound. The algorithm, permitted primitives, and resource convention must be fixed before the adversarial input is chosen. For growing levels, the implementation must be uniform in \(r\); separate finite tables for each fixed \(r\) do not constitute a single uniform polynomial algorithm.

The canonical cube provides a concrete target for such a theorem:

\[
\text{Exclude every fixed polynomial-time uniform implementation of }U_r
\text{ on all masks as }r\to\infty.
\tag{16}
\]

A valid proof of (16) would immediately exclude a polynomial-time solver for the raw strict-C5 residual language via the fixed-slot realization. Its SAT version is in NP, since a proposed extension is checkable in polynomial time, and complementing a deterministic polynomial-time decision preserves polynomial time. Thus this unrestricted superpolynomial lower bound, if proved, would already imply \(\mathrm P\ne\mathrm{NP}\). No NP-hardness theorem for this particular template is needed for that implication. The statement in (16) itself remains unproved here.

For simultaneous resource exclusions, the target can be a smaller forbidden region of triples \((T,S,C)\), but the same implementation must satisfy all three caps, and the reduction's complete length and access overhead must be included. The polynomial fixed-slot construction by itself does not inherit any near-linear SAT time-space theorem.

The exact established interfaces are (2), (3), and (10): how source obstructions combine across a released value, how their minimum support changes, and precisely how much positive information certifies UNSAT on a fully realizable input family. The missing computational theorem must show that every permitted implementation pays a large total physical cost for establishing incompatibility on some inputs, even after all sharing, preprocessing, and alternative obstructions have been allowed.

## References

[1] Stephen A. Cook and Robert A. Reckhow, “The Relative Efficiency of Propositional Proof Systems,” *The Journal of Symbolic Logic* 44(1), 1979, pp. 36–50. Propositions 1.1 and 1.4 and Definitions 1.3 and 1.5. Author-hosted copy: <https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf>. DOI: <https://doi.org/10.2307/2273702>.

[2] Stephen A. Cook, author homepage, correction to Corollary 4.7 of [1], accessed 22 November 2026: <https://www.cs.toronto.edu/~sacook/>.

Project definitions and earlier finite-template results: `fresh_static_levels/t5/T5_One_Two_Unknown_Core_Theorem.md`; resource conventions and transfer limitations: `fresh_static_levels/Static_Restriction_Resource_Transfer.md`. The present elementary proofs do not require the companion computation of the three-unknown bound.
