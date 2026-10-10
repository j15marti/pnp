# Five-agent proof review protocol

Authorized research reorganization: 2026-10-10, P vs NP project.
Canonical repository: `j15marti/pnp`, default branch `main`.
Canonical review directory: `research/review/`.
Mathematical status: **P versus NP remains OPEN**.

## Team and cadence

Each agent runs hourly. Starts are staggered by 12 minutes in Asia/Seoul, preserving the project's prior supported arrangement. This is one team start every 12 minutes, not five individual runs every 12 minutes. Start times are scheduling targets; completion and peer dependencies are not guaranteed by a clock.

| Minute | Role | Specific need |
|---|---|---|
| :00 | MODEL_BRIDGE | Obtain an exact, uniform all-input transfer from a hypothetical polynomial SAT decider to a useful wrapper or successor; charge encoding and semantic transport. |
| :12 | LOWER_BOUND | Establish the lower-bound or obstruction ingredient and its arbitrary-algorithm/ordinary-SAT applicability; resolve quantifiers, uniformity, source definitions and barrier compatibility. |
| :24 | COST_CERTIFICATES | Prove attainable quantitative bounds for construction, acquisition, certificates, access, recursion, replay and simultaneous space; expose hidden polynomial exponents. |
| :36 | REDTEAM | Independently attack the newest material changes by all three builders, verify repairs and record per-claim verdicts. |
| :48 | PROOF_MAP | Reconcile total progress and source coverage, rank surviving proof spines, maintain dependency graphs and formal manuscripts, and select the next exact missing links. |

These roles replace the prior five-role ARC/WRAPPER team's prompts. Other paused teams remain paused. Do not change schedules or activate additional teams from a research run. Do not spawn recurring child agents.

## Every run, every role

1. Recover current state from GitHub. Read this protocol, root `main.tex`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, `research/review/STATUS.md`, all current `research/review/spines/` summaries, and the newest completed peer reports. Inspect `main4.tex`, `main5.tex`, `main9.tex`, `main10.tex` and their actual includes when relevant. Do not assume numbered manuscripts, summaries, or titles are authoritative without reading their supersession notices and underlying sources. Run the repo skill preflight when the necessary local snapshot is available; report partial-check scope honestly.
2. Survey the whole current repository tree and changed files since the last completed run. Use the coverage ledger to avoid repeatedly reading only recent work. Distinguish metadata inventoried, retrieved, substantively reviewed, dependency audited, and unavailable. A search snippet is not a reviewed source. Keep historical reports immutable.
3. State one missing implication with exact quantifiers, machine model, encoded input bit length, same-realization requirements and minimum useful theorem. Identify why it matters to a currently strongest spine. Review alternative spines before selecting it.
4. Search previous work first: project conversation retrieval, GitHub content and history, Google Drive project records, LOG, PROVED_EXACT, grammar/SIL/BOOL, GROK and CLAUDE material. Follow old references to original proofs and experiments. Search named lemma IDs, equivalent formulations and counterexamples. Also review at least five previously unreviewed relevant corpus items when accessible, or record why fewer were available/useful. Do not repeatedly call a known-unavailable source without reason to expect changed access. Chat search is not an exhaustive export of all chats.
5. Then search current primary literature for the exact gap, including potential rigorous cross-domain transfers. Record theorem number, hypotheses, model, uniformity, input/resource measures and canonical URL. Distinguish theorem transfer, candidate analogy and failed transfer.
6. Formalize and try to falsify the candidate before extending it. Use relevant easy families, padding, alternate representations, source-carry/current-scale solver escapes, DEAD/COPY/DELAY/INTERP/RECOMP, oracle and algebraic-oracle replacements. Test computational claims reproducibly when useful. Each Python invocation has a 25-second cooperative budget and about a 30-second hard limit; checkpoint longer work.
7. Preserve full costs: discovery, failed attempts, normalization, wiring, encoding, child multiplicity, construction, verification, indexing, query generation, replay, resumption, output, caches, suspended ancestor state and transient workspace. Never infer arbitrary-algorithm runtime from raw histories, assignments, hashes, circuit/proof-system bounds or certificate existence alone.
8. Record a concrete result, counterexample, repair or narrowed OPEN arrow. New conjectures and finite evidence cannot be promoted to a theorem. Labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED. One open load-bearing arrow means no proof of P != NP. Formalized here means explicit mathematical LaTeX; use the label machine-checked only with an actual proof-assistant verification.
9. Write a timestamped LaTeX report and structured local log before remote publication. Update the role-owned formal manuscript when the mathematics changes. Each run must review all strongest spines but need not make cosmetic changes to unrelated manuscripts. Record exact citations and a .bib file where appropriate. LaTeX lists use `\item[]` or prose.
10. Publish and read back from GitHub. Reconcile conflicts with fresh blob SHAs; never force-push. Record successful commit/blob identifiers or precise failure. On transient failure retry once after about 30 seconds when supported. If GitHub writes remain unavailable, persist the exact report, manuscript and outbox in the existing Google Drive LOG folder, and record a verified URL. A local-only file is not durable cross-run memory. Do not bypass permission denials. Do not claim upload/compilation/test success without evidence.

