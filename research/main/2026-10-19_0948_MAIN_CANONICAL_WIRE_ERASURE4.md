# CANONICAL-WIRE-ERASURE4

Timestamp: 2026-10-19 09:48 KST  
Scope: physical-principles and asymptotic Circuit-SAT synthesis  
Global status: **P versus NP OPEN**

## Executive result

**PROVED/EXACT for the declared ordered Boolean compiler:** the complete local-false-pin plus cyclic REVFIX composite is not merely algebraically cancellable. Its original proper 3-SAT source is a fixed-offset projection of the target clause stream.

For a source with `n` variables and `m` clauses, the recovered local-pin stage has `n+22m` variables and `36m` clauses. Applying cyclic REVFIX to those `36m` clauses gives

- `n+526m` variables,
- `972m` proper clauses,
- `2916m` CNF literal incidences.

On the promise that the input is this canonical ordered image, source clause `i` is recovered with exactly three random literal reads. Consequently, the expansion cannot by itself amplify SAT difficulty: a solver may erase it and solve the original source.

**COMPUTATIONAL:** 120 independently generated proper source formulas were encoded and decoded exactly; all `525,852` generated target clauses participated in the construction checks. One thousand symbolic ledger rows passed.

**OPEN:** a low-space recognizer for arbitrary malformed near-images with a complete sequential-replay ledger; transistor placement, wire length, bisection, clocking, and arbitrary Circuit-SAT runtime.

## 1. Review of original project artifacts

This run read the current root `main4.tex` and `main5.tex`, original COMBINED-REPLAY1 report, implementation, and raw results; RECOVERY-STRENGTHEN6/7; STREAMCOMP1; RECURCLOSE1; PRIME-LQP1; REVFIXGATEAUDIT1; WIRE_LEDGER1; WIRE_REPLAY2; the 08:43 TETRALOCALPINREVFIX-RECOVERY1 report, code, and raw data; and the 09:36 WIRE-EQUIV-ELIM3 report, code, and raw data.

The recovered state is:

- **PROVED/EXACT:** local Boolean matching-selector compiler `n+22m`, `36m`, maximum auxiliary occurrence eight, and exact whole-clause separator preservation. Actual three-dimensional FTNC gluing remains open.
- **PROVED/EXACT:** for REVFIX, `y'_i=y_i XOR h_i` together with `y'_i=y_i` is equivalent to `h_i=0`; the feedback layer cancels semantically. The cyclic one-clause defect is irrelevant after the local-pin stage because it supplies `36m >= 36` clauses.
- **COMPUTATIONAL:** WIRE_REPLAY2 exhibits a source-replay/storage tradeoff for a particular Shannon solver, not a universal lower bound.
- **CONDITIONAL:** RECOVERY-STRENGTHEN6/7, RECURCLOSE1, and STREAMCOMP1 close resource recurrences only after a uniform all-input shrinker or implicit child generator is supplied with all access, replay, buffer, and live-state costs.
- **CANDIDATE / negative baseline:** PRIME-LQP provenance is syntactic and reacquirable unless a same-realization semantic consumer is proved.

## 2. Integrations proposed before literature search

1. **Canonical inverse:** recover the original source directly from fixed target positions and test exact read/write cost.
2. **Fanout correction:** add fanout-two buffer trees to the logical gate ledger rather than conflating a high-fanout signal name with one physical wire.
3. **Replay comparison:** decode before running COMBINED-REPLAY1 and determine whether any claimed composite cost survives canonical erasure.

Only item 1 becomes a new theorem. Item 2 receives an exact parametric ledger and finite measurements. Item 3 yields an upper-bound escape; an experimental same-input comparison remains assigned.

## 3. Literature check after the proposals

Eén and Biere's SAT preprocessing work confirms that satisfiability-preserving variable and clause elimination can dramatically shrink structured encodings; it does not prove a lower bound from the removed syntax. Williams's Circuit-SAT self-improvement theorem operates within its stated circuit-size and running-time hypotheses and does not convert an easily recognizable compiler image into a lower bound for all Circuit-SAT instances. Fortnow-Lipton-van Melkebeek-Viglas applies only after one algorithm is placed in its charged random-access time-space regime. Thompson-style VLSI area-time or bisection statements require an explicit layout model and cannot be inferred from CNF literal incidence or NAND cell count.

## 4. Exact fixed-offset inverse theorem

Let `B(F)` be the recovered ordered local-pin compiler. Inside local-pin block `i`, numbered from zero, the three source literals occur as the second literals of intermediate clauses at offsets

```text
36i + 11, 36i + 13, 36i + 29.
```

Let `R(G)` be the ordered cyclic REVFIX emitter. For intermediate clause `G[j]=(a,b,c)`, the first two violation gates occupy target clauses `10j,...,10j+9`, and

