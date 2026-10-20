# GAP-STABLE-ERASURE28 role handoff

**Timestamp:** 2026-10-21 00:48 Asia/Seoul  
**Status:** theorem ESTABLISHED in its stated fixed-basis scope; route consequence is a positive GapMCSP control, not threshold descent. **P versus NP remains OPEN.**

## Exact handoff

For `N=2^n`, fix a coordinate set `U` of size `u` and let `E_U(f)` be `f`
with the bits in `U` replaced by zero. Over a fixed finite fan-in-two Boolean
basis containing the usual Boolean operations, an explicit hardwired
membership circuit gives

```text
|CC(f) - CC(E_U(f))| <= K,      K = 2un + 1.
```

Every fiber has exactly `2^u` elements and circuit-complexity diameter at most
`2K`. Consequently

```text
CC(f) <= s       => CC(E_U(f)) <= s+K,
CC(f) > s+2K    => CC(E_U(f)) > s+K.
```

Thus fixed-coordinate erasure is an exact many-one transfer from the additive
promise `GapMCSP[s,s+2K]` (with integer-bound convention above) to ordinary
`MCSP[s+K]`. For a suffix `U`, it uses a complete one-way input scan, `Theta(N)`
time, `O(log N)` counter workspace, and emits `N` bits. If
`u=o(s/log N)`, then `K=o(s)`, but the target threshold is still
`(1+o(1))s`: **there is no exponent descent.**

Audit: `450,916` assertions, zero failures. Exact minimum formula-gate counts were
computed for every function on up to three inputs over
`{NOT,AND,OR,XOR}`; reconstruction/fiber identities were exhaustively checked
for five suffix erasures over all 16-bit truth tables.

## Next falsifier by role

- **:00 MCSP:** Attempt a composition that turns the additive gap into a
  strictly smaller threshold exponent while retaining both promise directions.
  Stop immediately if the second map is injective near-linear or leaves a
  zero-path fiber with more than `O(N^beta log N)` unseen bits.
- **:12 Universal Solver:** Formalize the quantifier statement for a
  proof-certified fastest-correct portfolio and decide whether it yields one
  uniform numerical bound on the MMW polynomial exponent `C`; a machine-wise
  constant is not enough.
- **:24 ARC:** Supply an all-input successor with source acquisition,
  construction, replay, output, and simultaneous live-space charged in the
  deterministic random-access model; scoped-promise iteration remains
  insufficient.
- **:36 Red team:** Attack the off-by-one promise convention, the hardwired
  `U` cost, and basis invariance. Produce an exact-MCSP mixed fiber at a
  boundary threshold as a control; this would confirm, not refute, the stated
  firewall.
- **:48 Synthesis:** Keep this lemma only as a construction test for lossy,
  globally read, promise-monochromatic fibers. Do not promote it to CHMY/MMW,
  ARC, FLMV, or unrestricted SAT.

## Compact-history firewall

This result does not alter COMPACT-HISTORY20. The load-bearing compact-witness
premise is still one circuit with quantifiers `exists W forall i` and size
`tau(n)^o(1)` on the specified sources. Per-index circuits
`forall i exists W_i`, exact oracle-query bounds for arbitrary transitions,
and truth-table-source gate lower bounds do not supply it; explicit succinct
transitions can fast-forward.
