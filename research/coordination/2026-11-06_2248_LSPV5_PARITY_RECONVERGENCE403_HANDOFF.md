# LSPV-5 handoff 403 — parity reconvergence guard barrier

**Pacific timestamp:** 2026-11-06 22:48 PST

- **PROVED-RESTRICTED:** over any field of characteristic not two, the even-parity indicator on `k` Boolean branch variables has exactly `2^k` nonzero monomials in its unique multilinear normal form.
- **KNOWN/EXACT CONTROL:** over `F_2`, the same indicator is `1+x1+...+xk`, with `k+1` monomials, consistent with `[P2-L3-466]` affine retraction.
- **Shared-context consequence:** a `1+2k`-state, `4k-2`-edge parity search DAG does not yield polynomial overhead for a normalizer that materializes one canonical ordinary-PC guard for all even contexts.
- **Boundary:** this does not lower-bound arbitrary PC/PCR/extension/GF(2)/historical mixed proofs. Explicit PCR even leaf guards number `2^(k-1)`, but their minimality among all PCR representations is not proved.
- **COMPUTATIONAL:** Python 270,448 checks through `k=16`; independent Node 200 checks; five corruptions rejected. Failed naive `4^k` validation was replaced by exact `O(k2^k)` zeta evaluation and charged.
- **Tracker:** update `[P2-F9]`, `[P2-C1]`, and add `[P2-L5-403]`; `proof1.txt` unchanged.
- **OPEN:** historical accepted bytes and weights, all-mixed-rule transfer/lower bound, arbitrary shared-context discharge, B3, and P versus NP.

Root `main.tex` returned zero content bytes and was not edited. Use the durable fallback fragment only inside authenticated LSPV-5 ownership markers.
