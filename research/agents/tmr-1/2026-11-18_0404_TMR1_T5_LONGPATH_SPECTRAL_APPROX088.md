# TMR-1/088: exact binomial path transfer and certified long-subdivision counting approximation

**Date:** 2026-11-18 04:04 America/Los_Angeles. **Owner:** TMR-1 / PNP Machine Model Lead. **Scientific status:** exact algebraic theorem with finite computational validation; independent mathematical review OPEN; **P versus NP OPEN**. New result is an explicit long-path counting envelope for the exact fixed T5 template, not a general fast algorithm or a new general Fourier technique.

## Source and exact template

The five-symbol target is the regular tournament on Z/5Z with R(a,b) iff b-a is 1 or 3 (mod 5). Its unrestricted homomorphism decision problem is NP-complete by Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3) (1988), 281–298, DOI https://doi.org/10.1137/0401029. The separate project's explicit C5 bridge /080 is compatible with this classification. The present input promise is that a supplied, fully authenticated graph is obtained by replacing each edge of an arbitrary undirected multigraph H with an **internally vertex-disjoint oriented path**. In particular, the underlying skeleton may have arbitrarily high treewidth, density, loops, or parallel edges. An authenticated decomposition is part of the algorithm's input. A rejected or absent certificate cannot be used to infer UNSAT.

## Theorem C1-T5-LONG-PATH-SPECTRAL-DECORRELATION088

For a path of length ell, traverse it from endpoint a to endpoint b. Let p of its arcs be oriented along the traversal and q=ell-p against it, in ANY order. Write T_{p,q}(a,b) for the number of assignments to its ell-1 internal vertices compatible with endpoint labels a,b in Z/5Z. Then

(1) T_{p,q}(a,b) = sum_{k=0}^{ell} binom(ell,k) [p-3q+2k = b-a (mod 5)].

In particular, **the order of forward/backward orientations does not change the transfer matrix**, only the counts p,q do. For every ell>=1 and every a,b,

(2) | T_{p,q}(a,b)/(2^ell/5) - 1 | <= 4((1+sqrt(5))/4)^ell <= 4(13/16)^ell.

Now let H have n vertices (including isolates) and m edges. Replace source edge e by an individually oriented path of length ell_e>=1 with internally disjoint new vertices. Let S=sum_e ell_e and Z be the number of homomorphisms from the resulting directed graph into T5. Define

Q_0 = 5^(n-m) 2^S  (an EXACT rational; 5^(n-m) may be a reciprocal),
delta_e = 4(13/16)^(ell_e).

Then the following unconditional certified rational interval holds:

(3) Q_0 * product_e max(0,1-delta_e) <= Z <= Q_0 * product_e (1+delta_e).

If m=0, Z=5^n=Q_0 exactly. For m>=1, choose any rational 0<epsilon<=1. If the authenticated path lengths satisfy

(4) 8m (13/16)^(min_e ell_e) <= epsilon,

then Q_0 is a DETERMINISTIC RELATIVE-epsilon approximation of Z, i.e.

(5) (1-epsilon) Q_0 <= Z <= (1+epsilon) Q_0.

Condition (4) can be checked in exact integers (no logarithms or floating point): if epsilon=A/B with positive integers A<=B, check 8m B 13^(ell_min) <= A 16^(ell_min). A sufficient closed length bound is ceil(log(8m/epsilon)/log(16/13)). **This does not assert an FPTAS for the fixed class of all long subdivisions at arbitrarily small epsilon.** The allowed approximation accuracy is certified only when the actual finite path lengths meet (4).

## Proof

For a traversal-forward arc the increment generating polynomial is x+x^3=x(1+x^2), and for a traversal-backward arc it is x^(-1)+x^(-3)=x^(-3)(1+x^2). In Z[x,x^(-1)]/(x^5-1), the path product equals x^(p-3q)(1+x^2)^ell. Taking the coefficient of residue b-a proves (1) and order invariance without relying on an unproved independence assumption.

Put omega=exp(2 pi i/5). The fifth-root filter expresses each residue coefficient as (1/5) sum_{j=0}^4 omega^{-j(b-a)} omega^{j(p-3q)} (1+omega^{2j})^ell. The j=0 term is exactly 2^ell/5. For j=1,...,4, |1+omega^{2j}| is either (1+sqrt(5))/2 or (sqrt(5)-1)/2, both at most phi=(1+sqrt(5))/2. The triangle inequality gives an absolute remainder at most 4 phi^ell/5, proving the first inequality in (2). Since sqrt(5)<=9/4, phi/2 <=13/16, proving its rational conservative bound.

