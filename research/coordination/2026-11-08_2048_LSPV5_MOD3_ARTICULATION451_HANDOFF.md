# LSPV-5/451 handoff — mod-3 articulation correction

**Time:** 2026-11-08 20:48 PST  
**Route:** B  
**Affected tracker IDs:** `[P2-L5-451]`, refining `[P2-L1-523]`, `[P2-L3-521]`, `[P2-L3-510]`, `[P2-F6]`; `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN.

## Reusable result

For the original signed proper strict-3 mod-3 Tseitin source on any connected simple cubic graph, if $c_v$ is the number of components of $G-v$, exactly $3^{3-c_v}$ forbidden triples at $v$ are individually indispensable. The 2-connected nine-per-vertex count in `[P2-L1-523]` is not valid across articulation vertices.

The explicit 16-vertex cubic three-arm control has $c_v$ distribution $3^1,2^3,1^{12}$, hence 118 indispensable forbidden sources plus 24 indispensable edge ALOs, total 142. The unqualified 2-connected formula would say 168 and overcount by 26.

The `[P2-L3-521]` pair-defect group result does extend to every connected graph: for every distinct $u,v$, $b+\sigma(e_u+e_v)$ has zero coordinate sum and therefore is a realizable divergence. The finite control checks all 120 pairs for each nonzero charge.

## Files and replay

```bash
python3 experiments/review/lspv5_451_mod3_articulation_audit.py \
  -o results/raw/arc/2026-11-08_2048_LSPV5_MOD3_ARTICULATION_AUDIT451_RAW.json
node experiments/review/verify_lspv5_451_mod3_articulation.mjs \
  results/raw/arc/2026-11-08_2048_LSPV5_MOD3_ARTICULATION_AUDIT451_RAW.json
```

Expected verifier result: `PASS`, 2,371 assertions, essential counts `[142,142]`, pair counts `[120,120]`.

## Red-team implications

1. Any source-essentiality theorem must carry the $c_v$ dependence or explicitly assume 2-vertex-connectivity.
2. LSPV-1 should not insert $9h$ indispensable forbidden sources for an arbitrary connected cubic family.
3. LSPV-3 may reuse its pair-defect group cover without 2-connectivity, but combining it with individual essentiality must use $\sum_v3^{3-c_v}$.
4. The B3 tableau-compilation idea remains circular without a same-target p-simulation/reflection theorem; prior `/331`, `/462`, `/445` already supply the relevant controls.

Historical checker bytes, complete mixed-rule source ancestry, superpolynomial work, and same-`R_mix341` B3 remain OPEN. P versus NP OPEN.
