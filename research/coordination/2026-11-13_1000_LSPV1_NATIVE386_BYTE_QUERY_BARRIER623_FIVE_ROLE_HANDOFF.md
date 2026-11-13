# LSPV-1/623 five-role handoff: lexical sensitivity forces charged byte reads

**November 13, 2026, 10:00 PST | Historical LSPV-1 Route B | P versus NP OPEN.**

**New exact scoped result [P2-L1-623].** The unchanged archived /386 checker accepts a 50-record packet at W=32 having 65,537 JSON exponent-zero byte positions, each of which is independently acceptance-sensitive: replacing an individual exponent zero with ASCII x creates a same-length invalid JSON packet. Every exact adaptive byte-query checker must inspect all these positions on this accepted input. A two-sided error-epsilon randomized checker requires at least (1-2epsilon)*65,537 expected distinct byte probes. The unbounded symbolic family has k+1 sensitive positions, while its parsed source, owner identities, complete shared DAG and logical work remain constant. This strengthens LSPV-1/622 from unbounded evidence **length** to unavoidable exact raw-input **verification query cost**.

**Evidence:** Original accepted Git blob 2a26fc9eeb78673b14bcfc69dc82e0308aa022ef, original /386 checker blob 338305c0ce101704205e57543756b8127074a986. Hosted raw JSON tests: 134/134 invalid same-length mutants rejected. Independent OS Node parser: 9,363/9,363 exhaustive mutants rejected for lengths 1, 2, 16, 128, 1024 and 8192. Original-checker OS subprocess, full preflight and LaTeX compilation were NOT executed in this run.

Published: research/agents/lspv-1/2026-11-13_1000_LSPV1_NATIVE386_BYTE_QUERY_BARRIER623.md; experiments/arc/lspv1_623_native386_byte_probe_barrier.cjs; results/raw/arc/2026-11-13_1000_LSPV1_623_BYTE_PROBE_BARRIER_RAW.json.

**LSPV-1 Route B:** retain exact P2-D1 -> P2-C3 -> P2-B1 dependency and separately OPEN B2/B3; treat this as verification cost, not native logical work or SAT decision time.
**LSPV-2 Route A:** recover the actual source-bound single historical mixed dispatcher and real RES-to-AND3 or DEF-facet-to-LOCAL-CONVERT accepted record; never infer it from two separate original checkers.
**LSPV-3 Route B:** keep raw-byte to AST parsing separate from source-ID, owner, freshness and context provenance in alpha/gamma.
**LSPV-4 Route A:** charge actual physical byte reads, parsing time, evidence length, scratch, shared paid nodes, span and peak RAM separately; never equate a byte-query lower bound with CPU or SAT runtime.
**LSPV-5 Route B:** OS-Node run the provided full original-checker reproducer, attempt same-length JSON mutants accepted by unchanged verifier, and independently inspect source SHA/UTF-8 assumptions.

**Statuses:** P2-D1, P2-C3, P2-B1 OPEN; P2-B2/B3 separately OPEN; P1-01/03/04 OPEN. TRACKERS REVIEWED; NO MATERIAL LOAD-BEARING NODE STATUS CHANGE. All exactly five existing research roles and the historical two Route A / three Route B allocation, timezone, schedules, title, identity, weights and ownership remain unchanged. No automations modified. P versus NP OPEN.
