# ACCESS-SLOPE-SEPARATION5

**Timestamp:** 2026-10-19 10:48 KST  
**Status:** PROVED/EXACT in the declared record-probe and NAND2 models; COMPUTATIONAL audit passed; physical layout and unrestricted Circuit-SAT consequences OPEN. P versus NP OPEN.

## 1. Review and unresolved arrow

The latest GitHub state adds `WIRE-SWITCH-ACCOUNTING1`, its 63-row CSV baseline, and its machine-readable summary. The baseline correctly keeps five abstraction families separate: an exact NAND2 evaluator, REVFIX macro censuses, and three NAE/tetra syntax families whose transistor and physical-wire columns remain `NULL`. The prior synthesis `CANONICAL-WIRE-ERASURE4` gives a fixed-offset promise inverse for the localpin-plus-REVFIX compiler. `WIRE-REPLAY2` remains a source-backed exact finite solver audit, not a universal lower bound. No newer complete :00, :12, or :36 specialist report or machine-readable raw file was present at review time. The :24 task remains paused and was not activated.

The unresolved proof arrow is unchanged:

> a static device/net/wire census for one implementation does not imply a lower bound on arbitrary Circuit-SAT algorithms.

The immediate accounting gap was narrower: the baseline showed constant-size post-dedup hardware on a repeated-clause family, but it did not charge the source-independent work required to certify that deduplication is sound.

## 2. Integrations proposed before literature review

1. **Exact repetition recognizer.** Scan every fixed-width literal token, retain the first clause, and emit one clause only after all records match. Falsifier: an accepted one-token corruption or fewer than `3m` probes on the accepted canonical word.
2. **REVFIX template validator plus erasure.** Combine the fixed-offset inverse with a complete streaming template check. Falsifier: a malformed near-image that passes validation and projects to the wrong source.
3. **Fanout-two physical completion.** Add the baseline's abstract buffer trees before comparing switch slopes. Falsifier: a real cell library or layout in which the nominal four-MOS buffer proxy or the derived pin/net census is invalid.
4. **Amortized compiler cache.** Charge one exact formula scan and reuse the normalized evaluator for `q` assignments. Falsifier: any use case in which the formula changes between evaluations, or cache construction/output is omitted.

Only proposal 1 is promoted to a new exact theorem here. The others remain falsifiable candidates with explicit ledgers below.

## 3. Theorem: exact source-access slope survives static-size collapse

Let an input consist of `m >= 1` ordered clause records, each containing three tokens of fixed width `b >= 1`. Let `R_m` be the language in which all `m` records are identical.

### ACCESS-SLOPE-SEPARATION5

On every accepted canonical word `C^m`:

1. Every deterministic exact random-access verifier for `R_m` probes all `3m` token positions in the worst case.
2. A one-pass streaming transducer meets this bound, emits exactly three tokens, uses zero replay transfers, and needs at most

   `4b + ceil(log2(m+1)) + 3`

   simultaneously writable bits, excluding the read-only input.
3. For `F_m=(x0 OR x1 OR x2)^m`, the emitted single clause preserves both evaluation and satisfiability. Under the declared four-MOS NAND2 library, the raw evaluator has `8m-2` NAND2 gates and `32m-8` nominal MOS devices, while the normalized evaluator has six NAND2 gates and 24 nominal MOS devices.

Therefore the post-normalization static-device slope is zero, while exact source-token access has slope one.

### Proof

Suppose an exact verifier omits token position `j` on the accepted word `C^m`. Change only position `j` to a different fixed-width token. The verifier observes the same transcript but the new word is not in `R_m`, contradicting exactness. Thus all `3m` positions are essential.

For the matching upper bound, store the three tokens of the first record, compare each later token as it streams past, and emit the stored clause only after the final comparison succeeds. This uses exactly `3m` token reads, `3(m-1)` token comparisons, three token writes, and no replay. The stated live-bit bound stores the first clause, one current token, a clause counter, a two-bit slot counter, and one mismatch flag.

The Boolean identity `(C AND ... AND C)=C` proves the semantic projection. The NAND2 counts are the published baseline counts under the same declared library. This proves the separation between static implementation slope and compiler access slope. It is not a SAT decision lower bound.

## 4. Mandatory wire-by-wire ledgers

