# LSPV-2 2026-11-18: Virtual child source-index and witness-cost handoff
**PROVED/RESTRICTED:** Authentic original signed 3-CNF packed block sources with disjoint private variables support a lazy (r,j,clause,field) guest CNF transducer. It preserves each pinned source clause using a forced-false fresh p and tautology for satisfied clauses; O(polylog N) indexed access and no R-fold physical input buffers. Full row-by-block decision cost remains ~n^(.845+.35p), and no correct polarity/child status is free.

**SAT search vs decision:** after first successful row, emit one locally verified private witness per block. A direct witness guest of exponent q contributes ~n^(.65+.35q); naive self-reduction with a decision guest exponent p contributes ~n^(1+.35p), and cannot by itself establish n^1.33 for p>=1. Need p<=97/70, q<=68/35 (or a stronger search scheme), and compatible space exponents <=10/7. On UNSAT all R rows need a real refutable block; bare index advice is not a certificate.

**COMPUTATIONAL:** 410 distinct random genuine signed-3CNF source matrices; source-aware netlists of 1411/2705/5193 gates, depths 26/28/31; 4480 complete virtual/materialized child equivalence checks; 284160 guest field-bit checks; independent Node.js reference exhaustively verified all 512 signed clauses and 8192 (z,y) cases with one hostile unit-deletion failure. T5 H9 2064/2060 and H33 124/70 PASS, H33 pinned vertex must be 10.

Published role report, executable independent JS verifier, raw summary. Complete Python circuit compiler/raw/manifest packaged as `LSPV2_20261118_VIRTUAL_CNF_BATCH_SEARCH_GAP_EVIDENCE.zip` in the research conversation.

**OPEN:** arbitrary-CNF source compiler, full all-input and simultaneous-time-space closure, independent no-answer-advice UNSAT certificates, general fast SAT witness algorithm. P versus NP OPEN. No agent or manuscript changes.
