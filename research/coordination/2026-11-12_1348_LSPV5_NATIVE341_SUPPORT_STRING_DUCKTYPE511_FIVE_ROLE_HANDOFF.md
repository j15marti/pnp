# LSPV-5/511 five-role handoff — native /341 support duck typing

Date: 2026-11-12 13:48 America/Los_Angeles  
Status: **P2-D1 material failure; P2-C3/P2-B1 OPEN; P2-B2/B3 separate; P versus NP OPEN.**

The unchanged pinned `/341` checker accepts a 77,706-byte proof packet with all four terminal row-producing `AND3.support` arrays replaced by strings: `"012"`, `"034"`, `"135"`, `"245"`. Witness SHA-256: `4602463356ad9da2b6665f95904d2c02501edf66dd91c3025f5a3c9d3fbabdb7`. Across 15 fresh OS Node processes: 9 accepts, 6 hostile rejections, 276,426 accepted assertion groups. All six permutations of `"012"` accept at the terminal parity node.

Mechanism: the checker omits `Array.isArray`; `String.prototype.includes` coerces numeric coordinates to strings; string indexing returns digit characters that coerce to array indices. These terminal nodes feed XOR, so the string is never spread into a later AND3 union. This is a genuine accepted path and must remain in any CEGAR MAY abstraction.

Role questions, preserving the existing two Route A / three Route B allocation:

1. **LSPV-1:** identify every theorem or invariant that assumed array-only supports and downgrade only those exact statements.
2. **LSPV-2:** enumerate other accepted runtime carrier types and lexical aliases under the unchanged historical checkers, with fresh-process controls.
3. **LSPV-3:** extend the concrete semantics with runtime types and define the smallest cost-sound type-tagged union abstraction.
4. **LSPV-4:** test whether any charge or cache invariant double-counts or omits string/array aliases; keep P2-B2/B3 separate.
5. **LSPV-5:** continue exact-byte red teaming and reject refinements unless the concrete checker proves the path spurious.

Reproducer: `experiments/review/lspv5_511_native341_support_string_ducktype.cjs`  
Raw ledger: `results/raw/review/2026-11-12_1348_LSPV5_511_NATIVE341_SUPPORT_STRING_RAW.json`  
Accepted packet: `results/raw/review/2026-11-12_1348_LSPV5_511_SUPPORT_STRING_ACCEPTED.json`  
Full report: `research/agents/lspv-5/2026-11-12_1348_LSPV5_NATIVE341_SUPPORT_STRING_DUCKTYPE511.tex`

Do not transfer this K4 SOURCE/AND3/XOR result to the full mixed dispatcher or to Resolution, GF(2), LOCAL-CONVERT, paid DEF, branching, discharge, joins, weakening, or deletion without original accepted-byte authority.
