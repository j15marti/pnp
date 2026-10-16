# ASSUME-RUP-TREE1, 2026-10-16 18:45 KST

Status: Restricted proof-model result. P versus NP remains open.

For an UNSAT CNF F, suppose a complete binary DPLL case tree uses verified unit-propagation conflicts at its leaves, and all globally learned clauses are RUP with chronological recorded reasons. Deletions must be validated against the active set. If U is the total number of propagations and B the number of internal branches, reverse unit propagation and bottom-up case discharge yield an ordinary Resolution refutation of F in at most U+B inferences. Missing pivots permit reusing the stronger child clause; temporary weakenings can be eliminated.

Finite audit: 82 UNSAT formulas; 772 independently replayed Resolution inferences; six hostile controls passed. Branch-local consequences are not automatically global clauses. RAT is not equivalent to RUP. Arbitrary SAT deciders are not obliged to emit this certificate.

Historical compiled Tseitin family: 36n variables, 48n clauses, and exponential Resolution size, hence exponential work for the declared proof-logging model. No arbitrary-decider lower bound follows.

Next: SCOPED-CDCL-EXPLAIN1 with explicit, typed preprocessing modules and resource accounting.

Local full report: 2026-10-16_1845_PROOF-TRANSPORT_ASSUME_RUP_TREE1.md
Source: Buss, Hoffmann, Johannsen (LMCS 2008), and Beame, Kautz, Sabharwal (JAIR 2004).
