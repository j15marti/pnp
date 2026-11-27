# Public proof release gate (user directive, 2026-11-27 Pacific)

User instruction: if we have a completed proof of either P=NP or P!=NP, publish a production-ready LaTeX document, PDF, and supporting data to GitHub j15marti/pvsnp and update the README there to describe the current results.

This is a standing instruction for all research agents, preserving existing identities, specialties, schedules, enabled states, manuscript ownership, common signed E/B input priorities, exact instance/guard/residual IDs, cooperative verification protocol and scientific safeguards. Ordinary research runs do not modify the scheduler or create/reactivate agents.

## Release eligibility
A completed P=NP proof must give a uniform deterministic algorithm with correctness on every input of an authenticated NP-complete decision problem and one fixed polynomial worst-case total bit-cost bound in the original encoding, including discovery, failed tracks, every required branch, arithmetic, verification, intermediate representations, reconstruction and memory. A completed P!=NP proof must exclude every fixed polynomial-time deterministic decider in the unrestricted standard model, or establish an audited equivalent implication. Finite benchmarks, scoped lower bounds, conditional progress theorems, reported external arithmetic proofs, and conjectures are not completed Boolean P versus NP proofs.

Immediately broadcast a candidate complete proof to issue #328 in j15marti/pnp, with a pinned full manuscript, precise theorem, complete dependency DAG, source/checker pins, open-gate audit and falsifiers. Request independent reconstruction and adversarial review from the relevant active proof tracks. Each reviewer must actually inspect the proof and report any unresolved dependency or counterexample; consensus or numerical tests are not a substitute for mathematical validity. Do not claim a completed proof until every load-bearing implication has a complete checked argument, all substantive objections are resolved, and independent review has actually occurred. If not complete, continue research, mark the gap OPEN, and publish only clearly scoped intermediate work.

## Public release artifacts and process
After the eligibility gate is satisfied for either direction, use the existing authorized public repository https://github.com/j15marti/pvsnp (default branch main). Coordinate a single release owner through issue #328 to prevent conflicting edits and duplicate publication. Publish a new timestamped, versioned release directory containing:
- Production-ready standalone LaTeX source, bibliography (.bib), figures and build instructions.
- The compiled, inspected PDF of the same revision, with no unresolved references or missing assets.
- Complete reproducibility supplement: code/checkers, exact input encodings and IDs, pinned dependencies, seeds, raw data, expected results, limitations, and checksums. Separate experimental evidence from mathematical proof.
- Independent audit/review record, proof status, explicit quantifiers and resource ledger, with all source and release revisions pinned.

Fetch the entire current README.md and its SHA before editing. Preserve prior results and history; add a clear dated current-result section, theorem and scope, proof link, PDF link, data/code links, reproducibility instructions and review status. Never overwrite another author's manuscript, claim an independent build that was not run, label a conjecture as a resolution or announce public publication before the commit and artifact readbacks are verified. Verify exact file contents/checksums and read the updated README at its resulting commit. If any connector/build/upload/review fails, preserve exact pending artifacts and report the blocker and which parts are actually published. Do not label an absent PDF as available.

The current E/B model manuscript is a specification and conditional framework, not a completed P versus NP proof. P versus NP remains OPEN until the release eligibility gate is met.
