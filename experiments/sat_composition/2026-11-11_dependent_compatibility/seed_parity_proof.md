# Bounded seed witnesses and a polynomial-workspace solver

Status: exact consequence of the closure-polynomial argument, implemented as an independently structured reference algorithm. No new universal polynomial SAT bound is asserted.

## Theorem

Let H be a Horn CNF on n Boolean variables and let Ax=b be a consistent affine system of rank d over F_2. If H AND (Ax=b) is satisfiable, it has a satisfying assignment of the form cl_H(S) for some set S of at most d variables. Here cl_H(S) is forward Horn closure of the positive seed S; a closure that violates a negative Horn clause is discarded.

## Proof

For every valid closed set K, let m_K be the Boolean function on models of H that is one exactly when the model contains K. These functions are linearly independent over F_2: their evaluation matrix on the closed model sets is the inclusion-zeta matrix, triangular with ones on the diagonal when sets are ordered by cardinality.

Every ordinary monomial on a variable set S is equal on Horn models to m_cl(S), or identically zero when the closure is inconsistent. Constants use cl_H(empty), which need not be empty. Multiplication sends closed supports K,L to cl_H(K union L), or zero for an inconsistent closure.

Multiply the d Boolean parity-satisfaction indicators of a row basis of Ax=b. Before closure reductions their product has degree at most d. Therefore every surviving normalized monomial has support cl_H(S) for some |S|<=d. The product is a nonzero function precisely when the instance is satisfiable, by independence of the closed-set basis. Choose a minimum-cardinality surviving support K. At the model K, its own monomial evaluates to one and every other surviving monomial evaluates to zero: a distinct set of at least the same cardinality cannot be contained in K. Thus K satisfies all parity equations and is cl_H(S) for a seed of size at most d.

The argument is an existence proof for a bounded seed. The seed solver does not construct or retain the indicator polynomial.

## Streaming algorithm and costs

Compute an affine row basis by Gaussian elimination. Enumerate every subset S of the n variables, in increasing cardinality, through size d. For each seed, recompute Horn closure from the input clauses and check the affine equations. Return the first valid witness, or UNSAT after complete exhaustion.

There are at most

$$
B(n,d)=\sum_{j=0}^{d}\binom{n}{j}
$$

attempts. Each closure and parity check is polynomial in the explicit source size. Therefore the time is polynomial(N) times B(n,d). The implementation uses repeated rule scans for its closure calculation, intentionally independent of the counter-based closure used in the polynomial engine.

Only the current seed and closure, the source, the affine row basis, and enumeration state are retained. There is no global table of previously visited seeds or closures. Workspace is polynomial even when d grows with the input. Storing all distinct closures for deduplication would destroy this particular workspace guarantee and is deliberately avoided.

The optional seed cap counts attempts before they begin. Exhausting the cap returns UNRESOLVED, never UNSAT. A contradiction found directly in the affine equations, or by the initial 2-SAT computation, can still return UNSAT without seed enumeration. Recorded closure_work counts antecedent-mask tests; it is not a complete bit-instruction ledger. The complexity proof charges the bit lengths and every remaining polynomial operation separately.

## 2-CNF version

Find one 2-SAT model a. Substitute x=a XOR y into the 2-CNF. Because y=0 satisfies it, every remaining nontrivial clause has at least one negative literal, so the translated formula is Horn. Transform each affine row to A y=b+A a. Apply the Horn seed algorithm and return x=a XOR y.

The row rank is unchanged by the translation. Thus every satisfiable 2-CNF-plus-affine instance has a witness a XOR cl(S), |S|<=d. The implementation reuses only the frozen engine's ordinary 2-SAT base-model path with no affine equations. Its seed search, closure evaluation, and affine row reduction are separate implementations.

For fixed d this is polynomial time; for growing d it is an XP bound and can be exponential. The existence of bounded seeds does not provide a polynomial procedure to identify a successful seed when d is unrestricted. P versus NP remains open.
