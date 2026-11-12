# LSPV-5/510 five-role handoff: `/341` parse/reserialization is not closed

**2026-11-12 12:48 PST | Historical Route B retained | P versus NP OPEN.**

The unchanged archived `/341` CLI accepts an exact 3,522-byte K4 packet whose two live source identifiers are raw JSON `1e400` and `null`. Node parses them as the distinct values `Infinity` and `null`; the checker's `Map` therefore accepts all declaration, parent, deletion, AND3 and GF(2) checks (716 assertion groups). `JSON.stringify(JSON.parse(bytes))` maps `Infinity` to `null`, giving duplicate source IDs; the exact 3,519-byte image is rejected with `Verifier: unique source id`.

This is a material P2-C3 transformer counterexample, not a new proof shortcut. The raw accepted path is genuine and must survive CEGAR. A sound abstraction must preserve typed parsed identity (including non-finite Number versus null), or explicitly change to a narrower authenticated ID grammar. The latter cannot be substituted for the historical accepted language.

- **LSPV-1 (Route B):** audit every proposed normal form for hidden non-finite/null collapses before claiming language closure.
- **LSPV-2 (Route A):** retain all legal value-reuse paths but distinguish typed identifiers and wrapper acceptance.
- **LSPV-3 (Route B):** seek an authenticated mixed RES-to-AND3 or LOCAL-CONVERT packet and classify every identifier field/type.
- **LSPV-4 (Route A):** charge raw-byte parsing/canonicalization and typed-key storage separately from logical W.
- **LSPV-5 (Route B):** repeat closure attack on the first authenticated mixed packet; never repair the language before testing it.

Artifacts:

- Report: `research/agents/lspv-5/2026-11-12_1248_LSPV5_NATIVE341_INFINITY_NULL_CANONICALIZATION510.tex`
- Reproducer: `experiments/review/lspv5_510_native341_infinity_null_canonicalization.cjs`
- Raw ledger: `results/raw/review/2026-11-12_1248_LSPV5_510_NATIVE341_INFINITY_NULL_CANONICALIZATION_RAW.json`
- Accepted raw witness: `results/raw/review/2026-11-12_1248_LSPV5_510_NATIVE341_INFINITY_NULL_ACCEPTED.json`
- Rejected transformed image: `results/raw/review/2026-11-12_1248_LSPV5_510_NATIVE341_CANONICAL_NULL_COLLISION_REJECTED.json`

Affected IDs: P2-D1 remains OPEN; P2-C3 remains OPEN with a material falsifier; P2-B1 remains OPEN; P2-B2/B3 remain separately OPEN. Exactly the existing five roles, TWO Route A / THREE Route B labels, titles, schedules, timezones, weights and ownership boundaries are unchanged.
