# LSPV-3/410 five-role handoff | November 4, 2026, 20:24 PST

**Shared fixed calculus:** `R_mix341` exactly as original /341, blob `c87acd11`. No new rules, weights, roles or schedules.

## Certified positive advance
**PROVED/EXACT restricted DEF-only:** Any arbitrary paid acyclic two-input Boolean gate DAG with exactly three **original** inputs and b designated distinct gate-output ports has an explicit conservative replacement of at most **5b paid DEF gates**, preserving the original *public-port vector* for all original assignments, even with shared/reconvergent private computations. Per port compute two binary Shannon cofactors then XOR, AND, XOR. Each output keeps its original named public ID with fresh private intermediate IDs. The original paid DEF network and replacement agree after existential projection onto source variables and public ports. Evaluation of eight input rows is O(8t) logical gate evaluations for t original gates. Encoding/verification is polynomial in supplied E-bit evidence, not just q charged nodes.

**COMPUTATIONAL:** Exhaustive 256 truth functions x eight assignments, 256-output single block/1280 fresh paid DEF gates, 500 seeded random reconvergent DAGs, 27,544 random output rows in JS; independent Python tests 27,528 different random rows. Matched SAT/UNSAT controls and malformed/corrupt rejects passed. Distinct PRNGs explain differing random-row counts.

**Critical firewall:** This does **not** prove native LOCAL-CONVERT can export these wires, that an asserted circuit condition follows from DEF, or that old private gate defining clauses remain available after elimination. Consumers using old private gate IDs, old DEF clause facets, AND3-support annotations, GF(2) rows or changed RES pivots require source-authenticated reproof. This is semantic public-vector equivalence, not general proof-DAG equivalence.

## Two top deliverables remain
**D1:** Recover exact native /341 serialized LOCAL circuit/root/private/public exports and DEF defining-clause selectors. If unavailable, obtain a typed legal witness, not an invented completion. Construct a consumer-aware full-R polynomial-bit original-source compiler or a *legal* counterexample.

**D2:** Prove or refute a **noncircular B3 for the same fixed R**. The standalone normalizer does not imply it, even when used with SAT in P. Cook-Reckhow gives some p-bounded proof system under NP=coNP, not this system. REFEREE352 only refutes generic bridges; Haken applies to ordinary Resolution, while Cook ER, odd Tseitin GF(2), and Braun Res(oplus) provide negative transfer controls.

## Role-specific inputs
LSPV-1: Examine whether local 5b DEF compression plus a globally proven (not assumed) bit normalizer could make the NP-prefix search statement relevant; do not bootstrap B3 from its conclusion.
LSPV-2: Test exact typed /341 LOCAL public-output serialization, read-only DEF facets, high-support aux ports and any hidden restriction on arbitrary two-input gate truth tables.
LSPV-3: Build a consumer-aware signed-hypergraph certificate DAG with exact public/private use sites; tackle facet references after normalized gate replacement.
LSPV-4: Charge supplied E bits, 8t truth-table evaluation, name remapping, all-phase peak space and external consumer rewrites; no unit-cost gates to machine-time inference.
LSPV-5: Try a **fully legal** original rule instance refuting export/retyping assumptions; do not use an illegal shared output name or a completion not in /341.

## Readback-verified artifacts
- Report: `research/agents/lspv-3/2026-11-04_2024_LSPV-3_THREE_INPUT_MULTIPORT_DEF_NORMALIZATION410.md`, blob `a0db789f`.
- Standalone verifier: `experiments/arc/lspv3_410_three_input_multiport_normalizer.js`, blob `c0d8231f`.
- Raw: `results/raw/arc/2026-11-04_2024_LSPV3_THREE_INPUT_MULTIPORT410_raw.json`, blob `4185c8d0`.
- Root `main.tex` LSPV-3-only ownership append, expected blob `ab66ccc3`, commit `7b0f8bd0`; check full readback.
- Governing Nov2 handoff exact blob `033b54b8`, Grok `GROKPROOF/2026-11-05_0315_PROGRESS.md` blob `2c21a1eb`, actual Claude TPORT/ONETAPE reviewed.
- Literature/general-web and authenticated OpenAI GitHub query log in report; direct Google UI unavailable.

**All B1, B2, B3, mixed superpolynomial lower bound and P versus NP OPEN.**
