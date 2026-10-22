# SEPARATOR-SCALING81 — empirical size of balanced separators vs the 0.1·log N budget

**Timestamp:** 2026-10-22 hourly check. **Global status:** P versus NP OPEN; P versus RP OPEN.
Responds to SEPARATOR-CONE-COVER80's ":48 synthesis" next experiment (wall/expander residual size).

## Experiment (COMPUTATIONAL, heuristic upper bounds only)
`research/experiments/separator_scaling81.py` (stdlib, chunked by n: {100,200,400} then {800,1600}; each call <30 s).
Primal graphs of random 3-CNF (m=4.2n) and random 3-regular graphs; min-degree elimination width (treewidth upper bound) and best BFS-layer balanced separator (every component <= 2n/3).

| n | 3CNF tw<= | 3CNF sep<= | 3-reg tw<= | 3-reg sep<= |
|---|---|---|---|---|
| 100 | 69 | 76 | 20 | 16 |
| 200 | 142 | 155 | 36 | 27 |
| 400 | 276 | 151 | 78 | 66 |
| 800 | 553 | 290 | 161 | 118 |
| 1600 | 1115 | 615 | 336 | 269 |

Separator sizes found grow roughly linearly (~0.2-0.4 n for 3CNF, ~0.17 n for 3-regular). Lemma 80B allows only k <= 0.1 log2 N (about 1 at n=1600). These are upper bounds from a crude heuristic, so true minimum separators are <= these; linear growth is consistent with, but does not prove, Omega(n) separators. 

## Literature
Dvorak–Norin (arXiv 1408.3869): treewidth and balanced-separator order are linearly equivalent. Sparse random graphs G(n,c/n) have linear treewidth (arXiv 1104.2132, 0907.5481). I found no direct published statement for primal graphs of random 3-CNF; transferring the first-moment argument to the 2-section of a random 3-uniform hypergraph is a plausible new bridge, NOT verified here (CANDIDATE).

## Classification
- Supplied 0.1·log N separator route on generic/random instances: consistent with RETIRED for syntax-preserving decomposition (agrees with EQUALITY-LOCALIZATION-MINOR-BARRIER65); no change of status.
- Nothing here strengthens any OPEN arrow. Hereditary separator compiler remains OPEN, restricted to instances with promised small separators.
- Not done this run: full corpus reconciliation, root main.tex edit (this is an ad hoc hourly check, not an LSPV run).

## Next
Prove (or find in literature) Omega(n) treewidth for random 3-CNF primal graphs at ratio 4.2 to turn the heuristic into a KNOWN THEOREM-backed barrier, with Tseitin variables counted in the same size measure.

% END_OF_VERIFIED_REPORT::SEPARATOR-SCALING81
