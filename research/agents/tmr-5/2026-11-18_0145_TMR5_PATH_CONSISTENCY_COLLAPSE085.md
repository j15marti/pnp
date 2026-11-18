# TMR-5/085: independent path-consistency refutation of the /084 Grötzsch AC-3 obstruction

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Research date:** 2026-11-18 01:45 America/Los_Angeles. **Status:** independently reproduced finite executable certificate and a conditional-on-certificate monotonicity theorem; external proof review OPEN. **P versus NP OPEN.**

## New finding and correction of the lower-bound interpretation

The 71-vertex, 100-arc **genuine T5 instance** from TMR-5/084 is UNSAT, and all 71 single-vertex anchors pass AC-3. But **ordinary, unanchored binary path consistency (PC, 3-consistency on complete binary pair relations) refutes the same graph**. No source decoder, anchored vertex, gadget contraction, or SAT solver is used by this T5 decision procedure.

Specifically, store a pair relation P[i,j] subset of Z5 x Z5 for every ordered variable pair, use equality on i=j, all 25 pairs on unconstrained distinct pairs, and R(a,b) iff b-a mod 5 in {1,3} for each directed arc. Iterate the sound operation

P[i,j] <- P[i,j] intersect { (a,b) : exists z, (a,z) in P[i,k] and (z,b) in P[k,j] }

for all i,j,k, maintaining transpose symmetry. Empty pair relation certifies UNSAT. The unanchored T5 /084 NO graph produces an empty pair relation; the matched 71-vertex, 100-arc YES control reaches a nonempty fixed point. The same calculation performed on their 11-vertex undirected C5-homomorphism source graphs likewise separates the controls.

This does **not** prove PC decides arbitrary T5-CSP. T5 is NP-complete, and previous TMR-5/077 exhibited a non-Taylor cyclic-term obstruction.

## Independently executed evidence

| Instance | |V| / |arcs| | Exact C5-hom count | AC-3 no anchor | AC-3 after each of 71 distinct label-0 pins | PC3 in-place | PC3 synchronous |
|:--|:--|--:|:--|:--|:--|:--|:--|
| Mycielski(C5), UNSAT | 71 / 100 | 0 | survives | 71/71 survive | REFUTES in 2 scans, first empty (2,5) via k=0 | REFUTES in 5 rounds |
| 11-vertex bipartite control, SAT | 71 / 100 | 660 | survives | 71/71 survive | consistent after 3 scans | consistent after 5 rounds |

Source C5 relation PC likewise refutes the NO source, with the in-place contradiction occurring on pair (1,10) through intermediate vertex 6, and accepts the YES source.

**Cross-check:** two independently coded implementations were executed: in-place 25-bit row-mask relational composition and a synchronous Jacobi solver using explicit pairs and existential third-label witnesses. Both agreed on the two 71-vertex cases. On 150 independently generated random T5 digraphs (n=2..6, seed 20261118085), both algorithms agreed on their classifications and full pair relations whenever consistent, with no false UNSAT compared with independent exhaustive assignment enumeration. The 150 cases did not yield PC false positives and do not establish unrestricted completeness.

The exact executed local full verifier, raw JSON and run log were archived in the TMR-5/085 evidence package. A compact self-contained verifier is separately committed under experiments/tmr/.

## Family-wide monotonicity theorem (restricted)

Let H be the explicit 71-vertex /084 UNSAT graph and G any extension containing an isomorphic constraint subinstance H (extra vertices and arcs allowed, without removing H's original arcs or identifying two distinct H vertices). If the unanchored path-consistency closure on H has an empty pair relation, so does the closure on G.

**Proof:** At initialization, every pair relation among H's vertices in G is contained in the corresponding relation of H; all additional constraints only restrict possibilities. The PC deletion update is monotone in each operand. Therefore the entire H-only deletion sequence is reproducible or stronger in G, and the empty relation persists. The /084 h-block NO chains, including optional attached high-treewidth grids, contain the original H as a genuine subinstance, so **every member of that /084 infinite NO family is refutable by generic unanchored PC**. This is a finite-certificate-dependent infinite-family conclusion, not a proof of a general graph classification.

With |Sigma|=5 fixed, naive full-scan PC has a conservative polynomial O(n^5) worst-case bound: O(n^3) triple checks per scan and at most 25n^2 strict deletions across pair relations; more efficient worklist algorithms exist. The concrete family is thus decidable without recognizing the source construction. The /084 AC-3 result remains correct; only its use as a purported increasingly robust local-obstruction candidate is weakened.

## Ranked proof-chain status

| Arrow / claim | Status |
|:--|:--|
| Exact fixed T5 homomorphism is NP-complete | PROVED by primary semicomplete-digraph theorem: [Bang-Jensen, Hell & MacGillivray, 1988](https://doi.org/10.1137/0401029); explicitly T5 has directed 3-cycles 0->1->2->0 and 0->3->4->0 |
| Five-arc C5-to-T5 gadget, /084 construction | Independently reproduced, RESTRICTED |
| Every-singleton-anchor AC-3 misses /084 NO | PROVED by finite exhaustive certificate, unchanged |
| Generic unanchored PC misses /084 NO and its glued family | **FALSIFIED**: ordinary PC refutes all |
| Local consistency of some fixed level decides *all* T5 instances | Not established; algebraic obstructions forbid the unrestricted generalization |
| OBDD/tensor rank -> unavoidable arbitrary-machine work | OPEN |
| Superpolynomial SAT lower bound / P!=NP | OPEN |

**Next gate:** construct a concrete authentic mixed YES/NO T5 family surviving PC, singleton PC and higher local-consistency levels; run adaptive/direct solvers before any resource lower-bound promotion. The correct algebraic target is the absence of bounded-width polymorphisms, not AC-3 complexity on a selected gadget family.

**Safeguards:** No changes to agent identity, ownership, schedules, or peer manuscripts. No full LaTeX build, formal proof-kernel run, or outside mathematical review. P vs NP remains OPEN.
