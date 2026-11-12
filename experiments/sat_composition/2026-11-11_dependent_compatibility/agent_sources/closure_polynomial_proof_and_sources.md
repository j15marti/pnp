# Closure polynomials for Horn and 2-CNF formulas with affine constraints

## Status and scope

The implementation in `../closure_parity.py` is a complete exact solver when run without a resource cap. Its running time is polynomial for every fixed rank of the additional affine system. It is not a general polynomial SAT algorithm. A resource-cap exit is `UNRESOLVED`, never an unsatisfiability conclusion. The tractability theorem and sparse-polynomial mechanism have established prior art [1–3]; no novelty claim is made here.

The proof below was independently checked against the source, and an independently written truth-table validator tested both public APIs. The proof is more general than the implication-only special case: it applies to any explicitly given Horn CNF, including positive facts, arbitrary antecedent sizes, and clauses with no positive head.

## 1. Least-model closure

Let H be a Horn formula on n Boolean variables. Identify an assignment with its support T, a subset of [n]. Let R be the family of satisfying supports. If R is empty, report UNSAT. Otherwise R is closed under intersection.

For each S subset of [n], define cl(S) as the intersection of all models T containing S. If no such T exists, define cl(S)=bottom. Whenever cl(S) is not bottom, it is itself a model, is the least model containing S, and can be found by Horn forward chaining with the variables in S pinned to one. Positive clauses with no antecedents are facts; a negative clause is a rule whose head is contradiction. An implementation with antecedent counters processes each rule incidence at most once per closure call.

For every model T and every S,

    S subset T  iff  cl(S) is not bottom and cl(S) subset T.

Consequently, the squarefree monomial x_S, viewed as a function on R, is zero if cl(S)=bottom and otherwise equals x_cl(S). This is an exact equality of functions on the full model set, not an abstract approximation.

The constant function is x_cl(empty). Its canonical key need not be the empty set because H can force variables to one.

## 2. Canonical closed-set monomials are linearly independent

For every T in R, define f_T(U)=1 if T subset U, and zero otherwise. Order the finite set R by nondecreasing cardinality, breaking ties arbitrarily. The evaluation matrix with row U and column T has entries 1[T subset U]. It is lower triangular with all diagonal entries equal to one. Thus it is invertible over every field, including GF(2).

It follows that the functions f_T form a basis of all functions R -> GF(2). Distinct closed, consistent keys are therefore independent. A polynomial reduced by the closure rule represents the zero function on R exactly when every coefficient has canceled.

Multiplication has the exact rule

    f_K f_L = f_cl(K union L),

with a bottom result interpreted as zero. For implication-only Horn formulas, the union of two implication-closed sets is already implication-closed, so one only checks conflicts. For arbitrary Horn formulas, union alone is insufficient: a rule with several antecedents can fire only after the union. The general Horn API correctly runs closure on that union.

## 3. Affine-system indicator and direct witness

Reduce the affine system A x=b by Gaussian elimination. An inconsistent system is UNSAT. Otherwise retain d independent rows a_j x=b_j, where d is the rank and hence d<=n.

Over GF(2), define

    P(x) = product_{j=1}^d (1 + b_j + a_j x).

For Boolean x, every factor is one exactly when its corresponding parity equation is satisfied. Thus P(x)=1 exactly when all affine equations hold. Multiply the factors in the closed-set basis, combining equal keys by XOR. H AND (A x=b) is satisfiable exactly when the resulting dictionary is nonempty.

Witness construction requires no additional SAT calls. Choose an inclusion-minimal surviving key K, for example one with minimum cardinality. On the assignment 1_K, a surviving term f_L is nonzero only when L subset K. Minimality implies that the only such surviving key is K itself. Its coefficient is one, so P(1_K)=1. Also K is a Horn model by construction. Therefore K is a satisfying witness for both parts.

For a 2-CNF formula F, first find any satisfying assignment a by ordinary 2-SAT. Substitute x=a XOR y. All-zero satisfies the translated formula. A nontrivial translated clause consequently has a negative literal and is a negative unit, implication, or pairwise conflict. This is Horn, and the parity right-hand sides become b+A a. The witness in the original coordinates is a XOR 1_K.

## 4. Degree bound concerns generators, not key cardinality

Before closure canonicalization, the product of the first j affine factors is a polynomial of degree at most j. After Boolean multilinearization, each monomial is indexed by a set S of size at most j. Each nonzero canonical key is cl(S) for at least one such S. Hence the number of distinct possible keys at stage j is at most

    D(n,j) = sum_{i=0}^{min(j,n)} binomial(n,i).

The same bound applies to the temporary output dictionary while processing a prefix of the products at stage j. Every generated output key still has an originating seed of size at most j. Its closed support may be much larger. For example, in an implication chain x1 -> x2 -> ... -> xn, cl({1}) contains all n variables even though the generating monomial has degree one.

