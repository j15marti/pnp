# MAIN GAUSSIAN-NONLINEAR-GUARD9 | 2026-10-19 14:48 KST

**Status:** one exact mixed XOR/nonlinear counterexample, one exact source-recognition lemma, and a same-library circuit census are proved; the newest specialist macro record remains conditional because its full generator, partition and trace are absent. Physical layout and arbitrary-machine SAT transfer remain open. **P versus NP remains OPEN.**

## 1. Review of actual artifacts

This cycle re-read the current `main4.tex` and `main5.tex`, WIRE_LEDGER1, COMBINED-REPLAY1, LQP, RECOVERY-STRENGTHEN6/7, STREAMCOMP1, REVFIX2, the canonical accounting protocol and summary, and the latest original specialist artifacts:

- `research/agents/physical/2026-10-19_1357_PHYSICAL_SCRAMBLE_GADGET_MACRO9_BRIEF.md`
- `results/raw/physical/2026-10-19_1357_SCRAMBLE_MACRO9_CENSUS.json`
- `research/main/2026-10-19_1348_MAIN_NONLINEAR_MASK_ERASURE8.md`
- `results/raw/synthesis/2026-10-19_1348_NONLINEAR_MASK_ERASURE8.json`

No newer quotient or red-team machine-readable artifact was present. The :24 experiment role remains paused. Root `main.tex` is still markerless/truncated and was not edited.

The new specialist brief reports that permutations, sign flips and clause/literal shuffles still allow recovery of padded AND constraints and XOR3 quartets. At `d=7`, it gives raw versus recovered-macro counts `G=22465/5286`, `E=42187/9882`, `W=25209/8030`, nominal MOS `123814/57108`, fanout-two buffers `12382/893`, and source/macro descriptions `256428/62854` bits. It reports 303 comparisons, 64 near-image rejections and a `Q_3` exhaustive check. The full report, generator and recognizer are not shared; source reads, cache/replay transfers, live state, macro `P_in/P_out`, depth/toggles, routing, placed area, transistor nets and energy are NULL.

The brief also says both that five XOR quartets **uniquely** require `(a,b,t,c,d)=(1,1,0,0,0)` and that there are “4 XOR-only extensions.” Those statements cannot both concern complete assignments to the same five variables. The extension count is quarantined and is not used below.

## 2. Ideas proposed before literature search

1. **Gaussian/nonlinear separation.** Build an invertible five-equation XOR subsystem whose unique solution violates a padded `t=a AND b` gadget. Falsifier: the XOR rank is below five, the claimed solution is not unique, or the full CNF remains satisfiable.
2. **Same-function macro guard.** Compile the exact 25-clause CNF both literally and as recovered XOR/AND gates under one named cell library; exhaust all 32 external assignments. Falsifier: any truth-table mismatch or any ledger identity failure.
3. **Recognition-charge guard.** Separate macro compression from the cost of recognizing the source image. Falsifier: a recognizer that accepts the canonical token word and rejects every Hamming-distance-one word without reading some token on the accepted input.
4. **Full-source recovery challenge.** Charge discovery, partition selection and output of the recovered macro description. Falsifier for the present conditional status: a shared replayable generator/recognizer with complete access/live traces and all-position mutation coverage.

## 3. Primary literature checked after proposals

- Laitinen, Junttila and Niemelä make Gaussian reasoning complete for parity explanations inside DPLL(XOR). This justifies treating the XOR subsystem as algebraically easy in that solver model; it does not justify dropping nonlinear constraints: https://arxiv.org/abs/1207.0988
- Eén and Biere formalize SAT preprocessing by variable elimination and related simplifications. Such source recovery is an algorithmic upper-bound technique whose recognition and output costs must still be charged: https://doi.org/10.1007/11499107_3
- Thompson's VLSI area-time lower bounds require a layout/communication model. Logical nets and nominal MOS proxies do not instantiate routed area-time when placement and wirelength are NULL: https://doi.org/10.1145/800135.804401
- Fortnow, Lipton, van Melkebeek and Viglas prove time-space lower bounds for satisfiability on a fixed random-access Turing-machine model. Their endpoint does not turn circuit compression, rank or a restricted physical ledger into a bound for all SAT algorithms: https://doi.org/10.1145/1101821.1101822

## 4. Exact counterexample: GAUSSIAN-NONLINEAR-SEPARATION9

Let the Boolean variables be ordered `(a,b,t,c,d)`. Over GF(2), impose

```text
a + b + t = 0
b + t + c = 1
t + c + d = 0
c + d + a = 1
d + a + b = 0.
```

The coefficient matrix has rank five. Its unique solution is

`(a,b,t,c,d)=(1,1,0,0,0)`.

Encode each ternary parity equation by its standard four proper 3-CNF clauses, giving 20 distinct clauses. Add the proper padded encoding of `t=a AND b`:

```text
(not a OR not b OR t)
(a OR not t OR c) AND (a OR not t OR not c)
(b OR not t OR d) AND (b OR not t OR not d).
```

These five clauses are also distinct, so the full formula has exactly 25 distinct proper clauses and 75 literal-token positions.

**Theorem.** The XOR-only subsystem has exactly one model, but the full 25-clause formula is unsatisfiable.

**Proof.** Rank five gives the unique XOR solution displayed above. In that solution `a=b=1` and `t=0`, so `(not a OR not b OR t)` is false. Hence no assignment satisfies the full formula. QED.

This is an explicit counterexample to “Gaussian elimination on every detected XOR quartet decides the mixed instance.” It does not imply hardness: the recovered macro formula is decided immediately by evaluating its one AND relation after the linear solve.

## 5. Exact recognition lemma

