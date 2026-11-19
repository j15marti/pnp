# SELECTOR-ADVERSARY1 handoff

Date: 2026-11-19 12:22 Asia/Seoul. P versus NP OPEN. External review pending.

PROVED/EXACT: every total function \(f:\{0,1\}^h\to[B]\) is realizable by an ordinary supplied-layout CNF with exactly block \(f(z)\) UNSAT on row \(z\), using two guarded clauses per row and disjoint private variables. The full selector table costs \(R\lceil\log B\rceil=N^{.195+o(1)}=o(N^{.5})\) bits. An invertible dense affine family has full shared support in every block yet selector evaluation is \(O(h^2)\); deleting one target produces a unique easy SAT row.

FALSIFIED: fixed bad block; small-support necessity; selector entropy/range as an unrestricted lower bound; selector-table square-root overflow; one favorable UNSAT path as a whole strategy; arbitrary polynomial seed as sufficient for the \(1.33\) one-step bound.

POLARITY: a SAT path must output/verify a shared row and every private witness. UNSAT requires \(\forall z\exists i\) coverage; a \(k\)-bit path handles one row, while an adaptive policy needs its whole strategy or charged universal traversal. Free polarity is answer advice. Standard nondeterministic guesses are not freely rereadable.

SOURCES: deterministic SAT has the Buss--Williams \((1.34070,.5)\) exclusion. Nondeterministic SAT has Fortnow's quasilinear/sublinear tradeoff, not a \((1.33,.5)\) point. Nondeterministic tautology has the Diehl--van Melkebeek--Williams \(c^2d<4\) theorem with some \(e>0\), not \(e=.5\). FLMV Corollary 6.5 yields a positive NO-side \((1.10,.5)\) point but none at \(1.33\).

COMPUTATIONAL: the checker passed 272 affine residuals, 72 support checks, an arbitrary eight-row permutation, five scaling points, and 9,680 T5 arc checks.

NEXT BLOCKER: a nontrivial local-residual class with uniform source-authenticated NO-certificate acquisition for every row and hereditary closure under child recursion.

No schedule, identity, ownership, enabled-state, or peer manuscript change.
