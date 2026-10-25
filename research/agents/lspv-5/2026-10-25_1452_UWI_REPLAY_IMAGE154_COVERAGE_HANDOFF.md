# UWI-REPLAY-IMAGE154 — Role 5 additive coverage / rejection handoff

Status: **PROVED/EXACT** replay theorem; **COMPUTATIONAL** finite audit; UWI common-input lower bound and P versus NP remain **OPEN**.

## Exact accepted lemma

For a fixed public generator/witness pair (G,W) and a polynomially readable formula header, if every family member of length N has an opening of at most c log2(N+2) bits and each opening can be generated and witness-lifted in polynomial work, one fixed constant-description program enumerates all polynomially many openings, compares full ordinary encodings, and outputs a verified witness. Thus H(F) is polynomial on the whole generated family for all sufficiently large N. Generator injectivity is unnecessary. If a fixed polynomial extractor recovers an opening from F, the seed-length bound is unnecessary.

## Rejection ledger

- **FALSIFIED/RETIRED as UWI hard-family mechanisms:** fixed public seed, source-readable planted witness, polynomially recoverable opening, or public O(log N)-seed witness-extensible generation.
- **FALSIFIED/RETIRED inference:** forall p exists F_p implies the required exists F forall p.
- **FALSIFIED/RETIRED transfer:** DNNF/proof size, SOS degree, range sparsity, switching/routing, hash/timer, entropy, physical energy, or large solution space implies work for every eligible witness program.
- **OPEN:** one satisfiable formula defeating the entire eligible portfolio at each fixed polynomial budget.

## Resource ledger

The replay program pays parsing, every failed seed, generator work, full source/candidate comparisons, source/workspace reads, unchanged and changed writes, control/addressing, witness output, and verification. Peak writable storage is seed/address state plus actual generator/witness workspace and at most one candidate/witness buffer. Full-state flips, physical switching, circuit size, and cumulative bit-time remain distinct.

## Reproducibility

- Report: research/agents/lspv-5/2026-10-25_1452_LSPV-5_UWI_REPLAY_IMAGE154.tex
- Script: research/agents/lspv-5/2026-10-25_1452_UWI_REPLAY_IMAGE154_audit.py
- Raw: research/agents/lspv-5/2026-10-25_1452_UWI_REPLAY_IMAGE154_results.json
- Executed in 0.76 s; 27 assertion-accounted checks; four planted SAT cases, one exhaustive UNSAT false-match control; zero failures.

## Corpus and source coverage

Full original read: corrected UWI PDF (18 pages / 911 extracted lines). Full Drive reads: SIM-2-0010, NONALG-0003, SIM-5-0009, SIM-3-0012. Targeted GitHub originals: UWI governance/reallocation, ARCARCHIVECURVE90 UWI recovery, STATUSQUOTE8, AFFINE-RESIDUAL-RANK1, CC-0004, LB-0002, POLYMASK1, current root/protocol/tasks, and newest verified Role 4 predecessor. Primary literature: Ko--Orponen--Schöning--Watanabe instance complexity, Levin universal search, Fortnow--Kummer resource-bounded instance complexity. This is targeted reconciliation, not a new full corpus census.

## Contradiction and next artifact

The repository ARC-only governance timestamped 22:51 Los Angeles is superseded for routing by the user's later 22:52 UWI-only instruction. Historical ARC/M22 theorems are preserved only as potential explicit UWI support.

Next inspect the original user-supplied PROOF_NOTE(1).md if directly accessible, and audit the first post-redirection peer reports. Every proposed generated hard family should provide a replay-exclusion certificate before any lower-bound claim.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::UWI-REPLAY-IMAGE154 -->
