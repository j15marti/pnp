# Independent LPS p73 Cayley girth replay | 2026-11-19
Research companion to [critical-girth report](../agents/critical-graphs/2026-11-19_LPS73_GIRTH_SOURCE_K6_LIFT_FALSIFIER.md). **COMPUTATIONALLY VERIFIED exact local girth; global Ramanujan spectral theorem still external; critical extraction OPEN.**

The first finite checker used explicit 2x2 projective matrices over F_q. A separate Python standard-library verifier now uses independent Hamilton quaternion multiplication and projective quaternion normalization. Both enumerate all 74 LPS p=73 generators and 5,402 non-backtracking two-step words, check that their endpoints are distinct and not adjacent to identity, check all 5-cycle candidate adjacencies where needed, then independently validate a shortest explicit cycle.

* q=89: quaternion checker certifies girth exactly 5 with a new 5-cycle; 5,402 distinct two-step endpoints. Thus direct strict-C private-head incidence girth exactly 10.
* q=257: certifies girth exactly 6; 5,402 distinct two-step endpoints and **399,748** five-cycle candidate adjacencies eliminated; produces a verified 6-cycle. Thus direct strict-C incidence girth exactly 12.
* The independent quaternion checker found its q257 6-cycle after 12,038 eligible 3-step evaluations, while the matrix checker found a different one after 6,654. They agree on girths, not on ordering-specific counters.

The executable script and its raw JSON witness ledger are in the local package **T5C_LPS73_Critical_Girth_Audit_20261119.zip** together with all earlier matrix and K6 witness tests, the complete mathematical report, and SHA-256 manifest. No random seeds. These are finite local checks, NOT a materialization of the 13,040,280- or 314,025,216-clause unsatisfiable inputs, nor independently verified global spectrum or clause-minimal critical cores.

**Required next step:** graph-coloring-guided extraction of an actual high-incidence-girth 6-critical core with all deletion witnesses, fully charged source, candidate search, child SAT/UNSAT calls, replay and output. P vs NP remains OPEN.