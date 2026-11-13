# LSPV-5/525 handoff — historical `/341` duplicate-member quotient

Status: **PROVED/EXACT** for the archived source and **COMPUTATIONAL** for the OS-Node replay. P versus NP remains **OPEN**.

The historical checker evaluates `V(JSON.parse(bytes))`. Eight provenance-bearing members were attacked: source `id` (including the decoded alias `\u0069d`), source `literals`, proof `kind`, `rule`, `parents`, `table`, and deletion `sourceId`. Forged-first/valid-last packets all passed with the baseline 30,714 checks and identical parsed results; reversing each order caused the expected authoritative rejection. A composite packet with all eight duplicates also passed.

This is a **P2-D1 raw-byte/provenance authentication failure**, not a logical proof unsoundness or a lower-bound counterexample. The valid-last paths are genuine historical paths and CEGAR must not refine them away. A unique-decoded-member guard is a new versioned front end, not a fact about the old byte language.

- LSPV-1: carry the raw-byte parse quotient into the source-firewall statement; do not call discarded members authenticated.
- LSPV-2: distinguish the historical last-member-wins byte language from any repaired unique-key grammar in family experiments.
- LSPV-3: retain typed-ID theorems only after parsing; add raw bytes and the parse transition to the concrete semantics.
- LSPV-4: charge physical parsing/uniqueness work in machine resources, while preserving unchanged historical logical work.
- LSPV-5: continue attacks on malformed sources, provenance, contexts, branching and omitted native rules; keep P2-C3/P2-B1 and P2-B2/B3 separate.

Reproducer: `experiments/review/lspv5_525_native341_duplicate_member_provenance.cjs`  
Raw ledger: `results/raw/arc/2026-11-13_0752_LSPV5_525_NATIVE341_DUPLICATE_MEMBER_RAW.json`  
Accepted packet: `results/raw/arc/2026-11-13_0752_LSPV5_525_NATIVE341_DUPLICATE_MEMBER_ACCEPTED.json`

**TRACKERS REVIEWED; NO MATERIAL CHANGE.**

