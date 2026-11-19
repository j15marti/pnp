# Strict-C critical construction: independent Hajós handoff (2026-11-19)
**Role:** fresh critical obstruction constructor. **P vs NP OPEN.**
Formal argument and finite results: [research report](../agents/strict-c-critical-constructor/2026-11-19_HAJOS_WITNESS_GIRTH_AUDIT.md).

**PROVED restricted:** Hajós join of edge-minimal non-5-colorable graphs preserves edge-criticality and minimum graph girth; its deletion colorings can be assembled from existing operand deletion colorings. The one-private-head direct C lift preserves clause-criticality; incidence girth is twice graph girth. Saving deletion colorings during a total exact criticalization pass is sound because subsequent edge deletions cannot invalidate them.

**COMPUTATIONAL:** Mycielski³(C5) k-fold join, k=1..5: 3,530 full strict-C deletion witnesses / 3,044,430 original-clause checks, all passed. Largest full source: 1,407 variables, 1,176 clauses, incidence girth 8. Independent literal-source witness replay: 1,176 witnesses / 1,382,976 original C evaluations, all passed. K6 Hajós chains k=1,2,3: independent full five-color UNSAT searches with 6/71/1722 nodes. Source-matched selector: 4/4 valid rows refuted, forged source 4/4 UNKNOWN; no polarity advice. All raw scripts and certificate ledger packaged locally, not uploaded in full to GitHub.

**HIGH-GIRTH route:** LPS X(73,q) with q prime, q≡1 mod292 has chromatic number >=6 by LPS + Hoffman and increasing ordinary girth. Local Cayley word enumeration gives exact graph girths q=37:3, q=61:4, q=89:5, q=293:6. **Do not claim these are critical**. Exact greedy critical extraction exists but would require all positive and negative five-color tests. Nothing polynomial established.

**Resource boundary:** This explicit joined family has B=Theta(N), not the desired B<=N^.65 layout. All source bytes, certificate generation, failed tests, full output and peak memory must be counted. No transfer from resolution or alternation-trading to unrestricted machines. An original-block identity matrix gives cover rank B but no machine hardness.

**OPEN blocker:** a source-explicit, efficiently obtainable, high-incidence-girth edge-critical seed with all deletion certificates; independent peer mathematical review.

Existing historical LSPV-3 files remain unchanged. No tasks/schedules modified by this report.
