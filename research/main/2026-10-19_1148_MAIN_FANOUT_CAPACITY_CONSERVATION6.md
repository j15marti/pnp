# FANOUT-CAPACITY-CONSERVATION6

**Timestamp:** 2026-10-19 11:48 KST  
**Status:** PROVED/EXACT in the declared rooted buffer-forest model; COMPUTATIONAL audit passed; SIGNCUBE specialization is source-backed and algebraically checked; placement, routing, device-level minima, unrestricted Circuit-SAT consequences and P versus NP remain OPEN.

## 1. Review of new and historical evidence

The new original specialist artifact is `results/raw/physical/2026-10-19_SIGNCUBE_ERASURE6_LEDGER.json`, timestamped 10:59 KST. It contains six raw and normalized ledger rows (`d=1..6`), labels 1,332 formula/circuit-equivalence checks and 2,532 guard/mutation controls with zero unexpected failures, and preserves `NULL` for physical wirelength, placed area, transistor nets and measured energy. No matching full proof report or generator was found in the repository at review time, so source-asserted theorem labels are not upgraded merely from the JSON status field.

The current accounting baseline and machine-readable summary were reread. `WIRE_LEDGER1` remains an implementation upper-bound census: two-shear REVFIX has `19m` NAND2 equivalents (`76m` nominal MOS) before feedback cancellation and `10m` (`40m` nominal MOS) after cancellation, while output tests, polarity, fanout, buffers and routing remain uncharged. `WIRE-REPLAY2` remains a finite audit of one source-backed solver, not an arbitrary-machine lower bound. `RECOVERY-STRENGTHEN7` and `STREAMCOMP1` retain conditional recursive accounting but still lack a uniform hereditary all-input shrinker. PRIME-LQP's semantic-quotient obstruction remains retired as a hardness mechanism. Older tetrahedral/NAE and Polynomial Calculus results remain syntax/proof-system benchmarks; their clause, port, tetra-edge and degree counts are not hardware nets or machine time.

Root `main.tex` still contains a literal truncation placeholder. It was not modified.

The unresolved arrow is unchanged:

> exact cells, pins, logical nets, source accesses or buffer counts for one declared realization do not imply a lower bound for arbitrary Circuit-SAT algorithms.

## 2. Integrations proposed before literature review

1. **Exact `k`-load fanout completion.** Given the fanout vector of a Boolean netlist and a one-input buffer whose output drives at most `k` sink terminals, calculate the exact minimum number of tree buffers and all pin/edge/net deltas. Falsifier: a legal rooted buffer forest serving `d` sinks with fewer cells than the proposed formula.
2. **Charged SIGNCUBE erasure recognizer.** Charge canonical source probes, semantic-certificate probes, tape crossings, replay and live bits before replacing a raw signed-cube evaluator by its source-asserted one-net normalized core. Falsifier: one accepted near-image mutation or a truth-table mismatch between source and normalized output.
3. **Balanced depth completion.** In addition to cell count, expose the least possible buffer-layer height under a `k`-load cap. Falsifier: a legal forest with fewer than `ceil(log_k d)-1` buffer layers, or a named physical library whose sizing/drive rules invalidate the abstract primitive.
4. **Same-library buffer-share trend.** Compare `B/G`, nominal core MOS and buffer-completed MOS only within the same SIGNCUBE library, semantics and source family. Falsifier: a library/semantics/implementation change in any compared row, or an independently generated row that violates the declared count identities.

Only proposal 1 is promoted to a new theorem. Proposal 3 follows as a model-local depth corollary. Proposals 2 and 4 remain source-backed tests.

## 3. Theorem: exact fanout-capacity conservation

Fix `k >= 2`. One source driver and every inserted one-input buffer may each drive at most `k` sink terminals. A signal must reach `d >= 1` terminal loads through a rooted forest that is a tree for that signal. Buffers do not compute or invert the signal.

### Theorem

The minimum number of buffers is

`B_k(d) = max(0, ceil((d-k)/(k-1)))`.

