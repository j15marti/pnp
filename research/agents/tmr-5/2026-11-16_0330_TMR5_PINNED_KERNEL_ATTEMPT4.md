# TMR-5 direct follow-up: pinned kernel attempt 4

November 16, 2026, 03:30 PST. User request: "Try that". Dependency C1-INDEPENDENT-KERNEL. This is an infrastructure retry, not a new mathematical result. **BLOCKED BEFORE EXECUTION; NOT A PROOF REJECTION.** P versus NP remains OPEN.

## Target and falsifiers

Rebuild the unchanged Anthropic source at 16a5ce41304fcdaea4e0be7c132e1c361dc26da5 using Lean 4.33.1 and pinned Mathlib, print the transitive axioms of MainResults.mainTheorem and MainResults.ethIsFalse, compare exact statements, and replay with Lean and nanoda. Falsifiers are (1) source/dependency mismatch; (2) extra axioms or different statements; (3) actual kernel rejection; (4) a mismatch in the separate ordinary-machine/hierarchy transfer. Executor unavailability is not a mathematical falsifier.

## Actual remote retry and stronger diagnostic evidence

The existing workflow was inspected at execution commit 8b6569ab0d7ab37bd41e6d55767c2d634fd4b9a7. It was not changed or duplicated. GitHub accepted a rerun of job 133106046298 and produced run 43804269099, attempt 4, job 133266252794.

The job began at 03:26:19 PST and completed with failure at 03:26:21 PST on November 16. The full jobs response gives runner_id=0, empty runner_name, runner_group_id=0, the label ubuntu-latest, and steps=[]. No runner assignment or executed step is recorded. The artifact list is empty. Downloading the job log returned HTTP 404 / BlobNotFound.

The commit-level check-runs endpoint returned additional evidence: the check has **two annotations**, while title, summary and text are null. Direct check-run, annotation and job-page fetches were rejected by the connector endpoint allowlist. Their text is therefore UNKNOWN. The available evidence does not establish billing, quota, repository policy, workflow syntax, or service outage as the underlying cause. Do not silently choose one.

This is stronger than the prior empty-step observation, but it does not constitute a successful or rejected Lean proof. No further blind retry was issued.

## Actual local attempt

The original scripts were recovered from the user-provided evidence ZIP. The runner was compared with a fresh connector read of the exact execution revision. Git blob hashes: runner 12b37a6c03ba7ef1fd3078df30dd543c505b3154; audit helper 75572af2a52a76fb0c4b92055ab4f5f4e54b3a46. The latter matches the prior captured script pin, not a new kernel audit.

A real invocation of the unchanged runner exited with code 1 at its prerequisite check. elan, lean, lake and cargo are absent. A real curl probe exited with code 6: github.com could not be resolved. The separate download tool did not acquire an elan bootstrap archive. Plugin discovery did not return a usable Linux/SSH executor. Shell syntax checks passed; these are not proof checks.

The evidence archive contains the actual local command outputs and separately labeled normalized connector observations. No synthetic validation output is presented as a Lean or nanoda result. No local checkout existed; repository preflight, LaTeX compilation, theorem kernels, and the physical-machine/hierarchy transfer were not executed.

## Four gates and exact scope

| Gate | Status |
|---|---|
| DISJ sanity | NOT APPLICABLE to executor provisioning; no rank-to-work claim. |
| Relativization | NOT APPLICABLE to this execution retry; no separation claimed. |
| Simultaneous DTISP | OPEN for the full chain; CI elapsed time is not a SAT time bound and no matched solver time/space run occurred. |
| Deterministic configuration counting | NOT APPLICABLE to build startup; remains an upper-bound safeguard only. |

All mathematical pipeline statuses are unchanged from the /064 handoff. No new reproduction of TMR-1/2/3/4 mathematical claims was performed. /341 remains FAIL as full UNSAT authority and /386 remains RESTRICTED. Compact algorithms, sharing and recomputation remain legal.

## Publication and next concrete action

Append this record, normalized evidence and a read-only diagnostic script to the existing TMR-5 PR #209 branch. Keep the PR draft and distinguish branch publication from main merge. The complete preceding handoff is preserved at commit 9b6619895e440d8cc02230b9bd7e176c75bfb0bb, blob 630cdac53a1e060563d51433e1a04dc1b688ae44. No manuscript is overwritten or claimed newly reviewed in this focused infrastructure follow-up. Peer manuscripts, retired trackers, agent identities, hourly schedules, workflow contents, runner configuration and billing settings are unchanged.

**One next action:** retrieve the two failure annotations for check 133266252794, then repair the evidenced executor-start problem or use a working Linux executor. The supplied fetch script is read-only and requires an authenticated GitHub CLI. It was syntax-checked, but annotation retrieval through it was not executed here. Only after a genuine clean dual-kernel success should the distinct ordinary-machine and E^NP hierarchy obligations be reviewed for promotion.

## Source records

- Existing workflow and runner: j15marti/pnp at 8b6569ab0d7ab37bd41e6d55767c2d634fd4b9a7.
- GET /repos/j15marti/pnp/actions/runs/43804269099/jobs?filter=latest, attempt 4.
- GET /repos/j15marti/pnp/commits/8b6569ab0d7ab37bd41e6d55767c2d634fd4b9a7/check-runs.
- Job log and artifact connector responses; local_attempt4.json and remote_attempt4.json in the local evidence archive.
- GitHub official troubleshooting documentation, https://docs.github.com/en/actions/how-tos/troubleshoot-workflows . This is general troubleshooting guidance, not evidence of this job's specific root cause.
