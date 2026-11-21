# Synthesis of authenticated WRAPPER quotients and counting pseudoentropy

2026-11-21 12:22 PST, America/Los_Angeles.
Source snapshot 24ee7d3860adcf7d2fe51428babd7a82b2d77fcb.

**T5-QUOTIENT-SIDEINFO1 — PROVED/EXACT as a distributional transfer lemma.** Normalizing a count by its authenticated equality multiplier preserves conditional entropy when the full encoded input remains available. Replacing that input by a recovered quotient gives a one-way distinguishing reduction and can strictly increase conditional entropy. A reverse reduction needs a paid common reconstruction kernel for both joint distributions. This supplies the missing condition for using the WRAPPER quotient as an equivalent pseudoentropy problem.

External independent adversarial review is pending. The proof below is direct. The target-specific indistinguishability premise and every unrestricted lower-bound consequence remain CONDITIONAL or OPEN. No peer report is retracted. The earlier Synthesis normalization theorem retained the full input and remains valid.

## Quantifiers and target

For each original encoded length N, let Gamma_N be a declared subset of valid symmetric strict-C inputs for which a fixed deterministic recovery procedure h returns H=h(X). H contains an explicitly encoded strict-C quotient G, its size fields, the actual number E of certified equality links, and any chosen retained metadata. Choose a fixed padded length L(N) for H. Sorting clause entries is permitted for symmetric C. Relabeling the quotient may depend on the procedure's tie breaking; no graph canonization oracle is assumed.

Assume recovery proves, on Gamma_N, F_N(x)=2^{E(x)} f(H), where f(H)=Z(G). More generally any known positive integer multiplier works with the same proof. For split sources all original variables must occur or their free-variable factor must be explicitly retained. This report uses the former promise. E is recovered from verified packets, not inferred by applying a specialized graph-header formula to every input.

For EVERY distribution X on Gamma_N and EVERY joint fake raw count W supported on
    W=2^{E(X)} V,  0<=V<=5^{n_G(X)},
write U=f(H). Counts are padded to ell=3N bits, enlarging that fixed length if a different declared quotient representation requires it. In the actual equality contraction n_G<=n_X<=N, so ell suffices. Every circuit uses fan-in-two AND/OR, unary NOT, constants and unrestricted fanout/sharing. Adv_B denotes the maximum absolute distinguishing advantage over circuits with at most B noninput gates.

Fix separately one total correct deterministic strict-C counter A on the input-charged fixed-alphabet sole-tape model, constants K>0,a>=1 independent of input, and proposed T_A(N)<=KN^a. Use a=2 as a concrete cap comparison. The counter, recovery algorithm, circuit generator and sampler are distinct executions. The theorem does not require A to run h.

C contains all 30 permutations of 012,123,234,340,401 on Z5, with distinct names per clause and full initial domains. The ordered 40-tuple R, whose first argument wins once and loses once, is distinct. No R conversion or S/Q substitution occurs. Throughout,
    N=n+2+2 floor(log2(m+1))+3m ceil(log2(n+1)).
H's size L and the source circuit size never replace N in the cap.

Four concrete falsifiers are a recovered packet with a nonconstant fiber, a fake outside the claimed multiplier support, an entropy equality that changes conditioning from X to H, or a reverse sampler that reproduces only the source marginal while destroying its correlation with V.

## The proved transfer

Let delta_N bound the Boolean circuit computing (h(x), w/2^{E(x)}) on the promised support, including recovery, authentication, address selection, exact shifts and output. For every b>=0,
    Adv_b((H,U),(H,V)) <= Adv_{b+delta_N}((X,F_N(X)),(X,W)).
Compose any quotient test with this circuit. This is a literal equality of the two acceptance differences before taking maxima. Uniform h gives uniform circuit construction when its implementation and resource bound are supplied. The statement also applies to nonuniform circuits.

For Shannon entropy and average conditional min-entropy respectively,
    H(W|X)=H(V|X)<=H(V|H),
    Hbar_inf(W|X)=Hbar_inf(V|X)<=Hbar_inf(V|H).
