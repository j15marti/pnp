# LSPV-5/496 five-role handoff — exact-source join firewall

**Date:** 2026-11-11 14:48 America/Los_Angeles  
**Status:** P2-D1 naive cross-checker join FALSIFIED; restricted exact-source interface repair validated; P2-C3/P2-B1 OPEN; P2-B2/B3 unsupported; P versus NP OPEN.

## Reproducer

Run:

```bash
node experiments/review/lspv5_496_dual_checker_source_firewall_audit.js
```

Expected scope and output:

- completes in under 30 seconds (observed under 14 seconds);
- reruns LSPV-1/581 unchanged: 12/12 decisions, accepted work 67;
- reruns LSPV-2/565 unchanged: 5 accept, 5 reject, 17,878 assertions;
- reruns LSPV-3/578 unchanged: 10/10 dual-checker decisions;
- reruns LSPV-4/551 unchanged: byte-first `(1925,157)`, slot-first `(156,1930)`, 1,129,302 states each, three original /386 checker replays;
- exhaustively checks all 262,144 edge assignments for the /386 source.

Raw evidence:
`results/raw/arc/2026-11-11_1448_LSPV5_496_DUAL_CHECKER_SOURCE_FIREWALL_RAW.json`.

## Finding

The exact 14,032-byte packet at Git blob
`1c3b400857ab2cfb7d78f37b2723945e6521a83a` is accepted by both archived
checkers. The /341 namespace binds a SAT 48-clause source (explicit assignment
`101001000000100000`); the /386 namespace binds a different UNSAT 49-record
source (zero models by exhaustive enumeration). Two acceptances are not one
source-authenticated mixed derivation.

## Repaired interface rule

A join may be considered only when every component checker verifies the same
externally supplied **full canonical source bytes**, including a schema/calculus
tag. SHA-256 values are telemetry only and carry no proof authority. The hostile
packet fails exact source equality. Keep each component acceptance; refine away
only the cross-source join.

## Role assignments (preserve existing identities and Route labels)

- **LSPV-1:** search for an accepted cheaper owner/weakening macro only after
  exact external-source binding; a genuine shortcut remains publishable.
- **LSPV-2:** extend the source-bound reference semantics from /386 SOURCE/DEF/RES
  to the next authenticated native opcode, with concrete-step inclusion.
- **LSPV-3:** mutate namespace ownership and source fields to find any packet that
  passes a proposed common-source join; do not combine sibling costs.
- **LSPV-4:** charge bytes/slots only inside a single source-authenticated proof
  DAG; fixed-DAG optimization is not global proof optimization.
- **LSPV-5:** require one checker and exact common source before reconciling
  P2-D1 -> P2-C3 -> P2-B1; keep P2-B2/B3 separate.

## Blockers

Historical `R_mix341` checker/grammar remains unauthenticated. No full shared-DAG
semantics or cost-sound abstraction exists. Issue #3 comment readback returned
`Transport closed`. LSPV-4/551 report/handoff/root reconciliation was absent at
preflight despite published code and packets; recovery request comment
`6809010398` was posted.

TRACKERS REVIEWED; NO MATERIAL CHANGE.

