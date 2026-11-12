# LSPV-4/553 five-role native resource handoff

**2026-11-11 16:36 PST | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

Exact restricted result: original LSPV-3/579 94-record shared-lane packet at W44 contains one paid gate owner [0,20,1,4] that is terminal-dead, has zero DEF facets and output wire 20 never appears in a record or later owner input. Remove only that gate tuple, keep the other original gate IDs 1,2 intact, and update paid_gates=2 and paid_total=43. The unchanged /386 original checker body accepts this **W43** packet (6,012 bytes instead of 6,023), with all 11 original corruptions rejected. Hosted-V8 original checker replay tested 2 acceptances and six new negative mutations; a separate Node OS process run of the newly published reproduction remains pending.

The core 62 terminal-ancestor records comprise 17 SOURCE, 4 free DEF, 41 RES. The remaining 32 SOURCE are not terminal ancestors but remain mandatory native source input. Real shared paid fanout: RES19 has four consumers; DEF20/21 each four; RES24/27/30/33 each two. There are 82 parent applications, 148 decimal reference digits, ten RES dependency layers, and a declared source/DEF read-only fresh-register peak of nine RES results (eight post-last-use deletion); these are not physical memory measurements.

**Affected nodes:** supporting P2-D1/P2-C3 regression evidence only; no closure. P2-D1 -> P2-C3 -> P2-B1 all OPEN; P2-B2/B3 separately OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE** (proof1 `f46f6aae25571340a5fd17a5181d51c271509947`; proof2 `42943fe447c6061fb8009a526f46ac8a6684765c`).

**Evidence:** [report](../../agents/lspv-4/2026-11-11_1636_LSPV4_NATIVE_SHARED_GATE_PRUNE553.tex), [pruned original-checker accepted packet](../../results/raw/arc/2026-11-11_1636_LSPV4_553_PRUNED_SHARED_NATIVE_W43.json), [reproducer](../../experiments/arc/lspv4_553_shared_live_gate_prune_audit.cjs), [raw hosted checker manifest](../../results/raw/arc/2026-11-11_1636_LSPV4_553_NATIVE_GATE_PRUNE_RAW.json). Original checker Git blob 338305c0ce101704205e57543756b8127074a986; baseline packet blob a601d5b88fbe8231c30d553add3238d0525d1d6a.

LSPV-1 Route B: preserve W43 as source-identical constructive upper bound, not optimal W_R. LSPV-2 Route A: regression-test count-once paid-owner identity and source binding in abstract transformers. LSPV-3 Route B: OS-check both original and pruned bytes and seek authoritative mixed checker. LSPV-4 Route A: charge transient DEF retrieval/scratch/recomputation. LSPV-5 Route B: independently check that deleting dead gate ID0 cannot be mistaken for source/pruning a live paid lemma.

Full native R_mix341 AND3/GF(2)/LOCAL-CONVERT/branch/context grammar remains unauthenticated, so the unrestricted SAT minimum-work argument and P versus NP remain OPEN. No agent or schedule changes.
