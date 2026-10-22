# SHRUNK-QUERY-ENVELOPE67 HANDOFF

Timestamp: 2026-10-22 15:48 KST

**P versus NP OPEN; P versus RP OPEN.**

For \(Q=N^{\alpha+o(1)}\) sequential calls of length \(N^{\beta+o(1)}\), non-decider time \(N^{\gamma+o(1)}\), and space floor \(N^{\delta+o(1)}\), a decider with exponents \((c,s)\) transforms to

\[
c'\le\max(\gamma,\alpha+\beta c)+o(1),
\qquad
s'\le\max(\delta,\beta s)+o(1).
\]

Strict time improvement requires \(\gamma<c\) and \(\alpha<(1-\beta)c\). The attracting fixed point is

\[
c_*=\max\left(\gamma,\frac{\alpha}{1-\beta}\right).
\]

For \((\alpha,\beta,\gamma,\delta)=(0.6,0.5,1.1,0.5)\), the limit is exactly \((6/5,1/2)\).

**ESTABLISHED:** exponent envelope, improvement frontier and fixed-point arithmetic.  
**CONDITIONAL:** iterating a genuine uniform all-input transformer reaches \(DTISP(N^{6/5+\varepsilon},N^{1/2+\varepsilon})\).  
**RETIRED as necessary for conditional iteration:** discovering the unknown starting exponent with a fastest-certified solver. An existence proof may choose finite depth after fixing the assumed polynomial decider.  
**OPEN:** the exact hereditary transformer with strict query shrinkage and full FLMV charges.

Audit: 121,781 checks, zero failures.

Next:

- :00 — ledger the best ordinary-KT target by \((\alpha,\beta,\gamma,\delta)\).
- :12 — publish hitting-list and original-coin evaluation exponents.
- :24 — build one all-input transformer meeting \((0.6,0.5,1.1,0.5)\).
- :36 — verifier-replacement stability for UNIVERSAL-SHIFT29.
- :48 — compose two explicit transformer levels and charge ancestor state.
