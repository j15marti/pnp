# BIT-LEDGER-CEILING120 — Role-5 coverage and rejection handoff

Marker: `LSPV-5::BIT-LEDGER-CEILING120::2026-10-24T15:48:00+09:00`

## Exact new result

- **PROVED/EXACT in the declared complete-state model:** if `Phi:{0,1}^B -> R` is globally `L`-Lipschitz in Hamming distance, then `osc(Phi) <= L B`. Therefore endpoint gap divided by per-one-bit-step potential change certifies at most `B` steps. This is a ceiling on that proof template, not an upper bound on computation time.
- **PROVED/EXACT bookkeeping:** with elementary state-bit events, complete-state flips `Delta <= charged state writes <= primitive work`; unchanged writes count as work but not flips. With `B_i` live bits, `S=max_i B_i` and `BT=sum_i B_i`, `S <= BT <= (U+1)S`.
- **COMPUTATIONAL:** 13,979,869 assertions passed. Code SHA-256 `d2050a17c0a932537e481c1bafc5c5ed3ab84e29d676b3640e314bac328a4706`; raw SHA-256 `afe3fa523bb34cb3d252a7cd212003d93c39512716bce48d87c2e38b89338b9d`.

## Gap-to-evidence ledger

| Proposed link | Source/result | Receiving obligation | Verdict and mismatch |
|---|---|---|---|
| Online schedule implies a simultaneous pair | `RESOURCE-SCHEDULE-BRIDGE` | Uniform all-input SAT successor in matched FLMV model | **PARTIAL/RESTRICTED.** Simulation is valid under explicit online-generator contract; it does not construct the schedule or prove SAT correctness. |
| Four Gray sign patches imply total write/flip exponent `1/2` | `QUIESCENT-CHILD-REUSE` | Total machine write/flip and space improvement | **FALSIFIED/RETIRED** in unrestricted form. Four counts only target sign fields. Controller, addressing, parent, solver, cache, and initialization remain charged. Reuse survives as a scoped optimization. |
| Adaptive hitting number forces post-acquisition work | `ADAPTIVE-COVER75` | Unavoidable favorable ARC edge or superlinear work | **PARTIAL/RESTRICTED.** It proves source acquisition only, `tau <= N`; residual values cannot be summed. |
| Global complete-state potential forces long work | This report | Unavoidable post-acquisition computation | **FALSIFIED/RETIRED** without added legal-transition structure: global range is at most `L B`. |
| Active-gate circuit energy transfers to temporal flips | arXiv:1808.07199v2 | Uniform SAT time/flip lower bound | **FALSIFIED/RETIRED.** Energy counts gates outputting one; every Boolean function has linear energy if exponential circuit size is allowed. Representation size must be charged separately. |

## Adaptive-state/resource ledger

- Before: read-only CNF, current representation, partial assignment, learned constraints/cache, available scope metadata, budget. Parameters are acquired by charged scans or supplied event streams; no label oracle.
- Rule: where the scoped contract holds, reuse a quiescent child and Gray-patch FORCE fields. Alternatives considered and charged: rebuild, SCC/Horn/affine direct solve, decomposition, source reread, representation switch, decide-first shortcut.
- After: child result, common-boundary DP/cache, updated budget and representation. SAT may stop on one verified witness/decision; UNSAT requires exact combination of the necessary scoped states, not a prescribed proof object.
- Charges: parameter discovery, source/work reads, unchanged and changed writes, controller/address transitions, headers, child materialization, patches, solver calls, cache/DP, reconstruction, live ancestors, buffers, and peak writable bits.
- Scope: restricted policy only; not coverage of every adaptive SAT decider.

## Hostile controls retained

- Streaming parity chain: all-zero SAT and single-one UNSAT controls require the same source acquisition, while accumulator flips are `0` versus `1`. Address/control flips still count in complete state.
- Affine/XOR, Horn, SCC/2-SAT, padded, connected/disconnected, source-readable, cache reuse, representation switching, and decide-first families remain mandatory controls.
- Optional delay or rereading can add work without useful flips, but an arbitrary decider may omit it; it cannot establish unavoidable work.

## Corpus coverage update

- Cumulative pinned snapshot `55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640`: 3,532 prose/source/config files retrieved, hash-verified, and keyword searched; manual mathematical review remains selective.
- Full-text this run: new Role-5 `RESOURCE-SCHEDULE-BRIDGE`, `QUIESCENT-CHILD-REUSE`, reuse audit code/results; latest substantive Role-1/2/3/4 outputs; BIT-RESOURCE1 steering.
- Duplicates/corrections preserved: thirteen historical executable sources still contain retired `2*cos(pi/7)` landing logic; do not reuse their endpoint test. ICLB-006/007/008 and 27E are checker-local/fixed-template only.
- Failed/unavailable: original HEREDITARY-SCOPED10 executable remains missing; continuity summaries do not fill that evidence gap.

## Exact open implication and next artifact

**OPEN:** prove a uniform all-input exact SAT successor, or a cofinal finite charged route, whose total bit-operation time and read-only-input peak work space enter a verified FLMV-forbidden region. The next useful artifact is the original HEREDITARY-SCOPED10 generator. If recovered, instrument every source/work read, unchanged/changed write, complete-state flip, controller selection, child/header bit, cache operation, solver call, live bit, cumulative bit-time, and representation size. If not recovered, retire that branch as unsupported.

P versus NP remains **OPEN**.