If a netlist has driver fanouts `f_1,...,f_W`, then its minimum tree-buffer count is

`B = sum_i B_k(f_i)`.

Adding these buffers changes the declared logical ledger exactly as follows:

- `G' = G + B` cells,
- `P_in' = P_in + B`,
- `P_out' = P_out + B`,
- `E' = E + B` driver-to-sink edges,
- `W' = W + B` distinct driven nets,
- nominal static devices increase by `c_B B` when the declared buffer cell costs `c_B` devices.

For one signal with fanout `d`, the least possible maximum number of buffer layers is `max(0,ceil(log_k d)-1)`.

### Proof

With `B` buffers, the source plus buffers provide at most `k(B+1)` outgoing load slots. The `d` terminals and the `B` buffer inputs consume `d+B` slots. Necessarily

`k(B+1) >= d+B`,

so `(k-1)B >= d-k` and the stated lower bound follows.

For sufficiency, begin with the source's `k` available slots. Replacing any available terminal slot by one buffer consumes one slot and creates `k` new slots, increasing terminal capacity by `k-1`. After exactly `B_k(d)` replacements there are at least `d` slots; attach the `d` terminal loads and leave any surplus slots unused. This constructs a legal tree and meets the lower bound.

Each inserted buffer contributes one cell, one input terminal, one output terminal, one new buffer-input edge and one driven output net. Original sink edges remain, proving the ledger deltas. A depth-`h` tree reaches at most `k^(h+1)` terminals when the source is level zero, yielding `h >= ceil(log_k d)-1`; a balanced construction attains it.

This theorem is exact only in the stated abstract fanout model. It is not a physical placement, wire-capacitance or delay theorem.

## 4. SIGNCUBE specialization and challenge

For the six published rows,

`n = 2^d + 1`, `m = d 2^(d+1)`.

The raw mixed-library evaluator satisfies:

- `G = 3m+n-2`,
- `P_in = 6m+n-3`, `P_out = 3m+n-2`,
- `E = 6m+n-2`,
- `W = 3m+2n-2`,
- `B_2 = 3m-3n+1`,
- `MOS_core = 18m+2n-8`,
- `MOS_buffered = 30m-10n-4` under `BUF2=4 MOS`.

The published abstract buffer total is consistent with `3m-1` fanout-one internal OR/AND-tree nets and `2n-1` remaining connected nets of fanout at least two:

`B_2 = E-(3m-1)-2(2n-1) = 3m-3n+1`.

The full fanout histogram and generator are absent from the new commit, so this structural specialization is recorded as source-backed/algebraically checked rather than independently reconstructed from a netlist file. The general theorem above does not depend on that missing artifact.

At `d=6, n=65, m=768`, the raw evaluator has `G=2367`, `P_in/P_out=4670/2367`, `E=4671`, `W=2432`, maximum fanout `768`, `B_2=2110`, core proxy `13,946 MOS`, and buffer-completed proxy `22,386 MOS`. The normalized core has `G=0`, `P_in/P_out=0/0`, `E=W=1`, no internal gate-output toggles and zero internal core MOS. Its output-driver MOS is `NULL`, not zero.

**Challenge.** The normalized result is an extensional circuit representation, while canonical recognition and source traversal are separate machine computations. The specialist reports `3m` canonical token probes, additional certificate probes, one-way tape crossings and finite live-bit bounds. These charges prevent the zero-gate normalized core from being misreported as zero end-to-end work. Conversely, the raw gate/buffer growth is redundant implementation growth and cannot be promoted to a SAT lower bound.

## 5. Mandatory wire-by-wire ledgers for the four proposals

`P_in/P_out` are primitive terminal incidences, `E` is driver-to-sink connectivity, and `W` is the count of distinct driven logic nets. CNF occurrences, transistor nets and abstract RAM accesses remain separate categories.

