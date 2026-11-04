# Agent GitHub Writing Protocol

## Reference resource: P vs NP world ledger (2026-10-28 09:24 America/Los_Angeles)

Optional reference added at the user's request. **This note is additive: it changes no task schedules, agent count, role ownership or scientific allocation, and it adds no mandatory preflight read.** `research/agents/claude/world-ledger/` holds a ledger of 40 complexity statements, each marked True/False/Open in Impagliazzo's five worlds (Algorithmica, Heuristica, Pessiland, Minicrypt, Cryptomania) and automatically classified as theorem, equivalent of P = NP or P != NP, half-win, implication, or world separator. Read `world_ledger.csv` (plain text) or `P_vs_NP_World_Ledger.xlsx`; `README.md` in that folder explains the categories and how to add rows through `build_ledger.py`. Proofs and status labels for the results the ledger cites are in `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`. Useful when classifying a candidate lemma: a statement equivalent to P = NP is a reformulation, not progress. Row L13 (Buss–Williams: alternation-trading proofs cannot reach SAT time exponent 2cos(π/7) with n^{o(1)} space) bears directly on the ARC/FLMV time–space spine. Governance record: `research/governance/2026-10-28_0924_WORLD_LEDGER_POINTER1.tex`. Addendum (2026-10-28 09:39): `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` audits a direct-product route to the UWI common-input statement (ledger rows L29–L33). Finding: a polynomial portfolio collapses into one algorithm with an N^d time factor, so that route is dominated; the proposed next target T-PORT (row L33) asks whether alternation-trading bounds transfer to the UWI portfolio in small space. Addendum (2026-10-28 13:26): `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` answers it for alternation trading: a barrier theorem (row L34) shows Williams-style proofs with the portfolio rules cannot beat linear time when the portfolio has about N programs (the UWI size), while every sublinear portfolio N^d, d < 1, gets a nontrivial bound (row L35). `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` adds the asymptotics: the provable exponent is 1 + Θ(1 − d), between 1 + 0.58(1 − d) and 1 + (1 − d) near d = 1 (row L37). Code and data: `research/agents/claude/tport/`. Addendum (2026-10-28 15:21): `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` reviews the one-tape crossing-sequence notes (rows L38–L40): the bound also holds for nondeterministic machines, so it cannot separate P from NP; with sequential input access the UWI portfolio statement holds up to exponent 2, so the L34 barrier is specific to random access; beating N^2 on one tape would imply superlinear multitape lower bounds for SAT. P versus NP remains OPEN. Addendum (2026-11-04): `research/agents/claude/2026-11-04_CLAUDE_B3-VACUITY-0001.md` (log: `research/agents/claude/worst-case/LIVING_LOG.md`) proves that for any R with a known superpolynomial lower bound the B3 bridge is equivalent to P != NP, so B3 transport lemmas must fail for Resolution/PHP as a red-team gate; B3 is informative only for open-lower-bound systems. Additive; changes no schedules or allocations.

## Shared SIL/M22 ladder research handoff (2026-10-25 00:05 America/Los_Angeles)

At the next preflight ALL FIVE active roles should read `research/coordination/2026-10-25_0005_SIL_M22_RESOURCE_LADDER_FIVE_ROLE_HANDOFF.md`, the full `research/language/2026-10-25_0005_SIL_M22_PARAMETERIZED_RESOURCE_LADDER.md`, the reproducer `experiments/sil_m22/2026-10-25_0005_sil_m22_ladder.py` and exact raw data `results/raw/sil_m22/2026-10-25_0005_sil_m22_ladder_results.json`. Analyze the original signed (2,2) grammar, SIL E/P/S/CTX correctness, paired/unpaired `q,d` classification, FA5/VE5 example, and the fully charged adaptive parameterized resource ledger. Carry this evidence into the assigned direct-hardness or FLMV/resource-contradiction proof obligations; no claim of an unconditional decision-time lower bound, nor of an ARC edge, follows from the finite reduction trace. **This handoff is additive and changes no task schedules, agent count, or scientific allocation.**


## Latest user scientific allocation: ALL FIVE ARC/FLMV (2026-10-24 23:46 America/Los_Angeles)

This is the newest user direction and **supersedes the 23:25 Option A3/B2 allocation, all-UWI routing, and every older mixed allocation**. Keep exactly the five existing enabled hourly agents at :00/:12/:24/:36/:48; do not create, reactivate, disable, or reschedule tasks. All five roles work exclusively on the single ARC/FLMV simultaneous time--space contraction spine. UWI, M22, universal selectors, wrappers, circuit SAT, proof systems, direct potentials, and post-quantum ideas are supporting evidence only when an explicit mathematical link fills or falsifies an ARC proof arrow. The additive governance note is `research/governance/2026-10-24_2346_ALL_ARC_REFOCUS3.tex`; every active agent must read it at preflight.

