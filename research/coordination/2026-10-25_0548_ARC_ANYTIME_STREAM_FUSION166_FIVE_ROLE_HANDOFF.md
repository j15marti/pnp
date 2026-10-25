# ARC-ANYTIME-STREAM-FUSION166 — five-role handoff

Status: **PROVED/EXACT under the executable scoped-stream interface**; **COMPUTATIONAL** finite audit. The favorable normalizer, ARC-EDGE-90, and P versus NP remain **OPEN**.

## New exact theorem

No exact output count, computable output envelope, or exponent is needed by the stream consumer. Number emitted records from one. In epoch (k), positions (2^k,ldots,2^{k+1}-1), use block capacity

`b_k = ceil(2^(k/2))`

and close any partial block at the epoch boundary or EOF. For every actual finite stream length (Mge1):

`max block <= sqrt(M)+1`

`number blocks <= (2+sqrt(2))*sqrt(M) + floor(log2 M)+1`.

The scheduler is one-pass, never restarts the producer, and uses `O(log(M+2))` live counter bits. If analysis later proves `M=N^(mu+o(1))`, both quantities are `N^(mu/2+o(1))`, although the fixed uniform program never knows `mu`.

Arbitrary epoch boundaries preserve the exact scoped SAT/UNSAT join: global assignments restrict to a compatible boundary path, and a compatible path glues because every source name remains live across every intervening block boundary.

## ARC consequence

The FUSION164 envelope therefore holds with no stream-length advice:

`t_d <= max(r, mu+2d delta, mu(1-2^-d)+2d delta+mu 2^-d t)`

`s_d <= max(eta, mu/2, delta, mu 2^-d s)`.

At `mu=1`, depth `d=2`, base `(t,s)=(6/5,1/2)`, strict entry still requires the unproved simultaneous conditions:

- `r < 241/200`,
- `eta < 11642479/23232400`,
- `delta < 31/800`.

The highest-value missing object is still the all-input or paid fixed-hard-image normalizer, not its online scheduler.

## Independent Role 2 audit

ARC-CHECKPOINT-ACCESS163 is accepted **PROVED/EXACT restricted** for its explicit copy-on-write checkpoint architecture. It correctly charges complete configurations, output counters, immutable snapshots, overlays, nested replay, and simultaneous checkpoint libraries. It is an upper bound, not a mandatory all-algorithm tax. Use it only when a proposed ARC construction needs arbitrary indexed virtual-output probes. The anytime fusion remains sequential and does not pay checkpoint conversion.

## Finite audit

- all stream lengths `M=1..8192` checked against the symbolic bounds;
- 18 ordinary-CNF SAT/UNSAT cases at one and two real recursive levels;
- Horn/2SAT/affine-semantic and disconnected controls;
- every ordinary child serialized and reparsed;
- parent producer counter unchanged across every child execution;
- 24,630 assertion groups, zero failures.

Finite Python counters are not FLMV traces and do not construct the normalizer.

## Role routing

- **LSPV-1:** remove exact stream-length/exponent discovery from heterogeneous route programs; retain actual analytic exponent proofs.
- **LSPV-2:** apply checkpoint access only to genuinely nonsequential consumers and search for sequential emitter interfaces first.
- **LSPV-3:** specify an executable valid scoped emitter with exact EOF and hereditary two-level grammar; the scheduler is now available.
- **LSPV-4:** audit retained producer/block/cache/ancestor sums under dynamic epoch boundaries and malformed-input EOF behavior.
- **LSPV-5:** preserve this no-advice refinement in root synthesis and continue red-teaming the all-input normalizer.

## Exact next implication

Construct one fixed total deterministic scoped producer, derived from the assumed polynomial SAT decider or an explicit existence theorem, whose actual `(mu,r,eta,delta)` enters the strict envelope and whose both-label semantics, malformed-input totality, source names, ordinary child grammar and two-level hereditary eligibility are proved and fully charged.

Artifacts:

- `research/agents/lspv-5/2026-10-25_0548_LSPV-5_ARC_ANYTIME_STREAM_FUSION166.tex`
- `research/agents/lspv-5/2026-10-25_0548_ARC_ANYTIME_STREAM_FUSION166_audit.py`
- `research/agents/lspv-5/2026-10-25_0548_ARC_ANYTIME_STREAM_FUSION166_results.json`
