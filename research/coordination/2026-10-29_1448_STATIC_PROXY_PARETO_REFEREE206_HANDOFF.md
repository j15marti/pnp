# LSPV-5 handoff — STATIC-PROXY-PARETO-REFEREE206

Status: **PROVED/EXACT (restricted proxy geometry and controller accounting)**; **FALSIFIED/RETIRED** for the mandatory-table-space and free-envelope interpretations; finite controls **COMPUTATIONAL**; general SAT time-space frontier and P vs NP **OPEN**.

## Exact corrections

For the relaxed permitted proxy

`q(b)=max(0,n/(12b)-1/4)`, `t(b)=b+q(b)`, `s(b)=b`,

the active branch is strictly convex:

- `t'(b)=1-n/(12b^2)`;
- `t''(b)=n/(6b^3)>0`;
- `b*=sqrt(n/12)`;
- `t(b*)=sqrt(n/3)-1/4`;
- first permitted log-proxy equality: `b=n/3`, `q=0`.

For `n=1200`, integer time exponent 20 occurs at `b=9,10,11`, but only `b=9` is Pareto-nondominated. The first equality point `(400,400)` is dominated by `(20,9)`.

## Falsifier

`S_proxy=2^b poly(N)` is the space cost of storing a reusable boundary table. A one-shot exhaustive evaluator can stream the same `2^(b+q)` assignments in `O(N+b+q)` live bits. Therefore the plotted equality does not imply equality of measured machine time and space.

## Realizability fork

Under the residual-hitting convention, the `q=0,n=3b` endpoint is realized for every `b>=3` by a connected 4-regular private circulant whose `4b` edges become clauses with one of `b` boundary variables. If `B_i` is instead required to hit boundary-touching clauses itself, `q=0` is excluded. Reports must state the convention.

## Adaptive controller theorem

- Sequential certified attempts: `T <= D+sum T_j`, `S <= S_D+max S_j`.
- Dovetail with retained states: `T <= D+m min_{solving j} T_j`, `S <= S_D+sum S_j`.

The coordinatewise ideal envelope `(min T_j,min S_j)` is not generally jointly achievable.

## Peer red-team

- ARC230 validly makes the supplied width-three, rank-one star class NP-complete; maximum edge width/local rank alone is not a tractability parameter.
- MATCHED-TORUS-BRIDGE232 supplies growing-width opposite labels but a P promise recognizer, so width is not a runtime lower bound.
- BRANCHING-EXACT22-GRAFT167 supplies a real bounded-bag two-answer polynomial family; bounded bags and authenticated grammar—not binary adhesion alone—drive the upper bound.
- No newer LSPV-4 artifact than HYBRID-BAD-MESSAGE228 was present; preserve/retry the missing body if it exists.

## Root recovery

Current remote `main.tex` blob `dd3e5f4d34b316101ef88884674631ba28f18772` is a truncated surrogate with no ownership markers. Recover from verified full run205 blob `826ffc0bbe40603f6ed5916c413cbb2ef169f591`, then add verified standalone peer results. Do not reconstruct omitted text.

## Next lemma

Build a realizable two-answer strict22 family with two competing algorithms, measure simultaneous `(T,S)` pairs on one declared machine, and prove a charged controller envelope including all failed methods, joins, source access, reconstruction, and peak live state.
