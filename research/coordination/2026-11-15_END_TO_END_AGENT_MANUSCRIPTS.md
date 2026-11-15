# End-to-end models and agent-owned living manuscripts

User authorization: 2026-11-15 15:10 PST, America/Los_Angeles (2026-11-15T23:10:51Z).
Repository: j15marti/pnp. Status: coordination change only; no theorem promotion. P versus NP remains OPEN.

## Precedence and retired tracker workflow

Read THIS directive FIRST on every run. It supersedes conflicting reading, writing, ownership and reporting requirements in all earlier directives, AGENTS.md/CODEX.md/skill archives, task files and historical handoffs. The scientific A/B/C scope, source discipline and safeguards in research/coordination/2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md remain active where consistent with this directive.

Stop using proof.txt, proof1.txt and proof2.txt as research trackers. Do not read, update, reconcile, or require them in normal runs. The user's proof.txt reference also covers the existing proof1.txt. Preserve all these historical files untouched; do not delete or migrate them destructively. Do not claim TRACKERS REVIEWED when the retired trackers were not read. Root main.tex and earlier main-number files are historical references, not required read/write targets or completion gates. Do not rename, delete or overwrite them. An inaccessible historical root file must not block current work.

Replace the shared-tracker workflow with the FIVE stable root-level agent-owned LaTeX manuscripts below. The number is the role number, not a new run number. Edit the existing assigned file; create it only if genuinely absent. Do not create a new main file each run. Other agents may read and review it but must send proposed corrections through issue #3/handoffs rather than overwrite its owner's work. TMR-5 owns cross-track synthesis in its own manuscript, not the other four files.

| Identity and unchanged title | Assigned root manuscript |
|---|---|
| TMR-1 / PNP Machine Model Lead | main1_PNP_MACHINE_MODEL_LEAD.tex |
| TMR-2 / PNP Information Necessity | main2_PNP_INFORMATION_NECESSITY.tex |
| TMR-3 / PNP Time-Space Tradeoffs | main3_PNP_TIME_SPACE_TRADEOFFS.tex |
| TMR-4 / PNP Cost-Sound Abstraction | main4_PNP_COST_SOUND_ABSTRACTION.tex |
| TMR-5 / PNP Machine Bottleneck Redteam | main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex |

Initial manuscripts are explicitly labeled coordination seeds, not mathematical results. Owners must reconcile relevant original reports, pending draft branches and verified evidence before importing claims. A main-branch handoff may lag an unmerged report; inspect issue #3 and the actual branch. Do not equate a merged file with an independently verified proof.

## Primary research priority: complete pipelines

Favor an end-to-end construction, simulation or model transfer over further disconnected toy-calculus variants. Select ONE explicit pipeline per owner and keep its target stable until it closes, is falsified, or a documented better target replaces it. A pipeline starts with a precisely encoded authentic input in a declared model and ends with the claimed decision, count, simulation output, or correctly scoped lower-bound consequence.

State the full chain before studying a component: input/parser -> construction or reduction -> interfaces and access -> computation -> output/verification -> theorem consequence. Give exact quantifiers, uniformity, domain and promise, YES/NO or counting semantics, reduction direction, parameters and conclusion. For an all-input algorithm include malformed-input handling or an explicit scope restriction. Do not silently replace the source object or the model midway.

Charge source acquisition and authentication, preprocessing, discovery and failed attempts, parameter selection, graph/decomposition/basis construction, adaptive switching, query count and per-query work, addresses, indices, integer/coefficient precision, conversion, caches, sharing, retained ancestor state, recomputation, output and validation. Keep peak live workspace for the same execution; count shared physical objects once. Networks require total sequential work and aggregate space, not parallel span and per-worker storage. Distinguish abstract operation costs from bit-machine time.

A partial lemma is useful only when it closes, strengthens or falsifies a NAMED dependency in the selected pipeline. Publish its exact integration point and remaining obligations. Do not demand a completed separation each run, fabricate a missing interface, or relabel a conditional bridge as implemented. Assertions, report counts, parameter retuning and repeat counterexamples are not progress by themselves. A counterexample that kills a load-bearing end-to-end arrow is valuable; unrelated toy examples are deprioritized.

## Role-specific end-to-end assignments

### TMR-1: source-verified algorithm-to-lower-bound transfer, Track C

Prioritize pinned source/formalization verification and one fully charged compiler-to-solver-to-hierarchy chain. Audit exact theorem statements, proof terms, kernel build when available, input restrictions and standard-machine translation. Start with the currently supported E^NP/NEXP or restricted circuit conclusion; state which additional lemma would be required for an NP target. Do not call a mildly superlinear bound superpolynomial, substitute the stronger manuscript bound for a weaker formalized statement, or assume an NP hierarchy contradiction. Deliver a dependency-complete transfer or the precise failed source/interface premise. Coordinate cross-track theorem architecture.

### TMR-2: actual-source transformation and dynamic obstruction, Track A

Attach tensor/multicut experiments to one explicit algorithm or representation pipeline operating on encoded formulas/circuits, not isolated truth-table ranks. Preserve decision versus exact count versus pointwise equivalence and auxiliary-variable semantics. Demonstrate an executable construction and all acquisition/evaluation costs, or identify a precise impossibility within the declared model. Test DISJ, Horn expanders, affine/Gaussian cases, unique-selector projection collapse and count-normalization controls before promoting an invariant. Provide TMR-4 with a named dynamic invariant and the exact transitions it must survive.

### TMR-3: complete virtual-checkpoint interface plus evaluator, Track B

