# BRANCHHIER37 / 2026-10-16 23:33Z

Status: P vs NP OPEN.

Conditional on P=NP, deterministic time hierarchy prevents uniformly fast faithful extraction of actual SAT guest queries chosen by arbitrary polynomial-time SAT deciders. For any r, choose a hard P-language L, let an exact decider A compute L(x) on an easily decodable satisfiable proper-3CNF carrier C(x), and then call its SAT guest on C(x) or a satisfiability-equivalent padded C(x). A faithful N^(r+o(1)) guest-query extractor reveals L(x) from clause count, contradicting time hierarchy.

Limitation: branch is extensionally erasable, so this excludes faithful A-trace recovery only; it does not exclude an extensional contractor. It also gives no SAT or space lower bound.

Audit: 510 carriers, 375 noncarriers, 1770 solver executions, 510 distinct actual-query pairs; independent MILP projected 76 SAT and 308 UNSAT queries. All passed.

Next: search for A-specific semantic-necessity quotient with cheap predecision acquisition, strict hereditary child size, and same-realization time-space charges. No claimed P vs NP proof.
END_BRANCHHIER37