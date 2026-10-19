# BISECTION-DECISION-DECOUPLING7

Timestamp: 2026-10-19 12:48 KST  
Scope: physical-principles × asymptotic Circuit-SAT synthesis  
Global status: **P versus NP OPEN**

## Executive result

**PROVED/EXACT:** for every finite connected undirected graph `G=(V,E)` with edge variables `x_e` and Tseitin charge equations

```text
XOR_{e incident to v} x_e = c_v,
```

the system is satisfiable iff `XOR_v c_v = 0`. A spanning-tree construction gives a witness in the even-charge case. This is a statement about the canonical parity system, not arbitrary CNF SAT.

For `|V|=128`, one declared balanced-tree charge decider using `XOR2=4 NAND2`, `NAND2=4 nominal MOS`, and one final `INV=2 nominal MOS` has exactly:

| G | P_in | P_out | E incl. output | W | max fanout | buffers | nominal MOS | depth |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 509 | 1,017 | 509 | 1,018 | 637 | 2 | 0 | 2,034 | 22 |

The streaming promise-model decider reads 128 charge bits, writes one answer bit, performs no cache/replay transfer, and uses at most nine writable bits including an eight-bit index.

**COMPUTATIONAL:** exhaustive Gaussian-elimination checks covered all 771 connected labeled simple graphs on 2–5 vertices and all 23,940 charge systems; zero failures. The gate/pin/net/device formulas also matched exactly.

**HARD FAILURE / QUARANTINE:** the 11:36 specialist compact record labels its source a canonical `Q7` parity CNF but reports 128 vertices, 960 variables, 2,560 clauses, 7,680 literal records, and eight occurrences per variable. A standard direct `Q7` parity CNF has 448 edge variables, 8,192 width-seven clauses, 57,344 literal records, and 128 occurrences per edge variable. The reported census could describe an auxiliary encoding, but the construction, primitive library, and full code are absent. Its raw/XOR counts are preserved verbatim but are not accepted as standard `Q7` counts and are excluded from same-library slopes.

## 1. Review of actual project evidence

This run re-read current `main4.tex`, `main5.tex`, CANONICAL-WIRE-ERASURE4, RECOVERY-STRENGTHEN7, WIRE_LEDGER1, the wire/switch accounting protocol and summary, and the new `TSEITIN_BISECTION_GAUSS7` handoff and compact raw JSON. Root `main.tex` still contains a literal truncation placeholder and was not edited.

Historical state retained:

- **PROVED/EXACT:** canonical local-pin plus REVFIX images admit fixed-offset source extraction; expansion, literal incidence, and gate inventory are not hardness amplification.
- **PROVED/EXACT:** WIRE_LEDGER1 counts declared REVFIX functional gates and NAND2 upper bounds, while leaving fanout, routing, transistor nets, and physical delay open.
- **CONDITIONAL:** RECOVERY-STRENGTHEN6/7, RECURCLOSE1, STREAMCOMP1, and LQP-style provenance become useful only with a uniform hereditary all-input phase and charged acquisition/replay/live state.
- **COMPUTATIONAL:** prior replay and netlist experiments characterize named implementations, not arbitrary SAT algorithms.
- **OPEN:** same-model layout lower bounds, an all-input quotient/shrinker, and entry into any forbidden SAT time-space region.

## 2. Integrations proposed before literature search

1. **Template validator → charge quotient.** Scan all source records, validate the declared graph/CNF template, and emit a charge vector. Falsifier: a malformed input is accepted, or output serialization/access is omitted.
2. **Spanning-tree witness extension.** For connected `G` and even total charge, set non-tree edges to zero and solve tree edges leaf-to-root. Falsifier: an even-charge connected instance lacks an extension or an emitted witness violates a vertex equation.
3. **Bisection/decision decoupling.** Use the standard `Q7` parity system as a counterexample to the implication “large balanced source interface ⇒ large promised SAT-decision circuit.” Falsifier: total charge parity fails to decide a canonical connected instance or the declared charge circuit count is wrong.
4. **Raw/XOR/charge semantic audit.** Compare counts only after identical input/output functions, library, and traces are established. Falsifier: any input produces different semantics. Status: **OPEN**, because full specialist code/netlists are not shared.

## 3. Literature reconciliation

Tseitin's original construction and Urquhart's expander formulas support proof-system hardness for particular encodings; they do not contradict the elementary solvability criterion for the underlying linear parity system. Harper-type edge isoperimetry supports a balanced `Q7` boundary of at least 64 edges. Thompson's area-time method requires a fixed function and explicit VLSI layout/communication model. Fortnow–Lipton–van Melkebeek–Viglas proves SAT lower bounds only for its charged random-access time/space model. None transfers source bisection or resolution hardness to an unrestricted SAT machine automatically.

Primary references:

- G. S. Tseitin, *On the Complexity of Derivation in Propositional Calculus* (1968): https://www.mathnet.ru/eng/znsl2268
- A. Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987: https://doi.org/10.1145/7531.8928
- L. H. Harper, *Optimal Numberings and Isoperimetric Problems on Graphs*, JCT 1, 1966: https://doi.org/10.1016/S0021-9800(66)80059-5
- C. D. Thompson, *Area-Time Complexity for VLSI*, STOC 1979: https://doi.org/10.1145/800135.804401
- L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005: https://doi.org/10.1145/1101821.1101822

## 4. Exact theorem and proof

### Theorem: connected Tseitin parity criterion

Let `G=(V,E)` be connected and let `c in F_2^V`. The system `Bx=c`, where `B` is the unoriented vertex-edge incidence matrix over `F_2`, is consistent iff `sum_v c_v=0`.

**Necessity.** Sum every vertex equation. Each edge variable occurs twice and cancels, leaving `0=sum_v c_v`.

