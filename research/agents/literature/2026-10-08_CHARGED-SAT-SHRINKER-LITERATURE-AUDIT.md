# Literature audit: the charged all-input SAT shrinker

**Audit date:** 2026-10-08  
**Scope:** kernelization and compression, OR-distillation, SAT sparsification, self-reducibility and search-to-decision, SAT time-space lower bounds, proof complexity, and the closest 2025--2026 semantic-compression results.  
**Purpose:** determine whether a published theorem supplies, rules out, or reframes the missing WRAPPER/generated-cover/typed-epoch arrow.

## Executive conclusion

No located theorem supplies the missing arrow for arbitrary encoded CNF-SAT.

The strongest defensible state of the project is therefore a **conditional internal meta-theorem**:

> If there is a uniform, source-checkable, all-input compiler that constructs an exact cover by genuinely smaller SAT instances, and if every bit of its discovery, materialization, replay, recursion, fanout, and workspace is charged, then the existing WRAPPER accounting can be tested against a published SAT time-space lower-bound endpoint.

The missing premise is not merely the existence of equivalent labels or the ability to verify a proposed merge. It is the efficient **acquisition** of enough exact merges or smaller successors on every input before making a circular current-scale SAT call.

The literature contains unusually close precedents:

- exact disjunctive covers for fixed-width SAT, but with exponential fanout;
- exact solution-preserving variable merges for 1-in-3-SAT, but not arbitrary CNF-SAT;
- existential zero-preserving CSP sparsifiers of size controlled by non-redundancy, but without a general efficient acquisition algorithm;
- a 2026 one-pass construction that retains a zero-preserving weighted subinstance in small space, but expressly places no restriction on postprocessing time and lists simultaneous time-and-space efficiency as open;
- efficient sparsification for explicit algebraic codes and restricted fixed predicates, but no transfer to the implicit exponential assignment code of general CNF-SAT;
- conditional kernelization and OR-compression barriers, whose hypotheses become unavailable inside a contradiction argument that assumes \(P=NP\).

These results reframe the open point very precisely. The project needs to prove, rather than posit, the following implication:

\[
\boxed{
  \text{arbitrary encoded CNF }F
  \ \longmapsto_{\text{uniform, exact, fully charged}}\ 
  \text{a bounded exact cover/DAG of power-smaller SAT instances}
}
\]

No complete P versus NP proof follows until that implication is established.

## Claim-status vocabulary

The manuscripts should use these labels consistently.

| Label | Meaning |
|---|---|
| **PROVED/EXACT** | A published theorem used with its exact hypotheses, or a source-checkable internal derivation in its declared scope. A conditional implication receives this label only as an implication with its OPEN premise displayed. |
| **COMPUTATIONAL** | Finite experiments, model checks, or searches; useful for falsification and design, but not an all-input proof. |
| **OPEN** | An unproved all-input statement, including the size-reducing acquisition step described below. |
| **FALSIFIED/RETIRED** | A claim defeated by a counterexample, source correction, or demonstrated quantifier/model mismatch. |

Statements marked `PROVED`, `PROVED/EXACT`, or `COMPUTATIONAL` in earlier project documents should be reclassified by their actual quantifiers. A finite test cannot establish the open all-input compiler theorem, even when every tested merge is exact.

## 1. Correct lower-bound endpoint

### 1.1 The universal product boundary is the golden ratio

