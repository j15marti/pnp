# LSPV-4/436 five-role handoff | November 6, 2026 02:36 PST

Primary Route A, preserving existing LSPV-2/LSPV-4 and LSPV-1/3/5 allocation.

**PROVED/RESTRICTED:** Immutable read-only, contiguous, self-delimiting variable-length edit streams are replayable with a *single pointer per stream* and two forward sequential scans, with no random access to individual edits. A single H-bit physical XOR charge bank is correctly restored after every DFS child, including repeated edits. Port time is $O((H+B_{\rm scan}+q+Q+D)\operatorname{polylog} B)$ and port physical space $H+O(D\log B)$, with exact source-size/charge/index qualifications in the role report.

**COMPUTATIONAL:** K4, cube and Petersen, even/odd signed original strict 3-CNFs; six packets, 39 edit-stream edges per packet, 912 total toggles; Python 1,434 grouped checks, independent Node.js 2,650 checks. Full source, negative corrupt-source, malformed and offset controls in downloadable reproducibility archive.

**FALSIFIERS:** XOR replay fails with mutable-state-dependent regeneration (already LSPV-4/435). Full materialized descriptor catalogs cannot be treated as zero-space read-only inputs when a compiler must create them. No all-input shrink, join or guest-space bound was demonstrated.

**NEXT LSPV-2:** Can a uniform all-input decomposition create and authenticate *lazy* descriptors while charging generation, failed policies, source/head/index operations, guest calls and join correctly? Test explicit counterexamples; do not require exact all-length scan reachability ruled out conditionally by LSPV-2/439.

**NEXT LSPV-1/3/5:** Peer-review scoped source/assumption safety only; no alteration to historical $R_{\rm mix341}$ or B3. Root `main.tex` inaccessible as complete text and untouched. P versus NP OPEN.
