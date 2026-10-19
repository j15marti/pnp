# REDTEAM26 (2026-10-20 07:17 Asia/Seoul)
Status: exact restricted construction, independent review pending. P versus NP OPEN. Two routes: MCSP/MKTP magnification; arbitrary SAT-decider ARC/FLMV. Compact histories diagnostic only.

## Four prespecified hostile tests
(1) Does a hard planted globally consistent witness imply all globally consistent witnesses hard?
(2) Can clauses be generated at any indexed position in poly(log N), without an exponential scan?
(3) Can equivalent CNF wrappers break syntactic Horn recursive eligibility?
(4) Can a universal certified solver remove unknown SAT exponent and input replay costs? Prior Hutter/CHMY/MMW/FLMV scopes retained.

## Exact counterexample, with proof
For every n>=1 let N=2^n and variables b,y_0,...,y_(N-1). For each index i of even parity, require y_i=0. For odd parity require y_i=NOT b, using clauses (b OR y_i) and (NOT b OR NOT y_i); unit clauses can be padded to width 3. A source flag a=0 adds contradictory clauses b and NOT b; a=1 adds nothing. Thus satisfiable iff a=1, with EXACTLY TWO all-clause satisfying assignments when a=1: (b=0,y_i=parity(i)) and (b=1,y_i=0).
The 3N/2 base clauses admit a poly(n) random-access generator: given clause index j, set (k,r)=(floor(j/3),j mod 3). Consecutive addresses 2k and 2k+1 have opposite parity; parity(k) chooses one of two explicit 3-clause patterns.
Address y_i by 0||i and b by 1||0^n. For the b=0 PLANTED assignment, any fixed-fanin AND/OR/NOT index circuit computing W(0||i) must compute n-bit parity and use at least n-1 binary gates. A connected fan-in-two output DAG with g binary gates, u unary gates and r input variables has <=2g+u edges and >=g+u+r-1 edges; hence r<=g+1. Parity depends on all n variables. In contrast, for b=1 the complete, globally shared satisfying assignment circuit is simply W(address)=its highest bit, using zero gates.
Therefore even a hard PLANTED satisfying circuit with poly(n) indexed clauses does NOT imply every shared satisfying circuit is hard. A unique-tableau or all-witness-hardness lemma on the ACTUAL special diagonal source is necessary. This example is easy and nonparsimonious and establishes NO SAT lower bound.

## ARC closure hostile control
Satisfiable Horn H=(NOT x OR y) AND x stays satisfiable after adding tautological (u OR NOT u OR v), but the resulting clause is syntactically non-Horn. A Horn-only promise solver with off-promise default NO fails the wrapped instance. This proves no free syntactic Horn closure; normalization may be easy and must be charged.

## Tests and proof status
Reproducible local standard-library Python checked n=1..7, all 381 clause-index positions; all 552 full assignments at n=1..3 (two solutions per YES, zero for NO); 23,400 <=2-gate descriptions on six address bits, 294 distinct truth tables: planted 0x96696996 absent, easy 0xffffffff00000000 present. SAT-equivalent Horn control passed. Zero failures. Mathematical proof separately establishes scoped all-n statement. Raw GitHub target results/raw/separation/2026-10-20_0717_REDTEAM26_PLANTED_EXISTENTIAL_raw.json.
Prior no-gos unchanged: CHMY small-beta transport OPEN; MMW SAT->ordinary-MKTP R_k OPEN; arbitrary ARC hereditary fully charged joint resource contraction OPEN. Hutter's certified fastest theorem does not remove candidate proof or runtime-exponent requirements.

Next peers: :00 validate true CHMY promises/tape; :12 check existential W vs planted and proof-certified racing; :24 verify recursive promise closure, DELAY and peak live space; :36 falsify the j/3 index generator and n-1 dependency argument; :48 integrate as diagnostic only. No root main.tex overwrite. No schedule edits.
References: McKay/Murray/Williams STOC 2019; CHMY STACS 2021; FLMV JACM 2005; Hutter IJFCS 2002; Oliveira/Pich/Santhanam ToC 2021.
END_REDTEAM26_SCOPE_P_VS_NP_OPEN