| Proposed model | Primitive library and semantics | `G; P_in/P_out; E; W` | Fanout / buffers | Source accesses, replay, live bits | Depth and physical assumptions | Charged discovery and output | Status / falsifier |
|---|---|---|---|---|---|---|---|
| Exact `k`-load completion | Existing netlist plus 1-input non-inverting buffer, capacity `k`, device proxy `c_B` | `G+B; (P_in+B)/(P_out+B); E+B; W+B` | `B=sum B_k(f_i)` | Given fanout vector: no source-machine claim; input decoding and live bits `NULL` until encoding is fixed | added buffer layers per signal `ceil(log_k f_i)-1`; placement, routing, capacitance, transistor nets `NULL` | read/validate fanout vector is charged but representation-dependent; output adds `B` cell and `B` edge/net records | PROVED/EXACT abstract model; falsified by smaller legal forest |
| Charged SIGNCUBE erasure | INV=2, OR2=6, AND2=6, BUF2=4 MOS proxy; source-asserted extensional normalization | raw formulas above; normalized `0;0/0;1;1` | raw `F_max=m`, `B_2=3m-3n+1`; normalized `B=0` | token probes `3m`; certificate probes `12,24,56,136,328,776`; replay 0; live `28..60` bits | raw depth `3+ceil(log2 m)`; normalized core depth 0; all routed quantities `NULL` | tape cells crossed `48..19220`; output serialization `NULL`; normalized output driver `NULL` | Candidate composite; falsifier is near-image acceptance or semantic mismatch |
| Balanced buffer depth | Same abstract `k`-load buffer forest | same count deltas as theorem | exact count plus balanced tree | source encoding/live construction state `NULL`; no replay claim | extra layers `max(0,ceil(log_k d)-1)`; real delay `NULL` | emits `B` cells and `B` added connections/nets | PROVED/EXACT depth in abstract tree; physical timing OPEN |
| Same-library buffer-share series | Analysis of six fixed SIGNCUBE rows, no new circuit | consumes recorded raw/normalized ledgers | `B/G` compared only within same library | six row reads; replay 0 in a one-pass analysis; live bits `NULL` for unspecified implementation | no placement or routing inference | chart-ready JSON records all rows and slopes; no netlist emitted | COMPUTATIONAL; invalid across any library/semantics/model change |

Functional logic wires, CNF literal incidences, transistor nets and RAM/source accesses are never substituted for one another. Unknown physical fields remain `NULL`.

## 6. Compact six-scale trend

All rows use the same mixed primitive library, raw evaluator semantics and abstract fanout-two completion. Slopes are OLS log-log slopes against `m` across these six rows.

| `d` | `m` | Raw `G` | Raw `W` | Core MOS | BUF2 | Buffered MOS | Token probes | Normalized nets |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 13 | 16 | 70 | 4 | 86 | 12 | 1 |
| 2 | 16 | 51 | 56 | 290 | 34 | 426 | 48 | 1 |
| 3 | 48 | 151 | 160 | 874 | 118 | 1,346 | 144 | 1 |
| 4 | 128 | 399 | 416 | 2,330 | 334 | 3,666 | 384 | 1 |
| 5 | 320 | 991 | 1,024 | 5,818 | 862 | 9,266 | 960 | 1 |
| 6 | 768 | 2,367 | 2,432 | 13,946 | 2,110 | 22,386 | 2,304 | 1 |

Slopes: raw `G` 0.990, raw `W` 0.958, core MOS 1.006, buffer-completed MOS 1.052, canonical token probes 1.000, normalized connected nets 0.000.

**Strongest new pattern.** Exact fanout completion steepens this raw implementation's nominal MOS slope, while extensional normalization leaves one connected net. Canonical source access still scales linearly. The three slopes describe different resources and do not combine into a universal lower bound.

**Pattern falsifier.** Under the identical library, Boolean semantics, raw generator and access model, an independently generated row that violates the formulas or a truth-table mismatch falsifies the series. A placed/routed library result with growing output-load, wire or energy cost would not falsify the abstract ledger; it would fill currently `NULL` physical columns and could eliminate the apparent zero physical slope.

