# TMR-2/072 | 2026-11-17 17:18 PST | Connected mixed YES/NO T5 source family with a gauge-cycle shortcut

**Role:** TMR-2 / PNP Information Necessity, Track A, owned manuscript `main2_PNP_INFORMATION_NECESSITY.tex`. **Status:** PROVED/EXACT for the explicit restricted constructions and the stated source recognizer; the adaptive read-once lower-bound corollary imports Razgon and LPS. Independent mathematical review OPEN. Finite tests COMPUTATIONAL. P versus NP OPEN.

## Candidate and falsifiers, stated before source/corpus audit

**D2-T5-CONNECTED-GAUGE-MIXED-TRACE** attacks the named dependency `D2-T5-MIXED-DECISION-SOURCE-ADAPTIVE-OBSTRUCTION`. Construct a genuinely connected, authentic, mixed YES/NO family with hard YES-side *pointwise* adaptive read-once representations, yet give a single entirely source-aware deterministic polynomial-time decision procedure for BOTH alternatives. This falsifies any inference that mixing answer labels plus a hard YES indicator already imposes costly source decisions.

Falsifiers: (F1) the three-arc successor diamond has more than one extension or forces a different offset; (F2) connecting a ring to a bipartite core changes the core predicate, loses multiplicities or leaves the graph disconnected; (F3) the claimed cheap decider needs a supplied gadget descriptor, labels, SAT oracle or expensive graph-isomorphism test; (F4) existentially projecting the ring variables fails to preserve the *syntactic* nondeterministic read-once restriction or misuses the Razgon/LPS hypotheses. Each is resolved for this restricted construction. Unrestricted solver-work necessity remains OPEN.

## Source, gadget, semantics and exact classification

Write the tournament as `R(x,y)=[y-x mod 5 in {1,3}]`. Input is the previously fixed, fully explicit, lexicographically sorted, duplicate-free, newline-terminated ASCII graph `p t5 n m`, `v i`, `a u v`. An invalid source is rejected. Correct general graph decision can fall back to finite exhaustive five-label enumeration; the polynomial theorem below is only for recognized sources.

Take **any connected nonempty pure-source/pure-sink digraph** H, so each vertex has positive degree and only incoming or only outgoing arcs. Choose an actual core vertex h. For k>=5, adjoin k-1 fresh ring vertices t_1,...,t_{k-1} and k fresh witnesses w_0,...,w_{k-1}; set t_0=h, t_k=t_0; for each i add exactly the three original T5 arcs

```
t_i -> t_(i+1),  t_i -> w_i,  w_i -> t_(i+1).
```

There are n_H+2k-1 original T5 vertices, m_H+3k original arcs, and the *entire* underlying undirected graph remains connected. No unary domain restriction, external promise bit, free latent witness or other template is introduced.

**Diamond identity (PROVED/EXACT):** for every a,b in Z5,

```
sum_{w in Z5} R(a,b)R(a,w)R(w,b) = [b=a+1 mod 5].
```

Indeed the direct arc permits differences 1,3. A two-step R path allows 1,2,4; their intersection is {1}, and for difference 1 the unique witness is w=a+3. Thus for any fixed original core assignment, the entire ring has **exactly one** extension when k=0 mod 5 and **zero** otherwise. Consequently

```
Z(G_k(H,h)) = Z(H) when k=0 mod 5, and =0 otherwise;
exists_ring C_G(core,ring) = C_H(core) or 0, respectively.
```

The first is an exact *original-five-label count*, not an identity about auxiliary CNF wires. The second is existential projection of the original assignment indicator, not pointwise equality on the full variable list.

Every pure-source/sink H has the explicit solution 0 on its sources and 1 on its sinks. Therefore the connected family is YES exactly for k divisible by five; it is NO for all other k. The YES witness assigns t_i=a+i, w_i=a+i+3 mod 5 after taking a=x_h. For NO, summing k forced successor increments gives 0=k mod5, impossible.

## Descriptor-free structural recognition (PROVED/EXACT for this class)

The executable does **not** rely on known indexing of h, H, k, a decomposition oracle or a supplied gadget description. It parses the complete original source, rejects loops/opposing arcs for the fast family, scans all triples to collect every undirected triangle, identifies its unique transitive orientation, and counts triangle incidences. In every member with k>=5, precisely k vertices occur in two triangles (ring terminals), k occur in one triangle (private witnesses), and all remaining core vertices in zero triangles. In each triangle the private witness is its middle vertex; the other two determine a successor arrow. These arrows must form one directed cycle through all terminals. Removing exactly the 3k triangle arcs leaves the original core with one ring terminal h attached. The recognizer authenticates exactly one such attachment, no other ring-core arcs, connectedness of the remaining core and the pure-source/pure-sink property.

