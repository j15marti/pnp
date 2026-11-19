# LSPV-3: critical length-three thread boundary pinning and high-girth theorem correction

Date: 2026-11-18 PST. Owner: historical LSPV-3 Hypergraph & Proof Certificates.
Status: PROVED/EXACT for the fixed-T5 thread pinning lemma; KNOWN THEOREM consequence for arbitrary fixed undirected-girth critical existence; COMPUTATIONAL for H9/H33 replay; OPEN for general SAT witness-time hardness. P versus NP remains OPEN.

## Exact setup and falsifiers

Fixed target is the five-color tournament with R(a,b) iff (b-a) mod 5 is 1 or 3. H is connected and edge-minimal UNSAT; G=H-e is SAT for any original e. The proposed mechanism was a forced modulo-five boundary offset across a complete length-three degree-two thread. Falsifiers: (1) a cited high-girth theorem measures directed, not undirected, cycles; (2) a coloring of H-P realizes a supported three-thread endpoint difference; (3) critical extraction loses connectedness or girth; (4) an explicit deletion H33-e permits a second branch-thread endpoint difference. The first falsifier killed the original Kayll-Morris transfer. The boundary claim survived the finite checks.

## Proven exact lemma: critical length-three thread pinning

Let P be a u-v path of three arcs with two internal degree-two vertices, disjoint from the rest of H except for u,v. Take its traversal u to v and let r be its number of backward-oriented arcs. Delete the entire internal thread to obtain K, retaining u,v.

Every coloring of K has

    c(v)-c(u) = r+1 (mod 5).

At least one K coloring exists. Furthermore every coloring of H-e for e in P restricts to such a K coloring; conversely every K coloring extends in exactly 2^(3-1)=4 ways to H-e for each of the three possible e. The same outside/branching-color assignments occur for all three deletions of P.

Proof. On an arc traversed forward, its endpoint difference is 1+2b, b in {0,1}; traversed backward, it is 2+2b. The three-edge path thus realizes exactly {3+r,5+r,7+r,9+r} modulo five, with unique missing residue r+1 modulo five. Were a coloring of K to realize any supported difference, its two internal vertices could be colored along P, contradicting H UNSAT. Since every H-e is SAT, K is SAT. Removing e leaves two detached rooted path stubs, with two independent options per surviving arc. The 2 remaining arcs give exactly 4 completions for each K coloring. QED.

The forced difference belongs to the FULL degree-two thread endpoints u,v, not necessarily to the actual deleted arc endpoints. Those are distinct binary interfaces. Finding a K coloring remains a legitimate SAT witness-search problem: the 3-bit syndrome is no acquisition oracle.

## High ordinary-undirected-girth theorem: literature firewall

Kayll and Morris, On Colouring Oriented Graphs of Large Girth (2023), DOI 10.55016/ojs/cdm.v18i2.73457, explicitly define girth by directed cycles (section 2). Their theorem DOES NOT prove high ordinary undirected girth. Example: a transitively oriented K4 has directed girth infinity and undirected girth 3. The earlier suggested Kayll-Morris inference is FALSIFIED/RETIRED and must not be used.

The correct source is Gabor Kun, Constraints, MMSNP and Expander Relational Structures, Combinatorica, DOI 10.1007/s00493-013-2405-4; arXiv:0706.1701. For any FIXED girth threshold it provides a polynomial-time relational/ordinary-undirected-girth sparse-incomparability transformation preserving fixed-target homomorphism. Apply it to the explicit 9-vertex 11-arc four-thread T5-UNSAT base with paths BBB, FBB, FFF, BB. Then extract an edge-minimal UNSAT subgraph and discard isolated vertices. Result: for every fixed girth threshold g there exists a connected intrinsically edge-minimal T5-UNSAT oriented H of ordinary undirected girth exceeding g, and every H-e is SAT. This is an existential consequence, NOT a uniform polynomial-time criticalization and NOT an NP-hardness proof for growing-girth critical-deletion witness search. Independently found earlier by LSPV-5; no novelty claim for this existence corollary.

## Independently executed source-backed tests

Pure Python exact arc-consistency/backtracking was run against a locally reconstituted byte-exact H33 source, SHA256 0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac (33 vertices, 44 arcs). A fresh H9 construction (9 vertices, 11 arcs) is UNSAT and every one of its 11 edge deletions is SAT. H33 is UNSAT.

Four H33 length-three threads and their uniquely forced endpoint differences (after removing the whole thread, and for every edge deletion within it):

| word | u | v | forced (c(v)-c(u)) mod 5 |
| --- | ---: | ---: | ---: |
| FBF | 1 | 18 | 2 |
| BFB | 1 | 26 | 3 |
| BFF | 8 | 32 | 2 |
| FBB | 13 | 25 | 3 |

The detailed independent runner performed 20 (4x5) complete-thread endpoint queries, 60 (4x3x5) direct H33-e thread-endpoint queries and 60 (4x3x5) different direct queries at each deleted arc's OWN endpoints. For all 12 relevant deletions, the latter arc-endpoint feasible differences are {0,2,4} while the full thread endpoints remain pinned to one value. Every accepted coloring was checked against ALL retained original arcs.

Source SHA256: 0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac.
Full independently executed script SHA256: 9be1a878638b4e7d7dd1c8e395a3a71393e083bf0f0a266c54d9a4c912a50e3d.
Full local JSON ledger SHA256: 323b7a993396ea8afbfde20eb3331895bb111775512f0ad6d54f48c014091bef.
Compact independent script SHA256: 876e452845d28f93d98c04d0f2e843c6b96fb8cd60f49e80c37dbee3aaf66379.
Finite executions are COMPUTATIONAL evidence and do not give an asymptotic lower bound.

## Resource and complexity firewall

Input source, source authentication, construction of the core, acquiring a K-coloring, internal extensions, and emission/verification of all n original colors remain charged. Arbitrary correct deterministic witness algorithms may use GF(5) syndrome algebra, compact circuits, Gaussian elimination, bounded-treewidth DP, min-fill decomposition, all alternative variable orderings, source recognition and caching. High girth and criticality alone do not force superpolynomial work. The quantified promise-hardness/witness-time claim remains OPEN. A prior peer independently showed H33 has tiny exact elimination width; the 1-symbol endpoint pinning does not alter that upper-algorithm control.

DISJ: PASS for connected intrinsic criticality, no disjoint hard component.
Relativization: no nonrelativizing lower-bound step.
Same-machine time/space: not inferred from structural counting.
Deterministic configuration counting: not invoked for a runtime lower bound.
Natural Proofs/algebrization: no unrestricted separation claim.
Independent peer audit of the new pinning result: OPEN.

Previously published: LSPV-1 critical-thread witness normal form (deletion bijection), LSPV-5 girth transfer firewall (Kun correction), SHIELD1 five-value deleted-ARC signature. These are cited and not claimed new.

NEXT BLOCKER: T5-CRIT-THREAD-PIN-ACQUISITION. Test whether any cross-deletion pinning constraints can be combined on one common feasible source. Do not combine mutually exclusive H-e worlds into a spurious global modulo-five contradiction. Seek a charged uniform witness algorithm or genuine promise-preserving reduction. No agent, paused state, ownership, schedule, tracker or manuscript was changed. MANUSCRIPTS REVIEWED; NO MATERIAL CHANGE.
