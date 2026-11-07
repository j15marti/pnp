# LSPV-2/458 five-role handoff, 2026-11-06 19:09 PST

**Role allocation unchanged:** two Route A (LSPV-2 construction, LSPV-4 resources), three Route B (LSPV-1 lead, LSPV-3 certificates, LSPV-5 red team). Historical R_mix341 grammar, weights, schedules, task IDs, titles and enabled states unchanged. P versus NP OPEN.

**PROVED/RESTRICTED:** For boundary width w every set S subseteq {0,1}^w is the existential projection of an original signed *proper width-three* CNF of O(w 2^w) clauses and O(w^2 2^w) encoded bits, even when padded to identical source lengths. Any one-pass deterministic fixed-b-bit summary whose original prefix becomes permanently inaccessible, and which must answer SAT against *every* strictly proper 3-CNF suffix, requires b >= 2^w; a truth bitmap attains this. Proof is via forbidden-assignment clause gadgets and point-pin distinguishing suffixes. This is NOT a machine-space lower bound if read-only indexed original input can be revisited.

**COMPUTATIONAL:** Exhaustive w=1,2,3 subset projections (276 cases); proper ternary OR gadgets through width 6; suffix pin controls through width 4; 16 original signed K4 Tseitin labels. 7,937 Python checks PASS, independent JavaScript 8,322 PASS. The published independent JS Git blob c62fa906327246c9cc762dd727e2f0ba3ac2e1ba matches locally executed bytes. No native FLMV or historical proof checker run.

**KNOWN HARD FAMILY:** Cubic-expander odd-charge Tseitin 3-CNF, 4H clauses and length Theta(H log H), exponential size only in ordinary DAG Resolution (Urquhart 1987, Ben-Sasson/Wigderson 2001). Algebraic GF(2) charge-parity shortcut needs one semantic bit on authenticated connected graphs, showing that large frontier width by itself is not arbitrary SAT hardness.

**Relevant proof trackers:** [P1-S3], [P2-A4] restricted controls; load-bearing [P2-A2], [P2-A5], [P1-01], [P1-04] unchanged OPEN. Update [P2-A4] only if current-head conflict-safe complete-file write/readback succeeds, otherwise write TRACKERS REVIEWED; NO MATERIAL CHANGE and record blocker.

**Artifacts:** research/agents/lspv-2/2026-11-06_1909_LSPV2_TIGHT_ONEPASS_FRONTIER_STATE458.md, experiments/arc/lspv2_458_independent.js, results/raw/arc/2026-11-06_1909_LSPV2_FRONTIER_STATE458_summary.json. Local reproduction archive contains complete Python producer and independent JS.

**Remaining cross-role target:** LSPV-4 should test whether retaining 2^w messages versus rereading original input improves full FLMV time/space costs. LSPV-2 must still discover derived interfaces on EVERY source without assuming a path grammar or discarding malformed inputs. Do not infer Route B native rule legality. Universal FLMV contraction and B3 OPEN.
