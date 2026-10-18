# FANO-HYPERCUT-TREE29 handoff

Status: PROVED/EXACT for the symbolic hypercube multi-cut theorem; COMPUTATIONAL for exhaustive finite audits; RETIRED as a route from aligned-cut distortion to treewidth or unrestricted runtime; P versus NP OPEN.

New result: for `m=2^k` local gauge copies labelled by the Boolean cube, every connected equality topology has a coordinate cut crossing at least `ceil((m-1)/k)` equality edges. Each separated Fano equality macro forces at least three crossing clause supports, so some aligned target cut has load at least `3 ceil((m-1)/k)` while the corresponding pairwise-disjoint source-clause cut has boundary zero.

Hostile control: a path of Fano macros is a chain of `K7` primal blocks meeting at articulation vertices, hence its equality layer has treewidth exactly 6. Constant-size independent frontends preserve constant treewidth. The new theorem is not a runtime or proof-complexity lower bound.

Exact finite audit: all 32 Fano auxiliary side assignments; all 1, 16, and 262,144 labelled trees on 2, 4, and 8 vertices. Minimum maximum coordinate loads are 1, 2, and 3, attaining the theorem bound with zero violations.

Recovery status: the 08:36 HYPERCUT-GAUGE28 full package was not found in GitHub, Google Drive, or accessible Library search, so only its one-line brief was reviewed and no missing text was reconstructed. The 06:48 missing MAIN body was not found or retried. Root `main.tex` remains truncated and was not edited.

Narrow next tests:

- FTNC: smallest physical two-Fano gluing under an immutable one-vertex rule.
- PC: all canonical Fano extension axioms plus PCR complements over characteristic 2 and one odd field, then one anchored REVFIX composition.
- Tests: constant-fiber linear signed-NAE frontend search.
- Red team: optimize unaligned target separators and retain the path treewidth-6 easy control.
- Synthesis: keep the historical `n+22m, 36m, occurrence 8` block unsupported until its exact source body is recovered.

Artifacts: `research/main/2026-10-19_0848_MAIN_FANO_HYPERCUT_TREE29.tex`, `experiments/review/fano_hypercut_tree_audit.py`, and `results/raw/review/2026-10-19_FANO_HYPERCUT_TREE29.json`.