The load-bearing target is a finite fully charged favorable route for cofinally many achievable integer diagonals into the strict FLMV box `t<241/200`, `s<11642479/23232400`, using one fixed uniform deterministic total exact ordinary-SAT decider per simultaneous pair in the matched indexed read-only-input random-access Turing-machine model. ARC-EDGE-90 and P versus NP remain **OPEN**. Preserve the retired status of the universal cosine endpoint, cross-machine resource borrowing, free semantic SAT answers, and source-only unconditional splitters.

## Latest user scientific allocation: THREE Option A, TWO Option B (2026-10-24 23:25 America/Los_Angeles)

This is the latest user direction and **supersedes ALL older five-ARC, all-UWI, and all-Option-A directives**, including the older "Latest user research allocation" heading below. Keep exactly five existing enabled hourly agents at :00/:12/:24/:36/:48 with no schedule or task-count changes. Three roles pursue Option A: LSPV-1 (:00) direct lower-bound lead; LSPV-2 (:12) signed-hypergraph hard instances; LSPV-3 (:24) general computational resources of an ideal adaptive, step-parameterized solver. Two roles pursue Option B: LSPV-4 (:36) FLMV and charged transport/contradiction; LSPV-5 (:48) independently audit FLMV and resource-accounting contradictions. The explicit complete instructions are in `research/governance/2026-10-24_2325_OPTION_A3_B2_ALLOCATION1.tex`; **every active agent must read that file at preflight**. Prior UWI/ARC artifacts remain reusable as supporting source material, not mutually exclusive primary assignments. Preserve project role ownership and original mathematical results; P versus NP and all unrestricted separation implications remain OPEN. This repository directive does **not** assert that scheduled automation prompts were successfully modified; scheduler permission may block a prompt update.


## Latest user research allocation: all five agents UWI-1 (2026-10-24 22:52 America/Los_Angeles)

The user's later instruction supersedes the 22:51 ARC/FLMV-only allocation: ALL FIVE existing active staggered research agents now focus on the single Universal Witness Insufficiency UWI-1 route, preserving the :00/:12/:24/:36/:48 schedules, current task count, verified prior theorems, scientific rigor, and role-owned writing safeguards. ARC/FLMV, M22, universal selectors, SIL/BOOL, WRAPPER, proof systems and direct potentials may supply exact supporting links only when they close or falsify a UWI obligation; they are not independent active spines. Every active agent must read `research/governance/2026-10-24_2252_ALL_UWI_REFOCUS2.tex` before substantive work. The exact UWI polynomial-boundedness equivalence is established; the common-SAT-input all-program lower bound and P versus NP remain OPEN. No schedules or tasks are created, reactivated or changed by this allocation.

Canonical repository: `j15marti/pnp`

Google Drive is no longer the primary write target for active LSPV reports. Write new reports directly to GitHub as LaTeX.

## Paths
- LSPV-1: `research/agents/lspv-1/YYYY-MM-DD_HHMM_LSPV-1_<RUN_ID>.tex`
- LSPV-2: `research/agents/lspv-2/YYYY-MM-DD_HHMM_LSPV-2_<RUN_ID>.tex`
- LSPV-3: `research/agents/lspv-3/YYYY-MM-DD_HHMM_LSPV-3_<RUN_ID>.tex`
- LSPV-4: `research/agents/lspv-4/YYYY-MM-DD_HHMM_LSPV-4_<RUN_ID>.tex`
- LSPV-5 MAIN: `research/main/YYYY-MM-DD_HHMM_MAIN_<RUN_ID>.tex`
- Governance changes: `research/governance/YYYY-MM-DD_HHMM_<CHANGE_ID>.tex`

## Post-quantum technique ledger

Every active LSPV run should consider whether one of the following post-quantum cryptography / cryptanalysis techniques is relevant to its current barrier. These are research prompts, not proof claims.

1. **Schur-square / componentwise-product distinguishers.**
   Our object `C_H^{*2}` is exactly a code Schur square. Consider shortening, puncturing, dualization, filtrations, and matched-random-code controls rather than only raw square dimension.

2. **Quadratic-form relation spaces.**
   Study the kernel of the multiplication/evaluation map and the rank spectrum of matrices representing quadratic relations. An unusually low-rank quadratic relation may reveal hidden structure even when total square dimension is large.

