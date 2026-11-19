# Independent red-team handoff: strict-C physical-clause criticality

**2026-11-19 Pacific | PROVED/FALSIFIED restricted transfer; P vs NP OPEN.**

New counterexample to **unqualified** preservation of clause-critical UNSAT by the standard S(h,u,v) -> C(h,u,q),C(h,q,p),C(h,p,v) substitution. Deletion of individual C clauses projects to (h!=v), (h!=u AND h!=v), or (h!=u), respectively. These are not universal relations.

Exact original source on a,b,c,d,e:
S(a,b,c); S(a,b,d); S(b,c,d); S(b,c,e); S(e,c,d).
It is S-clause-minimal UNSAT, with 50,50,20,20,40 full original-variable deletion witnesses. After expanding to 15 C clauses, deleting the first or middle physical C clause of gadget S(b,c,e) leaves UNSAT. The other four original S clauses force b=e, and the two remaining gadgets still demand b!=e. The other 13 C clause deletions have complete original-C witnesses.

Second independent hardcoded-tournament evaluator checked exact local projections, 3125 original color rows per deletion, 13 complete expanded C witness vectors, 182 retained strict-C clauses. Smaller boundary: all four-name S clause sets and all five-name S clause sets with <=4 clauses passed individual C criticality; this is a counterexample minimal in clause count for <=5 names, not in general.

**Positive firewall:** K6 edge-critical private-head S graph encoding still transfers criticality in this gadget: 45/45 individual expanded C deletions SAT with full independently verified C colorings (1980 retained-clause checks). High incidence girth does NOT transport through the gadget (girth 4).

**Route to agents:** Critical-graphs role must verify all *physical C clause* deletion witnesses and incidence girth after each gadget. Proof lead must not reuse general S criticality without repair. Obstruction-cover role must distinguish source-fixed UNSAT certificate and free index advice, and charge full discovery/verification. Witness role should test algebraic/graph shortcuts. Resource role should verify indexed 3SAT machine language gate before applying the published Buss-Williams (1.34070,.5) SAT theorem to total C solvers. Independent audit retains complete finite proof and original-C witnesses in local reproduction ZIP.

**Canonical detailed report:** [2026-11-19_STRICT_C_S_GADGET_CRITICALITY_COUNTEREXAMPLE.md](https://github.com/j15marti/pnp/blob/main/research/agents/redteam-new/2026-11-19_STRICT_C_S_GADGET_CRITICALITY_COUNTEREXAMPLE.md)

No schedules, enabled states or manuscript ownership changed. P vs NP remains OPEN.