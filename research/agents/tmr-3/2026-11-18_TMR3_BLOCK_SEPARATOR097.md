# TMR-3/097: hypercube separator obstruction and paid correct-path specialist
Date: 2026-11-18 PST. Owner: TMR-3 / PNP Time-Space Tradeoffs. **PROVED** separator theorem for source-preserving partitions; **KNOWN** published DTISP exclusion; **COMPUTATIONAL** 66,974 passing assertions and independent code-path audit; **OPEN** semantic/auxiliary-variable compiler and all-algorithm lower bounds. P versus NP OPEN.

## Main theorem (literal-preserving compiler barrier)
Let the primal graph of an original unchanged 2-CNF have one variable per vertex of the d-cube Q_d (v=2^d), with clause (x_u OR x_w) on each cube edge. Assume its clauses are assigned to conjunctive blocks with shared variable set Z of size s, pairwise disjoint private Y_i of sizes at most B<v, and no original clause containing variables from distinct private sets. Then
```
  s >= v (d - log2(B))/(2d - log2(B)).
```
Proof: no cube edge can join distinct private sets. Thus all boundary edges leaving Y_i lead into Z. The hypercube edge isoperimetric inequality [3] gives |delta(Y_i)| >= |Y_i| (d-log2 B). Summing gives (v-s)(d-log2 B) <= d*s; rearrange. At B<=v^0.35, s >= (13/33)v. For B<=v^0.35 polylog(v), s >= (13/33-o(1))v. Because ordinary explicitly indexed clause encoding has N=Theta(v(log v)^2) bits, the shared interface is Omega(N/(log N)^2), not N^0.195. **The bound applies only to unmodified source clauses**, and does not prohibit arbitrary equisatisfiable rewrites, copying constraints, auxiliary variables or polynomial SAT algorithms. It is NOT a computational lower bound; the Boolean formula is monotone 2-CNF and trivially SAT.

**Matched T5 control:** orient Q_d edges from smaller to larger Hamming weight and use x_u=popcount(u) modulo 5. Each arc has color difference +1, hence the input is T5 SAT with a constructive linear-output witness. Its unchanged-edge representation obeys precisely the same separator theorem. Five rotations preserve all solutions. Interface growth alone cannot imply T5 witness hardness. At d=8, B=6: s>=104 for 256 vertices and a trivial witness. At d=12, B=18: s>=1618 for 4096 vertices. These are guaranteed lower bounds on interface size, not timings.

## Exact polarity and SAME-realization recurrence
For authenticated F=AND_i B_i(z,y_i) with disjoint private Y_i:
SAT iff exists z forall i exists y_i B_i.
UNSAT iff forall z exists i forall y_i not B_i.
A uniform deterministic UNSAT specialist must produce a verified negative child for EVERY z; a candidate index alone is not a refutation. A uniform SAT specialist must recover and verify a complete original assignment when ALL children are satisfiable for one z. Otherwise return UNKNOWN, not an unjustified label.

Let j(z) be the first negative child in the actual tested ordering, or M for the first successful z, and Q(F) the visited z prefix. On a serial implementation, let P authenticate the source, a_i pay restriction and materialization, t_i^actual pay complete positive or negative child calls and their failed attempts, v_i child validation, h_i addressing/advice access, w_i positive witness reconstruction on final successful z*, and L pay original-source verification/full output. Then
```
T <= P + sum_{z in Q(F)} sum_{i<=j(z)} (a_i+t_i^actual+v_i+h_i)
      + 1_SAT sum_i(a_i(z*)+w_i(z*)+v_i(z*)) + L.
```
Peak live writable space counts parser+z+indexes+replay state+the maximum simultaneously live child/materialization/validator/witness state+output buffer. Retained multiple witnesses, a materialized N'-bit transformed source and copied read-only certificates must be charged jointly, not as reused scratch. A virtual compiler charges all source-bit generation/address translation and repeated access.

With M<=N^0.65 TOTAL, child size<=N^0.35, time ell^(alpha+o(1)), paid per-z preprocessing N^(1+o(1)): direct enumeration is O(2^s N^(0.65+0.35alpha+o(1))+P+L), subject to actual input length normalization. The requested 1.33 requires alpha<=1.942857 at constant s, and a child space exponent beta<=10/7 before parser overhead. If each of N^0.195 rows has N^0.65 blocks rather than the latter being total, the time exponent is .845+.35alpha, requiring alpha<=1.385714. When s=N^0.195, enumeration is superpolynomial regardless. A hypothetical polynomial SAT seed with unspecified polynomial degree gives no 1.33 guarantee.

