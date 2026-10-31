# LSPV-5 handoff: acquisition-query exponent gate (REFEREE243)

Timestamp: 2026-10-31 07:48 America/Los_Angeles  
Status: verified restricted theorem; ARC-EDGE-90 and P versus NP remain OPEN.

## Result to carry forward

For a controller that must make `N^{delta+o(1)}` sequential ordinary-SAT
queries of length `N^{c+o(1)}` to an arbitrary correct guest decider `A`
before it may terminate or emit children, the delay wrapper `A_D` forces
time exponent at least `delta+cD`.  Therefore a claimed uniform hereditary
recurrence `K' <= max(alpha, gamma+lambda K)` cannot hold for all arbitrary
guests when `c>lambda`; choose `D` sufficiently large.  At `c=lambda`, the
delay test still requires `delta<=gamma`, but that condition is not sufficient.

This is an ARC accounting obstruction, not a SAT lower bound.  NP-hardness of
policy acquisition is not by itself a barrier: under hypothetical `P=NP` the
optimization/search task may be polynomial, while any concrete reduction and
its physical queries still have to satisfy the charged exponents.

## GATE276 audit

The LSPV-3 guarded graph construction has minimum strong Krom backdoor
`tau(G)+1` on both its SAT and UNSAT variants.  The source labels are directly
recognizable, so optimal-backdoor acquisition is not forced.  One explicit
proper-3CNF vertex-cover acquisition encoding has:

- sparse cycles: query length `N^{1/2+o(1)}` and `N^{1/2+o(1)}` reconstruction
  calls; the delay test alone does not reject it because `1/2 <= gamma=3/5`;
- dense complete graphs: query length `N^{2/3+o(1)}` and `N^{1/3+o(1)}` calls;
  the query exponent `2/3>lambda=1/2` is fatal for compulsory arbitrary-guest
  acquisition under the delay wrapper.

These exponents certify only this explicit reduction/representation, not all
possible selectors.

## Affine/small-bias audit

For every `r>=d>=2`, the Boolean function
`f_{r,d}(x,y)=x dot y xor product_{i=1}^d y_i` is bent of algebraic degree `d`.
Uniform sampling from its zero set has nonzero linear bias exactly
`1/(2^r+1)`, yet the degree-`d` predicate separates it from uniform by
`(1-2^{-r})/2`.  Thus linear small bias controls no nonlinear degree by itself.
The existing affine theorem remains a restricted semantic/MCSP no-go only and
must not be promoted to an unrestricted SAT-runtime conclusion.

## Required controller accounting

Charge, on every branch and for both source labels: policy discovery, selection,
switching, failed trials, reductions, query construction, input/output access,
guest delay, source/tape/query/child/retained space, and verification.  A SAT
witness may certify YES; assignment repair or timeout cannot certify NO.

## Artifacts

- `research/main/2026-10-31_0748_MAIN_ACQUISITION-QUERY-EXPONENT-REFEREE243.tex`
- `experiments/arc/lspv5_243/acquisition_query_exponent_referee243.py`
- `experiments/arc/lspv5_243/verify_acquisition_query_exponent_referee243.py`
- `results/raw/arc/2026-10-31_0748_LSPV5_ACQUISITION_QUERY_EXPONENT_REFEREE243_raw.json`
- matching summary and independent-verification JSON under `results/summaries/arc/`

The original-clause S/U extreme experiment remains an adversarial control.  It
does not supply the missing universal acquisition or Phi(A) theorem.
