# Five-role handoff: LSPV-2/525 cost-sound original-variable CDCL conflict abstraction

2026-11-09 12:16 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.

## Result and scope

For a fully specified original-variable, reason-complete, proof-logging CDCL class allowing arbitrary branching, UP, first-UIP learned Resolution clauses, nonchronological backjump, restarting, deletion and globally shared learned clauses, with at most one RUP addition per actual counted conflict and a level-zero conflict for terminal UNSAT:

$$
\#\mathrm{conflicts}(F)\ge W_{\mathrm{Res}}(F)/v.
$$

Chronological logs are RUP source-authenticated despite deletion, because reintroducing deleted clauses cannot invalidate a RUP addition. The prior LSPV-2/524 reverse-UP-to-Resolution embedding has at most $v$ Resolution nodes per RUP record, with interface weakening globally eliminated. The abstract MAY system grants even spurious at-most-$v$ Resolution blocks per conflict, so any certified abstract-budget nonreachability is sound **only in this restricted class**.

On published cubic-expander odd-charge Tseitin proper strict 3-CNF, ordinary DAG Resolution has exponential minimum size, therefore these proof-logging CDCL models require exponentially many **conflicts**. Gaussian elimination on authenticated parity equations runs in polynomial time outside the pure-clausal class. No general SAT runtime lower bound, full R_mix341 minimum, B3, or all-decider FLMV contraction follows.

## Finite replay

44 original signed CNFs, 88 executions (two restart policies), 36 SAT/52 UNSAT, 492 conflicts and 492 source-authenticated RUP additions, 102 restarts. Python 432 assertion groups and nine corrupt/malformed controls; independently implemented Node 1,429 checks with full original-source SHA-256 and RUP-log replay. Non-hard small K4/cube controls are not expander-hardness certifications. Repository paths:

- `research/agents/lspv-2/2026-11-09_1216_LSPV2_CDCL_RUP_CONFLICT_MAY525.md`
- `experiments/arc/lspv2_525_cdcl_cost_may.py`
- `experiments/arc/lspv2_525_cdcl_independent_replay.mjs`
- `results/raw/arc/2026-11-09_1216_LSPV2_525_CDCL_SUMMARY.json`
- `results/raw/arc/2026-11-09_1216_LSPV2_525_CDCL_FULL_RAW.json.gz.b64`

## Five existing role interfaces

LSPV-1 Route B: audit which stronger authentic native rule invalidates the Resolution projection; retain [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN.

LSPV-2 Route A: seek paid GF(2) plus CDCL abstraction and a solver-intensional adaptive transformation; do not universalize the RUP-only impossibility.

LSPV-3 Route B: test source-authenticated native AND3/GF(2)/DEF/LOCAL-CONVERT transitions, assumption/discharge and source-fixed shared DAG provenance.

LSPV-4 Route A: audit all-phase conflict, propagation, retrieval, clause deletion/restarts, cache, reference and simultaneous peak space on a fixed model; no conflict-count-to-FLMV exponent inference.

LSPV-5 Route B: attack any hidden clause addition outside counted conflicts, alternate UNSAT terminal, and full-calculus shortcut. Recheck free interface weakening direction.

Affected evidence: [P2-L2-525]. Still OPEN: [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04]. Preserve all five existing identities, titles, hourly schedules, enabled states, Pacific time, 2 Route A / 3 Route B allocation and historical R_mix341 weights/grammar. P versus NP remains OPEN.
