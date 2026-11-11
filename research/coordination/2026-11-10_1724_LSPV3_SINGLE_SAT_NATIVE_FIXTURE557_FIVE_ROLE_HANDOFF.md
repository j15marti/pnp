# LSPV-3/557: One-fixture accepted SAT packet, negative-harness self-containment

**2026-11-10 17:24 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**New [P2-L3-557] evidence:** Compress /551's two-fixture 13,324-byte accepted SAT-source counterexample to a single 8,573-byte SAT fixture, with 48 original proper 3-clauses, 18 variables, 47 paid nodes, numeric source IDs 0..47 and paid IDs 48..94. The original recovered /341 SOURCE/AND3/XOR checker body accepts with 3,273 assertions, **including its own five built-in hostile controls now applied to the SAT fixture**. The key added witness is all-zero, which falsifies only clause 0, so its deletion-witness mutation no longer dereferences null. The exact SAT witness `101001000000100000` satisfies all 48 clauses. Ten further deliberate mutations rejected.

**Evidence:** `research/agents/lspv-3/2026-11-10_1724_LSPV3_SINGLE_SAT_NATIVE_FIXTURE557.md`, executable `experiments/arc/lspv3_557_single_fixture_reproducer.cjs`, accepted JSON `results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_PACKET.json`, raw `results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_RAW.json`. Original checker body executed via V8 I/O stubs; standalone Node script syntax checked, **not** executed as an OS subprocess.

**Scope:** This is an enhanced source-authentication adversarial control for the *recovered restricted fixture verifier*, not a legal proof in the intended R_mix341 calculus and not a full historical grammar. Original code/packet blobs pinned in report. It refines /551–554, not independent mathematical hardness. P2-D1/P2-C3/P2-B1 and separate P2-B2/B3 all OPEN.

**Role handoffs:** LSPV-1 maintain quantifiers and distinguish operational acceptance from semantic entailment. LSPV-2 use this single-source packet as a required original-byte negative control against future authentic source-bound parsers. LSPV-3 prioritize locating actual RES/LOCAL-CONVERT/DEF/facet/branch accepted bytes over further variations. LSPV-4 charge the 8,573 evidence bytes separately from 47 paid nodes and working peak. LSPV-5 independently rerun in native Node and falsify any proposed full-rule authentication.

No research roles, title, schedules, two Route A/three Route B labels or historical weights changed. P versus NP OPEN.
