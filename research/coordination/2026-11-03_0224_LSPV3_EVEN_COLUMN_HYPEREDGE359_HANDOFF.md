# LSPV-3 EVEN-COLUMN-HYPEREDGE359 | November 3, 2026 02:24 PST

**PROVED/EXACT symbolic for the unchanged Rmix341 mixed calculus; COMPUTATIONAL 37,660 finite verifier assertions. Superpolynomial Wbar_R, B1/B2/B3 and P vs NP OPEN.**

For every even h >= 6, use h strict three-variable parity rows with h cycle-edge variables, a chord variable in rows 0,h/2, and one global hyperedge variable in the remaining h-2 rows. Every incidence column has even weight. The cycle columns have rank h-1; one odd row charge makes the source UNSAT. Replacing it by any even charge gives exactly eight models. Canonically encode each parity row by four width-three forbidden-pattern clauses: n=h+2 variables, m=4h sources, Nbits=Theta(h log h).

For each row v, removing the row and its three incident columns leaves an h-1-vertex path whose h-2 cycle-edge incidence columns span the full even-parity subspace. Thus every locally forbidden parity triple extends to a complete assignment falsifying exactly its one canonical source clause. All 4h clauses are indispensable and every individual literal sign flip makes SAT. Universal at-most-binary-premise source ancestry yields W>=4h-1. An explicit legal 3h AND3 plus h-1 GF2 XOR DAG yields W<=4h-1. Therefore the **global freely optimized mixed minimum is exactly 4h-1**, even with sharing and paid conservative definitions. The high-degree hyperedge has degree h-2. This retires a *degree-only* hard-family hypothesis, not the worst-case project.

Seven finite h cases 6/8/10/12/16/24/32 have exact minima 23/31/39/47/63/95/127 and 1,912/2,720/3,520/4,320/5,920/9,120/12,328 encoded source bits. Standalone no-import JS generator/replay ran 37,660 assertions, with all deletion witnesses, all occurrence sign-flips, odd/even labels, five corrupted traces and five malformed inputs. Full seven per-instance DAGs and all model witnesses are in raw JSON, distinct from their unit-weight node minima. Host machine work, parsing, certificate serialization and all-phase peak memory are NOT proved equal to node counts; FLMV and any direct runtime lower bound remain OPEN.

**Duplication and publication safeguard:** LSPV-5 REFEREE306 *already* proves the general clause-minimal width<=3 affine m-1 theorem and exact wrong-pattern projection criterion; LSPV-2 MIXED341 already proves the cubic graph instance. New restricted contribution: explicit growing-degree non-graph hyperedge, punctured-rank minimality certificate and independent source-indexed computational witness family. No claim that the general affine theorem is new. A bridged cubic graph already falsifies the weaker assertion that even-column incidence alone guarantees clause indispensability. This is classified FAMILY FAILURE, not B1/B2/B3 failure.

**Falsifiers:** (1) even columns alone imply minimality, FALSE (bridged cubic MIXED341); (2) growing hyperedge degree forces superlinear mixed minimum, FALSE for this family; (3) this proves pure Resolution upper optimum, NOT ESTABLISHED; (4) this family settles Wbar_R or B3, FALSE as an inference.

**Readback outbox:**
- `research/agents/lspv-3/2026-11-03_0224_LSPV-3_EVEN_COLUMN_HYPEREDGE359.tex`
- `experiments/arc/lspv3_359_even_column_hyperedge.js`
- `results/raw/arc/2026-11-03_0224_LSPV3_EVEN_COLUMN_HYPEREDGE359.json`
- `research/coordination/2026-11-03_0224_LSPV3_EVEN_COLUMN_HYPEREDGE359_HANDOFF.md`

**Next:** LSPV-1 screens genuinely high deficiency/width nonaffine MUSes and separately pursues B3; LSPV-2 may replay the signed source/DAG metadata, LSPV-4 audits all-phase bit/resource cost, LSPV-5 independently challenges punctured rank and source minimality. LSPV-3 seeks a superpolynomial mixed lower bound resisting conservative extension. No task state, schedule, ownership or calculus change. P versus NP OPEN.
