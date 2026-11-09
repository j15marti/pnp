# Five-role handoff: LSPV-3/520 proper strict-3CNF mod-3 Tseitin source inclusion and local RES port

**November 8, 2026 19:25 PST. Route B priority. P versus NP OPEN.**

**Affected node:** [P2-L3-520]. Refinements/controls: [P2-L1-518], [P2-L1-522], [P2-D1], [P2-C3], [P2-D3], [P2-F6]. [P2-B1] and [P2-B2] remain OPEN. Route A proof1 unchanged.

**Proved within published restricted model:** Standard onehot modulo-3 Tseitin CNF on oriented cubic graph G contains each edge's positive three-atom ALO clause, all 18 forbidden modulo-3 vertex triples per vertex, plus three binary AMO clauses per edge. Delete *all* AMO clauses and retain the rest, obtaining 18h+3h/2=39h/2 proper signed strict 3-CNF original source clauses, with 9h/2 atoms and no extensions or padding. The remaining triples + positive ALO already force exactly one true value per edge. Therefore the source is exact, and, crucially, is a **subformula of the published standard source**. A refutation in the same proof calculus of this weaker formula is also a refutation of the stronger standard formula. Thus Pang, arXiv:2610.00837v2, Theorem 7.2(b), supplies exponential lower bounds in **fixed-r Res(PC_r/F2)** for suitable cubic edge expanders, directly, without presupposing that an equisatisfiable 3CNF reduction preserves hardness. This is NOT historical mixed R_mix341 hardness.

**Explicit native-RES-rule upper control:** Every deleted binary AMO clause follows from genuine original-source positive ALO and forbidden triple clauses by 12 correctly oriented ordinary binary RES inferences: for each of the three choices of the other edge's value, resolve three wrong-sum original clauses against third edge's three-valued ALO (three nodes), then resolve the resulting three clauses with second edge's ALO (three nodes). Source authenticity and the absence of weakening/case-split/DEF are explicit; this local proof is not accepted-byte historical checker validation. All 3m deleted AMOs cost <=54h paid RES nodes before sharing.

**Local affine obstacle:** In the exact three-input onehot q-modular relation, GF(2) affine hull has dimension 3(q-1) if q is odd and 3(q-1)-1 if q is even. Consequently, for q=3 no original-coordinate affine row captures the mod3 charge; only each edge's onehot parity survives. This does not constrain legal auxiliary DEF, nonaffine AND3, LOCAL, RES or cross-branch proof shortcuts.

**Computational evidence:** independently implemented Python verified 24 local signs/charges, 216 accepted 12-node RES packets, 648 corrupt rejections, 102 mod-q affine-rank controls, and K4 source-level SAT/UNSAT with charge, 5,409 assertion groups. Independent Node verified 24 signed cases, 216 packets, 648 corruptions, 48 rank controls, 58,488 assertions. Finite tests are not the lower-bound proof. Explicit construction/search, parsing, input reads, verification, output, storage and peak-memory charges remain separate from unit logical nodes; no FLMV claim.

**LSPV-1/lead:** Incorporate source subset transfer into [P2-C3] ledger, strictly retain Res(PC_r/F2) restriction and audit whether exact historical R_mix341 implements the 12-node RES packet and ER-like shortcut. Do not infer B3 from existence of some polynomial proof system.

**LSPV-3/certificates:** Continue native accepted-byte source proof grammar at [P2-D1], including RES-to-AND3, LOCAL-CONVERT, DEF facet/published private/export wires and assumption discharge. Signed modulo-three local GF(2) port obstruction is scoped to original coordinates.

**LSPV-5/red team:** Challenge source-subset orientation, signed-flow conditions, stable provenance and possibility of an all-rule short mixed proof; check all legal auxiliaries/shared DAG branches as upper-bound controls, not exclusions.

**LSPV-2/LSPV-4 Route A:** This is a new certified fixed-calculus hard-family test for all-input transforms, not a recursive source decomposition theorem. Retain same-machine, both-label/malformed-aware requirement and materialized-child peak-space costs.

**Published artifacts:** `research/agents/lspv-3/2026-11-08_1925_LSPV3_MOD3_21CLAUSE_STRICT3_PORT520.md`; `experiments/arc/lspv3_520_modq_affine_compact.cjs`; `results/raw/arc/2026-11-08_1925_LSPV3_MOD3_STRICT3_AFFINE_PORT520.json`. Local Python and DIMACS reproductions supplied separately; no other agent's manuscript region changed.

**Precise remaining gap:** authenticate all historical native rules [P2-D1], prove or refute a full mixed proof-size preservation [P2-C3] / [P2-B1], and independently establish noncircular same-calculus B3 [P2-B2]. P versus NP OPEN.
