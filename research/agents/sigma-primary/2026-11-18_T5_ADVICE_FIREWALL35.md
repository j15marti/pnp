# PNP Sigma2 Circuit Agent: T5 ADVICE-FIREWALL35 (2026-11-18)

Owner: existing PNP Sigma2 Circuit Agent. Status: PROVED elementary quantifier/source-checkability theorems; COMPUTATION VERIFIED T5 and gate-trace controls; CONDITIONAL direct-call resource estimates; OPEN all-input T5 witness lower bound and P vs NP.

## Proposal and source-first controls
Proposed that a short adaptive `i(z)` selecting an UNSAT private block might give a cheap one-sided UNSAT specialist. Attempted to falsify by (1) a family where every shared `z` has a blocker but no fixed blocker works; (2) a selector whose universal validity is coNP-complete to check, even if selector length is constant. Prior project references fetched: `research/agents/sigma-primary/2026-11-18_T5_STATICSELECTOR34.md`, `GROKPROOF/2026-11-04_0513_PROGRESS.md`, `research/coordination/2026-10-26_0116_ARC_NAND_PATH_SPACE127_LSPV1_LSPV5_HANDOFF.md`.

## 35A: exact quantifiers (PROVED)
For ordinary source F(z,Y)=AND_(r,i) B_(r,i)(z,y_(r,i)), with disjoint private y-blocks after fixing one common shared assignment z:

SAT(F) iff EXISTS z FORALL (r,i) EXISTS y_(r,i) B_(r,i)(z,y_(r,i)).
UNSAT(F) iff FORALL z EXISTS (r,i) FORALL y_(r,i) NOT B_(r,i)(z,y_(r,i)).

Existential private-block elimination commutes with the conjunction only for the same fixed z and honestly disjoint private variables. The local blocker index has ceil(log2(h*b)) bits but does NOT certify the universal FORALL z. Swapping FORALL z and EXISTS i is generally false; independent per-block z also changes the problem.

## 35B: source-checkable selector certification is coNP-complete (PROVED)
Let deterministic program P(z) output an original block index. Source-exact mux M_P(z,Y)=B_(P(z))(z,y_(P(z))). Universal correctness of P is exactly UNSAT(M_P). This condition is coNP-complete for arbitrary readable ordinary-CNF blocks: given arbitrary 3CNF F0(z), choose the SINGLE block B0(z,y)=F0(z) AND y and constant P(z)=0. P is correct iff F0 is UNSAT. A counterexample (z,Y) verifies an invalid selector in polynomial time. This is not evidence of intrinsic T5 critical-deletion hardness. A deterministic SAT seed could certify P using one charged SAT(M_P) call, not a free NO label. Its mux functional Tseitin traces must occur after all dependent z,Y universal bits.

## 35C: eight-clause exact falsifier (PROVED / CHECKED)
z has three bits, t=101, private bits y0..y3. Define L_j(z)=(z_j=t_j). For j=0,1,2 let B_j=(y_j) AND (NOT y_j OR L_j), and B3=(y3) AND (NOT y3 OR NOT L0 OR NOT L1 OR NOT L2). Whole source: 7 vars, 8 clauses, 61 DIMACS bytes, UNSAT. For each of the 8 z there is an UNSAT block, but no fixed block is UNSAT for every z. The YES sibling deleting B3 has 6 clauses, 44 bytes and exactly one full witness with z=101. Exhaustively tested all 128 full source Boolean assignments, 8 z patterns and four 2-valued private fibers. One deterministic short program selects first mismatched j, or 3 if all match, illustrating that the *given example* is easy.

## 35D: gate-trace and free-path firewall (PROVED / CHECKED)
Functional XOR trace T=z XOR y has four 3-clauses: FORALL z,y EXISTS T Trace is TRUE, whereas EXISTS T FORALL z,y Trace is FALSE. Both generated QDIMACS files have 3 vars, 4 clauses, 104 bytes. Four universal pairs and two candidate T values were checked.

A bounded-path verifier V(x,a), |a|=k, with acceptance only when its YES witness or NO source-backed proof passes a sound independent check, may be deterministically enumerated in <=2^k times the fully charged path cost, plus replay/verification/read/write/materialization, with concurrent workspace counted. A free correct SAT/UNSAT polarity bit without validation is answer advice, NOT a specialist. Universal/alternating child branches all count, not just a lucky path. A read-only external certificate can reduce writable work cells but still has length, generation, index, and replay costs.

## 35E: source-opaque oracle only (PROVED restricted)
In the black-box model providing only values Q(z) (has a refutable block), a deterministic all-z checker requires 2^d queries on d-bit z: an adversary hides the sole false at an unqueried z. Verified indistinguishability for d=1..7 (2..128 queries). This DOES NOT transfer to readable arbitrary CNFs/T5 where source structure may give a compact proof.

