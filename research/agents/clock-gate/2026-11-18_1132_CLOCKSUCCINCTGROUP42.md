# CLOCKSUCCINCTGROUP42 | 2026-11-18 11:32 PST

**PROVED/EXACT derived classification in a restricted model; independent mathematics review OPEN. COMPUTATIONAL finite controls. P versus NP OPEN.**

## One load-bearing dependency and four falsifiers

Authentic N=2^n source -> source-independent indexed one-pass transducer -> exact output-aware interval reachability -> two-sided Gap-MCSP source-image separation -> jointly fixed-PH supplied-circuit verifier -> fully charged one-way-input/one-work-tape consequence. This run investigates the **uniform general-index reachability acquisition** arrow left open by CLOCKINDEXOUTPUT40 and CLOCKSPARSEINDEX41.

Candidate (A): arbitrary polynomial-circuit-indexed reachability is uniformly acquirable in polynomial time. Candidate (B): a fixed nonabelian permutation group creates PSPACE-complete uniform reachability with only five streaming states. Candidate (C): the commutator construction works unchanged for the abelian two-state group. Candidate (D): hard uniform root reachability forces source-hard semantic fibers. (B) is established below from classical Barrington + TQBF; (A) implies P=PSPACE; (C) fails for the commutator construction; (D) is **FALSIFIED** for the exhibited source-independent family.

## 42.1 SUCCINCT-S5-ROOT-REACHABILITY theorem

**Model.** Input consists of unary n, a polynomial-size Boolean circuit I:{0,1}^n -> S_5 encoding one of 120 permutations, an initial state 0 and a specified terminal state. The transducer reads each genuine original source bit f_i, i=0,...,2^n-1, exactly once. Transition on either bit is p -> I(i)(p), and emission is epsilon. The source bits are deliberately ignored in this hostile control.

**THEOREM (uniform PSPACE-completeness).** Deciding whether its terminal state equals the requested state is PSPACE-complete under polynomial-time reductions. This also gives PSPACE-hardness of the uniform root query for the exact enriched dyadic interval-reachability predicate in CLOCKINDEXOUTPUT40.

**Upper bound.** Maintain the n-bit counter, the 3-bit state, and scratch to evaluate the explicitly supplied I circuit. Execute all 2^n steps using polynomial space; time need not be polynomial.

**Lower bound, constructive reduction.** Start with a closed prenex quantified Boolean formula Phi=Q1 x1 ... Qq xq phi, with a CNF matrix. Expand quantifiers conceptually to a binary AND/OR Boolean formula with 2^q leaves, one matrix value under each chosen assignment. Fix five-cycles a,b in S5 with commutator c=aba^{-1}b^{-1} also a five-cycle. Every target five-cycle alpha is conjugate to c; choose conjugated a',b' whose commutator is alpha. For any Boolean formula F, define a permutation word W(F,alpha) whose product is ID on false and alpha on true:
- Constant leaf: one ID or alpha instruction.
- NOT F: W(F,alpha^{-1}) followed by alpha.
- F AND G: concatenate W(F,a'), W(G,b'), W(F,(a')^{-1}), W(G,(b')^{-1}).
- F OR G: NOT((NOT F) AND (NOT G)).

Induction verifies the product and length O(4^q) for this bounded-depth expansion. **Uniform indexed access is essential:** the i-th group element can be computed in polynomial time from (Phi,i) without constructing the exponential formula or word. Descend the current quantifier, AND/NOT compilation, target 5-cycle and segment lengths. These lengths depend only on the remaining quantifiers, with O(q)-bit integer recurrences; keep at most q chosen assignment bits. At the leaf, evaluate the original CNF on that assignment in polynomial time. Compile this polynomial-time local index function into a polynomial-size circuit I_Phi, hardwiring Phi, and pad the group word with identity elements to the next 2^n, n=O(q). Hence the product is ID when Phi is false and alpha when true. From initial state 0 these give distinct terminal states, since alpha moves every point. TQBF is PSPACE-complete. QED subject to independent review.

The reduction is derived from Barrington's 1989 width-five permutation construction; no originality claim is made for the group method or general completeness paradigm.

## 42.2 Exact scope and MCSP red-team

