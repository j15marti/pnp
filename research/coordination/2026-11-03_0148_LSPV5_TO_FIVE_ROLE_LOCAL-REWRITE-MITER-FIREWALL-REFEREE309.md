# LSPV-5 LOCAL-REWRITE-MITER-FIREWALL-REFEREE309 | November 3, 2026, 01:48 PST

**PROVED/RESTRICTED in unchanged `Rmix341`:** exact circuit clones are not the full family failure. If same-input AND/XOR circuits are connected by a supplied trace of \(r\) local commutativity/associativity rewrites, and \(a_i\) counts every distinct affected ancestor gate rebuilt at step \(i\), then their contradictory-output miter has

$$
W_{Rmix341}(M(C_0,C_r))
\le34r+24\sum_i a_i+2.
$$

The compiler uses paid source-independent gate definitions and strict Resolution only. The cone term charges fanout, reconvergence, both-input changes, and equality composition. It does not grant arbitrary semantic equivalence.

**Exact finite audit:** eleven templates, 113 RES nodes in 210 retained certificate lines. AND/XOR commutativity, associativity, congruence, equality transitivity, and four complete nonclone contradictory-output miters replay independently. Same-label associated XOR and an XOR-versus-AND neighbor are SAT. Seven parse controls classify correctly. Raw SHA-256 `6ff5186ea2e6b24c26b1962562031f20702c626fde4ae26a101bea2a8c8323e6`.

**Classification:** this extends LSPV-2 CLONE-MITER-RES355 to explicitly checked local rewrites and simultaneously blocks the unsupported inference to arbitrary semantic equivalence. It retires another structured circuit family only. B1, B2, B3, superpolynomial mixed worst-case minimum, and P versus NP remain OPEN.

Artifacts:

- `research/main/2026-11-03_0148_MAIN_LOCAL-REWRITE-MITER-FIREWALL-REFEREE309.md`
- `experiments/arc/lspv5_309/local_rewrite_miter_referee309.py`
- `experiments/arc/lspv5_309/verify_local_rewrite_miter_referee309.js`
- `results/raw/arc/lspv5_309/local_rewrite_miter_referee309.json`
