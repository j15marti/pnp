# TMR-1/073: explicit anchored graph-3-coloring to C5 to T5

2026-11-17 14:59 PST. TMR-1 / PNP Machine Model Lead. Named dependency: **C1-T5-3COLOR-ANCHOR-PATH-REDUCTION**. Result **PROVED/EXACT, restricted to the declared standard graph-3-coloring input; independent external mathematical review OPEN**. Finite verification COMPUTATIONAL. P versus NP OPEN. Existing pinned Anthropic kernel and higher-class Track C transfer remain separate and CONDITIONAL.

## Candidate, falsifiers and authenticated end-to-end chain

For every canonical finite simple undirected graph X=(V,E), including empty, isolates and malformed bitstrings, build one canonically encoded T5 digraph D and show:
X has a proper 3-coloring iff D admits a labeling satisfying R(a,b) iff (b-a) mod5 belongs to {1,3}.
Falsifiers fixed before the test: (i) two-edge undirected C5 paths from the anchor admit a fourth label or exclude one of the needed three; (ii) three-edge C5 paths permit equal endpoint colors or fail for distinct colors; (iii) the anchor C5 folds under a nonautomorphic homomorphism; (iv) isolate-heavy inputs violate a claimed constant **encoded-bit** growth bound. Item (iv) is real if isolates are not removed, and is repaired by the explicit active-vertex pruning below. No solver lower bound is claimed.

Full chain: authenticate source bitstream -> remove isolated vertices and record renumbering -> construct anchored C5 graph -> compile each C5 edge using /072's four-arc *parsimonious* T5 gadget -> canonical sorted directed serialization -> T5 decision/checker -> reconstruct an ordinary 3-coloring -> NP-completeness consequence. No implicit oracle, semantic free gadget, or source-only access is assumed.

## Canonical bit interface

Use the pre-existing authenticated graph grammar 1^n 0 1^m 0 followed by m lexicographically increasing low-first pairs (u,v), each coordinate in w(n)=max(1,ceil(log2(max(2,n)))) bits, 0<=u<v<n and no duplicates; length L=n+m+2+2mw(n). Reject any malformed prefix, endpoint, ordering, trailer or missing bit as INVALID. A standard 3-color witness uses n two-bit codes restricted to 0,1,2; checking its edges costs polynomial bit time. For m=0, return the valid empty T5 graph, binary word 00, with a unique empty T5 witness; the reverse witness fills all original colors with 0. This branch is decision-preserving, not counting-preserving.

For m>=1, remove and renumber isolated original vertices in increasing original-index order. Let k be the remaining vertex count, so 2<=k<=min(n,2m); retain the original-to-core map as paid compiler workspace and recompute it on inverse witness conversion. The core graph is still 3-colorable iff X is.

## Explicit elementary 3-COLOR -> C5 construction

Let C5 be the undirected target Z5 with adjacency iff difference belongs to {1,4}. Add five anchor vertices a_0,...,a_4 and all five cycle edges a_i--a_(i+1 mod5). Add one original-core vertex v_i and one private t_i for each i; connect a_0--t_i--v_i (two edges). For every original core edge e={i,j}, add private vertices p_e,q_e and the length-three path v_i--p_e--q_e--v_j. There are exactly

  N_H=5+2k+2m vertices,  M_H=5+2k+3m edges.

The construction uses canonical names 0..4 for anchors, 5..5+k-1 for original core vertices, 5+k..5+2k-1 for unary interiors, and 5+2k+2e,5+2k+2e+1 for edge interiors, with all edges sorted and authenticated.

Every homomorphism from the anchor 5-cycle to C5 is an automorphism. Each of five consecutive walk increments is +1 or -1; a return after five steps has signed sum divisible by 5, forcing all five signs to agree. Thus there are exactly ten anchor maps a_i -> b+s i, b in Z5 and s in {+1,-1}.

A two-edge C5 walk has endpoint-difference multiplicities W2(0,d)=(2,0,1,1,0), d=0,...,4. Relative to anchored a0, this restricts every original v_i to {0,2,3}. A three-edge C5 walk has endpoint-difference multiplicities W3(0,d)=(0,3,1,1,3), so it is possible **exactly when endpoints differ**. Hence the length-three private edge path forces inequality on the triple {0,2,3}. Explicitly identify 3-color values 0,1,2 with relative C5 colors 0,2,3.

