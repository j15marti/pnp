# Proof review status

Updated: 2026-10-10. **P versus NP remains OPEN.**

The first scheduled builder cycle is synthesized in `PROOFMAP-0002`. No all-input SAT successor, arbitrary-algorithm lower bound, or bounded-list PFCERT verifier was constructed.

## Current route ranking

1. **Strict successor / charged wrapper — CONDITIONAL.** Composition is exact under one uniform all-input contract. The SAT-specific ordinary-CNF successor, descendant closure, access, and same-machine resources remain OPEN.
2. **Bounded-list PFCERT — CONDITIONAL.** Counting and time-bounded Kolmogorov immunity are exact at the endpoint. Verifier existence and executable acquisition remain OPEN.
3. **LSPV Boolean separator — OPEN.** Representation and scoped source-probe results exist; arbitrary-SAT extraction, reconstruction, and the nonrelativizing hinge do not.
4. **ARC15 / finite portfolios — COMPUTATIONAL.** Finite positive coverage does not close UNSAT/fallback or establish an all-input joint resource bound.

## New cycle-one results

- LOWER_BOUND LB-0002 proves a tight `Theta(r)` source-probe floor for self-contained source-free exact transporters on its switch family. It relativizes and is not an unrestricted SAT lower bound.
- COST_CERTIFICATES CC-0002 proves exact witness-string counting, a scoped bounded-list diagonal, semantic hash factorization, and collision-entropy identities.
- One CC-0002 corollary is corrected: its displayed per-candidate-copy bound has exponent `kappa+max(v,1)` when `|p|=O(N)`, not unconditionally `v+kappa`. Recovering `v+kappa` for `v<1` requires a separate shared-read-only-input random-access implementation.
- The newest complete REDTEAM artifact predates these two builder deltas, so independent red-team review remains pending.

## Highest-value next links

- MODEL_BRIDGE: one solver-independent all-input ordinary-CNF successor with strict shrink and descendant closure.
- LOWER_BOUND: an arbitrary-decider acquisition lower bound, or a matched collapsing-oracle countermodel to that extension.
- COST_CERTIFICATES: a fully charged shared-input exhaustive acquirer and corrected witness window.
- REDTEAM: claim-by-claim audit of LB-0002 and CC-0002, especially the acquisition repair.

## Reproducibility and scope

The LB-0002 and CC-0002 peer tests reproduced. A new exact-integer hostile control passed eleven sublinear-verifier and eleven linear-verifier cases and exposes the exponent mismatch. Seven additional historical Drive documents and four primary sources were reviewed. This is cumulative targeted review, not a claim that all chats, repository history, Drive files, or the full corpus have been read.

The retired universal cosine-product bound remains retired. Finite 12/13 coverage does not close the UNSAT/fallback gap. Formal LaTeX is not machine-checked unless an actual proof assistant verifies it.
