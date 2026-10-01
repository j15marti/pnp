---
name: pnp-research
description: Conduct rigorous P-vs-NP and exact-SAT research in j15marti/pnp. Use for theorem development, literature review, falsification, computational experiments, LSPV specialist/red-team/synthesis work, proof-status reconciliation, or updates to the project's LaTeX research record.
---

# P vs NP Research Skill

Use this skill for substantive research work in the `j15marti/pnp` repository.

The purpose of this skill is **research discipline**, not a preferred proof strategy. It must help discover, test, falsify, formalize, or retire arguments without turning conjectures or finite experiments into theorem claims.

## Mandatory startup

1. Run:
   ```bash
   python .codex/skills/pnp-research/scripts/preflight.py
   ```
2. Read, in this order:
   - repository-root `main.tex`;
   - `AGENTS.md`;
   - `CODEX.md`;
   - the newest relevant timestamped reports under `research/main/` and `research/agents/`;
   - the relevant task under `tasks/`, when one exists.
3. Determine the run mode from the task:
   - `structure`
   - `product-span`
   - `reconstruction`
   - `red-team`
   - `synthesis`
   - `experiment`
4. Read `references/modes.md` for the selected mode.
5. State internally before doing substantive work:
   - the single target;
   - the exact quantifier prefix;
   - the computation/model assumptions;
   - the SAME_REALIZATION object(s);
   - the weakest theorem that would materially advance the target.

If an exact construction or theorem definition needed for the task is missing, record the missing definition and stop that branch. Do not silently replace it with a schematic surrogate.

## Research loop

Follow this order unless the task genuinely requires another dependency order:

1. **STATE** — recover the current verified project state.
2. **TARGET** — identify one load-bearing arrow or one explicit falsification target.
3. **LITERATURE** — search primary literature before relying on a substantive theorem.
4. **FORMALIZE** — write exact definitions, quantifiers, model, parameters, and claimed implication.
5. **FALSIFY FIRST** — attack the weakest point before extending the proof.
6. **TEST** — when finite computation can clarify the claim, implement a reproducible experiment.
7. **BARRIER AUDIT** — relativization, algebrization, wrappers, model transfer, and Natural Proofs when applicable.
8. **STATUS** — assign only an allowed status.
9. **COMMIT** — write code/data/report separately enough to audit.
10. **HANDOFF** — end with one concrete next target.

Read `references/research-protocol.md` for the full guard and promotion checklist.

## Allowed proof statuses

Use only:

- `PROVED/EXACT`
- `KNOWN THEOREM`
- `COMPUTATIONAL`
- `CONDITIONAL`
- `CANDIDATE`
- `OPEN`
- `FALSIFIED/RETIRED`

Finite experiments are `COMPUTATIONAL` unless accompanied by a complete symbolic proof.

One `OPEN` load-bearing arrow means (P\neq NP) is not proved.

## Permanent guards

Never infer unrestricted runtime directly from:

- semantic multiplicity;
- number of candidate witnesses;
- formula/backdoor/treewidth/incidence geometry;
- representation size;
- proof-system size;
- communication complexity;
- circuit size in a restricted model;
- existence of a certificate/decomposition;
- a lower bound on an algorithm family rather than all relevant algorithms.

Keep distinct:

[
\text{existence}\neq\text{acquisition}\neq\text{verification}\neq\text{decision cost},
]

and

[
\text{semantic object}\neq\text{machine state}\neq\text{runtime}.
]

Do not invert quantifiers such as
[
\forall A\,\exists F_A
quad\not\Rightarrow\quad
\exists F\,\forall A.
]

Time, space, source, witness, extracted object, and lower-bound resource must refer to the same declared realization unless an explicit model-preserving transformation is proved and charged.

## Mandatory hostile controls

Apply the relevant subset of these before treating a resource as serious:

- Horn and dual-Horn;
- 2-SAT/Krom;
- affine/XOR/Tseitin with Gaussian elimination;
- bounded treewidth / dynamic programming;
- independent products;
- renaming and variable complementation;
- padding and auxiliary variables;
- compact alternative representations;
- DEAD / COPY / DELAY / INTERP / RECOMP wrappers;
- maximal semantic oracle;
- algebraic oracle / low-degree extension access.

A candidate invariant that makes an easy control falsely expensive is invalid unless the discrepancy is formally explained.

## Literature discipline

Prefer original papers and authoritative theorem statements.

For every theorem used materially, record:

- exact model;
- quantifiers;
- input measure;
- resource measure;
- uniformity/nonuniformity assumptions;
- hypotheses;
- conclusion;
- what the theorem does **not** imply for this project.

If the task is based on repository or user-provided sources, preserve their terminology and framing. Do not silently repair a source gap from memory. Outside literature may be added only as clearly distinguished verification or expansion.

## Computational discipline

For every experiment record:

- exact code revision;
- input parameters;
- random seed if any;
- exhaustive vs randomized vs heuristic;
- raw machine-readable output path;
- controls run;
- limitations.

Prefer code under `src/pnp_lab/`, runners under `experiments/`, immutable data under `results/raw/`, and derived summaries under `results/summaries/`.

Search for the smallest counterexample before searching for supporting examples.

## Proof-promotion gate

Do not mark a new project claim `PROVED/EXACT` unless all of the following are present:

1. exact theorem statement;
2. exact quantifiers;
3. declared machine/model;
4. complete proof;
5. dependency list;
6. SAME_REALIZATION audit where resources are joint;
7. easy-family hostile controls;
8. wrapper/representation audit where relevant;
9. relativization audit;
10. algebrization audit when relevant;
11. Natural Proofs audit when a constructive circuit property is used;
12. independent red-team review or an explicit note that such review is still pending.

If item 12 is pending, keep the result below final promotion in the living synthesis unless existing project governance explicitly allows otherwise.

## Repository writes

The one canonical living synthesis is repository-root `main.tex`. Never move it or create another `main.tex`.

- LSPV-1 may edit only its marked ownership region.
- LSPV-2 may edit only its marked ownership region.
- LSPV-3 may edit only its marked ownership region.
- LSPV-4 may edit only its marked ownership region.
- LSPV-5 owns whole-document reconciliation.
- Codex experiment work should normally create results/reports and hand off to LSPV-5 rather than rewriting executive conclusions.

Timestamped reports are append-only historical records.

Use `assets/report-template.tex` when a new standalone research report is needed.

After changing `main.tex` or a timestamped report, run:

```bash
python scripts/check_research_reports.py
python .codex/skills/pnp-research/scripts/preflight.py --check
```

Run relevant unit tests before committing computational results.

## Definition of done

A successful run leaves:

- one sharply stated result, counterexample, or narrowed open arrow;
- an allowed proof status;
- reproducible evidence when computation was used;
- an explicit barrier/hostile-control result;
- no silently strengthened claim;
- one next target;
- repository paths for every created artifact.

A reproducible falsification or route retirement is a successful outcome.
