# MAIN NONLINEAR-MASK-ERASURE8 | 2026-10-19 13:48 KST

**Status:** exact theorem and ledger identities proved; finite audit passed; source validator bound remains conditional; physical layout and arbitrary-machine SAT transfer remain open. **P versus NP remains OPEN.**

## 1. Review of actual artifacts

This cycle re-read the current `main4.tex` and `main5.tex` entry points, the canonical wire/switch accounting protocol and raw summary, WIRE_LEDGER1, the prior BISECTION-DECISION-DECOUPLING7 synthesis, and the newest original red-team report, kernel and raw JSON:

- `research/agents/physical/2026-10-19_1236_PHYSICAL_MASKED_PARITY_SHEAR8.md`
- `experiments/review/2026-10-19_MASKED_PARITY_SHEAR8_kernel.py`
- `results/raw/physical/2026-10-19_MASKED_PARITY_SHEAR8_MIN.json`

The historical spine is unchanged. COMBINED-REPLAY1 is an exact terminating source-backed solver, but it has no favorable general bound. RECOVERY-STRENGTHEN6/7, STREAMCOMP1 and LQP give useful accounting only conditional on a hereditary all-input shrinker with charged acquisition, replay and live state. WIRE_LEDGER1 gives implementation upper bounds, not physical or arbitrary-machine lower bounds. The older tetrahedral/PC results remain restricted-model benchmarks. Root `main.tex` is markerless/truncated and was not edited.

The new construction places a triangular reversible nonlinear map before a cube-graph parity system. At scale `d=7` it reports `V=128`, `M=448`, `N=2744`, `C=6574`, encoded source length `256428` bits, final-coordinate ANF degree `446`, raw evaluator `G=22465`, `W=25209`, `123814` nominal MOS, `12382` fanout-two buffers and `173342` buffered MOS. Routing, placed area, transistor nets, capacitance and measured energy are all NULL.

## 2. Ideas proposed before literature search

1. **Bijective-mask erasure.** Test whether high ANF degree is entirely representation-level: prove the triangular map bijective, then count parity-system preimages before and after masking. Falsifier: one collision, inverse failure, or model-count discrepancy.
2. **Proper-CNF multiplicity audit.** Independently enumerate the five-clause padded AND and four-clause XOR encodings. Falsifier: an invalid gate tuple satisfies, a valid AND tuple has other than four pad extensions, or an XOR tuple lacks unique extension.
3. **Library-granularity identity.** Expand the same charge-parity circuit from XOR2 macros to NAND2+INV and require equal nominal MOS but different `G/E/W/depth`. Falsifier: a count equality fails under the declared four-NAND XOR implementation.
4. **Validator-cost challenge.** Mutate one literal, gate pad, edge label or charge bit and require the canonical recognizer to reject or recompute the correct charge. The current full generator/validator is not shared, so this remains the next falsifiable implementation test.

## 3. Primary-literature check after proposals

- Soos, Nohl and Castelluccia, and the later DPLL(XOR) literature, explicitly integrate Gaussian or Gauss-Jordan elimination into SAT solving for parity constraints. This is a model-matched algebraic escape, not an argument about every CNF solver: https://www.msoos.org/wordpress/wp-content/uploads/2010/08/PoS10-Soos.pdf and https://arxiv.org/abs/1207.0988
- Thompson's area-time theorem is a VLSI layout result; it requires physical layout/communication hypotheses absent from the current NULL routing fields: https://doi.org/10.1145/800135.804401
- Fortnow--Lipton--van Melkebeek--Viglas fix a random-access machine model and transfer already established time-space bounds. They do not turn gate count, ANF degree or a promise quotient into an unrestricted SAT lower bound: https://doi.org/10.1145/1101821.1101822
- Branching-program and proof-complexity lower bounds remain model-specific. They do not close the current all-algorithm transfer: https://eccc.weizmann.ac.il/eccc-reports/1998/TR98-053/ and https://eccc.weizmann.ac.il/report/2014/081/

## 4. Exact theorem: BIJECTIVE-MASK-INVARIANCE8

