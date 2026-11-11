# LSPV-5/487 five-role handoff: live duplicate-facet normalization under a decoder alias

**2026-11-11 05:58 PST | Independent Proof Red Team | historical Route B | P versus NP OPEN**

The unchanged archived `/386` checker accepted an actively referenced duplicate DEF facet both with exact integer parent 20 and raw exact noninteger token `20.000000000000001`. Deleting that duplicate, redirecting the live child to the earlier identical owner/facet record 17, and reindexing every later parent exactly recovered authenticated seed blob `d0fa96a155672f8f6a6a3428eacafa15e79b9e88`, preserving $W=50$.

Four positive original OS-Node runs passed 18,052 assertion groups and 44 original bundled hostile tests. Three controls rejected: deletion without redirect, redirect to the wrong true facet, and alias `20.000000000000004` outside the rounding cell. The hostile alias packet is 4,208 bytes, SHA-256 `7b004589433d188a46efe579aa643977c97ed43fbfdb2ef5ef89a939df7aa62e`. Positive child-process high-water RSS was 41,272--41,404 KiB; this is an implementation measurement, not proof work or a lower bound.

Disposition: independently validates one live instance of LSPV-1/569 plus LSPV-5/485. Accepted aliases and duplicates are not CEGAR-spurious. A valid abstraction must redirect every consumer, preserve chronology and owner/facet identity, and satisfy abstract cost no greater than concrete cost. This does not authenticate full R_mix341 or prove P2-C3/P2-B1.

Artifacts:

- `research/agents/lspv-5/2026-11-11_0558_LSPV5_LIVE_DUPLICATE_NORMAL_FORM_AUDIT487.md`
- `experiments/review/lspv5_487_live_duplicate_normal_form_audit.js`
- `results/raw/arc/2026-11-11_0558_LSPV5_487_LIVE_DUPLICATE_NORMAL_FORM_RAW.json`
- `research/main/2026-11-11_0558_LSPV5_487_MAIN_OWNED_INSERTION_FALLBACK.tex`

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** `[P2-D1]`, `[P2-C3]`, `[P2-B1]` and separate `[P2-B2]`/B3 remain OPEN. Root `main.tex` blob `5c117868624d40e93251b35934453eba6a746cb3` returned zero readable content bytes, so it was not overwritten. No role, schedule, identity, timezone, weight or allocation changed.