```text
a = R(G)[10j][0]
b = R(G)[10j][1]
c = R(G)[10j+5][1].
```

Therefore source clause `F[i]` is exactly

```text
(
  R(B(F))[10(36i+11)][1],
  R(B(F))[10(36i+13)][1],
  R(B(F))[10(36i+29)][1]
).
```

### Theorem: canonical wire erasure

On promised canonical images `R(B(F))`, a random-access transducer recovers `F` with exactly `3m` literal reads and `3m` literal writes, zero cache transfers, and zero replay transfers. If

```text
w = ceil(log2(n+526m+1)) + 1
```

bits encode a signed literal, the implementation audited here uses at most

```text
3w + ceil(log2(972m+1)) + ceil(log2(m+1)) + 12
```

simultaneously live bits.

The proof is the displayed fixed-offset composition. It is an inverse of the canonical emitter, not a SAT decision procedure.

### Malformed-input firewall

The three-read decoder is a promise algorithm. Certifying that an arbitrary target is a canonical image requires checking the remaining `2916m-3m` literal incidences and all template relationships. A complete pass has the following unavoidable input/output accounting before extra replay or stored cross-references:

- `2916m` literal reads,
- `972m` clause-boundary reads,
- `3m` literal writes,
- `m` output clause boundaries,
- `3892m` record events total.

Later shear records refer back to first-position literals of earlier intermediate clauses. A strict sequential verifier must either store those references, replay the input, or use random access. No favorable all-input recognition bound is claimed here.

## 5. Mandatory wire-by-wire ledgers

Set `r=36m`, the number of local-pin clauses entering REVFIX.

### 5.1 Original functional REVFIX over the local-pin target

Primitive library: `AND2`, `XOR2`, equality comparator; unbounded named-net fanout only until the buffer row below.

Routing assumptions for this logical ledger: both literal polarities are available at the source interface, gates have no geometric coordinates, and a named net may drive every listed sink. If complement rails are not supplied, inverter cells and their nets must be added instance by instance. Clock distribution and wire length are not included.

| Quantity | Exact ledger |
|---|---:|
| AND gates | `3r = 108m` |
| XOR gates | `2r = 72m` |
| Equality comparators | `r = 36m` |
| Functional gates `G` | `6r = 216m` |
| Gate input-pin incidences | `12r = 432m` |
| Gate output-pin incidences | `6r = 216m` |
| Logical source-sink edges `E` | `12r = 432m` |
| Distinct named functional nets `W` | `n+22m+6r = n+238m` |
| Macro depth | at most `8` |
| External acceptance conditions | `r = 36m` |

CNF literal incidences are a different category: the local-pin CNF has `108m`, while the final REVFIX CNF has `2916m`. Neither number is a transistor-net count.

### 5.2 After exact feedback cancellation

Primitive library: `AND2`, `XOR2`, zero-output acceptance.

| Quantity | Exact ledger |
|---|---:|
| AND gates | `108m` |
| XOR gates | `36m` |
| Functional gates `G` | `144m` |
| Gate input-pin incidences | `288m` |
| Gate output-pin incidences | `144m` |
| Logical source-sink edges `E` | `288m` |
| Distinct named nets `W` | `n+166m` |
| Acceptance outputs | `36m` |
| Macro depth | at most `6` |

This is still only a verifier for a proposed assignment. Canonical source extraction leaves the original `m` source clauses; it does not decide them.

### 5.3 Declared NAND2 implementation upper bounds

Use `AND2 = 2 NAND2`, `XOR2 = 4 NAND2`, and `XNOR2 = 5 NAND2`. One explicit topology has depths 2, 3, and 4 respectively.

| Quantity | Original | After cancellation |
|---|---:|---:|
| NAND2 cells | `684m` | `360m` |
| NAND input pins | `1368m` | `720m` |
| NAND output pins | `684m` | `360m` |
| Declared NAND depth upper bound | `21` | `14` |

These are library-dependent implementation upper bounds. Static-CMOS transistor count would depend on the chosen cells; distinct transistor nets, diffusion sharing, placement, routing length, congestion, capacitance, clocking, and area remain **OPEN**.

### 5.4 Fanout-two buffer correction

For every named net `s` with sink fanout `d_s`, a declared balanced fanout-two tree uses

```text
B = sum_s max(0,d_s-2)
```

buffers. For the original macro network this changes the ledger to

```text
G' = 216m + B
E' = 432m + B
W' = n + 238m + B
```

and adds at most

```text
max_s max(0,ceil(log2 d_s)-1)
```

buffer stages. The audit computes `B` from each actual generated netlist. In eight retained samples it ranged from 94 buffers at `m=1` to 786 at `m=8`, with maximum named-net fanout between 16 and 20. This is an exact buffer count for the declared macro graph, not a transistor or placement optimum.

