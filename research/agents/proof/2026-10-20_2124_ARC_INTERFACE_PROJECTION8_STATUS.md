# ARC-INTERFACE-PROJECTION8 (2026-10-20 21:24 Asia/Seoul)
Status: PROVED restricted semantic contractor; OPEN unrestricted arbitrary-decider ARC/FLMV; P versus NP OPEN.

## Before-literature proposals
(1) Exact block interface projection and global shared-witness join; (2) affine Schur-complement symbolic boundaries; (3) collision-free exact compatibility bitsets; (4) a readable child factory with all source/replay costs charged.

## Verified primary theorem
FLMV, Time-Space Lower Bounds for Satisfiability, JACM 2005, Section 2.1, Theorem 3.1, Corollaries 3.2 and 5.8. Exact model has indexed read-only source, write-only one-way output, work/index tapes counted. Corollary 5.8 excludes NTIME[n] inside DTISP[n^c,o(n^d)] for d=((c+2)/c^2-c)/2. At c=241/200, d=11642479/23232400=0.50113113582755. SAT transfer uses Theorem 3.1, not an implicit equivalence. Primary: https://lance.fortnow.com/papers/files/tst.pdf .

## Actual candidate construction
Input: a VALID scoped 3CNF event stream with OPEN(v), CLAUSE(l1,l2,l3) referencing three currently open distinct variables, CLOSE(v). OPEN identifiers strictly increase consecutively. Live width w <= (log_2 N)/20. This is a restricted representation, NOT arbitrary SAT. Partition source of encoded bit length N into q=N^(1/2+o(1)) contiguous blocks of N^(1/2+o(1)) bits. Boundary sets S_(j-1), S_j list variables live at each cut. For boundary assignments a,b, define R_j(a,b)= [a and b agree on intersection] AND SAT(the actual clauses of block j with endpoints pinned to a,b). For each pair construct a complete, ordinary binary proper-3CNF child by substitution, full renumbering and standard 1/2-to-3-clause gadgets. One readable child buffer; sequential calls to any fixed correct SAT algorithm A.

The exact join theorem is SAT(F) iff EXISTS a_0...a_q FORALL j R_j(a_(j-1),a_j). Proof: any satisfying assignment restricts to boundaries. Conversely each local witness glues to all others because validated variable lifetimes are contiguous and matching border assignments enforce global consistency. It is NOT independent SAT-status gluing or independent per-index witnesses.

If A has simultaneous time L^t, workspace L^s, with t>=1, each child length L=N^(1/2+o(1)), number of pinned-child calls <=q*2^(2w)=N^(3/5+o(1)). Pay for all failed child construction, copying, serialized query bits, oracle execution as an actual subroutine with work-tape random access, source parsing and index storage, two frontier bitsets, and one live child. Then:
T=N^(max(1,3/5+t/2)+o(1)), S=N^(max(1/2,s/2)+o(1)).
This contraction is PROVED only on the scoped low-width class. It is NOT an arbitrary-input hereditary successor: source-to-scoped-width normalization is missing, child width relative to its shorter length need not preserve the width threshold, and total fallbacks to A lose the purported resource improvement.

## Second theorem (derivative FLMV corollary)
An all-input deterministic total streaming SAT-to-scoped-CNF normalizer K, preserving both labels, outputting M<=N^(1+o(1)) bits of valid width <=(log_2 N)/20, with one-pass output time N^(c0+o(1)), c0<241/200, and same-machine workspace N^(1/2+o(1)), CANNOT exist. Direct low-width DP maintains a 2^w-bit assignment-set bitset: OPEN branches both values, CLAUSE filters, CLOSE existentially projects. Its time M*2^w polylog=N^(21/20+o(1)), space N^(1/20+o(1)). Pipeline it with K's write-only output, without a readable full output copy. This would solve unrestricted SAT below FLMV's time-space forbidden region after Theorem 3.1. This is not a new SAT separation, just a precise obstruction to a cheaply assumed normalizer.

## Reproducible finite audit
Independent Python implementation checked 135 ordinary proper 3CNF formulas (123 SAT, 12 UNSAT), 1170 clauses, 4605 fully serialized/reparsed child SAT queries, 6514 candidate boundary pairs, 464 independently verified pinned-child equivalences, 135 separate direct bitset-DP checks (21820 state updates), 16 connected bounded-occurrence non-affine cycles, both sides of implication and XOR families, minimally UNSAT all-eight-clause controls, seeded random formulas, and four intentionally high-width correct fallback cases. Zero failed assertions. Max measured width 7; max encoded child 42 bytes. The experiment compiler from ordinary CNF to event streams stores O(n) first/last occurrence metadata: it is TEST ONLY and cannot be called the missing general contractor.

## Next OPEN arrow
Develop a source-queryable exact symbolic boundary relation that can handle connected, high-width NONAFFINE sources without exponential signature storage or enumeration, while emitting only short ordinary children and maintaining hereditary correctness. Test with DELAY-padded arbitrary deciders and two recursion levels, charging every source read and live ancestor. Do not infer P != NP.
