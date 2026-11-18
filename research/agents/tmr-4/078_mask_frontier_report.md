# TMR-4/078 | Exact 12-mask / 32-mask boundary in five-symbol BEAT CSP

Owner **TMR-4 / PNP Cost-Sound Abstraction**. Pacific date **2026-11-17**. Layered on TMR-4/077; schedules, agent identity, manuscript and safeguards preserved. **No P versus NP proof.**

## Exact mathematical statement

For Sigma = Z5 and R(x,y) iff y-x mod 5 ∈ {1,3}, forward-checking an unassigned domain only against already assigned neighbors produces **exactly 12 possible masks**: full, empty, five singletons, and five pairs B_a={a+1,a+3}. In-neighborhoods and out-neighborhoods of fixed colors generate the same five pairs and distinct pairs meet in at most one color.

**Falsifier:** AC propagation against other *unassigned* variables does not preserve the 12-mask family. Pin x to 0 via two edges from the five-vertex palette, add y->x and z->y. AC gives D_y={2,4}, D_z={1,3,4}.

In fact **all 32 subsets of Z5 are attainable** as AC domains at a root even when deleting the five queried palette vertices leaves a tree. Define U(S)={x: exists y∈S, R(x,y)} and V(S)={x: exists y∈S, R(y,x)}. A new source arc implements each operator; identifying roots of otherwise disjoint tree gadgets implements intersection. Pin P_a={a} with arcs p_(a-1)->root and p_(a-3)->root after querying a literal five-vertex T5 palette. Eight orbit representatives suffice:

| Root set | Construction |
|---|---|
| ∅ | P0 ∩ P1 |
| Z5 | free root |
| {0} | P0 |
| {0,2} | U(P3) |
| {0,1} | U(U(P2)) ∩ U(U(V(P0))) |
| {0,1,2} | V(U(U(P1))) ∩ U(U(V(P0))) |
| {0,1,3} | U(U(P2)) |
| {0,1,2,3} | V(U(U(P1))) |

Their cyclic translations cover all 32 masks. Full tree AC is exact on extendable root labels. Every two distinct masks can be distinguished by a later two-arc palette-pin test to a color in their symmetric difference. This establishes **32 distinct unary support states for this exact local interface**, not a lower bound on general FBDDs or decision algorithms.

## Exact original-source compilation and Boolean comparison

32 canonical graph inputs with only beat arcs were constructed and round-trip authenticated. Five palette vertices are genuine input variables, not baked-in constants. Their induced tournament has exactly five cyclic automorphisms. After choosing one gauge, the remaining vertices form a tree and permit exact polynomial-time sum-product DP. Thus, despite realizing all 32 masks, these are EASY source problems. Each full graph is compiled into a complete five-way OBDD that queries **every** original variable on every path, including dead-prefix completions. Frontier-state merging preserves every original assignment's decision and exact accepted/rejected multiplicities. Largest tested: n=12, m=20, width=76, 271 OBDD nodes.

A direct no-auxiliary Boolean 3-bit encoding uses three legal-code clauses per vertex and 15 forbidden-pair clauses per arc, exactly **3n+15m clauses**, width at most 6, with parsimonious counts. Seven binary decision nodes replace one five-way node. There is no asymptotic advantage from encoding symbols directly.

## Four verification gates

1. Algebraic: 32 constructive mask certificates; all 496 pairwise future contexts distinguish; exactly five palette rotations.
2. Source: 32 valid canonical raw graph encodings; six malformed input controls rejected; every source has at most 12 vertices and 20 arcs.
3. Semantic: 32 independent integer tree-DP vs AC support checks; 32 full-source OBDD exact counts; 17 complete brute-force counting controls; independent Node.js BigInt implementation matched all 32 source SHA-256, masks and full-source counts.
4. Encoding and pointwise: 4,096 random original-assignment comparisons among direct predicate/complete OBDD/CNF; 1,024 invalid Boolean code checks, 5,120 CNF tests total; zero unexpected failures. Two complete runs in each language were byte-identical.

Evidence SHA256: Python raw JSON \`37469b117221dcaae01d4d375384d97b82ee383c7ea9c63d5e846053d97bf3d9\`; independent JavaScript raw JSON \`7ab5a41e4aed3a25de1f2a32e018503a39982a9050dc28cad71993e13ce5a156\`. Complete scripts, raw graph sources, and audit outputs are in the downloadable TMR4_078_T5_mask_boundary.zip research package (delivered in the source conversation). The full Python and JS executables are not committed to the repo in this branch.

## SAME_REALIZATION cost ledger

The compiler starts from the same canonical source bytes used to check truth. Account for L-byte parsing, arc storage, connectedness/forest recognition, all 5-value mask filtering operations, fixed variable-order and frontier discovery, actual stored OBDD states, five outgoing arcs per node, state merging, reject completions, exact BigInt arithmetic, explicit CNF clauses, and output. Source generation, canonicalization and hash computation are separately charged to the experiment generator, not hidden in solver timing. No cache eviction, order switching, external swap or Z5/Fourier transforms were used, and no zero-cost powers are inferred from their absence.

## Four falsifiers and handoff

- F1 12-mask closure under full AC: **false** by a depth-two three-mask example.
- F2 context-exact merger of 32 local masks: **false** via all 496 future palette pin tests.
- F3 local mask proliferation necessarily implies high source runtime: **false** on the entire easy rooted-tree family.
- F4 5-way alphabet intrinsically outperforms a Boolean representation asymptotically: **false for the implemented fixed-width translations**.

TMR-2 should distinguish pure assigned-neighbor forward checking (12 masks) from full bidirectional AC (32 masks). TMR-4 should investigate a genuinely dynamic necessary resource after permitted source-aware tree/backdoor/twin/module/affine decomposition. Source-level SAT decision, full-input verification, and exact counting must not be conflated. General-machine lower bound remains **OPEN**.

References: Freuder, *JACM* 29(1):24–32 (1982), DOI 10.1145/322290.322292; Dechter & Pearl, *Artificial Intelligence* 34(1):1–38 (1987), DOI 10.1016/0004-3702(87)90002-6.
