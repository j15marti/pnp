# LSPV-5/484 handoff — Resolution-parent binary64 underflow

**Pacific timestamp:** 2026-11-11 02:51 PST  
**Role:** LSPV-5 Independent Proof Red Team, historical Route B  
**Status:** material `[P2-D1]` evidence; P2-D1, P2-C3, P2-B1, separate P2-B2/B3, and P versus NP remain OPEN.

## Advance

The unchanged archived `/386` verifier accepts raw Resolution-parent tokens `1e-324` and `-1e-324` as parent zero. These raw tokens denote exact, mathematically nonzero JSON decimals before binary64 conversion. The verified proof outcome remains 50 paid nodes, one DEF owner, 49 RES nodes, 69 records, 17 SOURCE records, and 4,492 assertions.

For every integer $k\ge324$,

$$
0<10^{-k}\le10^{-324}<2^{-1075},
$$

so ECMAScript round-to-nearest maps $\pm10^{-k}$ to signed zero. The script sampled $k=324,325,400,1000,1000000$ with both signs and replayed every packet in the unchanged verifier. `5e-324`, `1e-323`, `1e400`, and quoted `"1e-324"` reject.

This is a genuine accepted path and cannot be removed as a spurious CEGAR trace. A byte- or exact-decimal-authenticated abstraction must retain it or prove a coherent normalization. The local repair is exact decimal-token parsing, exact mathematical integrality and range validation, and unique unsigned-decimal serialization before any binary64 conversion. That repair is not yet a full historical-calculus normalizer.

## Evidence

- Report: `research/agents/lspv-5/2026-11-11_0251_LSPV5_RES_PARENT_BINARY64_UNDERFLOW484.md`
- Executable: `experiments/review/lspv5_484_res_parent_binary64_underflow_audit.js`
- Raw result: `results/raw/arc/2026-11-11_0251_LSPV5_484_RES_PARENT_BINARY64_UNDERFLOW_RAW.json`
- Checker blob: `338305c0ce101704205e57543756b8127074a986`
- Baseline packet blob: `b9c1d306c300a3f1917ee01ecab16358ac77d4de`
- First positive hostile packet digest: `ba64ceccfd859c756ea19ff76c94d26706b602897940f85e5331772e394f584d`
- First negative hostile packet digest: `3b0837a4193e01cd2f8e4d6b94ec2f977eabe5f1954273839e665418f95e2077`

## Cross-role requests

- **LSPV-1:** retain this exact-decimal alias in any P2-D1 grammar and do not claim binary64 integer checks authenticate mathematical integrality.
- **LSPV-2:** normalizers must validate exact tokens before Number conversion and rewrite every coherent identity occurrence or reject the packet.
- **LSPV-3:** shared-DAG concrete states need raw/token provenance; parsed positional identity alone is insufficient.
- **LSPV-4:** charge long-token parsing/evidence bits and all simultaneously live strings/objects; no logical-work-to-space inference follows.
- **LSPV-5:** next attack another actual native field or prove a cross-field exact-token repair; do not extrapolate this finite verifier to the unidentified full historical parser.

Exactly five existing roles, titles, schedules, Pacific timezone, ownership boundaries, historical weights, and TWO Route A / THREE Route B labels remain unchanged. No task or agent was created, renamed, rescheduled, duplicated, enabled, or disabled.
