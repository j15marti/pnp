# BACKDOOR-PRODUCT-FIREWALL97 handoff

**Status:** PROVED/EXACT restricted statements; COMPUTATIONAL audit; unrestricted deterministic SAT lower bound OPEN; P versus NP OPEN.

## New exact counterexample

Take `p` variable-disjoint copies of Role 4's `H_{q,sigma}`. The product has

- `n=p(q+4)` source variables,
- `m=k=p(2q+4)` proper ternary clauses,
- minimum strong syntactic 2-CNF backdoor `h=p`, exactly,
- `16^p` models iff all component orientation parities are even, and zero otherwise,
- uniform charged exact decision in `O(pq)` word operations by recognized component parity scan.

With fixed `q=3`, `h=n/7=Theta(N/log N)` but exact family decision is input-linear. Therefore minimum strong-2CNF backdoor size, even when linear, is not an arbitrary-decider lower-bound measure. This retires amplification from clause count, clause criticality, or disjoint products.

## All-decider and transport ledgers

On an all-even product, every one of the `pq` disjoint orientation flips changes the label. POINTWISE-DIFFERENTIAL64 forces `pq=Omega(N/log N)` input-word observations, matched by the scan. For any explicit materializing chain-to-product reduction, record writes alone satisfy `R>=p(2q+4)>L_old=pq`; the positive-remainder transport numerator is already negative. Direct inclusion preserves, but does not amplify, the input-order query bound.

## Reproduction

- Full report: `research/main/2026-10-23_1948_MAIN_BACKDOOR_PRODUCT_FIREWALL97.tex`
- Audit: `experiments/review/backdoor_product_firewall97_audit.py`
- Raw: `results/raw/review/BACKDOOR_PRODUCT_FIREWALL97_raw.json`
- Finite result: 285 assertion groups, 127,488 exhaustive assignments, 14 deletion checks, zero failures.

## Role routing

- **Roles 1–3:** do not use ternary count `k`, minimum 2-CNF backdoor `h`, or independent-product amplification as the residual parameter. Any compression-versus-continuation candidate must reject or quotient this easy family without circularly calling SAT.
- **Role 4:** the one-switch construction is independently validated and strengthened to a linear-backdoor hostile family; seek a genuinely nonseparable rung, not another disjoint product.
- **Role 5:** maintain exact transport margins; direct inclusion gives only input-order coverage.

## Single next missing lemma

Define a non-product semantic obstruction `r(F)` independently of runtime and prove an all-decider charged acquisition-or-continuation inequality `T_A(F) >= 2^{Omega(r(F))}/N^{O(1)}`, with `r(F)/log N` unbounded, surviving 2-SAT, affine/Horn, backdoors, separators, learned constraints, caching, source-aware recognition and decide-first normalization. This remains OPEN.

