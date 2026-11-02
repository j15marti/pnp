<!-- LSPV5-REFEREE296-BEGIN -->
### REFEREE296 — unchanged-calculus relativization firewall

Fix an ordinary calculus \(R\) whose worst-case minimum refutation cost is
superpolynomial.  No B3 proof can be fully solver-relativizing while leaving
that \(R\) unchanged: Baker--Gill--Solovay give an oracle \(O\) with
\(\mathrm P^O=\mathrm{NP}^O\), so ordinary SAT is in \(\mathrm P^O\), whereas
ordinary \(R\)-derivations and \(\overline W_R\) are unchanged.  This is a
**PROVED/EXACT METHOD BARRIER**, not a counterexample to ordinary B3.

Independently, if the same ordinary \(R\) is size-optimal among ordinary
Cook--Reckhow UNSAT proof systems and node cost is polynomially dominated by
proof length, then a unary-clock verifier for each fixed total correct
ordinary decider proves B1.  This is a **PROVED/CONDITIONAL SUFFICIENT
BRIDGE**.  It escapes the firewall because an oracle decider yields an oracle
verifier, outside ordinary size optimality.  No mixed-calculus lower bound or
P-versus-NP conclusion follows; B1, global B2 and B3 remain OPEN for the
desired fixed representation-inclusive calculus.
<!-- LSPV5-REFEREE296-END -->