Let `T_n:{0,1}^n->{0,1}^n` be

`y_0=x_0`, `y_1=x_1`, and `y_i=x_i XOR (y_{i-1} AND x_{i-2})` for `i>=2`.

For `n>=4`, `T_n` is a bijection and the ANF degree of `y_{n-1}` is exactly `n-2`. If `A` is the vertex-edge incidence matrix of the connected cube `Q_d`, with `V=2^d`, `M=d2^(d-1)`, then

`A T_M(x)=b`

is satisfiable iff `XOR_v b_v=0`, and in that case has exactly `2^(M-V+1)` assignments to `x`. When every one of the `M-2` mask ANDs is encoded by the stated five proper clauses with two free pad bits, the full proper-CNF model count is

`2^(M-V+1+2(M-2))`.

**Proof.** Given `y`, recover `x_0=y_0`, `x_1=y_1`, and sequentially `x_i=y_i XOR (y_{i-1} AND x_{i-2})`; hence `T_n` is bijective. Over Boolean ANF, `y_i=x_i+x_{i-2}y_{i-1}`. The exceptional base is `n=3`, where `deg(y_2)=2`; for `i>=3`, induction gives the unique maximum-degree monomial `x_0...x_{i-2}` in `y_i`, hence `deg(y_{n-1})=n-2` for `n>=4`. A connected graph incidence matrix over GF(2) has rank `V-1`; its image is exactly the even-charge subspace and each feasible charge has `2^(M-V+1)` edge preimages. Bijection preserves this count. The proper AND clauses admit exactly four pad assignments for each valid gate tuple and zero for invalid tuples; XOR and parity-chain gates have unique extensions. Multiplying by `4^(M-2)` proves the last formula. QED.

This is a counterexample to the proposed implication “large nonlinear ANF degree or a large compiled evaluator implies a hard SAT decision.” It does not show that arbitrary SAT is easy.

## 5. Exact library-granularity counterexample

For a balanced parity tree on `V=2^d` charge bits followed by one INV, the mixed library counts `V-1` XOR2 cells plus one INV:

| Ledger | G | P_in | P_out | E incl. sink | W | depth | nominal MOS |
|---|---:|---:|---:|---:|---:|---:|---:|
| XOR2+INV macro | `V` | `2V-1` | `V` | `2V` | `2V` | `d+1` | `16(V-1)+2` |
| NAND2+INV expanded | `4V-3` | `8V-7` | `4V-3` | `8V-6` | `5V-3` | `3d+1` | `16(V-1)+2` |

At `d=7`, the same circuit is `G=128, W=256, depth=8` at macro granularity and `G=509, W=637, depth=22` after NAND expansion, while both have `2034` nominal MOS. Therefore gate/net/depth trends are meaningless unless library granularity is fixed. Physical wirelength still remains NULL.

## 6. Independent computational audit

`masked_parity_invariance_audit.py` passed:

- 32,760 exhaustive forward/inverse assignments for `n=3..14`;
- 20 symbolic ANF instances for `n=3..22`, including the explicit `n=3` exception;
- 32 proper-AND and 8 proper-XOR truth assignments;
- all 4,096 `Q_3` edge assignments, yielding 128 even charge vectors with 32 preimages each;
- 75 raw-ledger formula equalities over `d=3..7`.

The shared specialist kernel checks only the reversible map and count formula; the full CNF generator and validator remain local-only. Consequently full-template mutation coverage is **not** promoted to shared computational evidence.

## 7. Mandatory wire/access ledger and trend

Declared library: `INV=2`, `OR2=6`, `AND2=6`, `XOR2=16`, `BUF2=4` nominal MOS. CNF literal incidences are syntax; `P` is gate input/output terminal incidence; `E` is logical source-sink edges; `W` is distinct driven nets. None is routed wirelength or transistor-net count.

