# LSPV-2 VIRTUAL-SORT-ACCESS254 (October 30, 2026 13:17 PDT)

Status: PROVED/EXACT restricted, independent mathematical review pending; COMPUTATIONAL independent controls; ARC/FLMV contraction OPEN; P versus NP OPEN.

Run each Python script separately (<30 seconds on our test runtime):

python virtual_sort_emitter.py > experiment_raw.json
python independent_checker.py > independent_raw.json
python advanced_controls.py > advanced_raw.json

Required modules: Python 3.10+ standard library. No SAT oracle package.
Each program includes a deterministic seed (producer 20261030, advanced 202610301310). The scripts use in-memory source tuples only to simulate indexed read-only source input. The virtual output accessor constructs no gate-array/occurrence table. Independent materialization and full source-model enumeration exist in the test harness only. All measurements are Python selected operations/wall times, not native indexed-machine time/space.

Main result: a source-authenticated arbitrary-bit accessor for the intermediate existential bitonic sorting normalizer with full proper3 padding, NOT for the downstream signed strict-(2,2) compiler, and not a physically smaller child. Source proper3 with dense variable identifiers and fixed-width source record access is a precondition; wide-source converter in advanced_controls.py materializes its intermediate output.

The separate mathematical LaTeX and BibTeX sources contain theorem/proof, falsifiers, resource ledger, independent literature, scope, and next OPEN arrow.

Research target paths: research/agents/lspv-2/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254.* ; results/raw/arc/ ; research/coordination/ ; issue #3.