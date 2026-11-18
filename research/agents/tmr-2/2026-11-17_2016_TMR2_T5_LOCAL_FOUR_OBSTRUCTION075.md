# TMR-2/075 | 2026-11-17 20:16 PST | Smallest acyclic T5 UNSAT motif and path-consistency collapse

**Owner:** TMR-2 / PNP Information Necessity. **Object:** the exact five-symbol beat relation R(a,b) iff (b-a) mod 5 in {1,3} and canonical explicitly enumerated source digraphs. **Dependency:** D2-T5-QUOTIENT-PRIME-ADAPTIVE-DECISION-BARRIER. **Result:** a necessary negative control for TMR-2/074 is **FALSIFIED** as a candidate hard NO instance by a four-vertex, five-arc forbidden pattern. The source-local theorem is **PROVED/EXACT restricted**, independent mathematical review **OPEN**, finite tests **COMPUTATIONAL**. **P versus NP OPEN.**

## 1. Precise candidate, falsifiers and interface

Prior to primary-source/corpus review: candidate D2-T5-FOURVERTEX-LOCALUNSAT-TRACE. In the equal-size mixed sources of /074, the NO variant is locally inconsistent on four genuine original vertices, independently of h, b, high minimum degree or treewidth. Hence a charged algorithm can detect UNSAT in polynomial time before expensive 25-state tensor/orbit calculation, and a standard (2,3)-path-consistency closure can also reject that local subinstance.

Falsifiers: (F1) one genuine T5 assignment satisfying all five motif arcs; (F2) a four-vertex acyclic T5 source with at most four arcs that is already UNSAT, defeating claimed minimum-arc scope; (F3) true path-consistency closure retains nonempty pair constraints on the motif; (F4) /074's actual NO input lacks these five original arcs or the YES control contains one of the two forbidden motifs. F1/F4 are settled by mathematical proof and authenticated-source generation; F2/F3 have finite exhaustive mathematical certificates below and independent executed code.

End-to-end chain: canonical actual source bytes -> strict ASCII parser and all declared original vertices/edges -> adjacency lists and/or bitsets -> scan every directed two-step path s->t->u for a common out-neighbor q of s,t,u -> if found return UNSAT with the four source IDs and five exact arcs, otherwise invoke the earlier genuine /074 source recognizer and exact original-label counting, or its all-input exact exhaustive fallback -> return actual decision/count/witness. This is a sound fast **negative certificate**, not a complete solver for arbitrary sources. An alternative branch computes full path consistency, with all relation updates charged.

## 2. Exact local theorem

Let Out(x)={x+1,x+3} mod 5. For distinct labels x,y, the intersection Out(x)∩Out(y) is nonempty precisely when y-x mod 5 belongs to {0,2,3}. If x->y is also required, then y-x must belong to {1,3}∩{0,2,3}={3}.

Consider four distinct original source variables s,t,u,q and precisely these five required arcs:

    s -> t,  t -> u,  s -> q,  t -> q,  u -> q.

The first and shared-sink constraints force t=s+3 mod 5. The second and shared-sink constraints force u=t+3=s+1 mod 5. But s and u both point to q, requiring u-s in {0,2,3}, contradiction. Thus this pattern is UNSAT in EVERY supergraph regardless of other variables, arcs or symbols used elsewhere. Reversing every arc yields another UNSAT pattern because the target admits an arc-reversing label bijection x↦-x. Both are genuine five-symbol original-source obstructions, not a prescribed representation cost or an auxiliary-label projection.

The /074 NO variant adds the actual terminal path s->t->u, and every source block has a private sink q with s,t,u->q. It therefore contains this pattern for all h>=4,b>=2. The /074 YES variant uses s->t and s->u and has no terminal length-two directed path, so the corresponding local detector cannot reject it. Its exact positive count 5*(2^(h-3))^b remains valid.

## 3. Minimum-arc statement and explicit certificate

Every directed acyclic source on at most three vertices embeds into the three-vertex transitive subtournament of T5 (e.g. labels 0,3,1 for the order 0<1<2). For n=4, choose a topological order and view its arcs as a subset of the six possible edges 01,02,03,12,13,23. It suffices to show all fifteen 4-arc subsets admit colorings: smaller edge sets extend acyclically to four arcs. In the table, “missing” indicates the two omitted edges of the six, and “witness” gives actual original labels for vertices 0,1,2,3 in Z5.

| Missing | Witness | Missing | Witness | Missing | Witness |
|---|---|---|---|---|---|
| 01,02 | 0,0,3,1 | 01,03 | 0,0,3,1 | 01,12 | 0,0,3,1 |
| 01,13 | 0,0,3,1 | 01,23 | 0,0,1,1 | 02,03 | 0,1,4,2 |
| 02,12 | 0,3,0,1 | 02,13 | 0,1,2,3 | 02,23 | 0,3,1,1 |
| 03,12 | 0,1,1,2 | 03,13 | 0,3,1,2 | 03,23 | 0,3,1,1 |
| 12,13 | 0,1,3,1 | 12,23 | 0,3,1,1 | 13,23 | 0,3,1,1 |

For n=4 and five arcs, the only two UNSAT cases (under a fixed topological order) are the pattern above and its converse up to a vertex order reversal. The complete transitive six-arc tournament on four source vertices is also UNSAT. Thus **four vertices and five arcs are necessary and sufficient** for a DAG UNSAT instance of this T5 relation. This minimum statement is for simple **acyclic** source digraphs without loops or opposite arcs, not unrestricted source graphs.

