# CLAUSE-EXTREME-DUALITY1: User-directed S/U inversion experiment (2026-10-29 21:53 America/Los_Angeles)

**ACTIVE SCIENTIFIC PRIORITY.** The user asks to set each original signed occurrence `x_{i,j}` to its locally clause-SAT requirement, invert all values and see which clauses remain SAT; repeat starting from clause-UNSAT requirements. Cross-check these local requirements against a single globally consistent variable assignment, all TRUE, all FALSE and intermediate flips. **Do NOT resume equity.** Read [active issue #3](https://github.com/j15marti/pnp/issues/3). Existing five hourly agent tasks were updated; schedules and IDs retained. P versus NP OPEN.

## Exact semantics and sanity warning
For a proper 3-clause C_j and occurrence x_{i,j}, sign sigma_{ij}=+/-:
- S_j (strong local SAT) makes **each of its 3 literals TRUE**. This assigns x_i=1 for positive and x_i=0 for negative occurrences.
- U_j (local UNSAT) makes **each of its 3 literals FALSE**. This assigns x_i=0 for positive and x_i=1 for negative occurrences.
- Inverting all of S_j gives U_j, and vice versa.

An occurrence is NOT a separately assignable variable. If a source variable has both signs, independently setting every occurrence SAT gives contradictory local requirements and is not a genuine assignment. Also a SAT clause needs only ONE true literal, not 3. Independent local S_j then inversion leaves zero clauses SAT, a tautological observation; independent U_j then inversion makes every clause SAT, equally trivial. The useful question is which combinations of these clause-indexed requirements are globally feasible and what sound deductions follow.

## Exact four-mode clause-pair theorem
For distinct clauses C_j,C_k with no repeated variable within a clause:

| Local modes | Simultaneously realizable exactly when |
| --- | --- |
| S_j, S_k | no shared variable with OPPOSITE signs |
| U_j, U_k | no shared variable with OPPOSITE signs |
| S_j, U_k | no shared variable with the SAME sign |
| U_j, S_k | no shared variable with the SAME sign |

Proof: each occurrence and selected mode demands exactly one Boolean value. The only obstruction is two contradictory demands on the same source variable. The criterion extends from clause pairs to any collection of clauses labelled S/U, because their extreme requirements are unary.

**Derived forced-middle lemma.** If two clauses share both a same-polarity and opposite-polarity variable, then NONE of SS,SU,US,UU is possible. Therefore, under every complete assignment, at least one of those two clauses has 1 or 2 true literals, and remains SAT under complete inversion. Example: C1=(x1 OR x2 OR x3), C2=(x1 OR NOT x2 OR x4). Both clauses can still be satisfied: 1100 makes the true-literal counts 2 and 1; 0011 gives 1 and 2. No UNSAT conclusion follows.

Let H be the graph of clause pairs with BOTH shared-polarity types. The middle clauses (1 or 2 true literals) form a vertex cover of H in EVERY assignment. Therefore number remaining SAT after inversion is at least tau(H), at least the matching number. This is a universal invariant, NOT on its own a solver or meaningful exclusion of full assignments. For the eight 3-variable sign-pattern clauses, H=K8 minus four opposite-pattern edges, tau(H)=6, and all eight assignments have exactly six middle clauses, one entirely true and one entirely false. This is tight. Compare with established sign-sensitive *conflict graphs* and *hitting clause sets* (Kullmann), without claiming novelty.

## Genuine full-assignment experiment and deductions
For a globally consistent assignment a, t_j(a)=number of true literals in C_j. Then t_j(~a)=3-t_j(a). Let N_r(a)=#{clauses with t_j(a)=r}. N_r(~a)=N_(3-r)(a), F(a)=SAT iff N_0(a)=0, and F(~a)=SAT iff N_3(a)=0. If 0^n falsifies a clause it is all-positive; if 1^n falsifies a clause it is all-negative. All mixed-polarity clauses survive both endpoints. Failure at both endpoints is **not** UNSAT; (x OR y OR z) AND (NOT x OR NOT y OR NOT z) fails at 000 and 111 but is SAT at 001 and 110. This exact pair is a NAE constraint.

For flip set S, t_j(a XOR S)=t_j(a)+#(formerly false literals flipped)-#(formerly true literals flipped). An originally false clause demands at least one repair flip, but those flips may break other clauses. Track the actual source occurrence indices and full proof/trail through each flip. For opposite occurrences (x OR A),(NOT x OR B), derive the sound resolvent A OR B; falsifying its non-tautological literals excludes all extensions of that partial assignment, but this is standard resolution. If choose one satisfying literal occurrence per source clause, F SAT iff some such choices impose no opposing values on a shared variable; potentially exponential to find, so not yet a shortcut.

## Verified finite audit
Locally created `sat_extreme_clause_inversion_audit.py` and `sat_extreme_clause_inversion_results.json` in originating conversation (not yet published as repository code: reproduce independently). Python audit exhaustively verified pair-mode predictions against merged demand maps and full assignment enumeration: 496 pairs on four variables and 3,160 pairs on five variables. Also checked 3-clause mode families, 256 formula subsets on three variables (255 SAT, one UNSAT), 160 deterministic random 3-CNFs, all their full inversions, and the mixed graph. **71,840 counted condition checks, zero errors.** This is finite confirmation of separately proved elementary equivalences, not asymptotic algorithmic evidence.

## Agent mandates
- Formal Lead: prove complete joint-mode feasibility and investigate restrictions which genuinely force SAT solutions or rule out partial cubes.
- Circuit/Reduction: source-preserving S/U occurrence matrix, actual flip traces, reason/proof DAG and sound learned clauses; recognize NAE, XOR, 2SAT/Horn.
- Adaptive Certificate: compare S/U local extremes, globally coherent 0^n/1^n, Gray/Hamming partial flips and repair paths; SAT/UNSAT separately.
- Resource Auditor: charge all generation, polarity scans, pair/multi-clause compatibility, failed paths, proof checking and simultaneous storage.
- Red Team: expose conflicts between incompatible extreme targets and actual SAT, check full inversions and false deductions, test against affine/parity, Tseitin, dense random and exact-(2,2) controls.

Target a nontrivial **proved** inference or precisely scoped tractable family, not merely diagnostic counts of clauses that remain SAT after inversion. Record true branch elimination rather than number of impossible full assignments. Preserve all earlier verified work and schedule.

Literature:
- O. Kullmann, *Constraint Satisfaction Problems in Clausal Form II: Minimal Unsatisfiability and Conflict Structure* (2011), https://doi.org/10.3233/FI-2011-429
- O. Kullmann, *Sign-sensitive Graph Representations of CNFs: Conflict Graphs and Resolution Graphs* (2006), https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00009393/pcc06_NKE.pdf
- Marques-Silva et al., *Conflict-Driven Clause Learning SAT Solvers*, https://collaborate.princeton.edu/en/publications/chapter-4-conflict-driven-clause-learning-sat-solvers/
