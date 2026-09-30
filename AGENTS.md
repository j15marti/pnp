# Agent GitHub Writing Protocol

Canonical repository: `j15marti/pnp`

Google Drive is no longer the primary write target for active LSPV reports. Write new reports directly to GitHub as LaTeX.

## Paths
- LSPV-1: `research/agents/lspv-1/YYYY-MM-DD_HHMM_LSPV-1_<RUN_ID>.tex`
- LSPV-2: `research/agents/lspv-2/YYYY-MM-DD_HHMM_LSPV-2_<RUN_ID>.tex`
- LSPV-3: `research/agents/lspv-3/YYYY-MM-DD_HHMM_LSPV-3_<RUN_ID>.tex`
- LSPV-4: `research/agents/lspv-4/YYYY-MM-DD_HHMM_LSPV-4_<RUN_ID>.tex`
- LSPV-5 MAIN: `research/main/YYYY-MM-DD_HHMM_MAIN_<RUN_ID>.tex`
- Governance changes: `research/governance/YYYY-MM-DD_HHMM_<CHANGE_ID>.tex`

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


## Living progress document: `main.tex`

There is exactly one canonical living progress document named `main.tex` somewhere in the repository tree. Its directory may change. **Locate it from the current GitHub tree on every run; never assume a fixed path and never create a second `main.tex`.**

The living document explains the overall state of the project for a human reader. It should remain polished, readable, and mathematically typeset, with:
- executive status and one highest-value target;
- a proof-spine diagram;
- PROVED/EXACT, OPEN, and FALSIFIED/RETIRED tables;
- exact equations and quantifiers;
- current exponent/parameter ledger;
- barrier and hostile-control ledger;
- concise specialist sections;
- links or paths to supporting reports/results.

Specialists LSPV-1..4 may edit **only their explicitly marked ownership region**:
`% BEGIN LSPV-X OWNED` through `% END LSPV-X OWNED`.
They must preserve all other text byte-for-byte except a global last-updated timestamp if the document explicitly authorizes it.

If `main.tex` exists but ownership markers are absent, LSPV-1..4 must not restructure it; report the condition and leave structural initialization to LSPV-5.

LSPV-5 owns the executive sections and whole-document reconciliation. It may add/repair ownership markers, tables, diagrams, layout, cross-references, and remove stale material when supported by verified reports. Historical agent reports remain append-only snapshots; `main.tex` is intentionally edited in place.

After modifying `main.tex`, read it back from GitHub and verify that:
1. `P versus NP remains open` (or equivalent) is still explicit while any load-bearing arrow is OPEN;
2. ownership markers are balanced;
3. strict proof-status labels are preserved;
4. no verified result was silently strengthened;
5. LaTeX syntax remains structurally intact.
