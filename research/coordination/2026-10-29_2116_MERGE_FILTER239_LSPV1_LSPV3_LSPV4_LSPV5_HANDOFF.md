# MERGE-FILTER239: LSPV-2 additive issue #2 handoff

**Date:** 2026-10-29 21:16 America/Los_Angeles. **Owner:** LSPV-2. **Issue:** https://github.com/j15marti/pnp/issues/2. **Task identity/schedule:** unchanged. **P versus NP:** OPEN.

## Status and precise scope

**PROVED/EXACT, RESTRICTED, independently review before promotion:** For every integer k >= 2, the connected proper 3-CNF

    F_k = AND_{r=1}^k [(x_r OR a OR b) AND (NOT x_r OR a OR b)]

has all source clause-equities Q_j = 0, yet k non-tautological opposite-occurrence resolvent *occurrences* all equal (a OR b). The raw pair sum of 2^{-width} is k/4, while the exact union density of the forbidden full-assignment cubes is 1/4. The ratio k is unbounded. These F_k are **not** exact signed (2,2); no lower-bound or family transport claim is made.

**KNOWN THEOREM, independently proved and computationally certified:** For retained opposite parent clauses (x OR A) and (NOT x OR B), if A and B have no shared *signed* literal and their resolvent is non-tautological, then adding that resolvent does not change the conflict/nonconflict or complete forced-literal set of fully saturated UP at any partial assignment. This is non-merge / non-empowering resolution from Babka et al., *Complexity issues related to propagation completeness*, Artificial Intelligence 203 (2013), Lemma 3.3, DOI 10.1016/j.artint.2013.07.006. It is **not** a novel theorem. All retained-parent non-merge resolvents can be removed together from the one-step closure without changing UP saturation, even when merge resolvents remain. This says nothing about their separate use for proof construction, literal scoring, or after deleting parent clauses.

**FALSIFIED/RETIRED:** Raw additive opposite-pair weight as lower bound for distinct forbidden-assignment density or per-clause source equity. Likewise, counting all nonmerge one-step resolvents as new UP pruning certificates is incorrect.

## Computational controls

The script generates 39 original CNFs, including the connected strict signed exact22 SAT 3-variable parity quartet, 6- and 9-variable cyclic SAT sources, fixed connected strict22 15-variable W1 UNSAT and S SAT sources. These are independently enumerated for original labels; exact22 and connectivity checked. Total 160,566 finite assertions/checks reported in the JSON; 24 seeded random general 3-CNFs and Horn/2SAT/overlap controls also included. Strict22 facts are not inherited from non-strict descendants.

Six deterministic source-authenticated solver strategies were executed with each run's own start-to-finish elapsed time, Python tracemalloc peak, source scans, UP scans, failed branch/probe counts, cache reads, and output verification. The *selected primitive-work proxy* does not count all Python hash/list operations, so do not confuse it with exact TM time. Corpus totals (nodes / selected work): baseline UP 205 / 21,509; all first-order resolvents 181 / 46,319; merge-only resolvents 181 / 36,754; budgeted shared-support 185 / 35,755; failed-literal probing 169 / 30,481; complementary whole-assignment trials then UP 92 / 16,168. Merge-only preserves all 181 nodes while removing 20.65% of selected work relative to all-resolvents, but exceeds baseline source-only UP cost. No asymptotic advantage inferred.

On a 4-variable merge control, partial prefix (u=0,v=0) leaves original UP with x,a unset; after verified resolvent a OR u OR v, a=1 is forced, giving contextual unset-variable potential decrease 1. The same calculation includes discovery, UP scanning and verification. In contrast, disjoint-support opposite parents cannot add saturated-UP deductions. Complement N0,N1,N2,N3 / E,D and source occurrences x_{i,j} were independently checked by full assignment and complementation.

## Reproducibility/provenance

- `research/agents/lspv-2/2026-10-29_2116_LSPV-2_MERGE_FILTER239.tex` (complete proof; bibliography in `.bib`).
- `research/agents/lspv-2/2026-10-29_2116_LSPV-2_MERGE_FILTER239_repro.py`: stdlib Python, deterministic seed 20261029; SHA-256 `defbac55b36cf1408a6993d89d3ad488df7cce12e782a3b53a7675efab7ec663`.
- `research/agents/lspv-2/2026-10-29_2116_LSPV-2_MERGE_FILTER239_summary.json`: source-derived aggregate raw results; SHA-256 `da97a1d2d42234f27d9ac22b3f5efb41a7760c362a23e1532be23a58a27532e6`.
- Full detailed 39-instance per-source raw JSON SHA-256 `afbcc429c4e19bf737d523467dfa8d9a8e7d95885861692c73051e1a1424a7b6` (over 500 KB) is preserved in the research Library and downloadable ZIP, regardless of whether the connector permits the large GitHub upload.

**Primary prior sources actually inspected:** `arminbiere/cadical/src/elim.cpp` blob `c401152c7a733803d0b407d98e8a295ab44f7e99`; `arminbiere/cadical/src/probe.cpp` blob `c2942702647595ff32de5429bbc188729c8a7d0b`; `msoos/cryptominisat/src/occsimplifier.cpp` blob `daa726fb6e3d9e2308707b9d80b99f79ccb72738`; W1 strict22 source `j15marti/pnp/research/agents/lspv-5/2026-10-28_2048_W1-RING-TRANSFER-REFEREE188_repro.py` blob `f4a467c98ccfe0c3e17dee2913b4ed0e8b50a123`. First issue handoff blob `7d84e5312230c3b57bdcbe763ac05f1050eea6c5`. Supplementary primary sources: Atserias-Fichte-Thurley (JAIR 2011), Fleury-Biere (FMSD 2023), Li et al. (AI 2020). All are cited in the LaTeX report.

## Role-specific next actions

LSPV-1: decide how to define non-double-counted marginal forbidden-prefix potential with UP saturation and adaptive discovery charged. LSPV-2: construct quota-preserving connected strict22 overlapping-merge families with controlled Q_j and repeat full SAT/UNSAT pairing; do not extrapolate F_k. LSPV-3: quantify the index-building cost and physical work/peak-space savings for skipped non-merge pairs in RAM and sequential tape separately. LSPV-4: independently break the non-merge saturation lemma with short prefix controls, verify source-level complement profiles, and challenge k/4 to 1/4 ratio assumptions. LSPV-5: represent merge-only resolvent DAG without dropping needed source parents, and compare XOR/2SAT/Horn alternative shortcuts.

**Main manuscript:** LSPV-2 ownership region only, after report verification, with fresh blob SHA and readback. If unavailable, do not fabricate its content; record PENDING with exact reason. All schedules/states unchanged.