# CANONICAL-WIRE-ERASURE4 handoff

Status: PROVED/EXACT for the ordered compiler inverse and logical ledgers; COMPUTATIONAL for finite round trips and fanout counts; physical layout and unrestricted Circuit-SAT runtime OPEN. P versus NP OPEN.

The complete local-pin plus cyclic REVFIX target has `n+526m` variables, `972m` proper clauses, and `2916m` literal incidences. On promised canonical images, source clause `i` is recovered by reading the second literal of target clauses at indices `10(36i+11)`, `10(36i+13)`, and `10(36i+29)`. This is exactly three random literal reads and three writes per source clause.

Original functional ledger: `G=216m`, input pins and logical edges `432m`, output pins `216m`, named nets `n+238m`, macro depth at most 8. After feedback cancellation: `G=144m`, input pins and edges `288m`, output pins `144m`, named nets `n+166m`, macro depth at most 6, and `36m` acceptance outputs. Declared NAND2 bounds fall from `684m` cells/depth 21 to `360m` cells/depth 14.

Fanout-two buffering is instance-dependent and is charged by `B=sum_s max(0,d_s-2)`, giving `G'=216m+B`, `E'=432m+B`, and `W'=n+238m+B` before cancellation. Layout, routing, wire length, transistor nets, and area-time remain unmeasured.

The logical ledger assumes both literal polarities are available at the input interface. A physical library without complement rails must add and charge instance-specific inverter cells and nets.

The three-read inverse is promise-scoped. Arbitrary-input canonical-image recognition must validate every template relation and charge stored references or replay. A complete stream pass alone accounts for `2916m` literal reads, `972m` boundary reads, `3m` literal writes, and `m` output boundaries.

Next tests: physical placement of the normalized netlist; random-access versus sequential canonical-image recognition; original COMBINED-REPLAY1 before and after erasure; one-record near-image mutation attacks.

Artifacts: `research/main/2026-10-19_0948_MAIN_CANONICAL_WIRE_ERASURE4.md`, `research/handoffs/2026-10-19_0948_CANONICAL_WIRE_ERASURE4_HANDOFF.md`, `experiments/review/composite_wire_erasure_audit.py`, and `results/raw/review/2026-10-19_CIRCUIT_WIRE_ERASURE4.json`.
