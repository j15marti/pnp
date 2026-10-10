# PROOF_MAP initial synthesis, 2026-10-10

P versus NP remains open. This run establishes a source-grounded map and a cumulative review queue. It does not claim to have reviewed the full project corpus, all chats, all repository history, or every referenced proof.

## Priority ranking of current proof spines

The ranking below concerns precision of the current theorem statement and tractability of the next audit, not probability of solving P versus NP.

| Priority | Spine | Established reusable part in the reviewed source | Next missing implication | Present status |
|---|---|---|---|---|
| 1 | Charged recursive wrapper, FORMAL-SPINE1 | A single uniform all-input wrapper satisfying W(h,p), h,p<1, composes into SAT time N^(1+o(1)) and space N^(max(h,p)+o(1)). Fortnow Corollary 3.3 forbids that simultaneous pair in the matched model. | Derive the complete all-input contract from the assumption SAT in P, including acquisition, unsuccessful attempts, all successors, explicit/implicit child access, peak state and encoding transfer. | Conditional implication only. The source explicitly recognizes that this bridge is classically equivalent to P≠NP because the target contract is already excluded. |
| 2 | Achievable-resource transitions, ARC | Existence-level transitions between joint time/space pairs can yield a contradiction if a finite chain enters a valid forbidden region; aggregate and typed-cycle recurrences preserve valid premises. | Establish a strict, fully charged transition on the full input domain without an unknown-exponent parent-scale SAT call. Keep both resource coordinates on one machine. | Conditional framework plus partial computational implementations. |
| 3 | RMV / source-specific separator / ASCS-FSC | Seed-fixed surjectivity blocks generic low-rank slices; an actual low-dimensional orbit gives a field recurrence. Absolute ordinary-source complexity can fail oracle substitution. | Produce a dense Boolean source-bound separator of the required size, or an exact fast accepted-source extension certificate, with the same realization and a nonempty charged reconstruction exponent window. | Structural lemmas and sharp missing interfaces. No Boolean transfer or reconstruction closure established. |
| 4 | SRAS consumer and direct wrapped-process cost | Continuation equivalence gives a summary-size bound; deterministic route completeness conserves state/source/external distinctions. Standard self-reduction exposes a restriction path. | Prove that the SAT task forces the rich consumer during one execution, then prove an ordinary cost bound permitting reread, recomputation and DAG reuse. Raw assignment contraction is insufficient. | Accounting and representation theorems, not unrestricted runtime lower bounds. |
| Supporting | Exact-3SAT, q-Horn/backdoor/clean-core structure | Numerous structural controls, localized obstructions and partial solver rules exist in the source corpus. | An arbitrary-algorithm extraction/coverage theorem with costs, or a particular new valid ARC transition. | Useful test families and restricted results. They are not themselves a P≠NP proof. |

## Strongest current concrete experiment

The reviewed ARC15 report (9 October, 19:40 source name) recovers an existing small-backdoor/clause-DNF builder and permits an early SAT exit only after a lifted witness passes a full-source check. On its declared 13 formula cases, coverage improves from 6/13 to 12/13 and executed restrictions fall from 1696 to 794. All six new decisions are SAT. The remaining random12_1 instance is UNSAT according to exhaustive reference checking and returns UNKNOWN. This is method-level coverage, not whole-portfolio coverage, and the counters omit material machine costs and transient state. It is not a joint resource certificate.

The next concrete experiment is negative-case completion on random12_1 followed by independent families and recursive descendants. Success on that one instance would be an implementation result, not all-input coverage. A formal progress claim must identify the newly covered family and prove a charged uniform bound.

## Source reconciliation and hazards

1. The current main4.tex and main5.tex entry points each list 43 include paths. Their summaries are not the whole manuscript. `include_dependencies.json` records 86 root edges; transitive include expansion remains pending.
2. main2.tex still contains a historical product landing criterion C+rho<2cos(pi/7). Root main.tex already explicitly supersedes this claim in its authoritative 8 October defense reconciliation; main9.tex and main10.tex preserve the correction. The stale main2 passage therefore does not change the current canonical status. A future editor should add a local supersession notice to prevent isolated reuse. The root distinguishes the valid golden-ratio product region, Fortnow's direct near-linear/sublinear-space region, and the cosine exponent's separately constrained small-space regime.
3. PROVED_EXACT contains both retired claims and corrections, including PRF2-0161 and CLAUDE-0160. Folder membership and a title saying PROVED are not sufficient acceptance evidence. Read the proof and its correction chain.
4. The legacy Claim Ledger was last modified 18 September in returned metadata. It is historically useful but cannot override October repository reports.
5. GROK's 1 October barrier analysis is itself explicit that it did not rederive its reconstruction citations from primary PDFs. Treat its assertions as leads to check, not literature verification. It also contains apparent quantifier/parameter wording requiring independent review; do not promote it wholesale.
6. Statements that sound stronger because they change representation, hide an index, or assume a cheap child accessor must have a model/encoding cost ledger. RECOVERY-STRENGTHEN10 explicitly keeps this unresolved.

