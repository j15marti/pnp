# TMR-3/072: Polynomial exact T5 counts on source-recognizable modular-prime triple-incidence graphs

Date: 2026-11-17 16:24 PST (America/Los_Angeles).
Owner: TMR-3 / PNP Time-Space Tradeoffs.
Status: PROVED/EXACT restricted mathematical construction; independent mathematical review OPEN. Finite reference execution: COMPUTATIONAL. P versus NP OPEN.

## Selected source-to-output dependency and falsifiers

**C3-T5-PRIME-CORE-SIGNATURE**: Provide a complete, authenticated polynomial-time exact count on an infinite family of T5 source graphs having no nontrivial directed modules, minimum underlying degree at least three, linearly many cotree cycles and no identical-neighborhood twins. This falsifies the idea that the /071 module-irreducible nonpath quotient must entail expensive computation.

Before checking prior source/corpus and original published literature, four decisive falsifiers were specified:

F1: some triple of distinct hub colors has a common T5 outneighbor, invalidating the two-color palette restriction;
F2: a defective or incomplete incidence graph passes the recognition predicate;
F3: a proper nontrivial directed module exists in the proposed family;
F4: a hidden source acquisition, covering-vertex search, arithmetic, physical head, output, or auxiliary memory cost makes the proposed algorithm superpolynomial.

The implementation addresses F1-F3 with finite tests; the all-size proofs below discharge the declared restricted mathematical claims. F4 is discharged by the same-machine symbolic ledger, not by finite timing experiments.

## Source and fixed target

The fixed target is the five-vertex tournament `R(a,b) iff b-a in {1,3} (mod 5)`. The original instance is the **complete explicit** directed graph, not a graph-selection oracle.

The canonical binary source is `1^n 0 1^m 0` followed by exactly `m` ordered pairs of low-bit-first indices, each of width `w=max(1,bit_length(n-1))`. Thus the authentic bit length `N` satisfies `n,m<=N`. Invalid delimiters, length, binary characters, and endpoint indices are rejected; repeated directed arcs are normalized; loops and opposing arcs give exact zero. The output is the exact nonnegative integer `Z(G)` in binary and YES iff `Z(G)>0`. The code's `count_source` implements this contract.

For integer k>=5, define H_k with k hub vertices and one leaf L_S for each 3-element subset S of hubs, with precisely the arcs i->L_S for i in S, and no others. Set M=C(k,3), n=k+M, m=3M. This is a genuine input family, not a promised graph already in memory.

## Theorem A: exact all-input vertex-cover counter

For every original directed graph G and tau equal to the minimum vertex cover size of its undirected support, there exists one uniform blank-start deterministic locally headed exact counting algorithm with

`T(N)=O((N+1)^10(1+5^tau))` and `S_peak(N)=O((N+1)^3)` writable bits.

First discover a minimum cover C via iterative budgets j=0,...,tau, branching on the two endpoints of an uncovered support edge. This uses at most O(2^tau) search calls including failed budget attempts and polynomial cost per call. Its complement U=V\C is independent. For every one of the 5^tau assignments a:C->Z5, reject if any internal cover arc is violated. Otherwise define for each v in U

`d_v(a)=|{b in Z5: every incident original arc between v and C is respected}|`.

Then

`Z(G)=sum_{a in Z5^C} [a respects G[C]] product_{v in U} d_v(a)`.

Every original assignment restricts to one a and each outside color is independent conditional on a, so the identity is exact, including isolated vertices, disconnected components and unsatisfiable cases. Discovery and every access to the complete adjacency source are charged. Peak graph/cover storage, recursion, loops and exact O(N)-bit integer sums are all concurrent and polynomial. No optimum-cover oracle is assumed. The exponent 10 is a deliberately conservative multitape implementation polynomial, not a measured Python runtime.

## Lemma B: unique pair compatibility

Let Out(a)={a+1,a+3} mod5. For distinct a,b, `|Out(a) intersect Out(b)|` is exactly one if b-a in {2,3} mod5 and zero otherwise; `|Out(a)|=2`. No three distinct hub colors have a common outneighbor, because every possible target has exactly two in-neighbors.

There are exactly five unordered compatible distinct-color pairs, namely `{a,a+2}` over a in Z5. This is a statement in the fixed T5 algebra, not an assumption about general tournament templates.

## Theorem C: polynomial exact counting on a module-prime, high-core family

For k>=5 and G=H_k, the exact original homomorphism count is

```
M = binom(k,3)
Z(H_k) = 5*2^M + 5*SUM_{p=1}^{k-1} binom(k,p)*2^(binom(p,3)+binom(k-p,3)).
```

Here `binom(j,3)=0` for j<3. The all-source algorithm first authenticates the input, constructs in/out neighborhoods and recognizes H_k rather than presuming it. It finds hubs as vertices of positive outdegree, checks that k>=5, n=k+binom(k,3), m=3binom(k,3), hubs have zero indegree and degree binom(k-1,2), leaves have zero outdegree and three *distinct* hub in-neighbors, and checks that the leaf-neighbor triples contain each 3-subset exactly once. Failure goes to Theorem A's exact all-input cover counter. Successful recognition computes the displayed expression by O(k) exact binomial/exponent terms, and emits the exact binary output.

**Proof of count.** Given hub colors, each leaf L_S independently has the number of available colors `|intersection_{i in S} Out(color(i))|`. Because all triples occur, any use of >=3 distinct hub colors generates a leaf with zero possibilities. If all hubs are the same color there are five choices and each of M leaves has two choices, giving `5*2^M`. Otherwise exactly two distinct hub colors are used. Compatibility forces those colors to form one of the five unordered special pairs. For a fixed pair and p of the k hubs of its designated first color (1<=p<=k-1), there are binom(k,p) hub maps. Each monochromatic triple gives two leaf choices and each mixed triple exactly one. The number of monochromatic triples is `binom(p,3)+binom(k-p,3)`. Summing gives the claimed expression without overcounting. Every original leaf color is counted.

