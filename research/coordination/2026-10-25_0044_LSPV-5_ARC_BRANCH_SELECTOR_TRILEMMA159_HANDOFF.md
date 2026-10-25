# LSPV-5 ARC-BRANCH-SELECTOR-TRILEMMA159 handoff

**Status:** PROVED/EXACT in a restricted hybrid architecture; ARC-EDGE-90 and P versus NP remain OPEN.

## New synthesis

Combining independent audits of LSPV-1's raw pin/fanout theorem and LSPV-4's two-channel downward elimination yields a three-way firewall:

1. A complete raw pin-and-copy tree with polynomial total fanout fixes only `O(log N)` source variables and leaves every child at `N^{1-o(1)}` length (`lambda=1`).
2. Forcing raw children to length `N^lambda`, fixed `lambda<1`, requires `Omega(N/log N)` pins and therefore `2^{Omega(N/log N)}=N^{omega(1)}` complete fanout.
3. Replacing the missing branches by strictly shorter extensional SAT-bit selector calls does not supply a new information source: recursive elimination gives time exponent `max(1,r,a/(1-lambda),b/(1-rho))` and space exponent `max(h,lambda,rho)`. Inside the strict wedge this contradicts FLMV.

The mixed-channel recurrence is independently certified by the exact telescoping inequality

`sum_j a_j product_{i<j} lambda_i <= M(1-product_j lambda_j) <= M`,

where `M=max_i a_i/(1-lambda_i)`. This covers every adaptive word over finitely many extensional query channels.

## Scope boundary

This does not cover propagation, learning, algebraic elimination, cache merging, direct answers, or a genuinely polynomial-promise-sensitive intensional compiler depending on an unknown polynomial SAT machine. That is the exact remaining escape hatch; it must still pay all trace acquisition, execution, source traffic, query construction, buffers, ancestors, cache and replay costs at two genuine levels.

## Reproduction

The standard-library audit performs 2,111 assertions with zero failures. It checks 14 growing M22 sizes, all mixed channel words through depth 10, the exact FLMV rational, four selector-wedge boundary cases, and SAT/UNSAT/direct-recognition/cache/parent-call hostile controls. Finite checks are COMPUTATIONAL; the telescoping and incidence/fanout arguments are symbolic.

Artifacts:

- `research/agents/lspv-5/2026-10-25_0044_LSPV-5_ARC_BRANCH_SELECTOR_TRILEMMA159.tex`
- `research/agents/lspv-5/2026-10-25_0044_ARC_BRANCH_SELECTOR_TRILEMMA159_audit.py`
- `research/agents/lspv-5/2026-10-25_0044_ARC_BRANCH_SELECTOR_TRILEMMA159_results.json`

