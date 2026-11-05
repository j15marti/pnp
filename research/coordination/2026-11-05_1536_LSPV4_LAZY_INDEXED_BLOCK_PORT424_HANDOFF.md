# LSPV-4/424 five-role handoff | 2026-11-05 15:36 PST

**Route A, PROVED/RESTRICTED + COMPUTATIONAL; arbitrary-decider all-input FLMV contraction OPEN.**

The earlier general lazy-source bit-simulation idea is present in LSPV-1/147, not new. This run supplies an exact original-source indexed-reader construction and independent physical-operation proxies on a syntactically recognized family of *ordinary strict 3CNF*. Under an already certified source-to-child decomposition with q<=N^(a+o(1)), child lengths L<=N^(lambda+o(1)), fully charged local time N^(d+o(1)), live phase/ancestor exponents rho,eta, and uniform polylog-indexed child-bit access on the immutable original, a fixed arbitrary FLMV indexed guest A with time exponent t and space exponent s has conditional envelope

$$
t'\le\max\{d,a+\lambda t\},\qquad
s'\le\max\{\rho,\eta,\lambda s\}.
$$

Guest arbitrary indexed input jumps, source head/index-digit writes, index erasures, reconstruction on every access, guest control, output and simultaneous memory are charged. Materialized children instead add the lambda peak-space exponent. This proves the *port simulation component*, not the existence of an all-input splitting policy.

Concrete control: h source-contiguous disjoint cubic graph Tseitin components, 4h proper 3-clauses per component, disjoint edge-variable ranges, all charges even (SAT) or at least one odd (UNSAT). Entire block class, even non-Tseitin formulas, is correctly decided by AND of independently evaluated component SAT labels. Elias-gamma canonical source N=H_p+12h^2(w+1), q=h, L=H_c+12h(w+1), H_p,H_c=O(logh). Child body bit j is the original bit at H_p+i*12h(w+1)+(j-H_c). Local validation is O(N polylogN) time, O(logN) scratch. K4/cube/Petersen both-label and malformed/out-of-class controls: Python **58,869** checks; independent JS **58,765** assertions, nine source controls. Distinguish host operation counters from native FLMV time.

A hard odd-charge cubic-expander component preserves its exponential **ordinary Resolution only** lower bound in disjoint union by assignment restriction of other SAT components; mixed GF(2) shortcut remains linear. Source hard-family evidence is not general SAT algorithm hardness.

**Decisive failed property:** every emitted child has 4h clauses, not 4h², so the supported block grammar is **not hereditary**. No universal all-input, recursively iterable A->Phi(A) theorem; no unchanged-guest fallback permitted. The next obligation for Route A is to construct a genuinely general, source-authenticated, recursively iterable child family with inexpensive locally addressable bits and legal AND/OR composition, then audit all machine operations.

Published report: research/agents/lspv-4/2026-11-05_1536_LSPV-4_LAZY_INDEXED_BLOCK_PORT424.md. Compact executable: experiments/arc/lspv4_424_lazy_port.mjs. Raw summary: results/raw/arc/2026-11-05_1536_LSPV4_424_LAZY_PORT_summary.json. Expanded independently rerun Python+JS producer and logs: conversation reproducibility ZIP. Root main.tex **not edited** because exact retrieval returned empty content with a valid SHA. No changes to five task identities, schedules, enabled states, R_mix341 grammar/weights, or other roles' work. Route B and P versus NP OPEN.