**Proof of modular primeness.** A nontrivial directed module M contained solely in hubs is separated by a leaf corresponding to a triple containing one member but not another; a module contained solely in leaves is separated by a hub in the symmetric difference of their triple neighborhoods. Suppose M contains hub i and some leaf L_S. For every triple T containing i, its leaf L_T must be in M, because any such leaf outside M sees different outgoing adjacency from i and from L_S. For any other hub j outside M, choose a triple T containing i and j; j points to L_T in M but not to i in M, violating modular uniformity. Thus all hubs are in M. Every leaf must then be in M because a leaf outside sees different incoming adjacency from an incident hub and an inside leaf. Hence M=V. This proves H_k has no proper module of size between 2 and n-1 for all k>=5.

**Other structural facts.** H_k is connected, every leaf has undirected degree 3, and every hub has degree C(k-1,2)>=6, so the 2-core is all n vertices with minimum degree at least three. It has no directed identical-neighborhood twins. The cycle rank is `r=m-n+1=2C(k,3)-k+1=Theta(n)`. Minimum vertex cover tau=k: the k hubs form a cover, while Hall's condition holds for a matching saturating hubs, since any nonempty set U of hubs has at least C(k-1,2)>=k>=|U| leaf neighbors. Thus the general vertex-cover counter takes 5^k iterations in the loose bound, but the exact H_k recognizer yields polynomial time even though the older forest, Fourier, degree-two, twin and module-quotient *parameter envelopes* are exponentially large.

**Same-realization physical ledger.** Build/validate source, normalize and check arcs, construct and test hub/leaf neighborhoods and triples, compute O(k) binomial coefficients, repeatedly double/shifts O(N)-bit nonnegative integers, accumulate an O(N)-bit result and emit O(N) output bits. No recursive graph expansion, free access, parallel work, preloaded values or uncharged internal buffers occur. With n,m<=N, at most O(N^3) live writable bits and O(N^10) locally headed bit steps conservatively cover all operations; even a simple adjacency-matrix implementation is within the bounds. The universal fast-path selector followed by Theorem A gives

`T(N)=O((N+1)^10)` on H_k, `T(N)=O((N+1)^10(1+5^tau))` on arbitrary source graphs; `S_peak(N)=O((N+1)^3)` on both.

The H_k formula may be easier to compute than 5^k by arbitrary cover enumeration; this is **not** a lower bound on any other representation or runtime. A proof that no small module exists is not evidence against algebraic compression.

## Falsification controls, four gates and boundaries

**DISJ sanity: PASS RESTRICTED.** This is a positive explicit algorithm, no rank/mass-to-work inference. The input bipartite incidence graph is not equated to the DISJ communication matrix.

**Relativization: NOT APPLICABLE WITH REASON** to P versus NP separation (none claimed). The closed combinatorial identities relativize as source-local arithmetic. BGS/algebrization/Natural Proofs restrictions remain for any future separation.

**Simultaneous DTISP: PASS RESTRICTED** for the same completed program's upper time and peak space. No forbidden pair or all-SAT lower-bound transfer is proved.

**Deterministic configuration counting: PASS UPPER-BOUND CONSISTENCY ONLY.** Counting configurations supplies no deterministic work lower bound and no automatic randomized/quantum conclusion.

Horn/2-SAT, affine/Gaussian, bounded treewidth, equality, autarky/product, padding, auxiliary, selector, unique-solution, alternative field/basis, source-dependent recognition and recomputation remain legal. /341 FAIL as full UNSAT authority; /386 RESTRICTED. A quantitative source-bounded 3SAT->T5 reduction, ETH exponent transfer and unrestricted P-vs-NP consequence remain OPEN.

## Actually executed finite reference evidence

CPython 3.13 reference `tmr3-t5-prime-incidence072-v1`, deterministic seed 202611171624, run **twice with byte-identical outputs** in a local container. 117 assertions, including 92 exact comparisons to independent vertex-cover enumeration, two complete module-prime closures for k=5 and k=6, and seven malformed rejections; zero failures. For k=10, n=130, m=360, formula exact answer has 37 decimal digits and SHA256 `e647518813eaf0964785abd75a61ac6ceaa66fd9b71ebd0585100ae20e6f1da0`. Source SHA256 `7ebe8497ccdae7271d0dddd6e2d4670cd39698ad8a4a19dd4985bbff6d7a0ed7`; raw JSON SHA256 `46a3067ac15ab3a7035576f3a7d5e2db9f0853ae8401cd68987f07f94552e125`.

The local Python file was actually executed; native physical TM microcode, independent mathematical review, full LaTeX build, and repository preflight were **not** executed. Checkout via git failed because github.com DNS did not resolve. GitHub connector readback and main-merge status must be reported separately.

## Pinned original reference and next dependency

Bang-Jensen, Hell, and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 281-298 (1988), DOI: https://doi.org/10.1137/0401029. Its NP-completeness classification is for the general fixed-target decision problem. This manuscript adds a constructive, special-family **exact count upper bound**; it does not transfer ETH, SAT time-space lower bounds or prove any P-versus-NP separation.

**ONE next load-bearing lemma: C3-T5-PARTIAL-TRIPLE-INCIDENCE-SIGNATURE.** For a source-recognized general 3-uniform hypergraph incidence family, find a polynomially constructible extension of the two-color-palette quotient (or a rigorously charged counterexample showing that sparse missing triples allow incompatible 3+-color palettes), preserving same-realization time, space and exact output.