**Sufficiency and witness extension.** Choose a rooted spanning tree and set every non-tree edge to zero. Repeatedly remove a non-root leaf `v`, assigning its parent edge the unique bit that satisfies the equation at `v`. After all non-root vertices are removed, every edge contribution has been fixed. The root equation holds because the sum of all equations is zero and the total charge is even. Projection reads the charge vector; extension is the displayed construction.

### Corollary: standard `Q7` decision decoupling

The graph `Q7` has 128 vertices and 448 edges. A coordinate bisection crosses 64 edges, and the edge-isoperimetric theorem makes 64 the minimum balanced edge boundary. Nevertheless, on the canonical parity-system promise, satisfiability is one parity bit of the 128 charges. Therefore source bisection is not by itself a lower bound on the promised decision circuit.

This does not refute a Thompson lower bound for computing the complete source predicate, producing a full witness, or validating arbitrary serialized inputs. Those are different functions and interfaces.

## 5. Mandatory wire/access ledger

### Exact declared charge circuit

- Primitive library: `NAND2=4 nominal MOS`, `INV=2 nominal MOS`; `XOR2` macro is four NAND2 cells.
- Functional structure: 127 XOR2 macros in seven balanced levels, then one INV.
- `G=508 NAND2 + 1 INV = 509`.
- `P_in=2·508+1=1,017`; `P_out=509`.
- `E=P_in+1=1,018`, including one external output sink.
- `W=128 primary-input nets + 509 gate-output nets =637`.
- Maximum pin-load fanout is two; no buffers are needed in this declared topology.
- Static nominal MOS `=508·4+2=2,034`; depth `=3·7+1=22`.
- Source reads: 128 charge bits under the promise interface. Output: one bit. Cache/replay: zero. Writable live state for the streaming alternative: nine bits.
- Routing/layout: **NULL**. Placed area: **NULL**. Actual transistor nets: **NULL**. Measured energy: **NULL**.

### Source-reported compact variants, quarantined

| Variant | G | reported E | W | buffers | nominal MOS | toggles | missing/guard |
|---|---:|---:|---:|---:|---:|---:|---|
| raw predicate | 8,639 | 16,319 | 9,599 | 4,800 | 47,994 | 188,094 | library, P_in/out, fanout, depth, trace, routing; schema mismatch |
| XOR rewrite | 6,398 | 12,158 | 7,358 | 1,920 | 25,592 | 161,053 | same missing fields; different function |
| charge decision | 509 | 1,018 | 637 | 0 | 2,034 | 12,986 | circuit counts independently derived; toggle trace unspecified |

The descriptive ratios `47,994/2,034≈23.596` and `25,592/2,034≈12.582` are cross-function, partly cross-library ratios, not slopes and not lower bounds.

### Validation/access boundary

The specialist record reports an 84,504-bit serialized source, 7,680 source-record reads, zero cache/replay reads, and a 236-live-bit upper bound. Its quotient output writes are unspecified and remain **NULL**. On a separately supplied 128-bit charge vector, the one-pass parity stream uses 128 reads, one write, zero replay, and nine live writable bits. These interfaces must not be conflated.

## 6. Weekly-scale trend and strongest pattern

The chart-ready JSON preserves all NULLs and marks all three new variants `comparable_slope=false`. The strongest valid pattern is qualitative and model-matched: a large source boundary may coexist with a small promised quotient decision because validation, predicate evaluation, witness production, and SAT decision are distinct functions.

Falsifier: a connected canonical parity system whose satisfiability differs from total charge parity; a mismatch in the 128-input circuit ledger; or a published auxiliary `Q7` encoding reconciling the reported `960/2560/eight-occurrence` census.

## 7. Versioned proof DAG

- **PROVED/EXACT:** connected Tseitin parity system → even-total-charge criterion → spanning-tree witness extension.
- **PROVED/EXACT:** 128-bit charge decision → declared 509-gate, 2,034-MOS upper-bound circuit and 128-read streaming algorithm.
- **COMPUTATIONAL:** 23,940 systems on 771 connected graphs; zero theorem failures.
- **QUARANTINED:** specialist raw/XOR `Q7` counts pending the missing auxiliary encoding, library, pin ledger, code, and trace.
- **CONDITIONAL:** arbitrary serialized input → validated canonical template → extracted charge vector; output serialization and full malformed-input proof are missing.
- **RETIRED:** source bisection, CNF literal incidence, fold count, PC degree, or static MOS count alone implies unrestricted SAT runtime.
- **OPEN:** model-matched physical routing/area-time lower bound for the full function; uniform all-input quotient/shrinker; unrestricted SAT machine lower bound.
- **OPEN:** P versus NP.

## 8. Narrow role handoff

- **Physical models (:00):** publish the missing auxiliary encoding and full code/netlists; declare primitive cells, P_in/P_out, max fanout, depth, buffer inclusion, and toggle trace. Reconcile `Q7: 448 edges/8,192 direct clauses` with `960/2,560/eight occurrences`.
- **Quotient (:12):** formalize the arbitrary-input template validator and exact charge-vector output serialization; prove rejection of one-record mutations.
- **Experiments (:24):** remains paused; do not activate without user request.
- **Red team (:36):** attack the promise boundary and the graph/CNF schema; distinguish full predicate, witness production, and one-bit decision.
- **Synthesis (:48):** ingest only timestamped raw records; keep cross-function/library ratios quarantined and preserve NULL physical fields.

Root `main.tex` was left untouched because it remains markerless/placeholder-truncated.

FINAL_VERIFICATION_SENTINEL::MAIN::BISECTION-DECISION-DECOUPLING7::P_VS_NP_OPEN
