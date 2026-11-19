# TMR-3/095: intrinsic-critical T5 witnesses via minimum-product branch trees

**Date:** 2026-11-18 PST. **Owner:** TMR-3 / PNP Time-Space Tradeoffs. **Status:** PROVED (constructive upper bounds and explicit counterexample), COMPUTATIONAL (finite audits), OPEN (unrestricted witness-time lower bound). **P versus NP OPEN.** Independent peer review pending.

## Statement and quantifiers
T5 is the fixed tournament on Z5 with arc constraint x_v-x_u in {1,3} mod 5. Input (H,e) is promised to have a connected edge-bearing *physical-arc-minimal UNSAT* H and a designated deleted arc e; the output is a complete coloring of H-e. The algorithm does not assume a promise-membership oracle, witness advice, or a refutation. Original source parsing, path recovery, state enumeration, reconstruction, full output and verifier are charged; five global rotations are factored out.

## Theorem A (PROVED): general binary tree search
Every connected n-vertex T5 instance can be solved by fixing one vertex to color 0 and choosing one of **two** differences along each edge of an undirected spanning tree. Non-tree arcs are then checked. Each rooted satisfying coloring corresponds to exactly one of at most **2^(n-1)** choices. Separate connected components can be solved independently. This is also the exact GF(5) binary cycle formulation: tree increments are sigma_e (1+2z_e), z_e in {0,1}, and chords impose modular disjunctive constraints; Gaussian elimination alone does not solve the Boolean-domain problem.

## Theorem B (PROVED): minimum-product branch-core witness search
In an arc-minimal UNSAT H, every maximal degree-two thread has length at most three. Suppress threads and keep exact endpoint difference supports. Delete the *entire support* of the one thread containing e, since its two portions then extend independently. For each surviving unordered branching-vertex pair uv intersect all its thread supports into S_uv. Bridgelessness ensures the remaining branch graph is connected. Choose a spanning tree T minimizing W = product_{uv in T}|S_uv|, found by Kruskal in nondecreasing support size; fix a root color 0 and branch only through tree-supported differences. Check non-tree supports as soon as endpoints are colored. Five-state path DP then reconstructs the complete H-e witness.

With b branch vertices and n' edge-bearing vertices,
**Q(H,e) <= min(2^(n'-1),W) <= min(2^(n'-1),4^(b-1))**
complete terminal combinations suffice. Intersections may produce singleton supports, giving factors 1. A direct conservative simultaneously charged random-access realization uses O((N+1)^4(1+Q)) time and O((N+1)^2) peak bits, where N is full source bit-length. A conservative direct sequential-tape realization uses O((N+1)^8(1+Q)) time, O((N+1)^3) bits. These are upper bounds for specified executions, **not machine-independent lower bounds**; a native TM audit is still pending. Full explicit output alone gives Omega(n') time.

## Theorem C (PROVED/FALSIFIED candidate): a cycle of rigid pins is NOT intrinsically arc-minimal
For k>=3 form a cycle of terminal vertices v_i and a private vertex w_i per segment. Give each segment arcs v_i->v_(i+1), v_i->w_i, w_i->v_(i+1). Each three-arc pin forces endpoint difference +1. Consequently the full H_k is UNSAT iff k not congruent 0 mod 5, and the *module-level* modular cycle is minimally inconsistent. But H_k is not physical-arc-minimal UNSAT: all unchanged modules force +1, so the altered module would need difference 1-k mod 5. Removing its direct arc leaves support {1,2,4}, whereas removing one private-side arc leaves {1,3}; their intersection is {1}, inconsistent with the required difference. At k=3, only 6/9 physical arc deletions restore SAT; at k=6, **0/18** do. Thus rigid gadgets cannot be declared intrinsically critical merely because their compressed modular cycle is minimal. This is an explicit falsification of one tempting hard-family generator, not a barrier to all generators.

## Computational audit (COMPUTATIONAL, no failed assertions)
- Independently enumerated all 3^9=19,683 absent/forward/reverse cross-edge patterns of K3,3. Found 216 labeled edge-minimal UNSAT cases using all six vertices; tested all 1,512 arc-deletion witness inputs. Exact minimum-product search bounds at most 3, with root-fixed witness counts 4 to 15.
- Rechecked five-vertex six-arc critical H on every deletion; 480 general connected graphs and 150 disconnected/isolate graphs against independent exhaustive enumeration.
- Reconstructed all nine short-thread relations, tested all 512 subfamilies: maximum irredundant intersection size 4, with size counts (9,26,24,4). Verified saturation for every four-arc path orientation.
- Tested pin cycles k=3,...,9 and all 126 arc deletions, matching the theorem.
- Separately used a five-bit-domain AC-3 exact solver to shrink 29 UNSAT random orientations into edge-minimal cores. Twelve cores had 3 to 6 branching vertices; all 145 deletions in those twelve were constructed and verified. One n=10,m=13,b=6 source had W<=48 across all deletions, versus 5^5=3125 unrestricted branch tuples and 2^9=512 original-tree tuples.
- Deterministic primary JSON audit reproduced byte-identically in two runs. Original external branch-core ZIP remains unavailable; its short-thread nine-relation statement was independently tested. Independent mathematical peer audit, integrated manuscript compilation and native Turing-machine execution pending.

## Time-space transfer firewall
The FLMV 2005 SAT time-space forbidden region is a language-*decision* result on a specific random-access model. It cannot be imported into a promise of guaranteed SAT witness inputs merely from T5 NP-hardness. Any uniform reduction must specify both promise cases, witness decoder, source-expansion exponent, generator access cost and simultaneous workspace. Rank, representation, restricted branching, oracle-query, and proof-complexity costs do not by themselves force machine running time. All four established verification gates remain restricted/non-separation. No superpolynomial worst-case lower bound is obtained.

**Next:** C3-T5-PHYSICAL-CRITICAL-TRANSFER096. Design a uniform intrinsically physically critical and growing-girth source family, or disprove a proposed mechanism; prove every physical arc essential, and test all source-derived algebraic/graph algorithms. P versus NP OPEN.

Sources: Fortnow, Lipton, van Melkebeek & Viglas (2005), https://doi.org/10.1145/1101821.1101822 ; Burjons et al. (2019), https://arxiv.org/abs/1906.10078 ; Bang-Jensen, Hell & MacGillivray (1988), https://doi.org/10.1137/0401029.

**Local complete reproducibility:** tmr3_t5_tree095.py, critical_samples095.py, audit095.json, critical_samples095.json and standalone full report in TMR3_T5_WEIGHTED_CORE095_Reproducible.zip attached to the run.
