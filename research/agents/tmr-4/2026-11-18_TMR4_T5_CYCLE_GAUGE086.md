# TMR-4/086: exact Z5 cycle-gauge transfer and sparse-cycle native OBDD

2026-11-18 Pacific. Primary CSP: source-encoded directed graph over Z5 with R(a,b) iff (b-a) mod5 is 1 or 3. This extends /085, retaining all model-transfer conditions. Restricted mathematics, independently audited finite computation. P versus NP OPEN.

## Exact restricted theorem
Let n be explicit source vertices, m original directed arcs (including loops and opposed arcs), c weak components, and q=m-n+c. Form the signed incidence D over F5 (one distinct column per original arc, -e_u+e_v), and any q-row signed fundamental-cycle basis C of ker D. Each permitted arc difference is d_e=1+2b_e mod5, b_e∈{0,1}. The edge differences arise from vertex colors exactly iff C d=0. Therefore

    Z_T5(G)=5^c * #{b∈{0,1}^m : Cb=2C1 (mod5)}.

Every feasible b has exactly 5^c original vertex-color liftings. Loop and digon controls produce zero without hidden promises. A deterministic syndrome DP over F5^q computes exact counts using O(mq5^q) field-coordinate operations and O(m5^q) O(m)-bit integer additions, plus source authentication, forest/cycle discovery, storage, and output. This is polynomial for q=O(log L) where L is the actual explicit source length.

## Pointwise native compilation
Read all endpoints X of the q nonforest arcs first (at most 2q). The remaining induced graph is a forest. Query those remaining vertices centroid-first by component. Store only colors of the already queried frontier vertices adjacent to future vertices, check each original directed edge as its later endpoint is queried, merge exact-color frontier states, and route failures through complete reject chains. The maximum number of frontier vertices is <=2q+ceil(log2 n)+1. Hence

    native complete OBDD width <= 5^(2q+ceil(log2 n)+1)+1
    native complete OBDD nodes <= n*(5^(2q+ceil(log2 n)+1)+1).

All original assignments, both accepted and rejected, are represented by exactly one complete n-query path, so exact multiplicities are preserved. Preprocessing and output are both paid. A grouped 3-bit binary OBDD uses at most six decoder nodes per native node, retaining invalid-code rejection. Auxiliary-free CNF uses 3n bits and 3n+15m clauses; turning the m edge bits and q modular equations into CNF requires charged long-equation gadgets and is not a constant-size free conversion. All 32 validity-restricted unary domain states persist; 2,048 oriented mask cases were audited.

## Four falsifiers
- Dropping 5^c undercounts trees and edgeless sources.
- Wrong signed cycles or hidden simple-graph promises misclassify directed 3-cycles, loops and digons.
- Counts may not depend on the arbitrary spanning forest; 338 forest-order variants were audited.
- High connection rank, large q or one expensive bit order does not establish necessary computation. The min-size unrestricted interleaved-bit/native FBDD question remains OPEN.

## SAME_REALIZATION and verification gates
G1 source/authentication: 169 canonical inputs (72 SAT, 97 UNSAT), eight malformed rejections, 169 independently rehashed source records. G2 pointwise: Python 139,290 original five-symbol assignments and 181,016 full three-bit words, independent Node.js 342,415 source assignments and the same 181,016 words. G3 exact: 169 signed-cycle counts equal 169 complete native OBDD counts; 163 exhaustive edge-bit counts, 338 alternative forests, 2,048 mask cases, independent Node.js BigInt vertex-domain tree DP on all 169 inputs. G4 repeatability: Python and JS each run twice, byte-identical outputs, zero unexpected failures. Largest tested source n=127, q=6; max OBDD width 2,126 and nodes 15,826; max cycle DP 960 syndrome states.

All source bytes, parsing, graph discovery, ordering, state hashing/sharing, switches, fan-out, eviction/retention, exact arithmetic, output, CNF conversion and cache are charged. No free Fourier transform or arithmetic oracle. Full executable and raw case evidence in TMR4_086_T5_cycle_gauge.zip attached to the research response.

## Reconciliation
Prior /084 block equivalence and /085 interleaved transducer remain intact. This result restricts attention to *high q* for the D4-T5-HIGH-Q-INTERLEAVED-MINIMUM-BARRIER-087 target, requiring genuinely mixed source cases surviving all inexpensive preprocessing and careful comparison of **minimum** representations. Independent mathematics, full LaTeX compilation and physical machine microsteps remain OPEN. P versus NP OPEN.

Background: Barto, Kozik, Niven (2009), SIAM J. Comput. 38(5), DOI 10.1137/070708093; Wegener (2000), Branching Programs and Binary Decision Diagrams, SIAM. Neither source claims the /086 construction.
