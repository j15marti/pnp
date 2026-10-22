# RESTRICTION-SHRINKAGE-BARRIER63 HANDOFF

Timestamp: 2026-10-22 11:48 KST

**P versus NP OPEN; P versus RP OPEN.**

For an \(M\)-clause CNF with maximum occurrence \(\Delta\), assigning \(r\) variables touches at most \(\Delta r\) clauses, so every direct restricted child retains at least \(M-\Delta r\) clauses.

Exhaustive self-reduction has the exact all-input relation

$$
SAT(F)=\bigvee_{\alpha\in\{0,1\}^r}SAT(F\!\upharpoonright\!\alpha)
$$

and restrictions compose hereditarily. But \(Q\le N^{0.6+o(1)}\) branches imply \(r\le(0.6+o(1))\log_2N\). On constant-occurrence formulas with \(M=\Theta(n)\), every child therefore has length \(N^{1-o(1)}\), not \(N^{0.5+o(1)}\). Tovey's occurrence-four NP-complete 3-SAT family makes the obstruction relevant to the full route.

This complements SELECTOR-VIRTUAL-CHILD62:

- clause selection: target shrinkage/local access succeed, exact label reconstruction fails;
- exhaustive restrictions: exact labels/heredity succeed, target shrinkage fails.

**ESTABLISHED:** counting bound, exact OR semantics, restriction heredity.  
**RETIRED:** polynomial exhaustive direct restriction as the target ARC contraction.  
**OPEN:** nonlocal parent-aware compatibility join with exact labels, virtual child access, bounded rounds, and matched FLMV charges.

AFFINE-PIN27 remains a restricted deterministic circuit algorithm. Polynomially many affine-control branches do not imply explicit child shrinkage; a growing control exponent is not a language lower bound.

Finite audit: 90 bounded-occurrence fixtures, 6,360 checks, 2,310 semantic branches, zero failures.

Next tests:

- :00 — compute the complete ordinary-KT LOW upper bound for selector and restriction targets.
- :12 — measure growing WRAPPER \(k,d,b\), direct bypass, and SAT-NO soundness.
- :24 — build or falsify a parent-aware exact compatibility join.
- :36 — certify complete original-coin affine controls only after source joins and full gate charges.
- :48 — reject any contractor that fails either bounded-occurrence shrinkage or exact joint-label reconstruction.
