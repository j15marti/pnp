# BINARY-WORK-SAT4-EXACT22: verified two-bit AND gadget and communication barrier
Date 2026-10-26. Status PROVED for explicit constant gadget and derived restricted communication/circuit models, independently tested. P versus NP remains OPEN. Additive handoff to ACTIVE LSPV-1 through LSPV-5; preserve schedules and previous valid findings.

A new exact signed (2P,2N)-3CNF gadget carries two independent, variable-occurrence-preserving Boolean controls a,b. Start from the verified proper clause-distinct W1, 15 variables, 20 clauses, 0 satisfying assignments (source j15marti/pnp/experiments/review/early22_compiler_redteam_audit.py). Use zero-based original clause/literal positions:
  A: (6,0) and (11,0), opposite signs of variable 4;
  B: (17,2) and (9,2), opposite signs of variable 15.
For (a,b)=(1,1) leave W1 unchanged. For a=0 reverse both A signs; for b=0 reverse both B signs. The two swaps touch distinct variables AND distinct clauses. All four resulting formulas preserve proper width3, clause-distinctness, the exact same unordered supports at each of the 20 positions, and exact 2 positive + 2 negative occurrences per variable.

FULL EXHAUSTIVE 2^15 truth-table counts:
  (a,b)=(0,0): 772 models;
  (0,1): 272 models;
  (1,0): 272 models;
  (1,1): 0 models.
Thus UNSAT(H(a,b))=a AND b exactly. This is a fixed 15-variable finite certificate, not an assumed general solver rule. Source archive includes complete W1, all transformations, independent truth-table counters and validating witnesses.

For d disjoint module copies with each module's 15 variables renumbered, F_d(a,b) has EXACTLY V=15d, M=20d and explicit clause-list bit length N=Theta(d log d); every input is valid proper signed exact-(2,2) 3CNF and
  UNSAT(F_d(a,b)) = OR_{i=1}^d (a_i AND b_i).
Choose fixed clause order: ALL 2d clauses with A-controlled signs first, ALL 2d clauses with B-controlled signs second, then all 16d independent fixed clauses. Both halves carry input signs while clause counts, record lengths, supports and IDs stay fixed, so the bound is literal on a standard ordered clause-list encoding, NOT an invented metadata header.

Three corollaries, all precisely scoped:
(1) One-way Alice-before-Bob preprocessing without Alice rereads must retain >=d complete-state bits, even if preprocessing may perform unlimited Boolean operations. Bob's one-hot b=e_j gives response a_j, so 2^d row functions are distinct. In explicit sparse input, retained bits >=Omega(N/log N); fixed-order read-once BP width >=2^d. Not a random-access RAM lower bound.
(2) Any deterministic arbitrary-round two-party communication protocol with the a signs at Alice and b signs at Bob requires >=d bits, by the 2^d fooling set (a,NOT a). The communication matrix has rank 2^d-1 over EVERY field, by the full nonconstant monomial evaluation factorization of OR_i a_i b_i.
(3) In XOR/AND/NOT nonlinear-gate accounting, the Boolean ANF has degree 2d (top monomial product_i a_i b_i), hence >=2d-1 AND gates. Since a circuit using d ANDs plus d-1 ORs attains this, multiplicative complexity and arbitrary fan-in-two gate count for the PROMISED function are exactly 2d-1. The embedded literal-sign input map is affine/constant, so the same lower bound transfers to the all-input exact22SAT DECISION circuit at corresponding explicit lengths. This remains Omega(N/log N), not superlinear in N.

Sharp escape: for the one-hot Bob promise b=e_j, a RAM with indexed input detects j, then reads ONE A-controlled sign from the selected module (and optionally verifies the whole literal pattern in O(N) time), requiring O(log N) live work. For general b, RAM can directly scan both input blocks and compute OR_i a_i b_i in O(d) gates and O(log N) workspace. Exponential communication rank and strong one-way memory do not imply superlinear unrestricted work. The one-way source cutoff is not an assumption of general SAT algorithms.

Audits: 60 opposite-sign swaps available in W1; all 60 individually make SAT; 1,680 pairs on disjoint variables have all three nonbase variants SAT. Chosen pair (A var4, B var15): full counts 772,272,272,0. 2,708 composite exact22 sign/order/balance/witness tests passed through d=12, no failures. Previous dense INDEX SAT embedding: 51,306 direct truth-table cases, 19,426 indexed-escape cases; previous dense NONDISJ embedding: 30,036 cases; GF2 rank d<=8 and GF2/GF3/GF5/GF7 for d<=5 passed. Full 8-page formal PDF, complete scripts, raw JSON, LaTeX, bibliography, two plots are in the user's saved BINARY-WORK-SAT4 complete source archive.

What is OPEN: an unrestricted RAM/TM simultaneous time-space bound beyond ordinary input acquisition and linear logical operations. Do not claim native SAT hardness from the input order, restricted OBDD, or a communication protocol whose parties lack shared random access. Seek a cost-preserving repeated-interaction theorem that survives ANY finite polynomial RAM time and storage and BOTH SAT/UNSAT, or a true derived same-machine upper coupling into FLMV/Buss-Williams forbidden regions. P vs NP OPEN.