Fix a coloring of the n skeleton vertices. Because the substituted paths have pairwise disjoint interiors, the exact number of extensions is the product over edges of the corresponding endpoint transfers. By (2), each factor lies between (2^ell/5)max(0,1-delta_e) and (2^ell/5)(1+delta_e), independently of its endpoint colors. Multiply and sum over the 5^n skeleton colorings to obtain (3). For (4), each delta_e <= epsilon/(2m); hence (1-epsilon/(2m))^m >=1-epsilon/2 and (1+epsilon/(2m))^m <= exp(epsilon/2) <=1+epsilon for 0<epsilon<=1. This proves (5). QED.

## Canonical bits, witness interface and SAME_REALIZATION

Use the existing TMR-1 canonical authenticated bit representation: unary N, delimiter zero, unary M, delimiter zero, followed by lexicographically sorted distinct oriented arcs; low-bit-first fixed endpoint width w(N)=max(1,ceil(log2 max(2,N))). The exact source length is L=N+M+2+2M w(N). For the subdivided graph N=n+S-m and M=S, hence L=n+2S-m+2+2S w(n+S-m), with 3N-bit T5 witness coding if one is requested. Reject malformed binary strings, endpoints outside 0..N-1, duplicate or out-of-order arcs, bad lengths, incomplete headers, and trailing bits before accepting the source.

The decomposition certificate must explicitly identify all skeleton vertices, each ordered path including all internal vertices, endpoint identifications, and each arc orientation. Authenticate that every input arc appears exactly once in the decomposition, interiors are pairwise disjoint and excluded from skeleton vertices, and reconstructed arcs exactly match the canonical source. This is a **promise-algorithm** with a verified decomposition, not an unbounded graph-isomorphism subroutine. A usable source-driven subclass also results from correctly verified maximal-degree-two chain decompositions, as in /087, when all chains meet (4).

Compute Q_0 as a numerator/denominator pair:
numerator = 2^S * 5^max(n-m,0),
denominator = 5^max(m-n,0).
Both have O(L) bits. The rational interval (3) can likewise be written with products of the integer factors 16^(ell_e) +/- 4*13^(ell_e); zero-truncate the lower factors. Their total output bit length is O(L). The threshold (4), input validation, failed checks, exact powering, multiplication, and final writing have a simultaneous conservative standard sequential bit-machine bound O((L+B+1)^8) time and O((L+B+1)^3) peak writable space, where B is the bit length of the rational epsilon plus decomposition. This is an **upper** bound for one complete actual realization and does not imply a lower bound for any other realization.

## Executed finite computational evidence

The full local dependency-free Node.js certificate executed **53,661 assertions with zero failures**, covering all 2,046 orientation words of path lengths 1..10, 51,150 rational exact spectral checks across all five endpoint differences, canonical-bit authentication, five small subdivided multigraphs cross-checked by COMPLETE 5^N direct assignment enumeration, source-malformation controls, and a 200-vertex, 202-arc subdivided K4. The latter has six paths with lengths 33..36 and a certified epsilon=1/10 bound. Exact count:

257110087050244651988479219659283289564203533245146913214300.

Approximation Q_0 is the rational

6427752177035961102167848369364650410088811975131171341205504 / 25,

and the measured relative error is approximately 1.21324653e-10 (this decimal is descriptive only; the certificate checks integer inequalities). A standalone shorter public Node certificate separately executed **20,462 assertions, zero failures**, including all orientation words and the same exact K4 relative-error check. FINITE CHECKS ARE COMPUTATIONAL, not proof of the arbitrary-size theorem.

Full executed source SHA256 e3b9f40134aa5024ec9e0a15026871ee569b7b399c9a063d4f9ebb5b0bd25277; full raw SHA256 371e3cce664d7ecedd1f2b5013f982e86fe908d99811394696f0a78eefd8bf36; shorter independently run public source SHA256 c25e10b736f21ccfaeeb98ee80f55ad4ad970c5372e5a28506b015ef3f32bce7. The full local source and raw are preserved as separate run artifacts. The shorter source is published in the draft branch, and test statistics are published as GitHub raw evidence.

## Scientific limitations and next step

This precise structural result strengthens /087's *existence* guarantee into a certified *counting approximation*. It does not show polynomial exact counting on arbitrary subdivided graphs, or on all T5 inputs; it does not refute NP-completeness and is consistent with the known hard source gadgets containing extra shortcut arcs. All Fourier/flow, binary-cycle, local consistency, Gaussian restricted-class, polymorphism, separator, quotient and compact representations remain legal cheap algorithms. Rank/treewidth/long girth are not computational necessity statements. The general superpolynomial lower-bound implication is absent, so P versus NP remains OPEN. Independent mathematical review, full manuscript LaTeX compilation and formal kernel reconstruction remain OPEN. Next TMR-1 dependency: hard-source YES/NO images that survive verified preprocessing, along with a quantified exact-count boundary under short vs long replaced paths.

No agents were created, duplicated, disabled, rescheduled or immediately rerun. Existing PR #197 remains draft and unmerged.
