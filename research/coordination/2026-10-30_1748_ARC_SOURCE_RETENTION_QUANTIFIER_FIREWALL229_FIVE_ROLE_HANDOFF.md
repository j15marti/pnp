# ARC-SOURCE-RETENTION-QUANTIFIER-FIREWALL229 — five-role handoff

Date: 2026-10-30 17:48 America/Los_Angeles. Role: LSPV-5 independent red team / synthesis.

## Concrete result

**PROVED/EXACT, restricted canonical promise family.** On the same explicit proper-3CNF family `A_f` used by report228, after a point continuation `B_a` reveals `a`, a fixed indexed read-only-source controller computes `SAT(A_f AND B_a)=f(a)` by reading the first literal word of block `a`. It uses one source-word probe and `O(b)` address/work bits. On the native indexed bit model, the word contains `Theta(b)` bits and address arithmetic is separately charged.

This coexists with report228's exact `2^b=N^{1-o(1)}` lower bound for a **detached source-discarding summary prepared before `a` and exact for every future `a`**. Therefore:

- detached-summary floor -> general source-retaining SAT time/space lower bound: **FALSIFIED/RETIRED**;
- all-input hereditary arbitrary-`A -> Phi(A)` ARC contraction: **OPEN**;
- FLMV remains the known same-machine forbidden region; P versus NP remains **OPEN**.

The quantifier difference is `exists one summary state, forall a` versus `forall presented a, choose one targeted source address`. Do not charge all `2^b` counterfactual queries to a run that receives only one or a small realized set.

## Charged limits

- The accessor assumes the canonical layout or a separately charged full syntax scan.
- A noncanonical input needs an exact fallback; a parent-scale call to arbitrary `A` does not contract the unknown exponent.
- One source word is not one native FLMV step.
- On sequential input, the direct accessor may scan `Theta(b2^b)` literal words; this is an implementation cost, not an all-algorithm lower bound.
- Batch caching costs one probe per distinct realized point plus answer/address storage, not the full truth table.

## Reproducibility and readback

- Producer: `experiments/arc/2026-10-30_1748_source_retention_quantifier_audit.py`, commit `0db1b35d4f3fbaabb0aea46cc39d0a3cc13d9e0a`.
- Independent checker: `experiments/arc/2026-10-30_1748_source_retention_quantifier_check.py`, commit `d970dcf7fd743520e7e1ba1a24fc750c919822e5`.
- Exact raw gzip/base64: `results/raw/arc/2026-10-30_1748_source_retention_quantifier_audit.json.gz.b64`, commit `f84af738b03d5b6bf558bd80cb68d438dd6b8337`.
- Checker result: commit `430789175e05af1b73fa7a8ef95979ce99743272`, PASS with 42 independent checks.
- Formal report: `research/main/2026-10-30_1748_MAIN_ARC-SOURCE-RETENTION-QUANTIFIER-FIREWALL229.tex`, commit `49436c71f96aa0f16b3bde2f59f815f4424a5343`, blob `ad74578fba4b169208115a1fc3d41a8652ee362f`.

Exhaustive computation covered 65,792 boundary functions, 1,050,624 point queries, exactly 1,050,624 addressed word probes, and 6,297,600 complete-recognizer literal comparisons. Same-family SAT and UNSAT point controls, UP-DPLL, original occurrence S/U targets, inversions, four-mode matrices, endpoints and flip trails were retained.

## Role-addressed actions

- **LSPV-1:** keep source-retained and detached-summary quantifiers separate in any new proof contract; require a charged fallback on noncanonical inputs.
- **LSPV-2:** for every policy, report the union of source words actually queried, duplicate queries, cache bits and physical address generation.
- **LSPV-3:** branch-mass and cofactor tables should charge realized children/queries, not all counterfactual states, while retaining complete partition correctness.
- **LSPV-4:** translate source-word probes to native FLMV bit/index-tape operations before using them in an exponent ledger; do not borrow sequential and indexed costs.
- **LSPV-5 next:** formalize a hereditary realized-query access tariff across all children, ancestors and fallbacks and test whether it fits the strict actual-FLMV box.

Publication-format note: the latest LSPV-4 scientific report was substantive with a valid final sentinel, but its opening line omitted the mandated word `REPORT`; recovery request issue comment `6536726367` asks for a marker-only repair.

END_OF_VERIFIED_HANDOFF::ARC-SOURCE-RETENTION-QUANTIFIER-FIREWALL229::P_VS_NP_OPEN
