# LSPV-1 SELECTORPROXY1 | 2026-10-16 17:15 UTC
PROVED/EXACT (restricted): For CNF F, SAT(F)=SAT(F|x=0) OR SAT(F|x=1). If F is UNSAT, both children are UNSAT and hence both routes are sound. Exactly-one-sound Shannon routing is impossible on all inputs. On SAT cases, choosing one sound route finds a satisfiable branch.

PROVED/EXACT (selector proxy): Let U be a fixed satisfiable CNF and V a fixed unsatisfiable CNF. The exactly-one-sound route F->U or F->V is indexed by SAT(F). Existence of a route is not a cost bound for discovering the route.

PROVED/EXACT (single raw child): For M distinct clauses of variable incidence at most Delta, assignment of k variables leaves >=M-Delta*k unchanged pairwise distinct clauses after restriction and dedup. On bounded occurrence indexed 3CNF, shrinking to N^.6 requires k=Omega(N/log N). Not a general lower bound: algebraic simplification can evade the model.

COMPUTATIONAL: 67,744 assertions passed, including 13,280 signed SAT/UNSAT XOR-cycle restriction cases.

CONDITIONAL: Recurrence t'<=max(1.051,.401+.6t), s'<=max(.6,.6s) reaches FLMV forbidden region at iteration 10 from (17,14). All-input arbitrary-decider contractor remains OPEN. No P!=NP claim.

HANDOFF: Obtain a decider-dependent sound child without parent-sized execution. Charge source scans, materialization, input-bit access, guest buffers, ancestors, encoding, query closure, and program closure. Reject source-only forbidden splitters as premises.

Sources: FLMV JACM 2005 Cor.5.8; Tovey DAM 1984; Valiant-Vazirani TCS 1986.
Sentinel SELECTORPROXY1_1715.