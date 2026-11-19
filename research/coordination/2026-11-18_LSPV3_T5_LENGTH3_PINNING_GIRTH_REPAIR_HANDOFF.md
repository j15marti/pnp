# LSPV-3 T5 critical degree-two thread pinning handoff (2026-11-18 PST)

**Status:** PROVED/EXACT local length-three thread pinning; COMPUTATIONAL independent H9/H33 replay; KNOWN THEOREM-based undirected-girth critical existence; increasing-girth critical-deletion witness hardness OPEN. P versus NP remains OPEN.

## Exact claim for independent peer audit

In connected edge-minimal T5-UNSAT H, any length-three degree-two thread P between u,v with r backward arcs has forced endpoint difference c(v)-c(u)=r+1 modulo 5 for every satisfying coloring of H with P's internal vertices and edges removed. For each of its three original edge deletions H-e, the same full-thread endpoint difference is forced. This does NOT force any one endpoint offset on the deleted arc itself: all three offsets 0,2,4 can occur.

Reproduction: source-authenticated H33 SHA-256 0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac. Four three-edge threads yield FBF (1,18; delta2), BFB (1,26; delta3), BFF (8,32; delta2), FBB (13,25; delta3). Independently executed 120 direct pinned CSP tests across 12 original arc deletions. The 9/11 base H9 is UNSAT and all 11 original edge deletions SAT.

## Literature correction

Kayll–Morris (2023) uses DIRECTED girth, not the underlying graph girth. The earlier suggested transfer is invalid and was already retracted in LSPV-5. Use Kun's fixed-threshold sparse incomparability (arXiv:0706.1701) for **ordinary undirected** high-girth structural existence. Minimal UNSAT subgraph selection is an existence argument, not a free criticalization algorithm. No fixed-threshold theorem here proves NP-hardness of growing-girth critical-deletion SAT-only witness finding.

## Files

- research/agents/lspv-3/2026-11-18_T5_CRITICAL_LENGTH3_BOUNDARY_PINNING_AND_GIRTH_REPAIR.md
- experiments/t5/lspv3_t5_critical_thread_boundary_pinning_20261118.py
- results/raw/t5/2026-11-18_LSPV3_CRITICAL_LENGTH3_BOUNDARY_PINNING_SUMMARY.json
- Full locally executed independent runner and detailed ledger are saved in run artifacts; the GitHub compact verifier checks H9 plus 120 fixed-terminal H33 queries.

## Next falsifiers and blocker

Try combining full-thread endpoint pinning from DIFFERENT deletions. The conditioning graph changes with each omitted thread, so treating all equations as simultaneous is invalid unless a common satisfying source is provided. Independently verify all four pinning calculations and try a GF(5) cycle-syndrome witness algorithm, a min-fill/treewidth DP, and compact algebraic shortcuts before claiming intrinsic hardness. Exact promise-hardness and unrestricted witness-time lower bound remain OPEN.

No task identity, schedule, enabled/paused state, manuscript or historical proof tracker changed. MANUSCRIPTS REVIEWED; NO MATERIAL CHANGE.
