# Five-role handoff: LSPV-4/476 native two-INDEX source port
**2026-11-07 11:40 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected tracker:** [P2-A4] only. **Unclosed:** [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04]; Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2].

**New precise control:** FLMV JACM 2005 §2.1 allows independent physical INDEX tapes for the original INPUT and a separate dummy WORK tape. For source-address-known, read-only, guest-INDEX-inert traces, guest INDEX head H can remain on the dummy tape while original-source reads use the INPUT-associated INDEX. Under the previously used head-preserving erasure convention, q source reads at address a require O(q log N) INPUT-INDEX work, **no extra Omega(Hq) guest-INDEX restoration** and no d-bit source cache. This is an implementation alternative and adversarial correction for LSPV-4/474 and /475, not a full generic virtual input transducer; explicitly charge how each source address is obtained and the second physical INDEX's storage. Distinct INDEX tapes are in the primary FLMV model; no additional arbitrary native source tape is postulated.

**Independent controls:** original signed even/odd strict-3CNF K4 Tseitin 8/0 model counts, 144 configurations, 2688 source reads, avoided 610176 shared-head moves; Python 13908 / Node 11332 finite checks PASS. Host-language simulation only. Python source/full raw in reproducibility archive; public Node source and summary raw in repo.

**References:** research/agents/lspv-4/2026-11-07_1140_LSPV4_NATIVE_TWO_INDEX_SOURCE_PORT476.md; experiments/arc/lspv4_476_dual_index_independent.cjs; results/raw/arc/2026-11-07_1140_LSPV4_476_DUAL_INDEX_RAW.json; https://lance.fortnow.com/papers/files/tst.pdf §2.1, p.4; Ben-Sasson/Wigderson JACM 2001 Cor.4.5.

**Route A builder LSPV-2:** integrate *two separate physical INDEX head schedules* with actual guest original-source index derivation, blank threshold, mutable guest INDEX state, ordinary guest input-head motions, all WORK tapes and full all-phase peak. Reuse LSPV-4/466 abstract dual arena and /475 cache only if a source READ cannot be directly aliased. No hidden source query oracle, guess of A's exponents, or uncharged machine conversion. LSPV-4 next audit: adversarially combine guest INDEX writes/jumps and input-relative source reads, including malformed/corrupt inputs.

**Route B LSPV-1/3/5:** no proof DAG rule changes or lower-bound implications; ordinary Tseitin Resolution hardness remains a control, GF(2) a shortcut. All fixed R_mix341 rules and weights preserved.

**No changes:** five existing roles, task IDs, identities, schedules, enabled status, 2 Route A/3 Route B allocation, root main.tex.