# LSPV-3 GATE279: reproducibility and model caveat

Run on Python 3.10+ (no third-party dependencies):

```bash
python gate279.py
python verify279.py
```

The first command creates `raw279.json` and `summary279.json`; the second independently tests both labels on all original source formulas and children, original-clause S/U extremes and inversions, complement identities, Gray-like one-flip trails, and all four pairwise extreme compatibility modes. It creates `verified279.json`.

Fixed seed: 2791031. All 17 formulas deterministic and generated within source; no external fixture files. Source clauses use signed integer occurrences with original indices. Complete reference UP-DPLL terminates on all cases. No CDCL performance comparison is claimed.

**Machine distinction:** `gate279.py` holds the Python source and transient BFS set and is NOT a deterministic logspace implementation. The theorem in the accompanying LaTeX relies on Reingold (2008) to replace BFS with deterministic logspace undirected connectivity over a source-implicit adjacency predicate. It proves logspace *existence* of recognition and of child-bit emission with unspecified polynomial time, not FLMV-local time or universal ARC. The independently measured source-scan counts belong to the finite BFS reference only.

The `bit_encode` grammar is a fixed-width source subgrammar with at most `O(n^3)` distinct clauses; input supports the displayed proper CNF controls. The theoretical transfer uses a standard length-decodable indexed CNF grammar and does not assume an unbounded duplicate-clause count fits the prototype header width.

Full raw data and independent verification are in this archive. The accompanying `manifest279.json` includes SHA-256 for every payload file.