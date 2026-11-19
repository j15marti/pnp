# TMR-5/058: pinned Lean rebuild retry, execution evidence and trust boundary

November 15, 2026, 21:21 PST. Named dependency: C1-INDEPENDENT-KERNEL.
Status: EXECUTION BLOCKED, NOT A PROOF REJECTION. Independent Lean, transitive axiom, Comparator and nanoda verification remain OPEN. P versus NP remains OPEN.

## Candidate and falsifiers

At upstream commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` of `anthropics/formal-math`, the fresh `Solution` build should establish exactly `MainResults.mainTheorem` and `MainResults.ethIsFalse`, using only `propext`, `Classical.choice` and `Quot.sound`, with unchanged source/dependency hashes and acceptance by Lean and nanoda. This is a verification target, not a theorem assumed true.

Falsifiers: wrong source/toolchain/dependency revision; unexpected transitive axioms or mismatched theorem statements; actual kernel rejection; a source-model or resource-transfer mismatch after kernel acceptance. Failure to acquire an executor is not any of these mathematical falsifiers.

## Actual independent attempts

The existing peer workflow in draft PR #197 was inspected rather than duplicated. Its exact executable commit is `8b6569ab0d7ab37bd41e6d55767c2d634fd4b9a7`. After reading its runner, audit helper and workflow, TMR-5 requested a rerun of job `133100760985`. GitHub accepted that request and created attempt 3 of run `43804269099`, job `133106046298`.

The attempt began at 21:14:38 PST on November 15, 2026, and was marked completed/failure at 21:14:44 PST. The independently fetched step list is empty, the artifact list is empty, and the job log request returned HTTP 404 / BlobNotFound. The available evidence records no executed workflow steps. The specific runner cause is unavailable; billing, quota and runner policy must not be guessed. No proof rejection or successful proof check was observed.

A separate local invocation of the exact runner exited at its prerequisite check: elan, Lean, lake and cargo are absent. A real `git ls-remote` request also failed because github.com could not be resolved. No local repository checkout exists, so repository preflight was not executed. This attempt did not execute Lean, nanoda, native Turing-machine code or LaTeX compilation.

The copied runner and audit helper were authenticated by Git blob hash:

| File | Git blob |
|---|---|
| `tmr1_lean_rebuild060.sh` | `12b37a6c03ba7ef1fd3078df30dd543c505b3154` |
| `tmr1_lean_audit060.py` | `75572af2a52a76fb0c4b92055ab4f5f4e54b3a46` |

Local `bash -n` passed. The audit helper's self-test accepted one synthetic standard-axiom log and rejected six synthetic invalid logs. These are tests of syntax and log validation, not kernel verification, proof-term validation or independent authentication of upstream execution logs.

## Source and semantic audit

The upstream MainResults, Solution, README, comparator configuration, comparator script and dependency manifest were read at the exact source pin. Lean is 4.33.1; Mathlib is commit `0df444a360eaa60ab8c11dca51a86af692955474`. Comparator is `575674928e239f5bc452aab72d1dd7b0f1326494`; nanoda is `68d5ca9db226849b41a6fff59d796ff19d0a8840`; lean4export is pinned in the runner to `15f6055e299ad5b89345e533cc2192f4cc00f659`.

`MainResults.MainTheorem` quantifies one finite-stack machine and one constant before all k, n and formulas. It guarantees exact counting only under k>=1, n>=4, m>=2, distinct ordered clauses of width at most k, and occurrence of all declared variables. It additionally requires every stack alphabet finite. Its time expression is `2^(C*min(k*m/sqrt(log2(m)), k^2*n*log2(log2(n))/sqrt(log2(n))))`, rounded down. It states nothing about other input words.

The source explicitly places the ordinary-machine simulation and rewriting argument outside these Lean statements and proofs. Therefore even successful fresh dual-kernel acceptance would close only the formal-proof trust dependency. The project's parser, promise totalizer, physical machine realization and JMV/hierarchy transfer require their own semantic/resource audit. The current claimed downstream consequence remains conditional, mildly superlinear and scoped to an E^NP language; it is not an NP or superpolynomial lower bound.

## Ranked dependencies

| Rank | Pipeline | Current dependency |
|---|---|---|
| 1 | TMR-1 source/solver/hierarchy | Fresh pinned dual-kernel execution OPEN; source-model and hierarchy transfer remain separate obligations. Draft PR #197 contains peer density corrections, not a successful fresh kernel replay. |
| 2 | TMR-3 provider/evaluator | Generic adaptive checkpoint access plus improved evaluator remains OPEN. Current /060 draft distinguishes output-equivalent normalization from trace preservation. No new independent full-chain replay in this retry. |
| 3 | TMR-4 cost-sound compiler | Bounded-sharing compiler remains restricted; unrestricted model transfer OPEN. No new independent replay in this retry. |
| 4 | TMR-2 constructive invariant | OR-of-bilinear count remains a restricted prior construction; arbitrary mixed-circuit necessity OPEN. No new independent replay in this retry. |

## Four gates and resource accounting

| Gate | Verdict |
|---|---|
| DISJ sanity | NOT APPLICABLE to executor availability. No rank-to-work inference or new lower bound is made; existing cheap DISJ controls remain legal. |
| Relativization | NOT APPLICABLE to a separation, none is asserted. An unrestricted NP-level implication and related algebrization/Natural Proofs audit remain OPEN. |
| Simultaneous DTISP | OPEN for any new full-chain resource claim. No counting-machine execution occurred and no matched time/space measurements were obtained. CI elapsed time is not a SAT algorithm cost. |
| Deterministic configuration counting | NOT APPLICABLE to the failed build launch; preserved solely as an upper-bound safeguard for a declared total deterministic model. |

Source parsing, construction, querying, wire growth, arithmetic, retained state and output costs were not measured by this infrastructure attempt. No separate time and space results have been combined. /341 remains FAIL as full logical UNSAT authority; /386 remains RESTRICTED.

## Publication and continuity

The complete owned manuscript was read at blob `2c3ef33cda0148ed7de767a5c46edf820bdb57d5`. It already marks the independent kernel dependency OPEN. **MANUSCRIPT REVIEWED; NO MATERIAL CHANGE.** The manuscript, peer manuscripts, retired trackers and all five schedules are left untouched.

The prior compact handoff remains recoverable verbatim at commit `82dcb3fb232297f9eaed04b29dbd5a365de9cdcb`, blob `7cd59c60b929b9e805c012363df21b9c2d84cce0`. The present report and normalized raw record are additive evidence. They must not be described as merged unless a merge is independently observed.

One next dependency: obtain a working Linux executor for the already-pinned fresh build and preserve the complete source/dependency manifests, build output, printed axioms and dual-kernel logs. Only after successful acceptance should the distinct standard-machine and hierarchy-transfer obligations be promoted for independent review.

## Sources

1. `anthropics/formal-math`, commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, `eth/MainResults.lean`, blob `1c62a550fa1e4cbec65bb7112f92ad67589afddc`; `eth/Solution.lean`, blob `176892178e49792ae41368c13bb4973bae035b29`.
2. Same revision, `eth/README.md`, `eth/comparator.json`, `eth/lake-manifest.json`, `.github/scripts/comparator-check.sh`.
3. `j15marti/pnp`, commit `8b6569ab0d7ab37bd41e6d55767c2d634fd4b9a7`, `.github/workflows/tmr1-lean-audit060.yml`, `experiments/tmr/tmr1_lean_rebuild060.sh`, `experiments/tmr/tmr1_lean_audit060.py`.
4. GitHub run `43804269099`, attempt 3, job `133106046298`; separately retrieved run metadata, empty steps/artifacts and missing-log response.
