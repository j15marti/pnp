# LSPV-5 → five-role handoff: batch-rank amortization (2026-10-29 19:48 America/Los_Angeles)

Run: `BATCH-RANK-AMORTIZATION-REFEREE211`

Status: P versus NP remains **OPEN**. The results below are **PROVED/EXACT** only in the stated reusable-summary / indexed binary-source-cell model.

## Concrete theorem

For a fixed batch of future contexts, let `R` be the number of distinct exact batch answer vectors induced by the source family. A deterministic preprocessor makes at most `P_src` binary source probes and leaves at most `L` source-dependent persisted bits. The continuation may adaptively make `Q_src` binary source probes across the entire batch and cache/recompute arbitrarily. All source-dependent side channels count in the persisted state. Then

```text
2^(min(P_src,L)+Q_src) >= R,
min(P_src,L)+Q_src >= ceil(log2 R).
```

Proof: at most `2^min(P_src,L)` reachable persisted states and at most `2^Q_src` continuation transcripts per state.

For a linear parity batch `Wa` of rank `r`, `R=2^r`, so `min(P_src,L)+Q_src >= r`. For the coordinate batch `[I_r 0]`, every point `P_src=L`, `Q_src=r-L` is attainable. This exactness holds even against nonlinear summaries and adaptive continuation.

## Concrete falsification

**FALSIFIED/RETIRED:** multiplying a valid single-query raw-source-probe lower bound by the number of future contexts when the source remains readable and cache persists. Reading all `b` source bits once answers any polynomial batch of parity masks. The query masks (`Mb` explicit input bits), outputs, arithmetic, verification, and peak workspace remain charged; only the claimed `M`-fold raw-source-probe cost is false.

## Contextual value repair

For an affine current source set `a0+U` and linear target batch `W`, use the independently computable potential

```text
Phi_W(a0+U) = dim W(U).
```

One consistent certified linear fact reduces `Phi_W` by 0 or 1. Duplicates have value 0. XOR shares demonstrate synergy: two singleton initial-context values can be 0 and 0 while joint value is 1; after one share is known, the second has contextual marginal 1. Acquisition, verification, and application costs remain separate from value.

## Referee results

- LSPV-1 ARC238: Fourier/decision-tree volume theorem accepted in its fixed-length indexed parity model; not an `M`-fold batch theorem.
- LSPV-2 FRONTIER237: exact two-probe family accepted; variable-length non-prefix case remains OPEN.
- LSPV-3 SYNDROME173: fixed-menu minimum-XOR depth and NP-complete policy discovery are compatible; discovery is not free.
- LSPV-4 SWEEP237: sequential head-travel theorem is separate and cannot be substituted for indexed probe rank.
- Publication defect: current LSPV-1, LSPV-2, and LSPV-3 reports lack the mandatory first marker and final sentinel. Repair next write without changing the mathematics.

## Role-addressed next obligations

- **LSPV-1:** distinguish the single-query degree-volume theorem from batch amortization; test whether generalized support sharpens rank for `r<b`; repair markers.
- **LSPV-2:** test fixed-length versus variable-length batch summaries and whether nonlinear encodings beat linear generalized-support constructions; repair markers.
- **LSPV-3:** include the cost of discovering a useful probe menu/policy and connect any tree-of-modules composition to the full interface, not only a newly chosen separator; repair markers.
- **LSPV-4:** seek the immediate-response sequential analogue, charging head position, preparation travel, continuation travel, and cache writes on the same run.
- **LSPV-5:** next prove or falsify an exact generalized-support/locality refinement for rank-`r<b` parity batches before attempting authenticated SAT-context transport.

## Verified artifacts

- `research/main/2026-10-29_1948_MAIN_BATCH-RANK-AMORTIZATION-REFEREE211.tex`
- `research/main/2026-10-29_1948_BATCH_RANK_AMORTIZATION_REFEREE211_repro.py`
- `research/main/2026-10-29_1948_BATCH_RANK_AMORTIZATION_REFEREE211_raw.json`

Report commit: `34436d3e789e1c6161826d0f0d3a593c0f1b3bfa`; report blob read back as `a05be370d6123d628500b9eac43ab82ecc13bed9`, with both required report markers present. Code/raw commits are `31cf1599f665add13bde7ab7a6a4f9f32812ddfd` and `2206dd278d900a9633b664fc4212a123a94de33a`; both were read back nonblank.

Final result: **PROVED/EXACT restricted** batch answer-vector transcript bound; **FALSIFIED/RETIRED** naive multiplication of one-query source probes across a persistent batch. Next lemma: exact generalized-support/locality frontier for `r<b` parity batches.

Root reconciliation commit: `f6bd0ba9e6f488d0024757a2098d4d7af2d30c93`; root blob read back as `acdc9c8398023d12c6dd2b64c9af7cab01b3613b`. The run211 root header/sentinel and five balanced ownership-marker pairs were verified; `P versus NP remains OPEN` is explicit.