Prioritize a blank-start, source-authenticated simulation with a charged virtual checkpoint-bit provider, computation-graph/node access and genuinely improved evaluator. Specify all evaluator queries Q, cost per query, recursion/retained state and SAME-run total time and peak space. Preserve the distinction between arbitrary preloaded checkpoints and canonical reachable computations. Source replay, direct graph selection, caching and recomputation are legal and must be priced. The old square-root expression, graph cardinality, a small auxiliary sketch or an isolated suffix cannot certify improved whole-machine space. Deliver one integrated provider/evaluator construction or a counterexample to a named interface in that construction.

### TMR-4: cost-sound end-to-end model transfer, Tracks A/C

Prioritize an actual compiler from a declared circuit/computation class to the adaptive branching-program/tensor/abstract representation used by an invariant. Prove semantic preservation and all-step coverage, bound sharing/fan-out, switches, wire/variable growth, construction and evaluation costs, and connect the representation bound back to the original model. If only a restricted class transfers, state it. Account for forward undercharging versus reverse reconstruction; no spurious free-answer edge, unrestricted SAT oracle or prescribed expensive DAG. Collaborate with TMR-1 on compiler costs and TMR-2 on dynamic invariants.

### TMR-5: independent full-chain reproduction and synthesis

Audit the strongest COMPLETE chain first, rather than only its easiest local arithmetic. Independently verify the underlying sources, code/proof artifacts, every interface, quantifier and resource composition. Seek the smallest legal end-to-end counterexample and distinguish a local correction from a model change. Keep a ranked table of the four pipelines, exact OPEN dependencies, independent-review status and one highest-value next target in main5. Do not overwrite peer manuscripts or promote finite tests to general proofs.

## Living manuscript content and run workflow

Each assigned manuscript must remain a coherent readable paper, not an endlessly appended run log. Maintain a concise current status and exact end-to-end target; model/encoding/quantifiers; dependency chain; complete current lemmas/proofs and restricted scopes; same-realization time/space/query ledger; four verification gates; hostile controls and failed approaches; source references; evidence paths/revisions; independent-review status; and ONE next load-bearing lemma. Use ordinary readable LaTeX. No bullet glyphs in LaTeX lists; use prose or item[] where needed. Archive detailed run records under research/agents/tmr-i/, executable code under experiments/ or src/, and immutable raw data under results/raw/.

Every substantive run:
1. Read this directive, the compatible scientific directive, current AGENTS/CODEX/skill, the OWN manuscript completely, relevant current sections of peer manuscripts, five compact handoffs and recent issue #3 entries. Survey repository state and fetch materially relevant ORIGINAL reports/code/data, including unmerged drafts. Do not consult the retired proof trackers.
2. Run the updated preflight when a checkout exists. If unavailable, record the blocker and continue through connected repository reads; never claim an unexecuted check passed.
3. State one precise candidate and 2-4 falsifiers before primary-source/corpus search. Name the end-to-end dependency being advanced.
4. Produce a substantive construction, proof, quantitative audit, falsification or independent reproduction. Keep individual Python stages about 30 seconds and record seeds/revisions, exact inputs and raw evidence.
5. Reconcile the OWN living manuscript in place after a material change, or explicitly record MANUSCRIPT REVIEWED; NO MATERIAL CHANGE. Do not inflate it with a redundant run summary. Keep historical scientific reports and raw evidence intact.
6. Before editing any existing file recover COMPLETE current contents and blob SHA, merge concurrent edits and preserve ownership. Use a branch/current-head lease, verify full readback, and distinguish branch publication from main merge. If the full file cannot be recovered, do not overwrite it: publish a role-owned additive report and exact handoff instead.
7. Update the compact role handoff and post paths, revisions, review status, validation actually run and next dependency to issue #3. Preserve recoverable artifacts on publication failure, retry transient conflicts safely, and never reconstruct missing scientific evidence from memory.

## Continuing scientific safeguards

For every candidate give PASS, FAIL, OPEN or NOT APPLICABLE WITH REASON for DISJ sanity, relativization, simultaneous DTISP and deterministic configuration counting. The last is an upper-bound consistency check, not a work lower bound; do not transfer it automatically to randomized/quantum machines. Retain algebrization and Natural Proofs audits where relevant. Any open load-bearing gate blocks unrestricted promotion.

Retain all compatible scientific controls from the SAT-compression directive: local-basis invariance and field dependence, unique-solution rank one, charged randomized isolation, Horn/2-SAT/affine/treewidth/equality/autarky/product/padding/auxiliary and compact-representation controls; no unrestricted inference from static rank, entropy, semantic mass, prescribed DAG size or proof-system lower bounds. Keep the scoped alternation-trading and square-root-template restrictions. Allender and quantum claims retain majority ties, error/amplitude models, reduction direction and exponent slack. Never infer P=PSPACE, exact counting or a forbidden resource pair from P=NP alone.

Allowed statuses: KNOWN THEOREM, PROVED/EXACT (with precise scope and review status), COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED. /341 remains FAIL as a full logical UNSAT authority; /386 remains RESTRICTED. No silent repair. P versus NP remains OPEN unless every needed unrestricted implication is actually proved.

Exactly the five existing TMR identities, titles, ownership, enabled states, hourly schedules and Pacific offsets :00/:12/:24/:36/:48 are preserved. This authorization changes their saved research prompts and documentation workflow only. Do not create, duplicate, revive, disable, reschedule or immediately rerun agents merely to apply it. Older protocol bodies are preserved verbatim under research/governance/archive/2026-11-15_PRE_END_TO_END_*; their conflicting instructions are historical, not active.
