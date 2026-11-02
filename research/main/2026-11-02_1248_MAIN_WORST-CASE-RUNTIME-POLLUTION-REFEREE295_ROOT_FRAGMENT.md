<!-- LSPV5-REFEREE295-BEGIN -->
### REFEREE295 — B1/B2 separation by valid-input worst-case pollution

For fixed source-axiom Resolution+Weakening, every \(v\)-variable UNSAT CNF
has a blocking-clause refutation of cost at most \(2^{v+1}-1\).  A fixed total
correct decider that solves authenticated Tseitin formulas by GF(2), uses exact
fallback elsewhere, and deliberately waits \(2^{L^2}\) steps on dense valid
SAT sentinels has B1 false (easy Tseitin versus exponential Resolution) but B2
true (unrelated worst-case delay dominates the universal proof upper bound).
This proves B2 does not imply B1.  It does not attack B3, because the decider
is deliberately superpolynomial.  Adding XOR reasoning collapses the family,
so no representation-inclusive lower bound or P-versus-NP conclusion follows.
<!-- LSPV5-REFEREE295-END -->
