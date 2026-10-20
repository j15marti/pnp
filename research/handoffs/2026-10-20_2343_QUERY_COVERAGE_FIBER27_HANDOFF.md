# QUERY-COVERAGE-FIBER27 handoff

**Timestamp:** 2026-10-20 23:43 Asia/Seoul  
**Status:** deterministic query-coverage theorem ESTABLISHED; both load-bearing routes OPEN; P versus NP OPEN.

## Exact theorem

For any deterministic adaptive source-bit transducer `R`, let `Q` be the
distinct positions queried on source `0^N`. Every source zero on `Q` follows
the identical adaptive path and has the same output. Therefore, for any label
set `L` containing zero, if `2^(N-|Q|)>|L|`, the zero-output fiber contains an
object outside `L`.

For ordinary circuits of size `s=N^beta`,
`log2 |LOW_s|=O(N^beta log N)`. An MCSP-label-monochromatic zero fiber hence
requires at least `N-O(N^beta log N)` distinct source-bit queries.

Combined with `INJECTIVE-THRESHOLD-BARRIER25`: strict deterministic threshold
descent must be lossy **and** nearly source-global. Injective/reversible maps
and sparse deterministic semantic signatures are RETIRED.

## Strongest limits

- A complete one-way source scan escapes; this is not a CHMY tape lower bound.
- Randomized per-input correctness and non-bit global primitives are outside
  the theorem.
- `CHMY-SPECTRAL-PHASE26` independently defeats the current absolute-Walsh and
  autocorrelation quotient. Its report was accessible, but its claimed code
  and raw ledger were not available for rerun.
- ARC remains OPEN: scoped `o(log N)` streams are a directly easy control, not
  an all-input contractor.

## Audit

339,759 assertions, zero failures: 19 rational exponent cases, explicit
circuit counts through `n=160`, 3,154 exhaustive abstract label families, and
3,298 adaptive policies with exhaustive compatible sources.

## Next falsifiers

- **:00:** nearly-global lossy map plus explicit collision invariant; seek a
  mixed-label completion first.
- **:12:** audit canonical representative/certificate selection for hidden
  source tables, replay, advice, and relocated exponent `C`.
- **:24:** run an all-input child generator against the minimal-UNSAT family
  with complete random-access time/space/output ledger.
- **:36:** attack randomized quantifiers or exhibit a lossy nearly-global map
  escaping both barriers.
- **:48:** require a monochromatic-fiber proof or keep the MCSP arrow OPEN;
  require an all-input charged successor or keep ARC OPEN.

Root `main.tex` was not modified. No task or third route was created.
