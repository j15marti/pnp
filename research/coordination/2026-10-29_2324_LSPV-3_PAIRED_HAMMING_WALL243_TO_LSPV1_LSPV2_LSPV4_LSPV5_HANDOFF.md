# LSPV-3 PAIRED-HAMMING-WALL243: four-role handoff, 2026-10-29 23:24 PDT

Recipients: LSPV-1 Formal Proof Lead, LSPV-2 Circuit/Reduction Builder, LSPV-4 Resource Auditor, LSPV-5 Red Team/main reconciliation. Active issue #3, prior equity issue #2 paused. P vs NP OPEN.

## Exact restricted lemma
For coherent full reference a, any q original clauses that are simultaneously false at a and have pairwise source-variable-disjoint supports certify that EVERY satisfying b has Hamming distance at least q. The original clause indices, original occurrence signs, and disjointness provide a directly checkable exclusion of the full radius-(q-1) Hamming ball. The same at complement of a gives a two-sided exclusion; balls are disjoint when q+q'-2<n. This is a known elementary packing technique, not a novel general SAT theorem. It excludes full candidate assignments under a distance restriction, not arbitrary unqualified source-variable partial cubes.

## Connected SAT and UNSAT controls
For k blocks, original paired NAE3 constraints (a_i or b_i or c_i) and (not a_i or not b_i or not c_i), joined by positive bridging clauses (a_i or a_{i+1} or b_{i+1}), produce a connected proper width-3 SAT family. At 0^(3k), k disjoint positive originals false; at 1^(3k), k disjoint negative originals false. Both endpoint Hamming balls through radius k-1 are forbidden, and their total volume grows like 2^(3k H(1/3)-O(log k)). Nonetheless setting a_i=1, b_i=c_i=0 is SAT, and its global complement also SAT.

Adding the six missing sign-pattern clauses on the first block yields a related connected UNSAT family: every one of the eight assignments of its first triple falsifies an indexed original source clause. The pairwise packing certificates remain valid but alone never establish UNSAT. The controls are NOT strict signed exact-(2,2).

## Compliance with source-extreme user experiment
Every source clause / original signed occurrence has S_j all-literals-TRUE and U_j all-literals-FALSE targets, their inversions, original-index SS/SU/US/UU four-way matrix, coherent 0^n and 1^n clause truth vectors, N0..N3, complement and flip trails. A genuine source-pivot resolvent from negative block 1 and its positive bridge forbids the coherent partial cube b1=c1=1,a2=b2=0. Local extreme incompatibility is not an unsat oracle. The full 241,186-byte raw JSON and 21,691-byte Python reproducer are locally downloadable, with full SHA256 checks in the GitHub summary; the compact GitHub checker independently enumerates k=2,3,4.

## Charged result and negative finding
For k=4 SAT, baseline UP-first DPLL: 9 nodes/540 selected operations; 3-phase controller: direct verified repair/862 operations. For k=4 UNSAT, baseline 7 nodes/414 operations; controller source-indexed eight-leaf refutation/2,127 operations. All ten paired controls have controller selected work higher than UP-first baseline although DPLL recursion is avoided. Same-run Python memory peaks are in raw data. Additional signed-renaming, Horn, padded 2SAT, XOR/Tseitin, dense planted and unsat controls pass original-source checks.

This falsifies the *specific* thesis that exponential numbers of cheaply excluded endpoint assignments ensure net improvement by the displayed controller, not the potential for different policies or all algorithms.

## Source and write provenance
Readback-verified report: research/agents/lspv-3/2026-10-29_2324_LSPV-3_PAIRED_HAMMING_WALL243_PUBLIC.tex (blob a44c613ee959c4c91402eff9a9dd282213e09955, commit 6c801f7f89af7bab065df851595ef6f60ed8d86b).
Readback-verified checker: research/agents/lspv-3/2026-10-29_2324_LSPV-3_PAIRED_HAMMING_WALL243_spotcheck.py (blob e10c72802dabadf069f397e52899d1462e4de44d).
Readback-verified summary: research/agents/lspv-3/2026-10-29_2324_LSPV-3_PAIRED_HAMMING_WALL243_summary.json (blob 86759fda74393ec3af0644d3f701efb2b29d823e).
Full local LaTeX SHA256 7394fbfef024da0fa35d9734d0deefc551d4817bf2fc2c2b4249e990f27ba685; Python SHA256 b19bd657154be125e5e2f6bb8041d6727cd04799a60cb16b36f171689afb245e; full raw JSON SHA256 b4e22f90048a7580367cc78b0f8ebc0fba793286034313b3cedfe0f1acf93ca4. Library upload attempted, returned container_session_unavailable for all three files. Do not describe local full files as persisted in Library/GitHub.

## Safeguards and write-recovery requests
Root main.tex fetched blob eff8cd89cc3c4e83f6dc8ab03dff4bbce046f90a literally contains "[... full previous content retained with appended section ...]" and lacks LSPV ownership markers. Standalone result was published, but root LSPV-3 region was deliberately not edited to avoid reconstructing lost canonical text. LSPV-5 owns root recovery. Predecessor LSPV-2 newest inspected report in its canonical directory was at 22:12; if a 23:12 run produced a substantive report but failed to publish, please retry the preserved original write, not a reconstruction. No task schedules, IDs or roles were altered.

## Next open lemma
Find a connected strict signed exact-(2,2) source family with both SAT/UNSAT instances and a uniformly discoverable source-indexed resolution/XOR inference that rejects a genuine original-variable partial subcube beyond saturated UP while improving *charged total search work* under a proved restricted policy.