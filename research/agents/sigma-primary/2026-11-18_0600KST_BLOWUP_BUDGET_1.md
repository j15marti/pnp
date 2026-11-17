# BLOWUP-BUDGET-1 | 2026-11-18 06:00 KST
Circuit-SAT / Sigma2 / Sigma3. **P versus NP OPEN.** **Status: PROVED/EXACT model-scoped accounting lemmas; COMPUTATIONAL finite checks; arbitrary all-input hereditary A -> Phi(A) OPEN.**

## Mechanisms proposed before search
1. Source-to-promise padding cost measured on original unpadded n-bit SAT input.
2. Delay-padded SAT decider and saturated guest-call exponent slope.
3. Charged virtual child input-index/source-replay overhead.
4. Added semantic-validation call budget against FLMV Corollary 5.8.

## Project and literature checked
Read `research/agents/sigma-primary/2026-11-18_0501KST_AUTOENC_SIGMA3_1.md`, its handoff, `research/agents/sigma-redteam/2026-11-18_0538KST_SIGMA19_CLIQUE_PORT_FIREWALL.md`, and `research/review/spines/2026-10-21_CONTRACTION_ACQUISITION1.md`. Also reviewed TMR-2's five-symbol CSP cofactor audit. Primary: FLMV, JACM 2005, Cor. 5.8 https://doi.org/10.1145/1101821.1101822 (the published PDF page 18 was visually checked); Williams, STOC 2024 https://doi.org/10.1145/3618260.3649723; Reichl et al., SAT 2024 https://doi.org/10.4230/LIPICS.SAT.2024.23; Charwat et al. 2019 https://doi.org/10.3233/FI-2019-1810.

## Theorem 1: charged source-expansion firewall, literal saturated-call architecture
Assume P=NP and let B be any correct fixed polynomial Circuit-SAT decider. For arbitrarily large integer D above the base exponent, form correct A_D by executing B plus Theta(m^D) dummy work on every m-bit guest input. Let a literal architecture on some family of original n-byte inputs create a promised source of size N=n^{alpha+o(1)}, then execute at least N^{a-o(1)} calls each of guest length at least N^{lambda-o(1)}; do not optimize away these calls. On the ORIGINAL input its charged running time is at least n^{alpha(a+lambda D)-o(1)}.

To meet requested H(D)=max(11/10,3/5+D/2)=3/5+D/2 for all arbitrarily large fixed D, necessarily alpha*lambda<=1/2; if alpha*lambda=1/2, also alpha*a<=3/5. Compare slopes and intercepts. For a purely algebraic certificate for every real D>=1, alpha*lambda<=1/2 and alpha*(a+lambda)<=11/10 are necessary and sufficient for this one guest-term inequality; local and space costs must additionally be charged.

**Application:** the latest AUTOENC promise evaluator has a=29/50, lambda=1/2, r=27/25, hence its saturated guest term after an n -> n^alpha source conversion is n^{alpha(29/50+D/2)}. Any fixed alpha>1 violates the target for sufficiently large D, even alpha=1.001. Alpha=1.01 first fails between D=2 and 3 (threshold D=2.84); alpha=1.001 first fails between D=38 and 39 (threshold 38.84). This blocks padding-based *literal-call transfer*, not code-aware transformations which bypass padding or the guest.

An actual forced guest call of length n^{nu} by itself requires nu<=1/2 for uniformly unbounded D. A fast source-only algorithm cannot use a 0.51-exponent guest query and charge it as 0.50 by relabeling the original input.

## Theorem 2: virtual-child lookup and validation-call headroom
For N^a guest calls to A on N^lambda-bit inputs, an indexed virtual child which charges N^tau extra per guest step has conservative total guest time N^{a+tau+lambda K}; this is a **conditional upper ledger**, not a general virtual-input lower bound. With a=29/50, lambda=1/2, alpha=1, the target permits tau<=1/50. Naively replaying the entire N-bit source for each virtual guest access gives tau=1 and fails. Explicit materialization avoids that replay but charges an N^{1/2} child buffer.

If an as-yet-unproved all-input hereditary same-machine compiler additionally makes n^{delta+o(1)} validation calls of size n^{1/2+o(1)}, its exponent maps would be
```
K' <= max(27/25,29/50+K/2,delta+K/2)
L' <= max(1/2,L/2)
```
with fixed point (c(delta),1/2), c(delta)=max(27/25,29/25,2delta). The FLMV Cor.5.8 sufficient forbidden boundary is beta(c)=((c+2)/c^2-c)/2. Strict beta(c)>1/2 iff c is below the positive real root c_* of c^3+c^2-c-2=0, with 1.205569<c_*<1.205570. Thus a **conditional** validation-query budget is delta<c_*/2 approximately 0.602784715. At delta=3/5, c=6/5, margin beta(c)-1/2=1/90>0. At delta=0.603, c=1.206 and this corollary no longer forces contradiction. No all-input hereditary compiler or same-machine transfer has been built.

The original promise-only AUTOENC map has algebraic fixed point 29/25, not 6/5; it is a strict exponent improvement only when K>29/25. It cannot be recursively applied to arbitrary ordinary Circuit-SAT children on the present evidence.

## Exact finite falsification
Standard-library Python `test_budget.py` executed 1,000 seeded independent three-block exact QBF truth-table comparisons, adversarial global-x/locally adaptive-b/shared-b and reconvergence checks, a disjoint-private-variable failure control, exact Fraction alpha-vs-D comparisons and FLMV root-bracket assertions. **1,087 assertions, zero failures.** Raw and full report are in the local bundle SHA-256 manifest:
- test_budget.py: 7d23c453d091df5c5e8cf9f3ebdab05c72f72d88fede30270e43f1c309104f0f
- raw.json: 9ef967def333c369db5188a313cd77907579149896d60a56572d10a46283b9c5
- REPORT.md: 1311e2f93540a924f01a30819894fa29c665fb3c183dcf20338238c682e1bde3
All finite tests are COMPUTATIONAL, not SAT lower bounds.

## Handoff
Next: demand a real ordinary-Circuit-SAT-to-S3C converter with alpha=1+o(1), half-size fully accessible ordinary Circuit-SAT guests, source/bit-index costs charged, exact quantified dependencies, and hereditary children. Stress-test one-port hidden SAT/UNSAT, high-boundary nonaffine incidence, five-symbol CSP, padded code and reconvergence. Cross-reference but do not edit TMR-owned manuscripts, root proof trackers or agent schedules. The existing source-tagged promise evaluator is not an all-input SAT algorithm. **P versus NP OPEN.**

FINAL_VERIFICATION_SENTINEL_BLOWUP_BUDGET_1_20261118_0600KST
