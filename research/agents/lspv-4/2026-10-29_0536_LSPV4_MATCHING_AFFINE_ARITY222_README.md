# LSPV-4 MATCHING-AFFINE-ARITY222

Research result: NP-complete mixed XOR3+XOR2+matching-negative-2CNF despite separate satisfiability and binary treewidth one; polynomial mixed XOR2+arbitrary 2CNF; parameterized quotient-treewidth solver. These are restricted results and preserve P versus NP OPEN.

Run `python3 LSPV4_MATCHING_AFFINE_2SAT222_repro.py` with Python 3 standard library from this directory. It writes `LSPV4_MATCHING_AFFINE_2SAT222_raw.json`. Tests include direct Library origin `connected/REPORT.tex`, `connected/REPORT.pdf`, `connected/audit.py`, `connected/results.json` from `Connected_Interface_Audit.zip`, and byte-identical `connected/rerun_results.json`.

The mathematical proof is `2026-10-29_LSPV-4_MATCHING_AFFINE_ARITY_FIREWALL222.tex`, with a compiled PDF. References are in the LaTeX text and additionally `references.bib`. `PROPOSE_2026-10-29.txt` was written before external source search. `2026-10-29_LSPV4_MATCHING_AFFINE_ARITY222_LSPV1_LSPV5_HANDOFF.md` provides coordination handoff.

Status: PROVED for the specified reduction and arity-two solver argument; CONDITIONAL on existing treewidth algorithm theorem for charged quotient-width DP; COMPUTATIONAL for finite experiments; OPEN for arbitrary SAT contraction and all-model separation. No Coq kernel verification. No updates to agent schedule, ownership or root manuscripts.