Chart-ready data are in `results/raw/review/2026-10-19_1148_WIRE_SWITCH_TREND6.json`.

## 7. Computational audit

`fanout_capacity_audit.py` exhaustively compared the closed form against direct capacity enumeration for all `k=2..8` and `d=1..256`: 1,792 checks, zero failures. It then reconstructed the six published SIGNCUBE buffer, core-MOS and buffered-MOS totals: six checks, zero failures. The script does not simulate physical routing.

## 8. Literature reconciliation after proposals

- Thompson's VLSI area-time framework is layout and communication/bisection sensitive. With placement, routed length and physical area still `NULL`, this work has no Thompson-style endpoint.
- Fortnow, Lipton, van Melkebeek and Viglas prove SAT time-space lower bounds for specified machine computations. A static fanout-cell theorem does not instantiate their hypotheses.
- Williams's Circuit-SAT self-improvement starts from an algorithmic running-time hypothesis for circuit analysis. A nominal transistor proxy is not such an algorithm.
- Branching-program and recursive-shrinker comparisons require an explicit program/state transition system and charged input access. Neither a raw circuit census nor a normalized one-net core supplies that object.

Primary sources:

1. C. D. Thompson, *Area-Time Complexity for VLSI*, STOC 1979. https://doi.org/10.1145/800135.804401
2. L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005. https://doi.org/10.1145/1101821.1101822
3. R. Williams, *Self-Improvement for Circuit-Analysis Problems*, STOC 2024 / ECCC TR23-082. https://eccc.weizmann.ac.il/report/2023/082/

## 9. Proof DAG

| Arrow | Status |
|---|---|
| Fanout vector + abstract `k`-load buffers -> exact minimum buffer count | PROVED/EXACT |
| Buffer count -> exact cell/pin/edge/net deltas | PROVED/EXACT |
| Fanout cap -> minimum balanced buffer-layer height | PROVED/EXACT in abstract tree model |
| Published SIGNCUBE rows -> six count identities | COMPUTATIONAL, zero failures |
| SIGNCUBE raw circuit -> normalized one-net core | SOURCE-ASSERTED PROVED; finite checks published; full proof/generator absent from commit |
| Canonical source -> charged probes/tape/live-state ledger | COMPUTATIONAL/source-backed |
| Abstract BUF2 -> named transistor cell with load/sizing constraints | OPEN |
| Logic nets -> routed wirelength/area/transistor nets/energy | OPEN |
| Static implementation slope -> branching-program or RAM SAT lower bound | OPEN / invalid without model transfer |
| Conditional recursive shrinker -> unrestricted SAT endpoint | OPEN; hereditary all-input arrow missing |
| Raw redundant-gadget inflation -> SAT hardness | FALSIFIED/RETIRED |
| P versus NP | OPEN |

## 10. Role handoff

- **Physical models (:00):** for SIGNCUBE `d=5,6`, use one named standard-cell library and report cell types, drive strengths, transistor-device count, transistor nets, output load, placed area, routed length, clock assumptions if any, and post-route delay. Preserve the logical and physical ledgers separately.
- **Quotient (:12):** publish the missing full SIGNCUBE normalization proof/generator and a complete canonical-image recognizer; mutate every record class once and report source reads, certificate reads, replay, output serialization and live RAM.
- **Experiments (:24):** remains paused. No task or schedule was activated.
- **Red team (:36):** reconstruct the complete fanout histogram for all six rows and attack the assumptions `3m-1` singleton nets, all remaining connected nets having fanout at least two, and `B_2=3m-3n+1`; separately attack the zero-output-driver interpretation.
- **Synthesis (:48):** accept only timestamped machine-readable rows, preserve `NULL`, and compare trends only under the same primitive library, semantics and machine model.

Artifacts were published with checked readback. The shared tracker now contains 82 model records plus a 12-row detailed SIGNCUBE ledger. Root `main.tex` was left untouched.

<!-- FINAL_VERIFICATION_SENTINEL::FANOUT-CAPACITY-CONSERVATION6::P_VS_NP_OPEN -->
