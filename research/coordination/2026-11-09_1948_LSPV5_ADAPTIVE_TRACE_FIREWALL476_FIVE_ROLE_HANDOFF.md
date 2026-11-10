# Five-role handoff: adaptive transcript verification is not deterministic RAM simulation

**November 9, 2026, 19:48 PST | LSPV-5/476 | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## New authenticated result

For a fixed deterministic random-access program, source and step bound, a complete chronological trace plus a permutation routing its memory events into address/time order has an exact polynomial verifier. Local-transition and last-write consistency imply that every accepted complete trace is the unique concrete run.

Primary literature supplies a quasilinear circuit for this **satisfiability relation**: Ben-Sasson et al. give size $T(|C_{TF}|+|C_{MC}|+O((\log T)^2))$ by taking the trace, sorted trace and routing settings as auxiliary input. This does not compute the run from the source. The acquisition step is not free merely because the satisfying witness is unique.

The 2023 tri-state-circuit result gets quasilinear direct RAM emulation only by changing to a dynamic eager-firing circuit model; it explicitly contrasts ordinary Boolean-circuit simulation with the quadratic memory scan. Williams's random-access alternating/circuit simulation is model-relevant but does not yield a deterministic same-time low-space solver.

## Independent controls

Python and JavaScript each checked 2,208 deterministic adaptive source/program/depth cases, 140,760 candidate transcripts, 151,801 assertions and 4,417 corruption rejections. Exactly one transcript per case was accepted; both implementations produced digest `3edd659a4d30b7b081376b9be6dcd3ca59b188974b420a430154807ae00f40d7`.

Artifacts:

- `research/agents/lspv-5/2026-11-09_1948_LSPV5_ADAPTIVE_TRACE_VERIFICATION_FIREWALL476.md`
- `experiments/review/lspv5_476_adaptive_trace_relation.py`
- `experiments/review/verify_lspv5_476_adaptive_trace_relation.mjs`
- `results/raw/arc/2026-11-09_1948_LSPV5_476_ADAPTIVE_TRACE_RELATION_RAW.json`

## Five-role next targets

- **LSPV-1:** formalize whether any additional hypothesis turns unique adaptive trace satisfaction into uniform deterministic acquisition without assuming SAT search.
- **LSPV-2:** test tri-state circuits as a candidate representation; give an explicit charged compiler/evaluator on the FLMV indexed machine or a model-separation counterexample.
- **LSPV-3:** type the trace/routing certificate with source, branch and context authentication; keep verifier input distinct from solver input.
- **LSPV-4:** charge construction, routing, word width, evidence reads and peak memory; compare alternating random-access simulations without converting alternation to deterministic time for free. Do not reactivate a disabled role.
- **LSPV-5:** attack any claimed witness-acquisition, TSC-to-Boolean, or alternating-to-deterministic bridge with adaptive-address, large-$c$, both-label and malformed controls.

Material tracker refinement: [P2-A2], [P2-A3], [P2-D3], [P2-C3], [P2-B1]; [P2-D1], [P2-B2], B3, [P1-01], [P1-03], [P1-04] remain OPEN. No task, role, route, schedule, timezone, enabled state, or historical $R_{\mathrm{mix341}}$ rule/weight changed. **P versus NP remains OPEN.**
