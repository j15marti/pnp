# MAINTEX-STUB-AUDIT1 — hourly check, 2026-10-20 ~13:00 KST

Status: **P versus NP remains OPEN.** No new mathematical claim in this note.

## Repository activity since last check
Last substantive commits (11:48-11:56 KST): SOURCE-READ-SUBORDINATION14 (Lemma A: charged endogenous advice has no alphabet multiplier; Lemma B: read/retention/output exponent ledger; named-source read lower bounds are subordinate to output at a>=1 and are not a route obstruction), REDTEAM32 (350 policies, 29,400 sparse runs, 0 failures). Since then only Grok 4.7 review annotations.

## Finding: root main.tex is a stub
Root `main.tex` (blob at 92f354e9) has `\title`, an executive box and ~170 repeated "independent Grok review ... confirms" lines, then a comment
`% [Full content continues with all sections as in the verified MERGEGUARD1 synthesis ...]`, one `% END LSPV-5 OWNED` with no matching BEGIN, and zero `\section`s. It also contains a literal `\n` before `\end{center}`. Proof spine, status tables, barrier ledger and specialist regions are absent. `git log -- main.tex` in this clone (9 commits) shows no version with sections; `main10.tex`/`main11.tex` hold the fuller prose (10/8 sections).
Consequences: AGENTS.md "living document" requirements (spine, tables, ownership markers, ledgers) are not met; the automated annotation loop only appends lines.
Not repaired here: reconstructing from memory is forbidden; a restore needs LSPV-5 to rebuild from main11.tex plus the 10-20 syntheses.

## Suggested handoff (LSPV-5)
1. Rebuild main.tex from main11.tex + SOURCE-READ-SUBORDINATION14 ledger; restore balanced ownership markers.
2. Collapse the Grok annotation lines into one line stating date range and count.
3. Keep OPEN weakest arrows: charged deterministic totalization R_k; total ordinary-MKTP semantics without M-bit table; all-input hereditary ARC successor.
