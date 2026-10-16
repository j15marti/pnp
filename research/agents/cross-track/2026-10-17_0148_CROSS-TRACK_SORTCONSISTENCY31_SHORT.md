# SORTCONSISTENCY31 | 2026-10-17 01:48 KST

Cross-track status: SAT-hard, source-sign-dependent, fixed-unsigned-incidence proper 3-CNF is obtained by sorting occurrence records and checking adjacent address consistency. Arbitrary-decider lower bounds remain open.

Let r=3m, k=ceil(log2(n+1)), t=nextpow2(r), a=log2(t), Q=t*a*(a+1)/4. Pin the address and sign bits; sort (address, guessed value) records with a bitonic sorting network; enforce equal values on adjacent equal addresses and each original source clause's truth. This is satisfiable exactly when the source proper 3-CNF is satisfiable. Only literal signs on the source pin gadgets vary.

Exact comparator blocks: gates 12k-1, clauses 56k-8, variables 28k-9. Total target clauses:
C=Q*(56k-8)+4*(t*(k+1)+1)+(t-1)*(9k+4)+22m+5*(t+m-2).
Target bitlength is source length times polylogarithmic factors.

Clause lookup, occurrence degree, cumulative-degree prefix and inverse occurrence ranks have fixed block-arithmetic algorithms. Comparator degree totals are 3*(56k-8) before the final stage, and 3*(56k-8)-20k with endpoint corrections in the final stage.

Finite audit: 63 sources, 4,736 occurrence assignments, 92,272 local degrees, 92,272 cumulative prefixes, 677,260 inverse positions, 61 incidence comparisons and an UNSAT control. All matched. This does not demonstrate an arbitrary-decider contraction, proof-system transport, nonrelativizing WRAPPER operation, or same-input UWI obstruction.

Resource Contraction: fully charge virtual reads, materialization and recursion. Nonrelativizing Simulation: require a necessary post-release SAT event. Universal Obstruction: test source-aware same-input programs. Proof Transport: test complete exact-(2,2) compilation and calculus-specific retraction.

Sources read: GUARDCOVER1 and ROUTECERT1; CAUSALBRANCH16; SAMPLERGATE30; SEMDEG-FIREWALL1; previous XORBITONIC29, earlier JMV archive and primary literature.

P versus NP remains OPEN.
END_SORTCONSISTENCY31_0148_KST