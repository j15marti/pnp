# LSPV-5 REFEREE372 handoff: strict-subclause normalization passes; exact facet identity fails

**November 5, 2026, 15:48 PST · Route B · PROVED/EXACT CHECKER-RELATIVE + LEGAL COUNTEREXAMPLE · P versus NP OPEN.** Fixed historical `R_mix341`, weights, roles, tasks, schedules and enabled states unchanged.

## Result

All 16 arbitrary binary DEF tags accepted by the frozen proposed CANON2R checker compile to at most three AND-only DEF owners. All 64 exposed old facets have actually accepted strict-Resolution representatives; each is a subclause with at most two Resolution ancestors. Trimmed validation traces use 2--12 paid nodes.

Exact positional-facet identity is false for 24/64 facets. Minimal witness:

$$z=0\quad\leadsto\quad z\leftrightarrow(b\land\neg b).$$

The old distinct-input facet $(a\lor b\lor\neg z)$ cannot be derived exactly from replacement clauses mentioning only $b,z$, since strict Resolution cannot introduce absent $a$. The checker accepts the stronger derived clause $\neg z$. This is a legal accepted-byte counterexample, not a malformed-proof exploit.

## Scope firewall

This proves a local DEF+Resolution subclause interface for the frozen **proposed** CANON2R completion. It does not authenticate historical `/341` bytes and does not yet translate all mixed consumers. In particular, strengthened original-coordinate clauses may interact nontrivially with AND3/LOCAL, while GF(2) uses typed affine ports. Full rule-by-rule proof normalization and same-system B3 remain OPEN.

The first serialization failed because REFEREE371 used row index $2a+b$ while CANON2 uses $a+2b$; an explicit bit permutation repaired the bytes. This is relevant to any claimed source-authenticated normalizer.

## Established-family control

Cubic-expander odd-Tseitin remains exponentially hard only for ordinary DAG Resolution in the cited model. Native GF(2)/AND3 has the known exact $4h-1$ shortcut, so the family does not give a full-mixed lower bound. LSPV-1/428's $2^t-1$ explicit-row compiler versus one native GF(2) join is the same transfer warning. PHP Resolution hardness is controlled by polynomial ER/Frege shortcuts; equisatisfiable 3-CNF conversion is not enough.

## Verification

Actual CANON2 and CANON2R checkers accept every trimmed trace. Independent Node replay passed 941 checks. Counts: 16 functions, 64 facets, 40 exact, 24 proper-subclause only, at most 3 replacement definitions, at most 12 paid validation nodes. Corrupt truth, nonfresh output, corrupt pivot, hidden payload, raw hash mismatch, and SAT-source controls all reject.

Artifacts:

- `research/main/2026-11-05_1548_MAIN_CANON2R-DEF-FACET-IDENTITY-COUNTEREXAMPLE-REFEREE372.md`
- `experiments/arc/lspv5_372/canon2r_binary_def_normalizer_referee372.py`
- `experiments/arc/lspv5_372/verify_canon2r_binary_def_referee372.mjs`
- `results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_raw.json`
- `results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_certificates.json`
- `results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_independent.json`

## Exact next gap

For each native mixed consumer, prove that replacing an exact old facet by its stronger accepted subclause preserves legality and context, including original-source authentication and shared/reconvergent ancestry. Otherwise give the smallest accepted mixed trace where it fails. Independently, B3 still needs a noncircular compiler from bare `SAT in P` to polynomial proofs in this same fixed calculus. Root `main.tex` was not touched. P versus NP remains OPEN.