### 5.5 Source, cache, replay, and output charges

| Operation model | Source/target accesses | Cache/replay | Live bits | Output |
|---|---:|---:|---:|---:|
| Promised random-access inverse | `3m` target literal reads | `0 / 0` | displayed logarithmic bound | `3m` literals + `m` boundaries |
| Full target stream pass | `2916m` literals + `972m` boundaries | extra validation replay **OPEN** | log-space for extraction; validation tradeoff **OPEN** | same |
| Decode then COMBINED-REPLAY1 | inverse cost plus COMBINED-REPLAY1 on `F` | exactly the source solver's charged cache/replay | inverse bound plus solver live state | SAT bit |

Reduction discovery is constant template selection on a promised canonical image. For arbitrary inputs, discovering and validating membership in the image is charged separately. No input is treated as free, and writing recovered `F` is charged.

## 6. Composite consequence and challenge

For every exact SAT solver `A`, the canonical composite has the algorithmic upper bound

```text
T_A(R(B(F))) <= T_decode(R(B(F))) + T_A(F),
S_A(R(B(F))) <= S_decode + S_A(F) + O(1).
```

Thus no lower bound can be obtained solely from the composite's `972m` clauses, `2916m` literal incidences, `684m` NAND cells, or physical fold multiplicity. COMBINED-REPLAY1 may be run after erasure on `F`; any additional composite replay is avoidable on canonical images.

The challenge is equally explicit: malformed near-images may make validation costly, but Circuit-SAT includes all circuits, not only malformed encodings, and a hardness proof must establish a model-matched all-input implication. PRIME-LQP tags do not block the decoder when they are deterministic syntax; they can be dropped and reacquired.

Area-time and bisection conclusions remain unavailable. The ledgers above contain no geometric placement or wire-length embedding, and a verifier circuit for one assignment is not a Circuit-SAT decider.

## 7. Versioned proof DAG

- **PROVED/EXACT:** proper 3-SAT -> local false-pin Boolean matching CNF (`n+22m`, `36m`, auxiliary occurrence eight).
- **PROVED/EXACT:** local-pin CNF -> cyclic REVFIX CNF (`n+526m`, `972m`) because the intermediate has at least 36 clauses.
- **PROVED/EXACT:** REVFIX feedback equality cancels to zero-output conditions.
- **PROVED/EXACT:** the complete ordered composite has the displayed `3m`-read canonical inverse.
- **COMPUTATIONAL:** 120 exact round trips, 525,852 target clauses constructed, 1,000 ledger rows, and instance-specific fanout-two buffer counts.
- **CONDITIONAL:** recursive quotient/shrinker closure and implicit-child simulation under RECOVERY-STRENGTHEN6/7, RECURCLOSE1, and STREAMCOMP1 premises.
- **OPEN:** low-space arbitrary-input image recognition, layout/bisection/area-time, and a source-matched all-input Circuit-SAT shrinker.
- **RETIRED:** using functional wire count, CNF literal incidence, transistor-cell count, fold count, or PC degree alone as an unrestricted SAT runtime lower bound.
- **OPEN:** any transfer into the FLMV forbidden random-access time-space region.
- **OPEN:** P versus NP.

## 8. Narrow role handoff

- **Physical models:** emit the normalized macro netlist and place both original and fanout-two-buffered versions in one explicit VLSI model; report wire length, bisection, area, and clock depth separately from gate count.
- **Quotient:** build an arbitrary-input canonical-image recognizer. Compare random access, stored-reference, and sequential-replay implementations with exact live-bit ledgers.
- **Experiments:** run the original COMBINED-REPLAY1 implementation on each `F` and on `R(B(F))` after canonical decoding, using polynomial-size hard controls and identical cache budgets.
- **Red team:** mutate one record at a time outside the three projection positions and find the minimum validation work needed to reject near-images. Attack the stated 3-read promise boundary, not the proved formula.
- **Synthesis:** compare Williams, FLMV, VLSI, and branching-program endpoints only after the same algorithm and access model are fixed. Preserve tetrahedral and PC results as restricted benchmarks.

## Primary references

1. N. Eén and A. Biere, *Effective Preprocessing in SAT through Variable and Clause Elimination*, SAT 2005, DOI 10.1007/11499107_5.
2. R. R. Williams, *Self-Improvement for Circuit-Analysis Problems*, STOC 2024, DOI 10.1145/3618260.3649723.
3. L. Fortnow, R. Lipton, D. van Melkebeek, and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822.
4. C. D. Thompson, *Area-Time Complexity for VLSI*, STOC 1979.

FINAL_VERIFICATION_SENTINEL::MAIN::CANONICAL-WIRE-ERASURE4::P_VS_NP_OPEN
