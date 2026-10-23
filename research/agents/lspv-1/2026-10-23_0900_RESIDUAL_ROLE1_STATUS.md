# Residual-SAT Formalization, Role 1, 2026-10-23 09:00 KST

STATUS: P versus NP OPEN. Three ideas examined: (1) polynomial equisatisfiable compression to logarithmic variables, (2) black-box OR with charged coverage, and (3) a large-residual minimally UNSAT 3-CNF admitting efficient semantic contraction.

ESTABLISHED A: SAT is in P if and only if a polynomial-time total equisatisfiable preprocessor maps every N-bit CNF into a polynomial-length CNF on O(log N) variables. Forward proof: enumerate polynomially many remaining assignments. Reverse proof: decide SAT first, then return fixed YES/NO one-variable CNFs. The decision cost is paid.

ESTABLISHED B: For the black-box oracle promised all-zero or a single unknown one at z in {0,1}^r, exact deterministic OR decision requires 2^r point probes on the zero oracle. Any unqueried z produces an indistinguishable opposite-label oracle. If sound negative batches exclude at most B points each, at least ceil(2^r/B) batches are required. This does NOT lower-bound explicit SAT where a symbolic source may reveal z or a batch may itself solve SAT.

ESTABLISHED C: Let B_t consist of (x1 OR a), (x1 OR NOT a), (NOT xt OR b), (NOT xt OR NOT b), plus (NOT xi OR x(i+1)) for 1<=i<t. It is clause-minimally UNSAT, by forcing x1 true, xt false, and a chain of implications; deleting any clause allows an explicit satisfying assignment. Replace each binary clause (u OR v) by (u OR v OR z_j) and (u OR v OR NOT z_j), with fresh z_j. The proper-3CNF H_t is clause-minimally UNSAT, has n=2t+5 variables, 2(t+3) clauses, and no units. Unit propagation eliminates k=0, so r=n, v=1 and r/log N tends to infinity for N=Theta(t log t). Yet an exact paired-clause recognizer reduces H_t to 2-SAT, decidable by implication-graph SCC in O(N) time and O(N) writable bits on its canonical encoding. Thus large r and a large minimally UNSAT core DO NOT imply an all-algorithm 2^r SAT-decision lower bound.

COUNTERTHEOREM: Any invariant unchanged by every equisatisfiability-preserving formula transformation depends only on the one-bit satisfiability label. Rich noncircular residual measures must restrict their symbolic calculus and charge discovery, checks, source reads, failed work, intermediate representations, DAG reuse and output.

COMPUTATIONAL: 9,860 assertions passed, zero failures; t=2..20 deletion-minimality verified; black-box coverage r=1..10; 156 INDEX instances with 71 UNSAT and 568 minimal-core deletions; five padded opposite-label SAT pairs. At t=20: n=r=45, m=46, N=1012 encoded bits.

OPEN first arrow: extract from every unrestricted, uniform deterministic SAT decider a charged compression-or-distinguish/continuation obligation that cannot be bypassed by 2-SAT, Horn, affine, random-access or wrapper computation. This is not established. No circuit gate/wire/switch lower bounds claimed.

Sources: SOURCEPROBE19, MAIN82 and ES-ATLAS-0025 Google Doc from existing project; Aspvall-Plass-Tarjan (IPL 1979); Nishimura-Ragde-Szeider (SAT 2004).
