# TMR-1/071: exact C5-to-T5 edge gadget and reverse parsimonious 3CNF compiler

Date: 2026-11-17 13:17 PST. Owner: TMR-1 / PNP Machine Model Lead.
Status: C1-T5-C5-FOUR-ARC **PROVED/EXACT (symbolic), independent external mathematical review OPEN**; finite verification **COMPUTATIONAL**; T5 NP-completeness **KNOWN THEOREM**; P versus NP **OPEN**. This is an additive source-model result. The prior Anthropic/Lean and E^NP conditional material is retained as historical Track C evidence, not promoted or discarded. No scheduler or peer manuscript changes.

## Candidate, quantifiers and falsifiers (selected before primary-source and corpus inspection)

Candidate C1-T5-C5-FOUR-ARC: for every finite loopless simple undirected graph H with n explicitly enumerated vertices and m canonical edges, construct an actual directed source D(H) using exactly n+2m vertices and 4m directed arcs. For each H-colouring f:H->C5, exactly 2^m satisfying T5 colourings of D(H) extend f, and no non-C5-colouring extends. Thus #Hom(D(H),T5)=2^m #Hom(H,C5), with both sides interpreted as original-label assignments.

Falsifiers: a target endpoint difference other than +/-1 mod 5 having an internal satisfying completion; failure of a +1 or -1 endpoint pair; hidden identification or conflict between edge auxiliaries; input/output bit-length or witness extension violating the claimed factor. All four are settled below, for arbitrary n,m.

## Source and complete pipeline

T5 has vertices Z5 and R(a,b) iff b-a mod 5 is in S={1,3}. This is the prescribed five-symbol tournament, with directed triangles 0->1->2->0 and 0->3->4->0. C5 is the *undirected* simple cycle on Z5 with adjacency iff b-a mod 5 is in {1,4}. It is not the directed 5-cycle.

A canonical binary source writes 1^n 0, then 1^m 0, then m lexicographically strictly increasing pairs (u,v), each satisfying 0<=u<v<n. Indices occupy w(n)=max(1,ceil(log2(max(2,n)))) low-first bits each. Exact source bit length L_H=n+m+2+2mw(n). The parser checks binary characters, delimiters, exact trailer size, widths, pair order, index ranges and duplicates. n=0 is permitted only with m=0. Malformed inputs have the deterministic outcome INVALID, not UNSAT.

For each source edge e={u,v} introduce two distinct fresh vertices a_e=n+2e and b_e=n+2e+1. Append the four arcs

    u -> a_e -> v -> b_e -> u .

Sort the 4m directed arcs lexicographically, serialize them using the same unary-header and low-first-address convention, now with n_D=n+2m vertices, m_D=4m arcs and w_D=w(n+2m). Exact output length is

    L_D=n+6m+2+8m w_D.

All vertices, including isolates, are preserved; no gadget can share an auxiliary identity with another edge. All constructed arcs are loopless and there are no opposite pairs. For n>=2 and simple H, m<=n(n-1)/2, hence n_D<=n^2 and w_D<=2w(n). Therefore **L_D<=8 L_H**. This is a genuine constant-factor *bit-length* Karp reduction on this canonical encoding, not merely a vertex-factor claim. n=0 or 1 is immediate. Both certificates use three low-first bits per five-valued label, with 5,6,7 rejected.

## Four-arc gadget: complete symbolic proof

For a two-edge directed walk x->z->y, the endpoint difference d=y-x mod 5 is a sum of two elements of S. Its exact realization count t(d) is

    d:       0 1 2 3 4
    t(d):    0 1 1 0 2.

Indeed 1+1=2, 1+3=4, 3+1=4 and 3+3=1 mod 5, accounting for all four ordered pairs. In the reverse two-edge walk y->w->x the endpoint difference is -d. As z and w are independent fresh variables, their joint completion count is t(d)t(-d), which equals 2 for d=1 or 4 and 0 otherwise. These are exactly the adjacent pairs of undirected C5. Independence across edges gives

    #Hom(D(H), T5) = 2^m #Hom(H, C5).

