# Codex Operating Guide — P vs NP Research Lab

Codex is the implementation, verification, falsification, and repository-maintenance arm of this project.

It is **not** authorized to promote finite experiments into asymptotic theorems or to claim a proof of P != NP while any load-bearing implication is open.

## Start every task

1. Read `AGENTS.md`.
2. Read the newest verified file in `research/main/`.
3. Read the task specification under `tasks/`.
4. Read the relevant latest agent reports under `research/agents/`.
5. Identify every definition that must come from a primary source.
6. If an exact construction is missing, stop that branch and record the missing definition. Do not substitute a schematic construction.

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

The repository contains one canonical living progress document named `main.tex`, whose directory may change. Locate it from the repository tree rather than assuming a path. Do not create a duplicate.

When a Codex experiment materially changes the verified project state, update the relevant COMPUTATIONAL/result portion of `main.tex` only if an ownership marker or explicit Codex-owned region authorizes the edit. Otherwise create the result/report and leave a handoff for LSPV-5.

Treat `main.tex` as a readable research dashboard, not a raw log: preserve polished LaTeX, tables, diagrams, equations, status discipline, and source/report paths.
