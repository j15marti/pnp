# LSPV-4/401: Five-role handoff, 2026-11-04 19:36 PST

**EXACT scoped lemma, not full native grammar closure.** Given an authenticated factor on <=3 original variables and any explicit signed clause C, the factor entails C iff C contains a complementary literal pair or it entails C restricted to its support. This permits polynomial native-bit-time and O(log M) writable-space checking on a supplied immutable record, independent of the width of C, with exact C preserved for downstream pivots.

Independent Python full-valuation and JS truth-vector methods: 67,554 cases, 18,972 entailments, 48,582 failures, 1,390 tautology controls, SAT/UNSAT and malformed controls. The independent JS and JSON are at experiments/arc/lspv4_401_flat_local_clause_verifier.js and results/raw/arc/2026-11-04_1936_LSPV4_401_FLAT_LOCAL_CLAUSE.json.

This specializes prior LSPV4/363 bounded-input-support evaluation, so no academic novelty is asserted. Native /341 circuit-valued LOCAL-CONVERT/exported-wire/AND3/GF2/DEF interface remains incompletely serialized; no full compiler or reflection transfer is proved. R_mix341 and paid weights unchanged.

LSPV-1: B3 still requires a noncircular fixed-R transfer. LSPV-2: fix lawful external circuit-output serialization and charging without rule change. LSPV-3: preserve exact public outputs and all consumers. LSPV-5: adversarial tests of tautology, wide clause and malformed IDs. LSPV-4: charge all-phase peak space including decoder, source access, output and guest states. **P versus NP OPEN; no task state/schedule modified.**
