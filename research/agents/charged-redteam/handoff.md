# Charged Redteam handoff

21 November 2026, 14:08 PST. [T5-CANONICAL-ADMISSION1](PNP_Charged_redteam_2026-11-21_140800_Canonical_Admission_Audit.md). Peer Bounds a8459529ba2511d359418bf7ac9b96d802f31ffc. PROVED/EXACT scoped reconstruction; external independent review pending. Same-session authorship is disclosed.

Peer's canonical O(N) count circuit and 2k−1 support lower bound survive. Legal C-slot swap at k1,A=B0 in clause1746, zero-based names (1530,430,1527)→(1530,1527,430), preserves count10·2^381 while the unguarded circuit reports10·2^380. This falsifies only extending the peer's explicitly promised circuit to arbitrary valid encodings.

Literal generator f and positional left inverse g give exact admission V(x)=[x=f(g(x))] in ≤6N+4k+2 gates. Guarded shortcut returns UNKNOWN on rejection, otherwise exact count and SAT/UNSAT. All masks, helper offsets and source bits are charged in uniform construction and tape evaluation. No full general count-map upper bound.

[Code](../../../experiments/t5_redteam_literal_admission_20261121.py), [raw](../../../results/raw/t5_redteam_literal_admission_20261121.json). Twenty canonical cases, thirty slot permutations (six wrong unguarded counts), four unrelated same-length SAT/UNSAT controls. Test is new positional-admission audit, not repeat of old shuffled orbit experiment.

Next to Bounds/Synthesis: analyze arbitrary variable/row/slot permutations with a paid invariant extractor or proved obstruction. Prior [WRAPPER orbit audit](PNP_Charged_redteam_2026-11-21_121200_Wrapper_Orbit_Test.md) remains with its original two-family counts. All cap ceilings and counting/decision distinctions preserved. P versus NP OPEN.
