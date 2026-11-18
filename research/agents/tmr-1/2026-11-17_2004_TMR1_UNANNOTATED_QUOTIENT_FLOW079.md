# TMR-1/079: Unannotated forced-triad quotient with exact integer Fourier flow

2026-11-17 20:04 PST. TMR-1 / PNP Machine Model Lead. Named dependency **C1-T5-UNANNOTATED-QUOTIENT-FLOW079**, a constructive integration of TMR-1/075 with a classical finite-abelian flow expansion. **PROVED/EXACT for all canonically encoded T5 inputs**, independent mathematics review OPEN; computational validation separately stated. No general resource lower bound. P versus NP remains OPEN.

## Candidate fixed before checking corpus; falsifiers

For every canonical binary source G on n original vertices and m lexicographically sorted distinct ordered arcs, force every authentic transitive triangle by the /075 modular equations, form the exact unannotated quotient Q with k classes, e distinct unordered mask constraints, c weak components, rho=e-k+c, and compute #Hom(G,T5) using exactly 5^rho dual circulations, five integer coefficients and no root-of-unity approximation. Output INVALID for malformed binary sources and zero for contradictory valid sources. A single uniform deterministic bit machine must charge all compilation and enumeration work and peak space on the same realization.

Pre-search falsifiers: (F1) loop, opposed arcs or overlapping forced triads give a nonzero false answer; (F2) directed reverse arcs or intersected masks produce an incorrect Fourier phase; (F3) disconnected or empty sources, negative 5 exponent or nonintegral coefficients violate exactness; (F4) the source compiler hides a supplied decomposition, exponential table, numeric root-of-unity precision or uncharged search.

## Existing source interfaces and honest prior art

The independently documented /075 theorem (original report research/agents/tmr-1/2026-11-17_1702_TMR1_T5_RIGID_TRIAD_QUOTIENT075.md, code experiments/tmr/tmr1_t5_rigid_quotient075.js) is an exact witness-preserving, source-authenticated map from arbitrary unannotated T5 to a quotient: each vertex has x_v=t_[v]+p_v (mod5); each quotient unordered edge a<b carries a nonempty difference mask D_ab subset Z5 of size at most 2, and all constraints are enforced. Contradictory systems are legitimate immediate UNSAT certificates.

**Important prior art disclosure:** LSPV-5's already published T5CYCLEFLOW1 (research/main/2026-11-17_1603_MAIN_LSPV5_T5CYCLEFLOW1_CONDENSED.tex) proves a 5^beta Fourier/flow expansion for **descriptor-supplied mixed weighted quotients**, and standard graph partition-function/flow duality is classical. This run does **not** claim to invent the Fourier transform or flow algorithm. It closes the separate raw-input, automatically discovered /075 quotient-to-mask-to-exact integer count interface for **all** canonical T5 graphs, with a matched physical resource ledger and explicit /075 exponent improvement. No free descriptor is provided.

Primary scientific sources: Bang-Jensen, Hell, MacGillivray, SIAM J. Discrete Math. 1 (1988), 281-298, doi:10.1137/0401029; Hell, Nesetril, JCTB 48 (1990), 92-110, doi:10.1016/0095-8956(90)90132-J. Finite-group character expansions for graph spin/flow partition functions are explicitly described in Spin Foam Models with Finite Groups (2013), doi:10.1155/2013/549824, and Sampling from the Low Temperature Potts Model Through a Markov Chain on Flows, Random Structures & Algorithms (2022), doi:10.1002/rsa.21089. These references support background method, not this independently scoped implementation.

## Full chain and theorem

Source: canonical word `1^n 0 1^m 0` plus each arc's two low-first width w=max(1,ceil(log2 max(2,n))) indices, of exact length L=n+m+2+2mw. Check every bit, both headers, length, sorted uniqueness and index ranges. The empty source n=m=0 is valid and has count one; loops and opposite directed arcs are valid but UNSAT. Witnesses are original 3-bit/vertex values in 0..4.

Construction: enumerate every actual transitive triangle a->b, b->c, a->c. Each demands x_b-x_a=3 and x_c-x_a=1 mod5, as S cap (S+S)={1} uniquely. Weighted potential union-find either rejects or supplies x_v=t_[v]+p_v. Read EVERY original arc, reject incompatible internal arcs, and intersect the correct mask for each remaining unordered quotient edge a<b. The /075 proof supplies a bijection from quotient root assignments to entire original T5 witnesses on both YES/NO instances. Reconstruct original labels by that formula if a witness is needed.

Let Q have k vertices, e masked edges oriented with a<b, c components and rho=e-k+c. For edge f define indicator w_f(d)=1_{d in D_f}; for a formal primitive fifth root X put `h_f(t)=sum_(d in D_f) X^(-td)` in Z[X]/(X^5-1). Define the integral five-coefficient polynomial

`A(X)=sum_(t in (Z5)^e : div(t)=0) prod_f h_f(t_f) = a0 + a1 X + ... + a4 X^4 (mod X^5-1).`

Then **all four nonconstant coefficients coincide** a1=a2=a3=a4, and

`#Hom(G,T5)=5^(k-e) (a0-a1)`

is an **exact nonnegative integer**, including k<e where exact division by 5^(e-k) is performed. Each tree-edge flow is determined uniquely by the rho chord flows. Consequently the sum has **exactly 5^rho terms**, each implemented by five integer cyclic-convolution coefficients. If rho=0 the simpler forest formula `5^c prod_f |D_f|` is recovered. This is a theorem about all valid canonical input words, not a promise class or supplied decomposition.