3. **Hilbert functions, syzygies, graded Betti numbers.**
   If degree-two square dimension saturates, test higher-order algebraic invariants and syzygies, as modern code-based cryptanalysis does.

4. **Lossiness / collision entropy.**
   For proof-to-node map `L:A -> F_acc`, consider the full collision distribution, not only maximum fiber. In particular track
   `Coll(L)=|{(y,y'):L(y)=L(y')}|`
   and the exact Cauchy-Schwarz bound
   `|im L| >= |A|^2 / Coll(L)`.
   Compare collision-effective entropy against `kappa+M`.

5. **Worst-case/average-case reduction architecture (LWE lesson).**
   Rather than forcing an arbitrary SAT algorithm to internally materialize a chosen resource, consider whether the resource can be externally extracted from black-box behavior of an arbitrary solver. Treat this as a CANDIDATE only; known NP worst-case/average-case barriers must be audited.

6. **Collision extraction / special soundness / collapse-binding lesson.**
   For reconstruction binding, prefer a construction-specific theorem of the form “two conflicting valid openings yield an explicit forbidden algebraic witness” over generic uniqueness/canonicalization. Cryptographic binding assumptions themselves are not admissible in an unconditional P-vs-NP proof.

7. **Hash/random-oracle methods.**
   Treat these as engineering/cryptographic analogies only unless an unconditional theorem survives removal of the hardness/random-oracle assumption.

For every PQ-derived idea, classify it as:
- EXACT OBJECT/THEOREM TRANSFER;
- ANALOGY/CANDIDATE needing a new bridge;
- FAILED TRANSFER.

Always ask whether the same structure is exploitable by an algorithm; hidden algebraic structure may be a weakness rather than a hardness source.

## Barrier-transfer literature preflight

Every active LSPV run must identify the **one or two major current obstacles** blocking its target and search current primary literature before substantive work.

In addition to direct complexity-theory literature, each run must ask whether the same structural type of obstacle has been solved elsewhere. Relevant transfer domains may include, when appropriate:

- electronics and circuit design: fan-out, signal integrity, clocking, locality, routing congestion, fault tolerance, error correction, synchronization, switching networks, memory hierarchy, VLSI area-time tradeoffs;
- control theory and dynamical systems: invariants, Lyapunov functions, state observability, controllability, dissipativity, barrier certificates, hybrid systems;
- coding theory: local decoding, list decoding, Schur/Hadamard powers, duality, rank growth, expander codes, locally testable codes;
- algebra and geometry: invariant theory, algebraic geometry, singularities, representation theory, matroids, algebraic combinatorics;
- topology and category theory: obstruction theory, cohomology, sheaves, descent/gluing, monodromy, compactness and local-to-global principles;
- optimization and operations research: duality, cutting planes, relaxations, integrality gaps, amortized potentials;
- distributed computing and communication: locality, consensus, lower bounds from communication cuts, message compression, fault models;
- proof complexity / logic: feasible interpolation, bounded arithmetic, proof search versus verification, canonical forms, switching and restriction techniques;
- information theory / statistical mechanics only when a real model-matched transfer is available.

The report must distinguish:
1. **directly transferable theorem**;
2. **useful structural analogy requiring a new transfer theorem**;
3. **misleading analogy / failed transfer**.

Do not import a result across models merely because the language sounds similar. State the exact object correspondence and the missing theorem needed for transfer.

## Mandatory corpus-wide reconciliation on every LSPV run

Every active LSPV run must review its own target in light of the **total current GitHub corpus**, not merely the immediately preceding report.

Before substantive work, the agent must:

1. enumerate or otherwise survey the current repository tree;
2. read root `main.tex`, `AGENTS.md`, `CODEX.md`, and `.codex/skills/pnp-research/SKILL.md`;
3. inspect all current task specifications under `tasks/`;
4. inspect the newest verified MAIN plus materially relevant historical MAIN snapshots;
5. inspect all LSPV-1..5 reports that bear on the active claim, including older reports when repository search shows the same theorem/route was attempted before;
6. inspect relevant `research/explorations/` components, especially the HEC / VSC-HEC / G-PPC-HEC / CRS-PPC / CCSPC causal branch when the arbitrary-algorithm bridge is relevant;
7. inspect governance notes and the experiment/result artifacts cited by active claims;
8. search repository content/history for duplicate formulations, contradictions, superseded assumptions, failed transfers, and retired routes;
9. distinguish what is newly proved from what was already in the corpus.

Every LSPV report must include explicit sections or entries for:

