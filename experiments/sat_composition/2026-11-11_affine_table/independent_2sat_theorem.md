# Polynomial terminal rule for independent affine 2-SAT coordinates

Status: PROVED for the stated sufficient condition. Implemented in `independent_2sat.py`. No all-input polynomial SAT bound is claimed.

## Statement

Suppose an explicitly represented residual is a conjunction of factors

$$
F(x)=\bigwedge_{i=1}^{m}\bigl([A_i x=b_i]\land f_i(L_i x)\bigr),
$$

where each table f_i has at most two input coordinates. Stack all affine systems into A x=b. If inconsistent, F is UNSAT. Otherwise put the global system in reduced row echelon form and reduce every row of every L_i modulo its equations. This writes each table argument as either a constant or a reduced linear form plus a known constant shift.

Identify equal nonzero reduced forms, retaining the separate shifts of their uses. Let Q be the matrix whose rows are the distinct nonzero reduced forms. Assume

$$
\operatorname{rank}(Q)=\text{number of rows of }Q.
$$

Then F is decidable in polynomial time, even when Q has arbitrarily many rows. A satisfying assignment, if one exists, can also be found in polynomial time.

## Proof

The reduced forms involve only free columns of the global affine core. Their independence means that as the free variables vary, the vector q=Qx ranges over every Boolean vector of the relevant dimension. Thus these coordinate values are jointly surjective on the affine solution set. Known constant offsets in the original forms do not change this statement.

Each factor is a Boolean condition on at most two of these independent coordinate values, possibly repeated or complemented. Enumerate its at most four local assignments. For every forbidden local assignment, add the one clause excluding that assignment. The clause has at most two literals. A forbidden constant assignment gives an empty clause. This translates the factor conjunction into a 2-CNF of at most four clauses per factor.

The 2-CNF is satisfiable exactly when F is satisfiable. The forward implication follows by mapping any original model through Q. The reverse implication follows from joint surjectivity: any satisfying coordinate vector lifts to an x satisfying A x=b and all coordinate equations, hence all original factors. Strongly connected components of the implication graph decide 2-SAT in linear time in that graph's size. Gaussian elimination constructs the lift.

All preprocessing is polynomial matrix work. No table on the full coordinate set is built. The potentially large number of distinct coordinates therefore does not appear as an exponent.

## Scope

This terminal rule covers ordinary 2-SAT by taking A empty and Q to consist of individual variable coordinates. It also covers any invertible affine change of those coordinates, consistent affine cores, repeated forms, complements induced by the core, and constant coordinates.

It does not cover every factor network whose local tables have width two. For example, the distinct coordinates x, y, and x XOR y are dependent. Treating their values as independent can produce spurious models. The implementation returns UNRESOLVED on that condition and does not infer SAT from the relaxation.

The implemented checks include a dependent UNSAT control in which each factor is already intrinsically width two. It therefore cannot be dismissed as an artifact of failing to extract unary affine constraints.

The current test returns UNRESOLVED immediately when dependencies remain, as requested. A sound optional extension could still build the relaxed 2-CNF and accept an UNSAT result: dropping dependencies only enlarges the set of potential coordinate assignments. A SAT answer to that relaxation would continue to mean UNRESOLVED until the dependencies were enforced.

## Verification

`independent_2sat_small.json` records exhaustive two-variable 2-CNF cases, every pair of two-coordinate Boolean tables, randomized affine-core cases, and dependent controls. Every resolved answer is compared against independent enumeration of the original variable assignments. SAT outputs additionally carry witnesses checked against the original factors.

`independent_2sat_wide.json` records four 1000-coordinate controls: ordinary 2-SAT and an invertible affine-coordinate version, each with a SAT chain and an UNSAT chain. These controls have 1000 independent coordinates but at most two coordinates per factor. They demonstrate that this rule does not require a logarithmic global coordinate bound. They are finite verification, not evidence for a universal polynomial algorithm.
