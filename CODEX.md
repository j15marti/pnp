# Codex Operating Guide — P vs NP Research Lab

Codex is the implementation, verification, falsification, and repository-maintenance arm of this project.

It is **not** authorized to promote finite experiments into asymptotic theorems or to claim a proof of P != NP while any load-bearing implication is open.

## Required project skill

For any substantive P-vs-NP / exact-SAT research task in this repository, invoke the repo-scoped skill:

`$pnp-research`

located at `.codex/skills/pnp-research/SKILL.md`.

The skill owns the shared research workflow: state recovery, exact quantifiers, falsification-first testing, hostile controls, barrier audits, proof-status discipline, experiment provenance, and report/main.tex write rules. `CODEX.md` remains the repository-level operating guide; the skill is the reusable execution protocol.

## Start every task

1. Invoke `$pnp-research` and run its preflight.
2. Read `AGENTS.md` and repository-root `main.tex`.
3. Read the newest verified file in `research/main/`.
4. Read the task specification under `tasks/`.
5. Read the relevant latest agent reports under `research/agents/`.
6. Identify every definition that must come from a primary source.
7. If an exact construction is missing, stop that branch and record the missing definition. Do not substitute a schematic construction.

## Corpus-wide reconciliation

For every substantive P-vs-NP task, survey the current repository tree before new work. Do not assume the newest report contains the whole project state.

At minimum, inspect root `main.tex`, current task files, newest and relevant historical MAIN snapshots, materially relevant LSPV reports across all specialists, active `research/explorations/` components (including CRS-PPC and CCSPC when relevant), governance notes, and the code/data/result artifacts cited by the claims under review. Use repository search/history to locate prior formulations, counterexamples, contradictions, and retired routes.

Every research output should state what was already known, what changed, and whether any root-MAIN statement became stale.

For LSPV work, a successful run must also reconcile root `main.tex` in the same run according to the ownership rules in `AGENTS.md`. LSPV-5 remains final arbiter of whole-document synthesis.

## Research discipline

Every computational result must record:
- exact code revision / commit;
- parameters and random seed;
- whether the result is symbolic, exhaustive, randomized, or heuristic;
- raw machine-readable output;
- the hostile controls run;
- limitations;
- proof status.

Allowed statuses:
`PROVED/EXACT`, `KNOWN THEOREM`, `COMPUTATIONAL`, `CONDITIONAL`, `CANDIDATE`, `OPEN`, `FALSIFIED/RETIRED`.

Finite evidence is always `COMPUTATIONAL` unless accompanied by a complete proof.

## Preferred workflow

Create a branch or worktree per task. Keep code, raw results, and interpretation separable.

Typical commands:

```bash
python -m pip install -e '.[dev]'
pytest -q
python scripts/check_research_reports.py
python experiments/product_span/run.py --toy-affine --source-bits 4 --outputs 8 --seed 1
```

## Current priority tasks

1. `tasks/TASK-001-su-vms-product-span.md`
2. `tasks/TASK-002-hostile-controls.md`
3. `tasks/TASK-003-primitive-trace-battery.md`
4. `tasks/TASK-004_HEC-static-to-online-compiler.md`
5. `tasks/TASK-005_CRS-PPC-bridge-theorems.md`

The reusable CCSPC component is recorded under
`research/explorations/random-challenge/2026-10-01_CCSPC1_CANONICAL-CAUSAL-SAT-POINTER-CASCADE.md`.

Do not start TASK-001's exact SU/vMS implementation until the primary-source definitions required by the task are present in the repository or otherwise explicitly supplied.

## Output conventions

- reusable code: `src/pnp_lab/`
- task-specific runners: `experiments/<task>/`
- immutable raw outputs: `results/raw/`
- concise derived summaries: `results/summaries/`
- research interpretations: new LaTeX reports under the appropriate `research/` path
- task specifications: `tasks/`

A negative result, counterexample, or route retirement is a successful research outcome when reproducible.


## Living project document

The canonical living progress document is permanently `/main.tex` at repository root. Do not move it, rename it, or create another `main.tex`.

When a Codex experiment materially changes the verified project state, update the relevant COMPUTATIONAL/result portion of root `main.tex` only if an ownership marker or explicit Codex-owned region authorizes the edit. Otherwise create the result/report and leave a handoff for LSPV-5. For LSPV-1..4 runs, the owned specialist region must be reconciled every successful run; for LSPV-5, whole-document reconciliation is mandatory every successful run.

Treat `main.tex` as a readable research dashboard, not a raw log: preserve polished LaTeX, tables, diagrams, equations, status discipline, and source/report paths.
