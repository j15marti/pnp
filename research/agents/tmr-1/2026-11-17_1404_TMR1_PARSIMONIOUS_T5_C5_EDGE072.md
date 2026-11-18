# TMR-1/072: bijective four-arc C5-to-T5 edge reduction

2026-11-17 14:04 America/Los_Angeles. TMR-1 / PNP Machine Model Lead. PROVED/EXACT restricted mathematical construction, independent review OPEN. Tests COMPUTATIONAL. T5 NP-completeness KNOWN THEOREM. P versus NP OPEN.

## Candidate and falsifiers, before source search

Named dependency **C1-T5-C5-BIJECTIVE-EDGE**, replacing the nonparsimonious /071 gadget. For every authenticated, finite, simple undirected graph H=(V,E), a single uniform compiler produces D*(H) and a translation-equivariant BIJECTION between Hom(H,C5) and Hom(D*(H),T5). Falsifiers: (1) improper endpoint colors permit an auxiliary completion; (2) proper endpoint colors permit zero or more than one; (3) edges share unexpected auxiliaries or lose isolated/empty vertices; (4) actual sorted binary serialization, witnesses or compiler costs exceed claimed bounds. The symbolic proof below covers all inputs.

## Actual encoded input, reduction and complete proof

Let T5 be Z5 with R(a,b)=1 iff b-a mod5 in S={1,3}. Let undirected C5 have adjacency iff b-a mod5 in {1,4}. A simple undirected source is encoded as

    1^n 0 1^m 0 (u0,v0) ... (u(m-1),v(m-1)),

with both endpoints low-first in w(n)=max(1,ceil(log2(max(2,n)))) bits, strictly lexicographically sorted and 0<=u<v<n. Exact source bit length L_H=n+m+2+2m*w(n). The compiler reads and authenticates every bit, header, width, edge order, range, duplicate restriction and trailer, rejects malformed input as INVALID, and retains all n original vertices. The directed target uses the analogous sorted arc grammar.

For each original edge e={u,v} (u<v), create two DISTINCT new vertices z_e=n+2e and w_e=n+2e+1 and append the FOUR arcs

    u -> z_e,   u -> w_e,   w_e -> z_e,   w_e -> v.

This is a TMR-2/068 unique-successor triangle followed by one additional arc. For any u,z,w, the first three beat constraints hold if and only if z=u+1, w=u+3 (mod5). In detail, u->z requires z-u in {1,3}. The two-step u->w->z requires z-u in S+S={1,2,4}. Their intersection is {1}, and its only ordered summand is 3+3=1 (mod5). Thus z=u+1 and w=u+3, uniquely. The final edge w->v then holds iff v-u lies in 3+{1,3}={4,1} (mod5), EXACTLY the undirected C5 adjacency relation.

Consequently the gadget's number of internal completions for endpoint differences 0,1,2,3,4 is

    (0,1,0,0,1),

unlike the old four-cycle completion vector (0,2,0,0,2). Extend any C5-coloring c of H by z_e=c(u)+1 and w_e=c(u)+3, modulo 5, on every edge. This is a T5 homomorphism and is the ONLY extension. Conversely restricting any T5 homomorphism of D*(H) to the original n vertices returns a C5 homomorphism and its auxiliaries are forced. Fresh edge-specific names ensure the maps are inverse independently over all edges. Isolates retain their five states and the empty graph has one assignment. Therefore, for EVERY source:

    #Hom(D*(H),T5) = #Hom(H,C5). [PARSIMONIOUS, EXACT]

This is an actual witness-level bijection, not just satisfiability or an unknown correction factor. Adding a constant c mod5 to every original and auxiliary color commutes with the map. For n>0 the Z5 translation action is free on solutions, hence nonzero solution counts are multiples of five; this is a symmetry reduction, NOT a lower bound.

## Exact output size and two-direction interfaces

The output has n_D=n+2m vertices, m_D=4m arcs, sorted as authentic canonical records. Its exact bit length is

    L_D=n+6m+2+8m*w(n+2m).

For n>=2, simple H has m<=n(n-1)/2 and n+2m<=n^2, giving w(n+2m)<=2w(n), whence L_D<=8 L_H. n=0,1 are immediate. The input witness has 3n bits (valid codes 0..4); the unique extension has 3(n+2m) bits and is produced after source authentication in polynomial bit time, while the inverse simply restricts the original coordinates. For a genuine T5 algorithm of time T5(L_D) and peak writable space S5(L_D), one ordinary sequential composition gives the SAME-REALIZATION upper ledger

    T=O((L_H+1)^4+T5(8L_H)),
    S_peak=O((L_H+1)^2+S5(8L_H)).