An equivalent constructive corollary is useful: if a degree-at-most-d polynomial is nonzero somewhere on a Horn model set, then it is nonzero on cl(S) for some seed |S|<=d. Thus one can also enumerate all such seeds, compute their least models, and directly test the affine rows. That simple enumeration has the same worst-case fixed-d XP bound. The sparse polynomial implementation can save work when canonical terms cancel or merge.

Streaming this seed enumeration also gives a polynomial-space reference algorithm. Keep the current seed, its closure, the original Horn/2-CNF data, and the affine rows, and discard unsuccessful closures before advancing. The number of iterations is D(n,d), but the number of simultaneously stored assignments remains polynomial. A global cache of all seen closures must be avoided for this space guarantee. This seed-generation technique is already present in the `FindMinimal` approach of [2]; it is not a new tractability theorem.

## 5. Actual live-term cost and cap semantics

Let B_(j-1) be the number of surviving keys after stage j-1. Let F_j be the number of surviving keys in the canonicalized jth affine factor. The factor has at most n+1 raw terms, so F_j<=n+1. The current source generates exactly B_(j-1)*F_j candidate products at that stage, unless it exits on a cap. Its factor-building work also visits every nonzero coefficient of that row.

Canceled products must still be charged. Final B_j does not bound the work that created and then canceled its terms. The temporary output dictionary can have as many as B_(j-1)*F_j keys before cancellation, bounded independently by D(n,j). With polynomial time per closure, consistency check, integer operation, and dictionary/sorting operation, a safe bound is

    poly(N) * (1 + sum_j (n+1) B_(j-1)),

where N includes the explicit source and n variable slots. In particular this is poly(N)*D(n,d). If B=max_j B_j denotes completed-stage sizes, temporary polynomial storage is at most O(nB) keys in this bound. That n factor cannot be dropped merely because the next completed dictionary is small.

The implementation's term cap instead applies to each individual current/factor/output polynomial at every insertion, including temporary prefixes. It may halt before a later cancellation would reduce the size. This is sound because the result is UNRESOLVED. Its `peak_live_polynomial_terms` counter sums the sizes of the active polynomial sets. Sorted iteration lists, source data, closure arrays, dictionaries, Python object overhead, and n-bit integer costs are additional storage/work. The counters are implementation events, not a full bit-machine complexity ledger.

Affine row order and the chosen independent row basis can change actual intermediate sizes. The measured live-term width is an execution property, not a demonstrated basis-independent structural invariant.

## 6. Why affine-hull exchange is incomplete

Take six variables and let H contain every pairwise at-most-one clause:

    H = AND_{1<=i<j<=6} (NOT xi OR NOT xj).

Let A impose odd parity separately on the two triples:

    x1 XOR x2 XOR x3 = 1,
    x4 XOR x5 XOR x6 = 1.

The conjunction is UNSAT: each triple requires at least one true variable, but H permits at most one overall. Nevertheless, the affine hull of H is the full cube, since its models include zero and every unit vector. Every one- or two-coordinate projection of A is full, so its strongest 2-CNF consequence is TRUE. Alternately communicating all affine consequences of the 2-CNF component and all bijunctive consequences of the affine component reaches a nonempty fixed point immediately. This refutes that precise separate-summary exchange procedure. It does not refute stronger mixed propagation or the exact closure algorithm.

For a nonempty translated 2-CNF model set, the degree-one closed-set argument also shows that all affine consequences are generated by fixed coordinates and pairwise equality classes. In original coordinates these include disequalities. This gives a direct explanation of why affine-hull reasoning can be exact for one parity yet incomplete for several.

## 7. Prior art and exact scope

[1] V. Arvind and Venkatesan Guruswami, *CNF Satisfiability in a Subspace*, IPEC 2021. Theorem 2 gives a deterministic O*(sum_{i<=d} binomial(n,i)) algorithm for 2-SAT on an affine subspace of codimension d. Theorem 17 describes the deterministic variable-plucking construction. The full version also explains back-substitution of the eliminated equations to recover a witness. Conference Theorem 19, full-version Theorem 22, gives W[1]-hardness by codimension. W[1]-hardness excludes an FPT algorithm only under the additional assumption FPT != W[1]; it does not exclude polynomial time for each fixed d. The algorithms and the hardness reduction do not require ETH.

- https://drops.dagstuhl.de/storage/00lipics/lipics-vol214-ipec2021/LIPIcs.IPEC.2021.5/LIPIcs.IPEC.2021.5.pdf
- https://arxiv.org/pdf/2108.05914
- Retrieved refs: turn13view0, turn15view0, turn17view0.

[2] Joshua Brakensiek, Sivakanth Gopi, Venkatesan Guruswami, *CSPs with Global Modular Constraints: Algorithms and Hardness via Polynomial Representations*, arXiv:1902.04740; journal DOI 10.1137/19M1291054. Section 3.1 uses `FindMinimal`, the least Horn model containing a seed. Section 3.2 explicitly states n^{k(M-1)+O(1)} time for Horn formulas with k modulo-M linear equations when M is a prime power. Setting M=2 gives n^{k+O(1)} for parity constraints. Section 5 treats 2-SAT with finite abelian-group constraints and notes an n^{O(k)} improvement for GF(2)^k. The present Horn tractability conclusion is therefore established prior work.

