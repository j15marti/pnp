# Strict-C NTIME(n) local-transfer handoff, 2026-11-19
**OPEN:** P versus NP. Generic SAT-lower-bound routine; no TMR manuscript, schedule or retired tracker touched.

**Transfer gate narrowed to one premise.** Chain: NTIME(n) -> clause-addressable width-W CNF (P-CA: clause-addressed reading of van Melkebeek survey Lemma 2.2, proof Sec. 2.3.1; review OPEN) -> FW3 by width chain (Lemma A, PROVED, one oracle call per clause) -> strict-C K(F) (Lemma B, 15+9v+39m names, 10+7v+31m clauses) -> encoded bit p in polylog time / O(log n) space (Lemma C). Theorem (CONDITIONAL on P-CA only): NTIME(n) not in DTISP(n^d', n^e') with d'>d, e'>e implies STRICTC-FW not in DTISP(N^d, N^e); hence strict-C not decidable in N^d time, N^o(1) space for every d<2cos(pi/7)~1.801 (Williams; survey Thm 1.2).

**Correction:** the earlier "(1.33, .5+o(1)) is excluded by Buss-Williams (1.34070, .5)" is too strong at the space boundary; transfer costs polylog space, so only c<1.34070 AND s<0.5 strictly.

**New executed evidence:** `experiments/strictc_local_transfer/strictc_transfer.py` (SHA256 4f176de4...e96e3, seed 2026111917, 13.7 s), raw `results/raw/strictc_local_transfer/2026-11-19_run1.json`. 67 sources, records and sampled bits equal an independent builder 67/67, <=1 source call per record, FW3 equisat 67/67, independent 5-colour GAC solver agrees 64/64 incl. **4 UNSAT refuted at full C level**; 3 UNSAT controls undecided at 60k nodes (disclosed).

**Next lemma:** discharge P-CA explicitly (step blocks + Batcher comparators, arithmetic index maps), then confirm Buss-Williams Fig. 8.3 is NTIME(n)-level. Report: research/agents/claude/strictc-local-transfer/2026-11-19_STRICTC_NTIME_LOCAL_TRANSFER.md.