The compiler separately has same-run T_comp=O((L_H+1)^4), S_comp=O((L_H+1)^2), including all parsing, failed checks, sorting, all bit accesses, arithmetic, target addresses, buffers, wire sharing, output and validation. These are conservative upper bounds of a fixed locally headed finite-alphabet multitape realization, not an all-decider lower bound.

Composing with the /071 exact-count-preserving five-one-hot-plus-three-functional-OR-prefix Boolean compiler gives precisely

    q=8(n+2m)=8n+16m Boolean variables,
    c=20(n+2m)+15(4m)=20n+100m raw width-at-most-three CNF clauses,
    #SAT(F_D*)=#Hom(D*,T5)=#Hom(H,C5).

No factor 2^m and no division or integer-precision correction is required. The width-at-most-three target is not automatically strict three-distinct-variable CNF. If a different direct C5-to-Boolean compiler is cheaper, it remains LEGAL.

The 1990 Hell–Nešetřil undirected H-coloring dichotomy shows C5-homomorphism NP-complete because C5 is loopless and nonbipartite. The 1988 Bang-Jensen–Hell–MacGillivray semicomplete-target theorem independently makes this exact T5 target NP-complete: T5 has two distinct directed triangles. A hypothetical polynomial-time T5 solver would imply polynomial-time C5-coloring and hence P=NP; NP-hardness or parsimony does not provide a T5 lower bound or settle P vs NP.

## Verification, sources, scope and review

PRIMARY LITERATURE: (1) Hell and Nešetřil, On the complexity of H-colouring, JCTB 48:92-110 (1990), DOI 10.1016/0095-8956(90)90132-J. (2) Bang-Jensen, Hell and MacGillivray, The Complexity of Colouring by Semicomplete Digraphs, SIAM J Discrete Math 1:281-298 (1988), DOI 10.1137/0401029. Cross-agent original: TMR-2/068 unique-successor lemma, research/agents/tmr-2/2026-11-17_1336_TMR2_T5_SUCCESSOR_GRID068.md, merged to main. The fourth-arc C5 count-bijection here is new relative to that predecessor.

PUBLISHED V8 validator experiments/tmr/tmr1_t5_parsimonious072.js was actually executed under Node v22.16.0, deterministic with no seed: all 25 endpoint pairs, all 76 undirected simple graphs n<=4, 1024 one-hot/CNF patterns, **1212 assertions, zero failures**; raw results at results/raw/tmr/2026-11-17_1404_TMR1_T5_PARSIMONIOUS072_NODE_RAW.json. Separate independent extended local validator /mnt/data/tmr1_t5_parsimonious072.js, SHA256 a5dac8f09da75a8b954d2f2c8f2a35380a24151104d881d81cfeddf4eac208e2, was also actually executed: **11818 assertions**, 152 authentic input/output round trips, 10 malformed rejections, 11 full T5 enumeration instances, and 1692 labelled at-most-three-arc candidate gadgets, zero unexpected failures. Its raw SHA256 is 04c06cd806e2fe74f79af332371fa3b820a857ac2ca5f6fda6356612823ba2bc. That bounded negative search is computational ONLY, not a proof of minimum gadget size. The two sources are separate revisions; extended source is local and is not claimed published to GitHub.

DISJ sanity: **PASS restricted** (no rank-to-work inference). Relativization: **PASS for syntactic reduction; NP separation OPEN** (algebrization/Natural Proofs remain barriers). Simultaneous DTISP: **PASS for stated same-execution upper ledger only**, no forbidden pair. Deterministic configuration counting: **NOT APPLICABLE WITH REASON** to gadget NP-hardness; remains an upper-bound check on total deterministic deciders only. Preserve all cheap Z5/Fourier, polymorphism, Gaussian, local consistency, treewidth-DP, Horn/2SAT, affine, equality, autarky, selector, product, padding, alternate representations and caching paths. TMR-2/068 gives cheap high-treewidth instances. /341 FAIL as unrestricted UNSAT authority; /386 RESTRICTED. Other operations MAY be cheaper.

No local repository checkout/preflight, independent Lean/nanoda pinned theorem rebuilding, complete LaTeX compilation or external mathematical peer review performed. Existing conditional higher-class E^NP Track C implications are unchanged and do NOT become NP lower bounds.

ONE NEXT LOAD-BEARING DEPENDENCY: **C1-T5-DIRECT-3SAT-C5-COMPILE**. Build and authenticate an explicit quantitative signed-literal 3SAT->undirected-C5 reduction and compose it with this exact witness-bijective T5 gadget, tracking Boolean encodings, size and every witness. P versus NP OPEN.
