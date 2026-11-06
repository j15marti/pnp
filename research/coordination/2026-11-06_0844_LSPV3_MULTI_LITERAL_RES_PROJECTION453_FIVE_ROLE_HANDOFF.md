# LSPV-3/453 five-role handoff | 2026-11-06 08:44 PST

**Route B LSPV-3 primary; exactly two Route A (LSPV-2, LSPV-4) and three Route B (LSPV-1, LSPV-3, LSPV-5).** All original task IDs, titles, schedules, time zones, enabled states and historical mixed-calculus weights unchanged. P versus NP OPEN.

## New scoped result

**PROVED/RESTRICTED:** A supplied, original-source-authenticated, non-tautological **pure RES** DAG refutation under any jointly consistent set of literal assumptions A can be converted in one pass to an unconditional original-source RES derivation of a clause contained in the complement of A. Every old shared inference is processed once, at most one new paid RES node per old paid RES. No added case split, discharge, weakening or free zero source. This generalizes LSPV-3/448's single literal, but REFEREE367 had already established a broader context-typed RES equivalence; avoid novelty overclaim.

**PROVED/RESTRICTED:** For two degree-d full parity constraints sharing one wire, the exact boundary CNF with k=2d-2 boundary variables requires exactly $2^{k-1}=2^{2d-3}$ distinct full-width clauses, each derivable by **one** original-source paid RES. Any **one** forbidden boundary assignment is blocked by exactly one such RES step. The d=3 instance uses original strict 3-CNF; d>3 uses width-d sources and is NOT advertised as 3-CNF hardness. This is an exact **multi-output projector cost** compared to a context-specific **one-clause consequence**, not a lower bound for optimal UNSAT mixed refutations.

**Specific K4 mixed shortcut:** Previous LSPV-3/451 spent seven mixed AND3/XOR paid nodes deriving a four-variable affine parity consequence of the original SAT even-charge K4. The same four boundary variables set to zero are blocked by the single original-source RES inference from $(x_{01}\lor x_{02}\lor x_{03})$ and $(\neg x_{02}\lor x_{12}\lor x_{23})$ to $x_{01}\lor x_{03}\lor x_{12}\lor x_{23}$. Complete exact boundary parity CNF needs eight distinct clauses, each one RES. This shows why full projection size cannot be used as the minimum-work lower bound when only a weaker local consequence is required.

## Independent checks

- All 729 consistent partial contexts per original K4: even-charge SAT original has 336 UNSAT contexts, odd-charge UNSAT original has 729.
- Python source/projector testing: 1,065 contextual RES refutations; paid goal-ancestry total 6,179, projected total 1,435, each individual output no more than its input.
- Independent Node checker replayed 42 complete original-source/projected certificates, original-source parity/model controls and 16 single-clause deletions, 7 corrupted controls, 5 malformed DIMACS controls: **5,025 assertions PASS**.
- Exact two-vertex full CNF original-source one-step RES projector independently regenerated for degrees 2,3,4,5: 2,8,32,128 outputs.
- Actual host measurements: producer 1.37 s / 97,160 KiB RSS; independent checker 0.06 s / 35,268 KiB RSS, not FLMV measurements.
- Full code/raw/certificates, output and SHA256 manifest in attached ZIP LSPV3_453_MULTIASSUMPTION_RES_AND_PROJECTION_REPRO.zip, raw SHA256 f6b8c0475ac3ea03b57685aa20d2476f26e84f528a5e53d8d247ee9ef96b486a.

## Precisely scoped next obligations

**To LSPV-1:** Seek a lower-bound obstruction that survives **weaker consequence selection** and shared mixed legal rules, not simply exact boundary CNF projection size; B3 remains OPEN.

**To LSPV-5:** Red-team source-retaining AND/OR branch reconvergence and verify whether a mixed XOR-to-clause export is a *native paid* LOCAL inference, particularly support >3 and private/DEF wires. REFEREE367 already covers pure RES only.

**To LSPV-2/4:** Projection is an upper-bound implementation; if used in Route A, charge *all* source reads, failed branch search, intermediate clauses, proof construction, memory retention and output on the same original machine. Never infer FLMV contraction from this offline test.

Root main.tex not edited because complete bytes and ownership-safe splice not available. This is a new role-owned standalone report and coordination handoff, not an unauthorized change to another role's region. Governing original /341 grammar remains unresolved for some LOCAL/DEF accepted bytes.

Role-owned report: research/agents/lspv-3/2026-11-06_0844_LSPV3_MULTI_LITERAL_RES_AND_EXACT_PROJECTION453.md

Standalone compact code: experiments/arc/lspv3_453_two_vertex_projection_replay.cjs

**Remaining:** full historical native mixed RES/AND3/GF(2)/LOCAL/DEF multi-context compiler; all-legal-rule superpolynomial Wbar_R; noncircular same-calculus B3. P versus NP OPEN.
