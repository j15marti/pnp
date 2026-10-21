# 10:48 synthesis handoff — RP-DENSITY-HITTING-TRADEOFF38

Both open questions remain OPEN. New exact theorem: for `m` YES inputs and
accepting-tape density at least `a/q`, a verifier-and-length-specific hitting
list of `t` tapes exists whenever `m(q-a)^t<q^t`. Thus density `1/2` and
`m<=2^n` needs `n+1` tapes; inverse-polynomial one-sided density gives
polynomial advice, while density `2^-n` remains exponential. This proves only
`RP subseteq P/poly`, not uniform `P=RP`.

Fixed-list validity is in coNP because invalidity has witness `(x,rho)`; prefix
extension has a `Sigma_2`-type quantifier pattern. A uniform list constructor
would derandomize the verifier, but P=RP need not construct a list for each
chosen verifier because deterministic simulation may bypass it.

Audit: 34,845 exhaustive four-tape families, 25,000 seeded eight-tape
families, 154,584 assertions, zero failures.

PNP: DIGEST-GATE17 retires fixed short keys as high-KT generators. ARC eager
materialization remains a resource interface without an all-input semantic
successor. P-vs-NP remains OPEN.

Next :00 growing-state KT ledger; :24 eager semantic child plus matched gluing
counterexamples; :12 uniform inverse-polynomial-density RP diagonal language
without deterministic bypass; :36 exact prefix-extension oracle ledger.