| d | B source bits | ANF deg | raw G | raw P_in | raw E | raw W | buffers | raw MOS | buffered MOS | projection MOS | SAT MOS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 2,592 | 10 | 417 | 782 | 783 | 469 | 230 | 2,294 | 3,214 | 526 | 114 |
| 4 | 10,780 | 30 | 1,361 | 2,554 | 2,555 | 1,529 | 750 | 7,494 | 10,494 | 1,538 | 242 |
| 5 | 32,618 | 78 | 3,713 | 6,970 | 6,971 | 4,169 | 2,046 | 20,454 | 28,638 | 3,982 | 498 |
| 6 | 98,464 | 190 | 9,345 | 17,546 | 17,547 | 10,489 | 5,150 | 51,494 | 72,094 | 9,734 | 1,010 |
| 7 | 256,428 | 446 | 22,465 | 42,186 | 42,187 | 25,209 | 12,382 | 123,814 | 173,342 | 22,982 | 2,034 |

Finite endpoint log-slopes, only within fixed semantics/library/model families: raw MOS versus serialized source bits `0.8681`; raw buffered MOS `0.8680`; raw nets `0.8672`; projection MOS versus `M` source bits `1.0434`; charge-decision MOS versus `V` charge bits `1.0393`. These are five-scale descriptors, not asymptotic lower bounds and not cross-function minima.

Canonical validator accounting is conditional/source-reported: source reads `3C`, cache/replay transfers `0`, one output bit, and uninstrumented live-bit upper bound `16 bit_length(B)+128` (320, 352, 368, 400, 416 bits). Its stated `O(B polylog B)` bit-time includes validation/charge extraction, but the actual implementation trace is absent. Reduction discovery, selection and read-only source access therefore remain charged and open for instrumentation.

Dynamic gate-output toggles at `d=7` are `71132` raw, `19086` projection and `1452` charge decision, but the circuits, domains and stimuli differ. They are not energy measurements or valid minimum comparisons.

**Strongest pattern:** nonlinear degree and compiled size can grow dramatically while a source-specific reversible quotient leaves an exact one-bit parity SAT decision. **Falsifier:** break bijectivity, the cube-incidence rank/model count, proper-CNF extension counts, or the declared circuit census; alternatively, exhibit a fully charged same-input same-function implementation whose decision does not reduce to total charge parity.

## 8. Proof DAG

- **PROVED:** the triangular nonlinear mask is bijective; for the actual `M>=12` scales its last-coordinate ANF degree is `M-2`.
- **PROVED:** cube parity after the mask is satisfiable exactly for even total charge; exact edge/model counts follow.
- **PROVED:** padded AND contributes four extensions; XOR contributes one; macro-to-NAND expansion preserves nominal MOS while changing `G/E/W/depth`.
- **COMPUTATIONAL:** independent inverse, ANF, gate semantics, `Q_3` charge distribution and 75 ledger identities pass.
- **CONDITIONAL:** canonical-image validation and charge extraction fit the stated access/live bounds; no shared implementation trace yet.
- **RETIRED:** ANF degree, raw evaluator size, fanout buffers, separator width, finite toggles or physical-looking MOS proxies as stand-alone unrestricted SAT lower bounds.
- **OPEN:** routed area-time/energy; unrestricted Circuit-SAT decision cost; a hereditary all-input quotient/shrinker with full discovery/selection/replay/read-only-input/live-RAM charges; transfer to arbitrary SAT machines. P versus NP remains OPEN.

## 9. Narrow role handoffs

- **Physical models (:00):** place and route `d=5,6,7` raw and charge circuits under one cell library; report routed length, area, repeater insertion, transistor nets and energy without changing semantics.
- **Quotient (:12):** implement full canonical validator plus single-record mutations; trace source reads, random/sequential accesses, cache/replay and peak live bits.
- **Experiments (:24):** remains paused; do not reactivate without user request.
- **Red team (:36):** search for a non-bijective or source-indistinguishable mutation that passes the promised recognizer but changes total charge/SAT; publish full generator if no counterexample.
- **Synthesis (:48):** compare only same-library, same-semantics, same-machine slopes; preserve macro and primitive ledgers separately and reject cross-function “minimum” claims.

FINAL_VERIFICATION_SENTINEL::MAIN::NONLINEAR-MASK-ERASURE8::P_VS_NP_OPEN
