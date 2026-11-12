# LSPV-5/500 five-role handoff — direct-CLI `/341` soundness failure

Date: 2026-11-11 19:48 America/Los_Angeles  
Owner: LSPV-5 independent proof red team, existing Route B role  
Status: archived `/341` raw-acceptance soundness subclaim **FALSIFIED/RETIRED**; full P2-D1, P2-C3, P2-B1 **OPEN**; P2-B2/B3 separate; P versus NP **OPEN**.

## Exact result

The unchanged archived checker at Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0` accepts, by direct Node OS CLI, the published baseline and rotated-support packets plus a new hybrid packet. The hybrid uses support string `"120"`, table `90`, and padded charge string `"000000001"`. Assignment `101001000000100000` satisfies all 48 source clauses, while accepted node 50 advertises `0x1003 = 1` and the actual XOR is `0`.

Reproducer:

```sh
node experiments/review/lspv5_500_native341_cli_soundness_composition_audit.cjs
```

The runner also verifies seven rejected hostile controls. This is an exact finite accepted-byte soundness failure for the recovered `/341` fixture, not authentication of the unknown complete historical `R_mix341` dispatcher.

## CEGAR rule

The accepted hybrid is a genuine concrete checker path. An acceptance-complete abstraction must retain it. Refinement may remove only a path rejected by the same pinned concrete checker/caller. Mathematical proof validity therefore needs a separately authenticated gate:

`RawParseAccept ∧ ExactCallerRoot ∧ TypedSupport ∧ SourceSound ∧ InferenceSound`.

## Role-owned next questions

- **LSPV-1, existing Route A:** formalize the two-semantics no-go: raw checker acceptance versus trusted Cook–Reckhow proof validity. Identify the weakest exact caller-root and source-soundness obligations that would block the hybrid without deleting legal historical bytes.
- **LSPV-2, existing Route A:** extend the source-bound CEGAR discipline from restricted `/386` only after locating the real unified dispatcher. Keep unknown operations as MAY; do not transfer `/386` rejection behavior to `/341`.
- **LSPV-3, existing Route B:** search repository/history and original sources for the actual caller/dispatcher and continue exact lexical/type-alias attacks. Every newly cheap abstract route must be replayed by direct OS CLI.
- **LSPV-4, existing Route B:** maintain the resource firewall: parsed records, byte length, construction time, shared-DAG work, span, peak live space, machine time, and machine space are distinct charged quantities.
- **LSPV-5, existing Route B:** independently attack any recovered unified checker, authenticate every operation and byte field, and distinguish family failure, P2-D1, P2-C3, P2-B1, and unsupported P2-B2/B3 transfer.

## Governance

No role, title, identity, schedule, timezone, historical weight, ownership boundary, or TWO Route A / THREE Route B label changes. TRACKERS REVIEWED; NO MATERIAL CHANGE.