`P_in/P_out` count primitive gate input/output terminals. `E` counts logical driver-to-sink connections. `W` counts distinct driven logical nets. These are not transistor nets or CNF literal incidences.

| Model | Primitive library and semantics | Encoded source / output | G; P_in/P_out; E; W | Fanout / buffers | Access, transfers, live state | Depth / layout / output charge | Status |
|---|---|---|---|---|---|---|---|
| Exact repetition recognizer + normalized evaluator | One-pass token transducer; NAND2=4 nominal MOS; fixed-assignment evaluation | `3bm` bits / `3b` bits | evaluator `G=6`; `12/6`; `E=13`; `W=9` | max load 2; `B=0` | `3m` token reads; 0 replay; live `<=4b+ceil(log2(m+1))+3` | evaluator depth 4; transducer `3m` reads; placement, routed length, capacitance and transistor nets `NULL`; output 3 token writes | PROVED/EXACT |
| Complete canonical composite validator + erasure | Ordered localpin-plus-cyclic-REVFIX grammar; declared NAND2 mapping | target has `2916m` literal records plus `972m` boundaries; output `3m` literals plus `m` boundaries | normalized functional `G=144m`, functional `E=288m`, functional `W=n+166m`; declared NAND2 `G=360m`, `P_in/P_out=720m/360m`; NAND-net count `NULL` | `B=NULL`; complement rails assumed unless inverters are charged | full pass `2916m` literal + `972m` boundary reads; replay 0 only for ordered stream; live `3w+ceil(log2(972m+1))+ceil(log2(m+1))+12` | NAND depth <=14; all physical layout quantities `NULL`; output `3m` literal + `m` boundary writes | Prior exact promise inverse; full arbitrary-input validator OPEN |
| Fanout-two repeated evaluator | NAND2 plus abstract one-input four-MOS buffer; fixed-assignment evaluation | `3bm` formula bits; netlist serialization bits `NULL` | `G_cells=14m-8`; `P_in=22m-10`; `P_out=14m-8`; `E=22m-9`; `W=14m-5` | max load 2; `B=6m-6` | exact family recognition requires `3m` token reads; netlist-emission transfers and live state `NULL` | depth upper bound `2m+1+ceil(log2(2m))`; placement/routing `NULL`; output serialization `NULL` | CANDIDATE physical completion |
| Amortized normalized evaluation over `q` assignments | Exact repetition recognizer plus six-NAND evaluator | `3bm+3q` input bits / `q` answer bits | static `G=6`; `12/6`; `E=13`; `W=9` | max load 2; `B=0` | formula reads `3m` once; assignment reads `3q`; answer writes `q`; replay 0; live bound adds three assignment bits | depth 4 per evaluation; end-to-end sequential work is a separate machine metric; all physical layout quantities `NULL` | CONDITIONAL on same-formula reuse |

The raw repeated evaluator has `G=8m-2`, `P_in/P_out=16m-4 / 8m-2`, `E=16m-3`, `W=8m+1`, maximum fanout `2m`, depth `2m+2`, and `14m-2` logical NAND-output toggles under the declared three-bit Gray trace. With the abstract fanout-two buffers, gate/buffer output toggles become `28m-16`; these are logical transitions, not measured energy.

## 5. Seven-scale trend

All static counts below use the same four-MOS NAND2/buffer proxy and the same repeated-clause evaluation semantics. Source reads remain a separate machine metric.

| m | Raw nominal MOS | Buffered nominal MOS | Dedup nominal MOS | Exact token reads | Live-bit upper bound |
|---:|---:|---:|---:|---:|---:|
| 2 | 56 | 80 | 24 | 6 | 17 |
| 4 | 120 | 192 | 24 | 12 | 18 |
| 8 | 248 | 416 | 24 | 24 | 19 |
| 16 | 504 | 864 | 24 | 48 | 20 |
| 32 | 1,016 | 1,760 | 24 | 96 | 21 |
| 64 | 2,040 | 3,552 | 24 | 192 | 22 |
| 128 | 4,088 | 7,136 | 24 | 384 | 23 |

OLS log-log slopes over these seven scales are approximately 1.028 raw MOS, 1.069 buffer-completed MOS, 0 deduplicated MOS, 1 exact token reads, and 0.073 live bits. The strongest pattern is the split between static-size slope zero and mandatory access slope one after exact normalization.