**Lemma.** Let `R` be a deterministic exact recognizer that accepts a fixed length-`L` token word `w` and rejects every word at Hamming distance one from `w`. On input `w`, `R` must query all `L` positions.

**Proof.** If position `i` is not queried on the accepting run, change only token `i`. The run and answer are unchanged, so the distance-one word is accepted, a contradiction. QED.

For the exact control, `L=75`. For the specialist `d=7` formula, `L=3C=19722`. Testing 64 selected single-literal mutations is useful but cannot establish complete Hamming-neighbor recognition. This is a decision-tree source-access lower bound only; it is not an unrestricted SAT-runtime lower bound.

## 6. Same-library circuit census

Library: `INV=2`, `OR2=6`, `AND2=6`, `XOR2=16`, `BUF2=4` nominal MOS. `P_in` and `P_out` count terminal incidences; `E` counts logical source-sink edges including the output sink; `W` counts physically distinct logical signal nets in the netlist. CNF literal incidences, transistor nets and RAM accesses are separate quantities.

| Variant | G | P_in | P_out | E | W | max fanout | F2 buffers | MOS | MOS+buffers | depth | Gray toggles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| specialist `d=7` raw | 22,465 | NULL | NULL | 42,187 | 25,209 | NULL | 12,382 | 123,814 | 173,342 | 16 | 71,132 |
| specialist `d=7` macro | 5,286 | NULL | NULL | 9,882 | 8,030 | NULL | 893 | 57,108 | 60,680 | NULL | NULL |
| exact 25-clause raw evaluator | 79 | 153 | 79 | 154 | 84 | 10 | 60 | 454 | 694 | 8 | 618 |
| exact recovered macro evaluator | 21 | 38 | 21 | 39 | 26 | 4 | 8 | 220 | 252 | 6 | 316 |

The two control circuits agree on all 32 external assignments; 64 evaluations passed. Their gate mixes are raw `5 INV + 50 OR2 + 24 AND2` and macro `11 XOR2 + 4 INV + 6 AND2`.

At the single specialist scale, macro/raw ratios are `0.2353 G`, `0.2342 E`, `0.3185 W`, `0.4612 MOS`, `0.0721 buffers`, and `0.3501 buffered MOS`. The exact control gives comparable ratios `0.2658`, `0.2532`, `0.3095`, `0.4846`, `0.1333`, and `0.3631`. These are same-scale compression ratios, **not growth slopes** and not hardware minima.

The specialist macro's routing, area, transistor nets, energy, pin counts, max fanout, source accesses, cache/replay transfers, maximum live bits, discovery/selection charge and output cost remain NULL. Dynamic toggles are kept separate from static switch equivalents and are not energy.

## 7. Strongest new pattern and falsifier

**Pattern.** Even after source scrambling, a repeated proper-CNF family may expose a much smaller XOR/AND representation. In both the reported `d=7` record and the exact control, logical `G/E/W` shrink more than nominal MOS because XOR2 is an expensive macro in the fixed library. This is evidence for redundant-gadget inflation and recoverable syntax, not a physical SAT lower bound.

**Falsifier.** Publish the full `d=7` generator and recognizer; replay the partition and same-function claim; reject every one of the 19,722 single-literal-position corruptions; and trace all discovery, selection, reads, transfers, live state and output. Any accepted semantics-changing corruption, overlapping gadget partition, count mismatch, changed cell implementation, or failed same-function replay falsifies the guarded pattern.

## 8. Proof DAG

- **PROVED:** the five-equation XOR matrix has rank five and unique solution `(1,1,0,0,0)`; the 25-clause mixed formula is UNSAT.
- **PROVED:** literal and recovered-macro evaluators are the same Boolean function; exact `G/P/E/W/fanout/buffer/MOS/depth` ledgers follow under the named library.
- **PROVED:** exact full Hamming-neighbor recognition of a fixed `L`-token source requires `L` token probes on the accepted word.
- **COMPUTATIONAL:** 32 assignments × 2 evaluator implementations, clause distinctness, rank/model enumeration and toggle traces pass with no failure.
- **CONDITIONAL:** specialist `d=7` macro equality and census; only the compact brief/raw record is shared, with 64 selected mutations and no replayable full generator.
- **RETIRED:** XOR rank, gate count, nominal MOS, finite compression ratio, fold count, PC degree, separator width or selected mutation rejection as stand-alone evidence for unrestricted SAT time/space lower bounds.
- **OPEN:** physical routing/layout/energy; all-input hereditary quotient or recursive shrinker with charged discovery/selection/replay/read-only input/live RAM; transfer from these restricted representations to arbitrary SAT machines. **P versus NP remains OPEN.**

## 9. Narrow handoffs

- **Physical models (:00):** publish the complete macro partition/generator for `d=7`; add macro `P_in/P_out`, max fanout, depth/toggles, placement, routed length, repeaters, area, transistor nets and measured energy under the unchanged library.
- **Quotient (:12):** run or prove the all-19,722-position near-image test; instrument source reads, random/sequential access, cache/replay, peak live bits, discovery/selection and macro-output writes.
- **Experiments (:24):** remains paused; do not reactivate without user request.
- **Red team (:36):** search for overlapping gadget partitions and one-token semantic mutations that the 64-case suite misses; resolve the “unique” versus “four extensions” discrepancy from the full source.
- **Synthesis (:48):** admit only same-library, same-function, same-semantics and same-machine comparisons; preserve NULL physical/access fields and refuse cross-model lower-bound transfer.

FINAL_VERIFICATION_SENTINEL::MAIN::GAUSSIAN-NONLINEAR-GUARD9::P_VS_NP_OPEN
