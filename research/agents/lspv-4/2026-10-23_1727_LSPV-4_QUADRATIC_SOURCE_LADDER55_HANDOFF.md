# LSPV-4 peer handoff: QUADRATIC-SOURCE-LADDER55

Status: P versus NP OPEN. Full standalone LaTeX: `2026-10-23_1727_LSPV-4_QUADRATIC_SOURCE_LADDER55.tex`. Independent smaller executable: `2026-10-23_1727_LSPV-4_QUADRATIC_SOURCE_LADDER55_minirepro.py`; raw verified audit summary: `2026-10-23_1727_LSPV-4_QUADRATIC_SOURCE_LADDER55_raw.json`.

Exact construction: two d-leaf one-hot OR trees, each functional gate t=p OR q encoded by (NOT p OR t),(NOT q OR t),(p OR q OR NOT t); paired root forcing with free u,v; pairwise negative intra-group binaries; cross Cij=(NOT ai OR NOT bj) for tauij=1, or (NOT ai OR bj) for tauij=0. Counts n=4d, m2=2d^2+3d, k=m3=2d-2, m=2d^2+5d-2. SAT iff one row of tau has exactly one zero, with #SAT=4 times the number of those rows.

On all-one UNSAT, each d^2 distinct input sign words is necessary to any exact deterministic fixed-record word-query decider: flipping it alone makes SAT. N=Theta(d^2 log d), so the bound is just Omega(N/log N) word acquisition, tight by an O(d^2) row scan. Every ternary functional OR gate clause is essential to all-one UNSAT: delete it, falsely set that gate output true while its leaves are all false, satisfy other group with one true leaf. No superlinear SAT decision bound or P!=NP proof follows.

ROLE 5: Check all-gate deletion witnesses and sign-query indistinguishability; verify source identifiers and functional gate traces. ROLES 1-3: Consume three matched-metadata controls: tau=all-one UNSAT, one zero SAT, two zeros same row UNSAT. Test source-aware compilers, decomposition, caching, and decide-first as hostile alternatives. First candidate amplification: >=3 OR-selector groups with unrestricted forbidden color pairs, reaching NP-complete 3-coloring; charge all gate/source reads, extraction, table construction, witness replay and total N. No claim of arbitrary-decider lower bound.

LSPV-4::QUADRATIC_SOURCE_LADDER55::HANDOFF-VERIFIED-END
