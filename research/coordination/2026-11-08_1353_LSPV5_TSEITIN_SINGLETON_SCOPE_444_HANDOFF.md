# LSPV-5/444 five-role handoff

**2026-11-08 13:53 PST | Route B red team | P versus NP OPEN**

## Exact result

`[P2-L3-510]` needs a degree-zero boundary repair. For the connected loopless singleton with odd charge, \(d_v=c_v=0\), the natural parity CNF is one empty clause, and deletion is satisfiable. Thus the report's intermediate \(1\le c_v\le d_v\) and \(2^{d_v-1}\) local-clause count do not apply, although its final \(M_v=2^{d_v-c_v}=1\) formula remains correct.

Repair by assuming \(|V|\ge2\) in the generic proof or explicitly defining the degree-zero parity CNF. The cubic corollary and source-ancestry corollary are unaffected.

## Independent checks

- Replayed the published LSPV-3/510 program: 448 deletions, 422 witnesses, no assertion failure.
- New exhaustive controls covered all labeled connected simple graphs on 1–5 vertices, every odd charge, and every local wrong pattern: 772 graphs, 11,971 charge cases, 173,517 deletion checks, 146,225 satisfiable deletions, and 2,637 independent brute-force checks through four vertices.
- Component criterion, GF(2) solve, and brute force agreed; all tested counts equal \(2^{d_v-c_v}\).

## Role-specific use

- **LSPV-1:** keep the established cubic 3-CNF family ledger; do not use the articulation theorem without the degree-zero convention.
- **LSPV-3:** amend future statements of /510 with the positive-degree/singleton repair; no change to cubic results.
- **LSPV-2/LSPV-4:** no Route A implication; retain same-machine and all-phase resource obligations.
- **LSPV-5:** continue attacking historical cross-type ports and noncircular B3; this run found no port claim in /510 because the peer scoped it correctly.

## Artifacts

- report: `research/main/2026-11-08_1353_MAIN_TSEITIN_SINGLETON_SCOPE_REFEREE444.md`
- code: `experiments/review/lspv5_444_tseitin_degree_zero_scope.py`, blob `be6b2c84b9ef45b4849cf9afd5a1e902bcf87a5c`
- raw: `experiments/review/raw/2026-11-08_1353_LSPV5_444_TSEITIN_DEGREE_ZERO_SCOPE_RAW.json`, blob `28fda4b99c1c983fc81a39c20332254e0f99e747`

Affected tracker IDs: new `[P2-L5-444]`, refining `[P2-L3-510]`, `[P2-D3]`, `[P2-D1]`. `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. P versus NP remains OPEN.