The first equalities hold because, for each fixed x, multiplication by 2^E is injective on the stated support. For Shannon, the increase is exactly I(V;X|H). For average min-entropy write the guessing probability as
    p_guess(V|X)=sum_x max_v Pr[X=x,V=v].
Since H is a function of X,
    sum_h max_v sum_{x:h(x)=h} Pr[X=x,V=v]
    <= sum_x max_v Pr[X=x,V=v].
Apply minus log. No pointwise-min-entropy or expectation-of-log substitution is used. U and F_N(X) are deterministic given H and X respectively, so their conditional entropies are zero.

The reverse direction holds under the following explicit extra hypothesis. There is a circuit kernel K_N(h;r), with r an independent uniform string of a fixed worst-case length, such that
    (K_N(H;R),H,V) has exactly the law of (X,H,V).
This one identity includes h(K_N(H;R))=H on support, the correct conditional source distribution, and V conditionally independent of the reconstructed presentation given H. Since U=f(H), the same kernel reconstructs the true joint law as well. Let rho_N pay for K_N and multiplication by the E recorded in H. Then
    Adv_b(raw true,raw fake) <= Adv_{b+rho_N}(quotient true,quotient fake).
The composed test uses randomness. Its signed acceptance difference is an average over seeds, so some fixed seed has absolute difference at least that average's absolute value. Hardwiring that seed proves the inequality for the nonuniform circuit class. This argument does not provide a uniform algorithm for finding the seed.

Under the common-kernel hypothesis V is conditionally independent of X given H, so both conditional entropies are equal before and after dropping presentation. If a kernel approximates each of the two joint distributions to total variation eta, the reverse inequality gains at most 2eta. Entropy equality is asserted only for the exact hypothesis.

Consequently a quotient pair with Hbar_inf(V|H)>=k and (B,epsilon) indistinguishability transfers to the raw pair at budget B-rho_N and the same k under the exact kernel. Comparing with an exact count circuit and a 3N-bit equality comparator yields
    C_F(Gamma_N) > B-rho_N-O(N)
whenever epsilon<1-2^{-k}. A sufficient fixed-cap exclusion requires
    B-rho_N-O(N)=omega(N^a log N).
Neither B nor the required indistinguishability is established here. With approximate reconstruction use epsilon+2eta<1-2^{-k} and separately justify any entropy loss. The forward inequality alone cannot justify this reverse hardness conclusion.

## Smallest nonempty strict-clause conditioning control

Let X choose fairly between the two encodings of C(x0,x1,x2) and C(x1,x0,x2). They have n=3,m=1,N=13, no equality links, and exactly 30 satisfying assignments. Let h sort the clause's names, so H is constant and E=0. Set V=0 on the first presentation and V=30 on the second. These are permitted count-range values and lie on the multiplier lattice. Then
    H(V|X)=Hbar_inf(V|X)=0,
    H(V|H)=Hbar_inf(V|H)=1.
Erasing presentation creates one ordinary conditional entropy bit. A kernel that picks either presentation independently of V has the correct X marginal but the wrong (X,V) law. It assigns probability 1/4 to each of four pairs; the actual law has only two pairs of probability 1/2. Their total variation distance is 1/2.

This is minimal in variables and clauses among nonempty strict-clause sources, since a strict clause needs three names. It is a counterexample to entropy-preserving quotient claims, not a claim of computational indistinguishability. Equality to 30 distinguishes the true and fake outputs with advantage 1/2. If V is instead independently fair on {0,30}, the common reconstruction kernel is valid and both conditional entropies equal one.

## Reconciliation and dependency graph

All report paths below were recovered at the source snapshot. Their existing review status is preserved.