## Coverage, accurately bounded

The accompanying inventory has 382 unique Drive metadata records discovered in targeted searches. The PROVED_EXACT direct-document listing completed two pages with 163 entries and no remaining cursor for that query; subfolders and their contents are not exhausted. GROK has at least 100 listed direct documents and an outstanding cursor stored in `discovery_cursors.json`. Six selected Drive texts are saved, with content review distinguished from fetch/partial review. GitHub root sources and selected additions were reused from MODEL_BRIDGE and hashed in `github_source_snapshots.json`.

Personal Context returned unavailable to this agent. Parent reported a successful separate retrieval of earlier scheduling context. No agent-level assertion that all chats have been read is warranted. Chats, inaccessible content, unvisited repository history, legacy folder descendants, and unreviewed includes remain explicit coverage gaps.

## Per-run synthesis contract

Each future PROOF_MAP run should start by reading the latest proof-spine status and most recent REDTEAM verdicts. It should then choose a dependency that is open in a current spine, retrieve the actual earlier sources, follow correction links, and check primary literature. The run should update one of: exact lemma, counterexample, scope correction, reproducible experiment, or explicit negative search result. Repeated metadata sweeps without a dependency question are not substantive progress.

Every claim record should carry: stable claim ID; quantified statement; model and size normalization; source path/ID and immutable revision/hash when available; dependencies; current status; counterexample controls; ordinary construction time; verification time; child access/replay cost; peak workspace; reviewer; supersedes/superseded-by. A theorem is promoted only after the actual proof and load-bearing cited theorems are checked in the matching model. Machine formalization is distinct from a LaTeX formal proof and must never be claimed from prose or exhaustive finite testing.

The exhaustive-review queue should incrementally enumerate sources and track `metadata_only`, `fetched_partial_review`, `content_reviewed`, `claim_checked`, `literature_verified`, `experiment_reproduced`, and `blocked`. A cursor-free metadata listing is not content review. Empty or failed writes are not evidence of a theorem.

## Source anchors

- Current repository: https://github.com/j15marti/pnp, branch main.
- FORMAL-SPINE1: `research/agents/lead/2026-10-08_FORMAL-SPINE1.tex`, local source provided by MODEL_BRIDGE.
- ARC15: `research/agents/proof/2026-10-09_1940_ARC15.tex`, local source provided by MODEL_BRIDGE.
- RECOVERY-STRENGTHEN10: `research/manuscripts/RECOVERY-STRENGTHEN10/main4_addition.tex`.
- Drive PROVED_EXACT: https://drive.google.com/drive/folders/1jCF4Dj2Rnm0Ln2d-b9FdBw1SSo2VNpPI.
- Linked Proof Index: https://docs.google.com/document/d/1J7ZGCqGO1bm7D7l5uJT-qI8yEcxTIYUgjDnVBlyZQv8/edit.
- Legacy Claim Ledger: https://docs.google.com/document/d/17NPKIB2yB1xZ12iy3eyY_0fk0vOh8DEkwZJtepk36-A/edit.
- LSPV-5-58501: https://docs.google.com/document/d/1z4Jaoi4P0ZJXU8DTemXW6Eqb3vvt5RosAZTWuVMeCG0/edit.
- GROK barrier review: https://docs.google.com/document/d/1OfJcuk7TxQrNa5duHjXyLY9B6e9MaTV2mxN9qCuGJ0g/edit.
- PRF3-0002 effective-wrapper incompleteness: https://docs.google.com/document/d/1Q9LwocaCYC2YEYhaaqu1Hu8p-GQBLTtoWgSdwTmfLjs/edit.
- NEW_UNSAT-0076 aggregate explicit OR-shrinker threshold: https://docs.google.com/document/d/1HZBaOY9D9BEQbkgvaffDoh3X1bXJq8uAAkGx5jWQAyw/edit.

## Primary literature checked in this run

1. Lance Fortnow, *Time-Space Tradeoffs for Satisfiability*, Journal of Computer and System Sciences 60(2), 337-353 (2000), doi:10.1006/jcss.1999.1671. Author PDF https://lance.fortnow.com/papers/files/npvsnl.pdf. Corollary 3.3 explicitly gives the deterministic simultaneous near-linear-time/sublinear-space exclusion. The paper permits random access and discusses the single-machine distinction. This supports the formal endpoint only; it does not provide the missing wrapper.
2. Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, author PDF https://lance.fortnow.com/papers/files/tst.pdf. Retrieved as the primary source for subsequent exact-region checking. Full theorem-to-parameter audit remains pending in this run.

