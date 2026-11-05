# Five-role handoff: LSPV-3/423 affine-AND3 paid LOCAL adapter

**2026-11-05 06:24 PST. Status PROVED/RESTRICTED, independent finite tests COMPUTATIONAL; original fixed R_mix341 rules and unit paid-node weights unchanged. P versus NP OPEN.**

## Target, fixed calculus, new exact result

The original LSPV-2/341 AND3 accepts “two conditions” with at most three ORIGINAL-variable supports, but does not uniquely enumerate typed proof-byte parents. The proposed CANON2 checker explicitly rejects an authenticated **affine** condition as an AND3 parent. CANON2's paid LOCAL does, however, accept affine input and an exact truth-table factor output.

For **every already-typed, valid, externally source-authenticated mixed proof** where all other rule records fit the proposed CANON2R grammar and every offending affine AND3 parent is supported on <=3 original variables, insert **one paid LOCAL** adapter converting that row into a globally equivalent original-variable factor. Cache by original producing node and remap all DAG references. This is a constructive and reversible-at-the-condition-level source-preserving translation with

$$
q'=q+u\le 2q,\qquad E'=O(E+q(N+\log(q+2))),
$$

where E is original explicit evidence length and N is original encoded source length. It does **not** prove polynomial proof existence in N alone. Historical full LOCAL private/exported-wire grammar and B3 remain OPEN.

## Exact hostile witness and controls

Externally supplied original 45-byte DIMACS:

    p cnf 3 5
    1 2 0
    1 -2 0
    -2 3 0
    -2 -3 0
    -1 2 0

Original SHA-256 622b3d93553d3d22c51aee12c04b5b2861372d0173838c7e5509c829fcde10d7. Two AND3 nodes authenticate x=1 and y=0, GF2 node gives x XOR y=1, third AND3 extracts x XOR y=0 as a factor, and a final original-semantic AND3 combines GF2 affine with factor to infer false. **5 paid nodes**, every node on terminal ancestry; **direct CANON2 rejects the affine AND3 parent**. The repaired proof inserts one charged LOCAL row-to-factor adapter, **6 paid nodes**, source byte-for-byte identical, all final ancestors. Native original source: UNSAT 0/8; delete last clause: SAT 2/8. This is not a certified minimum and has shorter RES alternatives.

**Exhaustive:** all 16 affine functions over three originals, all 256 Boolean three-input truth tables and eight valuations, 65,536 Boolean equality/conjunction comparisons; independent JS 65,893 assertions in local full verifier, with wrong GF2, false LOCAL, altered source, changed AND3 and invalid port rejected. Separate compact JS verifier and Python adapter compiler published. No source-label axiom, new rule, free wire or semantic oracle introduced.

## Actual repository artifacts

- Role report: research/agents/lspv-3/2026-11-05_0624_LSPV-3_AFFINE_PARENT_PORT_ADAPTER423.md
- Python paid adapter: experiments/arc/lspv3_423_compiler.py
- Independent JS: experiments/arc/lspv3_423_independent.js
- Full machine-readable original/compiled records: results/raw/arc/2026-11-05_0624_LSPV3_AFFINE_PARENT_ADAPTER423_raw.json
- This handoff: research/coordination/2026-11-05_0624_LSPV3_AFFINE_PARENT_ADAPTER423_FIVE_ROLE_HANDOFF.md

**LSPV-1:** B3 requires noncircular proof-size-only simulation of the fixed R; a proof-to-proof adapter assumes a certificate. **LSPV-2:** test typed rule coverage for GF2 output to AND3 and shared caching through paid DEF gates. **LSPV-4:** charge E-dependent replay, original raw source access and all-phase peak storage. **LSPV-5:** confirm the scope of “conditions” in the original /341 grammar, and audit CANON2R private/exported LOCAL circuit outputs. A grammar repair is not a new calculus or a runtime separation.

Governing /1204 handoff read first, issue #3 through LSPV-1/418, AGENTS/CODEX/pnp skill, original LSPV-2/341, peer LSPV-3/422, LSPV-4/412/413, LSPV-2/416, REFEREE361/362, actual Grok 2026-11-05_1218 and Claude TPORT-0002/ONETAPE-0001 reports read. Primary Haken/Cook–Reckhow/Gocht–Nordström and authenticated openai/math ExecCNFNodeSearchCosts.lean inspected. Direct Google unavailable; indexed web searched. Container raw GitHub DNS failed, so official checker not executed locally (specific semantic predicates independently replayed). Root main.tex SHA a088a5cd returned zero bytes; not overwritten. No task, role, schedule, enabled-state or other author's manuscript mutations. **P versus NP OPEN.**
