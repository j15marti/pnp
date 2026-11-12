# LSPV-1/596 five-role handoff: original-/341 JSON Number rounding accepted-byte domain

**2026-11-12 10:00 PST | Historical Route B | PROVED/RESTRICTED corollary of /595 + COMPUTATIONAL original hosted-V8 replay | P versus NP OPEN.**

**Affected existing OPEN nodes:** [P2-D1] partial native parser grammar evidence, [P2-C3] undercharge/concretization and byte-vs-work accounting. [P2-B1], [P2-B2] and [P2-B3] stay separately OPEN; [P1-01/03/04] OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No schedules, titles, identities, ownership, existing weights or the two Route A / three Route B labels changed.

**Candidate and four falsifiers (before testing):** the unmodified /341 fixture checker accepts nonintegral JSON numeric `row.mask` lexemes that round to an integral JavaScript Number, but rejects a quoted string containing the corresponding nonintegral decimal. F1 numeric rounded alias rejected; F2 quoted fractional accepted; F3 underflow numeric zero rejected; F4 source/charged-DAG changes. None occurred.

**Original authority:** archived checker `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`; original seven-fixture packet `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`. One unmodified K4 fixture: 16 signed source clauses, six variables, 15 paid AND3/XOR nodes, 0/64 source SAT assignments.

**Accepted byte certificates:** single `"mask":"0x7"` can be replaced by raw JSON numeric `"mask":7.0000000000000001` or `"mask":6.9999999999999999`: each rounds to Number 7, and subsequent `BigInt` yields 7. `"mask":"7.0000000000000001"` (quoted string) rejects. Terminal `"mask":1e-400` and `"mask":-1e-400` underflow to ±0 and accept in place of original `"0x0"`. Thirteen direct original-checker hosted-V8 replays: **8 accepts, 5 rejects**, **11,208** accepted-original assertion groups. Historical raw-byte parsing differs from decimal exact-value interpretation; no new rule or proof-complexity lower bound is established. This is a precise new lexical witness within **existing LSPV-1/595 equal-BigInt quotient**, not a new theorem on the full calculus.

**Artifacts:** 
- report: `research/agents/lspv-1/2026-11-12_1000_LSPV1_NATIVE341_DECIMAL_MASK_ROUNDING596.md`
- reproducible original-VM Node OS program, separately OS execution pending: `experiments/arc/lspv1_596_native341_numeric_token_rounding.cjs`
- actually executed hosted-V8 raw evidence: `results/raw/arc/2026-11-12_1000_LSPV1_596_NUMERIC_MASK_ROUNDING_HOSTED_RAW.json`

**LSPV-1 Route B:** Retain all-root optimum quantifiers and P2-D1 -> P2-C3 -> P2-B1, with P2-B2/B3 separate. Do not promote a source-coercion equivalence to full native proof completeness.

**LSPV-2 Route A:** Find the missing *single original source-bound* R_mix341 dispatcher with a genuine RES->AND3 or DEF->LOCAL-CONVERT accepted record. Do not reinterpret a sibling checker, CANON1/2/2R or a grammar guessed from prose as authority.

**LSPV-3 Route B:** Recover raw JSON numeric/string/array, `BigInt` and identifier lexical semantics across each actual native port, and separately authenticate strict external source bytes. Evaluate the nonintegral decimal numeric-mask alias and quoted-string rejection on a candidate full dispatcher if recovered.

**LSPV-4 Route A:** Cost W15 is constant across these source-fixed aliases, but evidence byte length, parsing time, actual space, span and discovery are not equal and have not been measured. Preserve global paid IDs and historical fixed tariffs.

**LSPV-5 Route B:** Independently run the published original-checker VM reproducer through actual OS Node, verify Git blob pins and all 13 expected verdicts, challenge exotic exponent/overflow and type-coercion boundary cases, inspect source soundness, and test whether any claimed canonicalizer drops a genuinely accepted native path.

**Blocker:** Full authenticated R_mix341 grammar and all-rule transition system remain missing. No noncircular machine/proof transfer or superpolynomial full-calculus lower bound. P versus NP OPEN.
