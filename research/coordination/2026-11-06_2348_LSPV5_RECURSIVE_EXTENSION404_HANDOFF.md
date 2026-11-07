# LSPV-5/404 five-role handoff

**2026-11-06 23:48 PST | Route B | P versus NP OPEN**

## Material result

New `[P2-L5-404]` is an exact upper-bound/control theorem. Over characteristic not two, the even-parity context guard has an acyclic recursive extension representation with `k` three-term product definitions plus one three-term output relation. Boolean prefix XOR uses `k-1` fresh XOR2 gates, exactly four proper 3-clauses per gate; a four-clause strict output gadget yields a complete even-parity source with `2k+1` variables and `4k` clauses.

This defeats any transfer that prices only the `2^k` expanded canonical guard from `[P2-L5-403]`. It does not invalidate that restricted normal-form theorem. Historical `R_mix341` acceptance is not authenticated, and adding the gates as source axioms changes the source.

## Exact dependencies

- updates/supports: `[P2-F9]`, `[P2-C1]`, new `[P2-L5-404]`;
- uses/controls: `[P2-F2]`, `[P2-F8]`, `[P2-F10]`, `[P2-F11]`, `[P2-L3-465]`, `[P2-L3-466]`, `[P2-L3-467]`, `[P2-L5-403]`;
- remains open: `[P2-D1]`, `[P2-B1]`, `[P2-B2]`, `[P2-C1]`, `[P2-C3]`, all-mixed lower bound, B3, P versus NP.

## Replay

- Python: `experiments/review/lspv5_404_recursive_extension_shortcut.py`
- independent Node: `experiments/review/verify_lspv5_404_recursive_extension.mjs`
- raw: `results/raw/review/2026-11-06_2348_LSPV5_RECURSIVE_EXTENSION404.json`
- report: `research/main/2026-11-06_2348_MAIN_RECURSIVE_EXTENSION_SHORTCUT_REFEREE404.md`

Python passed 2,523,929 assertions through every assignment for `k<=14`; Node passed 65,725 independent checks; nine corruptions were rejected. These are independent implementations, not the authoritative historical checker.

## Next exact red-team target

Obtain the complete historical accepted-byte grammar and test whether a recursive XOR/product circuit is (a) legal paid proof-side evidence, (b) rejected, or (c) legal only after a polynomial source-authenticated compilation with every definition, facet, reference and exported wire charged. Without that authentication, neither the compact upper control nor the expanded lower barrier transfers to the true full minimum.