| Role and exact source | Established result used here | Remaining implication |
|---|---|---|
| Construction, 16db13effd093c0df7ce104b3c117ec570be7c7c, positive-offset report | PROVED/EXACT peer reduction Z(B-)=2M #H and Z(B+)=M(2^p+#H), same target n,m,N. Full-domain occurrence-five clauses. | SAT(B-) iff SAT(H). B+ always SAT. No compulsory core work follows from the reduction. |
| Accounting, 9f6787be1c19431c5848f0cc44f8e3ccd4b4a75c, orientation report | FALSIFIED/RETIRED auxiliary independent orientations as decodable obligations even from a complete deterministic trace. | OPEN actual source-dependent core service exceeding brKN^a plus metadata. |
| Discovery, 899d207c4f94559db08d730d588de99bce3b055b, extremal closure | PROVED/EXACT restricted constant handles from authenticated Boolean counts 0 or 2^scope; unpruned fixed-scope view compiler. | OPEN paid certificate coverage for arbitrary scalar solvers. Typed node bounds are unrelated to the raw count-circuit target without a bridge. |
| Bounds, f39c4a081ce8a42a5ba8ee0bdb939f9197f747bf | PROVED/EXACT falsifier of the two canonical positive images, advantage 1/2 at <=12N+3 gates despite equal output marginals. | OPEN a genuine jointly indistinguishable fake. |
| Redteam, 064577d8c8fab8b11d167928cb8ed93dde801b38 | PROVED/EXACT scoped packet contraction and arbitrary-presentation attack O(N log²N) on that pair. NOR/implication examples have matching full path histograms and different counts. | External adversarial review pending; higher incidence information on the latter pair remains to test. |
| Earlier Synthesis, 4c1d7f5ef16531313c82bd7a888fca03edd3f4f3 | PROVED/EXACT multiplier normalization preserving full X, O(N log N) gate loss on its graph image. | Its weighted graph parameters differ from the later unweighted and circuit families. No unconditional preservation after erasing X. |
| This report | PROVED/EXACT one-way quotient transfer and conditional reverse transfer with a common paid kernel. | OPEN the target-specific pair and reconstruction budget needed for a separation. |

Dependency graph, with each arrow carrying the assumptions above:
    exact equality fibers -> authenticated quotient and multiplier
    -> forward test composition (proved)
    -> reverse hardness transfer (requires common paid kernel)
    -> count-map lower demand (requires quotient indistinguishability)
    -> fixed-A cap contradiction (requires demand above same-N ceiling).

The separate decision branch runs from the negative twin reduction to an OPEN decision progress theorem. The typed completion and dynamic accounting branches remain separate. No sum or product of their demands is asserted. The strongest construction advance is the explicit same-length positive/decision pair. The strongest recent adversarial advance is the keyless structural distinguisher. Both have precise scope and pending external review.

## Resource ledger and controls

Parsing and authentication must read the actual unary/gamma/ID fields and certify the six-clause packets, disjoint private variables, copy paths, and core occurrence coverage. The exact packet relation is 2[u=v]; hash equality alone cannot certify it. General h must emit its recovered quotient and E and pay for all rejected matches, tie choices, scans and caches. A failed operational check returns UNKNOWN and falls back to a correct solver. This proof of distributional composition does not assume a free recognizer or a tight universal recovery bound.

Delta_N and rho_N are gate counts of those complete functions. Their wire descriptions cost O((delta_N+rho_N+N+L) log(delta_N+rho_N+N+L+2)) bits. The earlier O(N log N) arithmetic converter pays only for header-driven multiplier normalization on its promised image. The O(N log²N) Redteam selector reads constant-radius information on its particular slice. Neither bound is silently assigned to full quotient extraction or to a common presentation sampler. Variable E requires a paid barrel shift; fixed E permits wiring. Missing multipliers, discarded free variables, modular/floored division, overflow and arbitrary fake counts invalidate the interface.

On an actual tape run retain input, addresses, buffers, current quotient, certificates, random seed if used, arithmetic words and output simultaneously. Sharing pays once for a retained result; deletion followed by regeneration is charged again. Adaptive changes and failed candidate recognizers belong to the same run. No virtual residual queries, clock, source access or externally sampled witness bits are free. Uniform generation of the circuit, its serialization and evaluation are additional tasks. An exact uniform permutation sampler can have an unbounded random-bit rejection tail; it does not satisfy the fixed worst-case seed premise automatically. A bounded approximation requires the stated eta accounting.

