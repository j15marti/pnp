# WIRE-SWITCH-ACCOUNTING1 | 2026-10-19 01:05 UTC

**Status:** Reproducible initial accounting, with model-specific implementation counts. P versus NP OPEN. The full audit, seven-scale CSV/JSON, workbook, and runnable netlist generator are packaged in the current conversation.

## Required accounting fields for EVERY proposed model

Record a row for the source, raw construction, simplified construction, and any genuinely routed/synthesized version.

- **Identity:** input family, model/version, parameters (n,m), source and target encoded bit lengths, primitive gate library, semantics, source URL and proof status.
- **Static logic:** gate counts by type; gate input/output terminal incidences P; driver-to-sink directed connection endpoints E; distinct driven signal nets W; fanout distribution; circuit depth.
- **Switch count:** nominal **CMOS MOSFET device equivalents** under an explicit declared library (the baseline uses NAND2 = 4 transistors). This is an *implementation upper-bound proxy*, not a physical minimum.
- **Routing and buffers:** output loads, fanout cap, number/type of buffers, routing wirelength ONLY if a technology/layout is actually supplied. Do not conflate net count, formal tetrahedron edges, or CNF literal occurrences with physical wires.
- **Dynamic activity:** separately record gate-output toggles for a declared input trace, or measured switching energy if supported. Static device count does NOT equal dynamic switching events.
- **Execution resources:** source reads, bit transfers/copies, cache and replay reads, live parent/child memory, output serialization, discovery/reduction and reuse cost.
- **Completeness:** NULL means *not measured*, never zero. Mark NETLIST_EXACT_DECLARED_LIBRARY, MACRO_CENSUS_ONLY, SYNTAX_ONLY_NO_SWITCH_COUNT, or PHYSICALLY_ROUTED_MEASURED.

## Exact finite baseline for repeated clauses

Let F_m=(x0 OR x1 OR x2) repeated m times. For the declared NAND2-only evaluator before clause deduplication:

  G = 8m - 2          NAND2 gates
  MOS = 32m - 8       nominal transistors
  E = 16m - 3         pin-to-driver sink edges, including output sink
  W = 8m + 1          distinct driven logical nets, n=3
  fanout_max = 2m     pin-terminal load count, tied NAND(x,x) loads counted twice
  B_f2 = 6m - 6       abstract two-pin-load buffers
  MOS_with_B_f2 = 56m - 32.

When duplicate clauses are removed, the **same Boolean evaluation function** has G=6, MOS=24, E=13, W=9, fanout_max=2 and B_f2=0, for every m.

m=64: raw G=510, MOS=2040, E=1021, W=513, B_f2=378, buffer-included MOS proxy=3552; normalized G=6, MOS=24, E=13, W=9, B_f2=0.

The declared three-input Gray-code stimulus produced raw logical NAND-output transitions 14m-2 and normalized 12, for each audited scale m=2,4,8,16,32,64,128. Exhaustive Boolean equivalence across 8 assignments and 7 scales: 112/112 passed. Logical activity is not measured energy.

**Falsifier/pattern:** linear growth of raw gates, nets and device proxies does not imply increased minimum circuit size or SAT runtime when the extra clauses are redundant.

## Historical REVFIX census (MACRO, not routed)

For m>=2, two-shear original: AND=3m, XOR=2m, equality=m. WIRE_LEDGER1's NAND2 mapping (2 AND, 4 XOR, 5 EQ) gives G=19m, nominal MOS=76m. Feedback cancellation gives G=10m, nominal MOS=40m, but m output zero-tests, source polarity, actual buffers and routing remain uncharged. Anchored original G=19m-6; feedback-eliminated G=10m-6. These counts are implementation-dependent component inventories, not minima.

## Tetrahedral / NAE models

Keep NAE-GAUGE-TREE signed clauses 6m-6, FACEFREE 8m-9, FANO-LINEAR-PORT 30m-7n-7 as syntax/Boolean-port rows ONLY. Three NAE port incidences and six formal K4 edge incidences per clause are **not** CMOS switches or physical wires. MOS, fanout, routed lengths and energy remain NULL until a matching gate-level FTNC realization exists.

## Analysis in every future hourly run

Fit log-log slopes and compare count ratios only within a fixed library and equivalent functionality. Show *raw versus normalized* counts; identify fanout/buffer growth, source/target serialization and charge any source-specific simplifier. Search for persistent netlist motifs, low-rank/redundant feedback, repeated clauses, and routing hotspots. Never infer arbitrary-machine SAT time from a physical device count.

**Sources:** 
WIRE_LEDGER1: https://github.com/j15marti/pnp/blob/main/research/agents/physical/2026-10-19_WIRE_LEDGER1.md
WIRE-EQUIV-ELIM3: https://github.com/j15marti/pnp/blob/main/research/agents/physical/2026-10-19_0936_PHYSICAL_WIRE_EQUIV_ELIM3_BRIEF.md
FANO-LINEAR-PORT27: https://github.com/j15marti/pnp/blob/main/research/main/2026-10-19_0748_MAIN_FANO_LINEAR_PORT27.tex
Thompson VLSI area-time model: https://doi.org/10.1145/800135.804401

<!-- FINAL_VERIFICATION_SENTINEL::WIRE-SWITCH-ACCOUNTING1::P_VS_NP_OPEN -->
