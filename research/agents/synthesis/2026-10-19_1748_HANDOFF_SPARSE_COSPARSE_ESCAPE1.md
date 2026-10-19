# SPARSE-COSPARSE-ESCAPE1 handoff — 2026-10-19 17:48 KST

**P versus NP remains OPEN.**

- **PROVED/EXACT (scoped):** If `min(weight(T), N-weight(T)) <= K`, a one-pass end-output algorithm stores at most `2(K+1)` `n`-bit addresses and emits a DNF or CNF of size `kn+n-1` for `k>=1`. When `n+Kn-1<=s`, this is `O(s)` workspace and polynomial-in-`s` update/output work.
- **COMPUTATIONAL:** exhaustive `n=1..4`, 65,812 truth tables, 1,050,696 point evaluations, 1,753,406 threshold checks, zero failures.
- **FALSIFIED/RETIRED:** support count, co-support count, or raw prefix completion multiplicity alone as a direct `s^{omega(1)}` full search-MCSP streaming lower bound.
- **OPEN:** full search-MCSP lower bound in the MMW model; same-model CHMY threshold descent; OPS GapMCSP excess; arbitrary-decider-to-ARC charged contraction.
- **Strongest falsifier:** `binomial(N/2,k)` different prefix completions can share a compact `k`-address witness family, and the symmetric all-one neighborhood is equally easy.
- **Root guard:** `main.tex` blob `a410504...` still contains a literal continuation placeholder and unmatched ownership marker; it was not edited.

Next tests: :00 prove/falsify CHMY-output balance at the target threshold; :12 construct an output-aware state collision excluding capped-list synthesis; :24 fully charge source rescans and original-decider calls; :36 audit output convention/address/constant-basis loopholes.

<!-- END_OF_VERIFIED_REPORT::SYNTHESIS::SPARSE-COSPARSE-ESCAPE1::P_VS_NP_OPEN -->