No extra triangle exists: H is bipartite, there are no cross arcs except at h, and for k>=5 the terminal cycle is chordless. Conversely, an accepted graph decomposes **exactly** as a core plus a single ring of the specified three-arc diamonds, so the modular decision is sound and complete on every accepted source. The recognizer accepts arbitrary renumberings of the original vertices. All other valid graphs use a correct exhaustive fallback. The recognizer uses no source-generation index q and works for every connected H of the described type.

## Hard YES pointwise representation, easy mixed source decision

For the YES/NO infinite pair, use the connected six-regular bipartite double-cover H_q of the nonbipartite degree-six LPS expander X^(5,q) from TMR-2/071, q>125 prime and q=1 mod 20. Let N=|V(H_q)|=q(q^2-1). Take `k_0=5N` and `k_1=5N+1`; adjoin the ring to one actual core vertex. Both sources have Theta(N) original vertices/arcs and `L=Theta(N log(N+2))` ASCII bytes, high original treewidth, and are fully connected. Source generation, original-index labeling and full source serialization are polynomial in **output length** (not claimed polynomial in binary q).

The first is YES and the second NO. On the YES source, existentially removing the 2k-1 ring variables from its *pointwise* indicator returns exactly the original five-label indicator of H_q. Any syntactic nondeterministic read-once branching program for the full YES indicator can be projected to the core by replacing all ring-variable tests by epsilon transitions. Every remaining source-to-sink path is still syntactically read-once on core variables; because removed variables each appeared at most once per path, no inconsistent guessed value is introduced. The new program has at most the original number of nodes/edges and computes the exact existential projection. Restricting its core labels to the two palettes of /071 then gives Razgon's monotone-2CNF NROBP. Therefore the existing Razgon/LPS lower bound carries unchanged:

```
size(syntactic 5-way NROBP for YES G_k(H_q,h)) = 2^Omega(N)
                                           = 2^Omega(L/log L).
```

For the NO source, the pointwise indicator is identically zero and its smallest read-once program is a rejecting sink. A **single** polynomial-time unannotated source recognizer decides BOTH sides and constructs a YES witness. This is an explicit, connected and asymptotically high-treewidth counterexample to transferring either YES representation size or YES/NO mixture into a source-SAT machine-work lower bound. It does not settle a lower bound for another restricted model on more carefully selected mixed families.

The NROBP theorem is only about exact pointwise assignment representations; no conclusion about SAT algorithms, FBDD *solvers*, exact counting on arbitrary cores, general circuits or P vs NP is asserted. For exact counts, YES members inherit `Z(H_q)`, which is not claimed polynomial-time computable.

## Matched physical resources and TMR-4 dynamic invariant

With complete canonical source length L, n,m<=L. On one conventional blank-start, read-only-input, locally headed deterministic multitape realization: parsing/record checks; adjacency table; O(n^3) triangle discovery; directed triangle orientation; the incidence map; successor-cycle authentication; full core extraction, BFS and source/sink checks; attempted failures; and output/witness verification all use a conservative

```
T_fast(L) = O((L+1)^9),  S_peak(L) = O((L+1)^3) writable bits.
```

This is an intentionally loose costed **upper bound**, not a physical microstep replay. Source addresses/heads, counters, all triangle and arc sets, failed candidate checks, labels, caches, retained arrays and output are charged. The generic valid nonmember fallback has `O(5^n (L+1)^9)` time and polynomial peak writable storage; no general polynomial guarantee is claimed. The theorem does not assume the expensive NROBP is ever generated.

**D2-T5-CONNECTED-GAUGE-MIXED-TRACE** stores SOURCE_CURSOR, FULL_ARCS, TRIANGLE_INDEX, INCIDENCE_CLASSES, SOURCE_SINK_CORE, SUCCESSOR_PERMUTATION, ROOT_OFFSET, CYCLE_SUM_MOD5, CERTIFIED_WITNESS, SCOPED_COUNT_MULTIPLICITY, CACHE and OUTPUT. Complete transitions: READ/PARSE/GUARD; TRIANGLE/ORIENT/VERIFY; RECONSTRUCT/INCIDENCE; SUCCESSOR/SCC; CORE/BFS/SOURCE-SINK; MOD5-PROPAGATE/CYCLE-CHECK; CONSTRUCT/VERIFY-WITNESS; BRANCH/FALLBACK; PALETTE/EXISTENTIAL-PROJECT for restricted read-once analysis; CACHE/DROP/RECOMPUTE; OUTPUT. No transition is compulsory for an arbitrary solver; source-aware alternatives and unknown conservative MAY operations remain allowed.

## Finite verification and original-source provenance