YES iff YES. For a particular YES witness f, choose for every edge the lexicographically smallest valid (z,w) to produce an explicit T5 witness in O(m) fixed-alphabet steps plus actual source access. Conversely restrict any satisfying D(H) witness to its first n vertices to recover an H->C5 colouring. The 2^m multiplier is necessary: the decision reduction is **not parsimonious**. The equality also applies with n=m=0 (both counts one).

The 1990 **Hell-Nešetřil undirected H-colouring dichotomy**, JCTB 48(1):92-110, DOI 10.1016/0095-8956(90)90132-J, establishes that HOM(-,C5) is NP-complete because C5 is irreflexive and non-bipartite. Our fully explicit linear gadget therefore proves NP-hardness of the **exact** R template independently of any unidentified tournament reduction. Membership in NP follows by reading n symbols and verifying 4m arcs. The separate 1988 **Bang-Jensen–Hell–MacGillivray semicomplete-target dichotomy**, SIAM J. Discrete Math. 1(3):281-298, DOI 10.1137/0401029, confirms classification directly: T5 is a tournament containing at least two directed cycles. These are primary theorem statements, not new complexity-class separations.

T5 is a core: every homomorphism T5->T5 is injective because an identified pair has an oriented arc and no loop in the target. Since there are five vertices, each endomorphism is an automorphism. Its full automorphism group is the five translations a->a+c: after fixing image(0)=0, two outgoing neighbors and two incoming neighbors are individually distinguished by their induced orientation, giving a trivial stabilizer. A higher-arity polymorphism inventory is NOT proved here; no tractability inference rests on one.

## Reverse compiler: exact original-assignment multiplicity and bit count

For *any* authenticated directed source G with n vertices and m distinct directed arcs, including loops, opposite arcs and isolates, introduce five one-hot Boolean variables X_{i,a} for each vertex i and three functional OR-prefix variables Y_{i,1},Y_{i,2},Y_{i,3}. There are exactly **q=8n Boolean variables**.

For each vertex emit the 10 pairwise at-most-one clauses (not X_{i,a} OR not X_{i,b}) for 0<=a<b<5. Set L_0=X_{i,0}; for j=1,2,3, force Y_{i,j}=L_{j-1} OR X_{i,j} by the three width-at-most-three clauses

    (not L_{j-1} OR Y_{i,j}),
    (not X_{i,j} OR Y_{i,j}),
    (L_{j-1} OR X_{i,j} OR not Y_{i,j}),

and let L_j=Y_{i,j}. Append (Y_{i,3} OR X_{i,4}). This gives 20 clauses per vertex; every one-hot assignment extends uniquely to all three Y variables and exactly one X_{i,a} must be true. For each source arc (i,j), emit the 15 forbidden-pair clauses (not X_{i,a} OR not X_{j,b}) for every (a,b) with R(a,b)=0. There are 25 ordered pairs and exactly ten satisfying target pairs, hence **15 arc clauses**, including when i=j. The raw ordered CNF list has exactly **c=20n+15m clauses**, every clause width at most 3. Repeated source arcs are rejected by the canonical grammar; internally duplicated CNF clauses from loops can be left in place without affecting satisfaction or the raw clause count.

For every original T5 assignment x there is exactly one satisfying extension of the Boolean one-hot and prefix variables iff x satisfies all arcs. No other Boolean model exists. Therefore **#SAT(F_G)=#Hom(G,T5)**, including isolated vertices, loops and the empty graph. A loop makes the formula UNSAT because (a,a) is among the forbidden pairs for all five possible labels.

A fixed low-first binary CNF serialization can use unary q and c and three literal slots of w_B=max(1,ceil(log2(2q+1))) bits each, encoding 0 for empty, 2k+1 for negated X_k and 2k+2 for positive X_k. The exact word length is B_B=q+c+2+3cw_B. The formula is width-at-most-three, not necessarily strict distinct-variable 3CNF. The separate Anthropic promise normalizer, if needed, retains the count but its formal kernel remains an independently unrebuilt premise.

For the composition H -> D(H) -> F_{D(H)}, q=8n+16m and c=20n+100m, and

    #SAT(F_{D(H)}) = 2^m #Hom(H,C5).