**Falsifier:** an exact verifier that accepts the canonical repeated stream, rejects every one-token corruption, and uses fewer than `3m` worst-case token probes. The theorem rules this out in the stated random-access token model. Randomized error, authenticated/checksummed inputs, or a different representation are different models and must be relabeled.

## 6. Computational audit

The Python audit checked seven published formula rows, all 56 Boolean assignment/scale equivalences, and all 762 one-token corruptions across `m=2,4,8,16,32,64,128`. It found zero unexpected failures. The experiment replays the finite controls; the probe lower bound itself is proved above.

## 7. Literature reconciliation after proposal construction

- Eén and Biere show that variable/clause elimination and subsumption can shrink SAT instances in preprocessing. This supports treating normalization as a charged algorithmic stage; it does not turn the resulting small circuit into a lower bound.
- Thompson's VLSI area-time framework requires an actual layout/communication model. Because placement, routed length, capacitance, and transistor nets are `NULL` here, no Thompson-style area-time conclusion is available.
- Fortnow, Lipton, van Melkebeek, and Viglas prove SAT time-space lower bounds in specified machine models. A token-probe lower bound for a recognizer does not transfer to unrestricted SAT computation.
- Williams's Circuit-SAT self-improvement results require algorithmic hypotheses for stated circuit families. Nominal device counts or compiler syntax alone do not meet those hypotheses.

## 8. Proof DAG

| Arrow | Status |
|---|---|
| Repeated-clause stream -> exact equality recognition | PROVED/EXACT |
| Exact equality recognition -> one-clause projection | PROVED/EXACT |
| One-clause projection -> constant declared NAND2 evaluator | PROVED/EXACT |
| `3m` token-probe lower bound on accepted canonical word | PROVED/EXACT |
| Published seven-scale formulas and finite controls | COMPUTATIONAL, zero failures |
| Full arbitrary-input REVFIX canonical-image validation | OPEN |
| Fanout proxy -> transistor-level routed implementation | OPEN |
| Static switch/net slope -> Thompson area-time lower bound | OPEN; missing layout and communication hypotheses |
| Restricted physical/stream model -> arbitrary Circuit-SAT machine lower bound | OPEN |
| Raw gadget inflation implies SAT hardness | FALSIFIED/RETIRED |
| P versus NP | OPEN |

Older tetrahedral/PC results remain model-specific benchmarks. NAE clause counts, NAE ports, tetrahedral edge incidences, PC degree, and finite fold counts are not inserted into MOS/net columns.

## 9. Role handoff

- **Physical Models (:00):** replace the abstract four-MOS buffer proxy by one named standard-cell library; report transistor-device count, transistor nets, placed area, routed length, maximum load, and post-layout depth on `m=64,128`.
- **Quotient (:12):** prove or falsify a token-probe lower bound for complete canonical-image recognition of the localpin-plus-REVFIX grammar, including one-record near-image mutations.
- **Experiments (:24):** remains paused; no schedule or task was activated.
- **Red Team (:36):** attack `E_buffered=22m-9` and `W_buffered=14m-5` under explicit buffer-tree construction, complement-rail removal, and primary-output loading.
- **Synthesis (:48):** ingest only timestamped machine-readable records, preserve `NULL`, and compare slopes only within the same library, semantics, and machine model.

Root `main.tex` was not modified. Its current body still contains a literal truncation placeholder, so a markerless overwrite would be unsafe.

## Primary sources

1. N. Eén and A. Biere, *Effective Preprocessing in SAT Through Variable and Clause Elimination*, SAT 2005. https://www.cs.toronto.edu/~fbacchus/csc2512/Readings/EenBiere-SAT05.pdf
2. C. D. Thompson, *Area-Time Complexity for VLSI*, STOC 1979. https://doi.org/10.1145/800135.804401
3. L. Fortnow, R. Lipton, D. van Melkebeek, and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005. https://lance.fortnow.com/papers/files/tst.pdf
4. R. Williams, *Self-Improvement for Circuit-Analysis Problems*, STOC 2024. https://dspace.mit.edu/entities/publication/22d21e42-9505-4a6e-88df-977013805dd2

<!-- FINAL_VERIFICATION_SENTINEL::ACCESS-SLOPE-SEPARATION5::P_VS_NP_OPEN -->