Executed and rerun byte-identically locally with Python 3 stdlib, seed **20261117**, script `experiments/tmr/tmr2_t5_mixed072_compact.py`, exact local SHA256 **5acf31fdcbd26d1b374d9ffc851ffe1fa8590bf65db695e3b407937c4c3ad620**, immutable JSON `results/raw/tmr/2026-11-17_1718_TMR2_T5_MIXED072_COMPACT_RAW.json`, local SHA256 **961cc5b6d5c3483c6a93f8f2ace7094bba2b82781e3631032834eef4ec96eddf**. The published compact script ran **167 explicit assertions, 16 YES/NO exact original-label count tests**, independent generic raw-R backtracking, 25 gadget endpoint checks, two seeded arbitrary relabelings per case, structural negative controls and malformed canonical-source rejections, zero failures. Core controls: K1,1, K2,2, K2,3 and K3,3; k=5,6,10,11. An expanded local audit independently completed 237 assertions and 20 additional comparable controls (script SHA256 53ad536a65d16c211e9346efb3c35288d968478b95fb2b5118d97d864497002a). No large LPS graph was constructed here. Finite tests are COMPUTATIONAL; the infinite-family corollary depends on imported LPS/Razgon theorems and the symbolic gadget/recognizer proofs.

Prior original results distinguished: TMR-2/068 successor gadget and cheap successor-grid count; TMR-2/071 adaptive read-once palette lower bound; TMR-5/075 binary/affine polymorphisms (draft PR #209); TMR-3/071 module support (draft PR #233); TMR-4/074 feedback-edge compiler (open draft #237); LSPV-5 `T5CYCLEFLOW1` uses certified mixed gadgets and explicitly leaves unannotated extraction open. This report adds **unannotated structural extraction**, an actual connected mixed pair and existential read-once projection transfer, not a new successor gadget or new Razgon theorem.

## Four gates and hostile controls

| Gate | Verdict and reason |
|---|---|
| DISJ | **PASS for restricted model; FAIL any rank/pointwise-to-work transfer.** The oriented core's exact binary palette is monotone 2-CNF, SAT-trivial despite exponential representation width. |
| Relativization | **PASS locally, OPEN globally.** The restricted constructive theorem is not a nonrelativizing P-versus-NP separation. BGS, algebrization and Natural Proofs remain applicable audit requirements for any later unrestricted implication. |
| Simultaneous DTISP | **PASS for the one fast source-authenticating upper machine. NOT APPLICABLE to a forbidden-time-space lower-pair contradiction**, because none is asserted. |
| Configuration counting | **PASS upper-bound sanity only.** A halting deterministic s-space total machine has T<=2^O(s+log L); no necessary-work lower bound and no automatic randomized/quantum transfer follows. |

Hostile/easy alternatives retained: small-domain all-32 mask propagation and exact incoming/outgoing maps from /067, Fourier and field-sensitive ranks, binary and affine polymorphism audit from TMR-5/075, Horn, 2-SAT, Gaussian-style modular equations, treewidth, products, selectors, padding, auxiliaries, unique-solution rank one, count normalization, local-basis rank invariance, compact shared circuits, autarky, cache, recomputation, source recognition, switching, full path consistency and arbitrary alternate orders. Full path consistency on these mixed ring sources was **not** tested or claimed resistant; the modular cycle shortcut itself is sufficient. /341 FAIL for full UNSAT authority; /386 RESTRICTED.

**Independent mathematical review:** OPEN. No local repository checkout/preflight, full manuscript LaTeX build, formal kernel or physical TM microtracing was performed; repo-source checks used GitHub connector. This file is a new report, not a proof of P != NP.

## ONE next load-bearing dependency

**D2-T5-SOURCE-DECISION-NON-GAUGE-OBSTRUCTION (OPEN):** Construct an authenticated mixed-answer T5 family whose YES read-once cofactor lower bound does not coexist with an easily extracted modular gauge inconsistency on NO members and a source-derived fixed witness on YES members. State the restricted evaluator and a **charged** obstruction surviving all natural source-aware certifiers, adaptivity, cache/recomputation, propagation and alternative decompositions. The mixed-answer property alone is insufficient.

## Pinned references

Razgon, *On the Read-Once Property of Branching Programs and CNFs of Bounded Treewidth*, arXiv:1411.0264, original Theorem 2 / 2015 revision, https://arxiv.org/abs/1411.0264. LPS, *Ramanujan Graphs*, Combinatorica 8 (1988) 261--277, DOI https://doi.org/10.1007/BF02126799. TMR-2/071 original original source and exact limitations at `research/agents/tmr-2/2026-11-17_1612_TMR2_T5_ADAPTIVE_NROBP_PALETTE071.md`. TMR-5/075 draft report `research/agents/tmr-5/2026-11-17_1642_TMR5_T5_BINARY_AFFINE_POLYMORPHISM075.md`. LSPV-5 original `research/main/2026-11-17_1603_MAIN_LSPV5_T5CYCLEFLOW1_CONDENSED.tex`.