This PSPACE-hardness is **uniform across supplied indexed-circuit descriptions**, not an unconditional lower bound on the nonuniform circuit size L_{n,y} of a particular instance's entire indexed reachability relation. It cannot refute CLOCKINDEXOUTPUT40's conditional canonical-section theorem. If someone claimed a polynomial-time universal uniform reachability-construction algorithm for *all* such indexed circuits, this classification would imply P=PSPACE; neither equality nor inequality is assumed.

Most importantly, the constructed transducer **ignores the authentic source f**. Every N-bit source has the same terminal output for each fixed instance Phi. The output fiber therefore contains the all-zero function and, for sufficiently large N, a function of circuit complexity >N^gamma for any fixed gamma<1 (circuit counting). This proves the machine **fails two-sided promise purity maximally**, despite its potentially difficult uniform terminal-reachability question. It supplies no NP/PH verifier, universal NO-source exclusion, efficient decoder obstruction or SAT lower bound. One cannot infer P=PSPACE from P=NP.

## 42.3 Executed hostile finite controls

CPython 3.13.5 standard-library audit, seed 20261118113242, **137 QBF instances** with 0..5 quantified variables and randomly selected CNF clauses. For each, compare an independently recursive QBF truth evaluator with full S5 product, check EVERY position of the compiled sequence against both an explicit and a truly lazy on-demand index compiler, verify identity padding and three different genuine source-bit patterns, enumerate conjugations for all 24 five-cycles, test malformed addresses and all commutators of S2. **121,680 assertions, zero failures**. Longest unpadded group word 2,729 instructions. QBF samples at q>=4 are not exhaustive over formulas. These controls prove neither asymptotic complexity nor physical Turing-machine microsteps and do not measure minimum circuits.

Executed complete local audit SHA256 36e21429a38089c132ea01934e55650199a18049b75f8a951847e131f669dce8. Raw JSON SHA256 08ac9afdd58c9e4118bef2df0a9d0b712b4cb376fb8023c2654ce100a33c4712. GitHub code and JSON publication status must be checked separately; these hashes refer to the expanded executed local source and raw.

## Complete cost ledger and gates

Reduction: charged QBF parsing, n and quantifier assignment bits, polynomial local-instruction generator, integer segment lengths, group-table lookup, circuit compilation and identity padding rule. Execution: N genuine source reads, N index-circuit evaluations, source authentication, state/counter storage, work-tape moves, output and retention; no free streamed word, seeds, forced/oracle answers or short physical clock. Polynomial **space** upper bound does not imply polynomial **time** or an improved simultaneous DTISP pair.

DISJ: NOT APPLICABLE (no rank argument). Relativization: restricted classical reduction only, unrestricted gate OPEN. Simultaneous DTISP: FAIL/OPEN for P vs NP, missing promise-pure source map and same-one-tape transfer. Deterministic configurations: PASS as upper-bound sanity, not a time lower bound. Natural Proofs/algebrization not bypassed. All earlier interpolation, histogram/transcript, hash/seed, Chevalley-Warning, affine/field, parity, provenance, majority, Horn/2SAT and low-certificate guards remain; /341 FAIL full UNSAT authority, /386 RESTRICTED.

**ONE NEXT: PROMISE-COUPLED-REACHABILITY43.** Require transitions genuinely dependent on authentic source bits and demonstrate an actual NO-source-exclusive output. Analyze uniform root access, nonuniform enriched circuit cost, jointly fixed-PH circuit witness verifier and charged one-way single-work-tape composition independently, without conflating them. No TMR-owned root manuscript or schedule changes. P versus NP remains OPEN.

## Primary sources and repository correspondence

[1] Barrington, *Bounded-Width Polynomial-Size Branching Programs Recognize Exactly Those Languages in NC1*, JCSS 38(1):150-164 (1989), https://doi.org/10.1016/0022-0000(89)90037-8 . [2] Stockmeyer and Meyer TQBF PSPACE-completeness (1973), see Stanford Encyclopedia of Philosophy's *Computational Complexity Theory*, https://plato.stanford.edu/archives/spr2026/entries/computational-complexity/ . [3] Cheraghchi et al., *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021, https://doi.org/10.4230/LIPIcs.STACS.2021.23 . Project precursors: CLOCKINDEXOUTPUT40, CLOCKSPARSEINDEX41, SOURCEQUERY_SYNTHESIS10, PUBLICSEED_PLOTKIN14, K_ELIMINATION_TRANSFER4. Latest AGENTS/CODEX/end-to-end directive and pnp-research skill were read. No local Git checkout, hence preflight was not executed. Independent mathematical review OPEN.