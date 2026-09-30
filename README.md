# P vs NP Research Repository

Canonical research log for the current LSPV / RMV program.

## Status
**P vs NP remains open.** No report should be interpreted as a proof unless every load-bearing implication is explicitly proved and independently verified.

## Structure
- `research/main/` — synthesis snapshots / shortest surviving proof spine
- `research/agents/lspv-1/` — exact SU/vMS/RMV encoder structure
- `research/agents/lspv-2/` — product-span / separator / quadratic-rank work
- `research/agents/lspv-3/` — reconstruction / quantifiers / exponent accounting
- `research/agents/lspv-4/` — hostile red-team work
- `research/agents/lspv-5/` — optional non-MAIN synthesis-agent reports
- `research/agents/grok/` — BOOL / computational explorer reports
- `research/agents/claude/` — independent verification
- `research/explorations/battery-mana/` — ratchet / battery / mana work
- `research/explorations/sequential-tape/` — primitive-trace / tape transport work
- `research/governance/` — agent-instruction changes / rollback records
- `research/retired/` — archived retired routes

## Format
New research reports are UTF-8 XeLaTeX-compatible `.tex` files. Every report should include exact quantifiers, literature reviewed, experiments, hostile controls, barrier audits, strict proof-status labels, missing implications, and one concrete next target.

Blank placeholder reports are not successful runs. If a write fails, record the failure in the automation result rather than committing an empty file.

## Initial migration
The initial migration contains the latest verified MAIN synthesis, latest verified LSPV-1 through LSPV-4 reports, current GROK/CLAUDE material, and the battery/tape investigations. Blank Google Drive print failures were intentionally excluded.


## Living progress document

The project maintains one living LaTeX status document at **repository-root `main.tex`**. This path is permanent and is the Overleaf/CI entry point. Timestamped files under `research/main/` remain historical snapshots.


For Overleaf, set the Main document to repository-root `main.tex`. The living document is pdfLaTeX-compatible.