Ryan Williams, *Alternation-Trading Proofs, Linear Programming, and Lower Bounds*, ACM TOCT 5(2), 2013, [full version](https://people.csail.mit.edu/rrw/automated-lbs.pdf):

- **Theorem 4.11:** for polynomially bounded \(t(n)\) and \(s(n)\), every SAT algorithm must satisfy
  \[
  t(n)s(n)=\Omega_{\mathrm{i.o.}}\!\left(n^{\varphi-\varepsilon}\right)
  \quad\text{for every fixed }\varepsilon>0,
  \qquad
  \varphi=\frac{1+\sqrt5}{2}.
  \]
- Section 2 states that the default model is a broadly construed random-access machine, that functions are appropriately constructible, and that \(\Omega\) is used in the infinitely-often sense.
- Section 4.5, **footnote 9**, explicitly says that an earlier version “unfortunately claimed” a universal \(n^{1.801}\) time-space product and that proving it would require new techniques.

Therefore a general landing with time exponent \(c\) and space exponent \(d\) is contradicted by Theorem 4.11 only when the fully charged exponents satisfy

\[
c+d<\varphi,
\]

with enough fixed slack to absorb all \(o(1)\) and polylogarithmic terms.

The retracted \(c+d<2\cos(\pi/7)\) test must not appear as a universal endpoint.

### 1.2 The near-linear-time strip is a separate theorem

Lance Fortnow, *Time-Space Tradeoffs for Satisfiability*, JCSS 60(2), 2000, [author PDF](https://lance.fortnow.com/papers/files/npvsnl.pdf):

- **Theorem 3.1:** for every fixed \(\varepsilon>0\),
  \[
  \mathrm{SAT}\notin \mathrm{NTISP}
  \left[n^{1+o(1)},n^{1-\varepsilon}\right].
  \]
- **Corollary 3.3:** the same exclusion holds for deterministic algorithms.
- The paper notes after Theorem 3.2 that Theorems 2.3 and 2.4 transfer the result to random-access machines.

Thus a fully charged landing such as \((c,d)=(1,2/3)\) is forbidden by Fortnow's theorem, even though \(1+2/3>\varphi\). This is a strip at near-linear time, not a product half-plane. It does not automatically cover \(c=1+\delta\) for a fixed \(\delta>0\).

### 1.3 The \(2\cos(\pi/7)\) exponent belongs to a small-space regime

Williams's small-space SAT lower bound gives time exponent

\[
\gamma_0=2\cos(\pi/7)\approx 1.80194
\]

against \(n^{o(1)}\) workspace. Buss and Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Computational Complexity 24(3), 2015, [full paper](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf), prove in **Theorem 1.1** that the specified inference rules R0--R2 derive contradictions only for \(c<2\cos(\pi/7)\); **Theorem 3.25** supplies the matching refutations below the threshold, and **Theorem 5.5** proves the limitation.

This characterizes that alternation-trading system in the subpolynomial-space setting. It is not a universal product theorem. Williams's 2008 result also gives, for each strict \(c<\gamma_0\), a sufficiently small positive-space neighborhood; the allowed space exponent depends on \(c\) and is not the line \(c+d<\gamma_0\).

### 1.4 Defensible endpoint union

A completed compiler may land in any separately verified region, provided the machine model and all resource charges match:

1. **Williams product region:** \(c+d<\varphi\).
2. **Fortnow strip:** \(c=1+o(1)\) and \(d<1\) by a fixed margin.
3. **Williams small-space region:** \(d=o(1)\) and \(c<2\cos(\pi/7)\), or a specifically sourced positive-space neighborhood.
4. **Specific published pairs:** only after checking the exact theorem or proof certificate; isolated computer-discovered points must not be interpolated into a new universal frontier.

The endpoint is therefore available. The missing theorem is upstream: producing the claimed total algorithm and its exponents.

## 2. Exact statement of the open arrow

The following is a source-checkable target specification. Variants may use a list, guarded OR, or typed DAG, but must prove equivalent obligations.

### Charged exact-cover compiler schema

There must be one uniform deterministic transducer \(C\) such that, on every bit string \(x\) of length \(N\):

1. **Parsing and malformed inputs.** \(C\) either interprets \(x\) as a CNF formula \(F_x\) under a fixed encoding or returns the prescribed answer for malformed encodings, within the same resource bounds.
2. **Pre-answer construction.** Before asking any SAT query of size \(N^{1-o(1)}\), \(C\) constructs or gives a random-access decoder for a finite object \(D_x\).
3. **Exact semantics.** The leaves \(G_1,\ldots,G_m\) of \(D_x\) obey a proved composition rule, for example
   \[
   \mathrm{SAT}(F_x)\iff \bigvee_{i=1}^{m}\mathrm{SAT}(G_i),
   \]
   or an explicitly typed Boolean composition with the same exactness. Equality of observed SAT answers is not enough; the reduction must preserve the required semantics.
4. **Actual encoded contraction.** Every recursive child/query has encoded bitlength
   \[
   |G_i|\le N^{\lambda+o(1)}
   \quad\text{for one fixed }\lambda<1,
   \]
   or satisfies another proved well-founded contraction whose solved recurrence yields the claimed exponent. Reducing clause count or variable count without bounding the chosen bit encoding is insufficient.
5. **Bounded total branching.** The number of leaves, total emitted bits, parallel alternatives, and products of fanouts over all recursive levels are bounded explicitly.
6. **Charged discovery.** Parsing, canonicalization, equivalence discovery, backdoor discovery, sorting, hashing, certificate production, and construction time are included. A cheaply checkable certificate does not imply cheap certificate discovery.
7. **Charged replay.** If \(D_x\) is implicit, every requested bit of every virtual query is reproducible within stated time and workspace; repeated decoding costs are included in total time.
8. **Charged recursive calls.** All SAT calls used to discover, verify, or solve successors appear in the recurrence. No current-scale call may be hidden inside “find a merge,” “choose a route,” or “construct a backdoor.”
9. **Workspace discipline.** Readable query material, indices, recursion stacks, prime labels, hash tables, certificates, and answer vectors count toward workspace. A write-only reduction tape may not be reread for free.
10. **Uniformity and words.** There is no input-length advice, unbounded word, uncharged random stream, or pointer to an exponentially large external object.
11. **Termination.** The recursion is well founded on actual encoded length, with total base-case solvers and a proved maximum depth.
12. **Model transport.** The final composed algorithm is converted to the precise random-access model used by the selected lower bound, with all polylogarithmic losses and constructibility conditions shown.

Only after these items are proved may the project derive total exponents \(c,d\) and invoke one clause of the endpoint union.

This schema also identifies why a double wrapper can be useful but is not by itself a solution. An outer recursive wrapper may schedule answers and an inner forward-only wrapper may emit alternatives, but the inner wrapper still has to generate the exact, power-smaller alternatives without first learning a current-scale SAT answer. Parallel wrappers help only if their combined fanout and acquisition/replay costs meet the same ledger.

## 3. Kernelization, compression, and OR-distillation

### 3.1 Dell--van Melkebeek: a quantitative multiquery barrier

Holger Dell and Dieter van Melkebeek, *Satisfiability Allows No Nontrivial Sparsification unless the Polynomial-Time Hierarchy Collapses*, JACM 61(4), 2014, [full paper](https://pages.cs.wisc.edu/~dieter/Papers/sparsification-full.pdf):

- **Theorem 1:** for each fixed integer \(d\ge3\) and \(\varepsilon>0\), if \(\mathrm{coNP}\nsubseteq\mathrm{NP/poly}\), there is no oracle communication protocol of cost \(O(n^{d-\varepsilon})\) deciding \(n\)-variable \(d\)-CNF-SAT, even with a conondeterministic first player.
- **Corollary 1:** under the same hypothesis, there is no polynomial-time reduction from \(d\)-SAT to any problem making \(O(n^b)\) queries of bitlength \(O(n^c)\) when \(b+c<d\).

Corollary 1 is directly relevant to a generated cover: it says that fanout exponent plus child-length exponent cannot beat \(d\) in this model unless a standard collapse occurs.

**Non-transfer limitation.** A proof by contradiction that assumes \(P=NP\) also has \(NP=coNP=P\subseteq NP/poly\). The hypothesis \(\mathrm{coNP}\nsubseteq\mathrm{NP/poly}\) is then false. Consequently, this theorem cannot be invoked inside the assumed \(P=NP\) world to rule out the compiler, nor does it construct one. It remains an excellent design calibration and an explanation of why a general shrinker would be a major theorem.

### 3.2 Fortnow--Santhanam and Drucker: list compression has collapse consequences

Fortnow and Santhanam, *Infeasibility of Instance Compression and Succinct PCPs for NP*, JCSS 77(1), 2011, [ECCC TR07-096](https://eccc.weizmann.ac.il/report/2007/096/), show that SAT instance compression/strong OR-distillation would imply \(NP\subseteq coNP/poly\) and collapse the polynomial hierarchy.

Andrew Drucker, *New Limits to Classical and Quantum Instance Compression*, SIAM J. Comput. 44(5), 2015, [ECCC full version](https://eccc.weizmann.ac.il/report/2012/112/download/):

- **Theorem 1.1:** a deterministic polynomial-time map compressing an arbitrarily long list according to AND for an NP-complete language implies \(NP\subseteq coNP/poly\).
- **Theorems 7.4 and 7.5:** quantitative probabilistic AND- and OR-compressions with sufficient reliability and compression imply nonuniform reductions to promise-SZK and \(NP\subseteq coNP/poly\); the theorem statements spell out the error/output tradeoff.

These theorems show that a polynomial-size disjunctive outer wrapper is not a routine normalization.

**Non-transfer limitation.** Again, their collapse conclusions are already consistent with the temporary assumption \(P=NP\). They cannot provide the desired contradiction under that assumption. Their compression format also combines a list of instances; the missing WRAPPER arrow starts from one arbitrary formula and must cheaply discover its smaller exact cover.

### 3.3 What these barriers do and do not say

They do say:

- a sufficiently strong all-input compiler would be structurally important;
- fanout and output bitlength must be analyzed jointly;
- changing the target language or using several queries does not automatically evade compression barriers.

They do not say:

- that the desired compiler is impossible unconditionally;
- that a compiler would contradict \(P=NP\);
- that a claimed compiler may omit its construction cost;
- that a restricted-predicate sparsifier transfers to general CNF-SAT.

## 4. SAT sparsification and disjunctive structure

### 4.1 The classical sparsification lemma gives an exact OR, but exponential fanout

The Impagliazzo--Paturi--Zane sparsification lemma is stated with explicit delay and density bounds as **Lemma 1** in Calabro, Impagliazzo, and Paturi, *On the Exact Complexity of Evaluating Quantified \(k\)-CNF*, IPEC 2010, [paper](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/CalabroImpagliazzoPaturi_2010_ipec.pdf): for fixed \(k\ge2\) and \(\varepsilon\in(0,1]\), an \(n\)-variable \(k\)-CNF is transformed into at most \(2^{\varepsilon n}\) \(k\)-CNFs, with \(n^{O(k)}\) delay, whose satisfying-assignment sets have exactly the original set as their union; each output has \(O((k/\varepsilon)^{3k}n)\) clauses.

This is a genuine exact disjunctive cover and is the best classical analogue of the proposed forward-only wrapper.

**Why it does not close the arrow:**

- the number of children is exponential in \(n\);
- delay per child is polynomial, so total generation is still exponential;
- the children are sparse in clauses but not necessarily power-smaller in encoded bitlength;
- fixed \(k\) is essential, whereas arbitrary CNF needs a separately charged width reduction;
- recursive use must multiply fanouts over levels.

The 2026 SOSA paper by Lokshtanov, Saurabh, and Xue, *The Sparsification Lemma via Measure and Conquer*, [DOI](https://doi.org/10.1137/1.9781611978964.22), provides a cleaner proof with the same essential \(2^{\varepsilon n}\)-type tradeoff. It does not turn the cover into a polynomial charged compiler.

### 4.2 Disjunction is useful only after its size is charged

For a list \(G_1,\ldots,G_m\), a guarded OR/Tseitin encoding can combine the alternatives exactly. That is a legitimate internal construction once:

- each \(G_i\) is already available or bit-decodable;
- the selector and full biconditional Tseitin constraints are emitted;
- the combined encoded length, variable namespace, and decoder time are charged.

The OR gadget does not discover the list and does not make
\(\sum_i |G_i|\) disappear. A “parallel wrappers” proposal therefore needs
a theorem bounding the union of their output sizes and the total time to
generate and answer them.

## 5. The closest 2025--2026 semantic-compression precedents

### 5.1 Existential code/CSP sparsification: exact zero preservation without efficient acquisition

Joshua Brakensiek and Venkatesan Guruswami, *Redundancy Is All You Need (for CSP Sparsification)*, STOC 2025/full ECCC 2026, [TR26-077](https://eccc.weizmann.ac.il/report/2026/077/) and [full PDF](https://eccc.weizmann.ac.il/report/2026/077/download/):

- **Theorem 1.1:** every binary code \(C\subseteq\{0,1\}^m\) has an \(\varepsilon\)-sparsifier with support
  \[
  O\!\left(\mathrm{NRD}(C)(\log m)^6/\varepsilon^2\right).
  \]
- **Theorem 1.2:** for every fixed nonempty proper finite relation \(R\subsetneq D^r\), the worst-case CSP sparsifier size is between its predicate-specific non-redundancy and that quantity times \(O((r\log n)^6/\varepsilon^2)\).
- The paper explicitly says it focuses on **existence** and leaves algorithmic aspects for future work.

Applied to the code whose coordinates are constraints and whose codeword for assignment \(\alpha\) marks violations, multiplicative preservation with \(0<\varepsilon<1\) preserves the zero set exactly:

\[
\operatorname{unsatval}_H(\alpha)=0
\iff
\operatorname{unsatval}_F(\alpha)=0.
\]

This is a strong conceptual precedent for an exact semantic wrapper: a weighted subinstance can preserve all satisfying assignments even though it only approximates positive violation counts.

**Why it does not close the arrow:**

- the theorem is existential in the needed generality;
- constructing the violation code explicitly would enumerate exponentially many assignments;
- the bound depends on predicate-specific non-redundancy, which can be as large as the trivial \(\Theta(n^r)\) scale for OR/AND-type predicates;
- it measures support in terms of variables for a fixed relation, not power contraction of arbitrary CNF bitlength;
- weights and their bitlength must be encoded and charged;
- general CNF is not one fixed finite relation unless a width-reduction encoding is first carried out and charged.

The key warning is that “a small exact semantic object exists” is not the same theorem as “a uniform algorithm finds it within the target time-space budget.”

### 5.2 Efficient restricted-CSP sparsification does not cover the SAT violation predicate

Khanna, Putterman, and Sudan, *Efficient Algorithms and New Characterizations for CSP Sparsification*, STOC 2025, [full paper](https://www.cis.upenn.edu/~sanjeev/papers/stoc25_csp_sparsification.pdf):

- **Theorem 1.1:** randomized polynomial-time near-linear sparsification for an explicitly represented linear code.
- **Theorem 1.5:** a fixed Boolean arity-\(r\) predicate with other than exactly one satisfying assignment has an efficient \(\widetilde O_r(n^{r-1}/\varepsilon^2)\) sparsifier; a predicate with exactly one satisfying assignment has no \(o(n^r)\) sparsifier in this model.
- **Theorem 1.7:** efficient near-linear sparsification for affine Abelian predicates, with the stated arity/group dependence.

The violation predicate of an OR clause is an AND-type unique-pattern predicate. Thus Theorem 1.5 does not provide nontrivial worst-case violation sparsification for ordinary \(r\)-CNF-SAT. Its lower bound is for weighted subinstance/count sparsification; it does not rule out every more powerful semantic transformation that may introduce variables or produce a disjunctive cover.

Nor does Theorem 1.1 automatically help: the code of all assignment-violation vectors is implicit and can have exponentially many codewords, whereas the theorem's efficient representation is algebraic/explicit. A reduction must prove that its required oracle operations on the implicit code are efficient.

### 5.3 Strong sparsification: exact variable merging for 1-in-3-SAT

Bedert, Nakajima, Okrasa, and Živný, *Strong Sparsification for 1-in-3-SAT via Polynomial Freiman--Ruzsa*, FOCS 2025, revised 2026, [arXiv:2507.17878v4](https://arxiv.org/html/2507.17878v4):

- **Definition 1:** a strong sparsifier outputs an equivalence relation that merges only variables equal in all solutions.
- **Theorem 2:** there is a polynomial-time strong sparsification algorithm for monotone 1-in-3-SAT with \(O(n^{2-\varepsilon})\) clauses, where \(\varepsilon\approx0.0028\).
- The construction gives a one-to-one correspondence between solutions before and after the permitted merges.
- Section 1 reports an unconditional strong-sparsifier lower bound of \(\Omega(n^{1.725\ldots})\) for some instances, even with unrestricted running time, because no further variable merges are possible.

This directly validates a central WRAPPER intuition: **semantic equivalence classes of variables can yield exact, polynomial-time, size-reducing merges.**

**Non-transfer limitation:** the theorem is predicate-specific. The paper itself notes that strong sparsification is, in particular, ordinary sparsification and that nontrivial results for 3-SAT are unlikely in light of Dell--van Melkebeek. It neither handles arbitrary CNF nor yields child bitlength \(N^\lambda\) for all encodings. Its method is a clue for what a valid merge certificate should look like, not the missing general theorem.

### 5.4 One-pass CSP cores: the closest statement of the acquisition gap

Brakensiek, Putterman, Sharma, and Velusamy, *Cores Characterize the One-Pass Streaming Complexity of CSPs*, arXiv, 5 October 2026, [arXiv:2610.07455v1](https://arxiv.org/html/2610.07455v1):

- **Theorem 5.1:** for every fixed nontrivial finite relation \(R\), deterministic one-pass \(\operatorname{SAT}(R)\) uses
  \[
  O_R(\mathrm{NRD}_n(\operatorname{core}(R))\log n)
  \]
  bits, with a matching randomized lower bound up to the logarithm.
- **Theorem 6.1:** a deterministic one-pass algorithm stores a weighted subinstance \(H\subseteq I\) in
  \[
  O_{R,\varepsilon}\!\left(\mathrm{NRD}_n(R)\operatorname{polylog}(n,m,1/\varepsilon)\right)
  \]
  space such that, simultaneously for every assignment \(\alpha\),
  \[
  \operatorname{unsatval}_H(\alpha)
  \in(1\pm\varepsilon)\operatorname{unsatval}_I(\alpha).
  \]
  Hence the satisfying-assignment set is preserved exactly.
- In the proof, the required sparsifier can be found by exhaustive enumeration because the streaming model places no restriction on computation/postprocessing time.
- **Section 8 explicitly asks** whether Theorems 5.1 and 6.1 can be made efficient in both time and space, observing that no general efficient method is known for detecting CSP non-redundancy and calling such a method a major milestone for CSP kernelization.

This is the closest published analogue of the missing charged-acquisition arrow. It supplies a small retained semantic object in a restricted fixed-relation streaming model, while explicitly leaving the time needed to find it open. The WRAPPER theorem needs precisely the missing strengthening, plus arbitrary-CNF and encoded-size guarantees.

### 5.5 Later 2026 refinements improve structural bounds, not the implicit-CNF compiler

- Lovett, Meka, and Wang, *Moonflowers and Efficient Code Sparsification*, [arXiv:2605.08676](https://arxiv.org/abs/2605.08676), improve the logarithmic dependence for efficiently represented codes.
- Khanna, Putterman, and Sudan, *A Unified Theory of Sparsification*, [arXiv:2607.16126](https://arxiv.org/abs/2607.16126), develop a structural theory for nonnegative real-valued codes through continuous-valued non-redundancy.
- Brakensiek, Guruswami, Jansen, Lagerkvist, and Wahlström, *Super-linear Lower Bounds for CSP Non-Redundancy via Shrinking Instances*, [arXiv:2605.19055](https://arxiv.org/abs/2605.19055), use hypergraph projections and shrinking factors to transfer non-redundancy bounds.

These works offer useful measures and gadgets for experiments, but none proves a polynomial-time, all-input, exact, power-shrinking compiler for the implicit violation code of arbitrary CNF-SAT.

## 6. Self-reducibility and search-to-decision

### 6.1 Standard SAT self-reduction is additive, adaptive, and same-scale

The usual witness recovery fixes variables one at a time and asks whether (F[x_i=0]) remains satisfiable. It uses (O(n)) adaptive SAT queries. Those queries generally shrink by only an additive amount and can retain (Theta(N)) encoded length for most of the process.

Therefore standard self-reducibility can:

- recover a witness after a SAT decision procedure is available;
- validate assignment-history logic in a wrapper;
- supply a well-founded recursion on variable count.

It cannot by itself:

- produce a query of size \(N^\lambda\) with \(\lambda<1\);
- select the successful route before receiving large SAT answers;
- prevent total branching from becoming (2^n);
- establish a low time-space recurrence after materialization costs.

### 6.2 Query-round normal forms do not imply query-length contraction

Buss and Hay, *On Truth-Table Reducibility to SAT*, Information and Computation 91(1), 1991, [author page](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/ttreduce/index.html), prove that polynomial-time circuit truth-table reductions, logspace formula truth-table reductions, and logspace Turing reductions to SAT coincide in the specified sense, and that a constant number of parallel-query rounds collapses to one.

This helps normalize orchestration, not size. The theorem does not make each SAT query power-smaller or make construction/replay free.

Ren and Williams, *Near-Maximum Circuit Lower Bounds for Exponential Time with Merlin-Arthur Queries*, [ECCC TR26-118](https://eccc.weizmann.ac.il/report/2026/118/), analyze \(P^{NP}[\#\mathrm{rounds}=r,\mathrm{length}=s]\), where “length” is NP witness length. This is relevant evidence that round complexity and witness/query scale are separate resources. It does not provide the required deterministic exact SAT cover or encoded-query contraction.

### 6.3 Downward self-reducibility in total search is not a SAT shrinker

Gajulapalli, Ghentiyala, Li, and Saraogi, *Downward Self-Reducibility in the Total Function Polynomial Hierarchy*, [arXiv:2507.19108](https://arxiv.org/abs/2507.19108), show that downward-self-reducible problems in \(TF\Sigma_i^P\) fall into \(PLS^{\Sigma_{i-1}^P}\), and essentially unique problems into \(UEOPL^{\Sigma_{i-1}^P}\), under their stated randomized/oracle framework.

This work stresses the importance of a strictly decreasing measure and sound reconstruction. It assumes access to smaller-instance answers; it does not construct the missing smaller SAT instances for arbitrary CNF within the WRAPPER budget.

## 7. Proof complexity and certificates

Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1), 1979, [primary PDF](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf), define polynomial-time verifiable propositional proof systems. Their framework yields the standard equivalence:

\[
NP=coNP
\iff
\text{there exists a polynomially bounded propositional proof system}.
\]

This distinction is crucial for the wrapper:

- a resolution, RUP, DRAT, or semantic certificate can make a **proposed** UNSAT consequence or merge cheaply checkable;
- a short proof's existence under a complexity-class collapse does not give a uniform algorithm that finds that proof within the needed time and space;
- lower bounds for resolution or another named proof system are system-specific and do not become lower bounds for unrestricted deterministic SAT algorithms;
- SAT instances also require sound certificates for positive semantic merges, not only refutations.

Proof-complexity generators and recent range-avoidance work study hardness of finding strings/proofs outside ranges. They do not license treating a hash, prime label, or compressed history identifier as an equisatisfiable SAT instance.

For defensibility, every certificate-based wrapper lemma must state both:

1. verifier time/space given the certificate; and
2. generator time/space for finding the certificate on every input.

Only the first is supplied by ordinary proof checking.

## 8. Space-efficient replay results

Williams, *Simulating Time with Square-Root Space*, STOC 2025, [DOI](https://doi.org/10.1145/3717823.3718225):

- **Theorem 1.1:** a time-\(t\) multitape Turing machine can be simulated in \(O(\sqrt{t\log t})\) space.
- **Remark 1.6:** the theorem is not known for arbitrary random-access machines; an oblivious-access extension is described.

Sibgatullin and Williams, *Space-Efficient Simulations Beyond Multitape Turing Machines*, FOCS 2026/full ECCC, [TR26-223](https://eccc.weizmann.ac.il/report/2026/223/):

- **Theorem 1.1:** their free-input parallel external-memory computation with \(T\) I/O rounds, \(P\) processors, external memory \(S\), and internal memory \(M\) can be simulated in
  \[
  O(T\log(PSM)+M)
  \]
  space under the stated goodness conditions.
- **Theorem 2.1:** every gate of a \(b\)-bit \(n\)-gate circuit is evaluable in \(O(\hbar(C)+b+\log n)\) space, where \(\hbar\) is normalized depth.
- The model gives processors free input access and permits arbitrary \(O(M)\)-space computation between charged I/O rounds.

These are valuable replay/space tools, but they do not bound the time needed to discover a semantic contraction. A time-space lower-bound contradiction requires one algorithm with both resources bounded simultaneously. Space-only replay cannot erase exponential recomputation time, and a free-input external-memory model cannot be silently identified with the random-access model of the SAT lower bound.

## 9. Hashes, prime labels, and output length

Changing a displayed hash from four to six or eight digits cannot affect the asymptotic proof unless the hash length grows with input size and is included in the ledger.

For a family with unboundedly many histories:

- a fixed-length hash has collisions by the pigeonhole principle;
- merging colliding histories is unsound unless an independent deterministic semantic certificate proves equivalence;
- a randomized fingerprint provides only a probability of collision, not exact all-input correctness;
- derandomization, collision resolution, and replay must be charged;
- an injective identifier for \(H\) histories needs at least \(\lceil\log_2 H\rceil\) bits;
- assigning distinct primes does not evade this information cost: the prime index/value, arithmetic, and storage all grow and must be charged.

Hashes are useful for memoization and experimental canonicalization after exact equality is checked. They are not semantic compression theorems. The labels `TRUE`, `NOT TRUE`, `FALSE`, and `NOT FALSE` may have distinct prime tags, but distinct tags neither prove equivalence of paths nor reduce the encoded SAT information needed to decide them.

## 10. What the WRAPPER variants currently establish

The present constructions can defensibly provide the following, subject to their internal proofs and ledgers:

- a DAG representation of explored assignment histories;
- exact merging when Boolean equivalence or another checkable semantic relation is independently proved;
- a test framework that finds counterexamples to unsafe “same SAT answer implies merge” rules;
- guarded-OR composition of an already generated finite list;
- an outer scheduler that supplies answers to a forward-only inner wrapper;
- finite-depth typed seed elimination when base solvers and types are total;
- explicit recurrence and resource accounting conditional on a successor/compiler theorem.

They do not yet establish:

- that every general CNF has enough efficiently discoverable equivalent histories;
- that the merged object is power-smaller in actual encoded bitlength;
- that the forward-only wrapper can generate the successful alternatives before large SAT answers;
- that total fanout over recursive levels is polynomial or has the claimed exponent;
- that every acquisition and replay step fits a verified endpoint.

This is why removing recursion is not, by itself, a fix. It removes recursive SAT costs only if the nonrecursive wrapper still outputs an exact size-reducing object cheaply. A double wrapper is a sound organizational pattern only when the inner, nonrecursive generation theorem is independently proved.

## 11. Most promising research routes

The literature suggests four concrete routes, none currently complete.

### Route A: efficient non-redundancy acquisition

Try to turn the Brakensiek--Guruswami existence theorem and the 2026 sparsify--merge--sparsify stream into a polynomial-time algorithm for the implicit violation code of a carefully restricted SAT representation.

Required breakthrough:

- implement the needed non-redundancy/separation oracle without enumerating assignments or calling same-scale SAT;
- prove a uniform subtrivial bound on non-redundancy for the resulting predicate family;
- translate support size to encoded bitlength and bounded weights.

The 2026 streaming paper explicitly identifies the first bullet as open.

### Route B: certified semantic merges beyond 1-in-3-SAT

Generalize the 1-in-3-SAT strong-sparsification mechanism to a SAT representation whose variables admit efficiently detectable “equal in all solutions” relations.

Required breakthrough:

- avoid the unique-pattern obstruction associated with ordinary clause violations;
- prove that every input admits enough merges, not only structured instances;
- charge certificates and show subpower encoded size, not merely fewer variables.

### Route C: polynomial exact generated cover

Strengthen the sparsification lemma from \(2^{\varepsilon n}\) children to a cover whose total generated bits and total acquisition time fit the endpoint after recursion.

Required breakthrough:

- a new structural theorem, because known exact covers pay exponential fanout;
- a proof that no route selection requires a current-scale SAT answer;
- an exact recurrence for fanout times child-solving cost.

### Route D: exploit a restricted endpoint landing

Instead of proving a universal product landing, design the compiler specifically for:

- Fortnow's near-linear-time/sublinear-space strip; or
- Williams's (n^{o(1)})-space region.

This may weaken the compiler requirements on one resource, but does not remove acquisition time, child size, or total fanout. In particular, a nominal ((1,2/3)) landing is attractive because Fortnow, not the golden-ratio product theorem, forbids it.

## 12. Defensibility requirements for the next manuscript revision

1. State the encoding and malformed-input behavior first.
2. State the exact compiler theorem as an explicit hypothesis until proved.
3. Distinguish support/variable reduction from encoded-bitlength contraction.
4. Give a resource ledger for construction, fanout, materialization or decoding, recursion, answer storage, and base cases.
5. Prove exact semantics of each merge and each OR/typed composition.
6. Separate certificate verification from certificate discovery.
7. Prove the closed recurrence; do not infer a total exponent from one recursion level.
8. Name exactly one applicable endpoint theorem for each claimed contradiction.
9. Use \(c+d<\varphi\), not the retracted universal \(c+d<2\cos(\pi/7)\).
10. If using \(2\cos(\pi/7)\), state the small-space hypothesis or the exact sourced positive-space neighborhood.
11. Do not use Dell--van Melkebeek, Fortnow--Santhanam, or Drucker as a contradiction inside a \(P=NP\) assumption; their noncollapse hypotheses/conclusions do not transfer that way.
12. Label experiments as computational evidence, with input range, encoding, and failure search stated.
13. Include a “non-transfer” paragraph for every imported theorem.
14. Conclude only
    \[
    (P=NP)\land H_{\mathrm{compiler}}\Longrightarrow\bot
    \]
    unless \(H_{\mathrm{compiler}}\) has been proved independently.

## 13. Bottom line

The endpoint is not the unresolved part. The corrected published endpoint is a union of Williams's golden-ratio product theorem, Fortnow's near-linear strip, and Williams's small-space \(2\cos(\pi/7)\) result.

The WRAPPER architecture is useful: it organizes exact compositions, exposes unsafe merges, and can convert a valid successor theorem into a fully charged SAT algorithm. Recent semantic-sparsification work strongly supports the *form* of the idea—exact zero sets can survive weighted sparsification, and solution-forced equivalences can justify variable merging.

But the same literature pinpoints the missing theorem. The closest all-relation result is existential or time-unbounded; the closest efficient exact merge is predicate-specific; the classical exact SAT cover has exponential fanout; and conditional compression barriers do not furnish a contradiction under \(P=NP\).

Accordingly, the present proof is defensible only as a conditional proof spine. A complete proof structure becomes possible precisely when the project supplies a uniform, all-input, exact, power-size-reducing compiler with discovery and replay fully charged and whose composed exponents land strictly inside one verified endpoint region.

## Primary-source index

- Williams 2013, Theorem 4.11 and footnote 9: <https://people.csail.mit.edu/rrw/automated-lbs.pdf>
- Williams 2008, Theorem 1.2 and Corollary 6.11: <https://people.csail.mit.edu/rrw/mod-lbs-journal-final.pdf>
- Buss--Williams 2015, Theorems 1.1, 3.25, 5.5: <https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf>
- Fortnow 2000, Theorem 3.1 and Corollary 3.3: <https://lance.fortnow.com/papers/files/npvsnl.pdf>
- Dell--van Melkebeek 2014, Theorem 1 and Corollary 1: <https://pages.cs.wisc.edu/~dieter/Papers/sparsification-full.pdf>
- Fortnow--Santhanam 2011: <https://eccc.weizmann.ac.il/report/2007/096/>
- Drucker 2015, Theorems 1.1, 7.4, 7.5: <https://eccc.weizmann.ac.il/report/2012/112/download/>
- Calabro--Impagliazzo--Paturi 2010, Lemma 1: <https://cseweb.ucsd.edu/~paturi/myPapers/pubs/CalabroImpagliazzoPaturi_2010_ipec.pdf>
- Brakensiek--Guruswami 2026, Theorems 1.1 and 1.2: <https://eccc.weizmann.ac.il/report/2026/077/download/>
- Khanna--Putterman--Sudan 2025, Theorems 1.1, 1.5, 1.7: <https://www.cis.upenn.edu/~sanjeev/papers/stoc25_csp_sparsification.pdf>
- Bedert--Nakajima--Okrasa--Živný 2026 revision, Definition 1 and Theorem 2: <https://arxiv.org/html/2507.17878v4>
- Brakensiek--Putterman--Sharma--Velusamy 2026, Theorems 5.1 and 6.1, Section 8: <https://arxiv.org/html/2610.07455v1>
- Buss--Hay 1991: <https://mathweb.ucsd.edu/~sbuss/ResearchWeb/ttreduce/index.html>
- Gajulapalli--Ghentiyala--Li--Saraogi 2025: <https://arxiv.org/abs/2507.19108>
- Ren--Williams 2026: <https://eccc.weizmann.ac.il/report/2026/118/>
- Cook--Reckhow 1979: <https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf>
- Williams 2025, Theorem 1.1 and Remark 1.6: <https://doi.org/10.1145/3717823.3718225>
- Sibgatullin--Williams 2026, Theorems 1.1 and 2.1: <https://eccc.weizmann.ac.il/report/2026/223/download/>
