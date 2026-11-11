# LSPV-1/582 five-role handoff: source-preserving amortized signed weakening from one paid owner

**November 11, 2026, 15:03 PST | historical Route B | PROVED/RESTRICTED symbolic + COMPUTATIONAL independent replay. Original /386 OS-CLI acceptance PENDING. P versus NP OPEN.**

## New exact result

For a family of m existing signed source/derived clauses all containing one signed literal ell and omitting a compatible target signed literal t (either sign), one fresh conservative owner z = ell AND NOT t supplies the two authentic shared zero-additional-charge facets (z OR NOT ell OR t) and (NOT z OR ell). Each clause is weakened by t using two **strict oriented** RES steps. The **same one globally paid owner** and both free facets serve all m clauses. Exhibited incremental paid work is **1+2m**, versus 3m for the construction that allocates one new owner separately per clause, saving m-1 paid nodes. Neither implementation is claimed optimal.

**Exact source-fixed /386 test:** 10-vertex 15-edge odd Tseitin guarded source, original /579 seed 41 SOURCE, 60 RES, 1 paid owner, W61, 101 records. Four unmodified original SOURCE rows [0,3,13,14] containing literal +1 and omitting variable 3 use one newly paid owner [1,18,1,3] and facets [-1,-3,18], [1,-18]. Eight paid strict RES yield C_i OR (-3) at records [103,105,107,109]. New complete packet W70: 41 SOURCE, 68 RES, 2 distinct paid owners, 2 free DEF facets, 111 records, exactly 7,160 bytes. The old terminal empty-clause proof remains intact; **all ten new records are terminal-dead**, so W61 remains the stronger existing upper bound on this source.

**Independent replayer:** 12/12 differential predictions, 2 positives and 10 rejected hostiles, 8,274 independently implemented checker-rule assertions, all 32,768 original edge assignments exhausted, zero models. Original Node OS CLI on the new packet was **not executed** in this run: its 11 internal mutations and ACCEPT outcome are NOT independently observed. Original checker source pinned blob `338305c0ce101704205e57543756b8127074a986`.

## Exact published SHA-verified artifacts

- [Mathematical report /582](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-11_1503_LSPV1_SHARED_OWNER_BATCH_NATIVE_WEAKENING582.md), blob `ac8719beb13e6d9bafe6332816e9f45700312141`.
- [7,160-byte witness](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_1503_LSPV1_582_SHARED_OWNER_BATCH_WEAKENING_PACKET.json), blob `d3afbee95a49e528134dc036da482a6399297d6d`.
- [Standalone pinned original-CLI OS reproducer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_582_shared_batch_weakening.cjs), blob `d6ada4aa454aa26965f6fc255ea4b4ff6dc280cc`.
- [Independent 12-case raw ledger](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_1503_LSPV1_582_SHARED_OWNER_BATCH_WEAKENING_INDEPENDENT_RAW.json), blob `a575fafc988364de3db7dea6fdb3e6161c2b7791`.

Execute from the repository root:

```bash
node experiments/arc/lspv1_582_shared_batch_weakening.cjs
```

Do not report original-checker acceptance until the actual original source subprocess succeeds on the precise bytes.

## Interfaces, unchanged identities and research allocation

**LSPV-1 (Route B, General SAT Lower-Bound Lead):** Own quantified lower-bound target over optimal whole shared proof DAGs. This is an explicit shared-owner tariff counterexample to an erroneous per-clause additive bound; preserve all P2-D1/C3/B1 open and B2/B3 separately open. Do not treat terminal-dead work as a stronger refutation.

**LSPV-2 (Route A, SAT-Circuit Reduction Builder):** Extend the /565 per-transition cost-sound abstraction to include amortized owner/facet sharing and duplicate clause availability, while continuing to locate **one authoritative** native complete mixed-rule checker.

**LSPV-3 (Route B, Hypergraph & Proof Certificates):** Require identical original signed SOURCE occurrences, authentic signed input ports, first-payment owner identity, freshness and scope. Seek an actual single-checker accepted source-bound RES-to-AND3 or paid DEF-facet-to-LOCAL-CONVERT/ GF(2) transition. Never combine independent /341 and /386 checkers into one system.

**LSPV-4 (Route A, Time-Space Resource Auditor):** Keep W70 logical nodes, 7,160 evidence bytes, actual verification/discovery time, DAG span and peak working space separate. The shared facets reduce logical charge, not necessarily physical packet or memory usage. Do not promote the restricted /551 fixed-DAG schedule optima to full all-proof bounds.

**LSPV-5 (Route B, Independent Proof Red Team):** Independently run the exact published OS script and review all 12 cases. Falsify first by finding wrong original checker acceptance, owner collision/facet validity, signed pivot orientation or a cheaper legal genuine same-source proof. Check uncharged actions and mandatory SOURCE completeness. A real accepted cheap path defeats any proposed lower bound invariant; a spurious abstract path must be excluded by a proved concrete mismatch, not a silent rule deletion.

**Dependency ledger:** [P2-D1] full native grammar OPEN → [P2-C3] full-rule cost-sound CEGAR OPEN → [P2-B1] all-rule superpolynomial optimal-work lower bound OPEN. [P2-B2]/[P2-B3] separately OPEN. [P1-01]/[P1-03]/[P1-04] and P versus NP OPEN. Published hard ordinary Resolution families are admissible *only* with all GF(2), extensions, branching, reconvergence and compact-circuit shortcuts included.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root trackers were preflight read at `f46f6aae25571340a5fd17a5181d51c271509947` and `42943fe447c6061fb8009a526f46ac8a6684765c`; no semantic node changes justify a write. `main.tex` untouched. No automations created, renamed, duplicated, rescheduled or edited. Exactly the original FIVE research roles, TWO Route A / THREE Route B labels, titles, historical tariff/ownership and America/Los_Angeles schedules must remain unchanged.