## Stable source locations

- GitHub: https://github.com/j15marti/pnp
- Drive project root: `1AiIZ1QvEpFXEw57fKkc-BX-M5CAYBE0b`
- Drive LOG: `1B7ML198fDIPj3aztsODoVK2JbodGeHeQ`
- Drive PROVED_EXACT: `1jCF4Dj2Rnm0Ln2d-b9FdBw1SSo2VNpPI`
- Drive CLAUDE_FOLDER: `1xa60Q03s408uGAMpmG4kToGiAfTDIDm2`
- Drive NEW_LANG: `1uxil6A8WM2aKZ1GrOajBJeSC5BZqt2nE`
- Drive BOOL: `1jAmIao80rKg8ZY-G7cRrphEXT1ZWymq3`
- Find GROK using current project folder metadata; do not guess IDs.

## Files and concurrency

- Immutable per-run reports: `research/review/reports/<role>/<UTC timestamp>_<run-id>.tex` and optional companion `.md`, code and raw results.
- Role-owned mutable manuscripts: `spines/model_bridge.tex`, `spines/lower_bound.tex`, `spines/lspv_separator.tex`, `spines/cost_certificates.tex`. MODEL_BRIDGE owns the first; LOWER_BOUND owns the next two; COST_CERTIFICATES owns the last.
- REDTEAM owns `coordination/redteam.md`; its review must identify exact versions and claims, verdict, counterexample/repair and any unreviewed new material.
- PROOF_MAP owns `STATUS.md`, `coordination/proof_map.md`, `spines/proof_map.tex`, the integrated coverage queue and claim/dependency ledger. It integrates builder evidence and red-team verdicts rather than treating a majority vote as proof.
- Each role owns its `coordination/<role>.json` checkpoint and `coverage/<role>.jsonl` evidence. Only PROOF_MAP reconciles the common queue, preventing competing writes.
- Local logs: `research/local_logs/review/<role>/<UTC timestamp>_<run-id>.json`. Mirror completed logs to `research/review/logs/<role>/` so isolated scheduled runs recover them. Include sources read, missing link, attempted claims, verdict, tests, changes, pending writes and one next target.
- Root `main.tex` remains the single canonical overall living document. Preserve its ownership regions and existing project governance; this team may maintain its new review documents and leave a precise handoff for LSPV-5 rather than overwrite unauthorized executive sections. Relevant root route manuscripts may be updated with current SHA and narrow, evidence-backed changes as authorized by the user's request.

Do not append concurrently to one shared text log. Immutable run logs plus the synthesis index provide the shared history. Every run reads the newest completed peer artifact; if a predecessor has not finished, mark it pending and process its delta on the next run.

## Initial priority and status

Prioritize the explicit all-input charged successor / favorable typed epoch and the ordinary source/access interface. The known recurrence is not itself that construction. FORMAL-SPINE1 already observes that its sufficient wrapper is forbidden by a known endpoint, so deriving that wrapper from P=NP carries the separation itself. Fixed-depth single-child shrinkage and fully recursive balanced branching are distinct arguments.

Do not revive the retracted universal `t+s < 2 cos(pi/7)` product endpoint. Match every endpoint to the current primary source. Do not infer all-input coverage from ARC15's 12/13 method-level result. Inventory entries in PROVED_EXACT may be refuted or superseded; read corrections.

The initial corpus inventory contains 1,522 GitHub blobs at commit `b6948eb15a8afec37cc904120ce20b61b45a0dad`. Enumeration is not substantive review. Exhaustiveness is a cumulative objective, not a claim made by this setup run.
