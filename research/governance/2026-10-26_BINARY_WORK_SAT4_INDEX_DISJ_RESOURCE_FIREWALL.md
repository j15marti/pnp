# BINARY-WORK-SAT4: Exact INDEX and DISJOINTNESS restrictions of dense 3SAT UNSAT
Date 2026-10-26. P vs NP OPEN. PROVED RESTRICTED communication/OBDD theorems with symbolic proofs and independent finite audit. All five current LSPV agents are enabled; preserve roles and schedules. Full user deliverables: BINARY_WORK_SAT4_report.pdf and source ZIP, 2026-10-26.

## 1. Exact INDEX reduction, near-maximal one-way memory

For n>=5 let p=n-2 and dense proper-3-clause selector U_n on Q=8*C(n,3) bits. Reserve m=C(p,3) Alice selector coordinates, one for every ALL POSITIVE triple of the p base variables x_1..x_p. Remaining clause selectors are Bob's.

For b in {0,1}, let literal ell_i(b)=x_i if b=1 else NOT x_i. Define proper 3-CNF G_i(b) as the 4 clauses
  (ell_i(b) OR sign1*u OR sign2*v), sign1,sign2 in {+,-},
using the SAME two auxiliary variables u,v for all i. G_i(b) iff x_i=b; u,v remain arbitrary.

For a query triple J subset[p], Bob selects exactly 4p clauses B_J=AND_{i in J} G_i(0) AND_{i notin J} G_i(1), setting every other Bob coordinate to zero. All Bob clauses involve u or v, so none overlaps Alice selector coordinates. B_J has four models differing only in u,v and precisely the x_i with i in J set to zero. Only Alice's ALL POSITIVE clause on J is falsified. Therefore
  U_n(a,B_J)=a_J
for EVERY Alice a in {0,1}^m and every J.

All 2^m early assignments induce distinct residual rows. Every deterministic preprocessor that sees only Alice first, passes a finite state, and cannot reread her bits in Bob's phase, needs m retained bits, regardless of its computation time; any Alice-before-Bob ordered read-once branching program has width >=2^m=2^{Omega(Q)}. Exact m/Q = (n-3)(n-4)/(8n(n-1)) -> 1/8. If head positions are not included in work-space bit count, add all persistent head/control information (O(log Q) for fixed-head polynomial-time machines).

This is one partition and a NO-REREAD promise. It is NOT an arbitrary RAM SAT lower bound.

## 2. Sharp escape and circuit comparison

On the INDEX promise, two indexed Bob-side clause sentinels per base variable reveal J in 2p probes. Read Alice bit a_J ONCE, using O(log Q) workspace; optional full Bob-promise validation scans other Q-m clause coordinates and still reads only one Alice bit. Hence even one source reread defeats the above m-bit bound. A two-pass sequential read-only input stream can also solve the promise in O(Q polylog Q) time and O(log Q) workspace. Two-way communication for INDEX needs only ceil(log_2 m)+1 bits (Bob sends J; Alice sends a_J).

A general all-input fan-in-two Boolean circuit for U_n has at most 2^n*C(n,3)-1=2^{O(Q^{1/3})} gates by OR-ing each assignment's falsified-clause set then AND-ing across all 2^n assignments. This is much smaller than the 2^{Omega(Q)} Alice-first OBDD width, showing the ORDER restriction cannot be dropped.

The INDEX communication submatrix has 2^m distinct rows but GF2 rank only m: one-way state bits m come from ROW DIVERSITY, not the logarithm of rank.

## 3. Interactive-robust DISJOINTNESS, another restricted barrier

Take n=d+2 variables x_1..x_d,u,v. Alice bit a_i selects ALL FOUR G_i(0) clauses, Bob bit b_i selects ALL FOUR G_i(1) clauses, and all other clause selectors are zero. Then
  U_{d+2}(a,b)= OR_{i=1}^d (a_i AND b_i).
For every d, 2^d pairs (a, complement(a)) are zero-input fooling-set pairs, requiring >=d bits in ANY deterministic two-way communication protocol, regardless of round count. The matrix rank is EXACTLY 2^d-1 OVER EVERY FIELD because its decomposition over nonconstant monomial evaluation columns has diagonal coefficients +-1. Yet the function has 2d-1 ordinary binary gates (d AND followed by d-1 OR). This is explicit rank/communication growth without superlinear circuit work inside a SAT-derived relation.

## 4. Reproducible audits

- INDEX full SAT truth-table masks checked 10,306 formula/query pairs exhaustively for p=3..5, plus 41,000 sampled cases p=6, all passed.
- Indexed access decoder tested 19,426 cases p=3,4,5,6,8, all passed; promised-query probes exactly 2p+1; optional validation of whole Bob side done.
- NONDISJ exact SAT masks checked 30,036 pairs d=1..8; fooling-set crossings checked for d<=7; all passed.
- GF2 rank verified for INDEX and NONDISJ through d=8; GF2/GF3/GF5/GF7 rank verified for NONDISJ through d=5. All zero discrepancies.
- Complete PDF, LaTeX+Biber bibliography, five standalone audit scripts, JSON raw results and plots supplied as user research archive. These tests check finite examples; the proofs give all-size theorems.

## 5. Exactly what is OPEN

Neither result proves ANY new superlinear RAM SAT time lower bound. INDEX requires irreversible information cutoff; one random-access reread destroys its storage bound. NONDISJ survives interactive messages but shared-input RAMs evaluate it in O(d) binary gates and O(log d) memory. Exponential communication-matrix rank is not exponential unrestricted circuit complexity. The full ANF-degree theorem and every-partition existential full-degree cofactor theorem from BINARY-WORK-SAT2/3 do not imply the row-diversity statement for all partitions (AND_Q is a simple counterexample). Dense Q=Theta(n^3) input cannot be confused with sparse 3-CNF bit length. The new result does NOT apply to exact signed 2P2N unless separately compiled with charged input-partition preservation.

Next test: derive or falsify a RAM-native repeated-interaction/direct-sum lower bound allowing arbitrary input revisits, adaptive representation changes, caching, and any finite polynomial degree. Do not use the INDEX one-way bound as RAM work or space. Keep FLMV/Williams/Buss-Williams same-machine strict tradeoffs separate and P!=NP OPEN.

Primary references: Roughgarden (2015) CC notes https://timroughgarden.org/w15/l/l2.pdf and l4.pdf; Beame, Jayram, Saks, JCSS 2001 https://www.sciencedirect.com/science/article/pii/S0022000001917787; FLMV JACM 2005 https://lance.fortnow.com/papers/files/tst.pdf.
