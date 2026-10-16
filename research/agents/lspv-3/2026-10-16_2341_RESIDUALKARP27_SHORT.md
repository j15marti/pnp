# RESIDUALKARP27 | 2026-10-16 23:41 KST
UNIVERSAL-OBSTRUCTION LSPV-3. Status: exact scoped lemmas; finite test. P versus NP and common-input UWI remain OPEN.

PRE-SEARCH CANDIDATES: (1) many-one residual anchor; (2) aggregate residual sparsity; (3) anchor self-bootstrap; (4) resource-charged witness-preserving transport.

SEARCH: newest FIXEDPOINT26, DREAMPORT25, TOTALSHIELD17; GitHub LSPV-3; Drive SIM-2-0003 and SIM-2-0007; primary Mahaney 1982, Cook 1971, Glaesser et al. 2006, Grochow 2016.

THEOREM: For fixed polynomial T and logarithmic program description cap, let D_T be the set of proper 3-CNF formulas on which some eligible program returns a *verified satisfying witness* within T. All O(n) programs can be boundedly simulated, hence D_T is in P and D_T is a subset of SAT. Let H_T=SAT minus D_T.

If H_T is empty, SAT is in P. If H_T is nonempty, choose any fixed anchor h in H_T and set r(F)=h if D_T(F), and r(F)=F otherwise. Then F in SAT iff r(F) in H_T. Therefore H_T is NP-complete under polynomial-time MANY-ONE reductions (not merely Turing reductions). Critically, this assumes an anchor h; it does NOT construct one.

CONDITIONAL COROLLARY: Under P!=NP each H_T is nonempty and NP-complete, and Mahaney implies H_T is not sparse. For every exponent k, infinitely many lengths have more than n^k uncovered formula encodings. This does NOT give a random-sampling guarantee.

COUNTEREXAMPLE: If h is uncovered, e is covered, and h has witness w, define a SAT-equivalent map g(F)=e if F=h, else F, and project target witnesses to w if F=h. Both maps are polynomial-time and witness-preserving, yet g(h)=e is covered. Resource-bounded hardness is not automatically transported by SAT reductions.

TEST: 16 proper 3-CNFs (8 SAT, 8 UNSAT), 8,192 full assignments, independent DPLL, 8,375 final assertions passed. Restricted toy portfolio covered 3/8 SAT; F_110 uncovered. Adding source-aware polarity reader covered 8/8 and broke the old anchor. Toy tests do not exhaust all short programs.

NEXT: establish existence of the initial uncovered explicit formula without assuming P!=NP. Any transport needs both code-length and fully charged runtime inequalities.

SENTINEL-RESIDUALKARP27-OPEN