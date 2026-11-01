# LSPV-2 K5-SOURCE-SCC295 reproducibility package

Exact scope: source-certified unsatisfiable five-variable K5 binary residual in every valid canonical monotone 3-SAT-(2,2) source. This is a standard 2-SAT implication contradiction, not a new complexity lower bound. Original canonical F15 has 770 satisfying assignments while one pinned cube is UNSAT.

Run with Python 3.10+ standard library:
```
python k5_scc295.py
python physical295.py
python logical295.py
python verify295.py
```
Independent verifier has no producer import. U198.txt is the source original from prior project controls. The physical event streams are gzip-compressed JSON lines; the physical machine simulated is explicitly a fixed-layout source-index and output register tape, not a native matched FLMV random-access TM, and no arbitrary solver steps / head motions / guest operations are claimed to be measured. Logical XOR is offline. Both P=NP and P!=NP remain open.

Report: 2026-11-01_0321_LSPV-2_K5_SOURCE_SCC295.tex/pdf. Raw: results295.json, independent295.json, logical295.json, physical295.json and matching physical_events*.gz. Published compact GitHub files are referenced in the report, and this ZIP is the complete raw fallback.