- **CORPUS REVIEWED**;
- **DUPLICATION / CONTRADICTION AUDIT**;
- **WHAT CHANGED RELATIVE TO ROOT MAIN**;
- **ADOPTED / REJECTED / RETIRED PRIOR COMPONENTS**;
- **STALE OR OVERSTATED CLAIMS FOUND**, if any.

"Total corpus review" does not mean mechanically rereading every byte of every historical file on every run. It means surveying the whole repository and reading every artifact materially relevant to the active claim, including older work surfaced by repository search. An agent may not rely only on peer summaries when the underlying report or data is available.

## Mandatory root `main.tex` reconciliation on every successful LSPV run

Every successful LSPV run must update root `main.tex` **in the same run** after its standalone report has been written and verified.

- LSPV-1 updates its marked LSPV-1 ownership region.
- LSPV-2 updates its marked LSPV-2 ownership region.
- LSPV-3 updates its marked LSPV-3 ownership region.
- LSPV-4 updates its marked LSPV-4 ownership region.
- LSPV-5 performs whole-document reconciliation and remains final synthesis arbiter.

Specialists must not edit other specialists' ownership regions or executive synthesis. They should summarize the current verified state of their specialty, including negative results and open arrows, rather than merely append the newest idea.

Required procedure:

1. verify the standalone report first;
2. refetch current root `main.tex` and its blob SHA;
3. reconcile the agent-owned region against the total corpus reviewed that run;
4. preserve all material outside the authorized region except an explicitly authorized global timestamp;
5. use the current SHA and resolve concurrent edits rather than overwriting them;
6. read root `main.tex` back from GitHub;
7. verify balanced ownership markers, explicit OPEN status while any load-bearing arrow is open, strict proof labels, and no silent strengthening.

A run is not complete until both the report and the authorized root `main.tex` reconciliation verify, unless a documented repository/write failure prevents the second write.

LSPV-5 must treat specialist edits as evidence-bearing inputs, not as final authority. Each LSPV-5 run must survey the total repository corpus and reconcile the executive summary, proof spine, status tables, barrier ledger, open targets, and references against all verified specialist changes.

## Peer write-failure diagnosis and repair

The predecessor-write check is not only a retry request. When a predecessor has no verified write, the current agent must attempt to diagnose **why** the write was blocked, using available automation state, GitHub history, target path state, and returned tool/error information.

Classify the failure when possible:

- **STALE REVISION / SHA CONFLICT:** refetch branch head/blob SHA and retry against current state.
- **PATH COLLISION:** if intended path now exists and verifies, treat as success; if partial/invalid, preserve body and write one fresh `-R1` path.
- **TRANSIENT API / CONNECTOR / RATE LIMIT / TIMEOUT:** preserve body, honor the timed retry rule, then retry once.
- **PERMISSION / REPOSITORY / BRANCH ERROR:** verify repository and branch identifiers; do not claim success; report the exact blocker.
- **PROMPT / PROCEDURE CONTRADICTION:** make the smallest write-procedure repair to the predecessor automation that resolves the contradiction. Do not alter the scientific target unless separately justified.
- **MALFORMED / EMPTY BODY:** if the predecessor body is available, preserve and rewrite it; if scientific content is missing, do not invent it.
- **CONCURRENT EDIT CONFLICT:** refetch current file and merge only the authorized ownership region.
- **UNKNOWN:** record the evidence available and the exact unresolved failure rather than guessing.

Agents are explicitly authorized to make the smallest technical repair to a peer's write procedure, path rule, retry rule, or stale revision handling when evidence supports it. Preserve schedules and scientific targets unless a separate governance reason exists.

If the same peer fails verified writes for two consecutive scheduled cycles, the next agent must escalate:
1. inspect the peer automation prompt for conflicting write instructions;
2. inspect GitHub path/branch conventions;
3. apply the smallest technical repair;
4. create a governance note describing failure evidence, repair, and rollback;
5. continue its own run.

Never “repair” a failed scientific write by reconstructing unrecorded mathematical claims from memory.

## Predecessor write-recovery preflight

Before **every** active LSPV run, check whether the immediately preceding agent in the stagger completed its most recent scheduled run with a verified GitHub write.

Predecessor order is cyclic:

- LSPV-1 checks LSPV-5.
- LSPV-2 checks LSPV-1.
- LSPV-3 checks LSPV-2.
- LSPV-4 checks LSPV-3.
- LSPV-5 checks LSPV-4.

A predecessor write counts as successful only if the newest report attributable to that scheduled run:
1. exists in the predecessor's canonical GitHub report directory;
2. is nonblank/substantive;
3. contains the expected report header and final verification sentinel; and
4. can be read back from GitHub.