For the same fixed A,K,a,N the ledger remains S=O(N^a), physical CM=O(N^(2a)), input-charged minimum-description CM=O(N^(a+1)), and count-map gates O(N^a log N). At a=2 these are N²,N⁴,N³ and N²logN. Conditional transfer must subtract the actual rho_N, even if it is polynomial. No fixed exponent is excluded here and defeating one exponent would not exclude every polynomial.

Full-state entropy of the true deterministic answer is zero. Affine/Tseitin algebra, matching cycles, private-leaf tree recurrences, forced domains, compact evaluators, complements, caching and renaming remain permitted. A semantic quotient can expose those cheap cases. Relocation changes physical accesses and never forces a revisit of original cuts. Decision-witness packing does not turn auxiliary fibers into compulsory output. The small counterexample is all SAT and proves a conditioning failure only. The equality contraction also preserves zero on UNSAT, but that fact gives no decision lower bound.

DISJ is not applicable because no communication partition is used. Relativization supplies no barrier bypass; the probability identities are ordinary data processing. Simultaneous DTISP is preserved by keeping each implementation separate. Deterministic configuration counting is a consistency upper bound, never the initial lower demand. Natural Proofs and algebrization barriers are not resolved.

## Evidence, searches and next dependency

New standalone code experiments/t5_synthesis_quotient_conditioning_20261121.py and raw results/raw/t5_synthesis_quotient_conditioning_20261121.json enumerate 125 colorings for each of two legal encodings and all 35 denominator-four laws on two presentations and two values. Exact rational guessing probabilities verify the conditioning inequality and strict failure of equality. These finite controls supplement the symbolic proof. The common-kernel proof is mathematical, with no claim of a general sampler implementation. Previous WRAPPER, multiplier and count suites were not rerun.

Recovered the complete baseline, assignment, AGENTS, CODEX, repository research instructions, all six handoffs, original reports, issue324, Redteam's source/raw, and the actual positive construction generator. Baseline a886f3387a8676b9cc86afbf3bebf22630109d49 is an inherited theorem source under its hypotheses. Connected recovery and a scratch experiment were used; there is no complete checkout and no repository preflight or LaTeX build. Scientific reconstruction within this continuous assistant session is not external independent review.

Fresh queries targeted “conditional pseudoentropy deterministic functions side information data processing” and “average conditional min entropy conditioning Dodis Ostrovsky Reyzin Smith.” Read Vadhan–Zheng, March 8 2013 ECCC revision3, Definitions2.6–2.9, and DORS arXiv cs/0602007v4, section2.4. They distinguish joint conditional pseudoentropy from entropy alone and define average guessing entropy. The Vadhan–Zheng sampling equivalence requires a polynomial-size output alphabet and is not imported for the exponential count alphabet. The proofs here use direct composition and the elementary max-of-sums inequality. [Vadhan–Zheng](https://salil.seas.harvard.edu/sites/g/files/omnuum4266/files/salil/files/eccc2013.pdf), [DORS](https://arxiv.org/pdf/cs/0602007).

Fresh official GitHub query '"conditional entropy" "data processing"' in anthropics,openai,xai-org,google,google-research,google-deepmind. Anthropic and xAI initially returned429, then no matches on retry. Google, Google Research and DeepMind returned no matches. OpenAI/math at4eaee87548250b2682affda7d05d947c05554bae returned a quantum-entropy bibliography and a directional-zero-one-law entropy proof excerpt. These do not establish the required strict-T5 common kernel and were rejected as theorem imports. No external repository code or kernel build was used. Official owner identities retain the earlier verified corporate-domain/official-release crosslinks in the recovered Redteam search log; repository matches were restricted to those exact owners. The bounded query has no exhaustive absence implication. [OpenAI result](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/A-directional-zero-one-law-under-strict-ellipticity-September-23-2026/build/05-entropy.tex).

ONE next dependency, Bounds owner with Redteam review and Synthesis tracking: **T5-COMMON-PRESENTATION-KERNEL1**, specify H and a fake on the NOR/implication candidate or another declared family, then prove a common reconstruction kernel with explicit rho_N and joint-law error. Alternatively supply a legal presentation-dependent fake that defeats the intended kernel. This is a prerequisite for treating erased WRAPPER presentation as a free reduction in the next pseudoentropy argument.

P versus NP remains OPEN.

