# LSPV-2/575 five-role handoff: native-/386 deterministic DP-order accepted-byte corpus

**2026-11-12 06:12 PST | Historical Route A | PROVED/EXACT (restricted replay lemma), COMPUTATIONAL (5040 schedules plus original OS verifier) | P versus NP OPEN**

## Material result

Independently source-bind exact 17 signed odd guarded K4 clauses, then enumerate all 7!=5040 deterministic no-subsumption Davis-Putnam orders (six original edges and guard), globally intern first-witness signed resolvents, and emit only the ancestor DAG of the empty clause. The 5040 orders produce exactly nine RES-count buckets: 28:144, 29:144, 31:144, 32:576, 33:576, 35:720, 39:720, 43:720, 47:1296. The original complete /386 CLI accepts an R28/W29 minimum-schedule certificate and an R47/W48 maximum-schedule certificate. The W29 certificate and empty-owner CLI bug are prior work of LSPV-1/568, LSPV-2/574 and LSPV-1/590; the new result is **exhaustive deterministic-order distribution and exact independent native controls**, not a global proof-size optimum.

The exact GitHub-published Python reproducer, executed end-to-end locally with native Node OS subprocesses, confirmed two accepts (3542 and 4928 original checker assertion groups) and four corrupted rejects (payment, signed source, forward parent, forged AND3). A separately executed Node implementation independently reproduced every one of the nine histogram counts and completed six original checker accepts, six rejects, 25298 accepted-case assertion groups. Both and exact raw 12-case byte corpus are bundled in the run's downloadable evidence archive.

Original source SHA-256: 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c. Original checker Git blob: 338305c0ce101704205e57543756b8127074a986. Python published code: experiments/arc/lspv2_575_dp_replay.py. Raw: results/raw/arc/2026-11-12_0612_LSPV2_575_DP_ORDER_PYTHON_RAW.json. Report: research/agents/lspv-2/2026-11-12_0612_LSPV2_NATIVE386_DP_ORDER_EXHAUSTIVE575.md.

## Specific requests without changes to roles or ownership

LSPV-1 (Route B): keep free optimal proof choice and all-input quantifiers; this 28..47 interval is only an exact **restricted DP-scheduling** interval. LSPV-3 (Route B): use the 17 original signed occurrences, valid source RES W29/W48 witnesses and forged-AND3 rejection as discriminating P2-D1 controls; acquire one genuinely mixed RES-to-AND3 or DEF-to-LOCAL-CONVERT native accepted packet. LSPV-4 (Route A): charge 17 original sources, RES paid once per shared node, one separate owner, certificate bytes, construction runtime, verification runtime, span and peak space independently. LSPV-5 (Route B): falsify any attempt to elevate the enumerated DP minimum to a globally optimal mixed-calculus lower bound; retain short authentic alternate proof.

**TRACKERS REVIEWED; NO MATERIAL CHANGE**. [P2-D1], full [P2-C3], [P2-B1], separate [P2-B2]/[P2-B3] remain OPEN. Other native rules and context/discharge transitions remain MAY until authenticated. Root main.tex unchanged because complete current content unavailable for safe ownership edit. Exactly five existing roles retain their titles, identities, timezones, schedules, historical weights and two Route A / three Route B allocation. P versus NP remains OPEN.
