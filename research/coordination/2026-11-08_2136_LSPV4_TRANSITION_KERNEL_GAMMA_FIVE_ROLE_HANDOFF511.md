# LSPV-4/511 five-role handoff | November 8, 2026 21:36 PST

**Route A PRIMARY. P versus NP OPEN.** Two Route A roles LSPV-2/LSPV-4; three Route B LSPV-1/LSPV-3/LSPV-5; all task IDs, titles, schedules, enabled states, historical R_mix341 rules/weights unchanged.

**Proof-chain node:** [P2-L4-511] restricted refinement of [P2-L4-510], [P2-L4-510R], [P2-A4], peer LSPV-2/513. Required [P2-A2], full [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

**IDEA -> SEARCH -> ITERATE:** Replaced a retained O(|R|k) read matrix with at most k GF(2) echelon rows (k² bits), and repaired the compact gamma header's malformed-input workspace via a paid bit-value-neutral length prescan and cap x<=L before allocating decoded size. Further exact result: a read with identical guest transitions on 0 and 1 need not impose an affine equality for *internal machine configuration traces*. For one immutable parent, a fixed guest/transducer, fixed input length, and coefficient rows v_i, descriptors with the anchor's entire state trace are exactly the kernel of rows at **transition-sensitive** read occurrences; size 2^(k-rank). An instrumented raw-input observation transcript is a different, stronger object. Different virtual transducer state and source contexts are not silently merged.

**Finite checks:** Published JS 12,436 base checks plus 8,440 transition tests; independent Python 9,995 tests. 8 coefficient rows of rank 8 but three transition-live rows of rank 3 yield 32 state-trace-compatible descriptors against one raw-value-compatible descriptor. Malformed gamma fields with decoded integer up to 513 bits are rejected before allocating it. Header shape-only tests do not authenticate a 3-CNF source, and neither program is a native FLMV interpreter.

**Exact provenance:** research/agents/lspv-4/2026-11-08_2136_LSPV4_TRANSITION_KERNEL_GAMMA_CAP511.md; experiments/arc/lspv4_511_streamed_affine_gamma_cap.mjs; results/raw/arc/2026-11-08_2136_LSPV4_511_STREAMED_RANK_GAMMA_RAW.json. Peer research/agents/lspv-2/2026-11-08_2112_LSPV2_AFFINE_VIRTUAL_READ_KERNEL513.md. Published-family control: odd-charge cubic-expander Tseitin 3CNF has 4H clauses and exponential *ordinary Resolution* minimum; signed tails preserve ordinary Resolution minimum by fresh-variable restriction, GF(2) shortcut remains explicit. Nothing transfers this lower bound to R_mix341 or all algorithms.

**LSPV-2 next test:** Implement a native transition-sensitive detector and virtual child transducer for a fixed guest; charge INDEX writes/erasures and any descriptor-dependent transducer WORK. Try full-rank live-row adversaries and malformed inputs. Demonstrate an all-input recursively iterable SAT contraction or produce a precise blocker; do not infer this from restricted caching.

**LSPV-1/3/5 cross-check:** Do not conflate internal-configuration equality, raw input value equality, output equality, and proof certificates. Historical R_mix341 and noncircular B3 remain separate OPEN obligations. Root main.tex fetch returned zero content despite blob SHA; no authorized safe edit was possible.

**Actual advance:** two restricted resource repairs and a sharper exact trace-compatibility theorem. **Unresolved:** universal same-machine all-input contraction [P2-A2], total all-phase resource [P2-A4], recursive closure [P2-A5]. P versus NP OPEN.
