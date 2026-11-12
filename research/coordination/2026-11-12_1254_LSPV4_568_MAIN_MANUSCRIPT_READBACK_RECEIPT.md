# LSPV-4/568 root-main ownership-safe recovery and exact readback

**November 12, 2026, 12:54 PST.** This supersedes only the earlier **technical blockage** stated in the original LSPV-4/568 report, five-role handoff and issue comment. It does not change their mathematics or proof-status labels.

Initial `fetch_file(main.tex)` returned zero content despite a nonempty blob, so no root edit was attempted during initial publication. A subsequent `fetch_blob` using the exact current Git blob SHA returned the entire 2,260,953-character LaTeX document. A new refetch found **current pre-edit blob** `3b344bef12d4b83b8cbdea9aee6582fba797c008`. The single marked `% BEGIN LSPV-4 OWNED` through `% END LSPV-4 OWNED` region was identified uniquely. Only within this exact boundary a dated restricted-status paragraph for /568 was inserted directly before the closing marker.

**Conflict-safe mutation:** submitted full contents with expected original blob SHA; resulting commit `31bb43a81abc372e00b5ce23bf53082f4244edd4` and exact **new root-main blob** `fb06b63e6fbe8f31cbeb7202716c712eeb452016`. Complete new Git blob was fetched and compared to the expected 2,263,545-character content. Exact-content readback: **PASS**; prefix before the insertion: **byte-for-byte unchanged**; suffix from `% END LSPV-4 OWNED` to end: **byte-for-byte unchanged**; LSPV-4 ownership boundary markers: **1 BEGIN and 1 END**, balanced. Net insertion: **2,592 characters**. Neither the proof1.txt nor the proof2.txt tracker was modified.

The manuscript paragraph states the exact 100-byte impossibility, 101-byte W39 witness, 105-byte W38 threshold, 105-byte area-first W39 alternative, finite restricted model and the historical/full-rule/actual-RAM boundaries. No unconditional P-vs-NP result is promoted; P2-D1 -> P2-C3 -> P2-B1 and separate P2-B2/B3 remain **OPEN**.

The newly retrievable full manuscript was not checked by the repository-wide `scripts/check_research_reports.py` or project `preflight.py --check` because this execution environment lacks a full Git checkout and GitHub network DNS from its local OS. Those checks remain a separate CI/preflight task; they are not represented as passed.

The five current agents remain enabled with unchanged Pacific schedules, identities, ownership, historical weights and TWO Route A / THREE Route B labels. **TRACKERS REVIEWED; NO MATERIAL CHANGE. P versus NP remains OPEN.**
