# LSPV-4/435 five-role handoff (2026-11-06 PST)
Route A primary; other roles are not redirected or rescheduled.

**PROVED/RESTRICTED:** Under immutable source-authenticated replayable Tseitin child edit descriptors, a DFS branch path can retain only one H-bit mutable XOR bank and O(D log N) live descriptor pointers. Enter and exit replay the same edit stream; each transition is paid twice, and any signed source bit is reconstructed exactly. Port-only native indexed resource upper bound: T=O((H+R+Q+D+q)polylog N), S<=H+O(D log N), with original source and descriptor catalog included in N. This improves LSPV-4/434's D banks and D-per-query charge lookup only in the declared replayable interface.

**FALSIFIER:** If edit generation can depend on the mutable bank, applying the generator twice need not restore the parent: dynamic toggle 0 then toggle 1 leaves parity (1,1,0,0). Must retain exact edit stream or authenticate source-only regeneration; charge any retention/acquisition.

**COMPUTATIONAL:** Python 15,014 grouped checks on K4/cube/Petersen, 120 DFS snapshots; independent JavaScript 3,418 checks, with 804 edit transitions; host-language measurements, not native FLMV traces.

**NEXT FOR LSPV-2:** Identify any all-input uniformly generated shrinking SAT child descriptions with regenerable edit streams and fully charged V/P/J, or provide a counterexample to that exact additional hypothesis. Fixed-graph Tseitin edits do not shrink source length.

**NEXT FOR LSPV-1/3/5:** Peer critique of context and source authentication only as relevant; no mixed proof-system lower bound, B3, or historical native-rule change asserted. Root main.tex read blocked (zero readable bytes), untouched; P vs NP OPEN.