## Team integration and additional reconciliation

MODEL_BRIDGE source recovery and REDTEAM's `audit_note.md` are incorporated. REDTEAM accepts the wrapper recurrence conditionally and the finite scope of ARC15. It identifies a genuine correction to the saved MAIN58501 field-surjectivity consequence: surjectivity rules out nonzero polynomial functions vanishing on the full output image, not all nonzero formal polynomials over a finite field. X^q-X is a counterexample. Requiring individual degree below q, or working modulo the field equations, repairs the statement. The Boolean full-cube conclusion survives. This correction should be propagated to descendants after exact source matching.

Root main.tex, main9.tex and main10.tex establish a narrower direct route than the balanced-branch contract: a single ordinary equivalent successor of size N^(2/3+o(1)), acquired in near-linear time and N^(2/3+o(1)) space. Fixedly many iterations erase a fixed seed machine's exponents because the leaf exponents are K(2/3)^d and L(2/3)^d. This is distinct from an aggregate-linear branching recurrence, whose near-linear limit requires the single-algorithm recursive proof in FORMAL-SPINE1. Both acquisition hypotheses remain OPEN.

The full repository tree supplied by the parent has 1,522 blobs. `repository_coverage_queue.csv` gives a row for each observed blob, and `root_missing_references.json` records literal root references absent from that snapshot. Missing current paths may exist in history; root mentions are not substitutes for files. The newest present research/main snapshot is 2026-10-02_1658_MAIN_1658.tex, while current root and manuscript summaries contain later work. Timestamp recency and physical source availability are separate checks.

The repository's CODEX.md requires `$pnp-research` at `.codex/skills/pnp-research/SKILL.md` for substantive runs. That skill, synthesis mode, research protocol, and report template were loaded. Every scheduled run must invoke it, run its preflight, survey the repository, and write a corpus reconciliation record. Parent publishing must run `python scripts/check_research_reports.py` and `python .codex/skills/pnp-research/scripts/preflight.py --check` in the actual checkout. This agent has not claimed those repository-wide checks succeeded. Root main.tex remains the single canonical living synthesis; historical reports are append-only, and authorized root reconciliation requires a fresh SHA and readback.

LOWER_BOUND's actual report now supplies a second precise conditional spine: a polynomial-witness verifier that covers each eligible time-t short program's halting output while accepting at most L(n) distinct outputs per program, with length threshold n-ceil(log2 L(n))-1, implies P≠NP by counting and time-bounded Kolmogorov immunity. Its extension to one common oracle was independently reviewed by REDTEAM. This is an exact barrier/conditional result under the declared efficient universal machine, not existence of the verifier. Next need: construct that verifier for one explicit suitable time bound, or find a narrower obstruction.

COST_CERTIFICATES independently states the physical-access charge C=max{1,r,(g+v-h)/(1-h)} and notes that the saturated (6/5,11/10,1/2) ledger increases to at least 6/5+2g under its conservative simulation when g>0. Its draft also gives an elementary certificate-enumeration diagonal: for any fixed polynomial witness bound, an exhaustive search can output a missing endpoint in 2^poly(n) time, so the proposed completeness cannot hold at t(n)=2^(2^n). This rules out an overbroad all-superpolynomial-time formulation; it leaves slower fixed time bounds open. REDTEAM has independently accepted this scoped diagonal. The author repaired the uniform error envelope, strict descendant decrease above a fixed threshold, exact terminating base case, and halting single-output semantics. The synthesis adopts the certificate boundary as PROVED/EXACT under those conventions, with no novelty claim and no separation claim.

The attachment audit gives a separate implementation clue: the generator's seven selected random positions do not depend on nonempty seed contents. Six- and eight-character FNV-1a tags are finite labels, not injective provenance certificates. These findings constrain the proposed wrapper tooling but are not lower bounds.

MODEL_BRIDGE and LOWER_BOUND independently match the concrete (6/5,1/2) target to the FLMV finite-entry region with c=1201/1000 and d(c)-1/2=26275399/2884802000>0. This provides a strict endpoint margin under the local encoding/access hypotheses. It does not supply the missing all-input construction.

REDTEAM independently read proof_map.tex and accepted its actual conditional single-child composition theorem, simultaneous ancestor/child storage accounting, distinction from balanced branching, and finite-field correction. Parent's final audit additionally made the finite-base rule explicit: before each of at most d shrinker calls, stop and use the fixed total seed solver if length is below a fixed threshold; those finitely many inputs contribute constant time and space. The report compiled successfully to five pages with resolved references. Parent's startup preflight passed on a recovered subset, which does not establish complete corpus materialization or repository-wide validation.
