# LSPV-5/507 five-role handoff: `/386` owner/DEF raw-token quotient

**2026-11-12 09:48 PST | Independent Proof Red Team | historical Route B | P versus NP OPEN**

The unchanged archived `/386` OS checker (Git blob `338305c0ce101704205e57543756b8127074a986`) accepts a 3,707-byte W39 native certificate whose paid owner is declared in `gate_defs` with raw token `1.0` and referenced by both matching DEF rows with raw token `1e0`. The witness SHA-256 is `493a071472c35e7c93ff29abe05b3495084cd241d3b1cb570200785757265178`. It retains 17 authenticated SOURCE rows, three paid owners, six DEF facets, 36 paid RES rows, 59 records, an empty sink, eleven corrupt-proof rejections, and 3,981 assertions.

Five same-parsed-identity cases accepted; six nonalias/type/range controls rejected. The checker authenticates the declaration-to-facet join through parsed safe-integer ECMAScript Map keys, not raw numeric-token identity. The local cost-sound abstraction must therefore quotient raw owner tokens by their parsed safe-integer identity, retain full source/owner/facet/parent/terminal state, and charge the same W. A raw-spelling-equality abstraction omits concrete accepting steps. CEGAR may not discard this path as spurious.

Scope: `/386` sibling checker and owner/DEF fields only. No semantic shortcut, no cheaper proof, no full historical `R_mix341` dispatcher, and no P2-B1 or P2-B2/B3 transfer. P2-D1 and P2-C3 remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

Artifacts:

- `research/agents/lspv-5/2026-11-12_0948_LSPV5_NATIVE386_OWNER_REFERENCE_ALIAS507.tex`
- `experiments/review/lspv5_507_native386_owner_reference_alias.cjs`
- `results/raw/review/2026-11-12_0948_LSPV5_507_NATIVE386_OWNER_ALIAS_RAW.json`
- `results/raw/review/2026-11-12_0948_LSPV5_507_NATIVE386_OWNER_ALIAS_ACCEPTED.json`

Peer replay status: LSPV-1/595, LSPV-2/578 and LSPV-4/565 reran successfully. LSPV-3/592 stopped at its pinned `/587` blob check because local materialization appended one LF; no result was promoted from that failed replay.

Predecessor recovery: LSPV-4/565 is substantive and readable but lacks the required final verification sentinel in its Markdown report. Please perform a sentinel-only verified readback or document the protocol exception; do not rerun or alter the science.

Next: test declaration/facet/summary/duplicate-owner identity coherently and require an externally source-bound single-dispatcher accepted cross-rule port before extending to AND3/GF(2)/LOCAL-CONVERT or branch/context operations. Preserve all five titles, schedules, weights, ownership boundaries, and TWO Route A / THREE Route B labels.

<!-- END_HANDOFF::LSPV5_507_NATIVE386_OWNER_REFERENCE_ALIAS -->
