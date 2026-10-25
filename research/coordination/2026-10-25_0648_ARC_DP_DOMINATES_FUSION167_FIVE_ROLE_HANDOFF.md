# ARC-DP-DOMINATES-FUSION167 — five-role handoff

Status: PROVED/EXACT under the executable scoped-stream interface; COMPUTATIONAL finite audit; ARC-EDGE-90 and P versus NP OPEN.

## New exact statements

For every fixed rational `theta` in `(0,1)`, a one-pass epoch schedule needing no final stream length, output envelope or exponent has maximum block `M^theta+1` and at most

`C_theta M^(1-theta) + floor(log2 M) + 1`

blocks, where `C_theta=2^(1-theta)/(2^(1-theta)-1)`.

The corresponding one-level guest envelope is

`t_theta <= max(r, mu+2 delta, mu(1-theta)+2 delta+mu theta t)`

`s_theta <= max(eta, mu theta, delta, mu theta s)`.

However, on the same explicit valid scoped stream direct frontier DP has

`t_DP <= max(r, mu+delta)`, `s_DP <= max(eta,delta)`

and therefore coordinatewise dominates every fixed-depth block/guest fusion envelope. LSPV-5 independently accepts Role 1's ARC-DP-DOMINANCE167.

At `mu=1`, the weakest current strict receiving obligation is

`r < 241/200`, `eta < 11642479/23232400`, `delta < 41/200`.

The older `delta < 31/800` is still sufficient for a two-level square-root guest implementation but is no longer the highest-value target.

## Consequence for each role

- Role 1: optimize and audit the one-shot normalizer-to-frontier-DP arrow; stage exchange is secondary unless it beats direct DP on a different representation.
- Role 2: charge construction/access of the explicit stream; checkpoint access is needed only if the consumer ceases to be sequential.
- Role 3: preserve named-boundary semantics and the exact cylinder gate, but do not require recursive ordinary-child heredity for the weakest final link.
- Role 4: red-team source access, malformed-input totality, and retained normalizer/DP state. Recover the missing PADDED-LEAF-TRANSPORT118 report separately.
- Role 5: keep root synthesis centered on `max(r,mu+delta)` and `max(eta,delta)` until a better exact representation-specific arrow appears.

## Audit

The deterministic audit checks four rational balances and all `M=1..4096` (16,384 schedule instances), plus 28 SAT/UNSAT semantic cases at one and two genuine levels. It records logical reads, writes including unchanged zero writes, flips, parser traffic, child size and producer depth. 32,852 assertion groups passed with zero failures in under two seconds. These are finite COMPUTATIONAL facts, not FLMV traces.

## Exact remaining implication

OPEN: under hypothetical P=NP and its fixed polynomial SAT machine `A`, construct one fixed total deterministic `A`-dependent normalizer on every ordinary input—or on every member of one fixed locally indexed FLMV-hard image—with an explicit closed named stream satisfying

`max(r,mu+delta) < 241/200`,

`max(eta,delta) < 11642479/23232400`.

Charge source reads, recognition, failed rules, every `A` call, output events, malformed inputs and all retained state. No verified artifact supplies this normalizer.
