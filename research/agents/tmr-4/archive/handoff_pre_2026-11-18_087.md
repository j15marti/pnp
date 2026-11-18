# TMR-4 compact handoff | 2026-11-18 PST | /086 Z5 cycle-gauge and sparse-cycle OBDD

**Program continuity.** TMR-4 / PNP Cost-Sound Abstraction, same enabled state, ownership, title, existing hourly schedule, root living manuscript `main4_PNP_COST_SOUND_ABSTRACTION.tex`. Previous /084 block equivalence and /085 live-cache s*6^p at-most-once reverse transducer remain unchanged. The exact /085 predecessor handoff was archived byte-for-byte at `research/agents/tmr-4/archive/handoff_pre_2026-11-18_086.md`. This /086 branch stacks on the /085 draft branch, without merging main or changing other agents.

**Exact source.** Original authenticated canonical JSON with explicit vertices [0,...,n-1] and sorted directed arcs, n<=L and m<=L. Beat relation R(a,b) iff (b-a) mod5 in {1,3}, including permitted source loops/digons (which yield UNSAT). No 3-SAT relabeling.

**THEOREM /086.** Given n vertices, m original directed arcs, c weak components and q=m-n+c, let C be any signed q-row fundamental-cycle matrix over F5 of the original multigraph. The precise count is

    Z_T5(G) = 5^c * #{ b in {0,1}^m : Cb = 2C1 (mod5) }.

A fully charged source-aware exact syndrome DP costs O(mq5^q) field-coordinate operations and O(m5^q) arbitrary-precision integer additions, plus parsing, cycle-basis generation, hash/state arithmetic, memory and output. Therefore polynomial in original length L if q=O(log L). This is not a general T5 polynomial-time algorithm.

**NATIVE OBDD /086.** Query endpoints of q nonforest arcs (<=2q) first, then centroid-order the remaining forest. Keep exact colors of active source frontier vertices; check original arcs on the later endpoint, and complete rejected paths with all remaining queries. Complete five-way OBDD width <=5^(2q+ceil(log2 n)+1)+1 and nodes <=n times that bound. Preserve decisions and both original full-assignment multiplicities. Grouped three-bit Boolean OBDD <=6 native nodes per native query; direct aux-free CNF has 3n+15m clauses. The edge-bit modular formulation has m bits, not free CNF gadgets. Full 32 domain masks retained, all 2048 orientation cases tested.

**FALSIFIERS.** Gauge factor 5^c required; cycle signs and loops/digons must be honored; alternate forest selections cannot change the count; source-aware low-q algorithms falsify any necessity inference from fixed-order bad Boolean complexity. Large q is not itself a hardness certificate.

**GATES and SAME_REALIZATION.** Python 169 canonical sources (72 SAT, 97 UNSAT), eight malformed rejections, 139290 source pointwise checks, 181016 full-code checks, 163 all-edge-bit brute checks, 338 alternative forest checks, 2048 masks, 169 complete OBDDs. Independent Node.js verified 169 source SHA-256 hashes, 169 BigInt vertex-side tree-DP counts, 342415 pointwise source inputs, 181016 Boolean code words, 121673 pinned boundary assignments. Two deterministic reruns each; no unexpected failures. Largest n=127, q=6, width2126, nodes15826. Charge raw input, basis, ordering, branching/sharing, precision, output, CNF and all external transforms. Physical TM microsteps and independent mathematical review OPEN. Full Python, JS, raw input records and JSON logs are in the ZIP evidence package; GitHub contains manuscript, research report and compact raw summary.

**NEXT.** D4-T5-HIGH-Q-INTERLEAVED-MINIMUM-BARRIER-087: mixed source-authenticated hard-core families with high q that survive cycle-syndrome DP, endpoint backdoors, sparse-tree OBDD, 32-mask, twin, palette, 1-3 separator and quotient controls. Compare the **minimum** unrestricted interleaved-bit Boolean FBDD with minimum five-ary FBDD on the identical source family; arbitrary machine lower-bound transfer OPEN. P versus NP OPEN.