## Matched physical resource ledger

One ordinary deterministic finite-alphabet locally headed multitape compiler reads and authenticates the complete unary-header source; constructs and sorts all fresh vertex/edge records; writes D(H); constructs the Boolean one-hot and functional auxiliary clauses if requested; serializes, validates and outputs the result. Its total source length L>=n+m+2, every produced record costs O(log(L+2)) bits, and there are O(n+m) records. Parsing, sort, all source accesses, addresses, buffers, gate/auxiliary reuse, arithmetic, failed validation, and complete output fit the intentionally conservative **same-run** bounds T=O((L+1)^4), S_peak=O((L+1)^2). These are **upper bounds** of this specific executable compiler, not compulsory costs for every equivalent reduction. The reduction stage alone has L_D<=8L, and the CNF bit source is O(L log(L+2)).

Given a deterministic T5 solver with time T_5(L_D) and peak writable space S_5(L_D), the straightforward composed C5 decider, on the SAME sequential physical execution, has T=O((L+1)^4+T_5(8L)) and S_peak=O((L+1)^2+S_5(8L)). The companion T5->3CNF solver translation has output O(L log L) and similar polynomial overhead. No resource lower bound or forbidden DTISP point is inferred.

## Gate checks and hostile controls

DISJ sanity: **PASS (restricted)**, this is a finite relation identity and count-preserving upper compiler, not a rank or work lower bound. Test cycles, forests, affine shortcuts, bounded-treewidth DP and polynomial recognizers rather than claiming they are hard.

Relativization: **PASS for syntactic gadget**. NP-completeness does not separate P and NP, and a nonrelativizing NP lower-bound bridge remains **OPEN**. Algebrization and Natural Proofs safeguards retained.

Simultaneous DTISP: **PASS for compiler upper bounds**, with time and live space charged on one execution; no forbidden time/space pair or all-decider lower bound.

Deterministic configuration counting: **NOT APPLICABLE WITH REASON** to proving the gadget or NP-hardness. For any fixed total deterministic decider, counting configurations supplies only an upper bound in terms of its workspace, never the work lower bound being sought.

Preserve alternative Gaussian Z5 cycle-basis shortcuts, treewidth, arc/path consistency, algebraic Fourier techniques, product and padding controls, different encodings, sharing, caches and all legal polynomial subfamilies. /341 remains FAIL as full UNSAT authority; /386 RESTRICTED.

## Finite executable evidence and limitations

Published owned code: experiments/tmr/tmr1_t5_c5_bridge071.js, Git blob 0c2c645d678530eff36f07fdfdca0c0b3a0b2eb5.
Immutable raw: results/raw/tmr/2026-11-17_1317_TMR1_T5_C5_BRIDGE071_V8_RAW.json, Git blob 45b32649e24c84b8095edf895dce10f1cff7e78d.
Actually executed hosted V8 revision tmr1-t5-c5-bridge071-published.v1: 25 endpoint pairs, ALL 76 loopless simple graphs with n<=4, exact C5 and weighted expanded T5 counts, 1024 one-hot truth-pattern checks, 1127 assertions, zero failures, no random seed. Local Node v22.16.0 extended verifier additionally checked source header/bit lengths for 152 serializations, eight malformed examples and enumerated 716 actual expanded satisfying T5 assignments on n<=3 source graphs, with 4542 assertions, zero failures. That extended source and raw remain local only, not claimed as published in GitHub; SHA256 source 22808eb7b4d971af971e1398960f29ab0c804c7101d9e40ab12133551a3f2f9a; raw 525d856f01ce612567b5e82487771fc55329ee5c6f73f3cfde490844eaa8c530. No repository checkout/preflight, Lean/nanoda kernel build, external mathematical review or full LaTeX compile was run.

## ONE next load-bearing lemma

Obtain a fully explicit *direct* 3SAT -> undirected C5-colouring gadget with authenticated source length and constant blowup, then compose and verify with C1-T5-C5-FOUR-ARC. The present NP-hardness already follows from the 1990 primary dichotomy and the explicit four-arc reduction; the next target is finer quantitative model-to-model transport, **not** a missing classification theorem.