For a proper source 3-coloring, select the identity anchor map, assign mapped original colors, choose one of the finitely many legal interior colors of every private path (lexicographically first suffices), then assign /072's uniquely forced T5 auxiliary states. Every directed arc is satisfied. Conversely, any T5 satisfying witness restricts via /072 to an H->C5 homomorphism; normalize its anchor by b,s and read the original v_i colors in {0,2,3}; decode the three source colors and put 0 on isolated source vertices. Each original source edge then has distinct endpoint colors. Thus the many-one reduction preserves YES and NO and has explicitly computed witness maps both ways.

## Compose with the previous exact C5 -> T5 edge gadget

For every sorted H edge u<v, add two private vertices z_e,w_e and directed arcs u->z_e, u->w_e, w_e->z_e, w_e->v. By the /072 exact proof, z_e=u+1 and w_e=u+3 modulo5 uniquely; the last arc is equivalent to C5 adjacency. Hence

  #Hom(D*(H),T5) = #Hom(H,C5),

even though the preceding 3-COLOR-to-C5 reduction is *not* parsimonious. The composed directed graph has

  N_D=N_H+2 M_H = 15+6k+8m vertices,
  A_D=4 M_H = 20+8k+12m arcs.

The reverse /071 one-hot-plus-three-functional-OR Boolean compiler has exactly

  q=8N_D=120+48k+64m Boolean variables,
  c=20N_D+15A_D=600+240k+340m width-at-most-three raw clauses.

Its count equals the directed T5 count. Distinguish width-at-most-three from strict three-distinct-literal clauses; any subsequent normalization must be charged.

For m>=1, let Col3(X_core) be the set of proper mappings c:Vcore->{0,2,3}. Let n_0(c) count vertices colored zero and e_23(c) count source edges with endpoint colors 2 and 3. All 10 anchor automorphisms have equal interior multiplicities. The exact count is

  #Hom(D,T5) = 10 sum_{c in Col3(X_core)} 2^{n_0(c)} 3^{e_23(c)}.

Indeed W2 contributes two choices for relative zero and one for either nonzero relative color; W3 contributes three for the 2/3 pair (difference +/-1), and one for 0/2 or 0/3 (difference +/-2). Fresh path interiors multiply independently, and /072 adds no multiplicity. For m=0 the target count is 1, whereas #3Col(X)=3^n. **Only decision and witness existence** transfer from arbitrary source 3-coloring. No parsimonious or simple count-preserving #3-COLOR theorem is asserted.

## Exact bit growth, malformed inputs and SAME_REALIZATION ledger

The original serialized source length is L=n+m+2+2m w(n). After isolating/pruning unused source vertices, k<=2m. The output uses sorted low-first directed arcs, with exact bit length

  L_D= N_D+A_D+2+2 A_D w(N_D)
      =37+14k+20m+(40+16k+24m) w(N_D).

For n>=2 and m>=1, m<=n(n-1)/2 and k<=n give N_D<=16n^2 and w(N_D)<=2w(n)+4. With k<=2m,

  L_D<=197+272m+80w(n)+112m w(n)
      <=661 m w(n) <=331 L.

For m=0, L_D=2<=L. This is **constant-factor encoded-bit growth on every authentic input, including arbitrarily many isolated vertices**. Without pruning, source m=0 has L=Theta(n) but the anchored output would have Theta(n log n) bits, so a uniform constant-bit factor claim would be false.

A conventional blank-start, locally headed finite-alphabet multitape compiler can parse all bytes and failed checks, discover active vertices, construct/sort H records, produce D via /072, retain the mapping, pay all addresses, indexes, buffers, sharing, arithmetic, output and optional certificate validation in T_comp=O((L+1)^4) time and S_comp=O((L+1)^2) peak writable bits. Given an actual deterministic T5 decider with same-machine upper bounds T5(B), S5(B), sequential physical composition has T=O((L+1)^4+T5(331L)) and S_peak=O((L+1)^2+S5(331L)), including physically retaining/reading the serialized reduction. These are joint UPPER bounds, not lower bounds, and do not imply a time-space forbidden pair.

