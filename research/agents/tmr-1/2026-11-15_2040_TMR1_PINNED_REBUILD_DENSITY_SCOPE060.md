# TMR-1/060 | 2026-11-15 20:40 PST | Pinned rebuild attempt and C1-Promise density correction

## Status and selected chain

**Independent kernel replay: BLOCKED BEFORE EXECUTION.** A real owned GitHub Actions attempt was created, but its job failed before any step ran. This is not a rejection of the Anthropic proof. **C1-Promise general four-density claim: FALSIFIED. Corrected exact clause accounting: PROVED/RESTRICTED, independent mathematical review OPEN.** Finite regression evidence is COMPUTATIONAL. The actual circuit-to-counting-to-hierarchy pipeline retains its restricted four-density interface because its compiler already supplies AllOccur. Its counting theorem and higher-class circuit consequence remain conditional. P versus NP remains OPEN.

The governing source is `research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md`; the owner is TMR-1, with only `main1_PNP_MACHINE_MODEL_LEAD.tex` edited among the five living manuscripts. Retired trackers, peer manuscripts, five existing agents and schedules were not changed.

## Candidate, quantifiers and falsifiers

Candidate: at Anthropic commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, independently rebuild the proofs of `MainResults.mainTheorem` and `MainResults.ethIsFalse`, verify their transitive axiom sets and both kernels, then connect the stated one-fixed-machine counting proposition to the already charged compiler and physical simulation.

The main proposition quantifies one machine M and one constant C before all k, n and formula inputs; every stack alphabet is required finite. The four falsifiers stated before source search were revision/dependency mismatch, unexpected transitive axioms, failed kernel replay, and an uncharged unbounded operation inside a formal step. An unavailable executor blocks verification but does not instantiate the kernel-rejection falsifier. The input-interface audit additionally found the concrete normalization falsifier below.

## Actual independent build attempt

Audit branch: `tmr1-20261115-independent-lean060`, based on main `32dd0eecf136d47ff313e6eabe65d6a1cb70978e`.

The published workflow used audit commit `8b6569ab0d7ab37bd41e6d55767c2d634fd4b9a7` and triggered run `43804269099`, job/check `133091313028`. GitHub records a failed job starting at 2026-11-15 20:28:06 PST and ending at 20:28:08 PST, with an empty step list. Retrieving its job log returned BlobNotFound. The check metadata reports two annotations, but their contents were unavailable through the connector. **No billing, quota, runner-policy or mathematical cause is established.** No rerun was requested.

Locally, lean, lake and nanoda are absent; direct GitHub git access fails DNS resolution. No repository checkout existed, so repository preflight did not run. The remote preflight was planned as the first substantive workflow step but also did not run. Scripts passed local shell syntax and Python parser controls; those checks are not a Lean build.

The independent runner is a fresh-source procedure, not a relabeling of upstream logs. It pins source files and every locked dependency, forbids pre-existing proof-project `.olean` objects, builds `Solution`, runs `PrintAxioms.lean`, checks exactly the two requested theorem names and the three expected standard axioms, runs the pinned Comparator with nanoda enabled, verifies sources/dependencies unchanged, and writes SUCCESS only after all checks pass. Dependency cache use is explicitly recorded and is not a from-source rebuild of all Mathlib. The workflow uses read-only repository permissions and no stored checkout credentials.

Reproduction on an appropriately provisioned Linux machine:

```sh
bash experiments/tmr/tmr1_lean_rebuild060.sh /absolute/path/to/audit-logs
```

This command is supplied for reproduction; a successful execution is not claimed here.

## Independently authenticated upstream artifact

Upstream run `40442388505` and artifact `12707409821` belong to the pinned Anthropic revision. The downloaded ZIP SHA-256 exactly matches GitHub metadata:

`6b0a8993626d37614c7843d9c3dfd181a847591c684f425b7a470cc41fb43bf6`.

Its three entries are `lake-build.log` (54,868 bytes), `comparator-logs/comparator.json` (293 bytes), and `comparator-logs/comparator.log` (1,173 bytes). The configuration names both requested theorems, permits only propext, Quot.sound and Classical.choice, and enables nanoda. The original log reports acceptance by Lean's default kernel and nanoda. These are authenticated upstream records, not an independent replay. The standalone PrintAxioms source itself warns that printed output inside imported code is not sufficient for validating untrusted imports; our attempted runner therefore also requires Comparator and both kernels.