- https://arxiv.org/pdf/1902.04740
- https://epubs.siam.org/doi/10.1137/19M1291054
- Retrieved refs: turn28view1, turn30view0, turn30view1.

[3] Monaldo Mastrolilli, *The Complexity of the Ideal Membership Problem for Constrained Problems over the Boolean Domain*, SODA 2019; revised arXiv:1904.04072v2, March 2021. Theorem 1.2 proves n^{O(d)} ideal-membership algorithms for Boolean languages preserved by Majority, Min, or Max. Section 2.2 explicitly permits an arbitrary field. Especially relevant is Lemma 5.5: for Min-closed languages, ideal membership for a polynomial with k ordinary monomials is decidable in (kn)^{O(1)}, without degree dependence. Its proof cancels equivalent monomial pairs or vanishing monomials. That is direct prior art for the sparse canonical-key mechanism here, even though this implementation computes explicit least-model closures.

- https://arxiv.org/pdf/1904.04072
- https://epubs.siam.org/doi/10.1137/1.9781611975482.29
- Journal DOI: 10.1145/3449350.
- Retrieved refs: turn29view0, turn29view1, turn30view2, turn31view0.

## 8. Recovered project corpus

The actual locally available source is `/workspace/scratch/34de249328b4/recovered_repo/main.tex`; most historical reports named inside it were not present in this partial snapshot. The following earlier entries substantially overlap the current work:

- ARC223: independent affine interface, with distinct nonzero observed coefficient rows independent after quotienting the affine core.
- ARC224: cyclic affine core of rank h, solved by enumerating 2^h core assignments and then 2-SAT on coloop coordinates.
- ARC225: projected codimension at most one, using 2-SAT with one parity equation.
- ARC227: one-parity affine-hull construction from minimum meet-generators, with a principal-upset incidence-matrix argument. This already contains the degree-one version of the closed-set basis insight.
- ARC228: explicit correction that all fixed codimensions, including two, are polynomial by Arvind–Guruswami. It also corrects an interface that had omitted unary constraints. Units must be included or substituted and the interface recomputed.
- ARC229: recognized bijunctive edge messages.
- ARC233: polynomially discovered block-cut decomposition with bounded local affine rank.

No explicit general-Horn sparse closure-polynomial solver was located by keyword audit of the recovered `main.tex`, `proof1.txt`, and `proof2.txt`. That is a statement about these available files, not a novelty claim or a complete audit of absent historical reports.

## 9. Independent validation

Engine SHA-256 at validation:

    9adfc46f465debb1d1e104c0a682f8057dc74edc30eb2e8ba308420dc88f4193

The independently authored `validate_closure_solver.py` does not import internal solver routines. It enumerates all truth assignments directly and constructs canonical definable model relations independently.

- Every 2-CNF relation and every affine relation on 0–3 variables: 8,844 instances, PASS.
- Every Horn relation and every affine relation on 0–3 variables: 6,532 instances, PASS.
- 700 larger randomized and resource-capped 2-CNF cases: PASS.
- 700 larger randomized and resource-capped Horn cases: PASS.
- Structured affine-hull/2-CNF fixed-point counterexample, a one-generator closure of size nine, zero-variable SAT and UNSAT controls: PASS.
- Source review confirms positive facts, multi-antecedent closure, the minimum-cardinality witness rule, and the advertised cap behavior.

These are finite validation results supporting the implementation, alongside the mathematical proof. They do not replace an all-input proof or establish a general polynomial bound.

## 10. Streaming seed reference implementation

The separate `../seed_parity.py` implements the polynomial-space seed enumeration described in Section 4. It leaves the sparse polynomial engine unchanged. Its Horn closure uses repeated rule scans, and its Gaussian reduction uses an independently implemented highest-pivot echelon routine. The 2-CNF wrapper reuses only the polynomial engine's public call with no affine equations to obtain a base 2-SAT model. The source stores no global seed table or cache of distinct closures. The `seed_cap` limits attempted seeds, not preprocessing or elapsed time.

Source SHA-256:

    2b8db485931551713d27e0539d49f6afae8f7706174a684da7e6250e0143163e

The independent `validate_seed_solver.py` passes all 15,376 exhaustive relation pairs from Section 9, plus 1,400 randomized/capped cases and structured controls. It additionally verifies every returned seed certificate by intersecting all truth-table models that contain the seed, after accounting for the 2-CNF coordinate translation. Thus the reported witness is independently confirmed to be the least model containing that seed, and the seed size is checked against affine rank. Seed-cap counts are checked directly. The raw output is `seed_validation_results.json`.

Source review confirms the polynomial-workspace claim: it retains only input/preprocessing data, the current combination, current closure, counters, and a witness. The numerical count of all seeds has at most n+1 bits, despite possibly being exponential in n. As before, this is an implementation of the established bounded-seed `FindMinimal` technique [2], not a new theorem.