Known NP-completeness of ordinary graph 3-colorability (Garey, Johnson, Stockmeyer 1976) plus this explicit reduction and the trivial polynomial T5 certificate verifier establish the specific template's NP-completeness without invoking the H-coloring dichotomy. The Hell--Nesetril (1990) C5 dichotomy and Bang-Jensen--Hell--MacGillivray (1988) semicomplete-target theorem independently agree. An efficient arbitrary-input T5 decider would imply P=NP; none has been established.

## Verification and evidence

Executed an original deterministic JavaScript V8 exhaustive verifier with seed NONE. It authenticated and rebuilt all 1,100 simple undirected source graphs of orders 0..5, enumerated 36,820 proper source 3-colorings, lifted and inversely recovered 36,820 full T5 witnesses, checked 50 independent two/three-step path endpoint multiplicities, rejected 7 malformed inputs, and executed **484,348 assertions with zero failures**. It checked canonical low-first source and directed-target round trips, exact vertex/edge/arc budgets and L_D<=331L for each enumerated source; 1,027 cases exhibited nonparsimonious count behavior (the expected feature). Tests are finite COMPUTATIONAL evidence, not the arbitrary-length mathematical proof. The published standalone script was generated from the executed V8 function; no independent native Node re-execution of the published standalone artifact is claimed.

Original executable: experiments/tmr/tmr1_threecolor_c5_t5_073.js
Immutable raw: results/raw/tmr/2026-11-17_1459_TMR1_THREECOLOR_C5_T5_073_V8_RAW.json
Living role manuscript: main1_PNP_MACHINE_MODEL_LEAD.tex, draft PR #197.
No local checkout or preflight, complete LaTeX compilation, Lean/nanoda kernel replay, or external mathematical peer review was executed. The prior /072 gadget and its evidence remain unchanged.

Four gates: DISJ **PASS RESTRICTED**, only a graph reduction, no rank-to-work claim; relativization **PASS for the syntactic reduction**, while nonrelativizing NP-separation premise OPEN under BGS/algebrization/Natural Proofs; simultaneous DTISP **PASS for the one real upper-bound ledger**, with any forbidden time-space pair NOT ESTABLISHED; deterministic configuration counting **NOT APPLICABLE WITH REASON** to an NP-hardness reduction, upper bound T<=2^{O(S+log L)} still applies to a fixed deterministic total decider when applicable. All compact Z5/Fourier, affine/Gaussian, direct homomorphism, bounded-treewidth DP, dynamic propagation, Horn/2SAT, equality, products, padding, auxiliaries, and cheap recognized image algorithms remain legal. /341 FAIL full UNSAT authority; /386 RESTRICTED.

References: (1) Garey, Johnson, Stockmeyer, "Some simplified NP-complete graph problems," Theoretical Computer Science 1 (1976), 237-267, DOI 10.1016/0304-3975(76)90059-1. (2) Hell and Nesetril, "On the complexity of H-colouring," JCTB 48 (1990), 92-110, DOI 10.1016/0095-8956(90)90132-J. (3) Bang-Jensen, Hell, MacGillivray, "The Complexity of Colouring by Semicomplete Digraphs," SIAM J Discrete Math 1 (1988), 281-298, DOI 10.1137/0401029. (4) TMR-1/072 role report, full exact C5-to-T5 gadget and functional reverse Boolean compiler, original path research/agents/tmr-1/2026-11-17_1404_TMR1_PARSIMONIOUS_T5_C5_EDGE072.md.

**ONE NEXT DEPENDENCY: C1-T5-SIGNED-3SAT-TO-3COLOR-COMPILER.** Source-authenticate an explicit signed-width-three Boolean-to-graph-3-coloring gadget (with clauses, negations, proper colors, malformed inputs, exact gadget size and witness conversions) and compose it with this now closed 3-COLOR -> anchored C5 -> T5 chain. This last explicit source leg is not supplied or assumed by the new theorem. The historical Anthropic independent kernel obligation is separately OPEN. P versus NP OPEN.