Source pins: MainResults `1c62a550fa1e4cbec65bb7112f92ad67589afddc`; Solution `176892178e49792ae41368c13bb4973bae035b29`; PrintAxioms `cb31f549acbce8de837f111979acfdd9836c8411`; manifest `296fefa9ac614013ab29708d71c1ae5dcbc39765`; Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`. Lean is v4.33.1. Comparator `575674928e239f5bc452aab72d1dd7b0f1326494`, nanoda `68d5ca9db226849b41a6fff59d796ff19d0a8840`, landrun `811cfff51ceaf3d9843708aa6d22e9b84ccac8b4`, and lean4export `15f6055e299ad5b89345e533cc2192f4cc00f659` are explicit in the runner. The last is the v4.33.0 exporter rebuilt with the project's v4.33.1 toolchain, matching the pinned upstream script's documented patch-release fallback.

## New connected falsifier: unused-variable cost at C1c

The original /055 totalizer takes a width-at-most-three CNF on n declared variables, deletes duplicate ordered clauses, inserts a tautology for every unused original variable, introduces d=max(1,4-n) new zero-pinned variables, and inserts one fresh-variable tautology. Its exact count preservation and promise normalization are valid. Its advertised universal implication `m <= 4n => m' <= 4n'` is not.

Let m0 be the number of distinct original ordered clauses and u the number of unused original variables. Then exactly

`n' = n+d`, and `m' = m0+u+d+1`.

Proof: the m0 retained lists are distinct; each of the u new tautologies contains an old symbol absent from those lists, and the d pins and final tautology use fresh symbols and are pairwise distinct. Nothing is deduplicated across these groups. The new pins each have one allowed value, so every old satisfying assignment has exactly one extension. No original unused variable is removed or fixed.

Consequently `m <= 4n` gives `m' <= 5n+d+1 <= 5(n+d)=5n'`. If `m0+u <= 4n`, then `m' <= 4n+d+1 <= 4(n+d)=4n'`. In particular the old four-density conclusion remains valid under **AllOccur**, where u=0. These inequalities use d>=1 and hold on the entire declared domain, including n=0.

### Explicit satisfiable counterexample

Declare five variables x0,...,x4, with only x0,x1 occurring. Let L=(x0,not-x0,x1,not-x1). Include the two positive unit clauses; all twelve ordered length-two clauses from L containing a positive literal; and six triples (x0,a,b) where either a=x0 and b ranges over L, or a=not-x0 and b is x0 or not-x0.

These are twenty distinct ordered clauses of width at most three. They force x0=x1=1 and leave three variables free, so the exact count is eight. Repeated literals and tautologies are legal in the stated source language. The authentic /055 normalizer has d=1 and produces six variables and **25 clauses, exceeding 4*6=24**. The normalized count remains eight, with AllOccur, NoDup and unique extensions intact. Its exact formal low-first input is 311 bits.

The circuit compiler in C1b already inserts all missing-input tautologies. Its output therefore has u=0 when passed to C1c. The restricted `m' <= 4n'` premise, the clause-sensitive solver application and the conditional 12C leading exponent bound survive this correction. This falsifier is neither a SAT-answer error nor a defect found in Anthropic's proof.

### Executed original-code reproduction

The new regression refuses to execute unless the original /055 file has Git blob `b3e4e6f2c1b9280e45cc4c523b3b6c45fd063536`. Native Node v22.16.0 reran its 22,728 original assertions, then checked the counterexample through the original `norm`, all 32 original assignments for unique extension, a genuine AllOccur circuit-output control, and 12,551 exact integer parameter combinations. New regression assertions: **13,457; unexpected failures: zero**. The intended old-claim falsifier is confirmed, not suppressed. The deterministic new revision is `tmr1-totalizer-density060.v2`; only the inherited baseline uses seed 20261115. Two independent local executions emitted byte-identical raw JSON.

The Python audit parser accepted one positive axiom-log control and rejected six hostile controls. The complete original manuscript was locally recovered with exact original blob `feb6a5b97414eba2f42dd788a3a27d2d22549fcc` before targeted editing. The corrected manuscript blob is `c12cfc454410b45fbc43c560ead9036005ed33f9`. Local `pdflatex -draftmode -interaction=nonstopmode -halt-on-error` succeeded; this is a LaTeX syntax build, not a visual PDF audit or mathematical verification.

## Same-realization ledger and four gates

No new SAT runtime bound is claimed. On a compiled circuit source the existing single physical execution still charges parsing, graph authentication, gate sharing, deduplication, missing-input tautologies, d pins, all actual formal-input bits, stack simulation and exact output. Its conditional totals remain `T=O((B_C+B_A)^4+T_M)` and `S_peak=O(B_C+B_A+T_M)` for that same realization. The correction explicitly charges u at the normalizer, rather than silently dropping its work or its clauses. Proof-verifier runtime is separate from the claimed counting algorithm runtime.

| Gate | Status and reason |
|---|---|
| DISJ sanity | PASS, restricted. This is clause accounting, with no static-rank-to-work inference. Compact shared circuits remain legal. |
| Relativization | PASS for the syntactic lemma; OPEN for any NP separation. No nonrelativizing NP bridge is supplied, and algebrization/Natural Proofs safeguards remain. |
| Simultaneous DTISP | PASS for the inherited conditional same-run upper accounting; OPEN for a forbidden pair. The failed CI job supplies no algorithm execution data. |
| Deterministic configuration counting | NOT APPLICABLE to the finite clause-count identity. The inherited deterministic physical model retains only the upper-bound guard, never a work lower bound or a quantum/randomized conclusion. |

Horn/2-SAT, affine, bounded-treewidth, equality, autarky, product, padding, auxiliary-variable and compact-source alternatives remain legal. The counterexample specifically tests unused-variable, tautology, repeated-literal and unique-extension controls. /341 remains FAIL as full UNSAT authority and /386 RESTRICTED.

## Publication and one next dependency

The owned manuscript is reconciled in place on the audit branch, previous compact handoff archived by its original blob, and executable code and raw evidence kept separately. Branch publication does not imply main merge. The independent build status remains OPEN, not upgraded by the successful upstream artifact audit.

**ONE next dependency:** obtain a successful fresh pinned Solution build, transitive axiom audit and dual-kernel replay in an available executor, with exact logs and unchanged source/dependency hashes. The original five agent schedules remain unchanged; no background delivery or automatic retry is asserted.

## Primary sources

[1] Anthropic, pinned MainResults and Solution: https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth

[2] Pinned verification runner: https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/.github/scripts/comparator-check.sh

[3] Original upstream run: https://github.com/anthropics/formal-math/actions/runs/40442388505

[4] Actual independent attempt: https://github.com/j15marti/pnp/actions/runs/43804269099

[5] Original /055 source: https://github.com/j15marti/pnp/blob/32dd0eecf136d47ff313e6eabe65d6a1cb70978e/experiments/tmr/tmr1_totalizer_e2e055.js
