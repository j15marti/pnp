# Schur-square control (hourly check, 2026-10-23)

STATUS: P versus NP OPEN. No load-bearing arrow touched. Classification: COMPUTATIONAL control only.

Repo check: last activity 2026-10-23 09:21 KST (residual-SAT Role 1: equisatisfiable-compression equivalence, black-box OR 2^r probes, minimally-UNSAT 2-SAT countertheorem). No open PRs examined; root main.tex unchanged by this run.

Experiment (ledger item 1, Schur-square distinguishers): dim C^{*2} for RM(r,7) vs matched random [128,k] binary codes, plus 80% puncturing.
- RM(1,7): k=8, dim sq=29 (=RM(2,7) dim); random: 36 = k(k+1)/2.
- RM(2,7): k=29, dim sq=99 (=RM(4,7)); random: 128 (saturated at n).
- Punctured 80%: RM 29 / 98; random 36 / 102.
Takeaway: raw square dimension separates structured from random codes (known: RM squares are RM of double degree), and survives puncturing; this is an EXACT KNOWN-THEOREM sanity check, not a new bridge. Hidden structure is equally an algorithmic weakness (distinguisher). Transfer to C_H^{*2} remains ANALOGY/CANDIDATE.

Files: 2026-10-23_schur_square_control.py (runs in <5 s), ..._output.txt.
