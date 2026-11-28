# Decomposition Obstructions: MODULAR-BLINDSPOT-1

**Timestamp:** 2026-11-23 10:29 PST (America/Los_Angeles)  
**Role:** Independent adversarial red-team, constructive universal-decomposition program  
**Coordination:** [issue #324](https://github.com/j15marti/pnp/issues/324)  
**Status:** PROVED/EXACT restricted counterexample, computational audit completed; independent peer review PENDING. P versus NP remains OPEN.

## 1. New failure condition beyond the Fano GF(3) shortcut

The 09:35 Meta Solver Theorem agent proves a useful, sound one-way rule: recognize integer EXACT-ONE constraints; if Gaussian elimination over GF(3) refutes their linear equations, the original Boolean formula is UNSAT. Its Fano-plane example has such a modular inconsistency. This red-team report constructs a **Boolean UNSAT** 3-CNF in the *same syntactically recognized mixed affine + 2-SAT class* for which:

* The parity subsystem (GF(2)) is satisfiable.
* The separate 2-SAT subsystem is satisfiable.
* **Every** modular system of the recovered EXACT-ONE integer equations is satisfiable, including GF(3), all other primes, and every composite modulus. In fact the integer equations themselves have an integer solution.
* The linear programming relaxation with every variable in [0,1] is feasible.
* Yet the original 0/1 problem is UNSAT, and deleting any one EXACT-ONE triple makes it SAT.

Thus no rule relying *solely on modular inconsistency of the recovered original linear equations*, even if it tests all moduli, can be a universal contradiction detector. This is a precise limitation on that rule, **not** a lower bound on an unrestricted algorithm, which may derive additional Boolean consequences and cuts.

## 2. Explicit core and proof

All variables x0,...,x6 are Boolean. For each listed triple, impose EXACTLY ONE true. Six rows:

E0: (0,5,6)  
E1: (1,2,5)  
E2: (0,1,2)  
E3: (2,3,6)  
E4: (3,4,5)  
E5: (4,5,6).

Each row e=(u,v,w) is the conjunction of an odd-parity equation u XOR v XOR w=1 and three binary pair exclusions (not u or not v), (not u or not w), (not v or not w). A parity row expands into four 3-clauses. Thus the ordinary CNF has 7 variables, 24 ternary clauses and 18 binary clauses, 42 clauses total. This expansion is assignment-preserving, not an informal identification of XOR with EXACT-ONE.

**UNSAT proof using integer Boolean reasoning.** Subtract E2 from E1: x5=x0. Subtract E5 from E4: x3=x6. Then E0 gives 2 x0+x3=1. Since x0,x3 lie in {0,1}, necessarily x0=0 and x3=1, and hence x6=1. But E3 then gives x2+1+1=1, impossible for Boolean x2. QED.

**Why every modular inconsistency-only test misses it.** The integer vector (x0,...,x6)=(0,2,-1,1,0,0,1) satisfies all six integer linear equations Ax=1 exactly. Its reduction modulo any q therefore satisfies the same equations modulo q. Moreover, the 6-by-6 minor of the 6-by-7 incidence matrix using columns (0,1,2,3,4,6) has determinant +1. Consequently A is surjective over every Z/qZ, including all prime fields; this rank claim is stronger than checking finitely many primes. The all-ones vector satisfies the original GF(2) odd-parity equations, while all-zero satisfies every negative 2-CNF pair exclusion. The fractional vector x_i=1/3 for every i belongs to [0,1]^7 and satisfies Ax=1 over Q. QED.

The failure is **not** a failure of Gaussian elimination itself: Gaussian elimination correctly reports the integer-equation system consistent. Failure occurs only if one mistakenly identifies this consistency with existence of an integral 0/1 assignment. Stronger cutting-plane, mixed-integer, or assumption-based SAT reasoning can refute this small core.

## 3. Exact computational controls

The linked standard-library Python reproducer independently enumerates all 128 Boolean assignments of the seven variables and checks equivalence between the 42-clause CNF and the six EXACT-ONE constraints. It also checks the six neighbors obtained by deleting each row; their numbers of satisfying models are [1,1,1,2,1,1]. The full core has zero. It verifies the integer and LP witnesses, the determinant +1 unimodular minor, and elimination over primes 2,3,5,7,11,13,17,31,97, each with rank six and consistent right-hand side.

An additional seeded 280-instance experiment samples 40 positive EXACT-ONE 3-uniform hypergraphs for each n=7,...,13 with m=n-1 distinct triples, and compares exhaustive 0/1 enumeration with exact GF(2) and GF(3) elimination. Results:

| n | cases | UNSAT | UNSAT but both GF(2) and GF(3) consistent | UNSAT with full row rank over GF(3) |
|---:|---:|---:|---:|---:|
| 7 | 40 | 17 | 4 | 4 |
| 8 | 40 | 19 | 8 | 7 |
| 9 | 40 | 20 | 6 | 4 |
| 10 | 40 | 25 | 12 | 10 |
| 11 | 40 | 25 | 10 | 8 |
| 12 | 40 | 24 | 10 | 6 |
| 13 | 40 | 29 | 12 | 9 |
| Total | 280 | 159 | 62 | 48 |

No SAT instance was falsely rejected by either field. These are finite reproducible observations, **not** evidence that random instances are asymptotically hard or that a prescribed family requires superpolynomial time. Some cases may have short counting or cutting-plane refutations.

Reproducer: [2026-11-23_modular_blindspot1.py](../../../experiments/decomposition_obstructions/2026-11-23_modular_blindspot1.py). Run it with any Python 3 version supporting int.bit_count(), passing a JSON output path.

## 4. Independent backdoor-growth warning, not a hardness theorem

Let G_r consist of r variable-disjoint copies of this 7-variable, 6-triple core, connected into one primal component by 2-CNF equality clauses joining one variable of each consecutive copy. The affine part remains satisfiable (all ones), the binary part remains satisfiable (all zeros), and G_r remains UNSAT. Every parity triple still has four 3-clauses; to make **every** residual syntactically 2-CNF, a strong 2-CNF backdoor must hit every triple. In one copy, the minimum triple-hitting set is {x2,x5}, of size two; no single variable belongs to all six triples. The copies are variable-disjoint, so the minimum strong syntactic 2-CNF backdoor has cardinality exactly 2r. Adding only binary equality clauses cannot change this lower bound or the matching 2r upper bound.

Yet each G_r has an easy, constant-sized local UNSAT witness! The growing backdoor size, connected primal graph, and growing affine nullity are **not** general SAT runtime lower bounds. They falsify only the claim that a universally useful algorithm must always find a logarithmic 2-CNF backdoor or must pay its 2^k branch tariff on this family. Whole-formula recognition or local proof extraction bypasses it cheaply.

## 5. Exact logical boundaries for proposed universal lemmas

1. **GF(p)-consistency implies Boolean compatibility:** FALSE. The six-row counterexample is consistent over every modulus and has an unrestricted integer solution but no 0/1 model.
2. **LP feasibility implies Boolean compatibility:** FALSE. The all-1/3 point is feasible.
3. **Polynomial-time recognizability and separate SAT algorithms for affine and 2-CNF imply polynomial-time intersection:** NOT ESTABLISHED; the recognized mixed language is NP-complete by the Meta Solver Theorem agent's disjoint-occurrence reduction from positive ONE-IN-THREE SAT (Schaefer 1978). A polynomial universal compatibility solver for this class would prove P=NP. This is a conditional complexity consequence, not a separation.
4. **Every input has a small strong 2-CNF backdoor:** FALSE even for easy connected UNSAT families G_r, where k=2r. An O(2^k poly(N)) algorithm conditional on discovery/certification remains valid but can be exponentially large in N for this route.
5. **Numerous distinct syntactic, canonical, or affine residuals imply compulsory work:** FALSE without a lower bound that survives paid semantic compaction, global decisions, shared proof DAGs, and arbitrary adaptive algorithms; the T5 handoff and the prior 09:25 redteam already establish such bypass cautions.
6. **Universal polynomial decomposition exists because each input has a short existential SAT/UNSAT explanation:** NOT PROVED. Finding, checking, selecting, combining and using representations on the same input must have an explicitly polynomial aggregate tariff.

For any fixed purported solver A with cap T_A(N) <= K N^a, a valid constructive P=NP argument must instead give one **uniform** method correct on every explicit 3-CNF input, bound its discovery + recognition + canonicalization + interface compatibility + proof production/verification + scheduling + communication + fallback costs by N^c for a fixed c, and show that all represented residual states are processed within that budget. The modular shortcut is a *sound possible branch*, never a universal coverage lemma.

## 6. Same-execution work / space / cumulative-memory ledger

Core CNF encoding: 7 Boolean identifiers and 42 clauses of length <=3, hence O(1) core size. For m triples on n variables, directly expand to 7m ordinary clauses; conventional explicit variable-index encoding uses N=O(n+m log n) bits, with exact constants depending on the selected representation. Input parse, pattern recognition and clause-normalization are charged; syntactically advertised parity groups can be reconstructed in polynomial time, but discovering hidden equivalent groups in arbitrary CNF is not free.

A dense m-by-n matrix takes O(mn) field cells, plus bit costs, and Gaussian elimination costs O(mn min(m,n)) fixed-field arithmetic operations (a conservative upper bound). Checking any constant number of fixed primes is polynomial. For general modulus q, charge its representation and arithmetic. Exhaustive independent oracle checks above cost O(2^n m) constraint evaluations and storage proportional to the output list of satisfying assignments; this is an **audit**, not part of the proposed solver. The Python finite experiment has no native machine instrumentation for time T, peak bits S, or physical CM=sum_t S_t, and offers no claimed measured CM lower bound. Reading or checking a proof has a distinct, charged cost; proof certificates here are elementary derivations, not a general polynomial-size proof-family claim.

In the T5 handoff's notation, unrestricted exact counting and decision stay separate; no claim transfers from a restricted architecture to an unrestricted TM. The decision target remains OPEN. Independent review is pending.

## 7. Next dependency / assigned adversarial test

To challenge a serious cooperative theorem rather than merely another local heuristic: require a **uniform polynomially bounded procedure that turns GF(2) + at-most-one constraints into a reusable stronger Boolean certificate**, whether by cutting planes, higher-modulus/Boolean ideals, variable elimination, certified clause learning, or separator summaries. Run that procedure on (a) this six-row modular-invisible UNSAT core and its six SAT neighbors, (b) seeded GF(3)-invisible cases with full row rank, and (c) adversarially generated high-coupling positive ONE-IN-THREE instances. Count the cost of *recognizing* implied EXACT-ONE and all proof-DAG nodes and synchronization, not just downstream Gaussian elimination. Ask the discovery team for a theorem bounding the growth of this proof process on **arbitrary** 3-CNF, or supply a counterexample to any proposed bound.

## Sources

- [Schaefer, The Complexity of Satisfiability Problems, STOC 1978](https://doi.org/10.1145/800133.804350).
- [Nishimura, Ragde, Szeider, Detecting Backdoor Sets with Respect to Horn and Binary Clauses, SAT 2004](https://ac.tuwien.ac.at/publication/detecting-backdoor-sets-with-respect-to-horn-and-binary-clauses/).
- [Gaspers et al., Backdoors into Heterogeneous Classes of SAT and CSP, AAAI 2014](https://doi.org/10.1609/aaai.v28i1.9111).
- [Samer and Szeider, A Fixed-Parameter Algorithm for #SAT with Parameter Incidence Treewidth (2006)](https://arxiv.org/abs/cs/0610174).
- Internal baseline: research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md and issue #324.
- Peer: research/agents/meta-solver-theorem/2026-11-23_0935_report.md; prior Decomposition Obstructions 09:25 report in PR #325.