## 4. Genuine path-consistency trace

Initialize C_ij to R for an actual arc i->j, to R^{-1} for a reversed original arc, to equality if i=j, and to all 25 label pairs otherwise. Iteratively replace
C_ij <- C_ij ∩ (C_ik ○ C_kj)
for every triple of original variables (i,j,k), until no relation changes. The motif's shared-sink paths prune s->t and t->u to increment +3; composing the two forces s->u increment +1, while the common sink q restricts s,u differences to {0,2,3}. An empty relation is reached. This is local binary consistency and does not require general exact counting.

The published verifier performs this actual closure over all 64 four-vertex DAG subgraphs of the six-edge transitive K4 and compares with independently enumerated original five-symbol assignments. It detects exactly the three UNSAT sources (two five-arc, one six-arc), with no false positives and no false negatives in this *finite* universe. This is NOT a completeness claim for path consistency on arbitrary T5 sources.

## 5. Audits, time/space and original controls

**Actual same-run published JavaScript audit:** revision tmr2-t5-fourvertex-pc075-js.v1, deterministic seed 202611172016, 556 assertions, 0 failures, 32 domain masks, 64 exact four-vertex DAG source graphs, 312 source renamings of the /074 mixed constructions, all 64 real path-consistency closures, four (h,b) parameter pairs, independent original-color conditional count for h=4, and target-T5 easy control (five automorphisms). Files:

- experiments/tmr/tmr2_t5_fourvertex_pc075.js; Git blob 730a2019be88b54e2de0bf5c515962e139391407.
- results/raw/tmr/2026-11-17_2016_TMR2_T5_FOURVERTEX_PC075_JS_RAW.json; Git blob 27d76accf3f6d629903bc7c48ee37d0757f5e50f.

**Independent locally executed CPython:** revision tmr2-t5-fourvertex-pc075.v1, same seed, 516 assertions, 0 failures, same 64 DAGs, 32 mask-image checks, 112 pseudorandom vertex renamings and malformed-source rejection. These local assets were not claimed to be GitHub-published. The JavaScript raw is separately immutable and publicly reproducible.

For complete canonical source length L, n,m<=L. The four-motif detector materializes true adjacency and at most polynomially many source IDs. On a conservative locally headed deterministic bit-machine, using an unoptimized triple-loop with explicit common out-neighbor checks gives **T(L)=O((L+1)^7), S_peak(L)=O((L+1)^3)** for parsing, motif scan and certificate emission. This is a genuine paired upper bound for the fast *certifying branch*, not an overall all-input bound. When composed with the /074 exact-count source recognizer, the recognized-family upper remains its existing **T=O((L+1)^9), S_peak=O((L+1)^4)**, and generic valid nonmembers still take an exhaustive fallback. Source bytes, parser/adjacency, all attempted triples, unsuccessful tests, cache, witness/source rereads, indices, bit registers, output and switching are included. The four-pattern proof charges no semantic oracle and no hypothetical decomposition. Shared physical objects counted once.

The named TMR-4 execution-sensitive invariant is **D2-T5-FOURVERTEX-LOCALUNSAT-TRACE** with SOURCE_BYTES, AUTHENTICATED_ARCS, ACTUAL_ADJACENCY, PATH_TRIPLES, COMMON_SINK_SCAN, FORBIDDEN_FOUR_CERTIFICATE, PC_PAIR_RELATIONS, UPDATE_QUEUE, EMPTY_RELATION, SWITCH_TO_COFACTOR, CACHE/DROP/RECOMPUTE and OUTPUT. All legal alternative ways of finding the same certificate, exact source recognition, cheap Horn/2SAT/affine/treelike/product routes, false twins, low-degree, one/two/three-separators, compact shared computations, and adaptive variable orders remain available.

**Four required gates:** DISJ **PASS scoped**, but any static-rank-to-general-work inference **FAIL**. Relativization **PASS only for elementary source-local proof**; nonrelativizing bridge, Natural Proofs and algebrization **OPEN**. Simultaneous DTISP **PASS as an actually integrated upper bound on the fast branch; NOT APPLICABLE to a forbidden machine pair**. Deterministic configuration counting **PASS as upper-bound consistency only**, never a machine-work lower bound or automatic randomized/quantum transfer. Finite evidence is COMPUTATIONAL. No complete LaTeX compile, native TM microstep trace, repository checkout/preflight, or independent external mathematical review is claimed. /341 remains FAIL as UNSAT authority; /386 remains RESTRICTED.

**Primary-source pin:** Bang-Jensen, Hell and MacGillivray (1988), “The Complexity of Colouring by Semicomplete Digraphs,” SIAM J. Discrete Math. 1(3), 281–298, doi:10.1137/0401029, proves NP-completeness of the unrestricted fixed T5 tournament homomorphism problem through the general semicomplete dichotomy. This does not imply any unconditional superpolynomial SAT algorithm lower bound.

## 6. Next dependency

**D2-T5-PC-RESIDUAL-QUOTIENT-PRIME-MIXED-DECISION (OPEN):** Find source-authentic mixed YES/NO families that remain nontrivial after full (2,3)-path consistency, this smallest four-node certificate, triad quotient, low-degree elimination, one/two/three-separator, directed-twin/semicomplete module recognition, direct witnesses, bounded-cover exact counting and all legitimate source-aware shortcuts. If a proposed restricted evaluator still needs exponential work, define and price its legal transition model and demonstrate a true same-source lower bound. No compulsory work assertion for arbitrary T5 machines follows. **P versus NP remains OPEN.**