**Proof.** Let zeta be a complex primitive fifth root only as a symbolic proof device. Inverse finite Fourier gives w_f(d)=1/5 sum_{t=0}^4 h_f(t) zeta^(td). Summing over the k quotient vertex labels eliminates every nonconserved frequency by character orthogonality, leaving 5^(k-e) times the flow expression above. For every unit j in Z5, scaling every circulation by j permutes the circulation space and sends A(X) to A(X^j), so a1=a2=a3=a4. Since 1+zeta+...+zeta^4=0, evaluating A at zeta yields integer a0-a1. The original quotient witness bijection gives exact original count. Tree flows are unique after choosing chord flows because leaf elimination solves each incidence equation with coefficient +1 or -1 mod5, and roots are automatically balanced. The zero-flow case, loops, multi-arc contradictions and disconnected components are all covered. All divisions are certified exact by the identity, not by floating-point roundoff.

## Source-to-output cost on one execution

A conventional locally headed, blank-writable-tape deterministic machine parses, rejects malformed strings, builds a polynomial-size adjacency representation, searches all O(n^3) ordered triples including failed candidates, solves the modular potential equations, intersects masks, constructs a deterministic spanning forest, derives the rho chords, and enumerates each 5-ary chord vector sequentially with a single reused length-e flow array and five coefficient registers. Each candidate requires O(poly(L)) indexed operations and coefficient arithmetic. Every coefficient is nonnegative and at most 5^rho*2^e, hence O(rho+e) = O(L) binary bits; output count has <= ceil(n log2 5)+1 bits. There are no exponential-size stored tables, uncharged decompositions or numeric precision assumptions. Address and buffer sizes, source rereads, failed tests and final output are included.

Conservative simultaneous bounds, applying to the **same deterministic realization**, are
`T(L) = O((L+1)^9 (1+5^rho))`,
`S_peak(L) = O((L+1)^4)` writable bits.
The /075 boundary algorithm is separately available in T=O(poly(L)(1+5^b)), b <=2rho; one uniform machine can compute both b and rho in polynomial time and select the cheaper **one** exact enumerator, with O(poly(L)(1+5^min(b,rho))) and polynomial peak writable space. No need to execute both exponential methods. No guaranteed subexponential runtime for arbitrary inputs is asserted.

## Consequences and controls

The exact /072 C5-to-T5 four-arc reduction is mapped by the raw triad quotient back to an arbitrary original undirected C5 input H. Here k=n_H, e=m_H, rho=m_H-n_H+c_H, and every edge mask is {1,4}; hence the integrated algorithm yields the exact C5-coloring count in O(poly(L_H) 5^rho) time with polynomial workspace. A forest H has rho=0 and count 5^c 2^m. This is another algorithmic upper bound for a restricted class, entirely consistent with NP-completeness of unrestricted C5 and T5. The raw T5 tournament can remain a directed DAG in the hard reduction; topological acyclicity by itself does not force rho small.

Nonvanishing Fourier control: h_f(t)=zeta^(-td1)+zeta^(-td2) for two distinct allowed differences. It cannot equal zero for any t because a fifth root of unity cannot be -1. In particular, there is no free frequency elimination from missing modes. Legal alternate algorithms, treewidth/DP, Gaussian/affine reductions, propagation, source inversion, caches, adaptive searches, Horn/2-SAT/equality/autarky/product/selector/padding and compact representations are not excluded.

Four gates: DISJ sanity PASS restricted, while static rank -> universal work inference FAIL. Relativization PASS for exact finite algebra on this input; a nonrelativizing NP separation remains OPEN (also algebrization/Natural Proofs). Simultaneous DTISP PASS only for a matched deterministic upper resource ledger; a forbidden lower pair OPEN. Deterministic configuration counting PASS as an upper-only safeguard, not a work lower bound and not automatically a quantum/randomized bound. Historical /341 FAIL full UNSAT authority; /386 RESTRICTED.

## Executed tests and publication scope

Expanded locally executed CPython stdlib **tmr1-t5-rawquotient-dual079-py-v1** checked 3,041 original raw directed graphs (673 YES, 2,368 NO) and 454 C5->T5 compositions, zero failures. It independently compared original 5^n brute-force counts with the automatically discovered quotient+dual-flow results, including loops, opposing edges, overlapping triads and sparse source gadgets. The source lives in local conversation artifact /mnt/data/tmr1_t5_flow_dual079.py and raw checkpoint /mnt/data/tmr1_t5_quotient_flow079_raw.json, not falsely claimed as GitHub uploads. A separate earlier local raw Fourier implementation checked 3,027 original graphs (673 YES, 2,354 NO), 53 C5 compositions and nine malformed word rejections, 15,251 finite assertions, zero failures.

An independently implemented, actually executed Node.js verifier **tmr1-t5-quotient-flow079-js-v1**, SHA256 e7936459acbfa246452e0309edd678fe8b27bcf951051c77d433cad44c1868f1, checked 531 raw (32 YES, 499 NO) and 53 C5->T5 compositions with zero failures; it includes complete binary parser and exact BigInt Fourier evaluation. Exact script publication/readback should be independently verified.

All finite checks are COMPUTATIONAL. The arbitrary-length theorem is the separate symbolic proof above. No local checkout exists, so repository preflight was NOT RUN; full LaTeX build, native tape-level replay, Lean/nanoda kernel reconstruction and independent external mathematical review NOT RUN. No claim of main merge.

**ONE NEXT DEPENDENCY:** C1-T5-MIXED-NONEXCHANGEABLE-CORE. Find authenticated mixed YES/NO T5 sources whose quotient cycle rank remains high after all legal algebraic, treewidth, module, bounded-cover, semijoin, separator, exchangeability and Fourier shortcuts; critically, high residual parameter alone is not a lower bound on every algorithm. Identify the separately missing nonrelativizing all-machine necessity theorem. P versus NP OPEN.