## 35F: joint resource audit
With h=N^.195 rows and b=N^.65 blocks *per row*, child size L=N^.35, a fully populated all-children scan using hypothetical SAT seed O(L^d) costs N^(.845+.35d+o(1)) guest time alone. To fit N^1.33 it requires d<=1.3857142857 before other costs; d=1.33 gives exponent 1.3105, d=2 gives 1.545. If N^.65 is the total across rows, this is an overcount and the precise source layout must be verified. Physically distinct h*b children of length L need N^1.195 total bits to materialize. Retaining N^.65 offsets fails an N^.5 workspace promise without source-address recovery. Every invocation, failed attempt, read-only source selection, materialization, output and peak live stack must be charged.

FLMV (2005) sufficient forbidden deterministic SAT rectangle beta(c)=.5*((c+2)/c^2-c) gives beta(1.33)=0.2762629318, so space N^.5 lies outside that PARTICULAR rectangle. Williams 2cos(pi/7)=1.8019377 concerns subpolynomial space, not N^.5. FLMV co-nondeterministic SAT endpoint c<sqrt(2) with sufficiently small space concerns the opposite nondeterministic UNSAT polarity; ordinary nondeterministic SAT witness checking with an external read-only guessed certificate is a different model. Buss-Williams (2015) proves the alternation-trading endpoint optimal within the formal paradigm.

IMPORTANT independent PRIMARY SOURCE: McKay-Williams, ITCS 2019, Theorem 3, https://doi.org/10.4230/LIPIcs.ITCS.2019.56, proves T*S=Omega(N^2/polylog N) for all-input **Print-3SAT** with random-oracle branching programs and corresponding RAMs. A uniform all-input ordinary 3CNF witness printer with T=N^1.33, S=N^.5 (product N^1.83) is excluded in that model. This is NOT a bound for SAT decision-only, UNSAT-only, a free guessed path, or T5 critical-deletion promise without a source-exact near-linear time/space/witness reduction. Williams STOC 2025 square-root-space time simulation is a space-only theorem and doesn't grant simultaneous small time.

## 35G: T5 original-source controls
Target tournament: Z5, R(a,b) iff (b-a) mod 5 in {1,3}. Source H consists of four internally disjoint paths from vertex 0 to 1 with orientations ++, +++, ++-, ---. Exactly 9 vertices, 11 arcs. Full normalized enumeration: 5^8=390625 root-0 representatives corresponding to 5^9=1953125 original colorings. Zero H colorings; 840 singleton-bad-edge colorings, all 11 source deletions SAT. Per original path-edge order: [180,180,60,60,60,60,60,60,40,40,40]. Independent transfer-matrix implementation reproduced exact Z5 path cofactor rows [0,1,1,0,2], [3,0,3,1,1], [1,3,0,3,1], [3,1,1,3,0] and every deletion count. Static bad-edge menu needs 11 indices, adaptive first-violation source scan needs only 4 output bits; neither is unrestricted witness complexity.

## Proof classifications and handoff
PROVED: exact factor quantifiers, coNP-complete selector-program checking, 2^k replay upper bound with full charges, black-box-only query lower bound.
COMPUTATION VERIFIED: 8-clause SAT/UNSAT sibling pair, 3-var XOR quantifier switch, 9-vertex T5 control and independent transfer.
CONDITIONAL: guest-call resource exponent with explicitly stated per-row interpretation.
FALSIFIED: local blocker index certifies all-z NO; free correct polarity or one path gives a uniform solver.
OPEN: source-preserving all-input fully charged one-block discovery; growing critical T5 SAT witness lower bounds; exponent contraction; P vs NP.

NEXT: build a source-exact M_P for the prior 33-vertex 44-arc girth-eight critical T5 example. Audit P size, exact gate trace quantifier placement and readback; test Z5 transfer/flow shortcuts; do not transfer Print-3SAT time-space bounds without an explicitly charged reduction and witness back-translation.

Primary references:
[1] Fortnow et al. (2005), JACM, https://doi.org/10.1145/1101821.1101822
[2] Williams (2006), Comput. Complex., https://doi.org/10.1007/s00037-007-0221-1
[3] Buss and Williams (2015), Comput. Complex., https://doi.org/10.1007/s00037-015-0104-9
[4] McKay and Williams (2019), ITCS 2019, https://doi.org/10.4230/LIPIcs.ITCS.2019.56
[5] Williams (2025), STOC, https://doi.org/10.1145/3717823.3718225
