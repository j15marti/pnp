# RESTRICTION-STREAM-SHRINK70

Timestamp: 2026-10-22 18:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

## Question
SOURCE-SCAN-SCHEDULING69 left open a source-complete streamable compiler producing Q=n^0.6 exact children of virtual length n^0.5. Can the natural candidate family — restriction (variable-fixing) child streams, i.e. a DFS over a partial-assignment tree with one scan per node — meet the target?

## Corpus reviewed
AGENTS.md, root main.tex (LSPV-5 region and notes), research/main SOURCE-SCAN-SCHEDULING69 and its handoff, the 69 audit script. Older MAIN snapshots were not re-read this run; duplication with earlier restriction no-go results was not searched exhaustively (limitation).

## Literature (primary, via search)
Fortnow–Santhanam (OR-distillation, NP in coNP/poly), Drucker (AND side), Bodlaender–Jansen–Kratsch cross-composition (arXiv 1206.5941). Classification: ANALOGY needing a new bridge. Those theorems bound *compression of the total instance*; here total child length Q*n^beta = n^1.1 > n, so they are not triggered. Not a transferable theorem. (Sources disagree in wording on the containment direction; primary papers not re-checked.)

## Result (counting, ESTABLISHED for restriction streams)
A depth-d restriction tree has 2^d leaves. With Q=n^alpha leaves, d=alpha*log2 n, so at most O(log n) variables are fixed and a 3-CNF with Theta(n) clauses keeps size n(1-O(log n / n)) = n^(1-o(1)): effective beta=1-o(1) > 0.5. Reaching size n^0.5 requires fixing n-O(n^0.5) variables, i.e. 2^(n-O(sqrt n)) leaves, not n^0.6. Hence restriction-type children cannot satisfy (alpha,beta)=(0.6,0.5); the beta=1 recurrence c'=alpha+c has no finite fixed point.

**Status: ESTABLISHED (restricted to restriction/self-reducibility children). Unrestricted compiler: OPEN.**
Classification: the 69 compiler must be a non-restriction, semantic construction; this is a FAILED TRANSFER for the obvious self-reduction candidate, and it does not touch other representations.

## Finite audit
`experiments/review/2026-10-22_restriction_stream_shrink70_audit.py` (0.14s, no chunking needed): random 3-CNF, n=64..1024, ratio 4.2, depth log2(n^0.6), 20 trials each. Mean child size stayed ~98% of parent; 0 of 5 scales reach target n^0.5. Raw: `research/raw/RESTRICTION_STREAM_SHRINK70_raw.json`. Illustrates the counting argument; proves nothing about other compilers.

## Stale/overstated claims found
None new. Note the 69 "target" is a *conditional* fixed point, and the compiler is effectively a fast SAT procedure; its existence would be a P=NP-type consequence, so it can only serve a proof by contradiction from an assumed fast decider (where the decider, not restriction, must supply semantic shrinkage).

## Next test
Specify what in an assumed n^c decider could yield non-restriction shrinkage (e.g. via decider-trace descriptors), and charge the trace in ordinary KT.

No other root material changed beyond one note in main.tex. Nothing here resolves P vs NP.