If the predecessor's latest scheduled run lacks such a verified write, the current agent must **prompt that predecessor to retry the write** before beginning substantive research. This is a recovery instruction, not a request to rerun the research from scratch. Preserve the predecessor's existing research body if available; do not reconstruct missing scientific content from guesswork.

The recovery request must not block the current run. After issuing the retry instruction, continue the current agent's own research normally.

Do not create duplicate recovery files when a valid retry is already present. A later agent should judge success from the newest verified predecessor artifact, not merely from automation status text.

## Write retry timing

For every required GitHub report write:

1. Attempt the write normally.
2. If the write is blocked by a transient connector/API/revision/rate-limit style failure, preserve the exact same report body and status.
3. Wait approximately **30 seconds** before retrying when the execution environment permits an actual delay.
4. Retry exactly once after that delay.
5. Before retrying, refetch the intended path/repository state. If the intended artifact now exists and verifies, treat the write as successful and do not duplicate it.
6. If an actual timed wait is not available in the execution environment, do not fabricate one; perform the single retry at the next possible tool opportunity and record that the 30-second delay could not be enforced.
7. A second failure is a write failure, not a successful run. Remain enabled and let predecessor-recovery logic handle the next opportunity.

## Write protocol
1. Read the newest verified MAIN and newest verified peer reports from GitHub before substantive work.
2. Search primary literature before substantive claims.
3. Create one new UTF-8 XeLaTeX-compatible `.tex` file per successful run.
4. Never overwrite another agent's report.
5. Read the created file back from GitHub and verify a unique header marker and final sentinel.
6. A missing/blank file is a failed write, not success. Do not commit placeholders.
7. Preserve SAME_REALIZATION, exact quantifiers, model matching, hostile controls, wrapper tests, relativization/algebrization audits, and strict statuses.
8. LSPV-5 remains synthesis arbiter.

## Required markers
LSPV reports:
```
% LSPV-X REPORT::<RUN_ID>::<TIMESTAMP>
...
% END_OF_VERIFIED_REPORT::LSPV-X::<RUN_ID>
```

MAIN:
```
% MAIN SNAPSHOT — LSPV/RMV::<RUN_ID>::<TIMESTAMP>
...
% END_OF_VERIFIED_MAIN::<RUN_ID>
```

## Status discipline
Use only: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

One OPEN load-bearing arrow means P != NP is not proved.


## Living progress document: root `main.tex`

The one and only canonical living progress document is permanently **`/main.tex` at repository root**. Do not move it, rename it, or create a second `main.tex` anywhere in the repository.

The living document explains the overall state of the project for a human reader. It should remain polished, readable, and mathematically typeset, with:
- executive status and one highest-value target;
- a proof-spine diagram;
- PROVED/EXACT, OPEN, and FALSIFIED/RETIRED tables;
- exact equations and quantifiers;
- current exponent/parameter ledger;
- barrier and hostile-control ledger;
- concise specialist sections;
- links or paths to supporting reports/results.

For Overleaf and CI, compile repository-root `main.tex` directly.

Specialists LSPV-1..4 must update **only their explicitly marked ownership region on every successful run**:
`% BEGIN LSPV-X OWNED` through `% END LSPV-X OWNED`.
The update must reconcile the specialty against the total verified corpus reviewed during that run, not merely append the latest report. They must preserve all other text byte-for-byte except a global last-updated timestamp if the document explicitly authorizes it.

If `main.tex` exists but ownership markers are absent, LSPV-1..4 must not restructure it; report the condition and leave structural initialization to LSPV-5.

LSPV-5 owns the executive sections and whole-document reconciliation and must perform that reconciliation on every successful run after surveying the total current repository corpus. It may add/repair ownership markers, tables, diagrams, layout, cross-references, and remove or downgrade stale material when supported by verified evidence. Historical agent reports remain append-only snapshots; `main.tex` is intentionally edited in place.

After modifying `main.tex`, read it back from GitHub and verify that:
1. `P versus NP remains open` (or equivalent) is still explicit while any load-bearing arrow is OPEN;
2. ownership markers are balanced;
3. strict proof-status labels are preserved;
4. no verified result was silently strengthened;
5. LaTeX syntax remains structurally intact.


## Python runtime rule
- Every individual Python program or experiment invocation should be designed to finish in roughly **30 seconds or less**.
- If a computation is expected to exceed roughly 30 seconds, split it into multiple independent or checkpointed stages, parameter chunks, seeds, or input-size batches.
- Persist intermediate outputs so later stages resume from verified results rather than rerunning completed work.
- Do not increase a tool timeout as a substitute for decomposition.
- Reports must state the chunking strategy whenever a larger experiment is partitioned this way.