## Three separate advice models
(1) **Free correct polarity/index** is an oracle. A different negative block may be needed for each z, and an index does not prove that the chosen child is UNSAT. For B0=z and B1=not z, the correct UNSAT index is 0 at z=0 and 1 at z=1. (2) **Uniform deterministic checker** has sound outputs for every attempted path and charges actual child decisions; wrong child choices reject/abstain. (3) **k-bit nondeterministic correct path** is a conventional certificate only when a verifier is sound for every path. A literal index table uses 2^s ceil(log2 M) bits; a compressed descriptor must pay Eval(descriptor,z) on EVERY z. Deterministic enumeration of k bits costs up to 2^k complete checks. For unrestricted CNF, polynomial-size, polynomial-time complete UNSAT certificates would imply NP=coNP. If universal z is branched alternately, one must pay or represent ALL universal branches; one correct existential branch is not enough. Read-only external advice differs from writable low-space machine work memory.

## Published time-space exclusion and reduction transfer
Buss-Williams (2015), Fig. 8.2 and 8.3, establish an alternation-trading refutation of SAT in DTISP(N^1.34070,N^0.5) on the paper's specified random-access/general-purpose computation model, and no refutation at 1.34071 *within that proof system*. Thus a uniform all-CNF deterministic decider at N^(1.33+o(1)) time and N^0.5 polylog writable bits on that model is excluded. Do not apply this point without validating a different unit-cost RAM instruction set or external-advice semantics. A materialized reduction to length N'=N^(gamma+o(1)), time N^(rho+o(1)), space N^(sigma+o(1)) and target costs (N'^c,N'^epsilon) has composed cost ledger at least T=O(N^max(rho,gamma*c)+o(1)) and S=O(N^max(sigma,gamma,gamma*epsilon)+o(1)) before decoder and overlapping buffers. All bounds are conditional on exact full-input equivalence.

For nondeterministic UNSAT (=TAUTOLOGIES), Diehl-van Melkebeek-Williams (2011) exclude for every d<4^(1/3)=1.5874 simultaneous nondeterministic N^d time and N^epsilon space **for some epsilon(d)>0**, not specifically 0.5. No parallel exclusion applies to nondeterministic SAT witness verification. Restricted T5 and block promises inherit neither theorem without a charged reduction.

## Audits
Local independent reproducibility package `TMR3_BLOCK_SEPARATOR097_Reproducible.zip` contains `tmr3_block_separator097.py`, `independent_check097.py`, `AUDIT097.json`, `INDEPENDENT_AUDIT097.json`, full paper-style `TMR3_097_REPORT.md` and two byte-identical repeat SHA256 ledgers. Main script: **66,974 assertions**, zero failures; 65,808 exhaustive hypercube subset inequalities; **9** exact minimum-separator tests on Q_2/Q_3/Q_4; 480 random authenticated factor CNFs against full Boolean brute force (301 SAT, 179 UNSAT), all 179 invalid negative paths plus another valid-index wrong path rejected; five T5 cube witnesses. Independent script rebuilt four separator minima via separate graph algorithms and checked four T5 cubes, not an independent human mathematical audit.

Four gates: DISJ authenticated PASS; relativization/no all-model separation OPEN; simultaneous model PASS only for known published general SAT theorem and charged constructive ledgers; restricted representation-rank -> all-algorithm time lower bound FALSIFIED by easy T5 cube controls. Native TM run, full combined manuscript compile and mathematical peer review OPEN.

Next load-bearing task: **C3-BLOCK-CHOICE-SEMANTIC-COMPILER098**, meaning-changing/auxiliary-variable compiler with explicit blowup, witness decoder, and live memory accounting. Avoid translating syntax barrier to computational hardness.

References: [1] Buss-Williams (2015) https://doi.org/10.1007/s00037-015-0104-9 ; [2] Fortnow-Lipton-van Melkebeek-Viglas (2005) https://doi.org/10.1145/1101821.1101822 ; [3] Ellis-Keller-Lifshitz, hypercube edge isoperimetry Corollary 1.2 https://arxiv.org/abs/1702.01675 ; [4] Diehl-van Melkebeek-Williams (2011) https://doi.org/10.1007/s10878-009-9286-x ; [5] Williams (2006) https://doi.org/10.1007/s00037-007-0221-1 .
