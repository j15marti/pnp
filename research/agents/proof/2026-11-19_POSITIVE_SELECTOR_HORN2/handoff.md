# POSITIVE-SELECTOR-HORN2 handoff

19 November 2026, Asia/Seoul. Assignment: positive restricted selector lemmas. P versus NP OPEN; external independent mathematical review pending.

PROVED/EXACT restricted: extend SUPPORT-SELECTOR1 to a sound three-valued backend with discovered strong Horn backdoors. NO completeness needs only one UNSAT residual of backdoor size <=d per shared row; remaining blocks may be arbitrary. YES completeness needs one row whose every block is SAT with such a backdoor. Failed recognition is UNKNOWN. Source blocks are explicitly delimited, private IDs have authenticated owner tags, and all shared assignments are traversed.

Same-execution bounds:
T=Otilde(N+2^d sum_i 2^{r_i} ell_i+BR);
S=Otilde(ell_max+R+d).
At R<=N^.195, B<=N^.65, ell_max<=N^.35 and d<=.135 log_2 N, this realizes T<=N^{1.33+o(1)}, S<=N^{.35+o(1)} on the promises, with discovery, failed branches, all Horn children, output and replay paid. A generic polynomial SAT seed is unnecessary here and does not establish an arbitrary-CNF compiler.

Correct-path distinction: d bits can identify a backdoor through deterministic violating-pair choices. YES supplies one satisfying backdoor assignment per block; NO must still verify every backdoor assignment of the chosen refuting block for every row. Whole path versus whole strategy, certificate rereads, rejected output prefixes and deterministic enumeration are explicitly distinguished in the report.

COMPUTATIONAL: 3,304 small formulas, 9,912 budget checks, 23,128 paths, 360 layouts (212 SAT / 40 UNSAT / 108 UNKNOWN), 3,552 residual calls, 4,320 row visits. T5 H9: all 11 deletions have full witnesses; all rotations passed 550 original-arc checks. One-hot Horn backdoor size 36 coexists with these cheap fixed witnesses. Functional reference code; no measured RAM memory claim.

Published to main and fully read back:
- report: research/agents/proof/2026-11-19_POSITIVE_SELECTOR_HORN2/report.md
  commit 377cacdaa6de4a3c209dda1b7a8a2f89aa22de18; blob 0a2af364629c84b6ca0972d6dad39a964b186f25.
- code: experiments/selectors/2026-11-19_positive_selector_horn2.py
  commit 04d64b0ba0960ea6ac9ee2454052eaacee78cc99; blob 72491c967a8b2a3e12f88d8a862483990e67bf9e.
  SHA256 4d48332d741668b71bab7de4915c315790d29dc302effcd4d59c24e5b69ad8b1.
- raw: results/raw/2026-11-19_positive_selector_horn2.json
  commit 9d1eb9a531a74319b5d66cb5778bebf3b16ce9aa; blob 22c375792a9d7a5824277047304b22ab8e1c2f96.

Literature ledger: all-CNF deterministic (1.33,.5) is excluded by Buss--Williams's (1.34070,.5) point. NO nondeterminism has the DVMW cube-root-four/some-positive-space exclusion and the explicit FLMV (1.10,.5) calibration; neither licenses the same (1.33,.5) assertion for nondeterministic SAT. LOCAL4's corrected polarity attribution is preserved.

Next blocker: obtain a uniformly discoverable refuting cover beyond the syntactic class while preserving actual source size, access and hereditary child budgets. Restriction closure at fixed absolute d is insufficient for d<=.135 log(child length).

No TMR manuscript is assigned to this role; publication is additive. No local checkout preflight or LaTeX build. Targeted corpus review, not full peer-manuscript/branch audit. No title, owner, schedule, or enabled/paused-state changes. Issue #3's known comment-limit block was not retried.
